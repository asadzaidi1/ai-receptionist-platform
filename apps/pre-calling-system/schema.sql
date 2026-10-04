PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_leads (
  raw_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  source_row_number INTEGER NOT NULL,
  imported_at_utc TEXT NOT NULL,
  raw_payload_json TEXT NOT NULL,
  UNIQUE(source_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS canonical_leads (
  lead_id TEXT PRIMARY KEY,
  raw_id TEXT NOT NULL REFERENCES raw_leads(raw_id),
  source_id TEXT NOT NULL,
  company_name TEXT NOT NULL,
  normalized_company TEXT NOT NULL,
  domain TEXT,
  normalized_domain TEXT,
  contact_name TEXT,
  contact_role TEXT,
  phone_e164 TEXT,
  phone_token TEXT,
  number_type TEXT NOT NULL,
  jurisdiction TEXT,
  time_zone TEXT,
  industry TEXT,
  source_permission TEXT NOT NULL,
  consent_status TEXT NOT NULL,
  source_date TEXT NOT NULL,
  data_confidence TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  dedupe_key TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  UNIQUE(dedupe_key)
);

CREATE TABLE IF NOT EXISTS suppression_entries (
  suppression_id TEXT PRIMARY KEY,
  scope TEXT NOT NULL CHECK(scope IN ('phone','domain','company','email','global')),
  match_value TEXT NOT NULL,
  reason TEXT NOT NULL,
  source TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
  created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eligibility_decisions (
  decision_id TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL REFERENCES canonical_leads(lead_id),
  queue TEXT NOT NULL CHECK(queue IN ('CAMPAIGN_READY','HUMAN_REVIEW_REQUIRED','DO_NOT_CONTACT')),
  decision_reason TEXT NOT NULL,
  suppression_match TEXT,
  policy_version TEXT NOT NULL,
  decided_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lineage_events (
  event_id TEXT PRIMARY KEY,
  raw_id TEXT,
  lead_id TEXT,
  event_type TEXT NOT NULL,
  event_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_canonical_domain ON canonical_leads(normalized_domain);
CREATE INDEX IF NOT EXISTS idx_canonical_phone ON canonical_leads(phone_e164);
CREATE INDEX IF NOT EXISTS idx_decisions_queue ON eligibility_decisions(queue);
CREATE INDEX IF NOT EXISTS idx_suppression_match ON suppression_entries(scope, match_value, active);
