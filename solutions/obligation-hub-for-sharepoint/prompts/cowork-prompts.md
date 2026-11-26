# Obligation Hub: Cowork prompt catalogue

Prompts for people who use Cowork with the hub. Cowork works through its SharePoint tools, and it loads the hub's own skills (from the kit's [`Skills/`](../../../Skills/) folder, or from `AgentAssets/Skills/` on the site), so a chat or automation run behaves like the site's AI workflows and quick steps.

Replace `<…>` with your values. How approvals work:
- Every SharePoint write (creating a site, list, item or file, or updating one) shows an **approval card**. You approve each call once.
- Sending mail or posting to Teams asks for approval in chat.
- Automations ask you to approve the trigger and the tools they may use unattended. Deletes can never be pre-approved.

For the install prompts, give Cowork the kit: attach or point it at a copy of this repository (the `Skills/` folder and this solution folder).

## A. Install with Cowork

| Prompt | What Cowork does | Approvals you'll see |
|---|---|---|
| Install the Obligation Hub from this kit on `<site>`. Our company is `<legal name>`. | Loads [`setup-obligation-hub`](../../../Skills/setup-obligation-hub/) from the kit, checks what the site already has, and shows a plan. After you confirm, it builds the lists, libraries, views, formatting, quick steps, settings file, type catalogue and default routing rule. Then it offers to upload the ten skill folders to `AgentAssets/Skills` and `assets/SHAREPOINT.md` to the AgentAssets root. | One card per list, view call, format, quick step, batch of rows and file upload |
| Set up an Obligation Hub on a new site called `<name>` for `<company>`. | Creates the site, then does the install above on it. | Create site; then as above |
| Check my Obligation Hub install on `<site>` and tell me what's missing. Don't change anything. | Runs the read-only check from `setup-obligation-hub` and stops at the plan. | None (read-only) |
| Fill in the hub's pages for `<site>`. | Follows the kit's [`deploy/cowork/README.md`](../deploy/cowork/README.md): reads the page templates in `deploy/pages/`, looks up this site's list IDs and addresses, fills in every token (including the six workflow prompts from [`../workflows/ai-workflow-prompts.md`](../workflows/ai-workflow-prompts.md)), uploads the pages to Site Pages and publishes them. It asks before making Home the site's home page. Pages must be published before they can be the home page. | Uploads; publish; set home page |
| Give `<site>` the hub's navigation and look. | Explains the two ways: run the deploy script with `pagesOnly: true` (it adds the eight hub navigation links and applies the theme, logo and compact header, and is the only way to apply the hub's own theme palette), or follow the **Settings > Change the look** steps in [`../SETUP.md`](../SETUP.md), step 10.1, which it can walk you through. | None from Cowork; the script or your clicks make the changes |
| Load the pre-captured sample on `<site>`. | Uploads the fictional sample contracts and their already-captured obligations from the kit's `sample-data/`, all marked `IsSample` = Yes, so the pages have data at once. If the Capture workflows are on, they run too and match the existing items by capture key, so nothing is duplicated. | Uploads; batch item creates |
| Load the sample contracts on `<site>` and let the hub capture them. | Uploads only the sample contracts (`IsSample` = Yes), base contracts before amendments, with **Amends** set. The Capture workflows (or Cowork, if you ask) capture them live. Use this to test capture. | Uploads |
| Remove the sample data from `<site>`. | Runs [`clear-obligation-sample-data`](../../../Skills/clear-obligation-sample-data/): shows what's marked as sample and removes it after you confirm. Real items are never touched. | Your typed confirmation; one card per delete call |
| Give me the AI workflow setup prompts for `<site>`. | Shows the six prompts from [`../workflows/ai-workflow-prompts.md`](../workflows/ai-workflow-prompts.md), with your time zone, for you to paste into Copilot in SharePoint. | None (read-only) |

## B. Configure

| Prompt | What Cowork does | Approvals you'll see |
|---|---|---|
| Add the Obligation Hub to my existing site `<url>`. | Runs `setup-obligation-hub`, which adds only the missing lists, libraries, columns and views. Existing lists and items are left as they are. | One card per list or column change; uploads |
| Route all Finance obligations to `<person>`, escalate to `<person>`. | Resolves both people and creates or updates an Obligation Owners rule. It asks whether "Finance" means the Finance business unit or Payment obligations. | Create or update one rule |
| Send Legal everything about `<counterparty>`, by Teams only. | Adds a counterparty rule (the most specific rule wins) with Notify = Teams. | Create one rule |
| Load our obligation catalogue from `<spreadsheet>`. | Reads the sheet and maps its columns to Obligation Types (Title, Category, Handling, DefaultRisk, DefaultRecurrence, Description, Examples). It shows the mapping and any values it can't map, then adds the rows, skipping duplicates. | One batch create, after you check the mapping |
| Import the contracts in my OneDrive folder `<folder>` into the hub. | Copies the files into the Contracts library, base contracts before their amendments, and sets **Amends** on amendments. The Capture workflows capture each file. | File uploads |
| Set the leadership digest recipients to `<emails>` on `<site>`. | Updates `leadershipRecipients` in `AgentAssets/Config/hub-settings.json`. | Overwrite one file |

## C. Daily use

| Prompt | What Cowork does | Approvals you'll see |
|---|---|---|
| What do I owe this week on the Obligation Hub? | Lists your open items that are overdue or due within 7 days, plus items waiting on triggers, each with its clause and a link ([`obligation-hub-guide`](../../../Skills/obligation-hub-guide/)). | None |
| What auto-renews or needs a renewal decision in the next 120 days? | Lists Notice & renewal deadlines and contracts expiring in that window, each with the last day to act. | None |
| Draft the non-renewal notice for `<counterparty>` from the contract and save it for my review. Don't send. | Reads the obligation and the notice clause (including any amended notice period) and drafts the letter as an Outlook draft to the contract's notice address. It doesn't send it. | Create draft |
| I sent the `<counterparty>` notice: save the Sent Items email as evidence and mark it fulfilled. | Finds the sent email and saves it to the Evidence library, then runs [`mark-obligation-fulfilled`](../../../Skills/mark-obligation-fulfilled/), linking the evidence and creating the next occurrence. | Upload the evidence file; update the item; create the next occurrence |
| Prepare me for my `<counterparty>` renewal call: obligations, notice dates, open items. | Builds a one-page brief in chat: key terms, deadlines (including any transition-request window), open and overdue items, and the clauses behind them. | None |
| Mark the `<obligation>` fulfilled. Evidence is in my OneDrive folder `<folder>`. | Finds the file, copies it to Evidence and runs `mark-obligation-fulfilled`. | Upload; update the item; create the next occurrence |
| Which obligations have no owner, and who should own them? | Lists unowned items and suggests routing rules that would cover them. It creates rules only if you say so. | Only if you create rules |
| Why was the `<obligation>` held for review? | Reads the item's Notes and the contract's Capture Run Log row, then explains the reason with the clause. | None |
| Remove the `<obligation>` for all contracts. | Runs [`exclude-obligation`](../../../Skills/exclude-obligation/), asking for the reason, then adds an Exclusions pattern and sets the item to Not applicable. | Create the exclusion; update the item |
| What did the hub send last week, and to whom? | Summarises the Run Log rows for the sweep, the digests and owner assignment. | None |

## D. Automate with Cowork
Use these if your tenant doesn't have SharePoint AI workflows yet, or as a personal layer on top of them. They run as you, from your mailbox and Teams account.

| Prompt | What Cowork does | Approvals you'll see |
|---|---|---|
| Every weekday at 7 AM, run the daily sweep on `<site>` and message me only if something is overdue. | Creates a scheduled prompt that loads [`sweep-obligations`](../../../Skills/sweep-obligations/) and messages you only when something is overdue. | Approve the schedule and its unattended tools: SharePoint writes on `<site>` and mail to your own address |
| When a file is added to the Contracts library on `<site>`, capture its obligations. | Creates an event trigger on the SharePoint connector (file created in Contracts) that runs [`capture-obligations`](../../../Skills/capture-obligations/) on the new file. | Create or approve the SharePoint connection; approve the trigger and its SharePoint writes |
| Every morning at 7 AM, assign owners on `<site>`. | Creates a scheduled prompt that runs [`assign-obligation-owners`](../../../Skills/assign-obligation-owners/). | Approve the schedule, its SharePoint writes and messages to owners |
| Every Friday at 3 PM, send me the leadership digest for `<site>`. | Creates a scheduled prompt that runs [`obligation-leadership-digest`](../../../Skills/obligation-leadership-digest/) with you as the only recipient. | Approve the schedule; mail limited to you |
| Every Monday at 8 AM, send me my obligations for the next 30 days. | Creates a scheduled prompt that runs [`obligation-owner-digest`](../../../Skills/obligation-owner-digest/), limited to items you own. | Approve the schedule; mail limited to you |
| Two days before any notice deadline on `<site>`, remind me in Teams. | Creates a daily check of Notice & renewal items due in two days and posts to your Teams chat. | Approve the schedule; Teams posts to you only |
| Pause my Obligation Hub automations until `<date>`. | Lists your hub schedules and triggers and turns them off until that date. | Confirm each change |

## E. Check quality

| Prompt | What Cowork does | Approvals you'll see |
|---|---|---|
| Score the capture on `<site>` against the sample answer key. | Matches Obligations items to the kit's answer key by contract, clause and action, as described in [`../evals/README.md`](../evals/README.md). Reports recall and precision per contract, due-date and party accuracy, pass or fail for each trap type, items that should be held for review ("held correctly x/y"), and anything tracked that should have been excluded or superseded. | None (read-only) |
| Re-capture all sample contracts on `<site>`, then score them against the answer key. | Runs `capture-obligations` (forced) on each sample file, then scores the results as above. | Item creates and updates per contract |
| Show every clause capture excluded from `<contract>` and why. | Reads the contract's Capture Run Log Details and the matching Obligation Types and Exclusions rows. | None |
| How many open items are High risk on `<site>`, and do they fit the risk rule? | Counts open items by Risk and checks each High item against the rule in `capture-obligations` (target: roughly 15–30% High). It suggests changes and makes them only if you say so. | Only if you change items |
| List Run Log failures this week and suggest fixes. | Groups Failed and Partial runs by workflow and quotes their Details. It suggests fixes, such as a missing setting or routing rule. | None |
| Check the hub's lists still match the skills' field names. | Compares the live list schemas with the internal names in [`setup-obligation-hub`'s schema reference](../../../Skills/setup-obligation-hub/references/schema.md) and reports anything missing or renamed. | None |
