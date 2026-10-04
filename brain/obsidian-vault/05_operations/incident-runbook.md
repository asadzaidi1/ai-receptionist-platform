---
type: incident
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Incident runbook

## Severity 1: compliance or harmful behavior

1. Pause the affected campaign immediately.
2. Preserve audit evidence and configuration versions.
3. Record the incident without editing the original events.
4. Notify the compliance and business owners.
5. Identify scope and affected records.
6. Correct, test, and approve before restart.

## Severity 2: material system failure

Pause or degrade to a safe mode when consent checks, suppression, identity, transfer, booking, or logging fails. Do not continue simply because calls can technically connect.

## Severity 3: quality issue

Tag the transcript, create a knowledge-gap or prompt-change request, add a regression test, and ship through the normal release process.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-gate]]
- [[campaign-rules]]
- [[06_performance/release-test-suite]]
