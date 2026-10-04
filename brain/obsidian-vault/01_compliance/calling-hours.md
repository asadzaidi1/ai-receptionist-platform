---
type: rule
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Calling hours and time zones

The dialer must calculate calling time from the recipient’s best-known jurisdiction and local time zone, not the agent’s location.

## Required fields

- jurisdiction or state;
- IANA time zone;
- time-zone confidence;
- approved campaign window;
- daylight-saving handling; and
- last time-zone verification.

If jurisdiction or time zone is unknown, return `DO_NOT_DIAL`. Do not hard-code one national window as the universal rule. Counsel must approve the state and campaign schedule, including holidays, emergency exceptions, existing-customer callbacks, and any stricter internal policy.

The scheduler must re-check the local time immediately before placing the call and record the result in the audit event.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[launch-checklist]]
