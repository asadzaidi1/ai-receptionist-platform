---
type: register
status: review
authority: reference
niche: general
compile: none
owner: Steve Anderson
version: v0.2
last_reviewed: 2026-10-04
---

# Production research synthesis

This register records the primary sources used for the production-grade upgrade. It is a research register, not a legal opinion, certification, or permission to dial.

## High-impact conclusions

1. The FCC has confirmed that AI-generated human voices fall within TCPA restrictions on artificial or prerecorded voice calls. Consent, caller identification, opt-out, number category, call purpose, and applicable exceptions must be analyzed for the exact campaign.
2. The FTC’s B2B Telemarketing Sales Rule treatment is limited. It does not resolve TCPA, state telemarketing, privacy, recording, or AI-specific questions. The FTC’s 2024 amendment also extends misrepresentation protections to B2B telemarketing.
3. Current covered-activity TSR recordkeeping generally uses a five-year period under 16 CFR §310.5, subject to applicability and exemptions. The vault therefore requires a counsel-approved retention schedule rather than a universal number.
4. Recording/transcription is a separate legal and privacy decision from permission to place a call. The jurisdiction of the parties and the circumstances of the communication matter.
5. A production voice system needs server-side policy enforcement, idempotent event processing, narrow tool permissions, trace correlation, safe handoff, release testing, monitoring, rollback, backups, and incident response. A prompt alone is not a control system.
6. Obsidian is the human authoring and governance layer. Only approved, versioned, access-filtered release snapshots should reach the runtime knowledge system. The vault is not the CRM, consent ledger, dial queue, evidence store, or live runtime.

## Sources

### Calling and telemarketing

- FCC, Declaratory Ruling FCC 24-17, AI-generated voices and TCPA: https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- 47 CFR §64.1200, delivery restrictions, identification, consent, opt-out, and revocation: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FCC 24-84, proposed AI-call disclosure rule; proposal status must not be treated as a final nationwide mandate: https://docs.fcc.gov/public/attachments/FCC-24-84A1.pdf
- FCC, TCPA consent-revocation Order update: https://www.fcc.gov/document/cgb-extends-effective-date-tcpas-consent-revocation-rule
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, Q&A for Telemarketers & Sellers About DNC Provisions: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- 16 CFR §310.5, TSR recordkeeping: https://www.law.cornell.edu/cfr/text/16/310.5
- 16 CFR §310.6, TSR exemptions: https://www.law.cornell.edu/cfr/text/16/310.6

### Privacy and security

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-61 Rev. 3 incident response: https://csrc.nist.gov/pubs/sp/800/61/r3/final
- CISA Secure by Design: https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_1025_508c.pdf
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- California Penal Code §632 recording example: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=632
- California Civil Code §1798.100: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100

### Telephony and voice runtime

- OpenAI Realtime API SIP guide: https://developers.openai.com/api/docs/guides/realtime-sip
- OpenAI Realtime API guide: https://developers.openai.com/api/docs/guides/realtime
- IETF RFC 3261, SIP: https://www.rfc-editor.org/info/rfc3261/
- IETF RFC 3550, RTP: https://www.rfc-editor.org/info/rfc3550/
- IETF RFC 3711, SRTP: https://www.rfc-editor.org/info/rfc3711/
- Twilio Media Streams: https://www.twilio.com/docs/voice/media-streams
- Twilio WebSocket messages: https://www.twilio.com/docs/voice/media-streams/websocket-messages
- Twilio SIP transfer: https://www.twilio.com/docs/sip-trunking/call-transfer
- Twilio secure webhooks: https://www.twilio.com/docs/usage/webhooks/webhooks-security
- Twilio SIP security: https://www.twilio.com/docs/voice/api/sip-security
- Twilio Answering Machine Detection: https://www.twilio.com/docs/voice/answering-machine-detection

### Knowledge and evaluation

- OpenAI Voice Agents: https://developers.openai.com/api/docs/guides/voice-agents
- OpenAI Cookbook voice-agent evaluation: https://developers.openai.com/cookbook/examples/audio/voice_agent_evaluation
- OpenAI trace grading: https://developers.openai.com/api/docs/guides/trace-grading
- Microsoft RAG and indexes: https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation
- Microsoft RAG evaluators: https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators
- Obsidian Properties: https://help.obsidian.md/Editing+and+formatting/Properties
- Obsidian plugin security: https://obsidian.md/help/plugin-security
- Obsidian Sync security: https://obsidian.md/help/sync/security
- GitHub protected branches: https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches

## Source-use rule

A source URL is not an approval. The owner must assign the source to a note, record the exact interpretation, attach the effective date/version, and obtain the appropriate business, security, privacy, or legal review before marking a control live.

## Related

- [[production-readiness]]
- [[legal-review-gate]]
- [[source-registry]]
- [[change-control]]
