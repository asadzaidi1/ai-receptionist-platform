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

# Lead eligibility and routing

Routing is a policy decision before it is a sales decision.

```text
RAW → CLEANED → VERIFIED
  ├─ BLOCKED_COMPLIANCE → SUPPRESSED/REVIEW
  ├─ INCOMPLETE_DATA → DATA_RESEARCH
  ├─ LOW_FIT → NURTURE_OR_ARCHIVE
  ├─ ELIGIBLE_LOW_INTENT → CONTROLLED_OUTREACH
  └─ ELIGIBLE_HIGH_INTENT → HUMAN_PRIORITY
```

## Hard eligibility fields

`campaign_id`, seller/brand, lead source, campaign purpose, recipient jurisdiction, number type, time zone, consent/legal-basis decision, suppression decision, caller identity, callback route, recording decision, source freshness, and policy version.

If any required field is absent, stale, mismatched, or unknown, route to `HUMAN_REVIEW_REQUIRED` or `DATA_RESEARCH`; never to the dialer. Routing decisions must be recomputed at dispatch, not trusted from import time.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[consent-gate]]
- [[dnc-and-suppression-operations]]
- [[jurisdiction-matrix]]
- [[lead-scoring]]
- [[campaign-config-template]]
