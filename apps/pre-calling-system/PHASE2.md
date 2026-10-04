# Phase 2: Staging CRM and dispatch gate

Phase 2 takes only `CAMPAIGN_READY` rows from Phase 1 and performs idempotent upserts into a local staging CRM. It does not place calls.

## Flow

```text
Phase 1 CAMPAIGN_READY CSV
  ↓
validate lead exists in canonical DB
  ↓
CRM idempotent upsert
  ↓
staging CRM account/contact/lead
  ↓
final dispatch-time gate
  ↓
provider outbox with idempotency key
  ↓
future provider adapter
```

## Idempotent upsert

The upsert key is `crm-upsert:{campaign_id}:{lead_id}:{brain_version}`. Replaying the same row returns the previous result without creating another account, contact, or lead. Replaying the same idempotency key with a different payload raises a conflict. Account and contact uniqueness prevent duplicate account/contact creation.

## Dispatch-time gate

The gate re-checks the current staging/Phase 1 data immediately before any provider request:

1. campaign status is `CANARY_APPROVED` or `PILOT`;
2. lead remains `CAMPAIGN_READY`;
3. source permission is approved;
4. consent is verified;
5. phone is valid;
6. number type is an approved business type;
7. jurisdiction and time zone are known;
8. current suppression check has no match;
9. caller ID is approved;
10. callback/handoff path is ready;
11. provider configuration is ready; and
12. current local time is within the campaign window.

If any check fails, the outbox record is `BLOCKED`. No provider call is made. The gate returns every check and a deterministic reason code.

## Provider boundary

`provider_outbox` is the handoff boundary. The provider adapter must consume only `PENDING` records, send the exact request once using `provider_idempotency_key`, verify signed callbacks, and update status idempotently. This project includes no live provider adapter and no network calls.

## Run Phase 2

```bash
cd /home/ubuntu/pre-calling-system
python3 -m pytest -q
python3 - <<'PY'
from pathlib import Path
from src.lead_pipeline import process
from src.staging_crm import upsert_ready_queue
process(Path('fixtures/raw_leads.csv'), Path('fixtures/suppression.csv'), Path('run/phase2.db'), today=__import__('datetime').date(2026,10,4))
print(upsert_ready_queue(Path('run/phase2.db'), Path('run/queues/campaign_ready.csv'), 'pilot_ca_001', 'brain-v1.3', 'policy-v1'))
PY
```

For real integration, keep a staging CRM, consent service, and provider adapter separate. Never treat `PENDING` as a sent call and never bypass the gate from a prompt or CSV.
