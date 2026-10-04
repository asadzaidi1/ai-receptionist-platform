# Unified architecture

## System of record boundaries

| Concern | System of record | Obsidian/GitHub role |
|---|---|---|
| Policy, scripts, approved claims, tests | Obsidian vault in GitHub | authoring, review, release |
| Raw leads and source lineage | controlled database/CRM | schema and import rules |
| Consent/suppression evidence | consent service/CRM | policy and evidence schema |
| Lead lifecycle/opportunity | CRM | state contract and mappings |
| Provider call/media events | calling provider + evidence store | adapter contract and tests |
| Analytics | operational database/analytics layer | metric definitions and dashboard code |
| Credentials/secrets | secret manager/environment | never committed |

## Runtime flow

```text
Obsidian note change
  → Git branch / review
  → metadata + link + validator checks
  → approved brain release manifest
  → runtime knowledge/policy snapshot

Raw database
  → immutable import
  → normalize/dedupe
  → verify
  → consent/suppression gate
  → fit/intent/readiness routing
  → CAMPAIGN_READY staging CRM
  → dispatch-time recheck
  → provider outbox
  → provider adapter
  → signed webhook
  → call state machine
  → CRM status sync
  → audit + reconciliation
  → dashboard / QA
```

## Obsidian architecture

`brain/obsidian-vault/` is organized into:

- `00_constitution`: authority, identity, value rules, release blockers;
- `01_compliance`: consent, suppression, jurisdiction, disclosure, recording, legal gates;
- `02_offer`: product, claims, price, capabilities, privacy/security;
- `03_call_playbook`: state machine, grounding, tools, discovery, objections, handoffs;
- `04_prospects`: raw import schema, verification, routing, scoring, lifecycle;
- `05_operations`: campaigns, CRM, nurture, handoff, runtime, vendors, security;
- `06_performance`: tests, metrics, QA, canary, rollback, observability;
- `07_niche_packs`: niche-specific activation controls; and
- `08_governance`: data classification, change control, source registry, release manifest.

## Security model

Only approved, minimal release artifacts reach runtime. Personal data, consent proof, recordings, transcripts, credentials, and live call records remain outside the vault. Every side effect carries correlation IDs, versions, actor identity, authorization, and idempotency.

## Failure model

The system fails closed for missing/unknown consent, suppression, jurisdiction, number type, time window, caller identity, provider readiness, or release integrity. It fails safe for provider timeouts, duplicate events, out-of-order events, CRM outages, calendar outages, and reconciliation uncertainty.
