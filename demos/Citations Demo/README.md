# AI Citation Pipeline for SharePoint

This demo shows how to run a fully automated citation pipeline against a strategic document — extracting every factual assertion, then searching a source library to find evidence for each claim, and writing structured citation records back to a SharePoint list.

The scenario: a strategy team has drafted an executive brief for **Zava**, an athletic apparel brand. The brief is full of market statistics and causal claims. Before presenting it, they need every assertion backed by a source. Three prompts. Zero manual research.

---

## Watch the Demo

[![AI Citation Pipeline for SharePoint](https://img.youtube.com/vi/xNLCwLIy_uE/0.jpg)](https://youtu.be/xNLCwLIy_uE)

---

## The Workflow

Three skills work in sequence to build and populate the citation list:

```
[Document]
    ↓
assertion-list-creator  →  Creates the SharePoint list
assertion-extractor     →  Extracts assertions → writes records
citation-finder         →  Searches corpus → writes citations
    ↓
[Populated Assertion Citations list]
```

---

## Demo Script

### Prompt 1 — Create the List

> *Use the assertion-list-creator skill to create the Assertion Citations SharePoint list at `https://{tenant}.sharepoint.com/sites/{site}`. Configure Record, Statements, and Citations columns, with Citations as multi-line text supporting unlimited length.*

The agent creates a new SharePoint list with three columns: **Record** (the assertion ID), **Statements** (the verbatim claim), and **Citations** (a multi-line field for structured citation blocks). The Citations column is explicitly configured to hold unlimited text — standard single-line fields would silently truncate long citation blocks.

Run this once per project. The list is reusable across multiple documents.

---

### Prompt 2 — Extract Assertions

> *Use the assertion-extractor skill to read `{file path or SharePoint URL to the brief}` and extract all factual assertions that need citations. Write each one as a new record to the Assertion Citations list at `https://{tenant}.sharepoint.com/sites/{site}`. Use the record ID prefix ZAVA-2025.*

The agent reads the document, identifies every claim a reader could reasonably ask "how do you know that?" about — statistics, market projections, causal claims, benchmarks — and writes each one as a separate list record. Opinions and internal company facts are excluded. Internal estimates are flagged with `[Internal estimate]` in the Statements field.

Each assertion gets a sequential ID: `ZAVA-2025-01`, `ZAVA-2025-02`, etc. The Citations column is left blank for the next step.

---

### Prompt 3 — Find Citations

> *Use the citation-finder skill to process all records in the Assertion Citations list at `https://{tenant}.sharepoint.com/sites/{site}` that have an empty Citations field. Search for supporting sources in `{SharePoint folder URL or local corpus path}` and write the citation results back to each record.*

The agent fetches every list record with an empty Citations field, then searches the source document library for each assertion. For quantitative claims it greps for exact figures first; for causal or conceptual claims it runs semantic search. Each citation is classified as Direct, Partial, Indirect, Contradicts, or Not Found, and written back to the list item immediately — so the list shows partial progress in real time.

After all records are processed, the agent prints a summary:

```
CITATION RUN COMPLETE — Zava Executive Brief
Records processed: 8
Direct Support:    5
Partial Support:   1
Indirect Support:  0
Contradicts:       0
Not Found:         2  (1 internal estimate, 1 no corpus match)
```

---

## Skills Used

| Skill | Used In | Description |
|-------|---------|-------------|
| [assertion-list-creator.md](./assertion-list-creator.md) | Prompt 1 | Creates the Assertion Citations SharePoint list with the correct column schema |
| [assertion-extractor.md](./assertion-extractor.md) | Prompt 2 | Reads a document, extracts factual assertions, and writes them as list records |
| [citation-finder.md](./citation-finder.md) | Prompt 3 | Searches a document corpus for supporting sources and writes citation blocks back to each record |

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `script.md` | Raw prompt templates used during the demo recording |
| `assertion-list-creator.md` | Skill file — creates the SharePoint list infrastructure |
| `assertion-extractor.md` | Skill file — extracts assertions from a document and writes list records |
| `citation-finder.md` | Skill file — searches source corpus and populates the Citations column |

---

## Prerequisites

- Microsoft 365 tenant with Copilot licenses
- SharePoint site with agent enabled
- All three skill files uploaded to the site's **Agent Assets > Skills** library
- The document to analyze accessible from SharePoint, OneDrive, or a local file path
- A source document corpus (SharePoint folder, OneDrive library, or local directory) for the citation search
