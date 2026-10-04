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

# Raw lead import schema

Keep the original source immutable and create a normalized working record. Never send raw database rows directly to a dialer.

## Required fields

| Field | Required | Rule |
|---|---|---|
| `source_id` | yes | original database and row reference |
| `source_acquired_at` | yes | UTC timestamp |
| `company_name` | yes | normalized legal/trading name |
| `domain` | preferred | canonical website/domain |
| `industry` | yes | controlled taxonomy |
| `location` | yes | business and likely recipient location separately |
| `contact_name` | optional | do not infer identity |
| `contact_role` | optional | confirmed or unconfirmed |
| `phone_token` | preferred | tokenized reference; full number stays in CRM/consent service |
| `email_token` | optional | tokenized reference |
| `source_permission` | yes | documented source and permitted use |
| `source_date` | yes | freshness |
| `raw_confidence` | yes | high/medium/low |
| `raw_payload_ref` | yes | restricted storage reference |

## Immutable rule

Never overwrite the raw record. Each transformation creates a new version with `transform_id`, `transformed_at_utc`, `transformer_version`, and `reason`. Preserve lineage from source row to CRM lead and campaign attempt.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[data-cleaning-dedupe]]
- [[lead-verification-workflow]]
- [[runtime-contract]]
- [[call-sheet-fields]]
