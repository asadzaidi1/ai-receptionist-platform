#!/usr/bin/env python3
from __future__ import annotations
import json, sqlite3, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from analytics import get_dashboard_metrics, get_recent_activity
from staging_crm import init_staging

HTML = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Calling Operations</title><style>
:root{--bg:#0d1117;--panel:#151c25;--line:#263342;--text:#e6edf3;--muted:#8b9aaa;--good:#39d98a;--warn:#ffca5c;--bad:#ff6b6b;--blue:#68a7ff}*{box-sizing:border-box}body{margin:0;background:linear-gradient(135deg,#0d1117,#101923);color:var(--text);font:14px system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1180px;margin:0 auto;padding:28px}.top{display:flex;justify-content:space-between;align-items:end;border-bottom:1px solid var(--line);padding-bottom:18px}.eyebrow{color:var(--blue);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:11px}h1{margin:7px 0 0;font-size:32px}p{color:var(--muted)}.pulse{color:var(--good);font-size:12px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0}.card,.panel{background:rgba(21,28,37,.9);border:1px solid var(--line);border-radius:12px;padding:16px}.label{color:var(--muted);font-size:12px}.value{font-size:28px;font-weight:750;margin-top:8px}.value.good{color:var(--good)}.value.warn{color:var(--warn)}.value.bad{color:var(--bad)}.layout{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}.panel h2{font-size:14px;margin:0 0 14px}.bars{display:grid;gap:12px}.barrow{display:grid;grid-template-columns:120px 1fr 45px;align-items:center;gap:10px;color:var(--muted);font-size:12px}.track{height:9px;background:#222d3a;border-radius:10px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,var(--blue),#9c7cff)}.activity{display:grid;gap:8px;max-height:420px;overflow:auto}.event{border-left:2px solid var(--blue);padding:7px 10px;background:#111820}.event small{color:var(--muted)}.event strong{display:block;margin:3px 0}.footer{color:var(--muted);font-size:11px;margin-top:18px}@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}.layout{grid-template-columns:1fr}}@media(max-width:480px){main{padding:16px}.grid{grid-template-columns:1fr 1fr}.value{font-size:22px}}
</style></head><body><main><section class="top"><div><div class="eyebrow">Phase 4 / Operations</div><h1>Calling Control Room</h1><p>CRM status, provider events, dispatch health, and conversion signals.</p></div><div class="pulse">● LIVE <span id="updated"></span></div></section><section class="grid" id="cards"></section><section class="layout"><div class="panel"><h2>Call status</h2><div class="bars" id="bars"></div></div><div class="panel"><h2>Recent audited activity</h2><div class="activity" id="activity"></div></div></section><div class="footer">Read-only analytics view. Dispatch authorization remains server-side and fail-closed.</div></main><script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function card(label,value,cls=''){return `<div class="card"><div class="label">${label}</div><div class="value ${cls}">${esc(value)}</div></div>`}
function render(m){document.getElementById('cards').innerHTML=card('Staged leads',m.staged_leads)+card('Pending dispatch',m.pending_dispatch,'warn')+card('Sent calls',m.sent_calls,'good')+card('Blocked dispatch',m.blocked_dispatch,'bad')+card('Answer rate',((m.answer_rate||0)*100).toFixed(1)+'%','good')+card('Failure rate',((m.failure_rate||0)*100).toFixed(1)+'%','bad')+card('Opt-out rate',((m.opt_out_rate||0)*100).toFixed(1)+'%','warn')+card('Reconciliation open',m.reconciliation_open,m.reconciliation_open?'bad':'good');const vals=[['Created',m.created_calls],['Ringing',m.ringing_calls],['Answered',m.answered_calls],['Completed',m.completed_calls],['Failed',m.failed_calls],['Opted out',m.opted_out_calls]];const max=Math.max(1,...vals.map(x=>x[1]));document.getElementById('bars').innerHTML=vals.map(x=>`<div class="barrow"><span>${x[0]}</span><div class="track"><div class="fill" style="width:${x[1]/max*100}%"></div></div><b>${x[1]}</b></div>`).join('');document.getElementById('updated').textContent='updated '+new Date().toLocaleTimeString()}
function renderActivity(items){document.getElementById('activity').innerHTML=items.map(e=>`<div class="event"><small>${esc(e.created_at_utc)} · ${esc(e.actor)}</small><strong>${esc(e.event_type)} — ${esc(e.outcome)}</strong><small>${esc(e.lead_id||'')} ${esc(e.call_id||'')}</small></div>`).join('')||'<p>No activity yet.</p>'}
async function refresh(){try{const [m,a]=await Promise.all([fetch('/api/metrics').then(r=>r.json()),fetch('/api/activity').then(r=>r.json())]);render(m);renderActivity(a.items)}catch(e){document.querySelector('.pulse').textContent='● OFFLINE'}}refresh();setInterval(refresh,2000);
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    db_path = None
    def send_json(self, obj, code=200):
        data=json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        u=urlparse(self.path); conn=init_staging(Path(self.db_path))
        try:
            if u.path=='/':
                data=HTML.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
            elif u.path=='/health': self.send_json({'ok':True,'db':str(self.db_path)})
            elif u.path=='/api/metrics': self.send_json(get_dashboard_metrics(conn, parse_qs(u.query).get('campaign_id',[None])[0]))
            elif u.path=='/api/activity': self.send_json({'items':get_recent_activity(conn,int(parse_qs(u.query).get('limit',['25'])[0]))})
            else: self.send_json({'error':'not_found'},404)
        finally: conn.close()
    def log_message(self, format, *args): return

def serve(db_path: str, host='0.0.0.0', port=8765):
    Handler.db_path=db_path
    server=ThreadingHTTPServer((host,port),Handler)
    print(f'Dashboard listening on http://{host}:{port}')
    server.serve_forever()

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--db',required=True); ap.add_argument('--host',default='0.0.0.0'); ap.add_argument('--port',type=int,default=8765); a=ap.parse_args(); serve(a.db,a.host,a.port)
