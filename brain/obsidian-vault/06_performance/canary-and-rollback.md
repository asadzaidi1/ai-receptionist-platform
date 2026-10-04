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

# Canary and rollback plan

Deploy a new brain, prompt, KB index, model, tool policy, or vendor configuration to a small approved cohort first. Keep the prior release immutable and immediately restorable.

Monitor quality, opt-outs, complaints, unsupported claims, gate blocks, dead air, transfer acceptance, CRM consistency, latency, errors, and call volume by release. Define stop thresholds before deployment.

Rollback must stop new dispatches for the new version, preserve in-flight calls safely, restore the last known-good policy/index/configuration, re-run suppression and consent checks, reconcile events, and record the incident/release decision. Never roll back by deleting evidence or replaying uncertain calls.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[release-gate]]
- [[production-architecture]]
- [[incident-severity-matrix]]
