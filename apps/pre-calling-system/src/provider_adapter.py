#!/usr/bin/env python3
"""Provider-neutral Phase 3 adapter harness. Network transport is intentionally absent."""
from __future__ import annotations
import hashlib, hmac, json, sqlite3
from datetime import datetime, timezone
from typing import Any
from staging_crm import now_utc
from provider_interface import ProviderRequest, ProviderResponse
from crm_status_sync import sync_call_status

MAX_WEBHOOK_SKEW_SECONDS = 300
TERMINAL = {'COMPLETED', 'FAILED', 'OPTED_OUT'}
TRANSITIONS = {
    'call.started': {'CREATED': 'RINGING'},
    'call.answered': {'CREATED': 'ANSWERED', 'RINGING': 'ANSWERED'},
    'call.completed': {'ANSWERED': 'COMPLETED', 'RINGING': 'COMPLETED'},
    'call.failed': {'CREATED': 'FAILED', 'RINGING': 'FAILED', 'ANSWERED': 'FAILED'},
    'call.opt_out': {'CREATED': 'OPTED_OUT', 'RINGING': 'OPTED_OUT', 'ANSWERED': 'OPTED_OUT'},
}

class MockCallingProvider:
    name = 'mock-provider'
    def __init__(self):
        self.calls = {}
        self.counter = 0
    def create_call(self, request: ProviderRequest) -> ProviderResponse:
        if request.provider_idempotency_key in self.calls:
            return self.calls[request.provider_idempotency_key]
        self.counter += 1
        response = ProviderResponse(request.provider_idempotency_key, f'pcall_{self.counter}', 'accepted')
        self.calls[request.provider_idempotency_key] = response
        return response

def sign_webhook(secret: str, timestamp: str, body: str) -> str:
    digest = hmac.new(secret.encode(), f'{timestamp}.{body}'.encode(), hashlib.sha256).hexdigest()
    return 'v1=' + digest

def verify_webhook_signature(secret: str, timestamp: str, body: str, signature: str, received_at: datetime, max_skew: int = MAX_WEBHOOK_SKEW_SECONDS) -> tuple[bool, str]:
    try:
        event_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
        skew = abs((received_at - event_time).total_seconds())
    except (ValueError, TypeError, OverflowError):
        return False, 'INVALID_TIMESTAMP'
    if skew > max_skew:
        return False, 'STALE_OR_FUTURE_TIMESTAMP'
    expected = sign_webhook(secret, timestamp, body)
    if not hmac.compare_digest(expected, signature or ''):
        return False, 'INVALID_SIGNATURE'
    return True, 'VERIFIED'

def audit(conn, event_type: str, actor: str, outcome: str, metadata: dict[str, Any], lead_id: str | None = None, call_id: str | None = None, idempotency_key: str | None = None):
    audit_id = 'audit_' + hashlib.sha256((event_type + '|' + (idempotency_key or '') + '|' + json.dumps(metadata, sort_keys=True)).encode()).hexdigest()[:24]
    conn.execute('INSERT OR IGNORE INTO audit_events VALUES(?,?,?,?,?,?,?,?,?)', (audit_id, event_type, actor, lead_id, call_id, idempotency_key, outcome, json.dumps(metadata, sort_keys=True), now_utc()))
    return audit_id

def dispatch_pending(conn, provider: MockCallingProvider, actor: str = 'phase3-adapter') -> list[dict]:
    rows = conn.execute('SELECT provider_idempotency_key,lead_id,campaign_id,provider_name,request_json,status FROM provider_outbox WHERE status="PENDING" ORDER BY created_at_utc').fetchall()
    results = []
    for key, lead_id, campaign_id, provider_name, request_json, status in rows:
        request_data = json.loads(request_json)
        request = ProviderRequest(key, request_data['lead_id'], request_data['campaign_id'], request_data['brain_version'], request_data['script_version'], request_data['policy_version'])
        response = provider.create_call(request)
        call_id = 'call_' + hashlib.sha256(response.provider_call_id.encode()).hexdigest()[:16]
        ts = now_utc()
        prior_session = conn.execute('SELECT call_id FROM call_sessions WHERE provider_call_id=?', (response.provider_call_id,)).fetchone()
        if not prior_session:
            conn.execute('INSERT INTO call_sessions VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (call_id, lead_id, campaign_id, provider_name, response.provider_call_id, 'CREATED', None, None, None, None, ts, ts))
            sync_call_status(conn, 'provider.call.created:'+key, call_id, lead_id, 'CREATED', {'provider_call_id': response.provider_call_id, 'provider_idempotency_key': key})
        conn.execute('UPDATE provider_outbox SET status="SENT",response_json=?,updated_at_utc=? WHERE provider_idempotency_key=? AND status="PENDING"', (json.dumps({'provider_call_id': response.provider_call_id, 'status': response.status}, sort_keys=True), ts, key))
        conn.execute('UPDATE crm_leads SET lifecycle_status="DISPATCHED",updated_at_utc=? WHERE lead_id=? AND lifecycle_status="ELIGIBLE_PENDING_DISPATCH"', (ts, lead_id))
        audit(conn, 'provider.call.create', actor, 'SENT', {'provider_name':provider_name,'provider_call_id':response.provider_call_id}, lead_id, call_id, key)
        conn.commit()
        results.append({'lead_id':lead_id,'call_id':call_id,'provider_call_id':response.provider_call_id,'status':'SENT','idempotency_key':key})
    return results

def _event_id(payload: dict, headers: dict[str, str], body: str) -> str:
    return headers.get('X-Provider-Event-Id') or payload.get('id') or 'body_' + hashlib.sha256(body.encode()).hexdigest()[:24]

def ingest_webhook(conn, provider_name: str, secret: str, headers: dict[str, str], body: str, received_at: datetime | None = None, actor: str = 'provider-webhook') -> dict:
    received_at = received_at or datetime.now(timezone.utc)
    timestamp = headers.get('X-Provider-Timestamp', '')
    signature = headers.get('X-Provider-Signature', '')
    event_id_hint = headers.get('X-Provider-Event-Id')
    try:
        payload = json.loads(body)
        event_id = _event_id(payload, headers, body)
    except json.JSONDecodeError:
        event_id = event_id_hint or 'invalid_' + hashlib.sha256(body.encode()).hexdigest()[:24]
        ok, reason = False, 'INVALID_JSON'
        payload = {}
    else:
        ok, reason = verify_webhook_signature(secret, timestamp, body, signature, received_at)
    prior = conn.execute('SELECT processing_status,result_json FROM provider_webhook_events WHERE provider_event_id=?', (event_id,)).fetchone()
    if prior and not ok:
        audit(conn, 'provider.webhook.reject', actor, reason, {'event_id':event_id,'duplicate_of_prior':True}, idempotency_key='webhook-reject:'+event_id+':'+reason)
        conn.commit()
        return {'event_id':event_id,'accepted':False,'reason_code':reason,'duplicate':True}
    if prior:
        result = json.loads(prior[1] or '{}')
        result.update({'duplicate': True, 'event_id': event_id})
        audit(conn, 'provider.webhook.duplicate', actor, 'NO_SIDE_EFFECT', {'event_id':event_id}, idempotency_key='webhook:'+event_id)
        conn.commit()
        return result
    status = 'RECEIVED' if ok else 'REJECTED'
    event_type = payload.get('type') if ok else None
    conn.execute('INSERT INTO provider_webhook_events VALUES(?,?,?,?,?,?,?,?,?,?,?)', (event_id, provider_name, event_type, timestamp, signature, int(ok), body, status, json.dumps({'reason':reason}, sort_keys=True), received_at.isoformat(), None))
    if not ok:
        audit(conn, 'provider.webhook.reject', actor, reason, {'event_id':event_id}, idempotency_key='webhook:'+event_id)
        conn.commit()
        return {'event_id':event_id,'accepted':False,'reason_code':reason,'duplicate':False}
    data = payload.get('data') or {}
    provider_call_id = data.get('provider_call_id')
    session = conn.execute('SELECT call_id,lead_id,status FROM call_sessions WHERE provider_call_id=?', (provider_call_id,)).fetchone()
    if not session:
        status = 'RECONCILIATION'
        reason = 'CALL_SESSION_NOT_FOUND'
        recon_id = 'recon_' + hashlib.sha256(event_id.encode()).hexdigest()[:24]
        conn.execute('UPDATE provider_webhook_events SET processing_status=?,result_json=? WHERE provider_event_id=?', (status, json.dumps({'reason_code':reason}, sort_keys=True), event_id))
        conn.execute('INSERT OR IGNORE INTO reconciliation_queue VALUES(?,?,?,?,?,?,?,?)', (recon_id,event_id,provider_name,reason,'OPEN',body,received_at.isoformat(),None))
        audit(conn, 'provider.webhook.reconcile', actor, reason, {'event_id':event_id,'provider_call_id':provider_call_id}, idempotency_key='webhook:'+event_id)
        conn.commit()
        return {'event_id':event_id,'accepted':True,'processed':False,'status':status,'reason_code':reason,'duplicate':False}
    call_id, lead_id, prior_status = session
    next_status = TRANSITIONS.get(event_type, {}).get(prior_status)
    if not next_status or prior_status in TERMINAL:
        reason = 'OUT_OF_ORDER_OR_ILLEGAL_TRANSITION'
        recon_id = 'recon_' + hashlib.sha256(event_id.encode()).hexdigest()[:24]
        conn.execute('UPDATE provider_webhook_events SET processing_status=?,result_json=? WHERE provider_event_id=?', ('RECONCILIATION', json.dumps({'reason_code':reason,'prior_status':prior_status}, sort_keys=True), event_id))
        conn.execute('INSERT OR IGNORE INTO reconciliation_queue VALUES(?,?,?,?,?,?,?,?)', (recon_id,event_id,provider_name,reason,'OPEN',body,received_at.isoformat(),None))
        audit(conn, 'provider.webhook.reconcile', actor, reason, {'event_id':event_id,'prior_status':prior_status,'event_type':event_type}, lead_id, call_id, 'webhook:'+event_id)
        conn.commit()
        return {'event_id':event_id,'accepted':True,'processed':False,'status':'RECONCILIATION','reason_code':reason,'duplicate':False}
    now = received_at.isoformat()
    conn.execute('INSERT INTO call_event_history VALUES(?,?,?,?,?,?,?)', (event_id,call_id,event_type,prior_status,next_status,json.dumps(payload,sort_keys=True),now))
    conn.execute('UPDATE call_sessions SET status=?,last_provider_event_id=?,started_at_utc=CASE WHEN ?="RINGING" THEN COALESCE(started_at_utc,?) ELSE started_at_utc END,answered_at_utc=CASE WHEN ?="ANSWERED" THEN COALESCE(answered_at_utc,?) ELSE answered_at_utc END,ended_at_utc=CASE WHEN ? IN ("COMPLETED","FAILED","OPTED_OUT") THEN COALESCE(ended_at_utc,?) ELSE ended_at_utc END,updated_at_utc=? WHERE call_id=?', (next_status,event_id,next_status,now,next_status,now,next_status,now,now,call_id))
    if next_status == 'OPTED_OUT':
        conn.execute('UPDATE crm_leads SET lifecycle_status="DISPATCH_BLOCKED",updated_at_utc=? WHERE lead_id=?', (now,lead_id))
    result = {'event_id':event_id,'accepted':True,'processed':True,'status':next_status,'duplicate':False}
    conn.execute('UPDATE provider_webhook_events SET processing_status="PROCESSED",result_json=?,processed_at_utc=? WHERE provider_event_id=?', (json.dumps(result,sort_keys=True),now,event_id))
    sync_call_status(conn, event_id, call_id, lead_id, next_status, payload)
    audit(conn, 'provider.webhook.process', actor, next_status, {'event_id':event_id,'event_type':event_type,'provider_call_id':provider_call_id}, lead_id, call_id, 'webhook:'+event_id)
    conn.commit()
    return result
