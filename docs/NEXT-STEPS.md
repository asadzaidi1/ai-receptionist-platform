

## Vapi playbook operating model

Apply a use-case-first rollout. Start with narrow, high-volume, low-ambiguity workflows such as intake, qualification, scheduling, reminders, and verified status checks. Keep humans in the loop for high-emotion complaints, legal/safety uncertainty, undocumented exceptions, and discretion-heavy disputes.

The next orchestration build must preserve one shared call context across bounded specialist agents, maintain explicit tool permissions, prevent transfer loops, and recover safely when a component fails. Every failed action must produce an approved next step, a human handoff or bounded callback, and an audit record.

Use the internal rollout tiers in `docs/VAPI-PLAYBOOK-BENCHMARK.md`: Foundation, Growth, Pro, and Enterprise. Advance only after evidence, monitoring, cost controls, canary testing, and rollback readiness are documented.
