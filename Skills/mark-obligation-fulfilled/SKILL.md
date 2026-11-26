---
name: mark-obligation-fulfilled
description: Marks one obligation on an Obligation Hub site fulfilled, records the evidence (a link, an uploaded file or none), creates the next occurrence for recurring items and writes one Run Log row. Use from the Mark fulfilled quick step on an Obligations item, or when asked to mark a named obligation fulfilled ("mark the insurance certificate fulfilled").
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Mark obligation fulfilled

Close one obligation, keep the proof with it, and line up the next occurrence so the daily sweep doesn't have to.

## Inputs
- **The item.** Use the Obligations item the quick step ran on. In chat, find it by what the user said (title words, counterparty, clause). If more than one open item matches, list up to 5 (`Title` – `DueDate` – `Counterparty`) and ask which one.
- **Evidence and date.** If the user gave evidence or a date ("sent on Nov 20") in the request, use it and don't ask again.
- **Config** `AgentAssets/Config/hub-settings.json`: `siteUrl`, `timeZone`.

## Steps
1. **Check the status.** If `Status` is already Fulfilled, reply "Already fulfilled on <FulfilledOn>." Log Skipped and stop. If `Status` is Waived or Not applicable, confirm before changing it.
2. **Ask for evidence once.** Ask only if the user hasn't given it: "Evidence? Paste a link, attach a file, or say none."
   - **A file:** upload it to the Evidence library as `<ID>-<YYYY-MM-DD>-<original name>`, set its `Title` to "Evidence: <obligation Title>" (and its `IsSample` to the item's `IsSample`, if the library has that column), and use its URL.
   - **A link:** use it as given.
   - **None:** leave `Evidence` empty.
3. **Update the item:**
   - `Status` = Fulfilled
   - `FulfilledOn` = the date the user gave, otherwise today in `timeZone`
   - `Evidence` = the URL, with the description "Evidence"
   - `Timing` = Closed
   - `ReviewState` = Confirmed
4. **Create the next occurrence** if `Recurrence` ≠ None. Use the same rule as `sweep-obligations` so the daily sweep finds this successor and doesn't create a duplicate.
   - **Base key**: `CaptureKey` without any "#…" suffix. If `CaptureKey` is empty, use `item-<ID>`.
   - **Next due date**: apply the schedule in `ObligationText` to the period after this item's `DueDate`. If the text states no schedule, add one interval: Weekly +7 days, Monthly +1 month, Quarterly +3 months, Semi-annual +6 months, Annual +1 year. Keep the same day of the month, or use the month's last day if that day doesn't exist.
   - **Skip** it if `ObligationText` says "Through <date>" or "Last due <date>" and the next date is later than that date.
   - **Skip** it if a successor already exists: an item with `CaptureKey` = `<base>#<next date>`, or an open item in the same series with a later `DueDate`.
   - **Otherwise create the successor.**
     - Copy these fields: `Title`, `ContractName`, `ContractLink`, `Counterparty`, `ObligationText`, `ClauseRef`, `SourceClause`, `Party`, `Category`, `TriggerType`, `Recurrence`, `TriggerEvent`, `Owner`, `EscalationOwner`, `BusinessUnit`, `ReviewState`, `Confidence`, `Risk` and `IsSample`.
     - Set:
       - `DueDate` = the next date
       - `Status` = Not started
       - `Timing` = computed
       - `CaptureKey` = `<base>#<next date>`
       - `Notes` = "Next occurrence after #<ID>"
     - Leave `FulfilledOn`, `Evidence` and `LastReminded` empty.
5. **Log.** Write one Run Log row:
   - `Title` = "Mark fulfilled - #<ID>"
   - `Workflow` = Mark fulfilled
   - `Outcome`: Succeeded, Partial, Failed or Skipped
   - `ItemsUpdated` = 1
   - `ItemsCreated` = 0 or 1
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details` = "<Title>; evidence: link / file / none; next: #<new ID> <date>"
6. **Confirm in one line**, for example: "Marked 'Send customer COI by Dec 15' fulfilled on 2026-11-24 (evidence attached). Next occurrence due 2027-12-15 (#58)."

## Writes
- The selected Obligations item: `Status`, `FulfilledOn`, `Evidence`, `Timing`, `ReviewState`.
- At most one new Obligations item (the next occurrence).
- At most one file in Evidence.
- Run Log: one row.

## Never
- Mark more than the one item the user chose, or change its other fields.
- Edit a previous occurrence's history.
- Send messages.
