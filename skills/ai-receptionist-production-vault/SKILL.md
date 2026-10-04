---
name: ai-receptionist-production-vault
description: Build, audit, and harden a production-grade Obsidian/Markdown operating system for AI receptionist outbound calling. Use for creating or upgrading lead ingestion, consent gates, call state machines, sales playbooks, telephony controls, CRM conversion workflows, QA/evaluation plans, governance, and target-state launch readiness.
---

# AI Receptionist Production Vault

Use this skill when a user wants to create or upgrade a governed knowledge vault for an AI voice receptionist, AI-assisted outbound sales operation, or database-to-lead-to-sale workflow.

## Core rule

Do not treat a large prompt or a folder of Markdown files as a production control system. Separate policy, knowledge, conversation, execution, data lineage, and assurance. The model may propose an answer or tool action; server-side policy must authorize it.

## Workflow

1. **Inspect the existing vault.** Inventory folders, metadata, naming, links, owner identity, lifecycle statuses, launch blockers, and current source notes.
2. **Preserve user work.** Work in a copy or new versioned package. Do not silently overwrite user-provided drafts.
3. **Research independently.** For broad upgrades, research outbound-call compliance; consent/privacy/retention; telephony/runtime; lead ingestion and verification; CRM/callback/handoff; security/reliability; QA/evaluation; sales/human closing; and knowledge/retrieval governance. Use primary sources and distinguish law from internal best practice.
4. **Build the control plane.** Add Constitution, authority/conflict order, owner identity, launch blockers, jurisdiction matrix, consent evidence standard, suppression operations, caller identity, and counsel review gate.
5. **Build the lead pipeline.** Keep raw imports immutable; normalize and deduplicate; verify business/contact/number/jurisdiction; route through compliance eligibility; score fit and explicit intent separately; assign campaigns; and preserve source-to-CRM lineage.
6. **Build deterministic conversation behavior.** Add an explicit state machine, transition guards, grounding/abstention policy, adversarial handling, tool permission matrix, qualification states, callbacks, and handoff acceptance.
7. **Build conversion operations.** Separate lead lifecycle, call disposition, handoff status, task/callback state, and opportunity stage. Add CRM contracts, bounded nurture, verified booking, human ownership, and funnel metrics.
8. **Build production operations.** Add architecture, webhook signature/idempotency rules, security baseline, vendor register, SLO/RTO/RPO, incident severity, backups, and recovery.
9. **Build assurance.** Add zero-hallucination prompts, lead-funnel tests, deterministic assertions, semantic evaluation, human audio review, observability schema, release gate, canary, rollback, and kill switch.
10. **Build the target-state action plan.** If the target state is missing, write `TARGET_STATE: REQUIRED INPUT`; never invent a state’s law. Include owner, evidence, dependency, exit criterion, and blocker status.
11. **Set identity consistently.** Use the user-approved pseudo-owner in metadata. Keep the legal seller/entity as a separate required launch input.
12. **Validate and package.** Check required files, Markdown metadata, internal links, owner identity, prohibited names, source register, no secrets/PII, lead lineage, CRM stages, state/evaluation controls, and launch-blocker notes. Run `scripts/validate_vault.py`. Package a versioned ZIP or vault copy and report whether it is a release candidate or authorized for launch.

## Lead-to-sale invariants

- No raw database record enters a dialer.
- Raw source rows remain immutable and every transformation has lineage.
- Verification proves data usability; it does not grant calling permission.
- Fit, intent, and readiness are separate; no score overrides suppression or eligibility.
- Eligibility is recomputed at dispatch.
- A connected call is not a qualified lead.
- A qualified lead is not a successful human handoff.
- A booked meeting requires a verified calendar event ID.
- A callback is a bounded task, not renewed consent for unrelated outreach.
- A won opportunity requires human commercial ownership and verified CRM evidence.

## Zero-hallucination invariants

Enforce these in the state machine and evaluation plan:

- Speak only from the active approved release.
- Require an evidence/source ID, source version, scope, and `allowed_for_agent: true` for every material answer.
- Do not convert unknown, stale, conflicting, unauthorized, or low-confidence facts into answers by paraphrasing.
- Permit no tool call without an allowlisted tool, schema-valid arguments, authorization, state guard, idempotency key, and audit event.
- Require confirmed fields for qualification and a positive human acceptance event for handoff success.
- Stop after opt-out, wrong-party stop, complaint, or safety trigger.
- Treat unsupported claims, invented details, hidden instructions, unauthorized actions, false success confirmations, cross-tenant retrieval, duplicate side effects, and lost source lineage as critical release failures.

## Vault conventions

Use Markdown with YAML frontmatter:

```yaml
---
type: rule
status: draft
authority: compliance
niche: general
compile: prompt
owner: APPROVED_PSEUDO_OWNER
version: v0.1
last_reviewed: YYYY-MM-DD
---
```

Keep personal data, consent proof, recordings, transcripts, credentials, raw lead files, and live call records outside Obsidian. Use Obsidian for governed authoring, schemas, policies, test cases, and release metadata; publish only approved snapshots to runtime retrieval.

## Legal handling

Never promise that a generic vault is legal to dial. Create a campaign-specific legal review gate covering seller identity, number type, recipient jurisdiction, purpose, AI/artificial voice, consent, DNC/suppression, caller ID, opt-out, call windows, recording/transcription, privacy, retention, and vendors. Treat B2B labels as insufficient by themselves. Cite authoritative sources near claims and label counsel decisions separately from general guidance.

## Target-state reference

When a target state is supplied, load `references/target-state-launch-plan.md` and fill the state-specific matrix. Keep the campaign blocked until the exact state/campaign memo is approved.

## Validation

Run:

```bash
python /home/ubuntu/skills/ai-receptionist-production-vault/scripts/validate_vault.py /path/to/brain
```

The validator must check structure, metadata, links, state-machine safety, zero-hallucination tests, release lineage, raw-to-dial prevention, separated CRM stages, negative lead-funnel paths, and interconnection. Fix all failures before delivery. The validator is a consistency check, not legal approval.

## Required final output

Deliver a versioned vault package or explicit changed files, a concise validation report, a target-state launch action plan, a statement of unresolved facts, and—when requested—the validated skill package itself.
