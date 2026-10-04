# Queue policy

## Decision precedence

Apply rules in this order:

1. **Active suppression or global do-not-contact:** `DO_NOT_CONTACT`.
2. **Invalid phone or duplicate contact conflict:** `DO_NOT_CONTACT`.
3. **Unknown/missing source permission, consent, number type, jurisdiction, or time zone:** `HUMAN_REVIEW_REQUIRED`.
4. **Stale or low-confidence data:** `HUMAN_REVIEW_REQUIRED`.
5. **Approved source, verified consent, approved business number type, current data, jurisdiction/time zone, and no suppression:** `CAMPAIGN_READY`.

## Queue meaning

### CAMPAIGN_READY

The record passed this deterministic pre-calling policy. It is ready for campaign review and a final dispatch-time eligibility check. It is not a command to place a call.

### HUMAN_REVIEW_REQUIRED

The record may be usable, but an accountable human must resolve missing, uncertain, stale, conflicting, or campaign-specific facts. Do not send it to an automated dialer.

### DO_NOT_CONTACT

Do not route the record to outreach. Preserve the reason and evidence. Active suppression must propagate across all seller campaigns and vendors.

## Required audit fields

Every decision must retain `lead_id`, source lineage, queue, reason, suppression match or null, policy version, decision timestamp, and dedupe key. A later change creates a new decision event; it does not erase the prior record.
