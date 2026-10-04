---
type: rule
status: draft
authority: compliance
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Opt-out handling

A request to stop is effective immediately. Do not argue, ask for a reason, make one more pitch, or offer a different channel without separate permission.

## Required sequence

1. Acknowledge briefly.
2. Confirm that the number will be suppressed.
3. End the call promptly.
4. Write an append-only suppression event to the operational system.
5. Block the number before any future campaign can dial it.

## Approved wording

> “Understood. I’ll mark this number so we don’t call you again. Thank you for your time.”

Treat “remove me,” “stop calling,” “take me off your list,” and equivalent language as an opt-out. Use disposition `DO_NOT_CALL`. The system must distinguish a number-level suppression from a person-, business-, seller-, or all-channel suppression. When uncertain, apply the broader protection and send it to compliance review.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[03_call_playbook/disposition-codes]]
