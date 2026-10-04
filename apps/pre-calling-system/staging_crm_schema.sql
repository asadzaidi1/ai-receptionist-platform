PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS crm_accounts (
  account_id TEXT PRIMARY KEY,
  normalized_domain TEXT UNIQUE,
  normalized_company TEXT NOT NULL,
  company_name TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_contacts (
  contact_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES crm_accounts(account_id),
  lead_id TEXT NOT NULL UNIQUE,
  contact_name TEXT,
  contact_role TEXT,
  phone_token TEXT,
  jurisdiction TEXT,
  time_zone TEXT,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_leads (
  lead_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES crm_accounts(account_id),
  contact_id TEXT NOT NULL REFERENCES crm_contacts(contact_id),
  campaign_id TEXT NOT NULL,
  source_id TEXT NOT NULL,
  source_row_number INTEGER NOT NULL,
  queue TEXT NOT NULL CHECK(queue = 'CAMPAIGN_READY'),
  lifecycle_status TEXT NOT NULL CHECK(lifecycle_status IN ('STAGED','ELIGIBLE_PENDING_DISPATCH','DISPATCH_BLOCKED','DISPATCHED')),
  fit_score INTEGER,
  intent_score INTEGER,
  readiness_tier TEXT,
  brain_version TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  source_lead_key TEXT NOT NULL UNIQUE,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_sync_events (
  idempotency_key TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL,
  operation TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  result_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dispatch_decisions (
  dispatch_decision_id TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  campaign_id TEXT NOT NULL,
  allowed INTEGER NOT NULL CHECK(allowed IN (0,1)),
  reason_code TEXT NOT NULL,
  gate_json TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  decided_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS provider_outbox (
  provider_idempotency_key TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  campaign_id TEXT NOT NULL,
  provider_name TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('PENDING','SENT','BLOCKED','FAILED')),
  request_json TEXT NOT NULL,
  response_json TEXT,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crm_leads_campaign_status ON crm_leads(campaign_id, lifecycle_status);
CREATE INDEX IF NOT EXISTS idx_dispatch_lead ON dispatch_decisions(lead_id, decided_at_utc);
CREATE INDEX IF NOT EXISTS idx_outbox_status ON provider_outbox(status);
