#!/usr/bin/env node
import { parseScript } from './parser.js';
import { Player } from './player.js';
import path from 'path';

function parseArgs(argv) {
  const args = { positional: [], flags: {} };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args.flags[key] = next;
        i++;
      } else {
        args.flags[key] = true;
      }
    } else {
      args.positional.push(argv[i]);
    }
  }
  return args;
}

function printHelp() {
  console.log(`
SharePoint AI Demo Runner

Usage:
  node demos/tool/runner.js <script.md> [options]

Options:
  --url <url>             Override the URL from script frontmatter
  --speed slow|normal|fast  Typing speed  (default: normal)
  --screenshots <dir>     Directory for screenshots  (default: ./screenshots)
  --session <id>          Reuse an existing Playwriter session
  --no-auto-pause         Don't pause after each AI prompt (use explicit <!-- wait --> instead)
  --dry-run               Print steps without executing

Example:
  node demos/tool/runner.js demos/PTO\\ App/demo.md --speed slow
`);
}

async function runSteps(player, steps, autoPause) {
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const label = `[${i + 1}/${steps.length}]`;

    switch (step.type) {
      case 'navigate':
        console.log(`${label} navigate → ${step.url}`);
        await player.navigate(step.url);
        break;

      case 'type':
        console.log(`${label} type: "${step.text.slice(0, 60)}${step.text.length > 60 ? '…' : ''}"`);
        await player.typeInAI(step.text);
        if (autoPause) await player.pause();
        break;

      case 'pause':
        console.log(`${label} pause`);
        await player.pause();
        break;

      case 'wait':
        console.log(`${label} wait ${step.ms}ms`);
        await player.wait(step.ms);
        break;

      case 'screenshot':
        console.log(`${label} screenshot: "${step.caption}"`);
        await player.screenshot(step.caption);
        break;

      case 'speed':
        console.log(`${label} speed → ${step.value}`);
        player.setSpeed(step.value);
        break;

      default:
        console.warn(`${label} Unknown step type: ${step.type}`);
    }
  }
}

async function main() {
  const { positional, flags } = parseArgs(process.argv.slice(2));

  if (flags.help || flags.h || positional.length === 0) {
    printHelp();
    process.exit(0);
  }

  const scriptPath = path.resolve(positional[0]);
  let parsed;
  try {
    parsed = parseScript(scriptPath);
  } catch (err) {
    console.error(`Error reading script: ${err.message}`);
    process.exit(1);
  }

  const { meta, steps } = parsed;
  const autoPause = !flags['no-auto-pause'];

  const playerOptions = {
    speed: flags.speed || meta.speed || 'normal',
    selector: meta.selector || '',
    screenshots: flags.screenshots || meta.screenshots || '',
  };

  if (flags['dry-run']) {
    console.log(`\nScript: ${meta.title || scriptPath}`);
    if (meta.url) console.log(`URL: ${meta.url}`);
    console.log(`Auto-pause after prompts: ${autoPause}`);
    console.log(`\nSteps (${steps.length}):\n`);
    steps.forEach((s, i) => {
      const detail =
        s.type === 'type'       ? `"${s.text.slice(0, 72)}${s.text.length > 72 ? '…' : ''}"` :
        s.type === 'navigate'   ? s.url :
        s.type === 'wait'       ? `${s.ms}ms` :
        s.type === 'screenshot' ? `"${s.caption}"` :
        s.type === 'speed'      ? s.value :
        '';
      const autoTag = autoPause && s.type === 'type' ? ' + auto-pause' : '';
      console.log(`  ${String(i + 1).padStart(2)}. ${s.type}${autoTag}${detail ? '  ' + detail : ''}`);
    });
    console.log('');
    return;
  }

  console.log(`\n▶  ${meta.title || path.basename(scriptPath)}`);
  if (meta.url) console.log(`   ${meta.url}`);
  console.log(`   ${steps.length} steps  |  speed: ${playerOptions.speed}  |  auto-pause: ${autoPause}\n`);

  let player;
  try {
    if (flags.session) {
      console.log(`[runner] Reusing session ${flags.session}`);
      player = new Player({ sessionId: flags.session, ...playerOptions });
    } else {
      player = await Player.create(playerOptions);
    }
  } catch (err) {
    console.error(`\nFailed to start Playwriter session: ${err.message}`);
    console.error('Make sure the Playwriter Chrome extension is running and connected.');
    process.exit(1);
  }

  if (meta.url && steps[0]?.type !== 'navigate') {
    await player.navigate(meta.url);
  }

  try {
    await runSteps(player, steps, autoPause);
    console.log('\n✓  Demo complete.\n');
  } catch (err) {
    console.error(`\nError during demo: ${err.message}`);
    process.exit(1);
  }
}

main();
