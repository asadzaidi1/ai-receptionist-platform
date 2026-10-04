PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS crm_call_status (
  call_id TEXT PRIMARY KEY REFERENCES call_sessions(call_id),
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  status TEXT NOT NULL CHECK(status IN ('CREATED','RINGING','ANSWERED','COMPLETED','FAILED','OPTED_OUT')),
  disposition TEXT,
  last_event_id TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_status_history (
  status_event_id TEXT PRIMARY KEY,
  call_id TEXT NOT NULL REFERENCES call_sessions(call_id),
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  from_status TEXT,
  to_status TEXT NOT NULL,
  disposition TEXT,
  source_event_id TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_status_sync_events (
  source_event_id TEXT PRIMARY KEY,
  call_id TEXT NOT NULL REFERENCES call_sessions(call_id),
  lead_id TEXT NOT NULL REFERENCES crm_leads(lead_id),
  sync_status TEXT NOT NULL CHECK(sync_status IN ('APPLIED','REPLAYED','REJECTED')),
  payload_hash TEXT NOT NULL,
  result_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crm_call_status_status ON crm_call_status(status, updated_at_utc);
CREATE INDEX IF NOT EXISTS idx_crm_status_history_lead ON crm_status_history(lead_id, created_at_utc);
CREATE INDEX IF NOT EXISTS idx_crm_sync_status ON crm_status_sync_events(sync_status, created_at_utc);
