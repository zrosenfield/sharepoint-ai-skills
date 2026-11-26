#!/usr/bin/env python3
"""S-05 / S-06 / S-11 / S-22 data invariants for the Obligations list.

Input: Obligations items as JSON: a list of items, or {"value"|"items"|"rows": [...]}, or list_items
tool output; Graph-style {"fields": {...}} items are flattened. Use internal names (Title, Status,
DueDate ...). --map SRC=DST renames a field first (for example --map NewRisk=Risk).

Errors (exit 1):
  INV-01 open item without Timing          INV-02 Timing contradicts Status (open vs Closed)
  INV-04 DueDate empty <=> TriggerType Event-driven or Ongoing
  INV-05 Recurrence <> None <=> TriggerType Recurring
  INV-07 "Superseded by" items not Not applicable/Closed, or the same note twice
  INV-08 IsSample wrong for sample contracts (--sample-manifest or --all-sample)
  INV-09 duplicate CaptureKey, or more than one open item in one recurring series
  INV-10 held item (Needs review) without a reason in Notes; Low confidence not held
  INV-11 choice value outside the schema          INV-12 captured item missing Title/Contract/Clause/Source clause
  INV-13 Fulfilled without FulfilledOn             INV-15 unparseable date
  RISK   share of open items with Risk High outside --risk-range (default 0.15-0.30)
Warnings (exit 0 unless --strict): INV-03 Timing stale for --today (error with --timing-strict), INV-06
Event-driven without TriggerEvent, INV-14 Not applicable without an explanation, title > 80 characters or
a non-ISO date in a title, successor key date <> DueDate, mixed IsSample representations.

Sample run:
  python3 check_invariants.py obligations.json --today 2026-11-24 --sample-manifest ../../sample-data/contracts-manifest.json
  -> one line per check (PASS/FAIL/WARN with counts and up to --examples examples), then "INVARIANTS: PASS"; exit 0/1.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLOSED = {"Fulfilled", "Waived", "Not applicable"}
UNDATED = {"Event-driven", "Ongoing"}
CHOICE_FIELDS = ["Party", "Category", "TriggerType", "Recurrence", "Status", "Timing", "ReviewState", "Confidence", "Risk", "BusinessUnit"]
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")
MONTH_DATE = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b")


def load_items(path, maps, utc_offset):
    data = json.load(open(path, encoding="utf-8"))

    def find(obj):
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for k in ("value", "items", "rows", "Items"):
                if isinstance(obj.get(k), list):
                    return obj[k]
            for k in ("result", "results", "content", "data"):
                if k in obj:
                    r = find(obj[k])
                    if r is not None:
                        return r
        return None

    items = find(data)
    if items is None:
        raise SystemExit(f"{path}: no list of items found")
    out = []
    for it in items:
        if isinstance(it, dict) and isinstance(it.get("fields"), dict):
            it = {**{k: v for k, v in it.items() if k != "fields"}, **it["fields"]}
        it = dict(it)
        for src, dst in maps:
            if src in it:
                it[dst] = it[src]
        for k in ("DueDate", "FulfilledOn", "LastReminded"):
            it[k] = to_date(it.get(k), utc_offset, k)
        out.append(it)
    return out


def to_date(v, utc_offset, field="date"):
    if v in (None, ""):
        return None
    if isinstance(v, str) and ISO.match(v):
        if len(v) > 10 and "T" in v:
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None) + timedelta(hours=utc_offset)
                return dt.date().isoformat()
            except ValueError:
                pass
        return v[:10]
    if isinstance(v, str):
        for fmt in ("%m/%d/%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(v, fmt).date().isoformat()
            except ValueError:
                pass
    return {"__bad__": v, "field": field}


def truthy(v):
    if isinstance(v, bool):
        return v
    if v is None or v == "":
        return None
    s = str(v).strip().lower()
    if s in ("yes", "true", "1"):
        return True
    if s in ("no", "false", "0"):
        return False
    return None


def text(v):
    if v is None:
        return ""
    if isinstance(v, dict):
        return str(v.get("Url") or v.get("url") or v.get("title") or v.get("Title") or v.get("LookupValue") or "")
    if isinstance(v, list):
        return ", ".join(text(x) for x in v)
    return str(v)


def load_choices(spec_path):
    try:
        spec = json.load(open(spec_path, encoding="utf-8"))
    except FileNotFoundError:
        return {}
    lists = spec["lists"] if isinstance(spec, dict) else []
    for lst in lists:
        if lst["title"] == "Obligations":
            return {f["internalName"]: f["choices"] for f in lst["fields"] if f.get("choices")}
    return {}


def timing_for(it, today, due_soon):
    if it.get("Status") in CLOSED:
        return "Closed"
    d = it.get("DueDate")
    if not isinstance(d, str):
        return "No date"
    if d < today:
        return "Overdue"
    if d <= (date.fromisoformat(today) + timedelta(days=due_soon)).isoformat():
        return "Due soon"
    return "Upcoming"


def label(it):
    return f"{(it.get('ContractName') or '?')[:2]} {it.get('ClauseRef') or '-'} '{(it.get('Title') or '')[:50]}'" + (f" #{it['ID']}" if it.get("ID") else "")


def run(items, a, choices, sample_files):
    res = []  # (id, severity, description, violations)

    def chk(cid, sev, desc, viol):
        res.append((cid, sev, desc, viol))

    is_open = lambda it: (it.get("Status") or "Not started") not in CLOSED  # noqa: E731
    opens = [it for it in items if is_open(it)]

    chk("INV-01", "error", "every open item has Timing", [label(it) for it in opens if not it.get("Timing")])
    chk("INV-02", "error", "Timing agrees with Status (Closed iff Fulfilled/Waived/Not applicable)",
        [f"{label(it)}: Status {it.get('Status')}, Timing {it.get('Timing')}" for it in items if it.get("Timing") and
         ((it.get("Status") in CLOSED) != (it.get("Timing") == "Closed"))])
    if a.today:
        stale = [f"{label(it)}: Timing {it.get('Timing')}, expected {timing_for(it, a.today, a.due_soon_days)}"
                 for it in items if it.get("Timing") and it.get("Timing") != timing_for(it, a.today, a.due_soon_days)]
        chk("INV-03", "error" if a.timing_strict else "warn", f"Timing current for {a.today} (dueSoonDays {a.due_soon_days})", stale)
    chk("INV-04", "error", "DueDate empty <=> TriggerType Event-driven or Ongoing",
        [f"{label(it)}: {it.get('TriggerType')} with DueDate {it.get('DueDate')}" for it in items
         if (it.get("TriggerType") in UNDATED) == bool(it.get("DueDate")) and it.get("TriggerType")])
    chk("INV-05", "error", "Recurrence <> None <=> TriggerType Recurring",
        [f"{label(it)}: {it.get('TriggerType')} / {it.get('Recurrence')}" for it in items if it.get("TriggerType") and
         ((it.get("TriggerType") == "Recurring") != ((it.get("Recurrence") or "None") != "None"))])
    chk("INV-06", "warn", "open Event-driven items name their TriggerEvent",
        [label(it) for it in opens if it.get("TriggerType") == "Event-driven" and not it.get("TriggerEvent")])
    sup = []
    for it in items:
        notes = text(it.get("Notes"))
        hits = re.findall(r"Superseded by [^;\n]+?(?=;|\n|\.\s|\.?$)", notes)
        if not hits:
            continue
        if len(hits) != len(set(hits)):
            sup.append(f"{label(it)}: duplicate note '{hits[0]}'")
        if it.get("Status") not in CLOSED:
            sup.append(f"{label(it)}: superseded but Status {it.get('Status')}")
        elif it.get("Status") == "Not applicable" and it.get("Timing") not in (None, "", "Closed"):
            sup.append(f"{label(it)}: superseded, Timing {it.get('Timing')}")
    chk("INV-07", "error", "superseded items are Not applicable + Closed, note once", sup)
    reps = Counter(type(it.get("IsSample")).__name__ for it in items)
    if sample_files is not None or a.all_sample:
        bad = []
        for it in items:
            want = True if a.all_sample else (it.get("ContractName") in sample_files)
            got = truthy(it.get("IsSample"))
            if got is not want:
                bad.append(f"{label(it)}: IsSample {it.get('IsSample')!r}, expected {'Yes' if want else 'No'}")
        chk("INV-08", "error", "IsSample = Yes exactly for items of sample contracts", bad)
    if len(reps) > 1:
        chk("INV-08b", "warn", "one IsSample representation", [f"mixed types: {dict(reps)}"])
    keys = Counter(it.get("CaptureKey") for it in items if it.get("CaptureKey"))
    series = defaultdict(list)
    for it in opens:
        if it.get("CaptureKey"):
            series[it["CaptureKey"].split("#")[0]].append(it)
    chk("INV-09", "error", "CaptureKey unique; at most one open item per series",
        [f"duplicate key {k} x{n}" for k, n in keys.items() if n > 1] +
        [f"series {k}: {len(v)} open items ({', '.join(str(x.get('DueDate')) for x in v)})" for k, v in series.items() if len(v) > 1])
    fmt = []
    for it in items:
        k = it.get("CaptureKey")
        if not k:
            continue
        parts = k.split("|")
        if len(parts) != 3 or parts[0] != it.get("ContractName"):
            fmt.append(f"{label(it)}: key '{k}' is not <ContractName>|<ClauseRef>|<slug>")
        elif "#" in parts[2] and parts[2].split("#", 1)[1] != (it.get("DueDate") or ""):
            fmt.append(f"{label(it)}: successor key date {parts[2].split('#', 1)[1]} <> DueDate {it.get('DueDate')}")
    chk("INV-09b", "warn", "CaptureKey format <file>|<clause>|<slug>[#<due date>]", fmt)
    chk("INV-10", "error", "held items carry a reason; Low confidence is held",
        [f"{label(it)}: Needs review with empty Notes" for it in opens if it.get("ReviewState") == "Needs review" and not text(it.get("Notes")).strip()] +
        [f"{label(it)}: Confidence Low but {it.get('ReviewState')}" for it in opens if it.get("Confidence") == "Low" and it.get("ReviewState") != "Needs review"])
    bad_choice = []
    for it in items:
        for f in CHOICE_FIELDS:
            v = it.get(f)
            if v not in (None, "") and f in choices and v not in choices[f]:
                bad_choice.append(f"{label(it)}: {f} = {v!r}")
        for f in ("Party", "Category", "TriggerType", "Status"):
            if it.get("CaptureKey") and not it.get(f):
                bad_choice.append(f"{label(it)}: {f} empty")
    chk("INV-11", "error", "choice values are valid schema choices", bad_choice)
    chk("INV-12", "error", "captured items have Title, ContractName, Counterparty, ClauseRef, SourceClause",
        [f"{label(it)}: missing {', '.join(f for f in ('Title', 'ContractName', 'Counterparty', 'ClauseRef', 'SourceClause') if not text(it.get(f)).strip())}"
         for it in items if it.get("CaptureKey") and not all(text(it.get(f)).strip() for f in ('Title', 'ContractName', 'Counterparty', 'ClauseRef', 'SourceClause'))])
    chk("INV-12b", "warn", "titles <= 80 characters with ISO dates",
        [f"{label(it)}: {len(it.get('Title') or '')} chars" for it in items if len(it.get("Title") or "") > 80] +
        [f"{label(it)}: date '{MONTH_DATE.search(it['Title']).group(0)}' in title" for it in items if MONTH_DATE.search(it.get("Title") or "")])
    chk("INV-13", "error", "Fulfilled items have FulfilledOn",
        [label(it) for it in items if it.get("Status") == "Fulfilled" and not it.get("FulfilledOn")])
    chk("INV-14", "warn", "Not applicable items explain why in Notes",
        [label(it) for it in items if it.get("Status") == "Not applicable" and not text(it.get("Notes")).strip()])
    chk("INV-15", "error", "dates parse as YYYY-MM-DD",
        [f"{label(it)}: {k} {it[k]['__bad__']!r}" for it in items for k in ("DueDate", "FulfilledOn", "LastReminded") if isinstance(it.get(k), dict)])
    if a.risk_range.lower() != "off":
        lo, hi = (float(x) for x in a.risk_range.split("-"))
        n = len(opens)
        high = sum(1 for it in opens if it.get("Risk") == "High")
        share = high / n if n else 0.0
        dist = Counter(it.get("Risk") or "(empty)" for it in opens)
        msg = [] if lo <= share <= hi else [f"High {high}/{n} = {share:.0%} outside {lo:.0%}-{hi:.0%}"]
        chk("RISK", "error", f"High risk share of open items {high}/{n} = {share:.0%} (target {lo:.0%}-{hi:.0%}); {dict(dist)}", msg)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Data invariants for Obligations items (S-05, S-06, S-11, S-22).")
    ap.add_argument("items", help="Obligations items JSON")
    ap.add_argument("--today", help="YYYY-MM-DD; enables the Timing currency check INV-03")
    ap.add_argument("--due-soon-days", type=int, default=14)
    ap.add_argument("--timing-strict", action="store_true", help="stale Timing is an error (use right after a sweep run)")
    ap.add_argument("--sample-manifest", help="contracts-manifest.json: items of these files must be IsSample = Yes, others No")
    ap.add_argument("--all-sample", action="store_true", help="every item must be IsSample = Yes")
    ap.add_argument("--map", action="append", default=[], metavar="SRC=DST", help="copy field SRC into DST first (e.g. NewRisk=Risk)")
    ap.add_argument("--risk-range", default="0.15-0.30", help="allowed High share of open items, or 'off' (default 0.15-0.30)")
    ap.add_argument("--spec", default=str(HERE / "schema-spec.json"), help="schema spec for choice values")
    ap.add_argument("--utc-offset", type=float, default=-8, help="hours added to UTC timestamps before taking the date (default -8, Pacific)")
    ap.add_argument("--examples", type=int, default=5, help="violations to print per check")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    maps = [tuple(m.split("=", 1)) for m in a.map]
    items = load_items(a.items, maps, a.utc_offset)
    sample_files = None
    if a.sample_manifest:
        sample_files = {c.get("fileName") for c in json.load(open(a.sample_manifest, encoding="utf-8"))}
    res = run(items, a, load_choices(a.spec), sample_files)
    failed = 0
    print(f"{len(items)} items ({sum(1 for i in items if (i.get('Status') or 'Not started') not in CLOSED)} open)")
    for cid, sev, desc, viol in res:
        st = "PASS" if not viol else ("FAIL" if sev == "error" or a.strict else "WARN")
        failed += st == "FAIL"
        print(f"{st:<5} {cid:<8} {desc}" + (f"  [{len(viol)}]" if viol else ""))
        for v in viol[:a.examples]:
            print(f"        - {v}")
        if len(viol) > a.examples:
            print(f"        - ... {len(viol) - a.examples} more")
    print(f"\nINVARIANTS: {'PASS' if not failed else 'FAIL'} ({failed} failing check(s))")
    if a.json_out:
        json.dump({"pass": not failed, "items": len(items), "checks": [
            {"id": c, "severity": s, "description": d, "violations": v} for c, s, d, v in res]},
            open(a.json_out, "w", encoding="utf-8"), indent=1)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
