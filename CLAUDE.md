# CLAUDE.md — Project Rules

## Repo Structure

| Path | Purpose |
|------|---------|
| `skills/` | AI skill files (`.md`) ready to upload to SharePoint. Each file has YAML frontmatter and self-contained instructions. See `skills/README.md` for the full index. |
| `skills/images/` | Screenshots and images embedded in `skills/README.md` — not skill content. |
| `demos/` | End-to-end demo setups. Each demo lives in its own subfolder and may include video recordings, scripts, and supporting assets. Not intended for direct reuse — reference and walkthrough material. |
| `branding.md` | Quick-reference brand cheat sheet for the forest-style brand system. Human-readable; not a skill. For the AI-instructional version see `skills/forest-style.md`. |

## Skills

### SharePoint skills cannot write code
Skills in this repo run in SharePoint, which does not support code execution. Skills must be written entirely in prose and Markdown — no code blocks containing executable code, no scripts, no shell commands, no pseudocode intended for execution.

### Follow the Claude skill definition format
Every skill file must include valid YAML frontmatter with exactly these two fields:

```yaml
---
name: skill-name-here
description: Third-person description of what the skill does and when to use it.
---
```

Frontmatter rules (enforced by the platform):
- `name`: lowercase letters, numbers, and hyphens only — no spaces, no uppercase, max 64 characters. Do not use reserved words: "anthropic", "claude".
- `description`: non-empty, max 1024 characters, written in third person ("Processes..." not "I can..." or "You can use this to..."), no XML tags. Include both what the skill does and the trigger conditions that should activate it.

### Follow the official best practices guide
Before creating or editing a skill, consult the official authoring guide:
**https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices**

Key points from that guide relevant to this repo:
- Keep `SKILL.md` body under 500 lines
- Descriptions must include what the skill does AND when to use it
- Be concise — only add context Claude doesn't already have
- Use consistent terminology throughout
- Avoid time-sensitive information
- Use gerund form for skill names where possible (`copy-editing`, not `copy-editor`)
