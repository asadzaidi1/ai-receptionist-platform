# Next implementation process

## Immediate repository step

- Choose **private** or **public** GitHub visibility. Private is the recommended default because the repository contains business operating logic.
- Enable/authorize the GitHub connector or use your approved GitHub workflow.
- Create the new repository and push the prepared tree.
- Connect Antigravity to the repository root.

## Pre-calling pilot

1. Select one niche and one target jurisdiction.
2. Provide the legal seller/entity and public brand.
3. Connect one approved lead source.
4. Keep raw data in a controlled operational store.
5. Run the Phase 1 import/dedupe/suppression pipeline.
6. Stage only `CAMPAIGN_READY` leads.
7. Manually review a small real cohort.
8. Do not call yet.

## Calling-provider pilot

1. Select a provider with API, signed webhooks, idempotency, opt-out, caller ID, recording, and audit support.
2. Configure secrets outside GitHub.
3. Implement the transport adapter only.
4. Run synthetic provider events.
5. Test timeout, duplicate, stale, out-of-order, opt-out, and reconciliation paths.
6. Obtain campaign-specific counsel approval.
7. Run a small human-monitored canary.
8. Pause automatically on critical failures.

## Required business inputs

```text
Target state:
Legal seller/entity:
Public brand:
Niche:
Offer and approved price:
Lead source and permission basis:
CRM:
Consent/suppression service:
Calling provider:
Caller ID:
Callback/handoff destination:
Calendar:
Recording/transcription policy:
Daily pilot cap:
Human reviewer/closer:
```

## Current unresolved items

The code is a validated production candidate. It is not live-authorized because the target state, seller identity, lead source, consent evidence, CRM/provider accounts, caller identity, and campaign legal memo have not been supplied.
