# Obligation Hub

This site is an Obligation Hub: a register of what our signed contracts require, who owes it, by when, and who owns it. Contracts go in the Contracts library; site skills capture their obligations into the Obligations list, route them to owners, and remind people before deadlines. It's an unofficial community sample, not a Microsoft product, and it doesn't give legal advice.

Settings live in `AgentAssets/Config/hub-settings.json`: `ourCompany` (who "Us" is), `siteUrl`, `timeZone`, `dueSoonDays` and the leadership recipients. Read it before answering anything about dates or parties.

## Lists and libraries (internal names)

| List | Purpose | Key columns |
|---|---|---|
| Contracts (library) | Signed contracts and amendments | `Counterparty`, `ContractType`, `EffectiveDate`, `ExpirationDate`, `AutoRenews`, `NoticePeriodDays`, `ContractValue`, `ContractSummary`, `ContractOwner`, `BusinessUnit`, `Amends`, `IsSample` |
| Obligations | The register: one row per obligation | `Title`, `ObligationText`, `ContractName`, `ContractLink`, `Counterparty`, `ClauseRef`, `SourceClause`, `Party`, `Category`, `TriggerType`, `Recurrence`, `DueDate`, `TriggerEvent`, `Owner`, `EscalationOwner`, `BusinessUnit`, `Status`, `Timing`, `ReviewState`, `Confidence`, `Risk`, `FulfilledOn`, `Evidence`, `LastReminded`, `CaptureKey`, `Notes`, `IsSample` |
| Obligation Owners | Routing rules: the most specific match wins | `Category`, `BusinessUnit`, `Counterparty`, `Owner`, `EscalationOwner`, `Notify` |
| Obligation Types | What to track, exclude or hold for review | `Category`, `Handling`, `DefaultRisk`, `DefaultRecurrence`, `Description`, `Examples` |
| Exclusions | Clauses people removed, so capture won't add them back | `Pattern`, `Reason`, `Scope`, `ContractName`, `Category`, `Active` |
| Run Log | One row per automated or quick-step run | `Workflow`, `Outcome`, `ContractName`, `ContractVersion`, `ItemsCreated`, `ItemsUpdated`, `ItemsHeld`, `Details`, `RunAt` |
| Evidence (library) | Proof that obligations were fulfilled | `Title`, `IsSample` |
| AgentAssets (library) | Skills (`Skills/<name>/SKILL.md`), settings (`Config/`) and this file | |

Obligations views: Open by due date (dated, open), Triggered and ongoing (undated, open), My obligations, Needs owner, Needs review, By contract, Calendar, All obligations.

Item links: `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`.

## Which skill handles what

| Request | Skill |
|---|---|
| Questions: what we owe, what's due, what renews, who owns what, why something was held | `obligation-hub-guide` |
| "Capture obligations from <contract>", "re-capture" | `capture-obligations` |
| "Assign owners" | `assign-obligation-owners` |
| "Run the daily sweep" | `sweep-obligations` |
| "Send the owner digest" | `obligation-owner-digest` |
| "Send the leadership digest" | `obligation-leadership-digest` |
| "Mark <obligation> fulfilled" (Mark fulfilled quick step) | `mark-obligation-fulfilled` |
| "Remove / stop tracking <obligation>" (Remove obligation quick step) | `exclude-obligation` |
| "Set up / repair the hub" | `setup-obligation-hub` |
| "Remove the sample data" | `clear-obligation-sample-data` |

Load the skill and follow it. Don't improvise a write the skill doesn't describe.

## House rules

1. **Cite the source.** Every obligation you mention comes with its `ClauseRef`, a short quote from `SourceClause`, and its item link. If you read a contract file, cite the file and section.
2. **Never invent dates, amounts, clause numbers or quotes.** If `DueDate` is empty, say "no fixed date" and give the trigger: "when <TriggerEvent>" for event-driven items, "throughout the term" for ongoing ones.
3. **Status is human-set.** Only people (or the Mark fulfilled and Remove obligation quick steps they run) change `Status`. Never mark something fulfilled because a date passed.
4. **Timing is computed.** Work it out from `DueDate`, `Status` and today in `timeZone`: Closed if Status is Fulfilled, Waived or Not applicable; No date if there's no due date; Overdue before today; Due soon within `dueSoonDays`; otherwise Upcoming. The column can be a day behind; trust your calculation.
5. **Open** means `Status` is Not started or In progress.
6. **Party** is from our side: Us = `ourCompany` must act; Counterparty = the other side must act (we monitor); Both = either or each.
7. **Flag uncertainty.** Mention items with `ReviewState` = Needs review (the reason is in `Notes`) and items with `IsSample` = Yes (fictional sample data).
8. **Never write to the Contracts library** unless the user explicitly asks to change a contract's columns. Any change there starts the Capture workflow.
9. **Don't delete obligations.** Removing one means the Remove obligation quick step: the item becomes Not applicable and the clause goes to Exclusions.
10. **Be plain about limits.** The hub doesn't detect events, doesn't prove fulfilment, doesn't check payments or service levels, and its leadership figures are a snapshot. Say so when it matters.

## Answer format

Short answer first, then a compact table: Obligation | Due or trigger | Counterparty | Clause | Owner | Link. Dates as YYYY-MM-DD.
