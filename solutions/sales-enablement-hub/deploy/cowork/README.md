# Copilot Cowork route

`deploy_run.py` is the script that deployed the tested copy of this hub (see
[../../docs/setup-walkthrough.md](../../docs/setup-walkthrough.md)). It runs `deploy/steps.json` phase by phase from a
Copilot Cowork session, through the SharePoint IQ plugin's helper for `via: iq` steps and the SharePoint connector's
"Send an HTTP request" action for `via: rest` steps.

## What it does for you

- Resolves every token as it goes and saves them in `<state>/tokens.json`:
  - list ids from step 02.14,
  - view ids from `get_views_of_list`,
  - quick step ids from the create result, or `get_quicksteps` as a fallback,
  - the Request content form id from the `create_form` result (`formEditUrl` … `formId=`),
  - item ids from `list_items`, field ids and group ids over REST, and the nav parent id from step 11.07.
- Renders pages, views, the form and seed payloads into `deploy/out/` with `deploy/tools/render.py` rules
  (UTF-8 with BOM for HTML).
- Base64-encodes binary uploads and passes large values as files, so nothing huge goes through the chat.
- Writes one line per step to `<state>/run_log.jsonl` (id, ok, seconds, a short result) and stops at the first failure.

## Run it

1. Put the repo in the Cowork workspace, for example `working/northwind-sales-hub`.
2. Copy `tokens.example.json` to `working/deploy/tokens.json` and fill in the five values.
3. Ask Copilot to run the script with RunScript, one phase or two at a time, after you approve each phase:

   ```
   path: deploy/cowork/deploy_run.py   (copy it under .aether/scripts/ first)
   args: {"phases": [1, 2], "pkg": "working/northwind-sales-hub", "state": "working/deploy"}
   ```

4. Skip the manual steps. 01.01 (create the site) can be done with SharePoint IQ `create_site` first. 11.15 is the theme.
   12.01 is the end-to-end check.

A full run took about 25 minutes of tool time on 2026-11-25. Phase 08 (67 uploads and metadata writes) took about 10 minutes.

## Notes

- Every call goes out with `confirmed: true`. The SharePoint IQ helper still checks that each tool exists and has
  its required settings, but it no longer stops to ask about writes. Approve each phase yourself before you run it.
- REST writes can raise Cowork's own approval card. If they do, the run pauses and resumes after you approve.
- A step that fails twice is a package bug. Record it in `docs/known-issues.md` and fix `deploy/steps.json`.
