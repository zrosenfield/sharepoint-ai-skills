# CLAUDE.md — Project Rules

## Repo Structure

| Path | Purpose |
|------|---------|
| `Skills/` | All AI skills live here. See `Skills/README.md` for the full index. |
| `Skills/<skill-name>/` | Each skill lives in its own folder. The folder name must exactly match the `name` field in the skill's frontmatter. Contains `SKILL.md` and optionally `references/`, `scripts/`, and `assets/` subdirectories per the agentskills.io spec. |
| `Skills/<skill-name>/SKILL.md` | The skill definition file. Required YAML frontmatter (`name`, `description`) followed by skill instructions in Markdown. |
| `demos/` | End-to-end demo setups. Each demo lives in its own subfolder and may include video recordings, scripts, and supporting assets. Not intended for direct reuse — reference and walkthrough material. |
| `branding.md` | Quick-reference brand cheat sheet for the forest-style brand system. Human-readable; not a skill. For the AI-instructional version see `Skills/forest-style/SKILL.md`. |

## Skills

### Follow the agentskills.io specification
Skills follow the [agentskills.io specification](https://agentskills.io/specification). Each skill is a directory inside `Skills/` containing a `SKILL.md` file:

```
Skills/
└── skill-name/
    └── SKILL.md          # Required
```

The directory name must exactly match the `name` field in the frontmatter. For example, a skill with `name: copy-editing` must live at `Skills/copy-editing/SKILL.md`.

### SharePoint skills cannot write code
Skills in this repo run in SharePoint, which does not support code execution. Skills must be written entirely in prose and Markdown — no code blocks containing executable code, no scripts, no shell commands, no pseudocode intended for execution.

### Required frontmatter
Every `SKILL.md` must include valid YAML frontmatter with at minimum these two fields:

```yaml
---
name: skill-name-here
description: Third-person description of what the skill does and when to use it.
---
```

Frontmatter rules (enforced by the platform):
- `name`: must match the parent directory name exactly. Lowercase letters, numbers, and hyphens only — no spaces, no uppercase, no consecutive hyphens, max 64 characters. Must not start or end with a hyphen.
- `description`: non-empty, max 1024 characters, written in third person ("Processes..." not "I can..." or "You can use this to..."), no XML tags. Include both what the skill does and the trigger conditions that should activate it.

Optional frontmatter fields: `license`, `compatibility`, `metadata`, `allowed-tools` — see the [spec](https://agentskills.io/specification) for details.

### Follow the official best practices guide
Before creating or editing a skill, consult the official authoring guide:
**https://agentskills.io/specification**

Key points:
- Keep `SKILL.md` body under 500 lines
- Descriptions must include what the skill does AND when to use it
- Be concise — only add context Claude doesn't already have
- Use consistent terminology throughout
- Avoid time-sensitive information
- Use gerund form for skill names where possible (`copy-editing`, not `copy-editor`)
