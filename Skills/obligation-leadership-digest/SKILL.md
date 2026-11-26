---
name: obligation-leadership-digest
description: Sends a weekly, read-only leadership summary of an Obligation Hub's register by email (and optionally a Teams channel). Covers counts by timing, top overdue items, notice deadlines in the next 120 days, unowned and held items, and items fulfilled this week, and writes one Run Log row. Use for the Leadership digest AI workflow (Fridays 3:00 PM) or when asked for the "leadership digest".
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Obligation leadership digest

A weekly snapshot for leadership, built only from counts and items in the lists. It's a snapshot, not a trend report.

## Inputs
- **Config** `AgentAssets/Config/hub-settings.json`: `siteUrl`, `timeZone`, `dueSoonDays`, `leadershipRecipients`, `leadershipTeamsChannel` (optional `team` and `channel`). If there are no recipients and no channel, log Failed ("no leadership recipients configured") and stop.
- **Obligations**: all items. Fields: `ID`, `Title`, `Counterparty`, `ContractName`, `Party`, `Category`, `DueDate`, `Status`, `ReviewState`, `Risk`, `Owner`, `FulfilledOn`, `ClauseRef`, `IsSample`.
- **Contracts** columns only: `Counterparty`, `ExpirationDate`, `AutoRenews`, `NoticePeriodDays`, `IsSample`. Never read contract text.
- **Run Log**: today's rows where `Workflow` = Leadership digest.

## Steps
1. **Check for a run today.** If a Succeeded Leadership digest row already exists for today and nobody asked for a resend, log Skipped and stop.
2. **Work out Timing.** Compute it fresh from `DueDate` and today; don't trust the column. Open means `Status` is Not started or In progress.
3. **Build these sections, in this order.** Use only counts and items taken from the lists. Don't add percentages, trends, scores, dollar exposure or forecasts.
   1. **At a glance.** Count open items as Overdue, Due soon, Upcoming and No date. Add the number of items needing review and the number fulfilled this week.
   2. **Overdue.** Show the top 10, sorted by `Risk` (High, Medium, Low) and then by days overdue, most first. Each line: `Title`, `Counterparty`, owner (or "No owner"), days overdue, link.
   3. **Notice deadlines, next 120 days.** List open items where `Category` = Notice & renewal and `DueDate` falls between today and today + 120. Each line: `Counterparty`, the action (`Title`), the deadline, the owner and a link. Sort by deadline. Then add "Expiring with no tracked decision": contracts whose `ExpirationDate` falls in the same window and that have no open Notice & renewal item with the same counterparty.
   4. **No owner.** Count open items with `ReviewState` = Confirmed and an empty `Owner`. List up to 10.
   5. **Needs review.** Count open items with `ReviewState` = Needs review. List the 5 oldest.
   6. **Fulfilled this week.** List items whose `FulfilledOn` falls in the last 7 days, up to 10.
4. **Format each line.** Link each item as `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`. If any listed item has `IsSample` = Yes, start the message with "Includes sample data."
5. **Send.**
   - Email `leadershipRecipients` with the subject "Obligation Hub, week of <date>: X overdue, Y notice deadlines in 120 days".
   - If a Teams channel is configured, post the same content there, shortened to the At a glance section, the top 5 overdue items and the top 5 notice deadlines, plus a link.
6. **Log.** Write one Run Log row:
   - `Title` = "Leadership digest - <today>"
   - `Workflow` = Leadership digest
   - `Outcome`: Succeeded, Partial, Failed or Skipped
   - `ItemsCreated`, `ItemsUpdated` and `ItemsHeld` = 0
   - `RunAt` = now
   - `Details`: the At a glance counts and the recipients.

## Writes
- One email to the leadership recipients, and optionally one Teams channel post.
- Run Log: exactly one row.

## Never
- Update any obligation or contract. This skill is read-only apart from its Run Log row.
- Invent metrics, or estimate dates for items that have no `DueDate`.
- Read contract files.
