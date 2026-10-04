import json, sqlite3, sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lead_pipeline import process, write_queue_csv
from staging_crm import upsert_ready_queue, init_staging
from dispatch_gate import evaluate_dispatch, queue_provider_request
from provider_adapter import MockCallingProvider, dispatch_pending, sign_webhook, ingest_webhook

RAW = ROOT / 'fixtures/raw_leads.csv'
SUP = ROOT / 'fixtures/suppression.csv'
SECRET = 'phase3-test-secret'
CAMPAIGN = {'campaign_id':'pilot_ca_001','status':'PILOT','brain_version':'brain-v1.3','script_version':'script-v1','provider_name':'mock-provider','caller_id_approved':True,'callback_ready':True,'window_start':'09:00','window_end':'17:00'}


def setup_pending(tmp_path):
    db = tmp_path / 'phase3.db'
    decisions = process(RAW, SUP, db, today=date(2026,10,4))
    out = tmp_path / 'queues'; write_queue_csv(decisions, out)
    upsert_ready_queue(db, out/'campaign_ready.csv', CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = init_staging(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    gate = evaluate_dispatch(c, lead_id, CAMPAIGN, datetime(2026,10,4,17,0,tzinfo=timezone.utc), [], provider_ready=True, local_minute_override=10*60)
    queued = queue_provider_request(c, lead_id, CAMPAIGN, gate)
    assert queued['status'] == 'PENDING'
    return db, c, lead_id


def headers_for(event_id, body, at):
    timestamp = str(int(at.timestamp()))
    return {'X-Provider-Timestamp': timestamp, 'X-Provider-Signature': sign_webhook(SECRET, timestamp, body), 'X-Provider-Event-Id': event_id}


def event(event_id, event_type, provider_call_id, extra=None):
    data = {'provider_call_id': provider_call_id}
    if extra: data.update(extra)
    return json.dumps({'id':event_id,'type':event_type,'data':data}, sort_keys=True)


def test_outbound_dispatch_is_idempotent_and_audited(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider()
    first = dispatch_pending(c, provider)
    second = dispatch_pending(c, provider)
    assert len(first) == 1 and len(second) == 0
    assert c.execute('select count(*) from call_sessions').fetchone()[0] == 1
    assert c.execute('select status from provider_outbox').fetchone()[0] == 'SENT'
    assert c.execute('select lifecycle_status from crm_leads where lead_id=?',(lead_id,)).fetchone()[0] == 'DISPATCHED'
    assert c.execute('select count(*) from audit_events where event_type="provider.call.create"').fetchone()[0] == 1
    c.close()


def test_valid_signed_webhooks_transition_call_and_replay_is_safe(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    pcid = sent['provider_call_id']; at = datetime(2026,10,4,17,1,tzinfo=timezone.utc)
    for eid, typ in [('evt_start','call.started'),('evt_answer','call.answered'),('evt_done','call.completed')]:
        body = event(eid, typ, pcid); result = ingest_webhook(c, 'mock-provider', SECRET, headers_for(eid,body,at), body, at)
        assert result['accepted'] and result['processed']
        at += timedelta(seconds=1)
    duplicate_body = event('evt_answer','call.answered',pcid)
    duplicate = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_answer',duplicate_body,at), duplicate_body, at)
    assert duplicate['duplicate'] is True
    assert c.execute('select status from call_sessions').fetchone()[0] == 'COMPLETED'
    assert c.execute('select count(*) from call_event_history').fetchone()[0] == 3
    assert c.execute('select count(*) from provider_webhook_events').fetchone()[0] == 3
    assert c.execute('select count(*) from audit_events where event_type="provider.webhook.process"').fetchone()[0] == 3
    c.close()


def test_invalid_signature_is_rejected_without_side_effect(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    at = datetime(2026,10,4,17,1,tzinfo=timezone.utc); body = event('evt_bad','call.started',sent['provider_call_id'])
    headers = headers_for('evt_bad', body, at); headers['X-Provider-Signature'] = 'v1=bad'
    result = ingest_webhook(c, 'mock-provider', SECRET, headers, body, at)
    assert result['accepted'] is False and result['reason_code'] == 'INVALID_SIGNATURE'
    assert c.execute('select status from call_sessions').fetchone()[0] == 'CREATED'
    assert c.execute('select processing_status from provider_webhook_events').fetchone()[0] == 'REJECTED'
    c.close()


def test_stale_signature_is_rejected(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    received = datetime(2026,10,4,17,10,tzinfo=timezone.utc); signed_at = received - timedelta(minutes=10)
    body = event('evt_stale','call.started',sent['provider_call_id'])
    result = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_stale',body,signed_at), body, received)
    assert result['accepted'] is False and result['reason_code'] == 'STALE_OR_FUTURE_TIMESTAMP'
    c.close()


def test_unknown_call_and_out_of_order_event_go_to_reconciliation(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    at = datetime(2026,10,4,17,1,tzinfo=timezone.utc); body = event('evt_unknown','call.answered','pcall_missing')
    result = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_unknown',body,at), body, at)
    assert result['status'] == 'RECONCILIATION'
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    body2 = event('evt_out_of_order','call.completed',sent['provider_call_id'])
    result2 = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_out_of_order',body2,at), body2, at)
    assert result2['status'] == 'RECONCILIATION'
    assert c.execute('select count(*) from reconciliation_queue').fetchone()[0] == 2
    c.close()


def test_opt_out_is_terminal_and_blocks_future_dispatch_state(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    at = datetime(2026,10,4,17,1,tzinfo=timezone.utc); body = event('evt_optout','call.opt_out',sent['provider_call_id'], {'opt_out': True})
    result = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_optout',body,at), body, at)
    assert result['status'] == 'OPTED_OUT'
    assert c.execute('select lifecycle_status from crm_leads where lead_id=?',(lead_id,)).fetchone()[0] == 'DISPATCH_BLOCKED'
    assert c.execute('select status from call_sessions').fetchone()[0] == 'OPTED_OUT'
    c.close()


def test_invalidly_signed_replay_is_rejected(tmp_path):
    db, c, lead_id = setup_pending(tmp_path)
    provider = MockCallingProvider(); sent = dispatch_pending(c, provider)[0]
    at = datetime(2026,10,4,17,1,tzinfo=timezone.utc); body = event('evt_replay_sig','call.started',sent['provider_call_id'])
    good = ingest_webhook(c, 'mock-provider', SECRET, headers_for('evt_replay_sig',body,at), body, at)
    assert good['processed'] is True
    bad_headers = headers_for('evt_replay_sig',body,at); bad_headers['X-Provider-Signature'] = 'v1=bad'
    bad = ingest_webhook(c, 'mock-provider', SECRET, bad_headers, body, at)
    assert bad['accepted'] is False and bad['reason_code'] == 'INVALID_SIGNATURE'
    assert c.execute('select count(*) from call_event_history').fetchone()[0] == 1
    c.close()
