---
type: guide
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Lead generation and conversion operating system

This is the canonical workflow for turning databases into qualified opportunities without bypassing compliance.

```text
SOURCE DATABASE
  → raw immutable import
  → normalize and deduplicate
  → verify business/contact/number/jurisdiction
  → consent and suppression gate
  → fit + intent + readiness scoring
  → campaign assignment and pacing
  → AI permission/opening/discovery
  → structured qualification
  → human handoff or verified booking
  → CRM opportunity
  → human discovery/proposal/close
  → QA, metrics, and reviewed learning
  → next brain release
```

## System boundaries

Obsidian stores schemas, rules, scripts, approved claims, campaign templates, tests, and release decisions. The raw database, CRM, consent ledger, dial queue, evidence store, calendar, closer queue, and analytics system store live operational data.

## Operating invariant

No raw record becomes a dial. No call becomes a qualified lead without confirmed evidence. No qualified lead becomes an opportunity without a next step and owner. No opportunity becomes won without human commercial ownership and verified CRM evidence.

## Daily control loop

1. Reconcile imports, duplicates, suppression, and failed events.
2. Recompute eligibility at dispatch.
3. Enforce campaign caps and local-time windows.
4. Review blocked/review-required records.
5. Monitor calls, opt-outs, complaints, hallucination failures, handoffs, and bookings.
6. Reconcile CRM, calendar, dialer, and consent events.
7. Review QA failures and create anonymized `_inbox` learnings.
8. Change the brain only through controlled release.

## Source

- Production lead-generation and conversion operating design, 2026-10-04.
- TODO: attach campaign-specific data-source, vendor, counsel, and pilot evidence before marking `live`.

## Related

- [[raw-lead-import-schema]]
- [[lead-eligibility-routing]]
- [[campaign-config-template]]
- [[crm-pipeline-contract]]
- [[conversion-funnel-metrics]]
- [[runtime-contract]]
