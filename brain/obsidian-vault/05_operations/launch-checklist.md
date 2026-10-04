---
type: guide
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Campaign launch checklist

- [ ] Seller, brand, campaign, niche, target state, and geography are named.
- [ ] Raw source export is immutable and lineage is preserved.
- [ ] Cleaning, dedupe, verification, and freshness rules are tested.
- [ ] Consent, jurisdiction, number-type, suppression, and time-window gate is enforced in code.
- [ ] Lead routing and scoring cannot override a hard compliance stop.
- [ ] Caller ID, callback, AI identity, and recording policy are approved.
- [ ] Offer, capabilities, claims, and prices are live and sourced.
- [ ] CRM, calendar, dialer, consent service, closer queue, and evidence store are connected.
- [ ] CRM fields, lifecycle states, dispositions, idempotency, and reconciliation are tested.
- [ ] Zero-hallucination and lead-funnel test suites pass.
- [ ] Handoff acceptance and booking event IDs are required before success states.
- [ ] Audit records exist for blocked, eligible, attempted, suppressed, and failed decisions.
- [ ] Human monitoring, daily cap, pause authority, stop thresholds, and rollback are assigned.
- [ ] Brain, script, offer, campaign, policy, and vendor versions are recorded.
- [ ] Counsel approves the exact pilot scope.

No checkbox may be marked complete with “probably,” “we have access,” or a verbal assumption.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[01_compliance/consent-ledger-spec]]
- [[06_performance/release-test-suite]]
