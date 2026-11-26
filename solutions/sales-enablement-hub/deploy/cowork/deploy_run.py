# Runs deploy/steps.json against one site from a Copilot Cowork session, resolving tokens as it goes.
#
# Requirements: Copilot Cowork with the SharePoint IQ plugin on (it provides .aether/scripts/iq_call.py and the
# SharePoint connector). Run it with RunScript, one or two phases at a time:
#   args {"phases": [1, 2], "pkg": "working/northwind-sales-hub", "state": "working/deploy"}
# The state folder holds tokens.json (seed it with SiteUrl, SiteTitle, ApproverEmail, ApproverName, OwnerEmail)
# and run_log.jsonl. Every call is sent confirmed: only run a phase the site owner has approved.
# Other args: "ids": ["05.01"], "skip": ["11.12"], "continueOnError": true, "dry": true (list the steps only).
import json, os, re, base64, urllib.parse, importlib.util, datetime, traceback
from aether_tools import tools, set_result, log, ToolError, args as _args
A = _args()
PKG = A.get("pkg", "working/pkg/northwind-sales-hub")
ST = A.get("state", "working/deploy")
TOKF = os.path.join(ST, "tokens.json")
LOGF = os.path.join(ST, "run_log.jsonl")
OUT = os.path.join(PKG, "deploy", "out")
tok = json.load(open(TOKF, encoding="utf-8"))
SITE = tok["{{SiteUrl}}"]
u = urllib.parse.urlparse(SITE)
tok.setdefault("{{TenantUrl}}", "%s://%s" % (u.scheme, u.netloc)); tok.setdefault("{{TenantHost}}", u.netloc)
tok.setdefault("{{SitePath}}", u.path.rstrip("/"))
def save_tok():
    json.dump(tok, open(TOKF, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
steps = json.load(open(os.path.join(PKG, "deploy", "steps.json"), encoding="utf-8"))["steps"]
spec = importlib.util.spec_from_file_location("render", os.path.join(PKG, "deploy", "tools", "render.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
TOKEN = re.compile(r"\{\{[^{}]+\}\}")

# ---- IQ helper (same checks as the helper; confirmed because the user asked for this deploy)
_src = open(".aether/scripts/iq_call.py", encoding="utf-8").read()
_src = _src[:_src.rindex("\ntry:\n    set_result(main())")]
def iq(tool, arguments, argFiles=None):
    a = {"mode": "call", "tool": tool, "arguments": arguments, "confirmed": True,
         "host": "%s://%s" % (u.scheme, u.netloc)}  # the tenant that hosts the site
    if argFiles: a["argFiles"] = argFiles
    for attempt in range(2):
        ns = {"__name__": "iq_call_batch"}
        exec(compile(_src, "iq_call.py", "exec"), ns)
        ns["args"] = lambda a=a: a
        try:
            r = ns["main"]()
        except ns["HelperError"] as e:
            r = dict({"ok": False, "error": str(e)}, **{k: v for k, v in e.extra.items() if v is not None})
        if r.get("needsLearn"):
            continue
        return r
    return r

# ---- REST through the SharePoint connector
C = "shared_sharepointonline"
DS = urllib.parse.quote(SITE, safe="")
_conns = tools.powerplatform.ListConnections(connector_id=C).payload
if isinstance(_conns, str): _conns = json.loads(_conns)
CONN = [c for c in _conns["connections"] if c.get("usable")][0]["connection_id"]
def rest(method, uri, body=None, headers=None):
    h = {"Accept": "application/json;odata=nometadata", "Content-Type": "application/json;odata=nometadata"}
    h.update(headers or {})
    req = {"dataset": DS, "method": method, "uri": uri, "headers": h}
    if body is not None:
        req["body"] = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
    try:
        r = tools.powerplatform.InvokeConnectorOperation(connector_id=C, connection_id=CONN, operation_id="HttpRequest", params=req)
    except ToolError as e:
        return {"ok": False, "error": str(e)[:800]}
    p = r.payload
    if isinstance(p, str):
        try: p = json.loads(p)
        except Exception: return {"ok": True, "response": p[:2000]}
    resp = p.get("response") if isinstance(p, dict) and "response" in p else p
    if isinstance(resp, str):
        try: resp = json.loads(resp)
        except Exception: pass
    st = p.get("status") if isinstance(p, dict) else None
    ok = not (isinstance(st, int) and st >= 400) and not (isinstance(resp, dict) and ("odata.error" in resp or "error" in resp and isinstance(resp.get("error"), dict)))
    return {"ok": ok, "status": st, "response": resp}

# ---- token resolvers
def list_id(title):
    k = "{{ListId:%s}}" % title
    if k not in tok:
        r = rest("GET", "_api/web/lists?$filter=Hidden eq false&$select=Id,Title")
        for L in (r.get("response") or {}).get("value", []):
            tok["{{ListId:%s}}" % L["Title"]] = L["Id"]
        save_tok()
    return tok.get(k)
def resolve(name):
    m = re.match(r"\{\{(\w+):(.+)\}\}$", name)
    if not m: return
    kind, rest_ = m.group(1), m.group(2)
    if kind == "ListId": list_id(rest_)
    elif kind == "ListIdB64":
        v = list_id(rest_)
        if v: tok[name] = base64.b64encode(v.encode()).decode()
    elif kind in ("ViewId", "ViewIdB64"):
        L, V = rest_.split("/", 1); lid = list_id(L)
        r = iq("get_views_of_list", {"siteKey": tok["{{SiteKey}}"], "listId": lid})
        for v in ((r.get("result") or {}).get("views") or []):
            tok["{{ViewId:%s/%s}}" % (L, v["title"])] = v["id"]
            tok["{{ViewIdB64:%s/%s}}" % (L, v["title"])] = base64.b64encode(v["id"].encode()).decode()
    elif kind == "QuickStepId":
        L, T = rest_.split("/", 1); lid = list_id(L)
        r = iq("get_quicksteps", {"siteKey": tok["{{SiteKey}}"], "listId": lid})
        res = r.get("result") or {}
        for q in (res.get("quicksteps") or []):
            tok["{{QuickStepId:%s/%s}}" % (L, q["Title"])] = q.get("RuleTemplateId") or q.get("ID")
    elif kind == "FieldId":
        L, F = rest_.split("/", 1); lid = list_id(L)
        r = rest("GET", "_api/web/lists(guid'%s')/fields?$select=Id,InternalName" % lid)
        for f in (r.get("response") or {}).get("value", []):
            tok["{{FieldId:%s/%s}}" % (L, f["InternalName"])] = f["Id"]
    elif kind == "ItemId":
        L, F = rest_.split("/", 1); lid = list_id(L)
        r = iq("list_items", {"siteKey": tok["{{SiteKey}}"], "listId": lid, "rowLimit": 500})
        items = (((r.get("result") or {}).get("data") or {}).get("items")) or []
        for it in items:
            if it.get("FileLeafRef"):
                tok["{{ItemId:%s/%s}}" % (L, it["FileLeafRef"])] = int(it["ID"])
    elif kind == "GroupId":
        r = rest("GET", "_api/web?$select=AssociatedOwnerGroup/Id,AssociatedMemberGroup/Id,AssociatedVisitorGroup/Id&$expand=AssociatedOwnerGroup,AssociatedMemberGroup,AssociatedVisitorGroup")
        w = r.get("response") or {}
        tok["{{GroupId:Owners}}"] = w["AssociatedOwnerGroup"]["Id"]
        tok["{{GroupId:Content Team}}"] = w["AssociatedMemberGroup"]["Id"]
        tok["{{GroupId:Sellers}}"] = w["AssociatedVisitorGroup"]["Id"]
    save_tok()

def fill(text):
    text = R.render(text, tok)
    left = [t for t in set(TOKEN.findall(text)) if not t.startswith(("{{seed:", "{{file:"))]
    if left:
        for t in left:
            if t not in tok: resolve(t)
        text = R.render(text, tok)
    return text
def fill_obj(o):
    if isinstance(o, str): return fill(o)
    if isinstance(o, list): return [fill_obj(x) for x in o]
    if isinstance(o, dict): return {k: fill_obj(v) for k, v in o.items()}
    return o
def unresolved(o):
    return sorted(set(TOKEN.findall(json.dumps(o, ensure_ascii=False))))

def render_out():
    # write deploy/out with what is known now (pages, views, form, seed)
    jobs = [("site/pages/" + p["file"], "pages/" + p["file"], True) for p in json.load(open(os.path.join(PKG, "site", "site.json"), encoding="utf-8"))["pages"]]
    jobs += [("site/views/decks-start-here.formatter.txt", "views/decks-start-here.formatter.txt", False),
             ("site/views/decks-start-here.html", "views/decks-start-here.html", True),
             ("site/views/deck-templates-pick-a-template.tiles.json", "views/deck-templates-pick-a-template.tiles.json", False),
             ("site/forms/content-requests.request-content.json", "forms/content-requests.request-content.json", False)]
    for src, dst, bom in jobs:
        text = open(os.path.join(PKG, src), encoding="utf-8-sig").read()
        p = os.path.join(OUT, dst); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n").write(fill(text))
def out_path(pkg_rel):
    rel = pkg_rel[len("site/"):] if pkg_rel.startswith("site/") else pkg_rel
    p = os.path.join(OUT, rel)
    return p if os.path.exists(p) else os.path.join(PKG, pkg_rel)
def seed_items(name):
    seed = json.loads(open(os.path.join(PKG, "content", "seed.json"), encoding="utf-8").read())
    rows = seed[name]
    items = []
    for r in rows:
        r = dict(r); f = r.pop("file", None)
        r = json.loads(fill(json.dumps(r, ensure_ascii=False)))
        names = list(r); vals = [R.person(v) if k == "ContentOwner" else R.iq_value(v) for k, v in r.items()]
        if f:
            key = "{{ItemId:%s/%s}}" % (name, f)
            if key not in tok: resolve(key)
            items.append({"itemId": tok.get(key, key), "fieldInternalNames": names, "newValues": vals})
        else:
            items.append({"fieldInternalNames": names, "values": vals})
    return items

def brief(r):
    if not isinstance(r, dict): return str(r)[:600]
    b = {k: r.get(k) for k in ("ok", "isError", "success", "error", "status", "correlationId", "missingRequired", "needsConfirmation", "reason") if k in r}
    res = r.get("result", r.get("response"))
    b["result"] = json.dumps(res, ensure_ascii=False)[:900] if res is not None else None
    return b

def run_step(s):
    via = s["via"]
    if via == "manual":
        return {"ok": True, "skipped": "manual"}
    if via == "rest":
        q = s["rest"]; uri = fill(q["uri"]); body = q.get("body")
        if s["id"] == "11.02":
            r = rest("GET", uri)
            done = []
            for n in (r.get("response") or {}).get("value", []):
                d = rest("POST", "_api/web/navigation/GetNodeById(%d)" % n["Id"], None, {"X-HTTP-Method": "DELETE", "IF-MATCH": "*"})
                done.append({"node": n["Title"], "ok": d.get("ok")})
            return {"ok": all(x["ok"] for x in done), "response": done}
        if body is not None:
            body = json.loads(fill(json.dumps(body, ensure_ascii=False)))
            if "{{file:" in json.dumps(body): render_out()
            for k, v in list(body.items()):
                if isinstance(v, str) and "{{file:" in v:
                    m = re.search(r"\{\{file:([^}]+)\}\}", v)
                    body[k] = v.replace(m.group(0), open(out_path(m.group(1)), encoding="utf-8-sig").read())
        left = unresolved([uri, body])
        if left: return {"ok": False, "error": "unresolved tokens: %s" % left}
        r = rest(q["method"], uri, body, q.get("headers"))
        if r.get("ok") and s.get("produces"):
            for p in s["produces"]:
                if p.startswith("{{NavId:"):
                    tok[p] = (r.get("response") or {}).get("Id"); save_tok()
        if r.get("ok") and s["id"] == "02.14":
            for L in (r.get("response") or {}).get("value", []):
                tok["{{ListId:%s}}" % L["Title"]] = L["Id"]
            save_tok()
        return r
    # iq
    a = dict(s.get("arguments") or {})
    argFiles = {}
    if "fromFile" in a:
        f = a.pop("fromFile"); render_out()
        a = dict(json.load(open(out_path(f), encoding="utf-8-sig")), **a)
    if s.get("contentFrom"):
        src = s["contentFrom"]
        if s.get("render"):
            render_out(); argFiles["content"] = out_path(src)
        elif s.get("encode") == "base64":
            p = os.path.join(ST, "b64", src.replace("/", "__") + ".b64")
            open(p, "w").write(base64.b64encode(open(os.path.join(PKG, src), "rb").read()).decode())
            argFiles["content"] = p
        else:
            argFiles["content"] = os.path.join(PKG, src)
    for k, f in (s.get("argFiles") or {}).items():
        render_out(); argFiles[k] = out_path(f)
    for k, v in list(a.items()):
        if isinstance(v, str) and v.startswith("{{seed:"):
            a[k] = seed_items(v[7:-2])
    a = fill_obj(a)
    if a.get("siteKey") is None and "{{SiteKey}}" in tok: a["siteKey"] = tok["{{SiteKey}}"]
    left = unresolved(a)
    for k, f in argFiles.items():
        left += unresolved(open(f, encoding="utf-8-sig").read()[:200000]) if not f.endswith(".b64") else []
    if left: return {"ok": False, "error": "unresolved tokens: %s" % sorted(set(left))}
    r = iq(s["tool"], a, argFiles or None)
    res = r.get("result") if isinstance(r.get("result"), dict) else {}
    if r.get("ok") and res.get("success") is False:
        r["ok"] = False
    if r.get("ok") and s["tool"] == "create_form":
        m = re.search(r"formId=([0-9a-fA-F-]{36})", res.get("formEditUrl") or "")
        for pr in s.get("produces") or []:
            if m and pr.startswith("{{ViewId:"):
                tok[pr] = m.group(1); tok[pr.replace("{{ViewId:", "{{ViewIdB64:")] = base64.b64encode(m.group(1).encode()).decode(); save_tok()
    if r.get("ok") and s["tool"] == "create_or_update_quick_step" and res.get("quickStepId"):
        for pr in s.get("produces") or []:
            tok[pr] = res["quickStepId"]; save_tok()
    if r.get("ok") and s["tool"] == "get_site_key":
        tok["{{SiteKey}}"] = res["siteKey"]; save_tok()
    return r

sel_ph = set(A.get("phases") or []); sel_id = set(A.get("ids") or []); skip = set(A.get("skip") or [])
todo = [s for s in steps if (s["phase"] in sel_ph or s["id"] in sel_id) and s["id"] not in skip]
results = []
for s in todo:
    t0 = datetime.datetime.now()
    if A.get("dry"):
        results.append({"id": s["id"], "title": s["title"], "via": s["via"]}); continue
    try:
        r = run_step(s)
    except Exception as e:
        r = {"ok": False, "error": "%s\n%s" % (repr(e), traceback.format_exc()[-1200:])}
    b = brief(r)
    rec = {"id": s["id"], "title": s["title"], "via": s["via"], "tool": s.get("tool"), "secs": round((datetime.datetime.now() - t0).total_seconds(), 1), "ok": bool(r.get("ok")), "brief": b}
    open(LOGF, "a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False) + "\n")
    log("%s %s -> %s" % (s["id"], s["title"][:50], r.get("ok")))
    results.append(rec)
    if not r.get("ok") and not A.get("continueOnError"):
        break
set_result({"ran": len(results), "ok": sum(1 for x in results if x.get("ok")), "failed": [x for x in results if not x.get("ok")][:3],
            "last": results[-1]["id"] if results else None, "tokens": len(tok)})
