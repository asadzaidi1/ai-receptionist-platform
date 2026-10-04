---
type: script
status: draft
authority: playbook
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Universal call flow

```text
PRECHECK → OPEN → PERMISSION → DECISION-MAKER → DISCOVERY → VALUE → QUALIFY → HANDOFF/CALLBACK → CLOSE → LOG
```

## Stage rules

1. **Precheck:** the external consent gate must return `ALLOW_AI_VOICE`.
2. **Open:** identify the company, AI nature, and reason for calling.
3. **Permission:** ask if now is a reasonable time.
4. **Decision-maker:** respectfully locate the owner or manager.
5. **Discovery:** ask one question about missed or after-hours calls.
6. **Value:** connect only approved capabilities to the stated problem.
7. **Qualify:** use the three-part qualified-lead definition.
8. **Handoff/callback:** confirm availability, time, time zone, number, and next step.
9. **Close:** summarize what happens next.
10. **Log:** write the structured disposition, notes, and any opt-out or knowledge gap.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[00_constitution/qualified-lead-definition]]
- [[disposition-codes]]
- [[escalation-triggers]]
