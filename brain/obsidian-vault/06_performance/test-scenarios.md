---
type: test
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Test scenarios

Create a test case for each scenario and record expected state, expected wording, expected disposition, and pass/fail evidence.

- owner is interested and books a demo;
- owner asks for a human;
- receptionist answers and offers a callback;
- rushed person says no;
- person asks “are you human?”;
- person asks to stop;
- consent is missing;
- consent is for email only;
- suppression service is unavailable;
- time zone is unknown;
- voicemail is reached;
- unsupported integration is requested;
- custom price or discount is requested;
- security or compliance question is asked;
- transfer destination is unavailable;
- wrong number is reported;
- agent encounters silence or interruption;
- technical failure occurs during booking; and
- prospect raises a complaint.

No release is live until every critical scenario passes.

## Detailed zero-hallucination prompts

Use [[zero-hallucination-test-cases]] for the exact prompt, expected state, allowed response pattern, forbidden behavior, and machine assertions for each critical fixture.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[03_call_playbook/call-flow]]
- [[05_operations/incident-runbook]]
