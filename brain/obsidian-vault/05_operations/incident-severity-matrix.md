---
type: incident
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Incident severity matrix

| Severity | Example | Immediate action | Notify | Restart authority |
|---|---|---|---|---|
| SEV-0 | unauthorized calls, suppression failure, credential compromise, cross-tenant disclosure | kill campaign/egress, preserve evidence | owner, compliance, security, vendor | Steve Anderson + compliance |
| SEV-1 | wrong disclosure, unsafe claim, repeated transfer failure, material data loss | pause affected campaign, triage scope | owner and responsible lead | operations + owner |
| SEV-2 | elevated errors, dead air, webhook backlog, degraded QA | reduce/pause, repair, monitor | operations/technical | technical owner |
| SEV-3 | isolated quality defect with no material impact | ticket, test, scheduled release | QA/knowledge owner | release owner |

Every incident has detection time, scope, affected versions, containment, evidence, notifications, root cause, corrective action, regression test, and restart approval. Do not delete or rewrite original events.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[incident-runbook]]
- [[security-baseline]]
- [[release-gate]]
