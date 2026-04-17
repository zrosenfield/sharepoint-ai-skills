---
name: copy-editing
description: Systematically edits Markdown documents — READMEs, skill files, and demo guides — using seven sequential sweeps. Each sweep focuses on one quality dimension so nothing gets missed. Use when a document needs to be clearer, tighter, or easier to act on. Triggers include "edit this", "clean this up", "review my README", "improve this skill", "tighten this up", or when a document feels long, vague, or hard to follow. Does NOT write or suggest code.
---

# Copy Editing Skill

> **Scope:** Edits prose and Markdown structure only. Does not write, suggest, or modify code.

---

## The Seven Sweeps

Run these in order. Complete each sweep fully before moving to the next. See [sweeps-reference.md](sweeps-reference.md) for detailed look-for lists, patterns, and checklists.

| # | Sweep | Goal | Key Focus |
|---|-------|------|-----------|
| 1 | Clarity | Every sentence understood on first read | Passive voice, buried leads, assumed knowledge |
| 2 | Voice and Tone | Sounds like a knowledgeable colleague | Formality, enthusiasm inflation, hedging, person consistency |
| 3 | So What | Every section answers "why does this matter?" | Features without benefits, descriptions without value |
| 4 | Prove It | Claims backed by examples | Assertions without illustration, vague capabilities |
| 5 | Specificity | Precise language over vague language | Quantity, scope, time, and outcome vagueness |
| 6 | Scannability | Structure visible without reading every word | Prose walls, heading hierarchy, table clarity |
| 7 | Action | Always clear what to do next | Passive instructions, buried CTAs, missing invocation guidance |

**Inline examples:**

- **Clarity fix:** "The file is loaded by the system on startup" → "The system loads the file on startup"
- **Specificity fix:** "The RALPH loop runs a few iterations until it's satisfied" → "RALPH runs up to 5 iterations and stops when all criteria score 9/10 or above"
- **So What fix:** "This skill includes four post type templates" → "Four post type templates mean you always start with the right structure — no blank page"

---

## Running the Sweeps

### Full Edit
Run all seven sweeps in order. Output the revised document after all sweeps complete. Briefly note what changed and why.

### Targeted Edit
If the user identifies a specific problem ("this feels vague", "the instructions are confusing"), start with the most relevant sweep and flag if other sweeps would also help.

### Review Mode
If asked to review rather than rewrite, score the document on each sweep (1–10) and list specific issues found. Do not rewrite unless asked.

---

## Output Format

After editing, provide:

1. **Revised document** — full Markdown, ready to save
2. **Edit summary** — brief bullets on the most significant changes made and which sweep caught them
3. **Remaining flags** — anything that couldn't be fixed without more context from the author (missing examples, unknown specifics, unclear intent)

---

## Boundaries

- Does not rewrite content so substantially that the author's intent changes
- Does not add sections or topics not already present (unless a required section like a CTA is missing entirely)
- Flags factual claims for author verification rather than changing them
