---
type: register
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Lead scoring

Use [[lead-scoring-v2]] as the canonical scoring model. Scoring prioritizes review and routing; it never bypasses compliance. A high score with an unresolved consent, suppression, jurisdiction, identity, or number-type issue is `BLOCKED`.

The score must preserve component values and evidence IDs. Do not infer authority, urgency, budget, or intent from tone, silence, company size, or a generic database label.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[ideal-customer-profile]]
- [[qualified-lead-definition]]
- [[01_compliance/consent-gate]]
