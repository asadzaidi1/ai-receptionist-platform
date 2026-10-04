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

# Recording and transcription consent

Recording, transcription, live monitoring, and quality review are separate data-processing decisions. Do not enable them merely because the telephony vendor makes them available.

Before a campaign records, document:

- every jurisdiction in scope;
- the notice and consent model;
- whether the notice is required before recording starts;
- where the recording and transcript are stored;
- who can access them;
- retention and deletion periods;
- redaction rules; and
- how a caller can request correction or deletion.

If the required notice or configuration is unavailable, the call must not be recorded. If the campaign cannot operate with recording disabled, return `DO_NOT_DIAL` until counsel approves the workflow. Never put identifiable recordings or transcripts in Obsidian.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[consent-gate]]
- [[consent-ledger-spec]]
- [[06_performance/qa-scorecard]]
