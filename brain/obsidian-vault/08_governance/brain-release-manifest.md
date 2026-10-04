---
type: register
status: draft
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Brain release manifest

This manifest makes the vault function as one governed brain without pretending that Obsidian is the live dialer or CRM.

## Release object

Every runtime release must have one immutable manifest:

```yaml
brain_version: TODO
source_revision: TODO
kb_release_id: TODO
prompt_release_id: TODO
policy_version: TODO
offer_version: TODO
script_version: TODO
campaign_id: TODO
niche: general
jurisdictions: []
approved_note_ids: []
retired_note_ids: []
chunk_count: TODO
build_hash: TODO
built_at_utc: TODO
approved_by: []
rollback_to: TODO
status: draft
```

## Export rules

1. Include only notes with `status: live` and complete metadata.
2. Exclude `## Source`, `## Related`, comments, TODO lines, personal data, secrets, and internal-only instructions from agent-facing exports.
3. Preserve source note ID, version, scope, owner, review date, and `allowed_for_agent` per chunk.
4. Apply tenant, campaign, niche, jurisdiction, and role filters before retrieval.
5. Reject expired, contradictory, draft, retired, unowned, or unverified content.
6. Atomically publish prompt, KB, policy, tool permissions, and evaluation references as one release.
7. Record the exact manifest ID in every call trace and CRM event.
8. Keep the previous release available for rollback and keep deleted content out of the active index.

## Interconnection map

```text
Constitution / compliance
        ↓ authorizes
Offer facts / claims / pricing
        ↓ constrains
Playbook / state machine / tools
        ↓ executes through
Campaign controller / dialer / CRM / calendar / closer queue
        ↓ produces
Events / traces / outcomes / QA reviews
        ↓ create reviewed changes in
_inbox → source registry → draft → review → live → release manifest
```

## Runtime boundary

Obsidian is the source-authoring and governance layer. The runtime must enforce consent, suppression, number/jurisdiction, state transitions, tool permissions, idempotency, audit logging, and human handoff in application code. A Markdown note cannot authorize a dial by itself.

## Release checklist

- [ ] Source revision is fixed.
- [ ] Approved notes and versions are enumerated.
- [ ] Draft/retired/expired content is excluded.
- [ ] Access/tenant filters are tested.
- [ ] Zero-hallucination suite passes.
- [ ] Tool/state/opt-out tests pass.
- [ ] Manifest is approved and hashed.
- [ ] Canary and rollback target are named.
- [ ] All runtime traces stamp this manifest ID.

## Related

- [[change-control]]
- [[source-registry]]
- [[data-classification]]
- [[03_call_playbook/agent-state-machine]]
- [[06_performance/evaluation-plan]]
- [[06_performance/release-gate]]
