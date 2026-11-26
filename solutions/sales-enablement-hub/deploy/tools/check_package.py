#!/usr/bin/env python3
"""Package lint for CI: valid JSON, referenced files exist, no tenant-specific leftovers, every token is documented.

  python deploy/tools/check_package.py
"""
import glob, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
errors = []
def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, "/")
# 1. JSON parses
for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    if "/out/" in p.replace(os.sep, "/") or p.endswith("tokens.local.json"): continue
    try: json.load(open(p, encoding="utf-8-sig"))
    except Exception as e: errors.append("bad JSON %s: %s" % (rel(p), e))
# 2. referenced files exist
site = json.load(open(os.path.join(ROOT, "site", "site.json"), encoding="utf-8"))
for l in site["lists"]:
    if not os.path.exists(os.path.join(ROOT, l["definition"])): errors.append("missing list definition " + l["definition"])
for pg in site["pages"]:
    if not os.path.exists(os.path.join(ROOT, "site", "pages", pg["file"])): errors.append("missing page " + pg["file"])
steps = json.load(open(os.path.join(ROOT, "deploy", "steps.json"), encoding="utf-8"))["steps"]
for s in steps:
    for k in ("contentFrom",):
        if s.get(k) and not os.path.exists(os.path.join(ROOT, s[k])): errors.append("step %s: missing %s" % (s["id"], s[k]))
    for f in (s.get("argFiles") or {}).values():
        if not os.path.exists(os.path.join(ROOT, f)): errors.append("step %s: missing %s" % (s["id"], f))
seed = json.load(open(os.path.join(ROOT, "content", "seed.json"), encoding="utf-8"))
for lib, rows in seed.items():
    for r in rows:
        if "file" in r and not os.path.exists(os.path.join(ROOT, "content", lib, r["file"])): errors.append("seed %s: missing file %s" % (lib, r["file"]))
# 3. no tenant leftovers in text files
LEAK = re.compile(r"sharepoint-df\.com|/sites/zachsaleshub|/sites/zavasaleshub|@microsoft\.com|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
ALLOWED_GUIDS = {"00000000-0000-0000-0000-000000000000"}
for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
    if os.path.isdir(p) or p.endswith((".pptx", ".docx", ".pdf", ".png", ".jpg")) or "/out/" in p.replace(os.sep, "/") or p.endswith("tokens.local.json"): continue
    if os.path.basename(p) == "check_package.py": continue
    t = open(p, encoding="utf-8-sig", errors="ignore").read()
    for m in LEAK.finditer(t):
        if m.group(0).lower() in ALLOWED_GUIDS: continue
        errors.append("tenant-specific value in %s: %s" % (rel(p), m.group(0))); break
# 4. tokens are documented
doc = " ".join(site["tokens"].keys())
known = {re.sub(r":.*", "", k.strip("{}")) for k in re.findall(r"\{\{[^{}]+\}\}", doc)}
known |= {"file", "seed", "NavId", "Today"}
for p in glob.glob(os.path.join(ROOT, "site", "**", "*"), recursive=True) + [os.path.join(ROOT, "deploy", "steps.json"), os.path.join(ROOT, "content", "seed.json")]:
    if os.path.isdir(p) or p.endswith((".png", ".jpg")): continue
    for tok in set(re.findall(r"\{\{([^{}]+)\}\}", open(p, encoding="utf-8-sig", errors="ignore").read())):
        base = re.sub(r"[:+-].*", "", tok)
        if base not in known: errors.append("undocumented token {{%s}} in %s" % (tok, rel(p)))
# 5. ids that only exist after a create step are produced before any step uses them (pages, views, form, formatter)
def step_text(s):
    parts = [json.dumps({k: v for k, v in s.items() if k not in ("notes", "title", "produces", "needs")})]
    files = list((s.get("argFiles") or {}).values())
    if s.get("contentFrom") and s.get("render"): files.append(s["contentFrom"])
    if (s.get("arguments") or {}).get("fromFile"): files.append(s["arguments"]["fromFile"])
    files += re.findall(r"\{\{file:([^}]+)\}\}", parts[0])
    for f in files:
        fp = os.path.join(ROOT, f)
        if os.path.exists(fp): parts.append(open(fp, encoding="utf-8-sig", errors="ignore").read())
    return "\n".join(parts)
produced = set()
for s in steps:
    for tok in set(re.findall(r"\{\{((?:ViewId|ViewIdB64|QuickStepId|NavId):[^{}]+)\}\}", step_text(s))):
        base = tok.replace("ViewIdB64:", "ViewId:")
        if base not in produced and not base.endswith(("/All Documents", "/All Items")):  # default views exist with the list
            errors.append("step %s uses {{%s}} before any step produces it" % (s["id"], tok))
    for pr in s.get("produces") or []:
        m = re.match(r"\{\{([^{}]+)\}\}", pr)
        if m: produced.add(m.group(1).replace("ViewIdB64:", "ViewId:"))
if errors:
    print("\n".join(sorted(set(errors)))); sys.exit(1)
print("Package OK: %d lists, %d pages, %d deploy steps, %d seed sets." % (len(site["lists"]), len(site["pages"]), len(steps), len(seed)))
