import csv, sqlite3, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lead_pipeline import process

RAW = ROOT / 'fixtures/raw_leads.csv'
SUP = ROOT / 'fixtures/suppression.csv'
EXPECTED = ROOT / 'fixtures/expected_queue.csv'

def run(tmp_path):
    return process(RAW, SUP, tmp_path / 'test.db', today=date(2026,10,4))

def by_source(rows, source_id, row_num):
    return next(r for r in rows if r['source_id'] == source_id and r['source_row_number'] == str(row_num))

def test_expected_queue_fixture_matches(tmp_path):
    actual = {(r['source_id'], r['source_row_number']): (r['queue'], r['reason']) for r in run(tmp_path)}
    with EXPECTED.open(newline='', encoding='utf-8') as f:
        expected = {(r['source_id'], r['source_row_number']): (r['expected_queue'], r['expected_reason']) for r in csv.DictReader(f)}
    assert actual == expected

def test_duplicate_rows_collapse_to_one_canonical_lead(tmp_path):
    rows = run(tmp_path)
    a1, a2, b1 = by_source(rows,'list_a',1), by_source(rows,'list_a',2), by_source(rows,'list_b',1)
    assert a1['lead_id'] == a2['lead_id'] == b1['lead_id']
    assert a1['queue'] == 'CAMPAIGN_READY'
    assert a2['reason'] == 'eligible_verified_record'

def test_conflicting_duplicate_is_do_not_contact(tmp_path):
    row = by_source(run(tmp_path),'list_b',2)
    assert row['queue'] == 'DO_NOT_CONTACT'
    assert row['reason'] == 'duplicate_conflict_same_phone_different_contact'

def test_active_phone_suppression_is_do_not_contact(tmp_path):
    row = by_source(run(tmp_path),'list_a',8)
    assert row['queue'] == 'DO_NOT_CONTACT'
    assert row['reason'] == 'active_phone_suppression'
    assert row['suppression_match'].startswith('sup_001:phone:')

def test_inactive_suppression_does_not_block_by_itself(tmp_path):
    row = by_source(run(tmp_path),'list_a',6)
    assert row['queue'] == 'HUMAN_REVIEW_REQUIRED'
    assert row['reason'] == 'stale_low_confidence_record'

def test_unknown_number_type_requires_review(tmp_path):
    row = by_source(run(tmp_path),'list_a',4)
    assert row['queue'] == 'HUMAN_REVIEW_REQUIRED'
    assert row['reason'] == 'unknown_number_type'

def test_missing_consent_requires_review(tmp_path):
    row = by_source(run(tmp_path),'list_a',5)
    assert row['queue'] == 'HUMAN_REVIEW_REQUIRED'
    assert row['reason'] == 'consent_missing'

def test_invalid_phone_is_do_not_contact(tmp_path):
    row = by_source(run(tmp_path),'list_a',9)
    assert row['queue'] == 'DO_NOT_CONTACT'
    assert row['reason'] == 'invalid_phone'

def test_missing_jurisdiction_requires_review(tmp_path):
    row = by_source(run(tmp_path),'list_a',10)
    assert row['queue'] == 'HUMAN_REVIEW_REQUIRED'
    assert row['reason'] == 'jurisdiction_or_timezone_missing'

def test_db_preserves_raw_and_lineage(tmp_path):
    db = tmp_path / 'test.db'
    process(RAW, SUP, db, today=date(2026,10,4))
    conn = sqlite3.connect(db)
    assert conn.execute('select count(*) from raw_leads').fetchone()[0] == 12
    assert conn.execute('select count(*) from canonical_leads').fetchone()[0] == 9
    assert conn.execute('select count(*) from lineage_events').fetchone()[0] == 12
    conn.close()
