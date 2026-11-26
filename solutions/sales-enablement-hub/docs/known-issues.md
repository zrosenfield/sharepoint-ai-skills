# Known issues and workarounds

These were all found while building the reference site. Each one is already handled in the package, and the notes
say how.

| # | Symptom | Cause | Workaround in this package |
|---|---|---|---|
| 1 | Copilot's merged deck saves fine, but PowerPoint for the web says "Sorry, we ran into a problem" | Copilot renumbers slide masters but keeps layout ids. Slides made from one template share layout ids, so the ids collide. | Every sample slide has its own master and layout id range: `tools/content-generators/fix_ids.py` adds 10,000 per file. Do the same for your slides. Product bug write-up below. |
| 2 | Copilot's write of Talking points fails: "This field can have no more than 255 characters" | Multi-line columns in **document libraries** cap at 255 characters unless *Allow unlimited length in document libraries* is on | Deploy phase 03 sets `UnlimitedLengthInDocumentLibrary` on every library Note column |
| 3 | A file's columns go blank after re-uploading it | Overwriting a file through upload replaces the list item's values | Upload first, then write metadata (phase 08). Don't overwrite seeded files. |
| 4 | Pages changes don't show for other people | Uploaded HTML pages in Site Pages are drafts | Publish each page (phase 09), or open it and press **Publish changes** |
| 5 | Links like `Plays.html#play=5` open the wrong place | HTML pages run in a sandboxed blob iframe, so hash and relative links don't survive | Pages use absolute URLs with `target="_top"` and full view URLs (`.../Forms/<View>.aspx`) |
| 6 | A middle dot shows as `Â·` | The HTML was saved without a BOM | Save pages as UTF-8 **with BOM**. `render.py` and the PnP script do this. |
| 7 | Some decks were saved with empty detail columns, SourceSlides most often | Copilot sometimes skips a column in its write | The skill lists all seven columns by internal name, reads the item back, and rewrites missing columns once |
| 8 | Copilot shows an **Update item** card before saving the details | Copilot in SharePoint confirms writes to item columns | Expected. The seller presses **Update** once. Mention it in demos. |
| 9 | The Industry question shows only two options and "Something else" | The card renders a short list plus free text | Acceptable. Free text works. The skill maps the answer to the Industry choice. |
| 10 | Copilot asks "How would you like to create this PowerPoint?" | The deck flow offers a visual redesign | The skill says to copy slides as they are and not offer a redesign |
| 11 | Copilot won't tailor the text inside copied slides | Copied slides are kept verbatim | Talking points carry the tailoring: the opening line, the new title for slide 1, one line per slide |
| 12 | The template gallery button does nothing on a new site | The tiles formatter calls the quick step by id, and ids are per site | Phase 06 renders `{{QuickStepId:Deck Templates/Build with this template}}` into the formatter after phase 05 creates the quick step |
| 13 | The Start here view (and every **Ask for content** link) needs the Request content form's id, but the form didn't exist yet | The Start here HTML was installed one phase before the form was created | Step order is now form (07.01), then Start here (07.03). `check_package.py` fails any step that uses a view, quick step or nav id before a step produces it. |
| 14 | `get_views_of_list` doesn't return the Request content form | The form is stored as a hidden FORMS view | Take the id from the `create_form` result: `formEditUrl` … `formId=<id>` (or base64 in `formShareUrl` … `nav=`) |
| 15 | Setting the site thumbnail returned HTTP 502 BadGateway | Seen once on the test deploy; the logo and header image calls succeeded | Step 11.12 is optional. Set the thumbnail in Change the look if you want one. |
| 16 | Page titles and headings say "Northwind Sales Hub" on a site with another name | The sample pages carry the sample brand | Expected for the sample. Rebrand with `tools/page-builder` (see customize.md). |
| 18 | No approval columns on Content Intake, and **Submit for approval** never appears | A view step that replaces the columns ran after approvals added them; the buttons' rules read `[$_ApprovalStatus]`, which must be in the view | 06.01 now keeps `_ApprovalStatus` and `_ApprovalAssignedTo` in the default view |
| 17 | Copilot opens in the side pane on every library page after you use it once | Copilot remembers the open pane | Close it with **X**. It doesn't affect the hub. |
