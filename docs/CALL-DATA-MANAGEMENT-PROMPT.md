

## SERVICE-OPERATIONS EXTENSION

When this platform is used as a 24/7 front desk or service-operations layer, add these controls:

### Intake and triage

Capture only the approved fields for the active niche. Classify the reason for contact, urgency, safety signal, requested service, location scope, availability, and next step. Do not provide safety-critical instructions, pricing, warranty decisions, or dispatch promises unless the active release contains an approved rule and the required evidence.

### Specialized bounded workers

Use separate bounded roles for intake, qualification, scheduling, dispatch coordination, customer updates, billing/RMA intake, follow-up, and QA. Each role must have an explicit tool-permission matrix and must hand off when the request exceeds its evidence or authority.

### Verified handoff packet

For every proposed handoff create:

```json
{
  "handoff_id": "string",
  "source_call_id": "string",
  "lead_or_customer_id": "string",
  "reason": "string",
  "urgency": "string",
  "facts": [],
  "unknowns": [],
  "safety_or_compliance_flags": [],
  "requested_next_step": "string",
  "assigned_team_or_human": "string",
  "sla_due_at_utc": "ISO-8601 UTC",
  "acceptance_required": true,
  "acceptance_id": "string|null"
}
```

A proposed handoff is not completed until the receiving human/system returns a verified acceptance ID. Never tell a caller that someone has been dispatched, a booking is confirmed, or a transfer succeeded without that evidence.

### Restricted call intelligence

Link authorized recording/transcript references, extracted entities, summary, disposition, work-order/opportunity ID, follow-up ID, handoff ID, confidence, retention policy, and consent policy to the call record. Keep recordings, transcripts, phone numbers, emails, and consent evidence in the approved restricted store—not Obsidian, Git, or a public dashboard.

### Human calibration loop

Route QA findings and edge cases through:

```text
call/event → QA label → human approval → draft workflow change → test scenario → release gate → versioned deployment
```

Never alter a live prompt, policy, price, warranty rule, dispatch matrix, or approved claim directly from an unreviewed call.
