import { spawn } from 'child_process';
import path from 'path';

const SPEEDS = { slow: 80, normal: 35, fast: 8 };

const BUTTON_ID = '__demo_next__';

const DEFAULT_SELECTORS = [
  '[data-testid="chat-input"]',
  '[data-automationid="chat-input"]',
  'textarea[placeholder*="Ask"]',
  'textarea[placeholder*="Message"]',
  'div[contenteditable="true"][aria-label*="Ask"]',
  'div[contenteditable="true"][aria-label*="Message"]',
  'div[contenteditable="true"]',
];

// Injected into the live Chrome tab when paused. JSON.stringify() embeds it
// safely — no escaping issues regardless of what the string contains.
const PAUSE_BUTTON_JS = `
  (() => {
    if (document.getElementById('${BUTTON_ID}')) return;
    const btn = document.createElement('button');
    btn.id = '${BUTTON_ID}';
    btn.textContent = '▶  Next';
    btn.style.cssText = [
      'position:fixed', 'bottom:28px', 'right:28px', 'z-index:2147483647',
      'padding:12px 24px', 'font-size:15px',
      'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif',
      'font-weight:600', 'color:#fff', 'background:#0f7b0f',
      'border:none', 'border-radius:8px',
      'box-shadow:0 4px 16px rgba(0,0,0,0.3)',
      'cursor:pointer', 'transition:background 0.15s',
    ].join(';');
    btn.onmouseenter = () => btn.style.background = '#0a5c0a';
    btn.onmouseleave = () => btn.style.background = '#0f7b0f';
    document.body.appendChild(btn);
  })();
`;

const REMOVE_BUTTON_JS = `
  (() => { const el = document.getElementById('${BUTTON_ID}'); if (el) el.remove(); })();
`;

function runPlaywriter(args) {
  return new Promise((resolve, reject) => {
    const proc = spawn('playwriter', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', (d) => (stdout += d));
    proc.stderr.on('data', (d) => (stderr += d));
    proc.on('close', (code) => {
      if (code !== 0) reject(new Error(`playwriter exited ${code}\n${stderr}`));
      else resolve({ stdout: stdout.trim(), stderr: stderr.trim() });
    });
    proc.on('error', (err) => {
      if (err.code === 'ENOENT')
        reject(new Error('playwriter not found — install it: npm install -g playwriter'));
      else reject(err);
    });
  });
}

export class Player {
  constructor(options = {}) {
    this.sessionId = options.sessionId;
    this.speed = options.speed || 'normal';
    this.customSelector = options.selector || '';
    this.screenshotsDir = options.screenshots || './screenshots';
    this._screenshotCount = 0;
    this._cachedSelector = null;
  }

  static async create(options = {}) {
    console.log('[player] Starting Playwriter session…');
    const { stdout } = await runPlaywriter(['session', 'new']);
    const idMatch = stdout.match(/\d+/);
    if (!idMatch) throw new Error(`Unexpected session output: ${stdout}`);
    const sessionId = idMatch[0];
    console.log(`[player] Session ${sessionId} ready`);
    return new Player({ ...options, sessionId });
  }

  async execute(code) {
    const { stdout } = await runPlaywriter(['-s', this.sessionId, '-e', code]);
    return stdout;
  }

  async navigate(url) {
    console.log(`[player] → ${url}`);
    // Clear cached selector — new page may have different DOM
    this._cachedSelector = null;
    await this.execute(`await page.goto(${JSON.stringify(url)}, { waitUntil: 'domcontentloaded' })`);
  }

  async typeInAI(text) {
    const delay = SPEEDS[this.speed] ?? SPEEDS.normal;

    // Discover and cache the AI input selector once per page.
    if (!this._cachedSelector) {
      const selectors = this.customSelector ? [this.customSelector] : DEFAULT_SELECTORS;
      const found = await this.execute(`
        for (const sel of ${JSON.stringify(selectors)}) {
          try {
            if (await page.locator(sel).first().isVisible({ timeout: 1500 })) {
              console.log(sel);
              break;
            }
          } catch (_) {}
        }
      `);
      if (!found) throw new Error(
        'Could not find SharePoint AI input box. Set selector: in your script frontmatter.'
      );
      this._cachedSelector = found;
    }

    await this.execute(`
      await page.locator(${JSON.stringify(this._cachedSelector)}).first().click();
      await page.keyboard.type(${JSON.stringify(text)}, { delay: ${delay} });
      await page.keyboard.press('Enter');
    `);
  }

  async pause() {
    process.stdout.write('[player] Paused — click ▶ Next in the browser to continue…');

    // Single round-trip: inject button, wait for click, remove it.
    await this.execute(`
      await page.evaluate(${JSON.stringify(PAUSE_BUTTON_JS)});
      await page.locator(${JSON.stringify('#' + BUTTON_ID)}).click({ timeout: 0 });
      await page.evaluate(${JSON.stringify(REMOVE_BUTTON_JS)});
    `);

    process.stdout.write(' ✓\n');
  }

  async wait(ms) {
    console.log(`[player] Waiting ${ms}ms…`);
    await this.execute(`await page.waitForTimeout(${ms})`);
  }

  async screenshot(caption) {
    this._screenshotCount += 1;
    const slug = caption
      ? caption.toLowerCase().replace(/[^a-z0-9]+/g, '-')
      : `step-${this._screenshotCount}`;
    const filename = `${String(this._screenshotCount).padStart(2, '0')}-${slug}.png`;
    const filepath = path.join(this.screenshotsDir, filename);

    await this.execute(`
      const fs = require('fs');
      fs.mkdirSync(${JSON.stringify(this.screenshotsDir)}, { recursive: true });
      await page.screenshot({ path: ${JSON.stringify(filepath)} });
    `);
    console.log(`[player] Screenshot saved: ${filepath}`);
  }

  setSpeed(value) {
    if (!SPEEDS[value]) {
      console.warn(`[player] Unknown speed "${value}", ignoring`);
      return;
    }
    this.speed = value;
    console.log(`[player] Speed → ${value}`);
  }
}
