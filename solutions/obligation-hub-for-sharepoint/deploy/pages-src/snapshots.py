"""Builds the SAMPLE snapshots embedded in every Obligation Hub page.

The snapshots mirror what is loaded on the live demo site, so the offline view
matches it:
  Obligations  ../site/loaded_obligations_risk.json (NewRisk is used as Risk; IDs 1..n in file order;
               Owner and EscalationOwner are the sample owner on confirmed items that are not
               "Not applicable", which is what Assign owners did on the site; everything else as in the file)
  Contracts    ../samples/contracts-manifest.json (the key terms filled in on the site)
  Run Log      ../capture-run/runlog.json plus the Assign owners and Daily sweep seed runs of 2026-11-24
  Owners       the routing rules in ../seed/obligation-owners.demo.json, with the owner shown by name
Output shape mirrors the live-data contract ({headers:[...], rows:[[...]]}) with every value as TEXT,
so the pages read snapshot and live rows through exactly the same parser.
All companies, people and contracts are fictional sample data.
"""
import json
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
SAMPLES = KIT / "samples"
OBLIGATIONS_SRC = KIT / "site" / "loaded_obligations_risk.json"
RUNLOG_SRC = KIT / "capture-run" / "runlog.json"
REFERENCE_DAY = date(2026, 11, 24)
SAMPLE_OWNER = "Avery Chen"

# ContractLink is left out: it is an absolute URL to the demo site (the pages carry no absolute
# URLs and never read the column). NewRisk replaces Risk.
OBLIGATION_HEADERS = [
    "ID", "Title", "ContractName", "Counterparty", "ObligationText", "ClauseRef", "SourceClause",
    "Party", "Category", "TriggerType", "Recurrence", "DueDate", "TriggerEvent", "Owner",
    "EscalationOwner", "BusinessUnit", "Status", "Timing", "ReviewState", "Confidence", "Risk",
    "CaptureKey", "Notes", "IsSample",
]
CONTRACT_HEADERS = [
    "ID", "FileLeafRef", "Title", "Counterparty", "ContractType", "EffectiveDate", "ExpirationDate",
    "AutoRenews", "NoticePeriodDays", "GoverningLaw", "ContractValue", "ContractSummary",
    "ContractOwner", "BusinessUnit", "Amends", "IsSample",
]
RUNLOG_HEADERS = [
    "ID", "Title", "Workflow", "Outcome", "ContractName", "ContractVersion", "ItemsCreated",
    "ItemsUpdated", "ItemsHeld", "Details", "RunAt",
]
OWNER_HEADERS = ["ID", "Title", "Category", "BusinessUnit", "Counterparty", "Owner", "EscalationOwner", "Notify"]
OWNER_RULES = [  # ../seed/obligation-owners.demo.json
    ("Default - all obligations", "Any"),
    ("Finance - payments", "Payment"),
    ("Legal - notices and renewals", "Notice & renewal"),
]


def _txt(v):
    if v is None:
        return ""
    if v is True:
        return "Yes"
    if v is False:
        return "No"
    return str(v)


def _long(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def contract_summary(c, by_file):
    role = (c.get("northwindRole") or "").lower()
    eff = date.fromisoformat(c["effectiveDate"]) if c.get("effectiveDate") else None
    exp = date.fromisoformat(c["expirationDate"]) if c.get("expirationDate") else None
    if c.get("amends"):
        base = by_file.get(c["amends"], {})
        first = (f"Amends the {base.get('title', 'base agreement')} with {c['counterparty']}, "
                 f"effective {_long(eff)}.")
    else:
        first = f"{c['title']} between Northwind Traders and {c['counterparty']}, with Northwind as {role}."
    if exp:
        term = f"Runs to {_long(exp)}"
    elif eff:
        term = f"Effective from {_long(eff)} with no fixed end date"
    else:
        term = "No term dates recorded"
    if c.get("autoRenews") == "Yes" and c.get("noticePeriodDays"):
        term += f" and renews automatically unless notice is given {c['noticePeriodDays']} days before renewal"
    elif c.get("autoRenews") == "Yes":
        term += " and renews automatically"
    else:
        term += " and does not renew automatically"
    if c.get("governingLaw"):
        term += f"; governed by the law of {c['governingLaw']}."
    else:
        term += "."
    return f"{first} {term}"


def assigned(r):
    return r.get("ReviewState") == "Confirmed" and r.get("Status") != "Not applicable"


def build():
    loaded = json.loads(OBLIGATIONS_SRC.read_text(encoding="utf-8"))
    manifest = json.loads((SAMPLES / "contracts-manifest.json").read_text(encoding="utf-8"))
    captures = json.loads(RUNLOG_SRC.read_text(encoding="utf-8"))
    by_file = {c["fileName"]: c for c in manifest}

    obligations = []
    for i, r in enumerate(loaded, start=1):
        d = dict(r)
        d["ID"] = i
        d["Risk"] = r["NewRisk"]
        d["Owner"] = d["EscalationOwner"] = SAMPLE_OWNER if assigned(r) else ""
        obligations.append([_txt(d.get(h)) for h in OBLIGATION_HEADERS])

    contracts = []
    for i, c in enumerate(manifest, start=1):
        contracts.append([
            str(i), c["fileName"], c["title"], c["counterparty"], c["contractType"],
            _txt(c.get("effectiveDate")), _txt(c.get("expirationDate")), _txt(c.get("autoRenews")),
            _txt(c.get("noticePeriodDays")), _txt(c.get("governingLaw")), _txt(c.get("contractValue")),
            contract_summary(c, by_file), SAMPLE_OWNER, _txt(c.get("businessUnit")),
            _txt(c.get("amends")), "Yes",
        ])

    runlog = [[_txt(i if h == "ID" else r.get(h)) for h in RUNLOG_HEADERS] for i, r in enumerate(captures, start=1)]
    n_assigned = sum(1 for r in loaded if assigned(r))
    held = sum(1 for r in loaded if r.get("ReviewState") == "Needs review")
    timing = Counter(r.get("Timing") for r in loaded if r.get("Status") not in ("Fulfilled", "Waived", "Not applicable"))
    seed = [
        ("Assign owners - demo seed", "Assign owners", "0", str(n_assigned), str(held),
         f"Demo seed run following assign-obligation-owners. Assigned {n_assigned} confirmed items to {SAMPLE_OWNER} "
         f"using the routing rules. The {held} items held in Needs review get an owner once someone confirms them.",
         "2026-11-24T23:40:00Z"),
        ("Daily sweep - demo seed", "Daily sweep", "0", str(len(loaded)), "0",
         f"Demo seed run following sweep-obligations. Open: {timing['No date']} no date, {timing['Upcoming']} upcoming, "
         f"{timing['Due soon']} due soon, {timing['Overdue']} overdue. No reminders sent (seed run).",
         "2026-11-24T23:45:00Z"),
    ]
    for title, workflow, created, updated, held_n, details, at in seed:
        runlog.append([str(len(runlog) + 1), title, workflow, "Succeeded", "", "", created, updated, held_n, details, at])

    owners = [[str(i), title, category, "Any", "", SAMPLE_OWNER, SAMPLE_OWNER, "Both"]
              for i, (title, category) in enumerate(OWNER_RULES, start=1)]

    note = ("SAMPLE DATA - fictional companies, people and contracts from the Obligation Hub demo kit, "
            f"as loaded on the demo site. Dates are relative to {REFERENCE_DAY.isoformat()}. "
            "Shown only when live list data is unavailable.")
    return {
        "obligations": {"sample": True, "note": note, "headers": OBLIGATION_HEADERS, "rows": obligations},
        "contracts": {"sample": True, "note": note, "headers": CONTRACT_HEADERS, "rows": contracts},
        "runlog": {"sample": True, "note": note, "headers": RUNLOG_HEADERS, "rows": runlog},
        "owners": {"sample": True, "note": note, "headers": OWNER_HEADERS, "rows": owners},
    }


if __name__ == "__main__":
    snaps = build()
    for k, v in snaps.items():
        print(k, len(v["rows"]))
