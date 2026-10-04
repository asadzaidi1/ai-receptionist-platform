---
type: metric
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# SLO, RTO, and RPO

Set targets before scale.

| Service | SLO target | RTO | RPO | Measurement | Owner |
|---|---|---|---|---|---|
| Consent gate | TODO | TODO | TODO | allow/block decision latency and error | compliance |
| Dial dispatch | TODO | TODO | TODO | successful eligible dispatch | operations |
| Voice runtime | TODO | TODO | TODO | session/audio health | technical |
| Handoff | TODO | TODO | TODO | accepted human handoff | sales |
| CRM eventing | TODO | TODO | TODO | complete/idempotent writes | technical |
| Evidence store | TODO | TODO | TODO | durable capture/retrieval | compliance |

SLOs are not permission to operate outside policy. If a dependency misses its threshold, the campaign pauses or moves to a safe human/callback mode.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[production-architecture]]
- [[incident-severity-matrix]]
- [[backup-and-restore]]
