---
type: metric
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Conversion funnel metrics

Measure the funnel by stage and cohort, not by vanity totals.

| Stage | Definition | Required evidence |
|---|---|---|
| Imported | raw row accepted | source ID |
| Cleaned | normalized and deduped | transform ID |
| Verified | business/contact facts checked | verification refs |
| Eligible | campaign gate passed | policy decision ID |
| Attempted | dispatch accepted by dialer | provider call ID |
| Connected | answered interaction | call event |
| Qualified | all required fields confirmed | qualification evidence |
| Handoff accepted | human accepted | acceptance ID |
| Meeting held | meeting outcome recorded | calendar/CRM event |
| Opportunity | human-owned opportunity created | opportunity ID |
| Won | verified commercial close | CRM contract/order evidence |

## Core metrics

Track counts and rates by source, niche, campaign, jurisdiction, number type, release version, and cohort: data-valid rate, duplicate rate, eligibility rate, answer rate, opt-out rate, complaint rate, qualification rate, accepted-handoff rate, meeting-book rate, show rate, opportunity rate, win rate, time-to-first-human, cost per qualified opportunity, cost per meeting, and cost per win.

Do not optimize for call duration or raw appointments if critical failures, complaints, no-shows, or false qualification increase.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[lead-generation-operating-system]]
- [[qa-scorecard]]
- [[observability-schema]]
- [[crm-pipeline-contract]]
