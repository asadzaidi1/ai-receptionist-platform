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

# Lead verification workflow

Verification proves that a record is usable; it does not prove that it may be called.

## Verification stages

1. Confirm the business exists through an approved source.
2. Confirm domain, industry, geography, and operating status.
3. Identify a role only when supported by source evidence; mark decision authority as `confirmed`, `unconfirmed`, or `unknown`.
4. Classify the number and likely recipient type through an approved method.
5. Resolve jurisdiction and recipient time zone with source and confidence.
6. Check source permission, consent evidence, suppression, and campaign scope.
7. Create a normalized CRM record only after lineage and evidence references exist.

## Outcomes

- `VERIFIED_FOR_REVIEW`: identity is credible but eligibility is not complete.
- `ELIGIBLE_TO_CONTACT`: all campaign gate requirements pass.
- `HUMAN_REVIEW_REQUIRED`: conflicting or high-impact uncertainty.
- `NOT_ELIGIBLE`: cannot be contacted by this campaign.
- `SUPPRESSED`: stop across seller campaigns according to suppression scope.

A high fit score cannot override `HUMAN_REVIEW_REQUIRED`, `NOT_ELIGIBLE`, or `SUPPRESSED`.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[data-cleaning-dedupe]]
- [[lead-eligibility-routing]]
- [[consent-gate]]
- [[jurisdiction-matrix]]
