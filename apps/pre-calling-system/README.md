
## Phase 3: provider adapter and signed webhooks

Phase 3 adds a provider-neutral adapter harness in `src/provider_adapter.py`. It uses HMAC-signed synthetic webhooks and never makes live network calls.

```bash
python3 -m pytest -q
```

The Phase 3 tables are created automatically with the staging database:

- `provider_webhook_events`
- `call_sessions`
- `call_event_history`
- `reconciliation_queue`
- `audit_events`

See [PHASE3.md](PHASE3.md) and [PROVIDER_INTERFACE.md](PROVIDER_INTERFACE.md) for the exact provider boundary.
