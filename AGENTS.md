# Antigravity / Gemini implementation contract

## Mission

Maintain and extend this AI receptionist platform as a governed, testable system for Steve Anderson. The repository is the engineering source of truth; the Obsidian vault is the policy and knowledge authoring source.

## Non-negotiable controls

- Never place a live call from a test, dashboard, notebook, prompt, or migration script.
- Never bypass `CAMPAIGN_READY`, the dispatch-time gate, suppression, consent, local-time, caller-identity, or provider-readiness checks.
- Never treat a high lead score as permission to contact.
- Never announce a transfer, booking, or provider success without a verified event.
- Never remove or weaken an opt-out/suppression record automatically.
- Never commit secrets, API keys, credentials, PII, phone numbers, emails, recordings, transcripts, consent evidence, or live database files.
- Never write directly into the Obsidian vault during a call.
- Never use a draft/retired/restricted note in a runtime release.

## Change workflow

1. Read the relevant code, schema, test, and Obsidian notes before editing.
2. Create a branch named `feature/<short-name>` or `fix/<short-name>`.
3. Make the smallest coherent change.
4. Add or update deterministic tests before claiming completion.
5. Run `cd apps/pre-calling-system && python3 -m pytest -q`.
6. Run the vault validator from the reusable skill against `brain/obsidian-vault`.
7. Run `make validate` from the repository root.
8. Update `docs/`, phase notes, and release metadata when behavior changes.
9. Review `git diff --check` and `git status --short`.
10. Open a pull request; merge only after review.

## Obsidian release rules

- `brain/obsidian-vault/` contains governed Markdown, not live data.
- Preserve YAML frontmatter, owner identity `Steve Anderson`, internal links, source registers, and launch blockers.
- A runtime release must include `brain_version`, `kb_release_id`, `policy_version`, `offer_version`, `script_version`, and `campaign_id`.
- Conflicting, stale, unknown, or unauthorized knowledge must abstain rather than become a plausible answer.

## Provider rules

- Outbound requests use the exact provider idempotency key.
- Webhooks require raw-body signature verification, timestamp freshness, event-ID deduplication, and audit logging.
- Unknown, duplicate, out-of-order, or terminal-state events go to reconciliation or return the prior result.
- The dashboard is read-only.

## Required completion report

Report: files changed, tests run and results, vault validation result, unresolved campaign inputs, whether the change is production-candidate or live-approved, and the exact branch/commit/PR.
