# Phase 4: Real-time analytics and CRM status synchronization

Phase 4 adds an event-driven CRM call-status synchronizer and a read-only operations dashboard. It uses the Phase 3 audited database as the source of truth.

## Automated CRM sync

Provider events are synchronized exactly once by `source_event_id`. Each accepted event creates:

- a current `crm_call_status` row;
- one `crm_status_history` row;
- one `crm_status_sync_events` row; and
- an audit event from the Phase 3 processor.

A replay returns the prior result. A changed payload with the same event ID raises a conflict. This prevents duplicate CRM updates and preserves history.

## Analytics

`src/analytics.py` derives live metrics from operational tables:

- staged leads;
- pending, sent, and blocked dispatch;
- created, ringing, answered, completed, failed, and opted-out calls;
- answer, failure, and opt-out rates;
- open reconciliation count;
- webhook event count; and
- audit event count.

The dashboard polls the metrics/activity endpoints every two seconds. It is intentionally read-only; it cannot dispatch calls or alter suppression.

## Dashboard endpoints

```text
GET /                 read-only dashboard
GET /health           service health
GET /api/metrics      current metrics JSON
GET /api/activity     recent audit events JSON
```

Start it with:

```bash
cd /home/ubuntu/pre-calling-system
python3 src/dashboard_server.py --db run/phase4.db --host 0.0.0.0 --port 8765
```

## Boundary

The dashboard is observability only. Dispatch remains controlled by the Phase 2 eligibility gate and Phase 3 provider outbox. CRM synchronization may update status from verified events, but it cannot authorize a call, remove suppression, or turn an uncertain provider outcome into success.
