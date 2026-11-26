import os, json, copy
from nw_data import *
from nw_pptx import *
from docx import Document
from docx.shared import Pt as DPt, RGBColor as DRGB, Inches as DIn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
SL = {s[0]: s for s in SLIDES}
def deck(path, title, files, customer_line=None, extra_note=None, mutate=None):
    prs = new_prs()
    for f in files:
        fn, role, t, prods, inds, share, verb, order, d = SL[f]
        d = copy.deepcopy(d)
        if mutate: t, d = mutate(role, t, d)
        RENDER[role](prs, t if role != "Title" else title, d, customer_line=customer_line)
    set_props(prs, title, "Pitch deck"); prs.save(path)

# ---------- DOCX ----------
def docx_file(path, title, kicker, sections, internal=False, footer=DISCLAIMER):
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Segoe UI"; st.font.size = DPt(10.5)
    for s in doc.sections: s.left_margin = s.right_margin = DIn(0.9)
    p = doc.add_paragraph(); r = p.add_run(kicker.upper() + ("   |   INTERNAL ONLY" if internal else "")); r.bold = True; r.font.size = DPt(9); r.font.color.rgb = DRGB.from_string(BRAND["coral"] if internal else BRAND["teal"])
    h = doc.add_paragraph(); r = h.add_run(title); r.bold = True; r.font.size = DPt(24); r.font.color.rgb = DRGB.from_string(BRAND["navy"])
    for head, body in sections:
        hp = doc.add_paragraph(); hr = hp.add_run(head); hr.bold = True; hr.font.size = DPt(13); hr.font.color.rgb = DRGB.from_string(BRAND["navy"])
        if isinstance(body, list) and body and isinstance(body[0], tuple):
            t = doc.add_table(rows=1, cols=len(body[0])); t.style = "Light Grid Accent 1"
            for i, c in enumerate(body[0]): t.rows[0].cells[i].text = c
            for row in body[1:]:
                cells = t.add_row().cells
                for i, c in enumerate(row): cells[i].text = c
        elif isinstance(body, list):
            for b in body: doc.add_paragraph(b, style="List Bullet")
        else: doc.add_paragraph(body)
    fp = doc.sections[0].footer.paragraphs[0]; fp.text = footer; fp.runs[0].font.size = DPt(8)
    doc.core_properties.title = title; doc.core_properties.author = "Northwind Cloud Sales Enablement"
    doc.save(path)

# ---------- PDF ----------
def pdf_file(path, title, kicker, blocks, stats=None, internal=False, footer=DISCLAIMER):
    c = canvas.Canvas(path, pagesize=letter); Wp, Hp = letter
    c.setTitle(title); c.setAuthor("Northwind Cloud Sales Enablement")
    c.setFillColor(HexColor("#" + BRAND["navy"])); c.rect(0, Hp - 150, Wp, 150, fill=1, stroke=0)
    c.setFillColor(HexColor("#" + BRAND["teal"])); c.roundRect(48, Hp - 62, 26, 26, 5, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold", 15); c.drawCentredString(61, Hp - 55, "N")
    c.setFont("Helvetica-Bold", 12); c.drawString(82, Hp - 54, "Northwind Cloud")
    c.setFillColor(HexColor("#" + (BRAND["coral"] if internal else "9FE3E2"))); c.setFont("Helvetica-Bold", 9); c.drawString(48, Hp - 88, (kicker + ("  |  INTERNAL ONLY" if internal else "")).upper())
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold", 22)
    for i, ln in enumerate(simpleSplit(title, "Helvetica-Bold", 22, Wp - 96)[:2]): c.drawString(48, Hp - 115 - i * 26, ln)
    y = Hp - 185
    if stats:
        w = (Wp - 96) / len(stats)
        for i, (a, b) in enumerate(stats):
            c.setFillColor(HexColor("#" + BRAND["teal"])); c.setFont("Helvetica-Bold", 28); c.drawString(48 + i * w, y, a)
            c.setFillColor(HexColor("#" + BRAND["ink"])); c.setFont("Helvetica", 10)
            for j, ln in enumerate(simpleSplit(b, "Helvetica", 10, w - 12)): c.drawString(48 + i * w, y - 18 - j * 12, ln)
        y -= 70
    for head, body in blocks:
        c.setFillColor(HexColor("#" + BRAND["navy"])); c.setFont("Helvetica-Bold", 13); c.drawString(48, y, head); y -= 18
        c.setFillColor(HexColor("#" + BRAND["ink"])); c.setFont("Helvetica", 10.5)
        items = body if isinstance(body, list) else [body]
        for it in items:
            pre = "\u2022 " if isinstance(body, list) else ""
            for ln in simpleSplit(pre + it, "Helvetica", 10.5, Wp - 96): c.drawString(48, y, ln); y -= 14
            y -= 3
        y -= 10
    c.setFillColor(HexColor("#" + BRAND["grey"])); c.setFont("Helvetica", 8); c.drawString(48, 30, footer)
    c.save()

os.makedirs("content/library", exist_ok=True); os.makedirs("content/archive", exist_ok=True); os.makedirs("content/intake", exist_ok=True); os.makedirs("content/generated", exist_ok=True)
L = "content/library/"
LIB = []  # metadata rows
def meta(fn, title, atype, sol, prods, aud, stage, inds, share, summary, pub, exp, pop, feat=False, notes=""):
    LIB.append(dict(file=fn, Title=title, AssetType=atype, Solution=sol, Products=prods, Audience=aud, SalesStage=stage, Industry=inds, Shareability=share, AISummary=summary, PublishedOn=pub, ExpiresOn=exp, Popularity=pop, Featured=feat, VersionNotes=notes))

deck(L + "Northwind Corporate Pitch FY27.pptx", "Northwind Cloud: from data to decisions", ["NW-Title-Corporate.pptx","NW-Agenda-Standard.pptx","NW-Problem-DataSilos.pptx","NW-Solution-DataPlatform.pptx","NW-Solution-AIStudio.pptx","NW-Proof-Platform.pptx","NW-Story-Wingtip.pptx","NW-NextSteps-90Day.pptx","NW-Close-ThankYou.pptx"], "Corporate overview  |  FY27")
meta("Northwind Corporate Pitch FY27.pptx","Northwind Corporate Pitch FY27","Pitch deck","Data & AI",["Northwind Data Platform","Northwind AI Studio","Northwind Analytics"],["Executive","Line of business"],"Discover",["Cross-industry"],"Customer-shareable (NDA)","The flagship first-meeting story: why data decisions stall and how Northwind fixes it. Use it to open any new account.","2026-10-01","2027-06-30",412,True,"FY27 refresh with new proof points.")
deck(L + "Healthcare AI Pitch - Clinician Time Back.pptx", "Better care, less admin: Northwind for Healthcare", ["NW-Title-Healthcare.pptx","NW-Agenda-Executive.pptx","NW-Problem-Healthcare.pptx","NW-Solution-AIStudio.pptx","NW-Proof-AI.pptx","NW-Story-Contoso.pptx","NW-NextSteps-Workshop.pptx","NW-Close-ThankYou.pptx"], "Healthcare briefing")
meta("Healthcare AI Pitch - Clinician Time Back.pptx","Healthcare AI Pitch: Clinician Time Back","Pitch deck","Data & AI",["Northwind AI Studio","Northwind Data Platform"],["Executive","Line of business"],"Discover",["Healthcare"],"Customer-shareable (NDA)","Shows hospital leaders how AI agents cut documentation time, with Contoso Health as proof. Use for CMIO and CNO conversations.","2026-09-15","2027-03-31",287,True)
deck(L + "Financial Services Zero Trust Pitch.pptx", "Secure, compliant growth: Northwind for Financial Services", ["NW-Title-FinServ.pptx","NW-Agenda-Standard.pptx","NW-Problem-FinServ.pptx","NW-Solution-SecureAccess.pptx","NW-Proof-Security.pptx","NW-Story-Woodgrove.pptx","NW-NextSteps-90Day.pptx","NW-Close-ThankYou.pptx"], "Financial services briefing")
meta("Financial Services Zero Trust Pitch.pptx","Financial Services Zero Trust Pitch","Pitch deck","Security",["Northwind Secure Access"],["IT decision maker","Executive"],"Qualify",["Financial services"],"Customer-shareable (NDA)","Makes the case for retiring VPNs in regulated banks, with Woodgrove Financial as proof. Use with CISOs and IT leaders.","2026-06-01","2026-12-15",198,False)
deck(L + "Field Service Executive Briefing.pptx", "The right technician, first time", ["NW-Title-Corporate.pptx","NW-Problem-FieldService.pptx","NW-Solution-FieldService.pptx","NW-Story-Tailspin.pptx","NW-Pricing-Packages.pptx","NW-NextSteps-90Day.pptx","NW-Close-ThankYou.pptx"], "Executive briefing  |  Manufacturing")
meta("Field Service Executive Briefing.pptx","Field Service Executive Briefing","Pitch deck","Business Applications",["Northwind Field Service"],["Executive","Line of business"],"Propose",["Manufacturing"],"Customer-shareable (NDA)","A short executive story on predictive field service and first-time fix, with Tailspin as proof. Use with service and operations leaders.","2026-08-20","2027-05-31",143)
deck(L + "Data Platform Technical Deep Dive.pptx", "Northwind Data Platform: technical deep dive", ["NW-Title-Corporate.pptx","NW-Agenda-Standard.pptx","NW-Problem-DataSilos.pptx","NW-Solution-DataPlatform.pptx","NW-Solution-Analytics.pptx","NW-Solution-AIStudio.pptx","NW-Proof-Platform.pptx","NW-NextSteps-Workshop.pptx","NW-Close-ThankYou.pptx"], "For architects and data engineers")
meta("Data Platform Technical Deep Dive.pptx","Data Platform Technical Deep Dive","Pitch deck","Data & AI",["Northwind Data Platform","Northwind Analytics","Northwind AI Studio"],["Technical practitioner","IT decision maker"],"Qualify",["Cross-industry"],"Customer-shareable (NDA)","Walks architects through connect, govern and serve, then proposes a design workshop. Use after the first meeting lands.","2026-07-10","2027-04-30",121)

docx_file(L + "Battlecard - Data Platform vs Legacy Warehouses.docx","Battlecard: Data Platform vs legacy warehouses","Battlecard",[
 ("When you'll meet this","The customer runs an on-premises warehouse and is weighing a lift-and-shift."),
 ("How we win",["One governed lakehouse instead of copies in five systems","Pay for what you query, not for idle capacity","AI-ready: agents read the same governed data"]),
 ("Landmines to lay",["Ask how many copies of the customer table they maintain","Ask how long a new data source takes to onboard","Ask who approves access today and how long it takes"]),
 ("Objections",[("They say","We say"),("Migration is risky","Run side by side; move one domain at a time with our migration factory"),("We already paid for licenses","Keep them for the long tail; move new workloads first")]),
 ("Be factual","Never disparage a competitor. Compare capabilities, not companies.")], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Battlecard - Data Platform vs Legacy Warehouses.docx","Battlecard: Data Platform vs legacy warehouses","Battlecard","Data & AI",["Northwind Data Platform"],["Technical practitioner","IT decision maker"],"Qualify",["Cross-industry"],"Internal only","How to win against an incumbent on-premises warehouse: landmines, objections and proof. Internal only.","2026-10-12","2027-04-12",356,True)
docx_file(L + "Battlecard - Secure Access vs VPN.docx","Battlecard: Secure Access vs legacy VPN","Battlecard",[
 ("When you'll meet this","The customer's VPN renewal is coming up or they've had a credential-based incident."),
 ("How we win",["Per-app access cuts lateral movement","Phishing-resistant sign-in by default","Retire VPN hardware and its maintenance"]),
 ("Discovery questions",["How many apps sit behind the VPN?","What happened in your last phishing test?","What do auditors ask you to prove today?"]),
 ("Objections",[("They say","We say"),("Users will hate it","Woodgrove saw fewer sign-in prompts, not more"),("We just renewed","Start with contractors and high-risk apps")])], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Battlecard - Secure Access vs VPN.docx","Battlecard: Secure Access vs legacy VPN","Battlecard","Security",["Northwind Secure Access"],["IT decision maker"],"Qualify",["Cross-industry","Financial services"],"Internal only","Talk track and objection handling for replacing a legacy VPN with zero-trust access. Internal only.","2026-09-02","2027-03-02",241)

for p, fn, inds, share, pop, exp in [("Northwind AI Studio","One-pager - Northwind AI Studio.pdf",["Cross-industry"],"Public",310,"2027-05-31"),("Northwind Field Service","One-pager - Northwind Field Service.pdf",["Manufacturing"],"Public",98,"2027-02-28")]:
    info = PRODUCTS[p]
    pdf_file(L + fn, f"{p}: {info['tag']}", "Product one-pager", [("What it does", [a + ": " + b for a, b in info["caps"]]), ("Why customers choose it", ["Live in weeks, not quarters","Built on the governed Northwind Data Platform","Backed by a named success manager"]), ("Next step", "Ask your Northwind account team for a 90-day pilot plan.")])
    meta(fn, f"One-pager: {p}", "One-pager", info["sol"], [p], ["Executive","Line of business"], "Discover", inds, share, f"A one-page overview of {p}: what it does, why customers choose it and the next step. Safe to leave behind.", "2026-09-01", exp, pop)
pdf_file(L + "One-pager - Northwind Analytics for Retail.pdf","Northwind Analytics for Retail: answers for every store","Industry one-pager",[("The challenge","Store managers wait days for reports and miss the moment."),("What changes",["Ask questions in plain language over certified data","Forecast demand by store and category","Share live dashboards in the tools teams already use"]),("Proof","Wingtip Retail moved 1,200 store managers to self-service and cut report requests by 40%. Source: Wingtip Retail case study, 2026."),("Next step","A two-week pilot with five stores.")], stats=[("1,200","store managers on self-service"),("-40%","report requests"),("+3.1%","basket size in pilot")])
meta("One-pager - Northwind Analytics for Retail.pdf","One-pager: Northwind Analytics for Retail","One-pager","Data & AI",["Northwind Analytics"],["Line of business","Executive"],"Discover",["Retail"],"Customer-shareable (NDA)","Retail leave-behind on self-service analytics for store managers, with Wingtip Retail results.","2026-10-20","2027-04-20",76)
for c, fn, exp, pop, feat in [("Contoso Health","Customer Story - Contoso Health.pdf","2027-08-31",265,True),("Tailspin Manufacturing","Customer Story - Tailspin Manufacturing.pdf","2027-06-30",134,False),("Woodgrove Financial","Customer Story - Woodgrove Financial.pdf","2026-12-10",159,False)]:
    i = CUSTOMERS[c]
    pdf_file(L + fn, f"{c}: {i['quote']}", f"Customer story | {i['ind']}", [("The challenge", f"{c} needed to move faster without adding risk."), ("The solution", f"{i['prod']} rolled out in phases, starting with one high-value team."), ("In their words", "\u201C" + i["quote"] + "\u201D  " + i["who"]), ("Reference status", "Reference approved. Request reference calls through the customer reference program.")], stats=i["outcomes"])
    meta(fn, f"Customer story: {c}", "Customer story", PRODUCTS[i['prod']]['sol'], [i["prod"]], ["Executive","Line of business"], "Propose", [i["ind"]], "Public", f"How {c} got results with {i['prod']}: {i['outcomes'][0][0]} {i['outcomes'][0][1]}. Reference approved.", "2026-07-01", exp, pop, feat)
docx_file(L + "Demo Script - AI Studio Clinical Summary Agent.docx","Demo script: clinical summary agent","Demo script",[("Setup (5 min before)",["Sign in to the demo tenant as the clinician persona","Open the Contoso Health sample patient","Clear the agent's chat history"]),("Click path",[("Step","Say","Show"),("1","Here's the discharge summary a nurse writes by hand today","Blank summary form"),("2","Watch the agent draft it from the chart","Agent draft with citations"),("3","Every line links back to its source","Click a citation")]),("If something breaks","Switch to the recorded backup in the demo kit.")], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Demo Script - AI Studio Clinical Summary Agent.docx","Demo script: clinical summary agent","Demo script","Data & AI",["Northwind AI Studio"],["Technical practitioner"],"Qualify",["Healthcare"],"Internal only","Seven-minute click path for the AI Studio clinical summary demo, with a backup plan.","2026-10-05","2027-04-05",88)
docx_file(L + "Demo Script - Analytics Ask Your Data.docx","Demo script: ask your data","Demo script",[("Story","A store manager asks why sales dipped last week, in plain language."),("Click path",[("Step","Say","Show"),("1","Ask: why did sales drop in store 12?","Answer with drivers"),("2","Drill into the weather driver","Forecast vs actual"),("3","Share it to the store team","Live dashboard in chat")])], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Demo Script - Analytics Ask Your Data.docx","Demo script: ask your data","Demo script","Data & AI",["Northwind Analytics"],["Technical practitioner","Line of business"],"Qualify",["Retail","Cross-industry"],"Internal only","Five-minute natural-language analytics demo for retail and general audiences.","2026-09-18","2027-03-18",64)
pdf_file(L + "Pricing and Packaging Guide FY27.pdf","Pricing and packaging guide FY27","Pricing guide",[("Packages",["Starter: one team, up to 50 users","Business: one business unit, up to 1,000 users","Enterprise: unlimited users, private networking"]),("Discount guidance",["Up to 10%: seller","10-20%: sales manager via deal desk","Over 20%: regional VP with business case"]),("Rules","Never send this guide to a customer. Quote through the deal desk.")], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Pricing and Packaging Guide FY27.pdf","Pricing and packaging guide FY27","Pricing guide","Data & AI",["Northwind Data Platform","Northwind AI Studio","Northwind Secure Access","Northwind Field Service","Northwind Analytics"],["Executive"],"Negotiate",["Cross-industry"],"Internal only","FY27 packages and discount approval levels. Internal only; quote through the deal desk.","2026-07-01","2027-06-30",377,True)
docx_file(L + "Playbook - Land with Data Platform.docx","Playbook: land with Data Platform, expand with AI","Playbook",[("Who to target",["CIOs and CDOs with a warehouse renewal in the next 12 months","Companies hiring data engineers faster than they can onboard them"]),("Motion",[("Stage","Goal","Asset"),("Discover","Find the data pain","Corporate Pitch FY27"),("Qualify","Prove technical fit","Technical Deep Dive"),("Propose","Agree a pilot","Pilot SOW template")]),("Expand","After the pilot, introduce AI Studio on the same governed data.")], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
meta("Playbook - Land with Data Platform.docx","Playbook: land with Data Platform, expand with AI","Playbook","Data & AI",["Northwind Data Platform","Northwind AI Studio"],["Executive","IT decision maker"],"Discover",["Cross-industry"],"Internal only","The land-and-expand motion: who to target, which asset to use at each stage, and how to expand into AI.","2026-08-01","2027-02-01",201)
docx_file(L + "Proposal Template - Northwind Pilot SOW.docx","Statement of work: Northwind 90-day pilot","Proposal template",[("Customer","[Customer name]"),("Objectives",["[Objective 1]","[Objective 2]"]),("Scope",[("Phase","Weeks","Deliverable"),("Discovery","1-2","Use-case brief"),("Pilot","3-8","One use case live"),("Scale plan","9-12","Business case and roadmap")]),("Commercials","Pilot fee per the current price list. Quote through the deal desk.")])
meta("Proposal Template - Northwind Pilot SOW.docx","Proposal template: 90-day pilot SOW","Proposal template","Data & AI",["Northwind Data Platform","Northwind AI Studio","Northwind Analytics"],["Executive","Line of business"],"Propose",["Cross-industry"],"Customer-shareable (NDA)","A fill-in statement of work for a 90-day pilot. Fill the bracketed fields before sending.","2026-09-10","2027-03-10",115)

# ---------- Archive ----------
ARCH = []
prs = new_prs(); r_title(prs, "Northwind DataHub overview", {"sub": "2025 edition"}); r_problem(prs, "Data is everywhere", SL["NW-Problem-DataSilos.pptx"][8]); prs.save("content/archive/Northwind DataHub Overview 2025.pptx")
ARCH.append(dict(file="Northwind DataHub Overview 2025.pptx", Title="Northwind DataHub overview 2025", AssetType="Pitch deck", Solution="Data & AI", Products=["Northwind Data Platform"], Shareability="Customer-shareable (NDA)", ArchivedOn="2026-10-01", ArchiveReason="Replaced", ReplacedBy="Northwind Corporate Pitch FY27.pptx", AISummary="Retired overview that uses the old DataHub product name."))
pdf_file("content/archive/Pricing Guide FY26.pdf","Pricing guide FY26","Pricing guide",[("Status","Expired. Use the FY27 guide.")], internal=True)
ARCH.append(dict(file="Pricing Guide FY26.pdf", Title="Pricing guide FY26", AssetType="Pricing guide", Solution="Data & AI", Products=[], Shareability="Internal only", ArchivedOn="2026-07-01", ArchiveReason="Expired", ReplacedBy="Pricing and Packaging Guide FY27.pdf", AISummary="Last year's pricing guide. Expired."))

# ---------- Intake submissions (deliberate issues for the validator) ----------
INTAKE = []
def bad_ai(role, t, d):
    if role == "Proof": d = dict(d); d["source"] = ""; d["stats"] = [("3x","faster store analytics with Northwind Insights"),("50%","lower cost than competitors"),("#1","platform retailers trust")]
    if role == "Title": t = "Northwind Insights + AI Studio for Retail"
    return t, d
deck("content/intake/AI Studio for Retail - pitch v3.pptx", "Northwind Insights + AI Studio for Retail", ["NW-Title-Corporate.pptx","NW-Problem-DataSilos.pptx","NW-Solution-AIStudio.pptx","NW-Proof-Platform.pptx","NW-NextSteps-90Day.pptx"], "Retail briefing", mutate=bad_ai)
INTAKE.append(dict(file="AI Studio for Retail - pitch v3.pptx", Title="AI Studio for Retail pitch v3", Shareability="Customer-shareable (NDA)", ReviewStatus="Needs fixes", SubmissionNotes="New retail pitch for the holiday push. Please publish by Dec 5.", ProposedExpiry="2027-06-30", expect="Fixable: retired name Northwind Insights, unsourced claims, disparaging '50% lower cost than competitors'"))
docx_file("content/intake/Battlecard - Field Service vs Spreadsheets.docx","Battlecard: Field Service vs spreadsheets and whiteboards","Battlecard",[("When you'll meet this","Dispatchers schedule from spreadsheets and phone calls."),("How we win",["AI scheduling balances skills, parts and travel","Technicians get guided repair on mobile","Managers see first-time fix by region"]),("Proof","Tailspin Manufacturing reached an 89% first-time fix rate. Source: Tailspin customer story, 2026. Reference approved.")], internal=True, footer="Northwind Cloud internal. Do not share with customers.")
INTAKE.append(dict(file="Battlecard - Field Service vs Spreadsheets.docx", Title="Battlecard: Field Service vs spreadsheets", Shareability="Internal only", ReviewStatus="Awaiting approval", SubmissionNotes="Internal battlecard for dispatch-heavy accounts.", ProposedExpiry="2027-05-31", expect="Pass"))
docx_file("content/intake/Fabrikam Bank win story.docx","How we won Fabrikam Bank","Customer story",[("Summary","Fabrikam Bank chose Secure Access over two competitors. We closed at a 27% discount approved by the RVP."),("Contacts","Champion: Jordan Lee, mobile 425-555-0143, jordan.lee.home@example.com"),("Results",["VPN retired in 5 months","Fewer help-desk tickets"])])
INTAKE.append(dict(file="Fabrikam Bank win story.docx", Title="Fabrikam Bank win story", Shareability="Public", ReviewStatus="Needs fixes", SubmissionNotes="Great win, let's make it a public story!", ProposedExpiry="2027-06-30", expect="Blocked: named customer without reference approval, internal discount, personal data"))
pdf_file("content/intake/Field Service ROI one-pager.pdf","Field Service ROI: what first-time fix is worth","One-pager",[("The math",["Each avoided repeat visit saves travel, labor and goodwill","Customers report fewer truck rolls in year one"]),("Proof","Tailspin Manufacturing cut truck rolls by 22%. Source: Tailspin customer story, 2026. Reference approved."),("Next step","Run the ROI calculator with your account team.")], stats=[("-22%","truck rolls"),("89%","first-time fix")])
INTAKE.append(dict(file="Field Service ROI one-pager.pdf", Title="Field Service ROI one-pager", Shareability="Customer-shareable (NDA)", ReviewStatus="Submitted", SubmissionNotes="Leave-behind for manufacturing execs.", ProposedExpiry="2027-06-30", expect="Pass or minor Fixable"))

# ---------- Generated deck example ----------
deck("content/generated/Contoso Health - Executive briefing - 2026-12-03.pptx", "Contoso Health: giving clinicians time back", ["NW-Title-Healthcare.pptx","NW-Agenda-Executive.pptx","NW-Problem-Healthcare.pptx","NW-Solution-AIStudio.pptx","NW-Proof-AI.pptx","NW-Story-Contoso.pptx","NW-Pricing-Packages.pptx","NW-NextSteps-Workshop.pptx","NW-Close-ThankYou.pptx"], "Executive briefing  |  December 3, 2026")
# Industry one-pager template (Word)
docx_file("content/templates/Template-IndustryOnePager.docx","[Headline for {Customer}]","Industry one-pager | {Industry}",[("The challenge","{Challenge}"),("How Northwind helps","{Solution}"),("Proof","{Proof point with source}"),("Customer story","{Reference-approved customer}"),("Next step","{Next step}")])
json.dump(dict(library=LIB, archive=ARCH, intake=INTAKE), open("content/meta.json", "w"), indent=1)
for d in ["library","archive","intake","generated","templates","slides"]:
    fs = os.listdir("content/" + d); print(d, len(fs), sum(os.path.getsize(f"content/{d}/{f}") for f in fs)//1024, "KB")
