---
name: authoring-sharepoint-markdown
description: Converts documents and knowledge gathered from Microsoft Copilot into well-structured, SharePoint-compatible markdown files. Use when a user has content from Copilot (summaries, research, meeting notes, process steps) and wants to produce a formatted page for a SharePoint site, wiki, or knowledge base. Triggers include "create a markdown file from this", "format this for SharePoint", "write this up as a knowledge base article", "turn this Copilot output into a page", or when a user pastes Copilot-generated content and asks for it to be documented.
---

# Authoring SharePoint Markdown

This skill turns Copilot-gathered content into a clean, well-structured markdown file that renders correctly in SharePoint's Markdown web part. It handles the format decisions so the author focuses on the content.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas of any kind.

---

## How SharePoint Renders Markdown

Before formatting, understand what SharePoint's Markdown web part supports and what it doesn't. Staying within these boundaries means no surprises when the page goes live.

**Renders reliably:**
- Headers (H1–H4; H5–H6 render but look identical to H4)
- Bold (`**text**`) and italic (`*text*`)
- Ordered and unordered lists, including nested lists (up to three levels)
- Tables (pipe-delimited; keep them narrow — wide tables scroll awkwardly on mobile)
- Links using the standard `[text](url)` format
- Blockquotes for callouts and notes
- Horizontal rules (`---`) as visual dividers
- Fenced code blocks (rendered in monospace; no syntax highlighting)

**Use with care:**
- Images: use absolute URLs (SharePoint CDN links or external sources); relative paths break outside the authoring context
- Task list checkboxes (`- [ ]`): render in some tenants, not others — avoid if readers need to rely on them

**Do not use:**
- Inline HTML (`<details>`, `<summary>`, `<div>`, etc.) — behavior is tenant-dependent and often stripped
- Footnotes — not supported
- Definition lists — not supported
- Emoji shortcodes (`:rocket:`) — use Unicode emoji directly (🚀) if needed

---

## Workflow: From Copilot Content to SharePoint Page

### Step 1 — Define purpose and audience

Before organizing any content, answer these two questions:

- **What is this document for?** (Reference, process guide, meeting record, knowledge article, project overview)
- **Who will read it?** (All staff, a specific team, new hires, external stakeholders)

The answers determine which template to use and how much context to include.

### Step 2 — Inventory the Copilot content

Review all Copilot-sourced material and sort it into three buckets:

- **Include as-is** — facts, summaries, or outputs that are accurate and complete
- **Include with edits** — content that is accurate but needs restructuring, simplification, or more concrete language
- **Exclude or verify** — any claims that may be hallucinated, outdated, or out of scope

Flag excluded items rather than silently dropping them so the author knows to verify or fill the gap.

### Step 3 — Choose a document type

Select the template that best matches the document's purpose (see Templates section below). If no single template fits, use the General Knowledge Article template as a base and adapt the section structure.

### Step 4 — Draft the document

Apply the chosen template. For each section:

- Lead with the most important information; put background and context after
- Use one heading per topic — do not cram multiple topics under one heading
- Turn any list of three or more parallel items into a bulleted or numbered list
- Use a table only when two or more attributes apply to each item in a list

### Step 5 — Apply SharePoint formatting

After drafting, do a formatting pass:

- Confirm heading levels don't skip (H1 → H2 → H3, never H1 → H3)
- Check that every table has a header row with the column names bolded or pipe-separated
- Replace any relative image paths with absolute URLs
- Remove any HTML tags
- Verify all links use `[display text](full URL)` format

### Step 6 — Deliver the output

Provide the complete markdown document, ready to paste into a SharePoint Markdown web part. Follow it with a brief list of any flagged gaps, unverified claims, or sections that need author input.

---

## Templates

### General Knowledge Article

Use for reference pages, FAQs, how-to guides, and most Copilot research outputs.

```
# [Topic Name]

> **Summary:** One or two sentences describing what this page covers and who it's for.

---

## Overview

[Context: why this topic matters, when to use this information]

---

## [Main Section 1]

[Content]

---

## [Main Section 2]

[Content]

---

## Key Takeaways

- [Concise summary point 1]
- [Concise summary point 2]
- [Concise summary point 3]

---

## Related Resources

- [Resource Name](url)
- [Resource Name](url)
```

---

### Process or How-To Guide

Use when the document describes a sequence of steps a person must follow.

```
# How to [Task Name]

> **Summary:** What this process does and who performs it.

---

## Before You Begin

**You will need:**
- [Prerequisite or access required]
- [Tool or resource required]

**Estimated time:** [duration]

---

## Steps

1. **[Step name]**
   [What to do and why, in plain language]

2. **[Step name]**
   [What to do and why, in plain language]

3. **[Step name]**
   [What to do and why, in plain language]

---

## What to Do If Something Goes Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| [symptom] | [cause] | [action] |

---

## Contact

Questions or issues: [name, team, or link]
```

---

### Meeting or Workshop Summary

Use to convert Copilot meeting summaries or transcripts into a structured record.

```
# [Meeting Name] — [Date]

**Attendees:** [Names or roles]
**Facilitator:** [Name]
**Related project or workstream:** [Name or link]

---

## Purpose

[One sentence: what this meeting was for]

---

## Key Discussion Points

**[Topic 1]**
[What was discussed and any relevant context]

**[Topic 2]**
[What was discussed and any relevant context]

---

## Decisions Made

| Decision | Owner | Date |
|----------|-------|------|
| [Decision description] | [Name] | [Date] |

---

## Actions

| Action | Owner | Due |
|--------|-------|-----|
| [What needs to happen] | [Name] | [Date] |

---

## Next Meeting

**Date:** [Date]
**Focus:** [What will be covered]
```

---

### Project or Initiative Overview

Use for project landing pages, program charters, and initiative summaries.

```
# [Project Name]

> **Status:** [Active / In Review / Complete]
> **Last updated:** [Date]
> **Owner:** [Name or team]

---

## What This Is

[Two to three sentences: what the project does, why it exists, and what success looks like]

---

## Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

---

## Scope

**In scope:**
- [Item]
- [Item]

**Out of scope:**
- [Item]
- [Item]

---

## Timeline

| Phase | Description | Target date |
|-------|-------------|-------------|
| [Phase 1] | [What happens] | [Date] |
| [Phase 2] | [What happens] | [Date] |

---

## Team

| Role | Name |
|------|------|
| [Role] | [Name] |

---

## Resources

- [Document or link name](url)
- [Document or link name](url)
```

---

## Formatting Decisions

These rules apply to all document types.

**Headers:**
- Use H1 for the document title only — one per document
- Use H2 for major sections
- Use H3 for subsections within a major section
- Never skip a level

**Lists:**
- Use bullet lists for unordered items (features, considerations, resources)
- Use numbered lists only when sequence matters (steps, rankings)
- Nest lists at most two levels deep; flatten anything deeper into separate sections

**Tables:**
- Use when each item in a list has two or more attributes
- Keep column headers short (two to four words)
- Align table pipes for readability in the source markdown

**Callouts and notes:**
- Use blockquotes (`>`) for important notices, scope statements, and warnings
- Label them: `> **Note:**`, `> **Warning:**`, or `> **Summary:**`

**Links:**
- Always use descriptive link text — never "click here" or bare URLs
- For SharePoint internal links, use the full absolute URL
- For email links, use `[Name](mailto:email@domain.com)` format

---

## Output Format

For every request, provide:

1. **Complete markdown document** — ready to paste into a SharePoint Markdown web part
2. **Flagged items** — any content that was excluded, needs verification, or requires the author to fill in details
3. **Formatting notes** — brief callouts if anything in the source content required a significant formatting decision

If the user's Copilot content is incomplete or ambiguous, ask for the missing pieces before drafting — do not invent content to fill gaps.
