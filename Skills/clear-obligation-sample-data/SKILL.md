---
name: clear-obligation-sample-data
description: Removes the fictional sample data from an Obligation Hub site after explicit confirmation. Finds obligations and contracts marked IsSample = Yes, sample Evidence files and Run Log rows whose Details start with "Demo seed", shows the counts, then deletes the list items and sends the files to the recycle bin. Never touches rows that aren't marked as sample, and writes one Run Log row. Use when asked to "remove the sample data", "clear the demo data" or "start fresh with real contracts".
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Clear obligation sample data

Take the hub's fictional sample out so the site holds only real work. The lists, views, settings, routing rules, types and skills stay. This is an unofficial community sample, not a Microsoft template.

## What counts as sample data
Only these. Anything else is real and stays, even if it looks like a demo.

| Where | Sample when | Action |
|---|---|---|
| Obligations | `IsSample` = Yes | Delete the list item (it goes to the site recycle bin) |
| Contracts | `IsSample` = Yes | Delete the file (recycle bin) |
| Evidence | `IsSample` = Yes, if the library has that column. If it doesn't, a file counts only when the `Evidence` field of a sample obligation links to it and no other obligation links to it | Delete the file (recycle bin) |
| Run Log | `Details` starts with "Demo seed" | Delete the list item (recycle bin) |

Not sample data, never touched: Obligation Owners rules, Obligation Types rows, Exclusions rows, AgentAssets (skills, `SHAREPOINT.md`, `Config/hub-settings.json`), the pages, and the lists and libraries themselves.

## Steps
1. **Find (read only).** Read the four places above and collect each match's ID, title or file name. Page through whole lists. Also note:
   - Obligations that aren't sample (`IsSample` not Yes) but whose `ContractName` is a sample contract's file name. People may have added them by hand; they stay.
   - How many non-sample items each place holds, so the user sees what stays.
2. **Show the counts** in one table: Where | Sample to remove | Stays (not sample) | Examples (up to 3 titles or file names). Add one line for the obligations that stay but refer to sample contracts. If nothing is sample, say "No sample data found on this site.", log Skipped (step 5) and stop.
3. **Confirm explicitly.** Ask: "Remove these N sample items and files? Reply **remove sample data** to confirm." Go ahead only on that reply or a similarly unambiguous yes. If the user says no, stop without logging. Never take a general "yes" given earlier in the chat as this confirmation.
4. **Remove, in this order**, checking each match again just before removing it (`IsSample` still Yes, or `Details` still starts with "Demo seed"; skip it otherwise):
   1. Obligations sample items, in batches.
   2. Evidence sample files.
   3. Contracts sample files. Deleting a file doesn't start the Capture workflows.
   4. Run Log sample rows.

   If a removal fails, note it and carry on. Don't retry more than once.
5. **Log.** Write one Run Log row:
   - `Title` = "Clear sample data - <today>"
   - `Workflow` = Setup
   - `Outcome`: Succeeded; Partial if any removal failed; Skipped if nothing was sample
   - `ItemsCreated` = 0
   - `ItemsUpdated` = the number of items and files removed
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details` (≤ 1,000 characters): "Removed sample data: X obligations, Y contracts, Z evidence files, W Run Log rows. Kept: N non-sample obligations (M refer to sample contracts). Failures: …". Never start Details with "Demo seed".
6. **Confirm in two lines**: what was removed, and "Removed items are in the site recycle bin and can be restored from there for a limited time." If Obligation Owners still holds demo routing rules, mention that the site owner may want to review them.

## Never
- Remove anything that isn't marked as sample under the table above, including items whose title or counterparty looks like sample data.
- Delete lists, libraries, columns, views, quick steps, pages, skills or the settings file.
- Empty the recycle bin.
- Edit any remaining item.
- Send email or Teams messages.
