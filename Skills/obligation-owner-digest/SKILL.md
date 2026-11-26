---
name: obligation-owner-digest
description: Sends each obligation owner on an Obligation Hub site one weekly message listing their overdue items, items due soon and items due in the next 30 days, with links and a reminder to use the Mark fulfilled quick step, and writes one Run Log row. Reads only the Obligations list. Use for the Owner digest AI workflow (Mondays 8:00 AM) or when asked to "send the owner digest".
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Obligation owner digest

One short weekly message per owner, so nobody has to open the site to know what's due.

## Inputs
- **Config** `AgentAssets/Config/hub-settings.json`: `siteUrl`, `timeZone`, `dueSoonDays` (14), `maxDigestItems` (25), `notifyDefault` (Both).
- **Obligations**: open items (`Status` = Not started or In progress) with `ReviewState` = Confirmed and `Owner` set. Fields: `ID`, `Title`, `DueDate`, `TriggerType`, `Counterparty`, `ClauseRef`, `Owner`, `LastReminded`.
- **Obligation Owners** `Notify`, to choose each owner's channel: the `Notify` of the rules that name the owner, Both if those rules disagree, and `notifyDefault` if no rule names them.
- **Run Log**: today's rows where `Workflow` = Owner digest.

## Steps
1. **Check for a run today.** If a Succeeded Owner digest row already exists for today and the user didn't ask for a resend, log Skipped ("already sent today") and stop.
2. **Sort items.** For each owner, work out Timing from `DueDate` and today, then sort the items into three sections:
   - **Overdue**: `DueDate` < today, oldest first
   - **Due soon**: due within `dueSoonDays`
   - **Next 30 days**: due after that but within 30 days of today

   Undated items (event-driven or ongoing) don't go in the sections.
3. **Cap the list.** Fill the sections in that order up to `maxDigestItems`. If items are left over, add "and N more" with a link to `<siteUrl>/Lists/Obligations`.
4. **Skip empty owners.** Don't message an owner whose three sections are all empty.
5. **Send.** Send each owner ONE message titled "Your obligations this week: X overdue, Y due soon".
   - **Each line:** `Title` – `DueDate` (overdue N days / in N days) – `Counterparty` – `ClauseRef` – `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`.
   - **Footer:**
     - "You also own N event-driven or ongoing obligations. Act when their trigger happens."
     - "Done? Open the item and choose the Mark fulfilled quick step, and add the evidence link or file."
6. **Record reminders.** Set `LastReminded` = today on the Overdue and Due soon items that were in messages actually sent. Use one batch.
7. **Log.** Write one Run Log row:
   - `Title` = "Owner digest - <today>"
   - `Workflow` = Owner digest
   - `Outcome`: Succeeded, Partial or Skipped
   - `ItemsCreated` = 0
   - `ItemsUpdated` = items whose `LastReminded` changed
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details`: "Sent to N owners (X overdue, Y due soon, Z next 30 days); skipped M owners with nothing due; failures: …"

## Writes
- Obligations: `LastReminded` only.
- One message per owner.
- Run Log: exactly one row.

## Never
- Read Contracts.
- Include held (Needs review) or closed items.
- Send more than one digest per owner per day.
- Change any other field.
