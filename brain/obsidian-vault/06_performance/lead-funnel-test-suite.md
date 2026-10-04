---
type: test
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Lead funnel end-to-end test suite

Use synthetic records and fake provider IDs. Each test must trace one correlation set across import, CRM, consent, dialer, agent, calendar, handoff, analytics, and QA.

| Test | Expected result | Blocker if failed |
|---|---|---|
| duplicate source rows | one canonical lead, lineage preserved | data integrity |
| conflicting suppression records | blocked and human review | compliance |
| unknown number type | no dispatch | compliance |
| stale source record | research or archive | data quality |
| high fit but missing consent evidence | blocked | compliance |
| eligible lead at wrong local time | queued, not dialed | compliance |
| positive conversation with unknown budget | qualified only if budget not required; unknown preserved | truthfulness |
| callback requested | bounded task and re-check | state integrity |
| transfer requested, closer unavailable | no handoff success; fallback | false success |
| calendar timeout | no booked claim | false success |
| opt-out during nurture | all future tasks cancelled | suppression |
| duplicate provider event | one side effect | idempotency |
| CRM write failure | dead-letter/reconcile, no announcement | reliability |
| qualified lead | human owner and next step created | conversion |
| closed-won update | verified source event | attribution |

Release requires zero critical failures and complete trace continuity.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[lead-generation-operating-system]]
- [[runtime-contract]]
- [[webhook-idempotency]]
- [[evaluation-plan]]
- [[release-gate]]
