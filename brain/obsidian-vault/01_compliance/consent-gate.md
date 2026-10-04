---
type: rule
status: draft
authority: compliance
niche: general
compile: prompt
owner: Steve Anderson
version: v0.1
last_reviewed: 2026-10-04
---

# Consent gate

## Purpose

This note defines the conditions that must be satisfied **before the AI voice agent may place an outbound marketing call**. It is an operational control, not a substitute for a written review by qualified U.S. telecom and privacy counsel.

The dialer or eligibility service must enforce this gate in code. The voice prompt must not be the only place where these rules exist.

## Default rule

> **If a required field is missing, stale, contradictory, or unknown, do not dial.**

The safe result is `DO_NOT_DIAL` until a qualified reviewer resolves the issue and the lead record is updated.

## What this gate covers

This gate applies to outbound calls that use an AI-generated or artificial voice to market the AI receptionist, qualify a prospect, book a demo, request a callback, or transfer a sales opportunity.

It applies regardless of whether the intended recipient is:

- a consumer;
- a business owner;
- a manager;
- a receptionist or other employee; or
- a number described as a business line.

Do not assume that a business-to-business label removes TCPA, FCC, state, privacy, carrier, or platform obligations. A large number of small-business owners and managers answer calls on mobile or residential numbers.

## Legal baseline used for this design

The FCC has stated that AI technologies that generate human voices fall within the TCPA restrictions on “artificial or prerecorded voice” calls. The FCC’s ruling says that calls using these technologies require prior express consent of the called party unless an applicable emergency purpose or exemption applies. The ruling also requires identification/disclosure information and specified opt-out methods when the message includes advertising or constitutes telemarketing. [1]

The FTC states that most business-to-business calls are generally exempt from the core Telemarketing Sales Rule, but the exemption has limits. The FTC’s current guidance also addresses National Do Not Call requirements, misrepresentations, and recordkeeping. [2]

The FTC’s 2024 update expanded protections against deceptive and abusive practices in business-to-business telemarketing and added recordkeeping requirements, including call-detail, consent, and Do Not Call compliance records. [3]

Our internal launch standard is therefore more conservative than “call unless somebody proves it is prohibited.” For AI voice marketing, require documented consent or a written, campaign-specific legal approval for an exception.

## Pre-dial decision sequence

The operational system must evaluate these checks in order:

```text
1. Is this campaign approved for AI voice?
   No → DO_NOT_DIAL

2. Is the number valid, reachable, and classified?
   No or unknown → DO_NOT_DIAL

3. Is the recipient’s jurisdiction and time zone known?
   No → DO_NOT_DIAL

4. Is there a current internal do-not-call or suppression match?
   Yes → DO_NOT_DIAL

5. Is the number on a required external suppression list for this campaign?
   Yes or check unavailable → DO_NOT_DIAL

6. Is there documented consent or a counsel-approved exception?
   No or unknown → DO_NOT_DIAL

7. Does the consent match this seller, purpose, channel, number, and AI-voice use?
   No or unclear → DO_NOT_DIAL

8. Is the call within the approved jurisdiction-specific time window?
   No or unknown → DO_NOT_DIAL

9. Are the caller identity, disclosure, opt-out path, and recording configuration approved?
   No → DO_NOT_DIAL

10. Is the human handoff/callback path operational if the prospect requests it?
    No → DO_NOT_DIAL or use an approved no-transfer campaign

11. All checks pass → DIAL and attach the brain version and campaign version
```

## Consent standard

For consumer, residential, and mobile numbers, the default standard for an AI voice marketing call is **documented prior express written consent** that is specific enough to show:

- who is receiving the consent;
- the phone number or number class covered;
- that the person agreed to receive calls about the relevant product or service;
- that an automated, artificial, or AI-generated voice may be used when applicable;
- how the consent was collected;
- the date and time of consent;
- the source page, form, advertisement, or interaction;
- the disclosure shown to the person; and
- any stated terms, frequency, or opt-out language.

A generic statement such as “I agree to marketing” is not automatically sufficient for this campaign. Counsel must confirm whether the actual consent language and collection flow are adequate.

For business numbers, the system must still record the number classification, the basis for calling, the campaign approval, and the suppression checks. Do not use “B2B” as a consent value. If the campaign relies on a B2B or other legal theory rather than documented consent, that theory must be written, approved for the exact campaign, and stored in the compliance register.

## Minimum consent-ledger fields

The consent ledger belongs in the CRM or compliance database, not in this Obsidian vault and not in the agent prompt. Each dialable lead must have:

```text
lead_id
phone_number_or_token
number_type: mobile | residential | business | unknown
business_name
contact_name_and_role_if_known
jurisdiction
local_time_zone
consent_status: written | other_documented | counsel_approved_exception | unknown | revoked
consent_collected_at
consent_source
consent_language_or_snapshot_reference
seller_identity_shown
purpose_shown
ai_voice_disclosure_shown
proof_location
last_suppression_check_at
internal_dnc_status
external_dnc_status_if_required
last_opt_out_at
campaign_id
campaign_version
reviewer_and_reviewed_at
```

Do not place names, phone numbers, emails, consent screenshots, recordings, transcripts, or other personal data in this vault. This note defines the schema; the evidence stays in the controlled operational system.

## Hard-stop conditions

Return `DO_NOT_DIAL` when any of these is true:

- consent status is unknown, missing, expired under the campaign policy, or contradictory;
- consent evidence cannot be retrieved;
- consent names a different seller, brand, or purpose without counsel-approved coverage;
- the phone number changed after consent and there is no approved basis to treat the consent as continuing;
- an internal do-not-call, opt-out, or suppression match exists;
- an external Do Not Call check required by the campaign is missing, stale, or unavailable;
- the person previously asked to stop, even if the person had earlier consented;
- jurisdiction or local time is unknown;
- the call falls outside the approved time window;
- caller identification or disclosure configuration is missing;
- a required recording notice cannot be delivered or the recording configuration is not approved;
- the campaign, script, offer, or AI voice version is not approved;
- the dialing vendor cannot provide an auditable call record; or
- the campaign would target a sensitive or restricted category not expressly approved.

## Call opening requirements

At the beginning of an allowed call, the agent must use the approved identity and purpose wording. Until the company name and persona are finalized, use placeholders only in draft testing.

The opening must not imply that the agent is human, returning a personal call, or calling for a reason that is not true. The exact production wording belongs in `ai-disclosure-wording.md` and must be approved before any live campaign.

The agent should ask whether this is a reasonable time for a brief question. If the person says no, the agent must offer an approved callback path or end the call.

## Opt-out handling

A request to stop is effective immediately. Treat the following as opt-outs unless the person clearly corrects themselves:

- “Do not call me.”
- “Remove me from your list.”
- “Stop calling.”
- “Take me off this list.”
- “Do not contact this number again.”

The agent must:

1. acknowledge the request briefly;
2. not argue, sell, or ask for a reason;
3. end the call promptly;
4. write the suppression event to the operational system;
5. prevent future campaigns from dialing the number; and
6. create an auditable event containing the time, campaign, number, agent, and disposition.

Suggested wording:

> “Understood. I’ll mark this number so we don’t call you again. Thank you for your time.”

If the person asks whether email or another channel may be used, do not assume permission. Record the preference and use another channel only after a separate approved permission exists.

## Voicemail policy

Do not leave an AI-generated marketing voicemail unless the campaign’s counsel-approved policy expressly permits it and the same consent, identification, disclosure, opt-out, and content controls have passed. The default for this program is:

```text
AI voice reaches voicemail → do not leave a marketing message → log VOICEMAIL_NO_MESSAGE
```

## Recording and monitoring

Recording, transcription, human monitoring, and quality review require a separate approved policy. Before enabling them, determine the applicable notice and consent requirements for every jurisdiction in which the call recipient may be located.

If the required recording configuration or notice is unavailable, do not record. If the campaign cannot operate lawfully without recording, do not dial.

## Audit and retention

For every allowed or blocked attempt, retain an auditable event in the operational system containing:

- lead and campaign identifiers;
- dial decision and each gate result;
- consent basis and evidence reference;
- suppression-list check result and timestamp;
- caller identity and script/brain versions;
- call time zone and calling-window result;
- final disposition;
- opt-out event, if any; and
- error or override reason, if blocked.

The retention period must be set by counsel and the applicable campaign policy. For covered telemarketing activity, current 16 CFR §310.5 generally requires five-year retention of specified records; applicability and exceptions matter. Do not treat five years as a universal rule for every B2B campaign, and follow counsel’s documented retention schedule. [2] [3]

No human may override a `DO_NOT_DIAL` result from inside the voice-agent prompt. Any exception must be created as a documented, campaign-specific approval in the compliance register and implemented as a controlled configuration change.

## Launch checklist

This note must remain `status: draft` until all of the following are complete:

- [ ] Company and caller identity finalized.
- [ ] AI disclosure wording approved.
- [ ] Consent language and collection flow reviewed by U.S. counsel.
- [ ] Consumer, mobile, residential, and business-number handling defined.
- [ ] National and internal Do Not Call process defined where applicable.
- [ ] State calling hours and jurisdiction handling defined.
- [ ] Recording and transcription policy approved.
- [ ] Consent ledger implemented outside Obsidian.
- [ ] Suppression check is enforced in code.
- [ ] Opt-out event is tested end to end.
- [ ] Voicemail behavior is approved.
- [ ] Audit records are generated for both blocked and allowed calls.
- [ ] Test scenarios pass, including missing consent, stale consent, opt-out, unknown time zone, wrong number, voicemail, and human request.
- [ ] Counsel signs off on the exact pilot campaign and lead source.

## Source

- FCC, “Implications of Artificial Intelligence Technologies on Protecting Consumers from Unwanted Robocalls and Robotexts,” FCC 24-17, adopted February 2, 2024 and released February 8, 2024: https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- FCC, “Implications of Artificial Intelligence Technologies on Protecting Consumers from Unwanted Robocalls and Robotexts”: https://www.fcc.gov/document/fcc-confirms-tcpa-applies-ai-technologies-generate-human-voices
- FTC, “Complying with the Telemarketing Sales Rule”: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, “FTC Implements New Protections for Businesses Against Telemarketing Fraud and Affirms Protections Against AI-enabled Scam Calls”: https://www.ftc.gov/news-events/news/press-releases/2024/03/ftc-implements-new-protections-businesses-against-telemarketing-fraud-affirms-protections-against-ai
- TODO: U.S. telecom/privacy counsel review of this exact campaign, list source, number types, disclosures, recording workflow, and state coverage.

## Related

- [[_vault-guide]]
- [[one-job-statement]]
- [[never-say-list]]
- [[00_constitution/value-rules]]
- Planned: `consent-ledger-spec`, `opt-out-handling`, `ai-disclosure-wording`, `calling-hours`, `recording-consent`
