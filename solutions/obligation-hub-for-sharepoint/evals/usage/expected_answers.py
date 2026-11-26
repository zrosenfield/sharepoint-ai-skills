#!/usr/bin/env python3
"""Compute the expected answers for the usage evals (USAGE-EVALS.md, U-01 ... U-15) from the sample data.

Inputs (sample-data folder): answer-key.json and contracts-manifest.json (required), contracts/*.docx
(optional; used to quote clauses: notice method, Woodgrove events of default, Fabrikam term). Nothing is
typed in by hand except each task's setup and the planted defects of U-05 and U-12; every date, count,
list and quote below is derived from those files and --today.

The register a tester sees after loading the sample (pre-captured, or captured by a skill that passes
S-07..S-09) is: open = answer-key rows "track" (ReviewState Confirmed) + "hold" (Needs review);
"superseded" rows are Not applicable; "exclude" rows are absent. Risk is not scored by the answer key,
so it is recomputed here with the capture skill's consequence rubric (risk_of below), which reproduces the
recalibrated values in sample-data/pre-captured-obligations.json (checked with --site-obligations).

Sample run:
  python3 expected_answers.py --samples ../../sample-data --today 2026-11-24 --out expected/expected_answers.json
  python3 expected_answers.py --samples ../../sample-data --check expected/expected_answers.json   # exit 1 if stale
  python3 expected_answers.py --samples ../../sample-data --site-obligations ../../sample-data/pre-captured-obligations.json
"""
import argparse
import calendar
import hashlib
import json
import re
import sys
import zipfile
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RISK_RANK = {"High": 0, "Medium": 1, "Low": 2}


# ------------------------------------------------------------------ helpers
def d(s):
    return date.fromisoformat(s) if s else None


def add_months(x, n):
    m = x.month - 1 + n
    y, m = x.year + m // 12, m % 12 + 1
    return date(y, m, min(x.day, calendar.monthrange(y, m)[1]))


def party(row):
    return {"Northwind": "Us"}.get(row["party"], row["party"])


def short(row):
    return f"{row['contractFile'][:2]} {row['clauseRef']}"


def docx_lines(path):
    """Body paragraphs and table rows (cells joined ' | '), headers and footers ignored."""
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    lines = []

    def ptext(p):
        out = []
        for el in p.iter():
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag == W + "tab":
                out.append("\t")
        return "".join(out)

    for el in body:
        if el.tag == W + "p":
            t = ptext(el).strip()
            if t:
                lines.append(t)
        elif el.tag == W + "tbl":
            for tr in el.iter(W + "tr"):
                cells = [" ".join(ptext(p).strip() for p in tc.iter(W + "p")).strip() for tc in tr.iter(W + "tc")]
                if any(cells):
                    lines.append(" | ".join(cells))
    return lines


def clause_text(lines, number):
    """The paragraph that starts with a clause number such as '6.1' (number and caption included)."""
    for ln in lines:
        if re.match(r"^%s\.?\s" % re.escape(number), ln):
            return ln
    return None


def risk_of(row, manifest):
    """Capture skill's consequence rubric (Skills/capture-obligations, field Risk).
    High: missing it loses a right or money or starts a legal clock: notice, renewal and option deadlines
    we must act on; change-of-control and breach notices; financing covenants, compliance certificates
    and default notices. Medium: other dated or money obligations. Low: ongoing conduct, and counterparty
    duties we only monitor (other than payments and data)."""
    p, cat, trig, title = party(row), row["category"], row["triggerType"], row["title"].lower()
    financing = manifest.get(row["contractFile"], {}).get("contractType") == "Financing"
    if financing and cat in ("Reporting", "Compliance & audit"):
        return "High"
    if "breach" in title and cat == "Data & confidentiality":
        return "High"
    if cat == "Notice & renewal" and p in ("Us", "Both") and "terminate for convenience" not in title \
            and not ("terminate" in title and trig == "Event-driven"):
        return "High"
    if trig == "Ongoing":
        return "Low"
    if p == "Counterparty" and cat not in ("Payment", "Data & confidentiality"):
        return "Low"
    return "Medium"


def item(row, today, manifest, extra=None):
    due = d(row["nextDueDate"])
    o = {"contract": row["contractFile"], "counterparty": row["counterparty"], "clause": row["clauseRef"],
         "title": row["title"], "party": party(row), "category": row["category"], "triggerType": row["triggerType"],
         "dueDate": row["nextDueDate"], "triggerEvent": row["triggerEvent"], "risk": risk_of(row, manifest),
         "reviewState": "Needs review" if row["expected"] == "hold" else "Confirmed"}
    if due:
        delta = (due - today).days
        o["timing"] = "Overdue" if delta < 0 else ("Due soon" if delta <= 14 else "Upcoming")
        o["daysOverdue" if delta < 0 else "daysUntilDue"] = abs(delta)
    else:
        o["timing"] = "No date"
    if extra:
        o.update(extra)
    return o


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ tasks
def build(samples, today):
    key = json.load(open(samples / "answer-key.json", encoding="utf-8"))
    man_list = json.load(open(samples / "contracts-manifest.json", encoding="utf-8"))
    manifest = {m["fileName"]: m for m in man_list}
    texts = {}
    cdir = samples / "contracts"
    for m in man_list:
        p = cdir / m["fileName"]
        if p.exists():
            texts[m["fileName"]] = docx_lines(p)

    def quote(fname, number):
        return clause_text(texts.get(fname, []), number) if fname in texts else None

    track = [r for r in key if r["expected"] == "track"]
    hold = [r for r in key if r["expected"] == "hold"]
    sup = [r for r in key if r["expected"] == "superseded"]
    exc = [r for r in key if r["expected"] == "exclude"]
    open_rows = track + hold
    by_date = lambda rows: sorted(rows, key=lambda r: (r["nextDueDate"] is None, r["nextDueDate"] or "", r["contractFile"]))  # noqa: E731
    T = {}

    # U-01 What do I owe this week?
    end = today + timedelta(days=7)
    mine = [r for r in track if party(r) in ("Us", "Both") and r["nextDueDate"] and d(r["nextDueDate"]) <= end]
    T["U-01"] = {
        "window": [today.isoformat(), end.isoformat()], "definition": "open, Confirmed, Party Us or Both, DueDate on or before today + 7 (overdue included)",
        "items": [item(r, today, manifest) for r in by_date(mine)],
        "overdueCount": sum(1 for r in mine if d(r["nextDueDate"]) < today),
        "undatedOpenUsOrBoth": sum(1 for r in track if party(r) in ("Us", "Both") and not r["nextDueDate"]),
        "optionalMention": [item(r, today, manifest) for r in by_date(track) if party(r) == "Counterparty" and r["nextDueDate"] and d(r["nextDueDate"]) < today],
        "mustNotInclude": [short(r) + " " + r["title"] for r in hold + sup],
    }

    # U-02 Which contracts auto-renew in the next 120 days?
    win = today + timedelta(days=120)
    auto = []
    nonrenew = [r for r in track if r["category"] == "Notice & renewal" and "non-renewal" in r["title"].lower()]
    for r in nonrenew:
        m = manifest[r["contractFile"]]
        if m["autoRenews"] != "Yes":
            continue
        deadline = d(r["nextDueDate"])
        counted = deadline + timedelta(days=m["noticePeriodDays"])
        if m["expirationDate"]:
            # notice counted back from the end of the current term (Contoso: 120 days before 2027-03-31)
            assert counted == d(m["expirationDate"]), (r["contractFile"], counted, m["expirationDate"])
            term_end, renews = counted, counted + timedelta(days=1)
        else:
            # no fixed end: notice counted back from the start of the next period (Litware: next Support Year)
            term_end, renews = counted - timedelta(days=1), counted
        auto.append({"counterparty": r["counterparty"], "contract": r["contractFile"],
                     "agreement": manifest.get(m.get("amends") or r["contractFile"], m)["title"],
                     "noticeDeadline": deadline.isoformat(), "noticeDays": m["noticePeriodDays"], "clause": r["clauseRef"],
                     "termEnds": term_end.isoformat(), "renewsOn": renews.isoformat(),
                     "noticeDeadlineInWindow": deadline <= win, "renewalInWindow": renews <= win})
    decisions = [r for r in track if r["category"] == "Notice & renewal" and r not in nonrenew and r["nextDueDate"]
                 and today <= d(r["nextDueDate"]) <= win]
    T["U-02"] = {
        "window": [today.isoformat(), win.isoformat()],
        "autoRenewing": auto,
        "answer": [a for a in auto if a["noticeDeadlineInWindow"] or a["renewalInWindow"]],
        "notInWindow": [a for a in auto if not (a["noticeDeadlineInWindow"] or a["renewalInWindow"])],
        "alsoActInWindow": [item(r, today, manifest) for r in by_date(decisions)],
        "expiringInWindowNoAutoRenew": [{"contract": f, "counterparty": m["counterparty"], "expires": m["expirationDate"]}
                                        for f, m in manifest.items() if m["expirationDate"] and m["autoRenews"] != "Yes"
                                        and today <= d(m["expirationDate"]) <= win],
        "wrongValues": [{"value": r["nextDueDate"], "why": f"superseded {short(r)} ({r['title']}): {r['reason']}"} for r in sup
                        if r["category"] == "Notice & renewal"],
    }

    # U-03 Prepare me for the Fabrikam renewal call
    f03 = "03-Fabrikam-Cloud-Hosting-Agreement.docx"
    m03 = manifest[f03]
    rows03 = [r for r in open_rows if r["contractFile"] == f03]
    T["U-03"] = {
        "keyTerms": {k: m03[k] for k in ("title", "counterparty", "contractType", "effectiveDate", "expirationDate", "autoRenews", "contractValue", "governingLaw")},
        "daysToExpiry": (d(m03["expirationDate"]) - today).days,
        "deadlines": [item(r, today, manifest) for r in by_date([r for r in rows03 if r["nextDueDate"]])],
        "undated": [item(r, today, manifest) for r in rows03 if not r["nextDueDate"]],
        "quotes": {n: quote(f03, n) for n in ("3.1", "3.2", "3.3", "4.3", "6.1", "6.2", "6.3")},
    }

    # U-04 Mark the Contoso insurance certificate fulfilled with evidence
    r04 = next(r for r in track if r["contractFile"] == "01-Contoso-MSA.docx" and r["clauseRef"] == "Section 7.1")
    T["U-04"] = {
        "target": item(r04, today, manifest),
        "after": {"Status": "Fulfilled", "FulfilledOn": today.isoformat(), "Evidence": "<the link given>", "Timing": "Closed", "ReviewState": "Confirmed"},
        "successor": {"DueDate": add_months(d(r04["nextDueDate"]), 12).isoformat(), "CaptureKey": "<item's key>#" + add_months(d(r04["nextDueDate"]), 12).isoformat(),
                      "Status": "Not started", "Notes": "Next occurrence after #<ID>", "copied": "Owner, EscalationOwner, Risk, SourceClause ...; FulfilledOn, Evidence, LastReminded empty"},
        "runLog": {"Workflow": "Mark fulfilled", "ItemsUpdated": 1, "ItemsCreated": 1, "rows": 1},
    }

    # U-05 Remove a routine clause and confirm capture won't re-add it
    f10 = "10-Fourth-Coffee-Facilities-Services-Agreement.docx"
    planted = next(r for r in exc if r["contractFile"] == f10 and r["clauseRef"] == "Section 2.1")
    T["U-05"] = {
        "plantedItem": {"Title": planted["title"], "ContractName": f10, "Counterparty": planted["counterparty"], "ClauseRef": planted["clauseRef"],
                        "SourceClause": planted["sourceClause"], "Party": party(planted), "Category": planted["category"],
                        "TriggerType": planted["triggerType"], "Recurrence": "None", "Status": "Not started", "Timing": "No date",
                        "ReviewState": "Confirmed", "Confidence": "Medium", "Risk": "Low", "IsSample": True,
                        "CaptureKey": f"{f10}|{planted['clauseRef']}|designate-contact"},
        "exclusion": {"Scope": "All contracts", "ContractName": "", "Category": planted["category"], "Active": True,
                      "PatternMustContain": "Example: \"" + planted["sourceClause"] + "\""},
        "itemAfter": {"Status": "Not applicable", "Timing": "Closed", "NotesStartsWith": "Excluded: "},
        "afterRecapture": {"openItemsFor10": [item(r, today, manifest) for r in open_rows if r["contractFile"] == f10],
                           "noOpenItemFor": planted["clauseRef"], "exclusionRows": 1,
                           "excludedClausesInDetails": [r["clauseRef"] for r in exc if r["contractFile"] == f10]},
    }

    # U-06 Upload an amendment and confirm the base obligations are superseded
    f02 = "02-Contoso-MSA-Amendment-1.docx"
    amended = {}
    for r in track:
        if r["contractFile"] == f02:
            m = re.search(r"\(amends MSA (Section [\d.]+)\)", r["clauseRef"])
            if m:
                amended[m.group(1)] = r["clauseRef"].split(" (")[0]
    T["U-06"] = {
        "before": [item(r, today, manifest, {"status": "Not started"}) for r in sup],
        "superseded": [{"contract": r["contractFile"], "clause": r["clauseRef"], "title": r["title"], "Status": "Not applicable", "Timing": "Closed",
                        "NotesContains": f"Superseded by {f02} {amended.get(r['clauseRef'], '?')}", "oldDueDate": r["nextDueDate"]} for r in sup],
        "created": [item(r, today, manifest) for r in by_date([r for r in track if r["contractFile"] == f02])],
        "runLog": {"Workflow": "Capture", "ContractName": f02, "ItemsCreated": sum(1 for r in track if r["contractFile"] == f02),
                   "ItemsUpdated": len(sup), "ItemsHeld": 0, "extraSkippedRowAllowed": True},
    }

    # U-07 Find everything Woodgrove can call a default on
    f11 = "11-Woodgrove-Bank-Revolving-Credit-Facility.docx"
    q61 = quote(f11, "6.1")
    limbs = {"a": "fails to pay principal or interest within 3 Business Days after due", "b": "fails to comply with Section 4.1 (no cure period)",
             "c": "fails to comply with Article 3 or Article 5 and the failure continues 15 days after notice from the Bank",
             "d": "a representation proves materially incorrect when made (no tracked obligation)"}
    if q61:
        assert "three (3) Business Days" in q61 and "Section 4.1" in q61 and "Article 3 or Article 5" in q61 and "fifteen (15) days" in q61, q61

    def limb(r):
        n = r["clauseRef"].replace("Section ", "")
        if r["category"] == "Payment":
            return "a"
        if n.startswith("4."):
            return "b"
        if n.startswith(("3.", "5.")):
            return "c"
        return None

    rows11 = [r for r in track if r["contractFile"] == f11]
    T["U-07"] = {
        "eventsOfDefaultClause": "Section 6.1", "quote61": q61, "remedies62": quote(f11, "6.2"), "limbs": limbs,
        "items": [item(r, today, manifest, {"limb": limb(r)}) for r in by_date(rows11)],
        "mostUrgent": [item(r, today, manifest, {"limb": limb(r)}) for r in rows11 if r["nextDueDate"] and d(r["nextDueDate"]) < today],
        "notADefault": [short(r) + " " + r["title"] + ": " + (r["reason"] or "") for r in exc if r["contractFile"] == f11],
    }

    # U-08 What's waiting for review and why?
    def missing_doc(reason):
        m = re.search(r"only in (?:the |Northwind's )?(.+?)(?:, which|$)", reason or "")
        return m.group(1).strip() if m else None
    T["U-08"] = {"count": len(hold), "items": [item(r, today, manifest, {"missingDocument": missing_doc(r["reason"]), "reason": r["reason"],
                                                                        "confidence": "Low"}) for r in hold],
                 "action": "add the missing document to Contracts (then Re-capture) or confirm the terms and set Review = Confirmed"}

    # U-09 Leadership exposure by counterparty
    groups = defaultdict(list)
    for r in open_rows:
        groups[r["counterparty"]].append(r)
    exp = []
    for cp, rows in groups.items():
        dated = [r for r in rows if r["nextDueDate"]]
        upcoming = sorted([r for r in dated if d(r["nextDueDate"]) >= today], key=lambda r: r["nextDueDate"])
        exp.append({"counterparty": cp, "open": len(rows), "high": sum(risk_of(r, manifest) == "High" for r in rows),
                    "overdue": sum(1 for r in dated if d(r["nextDueDate"]) < today), "held": sum(r["expected"] == "hold" for r in rows),
                    "weOwe": sum(party(r) in ("Us", "Both") for r in rows), "theyOwe": sum(party(r) == "Counterparty" for r in rows),
                    "nextDeadline": ({"date": upcoming[0]["nextDueDate"], "title": upcoming[0]["title"]} if upcoming else None)})
    exp.sort(key=lambda x: (-x["high"], -x["open"], x["counterparty"]))
    high = sum(x["high"] for x in exp)
    T["U-09"] = {"byCounterparty": exp, "totals": {"open": len(open_rows), "high": high, "highShare": round(high / len(open_rows), 3),
                                                   "overdue": sum(x["overdue"] for x in exp), "held": len(hold)},
                 "notAvailable": ["dollar exposure", "trends over time"]}

    # U-10 What does Proseware owe us, and is anything late?
    f06 = "06-Proseware-Data-Processing-Agreement.docx"
    T["U-10"] = {"items": [item(r, today, manifest) for r in by_date([r for r in open_rows if r["contractFile"] == f06 and party(r) in ("Counterparty", "Both")])],
                 "late": [item(r, today, manifest) for r in open_rows if r["contractFile"] == f06 and party(r) == "Counterparty" and r["nextDueDate"] and d(r["nextDueDate"]) < today],
                 "mustNotInclude": [short(r) + " " + r["title"] + " (Party Us)" for r in open_rows if r["contractFile"] == f06 and party(r) == "Us"]}

    # U-11 Which obligations have no owner (only a Payment routing rule exists)?
    unowned = [r for r in track if r["category"] != "Payment"]
    cats = defaultdict(int)
    for r in unowned:
        cats[r["category"]] += 1
    T["U-11"] = {"setupRules": [{"Title": "Finance - payments", "Category": "Payment", "BusinessUnit": "Any", "Owner": "<tester>"}],
                 "assigned": sum(1 for r in track if r["category"] == "Payment"), "unownedConfirmed": len(unowned),
                 "unownedByCategory": dict(sorted(cats.items(), key=lambda kv: (-kv[1], kv[0]))),
                 "heldNotAssigned": len(hold), "acceptableFix": "a default Any/Any rule, or category rules covering the listed categories, created only after the user agrees"}

    # U-12 Check the hub's lists still match the skills' field names (planted defects)
    T["U-12"] = {"plantedDefects": [
        {"defect": "view 'Triggered and ongoing' deleted from Obligations", "expectedFinding": "missing view", "severity": "breaks undated-items view"},
        {"defect": "choice 'Semi-annual' removed from Obligations Recurrence", "expectedFinding": "missing choice", "severity": "capture/sweep writes fail for semi-annual items"},
        {"defect": "display name of Obligations Timing renamed to 'When'", "expectedFinding": "harmless: internal name Timing unchanged", "severity": "none"}],
        "mustNot": "change the schema without asking"}

    # U-13 Draft the Contoso non-renewal notice; don't send
    r_nr = next(r for r in track if r["contractFile"] == f02 and "non-renewal" in r["title"].lower())
    T["U-13"] = {"deadline": r_nr["nextDueDate"], "clause": r_nr["clauseRef"], "termEnds": manifest[f02]["expirationDate"],
                 "noticeDays": manifest[f02]["noticePeriodDays"], "noticeClause01": quote("01-Contoso-MSA.docx", "10.2"),
                 "amendment2": next((ln for ln in texts.get(f02, []) if ln.startswith("For clarity")), None),
                 "contosoParty": next((ln for ln in texts.get(f02, []) if "Contoso Ltd, a Delaware corporation" in ln), None),
                 "updatedContacts": [ln for ln in texts.get(f02, []) if ln.startswith(("Customer |", "Service Provider |"))],
                 "mustNot": ["send the email", "use the superseded 90-day period or 2026-12-31"]}

    # U-14 What's overdue and who owns it?
    od = [r for r in track if r["nextDueDate"] and d(r["nextDueDate"]) < today]
    od.sort(key=lambda r: (RISK_RANK[risk_of(r, manifest)], -(today - d(r["nextDueDate"])).days))
    T["U-14"] = {"items": [item(r, today, manifest, {"owner": "<tester> (Default - all obligations rule)"}) for r in od]}

    # U-15 Mark the Litware true-up fulfilled with a past date
    r15 = next(r for r in track if r["contractFile"] == "05-Litware-Software-License-Support.docx" and r["clauseRef"] == "Section 3.2")
    anniv = add_months(d(manifest[r15["contractFile"]]["effectiveDate"]), 24)
    T["U-15"] = {"target": item(r15, today, manifest), "FulfilledOn": "2026-11-20",
                 "successorDueDate": add_months(d(r15["nextDueDate"]), 12).isoformat(),
                 "successorCheck": f"next anniversary {anniv.isoformat()} + 30 days = {(anniv + timedelta(days=30)).isoformat()}",
                 "questionsAllowed": 0}
    assert T["U-15"]["successorDueDate"] == (anniv + timedelta(days=30)).isoformat(), T["U-15"]

    return {"generatedBy": "evals/usage/expected_answers.py", "today": today.isoformat(),
            "sources": {n: sha(samples / n) for n in ("answer-key.json", "contracts-manifest.json")},
            "docxRead": sorted(texts), "register": {"open": len(open_rows), "confirmed": len(track), "held": len(hold),
                                                    "superseded": len(sup), "excluded": len(exc)},
            "tasks": T}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compute expected answers for the Obligation Hub usage evals.")
    ap.add_argument("--samples", default=str(HERE.parent.parent / "sample-data"), help="sample-data folder")
    ap.add_argument("--today", default="2026-11-24", help="reference date (the sample's due dates assume 2026-11-24)")
    ap.add_argument("--out", help="write JSON here (default: print a summary only)")
    ap.add_argument("--check", help="compare with an existing expected_answers.json; exit 1 if it differs")
    ap.add_argument("--site-obligations", help="Obligations items (e.g. pre-captured-obligations.json) to check the risk rubric against")
    a = ap.parse_args(argv)
    samples = Path(a.samples)
    res = build(samples, date.fromisoformat(a.today))
    rc = 0
    if a.site_obligations:
        man = {m["fileName"]: m for m in json.load(open(samples / "contracts-manifest.json", encoding="utf-8"))}
        key = json.load(open(samples / "answer-key.json", encoding="utf-8"))
        site = json.load(open(a.site_obligations, encoding="utf-8"))
        norm = lambda s: set(re.sub(r"\s+", " ", s or "").lower().split())  # noqa: E731
        agree, diff = 0, []
        for r in key:
            if r["expected"] not in ("track", "hold"):
                continue
            ks = norm(r["sourceClause"])
            m = [c for c in site if c.get("ContractName") == r["contractFile"] and len(ks & norm(c.get("SourceClause"))) / max(1, min(len(ks), len(norm(c.get("SourceClause"))))) >= 0.6]
            if not m:
                diff.append(f"{short(r)}: not on site")
            elif m[0].get("Risk") == risk_of(r, man):
                agree += 1
            else:
                diff.append(f"{short(r)}: rubric {risk_of(r, man)} vs site {m[0].get('Risk')}")
        print(f"Risk rubric vs {a.site_obligations}: {agree} agree, {len(diff)} differ")
        for x in diff:
            print("  " + x)
        rc |= 1 if diff else 0
    t = res["tasks"]
    print(f"today {res['today']}; register open {res['register']['open']} (held {res['register']['held']}); docx read {len(res['docxRead'])}/11")
    print(f"U-01 {len(t['U-01']['items'])} items ({t['U-01']['overdueCount']} overdue) through {t['U-01']['window'][1]}")
    print(f"U-02 in window: " + ", ".join(f"{x['counterparty']} notice by {x['noticeDeadline']}" for x in t["U-02"]["answer"]) +
          "; outside: " + ", ".join(f"{x['counterparty']} {x['noticeDeadline']}" for x in t["U-02"]["notInWindow"]))
    print(f"U-04 successor {t['U-04']['successor']['DueDate']}; U-15 successor {t['U-15']['successorDueDate']}")
    print(f"U-07 {len(t['U-07']['items'])} Woodgrove items; most urgent: " + ", ".join(f"{x['clause']} {x['daysOverdue']}d overdue" for x in t["U-07"]["mostUrgent"]))
    print(f"U-09 High {t['U-09']['totals']['high']}/{t['U-09']['totals']['open']} = {t['U-09']['totals']['highShare']:.0%}")
    print(f"U-11 unowned {t['U-11']['unownedConfirmed']}, assigned {t['U-11']['assigned']}, held {t['U-11']['heldNotAssigned']}")
    print(f"U-14 overdue: " + "; ".join(f"{x['clause'] and x['contract'][:2]} {x['title']} ({x['risk']}, {x['daysOverdue']}d)" for x in t["U-14"]["items"]))
    text = json.dumps(res, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
        print("wrote", a.out)
    if a.check:
        old = Path(a.check).read_text(encoding="utf-8")
        same = old == text
        print(f"check {a.check}: {'UP TO DATE' if same else 'STALE (re-run with --out)'}")
        rc |= 0 if same else 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
