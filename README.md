# AI Receptionist Platform

**Steve Anderson — GitHub-canonical, Obsidian-governed pre-calling and calling-operations platform.**

This repository consolidates the validated Phase 1–4 system:

```text
Obsidian brain
  → lead import / dedupe / suppression
  → CAMPAIGN_READY staging CRM
  → dispatch-time eligibility gate
  → provider outbox
  → signed provider webhooks
  → CRM call-status synchronization
  → audit history / reconciliation
  → real-time operations dashboard
```

## Main operating instruction

> **GitHub is the canonical engineering and release repository. Obsidian is the governed authoring brain. Antigravity may implement changes, but must never bypass the release gates, modify production data directly, expose secrets/PII, or connect a live calling provider without campaign approval.**

Every change must:

1. be made in a Git branch;
2. preserve Obsidian note metadata and internal links;
3. pass the unified tests and vault validator;
4. update the appropriate version/manifest/docs;
5. be reviewed before merge to `main`; and
6. never commit credentials, consent evidence, recordings, transcripts, phone numbers, emails, or live databases.

## Repository map

```text
brain/obsidian-vault/        governed Markdown brain; upload/copy into Obsidian
apps/pre-calling-system/     Phases 1–4 Python implementation and tests
config/                      redacted campaign/provider examples only
docs/                        architecture, Obsidian, deployment, roadmap
AGENTS.md                    operating instructions for Antigravity/Gemini IDE
Makefile                     repeatable validation commands
tools/                       repository checks and release helpers
```

## Quick start

```bash
cd apps/pre-calling-system
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

Expected result: all Phase 1–4 tests pass. The test fixtures are synthetic and no live calling provider is contacted.

## Run the local dashboard

Seed a local demo database using the Phase 1–4 smoke workflow described in `docs/DEPLOYMENT.md`, then:

```bash
python3 apps/pre-calling-system/src/dashboard_server.py \
  --db apps/pre-calling-system/run/phase4.db \
  --host 127.0.0.1 --port 8765
```

The dashboard is read-only. It cannot authorize calls.

## Obsidian workflow

Use `brain/obsidian-vault/` as the versioned export/import boundary. Keep live records and sensitive evidence outside Obsidian. Only reviewed, approved notes enter runtime releases. See `docs/OBSIDIAN-INTEGRATION.md`.

## Current deployment status

This repository is **production-candidate infrastructure**, not authorization for live outbound calling. Real deployment still needs campaign-specific legal approval, consent/suppression services, CRM/provider credentials, caller identity, target jurisdiction, monitoring, and a human-supervised pilot.

## Next process

1. Decide GitHub repository visibility: private is the safe default.
2. Enable/authorize the GitHub connector in Manus or use your approved GitHub workflow.
3. Create the new repository and push this exact tree.
4. Connect Antigravity to the repository and `brain/obsidian-vault/`.
5. Run the synthetic tests in Antigravity.
6. Replace only the staging input adapters with approved CRM/data sources.
7. Validate a small real dataset without calling.
8. Choose a calling provider and implement its transport/webhook adapter.
9. Run a human-monitored canary only after the campaign gate is approved.
