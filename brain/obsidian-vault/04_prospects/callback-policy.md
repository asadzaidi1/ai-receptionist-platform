---
type: rule
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Callback policy

A callback is a bounded task with a purpose, owner, number, date, local time zone, evidence of the request, retry limit, expiry, and suppression re-check. It is not renewed consent for unrelated marketing.

At execution, re-run the consent/suppression gate, verify the number, check the local time, confirm the request scope, and cancel if the person opted out, the number is wrong, or the request expired. Use an idempotency key so retries cannot create duplicate calls.

If the callback cannot be completed after the approved attempts, close it with a reason rather than retrying indefinitely.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[consent-gate]]
- [[dnc-and-suppression-operations]]
- [[03_call_playbook/callback-protocol]]
