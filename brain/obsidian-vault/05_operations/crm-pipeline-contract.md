---
type: register
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# CRM pipeline contract

Use separate objects or fields for account, contact, lead, call, task, handoff, and opportunity. Never collapse them into one status.

## Lead lifecycle

## Required lifecycle

`NEW → CLEANED → VERIFIED → ELIGIBLE → ATTEMPTING → CONNECTED → QUALIFIED → OPPORTUNITY → CUSTOMER`

## Call dispositions

Parallel call dispositions include `NO_ANSWER`, `VOICEMAIL`, `GATEKEEPER`, `WRONG_NUMBER`, `NOT_INTERESTED`, `CALLBACK_REQUESTED`, `DEMO_BOOKED`, `HUMAN_HANDOFF`, `DO_NOT_CALL`, and `SYSTEM_ERROR`.

## Opportunity fields

## Required opportunity fields

`opportunity_id`, `lead_id`, owner, source, qualification evidence, unknowns, problem, impact, stakeholders, timeline, next step, next-step due time, offer version, handoff acceptance ID, meeting/event ID, last activity, loss reason, and suppression status.

## Write rules

Every write requires a schema-valid payload, current state, actor/service identity, idempotency key, source event, and audit record. A missed call is not a qualification. A callback request is not a sale. A booked meeting is not a won opportunity.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[call-sheet-fields]]
- [[lead-lifecycle-state-machine]]
- [[runtime-contract]]
- [[webhook-idempotency]]
