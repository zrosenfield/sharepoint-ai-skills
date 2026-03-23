#!/usr/bin/env node
/**
 * SharePoint AI Skills — Demo Launcher
 *
 * Usage:
 *   node tools/demo.mjs                        # interactive selector
 *   node tools/demo.mjs site-overview          # skip selector, match by name
 *   node tools/demo.mjs tools/scripts/my.demo  # skip selector, exact path
 *
 * Flow:
 *   1. Discover all .demo files in tools/scripts/
 *   2. Show interactive grouped-category selector (or match arg directly)
 *   3. Run the [setup] section as a pre-flight check
 *   4. Clear the terminal and start the [demo] section
 */

import { readdirSync, readFileSync } from 'fs';
import { resolve, join, basename } from 'path';
import { spawnSync } from 'child_process';

const SCRIPTS_DIR = resolve('tools/scripts');
const RUNNER = resolve('tools/run-demo.mjs');

// Preferred display order for categories — unlisted categories appear at the end.
const CATEGORY_ORDER = [
  'Site & Copilot',
  'Documents & Files',
  'Lists & Data',
  'Skills & Pipelines',
];

// ─── Demo discovery ───────────────────────────────────────────────────────────

function discoverDemos() {
  return readdirSync(SCRIPTS_DIR)
    .filter(f => f.endsWith('.demo'))
    .map(f => {
      const filePath = join(SCRIPTS_DIR, f);
      const src = readFileSync(filePath, 'utf8');
      const lines = src.split('\n').map(l => l.trim()).filter(Boolean);

      // Title and description from leading # comments
      const comments = lines.filter(l => l.startsWith('#')).slice(0, 2);
      const title = comments[0]?.replace(/^#+\s*/, '') || basename(f, '.demo');
      const description = comments[1]?.replace(/^#+\s*/, '') || '';

      // Category from [category: Name]
      const catMatch = src.match(/\[category:\s*([^\]]+)\]/);
      const category = catMatch ? catMatch[1].trim() : 'Other';

      // Which sections exist
      const hasSetup = src.includes('[section: setup]');
      const hasReset = src.includes('[section: reset]');

      return { name: basename(f, '.demo'), file: filePath, title, description, category, hasSetup, hasReset };
    })
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

  // ── Two-level loop ────────────────────────────────────────────────────────
  while (true) {
    const category = await pickCategory();
    const demo = await pickDemo(category);
    if (demo) return demo; // null means back — loop back to category picker
  }
}

// ─── Runner ───────────────────────────────────────────────────────────────────

function runSection(demoFile, section) {
  const args = [RUNNER, demoFile];
  if (section !== 'demo') args.push(`--${section}`);

  const result = spawnSync('node', args, {
    stdio: 'inherit',
    env: process.env,
  });

  return result.status ?? 1;
}

function clearTerminal() {
  process.stdout.write('\x1B[2J\x1B[H');
}

function printReadyBanner(demo) {
  const w = process.stdout.columns || 80;
  console.log('');
  console.log(`  \x1B[1;32m✓ Setup complete — ready to demo\x1B[0m`);
  console.log(`  \x1B[2m${'─'.repeat(Math.min(w - 2, 60))}\x1B[0m`);
  console.log(`  \x1B[1m${demo.title}\x1B[0m`);
  if (demo.description) console.log(`  \x1B[2m${demo.description}\x1B[0m`);
  console.log('');
  process.stdout.write('  Press Enter to begin the demo... ');
  return new Promise(resolve => {
    if (process.stdin.isTTY) process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.once('data', buf => {
      const key = buf.toString();
      if (key === '\x03') process.exit(0);
      if (process.stdin.isTTY) process.stdin.setRawMode(false);
      process.stdin.pause();
      console.log('');
      resolve();
    });
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const arg = process.argv[2];
  const demos = discoverDemos();

  if (!demos.length) {
    console.error('No .demo files found in tools/scripts/');
    process.exit(1);
  }

  let demo;

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
  } else {
    demo = await selectDemo(demos);
  }

  // Run setup section if present
  if (demo.hasSetup) {
    console.log(`\n  Running setup check for: ${demo.title}\n`);
    const exitCode = runSection(demo.file, 'setup');
    if (exitCode !== 0) {
      console.error('\n  Setup exited with errors. Fix issues before running the demo.');
      process.stdout.write('  Press Enter to continue anyway, or Ctrl+C to quit... ');
      await new Promise(r => {
        if (process.stdin.isTTY) process.stdin.setRawMode(true);
        process.stdin.resume();
        process.stdin.once('data', buf => {
          if (buf.toString() === '\x03') process.exit(1);
          if (process.stdin.isTTY) process.stdin.setRawMode(false);
          process.stdin.pause();
          r();
        });
      });
    }
  }

  clearTerminal();
  await printReadyBanner(demo);
  clearTerminal();
  runSection(demo.file, 'demo');
}

main().catch(err => {
  console.error('\nLauncher error:', err.message);
  process.exit(1);
});
