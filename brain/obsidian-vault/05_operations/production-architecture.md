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

# Production architecture

```text
Lead source / CRM
        ↓
Identity + dedupe + number classification
        ↓
Consent / jurisdiction / DNC / time-window gate
        ↓
Campaign controller + pacing + kill switch
        ↓
Telephony provider / SIP or media bridge
        ↓
Realtime agent runtime
  ├─ approved KB snapshot
  ├─ deterministic policy engine
  ├─ allowlisted tools
  └─ trace and event collector
        ↓
Human closer queue / calendar / callback
        ↓
CRM outcome + QA + analytics + incident queue
```

The model is not the controller. The controller authorizes the call, tools, transition, and release. Every component carries `lead_id`, `call_id`, `provider_call_id`, `session_id`, `campaign_id`, `brain_version`, `offer_version`, `script_version`, and `kb_release_id`.

Use signed webhooks, idempotent event handling, bounded retries, circuit breakers, rate limits, dead-letter queues, and a safe pause when policy, CRM, telephony, or human handoff is unhealthy.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[tool-map]]
- [[webhook-idempotency]]
- [[security-baseline]]
- [[03_call_playbook/tool-permission-matrix]]
