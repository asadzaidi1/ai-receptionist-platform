---
type: rule
status: draft
authority: playbook
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Voicemail policy

The default is to leave no AI-generated marketing voicemail. The consent gate must approve any exception.

If a campaign has an approved voicemail policy, it must specify the exact wording, identity, purpose, opt-out route, recording status, frequency cap, and evidence basis. If any part is missing, log `VOICEMAIL_NO_MESSAGE` and end the attempt.

Never leave a message that implies urgency, a personal relationship, an existing appointment, or a reason for calling that is not true.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[01_compliance/ai-disclosure-wording]]
- [[disposition-codes]]
