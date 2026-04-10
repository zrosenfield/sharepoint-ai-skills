/**
 * SharePoint AI Skills Demo Runner
 *
 * Connects to an existing Edge instance via CDP and runs demo scenarios
 * with step-by-step pacing, slow typing, and live navigation controls.
 *
 * Prerequisites:
 *   Launch Edge with remote debugging enabled:
 *     msedge.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\edge-debug"
 *   Or from PowerShell:
 *     Start-Process "msedge" "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\edge-debug"
 *
 * Usage:
 *   node tools/run-demo.mjs [scenario] [--setup | --reset] [--widget]
 *   node tools/run-demo.mjs tell-me-about-site
 *   node tools/run-demo.mjs tools/scripts/site-overview.demo --widget
 *
 * Flags:
 *   --widget  Inject a floating hover-control panel into the browser.
 *             Move the mouse to the bottom of the screen to reveal it.
 *             Useful when running full-screen — no need to alt-tab to the terminal.
 *
 * Step controls (press at any pause):
 *   Enter   run / continue
 *   s       skip this step
 *   b       go back and re-run the previous step
 *   ?       show help
 *   Ctrl+C  quit
 *
 * If Edge is not running on the CDP port, it is launched automatically.
 */

import { chromium } from 'playwright';
import { readFileSync, readdirSync, mkdirSync, existsSync, statSync, writeFileSync } from 'fs';
import { resolve, dirname, join, basename } from 'path';
import { spawn } from 'child_process';
import { get as httpGet, createServer } from 'http';
import { fileURLToPath } from 'url';

// ─── Local config files (gitignored — copy *.example.* to use) ───────────────

const _scriptDir = dirname(fileURLToPath(import.meta.url));
let _cfg = {};
try { _cfg = JSON.parse(readFileSync(join(_scriptDir, 'demo.config.json'), 'utf8')); } catch { /* defaults */ }

// Resolve scenario first so per-demo config overrides can be applied before
// any constants are derived from _cfg.
const args = process.argv.slice(2);
const SCENARIO = args.find(a => !a.startsWith('--')) ?? 'tell-me-about-site';
const _scenarioKey = SCENARIO.endsWith('.demo') ? basename(resolve(SCENARIO), '.demo') : SCENARIO;
if (_cfg.overrides?.[_scenarioKey]) Object.assign(_cfg, _cfg.overrides[_scenarioKey]);

const TYPE_CHUNK = _cfg.typeChunkSize ?? 5;   // characters per fill() call
const TYPE_DELAY = _cfg.typeDelayMs   ?? 10;  // ms between fills

// Variable overrides: demo.vars.json is seeded into every script's var map before
// [var:] declarations, so it wins over the script defaults.
let _demoVars = {};
try { _demoVars = JSON.parse(readFileSync(join(_scriptDir, 'demo.vars.json'), 'utf8')); } catch { /* none */ }

const CDP_URL = process.env.CDP_URL ?? 'http://localhost:9222';
const _sectionIdx = args.indexOf('--section');
const RUN_SECTION = args.includes('--setup') ? 'setup' : args.includes('--reset') ? 'reset' : args.includes('--all') ? 'all' : (_sectionIdx !== -1 && args[_sectionIdx + 1] ? args[_sectionIdx + 1] : 'demo');
const USE_WIDGET = args.includes('--widget');
const RECORD_MODE = args.includes('--record');

// ─── Scenarios ───────────────────────────────────────────────────────────────

const scenarios = {
  'tell-me-about-site': tellMeAboutSiteSteps,
};

// ─── Edge auto-launch ─────────────────────────────────────────────────────────

function checkCdpAvailable() {
  return new Promise(resolve => {
    const u = new URL(CDP_URL);
    const req = httpGet(
      { hostname: u.hostname, port: +u.port || 9222, path: '/json/version', timeout: 2000 },
      res => { resolve(res.statusCode < 400); res.resume(); }
    );
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

function findEdgePath() {
  const candidates = [
    process.env.LOCALAPPDATA && join(process.env.LOCALAPPDATA, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  ].filter(Boolean);
  return candidates.find(p => existsSync(p)) ?? null;
}

async function ensureEdgeRunning() {
  if (await checkCdpAvailable()) return;

  console.log('Edge not detected — launching Edge with remote debugging...');

  const edgePath = findEdgePath();
  if (!edgePath) {
    throw new Error(
      'msedge.exe not found. Start Edge manually:\n' +
      '  msedge.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\\edge-debug"'
    );
  }

  const port = new URL(CDP_URL).port || '9222';
  const userDataDir = _cfg.userDataDir ?? join(process.env.TEMP || process.env.TMPDIR || '/tmp', 'edge-debug');

  const launchArgs = [`--remote-debugging-port=${port}`, `--user-data-dir=${userDataDir}`];
  if (_cfg.profileDirectory) launchArgs.push(`--profile-directory=${_cfg.profileDirectory}`);
  if (_cfg.inPrivate) launchArgs.push('--inprivate');

  spawn(edgePath, launchArgs, {
    detached: true, stdio: 'ignore',
  }).unref();

  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, 600));
    if (await checkCdpAvailable()) { console.log('Edge is ready.\n'); return; }
  }
  throw new Error('Edge launched but did not become available within 15 seconds.');
}

// ─── Widget: local HTTP server + separate Edge app window ─────────────────────
//
// No browser injection — the widget is a small standalone Edge window that polls
// a local HTTP server for state and posts actions back.

let _widgetState = {};
let _widgetPauseRequested = false;

// OBS recording state (populated by main() in --record mode)
let _obsConn = null;
let _obsRecordingStartMs = null;

function widgetUpdate(patch) {
  if (!USE_WIDGET) return;
  Object.assign(_widgetState, patch);
}

const WIDGET_HTML = `<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><title>Demo</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#1b1b2e;color:#e0e0e0;user-select:none;overflow:hidden}

/* top bar */
#top{display:flex;justify-content:flex-end;gap:3px;padding:6px 8px 0}
.mi{width:22px;height:22px;border:none;border-radius:4px;background:#252540;color:#888;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .12s,color .12s;padding:0;flex-shrink:0}
.mi:hover{background:#3a3a58;color:#bbb}
.mi.on{background:#0078d4;color:#fff}

/* main */
#main{padding:4px 12px 12px}
#si{font-size:13px;color:#0078d4;font-weight:600;margin-bottom:2px}
#sn{font-size:14px;color:#fff;margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#ctx{display:none;font-size:13px;color:#c8922a;border-left:2px solid #c8922a;padding:3px 7px;margin-bottom:8px;line-height:1.55;max-height:90px;overflow-y:auto;white-space:pre-wrap;word-break:break-word}
#ctx.has{display:block}
.btn{display:block;width:100%;padding:7px 12px;margin-bottom:5px;border:none;border-radius:6px;cursor:pointer;font-size:15px;font-family:inherit;text-align:left;transition:opacity .1s}
.btn:hover{opacity:.82}
.btn:active{opacity:.65}
#bn{background:#0078d4;color:#fff;font-weight:600}
#bb,#bs{background:#2d2d44;color:#ccc}
#bp{background:#2d2d44;color:#bbb}#bp.on{background:#c8922a;color:#fff}
#br{background:#2d2d44;color:#c8922a;display:none}#br.show{display:block}
.bl{margin-left:2px}
#foot{display:flex;justify-content:space-between;align-items:center;padding-top:6px;border-top:1px solid #252540;margin-top:2px}
#tmr{font-size:14px;color:#fff;font-variant-numeric:tabular-nums;letter-spacing:.02em}
#stat{font-size:12px;color:#aaa}
#stat.w{color:#0078d4}

/* slim vertical */
body.sv #top{justify-content:center;padding:5px 5px 0;gap:2px}
body.sv .mi{width:19px;height:19px}
body.sv #main{padding:3px 4px 8px}
body.sv #si,body.sv #sn,body.sv #ctx{display:none!important}
body.sv #btns{display:flex;flex-direction:column;align-items:stretch}
body.sv .btn{padding:9px 0;font-size:18px;text-align:center;margin-bottom:4px;width:100%}
body.sv .bl{display:none}
body.sv #foot{flex-direction:column;gap:1px;border:none;padding-top:3px;margin-top:0}
body.sv #stat{display:none}
body.sv #tmr{font-size:10px;text-align:center;width:100%}

/* slim horizontal */
body.sh{display:flex;flex-direction:row;align-items:center;padding:0 8px;gap:6px;height:100vh}
body.sh #top{order:99;padding:0;gap:3px}
body.sh .mi{width:19px;height:19px}
body.sh #main{display:contents}
body.sh #si,body.sh #ctx{display:none!important}
body.sh #sn{margin:0;flex:1;min-width:0;font-size:11px}
body.sh #btns{display:flex;gap:4px;align-items:center;flex-shrink:0}
body.sh .btn{width:auto;padding:5px 10px;font-size:12px;margin:0;display:inline-block}
body.sh #foot{border:none;padding:0;margin:0;flex-shrink:0;gap:0}
body.sh #stat{display:none}
body.sh #tmr{font-size:11px;min-width:36px;text-align:right}

/* step list */
#sl{margin-top:6px;padding-top:6px;border-top:1px solid #252540}
.st{font-size:12px;color:#aaa;padding:1px 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-radius:2px}
.st.cur{color:#fff;background:#0078d4;font-weight:600}
.st.pause{color:#c8922a}
.st.cur.pause{color:#fff;background:#c8922a}
body.sv #sl,body.sh #sl{display:none!important}

/* button inactive state (running — inputs won't have effect yet) */
.btn.inactive{opacity:.38}
</style>
</head><body class="full">

<div id="top">
  <button class="mi on" id="mf" onclick="setMode('full')" title="Full">
    <svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
      <rect x="1" y="1" width="10" height="10" rx="1.5"/>
      <line x1="3" y1="4.5" x2="9" y2="4.5"/>
      <line x1="3" y1="6.5" x2="9" y2="6.5"/>
      <line x1="3" y1="8.5" x2="7" y2="8.5"/>
    </svg>
  </button>
  <button class="mi" id="msv" onclick="setMode('sv')" title="Slim vertical">
    <svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
      <rect x="3.5" y="1" width="5" height="10" rx="1.5"/>
    </svg>
  </button>
  <button class="mi" id="msh" onclick="setMode('sh')" title="Slim horizontal">
    <svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
      <rect x="1" y="3.5" width="10" height="5" rx="1.5"/>
    </svg>
  </button>
</div>

<div id="main">
  <div id="si">\u2014</div>
  <div id="sn">Starting\u2026</div>
  <div id="ctx"></div>
  <div id="btns">
    <button class="btn" id="bn" onclick="act('enter')">\u25ba\ufe0e<span class="bl">Next</span></button>
    <button class="btn" id="bb" onclick="act('b')">\u25c4\ufe0e<span class="bl">Back</span></button>
    <button class="btn" id="bs" onclick="act('s')">\u21e5<span class="bl">Skip</span></button>
    <button class="btn" id="bp" onclick="togglePause()">\u23f8\ufe0e<span class="bl">Pause</span></button>
    <button class="btn" id="br" onclick="act('r')">\u21ba<span class="bl">Reset</span></button>
  </div>
  <div id="foot">
    <div id="tmr">00:00</div>
    <div id="stat">Ready</div>
  </div>
  <div id="sl"></div>
</div>

<script>
var st=null;
var WIDTHS={full:364,sv:80,sh:520};
var SH_H=58; // slim-h fixed content height
var mode=localStorage.getItem('dw-mode')||'full';

function setMode(m){
  mode=m;
  document.body.className=m==='full'?'full':m;
  ['mf','msv','msh'].forEach(function(id){document.getElementById(id).classList.remove('on')});
  document.getElementById(m==='full'?'mf':m==='sv'?'msv':'msh').classList.add('on');
  localStorage.setItem('dw-mode',m);
  // Resize after layout settles; use scrollHeight so timer is never clipped
  requestAnimationFrame(function(){
    var chrome=Math.max(28, window.outerHeight-window.innerHeight);
    var h=m==='sh' ? SH_H+chrome : document.documentElement.scrollHeight+chrome+4;
    window.resizeTo(WIDTHS[m], h);
  });
}
setMode(mode);

function act(a){
  fetch('/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:a})});
}

function togglePause(){
  fetch('/pause',{method:'POST'});
}

function fmt(ms){
  var s=Math.floor(ms/1000),m=Math.floor(s/60);
  return String(m).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
}

function poll(){
  fetch('/state').then(function(r){return r.json()}).then(function(s){
    if(s.startTime&&!st) st=s.startTime;
    document.getElementById('si').textContent=s.step!=null?'Step '+s.step+' / '+(s.total||'?'):'\u2014';
    document.getElementById('sn').textContent=s.name||'';
    var ctxEl=document.getElementById('ctx');
    ctxEl.textContent=s.context||'';
    ctxEl.className=s.context?'has':'';
    var el=document.getElementById('stat');
    el.textContent=s.waiting?'\u25b6 Waiting \u2014 Next or Enter':'Running\u2026';
    el.className=s.waiting?'w':'';
    var bp=document.getElementById('bp');if(bp)bp.className='btn'+(s.pauseRequested?' on':'');
    var br=document.getElementById('br');if(br)br.className='btn'+(s.resetAvailable?' show':'');
    // Dim Next/Back/Skip while a step is running (still clickable — queued for next pause)
    var w=!!s.waiting;
    ['bn','bb','bs'].forEach(function(id){var b=document.getElementById(id);if(b){b.classList.toggle('inactive',!w);}});
    // Render step list
    var sl=document.getElementById('sl');
    if(sl&&s.steps&&s.steps.length){
      var html='';
      for(var j=0;j<s.steps.length;j++){
        var step=s.steps[j];var cur=s.step&&(j+1===s.step);
        var cls='st'+(cur?' cur':'')+(step.pause?' pause':'');
        var label=typeof step==='string'?step:step.name;
        html+='<div class="'+cls+'">'+String(j+1)+'. '+label.replace(/[<>&]/g,function(c){return c==='<'?'&lt;':c==='>'?'&gt;':'&amp;';})+'</div>';
      }
      if(sl.innerHTML!==html){
        sl.innerHTML=html;
      }
    }
  }).catch(function(){});
}

setInterval(function(){if(st)document.getElementById('tmr').textContent=fmt(Date.now()-st);},500);
setInterval(poll,250);
poll();
</script>
</body></html>`;

function startWidgetServer() {
  return new Promise((resolve, reject) => {
    const server = createServer((req, res) => {
      res.setHeader('Access-Control-Allow-Origin', '*');

      if (req.method === 'GET' && req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(WIDGET_HTML);
        return;
      }
      if (req.method === 'GET' && req.url === '/state') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(_widgetState));
        return;
      }
      if (req.method === 'POST' && req.url === '/action') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
          try {
            const { action } = JSON.parse(body);
            const key = action === 'enter' ? 'enter' : action[0].toLowerCase();
            _keyQueue.push(key);
            if (_keyQueueReady) { _keyQueueReady(); _keyQueueReady = null; }
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end('{"ok":true}');
          } catch {
            res.writeHead(400); res.end('{}');
          }
        });
        return;
      }
      if (req.method === 'POST' && req.url === '/pause') {
        _widgetPauseRequested = !_widgetPauseRequested;
        widgetUpdate({ pauseRequested: _widgetPauseRequested });
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ pauseRequested: _widgetPauseRequested }));
        return;
      }
      res.writeHead(404); res.end();
    });

    server.listen(0, '127.0.0.1', () => {
      resolve({ server, port: server.address().port });
    });
    server.on('error', reject);
  });
}

async function launchWidgetWindow(port, edgePath) {
  const userDataDir = join(process.env.TEMP || process.env.TMPDIR || '/tmp', 'edge-widget');
  spawn(edgePath, [
    `--app=http://127.0.0.1:${port}`,
    '--window-size=364,300',
    '--window-position=10,200',
    `--user-data-dir=${userDataDir}`,
  ], { detached: true, stdio: 'ignore' }).unref();
  console.log(`Widget window launched at http://127.0.0.1:${port}`);

  // Set always-on-top via PowerShell after the window has had time to open
  setTimeout(() => {
    const ps = [
      'Add-Type -TypeDefinition @"',
      'using System; using System.Runtime.InteropServices;',
      'public class Win32 {',
      '  [DllImport("user32.dll")] public static extern bool SetWindowPos(',
      '    IntPtr h, IntPtr hAfter, int x, int y, int cx, int cy, uint flags);',
      '  public static readonly IntPtr HWND_TOPMOST = new IntPtr(-1);',
      '}',
      '"@',
      '$title = "Demo"',
      '$hwnd = (Get-Process msedge | Where-Object { $_.MainWindowTitle -eq $title } | Select-Object -First 1).MainWindowHandle',
      'if ($hwnd) { [Win32]::SetWindowPos([IntPtr]$hwnd, [Win32]::HWND_TOPMOST, 0,0,0,0, 0x0003) }',
    ].join('\n');
    spawn('powershell', ['-NoProfile', '-NonInteractive', '-Command', ps], {
      detached: true, stdio: 'ignore',
    }).unref();
  }, 3000);
}

// ─── Entry point ─────────────────────────────────────────────────────────────

async function main() {
  await ensureEdgeRunning();

  console.log(`Connecting to Edge at ${CDP_URL}...`);
  const browser = await chromium.connectOverCDP(CDP_URL);

  const contexts = browser.contexts();
  const context = contexts[0] ?? await browser.newContext();
  const pages = context.pages();
  const page = pages[0] ?? await context.newPage();

  let _widgetServer = null;
  if (USE_WIDGET) {
    const edgePath = findEdgePath();
    if (!edgePath) {
      console.warn('  Warning: msedge.exe not found — widget window skipped.');
    } else {
      const { server, port } = await startWidgetServer();
      _widgetServer = server;
      await launchWidgetWindow(port, edgePath);
    }
  }

  let steps;
  let getActivePage = () => page;

  // If the argument is a .demo script file, parse it; otherwise use a named scenario.
  if (SCENARIO.endsWith('.demo')) {
    const scriptPath = resolve(SCENARIO);
    const scriptName = basename(scriptPath, '.demo');
    const { overrides: _overrides = {}, ..._globalVars } = _demoVars;
    const externalVars = { ..._globalVars, ...(_overrides[scriptName] ?? {}) };
    const src = readFileSync(scriptPath, 'utf8');
    const parsed = parseScript(src, page, RUN_SECTION, externalVars);
    steps = parsed.steps;
    getActivePage = parsed.getActivePage;
    if (!steps.length) {
      console.error(`No steps found for section "${RUN_SECTION}" in ${scriptPath}.`);
      console.error('Add a [section: setup], [section: demo], [section: reset], or custom [section: name] marker to the script.');
      process.exit(1);
    }
    if (RUN_SECTION === 'setup' || RUN_SECTION === 'reset') {
      console.log(`Running section: ${RUN_SECTION.toUpperCase()}\n`);
    }
  } else {
    const buildSteps = scenarios[SCENARIO];
    if (!buildSteps) {
      console.error(`Unknown scenario "${SCENARIO}". Available: ${Object.keys(scenarios).join(', ')}`);
      console.error('Or pass a path to a .demo script file.');
      process.exit(1);
    }
    steps = buildSteps(page);
  }

  // In record mode: attempt OBS connection before the demo starts
  if (RECORD_MODE) {
    try {
      const obs = await import('./obs-record.mjs');
      const obsPassword = process.env.OBS_PASSWORD || _cfg.obsPassword || '';
      _obsConn = await obs.tryConnectOBS('ws://127.0.0.1:4455', obsPassword);
      if (_obsConn) {
        const res = await obs.ensureFullResolution(_obsConn);
        _obsRecordingStartMs = await obs.startRecording(_obsConn);
        const resNote = res ? ` (${res})` : '';
        console.log(`  \x1B[33m⏺  OBS recording started${resNote}\x1B[0m\n`);
      } else {
        console.log('  OBS not reachable — screenshot-only mode\n');
      }
    } catch (e) {
      console.log(`  OBS skipped: ${e.message}\n`);
    }
  }

  await runSteps(getActivePage, steps);

  // Stop OBS recording and patch videoFile into the saved events.json
  if (RECORD_MODE && _obsConn) {
    try {
      const obs = await import('./obs-record.mjs');
      const videoFile = await obs.stopRecording(_obsConn);
      obs.disconnectOBS(_obsConn);
      if (videoFile) {
        const eventsPath = join(_scriptDir, '..', 'recordings', _scenarioKey, 'events.json');
        if (existsSync(eventsPath)) {
          const ev = JSON.parse(readFileSync(eventsPath, 'utf8'));
          ev.videoFile = videoFile;
          writeFileSync(eventsPath, JSON.stringify(ev, null, 2));
          console.log(`  \x1B[32m✓\x1B[0m  OBS recording → ${videoFile}`);
        }
      }
    } catch { /* ignore */ }
  }

  // After demo/all completes, offer to run the reset section if one exists.
  if (SCENARIO.endsWith('.demo') && (RUN_SECTION === 'demo' || RUN_SECTION === 'all')) {
    const scriptPath = resolve(SCENARIO);
    const src = readFileSync(scriptPath, 'utf8');
    if (src.includes('[section: reset]')) {
      widgetUpdate({ resetAvailable: true, waiting: true });
      waitPrompt('  Demo complete — press r to reset, or Enter to close: ');
      const k = await waitForKey();
      widgetUpdate({ resetAvailable: false, waiting: false });
      if (k === 'r') {
        const scriptName = basename(scriptPath, '.demo');
        const { overrides: _overrides = {}, ..._globalVars } = _demoVars;
        const externalVars = { ..._globalVars, ...(_overrides[scriptName] ?? {}) };
        const resetParsed = parseScript(src, page, 'reset', externalVars);
        if (resetParsed.steps.length) {
          console.log('\nRunning section: RESET\n');
          await runSteps(resetParsed.getActivePage, resetParsed.steps);
        }
      }
    }
  }

  await browser.close();
  if (_widgetServer) _widgetServer.close();
}

// ─── Scenario definitions ─────────────────────────────────────────────────────

/**
 * Returns the step list for the "tell-me-about-site" scenario.
 * Each step is { name, run } — run() is called when the operator presses Enter.
 */
function tellMeAboutSiteSteps(page) {
  const SITE_URL = 'https://microsoft.sharepoint-df.com/teams/ZachDemos/';
  // chatFrame is shared across steps; populated once the pane is open
  let chatFrame = null;

  return [
    {
      name: `Navigate to ${SITE_URL}`,
      async run() {
        await page.goto(SITE_URL, { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(3000); // let SPFx webparts settle
      },
    },
    {
      name: 'Open Copilot chat pane via FAB',
      async run() {
        const chatIframeLocator = page.locator('[data-automationid="ChatODSPFrame"]');
        const alreadyOpen = await chatIframeLocator.isVisible({ timeout: 8000 }).catch(() => false);
        if (alreadyOpen) {
          console.log('    Chat pane already open — skipping FAB.');
        } else {
          await openChatPane(page);
        }
        chatFrame = page.frameLocator('[data-automationid="ChatODSPFrame"]');
      },
    },
    {
      name: 'Type and submit: "Tell me about this site"',
      async run() {
        const input = await getChatInput(page, chatFrame);
        await slowType(input, 'Tell me about this site');
        await input.press('Enter');
      },
    },
    {
      name: 'Wait for Copilot response',
      async run() {
        await waitForCopilotResponse(page, chatFrame);
        await page.screenshot({ path: 'tools/result-screenshot.png' });
        console.log('    Screenshot saved to tools/result-screenshot.png');
      },
    },
  ];
}

// ─── Script parser ───────────────────────────────────────────────────────────

/**
 * Parse a .demo script into an array of steps for runSteps().
 *
 * Script syntax:
 *   # title/comment lines     — displayed as section headers, not steps
 *   plain text paragraphs     — talking points shown to presenter before the next command
 *   [command]                 — automated action (becomes a step)
 *   [command: value]          — automated action with an argument
 *
 * Section markers (optional — if omitted, all steps go to "demo"):
 *   [section: setup]          steps that run with --setup flag
 *   [section: demo]           steps that run by default
 *   [section: reset]          steps that run with --reset flag
 *
 * Commands:
 *   [var: NAME = value]       define a script variable — use as ${NAME} anywhere in the script
 *   [navigate: URL]           navigate to a URL
 *   [open-tab: URL]           open a new browser tab and switch all subsequent steps to it
 *   [open-chat]               open the Copilot chat pane via FAB
 *   [prompt: text]            slow-type text into chat and submit
 *   [wait]                    wait for Copilot to finish responding
 *   [pause]                   wait for presenter to press Enter
 *   [new-chat]                click Chat options → New chat to clear the conversation
 *   [upload: local/path]      open Attach in the input menu, then wait for presenter
 *                             to select the file in the OS dialog
 *   [confirm: message]        destructive action — warn presenter and wait for
 *                             confirmation that they've clicked the button in the UI
 *   [screenshot: path]        save a screenshot
 *   [enable-site-feature: Name]  navigate to ManageFeatures.aspx?Scope=Site and activate
 *                             the named feature if not already active, then return.
 *                             Preferred: [enable-site-feature: Name | GUID] uses the
 *                             REST API directly (/_api/site/features/add) — more reliable
 *   [upload-skill: Skills/name]  upload a local skill folder (SKILL.md + any subdirs) to
 *                             the AgentAssets library folder derived from the current page URL
 */
function parseScript(src, page, section = 'demo', externalVars = {}) {
  // Pre-process: collapse multi-line [command: ...] blocks into single lines.
  // A line that starts with '[' but doesn't end with ']' is continued until a
  // line ending with ']' is found; interior newlines become spaces.
  const rawLines = src.split('\n');
  const lines = [];
  let joining = null;
  for (const line of rawLines) {
    const trimmed = line.trim();
    if (joining !== null) {
      joining += ' ' + trimmed;
      if (trimmed.endsWith(']')) {
        lines.push(joining);
        joining = null;
      }
    } else if (trimmed.startsWith('[') && !trimmed.endsWith(']')) {
      joining = trimmed;
    } else {
      lines.push(line);
    }
  }
  if (joining !== null) lines.push(joining); // unterminated block — push as-is

  const blocks = []; // { type: 'comment'|'talking'|'command'|'section', value, raw }

  // Script variables — set with [var: NAME = value], used as ${NAME} anywhere in the script.
  // A first pass collects all [var] declarations before building steps, so vars defined
  // anywhere in the file are available everywhere (including lines before the declaration).
  // demo.vars.json (gitignored) is pre-seeded and takes precedence over script [var:] defaults.
  const vars = { ...externalVars };
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
      const inner = trimmed.slice(1, -1);
      const colonIdx = inner.indexOf(':');
      if (colonIdx !== -1) {
        const cmd = inner.slice(0, colonIdx).trim();
        const rest = inner.slice(colonIdx + 1).trim();
        if (cmd === 'var') {
          const eqIdx = rest.indexOf('=');
          if (eqIdx !== -1) {
            const name = rest.slice(0, eqIdx).trim();
            const value = rest.slice(eqIdx + 1).trim();
            if (!(name in vars)) vars[name] = value; // file vars win
          }
        }
      }
    }
  }

  // Substitute ${VAR} in a string using the collected vars map.
  const interpolate = str => str.replace(/\$\{([^}]+)\}/g, (_, name) => vars[name] ?? `\${${name}}`);

  // Allow var values to reference other vars (e.g. [var: LIBRARY = ${SITE}/Contracts/])
  for (const k of Object.keys(vars)) vars[k] = interpolate(vars[k]);

  let currentSection = 'demo'; // default section if no markers present

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (trimmed.startsWith('#')) {
      blocks.push({ type: 'comment', value: interpolate(trimmed.replace(/^#+\s*/, '')), section: currentSection });
    } else if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
      const inner = trimmed.slice(1, -1);
      const colonIdx = inner.indexOf(':');
      const cmd = colonIdx === -1 ? inner.trim() : inner.slice(0, colonIdx).trim();
      const arg = colonIdx === -1 ? '' : interpolate(inner.slice(colonIdx + 1).trim());

      if (cmd === 'section') {
        currentSection = arg.toLowerCase();
      } else if (cmd === 'var' || cmd === 'category') {
        // Metadata only — skip as a runnable step.
      } else {
        blocks.push({ type: 'command', cmd, arg, section: currentSection });
      }
    } else {
      // Merge consecutive talking-point lines into the previous talking block
      const interpolated = interpolate(trimmed);
      if (blocks.length && blocks[blocks.length - 1].type === 'talking' && blocks[blocks.length - 1].section === currentSection) {
        blocks[blocks.length - 1].value += ' ' + interpolated;
      } else {
        blocks.push({ type: 'talking', value: interpolated, section: currentSection });
      }
    }
  }

  // Filter to the requested section ('all' runs setup then demo in one pass)
  const sectionBlocks = section === 'all'
    ? blocks.filter(b => b.section === 'setup' || b.section === 'demo')
    : blocks.filter(b => b.section === section);

  // Convert blocks into steps. Each command becomes one step.
  // Talking points and comments that precede a command are attached to it.
  // Trailing talking points with no following command get an implicit [pause] step.
  const steps = [];
  let pendingContext = []; // talking points / comments accumulated before next command
  let chatFrame = null;
  let activePage = page;

  const flushContext = () => {
    const ctx = pendingContext.slice();
    pendingContext = [];
    return ctx;
  };

  const commandToStep = (cmd, arg, ctx) => {
    const talkingLines = ctx.filter(b => b.type === 'talking' || b.type === 'comment');
    const displayContext = talkingLines.map(b => b.value);

    const printContext = () => {
      if (!displayContext.length) return;
      const COL = '\x1B[33m';   // amber
      const RST = '\x1B[0m';
      const TXT = '\x1B[97m';   // bright white for talking point text
      const BAR = `${COL}▌${RST} `;
      const WIDTH = (process.stdout.columns || 80) - 6; // leave room for bar + indent

      console.log('');
      for (const line of displayContext) {
        const words = line.split(' ');
        let row = '';
        for (const w of words) {
          if (row.length + w.length + (row ? 1 : 0) > WIDTH) {
            console.log(`  ${BAR}${TXT}${row}${RST}`);
            row = w;
          } else {
            row += (row ? ' ' : '') + w;
          }
        }
        if (row) console.log(`  ${BAR}${TXT}${row}${RST}`);
      }
      console.log('');

      // Mirror talking points to the widget's full-mode view
      widgetUpdate({ context: displayContext.join('\n\n') });
    };

    switch (cmd) {
      case 'navigate':
        return {
          name: `Navigate to ${arg}`,
          async run() {
            printContext();
            await activePage.goto(arg, { waitUntil: 'load', timeout: 60000 });
            await activePage.waitForTimeout(3000);
          },
        };

      case 'open-chat':
        return {
          name: 'Open Copilot chat pane',
          async run() {
            printContext();
            const iframe = activePage.locator('[data-automationid="ChatODSPFrame"]');
            if (!await iframe.isVisible({ timeout: 15000 }).catch(() => false)) {
              await openChatPane(activePage);
            } else {
              console.log('    Chat pane already open.');
            }
            chatFrame = activePage.frameLocator('[data-automationid="ChatODSPFrame"]');
          },
        };

      case 'prompt':
        return {
          name: `Prompt: "${arg}"`,
          async run() {
            printContext();
            if (!chatFrame) {
              const iframe = activePage.locator('[data-automationid="ChatODSPFrame"]');
              if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
                await openChatPane(activePage);
              }
              chatFrame = activePage.frameLocator('[data-automationid="ChatODSPFrame"]');
            }
            const input = await getChatInput(activePage, chatFrame);
            await slowType(input, arg);
            await input.press('Enter');
          },
        };

      case 'wait':
        return {
          name: 'Wait for Copilot response',
          async run() {
            printContext();
            const ac = new AbortController();
            let nav;

            // Listen for s/b from widget buttons or terminal keypress
            const prevReady = _keyQueueReady;
            _keyQueueReady = function () {
              if (prevReady) prevReady();
              const idx = _keyQueue.findIndex(k => k === 's' || k === 'b');
              if (idx !== -1) { nav = _keyQueue.splice(idx, 1)[0] === 'b' ? 'back' : 'skip'; ac.abort(); }
            };
            let rawListener = null;
            if (process.stdin.isTTY) {
              process.stdin.setRawMode(true);
              process.stdin.resume();
              rawListener = buf => {
                const k = buf.toString();
                if (k === '\x03') process.exit(0);
                if (k === 'b') { nav = 'back'; ac.abort(); }
                else if (k === 's') { nav = 'skip'; ac.abort(); }
              };
              process.stdin.on('data', rawListener);
            }

            try {
              await waitForCopilotResponse(activePage, chatFrame, 300000, ac.signal);
            } finally {
              _keyQueueReady = prevReady;
              if (rawListener) {
                process.stdin.off('data', rawListener);
                process.stdin.setRawMode(false);
                process.stdin.pause();
              }
            }
            if (nav) console.log('');
            return nav;
          },
        };

      case 'pause':
        return {
          name: arg || 'Pause — presenter moment',
          isPause: true,
          async run() {
            printContext();
            waitPrompt('  ▶  Enter=continue   b=back   s=skip   g<n>=goto  ');
            const key = await waitForKey();
            console.log('');
            if (key === 'b') return 'back';
            if (key === 's') return 'skip';
            if (key && key.startsWith('g') && /^\d+$/.test(key.slice(1))) return key;
          },
        };

      case 'login-if-needed':
        return {
          name: 'Login if needed',
          async run() {
            const AUTH_HOSTS = /login\.(microsoftonline|live|microsoft)\.com/i;
            const isAuthPage = () => AUTH_HOSTS.test(activePage.url());

            // Also check for the Microsoft sign-in form in case of silent redirect
            const hasSignInForm = async () => {
              return activePage.locator('input[type="email"], input[name="loginfmt"], [data-testid="i0116"]')
                .first().isVisible({ timeout: 2000 }).catch(() => false);
            };

            if (!isAuthPage() && !await hasSignInForm()) {
              console.log('    Already authenticated — skipping login.');
              return;
            }

            console.log('');
            console.log('  ┌─────────────────────────────────────────────────────────┐');
            console.log('  │  SIGN IN REQUIRED                                       │');
            console.log('  │  Complete the Microsoft login in the browser window,    │');
            console.log('  │  then press Enter to continue.                          │');
            console.log('  └─────────────────────────────────────────────────────────┘');
            waitPrompt('  ▶  Press Enter once signed in... ');
            await waitForKey();
            console.log('');

            // Wait for the post-login redirect to settle
            await activePage.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
            await activePage.waitForTimeout(2000);
            console.log('    Signed in. Continuing.');
          },
        };

      case 'confirm': {
        const confirmMsg = arg || 'Complete the action in the browser, then press Enter.';
        return {
          name: `⚠ Confirm in browser: ${confirmMsg}`,
          async run() {
            printContext();
            console.log('  ┌─────────────────────────────────────────────────────────┐');
            console.log(`  │  ACTION REQUIRED IN BROWSER                             │`);
            console.log('  │                                                         │');
            const words = confirmMsg.split(' ');
            let row = '  │  ';
            for (const w of words) {
              if (row.length + w.length + 1 > 60) { console.log(row.padEnd(60) + '│'); row = '  │  ' + w; }
              else row += (row === '  │  ' ? '' : ' ') + w;
            }
            if (row.trim() !== '│') console.log(row.padEnd(60) + '│');
            console.log('  │                                                         │');
            console.log('  └─────────────────────────────────────────────────────────┘');
            waitPrompt('  ▶  Press Enter once you have completed the action... ');
            const key = await waitForKey();
            if (key === 'b') return 'back';
            if (key === 's') return 'skip';
            console.log('  Confirmed.\n');
          },
        };
      }

      case 'new-chat':
        return {
          name: 'New chat (clear Copilot conversation)',
          async run() {
            printContext();
            // Re-check pane visibility even if chatFrame is set — the pane may have closed
            // or be temporarily hidden while the page re-renders after navigation.
            const iframe = activePage.locator('[data-automationid="ChatODSPFrame"]');
            if (!await iframe.isVisible({ timeout: 12000 }).catch(() => false)) {
              await openChatPane(activePage);
            }
            chatFrame = activePage.frameLocator('[data-automationid="ChatODSPFrame"]');
            await startNewChat(activePage, chatFrame);
          },
        };

      case 'upload': {
        const uploadPath = resolve(_scriptDir, '..', arg);
        const uploadFileName = uploadPath.split(/[\\/]/).pop();
        return {
          name: `Upload file: ${uploadFileName}`,
          async run() {
            printContext();
            if (!chatFrame) {
              const iframe = activePage.locator('[data-automationid="ChatODSPFrame"]');
              if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
                throw new Error('[upload] requires the chat pane to be open first.');
              }
              chatFrame = activePage.frameLocator('[data-automationid="ChatODSPFrame"]');
            }
            // Click the chat input to focus, then open the input menu
            await chatFrame.locator('[contenteditable="true"]').first().click();
            await activePage.waitForTimeout(200);
            await chatFrame.locator('[aria-label="Open input menu"]').click();
            await activePage.waitForTimeout(400);
            await chatFrame.locator('[role="menuitem"]:has-text("Attach")').first().click();
            await activePage.waitForTimeout(300);
            // File picker is an OS-native dialog — hand off to presenter
            console.log('');
            console.log('  ┌─────────────────────────────────────────────────────────┐');
            console.log('  │  FILE UPLOAD — select this file in the dialog:          │');
            console.log(`  │  ${uploadPath.slice(0, 53).padEnd(55)}│`);
            console.log('  └─────────────────────────────────────────────────────────┘');
            waitPrompt('  ▶  Press Enter once the file is attached in the chat... ');
            const key = await waitForKey();
            if (key === 'b') return 'back';
            if (key === 's') return 'skip';
            console.log('  File attached.\n');
          },
        };
      }

      case 'sleep': {
        const sleepMatch = arg.match(/^(\d+(?:\.\d+)?)(ms|s)?$/);
        const sleepMs = sleepMatch
          ? (sleepMatch[2] === 'ms' ? parseFloat(sleepMatch[1]) : parseFloat(sleepMatch[1]) * 1000)
          : 3000;
        return {
          name: `Sleep ${arg || '3s'}`,
          async run() {
            printContext();
            console.log(`    Waiting ${sleepMs}ms...`);
            await activePage.waitForTimeout(sleepMs);
          },
        };
      }

      case 'scene': {
        const sceneName = arg;
        return {
          name: `Scene: ${sceneName}`,
          async run() {
            if (!_obsConn) {
              console.log(`    OBS not connected — [scene: ${sceneName}] skipped.`);
              return;
            }
            try {
              const obs = await import('./obs-record.mjs');
              await obs.switchScene(_obsConn, sceneName);
              await activePage.waitForTimeout(300); // let the transition settle
              console.log(`    Scene → ${sceneName}`);
            } catch (e) {
              console.warn(`    Scene switch failed: ${e.message}`);
            }
          },
        };
      }

      case 'screenshot': {
        const screenshotPath = resolve(_scriptDir, '..', arg || 'tools/screenshots/demo.png');
        return {
          name: `Screenshot → ${screenshotPath}`,
          async run() {
            printContext();
            mkdirSync(dirname(screenshotPath), { recursive: true });
            await activePage.screenshot({ path: screenshotPath });
            console.log(`    Saved ${screenshotPath}`);
          },
        };
      }

      case 'assert': {
        const assertUrl = arg;
        return {
          name: `Assert accessible: ${assertUrl}`,
          async run() {
            printContext();
            process.stdout.write(`    Waiting for ${assertUrl} ...`);
            // Poll via fetch() inside the active page so we don't open a visible tab.
            // Runs in the browser's auth context so SharePoint cookies are included.
            // Retry every 3s for up to 60s — gives SharePoint time to finish creating
            // a library or list before the next navigate/upload step.
            const deadline = Date.now() + 60_000;
            let passed = false;
            while (!passed && Date.now() < deadline) {
              passed = await activePage.evaluate(async (url) => {
                try {
                  const r = await fetch(url, { method: 'HEAD', credentials: 'include' });
                  return r.ok;
                } catch { return false; }
              }, assertUrl).catch(() => false);
              if (!passed && Date.now() < deadline) {
                process.stdout.write('.');
                await new Promise(r => setTimeout(r, 3000));
              }
            }
            if (passed) {
              console.log(' OK');
            } else {
              console.log('');
              console.log('  ┌─────────────────────────────────────────────────────────┐');
              console.log('  │  ASSERTION FAILED — resource not accessible after 60s   │');
              console.log(`  │  ${assertUrl.slice(0, 53).padEnd(55)}│`);
              console.log('  │  Check the setup instructions before continuing.        │');
              console.log('  └─────────────────────────────────────────────────────────┘');
              waitPrompt('  ▶  Press Enter to continue anyway, or Ctrl+C to abort... ');
              await waitForKey();
              console.log('');
            }
          },
        };
      }

      case 'upload-library': {
        const localPath = resolve(_scriptDir, '..', arg);
        const uploadFileName = basename(localPath);
        return {
          name: `Upload to library: ${uploadFileName}`,
          async run() {
            printContext();

            // If the asset doesn't exist locally, fall back to a manual confirm.
            if (!existsSync(localPath)) {
              console.log('');
              console.log('  ┌─────────────────────────────────────────────────────────┐');
              console.log('  │  ASSET NOT FOUND — upload manually:                     │');
              console.log(`  │  ${uploadFileName.slice(0, 53).padEnd(55)}│`);
              console.log('  │  Upload the file to the current library, then continue. │');
              console.log('  └─────────────────────────────────────────────────────────┘');
              waitPrompt('  ▶  Press Enter once the file is uploaded, or s to skip... ');
              const k = await waitForKey();
              if (k === 'b') return 'back';
              if (k === 's') return 'skip';
              return;
            }

            // Derive server-relative folder path from current page URL.
            // Prefer RootFolder/id query param (set when browsing into a subfolder)
            // over the pathname (which only contains the library root in that case).
            // e.g. pathname: /sites/demo/Messy%20Files/Forms/AllItems.aspx → /sites/demo/Messy Files
            // e.g. ?RootFolder=%2Fsites%2Fdemo%2FMessy%20Files%2FSubfolder → /sites/demo/Messy Files/Subfolder
            const urlObj = new URL(activePage.url());
            const origin = urlObj.origin;
            const rootFolderParam = urlObj.searchParams.get('RootFolder') ?? urlObj.searchParams.get('id');
            const folderPath = rootFolderParam
              ? decodeURIComponent(rootFolderParam).replace(/\/$/, '')
              : decodeURIComponent(urlObj.pathname.replace(/\/Forms\/[^/]*$/, '').replace(/\/$/, ''));

            process.stdout.write(`    Checking "${uploadFileName}"... `);

            // Check existence and fetch form digest in one browser-context call.
            // Use _spPageContextInfo.webAbsoluteUrl so API calls are scoped to the
            // correct site (e.g. /teams/ZachEval/_api/...) not just the origin.
            const check = await activePage.evaluate(async ({ origin, folder, file }) => {
              const webUrl = window._spPageContextInfo?.webAbsoluteUrl ?? origin;

              const headResp = await fetch(
                `${origin}${encodeURI(folder)}/${encodeURIComponent(file)}`,
                { method: 'HEAD' }
              ).catch(() => null);
              if (headResp?.ok) return { exists: true };

              const digestResp = await fetch(`${webUrl}/_api/contextinfo`, {
                method: 'POST',
                headers: { 'Accept': 'application/json;odata=verbose' },
              }).catch(() => null);
              if (!digestResp?.ok) return { exists: false, error: 'no-digest' };
              const json = await digestResp.json().catch(() => null);
              const digest = json?.d?.GetContextWebInformation?.FormDigestValue ?? null;
              if (!digest) return { exists: false, error: 'no-digest' };
              return { exists: false, digest, webUrl };
            }, { origin, folder: folderPath, file: uploadFileName });

            if (check.exists) {
              console.log('already present — skipping.');
              return;
            }

            if (check.error) {
              console.log('\n  ⚠  Could not authenticate with SharePoint.');
              waitPrompt('  ▶  Upload the file manually, then press Enter... ');
              const k = await waitForKey();
              if (k === 'b') return 'back';
              if (k === 's') return 'skip';
              return;
            }

            console.log('uploading...');
            process.stdout.write(`    Uploading "${uploadFileName}"... `);

            // Files over 50 MB are too large to pass through page.evaluate() as base64
            // without crashing the browser tab. Fall through to a manual prompt.
            const fileSizeMB = statSync(localPath).size / (1024 * 1024);
            if (fileSizeMB > 50) {
              console.log(`skipping (${Math.round(fileSizeMB)} MB — too large for automated upload).`);
              console.log(`  ℹ  Upload "${uploadFileName}" manually to SharePoint.`);
              waitPrompt('  ▶  Upload the file manually, then press Enter... ');
              const k = await waitForKey();
              if (k === 'b') return 'back';
              if (k === 's') return 'skip';
              return;
            }

            // Upload via page.evaluate() so the request runs inside the browser and
            // automatically uses the live session cookies.
            const fileBase64 = readFileSync(localPath).toString('base64');
            const escapedFolder = folderPath.replace(/'/g, "''");
            const escapedFile   = uploadFileName.replace(/'/g, "''");
            const upload = await activePage.evaluate(
              async ({ webUrl, folder, file, b64, digest }) => {
                const binary = atob(b64);
                const buf = new Uint8Array(binary.length);
                for (let i = 0; i < binary.length; i++) buf[i] = binary.charCodeAt(i);
                const apiUrl = `${webUrl}/_api/web/GetFolderByServerRelativeUrl('${folder}')/Files/add(url='${file}',overwrite=true)`;
                const resp = await fetch(apiUrl, {
                  method: 'POST',
                  headers: {
                    'Accept': 'application/json;odata=verbose',
                    'X-RequestDigest': digest,
                  },
                  body: buf.buffer,
                }).catch(() => ({ ok: false, status: 0 }));
                return { ok: resp.ok, status: resp.status };
              },
              { webUrl: check.webUrl, folder: escapedFolder, file: escapedFile, b64: fileBase64, digest: check.digest }
            );

            if (upload.ok) {
              console.log('done.');
            } else {
              console.log(`failed (HTTP ${upload.status}).`);
              waitPrompt('  ▶  Upload the file manually, then press Enter... ');
              const k = await waitForKey();
              if (k === 'b') return 'back';
              if (k === 's') return 'skip';
            }
          },
        };
      }

      case 'select': {
        const selectArg = arg.trim().toLowerCase();
        return {
          name: `Select: ${selectArg}`,
          async run() {
            printContext();

            if (selectArg === 'all') {
              // Click the "Select all" checkbox in the list/library header.
              // SharePoint uses "Select All" (capital A) in modern lists; CSS attribute
              // selectors are case-sensitive so we try getByRole (case-insensitive) first,
              // then fall back through CSS variants.
              const attempts = [
                () => activePage.getByRole('checkbox', { name: /select all/i }).first(),
                () => activePage.locator('[data-automationid="SelectAllCheckbox"]').first(),
                () => activePage.locator('[data-automationid="SelectAllCheckbox"] input').first(),
                () => activePage.locator('[data-automationid="SelectAllCheckbox"] [role="checkbox"]').first(),
                () => activePage.locator('[aria-label="Select All"]').first(),
                () => activePage.locator('[aria-label="Select All Items"]').first(),
                () => activePage.locator('[aria-label="Select all items"]').first(),
                () => activePage.locator('[aria-label="Select all"]').first(),
              ];

              let clicked = false;
              for (const attempt of attempts) {
                const el = attempt();
                if (await el.isVisible({ timeout: 2000 }).catch(() => false)) {
                  // force:true bypasses decorative overlay spans (e.g. checkFocusRing)
                  // that sit on top of the checkbox and intercept pointer events.
                  await el.click({ timeout: 5000, force: true });
                  clicked = true;
                  break;
                }
              }
              if (!clicked) {
                throw new Error('[select:all] Could not find a "Select All" checkbox — is a list or library visible on this page?');
              }
              console.log('    Selected all items.');
              return;
            }

            // Parse "N" or "N-M"
            const rangeMatch = selectArg.match(/^(\d+)(?:-(\d+))?$/);
            if (!rangeMatch) {
              throw new Error(`[select] invalid argument "${arg}" — use a number, range (e.g. 1-3), or "all"`);
            }
            const start = parseInt(rangeMatch[1], 10);
            const end = rangeMatch[2] ? parseInt(rangeMatch[2], 10) : start;

            // Gather all list rows, skipping the header row (aria-rowindex="1" or no aria-rowindex).
            // SharePoint assigns aria-rowindex starting at 1 for the header and 2+ for data rows,
            // so item N corresponds to aria-rowindex N+1.
            for (let n = start; n <= end; n++) {
              // Try aria-rowindex first (modern SharePoint details list)
              let row = activePage.locator(`[role="row"][aria-rowindex="${n + 1}"]`).first();
              if (!await row.isVisible({ timeout: 3000 }).catch(() => false)) {
                // Fallback: nth data row by position (skip header)
                row = activePage.locator('[role="row"]').nth(n); // nth(0)=header, nth(1)=item1
              }
              await row.hover({ timeout: 5000 });
              await activePage.waitForTimeout(150); // let hover-reveal animation settle
              // Checkbox selector covers modern SP and classic variants
              const checkbox = row.locator(
                '[role="checkbox"], button[aria-label="Select"], [data-automationid="DetailsRowCheck"] button'
              ).first();
              await checkbox.click({ timeout: 3000 });
              console.log(`    Selected item ${n}.`);
            }
          },
        };
      }

      case 'open-tab': {
        const tabUrl = arg;
        return {
          name: `Open new tab: ${tabUrl}`,
          async run() {
            printContext();
            const newPage = await activePage.context().newPage();
            await newPage.goto(tabUrl, { waitUntil: 'load', timeout: 60000 });
            await newPage.waitForTimeout(3000);
            await newPage.bringToFront();
            activePage = newPage;
            chatFrame = null; // reset — new tab has its own chat context
            console.log(`    Opened new tab: ${tabUrl}`);
          },
        };
      }

      case 'upload-skill': {
        // Optional subfolder within the library: [upload-skill: Skills/name | Subfolder]
        const pipeIdx = arg.indexOf('|');
        const skillLocalPath = resolve(_scriptDir, '..', (pipeIdx === -1 ? arg : arg.slice(0, pipeIdx)).trim());
        const skillName = basename(skillLocalPath);
        const skillSubfolder = pipeIdx === -1 ? null : arg.slice(pipeIdx + 1).trim() || null;

        // Collect all files under the skill directory, returning relative paths.
        function collectSkillFiles(dir, rel = '') {
          const results = [];
          for (const entry of readdirSync(dir, { withFileTypes: true })) {
            const entryRel = rel ? `${rel}/${entry.name}` : entry.name;
            if (entry.isDirectory()) {
              results.push(...collectSkillFiles(join(dir, entry.name), entryRel));
            } else {
              results.push({ rel: entryRel, abs: join(dir, entry.name) });
            }
          }
          return results;
        }

        return {
          name: `Upload skill: ${skillName}`,
          async run() {
            printContext();

            if (!existsSync(skillLocalPath)) {
              console.log(`  ⚠  Skill folder not found: ${skillLocalPath}`);
              return;
            }

            const files = collectSkillFiles(skillLocalPath);

            // Derive the AgentAssets library server-relative path from the current page URL.
            const urlObj = new URL(activePage.url());
            const origin = urlObj.origin;
            const rootFolderParam = urlObj.searchParams.get('RootFolder') ?? urlObj.searchParams.get('id');
            const libraryFolder = rootFolderParam
              ? decodeURIComponent(rootFolderParam).replace(/\/$/, '')
              : decodeURIComponent(urlObj.pathname.replace(/\/Forms\/[^/]*$/, '').replace(/\/$/, ''));

            // Prefer _spPageContextInfo for the site URL; fall back to deriving it from the
            // server-relative library path so we always get the correct sub-site (not root).
            const webUrl = await activePage.evaluate(() => window._spPageContextInfo?.webAbsoluteUrl).catch(() => null)
              ?? (() => {
                const m = libraryFolder.match(/^\/(sites|teams)\/[^/]+/);
                return m ? `${origin}${m[0]}` : origin;
              })();

            // Fetch form digest once for all operations.
            const digest = await activePage.evaluate(async (url) => {
              const r = await fetch(`${url}/_api/contextinfo`, {
                method: 'POST',
                headers: { 'Accept': 'application/json;odata=verbose' },
              }).catch(() => null);
              if (!r?.ok) return null;
              const json = await r.json().catch(() => null);
              return json?.d?.GetContextWebInformation?.FormDigestValue ?? null;
            }, webUrl);

            if (!digest) {
              console.log('  ⚠  Could not get form digest. Skipping skill upload.');
              return;
            }

            // Collect unique folders to create (in order — parents before children).
            // If a subfolder is specified (e.g. "Skills"), insert it between the library
            // root and the skill folder, creating it first if needed.
            const skillBase = skillSubfolder
              ? `${libraryFolder}/${skillSubfolder}`
              : libraryFolder;
            const foldersNeeded = skillSubfolder
              ? [`${libraryFolder}/${skillSubfolder}`, `${skillBase}/${skillName}`]
              : [`${libraryFolder}/${skillName}`];
            for (const { rel } of files) {
              const parts = rel.split('/');
              let path = `${skillBase}/${skillName}`;
              for (let i = 0; i < parts.length - 1; i++) {
                path += `/${parts[i]}`;
                if (!foldersNeeded.includes(path)) foldersNeeded.push(path);
              }
            }

            // Ensure each folder exists (409 = already exists → treat as ok).
            for (const folderPath of foldersNeeded) {
              const parentFolder = folderPath.slice(0, folderPath.lastIndexOf('/'));
              const folderName   = folderPath.slice(folderPath.lastIndexOf('/') + 1);
              const displayPath  = folderPath.replace(`${libraryFolder}/`, '');
              process.stdout.write(`    Ensuring folder "${displayPath}"... `);
              const r = await activePage.evaluate(async ({ webUrl, parent, fullPath, digest }) => {
                const escapedParent = parent.replace(/'/g, "''");
                const resp = await fetch(
                  `${webUrl}/_api/web/GetFolderByServerRelativeUrl('${escapedParent}')/Folders`,
                  {
                    method: 'POST',
                    headers: {
                      'Accept': 'application/json;odata=verbose',
                      'Content-Type': 'application/json;odata=verbose',
                      'X-RequestDigest': digest,
                    },
                    body: JSON.stringify({
                      '__metadata': { 'type': 'SP.Folder' },
                      'ServerRelativeUrl': fullPath,
                    }),
                  }
                ).catch(() => ({ ok: false, status: 0 }));
                return { ok: resp.ok, status: resp.status };
              }, { webUrl, parent: parentFolder, fullPath: folderPath, digest });
              console.log(r.ok || r.status === 409 ? 'ok.' : `failed (HTTP ${r.status}).`);
            }

            // Upload each file.
            for (const { rel, abs } of files) {
              const relDir = rel.includes('/') ? rel.slice(0, rel.lastIndexOf('/')) : '';
              const uploadFolder = relDir ? `${skillBase}/${skillName}/${relDir}` : `${skillBase}/${skillName}`;
              const fileName = basename(rel);
              process.stdout.write(`    Uploading "${rel}"... `);
              const fileBase64 = readFileSync(abs).toString('base64');
              const r = await activePage.evaluate(async ({ webUrl, folder, file, b64, digest }) => {
                const binary = atob(b64);
                const buf = new Uint8Array(binary.length);
                for (let i = 0; i < binary.length; i++) buf[i] = binary.charCodeAt(i);
                const escaped = folder.replace(/'/g, "''");
                const escapedFile = file.replace(/'/g, "''");
                const resp = await fetch(
                  `${webUrl}/_api/web/GetFolderByServerRelativeUrl('${escaped}')/Files/add(url='${escapedFile}',overwrite=true)`,
                  {
                    method: 'POST',
                    headers: { 'Accept': 'application/json;odata=verbose', 'X-RequestDigest': digest },
                    body: buf.buffer,
                  }
                ).catch(() => ({ ok: false, status: 0 }));
                return { ok: resp.ok, status: resp.status };
              }, { webUrl, folder: uploadFolder, file: fileName, b64: fileBase64, digest });
              console.log(r.ok ? 'done.' : `failed (HTTP ${r.status}).`);
            }
          },
        };
      }

      case 'enable-site-feature': {
        // Accepts "Feature Name" (uses ManageFeatures.aspx UI) or
        // "Feature Name | GUID" (uses /_api/site/features/add — preferred when GUID is known).
        const pipeIdx = arg.indexOf('|');
        const featureName = (pipeIdx === -1 ? arg : arg.slice(0, pipeIdx)).trim();
        const featureGuid = pipeIdx === -1 ? null : arg.slice(pipeIdx + 1).trim();
        return {
          name: `Enable site feature: ${featureName}`,
          async run() {
            printContext();
            const currentUrl = activePage.url();
            process.stdout.write(`    Checking site feature "${featureName}"... `);

            if (featureGuid) {
              // REST API path — derive the site URL from the current page's managed path
              // so it works even when _spPageContextInfo is absent (e.g. on AgentAssets pages).
              const siteUrl = await activePage.evaluate((guid) => {
                const spUrl = window._spPageContextInfo?.siteAbsoluteUrl;
                if (spUrl) return spUrl;
                const m = window.location.pathname.match(/^\/(sites|teams)\/[^/]+/);
                return window.location.origin + (m ? m[0] : '');
              }, featureGuid);

              const result = await activePage.evaluate(async ({ siteUrl, guid }) => {
                // Check if already active
                const checkResp = await fetch(
                  `${siteUrl}/_api/site/features?$filter=DefinitionId eq guid'${guid}'`,
                  { headers: { Accept: 'application/json;odata=verbose' } }
                ).catch(() => null);
                if (checkResp?.ok) {
                  const cj = await checkResp.json().catch(() => null);
                  if (cj?.d?.results?.length) return { status: 'already-active' };
                }

                // Activate via REST
                const dr = await fetch(`${siteUrl}/_api/contextinfo`, {
                  method: 'POST',
                  headers: { Accept: 'application/json;odata=verbose', 'Content-Type': 'application/json;odata=verbose' },
                }).catch(() => null);
                if (!dr?.ok) return { status: 'no-digest' };
                const dj = await dr.json().catch(() => null);
                const digest = dj?.d?.GetContextWebInformation?.FormDigestValue;
                if (!digest) return { status: 'no-digest' };

                const resp = await fetch(`${siteUrl}/_api/site/features/add`, {
                  method: 'POST',
                  headers: {
                    Accept: 'application/json;odata=verbose',
                    'Content-Type': 'application/json;odata=verbose',
                    'X-RequestDigest': digest,
                  },
                  body: JSON.stringify({ featureId: guid, force: true }),
                }).catch(() => ({ ok: false, status: 0 }));

                if (resp.ok) return { status: 'activated' };
                const body = await resp.text().catch(() => '');
                // A 500 with "already" in body means already active
                if (resp.status === 500 && /already/i.test(body)) return { status: 'already-active' };
                return { status: 'error', httpStatus: resp.status, body: body.slice(0, 200) };
              }, { siteUrl, guid: featureGuid });

              if (result.status === 'already-active') {
                console.log('already active.');
              } else if (result.status === 'activated') {
                console.log('activated.');
                await activePage.waitForTimeout(2000);
              } else if (result.status === 'no-digest') {
                console.log('could not get form digest.');
                console.log(`  ⚠  Activate "${featureName}" manually, then press Enter.`);
                waitPrompt('  ▶  Press Enter to continue... ');
                await waitForKey();
              } else {
                console.log(`failed (HTTP ${result.httpStatus}).`);
                console.log(`  ⚠  ${result.body}`);
                console.log(`  ⚠  Activate "${featureName}" manually, then press Enter.`);
                waitPrompt('  ▶  Press Enter to continue... ');
                await waitForKey();
              }
              return;
            }

            // UI path — navigate to ManageFeatures.aspx and click the Activate button.
            // ManageFeatures.aspx uses <input type="button" value="Activate"> (ASP.NET postback),
            // so we find the element via DOM and trigger a proper Playwright click on it.
            const webUrl = await activePage.evaluate(() =>
              window._spPageContextInfo?.webAbsoluteUrl
            ).catch(() => null) ?? (() => {
              const u = new URL(currentUrl);
              const m = u.pathname.match(/^\/(sites|teams)\/[^/]+/);
              return `${u.origin}${m ? m[0] : ''}`;
            })();
            const featuresUrl = `${webUrl.replace(/\/$/, '')}/_layouts/15/ManageFeatures.aspx?Scope=Site`;

            await activePage.goto(featuresUrl, { waitUntil: 'load', timeout: 60000 });
            await activePage.waitForTimeout(2000);

            // Check feature state by inspecting button values (not textContent — inputs use .value).
            const featureState = await activePage.evaluate((name) => {
              const rows = Array.from(document.querySelectorAll('tr'));
              for (const row of rows) {
                if (!row.textContent.includes(name)) continue;
                const btns = Array.from(row.querySelectorAll('a, button, input[type="button"]'));
                const label = el => (el.value || el.textContent || '').trim();
                const hasDeactivate = btns.some(el => /deactivate/i.test(label(el)));
                const activateEl = btns.find(el => /^activate$/i.test(label(el)));
                return { found: true, active: hasDeactivate, hasActivate: !!activateEl };
              }
              return { found: false };
            }, featureName);

            if (!featureState.found) {
              console.log('not found on features page.');
              waitPrompt(`  ▶  Activate "${featureName}" manually, then press Enter... `);
              await waitForKey();
            } else if (featureState.active) {
              console.log('already active.');
            } else if (!featureState.hasActivate) {
              console.log('no Activate button found.');
              waitPrompt(`  ▶  Activate "${featureName}" manually, then press Enter... `);
              await waitForKey();
            } else {
              console.log('activating...');
              process.stdout.write(`    Activating "${featureName}"... `);
              // Use Playwright locator to click the input button properly (triggers postback).
              const activateBtn = activePage.locator('tr')
                .filter({ hasText: featureName })
                .locator('input[type="button"]')
                .filter({ hasAttribute: 'value' })
                .first();
              await activateBtn.click({ timeout: 10000 });
              await activePage.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
              await activePage.waitForTimeout(2000);
              console.log('done.');
            }

            await activePage.goto(currentUrl, { waitUntil: 'load', timeout: 60000 });
            await activePage.waitForTimeout(2000);
          },
        };
      }

      default:
        return {
          name: `[unknown command: ${cmd}]`,
          async run() {
            printContext();
            console.warn(`    Unknown command "${cmd}" — skipping.`);
          },
        };
    }
  };

  for (const block of sectionBlocks) {
    if (block.type === 'command') {
      const ctx = flushContext();
      const step = commandToStep(block.cmd, block.arg, ctx);
      if (step) {
        step.context = ctx.filter(b => b.type === 'talking' || b.type === 'comment').map(b => b.value).join('\n\n');
      }
      steps.push(step);
    } else {
      pendingContext.push(block);
    }
  }

  // Any trailing talking points with no command → implicit pause
  if (pendingContext.length) {
    const ctx = flushContext();
    const step = commandToStep('pause', '', ctx);
    if (step) {
      step.context = ctx.filter(b => b.type === 'talking' || b.type === 'comment').map(b => b.value).join('\n\n');
    }
    steps.push(step);
  }

  return { steps, getActivePage: () => activePage };
}

// ─── Step runner ─────────────────────────────────────────────────────────────

// Return the index to assign to i so that after the for-loop's i++ the runner
// lands on the nearest pause step before the current one.  If there is no
// earlier pause, returns -1 so that i++ brings us back to step 0.
function prevPauseIndex(steps, currentIndex) {
  let j = currentIndex - 1;
  while (j > 0 && !steps[j].isPause) j--;
  return Math.max(-1, j - 1); // after i++ this becomes j (or 0 if j was 0)
}

async function runSteps(getPage, steps) {
  const startTime = Date.now();
  widgetUpdate({ startTime, steps: steps.map(s => ({ name: s.name, pause: !!s.isPause })) });

  console.log('\nSteps:');
  const maxWidth = (process.stdout.columns || 80) - 6;
  steps.forEach((s, i) => {
    const name = s.name.length > maxWidth ? s.name.slice(0, maxWidth - 1) + '…' : s.name;
    console.log(`  ${i + 1}. ${name}`);
  });
  console.log('');

  if (RECORD_MODE) console.log('  \x1B[33m⏺  RECORD MODE — pauses auto-advance\x1B[0m\n');

  // Set up recording directory and frames folder up front
  let recordDir;
  if (RECORD_MODE) {
    recordDir = join(_scriptDir, '..', 'recordings', _scenarioKey);
    mkdirSync(join(recordDir, 'frames'), { recursive: true });
  }

  const recordedSteps = [];

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const elapsed = formatElapsed(Date.now() - startTime);
    console.log(`\x1B[2m[${elapsed}]\x1B[0m \x1B[1mStep ${i + 1}/${steps.length}:\x1B[0m ${step.name}`);

    const stepStartMs = Date.now() - startTime;

    try {
      await getPage().bringToFront().catch(() => {});
      widgetUpdate({ step: i + 1, total: steps.length, name: step.name, context: '', waiting: false });
      const nav = await step.run();

      if (RECORD_MODE) {
        const frameNum = String(i + 1).padStart(3, '0');
        const screenshotFilename = `frames/step-${frameNum}.png`;
        await getPage().screenshot({ path: join(recordDir, screenshotFilename) }).catch(() => {});

        const endMs = Date.now() - startTime;
        recordedSteps.push({
          name: step.name,
          talkingPoints: step.context || '',
          isPause: !!step.isPause,
          startMs: stepStartMs,
          endMs,
          durationMs: endMs - stepStartMs,
          // Pause steps auto-advance instantly — give them a display duration for the slideshow
          ...(step.isPause && { displayDurationMs: 5000 }),
          // Path relative to Remotion's public/ root
          screenshot: `recordings/${_scenarioKey}/${screenshotFilename}`,
        });
      }

      if (nav === 'back') { i = prevPauseIndex(steps, i); continue; }
      if (nav === 'skip') continue;
      if (nav && nav.startsWith('g') && /^\d+$/.test(nav.slice(1))) {
        i = Math.min(parseInt(nav.slice(1), 10) - 2, steps.length - 1); // -2: 1-indexed + loop i++
        continue;
      }
      if (_widgetPauseRequested) {
        _widgetPauseRequested = false;
        widgetUpdate({ pauseRequested: false });
        waitPrompt('  \u23f8  Widget pause \u2014 press Enter to continue... ');
        const pk = await waitForKey();
        console.log('');
        if (pk === 'b') { i = prevPauseIndex(steps, i); continue; }
        if (pk === 's') continue;
        if (pk && pk.startsWith('g') && /^\d+$/.test(pk.slice(1))) {
          i = Math.min(parseInt(pk.slice(1), 10) - 2, steps.length - 1);
          continue;
        }
      }
    } catch (err) {
      _widgetPauseRequested = false;
      widgetUpdate({ pauseRequested: false });
      console.error(`\n  Error in step ${i + 1}: ${err.message}`);
      await getPage().screenshot({ path: 'tools/debug-screenshot.png' }).catch(() => {});
      console.error('  Debug screenshot saved to tools/debug-screenshot.png');
      waitPrompt('  ▶  Press Enter to continue to the next step, or Ctrl+C to quit... ');
      await waitForKey();
      console.log('');
    }
  }

  const totalTime = formatElapsed(Date.now() - startTime);
  console.log(`\nDemo complete in ${totalTime}.`);

  if (RECORD_MODE && recordedSteps.length) {
    const eventsPath = join(recordDir, 'events.json');
    writeFileSync(eventsPath, JSON.stringify({
      demoName: _scenarioKey,
      recordedAt: new Date().toISOString(),
      // videoOffsetMs: how far into the OBS recording the demo steps begin.
      // Used by DemoVideo in Remotion to sync overlays to the video.
      ...(_obsRecordingStartMs && { videoOffsetMs: startTime - _obsRecordingStartMs }),
      steps: recordedSteps,
    }, null, 2));
    console.log(`\n  \x1B[32m✓\x1B[0m  Events saved → ${eventsPath}`);
    console.log(`       Copy to C:\\repos\\remotion\\public\\recordings\\ then run: npm run studio`);
  }
}


// ─── Terminal input ───────────────────────────────────────────────────────────

// In TTY mode: raw single-keypress.
// In piped mode (e.g. tests): buffer lines and dequeue one at a time.
const _keyQueue = [];
let _keyQueueReady = null;
let _stdinEOF = false;

if (!process.stdin.isTTY) {
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => {
    for (const ch of chunk) {
      const key = ch === '\r' || ch === '\n' || ch === ' ' ? 'enter' : ch.toLowerCase();
      _keyQueue.push(key);
    }
    if (_keyQueueReady) { _keyQueueReady(); _keyQueueReady = null; }
  });
  // EOF on piped stdin — wake any pending waitForKey so it can return 'enter'
  process.stdin.on('end', () => {
    _stdinEOF = true;
    if (_keyQueueReady) { _keyQueueReady(); _keyQueueReady = null; }
  });
  process.stdin.resume();
}

async function waitForKey() {
  if (RECORD_MODE) return 'enter';
  widgetUpdate({ waiting: true });

  let key;
  if (!process.stdin.isTTY) {
    // Drain one key from the queue; wait if empty (or return 'enter' on EOF)
    while (_keyQueue.length === 0 && !_stdinEOF) {
      await new Promise(r => { _keyQueueReady = r; });
    }
    key = _keyQueue.length > 0 ? _keyQueue.shift() : 'enter';
    if (key === '\x03') process.exit(0);
  } else {
    key = await new Promise(resolve => {
      // Also drain any widget-queued key that arrived while stdin was passive
      if (_keyQueue.length > 0) {
        const queued = _keyQueue.shift();
        if (queued === '\x03') process.exit(0);
        return resolve(queued);
      }
      process.stdin.setRawMode(true);
      process.stdin.resume();
      const onData = buf => {
        const raw = buf.toString();
        if (raw === '\x03') process.exit(0);
        const ch = raw === '\r' || raw === '\n' || raw === ' ' ? 'enter' : raw[0].toLowerCase();
        // Goto mode: 'g' followed by digits then Enter
        if (ch === 'g') {
          _keyQueue.length = 0;
          process.stdin.off('data', onData);
          process.stdout.write('g');
          let digits = '';
          const onDigit = buf2 => {
            const r = buf2.toString();
            if (r === '\x03') process.exit(0);
            if (r === '\r' || r === '\n') {
              process.stdin.setRawMode(false);
              process.stdin.pause();
              process.stdin.off('data', onDigit);
              process.stdout.write('\n');
              resolve(digits ? 'g' + digits : 'enter');
            } else if (r >= '0' && r <= '9') {
              digits += r;
              process.stdout.write(r);
            } else {
              // non-digit cancels goto — treat as that key
              process.stdin.setRawMode(false);
              process.stdin.pause();
              process.stdin.off('data', onDigit);
              resolve(r.toLowerCase());
            }
          };
          process.stdin.on('data', onDigit);
          return;
        }
        // A widget click may have also arrived via _keyQueue — prefer stdin
        _keyQueue.length = 0;
        process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdin.off('data', onData);
        resolve(ch);
      };
      process.stdin.on('data', onData);
      // Wake up if widget sends a key while stdin is listening
      const prevReady = _keyQueueReady;
      _keyQueueReady = () => {
        if (prevReady) prevReady();
        if (_keyQueue.length > 0) {
          const wk = _keyQueue.shift();
          process.stdin.setRawMode(false);
          process.stdin.pause();
          process.stdin.off('data', onData);
          resolve(wk === '\x03' ? (process.exit(0), 'enter') : wk);
        }
      };
    });
  }

  widgetUpdate({ waiting: false });
  return key;
}

function waitPrompt(msg) {
  process.stdout.write(`\x1B[1;33m${msg}\x1B[0m`);
}

function formatElapsed(ms) {
  const s = Math.floor(ms / 1000);
  const m = Math.floor(s / 60);
  return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}

// ─── Browser helpers ──────────────────────────────────────────────────────────

/**
 * Click Chat options → New chat to clear the active Copilot conversation.
 */
async function startNewChat(page, chatFrame) {
  await chatFrame.locator('[aria-label="Chat options"]').click();
  await page.waitForTimeout(400);
  const newChatItem = chatFrame.locator('[role="menuitem"]:has-text("New chat"), [aria-label="New chat"]').first();
  const isDisabled = await newChatItem.getAttribute('aria-disabled').catch(() => null);
  if (isDisabled === 'true') {
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    console.log('    Already in a new chat — skipping.');
    return;
  }
  await newChatItem.click();
  await page.waitForTimeout(1500);
  console.log('    New chat started.');
}

/**
 * Click the FAB and navigate through the popup to open the full chat pane.
 */
async function openChatPane(page) {
  // Check if the pane is already open — fast path.
  if (await page.locator('[data-automationid="ChatODSPFrame"]').isVisible({ timeout: 1000 }).catch(() => false)) return;

  // Dismiss any overlay panel (Tips and Tricks, What's New, etc.) that may be
  // intercepting pointer events and blocking the suite-bar FAB click.
  const overlayPanel = page.locator('.ms-tipsntricks-panel, [class*="tipsntricks"], .ms-Panel.is-open:not([data-automationid="ChatODSPFrame"])').first();
  if (await overlayPanel.isVisible({ timeout: 1500 }).catch(() => false)) {
    const closeBtn = overlayPanel.locator('button[aria-label="Close"], .ms-Panel-closeButton, button.ms-Dialog-button--close').first();
    if (await closeBtn.isVisible({ timeout: 1000 }).catch(() => false)) {
      await closeBtn.click();
    } else {
      await page.keyboard.press('Escape');
    }
    await page.waitForTimeout(400);
  }

  // "Open Agents" is a suite-bar button present when the pane is closed on some tenants.
  // Clicking it opens the pane directly (no popup). Try this first with a generous timeout
  // to handle slow page loads where the suite bar renders after a brief delay.
  // Use an exact-length check: ignore "Open Agents. Press tab to enter expanded region."
  // variants that open an agents marketplace panel instead of the chat pane.
  const openAgentsBtn = page.locator('[aria-label="Open Agents"]:not([aria-label*="."])').first();
  if (await openAgentsBtn.isVisible({ timeout: 10000 }).catch(() => false)) {
    console.log('    Trying "Open Agents" button...');
    await openAgentsBtn.click();
    const paneViaAgents = await page.locator('[data-automationid="ChatODSPFrame"]').isVisible({ timeout: 8000 }).catch(() => false);
    if (paneViaAgents) { console.log('    Opened via "Open Agents".'); return; }
    // Did not open ChatODSPFrame — dismiss whatever it opened before trying the FAB.
    console.log('    "Open Agents" did not open chat pane — dismissing and falling through to FAB.');
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
  }

  // Fallback: try FAB selectors (present when pane is open, opens a popup with "Open chat").
  const fabSelectors = [
    '[aria-label*="alt plus i"]',
    'button.spui-FloatingActionButton',
    'button[class*="FloatingActionButton"]',
    'button[class*="fabButton"]',
    '[data-automationid="CopilotFAB"]',
    '[aria-label*="Copilot"]',
  ];

  let fab = null;
  for (const sel of fabSelectors) {
    fab = page.locator(sel).first();
    if (await fab.isVisible({ timeout: 3000 }).catch(() => false)) break;
    fab = null;
  }

  if (!fab) {
    await page.screenshot({ path: 'tools/debug-screenshot.png' });
    throw new Error('Could not locate the Copilot FAB. Debug screenshot saved.');
  }

  await fab.click();

  // Wait for either the popup menu OR the pane to appear — whichever comes first.
  // A fixed 1 s sleep was unreliable: isVisible() doesn't retry, so if the popup
  // appears after the sleep all four selector checks instantly return false.
  const _fabResult = await Promise.race([
    page.locator('[role="menu"]').waitFor({ state: 'visible', timeout: 8000 }).then(() => 'menu').catch(() => null),
    page.locator('[data-automationid="ChatODSPFrame"]').waitFor({ state: 'visible', timeout: 8000 }).then(() => 'pane').catch(() => null),
  ]);
  if (_fabResult === 'pane') return; // FAB opened the pane directly — done.

  const openChatSelectors = [
    '[role="menuitem"]:has-text("Open chat")',
    'div.fui-MenuItem:has-text("Open chat")',
    '[aria-label="Open chat"]',
    '[data-automationid*="OpenChat"]',
  ];

  let openChatBtn = null;
  for (const sel of openChatSelectors) {
    openChatBtn = page.locator(sel).first();
    if (await openChatBtn.isVisible().catch(() => false)) break;
    openChatBtn = null;
  }

  if (!openChatBtn) {
    // "Close chat" in the popup means the pane is already open — dismiss and return.
    const closeChatSelectors = [
      '[role="menuitem"]:has-text("Close chat")',
      'div.fui-MenuItem:has-text("Close chat")',
      '[aria-label="Close chat"]',
    ];
    for (const sel of closeChatSelectors) {
      if (await page.locator(sel).first().isVisible({ timeout: 1000 }).catch(() => false)) {
        await page.keyboard.press('Escape');
        await page.waitForTimeout(300);
        return; // pane is already open
      }
    }
    // Neither "Open chat" nor "Close chat" found — the FAB click may have opened the pane
    // directly (no popup). Wait properly (not instant isVisible) before pressing Escape,
    // since Escape would close a still-loading pane.
    const paneVisibleDirect = await page.locator('[data-automationid="ChatODSPFrame"]').waitFor({ state: 'visible', timeout: 15000 }).then(() => true).catch(() => false);
    if (paneVisibleDirect) return;
    // Pane did not appear — now safe to dismiss any stray overlay and try once more.
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
    const paneVisible = await page.locator('[data-automationid="ChatODSPFrame"]').waitFor({ state: 'visible', timeout: 8000 }).then(() => true).catch(() => false);
    if (paneVisible) return;
    await page.screenshot({ path: 'tools/debug-screenshot.png' });
    throw new Error('Could not find "Open chat" in the FAB popup. Debug screenshot saved.');
  }

  await openChatBtn.click();
  await page.waitForSelector('[data-automationid="ChatODSPFrame"]', { state: 'visible', timeout: 15000 });
  await page.waitForTimeout(2000);
}

/**
 * Locate the chat text input inside the Copilot iframe.
 */
async function getChatInput(page, chatFrame) {
  const selectors = [
    '[placeholder*="Ask"]',
    '[placeholder*="Message"]',
    'textarea',
    '[contenteditable="true"]',
    '[role="textbox"]',
  ];

  // Try fast first, then one longer retry to handle post-response loading states.
  for (const pass of [3000, 10000]) {
    for (const sel of selectors) {
      const loc = chatFrame.locator(sel).first();
      if (await loc.isVisible({ timeout: pass }).catch(() => false)) return loc;
    }
  }

  await page.screenshot({ path: 'tools/debug-screenshot.png' });
  throw new Error('Chat input not found. Debug screenshot saved.');
}

/**
 * Type text in chunks so the audience can read it as it appears.
 */
async function slowType(locator, text, chunkSize = TYPE_CHUNK, delayMs = TYPE_DELAY) {
  await locator.click();
  await locator.fill('');
  for (let i = 0; i < text.length; i += chunkSize) {
    await locator.fill(text.slice(0, i + chunkSize));
    await locator.page().waitForTimeout(delayMs);
  }
}

/**
 * Wait for Copilot to finish generating a response.
 *
 * Strategy:
 *   1. Wait for "Stop generating" button to appear (generation started).
 *   2. Wait for it to disappear (generation ended).
 *   3. Fallback: poll for new Like/Dislike feedback buttons on the last message.
 */
async function waitForCopilotResponse(page, chatFrame, timeoutMs = 300000, signal = null) {
  const aborted = () => signal?.aborted ?? false;
  const deadline = Date.now() + timeoutMs;

  // If the input still has text, the prompt wasn't submitted — press Enter to re-submit.
  try {
    const inputSelectors = [
      '[placeholder*="Ask"]',
      '[placeholder*="Message"]',
      'textarea',
      '[contenteditable="true"]',
      '[role="textbox"]',
    ];
    for (const sel of inputSelectors) {
      const loc = chatFrame.locator(sel).first();
      if (await loc.isVisible({ timeout: 500 }).catch(() => false)) {
        const val = await loc.inputValue().catch(() => null) ?? await loc.textContent().catch(() => '');
        if (val && val.trim().length > 0) {
          console.log('\n    Input still has text — re-submitting...');
          await loc.press('Enter');
          await page.waitForTimeout(500);
        }
        break;
      }
    }
  } catch { /* best-effort */ }

  const stopSelectors = [
    '[aria-label*="Stop"]',
    'button:has-text("Stop")',
    '[aria-label*="stop generating"]',
  ];

  const DOT_INTERVAL = 15000; // print a dot at most once every 15 seconds

  process.stdout.write('    Waiting for generation to start');
  let stopBtn = null;
  const startDeadline = Date.now() + 10000;
  let lastDot = Date.now();
  outer: while (Date.now() < startDeadline) {
    if (aborted()) return;
    for (const sel of stopSelectors) {
      const loc = chatFrame.locator(sel).first();
      if (await loc.isVisible({ timeout: 500 }).catch(() => false)) {
        stopBtn = loc;
        break outer;
      }
    }
    if (Date.now() - lastDot >= DOT_INTERVAL) { process.stdout.write('.'); lastDot = Date.now(); }
    await page.waitForTimeout(300);
  }

  if (stopBtn) {
    process.stdout.write(' started.\n    Waiting for generation to finish');
    lastDot = Date.now();
    while (Date.now() < deadline) {
      if (aborted()) return;
      if (!await stopBtn.isVisible({ timeout: 500 }).catch(() => false)) {
        console.log(' done.');
        return;
      }
      if (Date.now() - lastDot >= DOT_INTERVAL) { process.stdout.write('.'); lastDot = Date.now(); }
      await page.waitForTimeout(500);
    }
    console.log('');
    waitPrompt('    ▶  Press Enter when the AI has finished to continue... ');
    await waitForKey();
    console.log('');
    return;
  }

  // Fallback
  console.log('\n    Stop button not seen — polling for feedback buttons...');
  const feedbackSel = '[aria-label="Like"], [aria-label="Dislike"]';
  const initialCount = await chatFrame.locator(feedbackSel).count().catch(() => 0);
  lastDot = Date.now();

  while (Date.now() < deadline) {
    if (aborted()) return;
    const count = await chatFrame.locator(feedbackSel).count().catch(() => 0);
    if (count > initialCount) {
      console.log('    Generation complete (feedback buttons appeared).');
      return;
    }
    if (Date.now() - lastDot >= DOT_INTERVAL) { process.stdout.write('.'); lastDot = Date.now(); }
    await page.waitForTimeout(500);
  }

  process.stdout.write('    Timed out — press Enter when the AI has finished to continue... ');
  await waitForKey();
  console.log('');
}

/**
 * Pause and prompt the operator to perform a manual step before continuing.
 * Mark the call site with: // [COMMAND]: <instruction>
 */
async function pause(message) {  // eslint-disable-line no-unused-vars
  console.log(`\n  [PAUSED] ${message}`);
  waitPrompt('  ▶  Press Enter to continue... ');
  await waitForKey();
  console.log('  Resuming.\n');
}

// ─── Run ──────────────────────────────────────────────────────────────────────

main().catch(err => {
  console.error('\nDemo runner error:', err.message);
  process.exit(1);
});
