# Page builder

This is the source of the HTML pages in `site/pages/` and the Decks **Start here** view in `site/views/`. Edit here,
not in the generated HTML.

```
cd tools/page-builder
python build_pages.py      # Home, Find, Plays, SlideBuilder, PublishingDesk -> ../../site/pages/
python build_deckview.py   # deck studio -> ../../site/views/decks-start-here.html
cd ../..
python deploy/tools/make_view_formatter.py site/views/decks-start-here.html "Start here" > site/views/decks-start-here.formatter.txt
```

| File | Role |
|---|---|
| `page_common.py` | Site and list tokens, the live-data loader (`ka-livedata-manifest` plus a `rows()` adapter with snapshot fallback), and URL helpers |
| `theme3.py` | The "Atmospheric Precision" design: CSS variables, icons, header, `page3()` wrapper |
| `build_pages.py` | Page content and per-page scripts |
| `build_deckview.py` | Deck studio view |
| `snapshot.json` | Fallback data embedded in pages for when live data isn't available (tokenized) |
| `thumbs_datauri.json` | Slide thumbnails (320×180 JPEG data URIs) keyed by slide file name |

Output keeps the double-brace tokens (`{{SiteUrl}}`, `{{ListId:...}}`). Deploy resolves them. Running both builders
reproduces the committed files byte for byte, so CI can check for drift.
