#!/usr/bin/env python3
"""S-01 Schema conformance: compare a site's list schemas and views with the Obligation Hub spec.

Input: one or more JSON dumps of the SharePoint tools get_list_schema (fields; optionally includeViews,
includeSchemaXml or a viewDefinition) and get_views_of_list, one file per call or combined. Any nesting
works: the script walks the JSON and finds list schemas (an object with "title" and a "fields" list),
view lists (an object with a "views" list, matched to its list by "listId") and view definitions
("viewDefinition"). REST shapes (InternalName, TypeAsString, Choices, SchemaXml) are accepted too.

Spec: schema-spec.json next to this script (default), or the kit's deploy lists.json (create_or_update_list
arguments), detected automatically.

Checks per list: exists, template; per column: internal name exists, type, choices (all spec choices
present), default, DateOnly format, display name (warning only); per view: exists, default view, view
columns, CAML filter terms, sort and group-by, calendar type; and that a leftover "All Items" view is not
the default (platform gotcha 10). Choices, formats and CAML can only be checked when the dump carries
them; otherwise the row is UNVERIFIED (a failure with --strict).

Sample run:
  python3 check_schema.py --dump dumps/ --json-out schema-result.json
  -> table of PASS/FAIL/WARN/UNVERIFIED rows, then "SCHEMA: PASS (n checks, 0 failed)"; exit 0 on pass, 1 on any FAIL.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TYPE_KIND = {2: "Text", 3: "Note", 4: "DateTime", 6: "Choice", 8: "Boolean", 9: "Number", 10: "Currency",
             11: "URL", 20: "User"}
TYPE_ALIAS = {"text": "Text", "note": "Note", "choice": "Choice", "datetime": "DateTime", "user": "User",
              "boolean": "Boolean", "number": "Number", "currency": "Currency", "url": "URL"}
OPS = "Eq|Neq|IsNull|IsNotNull|Lt|Leq|Gt|Geq|Contains|BeginsWith"


def norm_id(s):
    return str(s or "").strip().strip("{}").lower()


def g(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    return default


# ---------------------------------------------------------------- spec
def load_spec(path):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict) and "lists" in data:
        return data["lists"]
    if isinstance(data, list) and data and "args" in data[0]:  # deploy lists.json
        lists = []
        for entry in data:
            a = entry["args"]
            lst = {"title": a["listName"], "template": a["templateType"], "fields": [], "views": []}
            for raw in a.get("columns", []):
                c = json.loads(raw) if isinstance(raw, str) else raw
                f = {"internalName": c["internalName"], "displayName": c.get("displayName"), "type": c["type"]}
                m = re.search(r'DisplayName="([^"]+)"', c.get("editSchemaXml", ""))
                if m:
                    f["displayName"] = m.group(1)
                for src, dst in (("format", "format"), ("choices", "choices")):
                    if c.get(src):
                        f[dst] = c[src]
                dv = (c.get("defaultValueFields") or {}).get("defaultValue")
                if dv is not None:
                    f["default"] = dv
                lst["fields"].append(f)
            for raw in a.get("views", []):
                v = json.loads(raw) if isinstance(raw, str) else raw
                lst["views"].append({"title": v["name"], "default": bool(v.get("isDefaultView")),
                                     "fields": v.get("viewFields", []), "query": v.get("query"),
                                     "viewType2": v.get("viewType2")})
            lists.append(lst)
        return lists
    raise SystemExit(f"{path}: not a schema spec (expected {{'lists': [...]}} or a deploy lists.json)")


# ---------------------------------------------------------------- dump discovery
class Found:
    def __init__(self):
        self.lists = {}        # norm id or title -> {"title", "id", "baseType", "baseTemplate", "fields": {}, "views": {}}
        self.orphan_views = []  # (file, views, listId)
        self.orphan_defs = []


def field_info(f):
    t = g(f, "fieldType", "TypeAsString", "type", "FieldTypeKind")
    if isinstance(t, int):
        t = TYPE_KIND.get(t, str(t))
    t = TYPE_ALIAS.get(str(t).lower(), str(t)) if t is not None else None
    choices = g(f, "choices", "Choices")
    if isinstance(choices, dict):
        choices = choices.get("results")
    xml = g(f, "schemaXml", "SchemaXml", default="") or ""
    if choices is None and "<CHOICE>" in xml:
        choices = re.findall(r"<CHOICE>(.*?)</CHOICE>", xml)
    fmt = g(f, "displayFormat", "DisplayFormat", "dateTimeFormat", "format")
    if fmt is None:
        m = re.search(r'\bFormat="(\w+)"', xml)
        fmt = m.group(1) if m else None
    if fmt in (0, "0"):
        fmt = "DateOnly"
    elif fmt in (1, "1"):
        fmt = "DateTime"
    default = g(f, "defaultValue", "DefaultValue")
    if default in (None, "") and "<Default>" in xml:
        default = re.search(r"<Default>(.*?)</Default>", xml).group(1)
    return {"internalName": g(f, "internalName", "InternalName", "StaticName"), "displayName": g(f, "title", "Title", "displayName"),
            "type": t, "choices": choices, "format": fmt, "default": default}


def view_info(v):
    fields = g(v, "viewfields", "viewFields", "ViewFields")
    if isinstance(fields, dict):
        fields = fields.get("Items") or fields.get("results")
    return {"title": g(v, "title", "Title", "name"), "isDefault": g(v, "isDefault", "DefaultView", "isDefaultView"),
            "fields": fields, "query": g(v, "viewQuery", "ViewQuery", "query"),
            "viewType2": g(v, "viewType2", "ViewType2"), "isHidden": g(v, "isHidden", "Hidden")}


def merge_view(store, v):
    cur = store.setdefault(v["title"], {})
    for k, val in v.items():
        if val is not None:
            cur[k] = val


def discover(paths):
    found = Found()
    files = []
    for p in paths:
        p = Path(p)
        files += sorted(p.rglob("*.json")) if p.is_dir() else [p]
    if not files:
        raise SystemExit("no dump files found")

    def get_list(schema):
        key = norm_id(g(schema, "id", "Id")) or str(g(schema, "title", "Title")).lower()
        lst = found.lists.setdefault(key, {"title": g(schema, "title", "Title"), "id": norm_id(g(schema, "id", "Id")),
                                           "fields": {}, "views": {}})
        for k in ("baseType", "baseTemplate", "BaseType", "BaseTemplate"):
            if schema.get(k) is not None:
                lst[k[0].lower() + k[1:]] = schema[k]
        return lst

    def walk(obj, fname, ctx_list):
        if isinstance(obj, list):
            for x in obj:
                walk(x, fname, ctx_list)
            return
        if not isinstance(obj, dict):
            return
        here = ctx_list
        flds = obj.get("fields") if "fields" in obj else obj.get("Fields")
        if isinstance(flds, dict):
            flds = flds.get("results")
        if isinstance(flds, list) and g(obj, "title", "Title") and any(isinstance(f, dict) and g(f, "internalName", "InternalName") for f in flds):
            here = get_list(obj)
            for f in flds:
                if isinstance(f, dict) and g(f, "internalName", "InternalName"):
                    fi = field_info(f)
                    here["fields"][fi["internalName"]] = fi
        if isinstance(obj.get("schema"), dict) and g(obj["schema"], "title", "Title"):
            here = get_list(obj["schema"])
        views = obj.get("views")
        if isinstance(views, list) and views and isinstance(views[0], dict) and g(views[0], "title", "Title"):
            target = None
            lid = norm_id(obj.get("listId"))
            if lid and lid in found.lists:
                target = found.lists[lid]
            elif here is not None and (not lid or lid == here.get("id")):
                target = here
            if target is None:
                found.orphan_views.append((fname, views, lid))
            else:
                for v in views:
                    merge_view(target["views"], view_info(v))
        vd = obj.get("viewDefinition")
        if isinstance(vd, dict):
            lid = norm_id(vd.get("listId") or obj.get("listId"))
            target = found.lists.get(lid) if lid else here
            if target is None:
                found.orphan_defs.append((fname, vd, lid))
            else:
                merge_view(target["views"], view_info(vd))
        for k, val in obj.items():
            if k in ("fields", "Fields", "views", "viewDefinition"):
                continue
            walk(val, fname, here)

    for f in files:
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"{f}: not valid JSON ({e})")
        walk(data, str(f), None)
    # second pass for views whose list schema appeared in a later file
    for fname, views, lid in found.orphan_views[:]:
        if lid in found.lists:
            for v in views:
                merge_view(found.lists[lid]["views"], view_info(v))
            found.orphan_views.remove((fname, views, lid))
    for fname, vd, lid in found.orphan_defs[:]:
        if lid in found.lists:
            merge_view(found.lists[lid]["views"], view_info(vd))
            found.orphan_defs.remove((fname, vd, lid))
    return found


# ---------------------------------------------------------------- checks
def caml_terms(q):
    q = (q or "").replace('"', "'")
    terms = set()
    for m in re.finditer(r"<(%s)>\s*<FieldRef Name='(\w+)'\s*/>(?:\s*<Value Type='(\w+)'>(.*?)</Value>)?" % OPS, q, re.S):
        op, field, vtype, val = m.groups()
        val = re.sub(r"\s+", "", val or "")
        terms.add((op, field, vtype or "", val))
    return terms


def caml_order(q, tag):
    m = re.search(r"<%s\b[^>]*>(.*?)</%s>" % (tag, tag), (q or "").replace('"', "'"), re.S)
    if not m:
        return []
    return [(n, (a or "TRUE").upper()) for n, a in re.findall(r"<FieldRef Name='(\w+)'(?:\s+Ascending='(\w+)')?\s*/>", m.group(1))]


def check(spec_lists, found, only=None):
    rows = []

    def add(lst, item, what, exp, got, status):
        rows.append({"list": lst, "item": item, "check": what, "expected": exp, "found": got, "status": status})

    by_title = {}
    for lst in found.lists.values():
        by_title.setdefault(str(lst["title"]).lower(), lst)
    for sl in spec_lists:
        name = sl["title"]
        if only and name.lower() not in only:
            continue
        dl = by_title.get(name.lower())
        if not dl:
            add(name, "-", "list exists", "present", "missing from dump", "FAIL")
            continue
        add(name, "-", "list exists", "present", "present", "PASS")
        base = dl.get("baseType")
        if base is not None:
            want = 1 if sl.get("template") == "DocumentLibrary" else 0
            add(name, "-", "template", sl.get("template"), f"baseType {base}", "PASS" if int(base) == want else "FAIL")
        for sf in sl["fields"]:
            iname = sf["internalName"]
            df = dl["fields"].get(iname)
            if not df:
                alt = [k for k in dl["fields"] if k.lower() == iname.lower() or (dl["fields"][k].get("displayName") or "").lower() == (sf.get("displayName") or "").lower()]
                add(name, iname, "column exists", iname, f"missing{' (similar: ' + ', '.join(alt) + ')' if alt else ''}", "FAIL")
                continue
            add(name, iname, "column exists", iname, iname, "PASS")
            if df["type"]:
                add(name, iname, "type", sf["type"], df["type"], "PASS" if df["type"] == sf["type"] else "FAIL")
            else:
                add(name, iname, "type", sf["type"], "not in dump", "UNVERIFIED")
            if sf.get("displayName") and df.get("displayName") and sf["displayName"] != df["displayName"]:
                add(name, iname, "display name", sf["displayName"], df["displayName"], "WARN")
            if sf.get("choices"):
                if df.get("choices") is None:
                    add(name, iname, "choices", ", ".join(sf["choices"]), "not in dump (use includeSchemaXml)", "UNVERIFIED")
                else:
                    missing = [c for c in sf["choices"] if c not in df["choices"]]
                    extra = [c for c in df["choices"] if c not in sf["choices"]]
                    if missing:
                        add(name, iname, "choices", ", ".join(sf["choices"]), "missing: " + ", ".join(missing), "FAIL")
                    elif extra:
                        add(name, iname, "choices", ", ".join(sf["choices"]), "extra: " + ", ".join(extra), "WARN")
                    else:
                        add(name, iname, "choices", f"{len(sf['choices'])} values", "match", "PASS")
            if sf.get("format"):
                if df.get("format") is None:
                    add(name, iname, "date format", sf["format"], "not in dump", "UNVERIFIED")
                else:
                    add(name, iname, "date format", sf["format"], df["format"], "PASS" if df["format"] == sf["format"] else "FAIL")
            if sf.get("default") not in (None, "") and df.get("default") not in (None, ""):
                exp, got = str(sf["default"]), str(df["default"])
                ok = exp == got or {exp.lower(), got.lower()} in ({"0", "false"}, {"1", "true"}, {"0", "no"}, {"1", "yes"})
                add(name, iname, "default", exp, got, "PASS" if ok else "WARN")
        dviews = dl["views"]
        if sl.get("views"):
            if not dviews:
                add(name, "-", "views", ", ".join(v["title"] for v in sl["views"]), "no views in dump (add get_views_of_list)", "UNVERIFIED")
                continue
            for sv in sl["views"]:
                dv = dviews.get(sv["title"])
                if not dv:
                    add(name, sv["title"], "view exists", "present", "missing", "FAIL")
                    continue
                add(name, sv["title"], "view exists", "present", "present", "PASS")
                if sv.get("default"):
                    add(name, sv["title"], "default view", "default", "default" if dv.get("isDefault") else "not default",
                        "PASS" if dv.get("isDefault") else "FAIL")
                if sv.get("fields") and dv.get("fields") is not None:
                    have = [f for f in dv["fields"]]
                    missing = [f for f in sv["fields"] if f not in have]
                    if missing:
                        add(name, sv["title"], "view columns", ", ".join(sv["fields"]), "missing: " + ", ".join(missing), "FAIL")
                    elif [f for f in have if f in sv["fields"]] != sv["fields"]:
                        add(name, sv["title"], "view columns", "spec order", "different order", "WARN")
                    else:
                        add(name, sv["title"], "view columns", f"{len(sv['fields'])} columns", "match", "PASS")
                if sv.get("query"):
                    if dv.get("query") is None:
                        add(name, sv["title"], "view query", "CAML", "not in dump (get_list_schema with viewId)", "UNVERIFIED")
                    else:
                        want, have = caml_terms(sv["query"]), caml_terms(dv["query"])
                        miss = want - have
                        add(name, sv["title"], "filter terms", f"{len(want)} terms", "missing: " + "; ".join(
                            f"{o} {f}{' ' + t + ':' + v if t else ''}" for o, f, t, v in sorted(miss)) if miss else "match",
                            "FAIL" if miss else "PASS")
                        for tag in ("OrderBy", "GroupBy"):
                            if caml_order(sv["query"], tag) != caml_order(dv["query"], tag):
                                add(name, sv["title"], tag, str(caml_order(sv["query"], tag)), str(caml_order(dv["query"], tag)), "WARN")
                if sv.get("viewType2"):
                    if dv.get("viewType2") is None:
                        add(name, sv["title"], "view type", sv["viewType2"], "not in dump", "UNVERIFIED")
                    else:
                        add(name, sv["title"], "view type", sv["viewType2"], dv["viewType2"],
                            "PASS" if str(dv["viewType2"]).upper() == sv["viewType2"].upper() else "FAIL")
            spec_names = {v["title"] for v in sl["views"]}
            for vt, dv in dviews.items():
                if vt == "All Items" and "All Items" not in spec_names:
                    add(name, vt, "leftover built-in view", "removed or not default",
                        "default" if dv.get("isDefault") else "present, not default", "FAIL" if dv.get("isDefault") else "WARN")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="S-01: compare SharePoint list schema/view dumps with the Obligation Hub spec.")
    ap.add_argument("--dump", action="append", required=True, help="dump file or folder of .json files (repeatable)")
    ap.add_argument("--spec", default=str(HERE / "schema-spec.json"), help="schema-spec.json (default) or deploy lists.json")
    ap.add_argument("--lists", help="comma-separated list titles to check (default: all in the spec)")
    ap.add_argument("--strict", action="store_true", help="treat UNVERIFIED rows as failures")
    ap.add_argument("--show", default="FAIL,WARN,UNVERIFIED", help="statuses to print in the table (default FAIL,WARN,UNVERIFIED; 'all')")
    ap.add_argument("--json-out", help="write all rows as JSON")
    a = ap.parse_args(argv)
    spec = load_spec(a.spec)
    found = discover(a.dump)
    only = {s.strip().lower() for s in a.lists.split(",")} if a.lists else None
    rows = check(spec, found, only)
    show = None if a.show.lower() == "all" else {s.strip().upper() for s in a.show.split(",")}
    w = [14, 22, 22, 34, 40]
    print(f"{'Result':<11}{'List':<{w[0]}}{'Item':<{w[1]}}{'Check':<{w[2]}}{'Expected':<{w[3]}}Found")
    for r in rows:
        if show is None or r["status"] in show:
            print(f"{r['status']:<11}{r['list'][:w[0]-1]:<{w[0]}}{str(r['item'])[:w[1]-1]:<{w[1]}}{r['check'][:w[2]-1]:<{w[2]}}"
                  f"{str(r['expected'])[:w[3]-1]:<{w[3]}}{str(r['found'])[:80]}")
    for fname, _views, lid in found.orphan_views:
        print(f"NOTE: views in {fname} (listId {lid or '?'}) matched no list schema; dump get_list_schema for that list too.")
    counts = {s: sum(r["status"] == s for r in rows) for s in ("PASS", "FAIL", "WARN", "UNVERIFIED")}
    failed = counts["FAIL"] + (counts["UNVERIFIED"] if a.strict else 0)
    print(f"\nSCHEMA: {'PASS' if not failed else 'FAIL'} ({len(rows)} checks: {counts['PASS']} pass, {counts['FAIL']} fail, "
          f"{counts['WARN']} warn, {counts['UNVERIFIED']} unverified{' (counted as failures: --strict)' if a.strict else ''})")
    if a.json_out:
        json.dump({"pass": not failed, "counts": counts, "rows": rows}, open(a.json_out, "w", encoding="utf-8"), indent=1)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
