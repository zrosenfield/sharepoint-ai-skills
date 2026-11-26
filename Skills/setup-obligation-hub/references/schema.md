# Obligation Hub schema (version 1.0.0)

The lists, libraries, columns and views that `setup-obligation-hub` builds. Every hub skill reads and writes these **internal names**, so never change them. Display names can be renamed later without breaking anything.

No column is marked required: the workflows write partial rows (for example, an event-driven item has no due date). All text values below are exact; choices are case-sensitive and must be created in the order shown.

## Build plan

Create each list in one call with its columns, then add its views in a **separate** call. One call with many columns and views failed with "too many stages".

| Order | List or library | Template | Navigation link | Description (use as the list description) |
|---|---|---|---|---|
| 1 | Contracts | Document library | Yes | Signed contracts and amendments. Key terms fill in automatically; adding or changing a contract starts obligation capture. |
| 2 | Obligations | List | Yes | Every tracked contract obligation: who owes what, by when, and what triggers it. |
| 3 | Obligation Owners | List | No | Routing rules used to assign new obligations. The most specific matching rule wins. |
| 4 | Obligation Types | List | No | What counts as a trackable obligation. Capture uses this to classify, keep or exclude. |
| 5 | Exclusions | List | No | Clauses or obligation patterns that should not be tracked. |
| 6 | Run Log | List | No | Every automated run: what it did and whether it worked. Failures show on the home page. |
| 7 | Evidence | Document library | No | Proof that obligations were fulfilled. Linked from each obligation's Evidence field. |
| 8 | AgentAssets | Document library | No | Site skills for Copilot in SharePoint and AI workflows. Usually exists already. |

List addresses: libraries sit at the site root (`/Contracts`, `/Evidence`, `/AgentAssets`); lists sit under `/Lists/` (`/Lists/Obligations`, `/Lists/Obligation Owners`, `/Lists/Obligation Types`, `/Lists/Exclusions`, `/Lists/Run Log`). The pages and messages link to `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`, so keep the Obligations address exactly.

On every list, rename the built-in `Title` column's display name as shown; don't create a second title column.

**Built-in views.** Every new list or library comes with a view at `AllItems.aspx` ("All Items" in a list, "All Documents" in a library). The pages link to that address, so never delete it. Turn it into the view marked "(built-in)" in the tables below (the marker isn't part of the view name): rename it and set its columns, filter and sort. Create the other views as new views. Then make the view marked Default the default.

## 1. Contracts (document library)

| Internal name | Display name | Type | Choices | Default | Autofill |
|---|---|---|---|---|---|
| `Title` | Contract title | Single line of text | | | |
| `Counterparty` | Counterparty | Single line of text | | | Yes |
| `ContractType` | Contract type | Choice | Customer agreement, Supplier agreement, Partner agreement, License, Lease, Financing, Data processing, Amendment, Other | | Yes |
| `EffectiveDate` | Effective date | Date only | | | Yes |
| `ExpirationDate` | Expiration date | Date only | | | Yes |
| `AutoRenews` | Auto-renews | Choice | Yes, No, Unclear | | Yes |
| `NoticePeriodDays` | Notice period (days) | Number | | | Yes |
| `GoverningLaw` | Governing law | Single line of text | | | Yes |
| `ContractValue` | Contract value | Currency (USD) | | | Yes |
| `ContractSummary` | Summary | Multiple lines of text | | | Yes |
| `ContractOwner` | Contract owner | Person | | | |
| `BusinessUnit` | Business unit | Choice | Sales, Procurement, Finance, Legal, IT, Facilities, Operations | | |
| `Amends` | Amends | Single line of text | | | |
| `IsSample` | Sample data | Yes/No | | No | |

`ContractSummary` is a multi-line column in a library. On the tested build it was capped at 255 characters, so summaries longer than that failed to save. If the tool lets you allow unlimited length in a document library, turn it on; otherwise keep the autofill prompt's "under 250 characters".

**Autofill prompts (optional).** Only if the user said yes to autofill. Replace `<our company>` with `ourCompany` from the setup answers. Autofill may not run on every tenant; capture reads the contract text itself and never depends on these columns.

| Column | Extraction prompt |
|---|---|
| `Counterparty` | The legal name of the other party to this contract, i.e. the party that is not <our company>. Use the name exactly as written in the parties block. |
| `ContractType` | Classify the document from <our company>'s point of view: Customer agreement if <our company> provides goods or services to the other party; Supplier agreement if <our company> buys from them; Partner agreement for distribution, reseller or alliance deals; License, Lease, Financing or Data processing when that is the main subject; Amendment if the document amends an earlier agreement; otherwise Other. |
| `EffectiveDate` | The effective date of this agreement (or of this amendment). Return only the date. |
| `ExpirationDate` | The date the current term ends. If the contract states a term length instead of an end date, compute the end date from the effective date. Leave empty if the agreement has no fixed end. |
| `AutoRenews` | Yes if the term renews automatically unless a party gives notice; No if it simply expires or renews only by mutual agreement; Unclear otherwise. |
| `NoticePeriodDays` | The number of days of advance written notice required to prevent renewal or to terminate at the end of the term. Convert months to days (1 month = 30 days). Empty if none. |
| `GoverningLaw` | The governing law jurisdiction, e.g. 'Washington, USA'. |
| `ContractValue` | The total or annual contract value in US dollars if stated; empty if not stated. |
| `ContractSummary` | Two plain-language sentences, under 250 characters in total: what the contract is for and the most important dates or commitments. |

**Views**

| View | Default | Columns, in order | Filter, in words | Sort | Query (CAML, plain text) |
|---|---|---|---|---|---|
| All contracts (built-in) | Yes | DocIcon, LinkFilename, Counterparty, ContractType, EffectiveDate, ExpirationDate, AutoRenews, NoticePeriodDays, ContractOwner, BusinessUnit | None | Counterparty, A to Z | `<OrderBy><FieldRef Name='Counterparty'/></OrderBy>` |
| Expiring in 180 days | No | DocIcon, LinkFilename, Counterparty, ExpirationDate, AutoRenews, NoticePeriodDays, ContractOwner | Expiration date is set and is on or before today + 180 days | ExpirationDate, soonest first | `<Where><And><IsNotNull><FieldRef Name='ExpirationDate'/></IsNotNull><Leq><FieldRef Name='ExpirationDate'/><Value Type='DateTime'><Today OffsetDays='180'/></Value></Leq></And></Where><OrderBy><FieldRef Name='ExpirationDate'/></OrderBy>` |

## 2. Obligations (list)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Obligation | Single line of text | | |
| `ContractName` | Contract | Single line of text | | |
| `ContractLink` | Contract link | Hyperlink | | |
| `Counterparty` | Counterparty | Single line of text | | |
| `ObligationText` | What must happen | Multiple lines of text (plain) | | |
| `ClauseRef` | Clause | Single line of text | | |
| `SourceClause` | Source clause | Multiple lines of text (plain) | | |
| `Party` | Who owes it | Choice | Us, Counterparty, Both | Us |
| `Category` | Category | Choice | Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other | |
| `TriggerType` | Trigger | Choice | Fixed date, Recurring, Event-driven, Ongoing | |
| `Recurrence` | Recurrence | Choice | None, Weekly, Monthly, Quarterly, Semi-annual, Annual | None |
| `DueDate` | Due date | Date only | | |
| `TriggerEvent` | Trigger event | Single line of text | | |
| `Owner` | Owner | Person | | |
| `EscalationOwner` | Escalation owner | Person | | |
| `BusinessUnit` | Business unit | Choice | Sales, Procurement, Finance, Legal, IT, Facilities, Operations | |
| `Status` | Status | Choice | Not started, In progress, Fulfilled, Waived, Not applicable | Not started |
| `Timing` | Timing | Choice | Overdue, Due soon, Upcoming, No date, Closed | |
| `ReviewState` | Review | Choice | Confirmed, Needs review | Needs review |
| `Confidence` | Confidence | Choice | High, Medium, Low | |
| `Risk` | Risk | Choice | High, Medium, Low | Medium |
| `FulfilledOn` | Fulfilled on | Date only | | |
| `Evidence` | Evidence | Hyperlink | | |
| `LastReminded` | Last reminded | Date only | | |
| `CaptureKey` | Capture key | Single line of text | | |
| `Notes` | Notes | Multiple lines of text (plain) | | |
| `IsSample` | Sample data | Yes/No | | No |

Who sets what: people set `Status`, `Owner` overrides, `Notes` and `ReviewState` (confirming held items). `Timing` is computed by the skills from `DueDate` and `Status`; people shouldn't edit it.

**Views.** "Open" below means Status is not Fulfilled, not Waived and not Not applicable. Make "Open by due date" the default view; it excludes undated items, which would otherwise sort to the top.

| View | Default | Columns, in order | Filter, in words | Sort or layout | Row limit | Query (CAML, plain text) |
|---|---|---|---|---|---|---|
| Open by due date | Yes | LinkTitle, Counterparty, Category, DueDate, Timing, Status, Owner, Party, Risk, ReviewState | Open, and Due date is set (undated items would sort first) | DueDate, soonest first | 100 | `<Where><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Fulfilled</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Waived</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Not applicable</Value></Neq><IsNotNull><FieldRef Name='DueDate'/></IsNotNull></And></And></And></Where><OrderBy><FieldRef Name='DueDate' Ascending='TRUE'/></OrderBy>` |
| Triggered and ongoing | No | LinkTitle, Counterparty, Category, TriggerType, TriggerEvent, Owner, Party, Risk, ReviewState | Open, and Due date is empty | Counterparty, A to Z | 100 | `<Where><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Fulfilled</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Waived</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Not applicable</Value></Neq><IsNull><FieldRef Name='DueDate'/></IsNull></And></And></And></Where><OrderBy><FieldRef Name='Counterparty'/></OrderBy>` |
| My obligations | No | LinkTitle, Counterparty, Category, DueDate, Timing, Status, Risk | Owner is the signed-in user. The value type must be User with the current user ID; Integer was rejected | DueDate, soonest first | Default | `<Where><Eq><FieldRef Name='Owner'/><Value Type='User'><UserID/></Value></Eq></Where><OrderBy><FieldRef Name='DueDate' Ascending='TRUE'/></OrderBy>` |
| Needs owner | No | LinkTitle, Counterparty, Category, BusinessUnit, DueDate, Risk | Owner is empty | DueDate, soonest first | Default | `<Where><IsNull><FieldRef Name='Owner'/></IsNull></Where><OrderBy><FieldRef Name='DueDate'/></OrderBy>` |
| Needs review | No | LinkTitle, Counterparty, ClauseRef, Category, Confidence, DueDate, Notes | Review is Needs review | None | Default | `<Where><Eq><FieldRef Name='ReviewState'/><Value Type='Choice'>Needs review</Value></Eq></Where>` |
| By contract | No | LinkTitle, Category, Party, DueDate, Recurrence, Status, Owner | None; grouped by Contract, expanded | DueDate, soonest first | Default | `<GroupBy Collapse='FALSE'><FieldRef Name='ContractName'/></GroupBy><OrderBy><FieldRef Name='DueDate'/></OrderBy>` |
| Calendar | No | LinkTitle, DueDate, Counterparty, Status | None | Modern calendar, month layout; start and end date = DueDate; title = Title | Default | None |
| All obligations (built-in) | No | LinkTitle, Counterparty, Category, DueDate, Timing, Status, Owner, Party, Risk, ReviewState, ContractName, ClauseRef, TriggerType, Recurrence, TriggerEvent, EscalationOwner, BusinessUnit, Confidence, FulfilledOn, Evidence | None | None | Default | None |

## 3. Obligation Owners (list)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Rule | Single line of text | | |
| `Category` | Category | Choice | Any, Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other | Any |
| `BusinessUnit` | Business unit | Choice | Any, Sales, Procurement, Finance, Legal, IT, Facilities, Operations | Any |
| `Counterparty` | Counterparty (optional) | Single line of text | | |
| `Owner` | Owner | Person | | |
| `EscalationOwner` | Escalation owner | Person | | |
| `Notify` | Notify by | Choice | Email, Teams, Both | Both |

| View | Default | Columns, in order | Filter | Sort |
|---|---|---|---|---|
| All rules (built-in) | Yes | LinkTitle, Category, BusinessUnit, Counterparty, Owner, EscalationOwner, Notify | None | None |

**Default rule (seed).** If no rule has Category = Any, BusinessUnit = Any and an empty Counterparty, add one: Title "Default - all obligations", Category Any, BusinessUnit Any, Counterparty empty, Owner and EscalationOwner = the person running setup, Notify Both. Without an Any/Any rule, nobody is assigned or reminded.

## 4. Obligation Types (list)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Obligation type | Single line of text | | |
| `Category` | Category | Choice | Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other | |
| `Handling` | Handling | Choice | Track, Exclude, Hold for review | Track |
| `DefaultRisk` | Default risk | Choice | High, Medium, Low | Medium |
| `DefaultRecurrence` | Default recurrence | Choice | None, Weekly, Monthly, Quarterly, Semi-annual, Annual | None |
| `Description` | Description | Multiple lines of text (plain) | | |
| `Examples` | Example wording | Multiple lines of text (plain) | | |

| View | Default | Columns, in order | Filter | Sort | Query (CAML, plain text) |
|---|---|---|---|---|---|
| All types (built-in) | Yes | LinkTitle, Category, Handling, DefaultRisk, DefaultRecurrence, Description | None | Category, A to Z | `<OrderBy><FieldRef Name='Category'/></OrderBy>` |

Seed rows: [obligation-types.md](obligation-types.md).

## 5. Exclusions (list)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Exclusion | Single line of text | | |
| `Pattern` | Clause or pattern | Multiple lines of text (plain) | | |
| `Reason` | Reason | Multiple lines of text (plain) | | |
| `Scope` | Scope | Choice | All contracts, This contract | This contract |
| `ContractName` | Contract | Single line of text | | |
| `Category` | Category | Choice | Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other | |
| `Active` | Active | Yes/No | | Yes |

| View | Default | Columns, in order | Filter | Sort |
|---|---|---|---|---|
| All exclusions (built-in) | Yes | LinkTitle, Scope, ContractName, Category, Reason, Active | None | None |

Starts empty. People add rows through the Remove obligation quick step (`exclude-obligation`).

## 6. Run Log (list)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Run | Single line of text | | |
| `Workflow` | Workflow | Choice | Capture, Assign owners, Daily sweep, Owner digest, Leadership digest, Mark fulfilled, Exclude, Setup | |
| `Outcome` | Outcome | Choice | Succeeded, Partial, Failed, Skipped | |
| `ContractName` | Contract | Single line of text | | |
| `ContractVersion` | Contract version | Single line of text | | |
| `ItemsCreated` | Created | Number | | |
| `ItemsUpdated` | Updated | Number | | |
| `ItemsHeld` | Held for review | Number | | |
| `Details` | Details | Multiple lines of text (plain) | | |
| `RunAt` | Run at | Date and time | | |

| View | Default | Columns, in order | Filter | Sort | Query (CAML, plain text) |
|---|---|---|---|---|---|
| Recent runs (built-in) | Yes | LinkTitle, Workflow, Outcome, ContractName, ItemsCreated, ItemsUpdated, ItemsHeld, RunAt | None | Created, newest first | `<OrderBy><FieldRef Name='Created' Ascending='FALSE'/></OrderBy>` |

The Workflow value "Setup" is used by `setup-obligation-hub` and `clear-obligation-sample-data`. Sample rows loaded by the deploy script have `Details` starting with "Demo seed".

## 7. Evidence (document library)

| Internal name | Display name | Type | Choices | Default |
|---|---|---|---|---|
| `Title` | Evidence title | Single line of text | | |
| `IsSample` | Sample data | Yes/No | | No |

No extra views; keep the built-in "All Documents". `mark-obligation-fulfilled` names uploaded files `<ID>-<YYYY-MM-DD>-<original name>`.

## 8. AgentAssets (document library)

Holds the hub's skills and settings. It usually exists already, because Copilot in SharePoint loads site skills from it. Create it only if it's missing (title column display name "Asset title"). It needs these folders:

| Folder | Holds |
|---|---|
| `Skills` | One folder per skill, each with its `SKILL.md` (and `references/` where the skill has one) |
| `Config` | `hub-settings.json` |

The site context file `SHAREPOINT.md` goes in the AgentAssets **root**, not in `Skills`. Folder creation may need a folder colour; any colour works.

## 9. Settings file: AgentAssets/Config/hub-settings.json

A JSON object with these keys. Every hub skill reads it first.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `ourCompany` | text | (ask) | Our legal name, exactly as it appears in contracts. Decides Party = Us. |
| `siteUrl` | text | (this site) | Absolute site URL, no trailing slash. Used in links. |
| `timeZone` | text | Pacific Standard Time | Windows time zone name used for "today" and schedules. |
| `dueSoonDays` | number | 14 | Days ahead that count as Due soon. |
| `escalateAfterDaysOverdue` | number | 0 | Days overdue before escalation. |
| `reminderCooldownDays` | number | 3 | Minimum days between overdue reminders for one item (at least 1). |
| `leadershipRecipients` | list of text | (ask) | Email addresses for the Friday leadership digest. |
| `leadershipTeamsChannel` | object with `team` and `channel` text | both empty | Optional Teams channel for the leadership digest. |
| `notifyDefault` | text: Email, Teams or Both | Both | Channel for people no routing rule names. |
| `captureHoldBelowConfidence` | text: High, Medium or Low | Medium | Items below this confidence go to Needs review. |
| `maxDigestItems` | number | 25 | Most items in one owner digest. |
