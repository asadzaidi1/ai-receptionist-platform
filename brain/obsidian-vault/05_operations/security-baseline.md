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

# Security baseline

## Identity and access

Use SSO/MFA, individual accounts, least privilege, separate dev/test/prod credentials, short-lived secrets, restricted service accounts, quarterly access review, and logged break-glass access. Never put API keys in prompts, Markdown notes, transcripts, or client-side code.

## Data and network

Encrypt data in transit and at rest. Separate tenants and environments. Restrict SIP endpoints, webhook origins, transfer targets, storage buckets, and database roles. Verify provider signatures. Use TLS and SRTP where supported.

## Agent boundary

Treat caller speech, retrieved text, CRM notes, and transcripts as untrusted. Allow only schema-validated tools. Redact secrets and unnecessary personal data. Block arbitrary exports, pricing changes, campaign creation, and external communications.

## Evidence

Log access, configuration changes, model/prompt/KB release, policy decisions, tool calls, suppression events, transfers, and incidents with correlation IDs. Protect logs and define retention/deletion. This baseline is a control framework, not a certification claim.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[tool-permission-matrix]]
- [[production-architecture]]
- [[incident-severity-matrix]]
