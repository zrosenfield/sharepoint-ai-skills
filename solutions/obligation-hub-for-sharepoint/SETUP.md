# Manual setup (site owner, no admin)

This guide builds the Obligation Hub step by step, for a site owner who'd rather not run the deploy script. It's prompt-first: each step gives a prompt to paste into **Copilot in SharePoint** on the hub site, a fallback if the prompt doesn't work, and a "Check it worked" line. Allow 60 to 90 minutes. Pieces marked *optional* can be skipped.

> Unofficial, personal and unsupported. Not a Microsoft product, and not legal advice. See the [README](README.md).

Shortcut: steps 2 to 7 are exactly what the [`setup-obligation-hub`](../../Skills/setup-obligation-hub/) skill does in one go. Upload that skill (step 8 explains how), ask Copilot "Set up the Obligation Hub on this site", and jump to step 8. The full schema, with every view filter, is in that skill's [references/schema.md](../../Skills/setup-obligation-hub/references/schema.md).

**Rules that save time:**
- Use the internal names exactly as written. Every skill depends on them. Display names can be changed later.
- Create a list's columns and its views in **separate** prompts. One request with many columns and views failed with "too many stages".
- If Copilot says it did something, check it. The "Check it worked" lines tell you where.

## 1. Pick the site

Use a test site where you're an owner. For AI workflows, HTML pages with live data and Copilot site skills you need a tenant where those preview features are available; on other tenants, steps 2 to 7 still give you working lists, views, formatting and quick steps. Note the site's full URL without a trailing slash, for example `https://<tenant>.sharepoint.com/sites/<site>`.

**Check it worked:** you can open **Site contents** and see **New > List**.

## 2. Create the Contracts library

```text
Create a document library named Contracts with the description "Signed contracts and amendments. Key terms fill in automatically; adding or changing a contract starts obligation capture." and add it to the site navigation. Rename the Title column's display name to "Contract title". Add these columns with exactly these internal names, display names and types, and don't create any views yet:
- Counterparty ("Counterparty"): single line of text
- ContractType ("Contract type"): choice: Customer agreement, Supplier agreement, Partner agreement, License, Lease, Financing, Data processing, Amendment, Other
- EffectiveDate ("Effective date"): date only
- ExpirationDate ("Expiration date"): date only
- AutoRenews ("Auto-renews"): choice: Yes, No, Unclear
- NoticePeriodDays ("Notice period (days)"): number
- GoverningLaw ("Governing law"): single line of text
- ContractValue ("Contract value"): currency, US dollars
- ContractSummary ("Summary"): multiple lines of text
- ContractOwner ("Contract owner"): person
- BusinessUnit ("Business unit"): choice: Sales, Procurement, Finance, Legal, IT, Facilities, Operations
- Amends ("Amends"): single line of text
- IsSample ("Sample data"): yes/no, default No
```

Then, in a new prompt:

```text
In the Contracts library, rename the existing "All Documents" view to "All contracts" (don't delete it), keep it as the default, and set its columns to Type, Name, Counterparty, Contract type, Effective date, Expiration date, Auto-renews, Notice period (days), Contract owner, Business unit, sorted by Counterparty. Then create a view "Expiring in 180 days": columns Type, Name, Counterparty, Expiration date, Auto-renews, Notice period (days), Contract owner; show only files where Expiration date is not empty and is on or before today plus 180 days; sorted by Expiration date, soonest first.
```

**Fallback:** **New > Document library**, then **Add column** for each row of the Contracts table in [schema.md](../../Skills/setup-obligation-hub/references/schema.md#1-contracts-document-library). Type the internal name first when you create a column (that fixes the internal name), then rename it to the display name.

**Check it worked:** open the library's **Library settings**. All 13 columns above are listed, plus Contract title; hover over each and the address bar shows `Field=<internal name>`. The view menu has All contracts (default) and Expiring in 180 days.

**Why rename instead of delete?** The pages link to each list's built-in view address (`AllItems.aspx`). Renaming the built-in view keeps those links working. The same applies to every list below.

### 2.1 Autofill prompts (optional)

```text
In the Contracts library, turn on autofill for these columns with these prompts. Our company is <our legal name>.
- Counterparty: The legal name of the other party to this contract, i.e. the party that is not <our legal name>. Use the name exactly as written in the parties block.
- ContractType: Classify the document from <our legal name>'s point of view: Customer agreement if we provide goods or services to the other party; Supplier agreement if we buy from them; Partner agreement for distribution, reseller or alliance deals; License, Lease, Financing or Data processing when that is the main subject; Amendment if the document amends an earlier agreement; otherwise Other.
- EffectiveDate: The effective date of this agreement (or of this amendment). Return only the date.
- ExpirationDate: The date the current term ends. If the contract states a term length instead of an end date, compute the end date from the effective date. Leave empty if the agreement has no fixed end.
- AutoRenews: Yes if the term renews automatically unless a party gives notice; No if it simply expires or renews only by mutual agreement; Unclear otherwise.
- NoticePeriodDays: The number of days of advance written notice required to prevent renewal or to terminate at the end of the term. Convert months to days (1 month = 30 days). Empty if none.
- GoverningLaw: The governing law jurisdiction, e.g. 'Washington, USA'.
- ContractValue: The total or annual contract value in US dollars if stated; empty if not stated.
- ContractSummary: Two plain-language sentences, under 250 characters in total: what the contract is for and the most important dates or commitments.
```

Keep the summary under 250 characters: on the test build, multi-line columns in a library were capped at 255 characters. Autofill may not run on your tenant. Capture never depends on it.

**Check it worked:** upload a contract; within an hour the columns fill in. If they don't, fill the key ones by hand.

## 3. Create the Obligations list

```text
Create a list named Obligations with the description "Every tracked contract obligation: who owes what, by when, and what triggers it." and add it to the site navigation. Rename the Title column's display name to "Obligation". Add these columns with exactly these internal names, display names and types, and don't create any views yet:
- ContractName ("Contract"): single line of text
- ContractLink ("Contract link"): hyperlink
- Counterparty ("Counterparty"): single line of text
- ObligationText ("What must happen"): multiple lines of plain text
- ClauseRef ("Clause"): single line of text
- SourceClause ("Source clause"): multiple lines of plain text
- Party ("Who owes it"): choice: Us, Counterparty, Both; default Us
- Category ("Category"): choice: Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other
- TriggerType ("Trigger"): choice: Fixed date, Recurring, Event-driven, Ongoing
- Recurrence ("Recurrence"): choice: None, Weekly, Monthly, Quarterly, Semi-annual, Annual; default None
- DueDate ("Due date"): date only
- TriggerEvent ("Trigger event"): single line of text
- Owner ("Owner"): person
- EscalationOwner ("Escalation owner"): person
- BusinessUnit ("Business unit"): choice: Sales, Procurement, Finance, Legal, IT, Facilities, Operations
- Status ("Status"): choice: Not started, In progress, Fulfilled, Waived, Not applicable; default Not started
- Timing ("Timing"): choice: Overdue, Due soon, Upcoming, No date, Closed
- ReviewState ("Review"): choice: Confirmed, Needs review; default Needs review
- Confidence ("Confidence"): choice: High, Medium, Low
- Risk ("Risk"): choice: High, Medium, Low; default Medium
- FulfilledOn ("Fulfilled on"): date only
- Evidence ("Evidence"): hyperlink
- LastReminded ("Last reminded"): date only
- CaptureKey ("Capture key"): single line of text
- Notes ("Notes"): multiple lines of plain text
- IsSample ("Sample data"): yes/no, default No
```

Then the views, in a new prompt. "Open" means Status isn't Fulfilled, Waived or Not applicable.

```text
In the Obligations list, create these views:
1. "Open by due date" (make it the default; 100 items per page): Obligation, Counterparty, Category, Due date, Timing, Status, Owner, Who owes it, Risk, Review. Show items whose Status is not Fulfilled, not Waived and not Not applicable, AND whose Due date is not empty. Sort by Due date ascending.
2. "Triggered and ongoing" (100 items per page): Obligation, Counterparty, Category, Trigger, Trigger event, Owner, Who owes it, Risk, Review. Same Status filter, AND Due date is empty. Sort by Counterparty.
3. "My obligations": Obligation, Counterparty, Category, Due date, Timing, Status, Risk. Show items where Owner is the current user ([Me]). Sort by Due date ascending.
4. "Needs owner": Obligation, Counterparty, Category, Business unit, Due date, Risk. Show items where Owner is empty. Sort by Due date.
5. "Needs review": Obligation, Counterparty, Clause, Category, Confidence, Due date, Notes. Show items where Review is Needs review.
6. "By contract": Obligation, Category, Who owes it, Due date, Recurrence, Status, Owner. Group by Contract, expanded. Sort by Due date.
7. "Calendar": a calendar view by month using Due date as start and end date and Obligation as the title.
8. "All obligations": don't create a new view; rename the existing "All Items" view to "All obligations" and show Obligation, Counterparty, Category, Due date, Timing, Status, Owner, Who owes it, Risk, Review, Contract, Clause, Trigger, Recurrence, Trigger event, Escalation owner, Business unit, Confidence, Fulfilled on, Evidence.
Keep "Open by due date" as the default view.
```

If the views prompt fails as too large, split it into two prompts (views 1 to 4, then 5 to 8).

**Fallback:** create the columns with **Add column**, and the views with **Create new view** using the filters above (edit and rename "All Items" for "All obligations"). "My obligations" must filter Owner on **[Me]**. Through the API, the filter value needs type User with the current user ID; type Integer was rejected. "Open by due date" must exclude undated items, or they sort to the top.

**Check it worked:** the list opens on "Open by due date"; the view menu shows all eight views, and "All Items" has become "All obligations"; **List settings** shows the 26 columns above plus Obligation (the renamed Title).

## 4. Create the other lists

Do each list in two prompts (columns, then views), like step 3. Column details are in [schema.md](../../Skills/setup-obligation-hub/references/schema.md).

### 4.1 Obligation Owners

```text
Create a list named Obligation Owners with the description "Routing rules used to assign new obligations. The most specific matching rule wins." and no navigation link. Rename Title to "Rule". Add columns with exactly these internal names, and no views yet:
- Category ("Category"): choice: Any, Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other; default Any
- BusinessUnit ("Business unit"): choice: Any, Sales, Procurement, Finance, Legal, IT, Facilities, Operations; default Any
- Counterparty ("Counterparty (optional)"): single line of text
- Owner ("Owner"): person
- EscalationOwner ("Escalation owner"): person
- Notify ("Notify by"): choice: Email, Teams, Both; default Both
```

Then: "In Obligation Owners, rename the All Items view to "All rules", keep it as the default, and show Rule, Category, Business unit, Counterparty (optional), Owner, Escalation owner, Notify by."

### 4.2 Obligation Types

```text
Create a list named Obligation Types with the description "What counts as a trackable obligation. Capture uses this to classify, keep or exclude." and no navigation link. Rename Title to "Obligation type". Add columns with exactly these internal names, and no views yet:
- Category ("Category"): choice: Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other
- Handling ("Handling"): choice: Track, Exclude, Hold for review; default Track
- DefaultRisk ("Default risk"): choice: High, Medium, Low; default Medium
- DefaultRecurrence ("Default recurrence"): choice: None, Weekly, Monthly, Quarterly, Semi-annual, Annual; default None
- Description ("Description"): multiple lines of plain text
- Examples ("Example wording"): multiple lines of plain text
```

Then: "In Obligation Types, rename the All Items view to "All types", keep it as the default, and show Obligation type, Category, Handling, Default risk, Default recurrence, Description, sorted by Category."

### 4.3 Exclusions

```text
Create a list named Exclusions with the description "Clauses or obligation patterns that should not be tracked." and no navigation link. Rename Title to "Exclusion". Add columns with exactly these internal names, and no views yet:
- Pattern ("Clause or pattern"): multiple lines of plain text
- Reason ("Reason"): multiple lines of plain text
- Scope ("Scope"): choice: All contracts, This contract; default This contract
- ContractName ("Contract"): single line of text
- Category ("Category"): choice: Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other
- Active ("Active"): yes/no, default Yes
```

Then: "In Exclusions, rename the All Items view to "All exclusions", keep it as the default, and show Exclusion, Scope, Contract, Category, Reason, Active."

### 4.4 Run Log

```text
Create a list named Run Log with the description "Every automated run: what it did and whether it worked. Failures show on the home page." and no navigation link. Rename Title to "Run". Add columns with exactly these internal names, and no views yet:
- Workflow ("Workflow"): choice: Capture, Assign owners, Daily sweep, Owner digest, Leadership digest, Mark fulfilled, Exclude, Setup
- Outcome ("Outcome"): choice: Succeeded, Partial, Failed, Skipped
- ContractName ("Contract"): single line of text
- ContractVersion ("Contract version"): single line of text
- ItemsCreated ("Created"): number
- ItemsUpdated ("Updated"): number
- ItemsHeld ("Held for review"): number
- Details ("Details"): multiple lines of plain text
- RunAt ("Run at"): date and time
```

Then: "In Run Log, rename the All Items view to "Recent runs", keep it as the default, and show Run, Workflow, Outcome, Contract, Created, Updated, Held for review, Run at, sorted by Created, newest first."

### 4.5 Evidence

```text
Create a document library named Evidence with the description "Proof that obligations were fulfilled. Linked from each obligation's Evidence field." and no navigation link. Rename Title to "Evidence title" and add a yes/no column IsSample ("Sample data"), default No.
```

**Check it worked:** **Site contents** lists Contracts, Obligations, Obligation Owners, Obligation Types, Exclusions, Run Log and Evidence. Each list opens on the view named above.

## 5. Formatting

The four coloured columns on Obligations use the files in [formats/](formats/): `Status.json`, `Timing.json`, `Risk.json` and `ReviewState.json`. They use inline styles only.

```text
Apply column formatting to the Status column of the Obligations list using this JSON: <paste the contents of formats/Status.json>
```

Repeat for Timing, Risk and ReviewState with their files.

**Fallback:** in Obligations, open the column's menu > **Column settings > Format this column > Advanced mode**, paste the file's contents and save. The colours are also described in [formatting.md](../../Skills/setup-obligation-hub/references/formatting.md).

**Check it worked:** Status, Timing, Risk and Review show as coloured pills.

## 6. Quick steps

```text
On the Obligations list, create a quick step titled "Mark fulfilled" that asks Copilot this prompt for the selected item: "Mark this obligation fulfilled using the mark-obligation-fulfilled skill." Show it only when Status is not Fulfilled.
```

```text
On the Obligations list, create a quick step titled "Remove obligation" that asks Copilot this prompt for the selected item: "Remove this obligation from tracking using the exclude-obligation skill."
```

```text
On the Contracts library, create a quick step titled "Re-capture obligations" that asks Copilot this prompt for the selected file: "Re-capture obligations from this contract using the capture-obligations skill. Do a full capture even if the text hasn't changed."
```

Details: [workflows/quick-steps.md](workflows/quick-steps.md).

**Check it worked:** select an Obligations item; Mark fulfilled and Remove obligation appear. Select a Contracts file; Re-capture obligations appears.

## 7. Seed Obligation Types and the default routing rule

The 37 types are in [seed/obligation-types.json](seed/obligation-types.json) and, as tables, in [obligation-types.md](../../Skills/setup-obligation-hub/references/obligation-types.md).

**Option 1 (easiest):** upload the `setup-obligation-hub` skill (step 8), then ask:

```text
Using the setup-obligation-hub skill, seed the Obligation Types list and add the default routing rule with me as owner. Change nothing else.
```

**Option 2:** upload `seed/obligation-types.json` to the AgentAssets library, then ask:

```text
Add every row in AgentAssets/obligation-types.json to the Obligation Types list, copying Title, Category, Handling, DefaultRisk, DefaultRecurrence, Description and Examples exactly. Skip rows whose Title already exists.
```

Then add one routing rule by hand in Obligation Owners: Rule "Default - all obligations", Category Any, Business unit Any, Counterparty empty, Owner and Escalation owner = you (or a shared obligations account), Notify by Both. More examples are in [seed/obligation-owners.template.json](seed/obligation-owners.template.json).

**Check it worked:** Obligation Types shows 37 items (29 Track, 5 Exclude, 3 Hold for review). Obligation Owners has the Any/Any rule with an owner.

## 8. Upload the skills

Open the **AgentAssets** library (create it as a document library if it's missing), open or create the **Skills** folder, and upload each skill **folder** from [`../../Skills/`](../../Skills/), not the whole `Skills` directory. Where available, **Settings > Site skills** is another way in. You need Edit permission.

| Skill | Needed for |
|---|---|
| [`capture-obligations`](../../Skills/capture-obligations/) | Capture workflows; Re-capture quick step |
| [`assign-obligation-owners`](../../Skills/assign-obligation-owners/) | Assign owners workflow |
| [`sweep-obligations`](../../Skills/sweep-obligations/) | Daily sweep workflow |
| [`obligation-owner-digest`](../../Skills/obligation-owner-digest/) | Owner digest workflow |
| [`obligation-leadership-digest`](../../Skills/obligation-leadership-digest/) | Leadership digest workflow |
| [`mark-obligation-fulfilled`](../../Skills/mark-obligation-fulfilled/) | Mark fulfilled quick step |
| [`exclude-obligation`](../../Skills/exclude-obligation/) | Remove obligation quick step |
| [`obligation-hub-guide`](../../Skills/obligation-hub-guide/) | Questions in Copilot |
| [`setup-obligation-hub`](../../Skills/setup-obligation-hub/) | Setup and repair (include its `references` folder) |
| [`clear-obligation-sample-data`](../../Skills/clear-obligation-sample-data/) | Removing the sample data |

**Check it worked:** `AgentAssets/Skills/capture-obligations/SKILL.md` opens, and so on for each folder. Ask Copilot "Which Obligation Hub skills are on this site?".

## 9. Upload the site context file and settings

1. Upload [assets/SHAREPOINT.md](assets/SHAREPOINT.md) to the **root** of AgentAssets (not into Skills).
2. Copy [assets/hub-settings.template.json](assets/hub-settings.template.json). Replace `{{OUR_COMPANY}}` with your legal name as it appears in contracts, `{{SITE_URL}}` with the site URL from step 1, and `"{{LEADERSHIP_EMAILS}}"` with quoted, comma-separated addresses (or leave the list empty). Change `timeZone` if you're not on Pacific time. Save it as `hub-settings.json` and upload it to a **Config** folder in AgentAssets.

```text
Read AgentAssets/Config/hub-settings.json and tell me ourCompany, siteUrl, timeZone and leadershipRecipients.
```

**Check it worked:** Copilot reads back your values. A typo in the JSON shows up here as an error.

## 10. Pages

The seven pages (Home, My obligations, Review queue, Contract 360, Leadership, How it works, Settings) need this site's list IDs filled in, so they can't be uploaded as they are.

**Option 1:** run the deploy script ([README, path A](README.md#a-paste-in-browser-script)) with `pagesOnly: true`, and `setHome: true` if you want Home as the home page. It looks up this site's list IDs, fills in, uploads and publishes the seven pages, and applies the site look in step 10.1 (turn that off with `siteChrome: false`). It writes nothing else, and it stops if Obligations, Contracts, Run Log or Obligation Owners is missing.

**Option 2:** in Cowork, ask "Fill in the hub's pages for `<site>`" ([prompts/cowork-prompts.md](prompts/cowork-prompts.md)).

The script publishes the pages. Pages uploaded any other way arrive as drafts: publish each one, then set the home page:

```text
Publish every .html page in Site Pages that's still a draft, then make Home.html the site's home page.
```

**Fallback:** open each page in Site Pages and choose **Publish**; then, on Home.html, choose **Make homepage** from the Site Pages library.

**Check it worked:** the site opens on Home and shows a "Live" badge, meaning it reads the lists rather than built-in snapshot data. Ask another site member to open it, to confirm visitors see the published version.

### 10.1 Site navigation and look (optional)

The pages have no menu of their own; the site navigation is how people move between them. The deploy script with `pagesOnly: true` does all of this for you. By hand (site owner):

1. **Navigation.** **Settings** (gear) **> Change the look > Navigation**: make the site navigation visible and horizontal. Then choose **Edit** on the site navigation and add these links, in this order:

   | Link | Goes to |
   |---|---|
   | Overview | `SitePages/Home.html` |
   | My obligations | `SitePages/MyObligations.html` |
   | Contracts | the Contracts library |
   | Obligations | the Obligations list |
   | Review | `SitePages/ReviewQueue.html` |
   | Leadership | `SitePages/Leadership.html` |
   | How it works | `SitePages/HowItWorks.html` |
   | Settings | `SitePages/Settings.html` |

   If steps 2 and 3 already added Contracts and Obligations links, move them into place instead of adding them again. Remove the default Documents, Pages and Site contents links only if you want to.
2. **Header.** **Settings > Change the look > Header**: Layout **Compact**, Background **None**.
3. **Logo.** In the same Header panel, under **Site logo**, choose **Change** and upload [deploy/assets/obligation-hub-logo.png](deploy/assets/obligation-hub-logo.png).
4. **Theme.** **Settings > Change the look > Theme**. The hub's own "Obligation Hub" palette can only be applied by script (or added by a tenant admin as a company theme); otherwise pick the closest built-in blue theme.

**Check it worked:** every hub page shows the same eight links across the top, and the header shows the logo.

## 11. Create the AI workflows

Follow [docs/workflow-checklist.md](docs/workflow-checklist.md) and paste the six prompts in [workflows/ai-workflow-prompts.md](workflows/ai-workflow-prompts.md), the two Capture workflows first. For anything beyond a demo, create them signed in as a shared obligations account: messages come from whoever creates them.

**Check it worked:** upload one contract. A Capture row with Outcome Succeeded appears in **Run Log > Recent runs** within a few minutes, and new items appear in Obligations.

## 12. Sample data (optional)

Upload the fictional contracts in [sample-data/contracts/](sample-data/contracts/) to Contracts, base contracts before amendments. For each file set **Sample data** = Yes, and set **Amends** = `01-Contoso-MSA.docx` on `02-Contoso-MSA-Amendment-1.docx`. With the Capture workflows on, they're captured within minutes. The expected results are in [sample-data/answer-key.md](sample-data/answer-key.md).

To remove the sample later, ask Copilot "Remove the sample data from this site" ([`clear-obligation-sample-data`](../../Skills/clear-obligation-sample-data/)). It removes only items marked Sample data = Yes, after you confirm.

**Check it worked:** after capture, the Obligations list's "By contract" view shows items under each sample file, with Sample data = Yes.
