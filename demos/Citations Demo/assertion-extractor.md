---
name: assertion-extractor
description: >
  Extracts all factual assertions that require citations from a document — such as an executive brief,
  strategy deck, white paper, or report — and writes them as records into a SharePoint Assertion Citations
  list. Use this skill whenever someone asks to "find all the claims," "identify what needs citations,"
  "pull out the assertions," "fact-check this doc," "what statements need backing sources?" or
  "populate the citation list from this document." Also trigger when a user uploads or references a
  strategic document and wants to run it through an AI citation pipeline. This skill is the first step
  in the two-agent citation workflow; its output feeds directly into the Citation Finder skill.
---

# Assertion Extractor

Reads a document, identifies every factual assertion that requires an external citation, and writes
each assertion as a new record to the SharePoint Assertion Citations list (Record + Statements columns).
The Citations column is left empty for the Citation Finder skill to populate.

---

## Prerequisites

Before running, confirm:
1. The **Assertion Citations** SharePoint list exists (if not, run the **Assertion List Creator** skill first)
2. You have the list URL or site path
3. You have the document to analyze (file path, SharePoint URL, or upload)

---

## What Counts as an Assertion

An assertion is any specific factual claim that a reader could reasonably ask "how do you know that?" about.

**Include:**
- Quantitative statistics ("reduces inventory by 31%")
- Market size or growth projections ("$350B by 2027")
- Comparative performance claims ("3.5x conversion rate")
- Causal claims ("AI agents reduce onboarding time")
- Named benchmarks or industry norms ("80% of data is unstructured")
- ROI or cost figures attributed to a pattern or practice
- Research-backed behavioral claims ("customers who receive X do Y")

**Exclude:**
- Pure opinions or strategic intent ("Zava believes...")
- Internal company-specific facts that are self-reported ("Zava's team grew 22%")
- Definitions or explanations ("AI agents are systems that...")
- Transitional or framing language ("This brief outlines our plan to...")

**Edge case — internal estimates:** If the document attributes a figure to an internal audit or
internal analysis (e.g., "our internal data shows $4.2M"), flag it as an assertion but mark it
`source_type: internal`. It still gets a record in the list — it just needs a different downstream workflow.

---

## How to Read the Document

Use `search` to locate and retrieve the document if given a file name or SharePoint path.
Use `grep` to scan for assertion signal words when the document is long:

> **When to use grep vs. search:**
> - Use **grep** when scanning for specific patterns in a known document — numbers, percentages,
>   claim keywords like "reduces," "improves," "projects," "estimated." Grep is fast and precise
>   for structured pattern-matching within content you already have.
> - Use **search** when locating a document, retrieving content from SharePoint/OneDrive, or
>   looking up something by topic across a library. Search is broad; grep is targeted.

Good grep patterns for assertion hunting:
```
\d+%                → percentages
\$[\d,.]+           → dollar figures
\dx                 → multipliers (3x, 2.5x)
\b(by|reach|grow|reduce|improve|increase|decrease)\b   → directional claims
\b(project|estimate|forecast|expect|predict)\b          → forward-looking claims
```

---

## Record ID Assignment

Each assertion gets a unique Record ID before being written to the list.

Determine the ID format from context:

| Document type | Format | Example |
|---|---|---|
| Financial / earnings | `FY{YY}Q{N}-{NNN}` | `FY24Q3-001` |
| Strategy brief | `{ORG}-{YEAR}-{NN}` | `ZAVA-2025-01` |
| Generic | `{DOC-PREFIX}-{NNN}` | `BRIEF-001` |

If the user hasn't specified a format, ask:
> "What prefix should I use for the Record IDs? (e.g., ZAVA-2025 → ZAVA-2025-01, ZAVA-2025-02...)"

Assign IDs sequentially starting at 001. Check the existing list for the highest current ID to
avoid collisions when appending to an existing list.

---

## Writing Records to the SharePoint List

For each assertion, create a new list item with:

- **Record**: The assigned ID (e.g., `ZAVA-2025-01`)
- **Statements**: The verbatim or near-verbatim assertion text. Do not paraphrase — preserve exact numbers and wording.
- **Citations**: Leave blank. The Citation Finder will populate this field.

### REST API — Add Item

```http
POST https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getByTitle('Assertion Citations')/items
Authorization: Bearer {token}
Content-Type: application/json

{
  "__metadata": { "type": "SP.Data.Assertion_x0020_CitationsListItem" },
  "Title": "ZAVA-2025-01",
  "Statements": "The global athletic apparel market will reach $350 billion by 2027, with AI-personalized retail capturing 28% of total online sales.",
  "Citations": ""
}
```

### PnP PowerShell — Add Item

```powershell
Add-PnPListItem -List "Assertion Citations" -Values @{
  "Title"      = "ZAVA-2025-01"
  "Statements" = "The global athletic apparel market will reach $350 billion by 2027..."
  "Citations"  = ""
}
```

Write all assertions before handing off — do not wait for citations to populate records one at a time.

---

## Quality Checks Before Writing

1. **No duplicates** — if the same statistic appears twice, list it once and note "appears in multiple locations" in the Statements field.
2. **Exact numbers preserved** — never round or paraphrase a figure.
3. **Internal vs. external noted** — append `[Internal estimate]` to Statements text for internal-source claims.
4. **Count is plausible** — a 1-page brief typically yields 5–12 assertions. A full white paper, 20–40.

---

## Handoff to Citation Finder

After all records are written, confirm the count with the user and say:

> "I've added [N] assertion records to the Assertion Citations list. Ready to find citations? The Citation Finder will search the document corpus and fill in the Citations column for each record."

Pass the list URL and the list of Record IDs to the Citation Finder.
