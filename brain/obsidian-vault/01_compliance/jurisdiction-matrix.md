---
type: register
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Jurisdiction and channel matrix

One row is required for every target jurisdiction, number type, call purpose, channel, and campaign.

| Jurisdiction | Number type | Purpose | AI voice | Consent standard | DNC source | Call window | Recording rule | Counsel decision | Review date |
|---|---|---|---|---|---|---|---|---|---|
| TODO | TODO | marketing | yes | TODO | TODO | TODO | TODO | blocked | TODO |

Do not generalize from one state to another. Record the recipient’s likely location, not only the business headquarters. Treat unknown location, unknown number type, and stale rules as `DO_NOT_DIAL`. The matrix must be versioned, source-linked, and checked by the dispatch service before every attempt.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[calling-hours]]
- [[recording-consent]]
