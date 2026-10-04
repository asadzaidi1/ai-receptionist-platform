# Target-State Campaign Launch Plan Template

Use this template when the user names a state or territory. Do not fill the state with an assumption.

## Campaign identity

- Target state: `TARGET_STATE`
- Legal seller/entity: `REQUIRED`
- Public brand: `REQUIRED`
- Caller identity: `REQUIRED`
- Callback number: `REQUIRED`
- Lead source: `REQUIRED`
- Campaign purpose: `REQUIRED`
- AI voice/dialing method: `REQUIRED`

## Workstreams

1. **State-law matrix:** definitions, covered numbers, consent, caller ID, DNC, calling hours, recording, AI disclosure, penalties, private rights, regulator, source/effective date.
2. **Federal overlay:** TCPA/FCC, FTC TSR, DNC, number type, artificial/prerecorded voice, consent, opt-out, recordkeeping.
3. **Consent evidence:** exact seller/purpose/channel/AI-voice scope, number binding, timestamp, source, wording/version, evidence hash, revocation.
4. **Data/recording:** audio/transcript notice, jurisdiction analysis, privacy notice, retention/deletion, vendors/subprocessors, rights handling.
5. **Dialer controls:** preflight gate, suppression propagation, local-time window, caller ID, signed webhooks, idempotency, rate limits, kill switch.
6. **Conversation controls:** approved claims, grounding, abstention, qualification, handoff acceptance, no-answer fallback, opt-out speech handling.
7. **Testing:** deterministic legal/state fixtures, red-team, noisy audio, barge-in, tool failure, wrong number, voicemail, duplicate/replayed events, rollback.
8. **Counsel sign-off:** scope, assumptions, exceptions, evidence, expiry/review date.

## Evidence required to clear the blocker

- Counsel-reviewed matrix and campaign memo.
- Consent form/page/snapshot and evidence sample.
- Suppression and opt-out end-to-end test.
- Caller-ID and callback verification.
- Recording/transcription decision.
- Vendor/security/DPA review.
- Release test results and canary plan.
- Named owner and restart authority.

## Stop conditions

Keep the campaign blocked when any required fact is unknown, stale, mismatched, or unsupported. Do not use a public business listing, B2B label, or generic legal database entry as a substitute for campaign-specific approval.
