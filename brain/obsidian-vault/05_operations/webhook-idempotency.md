---
type: rule
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Webhook, retry, and idempotency standard

All inbound provider events are untrusted until signature-verified. Store the raw event in a restricted event store, then normalize it into a state transition.

Each side effect requires an idempotency key such as `provider:event_id`, `call_id:transition`, or `lead_id:callback_at:purpose`. Duplicate events must return the prior result. Out-of-order events enter a reconciliation queue rather than rewriting history.

Use bounded exponential backoff, circuit breakers, and dead-letter queues. Never retry a dial, transfer, callback, or message when the prior outcome is uncertain unless a human-approved reconciliation rule says it is safe and the suppression gate has been re-run.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[production-architecture]]
- [[incident-runbook]]
- [[01_compliance/dnc-and-suppression-operations]]
