import sqlite3, sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lead_pipeline import process, write_queue_csv
from staging_crm import upsert_ready_queue, init_staging
from dispatch_gate import evaluate_dispatch, queue_provider_request

RAW = ROOT / 'fixtures/raw_leads.csv'
SUP = ROOT / 'fixtures/suppression.csv'

CAMPAIGN = {
    'campaign_id': 'pilot_ca_001', 'status': 'PILOT', 'brain_version': 'brain-v1.3',
    'script_version': 'script-v1', 'provider_name': 'test-provider',
    'caller_id_approved': True, 'callback_ready': True,
    'window_start': '09:00', 'window_end': '17:00',
}

def setup(tmp_path):
    db = tmp_path / 'phase2.db'
    decisions = process(RAW, SUP, db, today=date(2026,10,4))
    out = tmp_path / 'queues'; write_queue_csv(decisions, out)
    return db, out / 'campaign_ready.csv'

def test_idempotent_ready_upsert_and_duplicate_prevention(tmp_path):
    db, ready = setup(tmp_path)
    first = upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    second = upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    assert len(first) == 4
    assert sum(not x['replayed'] for x in first) == 2  # one canonical row per account
    assert sum(x['replayed'] for x in first) == 2     # duplicate source rows replay in-batch
    assert all(x['replayed'] for x in second)
    c = sqlite3.connect(db)
    assert c.execute('select count(*) from crm_leads').fetchone()[0] == 2
    assert c.execute('select count(*) from crm_accounts').fetchone()[0] == 2
    assert c.execute('select count(*) from crm_contacts').fetchone()[0] == 2
    assert c.execute('select count(*) from crm_sync_events').fetchone()[0] == 2
    c.close()

def test_true_payload_mutation_is_rejected(tmp_path):
    db, ready = setup(tmp_path)
    upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = sqlite3.connect(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    c.execute('update canonical_leads set company_name=? where lead_id=?', ('MUTATED COMPANY', lead_id)); c.commit(); c.close()
    try:
        upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    except ValueError as e:
        assert 'idempotency conflict' in str(e)
    else:
        raise AssertionError('expected idempotency conflict')

def test_dispatch_gate_allows_only_when_all_checks_pass(tmp_path):
    db, ready = setup(tmp_path)
    upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = init_staging(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    result = evaluate_dispatch(c, lead_id, CAMPAIGN, datetime(2026,10,4,17,0,tzinfo=timezone.utc), [], provider_ready=True, local_minute_override=10*60)
    assert result['allowed'] is True
    assert result['reason_code'] == 'ALLOW_DISPATCH'
    c.close()

def test_dispatch_gate_blocks_provider_when_provider_not_ready(tmp_path):
    db, ready = setup(tmp_path)
    upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = init_staging(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    result = evaluate_dispatch(c, lead_id, CAMPAIGN, datetime(2026,10,4,17,0,tzinfo=timezone.utc), [], provider_ready=False, local_minute_override=10*60)
    queued = queue_provider_request(c, lead_id, CAMPAIGN, result)
    assert result['allowed'] is False
    assert result['reason_code'] == 'PROVIDER_READY'
    assert queued['status'] == 'BLOCKED'
    assert c.execute('select count(*) from provider_outbox where status="BLOCKED"').fetchone()[0] == 1
    c.close()

def test_dispatch_gate_blocks_outside_local_window(tmp_path):
    db, ready = setup(tmp_path)
    upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = init_staging(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    result = evaluate_dispatch(c, lead_id, CAMPAIGN, datetime(2026,10,4,17,0,tzinfo=timezone.utc), [], provider_ready=True, local_minute_override=8*60)
    assert result['allowed'] is False
    assert result['reason_code'] == 'LOCAL_WINDOW'
    c.close()


def test_allowed_provider_outbox_is_pending_and_replay_safe(tmp_path):
    db, ready = setup(tmp_path)
    upsert_ready_queue(db, ready, CAMPAIGN['campaign_id'], CAMPAIGN['brain_version'], 'policy-v1')
    c = init_staging(db)
    lead_id = c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]
    result = evaluate_dispatch(c, lead_id, CAMPAIGN, datetime(2026,10,4,17,0,tzinfo=timezone.utc), [], provider_ready=True, local_minute_override=10*60)
    first = queue_provider_request(c, lead_id, CAMPAIGN, result)
    second = queue_provider_request(c, lead_id, CAMPAIGN, result)
    assert first['status'] == 'PENDING' and not first['replayed']
    assert second['status'] == 'PENDING' and second['replayed']
    assert c.execute('select count(*) from provider_outbox where status="PENDING"').fetchone()[0] == 1
    assert c.execute('select count(*) from dispatch_decisions').fetchone()[0] == 1
    c.close()
