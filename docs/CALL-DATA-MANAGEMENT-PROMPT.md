

## INBOUND / OUTBOUND EXPERIENCE-MATCHING EXTENSION

When routing or selecting an AI/human agent, use this decision order:

```text
consent / suppression / jurisdiction / local time / campaign gate
  → skill / SLA / availability / coverage
  → explicitly provided customer experience preferences
  → explainable match recommendation
  → assignment or human review
```

Allowed preference signals include explicitly selected language, voice style, communication channel, callback window, service category, urgency, required skill, coverage, continuity preference, accessibility accommodation, and interaction purpose.

Never infer or use protected or highly sensitive traits for pairing or outbound targeting. Do not use accent as a proxy for identity. Do not imitate real people or public figures. A matching score never authorizes an outbound call; the consent and dispatch gates remain authoritative.

For inbound calls, support intent classification, urgency/safety triage, required intake fields, scheduling, verified transfers, work-order creation, CRM updates, and human escalation.

For outbound calls, require campaign eligibility, defined purpose and scope, local-time check, number validation, consent/suppression recheck, approved language/voice profile, bounded retry policy, answering-machine handling, factual disposition, and CRM synchronization.

For every pairing recommendation, store reason codes, input provenance, configuration/model version, confidence, selected agent/voice, override actor, and outcome. Route uncertain or materially consequential matches to human review.

Measure optimization using versioned KPIs and control/holdout groups where appropriate. Do not claim uplift without evidence.
