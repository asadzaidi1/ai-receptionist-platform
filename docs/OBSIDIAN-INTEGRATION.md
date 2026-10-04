# Obsidian, GitHub, and Antigravity integration

## Recommended model

```text
GitHub repository
  ├── brain/obsidian-vault/      ← Obsidian vault folder
  ├── apps/                      ← runtime code
  └── docs/config/tests/         ← engineering controls
```

Use GitHub as the shared versioned boundary. Open `brain/obsidian-vault/` as the Obsidian vault or sync it into the Obsidian workspace according to your preferred Git workflow. Antigravity should open the repository root, not only a loose copy of the Markdown files.

## Safe authoring loop

1. Pull the current `main` branch.
2. Create a branch for brain or code changes.
3. Edit policy/knowledge in Obsidian under `brain/obsidian-vault/`.
4. Keep YAML frontmatter and internal links intact.
5. Never add PII, raw lead files, consent screenshots, recordings, transcripts, or credentials.
6. Run vault validation and repository tests.
7. Review the diff.
8. Open a pull request.
9. Merge only after human approval.
10. Build a new runtime release manifest; do not hot-edit a live prompt.

## Runtime compilation boundary

The compiler should export only notes that are approved for runtime use. Each export must carry:

```text
brain_version
kb_release_id
policy_version
offer_version
script_version
campaign_id
source note IDs
source versions
scope/jurisdiction
expiry/review date
```

Nothing writes directly into the vault during a live call. Live outcomes become anonymized review inputs, then a human creates a draft note and a tested release.

## Antigravity prompt to use

> Open this repository as the canonical workspace. Read `AGENTS.md`, `README.md`, `docs/ARCHITECTURE.md`, and the relevant Obsidian notes before editing. Preserve all release gates. Work on a branch, add tests, run `make validate`, and do not use real credentials or live calling providers. Treat `brain/obsidian-vault/` as governed authoring, not a live database.
