---
applyTo: "solutions/sales-enablement-hub/**"
---

# Copilot instructions for Sales Enablement Hub

This repo is a **deployable SharePoint sample**: a sales enablement hub built only from SharePoint lists and libraries,
quick steps, approvals, Copilot in SharePoint site skills, and HTML pages and views. It has no server code and no SPFx.

## Ground rules
- `site/` and `content/` are tenant-neutral. Never commit a real tenant URL, list GUID, email address or user name.
  Use double-brace tokens (documented in `site/site.json` > `tokens`). `python deploy/tools/check_package.py` enforces this.
- `site/pages/*.html` and `site/views/decks-start-here.html` are **generated**. Change `tools/page-builder/*`, then
  rebuild, then regenerate `site/views/decks-start-here.formatter.txt` with `deploy/tools/make_view_formatter.py`.
  CI fails if they drift.
- `deploy/steps.json` is the ordered source of truth for deployment. When you add a column, view, quick step or file,
  add it to the list definition in `site/lists/` **and** to `deploy/steps.json`. Also update the PnP script if it
  should handle it.
- Column internal names are an API. Skills, pages and seed data reference them (`MeetingGoal`, `SourceSlides`,
  `TalkingPoints`, `Shareability`, ...). Don't rename them.
- Library multi-line columns must be listed in `unlimitedLength`, or Copilot writes over 255 characters fail.
- Slide files must keep unique master and layout id ranges (`tools/content-generators/fix_ids.py`).
- A step that uses a view, quick step or nav id must come after the step that `produces` it. `check_package.py`
  enforces this. Forms are hidden views: their id comes from the `create_form` result, not `get_views_of_list`.
- Screenshots in `docs/images/` must not show real names, emails or profile photos. Blur or crop them first.

## Useful commands
```
python deploy/tools/check_package.py
python deploy/tools/render.py --tokens deploy/tokens.local.json --check
cd tools/page-builder && python build_pages.py && python build_deckview.py
```

## Open work (good first issues)
1. Run `deploy/pnp/Deploy-NorthwindSalesHub.ps1` against a test site and fix the TODOs: autofill through the field
   XML, and `ViewType2` over REST.
2. Port `deploy/cowork/deploy_run.py` to a plain SharePoint IQ MCP client, so it runs outside Copilot Cowork.
3. Add a `{{HubName}}` token so the page titles and headings follow the site name instead of "Northwind Sales Hub".
4. Generate `tools/page-builder/thumbs_datauri.json` from `content/Slide Library/*.pptx` instead of keeping it by hand.
