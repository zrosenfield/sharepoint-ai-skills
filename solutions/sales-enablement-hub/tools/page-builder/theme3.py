# "Atmospheric Precision" theme for the Northwind Sales Hub pages (design language 01 in the playbook)
import json
from page_common import SITE, SITEPATH, LISTS, LIBPATH, FORMS, DATA_JS, snapshot_for, manifest

IC = {
 "deck": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v4M8 20h8M7 12l3-3 3 2 4-4"/>',
 "shield": '<path d="M12 3l7 3v5c0 4.6-3 8-7 10-4-2-7-5.4-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "star": '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.9z"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l5.5 3.5-5.5 3.5z"/>',
 "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.4"/>',
 "pen": '<path d="M4 20h4L19.5 8.5a2.1 2.1 0 00-3-3L5 17z"/><path d="M14.5 6.5l3 3"/>',
 "book": '<path d="M5 4.5A1.5 1.5 0 016.5 3H19v15H6.5A1.5 1.5 0 005 19.5z"/><path d="M5 19.5A1.5 1.5 0 006.5 21H19"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="2.8"/>',
 "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "left": '<path d="M15 6l-6 6 6 6"/>', "right": '<path d="M9 6l6 6-6 6"/>',
 "inbox": '<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1.5 2h5L16 13h5"/>',
 "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 00-1-1H5a1 1 0 00-1 1v10a1 1 0 001 1h3"/>',
}
def svg(n, s=20):
    return '<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (s, s, IC[n])

CSS = r"""
:root{--ink:#111827;--ink2:#374151;--ink3:#5B6472;--cloud:#EAF3FC;--ice:#9AC7F5;--iceD:#2F6DB5;--violet:#8B83DB;--violetD:#5A52B0;--bg:#F5F8FC;
--hair:rgba(17,24,39,.08);--hair2:rgba(17,24,39,.14);--rm:20px;
--sh1:0 1px 1px rgba(17,24,39,.04),0 2px 6px -2px rgba(17,24,39,.06);
--sh2:0 1px 1px rgba(17,24,39,.04),0 18px 40px -20px rgba(17,24,39,.22);
--spring:cubic-bezier(.2,.8,.2,1);--ok:#1F7A4D;--okB:#E7F4EC;--warn:#8A5A00;--warnB:#FFF4DC;--bad:#B4232C;--badB:#FDECEE}
*{box-sizing:border-box}html,body{margin:0}
body{position:relative;font-family:"Segoe UI Variable Text","Segoe UI Variable","Segoe UI",-apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;font-size:15px;line-height:1.5;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;min-height:100vh}
.aura{position:absolute;inset:0 0 auto 0;height:760px;pointer-events:none;z-index:0;background:radial-gradient(900px 480px at 88% -12%,rgba(154,199,245,.5),transparent 62%),radial-gradient(720px 420px at 4% -4%,rgba(139,131,219,.22),transparent 62%)}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.stage{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:72px 32px 40px}
.wrap{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:0 32px 96px}
.eyebrow{font-size:13px;font-weight:600;color:var(--violetD);letter-spacing:.01em;display:flex;align-items:center;gap:8px}
h1{font-size:clamp(34px,4.6vw,54px);line-height:1.05;letter-spacing:-.03em;font-weight:600;margin:12px 0 16px;max-width:860px}
.lede{font-size:clamp(16px,1.6vw,19px);line-height:1.5;color:var(--ink2);max-width:680px;margin:0}
h2{font-size:22px;letter-spacing:-.015em;font-weight:600;margin:56px 0 20px;display:flex;align-items:baseline;gap:10px}
h2 .n{font-size:14px;font-weight:500;color:var(--ink3);font-variant-numeric:tabular-nums}
h2 .more{margin-left:auto}
.row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.row.sp{justify-content:space-between}.mt3{margin-top:24px}.mt4{margin-top:32px}
.link{color:var(--iceD);font-weight:600;font-size:14px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;cursor:pointer;background:none;border:0;font-family:inherit;padding:0}
.link:hover{text-decoration:underline;text-underline-offset:3px}
:focus-visible{outline:2px solid var(--iceD);outline-offset:3px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 20px;border-radius:999px;font:inherit;font-size:15px;font-weight:600;text-decoration:none;border:0;cursor:pointer;background:var(--ink);color:#fff;white-space:nowrap;box-shadow:0 1px 1px rgba(17,24,39,.2),0 10px 24px -10px rgba(17,24,39,.55);transition:transform .3s var(--spring),box-shadow .3s var(--spring),background .2s}
.btn:hover{transform:translateY(-1px);box-shadow:0 1px 1px rgba(17,24,39,.2),0 16px 32px -12px rgba(17,24,39,.6)}.btn:active{transform:scale(.98)}
.btn.sec{background:#fff;color:var(--ink);border:1px solid var(--hair2);box-shadow:var(--sh1)}
.btn.ice{background:var(--ice);color:var(--ink);box-shadow:0 10px 30px -10px rgba(154,199,245,.8)}
.btn.glass{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.22);box-shadow:none}
.btn.glass:hover{background:rgba(255,255,255,.16)}
.btn.sm{height:36px;padding:0 14px;font-size:14px}
.grid{display:grid;gap:24px}.g2{grid-template-columns:repeat(auto-fill,minmax(440px,1fr))}.g3{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.g4{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.card{position:relative;display:flex;flex-direction:column;background:#fff;border-radius:var(--rm);padding:24px;border:1px solid var(--hair);box-shadow:var(--sh2);color:inherit;text-decoration:none;transition:transform .4s var(--spring),box-shadow .4s var(--spring)}
a.card:hover,.card.hov:hover{transform:translateY(-3px);box-shadow:0 1px 1px rgba(17,24,39,.04),0 30px 60px -26px rgba(17,24,39,.34)}
.card h3{font-size:17px;line-height:1.3;letter-spacing:-.01em;font-weight:600;margin:16px 0 8px}
.card p{margin:0;color:var(--ink2);font-size:14px;line-height:1.55}
.clamp3{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.kind{font-size:13px;color:var(--ink3);font-weight:500}
.cardfoot{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:16px;border-top:1px solid var(--hair);flex-wrap:wrap}
.card p+.cardfoot,.card .clamp3+.cardfoot{margin-top:20px}
.go{margin-left:auto;color:var(--iceD);font-weight:600;font-size:14px;display:inline-flex;align-items:center;gap:6px}
.tile{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;color:var(--iceD);background:linear-gradient(150deg,#F4F9FE,#E1ECFA);box-shadow:inset 0 0 0 1px rgba(47,109,181,.1),inset 0 1px 0 #fff;flex:none}
.tag{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:500;color:var(--ink2);white-space:nowrap}
.tag i{width:7px;height:7px;border-radius:50%;background:var(--ink3)}.tag.pub i{background:var(--iceD)}.tag.nda i{background:var(--violet)}
.tag.int,.tag.bad{color:var(--bad)}.tag.bad i{background:var(--bad)}.tag.warn{color:var(--warn)}.tag.warn i{background:#E0A100}
.pill{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 10px;border-radius:999px;font-size:12px;font-weight:600;background:rgba(17,24,39,.05);color:var(--ink2);white-space:nowrap}
.pill.ok{background:var(--okB);color:var(--ok)}.pill.warn{background:var(--warnB);color:var(--warn)}.pill.bad{background:var(--badB);color:var(--bad)}.pill.info{background:#E7EFFB;color:var(--iceD)}.pill.vio{background:#EEEDFA;color:var(--violetD)}
.toolbar{position:sticky;top:16px;z-index:10;display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:12px;border-radius:24px;background:rgba(255,255,255,.74);-webkit-backdrop-filter:blur(20px) saturate(180%);backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(255,255,255,.85);box-shadow:var(--sh1),0 24px 48px -28px rgba(17,24,39,.3)}
.field{display:flex;align-items:center;gap:10px;height:44px;padding:0 16px;border-radius:999px;background:#fff;border:1px solid var(--hair2);flex:1;min-width:220px;color:var(--ink3);transition:border-color .2s,box-shadow .2s}
.field input{border:0;outline:0;font:inherit;font-size:15px;flex:1;min-width:0;background:transparent;color:var(--ink)}
.field:focus-within{border-color:var(--iceD);box-shadow:0 0 0 4px rgba(47,109,181,.12)}
.select{position:relative;display:inline-block}.select select{-webkit-appearance:none;appearance:none;height:44px;padding:0 38px 0 16px;border-radius:999px;border:1px solid var(--hair2);background:#fff;font:inherit;font-size:14px;color:var(--ink);cursor:pointer;max-width:220px}
.select::after{content:"";position:absolute;right:17px;top:50%;width:7px;height:7px;border-right:1.6px solid var(--ink3);border-bottom:1.6px solid var(--ink3);transform:translateY(-70%) rotate(45deg);pointer-events:none}
.seg{display:inline-flex;gap:2px;padding:4px;border-radius:999px;background:rgba(17,24,39,.05);max-width:100%;overflow-x:auto;scrollbar-width:none}.seg::-webkit-scrollbar{display:none}
.seg button{flex:none;height:36px;padding:0 16px;border:0;border-radius:999px;background:transparent;font:inherit;font-size:14px;font-weight:500;color:var(--ink2);cursor:pointer;transition:background .3s var(--spring),color .2s,box-shadow .3s var(--spring)}
.seg button:hover{color:var(--ink)}.seg button[aria-pressed=true],.seg button[aria-selected=true]{background:#fff;color:var(--ink);box-shadow:0 1px 1px rgba(17,24,39,.06),0 6px 16px -6px rgba(17,24,39,.28)}
.seg .c{margin-left:6px;font-size:12px;color:var(--ink3);font-variant-numeric:tabular-nums}.seg .c.hot{color:var(--bad);font-weight:600}
.seg.full{flex-basis:100%}
.switch{display:inline-flex;align-items:center;gap:10px;font-size:14px;color:var(--ink2);cursor:pointer}
.switch input{-webkit-appearance:none;appearance:none;width:44px;height:26px;border-radius:999px;background:rgba(17,24,39,.16);position:relative;cursor:pointer;transition:background .25s;margin:0;flex:none}
.switch input::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);transition:transform .35s var(--spring)}
.switch input:checked{background:var(--iceD)}.switch input:checked::after{transform:translateX(18px)}
.panel{background:#fff;border-radius:var(--rm);border:1px solid var(--hair);box-shadow:var(--sh2);overflow:hidden}.panel.scroll{overflow-x:auto}
.panel.pad{padding:24px}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:640px}
th{text-align:left;font-weight:500;font-size:12.5px;color:var(--ink3);padding:18px 20px 12px;border-bottom:1px solid var(--hair);white-space:nowrap}
td{padding:16px 20px;border-bottom:1px solid var(--hair);vertical-align:top}tbody tr:last-child td{border-bottom:0}
tbody tr{transition:background .2s}tbody tr:hover{background:#F8FBFE}
td a{color:var(--ink);font-weight:600;text-decoration:none}td a:hover{color:var(--iceD)}
.sub{font-size:13px;color:var(--ink3)}
.empty{display:flex;flex-direction:column;align-items:center;gap:12px;padding:48px 24px;text-align:center;color:var(--ink3);background:rgba(255,255,255,.55);border:1px dashed var(--hair2);border-radius:var(--rm)}
.empty svg{color:var(--violet)}.empty p{margin:0;max-width:380px}
.skel{height:220px;border-radius:var(--rm);border:1px solid var(--hair);background:linear-gradient(100deg,#fff 30%,#EFF5FC 50%,#fff 70%);background-size:300% 100%;animation:sh 1.4s linear infinite}
@keyframes sh{to{background-position:-150% 0}}
.rise>*{animation:rise .7s var(--spring) both}
.rise>*:nth-child(2){animation-delay:.04s}.rise>*:nth-child(3){animation-delay:.08s}.rise>*:nth-child(4){animation-delay:.12s}.rise>*:nth-child(5){animation-delay:.16s}.rise>*:nth-child(6){animation-delay:.2s}.rise>*:nth-child(n+7){animation-delay:.24s}
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
.src{position:absolute;top:16px;right:20px;z-index:20;display:inline-flex;align-items:center;gap:8px;height:28px;padding:0 12px;border-radius:999px;font-size:12px;font-weight:500;color:var(--ink2);background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border:1px solid var(--hair)}
.src i{width:7px;height:7px;border-radius:50%;background:#9CA3AF}.src.live i{background:#2FB872;box-shadow:0 0 0 4px rgba(47,184,114,.18)}.src.part i{background:#D69E2E;box-shadow:0 0 0 4px rgba(214,158,46,.18)}
.src{cursor:default;outline:0}.src .pop{display:none;position:absolute;top:36px;right:0;min-width:260px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);border:1px solid var(--hair);box-shadow:var(--sh2);color:var(--ink2);font-size:12.5px;line-height:1.4}
.src:hover .pop,.src:focus .pop,.src:focus-within .pop{display:block}.pop b{display:block;color:var(--ink);font-weight:600;margin-bottom:6px}.pop .r{display:flex;justify-content:space-between;gap:16px;padding:3px 0}.pop .y{color:var(--ok);font-weight:600}.pop .n{color:var(--warn);font-weight:600}.pop .note{display:block;border-top:1px solid var(--hair);margin-top:6px;padding-top:8px;color:var(--ink3)}
.foot{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:0 32px 48px;color:var(--ink3);font-size:12.5px}
.bars .b{display:grid;grid-template-columns:150px 1fr 48px;gap:14px;align-items:center;margin:12px 0;font-size:14px}
.track{height:8px;border-radius:999px;background:rgba(17,24,39,.06);overflow:hidden}.track i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,var(--ice),var(--violet))}
.bars b{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.listrow{display:flex;gap:16px;align-items:center;padding:16px 24px;border-top:1px solid var(--hair);text-decoration:none;color:inherit;transition:background .2s}
.listrow:first-child{border-top:0}a.listrow:hover{background:#F8FBFE}.listrow .t{flex:1;min-width:0}.listrow b{display:block;font-weight:600}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
@media (max-width:768px){.stage{padding:56px 20px 24px}.wrap{padding:0 20px 64px}.foot{padding:0 20px 40px}h2{margin-top:40px}.toolbar{top:8px;border-radius:20px}.g2,.g3{grid-template-columns:1fr}.select select{max-width:160px}.src{top:10px;right:12px}}
"""

THEME_JS = r"""
var IC=__IC__;
function svg(n,s){s=s||20;return '<svg viewBox="0 0 24 24" width="'+s+'" height="'+s+'" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(IC[n]||IC.doc)+'</svg>';}
var TYPEMAP={'Pitch deck':'deck','Battlecard':'shield','One-pager':'doc','Customer story':'star','Demo script':'play','Pricing guide':'tag','Proposal template':'pen','Video':'play','Playbook':'book'};
function icon(t){return '<span class="tile">'+svg(TYPEMAP[t]||'doc')+'</span>';}
function shareChip(s){s=txt(s);if(!s)return '';var k=s.indexOf('Internal')===0?'int':(s.indexOf('Public')===0?'pub':'nda');
 return '<span class="tag '+k+'">'+(k==='int'?svg('lock',13):'<i></i>')+({int:'Internal only',pub:'Public',nda:'Customer \u00B7 NDA'}[k])+'</span>';}
function expiryChip(d){if(!d)return '';var n=days(d);if(n<0)return '<span class="tag bad"><i></i>Expired '+fmt(d)+'</span>';if(n<=30)return '<span class="tag warn"><i></i>Expires in '+n+' days</span>';return '';}
function setSource(){var el=document.getElementById('src');if(!el)return;var k=Object.keys(SRCS),lv=k.filter(function(n){return SRCS[n].live;}).length,all=k.length&&lv===k.length;
 var st=all?'live':(lv?'part':'');el.className='src '+st;el.innerHTML='<i></i>'+(all?'Live':(lv?'Partly live':'Sample data'))+'<span class="pop" role="tooltip"><b>Data sources</b>'+k.map(function(n){return '<span class="r"><span>'+esc(n==='Generated Content'?'Decks':n)+'</span><span class="'+(SRCS[n].live?'y':'n')+'">'+(SRCS[n].live?'Live':'Sample')+' \u00B7 '+SRCS[n].n+'</span></span>';}).join('')+(window.__USAGE_NOTE__?'<span class="r note">'+esc(window.__USAGE_NOTE__)+'</span>':'')+'</span>';
 el.setAttribute('tabindex','0');el.setAttribute('aria-label',(all?'Live':(lv?'Partly live':'Sample data'))+': '+k.map(function(n){return n+' '+(SRCS[n].live?'live':'sample')+' '+SRCS[n].n+' rows';}).join(', '));}
function empty(msg){return '<div class="empty">'+svg('spark',28)+'<p>'+msg+'</p></div>';}
function skel(n){var s='';for(var i=0;i<(n||6);i++)s+='<div class="skel"></div>';return '<div class="grid g3">'+s+'</div>';}
function bars(obj){var ks=Object.keys(obj).sort(function(a,b){return obj[b]-obj[a];});var m=Math.max.apply(null,ks.map(function(k){return obj[k];}).concat([1]));
 return '<div class="bars">'+ks.map(function(k){return '<div class="b"><span>'+esc(k)+'</span><div class="track"><i style="width:'+Math.max(2,Math.round(100*obj[k]/m))+'%"></i></div><b>'+obj[k]+'</b></div>';}).join('')+'</div>';}
function assetCard(r){var t=txt(r.AssetType);return '<a class="card" target="_blank" href="'+fileUrl('Content Library',r)+'"><div class="row">'+icon(t)+'<span class="kind">'+esc(t)+'</span>'+(yes(r.Featured)?'<span class="pill info" style="margin-left:auto">Featured</span>':'')+'</div><h3>'+esc(title(r))+'</h3><p class="clamp3">'+esc(txt(r.AISummary))+'</p><div class="cardfoot">'+shareChip(r.Shareability)+expiryChip(date(r.ExpiresOn))+'<span class="go">Open '+svg('arrow',16)+'</span></div></a>';}
"""

def page3(ptitle, lists, body, script, extra_css="", extra_json=""):
    js = DATA_JS.replace("__SITE__", json.dumps(SITE)).replace("__SITEPATH__", json.dumps(SITEPATH)) \
        .replace("__LISTS__", json.dumps({k: LISTS[k] for k in LIBPATH})).replace("__LIBPATH__", json.dumps(LIBPATH)) \
        .replace("__FORMS__", json.dumps(FORMS))
    tj = THEME_JS.replace("__IC__", json.dumps(IC))
    h = ("<!DOCTYPE html><html lang=\"en\"><head>"
         '<script type="application/json" class="ka-livedata-manifest">' + manifest(lists) + "</script>"
         '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         "<title>" + ptitle + " &#183; Northwind Sales Hub</title><style>" + CSS + extra_css + "</style></head><body>"
         '<div class="aura" aria-hidden="true"></div><span class="src" id="src" role="status"><i></i>Loading</span>'
         + body +
         '<footer class="foot">Northwind Cloud is a fictional company used for this sample. Built entirely on SharePoint: lists, libraries, approvals, quick steps, forms and site skills.</footer>'
         + extra_json +
         '<script type="application/json" id="snapshot">' + snapshot_for(lists) + "</script>"
         "<script>" + js + "\n" + tj + "\n" + script + "</script></body></html>")
    return h.encode("utf-16", "surrogatepass").decode("utf-16")

def stage(eyebrow, h1, lede, extra=""):
    return '<header class="stage"><div class="eyebrow">%s</div><h1>%s</h1><p class="lede">%s</p>%s</header>' % (eyebrow, h1, lede, extra)
