# Afiniti Pairing + CallAgentAI target benchmark

**Reviewed:** 2026-10-04

**Public sources:**

- https://www.afiniti.com/products/afiniti-pairing/
- https://callagentai.com/
- https://callagentai.com/features

This is a public capability benchmark. It does not verify vendor claims and does not copy proprietary code, prompts, models, customer data, branding, or implementation details.

## Target capability map

| Public capability theme | Target implementation in this platform |
|---|---|
| Customer-agent pairing | Preference-aware, constraint-first match recommendation after compliance/routing gates |
| Outcome optimization | Versioned outcome definitions, holdout/control groups, transparent KPI measurement |
| Inbound answering | 24/7 front-desk intake state machine with urgency and consent gates |
| Outbound follow-up | Bounded campaign/callback controller with dispatch-time rechecks |
| Smart routing | Route by skill, availability, SLA, language, niche, prior relationship, and approved preferences |
| Scheduling | Calendar availability, booking, confirmation, reschedule, cancellation, verified event IDs |
| Voicemail | Detection, approved message policy, transcription reference, task/follow-up rules |
| Transcription and summaries | Restricted transcript/recording store plus concise CRM note and evidence references |
| Multilingual voice | Approved language/voice profiles with explicit customer preference or campaign setting |
| CRM sync | Idempotent call, contact, lead, task, opportunity, suppression, and handoff updates |
| Follow-up automation | SMS/email/task triggers only after policy and permission checks |
| Custom triggers and APIs | Signed webhooks, event schemas, idempotency, retries, reconciliation, audit |
| Human handoff | Context-rich handoff packet with acceptance ID and SLA |
| Continuous tuning | QA labels → human approval → test → versioned release |
| Dashboard and analytics | Real-time operational metrics, searchable authorized metadata, control-group reporting |

## Preference-aware pairing model

The system must not replace compliance or routing with a score. It should work in this order:

```text
consent / suppression / jurisdiction / time / campaign gate
  → required operational constraints
  → eligible queue and skill routing
  → approved experience-preference match
  → explainable recommendation
  → human/provider assignment
  → outcome capture
```

### Allowed matching signals

Use only signals that are necessary, documented, approved, and available from a lawful/authorized source:

- requested language;
- explicitly selected voice or communication style;
- requested channel or callback window;
- service category or niche;
- urgency and SLA;
- required skill/certification;
- location/service coverage;
- availability;
- prior assigned representative or continuity preference;
- customer-stated accessibility preference;
- interaction purpose; and
- historical outcome data aggregated and reviewed for fairness.

### Prohibited or restricted signals

Never infer or use protected or highly sensitive traits for pairing or outbound targeting, including race, ethnicity, religion, health/disability beyond an explicitly necessary accessibility accommodation, gender identity, sexual orientation, political views, financial hardship, or other sensitive proxies. Do not use accent as a proxy for identity or desirability. Voice selection must be a customer-experience choice, not identity imitation.

Every recommendation must include reason codes, input provenance, model/version, confidence, and an override path. If the match is uncertain or materially affects access, route to human review.

## Inbound workflow target

```text
incoming call
  → signed provider event
  → caller/consent/suppression check
  → language/voice preference if explicitly provided
  → intent and urgency classification
  → required intake fields
  → constraint-first routing
  → experience match recommendation
  → intake / booking / transfer / work-order action
  → verified result
  → CRM + audit + dashboard
```

## Outbound workflow target

```text
eligible lead/callback task
  → dispatch-time recheck
  → purpose and scope confirmation
  → allowed time/language/channel preference
  → eligible agent/voice match
  → call attempt
  → answering-machine/voicemail handling
  → factual summary and disposition
  → CRM status + follow-up trigger
  → suppression/reconciliation/audit
```

Outbound must never rely on a match score as permission to call. Authorization comes from the consent/suppression/campaign gates.

## Release requirements

Before enabling a capability, add:

- schema and versioned configuration;
- positive and negative tests;
- prompt-injection and unsupported-claim tests;
- fairness and proxy review for matching signals;
- audit and idempotency coverage;
- human override and escalation path;
- control-group or holdout measurement where optimization is claimed;
- rollback plan; and
- campaign/jurisdiction approval.

## Product direction

Build a **governed AI contact-center operating layer**:

> answer every authorized inquiry, understand the purpose, route using explicit constraints and approved experience preferences, take only verified actions, synchronize every outcome, and improve through controlled evidence.
