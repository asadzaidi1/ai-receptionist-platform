---
type: register
status: draft
authority: compliance
niche: general
compile: none
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Consent ledger specification

## Purpose

The consent ledger records **why a lead may be contacted, what channel and purpose were covered, what evidence supports that decision, and whether the permission has later been revoked or suppressed**.

It is the evidence layer behind `consent-gate`. It is not a simple `consent: true/false` field.

The ledger must support two separate questions:

1. **What happened?** The immutable history of consent, revocation, suppression, correction, and review events.
2. **May we dial now?** A derived decision calculated from the current event history, campaign rules, suppression checks, and jurisdiction controls.

The second question must never be answered by an agent prompt alone.

## System of record

The consent ledger must live in the controlled CRM, compliance database, or consent-management service used by the dialer. It must not live in the Obsidian vault.

Obsidian may contain this schema, field definitions, policies, review decisions, and synthetic examples. It must not contain:

- names of real prospects or customers;
- phone numbers or email addresses;
- consent screenshots or form submissions;
- call recordings or identifiable transcripts;
- IP addresses, device identifiers, or browser fingerprints;
- payment data;
- passwords, API keys, or access tokens; or
- raw exports from a lead source.

Store evidence in an access-controlled evidence store. The ledger should contain a stable evidence reference and cryptographic hash, not an unrestricted copy of the evidence.

## Design principles

1. **Append-only events:** never overwrite the historical fact that consent was granted or revoked.
2. **Derived status:** calculate the current dial decision from the event history and active rules.
3. **Purpose limitation:** consent for one seller, purpose, channel, or campaign does not automatically transfer to another.
4. **Channel specificity:** voice, AI voice, SMS, email, and recording are separate permissions unless counsel approves a broader definition.
5. **Number specificity:** bind the permission to the normalized number or an approved account-level identifier.
6. **Seller specificity:** record the legal entity and brand shown at collection.
7. **Evidence first:** every granted or claimed permission must point to evidence or an approved legal basis.
8. **Revocation wins:** a valid opt-out or suppression event overrides an earlier consent event.
9. **Fail closed:** missing, stale, contradictory, or unavailable data produces `DO_NOT_DIAL`.
10. **Least privilege:** agents can read only the minimum derived fields needed to make a call and handle an opt-out.

## Entities

Use three linked entities rather than one overloaded record:

### 1. Consent subject

A prospect or business contact represented by a stable internal identifier.

This entity may contain personal data in the CRM, but the consent service should expose a tokenized identifier to most systems.

### 2. Consent event

An immutable event stating that permission was granted, denied, revoked, expired, disputed, or otherwise changed.

### 3. Dial decision

A derived, time-bounded result such as `ALLOW_AI_VOICE`, `BLOCK_SUPPRESSION`, or `BLOCK_MISSING_EVIDENCE`. It must include the rule version and the inputs used to reach the decision.

## Consent subject fields

```text
subject_id                 stable internal ID; never reused
phone_token                tokenized or encrypted phone reference
phone_last4                optional display-only value for human review
number_type                mobile | residential | business | unknown
jurisdiction               state/territory/country when known
local_time_zone            IANA time zone when known
business_id                CRM business ID, if applicable
contact_role               owner | manager | employee | consumer | unknown
source_record_id           source-system record ID
created_at                 timestamp in UTC
updated_at                 timestamp in UTC
subject_data_status        active | corrected | deleted | restricted
```

Do not use the last four digits as an identity key. It is only a limited human-review aid.

## Consent event fields

Every event must have a unique immutable `event_id` and an event timestamp in UTC.

```text
event_id                   UUID or equivalent immutable ID
subject_id                 link to consent subject
event_type                 grant | deny | revoke | suppress | unsuppress |
                           expire | dispute | correction | legal_override |
                           review | import
occurred_at                when the event happened, UTC
recorded_at                when the system recorded it, UTC
recorded_by                system, agent, user, or integration ID
source_system              form, CRM, call, import, support, compliance, API
source_record_id           source event or lead ID
seller_legal_entity        exact seller/entity represented
brand_name                 exact brand represented
purpose                    plain-language intended purpose
campaign_id                campaign or acquisition flow
channel                    voice | ai_voice | sms | email | other
use_case                   marketing | service | appointment | callback |
                           account_related | other
consent_level              written | documented_other |
                           counsel_approved_exception | none | unknown
consent_text_version       version ID for the wording shown
consent_text_hash          hash of normalized wording, if available
collection_method          web_form | inbound_call | ad_form | demo_request |
                           written_agreement | import | verbal | other
collection_url_or_source   URL or source name, if applicable
evidence_ref               access-controlled evidence object reference
evidence_hash              cryptographic hash of evidence object
captured_at                when the person gave permission, UTC
expires_at                 explicit expiry, if one exists
jurisdiction_at_capture    known location/jurisdiction at capture
ai_voice_explicit          true | false | unknown
marketing_explicit         true | false | unknown
seller_explicit            true | false | unknown
number_explicit            true | false | unknown
frequency_terms            stated frequency or restrictions, if any
opt_out_method_shown       method shown at collection, if applicable
notes_code                 controlled code only; no free-form personal data
schema_version             ledger schema version
```

The fields `ai_voice_explicit`, `marketing_explicit`, `seller_explicit`, and `number_explicit` are evidence attributes. They do not by themselves prove legal sufficiency; counsel-approved campaign rules determine how they are used.

## Suppression and revocation fields

A suppression event must be recorded even if there was never a valid consent event. A person’s request not to be called is itself important operational evidence.

```text
suppression_id             immutable ID
subject_id                 link to subject
phone_token                tokenized number reference
suppression_type           internal_dnc | consumer_request | wrong_number |
                           complaint | legal_hold | carrier_block |
                           campaign_block | global_block
scope                      number | subject | business | campaign | seller | all_channels
channel_scope              voice | ai_voice | sms | email | all
reason_code                requested_stop | disputed_consent | wrong_number |
                           complaint | risk_review | other
requested_at               UTC timestamp
applied_at                 UTC timestamp
requested_via              live_call | voicemail | email | web | support |
                           import | other
source_event_id            link to originating event
requested_by               system or reviewer ID
active                     true | false
cleared_at                 only when lawfully cleared
cleared_by                 reviewer ID
clearance_basis_ref        approved evidence or decision reference
```

A suppression record must not be cleared merely because a campaign wants to call again. Clearance requires an approved basis, a documented review, and rules that permit clearance for that scope.

## Derived consent status

The operational system may expose a read-only summary to the dialer:

```text
consent_status              granted | not_granted | revoked | suppressed |
                            expired | disputed | unknown
ai_voice_status              allowed | not_allowed | unknown
marketing_status             allowed | not_allowed | unknown
internal_dnc_status          clear | blocked | unknown
external_dnc_status          clear | blocked | not_required | unknown
last_event_at                UTC timestamp
last_suppression_check_at    UTC timestamp
decision_expires_at          UTC timestamp, if a recheck is required
dial_decision                ALLOW_AI_VOICE | DO_NOT_DIAL | HUMAN_REVIEW
blocking_reason_code         controlled code
policy_version               consent policy version used
computed_at                  UTC timestamp
```

The dialer must not edit these fields. It may consume the result and write back the call-attempt event.

## Required decision logic

A simplified decision function is:

```text
if campaign is not approved for AI voice:
    DO_NOT_DIAL
elif subject or phone is missing or unresolved:
    DO_NOT_DIAL
elif active internal suppression exists:
    DO_NOT_DIAL
elif required external suppression check is blocked, stale, or unavailable:
    DO_NOT_DIAL
elif jurisdiction or local time zone is unknown:
    DO_NOT_DIAL
elif current time is outside the approved window:
    DO_NOT_DIAL
elif current consent status is revoked, suppressed, expired, disputed, or unknown:
    DO_NOT_DIAL
elif consent does not match seller, purpose, channel, number, or campaign rules:
    DO_NOT_DIAL
elif AI voice permission is not expressly allowed by the campaign rule:
    HUMAN_REVIEW or DO_NOT_DIAL
elif required disclosure or recording configuration is unavailable:
    DO_NOT_DIAL
else:
    ALLOW_AI_VOICE
```

Every decision must store the result, blocking reason, policy version, and the IDs/timestamps of the inputs checked. A later policy change must not erase how an earlier call decision was made.

## Consent matching rules

Before dialing, match the intended call against the event history on at least these dimensions:

- legal seller/entity;
- brand presented to the recipient;
- marketing purpose;
- voice channel;
- AI-generated voice use;
- phone number or approved account identifier;
- campaign and lead source;
- jurisdiction and number type; and
- any frequency or timing limitation.

If a field is not covered or the wording is ambiguous, treat it as not matched. Do not “fill the gap” with a broad interpretation.

Consent for a demo request may support a callback about that requested demo. It does not automatically authorize unrelated cold outreach, a different seller, a different channel, or a different product campaign.

## Event ordering and conflict rules

Use event timestamps from the source event, not only the time the event was imported. When timestamps conflict or an event arrives late:

1. preserve all events;
2. mark the subject for reconciliation;
3. apply the more protective status while unresolved; and
4. record the reconciliation decision and reviewer.

For operational dialing, an active suppression or revocation blocks the call even if a later import incorrectly suggests consent. A later consent may only be used after the suppression scope and validity are reviewed.

## Storage and security requirements

### Evidence store

Store raw consent proof in an encrypted, access-controlled evidence store with:

- immutable object ID;
- encryption at rest and in transit;
- restricted human access;
- audit logs for view, download, and deletion;
- malware scanning for uploaded files;
- retention and legal-hold support; and
- a cryptographic hash recorded in the ledger.

### Ledger database

The ledger database must support:

- append-only event creation;
- unique IDs and foreign-key relationships;
- UTC timestamps;
- encryption at rest and in transit;
- role-based access control;
- queryable suppression status;
- point-in-time reconstruction;
- audit logging;
- backups and restore testing; and
- export for lawful audit or dispute response.

### Access roles

Minimum roles:

- **Dialer:** read derived dial decision; write call-attempt outcome and opt-out event; no raw evidence access.
- **AI quality reviewer:** read redacted decision context; no unrestricted evidence download.
- **Compliance reviewer:** read ledger and evidence when necessary; create review and legal-override records.
- **System administrator:** manage infrastructure; cannot silently alter events.
- **Data subject request handler:** handle access, correction, or deletion requests under the approved privacy process.

No role may delete or rewrite an original consent or revocation event. Corrections create a new event linked to the original.

## Retention and deletion

Set final periods with counsel and the applicable campaign policy. At minimum:

- retain consent and suppression evidence for the period required by applicable law, contractual obligations, disputes, and legal holds;
- keep enough event history to explain every dial decision during the retention period;
- separate operational deletion from legal-hold preservation;
- delete or irreversibly anonymize data when the retention period expires and no hold applies; and
- record the deletion/anonymization event without retaining unnecessary personal data.

For covered telemarketing activity, current 16 CFR §310.5 generally requires five-year retention of specified records, subject to the rule’s applicability and exemptions. Treat five years as a covered-activity requirement, not as a universal rule for every B2B campaign or a substitute for counsel’s retention schedule. [1]

## Data quality and reconciliation checks

Run these checks before a campaign is activated and on a recurring schedule:

- every dialable subject has a non-unknown number type or an approved campaign rule;
- every allowed AI-voice decision points to a valid consent basis or approved exception;
- every evidence reference resolves and its hash matches;
- no active internal suppression is paired with `ALLOW_AI_VOICE`;
- consent seller and campaign match the active campaign;
- event timestamps are valid UTC values;
- no duplicate subject/phone tokens exist without a merge decision;
- external suppression checks are not stale;
- imports do not downgrade a suppression or revocation; and
- blocked decisions are visible in an exception queue.

Any failed check should fail closed for the affected record and create a review task.

## Synthetic example

The following is intentionally fictional and contains no real personal data:

```yaml
subject_id: SUBJ_example_001
phone_token: tok_phone_example_001
number_type: mobile
jurisdiction: US-CA
local_time_zone: America/Los_Angeles
consent_status: granted
ai_voice_status: allowed
marketing_status: allowed
internal_dnc_status: clear
external_dnc_status: clear
last_suppression_check_at: 2026-10-04T16:00:00Z
campaign_id: CAMPAIGN_demo_leads_v1
policy_version: v0.1
dial_decision: ALLOW_AI_VOICE
computed_at: 2026-10-04T16:00:02Z
```

This example is a schema illustration only. It is not evidence that a real person may be called.

## Launch acceptance tests

The consent-ledger implementation must pass these tests before the first live pilot:

- [ ] Missing consent produces `DO_NOT_DIAL`.
- [ ] Unknown number type produces `DO_NOT_DIAL` unless counsel-approved campaign logic explicitly handles it.
- [ ] Consent for email only does not allow AI voice.
- [ ] Consent for a different seller does not allow this seller’s call.
- [ ] Consent for a different purpose does not automatically allow this campaign.
- [ ] A revoked consent blocks a previously allowed number.
- [ ] A verbal “do not call” creates an immediate suppression event.
- [ ] Duplicate imports preserve the original event and do not create contradictory active grants without review.
- [ ] A stale external suppression check blocks dialing when the campaign requires a fresh check.
- [ ] Evidence hash mismatch blocks the call and creates an exception.
- [ ] The dialer can read the decision but cannot edit historical events.
- [ ] A correction creates a new linked event rather than rewriting history.
- [ ] Every allowed and blocked decision has a policy version and audit trail.
- [ ] Data deletion and legal-hold behavior have been tested.

## Source

- FCC, “Implications of Artificial Intelligence Technologies on Protecting Consumers from Unwanted Robocalls and Robotexts,” FCC 24-17: https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- FCC, “Implications of Artificial Intelligence Technologies on Protecting Consumers from Unwanted Robocalls and Robotexts”: https://www.fcc.gov/document/fcc-confirms-tcpa-applies-ai-technologies-generate-human-voices
- FTC, “Complying with the Telemarketing Sales Rule”: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, “FTC Implements New Protections for Businesses Against Telemarketing Fraud and Affirms Protections Against AI-enabled Scam Calls”: https://www.ftc.gov/news-events/news/press-releases/2024/03/ftc-implements-new-protections-businesses-against-telemarketing-fraud-affirms-protections-against-ai
- TODO: counsel-approved retention schedule, consent wording, state coverage, number classification rules, and data-subject request procedure.

## Related

- [[consent-gate]]
- [[_vault-guide]]
- [[00_constitution/never-say-list]]
- Planned: `opt-out-handling`, `ai-disclosure-wording`, `calling-hours`, `recording-consent`
