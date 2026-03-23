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

  // If the argument is a .demo script file, parse it; otherwise use a named scenario.
  if (SCENARIO.endsWith('.demo')) {
    const scriptPath = resolve(SCENARIO);
    const src = readFileSync(scriptPath, 'utf8');
    steps = parseScript(src, page, RUN_SECTION);
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

  await runSteps(page, steps);
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
 *   [navigate: URL]           navigate to a URL
 *   [open-chat]               open the Copilot chat pane via FAB
 *   [prompt: text]            slow-type text into chat and submit
 *   [wait]                    wait for Copilot to finish responding
 *   [pause]                   wait for presenter to press Enter
 *   [confirm: message]        destructive action — warn presenter and wait for
 *                             confirmation that they've clicked the button in the UI
 *   [screenshot: path]        save a screenshot
 */
function parseScript(src, page, section = 'demo') {
  const lines = src.split('\n');
  const blocks = []; // { type: 'comment'|'talking'|'command'|'section', value, raw }

  let currentSection = 'demo'; // default section if no markers present

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (trimmed.startsWith('#')) {
      blocks.push({ type: 'comment', value: trimmed.replace(/^#+\s*/, ''), section: currentSection });
    } else if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
      const inner = trimmed.slice(1, -1);
      const colonIdx = inner.indexOf(':');
      const cmd = colonIdx === -1 ? inner.trim() : inner.slice(0, colonIdx).trim();
      const arg = colonIdx === -1 ? '' : inner.slice(colonIdx + 1).trim();

      if (cmd === 'section') {
        currentSection = arg.toLowerCase();
      } else {
        blocks.push({ type: 'command', cmd, arg, section: currentSection });
      }
    } else {
      // Merge consecutive talking-point lines into the previous talking block
      if (blocks.length && blocks[blocks.length - 1].type === 'talking' && blocks[blocks.length - 1].section === currentSection) {
        blocks[blocks.length - 1].value += ' ' + trimmed;
      } else {
        blocks.push({ type: 'talking', value: trimmed, section: currentSection });
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
      console.log('');
      for (const line of displayContext) {
        // Word-wrap at 72 chars for readability
        const words = line.split(' ');
        let row = '  ';
        for (const w of words) {
          if (row.length + w.length + 1 > 74) { console.log(row); row = '  ' + w; }
          else row += (row === '  ' ? '' : ' ') + w;
        }
        if (row.trim()) console.log(row);
      }
      console.log('');
    };

    switch (cmd) {
      case 'navigate':
        return {
          name: `Navigate to ${arg}`,
          async run() {
            printContext();
            await page.goto(arg, { waitUntil: 'load', timeout: 60000 });
            await page.waitForTimeout(3000);
          },
        };

      case 'open-chat':
        return {
          name: 'Open Copilot chat pane',
          async run() {
            printContext();
            const iframe = page.locator('[data-automationid="ChatODSPFrame"]');
            if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
              await openChatPane(page);
            } else {
              console.log('    Chat pane already open.');
            }
            chatFrame = page.frameLocator('[data-automationid="ChatODSPFrame"]');
          },
        };

      case 'prompt':
        return {
          name: `Prompt: "${arg}"`,
          async run() {
            printContext();
            if (!chatFrame) {
              const iframe = page.locator('[data-automationid="ChatODSPFrame"]');
              if (!await iframe.isVisible({ timeout: 8000 }).catch(() => false)) {
                await openChatPane(page);
              }
              chatFrame = page.frameLocator('[data-automationid="ChatODSPFrame"]');
            }
            const input = await getChatInput(page, chatFrame);
            await slowType(input, arg);
            await input.press('Enter');
          },
        };

      case 'wait':
        return {
          name: 'Wait for Copilot response',
          async run() {
            printContext();
            await waitForCopilotResponse(page, chatFrame);
          },
        };

      case 'pause':
        return {
          name: arg || 'Pause — presenter moment',
          async run() {
            printContext();
            process.stdout.write('  [Press Enter to continue...] ');
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
            process.stdout.write('  Press Enter once you have completed the action... ');
            await waitForKey();
            console.log('  Confirmed.\n');
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
            await page.screenshot({ path: screenshotPath });
            console.log(`    Saved ${screenshotPath}`);
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

  return steps;
}

// ─── Step runner ─────────────────────────────────────────────────────────────

async function runSteps(page, steps) {
  const startTime = Date.now();

  console.log('\nSteps:');
  steps.forEach((s, i) => console.log(`  ${i + 1}. ${s.name}`));
  console.log('\nControls: Enter = run  |  s = skip  |  b = back  |  ? = help\n');

  let i = 0;
  while (i < steps.length) {
    const step = steps[i];
    const elapsed = formatElapsed(Date.now() - startTime);
    process.stdout.write(`[${elapsed}] Step ${i + 1}/${steps.length}: ${step.name}\n         › `);

    const key = await waitForKey();

    if (key === '?') {
      printHelp();
      continue; // re-prompt same step
    }

    if (key === 's') {
      console.log('skipped.');
      i++;
      continue;
    }

    if (key === 'b') {
      if (i === 0) {
        console.log('already at first step.');
        continue;
      }
      i--;
      console.log(`back — re-running step ${i + 1}.`);
      // fall through to run
    } else {
      console.log('running...');
    }

    try {
      await steps[i].run();
    } catch (err) {
      console.error(`\n  Error in step ${i + 1}: ${err.message}`);
      await page.screenshot({ path: 'tools/debug-screenshot.png' }).catch(() => {});
      console.error('  Debug screenshot saved to tools/debug-screenshot.png');
      console.error('  Press Enter to continue to the next step, or Ctrl+C to quit.');
      await waitForKey();
    }

    // Only advance when we ran forward (not on 'b')
    if (key !== 'b') i++;
  }

  const totalTime = formatElapsed(Date.now() - startTime);
  console.log(`\nDemo complete in ${totalTime}.`);
}

function printHelp() {
  console.log(`
  Enter   run the current step
  s       skip this step
  b       go back and re-run the previous step
  ?       show this help
  Ctrl+C  quit
`);
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
      const key = ch === '\r' || ch === '\n' ? 'enter' : ch.toLowerCase();
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
      resolve(key === '\r' || key === '\n' ? 'enter' : key[0].toLowerCase());
    });
  });
}

function formatElapsed(ms) {
  const s = Math.floor(ms / 1000);
  const m = Math.floor(s / 60);
  return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}

// ─── Browser helpers ──────────────────────────────────────────────────────────

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
async function slowType(locator, text, delayMs = 40) {
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
async function waitForCopilotResponse(page, chatFrame, timeoutMs = 60000) {
  const deadline = Date.now() + timeoutMs;

  const stopSelectors = [
    '[aria-label*="Stop"]',
    'button:has-text("Stop")',
    '[aria-label*="stop generating"]',
  ];

  process.stdout.write('    Waiting for generation to start');
  let stopBtn = null;
  const startDeadline = Date.now() + 10000;
  outer: while (Date.now() < startDeadline) {
    for (const sel of stopSelectors) {
      const loc = chatFrame.locator(sel).first();
      if (await loc.isVisible({ timeout: 500 }).catch(() => false)) {
        stopBtn = loc;
        break outer;
      }
    }
    process.stdout.write('.');
    await page.waitForTimeout(300);
  }

  if (stopBtn) {
    process.stdout.write(' started.\n    Waiting for generation to finish');
    while (Date.now() < deadline) {
      if (!await stopBtn.isVisible({ timeout: 500 }).catch(() => false)) {
        console.log(' done.');
        return;
      }
      process.stdout.write('.');
      await page.waitForTimeout(500);
    }
    console.log('\n    Timed out waiting for stop button to disappear.');
    return;
  }

  // Fallback
  console.log('\n    Stop button not seen — polling for feedback buttons...');
  const feedbackSel = '[aria-label="Like"], [aria-label="Dislike"]';
  const initialCount = await chatFrame.locator(feedbackSel).count().catch(() => 0);

  while (Date.now() < deadline) {
    const count = await chatFrame.locator(feedbackSel).count().catch(() => 0);
    if (count > initialCount) {
      console.log('    Generation complete (feedback buttons appeared).');
      return;
    }
    await page.waitForTimeout(500);
  }

  console.warn('    Timed out waiting for response. Proceeding anyway.');
}

/**
 * Pause and prompt the operator to perform a manual step before continuing.
 * Mark the call site with: // [COMMAND]: <instruction>
 */
async function pause(message) {  // eslint-disable-line no-unused-vars
  console.log(`\n  [PAUSED] ${message}`);
  process.stdout.write('  Press Enter to continue...');
  await waitForKey();
  console.log('  Resuming.\n');
}

// ─── Run ──────────────────────────────────────────────────────────────────────

main().catch(err => {
  console.error('\nDemo runner error:', err.message);
  process.exit(1);
});
