#!/usr/bin/env python3
"""Read-only real-time analytics derived from the audited staging database."""
from __future__ import annotations
from datetime import datetime, timezone


def _count(conn, sql, args=()):
    return conn.execute(sql, args).fetchone()[0]

def get_dashboard_metrics(conn, campaign_id: str | None = None) -> dict:
    where = ''
    args = ()
    if campaign_id:
        where = ' WHERE campaign_id=? '
        args = (campaign_id,)
    metrics = {
        'staged_leads': _count(conn, 'SELECT count(*) FROM crm_leads' + where, args),
        'pending_dispatch': _count(conn, 'SELECT count(*) FROM provider_outbox WHERE status="PENDING"' + (' AND campaign_id=?' if campaign_id else ''), args),
        'sent_calls': _count(conn, 'SELECT count(*) FROM provider_outbox WHERE status="SENT"' + (' AND campaign_id=?' if campaign_id else ''), args),
        'blocked_dispatch': _count(conn, 'SELECT count(*) FROM provider_outbox WHERE status="BLOCKED"' + (' AND campaign_id=?' if campaign_id else ''), args),
        'created_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="CREATED"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'ringing_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="RINGING"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'answered_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="ANSWERED"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'completed_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="COMPLETED"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'failed_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="FAILED"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'opted_out_calls': _count(conn, 'SELECT count(*) FROM crm_call_status WHERE status="OPTED_OUT"' + (' AND call_id IN (SELECT call_id FROM call_sessions WHERE campaign_id=?)' if campaign_id else ''), args),
        'reconciliation_open': _count(conn, 'SELECT count(*) FROM reconciliation_queue WHERE status="OPEN"'),
        'webhook_events': _count(conn, 'SELECT count(*) FROM provider_webhook_events'),
        'audit_events': _count(conn, 'SELECT count(*) FROM audit_events'),
        'last_updated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
    }
    metrics['answer_rate'] = round(metrics['answered_calls'] / metrics['sent_calls'], 4) if metrics['sent_calls'] else 0
    metrics['failure_rate'] = round(metrics['failed_calls'] / metrics['sent_calls'], 4) if metrics['sent_calls'] else 0
    metrics['opt_out_rate'] = round(metrics['opted_out_calls'] / metrics['sent_calls'], 4) if metrics['sent_calls'] else 0
    return metrics

def get_recent_activity(conn, limit: int = 25) -> list[dict]:
    rows = conn.execute('SELECT created_at_utc,event_type,actor,outcome,lead_id,call_id,idempotency_key,metadata_json FROM audit_events ORDER BY created_at_utc DESC LIMIT ?', (limit,)).fetchall()
    return [{'created_at_utc':r[0],'event_type':r[1],'actor':r[2],'outcome':r[3],'lead_id':r[4],'call_id':r[5],'idempotency_key':r[6],'metadata':r[7]} for r in rows]
