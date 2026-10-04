#!/usr/bin/env python3
"""Fail-closed dispatch gate. It creates provider outbox records but never sends calls."""
from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from lead_pipeline import normalize_phone, load_suppression, suppression_match
from staging_crm import init_staging, now_utc

POLICY_VERSION = 'dispatch-gate-v0.1'

def local_minutes(now_utc_value: datetime, timezone_name: str) -> int:
    return now_utc_value.astimezone(ZoneInfo(timezone_name)).hour * 60 + now_utc_value.astimezone(ZoneInfo(timezone_name)).minute

def in_window(minutes: int, start: str, end: str) -> bool:
    sh, sm = map(int, start.split(':')); eh, em = map(int, end.split(':'))
    a, b = sh*60+sm, eh*60+em
    return a <= minutes < b if a <= b else minutes >= a or minutes < b

def evaluate_dispatch(conn, lead_id: str, campaign: dict, now_utc_value: datetime, suppressions: list[dict], provider_ready: bool = False, local_minute_override: int | None = None):
    row = conn.execute('''SELECT l.*, c.contact_name, c.contact_role, c.phone_token, c.jurisdiction, c.time_zone,
                         k.company_name, k.normalized_domain, k.phone_e164, k.number_type,
                         k.source_permission, k.consent_status, k.source_date
                         FROM crm_leads l JOIN crm_contacts c ON c.contact_id=l.contact_id
                         JOIN canonical_leads k ON k.lead_id=l.lead_id
                         WHERE l.lead_id=?''', (lead_id,)).fetchone()
    if not row: return {'allowed': False, 'reason_code': 'LEAD_NOT_FOUND'}
    cols = [d[1] for d in conn.execute('PRAGMA table_info(crm_leads)').fetchall()] + ['contact_name','contact_role','phone_token','jurisdiction','time_zone','company_name','normalized_domain','phone_e164','number_type','source_permission','consent_status','source_date']
    data = dict(zip(cols, row))
    checks = {}
    checks['campaign_approved'] = campaign.get('status') in {'CANARY_APPROVED','PILOT'}
    checks['queue_ready'] = data['queue'] == 'CAMPAIGN_READY'
    checks['source_permission'] = data['source_permission'] == 'approved'
    checks['consent_verified'] = data['consent_status'] == 'verified'
    checks['phone_valid'] = bool(normalize_phone(data['phone_e164']))
    checks['number_type_approved'] = data['number_type'] in {'business_landline','business_voip'}
    checks['jurisdiction_known'] = bool(data['jurisdiction'])
    checks['timezone_known'] = bool(data['time_zone'])
    sm = suppression_match({'phone': data['phone_e164'], 'domain': data['normalized_domain'], 'company_name': data['company_name']}, suppressions)
    checks['not_suppressed'] = sm is None
    checks['caller_id_approved'] = bool(campaign.get('caller_id_approved'))
    checks['callback_ready'] = bool(campaign.get('callback_ready'))
    checks['provider_ready'] = provider_ready
    checks['local_window'] = False
    if checks['timezone_known']:
        try:
            minutes = local_minute_override if local_minute_override is not None else local_minutes(now_utc_value, data['time_zone'])
            checks['local_window'] = in_window(minutes, campaign.get('window_start','09:00'), campaign.get('window_end','17:00'))
        except Exception:
            checks['local_window'] = False
    allowed = all(checks.values())
    reason = 'ALLOW_DISPATCH' if allowed else next(k.upper() for k,v in checks.items() if not v)
    decision_id = 'dispatch_' + lead_id + ':' + campaign['campaign_id'] + ':' + now_utc_value.isoformat()
    result = {'allowed': allowed, 'reason_code': reason, 'dispatch_decision_id': decision_id, 'suppression_match': sm, 'checks': checks, 'policy_version': POLICY_VERSION}
    conn.execute('INSERT OR REPLACE INTO dispatch_decisions VALUES(?,?,?,?,?,?,?,?)', (decision_id, lead_id, campaign['campaign_id'], int(allowed), reason, json.dumps(result, sort_keys=True), POLICY_VERSION, now_utc_value.isoformat()))
    conn.commit()
    return result

def queue_provider_request(conn, lead_id: str, campaign: dict, gate_result: dict):
    key = f"provider:{campaign['campaign_id']}:{lead_id}:{campaign['brain_version']}"
    now = now_utc()
    request = {'lead_id': lead_id, 'campaign_id': campaign['campaign_id'], 'brain_version': campaign['brain_version'], 'script_version': campaign['script_version'], 'policy_version': POLICY_VERSION}
    prior = conn.execute('SELECT status,request_json FROM provider_outbox WHERE provider_idempotency_key=?', (key,)).fetchone()
    if prior:
        if prior[1] != json.dumps(request, sort_keys=True):
            raise ValueError('provider idempotency conflict')
        return {'status': prior[0], 'provider_idempotency_key': key, 'replayed': True}
    if not gate_result['allowed']:
        conn.execute('INSERT INTO provider_outbox VALUES(?,?,?,?,?,?,?,?,?)', (key, lead_id, campaign['campaign_id'], campaign['provider_name'], 'BLOCKED', json.dumps(request, sort_keys=True), json.dumps(gate_result, sort_keys=True), now, now))
        conn.commit()
        return {'status':'BLOCKED','provider_idempotency_key':key,'replayed':False,'reason_code':gate_result['reason_code']}
    conn.execute('INSERT INTO provider_outbox VALUES(?,?,?,?,?,?,?,?,?)', (key, lead_id, campaign['campaign_id'], campaign['provider_name'], 'PENDING', json.dumps(request, sort_keys=True), None, now, now))
    conn.execute('UPDATE crm_leads SET lifecycle_status="ELIGIBLE_PENDING_DISPATCH", updated_at_utc=? WHERE lead_id=?', (now, lead_id))
    conn.commit()
    return {'status':'PENDING','provider_idempotency_key':key,'replayed':False}
