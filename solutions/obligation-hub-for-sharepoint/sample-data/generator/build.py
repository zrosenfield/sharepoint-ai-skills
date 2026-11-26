"""Build the 11 sample contracts, answer key, manifest and readable key; then self-check.

Run:  python3 build.py   (from this folder)
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

from docx import Document

import contracts_1 as c1
import contracts_2 as c2
from lib import TODAY

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CONTRACTS = OUT / "contracts"
CONTRACTS.mkdir(parents=True, exist_ok=True)

ENUMS = {
    "party": {"Northwind", "Counterparty", "Both"},
    "category": {"Payment", "Reporting", "Notice & renewal", "Compliance & audit", "Service levels", "Insurance",
                 "Data & confidentiality", "Purchasing & volume", "Other"},
    "triggerType": {"Fixed date", "Recurring", "Event-driven", "Ongoing"},
    "recurrence": {"None", "Weekly", "Monthly", "Quarterly", "Semi-annual", "Annual"},
    "risk": {"High", "Medium", "Low"},
    "expected": {"track", "exclude", "superseded", "hold"},
}
MAN_ENUMS = {
    "northwindRole": {"Customer", "Supplier", "Licensee", "Tenant", "Borrower", "Distributor", "Controller", "Reseller"},
    "contractType": {"Customer agreement", "Supplier agreement", "Partner agreement", "License", "Lease", "Financing",
                     "Data processing", "Amendment"},
    "autoRenews": {"Yes", "No"},
    "businessUnit": {"Sales", "Procurement", "Finance", "Legal", "IT", "Facilities", "Operations"},
}
KEY_ORDER = ["contractFile", "counterparty", "title", "obligationText", "clauseRef", "sourceClause", "party", "category",
             "triggerType", "recurrence", "nextDueDate", "triggerEvent", "risk", "expected", "reason", "isTrap", "trapType"]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def doc_text(path):
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            seen = set()
            for cell in row.cells:
                if id(cell._tc) in seen:
                    continue
                seen.add(id(cell._tc))
                parts.extend(p.text for p in cell.paragraphs)
    return "\n".join(parts)


def bucket(iso_date):
    if iso_date is None:
        return "No date"
    d = date.fromisoformat(iso_date)
    delta = (d - TODAY).days
    if delta < 0:
        return "Overdue"
    if delta <= 14:
        return "Next 14 days"
    if delta <= 120:
        return "15-120 days"
    return "Later (>120 days)"


def build():
    obs, man = [], []
    for fn in (c1.c01, c1.c02, c1.c03, c1.c04, c1.c05, c2.c06, c2.c07, c2.c08, c2.c09, c2.c10, c2.c11):
        o, m = fn(CONTRACTS)
        obs.extend(o)
        man.append(m)
    obs = [OrderedDict((k, r[k]) for k in KEY_ORDER) for r in obs]
    return obs, man


def check(obs, man):
    errors = []
    texts = {}
    for m in man:
        p = CONTRACTS / m["fileName"]
        texts[m["fileName"]] = norm(doc_text(p))
    # 1. verbatim source clauses
    for i, r in enumerate(obs):
        t = texts.get(r["contractFile"])
        if t is None:
            errors.append(f"row {i}: unknown file {r['contractFile']}")
            continue
        if norm(r["sourceClause"]) not in t:
            errors.append(f"row {i} ({r['title']}): sourceClause not found verbatim in {r['contractFile']}")
    # 2. enums / field rules
    for i, r in enumerate(obs):
        for k, allowed in ENUMS.items():
            if r[k] not in allowed:
                errors.append(f"row {i}: {k}={r[k]!r} not allowed")
        if len(r["title"]) > 60:
            errors.append(f"row {i}: title too long ({len(r['title'])}) {r['title']}")
        tt = r["triggerType"]
        if tt in ("Event-driven", "Ongoing") and r["nextDueDate"] is not None:
            errors.append(f"row {i}: {tt} must have null nextDueDate")
        if tt in ("Fixed date", "Recurring") and r["nextDueDate"] is None:
            errors.append(f"row {i}: {tt} needs nextDueDate")
        if tt == "Event-driven" and not r["triggerEvent"]:
            errors.append(f"row {i}: Event-driven needs triggerEvent")
        if tt != "Event-driven" and r["triggerEvent"] is not None:
            errors.append(f"row {i}: triggerEvent only for Event-driven")
        if tt == "Recurring" and r["recurrence"] == "None":
            errors.append(f"row {i}: Recurring needs recurrence")
        if tt != "Recurring" and r["recurrence"] != "None":
            errors.append(f"row {i}: non-recurring must have recurrence None")
        if r["expected"] == "track" and r["reason"] is not None:
            errors.append(f"row {i}: track rows have null reason")
        if r["expected"] != "track" and not r["reason"]:
            errors.append(f"row {i}: {r['expected']} rows need reason")
        if bool(r["isTrap"]) != bool(r["trapType"]):
            errors.append(f"row {i}: isTrap/trapType mismatch")
    # 3. manifest
    files = sorted(p.name for p in CONTRACTS.glob("*.docx"))
    if files != sorted(m["fileName"] for m in man):
        errors.append(f"manifest/file mismatch: {files}")
    for m in man:
        for k, allowed in MAN_ENUMS.items():
            if m[k] not in allowed:
                errors.append(f"manifest {m['fileName']}: {k}={m[k]!r}")
        if " " in m["fileName"]:
            errors.append(f"space in file name {m['fileName']}")
    # 4. word counts
    wc = {}
    for m in man:
        n = len(re.findall(r"\S+", texts[m["fileName"]]))
        wc[m["fileName"]] = n
    return errors, wc


def write_outputs(obs, man, wc):
    (OUT / "answer-key.json").write_text(json.dumps(obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "contracts-manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "answer-key.md").write_text(render_md(obs, man), encoding="utf-8")


def md_escape(s):
    return (s or "").replace("|", "\\|")


TRAP_GUIDE = OrderedDict([
    ("amendment", "Read the amendment with the base contract. Track the amended values (120-day non-renewal notice, 10-day report) from file 02 and treat the original MSA clauses (90 days, 15 days) as superseded, not as separate live obligations."),
    ("notice-window", "Compute the window from the expiry date and track the closing date (lease option: opens 2026-09-30, closes 2026-12-30; Fabrikam transition request by 2027-01-30). Missing the window forfeits the right."),
    ("claim-window", "Track Northwind's duty to claim the Fabrikam service credit within 30 days after month end, even though the SLA itself is Fabrikam's obligation."),
    ("event-driven", "Capture with triggerType Event-driven, a plain-language triggerEvent and no due date (change of control, repairs, defects, sub-processor objection, MFN price match, default notice)."),
    ("counterparty-vs-us", "Assign the right party. A counterparty right (an audit) can create a Northwind duty to cooperate; counterparty duties (breach notice, price-increase notice, discontinuation notice) are tracked as Counterparty so Northwind can hold them to it."),
    ("fixed-expiry", "A fixed end date with no auto-renewal is itself a tracked decision date (Adventure Works 2026-12-31, Fabrikam 2027-03-31)."),
    ("prohibition", "A standing restriction (no affiliate use of Litware software) is tracked as an Ongoing compliance obligation with no date."),
    ("routine-admin", "Do not create obligations for administrative boilerplate (points of contact, invoice address, good-faith cooperation, headings, uniforms, access badges, counterparts, own costs)."),
    ("condition-precedent", "A closing-date fee that was a condition to effectiveness was satisfied at signing; do not track it as an overdue payment."),
    ("missing-document", "A protected obligation (payment terms, data return) whose terms are only in a referenced document missing from the Contracts library: create one open item held for review (ReviewState Needs review, Confidence Low) rather than excluding it or guessing its terms."),
])


def render_md(obs, man):
    L = []
    track = [r for r in obs if r["expected"] == "track"]
    L.append("# Answer key - sample contract obligations (Northwind Traders demo kit)")
    L.append("")
    L.append(f"Reference date (\"today\"): **{TODAY.isoformat()}** (Pacific time). All companies, people and contracts are fictional. "
             f"Machine-readable version: `answer-key.json` (same rows, same order).")
    L.append("")
    L.append("## Summary")
    L.append("")
    ce = Counter(r["expected"] for r in obs)
    L.append(f"- Rows: **{len(obs)}** in total: **{ce['track']} track**, **{ce['hold']} hold**, **{ce['exclude']} exclude**, **{ce['superseded']} superseded**, across **{len(man)}** documents.")
    L.append(f"- Trap rows (isTrap = true): **{sum(1 for r in obs if r['isTrap'])}** ({sum(1 for r in track if r['isTrap'])} of them are tracked obligations; the rest are hold/exclude/superseded).")
    L.append("")
    L.append("### Tracked obligations by category")
    L.append("")
    L.append("| Category | Track rows |")
    L.append("|---|---:|")
    for k, v in sorted(Counter(r["category"] for r in track).items(), key=lambda x: (-x[1], x[0])):
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("### Tracked obligations by party and trigger type")
    L.append("")
    L.append("| Party | Track rows |  | Trigger type | Track rows |")
    L.append("|---|---:|---|---|---:|")
    cp = sorted(Counter(r["party"] for r in track).items(), key=lambda x: -x[1])
    ct = sorted(Counter(r["triggerType"] for r in track).items(), key=lambda x: -x[1])
    for i in range(max(len(cp), len(ct))):
        a = cp[i] if i < len(cp) else ("", "")
        b = ct[i] if i < len(ct) else ("", "")
        L.append(f"| {a[0]} | {a[1]} |  | {b[0]} | {b[1]} |")
    L.append("")
    L.append("### Due-date distribution (track rows, relative to today)")
    L.append("")
    L.append("| Bucket | Rows | Obligations |")
    L.append("|---|---:|---|")
    for b in ["Overdue", "Next 14 days", "15-120 days", "Later (>120 days)", "No date"]:
        rows = [r for r in track if bucket(r["nextDueDate"]) == b]
        names = "; ".join(f"{r['title']} ({r['nextDueDate']})" for r in sorted(rows, key=lambda r: r["nextDueDate"] or "")) if b != "No date" else "Event-driven and ongoing obligations"
        L.append(f"| {b} | {len(rows)} | {md_escape(names)} |")
    L.append("")
    L.append("Buckets: Overdue = due before today; Next 14 days = today through 2026-12-08; 15-120 days = 2026-12-09 through 2027-03-24; Later = after 2027-03-24.")
    L.append("")
    L.append("### Traps and what a correct extraction does")
    L.append("")
    L.append("| Trap type | Rows | Correct handling |")
    L.append("|---|---:|---|")
    ctrap = Counter(r["trapType"] for r in obs if r["isTrap"])
    for k, txt in TRAP_GUIDE.items():
        L.append(f"| {k} | {ctrap.get(k, 0)} | {md_escape(txt)} |")
    L.append("")
    L.append("### Conventions used in this key")
    L.append("")
    L.append("- `party` is from Northwind's point of view: Northwind = our obligation; Counterparty = the other side's obligation we monitor; Both = mutual (e.g., either party may give non-renewal notice). If your list uses \"Us\", map Northwind to Us.")
    L.append("- `nextDueDate` for Recurring rows is the next occurrence on or after today; earlier occurrences are assumed fulfilled. Overdue rows are one-time (Fixed date) obligations whose date has passed and are assumed not yet done (Contoso BCP plan, Tailspin marketing plan, Proseware initial SOC 2 report, Woodgrove insurance endorsements).")
    L.append("- Event-driven and Ongoing rows have no date; Event-driven rows carry a `triggerEvent`.")
    L.append("- `sourceClause` is verbatim text from the .docx (straight ASCII quotes; compare after collapsing whitespace). Clause numbers and captions are in `clauseRef`, not in `sourceClause`.")
    L.append("- Superseded rows carry the date the original clause would have produced, so a scorer can recognise (and penalise) an extraction that tracks the pre-amendment value.")
    L.append("- Hold rows are expected as open items with ReviewState \"Needs review\" (Confidence Low) and no due date. They are scored separately (held correctly x/y), not as tracked obligations and not as extras. The tables above count track rows only.")
    L.append("- The manifest records each document's own text (MSA notice period 90 days; Amendment notice period 120 days). The amendment controls, so the effective Contoso notice period is 120 days.")
    L.append("- Boilerplate that is neither an obligation nor a listed trap (governing law, limitation of liability, entire agreement, termination-for-cause rights) is not listed; an extractor should not create rows for it.")
    L.append("")
    L.append("## Documents")
    L.append("")
    L.append("| File | Counterparty | Northwind role | Type | Effective | Expires | Auto-renews | Notice (days) | Value (USD) | Words |")
    L.append("|---|---|---|---|---|---|---|---:|---:|---:|")
    for m in man:
        v = f"{m['contractValue']:,}" if m["contractValue"] else ""
        L.append(f"| {m['fileName']} | {m['counterparty']} | {m['northwindRole']} | {m['contractType']} | {m['effectiveDate']} | "
                 f"{m['expirationDate'] or ''} | {m['autoRenews']} | {m['noticePeriodDays'] if m['noticePeriodDays'] is not None else ''} | {v} | {WC.get(m['fileName'], '')} |")
    L.append("")
    L.append("## Answer key by contract")
    for m in man:
        rows = [r for r in obs if r["contractFile"] == m["fileName"]]
        L.append("")
        L.append(f"### {m['fileName']} - {m['title']} ({m['counterparty']})")
        L.append("")
        L.append("| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |")
        L.append("|---:|---|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            note = r["reason"] if r["expected"] != "track" else (r["triggerEvent"] or r["obligationText"])
            due = r["nextDueDate"] or ""
            if r["expected"] == "track" and r["nextDueDate"]:
                due += f" ({bucket(r['nextDueDate'])})"
            L.append(f"| {i} | {r['expected']} | {md_escape(r['title'])} | {r['party']} | {r['category']} | {r['triggerType']} | "
                     f"{r['recurrence']} | {due} | {r['risk']} | {md_escape(r['clauseRef'])} | {r['trapType'] or ''} | {md_escape(note)} |")
    L.append("")
    return "\n".join(L)


WC = {}

if __name__ == "__main__":
    obs, man = build()
    errors, WC = check(obs, man)
    write_outputs(obs, man, WC)
    track = [r for r in obs if r["expected"] == "track"]
    print("rows:", len(obs), dict(Counter(r["expected"] for r in obs)))
    print("track by category:", dict(Counter(r["category"] for r in track)))
    print("track by party:", dict(Counter(r["party"] for r in track)))
    print("track by trigger:", dict(Counter(r["triggerType"] for r in track)))
    print("date buckets (track):", dict(Counter(bucket(r["nextDueDate"]) for r in track)))
    for b in ["Overdue", "Next 14 days"]:
        for r in track:
            if bucket(r["nextDueDate"]) == b:
                print(f"   {b}: {r['nextDueDate']}  {r['title']}")
    print("word counts:", WC)
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("ALL CHECKS PASSED")
