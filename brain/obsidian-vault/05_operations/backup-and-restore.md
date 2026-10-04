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

# Backup and restore plan

Back up vault source, production release artifacts, consent/suppression evidence, campaign configuration, audit logs, and critical CRM state according to their separate retention and access rules. Encrypt backups, separate backup credentials, restrict deletion, and test restores on a schedule.

A restore test must rebuild a known-good release, recover consent/suppression decisions, verify version lineage, and prove that the system will not replay uncertain calls. Maintain a clean export path if a vendor fails or the account is locked.

Obsidian Sync history and Git history are conveniences, not the only backup. Record restore date, scope, result, gaps, and owner.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[production-architecture]]
- [[vendor-risk-register]]
- [[slo-rto-rpo]]
