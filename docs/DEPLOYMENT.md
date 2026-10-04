# Deployment and hosting

## What can be hosted from this repository

- Phase 1–4 Python services;
- staging database and test fixtures;
- read-only analytics dashboard;
- future provider adapter transport;
- CRM/consent integrations; and
- release/validation automation.

## What must not be hosted in Git

- API keys or OAuth tokens;
- production `.env` files;
- live SQLite databases;
- raw lead databases;
- phone numbers/emails;
- consent evidence;
- recordings/transcripts; or
- provider signing secrets.

Use the hosting platform's secret manager/environment variables. The current dashboard has no authentication and is suitable only for local/private staging until authentication, TLS, authorization, tenant isolation, and rate limits are implemented.

## GitHub Actions target

A future workflow should run on pull requests and `main`:

```text
checkout
→ Python setup
→ install requirements-dev
→ run pytest
→ run vault validator
→ run git diff / secret scan
→ build release manifest
→ publish only after review
```

## Hosting the dashboard

The dashboard is a read-only Python HTTP service. For a real deployment:

1. run it behind an authenticated reverse proxy;
2. use TLS;
3. restrict network access;
4. use a production database, not SQLite;
5. provide a secret manager and signed webhook endpoint;
6. add tenant isolation and authorization; and
7. monitor errors, provider lag, reconciliation, and audit-store health.

## Real provider onboarding

Do not replace the mock provider until the vendor supplies API, webhook, signature, idempotency, retry, recording, transfer, caller-ID, and data-processing documentation. Implement the vendor transport behind `provider_interface.py`; preserve the Phase 3 state machine and Phase 4 CRM/analytics contracts.
