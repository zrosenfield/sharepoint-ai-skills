# Client Hub for SharePoint

> **Status: experimental solution sample.** A complete kit for test-site evaluation, not a production-ready CRM. Deployment and tenant behavior have not been verified as part of this repository import.

A simple client tracker for teams that run their clients out of a spreadsheet. It uses three SharePoint lists and the features you already have. You don't need a CRM budget, a tenant admin, Power Apps or a premium licence.

> **Unofficial, personal and unsupported.** This is my personal side project, not a Microsoft product, template or recommendation. Microsoft hasn't reviewed it and doesn't support it. Read the script before you run it, try it on a test site first, and use it at your own risk. Issues and pull requests are welcome, but I can't promise a fix.

## What you get

| Piece | What it does |
|---|---|
| **Clients** list | One row per client: type, products, environments, health, owners, main contact, annual value, renewal date, service desk link |
| **Projects** list | Implementations, migrations and upgrades for each client, with status, owner, target date and next milestone. Includes a **Board** view |
| **Client Activity** list | The timeline: meetings, calls, emails, decisions, changes and issues. Each entry can carry a follow-up with a due date and a ticket link |
| Views | Portfolio cards, Renewals, Due in 30 days, Migrations, Open follow-ups, My follow-ups, Decision log |
| Formatting | Coloured pills for health, status, follow-up and sentiment, a red cue on overdue dates, and a **Mark done** button on open follow-ups |
| Visual timeline (optional) | A view on Client Activity that puts every client's calls, decisions and issues on one timeline, with open follow-ups and renewals marked |
| Client 360 (optional) | One page that shows a client's profile, projects, timeline and open follow-ups together |
| Copilot skills (optional) | Five skills for Copilot in SharePoint: set up the hub, brief me on a client, log this activity, run the weekly review, change the hub safely |
| Sample data | 8 fictional clients, 17 projects and 66 activity entries, so you can try it before you load your own |

Projects and Client Activity each link to a client through a lookup, so one client's history stays in one place and is easy to filter.

## What you need

- A SharePoint site where you can create lists. A site owner can; so can a member with the default Edit permission.
- A modern browser.
- That's it for the core. The Copilot skills also need a Microsoft 365 Copilot licence, and Copilot in SharePoint has to be available in your tenant.
- The optional Visual timeline needs HTML list view support in your tenant. Everything else works without it.

You **don't** need a tenant or SharePoint admin, an app registration, PowerShell, PnP, site scripts, custom script, Power Automate or Power Apps.

## Three ways to set it up

| Path | Best for | Time |
|---|---|---|
| **A. Paste-in script** ([deploy/deploy-clienthub.js](deploy/deploy-clienthub.js)) | Getting everything, including sample data, in one go | About 10 minutes |
| **B. Ask Copilot in SharePoint** ([setup-client-hub](../../Skills/setup-client-hub/SKILL.md)) | People with Copilot who'd rather not run a script | About 15 minutes |
| **C. Click through it** ([SETUP.md](SETUP.md)) | Locked-down browsers, or people who want to understand every piece | 45 to 60 minutes |

All three target the same core list schema, but sample quantities and optional features differ. The script loads the full bundled dataset; the setup skill creates a smaller illustrative dataset. Each path still needs the finishing touches below. The script is not a resume tool: it stops if any target list already exists.

### A. Paste-in script

The script runs in your browser as you, against the site you have open. It uses SharePoint's own REST API, so it can only do what you could already do by hand. It checks that you can manage lists, stops if the lists already exist, and asks before it changes anything.

1. Make a new site, or pick a test site. A Team site or Communication site both work.
2. Open [deploy/deploy-clienthub.js](deploy/deploy-clienthub.js) and read it. If you like, change the options at the top:
   - `sampleData` loads the fictional clients.
   - `shiftDatesToToday` makes "overdue" and "renews in 55 days" true on the day you run it.
   - `timelineView` adds the Visual timeline view to Client Activity. It's on by default.
   - `dashboardPage` uploads the Client 360 page.
   - `setDashboardAsHome` makes that page the site home page. It's off by default.
3. Open the site's home page and press **F12**, or **Ctrl+Shift+I** (**Cmd+Option+I** on a Mac). Go to the **Console** tab.
4. Paste the whole file and press Enter. Chrome and Edge may ask you to type `allow pasting` first.
5. Confirm the prompt. Progress shows in the console, and the script ends with links to everything it made.
6. Do the [finishing touches](#finishing-touches-5-minutes-by-hand).

If something fails partway through, run [deploy/remove-clienthub.js](deploy/remove-clienthub.js) the same way and start again. If your organisation blocks the browser console, use path C.

### B. Ask Copilot in SharePoint

1. Install [setup-client-hub](../../Skills/setup-client-hub/) using the [skill installation instructions](../../Skills/README.md#installing-an-experimental-skill): upload the individual skill folder into **Agent Assets > Skills**. Where **Settings > Site skills** is available, that is another entry point. You need Edit permission to add skills.
2. Open Copilot in SharePoint on the site and ask: **"Set up the client hub on this site."**
3. Copilot shows the plan, asks you to confirm, then builds the lists, columns and views. The setup skill can create a smaller illustrative dataset after confirmation. For the exact 8-client, 17-project, 66-activity dataset, use the script or the CSV files in [sample-data](sample-data).

This path is new and less tested than the script. If Copilot stops partway, use SETUP.md to finish the missing pieces. To restart with the script, first review and remove only the sample lists you created; removal also recycles their data.

### Copilot skills

All five canonical skill sources live in the repository's top-level `Skills/`, not in a second copy inside this kit.

| Skill | Purpose |
|---|---|
| [setup-client-hub](../../Skills/setup-client-hub/) | Builds the lists after confirmation |
| [client-briefing](../../Skills/client-briefing/) | Prepares a client briefing from live list data |
| [log-client-activity](../../Skills/log-client-activity/) | Previews and records an activity after confirmation |
| [weekly-client-review](../../Skills/weekly-client-review/) | Reviews portfolio health, renewals, and follow-ups |
| [crm-change-request](../../Skills/crm-change-request/) | Plans and confirms list-design changes |

The four day-to-day skills require the Client Hub lists to exist first. Upload only the individual folders you need, following the installation instructions above.

### C. Click through it

[SETUP.md](SETUP.md) walks through every list, column, view and format, with JSON you paste into **Format this column** and **Format current view**.

## Finishing touches (5 minutes, by hand)

There's no supported way for a site owner to script these, so they're quick clicks:

1. **Mark done quick step** (where Quick steps are available). In Client Activity, choose **Add column > Quick steps**, then add a step that sets **Follow-up** to **Done**. The Follow-up pill already has a Mark done button, so this is a nice-to-have.
2. **Reminders.** In Client Activity, open the **Due** column menu and choose **Set a reminder** to get an email before a follow-up is due. You can also use **Automate > Rules > When a column changes** to notify the owner.
3. **Form.** Choose **Forms** on Client Activity and make "Log client activity" with Client, Type, Date, Summary, Notes, Follow-up, Next step and Due. Show Next step and Due only when Follow-up is Open.
4. **Client 360 page.** If the HTML page works in your tenant, you're done. If it doesn't (see the FAQ), make a normal page with three List web parts and dynamic filtering. SETUP.md step 6 has the details.

## Using it day to day

- **Monday:** open **Open follow-ups**, sorted by due date. Red means overdue. Click **Mark done** as you clear them.
- **After a call:** add a Client Activity entry. Use Decision for anything agreed and Change for environment or configuration changes, so the Decision log stays useful.
- **Before a renewal:** check the **Renewals** view and the client's Client 360.
- **With Copilot:** "Prep me for my Woodgrove Bank call", "Log this: ...", "Run my Monday client review".

## Uninstall

Run [deploy/remove-clienthub.js](deploy/remove-clienthub.js) from the browser console on the same test site. Review the confirmation carefully: it targets lists by the `Clients`, `Projects`, and `ClientActivity` URLs, not by proof that this kit created them. It moves those lists and `SitePages/Client360.html` to the site recycle bin, where they can normally be restored within 93 days.

If Client 360 is the homepage, removal attempts to set the homepage to `SitePages/Home.aspx`; it does not remember the previous homepage. Restore your preferred homepage yourself. Installed Copilot skills and any normal page or other finishing touches you created separately are not removed by the script.

## FAQ

**Is this a CRM?** No. It's the smallest useful thing: one row per client, a timeline, a next step with a date, and one page that pulls them together. If you need pipelines, quotes, marketing or integrations, buy a CRM.

**Who can see the data?** Everyone with access to the site. The lists inherit the site's permissions, so put it on a site with the right members, and don't keep anything there your organisation wouldn't allow on that site.

**Does the script need custom script turned on?** No. It only creates lists, columns, views and items, and uploads one file to Site Pages.

**The Client 360 page downloads instead of opening.** Your tenant doesn't show .html files from Site Pages as pages. Use the List web part page in SETUP.md step 6 instead. Everything else works without it.

**The Visual timeline is missing or shows a plain list.** Your tenant may not support HTML list views yet. If creation fails, the script attempts to remove the view and reports a manual step; a first load can also take a few seconds. Nothing else depends on it. [SETUP.md section 7](SETUP.md#7-visual-timeline-view-optional) has another way to build one.

**Does opening the HTML page guarantee live data?** No. The experimental template expects its hosting viewer to supply live list results. Without that integration it shows the embedded deployment-time sample snapshot, or empty data if sample data was disabled. Check the live/snapshot badges; use the lists or the normal List web part page for current data.

**Some features look different or missing.** Quick steps, list forms with branching, and Copilot site skills are rolling out at different times in different tenants. The core (lists, lookups, views, column and view formatting, the board view, reminders and rules) is standard SharePoint.

**Can I rename things?** Yes. Change display names freely. The internal names (shown in the script and SETUP.md) are what the formatting and skills refer to, so leave those alone.

## What's in this folder

```
deploy/            deploy-clienthub.js, remove-clienthub.js, spec.json (the list design),
                   client360.template.html, timeline.template.html
formats/           the column and view formatting JSON, for path C
sample-data/       clients.csv, projects.csv, client-activity.csv (fictional)
SETUP.md           manual, click-by-click setup
```

The five skill folders are linked under [Copilot skills](#copilot-skills). Download the repository, not just this solution folder, if you want both the kit and the skills.

## Maintaining the sample

The paste-in deploy script is intentionally self-contained: it embeds the list specification, sample rows, formatting JSON, and dashboard and timeline templates. Changes to `deploy/spec.json`, `formats/`, `sample-data/`, `deploy/client360.template.html`, or `deploy/timeline.template.html` must also update the corresponding embedded content in `deploy/deploy-clienthub.js`; editing an asset alone does not change script deployment.

Keep deployment code outside `Skills/`. SharePoint skills are prose instructions, not a way to execute these browser scripts.

## Licence

MIT. See [LICENSE](LICENSE). The sample companies are the fictional names Microsoft uses in its documentation; any resemblance to real clients is accidental.
