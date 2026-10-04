---
type: rule
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Data cleaning and deduplication workflow

Process every imported record through these states:

```text
IMPORTED → NORMALIZED → DEDUPE_CHECK → VERIFIED | REVIEW_REQUIRED | INVALID | SUPPRESSED
```

Normalize company names, domains, addresses, phone formats, time zones, and source timestamps. Use deterministic duplicate keys in this order: CRM account ID, normalized domain, normalized company plus location, then tokenized phone with a human review for collisions. Never merge records when the merge could erase consent, suppression, owner, call history, or source lineage.

## Reject or review

- disconnected or malformed phone;
- duplicate with conflicting owner or suppression;
- business cannot be verified;
- stale record beyond campaign freshness policy;
- restricted/emergency/sensitive organization;
- missing source permission;
- unknown jurisdiction or time zone;
- individual/personal contact where campaign approval is absent; or
- conflicting company/contact identity.

Every decision records `dedupe_key`, `match_method`, `confidence`, `reviewer_or_rule_version`, and `decision_reason`.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[raw-lead-import-schema]]
- [[lead-verification-workflow]]
- [[lead-eligibility-routing]]
- [[data-classification]]
