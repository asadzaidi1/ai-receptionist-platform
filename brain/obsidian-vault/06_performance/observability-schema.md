---
type: register
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Observability and trace schema

Every attempt and session should be traceable with: `lead_id`, `call_id`, `provider_call_id`, `session_id`, `campaign_id`, `brain_version`, `script_version`, `offer_version`, `kb_release_id`, `policy_version`, `model_version`, `tenant_id`, `jurisdiction`, `number_type`, and `consent_decision_id`.

Capture timestamps for gate, dial, ringing, answer, media-ready, first agent audio, user turn, tool request/result, transfer requested/accepted, hangup, CRM write, suppression event, and final disposition.

Metrics: eligible/block rate, answer rate, first-audio latency, turn latency, dead air, interruption recovery, ASR/voice errors where available, tool errors, duplicate events, transfer acceptance, callback completion, opt-out latency, complaint rate, unsupported-claim rate, qualification accuracy, and campaign pause events.

Keep raw audio/transcript out of general logs. Use restricted references and redaction.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[production-architecture]]
- [[qa-scorecard]]
- [[01_compliance/consent-ledger-spec]]
