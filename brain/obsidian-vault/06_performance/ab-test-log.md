---
type: decision
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# A/B test log

Do not run experiments that change legal disclosures, opt-out behavior, consent gates, or required identity information.

| Test ID | Variable | A | B | Audience | Primary metric | Guardrails | Result | Decision |
|---|---|---|---|---|---|---|---|---|
| TODO | opener | TODO | TODO | TODO | qualified transfer rate | opt-outs, complaints, QA | TODO | TODO |

Change one variable at a time. Predefine the stopping rule, sample boundaries, guardrails, owner, and review date. A conversion increase is not a win if complaint rate, opt-out rate, or unsupported claims worsen.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[kpis-and-unit-economics]]
- [[qa-scorecard]]
- [[05_operations/campaign-rules]]
