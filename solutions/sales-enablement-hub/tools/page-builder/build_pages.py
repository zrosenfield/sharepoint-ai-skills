import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
OUT = os.path.join(HERE, "..", "..", "site", "pages")
from theme3 import *
THUMBS = json.load(open(os.path.join(HERE, "thumbs_datauri.json")))
KEEP = {"Home.html", "Find.html", "Plays.html", "SlideBuilder.html", "PublishingDesk.html"}
P = {}
SP = SITE + "/SitePages/"
DECKS = SITE + "/Deck%20Templates/Forms/Pick%20a%20template.aspx"

# ================= HOME =================
HOME_CSS = r"""
.night{position:relative;z-index:1;background:#0A101C;color:#fff;overflow:hidden;border-radius:0 0 40px 40px}
.night::before{content:"";position:absolute;inset:0;background:radial-gradient(560px 400px at 76% 26%,rgba(154,199,245,.42),transparent 62%),radial-gradient(500px 360px at 22% 92%,rgba(139,131,219,.40),transparent 64%),radial-gradient(1000px 320px at 50% 130%,rgba(154,199,245,.20),transparent 70%)}
.night::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,rgba(154,199,245,.7),transparent)}
.night .stage{padding:88px 32px 136px}.night .eyebrow{color:var(--ice)}.night h1{color:#fff}.night .lede{color:#C7D2E3}
.night :focus-visible{outline-color:var(--ice)}
.find{display:flex;align-items:center;gap:10px;margin-top:40px;max-width:720px;height:62px;padding:7px 7px 7px 22px;border-radius:999px;color:#C7D2E3;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);-webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 24px 60px -24px rgba(0,0,0,.7);transition:border-color .25s,box-shadow .25s}
.find:focus-within{border-color:rgba(154,199,245,.75);box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 0 0 4px rgba(154,199,245,.18),0 24px 60px -24px rgba(0,0,0,.7)}
.find input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:#fff;font:inherit;font-size:17px}.find input::placeholder{color:#9AA6B8}
.lift{margin-top:-80px}
.play{background:rgba(255,255,255,.86);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px)}
.numeral{font-size:44px;font-weight:600;letter-spacing:-.04em;line-height:1;background:linear-gradient(135deg,var(--iceD),var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent}
@media (max-width:768px){.night .stage{padding:72px 20px 104px}.find{height:56px}.lift{margin-top:-64px}}
"""
P["Home.html"] = page3("Home", ["Content Library", "Solution Plays"],
 '<section class="night"><div class="stage"><div class="eyebrow" id="today">For Northwind sellers</div><script>try{document.getElementById("today").textContent=new Date().toLocaleDateString(undefined,{weekday:"long",month:"long",day:"numeric"});}catch(e){}</script><h1>Everything for your next customer conversation.</h1>'
 '<p class="lede">Approved content, plays that work, and a deck built for your meeting in minutes.</p>'
 '<form class="find" role="search" onsubmit="go(event)"><label for="q" class="vh">Search content</label>' + svg("search") + '<input id="q" autocomplete="off" placeholder="Search decks, battlecards, customer stories"><button class="btn ice">Search</button></form>'
 '<div class="row mt3"><a class="btn glass" target="_top" href="' + DECKS + '">' + svg("spark", 18) + 'Build a deck</a><a class="btn glass" target="_blank" href="' + FORMS["request"] + '">Ask for content</a></div></div></section>'
 '<main class="wrap lift" id="main"><div class="grid g3"><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></main>',
 r"""
function go(e){e.preventDefault();window.top.location.href=SITE+'/SitePages/Find.html#q='+encodeURIComponent(document.getElementById('q').value);}
boot(function(){
 var lib=rows('Content Library').filter(function(r){var n=days(date(r.ExpiresOn));return n===null||n>=0;}),plays=rows('Solution Plays');
 var pl=plays.slice().sort(function(a,b){return num(a.PlayOrder)-num(b.PlayOrder);}).slice(0,3);
 var feat=lib.filter(function(r){return yes(r.Featured);}).sort(function(a,b){return num(b.Views)-num(a.Views);}).slice(0,6);
 var recent=lib.slice().sort(function(a,b){return (date(b.PublishedOn)||0)-(date(a.PublishedOn)||0);}).slice(0,4);
 var h='<div class="grid g3 rise">'+(pl.map(function(p,i){return '<a class="card play" target="_top" href="'+SITE+'/SitePages/Plays.html#play='+txt(p.ID)+'"><div class="row sp"><span class="numeral">0'+(i+1)+'</span><span class="kind">'+esc(txt(p.Solution))+'</span></div><h3 style="font-size:20px;margin-top:20px">'+esc(title(p))+'</h3><p class="clamp3">'+esc(txt(p.Pitch))+'</p><div class="cardfoot">'+list(p.Industry).slice(0,1).map(function(i){return '<span class="tag"><i></i>'+esc(i)+'</span>';}).join('')+'<span class="go">Open play '+svg('arrow',16)+'</span></div></a>';}).join('')||empty('No plays yet.'))+'</div>';
 h+='<h2>Featured <span class="n">'+feat.length+'</span><a class="link more" target="_top" href="'+SITE+'/SitePages/Find.html">Browse all '+lib.length+svg('arrow',16)+'</a></h2><div class="grid g3 rise">'+(feat.map(assetCard).join('')||empty('Nothing featured yet.'))+'</div>';
 h+='<h2>New this month</h2><div class="panel rise">'+(recent.map(function(r){return '<a class="listrow" target="_blank" href="'+fileUrl('Content Library',r)+'">'+icon(txt(r.AssetType))+'<div class="t"><b>'+esc(title(r))+'</b><span class="sub">'+esc(txt(r.AssetType))+' \u00B7 published '+fmt(date(r.PublishedOn))+'</span></div>'+shareChip(r.Shareability)+'<span class="go" style="margin-left:16px">'+svg('arrow',16)+'</span></a>';}).join('')||'<div class="empty">Nothing new yet.</div>')+'</div>';
 document.getElementById('main').innerHTML=h;});""", HOME_CSS)

# ================= FIND =================
P["Find.html"] = page3("Find", ["Content Library"],
 stage("Find content", "Every approved asset, in one place.", "Filter by solution, product, industry and stage. Only approved, current content lives here.")
 + '<main class="wrap"><div class="toolbar" role="search"><label class="field">' + svg("search", 18) + '<span class="vh">Search</span><input id="qq" placeholder="Search titles and summaries" autocomplete="off"></label><span id="sels"></span><div class="seg full" id="types" role="group" aria-label="Asset type"></div></div><div id="main" class="mt4"><div class="grid g3"><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></div></main>',
 r"""
var F={q:'',sol:'',prod:'',ind:'',type:'',share:'',stage:''};
(function(){var h=decodeURIComponent(HASH().replace(/^#/,''));h.split('&').forEach(function(p){var kv=p.split('=');if(kv[0]&&kv[0] in F)F[kv[0]]=kv.slice(1).join('=');});})();
var LIB=[];
function uniq(f){var s={};LIB.forEach(function(r){list(r[f]).forEach(function(x){s[x]=1;});});return Object.keys(s).sort();}
function sel(id,label,vals){return '<span class="select"><select aria-label="'+label+'" data-f="'+id+'"><option value="">'+label+'</option>'+vals.map(function(x){return '<option'+(F[id]===x?' selected':'')+'>'+esc(x)+'</option>';}).join('')+'</select></span>';}
function setF(k,x){F[k]=x;try{location.hash=Object.keys(F).filter(function(k){return F[k];}).map(function(k){return k+'='+encodeURIComponent(F[k]);}).join('&');}catch(e){}types();draw();}
function types(){var t=uniq('AssetType');document.getElementById('types').innerHTML=['All'].concat(t).map(function(x){var v=x==='All'?'':x;var n=LIB.filter(function(r){return !v||txt(r.AssetType)===v;}).length;return '<button type="button" data-type="'+esc(v)+'" aria-pressed="'+(F.type===v)+'">'+esc(x)+'<span class="c">'+n+'</span></button>';}).join('');}
function draw(){var q=F.q.toLowerCase();
 var res=LIB.filter(function(r){var hay=(title(r)+' '+txt(r.AISummary)+' '+txt(r.Products)+' '+txt(r.Industry)+' '+txt(r.AssetType)+' '+fname(r)).toLowerCase();
  return (!q||q.split(/\s+/).every(function(w){return hay.indexOf(w)>=0;}))&&(!F.sol||txt(r.Solution)===F.sol)&&(!F.prod||list(r.Products).indexOf(F.prod)>=0)&&(!F.ind||list(r.Industry).indexOf(F.ind)>=0)&&(!F.type||txt(r.AssetType)===F.type)&&(!F.share||txt(r.Shareability)===F.share)&&(!F.stage||txt(r.SalesStage)===F.stage);})
  .sort(function(a,b){return (yes(b.Featured)-yes(a.Featured))||(num(b.Views)-num(a.Views));});
 document.getElementById('main').innerHTML='<div class="row sp" style="margin-bottom:20px"><span class="sub" role="status"><b style="color:var(--ink)">'+res.length+'</b> of '+LIB.length+' assets</span><a class="link" target="_blank" href="'+FORMS.request+'">Can\u2019t find it? Ask the content team'+svg('arrow',16)+'</a></div>'
 +(res.length?'<div class="grid g3 rise">'+res.map(function(r){var t=txt(r.AssetType),internal=txt(r.Shareability).indexOf('Internal')===0;
  return '<article class="card hov"><div class="row">'+icon(t)+'<span class="kind">'+esc(t)+' \u00B7 '+esc(txt(r.SalesStage))+'</span>'+(yes(r.Featured)?'<span class="pill info" style="margin-left:auto">Featured</span>':'')+'</div><h3>'+esc(title(r))+'</h3><p class="clamp3">'+esc(txt(r.AISummary))+'</p><div class="row" style="gap:16px;margin:16px 0 20px">'+shareChip(r.Shareability)+expiryChip(date(r.ExpiresOn))+'<span class="tag" style="margin-left:auto;color:var(--ink3)">'+svg('eye',14)+num(r.Views)+'</span></div><div class="cardfoot"><a class="btn sm" target="_blank" href="'+fileUrl('Content Library',r)+'">Open</a>'+(internal?'<span class="sub">Keep internal</span>':'<a class="btn sm sec" target="_blank" title="Use Share with a customer in the Actions column" href="'+listUrl('Content Library')+'">Share\u2026</a>')+'</div></article>';}).join('')+'</div>':empty('Nothing matches those filters. Try removing one, or ask the content team for what you need.'));}
document.addEventListener('change',function(e){var f=e.target.getAttribute&&e.target.getAttribute('data-f');if(f)setF(f,e.target.value);});
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-type]');if(b)setF('type',b.getAttribute('data-type'));});
boot(function(){LIB=rows('Content Library');var q=document.getElementById('qq');q.value=F.q;q.oninput=function(){setF('q',q.value);};
 document.getElementById('sels').outerHTML='<span id="sels" style="display:contents">'+sel('sol','Solution',uniq('Solution'))+sel('prod','Product',uniq('Products'))+sel('ind','Industry',uniq('Industry'))+sel('stage','Stage',['Prospect','Discover','Qualify','Propose','Negotiate','Expand'])+sel('share','Shareability',['Public','Customer-shareable (NDA)','Internal only'])+'</span>';
 types();draw();});""")

# ================= PLAYS =================
PLAYS_CSS = r"""
.plays{display:grid;grid-template-columns:300px 1fr;gap:32px;align-items:start}
.rail{position:sticky;top:16px;display:flex;flex-direction:column;gap:4px}
.rail button{display:flex;gap:14px;align-items:flex-start;text-align:left;padding:14px 16px;border-radius:16px;border:0;background:transparent;font:inherit;color:var(--ink2);cursor:pointer;transition:background .3s var(--spring),box-shadow .3s var(--spring)}
.rail button:hover{background:rgba(255,255,255,.6)}.rail button[aria-current=true]{background:#fff;box-shadow:var(--sh2)}
.rail .num{font-size:22px;font-weight:600;font-variant-numeric:tabular-nums;color:var(--ice);line-height:1.15;min-width:30px}.rail button[aria-current=true] .num{color:var(--iceD)}
.rail b{display:block;font-weight:600;font-size:15px;color:var(--ink);line-height:1.3}.rail .s{font-size:13px;color:var(--ink3)}
.detail{background:#fff;border-radius:28px;border:1px solid var(--hair);box-shadow:var(--sh2);overflow:hidden}
.dhead{padding:40px 40px 32px;background:radial-gradient(520px 240px at 92% 0%,rgba(154,199,245,.38),transparent 70%),radial-gradient(420px 220px at 0% 110%,rgba(139,131,219,.18),transparent 70%),linear-gradient(180deg,#F6FAFE,#fff)}
.dhead h3{font-size:clamp(26px,3vw,34px);letter-spacing:-.025em;margin:10px 0 12px;font-weight:600;line-height:1.1}.dhead p{font-size:18px;color:var(--ink2);margin:0;max-width:640px}
.dbody{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:32px 40px 40px;border-top:1px solid var(--hair)}
.label{font-size:13px;font-weight:600;color:var(--ink3);margin:0 0 12px}.blk+.blk{margin-top:32px}
ol.q{list-style:none;margin:0;padding:0;counter-reset:q}ol.q li{counter-increment:q;position:relative;padding:2px 0 16px 42px}
ol.q li::before{content:counter(q);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;border:1px solid var(--hair2);display:grid;place-items:center;font-size:12px;font-weight:600;color:var(--iceD)}
.obj{padding:14px 0;border-top:1px solid var(--hair)}.obj:first-child{border-top:0;padding-top:0}.obj b{display:block;font-weight:600}.obj span{color:var(--ink2);font-size:14px}
.alist a{display:flex;gap:12px;align-items:center;padding:10px;margin:0 -10px;border-radius:14px;text-decoration:none;color:inherit;transition:background .2s}.alist a:hover{background:#F4F8FD}.alist b{display:block;font-size:14px;font-weight:600}
@media (max-width:900px){.plays{grid-template-columns:1fr}.rail{position:static;flex-direction:row;overflow-x:auto;padding-bottom:4px}.rail button{min-width:230px}.dbody{grid-template-columns:1fr;padding:24px}.dhead{padding:28px 24px}}
"""
P["Plays.html"] = page3("Plays", ["Solution Plays", "Content Library"],
 stage("Plays", "Know who to call, what to say, what to send.", "Each play brings the pitch, the questions to ask, answers to objections and the approved assets to use.")
 + '<main class="wrap"><div id="main"><div class="grid g3"><div class="skel"></div><div class="skel"></div></div></div></main>',
 r"""
var PL=[],BY={},CUR='';
function lines(x){return String(txt(x)).split(/\n|\r/).filter(Boolean);}
function draw(){var p=PL.filter(function(x){return txt(x.ID)===CUR;})[0]||PL[0];if(!p){document.getElementById('main').innerHTML=empty('No plays yet.');return;}CUR=txt(p.ID);
 var ids=String(txt(p.KeyAssets)).split(/[,; ]+/).filter(Boolean),assets=ids.map(function(i){return BY[i];}).filter(Boolean);
 var rail='<nav class="rail" aria-label="Plays">'+PL.map(function(x){return '<button type="button" data-play="'+txt(x.ID)+'" aria-current="'+(txt(x.ID)===CUR)+'"><span class="num">'+('0'+num(x.PlayOrder)).slice(-2)+'</span><span><b>'+esc(title(x))+'</b><span class="s">'+esc(txt(x.Solution))+'</span></span></button>';}).join('')+'</nav>';
 var d='<article class="detail rise"><div class="dhead"><div class="eyebrow">'+esc(txt(p.Solution))+(yes(p.Featured)?' \u00B7 Featured':'')+'</div><h3>'+esc(title(p))+'</h3><p>'+esc(txt(p.Pitch))+'</p><div class="row mt3"><a class="btn" target="_top" href="'+SITE+'/Deck%20Templates/Forms/Pick%20a%20template.aspx">'+svg('spark',18)+'Build a deck for this play</a>'+list(p.Industry).concat(list(p.Audience)).map(function(i){return '<span class="pill">'+esc(i)+'</span>';}).join('')+'</div></div>'
  +'<div class="dbody"><div><div class="blk"><p class="label">Why now</p><p style="margin:0;font-size:15px">'+esc(txt(p.WhyNow))+'</p></div><div class="blk"><p class="label">Products</p><div class="row" style="gap:8px">'+list(p.Products).map(function(x){return '<span class="pill info">'+esc(x)+'</span>';}).join('')+'</div></div><div class="blk"><p class="label">Use these assets</p><div class="alist">'+(assets.map(function(r){return '<a target="_blank" href="'+fileUrl('Content Library',r)+'">'+icon(txt(r.AssetType))+'<span style="flex:1"><b>'+esc(title(r))+'</b><span class="sub">'+esc(txt(r.AssetType))+'</span></span>'+shareChip(r.Shareability)+'</a>';}).join('')||'<p class="sub">No linked assets.</p>')+'</div></div></div>'
  +'<div><div class="blk"><p class="label">Discovery questions</p><ol class="q">'+lines(p.DiscoveryQuestions).map(function(l){l=l.trim();if(!/[?.!]$/.test(l))l+='?';return '<li>'+esc(l)+'</li>';}).join('')+'</ol></div><div class="blk"><p class="label">Objections</p>'+lines(p.Objections).map(function(l){var a=l.split('->');return '<div class="obj"><b>\u201C'+esc(a[0].trim())+'\u201D</b>'+(a[1]?'<span>'+esc(a[1].trim())+'</span>':'')+'</div>';}).join('')+'</div></div></div></article>';
 document.getElementById('main').innerHTML='<div class="plays">'+rail+d+'</div>';}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-play]');if(b){CUR=b.getAttribute('data-play');try{location.hash='play='+CUR;}catch(x){}draw();}});
boot(function(){PL=rows('Solution Plays').sort(function(a,b){return num(a.PlayOrder)-num(b.PlayOrder);});BY={};rows('Content Library').forEach(function(r){BY[txt(r.ID)]=r;});
 CUR=(HASH().match(/play=(\d+)/)||[])[1]||CUR;draw();});""", PLAYS_CSS)

# ================= BUILD A DECK =================
DECK_CSS = r"""
.process{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-top:56px}
.process::before{content:"";position:absolute;top:22px;left:22px;right:calc(33.333% - 10px);height:1px;background:linear-gradient(90deg,var(--ice),var(--violet))}
.ring{position:relative;z-index:1;width:44px;height:44px;border-radius:50%;background:#fff;border:1px solid var(--hair2);box-shadow:var(--sh1);display:grid;place-items:center;font-weight:600;color:var(--iceD)}
.ring.ai{border:1.5px solid transparent;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(135deg,var(--ice),var(--violet)) border-box;color:var(--violetD)}
.pstep b{display:block;font-size:17px;font-weight:600;margin:16px 0 6px;letter-spacing:-.01em}.pstep span{color:var(--ink2);font-size:14px}
.recipe{font-size:13px;color:var(--ink3)}
.who{display:grid;grid-template-columns:1fr 1fr;gap:24px}.who h3{margin:0 0 12px;font-size:15px;font-weight:600;display:flex;gap:8px;align-items:center}
.who ul{margin:0;padding-left:18px;color:var(--ink2);font-size:14px;line-height:1.7}
.notes{margin-top:12px;font-size:13px;color:var(--ink2);white-space:pre-line;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
@media (max-width:768px){.process{grid-template-columns:1fr;gap:24px}.process::before{display:none}.who{grid-template-columns:1fr}}
"""
P["DeckStudio.html"] = page3("Build a deck", ["Deck Requests", "Deck Templates"],
 stage("Build a deck", "Four questions. Copilot drafts the deck.", "Copilot picks the best approved slides for your meeting type and industry, puts them in order and writes your talking points. You finish it in PowerPoint.",
  '<div class="row mt4"><a class="btn" target="_blank" href="' + FORMS["deck"] + '">' + svg("spark", 18) + 'Start a deck request</a><a class="link" target="_top" href="' + SP + 'SlideBuilder.html">Browse the slide gallery' + svg("arrow", 16) + '</a></div>'
  '<div class="process" role="list"><div class="pstep" role="listitem"><div class="ring">1</div><b>Answer four questions</b><span>Customer, meeting type, industry and what the meeting should achieve.</span></div>'
  '<div class="pstep" role="listitem"><div class="ring ai">' + svg("spark", 18) + '</div><b>Press \u201cBuild my deck\u201d</b><span>Next to your request below. Copilot takes a few minutes.</span></div>'
  '<div class="pstep" role="listitem"><div class="ring">3</div><b>Finish in PowerPoint</b><span>Open the deck, retitle the first slide for the customer and use the talking points on your request.</span></div></div>')
 + '<main class="wrap"><div id="main"><div class="grid g3"><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></div></main>',
 r"""
var SC={'New':'','Building':'info','Ready':'ok','Needs input':'warn','Failed':'bad'};
boot(function(){var R=rows('Deck Requests').sort(function(a,b){return num(b.ID)-num(a.ID);}),T=rows('Deck Templates').filter(function(t){return txt(t.OutputFormat)!=='Word';});
 var h='<h2>Your requests <span class="n">'+R.length+'</span></h2>'+(R.length?'<div class="grid g3 rise">'+R.map(function(r){var u=urlOf(r.OutputDeck),st=txt(r.RequestStatus)||'New',n=txt(r.BuildNotes);
  var act=u?'<a class="btn sm" target="_blank" href="'+esc(u)+'">Open deck</a>':(st==='New'?'<a class="btn sm" target="_blank" href="'+listUrl('Deck Requests')+'">'+svg('spark',16)+'Build my deck</a><span class="sub" style="font-size:12px">Opens your requests; the button is in the Actions column.</span>':'<a class="btn sm sec" target="_blank" href="'+itemUrl('Deck Requests',r)+'">Open request</a>');
  return '<article class="card"><div class="row sp"><span class="pill '+(SC[st]||'')+'">'+esc(st)+'</span><span class="sub">'+esc(txt(r.Industry))+'</span></div><h3>'+esc(txt(r.Customer))+'</h3><p>'+esc(txt(r.Template))+'</p>'+(n?'<div class="notes">'+esc(n)+'</div>':'')+'<div class="cardfoot" style="margin-top:20px;gap:12px;flex-wrap:wrap">'+act+'</div></article>';}).join('')+'</div>':empty('No requests yet. Start one and it will appear here.'));
 h+='<h2>Who does what</h2><div class="panel pad rise who"><div><h3>'+svg('spark',16)+'Copilot</h3><ul><li>Picks approved slides that fit your meeting type and industry</li><li>Never uses internal-only or expired content</li><li>Saves the deck and links it to your request</li><li>Writes your opening line and talking points on the request</li></ul></div><div><h3>'+svg('deck',16)+'You</h3><ul><li>Retitle the first slide for the customer</li><li>Swap a slide if you know a better one</li><li>Rehearse with the talking points</li><li>Share it from the Content Library rules</li></ul></div></div>';
 h+='<h2>Meeting types</h2><div class="panel rise">'+T.map(function(t){var roles=String(txt(t.Recipe)).split(',').map(function(s){return s.trim();}).filter(Boolean);
  return '<div class="listrow"><span class="tile">'+svg('deck')+'</span><div class="t"><b>'+esc(txt(t.TemplateKind)||title(t))+'</b><span class="sub">'+esc(txt(t.BestFor))+'</span><div class="recipe" style="margin-top:6px">'+roles.map(esc).join('  \u00B7  ')+'</div></div><span class="pill">'+num(t.SlideCount)+' slides</span></div>';}).join('')+'</div>';
 document.getElementById('main').innerHTML=h;});""", DECK_CSS)

# ================= SLIDE GALLERY (file name kept: SlideBuilder.html) =================
SB_CSS = r"""
.slide{display:block;width:100%;text-decoration:none;color:inherit;background:#fff;border-radius:20px;border:1px solid var(--hair);box-shadow:var(--sh2);padding:10px;position:relative;transition:transform .4s var(--spring),box-shadow .4s var(--spring)}
.slide:hover{transform:translateY(-3px);box-shadow:0 0 0 1px var(--iceD),var(--sh2)}.slide:focus-visible{outline:2px solid var(--iceD);outline-offset:3px}
.slide img,.slide .ph{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;box-shadow:0 0 0 1px var(--hair)}
.slide .ph{background:linear-gradient(135deg,#1B2A44,#2F3F66);color:#fff;display:grid;place-items:center;padding:12px;text-align:center;font-weight:600;font-size:13px}
.sb{display:block;padding:12px 6px 4px}.sb b{display:block;font-size:14px;font-weight:600;line-height:1.3}
.sum{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:13px;color:var(--ink3);margin:4px 0 10px}
"""
P["SlideBuilder.html"] = page3("Slide gallery", ["Slide Library"],
 stage('<a class="link" target="_top" href="' + DECKS + '" style="font-size:13px">' + svg("back", 16) + 'Build a deck</a>', "Slide gallery.", "Every approved slide, by role. Open one to copy it into a deck in PowerPoint, or let Build a deck choose them for you.")
 + '<main class="wrap"><div class="toolbar" id="filters" style="position:relative;top:auto"></div><div id="main" class="mt4"><div class="grid g4"><div class="skel"></div><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></div></main>',
 r"""
var THUMBS=JSON.parse(document.getElementById('thumbs').textContent);
var ROLES=['Title','Agenda','Problem','Solution','Proof','Customer story','Pricing','Next steps','Close'];
var S=[],F={role:'',ind:'',prod:'',internal:false};
function byRole(a,b){return ROLES.indexOf(txt(a.SlideRole))-ROLES.indexOf(txt(b.SlideRole))||num(a.SlideOrder)-num(b.SlideOrder);}
function img(r){var t=THUMBS[fname(r)];return t?'<img src="'+t+'" alt="">':'<span class="ph">'+esc(title(r))+'</span>';}
function filters(){function u(f){var s={};S.forEach(function(r){list(r[f]).forEach(function(x){s[x]=1;});});return Object.keys(s).sort();}
 function sel(id,l,vals){return '<span class="select"><select aria-label="'+l+'" data-f="'+id+'"><option value="">'+l+'</option>'+vals.map(function(x){return '<option'+(F[id]===x?' selected':'')+'>'+esc(x)+'</option>';}).join('')+'</select></span>';}
 document.getElementById('filters').innerHTML='<div class="seg full" role="group" aria-label="Slide role">'+['All'].concat(ROLES).map(function(r){var v=r==='All'?'':r;return '<button type="button" data-role="'+v+'" aria-pressed="'+(F.role===v)+'">'+r+'</button>';}).join('')+'</div>'
 +sel('ind','Industry',u('Industry').filter(function(x){return x!=='Cross-industry';}))+sel('prod','Product',u('Products'))+'<label class="switch"><input type="checkbox" data-f="internal"'+(F.internal?' checked':'')+'>Show internal-only</label>';}
function draw(){
 var res=S.filter(function(s){return (!F.role||txt(s.SlideRole)===F.role)&&(!F.ind||list(s.Industry).indexOf(F.ind)>=0||list(s.Industry).indexOf('Cross-industry')>=0)&&(!F.prod||list(s.Products).indexOf(F.prod)>=0)&&(F.internal||txt(s.Shareability).indexOf('Internal')<0);}).sort(byRole);
 var h='<p class="sub" role="status" style="margin:0 0 8px"><b style="color:var(--ink)">'+res.length+'</b> of '+S.length+' slides</p>';ROLES.forEach(function(role){var g=res.filter(function(s){return txt(s.SlideRole)===role;});if(!g.length)return;
  h+='<h2>'+role+' <span class="n">'+g.length+'</span></h2><div class="grid g4">'+g.map(function(s){
  return '<a class="slide" target="_blank" href="'+fileUrl('Slide Library',s)+'" aria-label="Open '+esc(title(s))+'">'+img(s)+'<span class="sb"><b>'+esc(title(s))+'</b><span class="sum">'+esc(txt(s.SlideSummary))+'</span><span class="row" style="gap:12px">'+shareChip(s.Shareability)+(yes(s.UseVerbatim)?'<span class="tag"><i style="background:var(--ink)"></i>Use as is</span>':'')+'</span></span></a>';}).join('')+'</div>';});
 document.getElementById('main').innerHTML=res.length?h:empty('No slides match those filters.');}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-role]');if(b){F.role=b.getAttribute('data-role');filters();draw();}});
document.addEventListener('change',function(e){var f=e.target.getAttribute&&e.target.getAttribute('data-f');if(!f)return;F[f]=f==='internal'?e.target.checked:e.target.value;draw();});
boot(function(){S=rows('Slide Library');filters();draw();});""",
 SB_CSS, '<script type="application/json" id="thumbs">' + json.dumps(THUMBS) + '</script>')

# ================= PUBLISHING DESK =================
PD_CSS = r"""
.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:8px 0 32px}
.strip div{padding:16px;border-radius:16px;background:rgba(255,255,255,.7);border:1px solid var(--hair)}
.strip .ai{background:linear-gradient(150deg,rgba(154,199,245,.28),rgba(139,131,219,.16));border-color:rgba(139,131,219,.25)}.strip .hu{border-color:var(--ink)}
.strip small{font-size:12px;font-weight:600;color:var(--ink3)}.strip b{display:block;font-size:14px;margin:2px 0}.strip span{font-size:12.5px;color:var(--ink2)}
.board{display:grid;grid-template-columns:repeat(6,minmax(168px,1fr));gap:16px;overflow-x:auto;padding-bottom:8px}
.col{background:rgba(234,243,252,.65);border:1px solid rgba(47,109,181,.08);border-radius:20px;padding:12px;min-height:260px}
.colh{display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:600;padding:4px 6px 12px}.colh span{font-weight:500;color:var(--ink3);font-variant-numeric:tabular-nums}
.kc{display:block;background:#fff;border-radius:14px;padding:14px;margin-bottom:10px;box-shadow:var(--sh1);border:1px solid var(--hair);text-decoration:none;color:inherit;transition:transform .35s var(--spring),box-shadow .35s var(--spring)}
.kc:hover{transform:translateY(-2px);box-shadow:var(--sh2)}.kc b{display:block;font-size:14px;line-height:1.35;font-weight:600}
.kc .f{font-size:12.5px;color:var(--ink2);margin-top:10px;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.kc .fx{font-size:12px;color:var(--violetD);margin-top:8px;display:flex;gap:6px}.colempty{font-size:12.5px;color:var(--ink3);text-align:center;padding:24px 8px}
@media (max-width:900px){.strip{grid-template-columns:1fr 1fr}}
"""
P["PublishingDesk.html"] = page3("Publishing Desk", ["Content Intake", "Content Requests", "Content Library", "Customer Shares", "Archive"],
 stage("Content team", "Publishing Desk", "Review submissions, answer seller requests, keep content fresh and see what\u2019s used. An agent reviews every submission first; one person approves.",
  '<div class="row mt4"><a class="btn" target="_blank" href="' + SITE + '/Content%20Intake/Forms/AllItems.aspx">Open Content Intake</a><a class="btn sec" target="_blank" href="' + SITE + '/AgentAssets/Standards/publishing-standards.md">Publishing standards</a></div>')
 + '<main class="wrap"><div class="seg" id="tabs" role="tablist" aria-label="Publishing Desk sections"></div><div id="main" class="mt4"><div class="grid g3"><div class="skel"></div><div class="skel"></div><div class="skel"></div></div></div></main>',
 r"""
var TAB=(HASH().match(/tab=(\w+)/)||[])[1]||'review',D={};
var COLS=[['Submitted','New'],['Agent review','Agent review'],['Needs fixes','Needs fixes'],['Awaiting approval','Awaiting approval'],['Approved','Approved'],['Published','Published']];
function appr(r){var a=String(txt(r._ApprovalStatus)).toLowerCase();if(a==='3'||a.indexOf('approv')===0)return 'Approved';if(a==='2'||a.indexOf('reject')===0)return 'Rejected';if(a==='1'||a.indexOf('request')===0||a.indexOf('pend')===0)return 'Requested';return '';}
function stage(r){var a=appr(r),s=txt(r.ReviewStatus)||'Submitted';if(a==='Approved'&&s!=='Published')return 'Approved';if(a==='Requested')return 'Awaiting approval';return s;}
function vchip(x){x=txt(x);if(!x)return '<span class="pill">Not reviewed</span>';return '<span class="pill '+(x==='Pass'?'ok':(x==='Blocked'?'bad':'warn'))+'">'+(x==='Pass'?'Pass':(x==='Blocked'?'Blocked':'Fixable'))+'</span>';}
function review(){var I=D.I;var h='<div class="strip" role="list"><div role="listitem"><small>1</small><b>Submit</b><span>Upload to Content Intake.</span></div><div class="ai" role="listitem"><small>2 \u00B7 Agent</small><b>Review</b><span>Checks 10 publishing rules.</span></div><div class="ai" role="listitem"><small>3 \u00B7 Agent</small><b>Fix</b><span>Safe fixes as a new version.</span></div><div class="hu" role="listitem"><small>4 \u00B7 Person</small><b>Approve</b><span>One approver, findings attached.</span></div><div role="listitem"><small>5</small><b>Publish</b><span>One click into the library.</span></div></div><div class="board">';
 COLS.forEach(function(c){var g=I.filter(function(r){return stage(r)===c[0];});
  h+='<section class="col" aria-label="'+c[1]+'"><div class="colh">'+c[1]+'<span>'+g.length+'</span></div>'+(g.map(function(r){var f=String(txt(r.ValidationFindings)),fx=String(txt(r.AgentFixes));
   return '<a class="kc" target="_blank" href="'+fileUrl('Content Intake',r)+'"><b>'+esc(title(r))+'</b><div class="row" style="gap:10px;margin-top:10px">'+vchip(r.ValidationResult)+shareChip(r.Shareability)+'</div>'+(f?'<div class="f">'+esc(f).replace(/\n/g,'<br>')+'</div>':'')+(fx?'<div class="fx">'+svg('spark',14)+esc(fx.split('\n')[0])+'</div>':'')+'<div class="sub" style="font-size:12px;margin-top:10px">'+esc(txt(r.ContentOwner))+'</div></a>';}).join('')||'<div class="colempty">Nothing here</div>')+'</section>';});
 return h+'</div>';}
function requests(){var C=D.C;if(!C.length)return empty('No requests from sellers.');return '<div class="panel scroll"><table><thead><tr><th>Request</th><th>Need</th><th>Priority</th><th>Status</th><th>Needed by</th></tr></thead><tbody>'+C.map(function(r){var p=txt(r.Priority);return '<tr><td><b>'+esc(title(r))+'</b><div class="sub">'+esc(txt(r.Solution))+' \u00B7 '+esc(txt(r.Industry))+'</div></td><td style="max-width:420px;color:var(--ink2)">'+esc(txt(r.Need))+'</td><td><span class="pill '+(p==='High'?'bad':(p==='Medium'?'warn':''))+'">'+esc(p)+'</span></td><td>'+esc(txt(r.RequestStatus))+'</td><td class="sub">'+fmt(date(r.NeededBy))+'</td></tr>';}).join('')+'</tbody></table></div>';}
function stale(){return D.L.filter(function(r){var n=days(date(r.ExpiresOn));return n!==null&&n<=30;});}
function fresh(){var S=D.S,L=stale();var h=L.length?'<div class="panel scroll"><table><thead><tr><th>Asset</th><th>Expiry</th><th>Owner</th><th>Customer shares</th></tr></thead><tbody>'+L.map(function(r){var f=fname(r).toLowerCase(),fe=encodeURIComponent(fname(r)).toLowerCase();var sh=S.filter(function(s){var u=String(urlOf(s.SourceAsset)).toLowerCase();return u.indexOf(fe)>=0||u.indexOf(f)>=0;}).length;return '<tr><td><a target="_blank" href="'+fileUrl('Content Library',r)+'">'+esc(title(r))+'</a></td><td>'+expiryChip(date(r.ExpiresOn))+'</td><td>'+esc(txt(r.ContentOwner))+'</td><td>'+sh+'</td></tr>';}).join('')+'</tbody></table></div><p class="sub mt3">Run <b>Check freshness</b> in the Content Library to archive expired items and tell their owners.</p>':empty('Nothing expires in the next 30 days.');
 return h+'<h2>Archive <span class="n">'+D.A.length+'</span></h2><div class="panel scroll"><table><thead><tr><th>Asset</th><th>Reason</th><th>Archived</th></tr></thead><tbody>'+D.A.map(function(r){return '<tr><td>'+esc(title(r))+'</td><td>'+esc(txt(r.ArchiveReason))+'</td><td class="sub">'+fmt(date(r.ArchivedOn))+'</td></tr>';}).join('')+'</tbody></table></div>';}
var ST={'Active':'ok','Source updated':'warn','Source expired':'bad','Revoked':''};
function shares(){var S=D.S.slice().sort(function(a,b){return (date(b.SharedOn)||0)-(date(a.SharedOn)||0);});if(!S.length)return empty('Nothing has been shared with customers yet.');return '<div class="panel scroll"><table><thead><tr><th>What</th><th>Customer</th><th>Recipient</th><th>Shareability</th><th>Shared</th><th>Status</th></tr></thead><tbody>'+S.map(function(s){var st=txt(s.ShareStatus),u=urlOf(s.SharedAsset);return '<tr><td>'+(u?'<a target="_blank" href="'+esc(u)+'">'+esc(title(s))+'</a>':'<b>'+esc(title(s))+'</b>')+'<div class="sub">'+esc(txt(s.Author))+'</div></td><td>'+esc(txt(s.Customer))+'</td><td class="sub">'+esc(txt(s.Recipient))+'</td><td>'+shareChip(s.Shareability)+'</td><td class="sub">'+fmt(date(s.SharedOn))+'</td><td><span class="pill '+(ST[st]||'')+'">'+esc(st)+'</span></td></tr>';}).join('')+'</tbody></table></div>';}
function usageNote(L){var d=L.map(function(r){return date(r.ViewsAsOf);}).filter(Boolean).sort(function(a,b){return b-a;})[0];return d?'Views and viewers come from SharePoint file analytics, refreshed '+fmt(d)+'.':'No view data yet.';}
function usage(){var L=D.L,byType={},bySol={};L.forEach(function(r){var t=txt(r.AssetType)||'Other';byType[t]=(byType[t]||0)+num(r.Views);var s=txt(r.Solution)||'Other';bySol[s]=(bySol[s]||0)+1;});
 var top=L.slice().sort(function(a,b){return num(b.Views)-num(a.Views);}).slice(0,6);
 return '<div class="grid g2 rise"><div class="panel">'+top.map(function(r,i){return '<a class="listrow" target="_blank" href="'+fileUrl('Content Library',r)+'"><span class="numeral" style="font-size:22px;font-weight:600;color:var(--iceD);width:24px;font-variant-numeric:tabular-nums">'+(i+1)+'</span>'+icon(txt(r.AssetType))+'<div class="t"><b>'+esc(title(r))+'</b><span class="sub">'+esc(txt(r.AssetType))+'</span></div><span style="text-align:right"><b>'+num(r.Views)+'</b><span class="sub" style="display:block;font-size:12px">'+num(r.Viewers)+' '+(num(r.Viewers)===1?'person':'people')+'</span></span></a>';}).join('')+'</div><div class="panel pad"><p class="label" style="font-size:13px;font-weight:600;color:var(--ink3);margin:0">Views by asset type</p>'+bars(byType)+'<p class="label" style="font-size:13px;font-weight:600;color:var(--ink3);margin:24px 0 0">Library by solution area</p>'+bars(bySol)+'</div></div><p class="sub mt3">'+usageNote(L)+'</p>';}
function draw(){var openR=D.I.filter(function(r){return ['Published','Rejected'].indexOf(stage(r))<0;}).length,openC=D.C.filter(function(r){return ['Delivered','Declined'].indexOf(txt(r.RequestStatus))<0;}).length,st=stale().length,sf=D.S.filter(function(s){return ['Source updated','Source expired'].indexOf(txt(s.ShareStatus))>=0;}).length;
 var T=[['review','Review',openR,0],['requests','Seller requests',openC,0],['fresh','Freshness',st,1],['shares','Customer shares',sf,1],['usage','Usage',null,0]];
 document.getElementById('tabs').innerHTML=T.map(function(t){return '<button type="button" role="tab" data-tab="'+t[0]+'" aria-selected="'+(TAB===t[0])+'">'+t[1]+(t[2]!==null?'<span class="c'+(t[3]&&t[2]?' hot':'')+'">'+t[2]+'</span>':'')+'</button>';}).join('');
 document.getElementById('main').innerHTML={review:review,requests:requests,fresh:fresh,shares:shares,usage:usage}[TAB]();}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-tab]');if(b){TAB=b.getAttribute('data-tab');try{location.hash='tab='+TAB;}catch(x){}draw();}});
boot(function(){D={I:rows('Content Intake'),C:rows('Content Requests'),L:rows('Content Library'),S:rows('Customer Shares'),A:rows('Archive')};draw();});""", PD_CSS)

os.makedirs(OUT, exist_ok=True)
for f, h in P.items():
    if f in KEEP: open(os.path.join(OUT, f), "w", encoding="utf-8").write(h); print(f, len(h.encode()) // 1024, "KB")
