# Setup walkthrough (tested deploy, with screenshots)

This is a record of a real deploy of this package into a brand-new communication site in the SharePoint dogfood
ring on 2026-11-25. The site was called **Zava Sales Hub**. The sample brand inside the pages stays **Northwind Cloud**
unless you rebrand it (see [customize.md](customize.md)).

The deploy ran every step in [`deploy/steps.json`](../deploy/steps.json) with the Copilot Cowork runner in
[`deploy/cowork/`](../deploy/cowork/README.md). It took about **25 minutes of tool time**. The problems it found are
fixed in this version of the package and listed at the end.

| Phase | Steps | Result | Time |
|---|---|---|---|
| 01 Site | 2 | Site created with SharePoint IQ `create_site`, site key resolved | 1 min |
| 02 Lists and libraries | 14 | 11 lists and libraries, 2 renames, ids read back | 2 min |
| 03 Column settings | 13 | Unlimited length on every library Note column | 1 min |
| 04 Skills and assets | 37 | 5 skills, standards, 30 images | 4 min |
| 05 Approvals and quick steps | 12 | Approvals on, 7 quick steps, 2 Actions columns | 1 min |
| 06 Views | 12 | Default views, Pick a template tiles, Start here view | 2 min |
| 07 Forms and deck studio | 3 | Request content form, Start here HTML, one-pager Word form | 1 min |
| 08 Sample content | 67 | 58 files with metadata, 16 list rows | 10 min |
| 09 Pages | 11 | 5 HTML pages uploaded, published, Home set as home page | 1 min |
| 10 Permissions | 27 | 3 groups, unique permissions on 7 lists, item-level security | 3 min |
| 11 Navigation and branding | 15 | Menu, logo, header, theme (1 optional step skipped) | 1 min + manual theme |
| 12 Verify | 1 | One deck built end to end from a template | 5 min |

## Before you start

- You need to be able to create a communication site, or own an empty one.
- Copilot in SharePoint, native approvals, autofill, and SharePoint HTML pages and views must be on in your tenant.
- Choose who approves content (a person or a mail-enabled group) and who owns the sample content (usually you).

## Phase 01: Create the site

Any route works. In the test, SharePoint IQ `create_site` first ran a precheck (`sitecreationprecheckOnly: true`),
then created a communication site with the **General** sensitivity label in about 30 seconds.

A new site opens with a blank home page and a "Start designing your site" prompt. Choose **Maybe later**. Phase 09
replaces the home page.

![A new, empty communication site](images/setup/01-new-site.png)

Then get the SharePoint IQ site key with `get_site_key`. Every later IQ call needs it.

## Phase 02–03: Lists, libraries and column settings

Phase 02 creates the 11 lists and libraries with their columns, choices and autofill prompts. Two are created under
one name and renamed, so their URLs stay stable:

| Created as | Renamed to | URL |
|---|---|---|
| Generated Content | Decks | `/Generated Content` |
| AgentAssets | Agent Assets | `/AgentAssets` |

Step 02.14 reads every list id back. Phase 03 then turns on **Allow unlimited length in document libraries** for every
library Note column. Without it, Copilot's talking points (over 255 characters) fail to save.

![Site contents after phase 02](images/setup/02-site-contents.png)

## Phase 04: Agent skills and hub assets

The five site skills go to `Agent Assets/Skills/<name>/SKILL.md`. Copilot in SharePoint loads them by name when a
quick step says "Load the … site skill". The 28 slide thumbnails, the logo and the header image go to `HubAssets`.

![The five site skills in Agent Assets](images/setup/15-agent-skills.png)

## Phase 05: Approvals and quick steps

Approvals go on Content Intake first. The 7 quick steps come next, then the **Actions** button columns that show them
on each row. Each create returns its `quickStepId`, which later steps need, for example the template tiles.

The buttons are conditional, and their rules read the **Approval status** column, so that column must stay in the
view. A new submission shows only **Run agent review**. **Submit for approval** appears after a passing review, and
**Publish to library** after approval.

![Content Intake with Review status, Validation result and Approval status](images/setup/11-content-intake.png)

![The Actions column: Submit for approval shows only on the row that passed review](images/setup/12-content-intake-actions.png)

## Phase 06: Views

Phase 06 sets each library's default view. Then it adds the two views sellers see first:

- **Deck Templates > Pick a template**: a TILES view whose card formatter carries a **Build with this template** button.
  The button calls the quick step by id, so this runs after phase 05.
- **Decks > Start here**: a custom HTML view. Its HTML is installed in phase 07, after the form exists.

![Pick a template, the tile gallery sellers start from](images/setup/09-pick-a-template.png)

## Phase 07: Request content form, then the deck studio view

Step 07.01 creates the **Request content** form on Content Requests. The form is stored as a hidden view.
`get_views_of_list` does **not** return it, so take its id from the result's `formEditUrl` (`formId=<id>`). That id,
base64-encoded, is the **Ask for content** link on every page and in the Start here view.

![The Request content form](images/setup/13-request-content-form.png)

Step 07.03 then installs the **Start here** deck studio HTML into the Decks view. Step 07.02 is optional and runs after
phase 08: a Word document form on the industry one-pager template.

![Decks opens on Start here, the deck studio](images/setup/10-decks-start-here.png)

## Phase 08: Sample content

Upload every file first, then write its metadata. Uploading over an existing file clears its columns. The runner reads
item ids back with `list_items`, then writes all of a library's metadata in one `update_list_items_v2` call. Dates are
relative to deploy day, so one asset is always about to expire and one has expired.

## Phase 09: Pages

The five HTML pages are rendered for the site and uploaded as UTF-8 with BOM. Uploaded pages start as drafts, so each
one is published. Then Home.html becomes the site home page.

![Home: live content, search and the two main actions](images/setup/03-home-hero.png)

![Home: featured assets read live from Content Library](images/setup/04-home-featured.png)

![Find: every approved asset with filters](images/setup/06-find.png)

![Plays: guided selling plays, each with Build a deck for this play](images/setup/07-plays.png)

![Slide gallery: approved slides with real thumbnails](images/setup/08-slide-gallery.png)

![Publishing Desk: the content team's review, requests, freshness and usage](images/setup/14-publishing-desk.png)

## Phase 10: Permissions

The three associated groups are renamed and described: **Owners** (Full Control), **Content Team** (Edit) and
**Sellers** (Read). Then each list gets its own permissions:

- Sellers can't see Content Intake, Archive or the Publishing Desk page.
- Sellers get Contribute on Content Library, Decks, Content Requests and Customer Shares.
- In Content Requests and Customer Shares, people see and edit only their own items.
- The Content Team gets Read only on Agent Assets.

The "different permissions" banner is expected.

![Site permissions after phase 10](images/setup/16-permissions.png)

## Phase 11: Navigation and branding

The menu is Home, Find, Plays, Build a deck and Content team (Publishing Desk, Content Intake, Content Library), with
the logo, header image and a compact header.

![The site menu](images/setup/05-navigation.png)

The theme is the one manual step. Open the **home page** (not a settings page), then choose
**Settings > Change the look > Theme > Dark teal > Save**.

![Change the look > Theme > Dark teal](images/setup/17-theme-dark-teal.png)

## Phase 12: Build one deck end to end

On Deck Templates > Pick a template, press **Build with this template** on any card. In the test, Quarterly business
review was used. Copilot loads the `build-customer-deck` site skill:

![Build with this template starts Copilot with the site skill](images/setup/18-build-with-template.png)

Card 1 asks for the industry, the customer and the meeting goal:

![Card 1: industry, customer and goal](images/setup/19-copilot-questions.png)

Card 2 offers approved slides for each role in the template's recipe, with a recommendation:

![Card 2: approved slide choices](images/setup/20-copilot-slide-choices.png)

Copilot saves the deck to Decks, then asks once before it writes the details. Press **Update**:

![Copilot confirms the details write](images/setup/21-copilot-update-item.png)

The test deck was "Zava Retail - Quarterly business review", with 7 slides and the retail title slide. All seven
details were filled: Customer, Template, Industry, Meeting goal, Status, Source slides and Talking points.

![The finished deck](images/setup/22-deck-ready.png)

Finish with [deploy-checklist.md](deploy-checklist.md).

## What the test deploy found and fixed

| # | Found | Fix in this package |
|---|---|---|
| 1 | The Start here view failed to install: its HTML links to the Request content form, which was created one phase later | The Start here HTML is now step 07.03, after the form (07.01). `check_package.py` now fails any step that uses a view, quick step or nav id before a step produces it. |
| 2 | The form's id couldn't be read back with `get_views_of_list` (the form view is hidden) | Steps and playbook now take it from the `create_form` result (`formEditUrl` … `formId=`). The Cowork runner does this automatically. |
| 3 | Setting the site thumbnail (11.12) returned HTTP 502 | Marked optional. The logo, header image and header layout all applied. |
| 4 | Quick step ids were read back with an extra call | The create result returns `quickStepId`; notes updated. |
| 5 | The theme can't be set from a settings page | The note now says to open the home page first. |
| 6 | Content Intake showed no approval columns, and **Submit for approval** never appeared, even on items that passed review. Approvals were on; the view step (06.01) ran after them and replaced the view's columns without Approval status and Approvers. The buttons' rules read `[$_ApprovalStatus]`, so without it they stayed hidden. | Step 06.01 and the list definition now keep `_ApprovalStatus` and `_ApprovalAssignedTo` in the view. |
