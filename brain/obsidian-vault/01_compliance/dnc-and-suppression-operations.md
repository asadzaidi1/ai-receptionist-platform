---
type: rule
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# DNC and suppression operations

Run suppression as a centralized service, not a spreadsheet column. The service must accept opt-outs from AI calls, human closers, CRM users, vendors, support, email, and imports.

## Required behavior

- apply number-level suppression immediately;
- support person, business, seller, campaign, channel, and global scope;
- cancel queued retries, callbacks, transfers, and sequences;
- propagate to every dialer and closer queue;
- re-check at dispatch, not only at list import;
- preserve the event, source words, time, scope, and enforcement result; and
- alert when any downstream system fails to acknowledge the suppression.

Internal policy is stricter than the minimum legal timeline: the operating target is immediate suppression. A later consent event cannot silently erase an active stop request.

## Source

- Production-grade architecture review and current primary-source research, 2026-10-04.
- TODO: attach the exact organization, vendor, counsel, or pilot source before marking this note `live`.

## Related

- [[opt-out-handling]]
- [[consent-ledger-spec]]
- [[05_operations/webhook-idempotency]]
