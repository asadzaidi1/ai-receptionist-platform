---
type: guide
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Runtime contract

The “one brain” is a coordinated system, not a single file. Obsidian governs what the agent may know and say; operational services govern what is happening now.

## System ownership

| Concern | Authoritative system | Obsidian role |
|---|---|---|
| Lead/account/contact | CRM | schema and policy |
| Consent/suppression | consent service/CRM | rules and evidence schema |
| Dial eligibility | policy service | gate definition |
| Call state/media | telephony/runtime | architecture and test contract |
| Calendar availability | calendar system | booking rules |
| Human handoff | closer queue/telephony | SLA and packet definition |
| Audio/transcript evidence | restricted evidence store | retention and access policy |
| Knowledge/policy | Obsidian + release pipeline | authoring and approval |
| QA/metrics | analytics/evaluation system | rubric and test definitions |

## Required write path

Every runtime write must pass authentication, authorization, schema validation, state guard, idempotency, and audit logging. The agent cannot write directly to arbitrary files or databases.

## Required read path

Every material answer must come from the active campaign release, with scope and evidence metadata. Retrieval must enforce tenant, niche, jurisdiction, role, status, and expiry before content reaches the model.

## Safe degradation

If Obsidian sync, release index, policy service, CRM, calendar, telephony, human queue, or audit store is unhealthy, stop new side effects or use an approved fallback. Never let a degraded dependency cause the agent to improvise, bypass suppression, or announce unverified success.

## Interconnection test

A release is functionally connected only when a synthetic lead can be traced through:

```text
lead → eligibility → consent/suppression → dial → agent session → evidence retrieval
→ tool authorization → callback/demo/handoff → CRM outcome → trace → QA review
→ reviewed knowledge gap → draft note → approved release → next test
```

The test must preserve the same lead/call/release correlation IDs at every step.
