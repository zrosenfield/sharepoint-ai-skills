---
name: citation-finder
description: >
  Searches a library of source documents to find citations that support, partially support, or contradict
  each assertion — then writes the results back into the Citations column of the SharePoint Assertion
  Citations list. Use this skill whenever someone asks to "find sources for this claim," "cite this
  assertion," "verify this statistic," "what backs this up," "does our corpus support this?" "populate
  the citations," or is running a citation pipeline against a document library. Trigger when the
  Assertion Extractor has finished writing records and the user wants to fill in the Citations column.
  Designed for the Zava demo scenario and SharePoint AI workflows where source documents live in
  SharePoint, OneDrive, or a local document corpus.
---

# Citation Finder

Reads assertion records from the SharePoint Assertion Citations list, searches a source document
library to find supporting evidence for each claim, and writes structured citation blocks back into
the Citations column of each record.

---

## Inputs

You will receive one or more of the following:
1. **A SharePoint list URL** — read all records with empty Citations fields
2. **A list of Record IDs** — process only those records (e.g., `ZAVA-2025-01, ZAVA-2025-03`)
3. **A single assertion** — a verbatim claim passed directly (no list lookup needed)
4. **Source library location** — SharePoint folder, OneDrive path, or local corpus directory

If the source library location is not specified, ask:
> "Where is the source document library? (e.g., a SharePoint folder path, OneDrive location, or list of filenames)"

---

## Reading Records from the List

Fetch assertion records that need citations:

```http
GET https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getByTitle('Assertion Citations')/items
  ?$select=ID,Title,Statements,Citations
  &$filter=Citations eq ''
Authorization: Bearer {token}
```

Or via PnP PowerShell:
```powershell
Get-PnPListItem -List "Assertion Citations" `
  -Fields "Title","Statements","Citations" |
  Where-Object { $_["Citations"] -eq $null -or $_["Citations"] -eq "" }
```

This retrieves only unpopulated records, making the skill safe to re-run without overwriting existing citations.

---

## Search Strategy: grep vs. search

This is the most important judgment call in this skill.

> ### When to use **grep**
> Grep is your first move for **quantitative assertions**. If the claim contains a specific number,
> percentage, dollar figure, or multiplier — grep for it directly in the corpus.
> It is fast, exact, and will immediately confirm or rule out a direct match.
>
> **Use grep when:** The assertion contains `\d+%`, `\$[\d,]+`, `\d+x`, or a specific named figure.
>
> Example: Assertion is "reduces inventory by 31%"
> → `grep -i "31%" corpus/` — fast, high precision.
>
> ### When to use **search**
> Search is your move for **conceptual or causal assertions** — claims about behavior, trends, or
> relationships that won't be expressed in identical words across documents.
>
> **Use grep first, then search if grep returns nothing or only partial matches.**
>
> Example: Assertion is "AI agents reduce onboarding time for customer-facing roles"
> → grep for "onboarding" first; if the passage is too vague, follow with search using
> `"AI onboarding productivity customer-facing"` to surface semantically related content.
>
> ### The Two-Pass Rule
> Always run grep first. If grep gives a strong hit (exact figure confirmed in a passage),
> you have your citation — no need to search further. If grep misses or gives weak results,
> follow up with search using 2–4 substantive keywords from the assertion.

---

## For Each Assertion: Step-by-Step

**Step 1 — Extract the searchable signal**
- Stat present → use the figure as the grep target
- No stat → identify 2–4 core keywords for search

**Step 2 — Run grep (always first for stats)**
```
grep -ri "<figure or key term>" <corpus path>
```

**Step 3 — Evaluate the hit**
- Exact figure confirmed → Direct Support candidate
- Related but different figure → Partial Support candidate
- Conflicting finding → Contradiction candidate
- No result → proceed to Step 4

**Step 4 — Run search (if grep insufficient)**
Use 2–4 substantive keywords. Avoid generic words like "study," "data," "report."
Good: `"athletic apparel market 2027"` | Bad: `"market research report"`

**Step 5 — Read the source passage in context**
Don't rely on a grep snippet alone. Read the surrounding paragraph to confirm the claim
is being made in the same direction and context as the assertion.

**Step 6 — Classify and write back**

---

## Support Level Classification

| Level | Meaning |
|---|---|
| Direct | Source contains the same figure or claim in the same direction with comparable framing |
| Partial | Source supports the general claim but with a different figure, scope, or time horizon |
| Indirect | Source supports the underlying logic but doesn't cite this specific claim |
| Contradicts | Source presents a figure or finding that conflicts with the assertion |
| Not Found | No relevant passage found in the corpus |

Default to **Partial rather than Direct** when there is any meaningful difference in scope,
date, sample size, or population. Precision matters for strategic documents.

---

## Citations Field Format

Write structured citation blocks to the Citations column. Each entry follows this format:

```
{N}. {Document Name}
   {Full URL or file path}
   Support: {Direct | Partial | Indirect | Contradicts | Not Found}
   Passage: "{key supporting text, verbatim from source}"
```

**Example Citations field value** (what gets written to the list item):

```
Supporting Documents (3):

1. Apex_Research_Athletic_Apparel_2025.docx
   https://microsoft.sharepoint.com/sites/zava/research/Apex_Research_2025.docx
   Support: Direct
   Passage: "projects the market will reach $350 billion by 2027... AI-personalized commerce representing 28% of total online athletic apparel sales"

2. Global_Retail_AI_Trends_2024.pdf
   https://microsoft.sharepoint.com/sites/zava/research/Global_Retail_AI_Trends.pdf
   Support: Partial
   Passage: "AI-driven personalization is projected to account for 25-30% of online premium apparel revenue by late 2027"
```

If no citations were found:
```
No supporting documents found in corpus.
Note: This may be an internal estimate — recommend sourcing from [department/system].
```

---

## Writing Citations Back to the List

### REST API — Update Item

```http
PATCH https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getByTitle('Assertion Citations')/items({itemId})
Authorization: Bearer {token}
Content-Type: application/json
X-HTTP-Method: MERGE
If-Match: *

{
  "__metadata": { "type": "SP.Data.Assertion_x0020_CitationsListItem" },
  "Citations": "Supporting Documents (2):\n\n1. Apex_Research_2025.docx\n   https://...\n   Support: Direct\n   Passage: \"...\""
}
```

### PnP PowerShell — Update Item

```powershell
Set-PnPListItem -List "Assertion Citations" -Identity {itemId} -Values @{
  "Citations" = "Supporting Documents (2):`n`n1. Apex_Research_2025.docx`n   https://...`n   Support: Direct`n   Passage: `"...`""
}
```

Write citations to each record as they are found — don't batch all at the end. This allows
the list to show partial progress if the run is interrupted.

---

## Handling Multiple Assertions

When processing a batch:

1. Process **quantitative assertions** first (grep is fast — clear the easy ones)
2. Process **causal/conceptual assertions** second (may require search + reading)
3. Flag **internal source-type assertions** separately — append to Citations:
   `"Note: Internal estimate. Source from internal audit, not external corpus."`
4. After all records are updated, produce a **Summary** in the conversation:

```
CITATION RUN COMPLETE — [Document Name]
Records processed: 8
Direct Support:    5
Partial Support:   1
Indirect Support:  0
Contradicts:       0
Not Found:         2  (1 internal estimate, 1 no corpus match)

All records updated in Assertion Citations list.
```

---

## Edge Cases

**No exact match but a very close figure** → Partial Support; note the discrepancy explicitly.

**Multiple corpus documents support the same assertion** → List all supporting documents;
lead with the strongest citation.

**Source contradicts the assertion** → Always surface contradictions even if support exists elsewhere.
List both and let the user resolve.

**Compound claim** (two stats in one sentence) → Split and evaluate each component separately.
Both must be supported for a Direct Support rating. If only one is supported, rate as Partial.

**Citations column already populated** → Skip that record unless the user explicitly asks to overwrite.
Use the filtered fetch query (empty Citations only) to avoid re-processing.
