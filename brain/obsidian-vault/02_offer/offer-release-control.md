---
type: rule
status: draft
authority: offer
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Offer release control

The offer is a versioned release, not a set of claims scattered across scripts. A release includes the product overview, capabilities, price card, approved claims, privacy/security answers, implementation limits, evidence, effective date, owner, and rollback version.

A change to price, feature, integration, promise, refund, security statement, compliance claim, or implementation timeline is a major release. It requires a new version, regression tests, human approval, and a new export to the agent. The voice agent must never read a draft or retired offer note.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[price-card]]
- [[capabilities-register]]
- [[approved-claims]]
- [[06_performance/release-gate]]
