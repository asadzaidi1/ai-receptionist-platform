---
type: guide
status: live
authority: constitution
niche: general
compile: none
owner: Steve Anderson
version: v1.1
last_reviewed: 2026-10-04
---

# Vault Guide: Start Here

This vault is the **brain** of our AI receptionist sales operation. It holds what the calling agent *knows*, what it must *never do*, and how we improve it. It does **not** hold what the agent *did*: leads, call records and consent proof live in the CRM (the sheet or database that records leads and calls).

One principle sits above every rule below: **we only do what is legal, legitimate, and good for the customer.** If a note conflicts with that, the note is wrong.

## 1. Golden rules

1. **One fact, one home.** Prices, capabilities and approved claims each live in exactly one note. Everywhere else links to it or embeds it (`![[price-card]]`). Never copy and paste a fact.
2. **Closed world.** If it isn't in a note with `status: live`, the agent doesn't say it. Unknown means "good question, a specialist will cover that," plus a logged gap.
3. **Compliance outranks everything.** See the conflict order in section 4.
4. **Write for the ear.** Agent-facing text is spoken language: short sentences, plain words, one idea per answer.
5. **No header, no publish.** Every note carries the property header from section 3.
6. **No personal data in the vault.** See section 10.
7. **Nothing goes live without review, a changelog line and a test.**

## 2. Folder map

| Folder | The question it answers | What lives here |
|---|---|---|
| `00_constitution` | Who are we, and what do we never do? | One-job statement, definition of a qualified lead, never-say list, persona and AI-disclosure line, value rules |
| `01_compliance` | Am I allowed to make or continue this call? | Consent gate, calling-rule checklists, opt-out handling, disclosure and recording-notice wording, consent-ledger spec |
| `02_offer` | What are we selling, and what's true about it? | Product overview, price card, capabilities register, approved claims, FAQs, security and privacy answers |
| `03_call_playbook` | What do I say next? | Call flow, openers, discovery questions, objections, gatekeeper protocol, voicemail policy, escalation triggers, warm-transfer script |
| `04_prospects` | Who am I calling, and how do they think? | Ideal customer profile, personas, lead scoring, call-sheet fields, niche-pack template |
| `05_operations` | How does the machine run, and what happens when it breaks? | Roles, campaign rules, handoff SLA, tool map, incident playbooks, client onboarding template, launch checklist |
| `06_performance` | Is it working, and what do we change? | KPIs, QA scorecard, test scenarios, review notes, A/B test log |
| `07_niche_packs` | What differs for this industry? | One subfolder per niche (dental, salon, and so on), cloned from the template; only the differences |
| `08_governance` | How is the brain controlled? | Source registry, change control, data classification, backup, and vendor governance |

Outside the numbered folders:

- `_inbox/` holds raw learnings, drafts and ideas. It is never exported. Triage it weekly.
- `_templates/` holds note templates.
- `_changelog.md` records every live change, newest first.
- `_vault-guide.md` is this file.

## 2A. Production-grade extension

`08_governance` is mandatory for production. The owner identity is **Steve Anderson**. Legal seller identity, public brand, jurisdictions, vendors, consent sources, and counsel approvals remain separate launch inputs and must not be invented in notes.

## 3. Note header

Every note starts with this block:

```yaml
---
type: faq
status: draft
authority: offer
niche: general
compile: kb
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---
```

| Field | Allowed values | Meaning |
|---|---|---|
| `type` | guide, rule, script, faq, objection, persona, trigger, register, decision, learning, metric, test, incident, template | What kind of note it is |
| `status` | draft, review, live, retired | Lifecycle stage. Only `live` is exported |
| `authority` | compliance, constitution, offer, playbook, reference | Who wins a conflict (see section 4) |
| `niche` | `general`, or a niche name such as `dental` | Where the note applies |
| `compile` | prompt, kb, none | Where it goes on export: the live prompt, the knowledge base, or nowhere |
| `owner` | a name | Who is accountable for its accuracy |
| `version` | `vMAJOR.MINOR`, such as `v1.2` | Minor for wording changes; major when the meaning changes (a rule, price, claim or trigger). Kept as text so `v0.10` never collapses into `0.1` |
| `last_reviewed` | `YYYY-MM-DD` | The last day the owner confirmed it is still true |

No free-form tags. These properties are our taxonomy.

## 4. Conflict order

When two notes disagree, the higher one wins and the lower one is fixed the same day:

**compliance, then constitution, then offer, then playbook, then reference.**

A niche note can specialize a general note but can never override anything above its own level. When the agent is unsure, it never improvises: it hands the call to a human.

## 5. Naming and linking

- File names are lowercase with hyphens and no spaces (`price-card.md`). One topic per note, and every name is unique across the vault.
- Link with `[[wikilinks]]`. Link each objection to its proof point and rule, and each script to the rules it obeys. End every note with `## Source` (where its facts come from) and `## Related`.
- Use embeds (`![[note]]`) only for single-source facts such as prices, capabilities and approved claims. Obsidian shows them live, and the export step expands them.
- Keep Dataview queries out of live notes. Dashboards live in `06_performance`.

## 6. Writing agent-facing notes

- **`compile: kb` notes:** one question or topic per heading, answered in one to three short sentences (roughly 50 words). When natural, end with a question that moves the call forward.
- **`compile: prompt` notes:** the total across the vault stays under about 1,500 words, because every call carries them. We will tune this number after test calls.
- Write prices and numbers the way they are spoken ("two hundred dollars").
- Anything uncertain gets a `TODO:` line, and a note with a TODO cannot go live.

## 7. Lifecycle and going live

Notes move `draft`, `review`, `live`, `retired`. We never delete; we retire and keep the history.

A note goes `live` only when:

1. The header is complete, the file name follows the convention, and `## Source` says where the facts come from.
2. Its backlinks and related notes are checked, and nothing conflicts with a higher authority.
3. Anything the agent says to a prospect (scripts, prices, claims) has been checked by the compliance reviewer.
4. It has been tested on the closest scenarios in `06_performance` (once those exist).
5. `version` is bumped, `last_reviewed` is set, and one line is added to `_changelog.md` in the format `v0.1, 2026-10-04, what changed`. The newest line is the **brain version**: bump its major number when a rule, price, claim or trigger changes, and the minor number otherwise. `v0.x` means no real call has been made yet; `v1.0` is the first version that takes real calls.

Review cadence: compliance, price card, capabilities and claims every 30 days; everything else every 90. Live edits ship in one weekly batch, except compliance fixes, which ship immediately.

## 8. How knowledge gets in

- **Written from templates**, by us or drafted by an AI and then reviewed.
- **Learned from calls.** A lesson enters `_inbox` as a short note: what happened, what we would change, and the evidence, with identifying details removed. Weekly triage promotes it through the lifecycle above, merges it into an existing note, or discards it.
- Nothing writes into the vault during a call. The agent's call notes go to the CRM.

## 9. Export to the calling agent

Only `status: live` notes are exported.

- `compile: prompt` notes are assembled into the agent's live prompt.
- `compile: kb` notes are uploaded to the agent's knowledge base.
- `compile: none` notes stay here.

Embeds are expanded before export. Comments (`%% ... %%`), queries, `TODO` lines and everything from `## Source` downward are stripped. Phase 1 is a manual upload. Once the structure is stable, a script replaces it. Every call record in the CRM carries the brain version, so any change in results can be traced to a specific edit.

## 10. What never goes in the vault

Lead or customer names, phone numbers and emails; call recordings and transcripts with identifying details; consent proof; payment details; passwords and API keys. These belong in the CRM or a password manager.

## 11. Rules for AI assistants editing this vault

- Start every new note from `_templates/note-template`, with `status: draft`.
- Never invent prices, features, legal rules or statistics. If something is unknown, write `TODO:` and say so.
- Don't edit a `live` note unless asked. Propose the change and the changelog line instead.
- Obey the conflict order. If a request would break a higher-authority note, say so before writing.

## 12. One-time Obsidian setup

1. Create a folder for the vault (for example `Documents/brain`) and open it in Obsidian with "Open folder as vault."
2. Settings, Files and links: Wikilinks on, Automatically update internal links on, and Default location for new notes set to "In the folder specified below" with `_inbox`.
3. Settings, Core plugins: turn on Templates (set the template folder to `_templates`), Backlinks and Properties view. Bases is optional for dashboards.
4. Settings, Community plugins: turn on community plugins, then install **Dataview** for dashboards and, later, **Obsidian Git** for version history.
5. Create the folders from section 2, `_changelog.md` and `_templates/note-template.md`.
6. Back up the vault folder from day one, with cloud sync or Git.
7. To start a note, create it in the right folder, run the command "Templates: Insert template", pick `note-template`, and replace every `CHOOSE`.

## 13. Build order

We build file by file, in this order, with a changelog line after each step.

1. This guide.
2. `note-template` and the folder skeleton.
3. `00_constitution`: `one-job-statement`, `qualified-lead-definition`, `never-say-list`, `value-rules`.
4. `01_compliance`: `consent-gate`, `consent-ledger-spec`, `opt-out-handling`, `ai-disclosure-wording`.
5. `02_offer`: `price-card`, `capabilities-register`, `approved-claims`, product overview and FAQs.
6. `03_call_playbook`: `call-flow`, `escalation-triggers`, `gatekeeper-protocol`, objections, voicemail policy.
7. `04_prospects`: ideal customer profile, `call-sheet-fields`, niche-pack template.
8. `05_operations` and `06_performance`: onboarding template, incident playbooks, KPIs, QA scorecard, test scenarios.
9. The first niche pack in `07_niche_packs`, then dry runs and a pilot.

## Source

- Our own design decisions, 2026-10-04.

## Related

- [[_changelog]]
