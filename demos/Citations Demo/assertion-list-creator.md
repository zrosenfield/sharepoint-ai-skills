---
name: assertion-list-creator
description: >
  Creates a SharePoint list to store assertions and their citations, with columns for Record ID,
  Statements, and Citations. Use this skill whenever someone wants to "create the citation list,"
  "set up the assertion tracker," "make a SharePoint list for citations," "initialize the citation
  database," or is setting up the infrastructure for a citation pipeline. This skill creates the
  list once; the Assertion Extractor and Citation Finder skills then write into it. Trigger at the
  start of any Zava-style citation demo workflow, or any time a user needs a persistent store for
  assertion + citation records backed by SharePoint.
---

# Assertion List Creator

Creates a SharePoint list with three columns — **Record**, **Statements**, and **Citations** —
structured to store assertion records produced by the Assertion Extractor and populated by
the Citation Finder. The Citations column is configured as a multi-line text field to support
unlimited citation length.

---

## List Schema

| Column | Type | Notes |
|--------|------|-------|
| **Record** | Single line of text (Title) | The assertion ID — e.g., `FY24Q3-001`, `ZAVA-2025-A1`. This is the list's built-in Title field, renamed. |
| **Statements** | Multiple lines of text | The verbatim assertion text. Plain text, no rich formatting needed. |
| **Citations** | Multiple lines of text (enhanced) | Structured citation block. Must support unlimited length — configure as `numberOfLines: 100` and `richText: false`. Each citation is a numbered entry with document name and URL. |

> **Why multiple lines for Citations?**
> A single assertion may have 3–5 supporting documents, each with a document name and a full
> SharePoint URL. Standard single-line fields truncate at 255 characters. The Citations field
> must be configured as multi-line to hold the full citation block without truncation.

---

## Creation Method

Use the SharePoint REST API or PnP PowerShell. Choose based on what's available in the environment.

### Option A — SharePoint REST API (preferred for agent workflows)

```http
POST https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists
Authorization: Bearer {token}
Content-Type: application/json

{
  "__metadata": { "type": "SP.List" },
  "BaseTemplate": 100,
  "Title": "Assertion Citations"
}
```

Then add columns:

```http
POST https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getByTitle('Assertion Citations')/fields
Content-Type: application/json

{
  "__metadata": { "type": "SP.FieldMultiLineText" },
  "Title": "Statements",
  "FieldTypeKind": 3,
  "NumberOfLines": 10,
  "RichText": false
}
```

```http
POST .../fields
{
  "__metadata": { "type": "SP.FieldMultiLineText" },
  "Title": "Citations",
  "FieldTypeKind": 3,
  "NumberOfLines": 100,
  "RichText": false
}
```

Then add both fields to the default view:

```http
POST .../views/getByTitle('All Items')/viewfields/addviewfield('Statements')
POST .../views/getByTitle('All Items')/viewfields/addviewfield('Citations')
```

### Option B — PnP PowerShell

```powershell
Connect-PnPOnline -Url "https://{tenant}.sharepoint.com/sites/{site}" -Interactive

New-PnPList -Title "Assertion Citations" -Template GenericList

Add-PnPField -List "Assertion Citations" -DisplayName "Statements" `
  -InternalName "Statements" -Type Note -AddToDefaultView

Add-PnPField -List "Assertion Citations" -DisplayName "Citations" `
  -InternalName "Citations" -Type Note -AddToDefaultView

# Note field (SP type "Note") = multi-line text. No character limit.
```

### Option C — SharePoint UI (manual fallback)

If running as a demo without API access:
1. Create a new list: **New > List > Blank list**, name it "Assertion Citations"
2. Rename the **Title** column to **Record**
3. Add column → **Multiple lines of text** → Name: "Statements" → Plain text
4. Add column → **Multiple lines of text** → Name: "Citations" → Plain text → set to 100 lines

> **Critical:** Do not use "Single line of text" for Citations. It will silently truncate long citation blocks.

---

## Record ID Format

The **Record** field uses a structured ID. Choose the format that matches the document context:

| Context | Format | Example |
|---------|--------|---------|
| Financial / earnings doc | `FY{YY}Q{N}-{NNN}` | `FY24Q3-001` |
| Strategy brief | `{ORG}-{YEAR}-{NN}` | `ZAVA-2025-A1` |
| Generic | `{DOC-PREFIX}-{NNN}` | `BRIEF-001` |

IDs are assigned sequentially by the Assertion Extractor when it writes records to the list.

---

## Citations Field Format

Each citation entry in the Citations field follows this structure:

```
{N}. {Document Name}
   {SharePoint URL or file path}
   Support: {Direct | Partial | Indirect | Contradicts | Not Found}
   Passage: "{key supporting text}"
```

Example populated Citations field value:

```
1. Q3_FY24_ML_SANE_IR_Data_Pack.xlsx
   https://microsoft.sharepoint.com/sites/finance/docs/Q3_FY24_ML_SANE_IR_Data_Pack.xlsx
   Support: Direct
   Passage: "Revenue of $61.9 billion, a 17% increase year-over-year"

2. Q3 FY24 Momentum Package.pptx
   https://microsoft.sharepoint.com/sites/finance/docs/Q3_FY24_Momentum_Package.pptx
   Support: Direct
   Passage: "Q3 revenue growth of 17%, driven by Cloud and AI segments"

3. FY24-Q3 Momentum Backup Docs.zip
   https://microsoft.sharepoint.com/sites/finance/docs/FY24-Q3_Backup.zip
   Support: Partial
   Passage: "Quarterly revenue exceeded analyst estimates by 2.1%"
```

The multi-line field holds this entire block without truncation, regardless of how many citations are present.

---

## Verifying the List is Ready

After creation, confirm:
- [ ] List exists and is accessible at the expected URL
- [ ] Three columns are visible in the default view: Record, Statements, Citations
- [ ] Citations column is type "Multiple lines of text" (not single line)
- [ ] A test record can be added with a long Citations value (>500 chars) without truncation

Once confirmed, the list is ready to receive records from the Assertion Extractor and Citation Finder skills.

---

## Handoff

After creating the list, tell the user:

> "The Assertion Citations list is ready at [list URL]. Run the Assertion Extractor on your document to populate it with records, then run the Citation Finder to fill in the Citations column."
