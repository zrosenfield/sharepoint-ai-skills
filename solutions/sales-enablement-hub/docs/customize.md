# Make it yours

The Northwind names live in five places. Change them together.

| What | Where |
|---|---|
| Products, solutions, industries, audiences, stages, asset types | Choice columns in `site/lists/*.json`, and the matching rules in `site/agent-assets/Standards/publishing-standards.md` |
| Publishing rules (retired names, approved customer references, confidentiality line) | `site/agent-assets/Standards/publishing-standards.md` |
| Meeting types and slide roles | `site/lists/04-deck-templates.json` (Template kind), `site/lists/05-decks.json` (Template), `site/agent-assets/Skills/build-customer-deck/SKILL.md` |
| Page text, colors and brand | `tools/page-builder/theme3.py` (tokens and CSS), `build_pages.py` (page copy). Rebuild with `python build_pages.py && python build_deckview.py`, then regenerate the view formatter with `deploy/tools/make_view_formatter.py`. |
| Sample files and their tags | `content/<Library>/` and `content/seed.json` |

## Replace the sample content

1. Remove the Northwind files from `content/` and their rows from `content/seed.json`.
2. Slides: one slide per file. Fix the ids so Copilot's merged decks open (`tools/content-generators/fix_ids.py` shows how).
3. Templates: one example deck per meeting type. Recipe = slide roles in order.
4. Thumbnails for the slide gallery are embedded in `tools/page-builder/thumbs_datauri.json` (320×180 JPEG data
   URIs keyed by file name). Regenerate them from your slides, for example by exporting slide 1 of each file to PNG.

## Approver

Set `{{ApproverEmail}}` and `{{ApproverName}}` to a mail-enabled group so approvals don't depend on one person.

## Tightening for production

- Assign security groups, not people, to the three site groups.
- Review **Sellers: Contribute** on Content Library (see [sharing-model.md](sharing-model.md)).
- Apply a sensitivity label to the site and a retention label to Archive.
- Consider a scheduled freshness check (Copilot or Power Automate) instead of the on-demand quick step.
