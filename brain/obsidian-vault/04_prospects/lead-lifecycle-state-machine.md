---
type: register
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Lead and opportunity lifecycle

Keep these state machines separate:

**Lead lifecycle:** `NEW → ELIGIBLE → ATTEMPTING → CONNECTED → NURTURE | QUALIFIED | DISQUALIFIED | SUPPRESSED`.

**Call outcome:** `NO_ANSWER | VOICEMAIL_NO_MESSAGE | WRONG_NUMBER | GATEKEEPER | OWNER_REACHED | CALLBACK_REQUESTED | DEMO_BOOKED | HUMAN_HANDOFF | DO_NOT_CALL | ERROR`.

**Handoff:** `REQUESTED → OFFERED → ACCEPTED → INTRODUCED → OWNED | FAILED → CALLBACK_QUEUED`.

**Opportunity:** `OPEN → DISCOVERY → PROPOSAL → WON | LOST | CLOSED`.

A connected call is not a qualified lead. A qualified lead is not a successful handoff. A handoff request is not a handoff acceptance. Every transition has required fields, owner, timestamp, reason, and idempotency key.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[qualified-lead-definition]]
- [[call-sheet-fields]]
- [[03_call_playbook/agent-state-machine]]
