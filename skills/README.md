# Skills

AI skills are instruction files you can load into Copilot, an agent, or any AI assistant to give it a focused capability. Download the `.md` file and paste it into your agent's instructions or system prompt.

## Available Skills

| File | Skill | Description |
|---|---|---|
| [copy-editing.md](./copy-editing.md) | Copy Editing | Edits READMEs, skill files, site plans, and demo guides using seven sequential sweeps: Clarity, Voice & Tone, So What, Prove It, Specificity, Scannability, and Action. Run all sweeps for a full edit, or target a specific one. Does not write or suggest code. |
| [linkedin-post.md](./linkedin-post.md) | LinkedIn Demo Post Creator | Transforms demo video transcripts into LinkedIn posts in Zach Rosenfield's voice. Covers four post types (personal use case, feature announcement, natural language demo, public preview) and includes a full workflow from transcript to published post. Tuned for SharePoint / Knowledge Agent content. |
| [ralph-loop.md](./ralph-loop.md) | RALPH Loop | A self-evaluating iterative execution pattern (Reason → Act → Look → Probe → Harden). Keeps the agent looping until all success criteria hit a configurable score threshold, then stops. Use when a first-pass answer isn't good enough — document generation, data extraction, analysis, or any quality-sensitive task. |
| [style-guidelines.md](./style-guidelines.md) | Brand Style Guide Template | A fill-in-the-blank template for turning any organization's brand guide into an AI skill. Covers color palette, typography, spacing tokens, and component styles (buttons, cards, tables, badges, alerts). Replace the placeholders with your brand values, then load the skill whenever generating visual output, documents, or UI. |

## How to Use a Skill

1. Open the `.md` file and copy the contents
2. Paste into your agent's **Instructions** field (Copilot Studio, SharePoint agent, etc.) or prepend it to your chat as a system message
3. The skill's frontmatter `name` and `description` fields help the agent know when to apply it automatically

## Contributing a Skill

Skills work best when they are:
- **Focused** — one capability per file
- **Self-contained** — no external dependencies required to use it
- **Documented** — frontmatter with `name` and `description` so agents can self-select the skill
