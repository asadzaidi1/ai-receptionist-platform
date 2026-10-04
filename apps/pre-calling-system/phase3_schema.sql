PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS provider_webhook_events (
  provider_event_id TEXT PRIMARY KEY,
  provider_name TEXT NOT NULL,
  event_type TEXT,
  request_timestamp TEXT,
  signature TEXT,
  signature_verified INTEGER NOT NULL CHECK(signature_verified IN (0,1)),
  raw_body TEXT NOT NULL,
  processing_status TEXT NOT NULL CHECK(processing_status IN ('RECEIVED','PROCESSED','DUPLICATE','REJECTED','RECONCILIATION')),
  result_json TEXT,
  received_at_utc TEXT NOT NULL,
  processed_at_utc TEXT
);

CREATE TABLE IF NOT EXISTS call_sessions (
  call_id TEXT PRIMARY KEY,
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  campaign_id TEXT NOT NULL,
  provider_name TEXT NOT NULL,
  provider_call_id TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL CHECK(status IN ('CREATED','RINGING','ANSWERED','COMPLETED','FAILED','OPTED_OUT')),
  last_provider_event_id TEXT,
  started_at_utc TEXT,
  answered_at_utc TEXT,
  ended_at_utc TEXT,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS call_event_history (
  provider_event_id TEXT PRIMARY KEY,
  call_id TEXT NOT NULL REFERENCES call_sessions(call_id),
  event_type TEXT NOT NULL,
  prior_status TEXT NOT NULL,
  next_status TEXT NOT NULL,
  event_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reconciliation_queue (
  reconciliation_id TEXT PRIMARY KEY,
  provider_event_id TEXT NOT NULL UNIQUE,
  provider_name TEXT NOT NULL,
  reason_code TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('OPEN','RESOLVED','IGNORED')),
  payload_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  resolved_at_utc TEXT
);

CREATE TABLE IF NOT EXISTS audit_events (
  audit_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor TEXT NOT NULL,
  lead_id TEXT,
  call_id TEXT,
  idempotency_key TEXT,
  outcome TEXT NOT NULL,
  metadata_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  UNIQUE(event_type, idempotency_key)
);

CREATE INDEX IF NOT EXISTS idx_webhooks_status ON provider_webhook_events(processing_status);
CREATE INDEX IF NOT EXISTS idx_call_sessions_lead ON call_sessions(lead_id, updated_at_utc);
CREATE INDEX IF NOT EXISTS idx_audit_lead ON audit_events(lead_id, created_at_utc);
CREATE INDEX IF NOT EXISTS idx_reconciliation_status ON reconciliation_queue(status);
