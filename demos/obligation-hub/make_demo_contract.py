#!/usr/bin/env python3
"""Builds the beat-3 contract and the beat-4 evidence prop for the Obligation Hub demo, then verifies them.

Writes, next to this script:
  12-Relecloud-Order-Form.docx      the new contract Zach drops into the Contracts library on camera
  Northwind-COI-Contoso-2026.docx   the certificate he gives as evidence when he marks the Contoso COI fulfilled
  expected-obligations.md           what capture should produce from the contract, plus this script's checks

Every company, person, address and number is fictional. Reference "today" is 2026-11-24 (Pacific).
Run: python make_demo_contract.py   (needs python-docx). Exits non-zero if any check fails.
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
CONTRACT_FILE = "12-Relecloud-Order-Form.docx"
EVIDENCE_FILE = "Northwind-COI-Contoso-2026.docx"
EXPECTED_FILE = "expected-obligations.md"

TODAY = date(2026, 11, 24)
ORDER_DATE = date(2026, 11, 16)
START_DATE = date(2026, 12, 1)
PILOT_END = date(2027, 4, 30)
NOTICE_DAYS = 60
PILOT_FEE = 36_000
ANNUAL_FEE = 96_000
PILOT_FEE_DUE = date(2026, 12, 31)
FIRST_QUARTER_END = date(2026, 12, 31)
REPORT_DAYS = 15
VEHICLES = 60

NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x59, 0x59, 0x59)
FONT = "Calibri"


def fd(d):
    return f"{d:%B} {d.day}, {d.year}"


def money(n):
    return f"${n:,}"


# ---------------------------------------------------------------------------
# Contract text. Each operative sentence is a constant so the expected rows below
# quote exactly what the document says; verify() re-reads the .docx to prove it.
# ---------------------------------------------------------------------------
S_SERVICE = (f"Relecloud will provide Customer with access to the Service for up to the Vehicle Allowance "
             f"during the Pilot Term and each Renewal Term.")
S_SERVICE_DEF = ('"Connected Vehicle" means a Customer vehicle with a Relecloud telematics device that '
                 'reports to the Service.')
S_RENEWAL = ("At the end of the Pilot Term, this Order Form renews automatically for successive twelve (12)-month "
             "Renewal Terms at the Annual Subscription Fee unless either party gives the other written notice of "
             "non-renewal at least sixty (60) days before the end of the then-current term.")
S_PILOT_FEE = f"Customer shall pay the Pilot Fee on or before {fd(PILOT_FEE_DUE)}."
S_RATE_CARD = ("Customer shall pay the fees for each Renewal Term, and the fees for any Connected Vehicles above the "
               "Vehicle Allowance, on the invoicing and payment terms set out in the Relecloud Rate Card, which is "
               "incorporated into this Order Form by reference.")
S_INVOICES = "Relecloud will send all invoices by email to ap@northwind.example."
S_REPORT = (f"Within fifteen (15) days after the end of each calendar quarter, commencing with the quarter ending "
            f"{fd(FIRST_QUARTER_END)}, Customer shall send Relecloud a fleet report listing the vehicles added to or "
            f"retired from its fleet during that quarter.")
S_CONTACTS = "Each party will name a project contact for the Pilot Term and keep that contact's details current."
S_INCIDENT = ("Relecloud shall notify Customer in writing within seventy-two (72) hours after becoming aware of any "
              "Security Incident.")
S_INCIDENT_DEF = ('"Security Incident" means any unauthorized access to, or disclosure of, vehicle, route or driver '
                  'data that Customer uploads to the Service.')
S_SUPPORT = "Relecloud will provide email support from 7:00 a.m. to 6:00 p.m. Pacific time on business days."
S_ENTIRE = ("This Order Form is the entire agreement between the parties for the Service and supersedes all prior "
            "proposals.")
S_LAW = "This Order Form is governed by the laws of the State of Washington."
S_COUNTERPARTS = "This Order Form may be signed in counterparts and by electronic signature."

INTRO = ('This Order Form (this "Order Form") is entered into as of ' + fd(ORDER_DATE) + ' (the "Order Date") by and '
         'between Relecloud, Inc., a Delaware corporation with its principal place of business at 350 Skyline Drive, '
         'Kirkland, Washington 98033 ("Relecloud"), and Northwind Traders, Inc., a Washington corporation with its '
         'principal place of business at 4100 Harbor View Drive, Seattle, Washington 98121 ("Customer"). Capitalized '
         'terms in the order summary below have the meanings shown there.')

SUMMARY = [
    ("Service", "Relecloud Fleet Insights: route optimization and vehicle telematics dashboard (the \"Service\")"),
    ("Start Date", fd(START_DATE)),
    ("Pilot Term", f"{fd(START_DATE)} through {fd(PILOT_END)} (the \"Pilot Term\")"),
    ("Vehicle Allowance", f"Up to {VEHICLES} Connected Vehicles (the \"Vehicle Allowance\")"),
    ("Pilot Fee", f"{money(PILOT_FEE)}, one time (the \"Pilot Fee\")"),
    ("Annual Subscription Fee", f"{money(ANNUAL_FEE)} for each Renewal Term (the \"Annual Subscription Fee\")"),
]

ARTICLES = [
    ("1. Service and Term", [
        ("1.1", "Service", f"{S_SERVICE} {S_SERVICE_DEF}"),
        ("1.2", "Renewal", S_RENEWAL),
    ]),
    ("2. Fees and Payment", [
        ("2.1", "Pilot Fee", S_PILOT_FEE),
        ("2.2", "Renewal and Overage Fees", S_RATE_CARD),
        ("2.3", "Invoices", S_INVOICES),
    ]),
    ("3. Customer Responsibilities", [
        ("3.1", "Quarterly Fleet Report", S_REPORT),
        ("3.2", "Project Contacts", S_CONTACTS),
    ]),
    ("4. Customer Data and Support", [
        ("4.1", "Security Incidents", f"{S_INCIDENT} {S_INCIDENT_DEF}"),
        ("4.2", "Support", S_SUPPORT),
    ]),
    ("5. General", [
        ("5.1", "Entire Agreement", S_ENTIRE),
        ("5.2", "Governing Law", S_LAW),
        ("5.3", "Counterparts", S_COUNTERPARTS),
    ]),
]

SIGNATURES = [
    ("RELECLOUD, INC.", "NORTHWIND TRADERS, INC."),
    ("By: /s/ Jordan Ellis", "By: /s/ Maria Delgado"),
    ("Name: Jordan Ellis", "Name: Maria Delgado"),
    ("Title: Vice President, Sales", "Title: Chief Operating Officer"),
    (f"Date: {fd(date(2026, 11, 13))}", f"Date: {fd(ORDER_DATE)}"),
]

# ---------------------------------------------------------------------------
# What capture-obligations should do with it (v1.0 rules: risk by consequence,
# missing-document hold, routine-admin exclusions).
# ---------------------------------------------------------------------------
NOTICE_DEADLINE = PILOT_END - timedelta(days=NOTICE_DAYS)
REPORT_DUE = FIRST_QUARTER_END + timedelta(days=REPORT_DAYS)

EXPECTED = [
    dict(expected="track", title="Send non-renewal notice to Relecloud (60 days)", party="Both",
         category="Notice & renewal", trigger="Recurring", recurrence="Annual", due=NOTICE_DEADLINE, risk="High",
         confidence="High", review="Confirmed", clause="Section 1.2", source=S_RENEWAL,
         notes=f"Pilot Term ends {PILOT_END}; {NOTICE_DAYS} days before = {NOTICE_DEADLINE}. Miss it and the pilot "
               f"renews as a 12-month term at {money(ANNUAL_FEE)}. Fixed date is an acceptable TriggerType."),
    dict(expected="track", title="Pay Relecloud pilot fee by December 31, 2026", party="Us", category="Payment",
         trigger="Fixed date", recurrence="None", due=PILOT_FEE_DUE, risk="Medium", confidence="High",
         review="Confirmed", clause="Section 2.1", source=S_PILOT_FEE,
         notes=f"ObligationText should carry the {money(PILOT_FEE)} amount from the order summary."),
    dict(expected="track", title="Send Relecloud quarterly fleet report (15 days)", party="Us", category="Reporting",
         trigger="Recurring", recurrence="Quarterly", due=REPORT_DUE, risk="Medium", confidence="High",
         review="Confirmed", clause="Section 3.1", source=S_REPORT,
         notes=f"First report covers the quarter ending {FIRST_QUARTER_END}; due {REPORT_DUE}."),
    dict(expected="track", title="Relecloud: notify security incident within 72 hours", party="Counterparty",
         category="Data & confidentiality", trigger="Event-driven", recurrence="None", due=None, risk="High",
         confidence="High", review="Confirmed", clause="Section 4.1", source=S_INCIDENT,
         notes="TriggerEvent: Relecloud becomes aware of a Security Incident. Breach notices are High under v1.0."),
    dict(expected="hold", title="Pay Relecloud renewal and overage fees per Rate Card", party="Us",
         category="Payment", trigger="Event-driven", recurrence="None", due=None, risk="Medium", confidence="Low",
         review="Needs review", clause="Section 2.2", source=S_RATE_CARD,
         notes="Missing document: Notes = \"Terms in Relecloud Rate Card, which isn't in the Contracts library - add it "
               "or confirm the terms\". Ongoing is an acceptable TriggerType."),
]

NOT_CREATED = [
    ("Section 1.1", S_SERVICE, "Service description (routine service delivery)"),
    ("Section 2.3", S_INVOICES, "Invoicing logistics"),
    ("Section 3.2", S_CONTACTS, "Points of contact"),
    ("Section 4.2", S_SUPPORT, "Support hours"),
    ("Section 5.1", S_ENTIRE, "Boilerplate: entire agreement"),
    ("Section 5.2", S_LAW, "Boilerplate: governing law"),
    ("Section 5.3", S_COUNTERPARTS, "Boilerplate: counterparts and e-signature"),
]

MANIFEST_ENTRY = {
    "fileName": CONTRACT_FILE, "title": "Order Form - Relecloud Fleet Insights", "counterparty": "Relecloud, Inc.",
    "northwindRole": "Customer", "contractType": "Supplier agreement", "effectiveDate": ORDER_DATE.isoformat(),
    "expirationDate": PILOT_END.isoformat(), "autoRenews": "Yes", "noticePeriodDays": NOTICE_DAYS,
    "governingLaw": "Washington, USA", "contractValue": PILOT_FEE, "businessUnit": "Procurement", "amends": None,
}


# ---------------------------------------------------------------------------
# Document helpers (same look as the eleven sample contracts: Calibri, navy headings)
# ---------------------------------------------------------------------------
def _font(f, size=None, bold=None, color=None):
    f.name = FONT
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if color is not None:
        f.color.rgb = color


def _rfonts(style):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FONT)


def _shade(cell, fill):
    pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pr.append(shd)


def new_doc(header, footer, title_meta, subject):
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for m in ("left_margin", "right_margin"):
        setattr(sec, m, Inches(0.9))
    sec.top_margin = sec.bottom_margin = Inches(0.6)
    sec.header_distance = sec.footer_distance = Inches(0.3)
    normal = d.styles["Normal"]
    _font(normal.font, 9.5)
    _rfonts(normal)
    normal.paragraph_format.space_after = Pt(3)
    normal.paragraph_format.line_spacing = 1.0
    t = d.styles["Title"]
    _font(t.font, 18, True, NAVY)
    _rfonts(t)
    t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.space_after = Pt(2)
    h = d.styles["Heading 1"]
    _font(h.font, 10.5, True, NAVY)
    _rfonts(h)
    h.paragraph_format.space_before = Pt(6)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run(header)
    r.font.size, r.font.color.rgb = Pt(8), GREY
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(footer)
    r.font.size, r.font.color.rgb = Pt(8), GREY
    cp = d.core_properties
    cp.title, cp.author, cp.subject = title_meta, "Northwind Traders, Inc. (sample data)", subject
    return d


def para(d, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=None, color=None, after=None):
    p = d.add_paragraph()
    p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    if size:
        r.font.size = Pt(size)
    if color is not None:
        r.font.color.rgb = color
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def clause(d, num, caption, text):
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(f"{num} {caption}.").bold = True
    p.add_run(" " + text)


def kv_table(d, rows, widths=(1.9, 4.8), head=None):
    t = d.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    if head:
        cells = t.add_row().cells
        for c, txt in zip(cells, head):
            c.text = ""
            run = c.paragraphs[0].add_run(txt)
            run.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            _shade(c, "1F3864")
    for k, v in rows:
        cells = t.add_row().cells
        cells[0].text, cells[1].text = "", ""
        cells[0].paragraphs[0].add_run(k).bold = True
        _shade(cells[0], "EEF2F8")
        cells[1].paragraphs[0].add_run(v)
    t.autofit = False
    for col, w in zip(t.columns, widths):
        col.width = Inches(w)
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = Inches(w)
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(0)
    return t


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------
def build_contract(path):
    d = new_doc("Relecloud, Inc.  |  Order Form RC-2026-0412", "Order No. RC-2026-0412",
                "Order Form - Relecloud Fleet Insights", "Sample contract for obligation-management demo (fictional)")
    d.add_paragraph("Order Form", style="Title")
    para(d, "Relecloud Fleet Insights  |  Order No. RC-2026-0412", WD_ALIGN_PARAGRAPH.CENTER, size=9.5, color=GREY,
         after=8)
    para(d, INTRO)
    d.add_paragraph("Order Summary", style="Heading 1")
    kv_table(d, SUMMARY)
    for heading, clauses in ARTICLES:
        d.add_paragraph(heading, style="Heading 1")
        for num, cap, text in clauses:
            clause(d, num, cap, text)
    para(d, "Each party has signed this Order Form by its authorized representative as of the Order Date.", after=6)
    t = d.add_table(rows=0, cols=2)
    for left, right in SIGNATURES:
        cells = t.add_row().cells
        cells[0].text, cells[1].text = left, right
        if left.isupper():
            for c in cells:
                for r in c.paragraphs[0].runs:
                    r.bold = True
    d.save(path)


def build_evidence(path):
    d = new_doc("Humongous Insurance Brokerage  |  Certificate No. HIB-26-11873",
                "Sample document for the Obligation Hub demo. Fictional; not a real certificate of insurance.",
                "Certificate of Insurance - Northwind Traders for Contoso Ltd",
                "Evidence prop for the Obligation Hub demo (fictional)")
    d.add_paragraph("Certificate of Insurance", style="Title")
    para(d, f"Issued {fd(TODAY)}  |  Certificate No. HIB-26-11873", WD_ALIGN_PARAGRAPH.CENTER, size=9.5, color=GREY,
         after=10)
    kv_table(d, [
        ("Producer", "Humongous Insurance Brokerage, 1800 Pine Street, Seattle, Washington 98101"),
        ("Insured", "Northwind Traders, Inc., 4100 Harbor View Drive, Seattle, Washington 98121"),
        ("Certificate holder", "Contoso Ltd, 1 Contoso Plaza, Redmond, Washington 98052"),
        ("Regarding", "Master Services Agreement No. NW-MSA-2024-0117, Section 7.1 (Coverage and Certificates)"),
    ])
    d.add_paragraph("Coverage", style="Heading 1")
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for c, txt in zip(t.rows[0].cells, ("Type of insurance", "Policy number", "Policy period", "Limits")):
        c.text = ""
        run = c.paragraphs[0].add_run(txt)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _shade(c, "1F3864")
    for row in [
        ("Commercial general liability", "CGL-48213-26", "December 15, 2026 to December 15, 2027",
         "$2,000,000 each occurrence; $4,000,000 general aggregate"),
        ("Technology errors and omissions", "TEO-77140-26", "December 15, 2026 to December 15, 2027",
         "$5,000,000 each claim"),
    ]:
        cells = t.add_row().cells
        for c, txt in zip(cells, row):
            c.text = txt
    para(d, "This certificate summarizes the policies listed above as of the issue date. It does not amend, extend "
            "or alter the coverage those policies provide.", size=9, color=GREY)
    para(d, "Authorized representative: /s/ Riley Chen, Humongous Insurance Brokerage", WD_ALIGN_PARAGRAPH.LEFT)
    d.save(path)


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def doc_text(path):
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.extend(c.text for c in row.cells)
    return parts


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def word_count(parts):
    return sum(1 for p in parts for tok in p.split() if re.search(r"[A-Za-z0-9]", tok))


def verify(contract_path, evidence_path):
    lines, ok = [], True

    def check(cond, msg):
        nonlocal ok
        ok = ok and bool(cond)
        lines.append(f"{'PASS' if cond else 'FAIL'}  {msg}")

    parts = doc_text(contract_path)
    body = norm(" ".join(parts))
    for row in EXPECTED:
        check(norm(row["source"]) in body, f"{row['clause']} source sentence is verbatim in {CONTRACT_FILE} "
                                           f"({row['expected']}: {row['title']})")
    for ref, sentence, _ in NOT_CREATED:
        check(norm(sentence) in body, f"{ref} excluded sentence is verbatim in {CONTRACT_FILE}")
    check(NOTICE_DEADLINE == date(2027, 3, 1), f"Non-renewal deadline: {PILOT_END} minus {NOTICE_DAYS} days = "
                                               f"{NOTICE_DEADLINE}")
    check(REPORT_DUE == date(2027, 1, 15), f"First fleet report: {FIRST_QUARTER_END} plus {REPORT_DAYS} days = "
                                           f"{REPORT_DUE}")
    check((NOTICE_DEADLINE - TODAY).days <= 120, f"Non-renewal deadline is {(NOTICE_DEADLINE - TODAY).days} days "
                                                 f"from {TODAY}: inside the 120-day Copilot question")
    check((NOTICE_DEADLINE - TODAY).days <= 180, "Non-renewal deadline falls inside the Home page's 180-day "
                                                 "Notice windows timeline")
    check(all(r["due"] is None or (r["due"] - TODAY).days > 14 for r in EXPECTED),
          "No new item falls due within 14 days, so the Home hero stays at 10 and Due in 14 days stays at 6")
    check(sum(r["expected"] == "hold" for r in EXPECTED) == 1, "Exactly one item is expected to be held for review")
    check(sum(r["risk"] == "High" for r in EXPECTED) == 2, "Two expected items are High risk (Leadership: 13 -> 15)")
    check(money(PILOT_FEE) in body and money(ANNUAL_FEE) in body, "Pilot Fee and Annual Subscription Fee amounts "
                                                                   "appear in the order summary")
    check("Relecloud Rate Card" in body and "Rate Card" not in " ".join(
        p.stem for p in (HERE.parent.parent / "solutions").rglob("*.docx")), "The Relecloud Rate Card is referenced "
                                                                             "and no Rate Card file ships with the kit")
    w = word_count(parts)
    check(350 <= w <= 650, f"Contract is about one page: {w} words (capture fingerprint W, headers and footers "
                           f"excluded)")
    ev = norm(" ".join(doc_text(evidence_path)))
    check("$2,000,000 each occurrence" in ev and "$5,000,000 each claim" in ev,
          f"{EVIDENCE_FILE} shows the limits Contoso MSA Section 7.1 requires ($2M CGL, $5M tech E&O)")
    check("Contoso Ltd" in ev and "NW-MSA-2024-0117" in ev, f"{EVIDENCE_FILE} names Contoso as certificate holder "
                                                             f"and cites the MSA number")
    return ok, lines, w


# ---------------------------------------------------------------------------
# expected-obligations.md
# ---------------------------------------------------------------------------
def write_expected(path, lines, words):
    def due(r):
        return f"{r['due']} (in {(r['due'] - TODAY).days} days)" if r["due"] else "-"

    out = [
        "# Expected obligations: 12-Relecloud-Order-Form.docx",
        "",
        "> Generated by `make_demo_contract.py`. Edit the script, not this file. All companies, people and numbers "
        "are fictional. Reference date: **2026-11-24** (Pacific).",
        "",
        "The contract Zach drops into the Contracts library in beat 3. It is a one-page order form: Northwind buys a "
        "five-month pilot of Relecloud Fleet Insights that **renews automatically** into a "
        f"{money(ANNUAL_FEE)}-a-year subscription unless someone gives **60 days' notice**. "
        "It also has a quarterly report, a one-time pilot fee, a security-incident notice Relecloud owes Northwind, "
        "and one payment clause whose terms live in a document Northwind doesn't have (the Relecloud Rate Card).",
        "",
        "## Expected capture result",
        "",
        "Run Log: `Capture - 12-Relecloud-Order-Form.docx`, Outcome **Succeeded**, ItemsCreated **5**, "
        "ItemsUpdated **0**, ItemsHeld **1**. A second Capture row with Outcome Skipped (\"content unchanged\") is "
        "normal: the file-changed workflow fires after the upload.",
        "",
        "| # | Expected | Title (wording may vary) | Party | Category | Trigger | Recurrence | Due | Risk | "
        "Confidence | Review | Clause | Source sentence (verbatim) | Notes |",
        "|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(EXPECTED, 1):
        out.append(f"| {i} | {r['expected']} | {r['title']} | {r['party']} | {r['category']} | {r['trigger']} | "
                   f"{r['recurrence']} | {due(r)} | {r['risk']} | {r['confidence']} | {r['review']} | {r['clause']} | "
                   f"{r['source']} | {r['notes']} |")
    out += [
        "",
        "## Should not be created",
        "",
        "| Clause | Sentence (verbatim) | Why |",
        "|---|---|---|",
    ]
    out += [f"| {ref} | {s} | {why} |" for ref, s, why in NOT_CREATED]
    out += [
        "",
        "## What changes on the hub after capture (recording on 2026-11-24 to 2026-11-29)",
        "",
        "| Where | Before | After |",
        "|---|---|---|",
        "| Home hero | 10 need attention; 58 open across 10 contracts | 10 need attention; 63 open across 11 contracts |",
        "| Home tiles | Overdue 4, Due in 14 days 6, Needs an owner 3, Needs review 3 | Overdue 4, Due in 14 days 6, "
        "Needs an owner 8, Needs review 4 |",
        f"| Notice windows timeline | 6 notice deadlines | adds Relecloud - non-renewal notice, {fd(NOTICE_DEADLINE)} |",
        "| Review page (nav badge) | 3 | 4: the Section 2.2 Rate Card item, Confidence Low |",
        "| Badge | Live - 60 obligations | Live - 65 obligations |",
        "",
        "New items have no owner until Assign owners runs (daily, 7:00 AM). Held items are never assigned until "
        "someone confirms them.",
        "",
        "## What must match on camera, and what may vary",
        "",
        "- **Must match:** five new items; exactly one held for review with the Rate Card reason; the non-renewal "
        f"item dated {NOTICE_DEADLINE}; the source sentence quoted word for word.",
        "- **May vary:** titles and ObligationText wording; Recurring vs Fixed date on the non-renewal item; "
        "Reporting vs Compliance & audit on the fleet report; Event-driven vs Ongoing on the held item. If the dry "
        "run differs on a must-match point, re-run after the reset prompt in demo-script.md section 3, or change "
        "the talk-track line to what the screen shows.",
        "",
        "## Optional Contracts columns",
        "",
        "Autofill may not fill the key-term columns on the test tenant, and capture doesn't need them. If you "
        "fill them by hand after the demo, use these values (same shape as `contracts-manifest.json`). Don't edit "
        "them before or during the take: any column edit fires the file-changed workflow.",
        "",
        "```json",
        "{",
    ]
    items = list(MANIFEST_ENTRY.items())
    for i, (k, v) in enumerate(items):
        val = "null" if v is None else (str(v) if isinstance(v, int) else f'"{v}"')
        out.append(f'  "{k}": {val}' + ("," if i < len(items) - 1 else ""))
    out += [
        "}",
        "```",
        "",
        "## Verification (output of `python make_demo_contract.py`)",
        "",
        "```text",
        *lines,
        "```",
        "",
    ]
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    contract = HERE / CONTRACT_FILE
    evidence = HERE / EVIDENCE_FILE
    build_contract(contract)
    build_evidence(evidence)
    ok, lines, words = verify(contract, evidence)
    write_expected(HERE / EXPECTED_FILE, lines, words)
    print("\n".join(lines))
    print(f"\nWrote {CONTRACT_FILE}, {EVIDENCE_FILE}, {EXPECTED_FILE}")
    print("ALL CHECKS PASSED" if ok else "CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
