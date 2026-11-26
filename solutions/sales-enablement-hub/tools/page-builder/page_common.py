import json
SITE = "{{SiteUrl}}"
SITEPATH = "{{SitePath}}"
LISTS = {k: "{{ListId:%s}}" % ("Decks" if k == "Generated Content" else k) for k in ["Content Intake", "Content Library", "Slide Library", "Deck Templates", "Generated Content", "Customer Shares", "Solution Plays", "Content Requests", "Archive"]}
LISTS["Deck Requests"] = "00000000-0000-0000-0000-000000000000"  # retired list, kept so LIBPATH lookups stay valid
LIBPATH = {"Content Intake": "Content Intake", "Content Library": "Content Library", "Slide Library": "Slide Library",
           "Deck Templates": "Deck Templates", "Generated Content": "Generated Content", "Archive": "Archive",
           "Deck Requests": "Lists/Deck Requests", "Customer Shares": "Lists/Customer Shares", "Solution Plays": "Lists/Solution Plays",
           "Content Requests": "Lists/Content Requests"}
FORMS = {
  "deck": "{{SiteUrl}}/Deck%20Templates/Forms/Pick%20a%20template.aspx",
  "request": "{{SiteUrl}}/_layouts/15/listforms.aspx?cid={{ListIdB64:Content Requests}}&nav={{ViewIdB64:Content Requests/Request content}}",
}
PAGES_ALL = [("Home", "Home.html", "Home"), ("Find", "Find.html", "Find content"), ("Plays", "Plays.html", "Plays"),
         ("SlideBuilder", "SlideBuilder.html", "Slide Builder"), ("DeckStudio", "DeckStudio.html", "Deck Studio"),
         ("PublishingDesk", "PublishingDesk.html", "Publishing Desk"), ("ShareCenter", "ShareCenter.html", "Share Center"),
         ("Insights", "Insights.html", "Insights")]

CSS = r"""
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{position:relative;font-family:'Segoe UI Variable','Segoe UI',system-ui,-apple-system,sans-serif;color:#1F2A37;background:#F4F7FB;-webkit-font-smoothing:antialiased}
a{color:inherit}
.top{position:sticky;top:0;z-index:20;background:#0B1F3A;color:#fff;box-shadow:0 2px 18px rgba(11,31,58,.25)}
.topin{max-width:1280px;margin:0 auto;display:flex;align-items:center;gap:22px;padding:12px 28px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.2px;text-decoration:none;white-space:nowrap}
.logo{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#00A3A1,#00C2B8);display:grid;place-items:center;font-weight:800;color:#fff;box-shadow:0 4px 14px rgba(0,163,161,.45)}
.brand small{display:block;font-weight:500;font-size:11px;color:#9FE3E2;letter-spacing:1.4px;text-transform:uppercase}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#C9D6E8;text-decoration:none;font-size:14px;padding:8px 12px;border-radius:999px;transition:.15s}
nav a:hover{background:rgba(255,255,255,.08);color:#fff}
nav a.on{background:#00A3A1;color:#fff;font-weight:600}
.src{position:absolute;top:14px;right:20px;z-index:5;font-size:11px;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.12);color:#C9D6E8;white-space:nowrap}
.src.live{background:rgba(0,163,161,.25);color:#9FE3E2}
.hero{background:radial-gradient(circle at 12% 20%,rgba(0,163,161,.35),transparent 45%),radial-gradient(circle at 88% 80%,rgba(255,107,74,.18),transparent 40%),linear-gradient(140deg,#0B1F3A,#12325C 65%,#0B1F3A);color:#fff}
.heroin{max-width:1280px;margin:0 auto;padding:44px 28px 40px}
.kicker{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#9FE3E2;font-weight:700}
h1{font-size:40px;line-height:1.1;margin:10px 0 10px;font-weight:700;letter-spacing:-.5px}
.hero p.lead{font-size:18px;color:#C9D6E8;max-width:760px;margin:0}
.wrap{max-width:1280px;margin:0 auto;padding:28px}
h2{font-size:22px;margin:30px 0 14px;font-weight:700;color:#0B1F3A;display:flex;align-items:center;gap:10px}
h2 .count{font-size:12px;font-weight:600;color:#6B7785;background:#E6ECF3;border-radius:999px;padding:3px 9px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(auto-fill,minmax(420px,1fr))}.g3{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.g4{grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{background:#fff;border-radius:16px;padding:18px 18px 16px;box-shadow:0 1px 2px rgba(11,31,58,.06),0 8px 24px rgba(11,31,58,.06);border:1px solid #E6ECF3;transition:transform .15s,box-shadow .15s;position:relative}
.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(11,31,58,.08),0 14px 32px rgba(11,31,58,.10)}
.card h3{margin:8px 0 6px;font-size:16px;line-height:1.3;color:#0B1F3A}
.card p{margin:0;font-size:13.5px;line-height:1.5;color:#4A5666}
.meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font-size:11.5px;padding:3px 9px;border-radius:999px;background:#EEF3F8;color:#3B4A5C;white-space:nowrap}
.chip.t{background:#E0F5F4;color:#00706E}.chip.c{background:#FFE9E3;color:#B23C1F}.chip.g{background:#FFF4D6;color:#8A6500}.chip.n{background:#0B1F3A;color:#fff}.chip.ok{background:#E3F4E6;color:#1E7A34}
.type{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#00A3A1}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;font-weight:600;font-size:14px;text-decoration:none;border:0;cursor:pointer;background:#00A3A1;color:#fff;box-shadow:0 4px 14px rgba(0,163,161,.3);font-family:inherit}
.btn:hover{filter:brightness(1.07)}.btn.ghost{background:rgba(255,255,255,.12);color:#fff;box-shadow:none;border:1px solid rgba(255,255,255,.25)}
.btn.light{background:#fff;color:#0B1F3A;box-shadow:0 1px 2px rgba(0,0,0,.08);border:1px solid #DCE4EE}.btn.coral{background:#FF6B4A;box-shadow:0 4px 14px rgba(255,107,74,.3)}
.btn.sm{padding:6px 11px;font-size:12.5px;border-radius:8px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.search{display:flex;gap:10px;margin-top:22px;max-width:760px}
.search input{flex:1;font:inherit;font-size:16px;padding:14px 18px;border-radius:12px;border:0;outline:none;box-shadow:0 6px 24px rgba(0,0,0,.25)}
select,input[type=text]{font:inherit;font-size:13.5px;padding:8px 10px;border-radius:9px;border:1px solid #D5DEE9;background:#fff;color:#1F2A37}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#fff;border:1px solid #E6ECF3;border-radius:14px;padding:12px 14px;box-shadow:0 1px 2px rgba(11,31,58,.05)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-top:-34px;position:relative}
.kpi{background:#fff;border-radius:16px;padding:16px 18px;box-shadow:0 10px 30px rgba(11,31,58,.12);border:1px solid #E6ECF3}
.kpi b{display:block;font-size:30px;color:#0B1F3A;letter-spacing:-.5px}.kpi span{font-size:12.5px;color:#6B7785}
.kpi.alert b{color:#FF6B4A}.kpi.good b{color:#00A3A1}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #E6ECF3;font-size:13.5px}
th{text-align:left;background:#F7F9FC;color:#6B7785;font-weight:600;font-size:12px;letter-spacing:.4px;text-transform:uppercase;padding:10px 12px;border-bottom:1px solid #E6ECF3}
td{padding:11px 12px;border-bottom:1px solid #EEF2F7;vertical-align:top}tr:last-child td{border-bottom:0}
.empty{padding:28px;text-align:center;color:#6B7785;background:#fff;border-radius:14px;border:1px dashed #D5DEE9}
.icon{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;font-size:18px;flex:none}
.foot{max-width:1280px;margin:10px auto 40px;padding:0 28px;color:#8A96A6;font-size:12px}
.pill-ok{color:#1E7A34}.pill-warn{color:#B76E00}.pill-bad{color:#C2391B}
.bar{height:10px;border-radius:999px;background:#EEF2F7;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#00A3A1,#3CCFC8);border-radius:999px}
.flow{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:6px}
.step{background:#fff;border:1px solid #E6ECF3;border-radius:14px;padding:14px;position:relative}
.step .n{width:26px;height:26px;border-radius:50%;background:#0B1F3A;color:#fff;font-weight:700;font-size:13px;display:grid;place-items:center}
.step.ai .n{background:#00A3A1}.step.h .n{background:#FF6B4A}
.step b{display:block;margin:8px 0 4px;color:#0B1F3A}.step span{font-size:12.5px;color:#4A5666;line-height:1.45}
@media(max-width:900px){.flow{grid-template-columns:1fr 1fr}.g2{grid-template-columns:1fr}h1{font-size:30px}}
"""

DATA_JS = r"""
var SITE=__SITE__,SITEPATH=__SITEPATH__,LISTS=__LISTS__,LIBPATH=__LIBPATH__,FORMS=__FORMS__;
var SNAP=JSON.parse(document.getElementById('snapshot').textContent);
var SOURCE={live:0,total:0};
function decodeKey(k){return k.replace(/_x([0-9a-fA-F]{4})_/g,function(s,c){return String.fromCharCode(parseInt(c,16));});}
function liveRows(name){
  var key='list:'+SITE+'/'+LISTS[name];var R=window.__LD_RESULTS__||{};var r=R[key];
  if(!r){for(var k in R){if(k.toLowerCase().indexOf(String(LISTS[name]).toLowerCase())>=0){r=R[k];break;}}}
  if(!r||r.format!=='rows'||!r.content)return null;
  try{var p=JSON.parse(r.content);var h=p.headers||[];
    return (p.rows||[]).map(function(a){var o={};for(var i=0;i<h.length;i++){o[h[i]]=a[i];var d=decodeKey(h[i]);if(!(d in o))o[d]=a[i];}return o;});
  }catch(e){return null;}
}
var SRCS={};function rows(name){var l=liveRows(name);var out;if(l){SOURCE.live++;out=l;}else{out=(SNAP[name]||[]).slice();}SOURCE.total++;var res=out.filter(function(r){var t=String(v(r,'FSObjType')||'0');if(t==='1')return false;if(LIBPATH[name].indexOf('Lists/')!==0){var f=fname(r);return !!f&&f.indexOf('.')>0;}return true;});SRCS[name]={live:!!l,n:res.length};return res;}
function v(r,k){var x=r[k];if(x===undefined||x===null)return '';return x;}
function txt(x){if(x===null||x===undefined)return '';if(Array.isArray(x))return x.map(txt).filter(Boolean).join('; ');
  if(typeof x==='object')return x.title||x.Title||x.lookupValue||x.LookupValue||x.text||x.Label||x.label||'';
  var s=String(x);if(/^\s*[\[{]/.test(s)){try{return txt(JSON.parse(s));}catch(e){}}return s;}
function list(x){if(Array.isArray(x))return x.map(txt).filter(Boolean);var s=txt(x);if(!s)return [];
  if(s.indexOf(';#')>=0)return s.split(';#').map(function(t){return t.trim();}).filter(Boolean);
  return s.split(/\s*[;,]\s*(?=[A-Z0-9])/).map(function(t){return t.trim();}).filter(Boolean);}
function fname(r){var f=txt(r.FileLeafRef||r.LinkFilename||r.LinkFilenameNoMenu||'');if(!f&&r.FileRef){f=String(r.FileRef).split('/').pop();}return f;}
function title(r){return txt(r.Title||r.LinkTitle||r.LinkTitleNoMenu||'')||fname(r).replace(/\.[a-z0-9]+$/i,'');}
function fileUrl(name,r){return SITE+'/'+encodeURI(LIBPATH[name])+'/'+encodeURIComponent(fname(r));}
function HASH(){var h=location.hash||'';if(!h){try{h=window.top.location.hash||'';}catch(e){}}if(!h){try{h=window.parent.location.hash||'';}catch(e){}}return h;}
function listUrl(name){return SITE+'/'+encodeURI(LIBPATH[name])+(LIBPATH[name].indexOf('Lists/')===0?'/AllItems.aspx':'/Forms/AllItems.aspx');}
function itemUrl(name,r){return SITE+'/'+encodeURI(LIBPATH[name])+'/DispForm.aspx?ID='+txt(r.ID);}
function urlOf(x){var s=txt(x);if(!s)return '';if(typeof x==='object'&&x&&x.Url)s=x.Url;s=s.split(', ')[0];if(s.charAt(0)==='/')s='{{TenantUrl}}'+s;return s;}
function num(x){var n=parseFloat(String(txt(x)).replace(/[^0-9.\-]/g,''));return isNaN(n)?0:n;}
function date(x){var s=txt(x);if(!s)return null;var d=new Date(s);if(isNaN(d)){var m=s.match(/(\d{1,2})\/(\d{1,2})\/(\d{4})/);if(m)d=new Date(+m[3],+m[1]-1,+m[2]);}return isNaN(d)?null:d;}
var TODAY=new Date();TODAY.setHours(0,0,0,0);
function days(d){return d?Math.round((d-TODAY)/864e5):null;}
function fmt(d){return d?d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}):'';}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function yes(x){var s=String(txt(x)).toLowerCase();return s==='yes'||s==='1'||s==='true';}
var TYPEICON={'Pitch deck':['\uD83C\uDFAF','#E0F5F4'],'Battlecard':['\u2694\uFE0F','#FFE9E3'],'One-pager':['\uD83D\uDCC4','#EEF3F8'],'Customer story':['\uD83C\uDFC6','#FFF4D6'],'Demo script':['\uD83C\uDFAC','#EDE7FB'],'Pricing guide':['\uD83D\uDCB2','#E3F4E6'],'Proposal template':['\uD83D\uDCDD','#EEF3F8'],'Video':['\u25B6\uFE0F','#FFE9E3'],'Playbook':['\uD83D\uDCD8','#E0F5F4']};
function icon(t){var x=TYPEICON[t]||['\uD83D\uDCCE','#EEF3F8'];return '<div class="icon" style="background:'+x[1]+'">'+x[0]+'</div>';}
function shareChip(s){s=txt(s);if(!s)return '';var c=s.indexOf('Internal')===0?'c':(s.indexOf('Public')===0?'ok':'t');var l=s.indexOf('Internal')===0?'\uD83D\uDD12 Internal only':(s.indexOf('Public')===0?'\uD83C\uDF10 Public':'\uD83E\uDD1D Customer (NDA)');return '<span class="chip '+c+'">'+l+'</span>';}
function expiryChip(d){if(!d)return '';var n=days(d);if(n<0)return '<span class="chip c">Expired '+fmt(d)+'</span>';if(n<=30)return '<span class="chip g">Expires in '+n+' days</span>';return '<span class="chip">Current to '+fmt(d)+'</span>';}
function setSource(){var el=document.getElementById('src');if(!el)return;el.className='src'+(SOURCE.live?' live':'');el.textContent=SOURCE.live?('\u25CF Live from SharePoint ('+SOURCE.live+'/'+SOURCE.total+' lists)'):'\u25CB Sample snapshot';}
var _lastSig='';function sig(){try{return Object.keys(window.__LD_RESULTS__||{}).length+':'+JSON.stringify(window.__LD_RESULTS__||{}).length;}catch(e){return '';}}
function boot(render){function go(){SOURCE={live:0,total:0};SRCS={};try{render();}catch(e){var m=document.getElementById('main');if(m)m.innerHTML='<div class="empty">Something went wrong drawing this page: '+esc(e.message)+'</div>';}setSource();}
  go();_lastSig=sig();var t=0;var iv=setInterval(function(){t++;var s=sig();if(s!==_lastSig){_lastSig=s;go();}if(t>40)clearInterval(iv);},750);}
"""

def snapshot_for(lists):
    snap = json.load(open("snapshot.json"))
    s = json.dumps({k: snap[k] for k in lists}, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

def manifest(lists):
    items = [{"kind": "list", "spItemUrl": "list:%s/%s" % (SITE, LISTS[k]), "webUrl": SITE, "listId": LISTS[k],
              "listServerRelativeUrl": SITEPATH + "/" + LIBPATH[k]} for k in lists]
    return json.dumps(items, separators=(",", ":")).replace("</", "<\\/")

def page(key, ptitle, lists, body, script, extra_css=""):
    js = DATA_JS.replace("__SITE__", json.dumps(SITE)).replace("__SITEPATH__", json.dumps(SITEPATH)) \
        .replace("__LISTS__", json.dumps({k: LISTS[k] for k in LIBPATH})).replace("__LIBPATH__", json.dumps(LIBPATH)) \
        .replace("__FORMS__", json.dumps(FORMS))
    return ("<!DOCTYPE html><html lang=\"en\"><head>"
            '<script type="application/json" class="ka-livedata-manifest">' + manifest(lists) + "</script>"
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>" + ptitle + " | Northwind Sales Hub</title><style>" + CSS + extra_css + "</style></head><body>"
            '<span class="src" id="src">Loading\u2026</span>'
            + body +
            '<div class="foot">Northwind Cloud is a fictional company. Sample built on SharePoint: lists, libraries, approvals, quick steps, forms and site skills. Data on this page refreshes from the site\'s lists.</div>'
            '<script type="application/json" id="snapshot">' + snapshot_for(lists) + "</script>"
            "<script>" + js + "\n" + script + "</script></body></html>")

TABCSS = ".tabs{display:flex;gap:6px;margin:-22px 0 8px;position:relative;flex-wrap:wrap}.tabs a{background:#fff;border:1px solid #E6ECF3;border-radius:999px;padding:9px 16px;font-size:14px;font-weight:600;color:#3B4A5C;text-decoration:none;cursor:pointer;box-shadow:0 6px 18px rgba(11,31,58,.08)}.tabs a.on{background:#0B1F3A;color:#fff;border-color:#0B1F3A}.tabs a .count{margin-left:6px;font-size:11px;background:#FF6B4A;color:#fff;border-radius:999px;padding:1px 7px}"
