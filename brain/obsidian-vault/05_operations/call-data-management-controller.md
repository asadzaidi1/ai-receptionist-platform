---
type: rule
status: draft
authority: operations
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Call-data management controller

The runtime call-data controller uses the canonical `docs/CALL-DATA-MANAGEMENT-PROMPT.md` from the GitHub repository to process every verified provider event.

## Required behavior

- Create one concise factual note per call.
- Keep provider status separate from business disposition.
- Update call, lead, task, opportunity, suppression, and audit records separately.
- Use provider event IDs and follow-up task keys for idempotency.
- Treat `NO_ANSWER`, voicemail, and answering-machine outcomes as attempts, not contact or consent.
- Require a bounded purpose, owner, date, local time, timezone, scope, expiry, and attempt limit for every follow-up.
- Re-check consent, suppression, number validity, jurisdiction, local time, campaign status, and callback scope before a callback.
- Route missing, conflicting, out-of-order, or unsupported evidence to reconciliation.
- Handle opt-outs, complaints, wrong numbers, and compliance concerns before any other follow-up action.

## No-answer and answering-machine policy

`NO_ANSWER`, `VOICEMAIL_NO_MESSAGE`, `VOICEMAIL_MESSAGE_LEFT`, `ANSWERING_MACHINE_NO_MESSAGE`, and `ANSWERING_MACHINE_MESSAGE_LEFT` never mean that the person was reached, interested, qualified, or consenting.

A message may be left only when permitted by the approved campaign policy and the approved message version is recorded. A further attempt requires the retry policy, a suppression/consent re-check, local-time validation, and a deterministic task idempotency key.

## Related

- [[crm-pipeline-contract]]
- [[callback-policy]]
- [[03_call_playbook/disposition-codes]]
- [[01_compliance/opt-out-handling]]
- [[runtime-contract]]
