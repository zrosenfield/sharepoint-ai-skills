#!/usr/bin/env python3
"""Turn a custom HTML view page into the CustomFormatter value SharePoint stores for a CUSTOMHTML view.

  python deploy/tools/make_view_formatter.py site/views/decks-start-here.html "Start here" > site/views/decks-start-here.formatter.txt

The stored value is the overlay JSON with '&' escaped as '&amp;' and ']]>' escaped. When you write it through REST
(MERGE _api/web/lists(guid'..')/views(guid'..') {"CustomFormatter": ...}), wrap it as <![CDATA[ ... ]]>.
Run this after editing the HTML (or after tools/page-builder/build_deckview.py), then commit both files.
"""
import json, sys
SCHEMA = "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json"
def stored_formatter(html, title):
    fj = json.dumps({"$schema": SCHEMA, "viewOverlayFormatter": {"customHtml": html, "title": title}}, ensure_ascii=False, separators=(",", ":"))
    return fj.replace("&", "&amp;").replace("]]>", "]]\\u003e")
if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(stored_formatter(open(sys.argv[1], encoding="utf-8-sig").read(), sys.argv[2]))
