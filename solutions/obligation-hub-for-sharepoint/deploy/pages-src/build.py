#!/usr/bin/env python3
"""Build the Obligation Hub pages.

    python3 build.py

Reads shared sources from src/, inlines CSS, JS, the icon sprite and the
sample snapshots, and writes one standalone HTML file per page to dist/.
The pages carry no navigation bar: SharePoint's site navigation is the one
primary nav. Each page shows only a quiet "Obligation Hub" mark (no links).
Then it verifies every page: each inline script parses in Node
(`new Function(code)`), every JSON block parses, the page is < 300 KB,
there are no external URLs or forbidden APIs, and every {{TOKEN}} used is
documented in tokens.json (which this script also writes).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import snapshots

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
DIST = HERE / "dist"
MAX_BYTES = 300 * 1024

PAGES = [
    {"name": "Home", "title": "Obligations", "lists": ["OBLIGATIONS", "CONTRACTS", "RUNLOG", "OWNERS"]},
    {"name": "MyObligations", "title": "My obligations", "lists": ["OBLIGATIONS"]},
    {"name": "Contract360", "title": "Contract 360", "lists": ["CONTRACTS", "OBLIGATIONS", "RUNLOG"]},
    {"name": "ReviewQueue", "title": "Review queue", "lists": ["OBLIGATIONS"]},
    {"name": "Leadership", "title": "Leadership", "lists": ["OBLIGATIONS"]},
    {"name": "Settings", "title": "Settings", "lists": ["RUNLOG", "OWNERS"]},
    {"name": "HowItWorks", "title": "How it works", "lists": ["OBLIGATIONS"]},
]

DEMO = "https://contoso.sharepoint.com/sites/obligationhub"
TOKENS = {
    "SITE_URL": ("Absolute URL of the Obligation Hub site, no trailing slash.", DEMO, "url"),
    "SITE_URL_ORIGIN": ("Scheme and host of the site (https://host), no trailing slash. Prefixed to server-relative list URLs.",
                        "https://contoso.sharepoint.com", "url"),
    "PAGES_URL": ("Absolute URL of the folder that holds these .html pages (the SitePages library), no trailing slash.",
                  DEMO + "/SitePages", "url"),
    "LISTID_OBLIGATIONS": ("GUID of the Obligations list, without braces. Also used in the live-data manifest key.", "00000000-0000-0000-0000-000000000000", "guid"),
    "LISTID_CONTRACTS": ("GUID of the Contracts document library, without braces. Used in the live-data manifest and the library settings link.", "00000000-0000-0000-0000-000000000000", "guid"),
    "LISTID_RUNLOG": ("GUID of the Run Log list, without braces.", "00000000-0000-0000-0000-000000000000", "guid"),
    "LISTID_OWNERS": ("GUID of the Obligation Owners list, without braces.", "00000000-0000-0000-0000-000000000000", "guid"),
    "LISTURL_OBLIGATIONS": ("Server-relative root of the Obligations list (no trailing slash).", "/sites/obligationhub/Lists/Obligations", "path"),
    "LISTURL_CONTRACTS": ("Server-relative root of the Contracts library (no trailing slash). Views live under /Forms/.", "/sites/obligationhub/Contracts", "path"),
    "LISTURL_RUNLOG": ("Server-relative root of the Run Log list.", "/sites/obligationhub/Lists/RunLog", "path"),
    "LISTURL_OWNERS": ("Server-relative root of the Obligation Owners list.", "/sites/obligationhub/Lists/ObligationOwners", "path"),
    "LISTURL_TYPES": ("Server-relative root of the Obligation Types list.", "/sites/obligationhub/Lists/ObligationTypes", "path"),
    "LISTURL_EXCLUSIONS": ("Server-relative root of the Exclusions list.", "/sites/obligationhub/Lists/Exclusions", "path"),
    "LISTURL_EVIDENCE": ("Server-relative root of the Evidence library. Views live under /Forms/.", "/sites/obligationhub/Evidence", "path"),
    "LISTURL_AGENTASSETS": ("Server-relative root of the AgentAssets library (skills live in Skills/<skill-name>/SKILL.md).", "/sites/obligationhub/AgentAssets", "path"),
}
PROMPT_MEANING = ("Complete setup prompt for the \u201c{name}\u201d AI workflow. A site owner pastes it into Copilot in SharePoint "
                  "on this site to create the workflow; it starts \u201cCreate an AI workflow named \u2026\u201d.")
ENCODING = {
    "url": "Insert verbatim. Must not contain quotes, < > or whitespace (it appears in HTML attributes and JSON strings).",
    "guid": "Insert verbatim, lowercase or uppercase, without braces.",
    "path": "Insert verbatim, starting with '/', no trailing slash; percent-encode spaces (%20).",
    "html-text": "HTML-escape before inserting (& < > to &amp; &lt; &gt;). It sits inside a <pre> element; line breaks are preserved.",
}

# key, workflow name, its one trigger, skill, what it does, Run Log "Workflow" value it logs as
WORKFLOWS = [
    ("CAPTURE_NEW", "Capture new contracts", "When a file is added to the Contracts library", "capture-obligations",
     "Reads each newly added contract, classifies its clauses using Obligation Types and Exclusions, and creates its "
     "obligations. Anything it isn&rsquo;t sure about is held for review.", "Capture"),
    ("CAPTURE_CHANGED", "Capture changed contracts", "When a file is changed in the Contracts library", "capture-obligations",
     "Runs the same skill when a contract file changes &mdash; a new version, or edited key terms &mdash; and updates that "
     "contract&rsquo;s obligations instead of adding duplicates.", "Capture"),
    ("ASSIGN_OWNERS", "Assign owners", "Daily at 7:00 AM and after capture", "assign-obligation-owners",
     "Matches each obligation without an owner to the most specific routing rule and sets its owner and escalation owner.",
     "Assign owners"),
    ("DAILY_SWEEP", "Daily sweep", "Daily at 6:00 AM", "sweep-obligations",
     "Recalculates timing on every open obligation, reminds owners about items coming due and escalates overdue ones.",
     "Daily sweep"),
    ("OWNER_DIGEST", "Owner digest", "Mondays at 8:00 AM", "obligation-owner-digest",
     "Sends each owner a summary of their open obligations for the weeks ahead.", "Owner digest"),
    ("LEADERSHIP_DIGEST", "Leadership digest", "Fridays at 3:00 PM", "obligation-leadership-digest",
     "Sends leaders the week&rsquo;s picture: overdue and high-risk items, notice windows coming up and what changed.",
     "Leadership digest"),
]
for _key, _name, *_rest in WORKFLOWS:
    TOKENS["WORKFLOW_PROMPT_" + _key] = (PROMPT_MEANING.format(name=_name), "Create an AI workflow named \u201c%s\u201d \u2026" % _name, "html-text")


def workflows_html():
    items = []
    for key, name, trigger, skill, what, logs_as in WORKFLOWS:
        folder = "{{SITE_URL_ORIGIN}}{{LISTURL_AGENTASSETS}}/Forms/AllItems.aspx?id={{LISTURL_AGENTASSETS}}/Skills/" + skill
        items.append(f"""<li><article class="card wf-card" aria-labelledby="wf-{key}">
  <div><h3 id="wf-{key}">{name}</h3><p class="wf-card__what">{what}</p></div>
  <dl class="wf-facts"><div><dt>Trigger</dt><dd>{trigger}</dd></div><div><dt>Skill</dt><dd><a href="{folder}" target="_top"><code>{skill}</code></a></dd></div><div><dt>Run Log entry</dt><dd>{logs_as}</dd></div></dl>
  <div class="wf-last" id="wf-last-{key}"><span class="skel skel--w60"></span></div>
  <details class="wf-prompt disclose"><summary><svg aria-hidden="true"><use href="#i-chev"></use></svg>Setup prompt</summary>
    <div class="wf-prompt__box">
      <div class="wf-prompt__bar"><span>A complete instruction. Open <strong>Copilot in SharePoint on this site</strong>, paste it, and Copilot creates the workflow.</span>
        <button type="button" class="chip btn--sm" data-copy="" data-copy-from="prompt-{key}"><svg aria-hidden="true"><use href="#i-copy"></use></svg><span class="chip__state" data-idle="Copy prompt">Copy prompt</span><span class="sr-only"> for {name}</span></button></div>
      <pre id="prompt-{key}" tabindex="0" aria-label="Setup prompt for {name}">{{{{WORKFLOW_PROMPT_{key}}}}}</pre>
      <p class="wf-prompt__todo" id="prompt-todo-{key}" hidden>The prompt text is added when the kit is installed. Until then, this box shows its placeholder.</p>
    </div>
  </details>
</article></li>""")
    return '<ul class="wf">\n' + "\n".join(items) + "\n</ul>"


FORBIDDEN = [
    (re.compile(r"https?:", re.I), "absolute URL"),
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
    (re.compile(r"""(?:src|href)\s*=\s*["']//""", re.I), "protocol-relative URL"),
]


def read(p):
    return (SRC / p).read_text(encoding="utf-8")


def json_for_script(obj):
    s = json.dumps(obj, ensure_ascii=True, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def ascii_only(html):
    """Keep the output pure ASCII so the encoding never matters (the manifest
    must precede <meta charset>)."""
    parts = re.split(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)", html, flags=re.S | re.I)
    out = []
    for part in parts:
        if part.lower().startswith("<script"):
            out.append("".join(c if ord(c) < 128 else "".join("\\u%04x" % u for u in _utf16(c)) for c in part))
        elif part.lower().startswith("<style"):
            bad = [c for c in part if ord(c) >= 128]
            if bad:
                raise SystemExit(f"non-ASCII in CSS: {bad[:5]}")
            out.append(part)
        else:
            out.append("".join(c if ord(c) < 128 else "&#x%X;" % ord(c) for c in part))
    return "".join(out)


def _utf16(c):
    o = ord(c)
    if o <= 0xFFFF:
        return [o]
    o -= 0x10000
    return [0xD800 + (o >> 10), 0xDC00 + (o & 0x3FF)]


def config():
    return {
        "siteUrl": "{{SITE_URL}}", "origin": "{{SITE_URL_ORIGIN}}", "pagesUrl": "{{PAGES_URL}}", "currency": "USD",
        "lists": {
            "OBLIGATIONS": {"id": "{{LISTID_OBLIGATIONS}}", "url": "{{LISTURL_OBLIGATIONS}}"},
            "CONTRACTS": {"id": "{{LISTID_CONTRACTS}}", "url": "{{LISTURL_CONTRACTS}}", "library": True},
            "RUNLOG": {"id": "{{LISTID_RUNLOG}}", "url": "{{LISTURL_RUNLOG}}"},
            "OWNERS": {"id": "{{LISTID_OWNERS}}", "url": "{{LISTURL_OWNERS}}"},
            "TYPES": {"url": "{{LISTURL_TYPES}}"},
            "EXCLUSIONS": {"url": "{{LISTURL_EXCLUSIONS}}"},
            "EVIDENCE": {"url": "{{LISTURL_EVIDENCE}}", "library": True},
            "AGENTASSETS": {"url": "{{LISTURL_AGENTASSETS}}", "library": True},
        },
    }


def manifest(lists):
    return [{
        "kind": "list",
        "spItemUrl": "list:{{SITE_URL}}/{{LISTID_%s}}" % k,
        "webUrl": "{{SITE_URL}}",
        "listId": "{{LISTID_%s}}" % k,
        "listServerRelativeUrl": "{{LISTURL_%s}}" % k,
    } for k in lists]


def build_page(page, snaps, shared):
    name = page["name"]
    body = read(f"pages/{name}.body.html").replace("@@WORKFLOWS@@", workflows_html()).replace("@@HUB_MARK@@", shared["mark"])
    if "@@" in body:
        raise SystemExit(f"{name}: unreplaced @@ placeholder in body")
    page_css = (SRC / f"pages/{name}.css")
    page_js = read(f"pages/{name}.js")
    css = shared["css"] + ("\n" + page_css.read_text(encoding="utf-8") if page_css.exists() else "")
    snap_tags = "\n".join(
        f'<script type="application/json" id="snapshot-{k.lower()}" data-sample="true">{json_for_script(snaps[k.lower()])}</script>'
        for k in page["lists"])
    html = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        f'<script type="application/json" class="ka-livedata-manifest">{json.dumps(manifest(page["lists"]), separators=(",", ":"))}</script>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{page["title"]} &middot; Obligation Hub</title>\n'
        f"<style>\n{css}\n</style>\n</head>\n"
        f'<body class="page-{name.lower()}">\n{shared["sprite"]}\n{body}\n{shared["footer"]}\n'
        f'<script type="application/json" id="hub-config">{json_for_script(config())}</script>\n'
        f"{snap_tags}\n"
        f"<script>\n{shared['core']}\n</script>\n<script>\n{page_js}\n</script>\n</body>\n</html>\n"
    )
    return ascii_only(html)


def node_parse(code, label):
    js = "const fs=require('fs');const c=fs.readFileSync(0,'utf8');try{new Function(c);}catch(e){console.error(e.message);process.exit(1);}"
    r = subprocess.run(["node", "-e", js], input=code, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"JS parse error in {label}: {r.stderr.strip()}")


def verify(path, html):
    problems = []
    size = len(html.encode("utf-8"))
    if size >= MAX_BYTES:
        problems.append(f"too large: {size} bytes")
    scripts = re.findall(r"<script\b([^>]*)>(.*?)</script>", html, flags=re.S | re.I)
    n_js = n_json = 0
    for attrs, code in scripts:
        if "application/json" in attrs:
            json.loads(code)
            n_json += 1
        else:
            node_parse(code, f"{path.name} script #{n_js + 1}")
            n_js += 1
    if not html.startswith("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<script type=\"application/json\" class=\"ka-livedata-manifest\">"):
        problems.append("manifest is not the first element after <head>")
    for rx, what in FORBIDDEN:
        m = rx.search(html)
        if m:
            line = html.count("\n", 0, m.start()) + 1
            problems.append(f"{what} at line {line}: {html[m.start():m.start() + 60]!r}")
    if any(ord(c) > 127 for c in html):
        problems.append("non-ASCII characters present")
    tokens = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html))
    undocumented = tokens - set(TOKENS)
    if undocumented:
        problems.append(f"undocumented tokens: {sorted(undocumented)}")
    return {"bytes": size, "scripts": n_js, "json": n_json, "tokens": tokens, "problems": problems}


def write_tokens(used):
    doc = {
        "about": "Tokens in the Obligation Hub pages. The installer replaces each {{TOKEN}} in every dist/*.html file "
                 "with the value for the target site before upload. Values marked 'url', 'guid' or 'path' also appear "
                 "inside JSON strings, so they must be JSON-safe (no quotes or backslashes).",
        "demoSite": DEMO,
        "tokens": [
            {"token": "{{%s}}" % k, "meaning": v[0], "example": v[1], "kind": v[2], "encoding": ENCODING[v[2]],
             "usedIn": sorted(used.get(k, []))}
            for k, v in TOKENS.items()
        ],
    }
    (HERE / "tokens.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def main():
    snaps = snapshots.build()
    for k, v in snaps.items():
        (SRC / "data" / f"{k}.json").write_text(json.dumps(v, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    shared = {
        "css": read("shared/base.css"), "core": read("shared/core.js"), "sprite": read("shared/sprite.html").strip(),
        "mark": read("shared/hubmark.html").strip(), "footer": read("shared/footer.html").strip(),
    }
    DIST.mkdir(exist_ok=True)
    used, ok = {}, True
    print(f"{'page':<22}{'bytes':>9}  scripts  json  tokens")
    for page in PAGES:
        if not (SRC / f"pages/{page['name']}.body.html").exists():
            print(f"{page['name']}: source missing, skipped")
            ok = False
            continue
        html = build_page(page, snaps, shared)
        out = DIST / f"{page['name']}.html"
        out.write_text(html, encoding="utf-8")
        res = verify(out, html)
        for t in res["tokens"]:
            used.setdefault(t, []).append(out.name)
        print(f"{out.name:<22}{res['bytes']:>9}  {res['scripts']:>7}  {res['json']:>4}  {len(res['tokens']):>6}")
        for p in res["problems"]:
            ok = False
            print(f"   PROBLEM: {p}")
    write_tokens(used)
    unused = sorted(set(TOKENS) - set(used))
    if unused:
        print("documented but unused tokens:", unused)
    print("tokens.json written:", len(TOKENS), "tokens documented,", len(used), "used")
    if not ok:
        sys.exit(1)
    print("All pages built and verified.")
    if "--test" in sys.argv:
        run_tests()


def run_tests():
    """fixtures -> DOM-stub tests (dist + installed) -> contrast; add --browser for headless Chromium."""
    steps = [["python3", "tests/fixtures.py"], ["node", "tests/dom_stub_test.js", "dist"],
             ["node", "tests/dom_stub_test.js", "installed"], ["python3", "tests/contrast.py"]]
    if "--browser" in sys.argv:
        steps.append(["python3", "tests/browser_test.py"])
    for cmd in steps:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"{'PASS' if r.returncode == 0 else 'FAIL'}  {' '.join(cmd)}  ->  {tail}")
        if r.returncode:
            print(r.stdout[-3000:], r.stderr[-2000:])
            sys.exit(1)


if __name__ == "__main__":
    main()
