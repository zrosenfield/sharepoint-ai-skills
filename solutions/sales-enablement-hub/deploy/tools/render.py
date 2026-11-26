#!/usr/bin/env python3
"""Render the package for one target site.

Reads a tokens file (JSON object: {"{{SiteUrl}}": "...", "{{ListId:Decks}}": "...", ...}) and writes ready-to-upload
copies of the pages, the view formatters, the form definition and SharePoint IQ item payloads to deploy/out/.

  python deploy/tools/render.py --tokens deploy/tokens.local.json            # render everything
  python deploy/tools/render.py --tokens deploy/tokens.local.json --check    # only report unresolved tokens

Standard library only. Pages are written as UTF-8 with BOM (SharePoint HTML pages need it for non-ASCII characters).
"""
import argparse, base64, datetime, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = re.compile(r"\{\{[^{}]+\}\}")
TODAY = re.compile(r"\{\{Today([+-]\d+)?\}\}")

def load_tokens(path):
    t = json.load(open(path, encoding="utf-8-sig"))
    # derived tokens: base64 forms of list and view ids
    for k, v in list(t.items()):
        m = re.match(r"\{\{(ListId|ViewId):(.+)\}\}$", k)
        if m and v:
            t["{{%sB64:%s}}" % (m.group(1), m.group(2))] = base64.b64encode(str(v).encode()).decode()
    if "{{SiteUrl}}" in t:
        from urllib.parse import urlparse
        u = urlparse(t["{{SiteUrl}}"])
        t.setdefault("{{TenantUrl}}", "%s://%s" % (u.scheme, u.netloc))
        t.setdefault("{{TenantHost}}", u.netloc)
        t.setdefault("{{SitePath}}", u.path.rstrip("/"))
    return t

def render(text, tokens, today=None):
    today = today or datetime.date.today()
    text = TODAY.sub(lambda m: (today + datetime.timedelta(days=int(m.group(1) or 0))).isoformat() + "T12:00:00Z", text)
    for k in sorted(tokens, key=len, reverse=True):
        text = text.replace(k, str(tokens[k]))
    return text

def iq_value(v):
    """Value format SharePoint IQ update_list_items_v2 / create_list_items_v2 accept."""
    if isinstance(v, bool): return "1" if v else "0"
    if isinstance(v, list): return ";#" + ";#".join(v) + ";#"
    if isinstance(v, dict) and "Url" in v: return "%s, %s" % (v["Url"], v.get("Description") or v["Url"])
    return "" if v is None else str(v)

def person(email):
    return json.dumps([{"Key": "i:0#.f|membership|" + email}])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--out", default=os.path.join(ROOT, "deploy", "out"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    tokens = load_tokens(a.tokens)
    site = json.load(open(os.path.join(ROOT, "site", "site.json"), encoding="utf-8"))
    jobs = [("site/pages/" + p["file"], "pages/" + p["file"], True) for p in site["pages"]]
    jobs += [("site/views/decks-start-here.formatter.txt", "views/decks-start-here.formatter.txt", False),
             ("site/views/decks-start-here.html", "views/decks-start-here.html", True),
             ("site/views/deck-templates-pick-a-template.tiles.json", "views/deck-templates-pick-a-template.tiles.json", False),
             ("site/forms/content-requests.request-content.json", "forms/content-requests.request-content.json", False)]
    missing = {}
    for src, dst, bom in jobs:
        text = render(open(os.path.join(ROOT, src), encoding="utf-8-sig").read(), tokens)
        left = sorted(set(TOKEN.findall(text)))
        if left: missing[src] = left
        if not a.check:
            p = os.path.join(a.out, dst); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n").write(text)
    # SharePoint IQ item payloads from content/seed.json
    seed = json.loads(render(open(os.path.join(ROOT, "content", "seed.json"), encoding="utf-8").read(), tokens))
    payloads = {}
    for name, rows in seed.items():
        items = []
        for r in rows:
            r = dict(r); f = r.pop("file", None)
            names = list(r); vals = [person(v) if k == "ContentOwner" else iq_value(v) for k, v in r.items()]
            if f:
                items.append({"itemId": tokens.get("{{ItemId:%s/%s}}" % (name, f), "{{ItemId:%s/%s}}" % (name, f)), "file": f, "fieldInternalNames": names, "newValues": vals})
            else:
                items.append({"fieldInternalNames": names, "values": vals})
        payloads[name] = items
        left = sorted(set(TOKEN.findall(json.dumps(items))))
        if left: missing["seed:" + name] = left[:5] + (["…%d more" % (len(left) - 5)] if len(left) > 5 else [])
    if not a.check:
        p = os.path.join(a.out, "seed-iq.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(payloads, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if missing:
        print("Unresolved tokens:"); [print("  %s: %s" % (k, ", ".join(v))) for k, v in missing.items()]
    else:
        print("All tokens resolved.")
    if not a.check: print("Wrote", a.out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
