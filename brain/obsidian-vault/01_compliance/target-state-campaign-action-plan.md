---
type: decision
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Target-state campaign action plan

## Important input

**Target state: REQUIRED INPUT — not supplied yet.**

Do not invent the state. State law can materially change consent, caller identification, call windows, recording, DNC, privacy, and AI-disclosure requirements. Once Steve Anderson supplies the state or states, duplicate the matrix below per state and obtain campaign-specific counsel review.

## Current campaign status

**BLOCKED — planning only; no live dialing authorized.**

## Workstream plan

| Step | Workstream | Owner | Evidence required | Exit criterion | Status |
|---:|---|---|---|---|---|
| 1 | Name legal seller/entity and public brand | Steve Anderson | formation/brand record | caller identity is exact and approved | blocked |
| 2 | Name target state(s) and recipient-location method | Steve Anderson + counsel | jurisdiction decision | state matrix scope is fixed | blocked |
| 3 | Freeze lead source and number types | Operations | source contract/export + classification method | every lead has source, type, jurisdiction confidence | blocked |
| 4 | Approve consent basis and collection language | Counsel + Compliance | exact form/page/script and evidence sample | consent scope matches seller, purpose, channel, number, and AI voice | blocked |
| 5 | Build DNC/suppression propagation | Technical + Compliance | end-to-end test | opt-out blocks current and future attempts across vendors | blocked |
| 6 | Approve caller ID, callback, AI identity, and purpose wording | Counsel + Operations | approved copy + answered callback test | opening and opt-out behavior pass | blocked |
| 7 | Decide recording/transcription/monitoring | Counsel + Security | jurisdiction analysis + data-flow map | capture is lawful, minimized, secured, and deletable | blocked |
| 8 | Complete product/price/claim release | Product + Steve Anderson | capability evidence, price card, claim sources | no draft facts enter runtime | blocked |
| 9 | Configure dialer/CRM/calendar/handoff | Technical + Sales | vendor register, configs, test IDs | signed webhooks, idempotency, human acceptance, fallback | blocked |
| 10 | Run zero-hallucination test suite | QA + Knowledge | fixture results and traces | zero critical violations | blocked |
| 11 | Run security/vendor/restore/incident drills | Security + Technical | access review, restore log, tabletop | recovery and kill switch proven | blocked |
| 12 | Counsel signs exact campaign memo | Counsel | signed scope, assumptions, expiry | legal approval is current | blocked |
| 13 | Canary pilot with human monitoring | Operations | cohort, thresholds, incident log | pilot exits without critical failure | blocked |
| 14 | Approve expansion | Steve Anderson + owners | KPI/QA review | release gate and stop thresholds pass | blocked |

## Required legal matrix fields

For each state and campaign, record:

- covered number categories;
- recipient location method;
- AI/artificial/prerecorded voice treatment;
- consent standard and evidence;
- federal/state DNC and seller suppression;
- caller identity and callback rules;
- calling hours and holiday rules;
- opt-out/revocation behavior;
- recording/transcription/monitoring notice and consent;
- privacy notice, retention, deletion, and data-subject rights;
- penalties, private rights, regulator, and complaint route;
- source/effective date; and
- counsel interpretation, assumptions, and review date.

## No-go conditions

Do not dial when any required item is missing, stale, contradictory, or only supported by a generic legal database, public business listing, B2B label, vendor marketing page, or model answer.

## Pilot design

Use one state, one niche, one approved lead source, one offer release, one voice/campaign version, a small consented cohort, a human listening to every call, a closer on standby, a hard daily cap, and a pre-declared stop threshold. Do not add a second state or niche until the first passes QA, compliance, security, and economics review.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[jurisdiction-matrix]]
- [[legal-review-gate]]
- [[00_constitution/production-readiness]]
- [[06_performance/release-gate]]
