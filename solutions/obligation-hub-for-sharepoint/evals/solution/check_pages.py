#!/usr/bin/env python3
"""S-13 static checks on the hub's HTML pages after the tokens are filled in (what gets uploaded).

Per page: no {{TOKEN}} left; the ka-livedata-manifest is the first element in <head>, parses, and each
entry is {kind: list, spItemUrl: "list:<siteUrl>/<listId>", webUrl: <siteUrl>, listId: GUID,
listServerRelativeUrl: "/..."}; every JSON block parses (hub-config siteUrl = site, list ids are GUIDs);
every inline script parses (node `new Function`, skipped with a warning if node is missing); no
absolute URL outside the site's origin and no protocol-relative URL; none of the sandbox-forbidden
APIs (fetch, XMLHttpRequest, WebSocket, import, web storage, cookies, history API, <link>, external
scripts, @import, CSS url() other than #fragments); size < --max-kb; links between hub pages point to
pages that exist under <site>/SitePages. Warnings: non-ASCII characters, workflow setup prompts not
filled, missing sample snapshot, retired skill names (assign-owners, daily-sweep, owner-digest,
leadership-digest, mark-fulfilled), and an in-page menu of hub pages (the pages have none: SharePoint's
site navigation is the only navigation, so add the pages there).
Template files named <Page>.template.html count as <Page>.

Runtime behaviour (live badge, empty-list state, contrast) is covered by the page tests shipped with the
page sources (DOM-stub and contrast tests) and by S-16 on the site; see EVALS.md.

Sample run:
  python3 check_pages.py filled-pages/ --site-url https://<tenant>.sharepoint.com/sites/<site>
  -> one block per page (PASS/FAIL/WARN lines), then "PAGES: PASS (7 pages)"; exit 0/1.
  Templates before install: python3 check_pages.py ../../deploy/pages --allow-tokens
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

EXPECTED = ["Home", "MyObligations", "Contract360", "ReviewQueue", "Leadership", "Settings", "HowItWorks"]
GUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
FORBIDDEN = [
    (re.compile(r"\bfetch\s*\("), "fetch()"),
    (re.compile(r"XMLHttpRequest"), "XMLHttpRequest"),
    (re.compile(r"WebSocket"), "WebSocket"),
    (re.compile(r"\bimport\s*\(|^\s*import\s", re.M), "import"),
    (re.compile(r"localStorage|sessionStorage"), "web storage"),
    (re.compile(r"document\.cookie"), "cookies"),
    (re.compile(r"pushState|replaceState"), "history API"),
    (re.compile(r"<link\b", re.I), "<link> element"),
    (re.compile(r"<script[^>]+\bsrc=", re.I), "external script"),
    (re.compile(r"@import", re.I), "CSS @import"),
    (re.compile(r"url\((?!#|\s*['\"]?#)", re.I), "CSS url() other than in-page fragments"),
    (re.compile(r"""(?:src|href|action)\s*=\s*["']//""", re.I), "protocol-relative URL"),
]
RETIRED = re.compile(r"(?<![\w-])(assign-owners|daily-sweep|owner-digest|leadership-digest|mark-fulfilled)(?![\w-])")
URL = re.compile(r"https?://[^\s\"'<>()\\]+", re.I)


def page_name(path):
    return Path(path).name.split(".")[0]


def node_ok(code, node):
    js = "const fs=require('fs');const c=fs.readFileSync(0,'utf8');try{new Function(c);}catch(e){console.error(e.message);process.exit(1);}"
    r = subprocess.run([node, "-e", js], input=code, capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip()


def check_page(path, html, a, node, present):
    out = []  # (status, message)

    def add(st, msg):
        out.append((st, msg))

    size = len(html.encode("utf-8"))
    add("PASS" if size < a.max_kb * 1024 else "FAIL", f"size {size // 1024} KB (limit {a.max_kb} KB)")
    left = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
    if left and not a.allow_tokens:
        add("FAIL", f"unfilled tokens: {', '.join(left[:8])}{' ...' if len(left) > 8 else ''}")
    else:
        add("PASS", "no unfilled tokens" if not left else f"{len(left)} tokens (allowed)")
    m = re.match(r'\s*<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*<script type="application/json" class="ka-livedata-manifest">(.*?)</script>', html, re.S | re.I)
    site = a.site_url.rstrip("/") if a.site_url else None
    if not m:
        add("FAIL", "ka-livedata-manifest is not the first element in <head>")
    else:
        try:
            man = json.loads(m.group(1))
            problems = []
            for e in man:
                if e.get("kind") != "list":
                    problems.append(f"kind {e.get('kind')!r}")
                lid, web = e.get("listId", ""), e.get("webUrl", "")
                if not a.allow_tokens:
                    if not GUID.match(lid or ""):
                        problems.append(f"listId {lid!r} is not a GUID")
                    if site and web.rstrip("/") != site:
                        problems.append(f"webUrl {web} <> --site-url")
                    if e.get("spItemUrl") != f"list:{web}/{lid}":
                        problems.append(f"spItemUrl {e.get('spItemUrl')} <> list:<webUrl>/<listId>")
                    srv = e.get("listServerRelativeUrl", "")
                    if not srv.startswith("/") or (web and not srv.lower().startswith(urlparse(web).path.lower().rstrip("/") + "/")):
                        problems.append(f"listServerRelativeUrl {srv!r} not under the site path")
                site = site or web.rstrip("/")
            add("FAIL" if problems else "PASS", f"live-data manifest: {len(man)} list(s)" + (": " + "; ".join(problems) if problems else ""))
        except ValueError as e:
            add("FAIL", f"live-data manifest JSON does not parse: {e}")
    n_js = n_json = 0
    bad_js, bad_json = [], []
    for attrs, code in re.findall(r"<script\b([^>]*)>(.*?)</script>", html, flags=re.S | re.I):
        if "application/json" in attrs:
            n_json += 1
            try:
                obj = json.loads(code)
            except ValueError as e:
                bad_json.append(f"{attrs.strip()[:40]}: {e}")
                continue
            if 'id="hub-config"' in attrs and not a.allow_tokens:
                if site and str(obj.get("siteUrl", "")).rstrip("/") != site:
                    bad_json.append(f"hub-config siteUrl {obj.get('siteUrl')} <> {site}")
                for k, v in (obj.get("lists") or {}).items():
                    if "id" in v and not GUID.match(v["id"] or ""):
                        bad_json.append(f"hub-config list {k} id {v['id']!r} is not a GUID")
        else:
            n_js += 1
            if node:
                ok, err = node_ok(code, node)
                if not ok:
                    bad_js.append(f"script #{n_js}: {err[:120]}")
    add("FAIL" if bad_json else "PASS", f"{n_json} JSON blocks parse" + (": " + "; ".join(bad_json[:3]) if bad_json else ""))
    if node:
        add("FAIL" if bad_js else "PASS", f"{n_js} inline scripts parse (node)" + (": " + "; ".join(bad_js[:3]) if bad_js else ""))
    else:
        add("FAIL" if a.require_node else "WARN", f"{n_js} inline scripts NOT parsed: node not found")
    origin = None
    if site:
        u = urlparse(site)
        origin = f"{u.scheme}://{u.netloc}".lower()
    ext = sorted({x for x in URL.findall(html) if not origin or not x.lower().startswith(origin)})
    add("FAIL" if ext else "PASS", "no URLs outside the site origin" + (": " + ", ".join(ext[:5]) if ext else ""))
    hits = []
    for rx, what in FORBIDDEN:
        mm = rx.search(html)
        if mm:
            hits.append(f"{what} at line {html.count(chr(10), 0, mm.start()) + 1}")
    add("FAIL" if hits else "PASS", "sandbox: no forbidden APIs" + (": " + "; ".join(hits) if hits else ""))
    dead = []
    markup = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    for href in re.findall(r'href="([^"#?\s\'()+]+\.html)', markup):
        name = page_name(href.rsplit("/", 1)[-1])
        if present and name not in present:
            dead.append(href)
        elif site and not a.allow_tokens and not href.lower().startswith((site + "/sitepages/").lower()):
            dead.append(href + " (not in <site>/SitePages)")
    add("FAIL" if dead else "PASS", "links between hub pages resolve" + (": " + ", ".join(sorted(set(dead))[:5]) if dead else ""))
    if re.search(r'<nav\b[^>]*aria-label="Obligation Hub pages"|class="nav__track"', html):
        add("WARN", "in-page menu of hub pages found: the pages rely on SharePoint's site navigation; remove the in-page menu")
    if any(ord(c) > 127 for c in html):
        bad = sorted({c for c in html if ord(c) > 127})
        add("WARN", f"non-ASCII characters {''.join(bad[:10])!r}: the manifest precedes <meta charset>, keep pages ASCII")
    if 'data-sample="true"' not in html:
        add("WARN", "no bundled sample snapshot (data-sample) for the Sample snapshot fallback")
    pres = re.findall(r'<pre id="prompt-([A-Z_]+)"[^>]*>(.*?)</pre>', html, re.S)
    unfilled = [k for k, body in pres if "Create an AI workflow" not in body]
    if pres:
        add("WARN" if unfilled else "PASS", f"{len(pres)} workflow setup prompts" + (f"; not filled: {', '.join(unfilled)}" if unfilled else " filled"))
    old = sorted(set(RETIRED.findall(html)))
    if old:
        add("WARN", f"retired skill names: {', '.join(old)} (use assign-obligation-owners, sweep-obligations, obligation-owner-digest, obligation-leadership-digest, mark-obligation-fulfilled)")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="S-13: static checks on filled Obligation Hub pages.")
    ap.add_argument("paths", nargs="+", help="page files or a folder of .html pages")
    ap.add_argument("--site-url", help="expected site URL, no trailing slash (default: taken from each manifest)")
    ap.add_argument("--allow-tokens", action="store_true", help="templates before install: allow {{TOKENS}} and skip URL/GUID checks")
    ap.add_argument("--expect", default=",".join(EXPECTED), help="pages that must be present when a folder is given")
    ap.add_argument("--max-kb", type=int, default=300)
    ap.add_argument("--node", default=shutil.which("node"), help="node executable (default: on PATH)")
    ap.add_argument("--require-node", action="store_true", help="fail when node is not available")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    files = []
    folder = False
    for p in map(Path, a.paths):
        if p.is_dir():
            folder = True
            files += sorted(p.glob("*.html"))
        else:
            files.append(p)
    present = {page_name(f) for f in files}
    failed = 0
    report = {}
    if folder:
        missing = [n for n in a.expect.split(",") if n and n not in present]
        if missing:
            print(f"FAIL  missing pages: {', '.join(missing)}")
            failed += 1
    for f in files:
        res = check_page(f, f.read_text(encoding="utf-8", errors="replace"), a, a.node, present if folder else None)
        report[f.name] = res
        bad = [r for r in res if r[0] == "FAIL" or (a.strict and r[0] == "WARN")]
        failed += bool(bad)
        print(f"{'FAIL' if bad else 'PASS'}  {f.name}")
        for st, msg in res:
            if st != "PASS":
                print(f"      {st}  {msg}")
    print(f"\nPAGES: {'PASS' if not failed else 'FAIL'} ({len(files)} pages{', node ' + a.node if a.node else ', node not found'})")
    if a.json_out:
        json.dump({"pass": not failed, "pages": {k: [{"status": s, "check": m} for s, m in v] for k, v in report.items()}},
                  open(a.json_out, "w", encoding="utf-8"), indent=1)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
