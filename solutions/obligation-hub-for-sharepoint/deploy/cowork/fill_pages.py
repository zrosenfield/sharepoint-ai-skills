#!/usr/bin/env python3
"""Fill the Obligation Hub page templates for one site and write the upload jobs.

    python3 fill_pages.py --site-url https://contoso.sharepoint.com/sites/obligations \
        --lists discover.json --site-key <key> --out ../../../../live/obligation-hub-jobs [--set-home]

Reads ../pages/<Name>.template.html and the token rules in ../spec.json ("pageTokens"), replaces
every {{TOKEN}} with this site's URL, list IDs and list addresses (spaces as %20) and the AI
workflow prompts (HTML-escaped), checks nothing is left, and writes:
  <out>/pages/<Name>.html        the filled pages
  <out>/phase7_pages.json        upload_file jobs for Site Pages (+ set_site_homepage with --set-home)
Uploaded pages are drafts: publish each one (open it, Publish) before setting the home page.
"""
import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_jobs import REPO, find_lists  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default=str(HERE.parent / "spec.json"))
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--lists", required=True, help="saved discover_sharepoint_lists result")
    ap.add_argument("--site-key", default="{{SITE_KEY}}")
    ap.add_argument("--out", required=True)
    ap.add_argument("--set-home", action="store_true", help="add a set_site_homepage job for Home.html (run it after publishing)")
    ap.add_argument("--confirmed", action="store_true")
    ap.add_argument("--paths-relative-to", default=os.getcwd())
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    site = a.site_url.rstrip("/")
    m = re.match(r"^(https://[^/]+)(/.*)?$", site)
    if not m:
        sys.exit("--site-url must be an absolute https URL")
    origin, site_rel = m.group(1), m.group(2) or ""
    ids = find_lists(a.lists, spec, site_rel)
    by = {L["key"]: L for L in spec["lists"]}
    prompts = {w["key"]: w["prompt"] for w in spec["workflows"]}

    def value(t):
        v = t["value"]
        if v == "siteUrl":
            return site
        if v == "origin":
            return origin
        if v == "siteUrl + /SitePages":
            return site + "/SitePages"
        if v.startswith("listId:"):
            k = v[7:]
            if k not in ids:
                sys.exit("list %s not found in %s" % (by[k]["title"], a.lists))
            return ids[k]["id"]
        if v.startswith("listUrl:"):
            return quote(site_rel + "/" + by[v[8:]]["url"], safe="/")
        if v.startswith("workflowPrompt:"):
            return html.escape(prompts[v[15:]], quote=False)
        sys.exit("unknown token rule " + v)

    values = [(t["token"], value(t)) for t in spec["pageTokens"]]
    out = Path(a.out).resolve()
    (out / "pages").mkdir(parents=True, exist_ok=True)
    rel = lambda p: os.path.relpath(str(p), a.paths_relative_to).replace("\\", "/")
    jobs = []
    for p in spec["pages"]:
        t = (REPO / p["template"]).read_text(encoding="utf-8")
        for tok, val in values:
            t = t.replace(tok, val)
        left = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", t)))
        if left:
            sys.exit("%s: unfilled tokens %s" % (p["name"], ", ".join(left)))
        name = p["target"].split("/")[-1]
        dest = out / "pages" / name
        dest.write_text(t, encoding="utf-8")
        j = {"label": "Upload page " + name, "mode": "call", "tool": "upload_file"}
        if a.confirmed:
            j["confirmed"] = True
        j["arguments"] = {"siteKey": a.site_key, "folderServerRelativeUrl": site_rel + "/SitePages", "fileName": name, "contentType": "text", "overwrite": True}
        j["argFiles"] = {"content": rel(dest)}
        jobs.append(j)
        print("filled %s (%d bytes)" % (name, len(t.encode("utf-8"))))
    home = next((p for p in spec["pages"] if p.get("home")), None)
    if a.set_home and home:
        j = {"label": "Set home page (only after publishing " + home["target"] + ")", "mode": "call", "tool": "set_site_homepage"}
        if a.confirmed:
            j["confirmed"] = True
        j["arguments"] = {"siteKey": a.site_key, "webUrl": site, "pageUrl": site_rel + "/" + home["target"]}
        jobs.append(j)
    (out / "phase7_pages.json").write_text(json.dumps(jobs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d jobs). Publish each page before visitors can see it." % (out / "phase7_pages.json", len(jobs)))


if __name__ == "__main__":
    main()
