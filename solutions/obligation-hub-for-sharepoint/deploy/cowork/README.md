# Cowork installer path

For people who use Cowork with the SharePoint IQ tools and would rather not paste a script into the browser console. Two small Python scripts turn [`../spec.json`](../spec.json) into **job files**: ordered lists of SharePoint IQ tool calls that a Cowork helper runs one by one. You approve each write as it runs.

> Unofficial, personal and unsupported. Not a Microsoft product. See the [README](../../README.md).

The `setup-obligation-hub` skill covers the same ground in prose if you'd rather just ask Copilot or Cowork to build it. This path is more exact: every argument comes from the spec, in the shapes that worked when the hub was first built.

## What you need

- A test site where you're a **site owner**.
- Cowork with the SharePoint IQ tools, and a helper that runs a job file. A job file is a JSON array of `{"label", "mode": "call", "tool", "arguments", "argFiles"}`, where each `argFiles` entry names a local file whose text becomes that argument (for example a skill's `SKILL.md`).
- Python 3 to run `build_jobs.py` and `fill_pages.py`. They use only the standard library.
- A local copy of this repository. The jobs point at files in it.

**The job files hold your site key and list IDs. Write them to a folder outside the repository** (the examples use `../live/`) and don't commit them.

## Run order

| Step | You run | What it does | You approve |
|---|---|---|---|
| 0 | `get_site_key` for your site | Gets the opaque site key the tools need | Nothing |
| 1 | `python3 build_jobs.py --site-url <site> --site-key <key> --out <folder> --company "<legal name>"` (add `--sample` for the sample data) | Writes phases 1 to 3 | Nothing |
| 2 | `phase1_lists.json` | Creates Contracts, Obligations, Obligation Owners, Obligation Types, Exclusions, Run Log, Evidence and AgentAssets with their columns, but no views. Obligations takes two calls, because one call with every column and view failed with "too many stages". Skip the AgentAssets job if the site already has that library. | One card per list |
| 3 | `discover_sharepoint_lists`, then save its result as a JSON file. Also `get_user_info` for yourself, and copy its `formattedValue`. | Gets the list IDs and your Person value | Nothing |
| 4 | `build_jobs.py` again with the same arguments, plus `--lists <saved file> --owner-value '<formattedValue>'` | Writes phases 4 to 6 (`--owner-email` builds a Person value if you have no `formattedValue`) | Nothing |
| 5 | `phase2_views.json` | Adds the views in separate calls. Open by due date leaves out undated items, Triggered and ongoing holds the undated ones, and My obligations filters Owner with `Value Type='User'` | One card per call |
| 6 | `phase3_formatting.json` | Adds coloured pills for Status, Timing, Risk and Review | One card per column |
| 7 | `phase4_seeds_folders_uploads.json` | Seeds Obligation Types (37 rows) and the default routing rule (you), creates `AgentAssets/Skills/<skill>` and `Config` (each folder needs a colour), and uploads the skills, `SHAREPOINT.md` (to the AgentAssets root) and a filled-in `Config/hub-settings.json` | Item creates, folders, uploads |
| 8 | `phase5_sample.json` (only with `--sample`) | Uploads the 11 fictional contracts and fills in their key terms. Loads the 60 pre-captured obligations and the 13 Run Log rows labelled "Demo seed", all flagged IsSample | Uploads, updates, item creates |
| 9 | `phase6_quicksteps.json` | Adds the quick steps Mark fulfilled, Remove obligation and Re-capture obligations, and one Setup row in the Run Log | One card per quick step |
| 10 | `python3 fill_pages.py --site-url <site> --site-key <key> --lists <saved file> --out <folder>` (add `--set-home`), then `phase7_pages.json` | Fills the page templates with your site's URL, list IDs and workflow prompts, then uploads them to Site Pages | Uploads |
| 11 | Open each page in Site Pages and **Publish** it | Uploaded pages are drafts until published. There's no IQ tool for publishing. | Each page |
| 12 | The `set_site_homepage` job at the end of `phase7_pages.json`, if you added `--set-home` | Makes `SitePages/Home.html` the home page. Run it only after Home.html is published. | One card |

Run `python3 build_jobs.py --help` to see every option. `--no-autofill` creates the Contracts columns without autofill prompts. `--today YYYY-MM-DD` fixes the date that sample Timing is computed from. `--confirmed` marks write jobs as already approved, for helpers that support it.

## Finishing touches the IQ tools can't do

The script path does these for site owners (see `siteChrome` in [`../deploy-obligation-hub.js`](../deploy-obligation-hub.js)). On this path, do them by hand.

1. **Site navigation.** The site navigation is the hub's only navigation; the pages have none of their own. Go to **Settings (gear) > Change the look > Navigation** and set the site navigation to horizontal. Then select **Edit** on the site navigation and add these links in this order:

   | Link | Address |
   |---|---|
   | Overview | `<site>/SitePages/Home.html` |
   | My obligations | `<site>/SitePages/MyObligations.html` |
   | Contracts | `<site>/Contracts` |
   | Obligations | `<site>/Lists/Obligations` |
   | Review | `<site>/SitePages/ReviewQueue.html` |
   | Leadership | `<site>/SitePages/Leadership.html` |
   | How it works | `<site>/SitePages/HowItWorks.html` |
   | Settings | `<site>/SitePages/Settings.html` |

   You can remove the default Documents, Pages and Site contents links. The lists were created with a navigation link each, so remove the extra Contracts and Obligations links too.
2. **Header.** Go to **Settings > Change the look > Header** and set **Layout** to Compact and **Background** to None.
3. **Logo.** Go to **Settings > Change the look > Header > Site logo > Change**, then upload [`../assets/obligation-hub-logo.png`](../assets/obligation-hub-logo.png).
4. **Theme.** The "Obligation Hub" palette (`site.theme` in `spec.json`) **can only be applied by script**. One way is the deploy script with `pagesOnly: true`, which also does steps 1 to 3 for a site owner. The other is a tenant admin adding it as a company theme. Otherwise, pick the closest blue theme in **Settings > Change the look > Theme**.
5. **AI workflows.** Create the six workflows from [`../../workflows/ai-workflow-prompts.md`](../../workflows/ai-workflow-prompts.md), Capture first. Each has one trigger and runs as the person who creates it. AI workflows are a preview feature that may not be available in your tenant yet.
6. **Autofill (optional).** Phase 1 already includes the autofill prompts on the Contracts columns. Autofill may not run on every tenant, and capture never depends on it.

## How this path differs from the script

| | Script (`deploy-obligation-hub.js`) | Cowork job files |
|---|---|---|
| "All Items" view | Turned into the spec's "all" view, so it keeps its AllItems.aspx address | Kept as an extra view, as on the first build. The pages link to AllItems.aspx, so leave it. |
| Contracts summary length | Unlimited (`UnlimitedLengthInDocumentLibrary`) | Capped at 255 characters by the tool, so the autofill prompt asks for under 250 |
| Sample contract IDs | Looked up after each upload | Assumes a new, empty Contracts library numbers the uploads 1 to 11 in order. If it doesn't, fix the `itemId` values in phase 5. |
| Person values | Your user ID from REST | `--owner-value` (`formattedValue` from `get_user_info`) or `--owner-email` |
| Pages | Published by the script | Uploaded as drafts; you publish them |
| Site look | Navigation, theme, logo and header for site owners | By hand (see above) |

## If something fails

- **"too many stages":** a call held too many columns and views together. The job files already split them, so re-run only the failed job.
- **"folderColor is required":** every `create_folder` entry needs a colour. The generated jobs include one.
- **A view filter on Owner is rejected:** it must use `Value Type='User'` with `<UserID/>`. The spec already does.
- **A summary longer than 255 characters fails to save:** shorten it. Phase 5's summaries are all under 250.
- **To start again:** run [`../remove-obligation-hub.js`](../remove-obligation-hub.js) from the browser console. It moves the hub to the recycle bin. Or delete the lists by hand.
