import json, sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT/'src'))
from lead_pipeline import process, write_queue_csv
from staging_crm import upsert_ready_queue, init_staging
from dispatch_gate import evaluate_dispatch, queue_provider_request
from provider_adapter import MockCallingProvider, dispatch_pending, sign_webhook, ingest_webhook
from analytics import get_dashboard_metrics, get_recent_activity

RAW=ROOT/'fixtures/raw_leads.csv'; SUP=ROOT/'fixtures/suppression.csv'
SECRET='phase4-secret'
CAMPAIGN={'campaign_id':'pilot_ca_001','status':'PILOT','brain_version':'brain-v1.3','script_version':'script-v1','provider_name':'mock-provider','caller_id_approved':True,'callback_ready':True,'window_start':'09:00','window_end':'17:00'}

def setup(tmp_path):
    db=tmp_path/'phase4.db'; d=process(RAW,SUP,db,today=date(2026,10,4)); out=tmp_path/'queues'; write_queue_csv(d,out); upsert_ready_queue(db,out/'campaign_ready.csv',CAMPAIGN['campaign_id'],CAMPAIGN['brain_version'],'policy-v1'); c=init_staging(db); lead=c.execute('select lead_id from crm_leads order by lead_id limit 1').fetchone()[0]; gate=evaluate_dispatch(c,lead,CAMPAIGN,datetime(2026,10,4,17,0,tzinfo=timezone.utc),[],provider_ready=True,local_minute_override=600); queue_provider_request(c,lead,CAMPAIGN,gate); sent=dispatch_pending(c,MockCallingProvider())[0]; return c,lead,sent

def send(c,event_id,event_type,pcid,at):
    body=json.dumps({'id':event_id,'type':event_type,'data':{'provider_call_id':pcid}},sort_keys=True); ts=str(int(at.timestamp())); headers={'X-Provider-Timestamp':ts,'X-Provider-Signature':sign_webhook(SECRET,ts,body),'X-Provider-Event-Id':event_id}; return ingest_webhook(c,'mock-provider',SECRET,headers,body,at)

def test_crm_status_sync_is_idempotent_and_historical(tmp_path):
    c,lead,sent=setup(tmp_path); at=datetime(2026,10,4,17,1,tzinfo=timezone.utc)
    assert send(c,'s1','call.started',sent['provider_call_id'],at)['status']=='RINGING'
    assert send(c,'s2','call.answered',sent['provider_call_id'],at)['status']=='ANSWERED'
    replay=send(c,'s2','call.answered',sent['provider_call_id'],at)
    assert replay['duplicate'] is True
    assert c.execute('select status from crm_call_status').fetchone()[0]=='ANSWERED'
    assert c.execute('select count(*) from crm_status_history').fetchone()[0]==3
    assert c.execute('select count(*) from crm_status_sync_events').fetchone()[0]==3
    c.close()

def test_metrics_and_activity_reflect_events(tmp_path):
    c,lead,sent=setup(tmp_path); at=datetime(2026,10,4,17,1,tzinfo=timezone.utc)
    send(c,'m1','call.started',sent['provider_call_id'],at); send(c,'m2','call.answered',sent['provider_call_id'],at)
    m=get_dashboard_metrics(c,'pilot_ca_001'); activity=get_recent_activity(c,10)
    assert m['sent_calls']==1 and m['ringing_calls']==0 and m['answered_calls']==1
    assert m['answer_rate']==1.0 and m['reconciliation_open']==0 and m['audit_events']>=3
    assert len(activity)>=3 and any(x['event_type'].startswith('provider.webhook') for x in activity)
    c.close()

def test_failed_and_optout_metrics_are_distinct(tmp_path):
    c,lead,sent=setup(tmp_path); at=datetime(2026,10,4,17,1,tzinfo=timezone.utc)
    send(c,'f1','call.failed',sent['provider_call_id'],at)
    m=get_dashboard_metrics(c,'pilot_ca_001')
    assert m['failed_calls']==1 and m['failure_rate']==1.0 and m['opted_out_calls']==0
    c.close()
