# GitHub operations

## Repository target

Recommended name: `ai-receptionist-platform`

Recommended visibility: **private** until the business logic, campaign rules, provider configuration, and ownership decisions are finalized. A public repository can expose proprietary operating logic even if secrets are excluded.

## First push

From the repository root:

```bash
git remote add origin https://github.com/<github-owner>/ai-receptionist-platform.git
git push -u origin main
```

Use the approved GitHub connector or your authenticated Antigravity/GitHub workflow. Never paste tokens into the remote URL, shell history, Markdown, or chat.

## Branch protections

After the repository is created:

- protect `main`;
- require pull requests;
- require the validation workflow to pass;
- require at least one human review;
- disable force pushes;
- enable secret scanning/push protection if available; and
- restrict deployment credentials to protected environments.

## Suggested GitHub Actions workflow

```text
pull_request:
  checkout
  install Python 3.11+
  install apps/pre-calling-system/requirements-dev.txt
  run pytest
  run vault validator
  run git diff --check
  run secret scan

main:
  repeat checks
  build a release artifact
  publish only from an approved tag/environment
```

## What Antigravity should clone/open

Open the repository root so it can read:

- `AGENTS.md`;
- `README.md`;
- `docs/ARCHITECTURE.md`;
- `docs/OBSIDIAN-INTEGRATION.md`;
- `brain/obsidian-vault/`; and
- `apps/pre-calling-system/`.

Do not give an AI coding tool a production `.env`, raw lead database, consent evidence, recordings, transcripts, or provider secret.
