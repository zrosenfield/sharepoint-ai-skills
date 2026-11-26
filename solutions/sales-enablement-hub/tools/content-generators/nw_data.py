# Northwind Cloud fictional sample data
BRAND = dict(navy="0B1F3A", teal="00A3A1", coral="FF6B4A", sky="E8F4F8", ink="1F2A37", grey="6B7785", light="F4F7FB", gold="F5B400")
DISCLAIMER = "Northwind Cloud confidential. Subject to change."
PRODUCTS = {
 "Northwind Data Platform": dict(sol="Data & AI", tag="One governed home for all your data", caps=[("Connect","300+ connectors bring every source into one lakehouse"),("Govern","Lineage, quality and access policies in one place"),("Serve","Fresh, trusted data for every app, report and agent")]),
 "Northwind AI Studio": dict(sol="Data & AI", tag="Build and run AI agents on your own data", caps=[("Ground","Agents answer from your governed data, with citations"),("Orchestrate","Multi-step workflows with human approval built in"),("Evaluate","Quality, safety and cost dashboards for every agent")]),
 "Northwind Secure Access": dict(sol="Security", tag="Zero-trust access for every app and device", caps=[("Verify","Phishing-resistant sign-in and device health checks"),("Segment","Per-app access instead of flat network VPNs"),("Detect","Risky sessions flagged and contained in minutes")]),
 "Northwind Field Service": dict(sol="Business Applications", tag="The right technician, first time, every time", caps=[("Predict","IoT signals open work orders before failures"),("Schedule","AI scheduling balances skills, parts and travel"),("Resolve","Guided repair and remote expert video on mobile")]),
 "Northwind Analytics": dict(sol="Data & AI", tag="Answers for every team, without a ticket", caps=[("Ask","Natural-language questions over certified data"),("Forecast","Built-in forecasting with explainable drivers"),("Share","Live dashboards embedded where people work")]),
}
CUSTOMERS = {
 "Contoso Health": dict(ind="Healthcare", prod="Northwind AI Studio", quote="Our clinicians got two hours a week back, and our patients noticed.", who="Dr. Maya Patel, Chief Medical Information Officer", outcomes=[("2 hrs","saved per clinician each week"),("31%","faster discharge summaries"),("4.7/5","clinician satisfaction")], ref=True),
 "Tailspin Manufacturing": dict(ind="Manufacturing", prod="Northwind Field Service", quote="First-time fix went from a goal to a habit.", who="Luis Ortega, VP Service Operations", outcomes=[("89%","first-time fix rate"),("-22%","truck rolls"),("6 wks","to go live")], ref=True),
 "Woodgrove Financial": dict(ind="Financial services", prod="Northwind Secure Access", quote="We retired our VPN in one quarter without a single outage.", who="Priya Nair, CISO", outcomes=[("100%","apps behind zero trust"),("-64%","risky sign-ins"),("1 qtr","VPN retired")], ref=True),
 "Wingtip Retail": dict(ind="Retail", prod="Northwind Analytics", quote="Store managers stopped waiting for reports and started asking questions.", who="Hannah Kim, Chief Data Officer", outcomes=[("1,200","store managers on self-service"),("-40%","report requests"),("+3.1%","basket size in pilot")], ref=True),
}
# Slide Library: (file, role, title, products, industries, shareability, verbatim, order, data)
SLIDES = [
 ("NW-Title-Corporate.pptx","Title","Northwind Cloud: from data to decisions",[],["Cross-industry"],"Public",False,1,dict(sub="Corporate overview")),
 ("NW-Title-Healthcare.pptx","Title","Better care, less admin: Northwind for Healthcare",["Northwind AI Studio","Northwind Data Platform"],["Healthcare"],"Customer-shareable (NDA)",False,1,dict(sub="Healthcare briefing")),
 ("NW-Title-FinServ.pptx","Title","Secure, compliant growth: Northwind for Financial Services",["Northwind Secure Access","Northwind Analytics"],["Financial services"],"Customer-shareable (NDA)",False,1,dict(sub="Financial services briefing")),
 ("NW-Agenda-Standard.pptx","Agenda","Today's agenda",[],["Cross-industry"],"Public",False,2,dict(items=["Your priorities","What we're seeing in the market","How Northwind helps","Proof from customers like you","Next steps"])),
 ("NW-Agenda-Executive.pptx","Agenda","What we'll cover in 30 minutes",[],["Cross-industry"],"Public",False,2,dict(items=["Your 2027 goals","Three moves that matter","Proof","A 90-day plan"])),
 ("NW-Problem-DataSilos.pptx","Problem","Decisions are waiting on data",["Northwind Data Platform","Northwind Analytics"],["Cross-industry"],"Customer-shareable (NDA)",False,3,dict(lead="Most teams still stitch reports by hand.",pains=[("Silos","Data lives in dozens of disconnected systems"),("Trust","No one agrees which number is right"),("Speed","New questions take weeks to answer")])),
 ("NW-Problem-Healthcare.pptx","Problem","Clinicians spend their evenings on paperwork",["Northwind AI Studio"],["Healthcare"],"Customer-shareable (NDA)",False,3,dict(lead="Documentation burden is the top driver of burnout.",pains=[("Admin load","Notes, summaries and coding after every visit"),("Fragmented records","Context spread across EHR, labs and imaging"),("Staffing","Fewer people asked to see more patients")])),
 ("NW-Problem-FinServ.pptx","Problem","Every app is now a front door for attackers",["Northwind Secure Access"],["Financial services"],"Customer-shareable (NDA)",False,3,dict(lead="Flat VPN access turns one stolen password into a breach.",pains=[("Credentials","Phishing still beats passwords and SMS codes"),("Sprawl","Hundreds of SaaS and legacy apps to protect"),("Regulation","Auditors now expect zero-trust evidence")])),
 ("NW-Problem-FieldService.pptx","Problem","Every repeat visit costs margin and loyalty",["Northwind Field Service"],["Manufacturing"],"Customer-shareable (NDA)",False,3,dict(lead="Unplanned downtime is the most expensive hour in manufacturing.",pains=[("Reactive","Work orders open only after something breaks"),("Mismatch","The wrong skills or parts arrive on site"),("Knowledge","Expert know-how retires with your best techs")])),
]
for p,info in PRODUCTS.items():
    short=p.replace("Northwind ","").replace(" ","")
    SLIDES.append((f"NW-Solution-{short}.pptx","Solution",f"{p}: {info['tag'].lower()}",[p],["Cross-industry"],"Customer-shareable (NDA)",False,4,dict(product=p)))
SLIDES += [
 ("NW-Proof-Platform.pptx","Proof","Results customers report in year one",["Northwind Data Platform","Northwind Analytics"],["Cross-industry"],"Customer-shareable (NDA)",True,5,dict(stats=[("38%","faster month-end close"),("4.2x","more questions answered"),("-35%","data engineering backlog")],source="Source: Northwind customer benchmark 2026, n=42 customers, median values.")),
 ("NW-Proof-AI.pptx","Proof","AI that pays for itself",["Northwind AI Studio"],["Cross-industry"],"Customer-shareable (NDA)",True,5,dict(stats=[("6 mo","median payback"),("71%","of agent answers used without edits"),("0","ungoverned data sources")],source="Source: Northwind AI Studio early adopter study, Sept 2026, n=18.")),
 ("NW-Proof-Security.pptx","Proof","Zero trust, measured",["Northwind Secure Access"],["Cross-industry","Financial services"],"Customer-shareable (NDA)",True,5,dict(stats=[("-64%","risky sign-ins"),("12 min","median containment"),("98%","phishing-resistant sign-ins")],source="Source: Northwind Secure Access telemetry, Q3 2026, opted-in tenants.")),
]
for c,info in CUSTOMERS.items():
    SLIDES.append((f"NW-Story-{c.split()[0]}.pptx","Customer story",f"{c}: {info['outcomes'][0][0]} {info['outcomes'][0][1]}",[info['prod']],[info['ind']],"Customer-shareable (NDA)",True,6,dict(customer=c)))
SLIDES += [
 ("NW-Pricing-Packages.pptx","Pricing","Simple packages that grow with you",[],["Cross-industry"],"Customer-shareable (NDA)",True,7,dict(tiers=[("Starter","For one team","Up to 50 users, 2 products, standard support"),("Business","For a business unit","Up to 1,000 users, all products, 24x7 support"),("Enterprise","For the whole company","Unlimited users, private networking, named success manager")])),
 ("NW-Pricing-InternalDiscounts.pptx","Pricing","INTERNAL ONLY: discount guidance FY27",[],["Cross-industry"],"Internal only",True,7,dict(tiers=[("Up to 10%","Seller","No approval needed"),("10-20%","Sales manager","Approve in the deal desk"),("Over 20%","Regional VP","Business case required")],internal=True)),
 ("NW-NextSteps-90Day.pptx","Next steps","A 90-day path to value",[],["Cross-industry"],"Public",False,8,dict(steps=[("Weeks 1-2","Discovery workshop","Map goals, data and quick wins"),("Weeks 3-8","Pilot","One use case live with your team"),("Weeks 9-12","Scale plan","Business case and rollout roadmap")])),
 ("NW-NextSteps-Workshop.pptx","Next steps","Let's run a design workshop",[],["Cross-industry"],"Public",False,8,dict(steps=[("Day 1","Envision","Prioritize three use cases"),("Day 2","Design","Architecture and success measures"),("Day 3","Plan","Pilot scope, owners and dates")])),
 ("NW-Close-ThankYou.pptx","Close","Thank you",[],["Cross-industry"],"Public",False,9,dict()),
]
TEMPLATES = [
 ("Template-FirstMeetingPitch.pptx","First meeting pitch","PowerPoint","Title, Agenda, Problem, Solution, Proof, Customer story, Next steps, Close",["Line of business","IT decision maker"],8,"A first conversation with a new account: their problem, our answer, proof, and a clear next step."),
 ("Template-ExecutiveBriefing.pptx","Executive briefing","PowerPoint","Title, Agenda, Problem, Solution, Proof, Customer story, Pricing, Next steps, Close",["Executive"],9,"30 minutes with a C-level sponsor. Outcome-led, few words per slide, detail in the notes."),
 ("Template-TechnicalDeepDive.pptx","Technical deep dive","PowerPoint","Title, Agenda, Problem, Solution, Solution, Solution, Proof, Next steps, Close",["Technical practitioner","IT decision maker"],9,"Architects and engineers: capabilities product by product, then a pilot plan."),
 ("Template-QBR.pptx","Quarterly business review","PowerPoint","Title, Agenda, Proof, Customer story, Solution, Next steps, Close",["Executive","Line of business"],7,"Existing customers: results so far, what's next, and expansion."),
 ("Template-IndustryOnePager.docx","Industry one-pager","Word","Headline, Challenge, Solution, Proof, Customer story, Next step",["Executive","Line of business"],1,"A one-page leave-behind tailored to one industry."),
]
