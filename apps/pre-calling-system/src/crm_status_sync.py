#!/usr/bin/env python3
"""Idempotent CRM call-status synchronization from provider events."""
from __future__ import annotations
import hashlib, json
from staging_crm import now_utc

DISPOSITIONS = {
    'CREATED': 'CALL_CREATED',
    'RINGING': 'RINGING_NO_OUTCOME',
    'ANSWERED': 'CONNECTED',
    'COMPLETED': 'CALL_COMPLETED',
    'FAILED': 'CALL_FAILED',
    'OPTED_OUT': 'DO_NOT_CALL',
}

def sync_call_status(conn, source_event_id: str, call_id: str, lead_id: str, status: str, payload: dict, actor: str = 'crm-status-sync') -> dict:
    payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    prior = conn.execute('SELECT sync_status,result_json,payload_hash FROM crm_status_sync_events WHERE source_event_id=?', (source_event_id,)).fetchone()
    if prior:
        if prior[2] != payload_hash:
            raise ValueError(f'CRM sync payload conflict for {source_event_id}')
        result = json.loads(prior[1]); result['replayed'] = True
        return result
    prior_status_row = conn.execute('SELECT status FROM crm_call_status WHERE call_id=?', (call_id,)).fetchone()
    prior_status = prior_status_row[0] if prior_status_row else None
    disposition = DISPOSITIONS.get(status, 'UNKNOWN')
    ts = now_utc()
    conn.execute('INSERT OR REPLACE INTO crm_call_status VALUES(?,?,?,?,?,?)', (call_id, lead_id, status, disposition, source_event_id, ts))
    history_id = 'crmstatus_' + hashlib.sha256((source_event_id + call_id + status).encode()).hexdigest()[:24]
    conn.execute('INSERT INTO crm_status_history VALUES(?,?,?,?,?,?,?,?)', (history_id, call_id, lead_id, prior_status, status, disposition, source_event_id, ts))
    result = {'source_event_id':source_event_id,'call_id':call_id,'lead_id':lead_id,'from_status':prior_status,'to_status':status,'disposition':disposition,'replayed':False}
    conn.execute('INSERT INTO crm_status_sync_events VALUES(?,?,?,?,?,?,?)', (source_event_id,call_id,lead_id,'APPLIED',payload_hash,json.dumps(result,sort_keys=True),ts))
    conn.commit()
    return result
