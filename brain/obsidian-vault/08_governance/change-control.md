---
type: rule
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Change control and release management

## Change classes

- **Major:** consent, suppression, disclosure, caller identity, legal rule, price, claim, capability, tool permission, state transition, data flow, vendor, or handoff behavior. Requires owner plus relevant compliance/security/business approval and full regression.
- **Minor:** wording, formatting, non-material classification, or test-only change. Requires owner review and targeted regression.
- **Emergency:** change required to stop harm or unauthorized activity. Pause first, preserve evidence, document the change, then complete review and regression before normal restart.

Every change records author, reason, affected notes/configuration, risk, source, approvals, tests, release ID, rollout, rollback, and result. Protect the production branch and do not edit a live note silently.

The deployed release must be reproducible from a source-control revision, configuration snapshot, and index build ID.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[production-readiness]]
- [[release-gate]]
- [[source-registry]]
