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
 *   node tools/run-demo.mjs [scenario]
 *   node tools/run-demo.mjs tell-me-about-site
 *
 * Step controls (press before each step runs):
 *   Enter   run the current step
 *   s       skip this step
 *   b       go back and re-run the previous step
 *   ?       show help
 *   Ctrl+C  quit
 */

import { chromium } from 'playwright';
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';

const CDP_URL = process.env.CDP_URL ?? 'http://localhost:9222';
const args = process.argv.slice(2);
const SCENARIO = args.find(a => !a.startsWith('--')) ?? 'tell-me-about-site';
const RUN_SECTION = args.includes('--setup') ? 'setup' : args.includes('--reset') ? 'reset' : 'demo';

// ─── Scenarios ───────────────────────────────────────────────────────────────

const scenarios = {
  'tell-me-about-site': tellMeAboutSiteSteps,
};

// ─── Entry point ─────────────────────────────────────────────────────────────

async function main() {
  console.log(`Connecting to Edge at ${CDP_URL}...`);
  const browser = await chromium.connectOverCDP(CDP_URL);

  const contexts = browser.contexts();
  const context = contexts[0] ?? await browser.newContext();
  const pages = context.pages();
  const page = pages[0] ?? await context.newPage();

  let steps;
  let getActivePage = () => page;

  // If the argument is a .demo script file, parse it; otherwise use a named scenario.
  if (SCENARIO.endsWith('.demo')) {
    const scriptPath = resolve(SCENARIO);
    const src = readFileSync(scriptPath, 'utf8');
    const parsed = parseScript(src, page, RUN_SECTION);
    steps = parsed.steps;
    getActivePage = parsed.getActivePage;
    if (!steps.length) {
      console.error(`No steps found for section "${RUN_SECTION}" in ${scriptPath}.`);
      console.error('Add a [section: setup], [section: demo], or [section: reset] marker to the script.');
      process.exit(1);
    }
    if (RUN_SECTION !== 'demo') {
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

  await runSteps(getActivePage, steps);
  await browser.close();
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
 */
function parseScript(src, page, section = 'demo') {
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
  const vars = {};
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
            vars[name] = value;
          }
        }
      }
    }
  }

  // Substitute ${VAR} in a string using the collected vars map.
  const interpolate = str => str.replace(/\$\{([^}]+)\}/g, (_, name) => vars[name] ?? `\${${name}}`);

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

  // Filter to the requested section
  const sectionBlocks = blocks.filter(b => b.section === section);

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
            if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
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
            await waitForCopilotResponse(activePage, chatFrame);
          },
        };

      case 'pause':
        return {
          name: arg || 'Pause — presenter moment',
          async run() {
            printContext();
            waitPrompt('  ▶  Press Enter to continue... ');
            await waitForKey();
            console.log('');
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
            await waitForKey();
            console.log('  Confirmed.\n');
          },
        };
      }

      case 'new-chat':
        return {
          name: 'New chat (clear Copilot conversation)',
          async run() {
            printContext();
            if (!chatFrame) {
              const iframe = activePage.locator('[data-automationid="ChatODSPFrame"]');
              if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
                throw new Error('[new-chat] requires the chat pane to be open first.');
              }
              chatFrame = activePage.frameLocator('[data-automationid="ChatODSPFrame"]');
            }
            await startNewChat(activePage, chatFrame);
          },
        };

      case 'upload': {
        const uploadPath = resolve(arg);
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
            await waitForKey();
            console.log('  File attached.\n');
          },
        };
      }

      case 'screenshot': {
        const screenshotPath = arg || 'tools/screenshots/demo.png';
        return {
          name: `Screenshot → ${screenshotPath}`,
          async run() {
            printContext();
            mkdirSync(dirname(resolve(screenshotPath)), { recursive: true });
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
            process.stdout.write(`    Checking ${assertUrl} ... `);
            // Use a temporary page so we don't navigate away from the active tab
            const checkPage = await activePage.context().newPage();
            let passed = false;
            try {
              const response = await checkPage.goto(assertUrl, { waitUntil: 'load', timeout: 20000 }).catch(() => null);
              passed = !!(response && response.status() < 400);
            } finally {
              await checkPage.close().catch(() => {});
            }
            if (passed) {
              console.log('OK');
            } else {
              console.log('');
              console.log('  ┌─────────────────────────────────────────────────────────┐');
              console.log('  │  ASSERTION FAILED — resource may be missing             │');
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
      steps.push(commandToStep(block.cmd, block.arg, flushContext()));
    } else {
      pendingContext.push(block);
    }
  }

  // Any trailing talking points with no command → implicit pause
  if (pendingContext.length) {
    steps.push(commandToStep('pause', '', flushContext()));
  }

  return { steps, getActivePage: () => activePage };
}

// ─── Step runner ─────────────────────────────────────────────────────────────

async function runSteps(getPage, steps) {
  const startTime = Date.now();

  console.log('\nSteps:');
  const maxWidth = (process.stdout.columns || 80) - 6;
  steps.forEach((s, i) => {
    const name = s.name.length > maxWidth ? s.name.slice(0, maxWidth - 1) + '…' : s.name;
    console.log(`  ${i + 1}. ${name}`);
  });
  console.log('');

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const elapsed = formatElapsed(Date.now() - startTime);
    console.log(`\x1B[2m[${elapsed}]\x1B[0m \x1B[1mStep ${i + 1}/${steps.length}:\x1B[0m ${step.name}`);

    try {
      await getPage().bringToFront().catch(() => {});
      await step.run();
    } catch (err) {
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
}


// ─── Terminal input ───────────────────────────────────────────────────────────

// In TTY mode: raw single-keypress.
// In piped mode (e.g. tests): buffer lines and dequeue one at a time.
const _keyQueue = [];
let _keyQueueReady = null;

if (!process.stdin.isTTY) {
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => {
    for (const ch of chunk) {
      const key = ch === '\r' || ch === '\n' || ch === ' ' ? 'enter' : ch.toLowerCase();
      _keyQueue.push(key);
    }
    if (_keyQueueReady) { _keyQueueReady(); _keyQueueReady = null; }
  });
  process.stdin.resume();
}

async function waitForKey() {
  if (!process.stdin.isTTY) {
    // Drain one key from the queue; wait if empty
    while (_keyQueue.length === 0) {
      await new Promise(r => { _keyQueueReady = r; });
    }
    const key = _keyQueue.shift();
    if (key === '\x03') process.exit(0);
    return key;
  }

  return new Promise(resolve => {
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.once('data', buf => {
      process.stdin.setRawMode(false);
      process.stdin.pause();
      const key = buf.toString();
      if (key === '\x03') process.exit(0);
      const k = key === '\r' || key === '\n' || key === ' ' ? 'enter' : key[0].toLowerCase();
      resolve(k);
    });
  });
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
  await page.waitForTimeout(1000);

  const openChatSelectors = [
    '[role="menuitem"]:has-text("Open chat")',
    'div.fui-MenuItem:has-text("Open chat")',
    '[aria-label="Open chat"]',
    '[data-automationid*="OpenChat"]',
  ];

  let openChatBtn = null;
  for (const sel of openChatSelectors) {
    openChatBtn = page.locator(sel).first();
    if (await openChatBtn.isVisible({ timeout: 3000 }).catch(() => false)) break;
    openChatBtn = null;
  }

  if (!openChatBtn) {
    // Pane may already be open — dismiss popup and check
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
    const paneVisible = await page.locator('[data-automationid="ChatODSPFrame"]').isVisible({ timeout: 3000 }).catch(() => false);
    if (paneVisible) return; // already open, we're good
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

  for (const sel of selectors) {
    const loc = chatFrame.locator(sel).first();
    if (await loc.isVisible({ timeout: 5000 }).catch(() => false)) return loc;
  }

  await page.screenshot({ path: 'tools/debug-screenshot.png' });
  throw new Error('Chat input not found. Debug screenshot saved.');
}

/**
 * Type text character-by-character so the audience can read it as it appears.
 */
async function slowType(locator, text, delayMs = 10) {
  await locator.click();
  await locator.fill('');
  for (const char of text) {
    await locator.type(char, { delay: 0 });
    await new Promise(r => setTimeout(r, delayMs));
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
async function waitForCopilotResponse(page, chatFrame, timeoutMs = 180000) {
  const deadline = Date.now() + timeoutMs;

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
