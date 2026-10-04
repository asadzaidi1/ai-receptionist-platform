---
type: architecture
status: draft
authority: operations
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Experience matching and AI agent management

This note defines the target capability inspired by public descriptions of Afiniti Pairing and CallAgentAI. It is a planning benchmark, not a copy of proprietary implementation or a verification of vendor claims.

## Target

Support inbound and outbound operations with:

- constraint-first routing;
- approved customer experience preferences;
- specialized AI-agent roles;
- language and voice preferences;
- scheduling and rescheduling;
- voicemail/answering-machine handling;
- real-time transcription references and concise notes;
- CRM/task/opportunity synchronization;
- SMS/email/webhook triggers;
- human handoff acceptance;
- outcome analytics and control groups; and
- human-reviewed continuous calibration.

## Pairing order

```text
consent / suppression / jurisdiction / local time / campaign gate
  → skills / SLA / availability / coverage
  → explicit customer preference match
  → explainable recommendation
  → assignment or human review
  → outcome and fairness measurement
```

Matching never authorizes an outbound call. Never infer protected or sensitive traits. Do not use accent as an identity proxy. Keep recommendation reason codes, provenance, version, confidence, and override path.

## Inbound and outbound

Inbound calls use intake, urgency, intent, routing, scheduling, transfer, and verified action states. Outbound calls use campaign eligibility, purpose/scope, callback policy, customer preferences, answering-machine handling, retry limits, and suppression rechecks.

## Agent roles

Use bounded agents for front desk, qualification, scheduler, dispatch, customer updates, follow-up, CRM synchronization, and QA. Each has explicit tools, evidence requirements, escalation rules, and handoff acceptance.

## Required controls

The capability remains subject to [[consent-gate]], [[dnc-and-suppression-operations]], [[runtime-contract]], [[call-data-management-controller]], [[06_performance/release-gate]], and [[service-capability-benchmark]].
