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

# Fit, intent, and readiness scoring

Use separate scores. Scoring prioritizes work; it never authorizes contact.

## Fit score: 0–100

| Dimension | Weight | Evidence |
|---|---:|---|
| ICP/industry fit | 20 | verified industry and use case |
| company size/complexity | 15 | sourced company facts |
| geography/serviceability | 10 | approved territory |
| problem likelihood | 20 | sourced signal, not stereotype |
| role/decision access | 15 | confirmed or unconfirmed role |
| operational fit | 10 | approved capability match |
| data freshness/confidence | 10 | source age and verification |

## Intent score: 0–100

Use only explicit events: positive reply, question about offer, requested callback, accepted handoff, booked meeting, or stated timing. Tone, silence, email opens, and inferred urgency are not intent proof.

## Readiness outcome

- `A_HUMAN_PRIORITY`: fit and intent high, eligibility passed.
- `B_CONTROLLED_OUTREACH`: fit high, intent low, eligibility passed.
- `C_VERIFY_FIRST`: fit or identity uncertain.
- `D_ARCHIVE`: poor fit or outside serviceability.
- `BLOCKED`: any suppression, consent, jurisdiction, identity, or policy hard stop.

Store score components and evidence IDs. Never let an aggregate score hide a hard stop.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[lead-scoring]]
- [[lead-eligibility-routing]]
- [[qualified-lead-definition]]
- [[consent-gate]]
