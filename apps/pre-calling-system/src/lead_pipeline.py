#!/usr/bin/env python3
"""Deterministic pre-calling lead pipeline. No live dialing or external calls."""
from __future__ import annotations
import csv, hashlib, json, re, sqlite3
from datetime import date, datetime, timezone
from pathlib import Path

QUEUES = ('CAMPAIGN_READY', 'HUMAN_REVIEW_REQUIRED', 'DO_NOT_CONTACT')
READY_NUMBER_TYPES = {'business_landline', 'business_voip'}
POLICY_VERSION = 'pre-calling-v0.1'

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def norm_text(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (value or '').lower())

def normalize_domain(value: str) -> str:
    value = (value or '').strip().lower()
    value = re.sub(r'^https?://', '', value)
    value = value.split('/')[0].strip()
    return value.replace('www.', '').replace(' ', '')

def normalize_phone(value: str) -> str | None:
    digits = re.sub(r'\D', '', value or '')
    if len(digits) == 10:
        digits = '1' + digits
    if len(digits) == 11 and digits.startswith('1'):
        return '+' + digits
    return None

def token(value: str | None) -> str | None:
    if not value: return None
    return 'tok_' + hashlib.sha256(value.encode()).hexdigest()[:16]

def canonical_key(row: dict) -> str:
    domain = normalize_domain(row.get('domain',''))
    company = norm_text(row.get('company_name',''))
    phone = normalize_phone(row.get('phone',''))
    if domain: return 'domain:' + domain
    if phone: return 'phone:' + phone
    return 'raw:' + row['source_id'] + ':' + row['source_row_number']

def parse_date(value: str) -> date:
    return date.fromisoformat(value)

def age_days(value: str, today: date | None = None) -> int:
    return ((today or date.today()) - parse_date(value)).days

def load_csv(path: Path) -> list[dict]:
    with path.open(newline='', encoding='utf-8') as f:
        return [dict(r) for r in csv.DictReader(f)]

def load_suppression(path: Path) -> list[dict]:
    with path.open(newline='', encoding='utf-8') as f:
        return [dict(r) for r in csv.DictReader(f) if r.get('active') == '1']

def suppression_match(row: dict, suppressions: list[dict]) -> str | None:
    phone = normalize_phone(row.get('phone',''))
    domain = normalize_domain(row.get('domain',''))
    company = norm_text(row.get('company_name',''))
    for s in suppressions:
        scope, value = s['scope'], s['match_value']
        candidate = {'phone': phone, 'domain': domain, 'company': company, 'global': '*', 'email': None}.get(scope)
        if candidate and (candidate == value or (scope == 'global' and value == '*')):
            return f"{s['suppression_id']}:{scope}:{s['reason']}"
    return None

def normalize_row(row: dict, imported_at: str) -> dict:
    phone = normalize_phone(row.get('phone',''))
    domain = normalize_domain(row.get('domain',''))
    company = norm_text(row.get('company_name',''))
    return {
        **row,
        'raw_id': f"{row['source_id']}:{row['source_row_number']}",
        'normalized_domain': domain,
        'normalized_company': company,
        'phone_e164': phone or '',
        'phone_token': token(phone) or '',
        'dedupe_key': canonical_key(row),
        'imported_at_utc': imported_at,
    }

def classify(row: dict, suppressions: list[dict], duplicate_conflict: bool, today: date | None = None) -> tuple[str, str, str | None]:
    match = suppression_match(row, suppressions)
    if match:
        return 'DO_NOT_CONTACT', 'active_' + match.split(':')[1] + '_suppression', match
    if not row['phone_e164']:
        return 'DO_NOT_CONTACT', 'invalid_phone', None
    if duplicate_conflict:
        return 'DO_NOT_CONTACT', 'duplicate_conflict_same_phone_different_contact', None
    if row.get('source_permission') != 'approved':
        return 'HUMAN_REVIEW_REQUIRED', 'source_permission_unknown', None
    if row.get('consent_status') != 'verified':
        return 'HUMAN_REVIEW_REQUIRED', 'consent_missing', None
    if row.get('number_type') not in READY_NUMBER_TYPES:
        return 'HUMAN_REVIEW_REQUIRED', 'unknown_number_type', None
    if not row.get('jurisdiction') or not row.get('time_zone'):
        return 'HUMAN_REVIEW_REQUIRED', 'jurisdiction_or_timezone_missing', None
    if age_days(row['source_date'], today) > 365 or row.get('data_confidence') == 'low':
        return 'HUMAN_REVIEW_REQUIRED', 'stale_low_confidence_record', None
    return 'CAMPAIGN_READY', 'eligible_verified_record', None

def process(raw_path: Path, suppression_path: Path, db_path: Path, today: date | None = None) -> list[dict]:
    imported_at = now_utc()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    raw = load_csv(raw_path)
    suppressions = load_suppression(suppression_path)
    conn = sqlite3.connect(db_path)
    conn.executescript((Path(__file__).parents[1] / 'schema.sql').read_text())
    decisions = []
    groups: dict[str, list[dict]] = {}
    for row in raw:
        n = normalize_row(row, imported_at)
        groups.setdefault(n['dedupe_key'], []).append(n)
        conn.execute('INSERT OR IGNORE INTO raw_leads VALUES (?,?,?,?,?)', (n['raw_id'], n['source_id'], int(n['source_row_number']), imported_at, json.dumps(row, sort_keys=True)))
    canonical_ids = {}
    for key, rows in groups.items():
        base = rows[0]
        lead_id = 'lead_' + hashlib.sha256(key.encode()).hexdigest()[:16]
        canonical_ids[key] = lead_id
        conn.execute('INSERT OR IGNORE INTO canonical_leads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
            lead_id, base['raw_id'], base['source_id'], base['company_name'], base['normalized_company'],
            base['domain'], base['normalized_domain'], base['contact_name'], base['contact_role'], base['phone_e164'],
            base['phone_token'], base['number_type'], base['jurisdiction'], base['time_zone'], base['industry'],
            base['source_permission'], base['consent_status'], base['source_date'], base['data_confidence'],
            'verified' if len(rows) == 1 else 'dedupe_review', key, imported_at))
        for r in rows:
            base_contact = norm_text(base.get('contact_name',''))
            same_phone_conflict = bool(r['phone_e164']) and norm_text(r.get('contact_name','')) != base_contact and any(
                x['phone_e164'] == r['phone_e164'] and norm_text(x.get('contact_name','')) == base_contact
                for x in rows)
            queue, reason, match = classify(r, suppressions, same_phone_conflict, today)
            decision_id = 'dec_' + hashlib.sha256((r['raw_id'] + queue + reason).encode()).hexdigest()[:16]
            conn.execute('INSERT OR REPLACE INTO eligibility_decisions VALUES (?,?,?,?,?,?,?)', (decision_id, lead_id, queue, reason, match, POLICY_VERSION, imported_at))
            conn.execute('INSERT OR REPLACE INTO lineage_events VALUES (?,?,?,?,?,?)', ('evt_'+decision_id, r['raw_id'], lead_id, 'eligibility_decision', json.dumps({'queue':queue,'reason':reason,'dedupe_key':key}, sort_keys=True), imported_at))
            decisions.append({'source_id':r['source_id'],'source_row_number':r['source_row_number'],'lead_id':lead_id,'queue':queue,'reason':reason,'suppression_match':match,'dedupe_key':key})
    conn.commit(); conn.close()
    return decisions

def write_queue_csv(decisions: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for q in QUEUES:
        rows = [d for d in decisions if d['queue'] == q]
        with (out_dir / f'{q.lower()}.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['source_id','source_row_number','lead_id','queue','reason','suppression_match','dedupe_key'])
            w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw', type=Path, required=True)
    ap.add_argument('--suppression', type=Path, required=True)
    ap.add_argument('--db', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = process(args.raw, args.suppression, args.db)
    write_queue_csv(result, args.out)
    print(json.dumps({'records_processed': len(result), 'queues': {q: sum(x['queue']==q for x in result) for q in QUEUES}}, indent=2))
