# Phase 3: Calling-provider adapter and signed webhooks

Phase 3 adds a provider-neutral local adapter harness. It dispatches `PENDING` outbox records to a mock provider, persists provider responses, verifies HMAC-signed webhooks, applies idempotent state transitions, routes unknown/out-of-order events to reconciliation, and records audit events.

No network calls or real provider credentials are used.

## Outbound path

```text
PENDING provider_outbox
  → exact provider_idempotency_key
  → provider adapter
  → provider response persisted
  → call_sessions row created
  → CRM lead becomes DISPATCHED
  → audit event
```

A repeated dispatch request returns the existing provider call rather than creating another call.

## Webhook signature

The mock contract signs:

```text
signature = v1=HMAC_SHA256(secret, provider_timestamp + "." + raw_body)
```

The receiver verifies the raw body, timestamp skew, and constant-time signature equality before parsing or applying side effects. The default timestamp tolerance is five minutes.

Required headers:

```text
X-Provider-Timestamp
X-Provider-Signature
X-Provider-Event-Id (or event id in JSON)
```

## Webhook processing

1. Verify signature and timestamp.
2. Store the raw event before side effects.
3. Return the prior result for a duplicate provider event ID.
4. Resolve the provider call ID to a call session.
5. Apply only an allowed state transition.
6. Route unknown calls and out-of-order/terminal transitions to reconciliation.
7. Update CRM suppression state immediately on `call.opt_out`.
8. Store call event history and an audit event.

Call states:

```text
CREATED → RINGING → ANSWERED → COMPLETED
   └────→ FAILED
   └────→ OPTED_OUT
```

Terminal states are `COMPLETED`, `FAILED`, and `OPTED_OUT`.

## Run

```bash
cd /home/ubuntu/pre-calling-system
python3 -m pytest -q
```

The test suite uses `MockCallingProvider`, signed synthetic webhooks, replayed events, invalid signatures, stale timestamps, unknown calls, out-of-order transitions, opt-outs, and audit assertions.

The real provider integration must replace only the transport layer. It must retain the same idempotency key, raw-event receipt, signature verification, state machine, reconciliation path, and audit contract.
