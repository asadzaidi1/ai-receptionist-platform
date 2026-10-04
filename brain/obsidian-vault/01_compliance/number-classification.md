---
type: rule
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Number classification and identity resolution

Before dialing, classify the destination as `wireless`, `residential`, `business_landline`, `business_voip`, `emergency_or_restricted`, or `unknown`. Record the data source, confidence, timestamp, and whether the number may belong to a person rather than the business.

Unknown or conflicting classification is a hard stop for AI voice marketing until counsel-approved rules resolve it. A publicly listed business number, a CRM label, or an employer’s lead list is not proof that the called person consented or that the number is outside the TCPA.

Number reassignment, shared lines, extensions, forwarding, personal mobiles, and wrong-party reports require re-verification and may create a suppression event.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[jurisdiction-matrix]]
