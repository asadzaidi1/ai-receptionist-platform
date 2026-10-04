# HireBexa public-service benchmark

**Reviewed:** 2026-10-04
**Source:** https://hirebexa.ai/

This is a product-positioning benchmark based only on publicly visible website content. It is not a legal, technical, performance, or financial verification of HireBexa’s claims, and it does not copy proprietary prompts, code, workflows, customer data, or branding.

## Publicly visible service themes

HireBexa presents a done-for-you AI business automation service with:

- 24/7 front-desk call intake and qualification;
- capture of caller details and needs;
- priority/SLA handoffs;
- multiple specialized operational agents;
- direct CRM/ledger dispatch language;
- configurable brand voice and communication style;
- scheduling and next-step progression;
- domain-specific trade/service workflows;
- real-time telemetry and ingestion;
- searchable transcripts and call logs;
- recordings and playback;
- immediate handoffs and operational updates;
- human account-management and continuous calibration;
- edge-case testing before live deployment; and
- ROI/revenue-recovery positioning.

The website also displays numerical performance, latency, accuracy, ROI, and simulated/live-dispatch claims. Treat those as vendor marketing claims unless independently validated; do not copy them into our approved claims or use them in customer conversations without evidence and legal review.

## What our platform already has

- governed Obsidian operating brain;
- consent/suppression and dispatch-time gates;
- lead import, normalization, deduplication, and queue classification;
- staging CRM;
- provider-neutral idempotent outbox;
- signed webhook verification;
- call state machine;
- reconciliation queue;
- automated CRM status synchronization;
- audit history;
- read-only analytics dashboard;
- deterministic tests and zero-hallucination controls; and
- GitHub/Antigravity release workflow.

## Capabilities to add for a comparable service

### 1. Service-intake layer

Add configurable intake workflows for each niche:

```text
inbound call
  → caller identity / consent / urgency check
  → reason-for-call classification
  → required field capture
  → emergency/safety triage
  → availability / scheduling
  → verified handoff or work-order creation
```

The workflow must remain deterministic for safety-critical, pricing, warranty, dispatch, and booking actions.

### 2. Specialized-agent orchestration

Implement separate bounded roles rather than one unrestricted agent:

- front desk/intake;
- qualification;
- scheduler;
- dispatch coordinator;
- customer update agent;
- billing/RMA intake;
- follow-up controller; and
- QA/compliance reviewer.

Each role needs a tool-permission matrix, evidence requirements, escalation policy, and handoff schema.

### 3. Verified handoff packet

Every handoff should include:

```text
handoff_id
source_call_id
lead/customer ID
reason and urgency
facts stated by caller
unknowns
safety/compliance flags
requested next step
assigned human/team
accepted_at_utc
acceptance_actor
SLA due time
```

A proposed handoff is not a completed handoff. The receiving system or human must acknowledge it.

### 4. Searchable call intelligence

Extend the call record with restricted references to:

- recording;
- transcript;
- short summary;
- extracted entities;
- disposition;
- work-order/opportunity ID;
- follow-up task ID;
- handoff ID;
- evidence confidence; and
- retention/consent policy version.

Store sensitive artifacts outside Obsidian and Git. The dashboard should search metadata and authorized transcript indexes without exposing raw data to unauthorized users.

### 5. Continuous calibration

Create a controlled review loop:

```text
call/event
  → QA scorecard
  → edge-case label
  → human approval
  → draft workflow/note change
  → test scenario
  → release gate
  → versioned runtime deployment
```

No live prompt or policy should change directly from an unreviewed call.

### 6. Vertical service packs

For each niche, create a versioned pack containing:

- intake fields;
- urgency/safety rules;
- approved claims;
- pricing boundaries;
- scheduling rules;
- dispatch matrix;
- escalation triggers;
- voicemail/callback policy;
- required CRM fields;
- test calls and edge cases; and
- launch/canary evidence.

## Strategic recommendation

Position the platform as a **governed AI receptionist and operations layer**, not merely a voicebot:

> Capture every inquiry, qualify only with evidence, create the correct next step, synchronize the CRM, and keep every handoff auditable.

The strongest differentiators should be governance, evidence-bound behavior, consent/suppression safety, transparent handoffs, niche-specific workflow packs, and measurable operational outcomes—not unverified latency or ROI numbers.

## Related implementation files

- `docs/CALL-DATA-MANAGEMENT-PROMPT.md`
- `docs/ARCHITECTURE.md`
- `docs/NEXT-STEPS.md`
- `brain/obsidian-vault/05_operations/call-data-management-controller.md`
