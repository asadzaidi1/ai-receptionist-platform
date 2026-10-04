#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from staging_crm import upsert_ready_queue

ap = argparse.ArgumentParser(description='Stage CAMPAIGN_READY records; never place calls.')
ap.add_argument('--db', type=Path, required=True)
ap.add_argument('--ready-csv', type=Path, required=True)
ap.add_argument('--campaign-id', required=True)
ap.add_argument('--brain-version', required=True)
ap.add_argument('--policy-version', required=True)
args = ap.parse_args()
result = upsert_ready_queue(args.db, args.ready_csv, args.campaign_id, args.brain_version, args.policy_version)
print(json.dumps({'records_received': len(result), 'new_or_upserted': sum(not r['replayed'] for r in result), 'replayed': sum(r['replayed'] for r in result), 'live_calls': 0}, indent=2))
