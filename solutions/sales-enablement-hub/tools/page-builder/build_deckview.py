import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from theme3 import *
THUMBS = json.load(open("thumbs_datauri.json"))
IC.setdefault("up", '<path d="M12 19V5M6 11l6-6 6 6"/>'); IC.setdefault("down", '<path d="M6 9l6 6 6-6"/>')
snap = json.load(open("snapshot.json"))
ROLES = ['Title','Agenda','Problem','Solution','Proof','Customer story','Pricing','Next steps','Close']
pick = {}
for role in ROLES:
    c = [s for s in snap['Slide Library'] if s.get('SlideRole') == role and 'Internal' not in (s.get('Shareability') or '')]
    c.sort(key=lambda s: (0 if 'Cross' in (s.get('Industry') or '') else 1, int(s.get('SlideOrder') or 99)))
    if c and c[0]['FileLeafRef'] in THUMBS: pick[role] = THUMBS[c[0]['FileLeafRef']]
CSS = r"""
.hint{display:flex;align-items:center;gap:28px;margin-top:32px;flex-wrap:wrap}
.mock{position:relative;width:220px;height:118px;flex:none}
.cp{display:inline-flex;align-items:center;gap:6px;height:34px;padding:0 10px;border-radius:9px;background:#fff;border:1px solid var(--hair2);box-shadow:var(--sh1);font-size:13px;font-weight:600;color:var(--ink)}
.cp svg:first-child{color:var(--violetD)}.cp .dv{width:1px;height:18px;background:var(--hair2);margin:0 2px}
.dd{position:absolute;left:44px;top:40px;display:flex;flex-direction:column;width:170px;padding:4px;border-radius:10px;background:#fff;border:1px solid var(--hair);box-shadow:var(--sh2)}
.mi{display:flex;align-items:center;gap:8px;height:32px;padding:0 10px;border-radius:7px;font-size:13px;color:var(--ink2)}
.mi.on{position:relative;color:var(--ink);font-weight:600;background:var(--bg)}
.mi.on::after{content:"";position:absolute;inset:-3px;border-radius:9px;border:1.5px solid transparent;background:linear-gradient(135deg,var(--ice),var(--violet)) border-box;-webkit-mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:pulse 2.4s var(--spring) infinite}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){.mi.on::after{animation:none;opacity:.8}}
.how{margin:0;max-width:420px;font-size:15px;color:var(--ink2);align-self:center}.how b{color:var(--ink);font-weight:600}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.st{padding:20px;border-radius:var(--rm);background:rgba(255,255,255,.7);border:1px solid var(--hair);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}
.st b{display:block;font-size:15px;font-weight:600;margin:10px 0 4px}.st span{font-size:13.5px;color:var(--ink2)}
.st .k{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:600;background:var(--ink);color:#fff}
.st .k.ai{background:linear-gradient(135deg,var(--iceD),var(--violetD))}
.mt{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.mtc{background:#fff;border-radius:var(--rm);border:1px solid var(--hair);box-shadow:var(--sh2);padding:24px}
.mtc h3{margin:0 0 4px;font-size:18px;font-weight:600;letter-spacing:-.01em}.mtc p{margin:0;color:var(--ink2);font-size:14px}
.film{display:flex;gap:8px;margin-top:20px;overflow-x:auto;padding-bottom:4px}
.fr{flex:none;width:96px}.fr .ph{display:block;width:96px;aspect-ratio:16/9;object-fit:cover;border-radius:6px;box-shadow:0 0 0 1px var(--hair)}
.fr .ph{background:linear-gradient(135deg,#1B2A44,#2F3F66);background-size:cover;background-position:center}
.fr span{display:block;font-size:11px;color:var(--ink3);margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dk{background:#fff;border-radius:var(--rm);border:1px solid var(--hair);box-shadow:var(--sh2);padding:24px;display:flex;flex-direction:column}
.dk h3{margin:12px 0 2px;font-size:18px;font-weight:600}.dk .meta{font-size:13px;color:var(--ink3)}
.dk .tp{margin:14px 0 0;padding:12px 14px;border-radius:12px;background:var(--bg);font-size:13px;color:var(--ink2);white-space:pre-line;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.dk .cardfoot{margin-top:auto;padding-top:20px}
@media (max-width:768px){.steps,.mt{grid-template-columns:1fr}}
"""
GAL = SITE + "/Deck%20Templates/Forms/Pick%20a%20template.aspx"
BODY = stage("Build a deck", "Pick a template. Copilot builds the deck.",
  "Every template shows real example slides. Pick one, answer two quick cards in Copilot, and your deck is saved right here with talking points.",
  '<div class="hint"><a class="btn" target="_top" href="' + GAL + '">' + svg("spark", 16) + 'Pick a template' + svg("arrow", 16) + '</a>'
  '<div class="mock" aria-hidden="true"><span class="cp">' + svg("spark", 15) + 'Copilot<span class="dv"></span>' + svg("down", 14) + '</span><span class="dd"><span class="mi">Ask a question</span><span class="mi on">' + svg("spark", 14) + 'Build a deck</span></span></div>'
  '<p class="how">Already know what you need? <b>Open the Copilot menu</b> at the top of this library and choose <b>Build a deck</b>.</p>'
  '<a class="link" style="margin-left:auto;align-self:center" target="_top" href="' + SITE + '/SitePages/SlideBuilder.html">Browse the slide gallery' + svg("arrow", 16) + '</a></div>'
'<div class="steps"><div class="st"><span class="k">1</span><b>Pick a template</b><span>See the example slides, then choose \u2728 Build with this template.</span></div>'
  '<div class="st"><span class="k ai">' + svg("spark", 14) + '</span><b>Answer two quick cards</b><span>Your meeting first, then the slides you want. Approved content only, nothing to clean up afterwards.</span></div>'
  '<div class="st"><span class="k">3</span><b>Finish in PowerPoint</b><span>Open your deck below, retitle slide 1 and rehearse with the talking points.</span></div></div>') \
  + '<main class="wrap"><div id="main"><div class="grid g3"><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></div></main>'
JS = r"""
var ROLETH=JSON.parse(document.getElementById('roleth').textContent);
var SC={'Draft':'','Reviewed':'info','Shared':'ok'};
function opening(t){var s=txt(t);var m=s.match(/Opening:\s*([^\n]+)/);return m?m[1]:s.split('\n')[0];}
boot(function(){var D=rows('Generated Content').filter(function(r){return /\.pptx?$/i.test(fname(r));}).sort(function(a,b){return (date(b.Modified)||0)-(date(a.Modified)||0);}),
 T=rows('Deck Templates').filter(function(t){return txt(t.OutputFormat)!=='Word';});
 var h='<h2>Recent decks <span class="n">'+D.length+'</span></h2>'+(D.length?'<div class="grid g3 rise">'+D.slice(0,9).map(function(r){var st=txt(r.DraftStatus)||'Draft',tp=txt(r.TalkingPoints);
  return '<article class="dk"><div class="row sp"><span class="pill '+(SC[st]||'')+'">'+esc(st)+'</span><span class="sub">'+fmt(date(r.Modified))+'</span></div><h3>'+esc(txt(r.Customer)||title(r))+'</h3><div class="meta">'+esc([txt(r.Template),txt(r.Industry)].filter(Boolean).join(' \u00B7 '))+'</div>'+(tp?'<div class="tp">'+esc(opening(tp))+'</div>':'')+'<div class="cardfoot"><a class="btn sm" target="_blank" href="'+fileUrl('Generated Content',r)+'">Open deck</a></div></article>';}).join('')+'</div>':empty('No decks yet. Pick a template to make your first one.'));
 h+='<div class="row sp"><h2>Templates</h2><a class="link" target="_top" href="'+SITE+'/Deck%20Templates/Forms/Pick%20a%20template.aspx">Open the template gallery</a></div><div class="mt rise">'+T.map(function(t){var roles=String(txt(t.Recipe)).split(',').map(function(s){return s.trim();}).filter(Boolean);
  return '<article class="mtc"><div class="row sp"><h3>'+esc(txt(t.TemplateKind)||title(t))+'</h3><span class="pill">'+roles.length+' slides</span></div><p>'+esc(txt(t.BestFor))+'</p><div class="film" aria-label="Slide order">'+roles.map(function(ro){return '<div class="fr">'+'<span class="ph"'+(ROLETH[ro]?' style="background-image:url('+ROLETH[ro]+')"':'')+'></span>'+'<span>'+esc(ro)+'</span></div>';}).join('')+'</div></article>';}).join('')+'</div>';
 document.getElementById('main').innerHTML=h;});"""
html = page3("Build a deck", ["Generated Content", "Deck Templates"], BODY, JS, CSS,
             '<script type="application/json" id="roleth">' + json.dumps(pick) + '</script>')

open(os.path.join(HERE, "..", "..", "site", "views", "decks-start-here.html"), "w", encoding="utf-8").write(html)
print(len(html.encode()) // 1024, "KB", sorted(pick))
