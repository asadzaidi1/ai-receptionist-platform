# Vapi playbook benchmark

**Reviewed:** 2026-10-04
**Source:** https://vapi.ai/playbook/strategy#chapter-2-where-voice-agents-work
**Additional planning input:** user-provided feature-tier screenshot

This document uses Vapi’s public playbook as a strategy benchmark. It does not copy proprietary implementation, prompts, code, or vendor claims.

## Public strategic lessons

The playbook explains that voice agents improve on rigid IVR because they can understand meaning, ask clarifying questions, handle multi-step workflows, and take action. It also emphasizes that production failures are usually operational: wrong use-case selection, undocumented rules, high-emotion situations, exception-heavy workflows, missing monitoring, weak handoffs, and lack of rollback.

The platform should therefore treat voice as a controlled operations system, not as an unrestricted conversational model.

## Where voice agents fit well

Use voice agents first where the process is frequent, rules are documented, required fields are known, outcomes are verifiable, and a clear human fallback exists:

| Use-case class | Initial policy |
|---|---|
| Intake and qualification | Good candidate; capture fields and route with evidence |
| Scheduling/rescheduling | Good candidate with calendar event verification |
| Appointment reminders | Good candidate with consent and opt-out controls |
| Status checks | Good candidate when source-of-truth data is available |
| Routine support | Candidate when knowledge and escalation rules are stable |
| Outbound follow-up | Candidate only with consent/campaign/dispatch gates |
| High-value handoff | Candidate for preparation; human acceptance required |

## Where the system should prefer humans

Escalate or stop automation for high-emotion complaints, threats, legal issues, safety-critical uncertainty, ambiguous policy, exceptions outside the documented playbook, disputes requiring discretion, vulnerable-person situations, and any request where a human would materially change the outcome.

A polite script is not a substitute for human judgment.

## Production architecture lessons

### One conversation, multiple bounded capabilities

A single call can require intake, qualification, scheduling, billing context, and support. The system may maintain one caller context while invoking bounded specialist tools or sub-agents. It must not create a transfer loop or lose context.

### Orchestration is a first-class system

The orchestrator owns:

- current call state;
- caller context;
- active specialist;
- allowed tools;
- handoff reason;
- pending action;
- retry/timeout policy;
- confidence and evidence;
- human escalation; and
- recovery after component failure.

### Safe fallback

When an agent cannot complete a step, it must:

1. state what is known without inventing;
2. preserve the context and evidence;
3. create a human handoff or bounded callback task;
4. provide the caller with only an approved next step; and
5. audit the failure and reason.

### Operational readiness

Production requires monitoring, debugging, cost controls, versioned prompts/policies, canary release, rollback, provider-health checks, transcript/recording retention controls, and a reconciliation queue.

## Tiered capability roadmap

The supplied feature comparison suggests this staged implementation:

| Tier | Capabilities | Release condition |
|---|---|---|
| Foundation | Inbound calls, real-time transcription, recording where lawful, basic SMS/email triggers | Intake, consent, retention, audit, and human fallback validated |
| Growth | Outbound calls, follow-ups, CRM/task sync, analytics, voicemail/answering-machine handling | Campaign, suppression, retry, and dispatch controls validated |
| Pro | Multilingual voices, language preferences, experience-aware matching, specialist orchestration | Preference provenance, fairness review, language QA, and handoff tests validated |
| Enterprise | Multi-tenant orchestration, high-volume routing, control groups, SLAs, advanced observability, provider redundancy | Security, isolation, SLOs, incident response, rollback, and operational ownership validated |

The tier names are internal roadmap labels, not a claim about any vendor’s pricing or product availability.

## Target call loop

```text
caller speaks
  → speech recognition
  → state/context update
  → bounded reasoning
  → approved tool/action
  → verified result
  → natural response
  → event/audit/CRM update
```

The loop must have latency budgets, but latency never overrides safety, verification, or the handoff gate.

## Product rule

> Start with narrow, high-volume, low-ambiguity workflows. Expand only after evidence shows the agent handles variance safely.

## Related implementation

- `docs/ARCHITECTURE.md`
- `docs/AFINITI-CALLAGENTAI-TARGET.md`
- `docs/CALL-DATA-MANAGEMENT-PROMPT.md`
- `docs/NEXT-STEPS.md`
- `brain/obsidian-vault/05_operations/experience-matching-and-agent-management.md`
