---
name: sweep-obligations
description: Performs the daily maintenance of an Obligation Hub's Obligations list. Refreshes the computed Timing column, creates the next occurrence of fulfilled recurring items, reminds owners of items coming due, escalates overdue ones and writes one Run Log row. Reads the list only, never the contracts. Use for the Daily sweep AI workflow (6:00 AM) or when asked to "run the daily sweep" or "sweep the obligations".
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Sweep obligations

Keep the register current without reading a single contract: Timing, next occurrences, reminders and escalations. Runs unattended each morning (the "Daily sweep" workflow) or in chat. Safe to run twice.

## Inputs
- **Config** `AgentAssets/Config/hub-settings.json`: `siteUrl`, `timeZone`, `dueSoonDays` (14), `escalateAfterDaysOverdue` (0), `reminderCooldownDays` (3, minimum 1), `notifyDefault` (Both). If the file is missing, use these defaults and note it in Details.
- **Obligations**: all items, but read only the fields used here: `ID`, `Title`, `Status`, `DueDate`, `Timing`, `TriggerType`, `Recurrence`, `CaptureKey`, `Owner`, `EscalationOwner`, `ReviewState`, `LastReminded`, `Counterparty`, `ClauseRef`, `FulfilledOn` and `ObligationText`. Page through the whole list.
- **Obligation Owners** `Notify`. Read it only to choose each person's channel: use the `Notify` of the rules that name the person, Both if those rules disagree, and `notifyDefault` if no rule names them. **Never read Contracts.**

"Today" is the current date in `timeZone`. Open means `Status` is Not started or In progress.

## Steps
1. **Timing.** For every item, compute:
   - Closed if `Status` is Fulfilled, Waived or Not applicable
   - Otherwise No date if there's no `DueDate`
   - Overdue if `DueDate` < today
   - Due soon if `DueDate` ≤ today + `dueSoonDays`
   - Otherwise Upcoming

   Batch-update only the items whose `Timing` changed.
2. **Roll forward.** Handle each item where `Recurrence` ≠ None and `Status` = Fulfilled or Waived (waiving one occurrence does not end the duty; Not applicable does, so never roll it forward):
   - **Base key**: `CaptureKey` without any "#…" suffix. If `CaptureKey` is empty, use `item-<ID>`.
   - **Next due date**: apply the schedule in `ObligationText` to the period after this item's `DueDate`. For example, "within 45 days after each quarter end" gives 45 days after the next quarter end. If the text states no schedule, add one interval:
     - Weekly: +7 days
     - Monthly: +1 month
     - Quarterly: +3 months
     - Semi-annual: +6 months
     - Annual: +1 year

     Keep the same day of the month, or use the month's last day if that day doesn't exist.
   - **Skip** the item if `ObligationText` says "Through <date>" or "Last due <date>" and the next date is later than that date.
   - **Skip** the item if a successor already exists: an item with `CaptureKey` = `<base>#<next date>`, or any open item in the same series (key = base, or starting with base + "#") with a later `DueDate`.
   - **Otherwise create the successor.**
     - Copy these fields: `Title`, `ContractName`, `ContractLink`, `Counterparty`, `ObligationText`, `ClauseRef`, `SourceClause`, `Party`, `Category`, `TriggerType`, `Recurrence`, `TriggerEvent`, `Owner`, `EscalationOwner`, `BusinessUnit`, `ReviewState`, `Confidence`, `Risk` and `IsSample`.
     - Set:
       - `DueDate` = the next date
       - `Status` = Not started
       - `Timing` = computed
       - `CaptureKey` = `<base>#<next date>`
       - `Notes` = "Next occurrence after #<ID>"
     - Leave `FulfilledOn`, `Evidence` and `LastReminded` empty.
     - Never edit the fulfilled item.
3. **Remind owners.** Pick open items where all of these are true:
   - `ReviewState` = Confirmed
   - `Timing` = Due soon
   - `Owner` is set
   - `LastReminded` is empty or earlier than `DueDate` − `dueSoonDays`

   Send each owner ONE message titled "Coming due: N obligation(s)", soonest first.
4. **Escalate overdue items.** Pick open items where all of these are true:
   - `ReviewState` = Confirmed
   - `Timing` = Overdue
   - Days overdue ≥ `escalateAfterDaysOverdue`
   - `LastReminded` is empty, or on or before `DueDate`, or at least `reminderCooldownDays` ago

   Group the items by `EscalationOwner`, falling back to `Owner`. Send each recipient ONE message titled "Overdue: N obligation(s) need action", oldest first. On email, cc the items' owners. If an item has no owner and no escalation owner, don't send anything; count it in Details (the leadership digest lists those items).
5. **Message lines.** Each line in steps 3–4 reads: `Title` – due `DueDate` (overdue N days / in N days) – `Counterparty` – `ClauseRef` – `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`. End each message with: "Done? Open the item and use the Mark fulfilled quick step."
6. **Record reminders.** Set `LastReminded` = today on every item included in a message that was sent. Use one batch.
7. **Log.** Write one Run Log row:
   - `Title` = "Daily sweep - <today>"
   - `Workflow` = Daily sweep
   - `Outcome`: Succeeded; Partial if any write or message failed
   - `ItemsCreated` = successors
   - `ItemsUpdated` = distinct items whose `Timing` or `LastReminded` changed
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details`, for example: "Open: 4 overdue, 6 due soon, 12 upcoming, 25 no date. Timing changed 3. Rolled forward 2. Reminded 2 owners (5 items). Escalated to 1 (4 items). Overdue with no owner: 1."

Running the sweep twice on the same day changes nothing and sends nothing.

## Writes
- Obligations: `Timing`, `LastReminded`, and new successor items.
- Email and Teams messages to owners and escalation owners.
- Run Log: exactly one row.

## Never
- Read contract files or the Contracts library.
- Change `Status`, `Owner`, `DueDate`, `Notes` or any field of an existing item other than `Timing` and `LastReminded`.
- Remind or escalate items with `ReviewState` = Needs review.
- Delete anything.
