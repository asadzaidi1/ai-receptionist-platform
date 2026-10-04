# Downstream calling-provider interface

Phase 2 stops at `provider_outbox`. It does not make network calls.

## Required sequence

```text
CRM staged lead
  → evaluate_dispatch()
  → persist dispatch_decisions audit row
  → BLOCKED outbox record OR PENDING outbox record
  → provider adapter reads PENDING only
  → provider create-call API with provider_idempotency_key
  → signed provider webhook
  → verify signature and event ID
  → update outbox and CRM state idempotently
```

## Provider request contract

```json
{
  "provider_idempotency_key": "provider:campaign_id:lead_id:brain_version",
  "lead_id": "lead_x",
  "campaign_id": "pilot_x",
  "brain_version": "brain-v1.3",
  "script_version": "script-v1",
  "policy_version": "dispatch-gate-v0.1"
}
```

The provider adapter must never receive a raw database row or the entire Obsidian vault. The request must reference an approved campaign release, and the provider must receive only the minimum data required for the call.

## Provider-side rules

- Send only `PENDING` outbox records.
- Use the exact `provider_idempotency_key`; do not generate a new key on retry.
- Treat timeout/unknown outcome as reconciliation, not permission to retry blindly.
- Do not announce a call, transfer, booking, or success from a request attempt alone.
- Verify signed webhook events and store the raw event before applying a state transition.
- Reject out-of-order or duplicate events into reconciliation/idempotency handling.
- A provider callback cannot change suppression or consent without the controlled operational path.

`src/provider_interface.py` contains the provider-neutral contract and an explicit no-live-provider implementation for this phase.
