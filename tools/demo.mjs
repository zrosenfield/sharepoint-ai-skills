#!/usr/bin/env node
/**
 * SharePoint AI Skills — Demo Launcher
 *
 * Usage:
 *   node tools/demo.mjs                        # interactive selector
 *   node tools/demo.mjs site-overview          # skip selector, match by name
 *   node tools/demo.mjs tools/scripts/my/my.demo  # skip selector, exact path
 *
 * Flow:
 *   1. Discover all .demo files in tools/scripts/<name>/<name>.demo
 *   2. Show interactive grouped-category selector (or match arg directly)
 *   3. Run the [setup] section as a pre-flight check
 *   4. Clear the terminal and start the [demo] section
 */

import { readdirSync, readFileSync, statSync } from 'fs';
import { resolve, join, dirname, basename } from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPTS_DIR = join(__dirname, 'scripts');
const LOCAL_SCRIPTS_DIR = join(SCRIPTS_DIR, 'local');
const RUNNER = join(__dirname, 'run-demo.mjs');

// Preferred display order for categories — unlisted categories appear at the end.
const CATEGORY_ORDER = [
  'Site & Copilot',
  'Documents & Files',
  'Lists & Data',
  'Skills & Pipelines',
  'Vertical AI',
];

// ─── Demo discovery ───────────────────────────────────────────────────────────

function discoverDemosIn(dir) {
  try { readdirSync(dir); } catch { return []; } // folder may not exist
  return readdirSync(dir)
    .filter(entry => {
      try { return statSync(join(dir, entry)).isDirectory(); } catch { return false; }
    })
    .flatMap(entry => {
      const filePath = join(dir, entry, `${entry}.demo`);
      let src;
      try { src = readFileSync(filePath, 'utf8'); } catch { return []; }
      const lines = src.split('\n').map(l => l.trim()).filter(Boolean);

      const comments = lines.filter(l => l.startsWith('#')).slice(0, 2);
      const title = comments[0]?.replace(/^#+\s*/, '') || entry;
      const description = comments[1]?.replace(/^#+\s*/, '') || '';

      const catMatch = src.match(/\[category:\s*([^\]]+)\]/);
      const category = catMatch ? catMatch[1].trim() : 'Other';

      const hasSetup = src.includes('[section: setup]');
      const hasReset = src.includes('[section: reset]');

      return [{ name: entry, file: filePath, title, description, category, hasSetup, hasReset }];
    });
}

function discoverDemos() {
  // Each demo lives in its own subfolder: scripts/<name>/<name>.demo
  // Local (gitignored) demos live in scripts/local/<name>/<name>.demo
  return [...discoverDemosIn(SCRIPTS_DIR), ...discoverDemosIn(LOCAL_SCRIPTS_DIR)]
    .sort((a, b) => a.name.localeCompare(b.name));
}

// ─── Interactive selector ─────────────────────────────────────────────────────

async function selectDemo(demos) {
  // Group demos by category, in preferred order
  const byCategory = new Map();
  for (const demo of demos) {
    if (!byCategory.has(demo.category)) byCategory.set(demo.category, []);
    byCategory.get(demo.category).push(demo);
  }

  const sortedCategories = [...byCategory.keys()].sort((a, b) => {
    const ai = CATEGORY_ORDER.indexOf(a);
    const bi = CATEGORY_ORDER.indexOf(b);
    if (ai !== -1 && bi !== -1) return ai - bi;
    if (ai !== -1) return -1;
    if (bi !== -1) return 1;
    return a.localeCompare(b);
  });

  const header = () => {
    const w = process.stdout.columns || 80;
    process.stdout.write('\x1B[2J\x1B[H');
    console.log('');
    console.log('  \x1B[1mSharePoint AI Skills — Demo Launcher\x1B[0m');
    console.log(`  \x1B[2m${'─'.repeat(Math.min(w - 2, 60))}\x1B[0m`);
    console.log('');
    return w;
  };

  // ── Level 1: category picker ──────────────────────────────────────────────
  const pickCategory = () => new Promise(resolve => {
    let cursor = 0;

    const render = () => {
      const w = header();
      sortedCategories.forEach((cat, i) => {
        const demos = byCategory.get(cat);
        const selected = i === cursor;
        const arrow  = selected ? '\x1B[1;33m▶\x1B[0m' : ' ';
        const label  = selected ? `\x1B[1;33m${cat}\x1B[0m` : cat;
        const count  = `\x1B[2m${demos.length} demo${demos.length !== 1 ? 's' : ''}\x1B[0m`;
        console.log(`  ${arrow} ${label}  ${count}`);
        console.log('');
      });
      console.log(`  \x1B[2m↑ ↓  navigate   Enter  open   Ctrl+C  quit\x1B[0m`);
      console.log('');
    };

    render();
    if (process.stdin.isTTY) process.stdin.setRawMode(true);
    process.stdin.resume();

    const onData = buf => {
      const key = buf.toString();
      if (key === '\x03') { process.exit(0); }
      if (key === '\x1B[A' || key === 'k') { cursor = (cursor - 1 + sortedCategories.length) % sortedCategories.length; render(); }
      else if (key === '\x1B[B' || key === 'j') { cursor = (cursor + 1) % sortedCategories.length; render(); }
      else if (key === '\r' || key === '\n') {
        process.stdin.removeListener('data', onData);
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        resolve(sortedCategories[cursor]);
      }
    };
    process.stdin.on('data', onData);
  });

  // ── Level 2: demo picker within a category ────────────────────────────────
  const pickDemo = (category) => new Promise(resolve => {
    const list = byCategory.get(category);
    let cursor = 0;

    const render = () => {
      const w = header();
      console.log(`  \x1B[2m← \x1B[0m\x1B[33m${category.toUpperCase()}\x1B[0m`);
      console.log('');
      list.forEach((demo, i) => {
        const selected = i === cursor;
        const arrow    = selected ? '\x1B[1;36m▶\x1B[0m' : ' ';
        const titleFmt = selected ? `\x1B[1;36m${demo.title}\x1B[0m` : demo.title;
        const tags = [
          demo.hasSetup ? '\x1B[2m[setup]\x1B[0m' : null,
          demo.hasReset ? '\x1B[2m[reset]\x1B[0m' : null,
        ].filter(Boolean).join(' ');
        console.log(`  ${arrow} ${titleFmt}  ${tags}`);
        if (demo.description) {
          const maxDesc = (w || 80) - 10;
          const desc = demo.description.length > maxDesc ? demo.description.slice(0, maxDesc - 1) + '…' : demo.description;
          console.log(`      \x1B[2m${desc}\x1B[0m`);
        }
        console.log('');
      });
      console.log(`  \x1B[2m↑ ↓  navigate   Enter  select   Esc  back   Ctrl+C  quit\x1B[0m`);
      console.log('');
    };

    render();
    if (process.stdin.isTTY) process.stdin.setRawMode(true);
    process.stdin.resume();

    const onData = buf => {
      const key = buf.toString();
      if (key === '\x03') { process.exit(0); }
      if (key === '\x1B[A' || key === 'k') { cursor = (cursor - 1 + list.length) % list.length; render(); }
      else if (key === '\x1B[B' || key === 'j') { cursor = (cursor + 1) % list.length; render(); }
      else if (key === '\x1B' || key === '\x1B[D') { // Esc or left arrow — go back
        process.stdin.removeListener('data', onData);
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        resolve(null); // null = back
      } else if (key === '\r' || key === '\n') {
        process.stdin.removeListener('data', onData);
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdout.write('\x1B[2J\x1B[H');
        resolve(list[cursor]);
      }
    };
    process.stdin.on('data', onData);
  });

  // ── Level 3: action picker ────────────────────────────────────────────────
  const pickAction = (demo) => new Promise(resolve => {
    const actions = [
      { key: 'setup+demo', label: 'Setup + Demo', desc: 'Run setup, then run the demo' },
      ...(demo.hasSetup ? [{ key: 'setup', label: 'Setup only', desc: 'Prepare the environment for later' }] : []),
      { key: 'demo', label: 'Demo only', desc: 'Skip setup — jump straight to the demo' },
      ...(demo.hasReset ? [{ key: 'reset', label: 'Reset', desc: 'Tear down and restore to pre-demo state' }] : []),
    ];
    let cursor = 0;

    const render = () => {
      const w = header();
      console.log(`  \x1B[2m← \x1B[0m\x1B[33m${demo.title.toUpperCase()}\x1B[0m`);
      if (demo.description) console.log(`  \x1B[2m${demo.description}\x1B[0m`);
      console.log('');
      actions.forEach((action, i) => {
        const selected = i === cursor;
        const arrow    = selected ? '\x1B[1;36m▶\x1B[0m' : ' ';
        const labelFmt = selected ? `\x1B[1;36m${action.label}\x1B[0m` : action.label;
        const descFmt  = `\x1B[2m${action.desc}\x1B[0m`;
        console.log(`  ${arrow} ${labelFmt}   ${descFmt}`);
        console.log('');
      });
      console.log(`  \x1B[2m↑ ↓  navigate   Enter  select   Esc  back   Ctrl+C  quit\x1B[0m`);
      console.log('');
    };

    render();
    if (process.stdin.isTTY) process.stdin.setRawMode(true);
    process.stdin.resume();

    const onData = buf => {
      const key = buf.toString();
      if (key === '\x03') { process.exit(0); }
      if (key === '\x1B[A' || key === 'k') { cursor = (cursor - 1 + actions.length) % actions.length; render(); }
      else if (key === '\x1B[B' || key === 'j') { cursor = (cursor + 1) % actions.length; render(); }
      else if (key === '\x1B' || key === '\x1B[D') {
        process.stdin.removeListener('data', onData);
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        resolve(null); // back
      } else if (key === '\r' || key === '\n') {
        process.stdin.removeListener('data', onData);
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdout.write('\x1B[2J\x1B[H');
        resolve(actions[cursor].key);
      }
    };
    process.stdin.on('data', onData);
  });

  // ── Three-level loop ──────────────────────────────────────────────────────
  while (true) {
    const category = await pickCategory();
    while (true) {
      const demo = await pickDemo(category);
      if (!demo) break; // Esc → back to category picker
      const action = await pickAction(demo);
      if (action) return { demo, action };
      // null → back to demo picker, continue inner loop
    }
  }
}

// ─── Runner ───────────────────────────────────────────────────────────────────

function runSection(demoFile, section, extraFlags = []) {
  const args = [RUNNER, demoFile, ...extraFlags];
  if (section !== 'demo') args.push(`--${section}`); // handles setup, reset, all

  const result = spawnSync('node', args, {
    stdio: 'inherit',
    env: process.env,
  });

  return result.status ?? 1;
}

function clearTerminal() {
  process.stdout.write('\x1B[2J\x1B[H');
}


// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const flags = process.argv.slice(2).filter(a => a.startsWith('--'));
  const arg = process.argv.slice(2).find(a => !a.startsWith('--'));
  const extraFlags = flags.filter(f => f === '--widget'); // pass-through flags for the runner

  const demos = discoverDemos();

  if (!demos.length) {
    console.error('No .demo files found in tools/scripts/. Each demo should live at tools/scripts/<name>/<name>.demo');
    process.exit(1);
  }

  let demo;
  let action;

  if (arg) {
    const match =
      demos.find(d => d.file === resolve(arg)) ||
      demos.find(d => d.name === arg) ||
      demos.find(d => d.name.includes(arg));

    if (!match) {
      console.error(`No demo matched "${arg}". Available:`);
      demos.forEach(d => console.error(`  ${d.name}  —  ${d.title}  [${d.category}]`));
      process.exit(1);
    }
    demo = match;
    action = 'setup+demo'; // default when invoked directly
  } else {
    ({ demo, action } = await selectDemo(demos));
  }

  if (action === 'setup') {
    console.log(`\n  Running setup for: ${demo.title}\n`);
    runSection(demo.file, 'setup', extraFlags);
    return;
  }

  if (action === 'reset') {
    console.log(`\n  Running reset for: ${demo.title}\n`);
    runSection(demo.file, 'reset', extraFlags);
    return;
  }

  // action === 'setup+demo' or 'demo'
  clearTerminal();
  if (action === 'setup+demo' && demo.hasSetup) {
    // Run setup + demo in a single browser session via --all
    runSection(demo.file, 'all', extraFlags);
  } else {
    runSection(demo.file, 'demo', extraFlags);
  }
}

main().catch(err => {
  console.error('\nLauncher error:', err.message);
  process.exit(1);
});
