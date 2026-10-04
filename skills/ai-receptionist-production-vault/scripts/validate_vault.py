#!/usr/bin/env python3
"""Validate an AI receptionist production vault, including lead-system controls."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
files = list(root.rglob('*.md'))
if not files:
    raise SystemExit('ERROR: no Markdown files found')

def text_at(rel):
    p = root / rel
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''

all_text = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in files)
required = [
    '00_constitution/production-readiness.md',
    '01_compliance/consent-gate.md',
    '01_compliance/consent-ledger-spec.md',
    '01_compliance/target-state-campaign-action-plan.md',
    '03_call_playbook/agent-state-machine.md',
    '03_call_playbook/grounding-and-abstention.md',
    '03_call_playbook/tool-permission-matrix.md',
    '05_operations/production-architecture.md',
    '05_operations/webhook-idempotency.md',
    '05_operations/lead-generation-operating-system.md',
    '05_operations/campaign-config-template.md',
    '05_operations/crm-pipeline-contract.md',
    '05_operations/follow-up-and-nurture.md',
    '06_performance/evaluation-plan.md',
    '06_performance/zero-hallucination-test-cases.md',
    '06_performance/lead-funnel-test-suite.md',
    '06_performance/qa-scorecard.md',
    '06_performance/release-gate.md',
    '08_governance/brain-release-manifest.md',
]
missing = [p for p in required if not (root / p).exists()]
metadata_missing = []
for p in files:
    text = p.read_text(encoding='utf-8', errors='ignore')
    for field in ('type:', 'status:', 'authority:', 'niche:', 'compile:', 'owner:', 'version:', 'last_reviewed:'):
        if field not in text[:1200]:
            metadata_missing.append((str(p.relative_to(root)), field))

paths = {p.relative_to(root).with_suffix('').as_posix() for p in files}
bases = {p.stem for p in files}
broken = []
for p in files:
    for link in re.findall(r'\[\[([^\]|#]+)', p.read_text(encoding='utf-8', errors='ignore')):
        link = link.strip()
        if link in {'wikilinks', 'note'}:
            continue
        if link not in paths and link not in bases:
            broken.append((str(p.relative_to(root)), link))

state = text_at('03_call_playbook/agent-state-machine.md')
eval_plan = text_at('06_performance/evaluation-plan.md')
tests = text_at('06_performance/zero-hallucination-test-cases.md')
rubric = text_at('06_performance/qa-scorecard.md')
manifest = text_at('08_governance/brain-release-manifest.md')
lead_os = text_at('05_operations/lead-generation-operating-system.md')
crm = text_at('05_operations/crm-pipeline-contract.md')
lead_tests = text_at('06_performance/lead-funnel-test-suite.md')
content_checks = {
    'STATE_HAS_EVIDENCE_BUNDLE': all(x in state for x in ('evidence_id', 'source_note_id', 'source_version', 'allowed_for_agent')),
    'STATE_HAS_ABSTAIN_PATH': 'ABSTAIN_AND_CLARIFY' in state and 'HUMAN_REVIEW' in state,
    'STATE_HAS_SERVER_TOOL_GUARDS': all(x in state for x in ('allowlisted tool', 'schema-valid arguments', 'idempotency key', 'audit event')),
    'STATE_REQUIRES_HANDOFF_ACCEPTANCE': 'HANDOFF_ACCEPTED' in state and 'positive acceptance event' in state,
    'STATE_BLOCKS_OPT_OUT': 'opt-out' in state.lower() and 'forbidden' in state.lower(),
    'EVAL_HAS_DETERMINISTIC_ASSERTIONS': 'Deterministic assertions' in eval_plan,
    'EVAL_ZERO_CRITICAL_THRESHOLD': 'zero critical violations' in eval_plan.lower(),
    'EVAL_HAS_UNSUPPORTED_CLAIM_TESTS': 'unsupported price' in eval_plan.lower() and 'guarantee' in eval_plan.lower(),
    'EVAL_HAS_PROMPT_INJECTION_TESTS': 'hidden instructions' in eval_plan.lower() and 'ignore your rules' in tests.lower(),
    'EVAL_HAS_FALSE_SUCCESS_TESTS': 'false transfer' in eval_plan.lower() and 'tool returns timeout' in eval_plan.lower(),
    'TESTS_HAVE_EXPECTED_OUTCOMES': all(x in tests.lower() for x in ('prompt', 'expected state', 'forbidden behavior', 'assertions')),
    'RUBRIC_HAS_CRITICAL_FAILS': ('critical fail' in rubric.lower() or 'critical failure' in rubric.lower()) and 'unsupported claim' in rubric.lower(),
    'MANIFEST_HAS_RELEASE_LINEAGE': all(x in manifest for x in ('brain_version', 'kb_release_id', 'policy_version', 'rollback')),
    'HOME_HAS_CORE_PATH': all(x in text_at('home.md') for x in ('target-state-campaign-action-plan', 'agent-state-machine', 'zero-hallucination-test-cases', 'brain-release-manifest')),
    'GUIDE_HAS_EXPORT_BOUNDARY': 'Only `status: live` notes are exported' in text_at('_vault-guide.md') and 'Nothing writes into the vault during a call' in text_at('_vault-guide.md'),
    'RUNTIME_HAS_TRACE_PATH': all(x in text_at('05_operations/runtime-contract.md').lower() for x in ('synthetic lead', 'correlation ids', 'safe degradation')),
    'NO_GENERATOR_ARTIFACTS': not any(x in all_text for x in ("related=['", "'''")),
    'LEAD_OS_HAS_FULL_FUNNEL': all(x in lead_os for x in ('raw immutable import', 'consent and suppression gate', 'structured qualification', 'human handoff', 'reviewed learning')),
    'CRM_SEPARATES_STAGES': all(x in crm.lower() for x in ('lead lifecycle', 'call dispositions', 'opportunity fields', 'idempotency')),
    'LEAD_TESTS_HAVE_NEGATIVE_PATHS': all(x in lead_tests.lower() for x in ('unknown number type', 'missing consent', 'opt-out', 'duplicate provider event', 'crm write failure')),
    'NO_RAW_TO_DIAL_RULE': 'No raw record becomes a dial' in lead_os,
    'SCORING_CANNOT_OVERRIDE_COMPLIANCE': 'never authorizes contact' in text_at('04_prospects/lead-scoring-v2.md') and 'BLOCKED' in text_at('04_prospects/lead-scoring-v2.md'),
}

print(f'MD_FILES={len(files)}')
print(f'MISSING_REQUIRED={len(missing)}')
print(f'METADATA_ISSUES={len(metadata_missing)}')
print(f'BROKEN_LINKS={len(broken)}')
print(f'PROHIBITED_NAMES={bool(re.search(r"(?i)asad|asif", all_text))}')
print(f'OWNER_METADATA_OK={all("owner: Steve Anderson" in p.read_text(encoding="utf-8", errors="ignore") for p in files)}')
print(f'LAUNCH_BLOCKER_NOTE={"00_constitution/production-readiness.md" in [str(p.relative_to(root)) for p in files]}')
for name, ok in content_checks.items():
    print(f'{name}={ok}')

failed = missing or metadata_missing or broken or re.search(r'(?i)asad|asif', all_text) or not all(content_checks.values())
if failed:
    for item in missing[:10]: print('MISSING', item)
    for item in metadata_missing[:10]: print('META', item)
    for item in broken[:10]: print('BROKEN', item)
    for name, ok in content_checks.items():
        if not ok: print('CONTENT_CHECK_FAILED', name)
    raise SystemExit(1)
