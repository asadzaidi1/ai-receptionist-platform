#!/usr/bin/env python3
"""Local staging CRM adapter. It never calls a provider."""
from __future__ import annotations
import csv, hashlib, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from lead_pipeline import norm_text, normalize_domain, token

SCHEMA = Path(__file__).parents[1] / 'staging_crm_schema.sql'

def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def payload_hash(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def init_staging(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA.read_text())
    phase3_schema = SCHEMA.parent / 'phase3_schema.sql'
    if phase3_schema.exists():
        conn.executescript(phase3_schema.read_text())
    phase4_schema = SCHEMA.parent / 'phase4_schema.sql'
    if phase4_schema.exists():
        conn.executescript(phase4_schema.read_text())
    return conn

def load_ready_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def canonical_payload(conn, row: dict, campaign_id: str, brain_version: str, policy_version: str):
    lead = conn.execute('SELECT * FROM canonical_leads WHERE lead_id = ?', (row['lead_id'],)).fetchone()
    if not lead:
        raise ValueError(f"canonical lead not found: {row['lead_id']}")
    cols = [d[1] for d in conn.execute('PRAGMA table_info(canonical_leads)').fetchall()]
    record = dict(zip(cols, lead))
    if row.get('queue') != 'CAMPAIGN_READY':
        raise ValueError(f"non-ready row supplied: {row.get('queue')}")
    return {
        'lead_id': record['lead_id'], 'campaign_id': campaign_id,
        'source_id': record['source_id'], 'source_row_number': int(record['raw_id'].split(':')[-1]),
        'company_name': record['company_name'], 'normalized_company': record['normalized_company'],
        'normalized_domain': record['normalized_domain'], 'contact_name': record['contact_name'],
        'contact_role': record['contact_role'], 'phone_token': record['phone_token'],
        'jurisdiction': record['jurisdiction'], 'time_zone': record['time_zone'],
        'brain_version': brain_version, 'policy_version': policy_version,
        'source_lead_key': f"{campaign_id}:{record['lead_id']}",
    }

def upsert_ready_queue(db_path: Path, ready_csv: Path, campaign_id: str, brain_version: str, policy_version: str):
    conn = init_staging(db_path)
    results = []
    for row in load_ready_csv(ready_csv):
        payload = canonical_payload(conn, row, campaign_id, brain_version, policy_version)
        idem = f"crm-upsert:{payload['source_lead_key']}:{brain_version}"
        digest = payload_hash(payload)
        prior = conn.execute('SELECT payload_hash,result_json FROM crm_sync_events WHERE idempotency_key=?', (idem,)).fetchone()
        if prior:
            if prior[0] != digest:
                raise ValueError(f'idempotency conflict for {idem}')
            results.append({**json.loads(prior[1]), 'replayed': True})
            continue
        ts = now_utc()
        account_id = 'acct_' + hashlib.sha256((payload['normalized_domain'] or payload['normalized_company']).encode()).hexdigest()[:16]
        contact_id = 'contact_' + hashlib.sha256(payload['lead_id'].encode()).hexdigest()[:16]
        conn.execute('INSERT INTO crm_accounts(account_id,normalized_domain,normalized_company,company_name,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,?) ON CONFLICT(normalized_domain) DO UPDATE SET company_name=excluded.company_name,updated_at_utc=excluded.updated_at_utc', (account_id, payload['normalized_domain'] or None, payload['normalized_company'], payload['company_name'], ts, ts))
        actual_account = conn.execute('SELECT account_id FROM crm_accounts WHERE normalized_domain IS ? OR (normalized_domain IS NULL AND normalized_company=?)', (payload['normalized_domain'] or None, payload['normalized_company'])).fetchone()
        account_id = actual_account[0]
        conn.execute('INSERT INTO crm_contacts(contact_id,account_id,lead_id,contact_name,contact_role,phone_token,jurisdiction,time_zone,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(lead_id) DO UPDATE SET account_id=excluded.account_id,contact_name=excluded.contact_name,contact_role=excluded.contact_role,updated_at_utc=excluded.updated_at_utc', (contact_id, account_id, payload['lead_id'], payload['contact_name'], payload['contact_role'], payload['phone_token'], payload['jurisdiction'], payload['time_zone'], ts, ts))
        actual_contact = conn.execute('SELECT contact_id FROM crm_contacts WHERE lead_id=?', (payload['lead_id'],)).fetchone()[0]
        conn.execute('INSERT INTO crm_leads(lead_id,account_id,contact_id,campaign_id,source_id,source_row_number,queue,lifecycle_status,fit_score,intent_score,readiness_tier,brain_version,policy_version,source_lead_key,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(lead_id) DO UPDATE SET account_id=excluded.account_id,contact_id=excluded.contact_id,campaign_id=excluded.campaign_id,queue=excluded.queue,lifecycle_status=CASE WHEN crm_leads.lifecycle_status="DISPATCHED" THEN crm_leads.lifecycle_status ELSE "STAGED" END,brain_version=excluded.brain_version,policy_version=excluded.policy_version,updated_at_utc=excluded.updated_at_utc', (payload['lead_id'], account_id, actual_contact, campaign_id, payload['source_id'], payload['source_row_number'], 'CAMPAIGN_READY', 'STAGED', None, None, None, brain_version, policy_version, payload['source_lead_key'], ts, ts))
        result = {'lead_id': payload['lead_id'], 'account_id': account_id, 'contact_id': actual_contact, 'idempotency_key': idem, 'status': 'UPSERTED'}
        conn.execute('INSERT INTO crm_sync_events VALUES(?,?,?,?,?,?)', (idem, payload['lead_id'], 'UPSERT_READY', digest, json.dumps(result, sort_keys=True), ts))
        conn.commit(); results.append({**result, 'replayed': False})
    conn.close()
    return results
