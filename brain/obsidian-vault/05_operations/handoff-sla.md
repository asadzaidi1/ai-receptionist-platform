---
type: rule
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Human handoff SLA

Use [[crm-pipeline-contract]] and [[follow-up-and-nurture]]. A transfer request is not a successful handoff. The closer must accept and receive the context packet.

| Event | Target | Failure action |
|---|---|---|
| Warm transfer pickup | REQUIRED | fallback callback only with agreement |
| Callback confirmation | REQUIRED | notify owner and reconcile |
| Qualified lead review | REQUIRED | escalate queue |
| Compliance escalation | immediate | pause affected campaign |

The packet must include contact role, problem, impact, current process, confirmed qualification fields, unknowns, objections, requested next step, consent/suppression status, call ID, and release IDs. Never pass unsupported AI inferences as facts.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[03_call_playbook/warm-transfer-script]]
- [[03_call_playbook/callback-protocol]]
- [[campaign-rules]]
