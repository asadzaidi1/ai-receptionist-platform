---
type: register
status: draft
authority: playbook
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Call sheet fields

The CRM or call platform captures structured records, not only a transcript. Use [[crm-pipeline-contract]] as the data contract.

```text
lead_id, source_id, transform_id, campaign_id, brain_version, policy_version, call_id, started_at, ended_at,
business_name, contact_name, contact_role, phone_token, number_type, jurisdiction, time_zone,
source_permission, consent_decision, suppression_decision, eligibility_decision, eligibility_evidence_ref,
fit_score, intent_score, readiness_tier, opening_completed, permission_state, decision_maker_reached,
problem_in_own_words, current_process, business_impact, desired_outcome, timeline, budget_status,
qualification_evidence_ids, interest_level, objection_code, questions, callback_at, demo_at, calendar_event_id,
handoff_status, human_acceptance_id, primary_disposition, opt_out, knowledge_gap_id, incident_id,
recording_ref, transcript_ref, reviewer_status, opportunity_id, owner_id, next_step, next_step_due_at
```

Use controlled values. Keep full numbers, email addresses, recordings, transcripts, consent proof, and sensitive data outside this vault.

## Source

- Initial operating design, 2026-10-04.
- TODO: attach the authoritative product, counsel, vendor, or pilot source before setting `status: live`.

## Related

- [[01_compliance/consent-ledger-spec]]
- [[03_call_playbook/disposition-codes]]
- [[06_performance/qa-scorecard]]
