# Deploy playbook

`deploy/steps.json` lists, in order, every step that builds the hub. Each step names how it runs:

| via | Meaning |
|---|---|
| `iq` | A SharePoint IQ tool call: `tool` plus `arguments`. `contentFrom` is a file in this repo to send as `content`; `encode: base64` means send it base64 with `contentType: base64`. `argFiles` maps an argument to a file whose text is the value. |
| `rest` | A SharePoint REST call against `{{SiteUrl}}`, with `Accept` and `Content-Type` set to `application/json;odata=nometadata`. A `MERGE` carries `X-HTTP-Method: MERGE` and `IF-MATCH: *`. |
| `manual` | A person does it, for example creating the site or picking the theme. |

Steps that create something name the token they produce in `produces`. Later steps use that token.

## Tested route: Copilot Cowork runner

The tested deploy ([docs/setup-walkthrough.md](../docs/setup-walkthrough.md)) used [`deploy/cowork/deploy_run.py`](cowork/README.md).
It runs these steps phase by phase and resolves every token itself. Use it when you deploy from Copilot Cowork with the
SharePoint IQ plugin. Use the prompt below with any other agent.

## Agent prompt (Copilot + SharePoint IQ)

Enable the SharePoint IQ plugin, attach this repo or its zip, and paste:

> Deploy the Northwind Sales Hub package to **<site URL>**. The approver is **<name, email>**.
> Follow `deploy/PLAYBOOK.md`. Run `deploy/steps.json` phase by phase. Before each call, resolve every double-brace
> token from `site/site.json` "tokens" and from the ids that earlier steps produced. Keep a tokens file as you go.
> Use `deploy/tools/render.py` to render the pages, views, form and seed payloads. Ask me once per phase before
> writing. Stop and tell me if a step fails twice. When you finish, give me the checklist in `docs/deploy-checklist.md`
> with each item marked.

## Order and why

| Phase | What | Notes |
|---|---|---|
| 01 Site | Create the site, get the IQ site key | Use any communication site. Its title is used in the group names. |
| 02 Lists and libraries | Create all 11, then read their ids | Decks is created as `Generated Content` and then renamed, so pages and skills keep the same URL. Agent Assets is created as `AgentAssets` and then renamed. |
| 03 Column settings | Unlimited length on library Note columns | **Required.** Without it, Copilot's talking points (over 255 characters) fail to save. |
| 04 Skills and assets | Agent Assets folders, skills, standards, thumbnails, logo and header | Copilot loads skills from `Agent Assets/Skills/<name>/SKILL.md`. |
| 05 Approvals and quick steps | Approvals on Content Intake, then 7 quick steps, then the Actions button columns | The quick steps must exist before the buttons, and before the tiles card that calls one. |
| 06 Views | Default views, Pick a template (TILES) and its tile cards, the Start here view (CUSTOMHTML, empty for now) | The tile cards need the quick step id from phase 05. |
| 07 Forms and deck studio | Request content form (07.01), then the Start here HTML (07.03); optional one-pager Word form (07.02, after 08) | 07.01 produces the form id that the Start here HTML and the pages link to, so 07.03 must come after it. |
| 08 Sample content | Upload files, then write metadata; add list rows | Upload before writing metadata. Re-uploading a file wipes its columns. |
| 09 Pages | Render, upload as UTF-8 with BOM, publish, set Home.html as home | Uploaded HTML pages start as drafts. Publish them, or open each page and press **Publish changes**. |
| 10 Permissions | Rename and describe groups, break inheritance, set roles and item-level security | Group principal ids come from the associated groups. |
| 11 Navigation and branding | Top menu, mega menu, links, logo, header image, compact header | The theme step is manual. |
| 12 Verify | `docs/deploy-checklist.md` and one end-to-end deck build | |

## Resolving ids

| Token | How to get it |
|---|---|
| `{{SiteKey}}` | IQ `get_site_key` with `siteUrl` |
| `{{ListId:X}}` | REST `GET _api/web/lists?$select=Id,Title`. The title is the list title, for example `Decks`. |
| `{{ViewId:X/V}}` | IQ `get_views_of_list`, or REST `GET _api/web/lists(guid'..')/views?$select=Id,Title` |
| `{{ViewId:Content Requests/Request content}}` | The `create_form` result (step 07.01): the GUID after `formId=` in `formEditUrl`. The form view is hidden, so `get_views_of_list` does not list it. |
| `{{QuickStepId:X/T}}` | The `quickStepId` in the `create_or_update_quick_step` result. Or IQ `get_quicksteps` with `listId`: the `ID` (equals `RuleTemplateId`) of the step titled T. |
| `{{FieldId:X/F}}` | IQ `get_list_schema`, or REST `GET _api/web/lists(guid'..')/fields?$select=Id,InternalName` |
| `{{GroupId:...}}` | REST `GET _api/web?$expand=AssociatedOwnerGroup,AssociatedMemberGroup,AssociatedVisitorGroup` |
| `{{ItemId:Lib/file}}` | IQ `list_items` (with `listId`, `rowLimit`, `viewFields` `FileLeafRef`), or the upload result |
| `{{ListIdB64:X}}`, `{{ViewIdB64:X/V}}` | base64 of the GUID string. `render.py` derives them. |
| `{{Today+N}}` | `render.py` writes `yyyy-MM-ddT12:00:00Z` for deploy day plus N |
| `{{NavId:Content team}}` | The `Id` returned when step 11.07 adds the parent menu link |
| `{{seed:X}}` (step argument) | The `items` array for X from `deploy/out/seed-iq.json` |
| `{{file:path}}` (step argument) | The text of that file after rendering, from `deploy/out/` |
| `fromFile` (step 07.01) | Send the rendered JSON in that file as the arguments, plus `siteKey` |

Save resolved values in `deploy/tokens.local.json`, which git ignores. Then render:

```
python deploy/tools/render.py --tokens deploy/tokens.local.json          # writes deploy/out/
python deploy/tools/render.py --tokens deploy/tokens.local.json --check  # lists what is still unresolved
```

`deploy/out/seed-iq.json` holds ready-to-send `items` for `update_list_items_v2` (libraries) and `create_list_items_v2`
(lists).

## Value formats for SharePoint IQ item writes

| Column type | Format |
|---|---|
| Multi-choice | `;#A;#B;#` |
| Yes/No | `"1"` / `"0"` |
| Date | `2026-12-01T12:00:00Z` |
| Hyperlink | `"<url>, <description>"` |
| Person | `[{"Key":"i:0#.f|membership|user@contoso.com"}]` |
| Field names | Always the internal name (`MeetingGoal`, not "Meeting goal") |

## AI layer only (after the PnP route)

The PnP script builds lists, columns, views, content, pages, groups, permissions, navigation and branding. Then run
these phases with SharePoint IQ, using `deploy/tokens.local.json` written by the script:

1. **05.01**: approvals on Content Intake.
2. **05.02–05.08**: the 7 quick steps.
3. **05.09–05.12**: the Actions columns and their buttons.
4. **06.xx**:
   - Recreate **Pick a template** and **Start here** if their view type did not take.
   - Apply the tiles formatter (06.12).
5. **07.01**: the Request content form. Take its id from the result's `formEditUrl` (`formId=`).
6. **07.03**: install the Start here HTML, rendered with that form id.
7. Run the PnP script again with `-PagesOnly -RequestFormViewId <id>` so the pages' **Ask for content** links point at the form.
8. If the autofill prompts did not take through the field XML, run 02.xx `create_or_update_list` again with
   `isNewList: false` for Content Intake and Slide Library. Their columns carry `metadataExtractionPrompt`.

## Things that will bite you

- **Writes need confirmation.** SharePoint IQ holds every write until you approve it. Approve one phase at a time.
- **HTML pages are sandboxed iframes.** `#hash` deep links between pages do not survive. Link to full view URLs
  (`.../Forms/<View>.aspx`), as the pages already do.
- **Merged decks:** new slide files need unique slide master and layout ids, or Copilot's merged deck will not open.
  The sample slides already have them. See `tools/content-generators/fix_ids.py` and `docs/known-issues.md`.
- **Overwriting an upload** clears the file's columns. Write metadata after the final upload.
