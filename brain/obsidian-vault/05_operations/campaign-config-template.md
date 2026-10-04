---
type: template
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Campaign configuration template

Copy this template per campaign. Do not activate while any `REQUIRED` or `TODO` value remains unresolved.

```yaml
campaign_id: REQUIRED
status: draft
legal_seller_entity: REQUIRED
public_brand: REQUIRED
niche: REQUIRED
target_jurisdictions: []
recipient_location_method: REQUIRED
lead_source_id: REQUIRED
source_permission: REQUIRED
offer_version: REQUIRED
script_version: REQUIRED
brain_version: REQUIRED
policy_version: REQUIRED
voice_provider: REQUIRED
crm: REQUIRED
calendar: REQUIRED
closer_queue: REQUIRED
caller_id: REQUIRED
callback_number: REQUIRED
consent_policy_version: REQUIRED
suppression_policy_version: REQUIRED
recording_policy_version: REQUIRED
daily_cap: REQUIRED
retry_limit: REQUIRED
local_calling_windows: REQUIRED
human_monitoring: REQUIRED
stop_thresholds: REQUIRED
canary_cohort: REQUIRED
rollback_manifest: REQUIRED
counsel_review_ref: REQUIRED
```

## Activation states

`DRAFT → CONFIGURED → TESTING → CANARY_APPROVED → PILOT → PAUSED | RETIRED`. Only `CANARY_APPROVED` may enter a controlled pilot, and only when the release gate and campaign legal gate are both green.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[campaign-rules]]
- [[brain-release-manifest]]
- [[production-readiness]]
- [[target-state-campaign-action-plan]]
