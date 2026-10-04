---
type: register
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Tool map and system ownership

| Capability | System of record | Read by agent | Written by agent | Owner |
|---|---|---|---|---|
| Knowledge and policy | Obsidian release/export | compiled prompt/KB | no | knowledge owner |
| Leads and contacts | CRM | approved fields | outcome fields | operations |
| Consent and suppression | compliance database | derived decision | opt-out event | compliance |
| Calling | telephony platform | campaign config | call event | technical owner |
| Scheduling | calendar/booking system | availability | event request | operations |
| Transcript/recording | secured evidence store | no by default | reference only | compliance |
| Reporting | analytics store | no | metrics events | performance |

Replace the generic system names only after the actual vendors, APIs, data owners, and retention settings are confirmed.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-ledger-spec]]
- [[04_prospects/call-sheet-fields]]
