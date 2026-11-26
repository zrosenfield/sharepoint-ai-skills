---
name: setup-obligation-hub
description: Sets up the Obligation Hub, a contract obligation tracker, on the current SharePoint site. Builds the Contracts and Evidence libraries; the Obligations, Obligation Owners, Obligation Types, Exclusions and Run Log lists with their columns, views and colour formatting; the hub settings file; three quick steps; the obligation type catalogue and a default routing rule. Checks what already exists, shows a plan and builds only after one confirmation, never deleting or overwriting data. Use for "set up the obligation hub", "install the obligation tracker on this site", "repair the hub's lists" or the Cowork prompt "Install the Obligation Hub from this kit" on a named site.
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Set up the Obligation Hub

Build the lists, libraries, settings and quick steps the Obligation Hub's other skills depend on. Works in Copilot in SharePoint on the target site, and in Cowork with the SharePoint tools (the user names the site). It's safe to run again: it builds only what's missing. This is an unofficial community sample, not a Microsoft template.

The full specification is in four references. Follow them exactly; internal names must match because every hub skill uses them.
- [references/schema.md](references/schema.md): lists, columns, choices, defaults, views and the settings file
- [references/obligation-types.md](references/obligation-types.md): the 37 seed rows for Obligation Types
- [references/formatting.md](references/formatting.md): the four coloured columns
- [references/quick-steps.md](references/quick-steps.md): the three quick steps

## What this skill doesn't do
Say these up front, in the plan, so nobody expects them:
- **Pages.** The hub's pages (Home, My obligations, Review queue, Contract 360, Leadership, How it works, Settings) need this site's list IDs filled in, then uploading and publishing. Use the kit's paste-in deploy script (`deploy/deploy-obligation-hub.js` with its pages-only option, `pagesOnly`) or the Cowork prompt "Fill in the hub's pages for this site". The lists and views work without the pages.
- **Site look.** The hub's navigation links to the pages, its theme, logo and compact header. The deploy script's pages-only run applies them, or the site owner sets them in **Settings > Change the look**. This skill adds only the Contracts and Obligations navigation links.
- **AI workflows.** The site owner creates the six workflows from the kit's `workflows/ai-workflow-prompts.md`. They run as the person who creates them.
- **Skills and site context upload.** In Copilot in SharePoint this skill can only check whether the other hub skills and `SHAREPOINT.md` are in AgentAssets. Uploading them is a manual step (or a Cowork step when the kit's files are available).
- **Autofill.** It can set the optional autofill prompts on the Contracts columns, but autofill may not run on every tenant. Capture never depends on it.
- **Sample data.** Not loaded here. Use the deploy script's sample option or the Cowork prompt "Load the pre-captured sample".
- **Permissions.** Everyone with access to the site sees every contract and obligation. There are no per-contract permissions.

You need to be able to create lists on the site (site owner). No admin role and no Power Automate are needed.

## 1. Ask once
Ask in ONE message, skipping anything the user already gave:
- **Our company's legal name**, exactly as it appears in contracts (becomes `ourCompany`; decides Party = Us). Required.
- **Leadership digest recipients**: one or more email addresses. Optional; they can be added later.
- **Time zone** for "today" and schedules. Default: Pacific Standard Time.
- **Autofill prompts** on the Contracts columns, Yes or No. Default: Yes.

Use the current site's absolute URL, without a trailing slash, as `siteUrl`. The default routing rule's owner and escalation owner is the person running setup; resolve them once.

## 2. Check what exists (read only)
Read the site before planning. For each piece in references/schema.md, record what is there:
- **Lists and libraries**: present or missing, and their template (list or library).
- **Columns**: by internal name, with type and choices.
- **Views**: by name, and which view is the default.
- **Column formats** on Status, Timing, Risk and ReviewState.
- **Quick steps** on Obligations and Contracts, by title.
- **Obligation Types**: existing row titles.
- **Obligation Owners**: whether a rule with Category = Any, BusinessUnit = Any and an empty Counterparty exists.
- **AgentAssets**: the `Skills` and `Config` folders, `Config/hub-settings.json`, `SHAREPOINT.md` in the root, and which of these skill folders are in `Skills`: setup-obligation-hub, capture-obligations, assign-obligation-owners, sweep-obligations, obligation-owner-digest, obligation-leadership-digest, mark-obligation-fulfilled, exclude-obligation, obligation-hub-guide, clear-obligation-sample-data.

**Conflicts.** A conflict is a hub list name used by a different template (for example a Contracts *list* instead of a library), or a hub internal name on a column of a different type (for example `DueDate` as text). Never change an existing column's type and never rename a list. If a conflict would break the skills, stop before building, name each conflict, and suggest a fresh site or renaming the existing list by hand. A choice column that lacks some of the hub's choices isn't a conflict: plan to add the missing choices and keep the existing ones.

If an existing Contracts library already holds files, say so in the plan: its files and values stay as they are, and once the Capture workflows are on, any file added or changed there will be captured.

## 3. Show the plan and confirm once
Show one table: Piece | Now | Will do. For example:

| Piece | Now | Will do |
|---|---|---|
| Contracts library | Missing | Create with 13 columns plus the title (autofill prompts on 9), then 2 views; nav link |
| Obligations list | Missing | Create with 26 columns plus the title, then 8 views; formats on 4 columns; 2 quick steps; nav link |
| Obligation Types | Exists, 37 rows | Nothing |
| Config/hub-settings.json | Missing | Create with your answers and the defaults |

Under the table, list what this skill won't do (the section above) and the manual steps that will remain. End with: "Reply **yes** to build. Nothing existing is deleted or overwritten." Build only after a clear yes. Don't ask again per step. In Cowork, each SharePoint write still shows its own approval card; tell the user to expect them.

## 4. Build, in this order
Work through the pieces in this order. Skip anything that already exists and note it as skipped. If a step fails, report it, carry on with the steps that don't depend on it, and don't retry more than once.

1. **Contracts library.** Create the library with its columns in one call (references/schema.md, section 1). Rename the built-in title column's display name to "Contract title". If autofill is Yes, give each autofill column its extraction prompt, replacing `<our company>` with `ourCompany`; if the tool refuses the prompts, create plain columns and note "autofill not set". Then, in a **separate** call, make the views: turn the built-in "All Documents" view into "All contracts" (the default) and create "Expiring in 180 days". Add the navigation link.
2. **Obligations list.** Create the list with its 26 columns in one call (section 2), and rename the title column to "Obligation". Then make the eight views in a **separate** call; if that call fails as too large, split the views across two calls. Turn the built-in "All Items" view into "All obligations" and create the other seven. Make "Open by due date" the default. The My obligations filter must compare Owner with the current user as a User value; an Integer value was rejected. Add the navigation link.
3. **Obligation Owners list**, then its view (section 3).
4. **Obligation Types list**, then its view (section 4).
5. **Exclusions list**, then its view (section 5). It starts empty.
6. **Run Log list**, then its view (section 6).

   **Built-in views.** Never delete a list's built-in "All Items" (or, in a library, "All Documents") view: the pages link to its address, `AllItems.aspx`. On a list this run created, turn it into the view marked "(built-in)" in references/schema.md: rename it and set its columns and sort. If the tool can't rename it, leave it as it is, create the named view separately and note it in the report. On a list that already existed, add only the missing views and leave existing ones as they are.
7. **Evidence library** with its columns (section 7). No extra views.
8. **AgentAssets.** Create the library only if it's missing. Create the `Skills` and `Config` folders if they're missing; folder creation may require a folder colour, and any colour works.
9. **Settings file.** If `Config/hub-settings.json` is missing, create it as a JSON object with the keys and defaults in references/schema.md, section 9, filled with the user's answers (`leadershipRecipients` is an empty list if none were given; `leadershipTeamsChannel` has empty `team` and `channel`). If the file exists, don't change it; compare its keys with the table and list any missing ones in the report.
10. **Column formatting** on Obligations `Status`, `Timing`, `Risk` and `ReviewState`, as described in references/formatting.md. Inline styles only.
11. **Quick steps.** Create Mark fulfilled and Remove obligation on Obligations, and Re-capture obligations on Contracts, as described in references/quick-steps.md. Read each list's ID and address first. Skip any title that already exists.
12. **Seed Obligation Types.** Add each row in references/obligation-types.md whose `Title` isn't already in the list (ignore case). Write in batches. Never edit existing rows.
13. **Default routing rule.** If there's no Any/Any rule with an empty Counterparty, add "Default - all obligations": Category Any, BusinessUnit Any, Counterparty empty, Owner and EscalationOwner = the person running setup, Notify Both. Never edit existing rules.
14. **Log.** Write one Run Log row:
    - `Title` = "Setup - <today>"
    - `Workflow` = Setup
    - `Outcome`: Succeeded; Partial if any step failed; Skipped if everything already existed
    - `ItemsCreated` = lists, libraries, views, rows and files created
    - `ItemsUpdated` = existing lists that gained columns, choices or views
    - `ItemsHeld` = 0
    - `RunAt` = now
    - `Details` (≤ 1,000 characters): "Created: …; added: …; skipped (already there): …; failed: …; autofill: on/off/not set". Never start Details with "Demo seed"; that prefix marks sample rows.

## 5. Report, then hand over
Reply with one table: Piece | Result (Created, Added N columns or views, Skipped because it already exists, or Failed with the reason). Then list what is left, in this order:
1. **Skills.** Upload any missing skill folders to `AgentAssets/Skills` (one folder per skill, with its `references` folder where it has one). Name the missing ones.
2. **Site context.** Upload the kit's `assets/SHAREPOINT.md` to the AgentAssets root, if it's missing.

   In Cowork, when the kit's files are available to you, offer to upload the missing skill folders and `SHAREPOINT.md` now, copying them unchanged. Each upload is its own approval card. Never overwrite a file that's already there.
3. **Settings.** Add leadership recipients, or the missing keys found in step 9, by editing `Config/hub-settings.json`.
4. **Pages and site look.** Run the kit's deploy script with `pagesOnly` set to true (it also adds the hub's navigation links, theme, logo and compact header), or use the Cowork prompt "Fill in the hub's pages for this site". Pages uploaded by hand arrive as drafts and must be published before visitors see them or they can be the home page.
5. **AI workflows.** Create these six from the kit's `workflows/ai-workflow-prompts.md`, the two Capture workflows first, and follow `docs/workflow-checklist.md`:

   | Workflow | Trigger | Skill |
   |---|---|---|
   | Capture new contracts | A file is added to Contracts | `capture-obligations` |
   | Capture changed contracts | A file in Contracts is changed | `capture-obligations` |
   | Assign owners | Daily, 7:00 AM | `assign-obligation-owners` |
   | Daily sweep | Daily, 6:00 AM | `sweep-obligations` |
   | Owner digest | Mondays, 8:00 AM | `obligation-owner-digest` |
   | Leadership digest | Fridays, 3:00 PM | `obligation-leadership-digest` |

6. **Routing.** Add Obligation Owners rules beyond the default (by category, business unit or counterparty). The most specific rule wins.
7. **Test.** Upload one contract to Contracts. Within a few minutes the Run Log shows a Capture row, and new items appear in Obligations (held ones in the Needs review view).

Finish with one line pointing to the kit's `SETUP.md` for the same steps by hand.

## Never
- Delete or overwrite anything: lists, libraries, columns, views, items, files or the settings file. The only change to an existing view is turning the built-in view of a list this run created into its catalogue view.
- Change a column's type, remove choices, or rename a list or column internal name.
- Load sample data, upload contracts or use real company or people names in seed rows.
- Create, change or turn on AI workflows.
- Send email or Teams messages.
- Execute deployment code from this skill.
