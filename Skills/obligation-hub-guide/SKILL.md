---
name: obligation-hub-guide
description: Answers questions about an Obligation Hub site from its lists, with clause citations and links, such as what we owe a counterparty, what's due or overdue, what renews soon, which items have no owner, why an item was held, and what the hub can't do yet. Hands changes to the right hub skill. Use for any question about obligations, contracts, deadlines, owners or the hub itself on this site.
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Obligation Hub guide

Answer from the lists. They are the register. Read a contract file only when the answer needs wording the register doesn't hold, and then cite the file and section. The hub records what contracts say; it doesn't give legal advice.

## Where things are (internal names)
- **Obligations**: one row per obligation.
  - `Title`, `ObligationText`
  - `ContractName` (the file name) and `ContractLink`
  - `Counterparty`
  - `Party`: Us, Counterparty or Both
  - `Category`
  - `TriggerType`: Fixed date, Recurring, Event-driven or Ongoing
  - `Recurrence`, `DueDate`, `TriggerEvent`
  - `Owner`, `EscalationOwner`, `BusinessUnit`
  - `Status`: Not started, In progress, Fulfilled, Waived or Not applicable
  - `Timing`
  - `ReviewState`: Confirmed or Needs review
  - `Confidence`, `Risk`
  - `ClauseRef`, `SourceClause`
  - `FulfilledOn`, `Evidence`, `LastReminded`, `CaptureKey`, `Notes`, `IsSample`
- **Contracts** (library): `Title`, `Counterparty`, `ContractType`, `EffectiveDate`, `ExpirationDate`, `AutoRenews`, `NoticePeriodDays`, `ContractValue`, `ContractSummary`, `ContractOwner`, `BusinessUnit`, `Amends`.
- **Obligation Owners**: routing rules.
- **Obligation Types**: what's tracked, excluded or held.
- **Exclusions**: clauses people removed.
- **Run Log**: automated runs.
- **Evidence**: proof files.
- **Settings**: `AgentAssets/Config/hub-settings.json`. It holds `ourCompany` ("Us"), `dueSoonDays` and `timeZone`.

## Rules
- **Today** is the date in `timeZone`.
- **Open** means `Status` is Not started or In progress. Superseded or excluded items are Not applicable. Their `Notes` say why.
- **Timing.** Compute it yourself; the column can be a day behind.
  - Closed if `Status` is Fulfilled, Waived or Not applicable
  - No date if there's no `DueDate`
  - Overdue if `DueDate` < today
  - Due soon if `DueDate` ≤ today + `dueSoonDays`
  - Otherwise Upcoming
- **Never invent or estimate a date.** If `DueDate` is empty, say "no fixed date" and give the trigger: "when <TriggerEvent>" for event-driven items, "throughout the term" for ongoing ones.
- **Cite every obligation** with its `ClauseRef`, a short quote from `SourceClause`, and a link: `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`.
- **Flag** items with `ReviewState` = Needs review (the reason is in `Notes`) and items with `IsSample` = Yes.
- **Format.** Give the short answer first, then a compact table: Obligation | Due or trigger | Counterparty | Clause | Owner | Link.

## Common questions
- **"What do we owe <X>?"** Open items where `Counterparty` matches X and `Party` = Us or Both. List dated items by `DueDate` first, then event-driven and ongoing items.
- **"What does <X> owe us?"** The same, with `Party` = Counterparty or Both.
- **"What's due this week / overdue?"** Open, dated items, filtered by computed Timing or a date range.
- **"What auto-renews or needs a renewal decision in 120 days?"** Open items where `Category` = Notice & renewal and `DueDate` is within 120 days. The `DueDate` is the last day to act. Add contracts whose `ExpirationDate` falls in that window, noting `AutoRenews`. For auto-renewing contracts, `ExpirationDate` can show the initial term, so prefer the obligation's date.
- **"Which have no owner?"** Open items with `ReviewState` = Confirmed and an empty `Owner`. Mention separately that held items aren't assigned until someone confirms them.
- **"Why was this held / excluded / superseded?"**
  - Held, superseded or excluded items: read the item's `Notes`.
  - Clauses capture skipped: read the latest Capture Run Log row for that contract (`Details`).
  - Rules: read Exclusions.
- **"Prepare me for <X>"** Group <X>'s open items by Timing. List notice deadlines with their dates. Then list the contract's key terms from the Contracts columns.

## Say plainly what the hub doesn't do
If a question depends on these, say so in one line rather than guessing:
- **Events aren't detected.** Event-driven and ongoing items have no date, and nothing watches for the triggering event (a breach, a change of control, a delivery). Someone has to notice it.
- **Fulfilment isn't proven.** Evidence is optional, there's no sign-off step, and the Run Log is an editable list, not an audit trail.
- **Deadlines only.** The hub doesn't check payments against accounts payable or measure service levels.
- **Leadership figures are a snapshot.** No trends and no dollar exposure.
- **Accuracy.** Capture was measured on fictional sample contracts only. Items in Needs review need a person to confirm them.

## Hand off changes
- "Mark fulfilled" → **mark-obligation-fulfilled**
- "Remove / stop tracking" → **exclude-obligation**
- "Capture / re-capture" → **capture-obligations**
- "Assign owners" → **assign-obligation-owners**
- "Run the daily sweep" → **sweep-obligations**
- "Send the owner digest" → **obligation-owner-digest**
- "Send the leadership digest" → **obligation-leadership-digest**
- "Set up / repair the hub" → **setup-obligation-hub**
- "Remove the sample data" → **clear-obligation-sample-data**

Don't edit items directly while answering a question.
