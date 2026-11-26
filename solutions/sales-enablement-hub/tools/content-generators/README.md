# Content generators

These Python scripts produced the Northwind sample content in `content/`. You don't need them to deploy. Use them to
regenerate or extend the sample.

| Script | Makes |
|---|---|
| `nw_data.py` | Brand, products, customers, slide catalogue and template recipes (the single source of sample data) |
| `nw_pptx.py` | Slide renderers (title, agenda, problem, solution, proof, story, pricing, next steps, close) |
| `build_slides.py` | One-slide `.pptx` files for the Slide Library and the template shells |
| `build_examples.py` | Full example decks for Deck Templates (these are the gallery previews) |
| `build_assets.py` | Content Library documents: pitch decks, battlecards (docx), one-pagers and customer stories (pdf), and the intake and archive samples |
| `fix_ids.py` | Gives every pptx its own slide master and layout id range. **Run this after generating.** See docs/known-issues.md #1. |

Requirements: Python 3.10+, `python-pptx`, `python-docx`, `reportlab`, `Pillow`.

```
cd tools/content-generators
python build_slides.py && python build_examples.py && python build_assets.py && python fix_ids.py
# outputs land in ./content/...; copy them into ../../content/<Library>/
```

`NW-Title-Retail` and `NW-Title-Manufacturing` were added later with `nw_pptx.r_title`. They were given id offsets 40
and 41 so they don't collide with the first 28 files. When you add slides, use an offset that no other file uses.
