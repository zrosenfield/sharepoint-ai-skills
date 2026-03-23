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
 *   2. Show interactive selector (or match arg directly)
 *   3. Run the [setup] section as a pre-flight check
 *   4. Clear the terminal and start the [demo] section
 */

import { readdirSync, readFileSync } from 'fs';
import { resolve, join, basename } from 'path';
import { spawnSync } from 'child_process';

const SCRIPTS_DIR = resolve('tools/scripts');
const RUNNER = resolve('tools/run-demo.mjs');

// ─── Demo discovery ───────────────────────────────────────────────────────────

function discoverDemos() {
  return readdirSync(SCRIPTS_DIR)
    .filter(f => f.endsWith('.demo'))
    .map(f => {
      const filePath = join(SCRIPTS_DIR, f);
      const src = readFileSync(filePath, 'utf8');
      const lines = src.split('\n').map(l => l.trim()).filter(Boolean);

      // Extract title and description from leading # comments
      const comments = lines.filter(l => l.startsWith('#')).slice(0, 2);
      const title = comments[0]?.replace(/^#+\s*/, '') || basename(f, '.demo');
      const description = comments[1]?.replace(/^#+\s*/, '') || '';

      // Check which sections exist
      const hasSetup = src.includes('[section: setup]');
      const hasReset = src.includes('[section: reset]');

      return { name: basename(f, '.demo'), file: filePath, title, description, hasSetup, hasReset };
    })
    .sort((a, b) => a.name.localeCompare(b.name));
}

// ─── Interactive selector ─────────────────────────────────────────────────────

async function selectDemo(demos) {
  let cursor = 0;

  const render = () => {
    // Move to top of the list (cursor up by demos.length + header lines)
    process.stdout.write('\x1B[2J\x1B[H'); // clear screen, move to top

    const w = process.stdout.columns || 80;
    const bar = '─'.repeat(w);

    console.log('');
    console.log('  SharePoint AI Skills — Demo Launcher');
    console.log(`  ${bar.slice(0, w - 2)}`);
    console.log('');

    demos.forEach((demo, i) => {
      const selected = i === cursor;
      const prefix = selected ? '  ▶ ' : '    ';
      const titleLine = selected
        ? `\x1B[1;36m${demo.title}\x1B[0m`
        : demo.title;

      const tags = [
        demo.hasSetup ? 'setup' : null,
        demo.hasReset ? 'reset' : null,
      ].filter(Boolean).map(t => `\x1B[2m[${t}]\x1B[0m`).join(' ');

      console.log(`${prefix}${titleLine}  ${tags}`);

      if (demo.description) {
        const descPrefix = selected ? '      ' : '      ';
        console.log(`${descPrefix}\x1B[2m${demo.description}\x1B[0m`);
      }
      console.log('');
    });

    console.log(`  \x1B[2m↑/↓ navigate   Enter select   Ctrl+C quit\x1B[0m`);
    console.log('');
  };

  render();

  return new Promise((resolve, reject) => {
    if (process.stdin.isTTY) process.stdin.setRawMode(true);
    process.stdin.resume();

    process.stdin.on('data', buf => {
      const key = buf.toString();

      if (key === '\x03') { // Ctrl+C
        process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdout.write('\n');
        process.exit(0);
      }

      if (key === '\x1B[A' || key === 'k') { // Up arrow or k
        cursor = (cursor - 1 + demos.length) % demos.length;
        render();
      } else if (key === '\x1B[B' || key === 'j') { // Down arrow or j
        cursor = (cursor + 1) % demos.length;
        render();
      } else if (key === '\r' || key === '\n') { // Enter
        if (process.stdin.isTTY) process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdout.write('\x1B[2J\x1B[H'); // clear before running
        resolve(demos[cursor]);
      }
    });
  });
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
  const bar = '─'.repeat(w);
  console.log('');
  console.log(`  \x1B[1;32m✓ Setup complete — ready to demo\x1B[0m`);
  console.log(`  ${bar.slice(0, w - 2)}`);
  console.log(`  \x1B[1m${demo.title}\x1B[0m`);
  if (demo.description) console.log(`  \x1B[2m${demo.description}\x1B[0m`);
  console.log('');
  process.stdout.write('  Press Enter to begin the demo... ');
  // Wait for a single keypress
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
    // Match by filename or partial name
    const match =
      demos.find(d => d.file === resolve(arg)) ||        // exact path
      demos.find(d => d.name === arg) ||                  // exact name
      demos.find(d => d.name.includes(arg));              // partial name

    if (!match) {
      console.error(`No demo matched "${arg}". Available:`);
      demos.forEach(d => console.error(`  ${d.name}  —  ${d.title}`));
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

  // Clear terminal and show ready banner
  clearTerminal();
  await printReadyBanner(demo);

  // Clear once more and run the demo
  clearTerminal();
  runSection(demo.file, 'demo');
}

main().catch(err => {
  console.error('\nLauncher error:', err.message);
  process.exit(1);
});
