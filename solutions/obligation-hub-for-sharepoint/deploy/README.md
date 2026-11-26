# Deploy

Installs and removes the Obligation Hub on a SharePoint site. Everything is driven by [`spec.json`](spec.json).

> Unofficial, personal and unsupported. Not a Microsoft product. See the [README](../README.md).

| File | What it is |
|---|---|
| [`deploy-obligation-hub.js`](deploy-obligation-hub.js) | Paste-in browser console script. It runs as you, against the site you have open, using SharePoint REST. |
| [`remove-obligation-hub.js`](remove-obligation-hub.js) | Undo. It moves the hub's lists, pages, skills and settings to the site recycle bin and removes the hub's navigation links. |
| [`spec.json`](spec.json) | The single source of truth: lists, columns, views, formats, seeds, AgentAssets files, pages and their tokens, the site's look (navigation, header, theme, logo), quick steps, AI workflows, autofill, sample data and what removal covers. |
| [`sync-embedded-spec.js`](sync-embedded-spec.js) | Copies `spec.json` and `../formats/*.json` into the two scripts. Run `node sync-embedded-spec.js --check` to see whether they match. |
| [`pages/`](pages/) | The 7 page templates (`<Name>.template.html`) with `{{TOKENS}}`, and [`tokens.json`](pages/tokens.json), which documents each token |
| [`pages-src/`](pages-src/) | The sources and build script for the page templates |
| [`assets/`](assets/) | The hub logo (`obligation-hub-logo.png`, 300 × 300, and `.svg`) |
| [`cowork/`](cowork/) | The Cowork installer path: job files for the SharePoint IQ tools (see its [README](cowork/README.md)) |

## Run the deploy script

1. Use a test site where you can create lists. To get the site's look as well (navigation, theme, logo, header), you need to be a site owner.
2. Open the site's home page. Press F12, open **Console**, paste the whole of `deploy-obligation-hub.js` and press Enter. If the browser asks you to type "allow pasting", do that first.
3. Read the confirmation and select **OK**. Nothing is written before that.
4. When it finishes, it prints links to the lists and pages, plus the finishing touches that have no REST API: the six AI workflow prompts, the three quick steps (exact titles and prompts) and an autofill prompt for Copilot.

### Options (edit them at the top of the script before you paste)

| Option | Default | What it does |
|---|---|---|
| `assetsBaseUrl` | `https://raw.githubusercontent.com/zrosenfield/sharepoint-ai-skills/master` | Where the kit files come from (the repository root). If a file can't be fetched, it's skipped and reported. The spec and formats are also embedded in the script, so the lists still get built. |
| `sampleData` | `true` | 11 fictional contracts with their key terms, and 2 example routing rules. Every item and file is flagged IsSample = Yes. |
| `preCapturedSample` | `true` | With `sampleData`: 60 pre-captured obligations and 13 Run Log rows labelled "Demo seed", so the hub is full before any workflow runs |
| `shiftDatesToToday` | `false` | Moves every sample date by (today − 2026-11-24). The text inside the Word files doesn't move. |
| `pages` | `true` | Fills in the 7 page templates and uploads them to Site Pages |
| `publishPages` | `true` | Publishes them (an uploaded page is a draft until it's published) |
| `setHome` | `false` | Makes `SitePages/Home.html` the home page, but only once it's published. Needs a site owner. |
| `siteChrome` | `true` | The site's look, for site owners only: hub links in the site navigation, the theme, the logo and the header. It's skipped and listed as a finishing touch for anyone else. |
| `replaceNavigation` | `false` | With `siteChrome`: also removes the default Documents, Pages and Site contents links. Other links are never removed. |
| `applyTheme` | `true` | With `siteChrome`: applies the "Obligation Hub" theme (`spec.json` `site.theme`; the primary colour has 9:1 contrast on white) |
| `setLogo` | `true` | With `siteChrome`: uploads `assets/obligation-hub-logo.png` to Site Assets and makes it the site logo |
| `compactHeader` | `true` | With `siteChrome`: sets a compact header with no background emphasis |
| `companyName` | `""` | Your legal name as written in your contracts. It decides which obligations are "Us". If it's empty, the script uses Northwind Traders, Inc. with sample data, and asks you otherwise. |
| `leadershipEmails` | `[]` | Who gets the Friday leadership digest. If it's empty, the digest goes to you. |
| `pagesOnly` | `false` | Only (re)installs the pages and the site's look, on a site that already has the hub lists (for example, one built with SETUP.md or the `setup-obligation-hub` skill) |
| `resume` | `false` | Continues a run that stopped part-way. It reuses the hub lists and skips columns, views, items and files that already exist. |

### What it does, in order

1. Gets a request digest and checks your permissions: Manage Lists to install, Add Items for pages, and Manage Web for the home page and the site's look.
2. Refuses, and writes nothing, if any hub list or library already exists: Contracts, Obligations, Obligation Owners, Obligation Types, Exclusions, Run Log or Evidence. If AgentAssets exists, it reuses it.
3. Fetches the kit files and asks one `confirm()`.
4. Creates the lists, then the columns. In a library, multi-line text columns get `UnlimitedLengthInDocumentLibrary="TRUE"`, and Person columns are people-only.
5. Adds the views. The built-in "All Items" or "All Documents" view becomes the spec's "all" view, so the AllItems.aspx links the pages use keep working. "Open by due date" becomes the default. "My obligations" filters Owner with `Value Type='User'` and `<UserID/>`. The Calendar view is a modern calendar on Due date; if SharePoint refuses it, the script prints how to add it by hand.
6. Applies the column formatting, then seeds Obligation Types and an Any/Any routing rule that makes you owner and escalation owner.
7. Uploads the skills to `AgentAssets/Skills/<skill>/`, `SHAREPOINT.md` to the AgentAssets root, and `Config/hub-settings.json` (with your company, site URL and recipients). A `SHAREPOINT.md` or `hub-settings.json` that's already there is never overwritten.
8. Loads the sample data. Date-only values are written as `YYYY-MM-DDT12:00:00Z`, and Timing is recomputed for today.
9. Fills each page's tokens: site URL, list IDs, list addresses (spaces become `%20`) and the AI workflow prompts. It then uploads the pages, checks them in, publishes them and checks each one is published.
10. Sets the home page if you asked for it, then the site's look. On a communication site the navigation goes in the top navigation; on a team site it goes in the site navigation, switched to horizontal. A link with the same title and address is never added twice.
11. Writes one Run Log row (Workflow = Setup) and prints the summary and finishing touches.

If a step fails, the script stops and prints what it created so far. Fix the problem, then run it again with `resume: true`, or run `remove-obligation-hub.js`. Theme, logo, header and navigation are cosmetic: if SharePoint refuses one of them, the script lists it as a finishing touch and carries on.

## Remove

Paste `remove-obligation-hub.js` the same way. It lists exactly what it found, asks once, and then:
- Moves the hub lists and libraries, the 7 pages, the hub's skill folders and `Config/hub-settings.json` to the recycle bin, along with `SHAREPOINT.md` if it's the hub's (it mentions "Obligation Hub"). You can restore them from **Site contents > Recycle bin**.
- Deletes the hub's navigation links: only those with the hub's titles and addresses. Links can't go to the recycle bin.
- Sets the home page back to `SitePages/Home.aspx` if it was `SitePages/Home.html`.
- Leaves the AgentAssets library, other skills, other links, and the theme, logo and header alone. It also can't remove AI workflows. Delete those in the site's AI workflows panel, because they fail once the lists are gone.

## What has and hasn't been tested

The scripts are tested against an in-memory mock of the SharePoint REST endpoints they call. The tests cover payloads, order, refusals, cancel, failure and resume, offline mode, the site's look, and removal. **They haven't been run against a live tenant.** The list design, views, formats, skills and pages were built and checked on a test site through the SharePoint IQ tools (the Cowork path), not through this script. Run it on a test site first.

## Maintaining

- Change `spec.json` first, then run `node sync-embedded-spec.js`. Keep internal column names stable, because the skills use them.
- To change the pages, edit `pages-src/src/`, then run `python3 pages-src/build.py`. That rewrites `pages/*.template.html` and `pages/tokens.json`.
- The Cowork job files are generated from the same spec. Never commit generated job files: they hold your site key and list IDs.
