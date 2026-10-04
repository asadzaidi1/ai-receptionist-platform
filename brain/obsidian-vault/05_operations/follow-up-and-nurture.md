---
type: workflow
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Follow-up and nurture workflow

Follow-up is a bounded, permission-aware task—not an excuse for indefinite retries.

## Immediate outcomes

- `DO_NOT_CALL`: suppress immediately and cancel all future work.
- `NOT_INTERESTED`: close with reason; do not automatically re-add.
- `CALLBACK_REQUESTED`: create a scoped task with requested number, purpose, time zone, owner, expiry, and evidence.
- `DEMO_BOOKED`: use verified calendar event ID; attach reminder policy.
- `HUMAN_HANDOFF_FAILED`: create one bounded fallback task only if the person agrees.
- `NO_ANSWER/VOICEMAIL`: follow campaign-approved retry policy with fresh eligibility checks.

## Nurture states

`NURTURE_ELIGIBLE → SCHEDULED → DUE → RECHECKED → CONTACTED | EXPIRED | SUPPRESSED`.

Every future touch rechecks suppression, consent scope, jurisdiction, time zone, campaign status, and offer version. Stop nurture on opt-out, wrong party, complaint, stale consent, campaign pause, or data-quality conflict.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[callback-policy]]
- [[dnc-and-suppression-operations]]
- [[crm-pipeline-contract]]
- [[campaign-rules]]
