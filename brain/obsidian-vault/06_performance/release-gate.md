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

# Production release gate

A release is approved only when all applicable checks pass:

- [ ] source notes are owned, sourced, current, and approved;
- [ ] no draft, retired, expired, or restricted note enters the production index;
- [ ] consent, DNC, disclosure, recording, and identity tests pass;
- [ ] no fabricated claim, unauthorized tool, or illegal state transition is observed;
- [ ] retrieval grounding, access filtering, stale-note, conflict, and prompt-injection tests pass;
- [ ] deterministic state, webhook idempotency, transfer acceptance, and CRM reconciliation tests pass;
- [ ] audio, interruption, latency, voicemail, and provider-failure tests pass;
- [ ] canary plan, monitoring, kill switch, rollback, and incident contacts are ready;
- [ ] release IDs are stamped into calls and CRM events;
- [ ] counsel/business/security owners approve material changes; and
- [ ] launch blockers in `production-readiness` are cleared with evidence.

Any critical compliance, privacy, security, identity, suppression, or state-integrity failure blocks release regardless of conversion rate.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[evaluation-plan]]
- [[canary-and-rollback]]
- [[00_constitution/production-readiness]]
