#!/usr/bin/env python3
"""S-07 / S-08 / S-09 capture accuracy: score Obligations items against the sample answer key.

A port of the kit's scoring/score.py with the same matching (same contract file, and >= 60% word
overlap between SourceClause and the key's sourceClause, best match first), plus thresholds and an exit
code. Answer-key rows:
  track       must be captured as an open item (recall, precision, field accuracy)
  hold        must be an open item with ReviewState "Needs review" (Held correctly x/y; not in recall,
              precision or extras)
  exclude     must not be an open item           superseded  must not be an open item (it may exist as
              Not applicable with a "Superseded by" note)
Open = Status is not Not applicable (as in score.py; Fulfilled and Waived count as captured).

Gates (all must pass; defaults from evals/solution/EVALS.md):
  recall >= 0.90, precision >= 0.90, every field accuracy >= 0.90 (Party, Category, TriggerType,
  Recurrence, DueDate, Clause), trap handling 100% for trap types "amendment" and "routine-admin",
  held correctly >= 2/3.
Other trap types are reported (target 100%) but do not gate.

Sample run:
  python3 score_capture.py obligations.json --key ../../sample-data/answer-key.json
  -> "Recall 55/55 = 100%   Precision 55/55 = 100%" ... gate table ... "CAPTURE: PASS"; exit 0/1.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_KEY = HERE.parent.parent / "sample-data" / "answer-key.json"
FIELDS = ["Party", "Category", "TriggerType", "Recurrence", "DueDate", "Clause"]


def clause(s):
    return re.sub(r"[^0-9.]", "", (s or "").split("(")[0]).strip(".")


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def overlap(a, b):
    A, B = set(norm(a).split()), set(norm(b).split())
    return len(A & B) / max(1, min(len(A), len(B)))


def frac(s):
    return float(Fraction(s)) if "/" in str(s) else float(s)


def load_items(path, maps):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict):
        for k in ("value", "items", "rows"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    out = []
    for it in data:
        if isinstance(it.get("fields"), dict):
            it = {**it, **it["fields"]}
        it = dict(it)
        for src, dst in maps:
            if src in it:
                it[dst] = it[src]
        if isinstance(it.get("DueDate"), str):
            it["DueDate"] = it["DueDate"][:10] or None
        out.append(it)
    return out


def score(cap, key, only=None):
    if only:
        key = [k for k in key if any(k["contractFile"].startswith(p) for p in only)]
        cap = [c for c in cap if any((c.get("ContractName") or "").startswith(p) for p in only)]
    track = [k for k in key if k["expected"] == "track"]
    sup = [k for k in key if k["expected"] == "superseded"]
    exc = [k for k in key if k["expected"] == "exclude"]
    hold = [k for k in key if k["expected"] == "hold"]
    open_cap = [c for c in cap if c.get("Status") != "Not applicable"]
    used = set()

    def best(k, pool):
        cands = [(overlap(k["sourceClause"], c.get("SourceClause")), i) for i, c in enumerate(pool)
                 if c.get("ContractName") == k["contractFile"] and i not in used]
        cands = [x for x in cands if x[0] >= 0.6]
        return max(cands)[1] if cands else None

    hits, miss, fields, tot = [], [], Counter(), Counter()
    per_contract = defaultdict(lambda: {"track": 0, "hit": 0})
    for k in track:
        per_contract[k["contractFile"]]["track"] += 1
        i = best(k, open_cap)
        if i is None:
            miss.append(k)
            continue
        used.add(i)
        c = open_cap[i]
        hits.append((k, c))
        per_contract[k["contractFile"]]["hit"] += 1
        party = {"Northwind": "Us"}.get(k["party"], k["party"])
        checks = {"Party": c.get("Party") == party, "Category": c.get("Category") == k["category"],
                  "TriggerType": c.get("TriggerType") == k["triggerType"], "Recurrence": c.get("Recurrence") == k["recurrence"],
                  "DueDate": (c.get("DueDate") or None) == (k["nextDueDate"] or None), "Clause": clause(c.get("ClauseRef")) == clause(k["clauseRef"])}
        for f, ok in checks.items():
            tot[f] += 1
            fields[f] += ok
    held_ok, held_wrong, held_miss = [], [], []
    for k in hold:
        i = best(k, open_cap)
        if i is None:
            held_miss.append(k)
            continue
        used.add(i)
        c = open_cap[i]
        (held_ok if c.get("ReviewState") == "Needs review" else held_wrong).append((k, c))
    held_matched = len(held_ok) + len(held_wrong)
    extras = [c for i, c in enumerate(open_cap) if i not in used]
    for c in extras:
        per_contract[c.get("ContractName") or "?"].setdefault("extra", 0)
        per_contract[c.get("ContractName") or "?"]["extra"] += 1

    def is_open_match(k):
        return any(c.get("ContractName") == k["contractFile"] and overlap(k["sourceClause"], c.get("SourceClause")) >= 0.6 for c in open_cap)

    false_inc = [k for k in exc if is_open_match(k)]
    sup_ok = [k for k in sup if not is_open_match(k)]
    sup_noted = [k for k in sup if any(c.get("ContractName") == k["contractFile"] and c.get("Status") == "Not applicable"
                                       and "Superseded by" in (c.get("Notes") or "") and clause(c.get("ClauseRef")) == clause(k["clauseRef"]) for c in cap)]
    # trap handling per trap type
    hit_by_id = {id(k): c for k, c in hits}
    held_by_id = {id(k): c for k, c in held_ok}
    traps = defaultdict(lambda: [0, 0, []])
    for k in key:
        t = k.get("trapType")
        if not t:
            continue
        ok, why = False, ""
        if k["expected"] in ("exclude", "superseded"):
            ok = not is_open_match(k)
            why = "tracked as an open item"
        elif k["expected"] == "hold":
            ok = id(k) in held_by_id
            why = "not held for review"
        else:
            c = hit_by_id.get(id(k))
            party = {"Northwind": "Us"}.get(k["party"], k["party"])
            if c is None:
                why = "not captured"
            else:
                bad = [f for f, good in (("Party", c.get("Party") == party), ("TriggerType", c.get("TriggerType") == k["triggerType"]),
                                         ("DueDate", (c.get("DueDate") or None) == (k["nextDueDate"] or None))) if not good]
                ok, why = not bad, "wrong " + ", ".join(bad)
        traps[t][1] += 1
        traps[t][0] += ok
        if not ok:
            traps[t][2].append(f"{k['contractFile'][:2]} {k['clauseRef']}: {k['title']} ({why})")
    scored = len(open_cap) - held_matched
    return {"track": track, "hits": hits, "miss": miss, "fields": fields, "tot": tot, "hold": hold, "held_ok": held_ok,
            "held_wrong": held_wrong, "held_miss": held_miss, "extras": extras, "exc": exc, "false_inc": false_inc,
            "sup": sup, "sup_ok": sup_ok, "sup_noted": sup_noted, "traps": traps, "scored": scored,
            "recall": len(hits) / max(1, len(track)), "precision": len(hits) / max(1, scored), "per_contract": per_contract}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score captured obligations against the sample answer key (S-07, S-08, S-09).")
    ap.add_argument("items", help="Obligations items JSON (list, or {'value': [...]})")
    ap.add_argument("--key", default=str(DEFAULT_KEY), help="answer-key.json (default: ../../sample-data/answer-key.json)")
    ap.add_argument("--map", action="append", default=[], metavar="SRC=DST", help="copy field SRC into DST first")
    ap.add_argument("--contracts", help="comma-separated file-name prefixes to score (e.g. 01,02); default all")
    ap.add_argument("--min-recall", default="0.9")
    ap.add_argument("--min-precision", default="0.9")
    ap.add_argument("--min-field-accuracy", default="0.9")
    ap.add_argument("--min-holds", default="2/3", help="held correctly / hold rows (default 2/3)")
    ap.add_argument("--gating-traps", default="amendment,routine-admin", help="trap types that must be 100%%")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    maps = [tuple(m.split("=", 1)) for m in a.map]
    cap = load_items(a.items, maps)
    key = json.load(open(a.key, encoding="utf-8"))
    only = [p.strip() for p in a.contracts.split(",")] if a.contracts else None
    r = score(cap, key, only)
    hits, track = r["hits"], r["track"]
    print(f"Recall {len(hits)}/{len(track)} = {r['recall']:.0%}   Precision {len(hits)}/{r['scored']} = {r['precision']:.0%}")
    print(f"Held correctly {len(r['held_ok'])}/{len(r['hold'])} (open, ReviewState Needs review; {len(r['held_wrong'])} captured but not held, {len(r['held_miss'])} not captured)")
    print(f"Traps: excluded correctly {len(r['exc']) - len(r['false_inc'])}/{len(r['exc'])}; superseded correctly {len(r['sup_ok'])}/{len(r['sup'])}"
          f" (with a 'Superseded by' note on the base item: {len(r['sup_noted'])}/{len(r['sup'])})")
    print("Field accuracy on matched items: " + ", ".join(f"{f} {r['fields'][f]}/{r['tot'][f]}" for f in FIELDS if r["tot"][f]))
    print("\nTrap handling by type:")
    for t, (ok, n, fails) in sorted(r["traps"].items()):
        print(f"  {t:<20} {ok}/{n}")
        for f in fails:
            print(f"      - {f}")
    print("\nPer contract (track hit/total, extras):")
    for cf, v in sorted(r["per_contract"].items()):
        print(f"  {cf[:45]:<46} {v['hit']}/{v['track']}" + (f"  extras {v['extra']}" if v.get("extra") else ""))
    for title, rows in (("MISSED", [f"{k['contractFile'][:2]} {k['clauseRef']}: {k['title']} [{k.get('trapType') or ''}]" for k in r["miss"]]),
                        ("HOLD rows not captured as open items", [f"{k['contractFile'][:2]} {k['clauseRef']}: {k['title']}" for k in r["held_miss"]]),
                        ("HOLD rows captured but not in Needs review", [f"{k['contractFile'][:2]} {k['clauseRef']}: {k['title']} (ReviewState {c.get('ReviewState')})" for k, c in r["held_wrong"]]),
                        ("EXTRA (captured, not in key)", [f"{(c.get('ContractName') or '?')[:2]} {c.get('ClauseRef')}: {c.get('Title')}" for c in r["extras"]]),
                        ("WRONGLY INCLUDED traps", [f"{k['contractFile'][:2]} {k['clauseRef']}: {k['title']}" for k in r["false_inc"]])):
        print(f"\n{title}:" + ("" if rows else " none"))
        for x in rows:
            print("  " + x)
    mism = []
    for k, c in hits:
        party = {"Northwind": "Us"}.get(k["party"], k["party"])
        d = []
        if (c.get("DueDate") or None) != (k["nextDueDate"] or None):
            d.append(f"due {c.get('DueDate')} vs {k['nextDueDate']}")
        if c.get("Category") != k["category"]:
            d.append(f"cat {c.get('Category')} vs {k['category']}")
        if c.get("TriggerType") != k["triggerType"]:
            d.append(f"trig {c.get('TriggerType')} vs {k['triggerType']}")
        if c.get("Recurrence") != k["recurrence"]:
            d.append(f"recur {c.get('Recurrence')} vs {k['recurrence']}")
        if c.get("Party") != party:
            d.append(f"party {c.get('Party')} vs {party}")
        if clause(c.get("ClauseRef")) != clause(k["clauseRef"]):
            d.append(f"clause {c.get('ClauseRef')} vs {k['clauseRef']}")
        if d:
            mism.append(f"{k['contractFile'][:2]} {k['clauseRef']}: " + "; ".join(d))
    print("\nFIELD MISMATCHES:" + ("" if mism else " none"))
    for x in mism:
        print("  " + x)

    gates = []
    gates.append(("Recall", f">= {a.min_recall}", f"{r['recall']:.3f}", r["recall"] >= frac(a.min_recall) - 1e-9))
    gates.append(("Precision", f">= {a.min_precision}", f"{r['precision']:.3f}", r["precision"] >= frac(a.min_precision) - 1e-9))
    for f in FIELDS:
        if r["tot"][f]:
            acc = r["fields"][f] / r["tot"][f]
            gates.append((f"Field {f}", f">= {a.min_field_accuracy}", f"{acc:.3f}", acc >= frac(a.min_field_accuracy) - 1e-9))
    for t in [x.strip() for x in a.gating_traps.split(",") if x.strip()]:
        ok, n, _ = r["traps"].get(t, [0, 0, []])
        gates.append((f"Trap {t}", "100%", f"{ok}/{n}", n > 0 and ok == n or (n == 0 and only is not None)))
    if r["hold"]:
        share = len(r["held_ok"]) / len(r["hold"])
        gates.append(("Held correctly", f">= {a.min_holds}", f"{len(r['held_ok'])}/{len(r['hold'])}", share >= frac(a.min_holds) - 1e-9))
    print("\nGATES:")
    for name, want, got, ok in gates:
        print(f"  {'PASS' if ok else 'FAIL'}  {name:<22} {want:<10} got {got}")
    passed = all(g[3] for g in gates)
    print(f"\nCAPTURE: {'PASS' if passed else 'FAIL'}")
    if a.json_out:
        json.dump({"pass": passed, "recall": r["recall"], "precision": r["precision"],
                   "heldCorrectly": [len(r["held_ok"]), len(r["hold"])],
                   "fieldAccuracy": {f: [r["fields"][f], r["tot"][f]] for f in FIELDS},
                   "traps": {t: v[:2] for t, v in r["traps"].items()},
                   "missed": [f"{k['contractFile']}|{k['clauseRef']}" for k in r["miss"]],
                   "extras": [f"{c.get('ContractName')}|{c.get('ClauseRef')}|{c.get('Title')}" for c in r["extras"]],
                   "gates": [{"gate": g[0], "threshold": g[1], "value": g[2], "pass": g[3]} for g in gates]},
                  open(a.json_out, "w", encoding="utf-8"), indent=1)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
