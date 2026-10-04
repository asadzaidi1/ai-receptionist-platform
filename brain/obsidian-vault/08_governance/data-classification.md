---
type: rule
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Data classification and handling

| Class | Examples | Allowed locations | Controls |
|---|---|---|---|
| Public | approved public marketing copy | public site, approved KB | source/version |
| Internal | playbooks, metrics, release notes | private vault/repo | access control |
| Confidential | pricing drafts, vendor terms, campaign configs | restricted systems | least privilege, audit |
| Restricted | phone/email, consent proof, recordings, transcripts, credentials | secured CRM/evidence/secret manager | encryption, strict roles, retention, redaction |

Restricted data must never enter general Markdown, prompts, error logs, screenshots, or test fixtures unless synthetic or redacted. Derived lead scores and summaries inherit the most restrictive applicable classification. Review exports and backups under the same policy.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[security-baseline]]
- [[consent-ledger-spec]]
- [[backup-and-restore]]
