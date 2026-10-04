---
type: register
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Tool permission matrix

The model never calls vendors directly. Application middleware validates every tool request.

| Tool | Agent permission | Server checks | Human approval |
|---|---|---|---|
| Read approved FAQ | read | active release, scope | no |
| Read price card | read | live row, campaign | no |
| Create callback task | propose | consent/scope, time zone, suppression, dedupe | campaign policy |
| Book demo | propose | calendar availability, required fields, duplicate check | campaign policy |
| Warm transfer | request | allowlisted destination, closer availability, consent | no if policy passes |
| Modify pricing | none | blocked | required |
| Send contract/refund | none | blocked | required |
| Change suppression | event only | immediate audit, scoped event | no |
| Start a new campaign | none | blocked | required |

Validate schema, authorization, target, idempotency key, and state transition server-side. Keep secrets outside the model context.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[agent-state-machine]]
- [[01_compliance/dnc-and-suppression-operations]]
- [[05_operations/webhook-idempotency]]
