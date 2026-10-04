---
type: rule
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Campaign control rules

Every campaign uses [[campaign-config-template]] and [[lead-generation-operating-system]]. A campaign cannot dispatch raw records. It must import, normalize, deduplicate, verify, pass the compliance gate, score, pace, and re-check eligibility at dispatch.

## Automatic pause conditions

Pause the affected campaign immediately for any critical compliance failure, missed suppression, unsupported claim, hallucination, false transfer/booking, consent-service outage, unknown eligibility result, cross-tenant retrieval, excessive complaints/opt-outs, unapproved offer change, duplicate-dial event, or material CRM/provider reconciliation failure.

Thresholds are campaign-specific and must be approved before launch. See [[conversion-funnel-metrics]], [[qa-scorecard]], and [[incident-severity-matrix]].

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[handoff-sla]]
- [[launch-checklist]]
