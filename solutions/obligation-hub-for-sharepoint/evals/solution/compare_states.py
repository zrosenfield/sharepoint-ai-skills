#!/usr/bin/env python3
"""S-10 / S-12 / S-20 / S-21 state comparison: are two Obligations snapshots the same?

Uses:
  order independence (S-10)   capture 01 then 02 (A) against 02 then 01, or both at once (B)
  re-capture idempotency (S-12), capture skip (S-20)   before (A) and after (B) the run
  sweep idempotency (S-21)    after the first and after the second sweep of the day, with
                              --fields Timing,LastReminded,Status,DueDate,Notes
Items are keyed by CaptureKey (items without one by "(manual) <Title>"). Run-specific values (IDs,
Modified, RunAt) are not compared. A port of the kit's scoring/compare_states.py; additions: duplicate
CaptureKeys within one file count as differences (the old version silently kept the last), --fields,
--add-fields, --map and --json-out.

Sample run:
  python3 compare_states.py order-01-02.json order-02-01.json --prefix 01 --prefix 02
  -> "Compared 12 common items; 0 difference(s)." then IDENTICAL; exit 0 = identical, 1 = differences.
"""
import argparse
import json
import re
import sys
from collections import Counter

FIELDS = ["Title", "ClauseRef", "Party", "Category", "TriggerType", "Recurrence", "DueDate",
          "TriggerEvent", "Status", "ReviewState", "Confidence", "BusinessUnit"]


def load(path, prefixes, fields, maps):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict):
        for k in ("value", "items", "rows"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    items, dupes, counts = {}, [], Counter()
    for c in data:
        if isinstance(c.get("fields"), dict):
            c = {**c, **c["fields"]}
        c = dict(c)
        for src, dst in maps:
            if src in c:
                c[dst] = c[src]
        if prefixes and not any((c.get("ContractName") or "").startswith(p) for p in prefixes):
            continue
        key = c.get("CaptureKey") or f"(manual) {c.get('Title')}"
        counts[key] += 1
        notes = c.get("Notes") or ""
        sup = sorted(re.findall(r"Superseded by .+?(?=;|\n|\.\s|\.?$)", notes))  # duplicates count
        row = {}
        for f in fields:
            v = c.get(f)
            if f in ("DueDate", "FulfilledOn", "LastReminded") and isinstance(v, str):
                v = v[:10]
            row[f] = v
        row["Superseded notes"] = sup
        items[key] = row
    dupes = [f"{k} x{n}" for k, n in counts.items() if n > 1]
    return items, dupes


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare two Obligations snapshots by CaptureKey (exit 0 identical, 1 different).")
    ap.add_argument("a", help="snapshot A (JSON list of Obligations items)")
    ap.add_argument("b", help="snapshot B")
    ap.add_argument("--prefix", action="append", default=[], help="only items whose ContractName starts with this (repeatable)")
    ap.add_argument("--fields", help="comma-separated fields to compare instead of the capture fields")
    ap.add_argument("--add-fields", help="comma-separated fields to compare in addition")
    ap.add_argument("--map", action="append", default=[], metavar="SRC=DST")
    ap.add_argument("--json-out")
    # backwards compatible with: compare_states.py A B 01 02
    ap.add_argument("legacy_prefixes", nargs="*", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    fields = [f.strip() for f in a.fields.split(",")] if a.fields else list(FIELDS)
    if a.add_fields:
        fields += [f.strip() for f in a.add_fields.split(",") if f.strip() not in fields]
    prefixes = a.prefix + a.legacy_prefixes
    maps = [tuple(m.split("=", 1)) for m in a.map]
    A, dA = load(a.a, prefixes, fields, maps)
    B, dB = load(a.b, prefixes, fields, maps)
    diffs = [f"duplicate key in A: {d}" for d in dA] + [f"duplicate key in B: {d}" for d in dB]
    diffs += [f"only in A: {k}" for k in sorted(A.keys() - B.keys())] + [f"only in B: {k}" for k in sorted(B.keys() - A.keys())]
    for k in sorted(A.keys() & B.keys()):
        for f, v in A[k].items():
            if v != B[k][f]:
                diffs.append(f"{k}: {f} {v!r} vs {B[k][f]!r}")
    print(f"Compared {len(A.keys() & B.keys())} common items on {len(fields)} fields + superseded notes; {len(diffs)} difference(s).")
    print("\n".join("  " + d for d in diffs) or "IDENTICAL")
    if a.json_out:
        json.dump({"identical": not diffs, "common": len(A.keys() & B.keys()), "differences": diffs},
                  open(a.json_out, "w", encoding="utf-8"), indent=1)
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
