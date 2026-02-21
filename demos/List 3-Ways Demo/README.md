# Build a SharePoint List 3 Ways with AI

This demo shows three progressively more sophisticated approaches to building a SharePoint list using AI — from a single natural-language request all the way to a polished, brand-consistent list built with the RALPH loop skill.

The scenario throughout: building a session-submission tracking list for **ZachCon 2026**, an M365-focused conference.

---

## Watch the Demo

[![Build a SharePoint List 3 Ways with AI](https://img.youtube.com/vi/2coioZ8aK50/maxresdefault.jpg)](https://youtu.be/2coioZ8aK50)

---

## The 3 Approaches

### Way 1 — Natural Language, Let AI Decide Everything

> *Generate a site for running ZachCon 2026. We need a landing page and a list for submitting session ideas that we will review/approve. Sessions need a title, speakers, description, 100–400 level assignment, conference track, status (to say if we approved the session yet), and link to a deck.*

A single prompt. No column definitions, no schema — just a plain-English description of what you need. AI infers the structure, creates the list, and sets it up end to end.

**Best for:** Quickly standing up a new list when you have a clear idea but don't want to define every field manually.

---

### Way 2 — Specific Instructions with Structured Prompts

> *Create a new list called "Sessions 2026-B". Add speakers (people), description (multiline), level (choice: 100, 200, 300, 400), conference track (choice — you make it up for an M365 session list), and status (approved/rejected/pending). Generate 20 sample items for the list. Build a view to show the approved sessions and another to show the non-approved sessions. Make this view prettier and easier to read.*

Column types are specified. Sample data is requested. Views are defined. A follow-up prompt improves the visual presentation. More control, more predictable output.

**Best for:** When you know your schema and want consistent, reproducible results.

---

### Way 3 — RALPH Loop + Brand Skill for Maximum Polish

> *RALPH in max 15 iterations: Create a "Sessions 2026-C" list that is the ultimate session tracking solution for ZachCon 2026 — an M365-focused conference. Sessions must be approved to be official. Create the views needed to make this list operational. Provide 20 sample items in diverse states so we can see it in action. Make the list beautiful — use the style-definition skill to make sure it matches style guidelines for this site.*

The [RALPH loop skill](../../skills/ralph-loop.md) drives iterative self-evaluation — the agent keeps refining until it hits a quality threshold. The [style-definition skill](./style-definition.md) enforces brand standards at every step. The result is a production-ready list with no manual cleanup.

**Best for:** High-visibility lists where quality and brand consistency matter.

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `script.md` | The exact prompts used in each of the three approaches |
| `style-definition.md` | The brand skill loaded for Way 3 — enforces forest-style visual standards |

---

## Prerequisites

- Microsoft 365 tenant with Copilot licenses
- SharePoint site with agent enabled
- For Way 3: `ralph-loop.md` and `style-definition.md` uploaded to the site's **Agent Assets > Skills** library
