

## VOICE-AGENT USE-CASE AND ORCHESTRATION EXTENSION

Use voice automation first for documented, frequent, low-ambiguity workflows with known fields, verifiable outcomes, and a human fallback. Prefer human escalation for high-emotion complaints, legal threats, safety-critical uncertainty, vulnerable-person situations, undocumented exceptions, and disputes requiring discretion.

A single call may use multiple bounded specialists while preserving one shared context. The orchestrator must track current state, caller context, active specialist, allowed tools, handoff reason, pending action, timeout/retry policy, evidence, confidence, and human escalation state. Do not create transfer loops or make the caller repeat verified information.

When an agent cannot complete a step, it must state only what is known, preserve context, create a bounded human handoff or callback task, provide an approved next step, and audit the failure. Never fabricate a confirmation to hide an orchestration failure.

Use staged rollout:

```text
Foundation: inbound + transcription + lawful recording + basic messages
Growth: outbound + follow-up + CRM sync + voicemail handling
Pro: multilingual + preference matching + specialist orchestration
Enterprise: multi-tenant scale + control groups + SLAs + redundancy
```

A capability moves to the next stage only after tests, pilot evidence, monitoring, cost controls, canary results, rollback readiness, and human ownership are documented. Tier labels are internal roadmap labels, not vendor pricing claims.
