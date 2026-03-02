# SharePoint AI Skills

A curated library of AI skills and end-to-end demo setups for the latest AI features in Microsoft 365 SharePoint.

> **Status:** Active — new content added regularly.

---

## What's Inside

| Folder | Purpose | Intended use |
|---|---|---|
| `<skill-name>/` | AI skills — each skill in its own folder with a `SKILL.md` file, following the [agentskills.io](https://agentskills.io/specification) format | Download the skill folder and install it |
| [`demos/`](./demos/) | End-to-end demo setups with sample content, configuration steps, and screenshots | Reference and walkthrough — not intended for direct reuse |

---

## Skills

| Folder | Skill | Description |
|---|---|---|
| [authoring-sharepoint-markdown/](./authoring-sharepoint-markdown/) | Authoring SharePoint Markdown | Converts documents and gathered content into SharePoint-compatible markdown files. Covers formatting rules, templates, and a six-step workflow for publishing to SharePoint pages and web parts. |
| [brainstorming-design-docs/](./brainstorming-design-docs/) | Brainstorming to Design Doc | Guides a raw idea through structured brainstorming into a complete design document. Asks clarifying questions one at a time, proposes alternatives with trade-offs, builds the design incrementally with user approval, then delivers SharePoint-ready Markdown. |
| [copy-editing/](./copy-editing/) | Copy Editing | Edits documents using seven sequential sweeps: Clarity, Voice & Tone, So What, Prove It, Specificity, Scannability, and Action. Run all sweeps for a full edit, or target a specific one. |
| [decision-log/](./decision-log/) | Decision Log | Extracts Decision Records from video or audio transcripts. Captures the problem, options considered, who decided, rationale, dissent, conditions, and follow-on actions. |
| [executive-summary/](./executive-summary/) | Executive Summary | Distills long documents, reports, or transcripts into tight one-page summaries for leadership audiences. Surfaces the core situation, key findings, recommendation, and what the reader needs to do. |
| [faq-building/](./faq-building/) | FAQ Building | Builds structured FAQ pages from source documents, policies, process guides, or topic briefs. Anticipates reader questions, groups them into themes, writes clear Q&A pairs, and delivers SharePoint-ready Markdown. |
| [forest-style/](./forest-style/) | Forest-Style Brand | Applies the forest-style brand system to any visual output, document, web content, presentation, or interface element. Covers the full color palette, typography, spacing, component styles, and voice rules. |
| [gap-analysis/](./gap-analysis/) | Gap Analysis | Compares two documents and surfaces what is missing, conflicting, changed, or new between them. Categorizes findings by severity and summarizes implications and recommended actions. |
| [linkedin-post/](./linkedin-post/) | LinkedIn Post Writing | Crafts high-performing LinkedIn posts from any topic, story, announcement, or idea. Covers hook formulas, format rules, five content types, and an optimization checklist. |
| [meeting-notes/](./meeting-notes/) | Meeting Notes | Transforms raw video or audio transcripts into polished, structured meeting summaries. Handles messy auto-generated transcripts, extracts decisions, action items, discussion threads, and key quotes. |
| [project-brief/](./project-brief/) | Project Brief | Turns a rough idea or stakeholder request into a structured project brief. Asks clarifying questions to establish problem, goals, success criteria, scope, stakeholders, and risks, then delivers a decision-ready document. |
| [ralph-loop/](./ralph-loop/) | RALPH Loop | A self-evaluating iterative execution pattern (Reason → Act → Look → Probe → Harden). Keeps the agent looping until all success criteria hit a configurable score threshold. |
| [style-guidelines/](./style-guidelines/) | Brand Style Guide Template | A fill-in-the-blank template for turning any organization's brand guide into an AI skill. Covers color palette, typography, spacing tokens, and component styles. |
| [uppababy-brand-review/](./uppababy-brand-review/) | UPPAbaby Brand Compliance Review | Reviews any content file against UPPAbaby brand guidelines. Produces a weighted scorecard across five categories plus a prioritized remediation list. |
| [youtube-description/](./youtube-description/) | YouTube Description Generator | Turns a video transcript into an engaging YouTube description with a hook, summary, timestamps, key takeaways, and hashtags. |

---

## Getting Started

Each skill folder contains a `SKILL.md` with everything the agent needs. Download the folder for any skill you want to use.

---

## Installing a Skill

Skills follow the [agentskills.io specification](https://agentskills.io/specification). The `Skills/` folder in SharePoint is created automatically — you install by uploading the skill folder:

1. Download the skill folder (e.g., `copy-editing/`)
2. In your SharePoint site, open the **Agent Assets** library
3. Navigate into the **Skills** folder (auto-created)
4. Upload the folder — the agent discovers it by the `name` field in `SKILL.md`

![The Skills folder in SharePoint showing uploaded skill folders](./images/skills-folder.png)

---

## Creating a Skill

A skill is a folder containing a single `SKILL.md` file. The folder name must match the `name` field in the frontmatter exactly.

**Where it goes in SharePoint:** `Skills/<skill-name>/SKILL.md`
The `Skills/` folder is created automatically — you just upload the skill folder inside it.

**Minimal example — `Skills/summarize-page/SKILL.md`:**

```markdown
---
name: summarize-page
description: Summarizes a SharePoint page in 3 bullet points.
  Use when the user asks for a quick summary of a page.
---

# Summarize Page

## Instructions

1. Read the full content of the specified page.
2. Identify the 3 most important points.
3. Return a bulleted summary, each bullet no longer than one sentence.
```

That's a complete, valid skill. The frontmatter tells the agent when to activate it; the body tells it what to do.

---

## Prerequisites

- Microsoft 365 tenant with **Copilot licenses** (where noted per item)
- SharePoint admin or site owner permissions
- Familiarity with the [Microsoft 365 admin center](https://admin.microsoft.com) and [SharePoint admin center](https://admin.sharepoint.com)

---

## Contributing

Contributions and corrections are welcome!

1. Fork the repo and create a branch: `git checkout -b skill/your-skill-name`
2. Create a folder matching your skill name (e.g., `my-skill/`) with a `SKILL.md` inside
3. Ensure the `name` field in frontmatter matches the folder name exactly
4. Open a pull request with a short description of what the skill does

Please keep skills focused, self-contained, and free of tenant-specific credentials or internal URLs.

---

## License

[MIT](./LICENSE) © 2026 [zrosenfield](https://github.com/zrosenfield)

---

## Disclaimer

These skills and demos are provided as-is for learning and experimentation. They are not official Microsoft documentation. Always verify against the latest [Microsoft Learn](https://learn.microsoft.com) docs before deploying to production.
