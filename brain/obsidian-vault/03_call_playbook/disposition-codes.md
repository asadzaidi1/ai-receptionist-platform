---
type: register
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Disposition codes

Use exactly one primary final disposition per call.

| Code | Meaning | Required data |
|---|---|---|
| `CONNECTED_OWNER` | Owner/manager reached, no next step yet | role, summary |
| `CONNECTED_GATEKEEPER` | Staff member reached | role, callback path if given |
| `NO_ANSWER` | No person reached | attempt time |
| `VOICEMAIL_NO_MESSAGE` | Voicemail reached, no message left | attempt time |
| `WRONG_NUMBER` | Number is wrong or unrelated | source and correction if offered |
| `NOT_INTERESTED` | Explicit no | reason in their words |
| `CALLBACK_REQUESTED` | Specific callback agreed | time, time zone, number |
| `DEMO_BOOKED` | Demo scheduled | calendar event ID |
| `HUMAN_HANDOFF` | Live transfer completed | specialist and handoff packet |
| `DO_NOT_CALL` | Opt-out or suppression | suppression event ID |
| `OUT_OF_SCOPE` | Not an approved fit | reason |
| `COMPLIANCE_ESCALATION` | Rule or complaint issue | issue code |
| `TECHNICAL_FAILURE` | System or vendor failure | incident ID |

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[call-flow]]
- [[01_compliance/opt-out-handling]]
- [[04_prospects/call-sheet-fields]]
