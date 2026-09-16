---
name: find-expert
description: "Matches open Knowledge Gaps items to subject matter experts in the Expert Directory and assigns them. Reads the Knowledge Gaps list for items with Status = Open, cross-references each gap's Topic against the Expert Directory's Expertise Areas, then updates assignments. Use when asked to find experts, route open questions, review unassigned gaps, or match knowledge gaps to people. Triggers include 'find an expert for this', 'who knows about X', 'assign open gaps', or 'review unassigned knowledge gaps'."
---

# Find Expert

Match open knowledge gaps to the right subject matter experts and assign them.

> **Scope:** Reads and updates SharePoint lists only. Does not write code, scripts, or formulas.

---

## Data Sources

| List | Key Columns |
|------|-------------|
| **Knowledge Gaps** | Title, Topic (e.g. "Azure AD"), Status (Open/Assigned/Resolved), Assigned Expert |
| **Expert Directory** | Name, Expertise Areas (semicolon-delimited, e.g. "Azure AD; Identity; SSO"), Department |

---

## Workflow

### Step 1 — Read open gaps

Read the Knowledge Gaps list filtered to Status = Open. Note each item's Title and Topic.

### Step 2 — Read the Expert Directory

Read the full Expert Directory list. Build a lookup of Topic → matching experts by comparing each expert's Expertise Areas to the gap Topics.

### Step 3 — Match gaps to experts

For each open gap, find experts whose Expertise Areas contain or closely match the gap's Topic.

- **Single match:** assign directly.
- **Multiple matches:** prefer the expert with the fewest existing assignments (balance workload). If still tied, pick the expert whose department is closest to the gap's origin.
- **No match:** leave unassigned and flag for the user.

### Step 4 — Apply assignments

For each matched gap, update the Knowledge Gaps list:
- Set **Assigned Expert** to the matched expert's name
- Set **Status** to Assigned

### Step 5 — Verify and report

Re-read the updated Knowledge Gaps list to confirm all intended assignments were applied. Report:

- **Matched:** list of gaps with their assigned expert
- **Unmatched:** list of gaps where no expert was found, with the Topic that had no match
- **Summary:** total gaps processed, total assigned, total remaining open
