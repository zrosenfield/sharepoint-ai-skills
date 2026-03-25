/**
 * parser.js
 *
 * Parses a demo markdown script into an ordered array of steps.
 *
 * Script format:
 *   - YAML frontmatter (---) for title, url, selector
 *   - HTML comments <!-- directive --> for control flow
 *   - Paragraphs (blank-line separated) for AI prompts to type and submit
 *
 * Supported directives:
 *   <!-- pause -->               Wait for presenter to click ▶ Next button
 *   <!-- navigate: url -->       Go to a URL
 *   <!-- wait: 3s -->            Auto-wait (supports s and ms units)
 *   <!-- screenshot: caption --> Save a screenshot
 *   <!-- speed: slow|normal|fast --> Change typing speed
 *   <!-- comment: text -->       Ignored — documentation only
 */

import fs from 'fs';
import matter from 'gray-matter';

const DIRECTIVE_RE = /^<!--\s*(.+?)\s*-->$/;

/**
 * Parse a single directive comment into a step object.
 * Returns null for unknown or comment directives.
 */
function parseDirective(raw) {
  const text = raw.trim();

  if (text === 'pause') {
    return { type: 'pause' };
  }

  const navigateMatch = text.match(/^navigate:\s*(.+)$/);
  if (navigateMatch) {
    return { type: 'navigate', url: navigateMatch[1].trim() };
  }

  const waitMatch = text.match(/^wait:\s*(\d+)(ms|s)?$/);
  if (waitMatch) {
    const value = parseInt(waitMatch[1], 10);
    const unit = waitMatch[2] || 's';
    return { type: 'wait', ms: unit === 'ms' ? value : value * 1000 };
  }

  const screenshotMatch = text.match(/^screenshot(?::\s*(.+))?$/);
  if (screenshotMatch) {
    return { type: 'screenshot', caption: screenshotMatch[1] || '' };
  }

  const speedMatch = text.match(/^speed:\s*(slow|normal|fast)$/);
  if (speedMatch) {
    return { type: 'speed', value: speedMatch[1] };
  }

  // comment: ... — silently ignore
  if (text.startsWith('comment:')) {
    return null;
  }

  // Unknown directive — warn but skip
  console.warn(`[parser] Unknown directive ignored: <!-- ${text} -->`);
  return null;
}

/**
 * Parse a markdown demo script file.
 *
 * Returns:
 *   {
 *     meta: { title, url, selector },   // from frontmatter
 *     steps: Array<Step>                // ordered step list
 *   }
 *
 * Step shapes:
 *   { type: 'navigate', url }
 *   { type: 'type', text }
 *   { type: 'pause' }
 *   { type: 'wait', ms }
 *   { type: 'screenshot', caption }
 *   { type: 'speed', value }
 */
export function parseScript(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const { data: frontmatter, content } = matter(raw);

  const meta = {
    title: frontmatter.title || '',
    url: frontmatter.url || '',
    selector: frontmatter.selector || '',
  };

  const steps = [];

  // Split into blocks by one or more blank lines
  const blocks = content
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter(Boolean);

  for (const block of blocks) {
    const directiveMatch = block.match(DIRECTIVE_RE);

    if (directiveMatch) {
      const step = parseDirective(directiveMatch[1]);
      if (step) steps.push(step);
    } else {
      // Plain text block — becomes a "type" step.
      // Normalise internal newlines to spaces so multi-line paragraphs
      // are submitted as a single AI message.
      const text = block.replace(/\n/g, ' ').trim();
      if (text) steps.push({ type: 'type', text });
    }
  }

  return { meta, steps };
}
