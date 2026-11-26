"""Contracts 01-05."""
from lib import Doc, date, fd, iso, ob, relativedelta, timedelta

NW_ADDR = "4100 Harbor View Drive, Seattle, Washington 98121"

# ---------------------------------------------------------------- 01 / 02 Contoso
C_EFF = date(2024, 4, 1)
C_INIT_END = date(2026, 3, 31)
C_CUR_END = date(2027, 3, 31)
C_NEXT_RENEWAL_START = C_CUR_END + timedelta(days=1)
C_AMD = date(2026, 9, 1)
Q4_END = date(2026, 12, 31)

S_C_PAY = ("Service Provider shall invoice Customer monthly in arrears. Customer shall pay each "
           "undisputed invoice within forty-five (45) days after receipt.")
S_C_AVAIL = ("Service Provider shall ensure that the Service Portal achieves Availability of at least "
             "99.5% in each calendar month.")
S_C_CREDIT = ("If Availability in any calendar month falls below 99.5%, Service Provider shall issue Customer "
              "a service credit equal to five percent (5%) of the monthly Fees for each full percentage point "
              "(or portion of a percentage point) by which Availability falls below 99.5%, up to a maximum of "
              "twenty-five percent (25%) of the monthly Fees, applied against the next invoice.")
S_C_REPORT15 = ("Service Provider shall deliver to Customer a written service-level report for each calendar "
                "quarter, showing Availability, incident counts and service credits issued, within fifteen (15) "
                "days after the end of such calendar quarter.")
S_C_REPORT10 = ("Service Provider shall deliver to Customer a written service-level report for each calendar "
                "quarter, showing Availability, incident counts and service credits issued, within ten (10) "
                "days after the end of such calendar quarter.")
S_C_CONF = ("Each Party shall hold the other Party's Confidential Information in confidence, use it only to "
            "perform or receive the Services, and disclose it only to its employees and contractors who need to "
            "know it and are bound by written confidentiality obligations at least as protective as this Article 5.")
S_C_AUDIT = ("Upon not less than thirty (30) days' prior written notice, Customer or its independent auditor may "
             "audit Service Provider's records relating to the Services and the Fees, no more than once in any "
             "twelve (12) month period. Service Provider shall cooperate with any such audit and provide reasonable "
             "access to relevant records, systems and personnel during normal business hours.")
S_C_INS = ("During the Term, Service Provider shall maintain commercial general liability insurance with limits of "
           "not less than $2,000,000 per occurrence and technology errors and omissions insurance with limits of "
           "not less than $5,000,000 per claim. Service Provider shall deliver to Customer a certificate of "
           "insurance evidencing the coverage required by this Section 7.1 on or before December 15 of each "
           "calendar year during the Term.")
S_C_NR90 = ("Either Party may elect not to renew this Agreement by giving the other Party written notice of "
            "non-renewal at least ninety (90) days before the end of the then-current Term.")
S_C_NR120 = ("Either Party may elect not to renew this Agreement by giving the other Party written notice of "
             "non-renewal at least one hundred twenty (120) days before the end of the then-current Term.")
S_C_FEE = ("For each Renewal Term beginning on or after April 1, 2027, Service Provider may increase the Fees by "
           "up to four percent (4%) over the Fees in effect for the preceding Term, provided that Service Provider "
           "gives Customer written notice of the increase at least sixty (60) days before the start of that "
           "Renewal Term.")
S_C_BCP = ("Within sixty (60) days after the Amendment Effective Date, Service Provider shall deliver to Customer an "
           "updated business continuity and disaster recovery plan for the Services, including recovery time and "
           "recovery point objectives for the Service Portal.")


def c01(path):
    f = "01-Contoso-MSA.docx"
    cp = "Contoso Ltd"
    notice90 = C_CUR_END - timedelta(days=90)
    report15 = Q4_END + timedelta(days=15)
    ins_next = date(2026, 12, 15)

    d = Doc("Contoso Ltd  |  Master Services Agreement  |  Confidential", "NW-MSA-2024-0117", "Master Services Agreement - Contoso Ltd")
    d.title("Master Services Agreement", "Agreement No. NW-MSA-2024-0117")
    d.para(f'This Master Services Agreement (this "Agreement") is entered into as of {fd(C_EFF)} (the "Effective Date") '
           f'by and between Northwind Traders, Inc., a Washington corporation with its principal place of business at '
           f'{NW_ADDR} ("Service Provider"), and Contoso Ltd, a Delaware corporation with its principal place of '
           f'business at 1 Contoso Plaza, Redmond, Washington 98052 ("Customer"). Service Provider and Customer are '
           f'each referred to as a "Party" and together as the "Parties."')
    d.recitals([
        "Service Provider provides managed order-fulfillment, inventory analytics and supply-chain support services to commercial customers.",
        "Customer wishes to engage Service Provider to provide such services to Customer's retail and wholesale operations under one or more Statements of Work.",
        "The Parties wish to set out the terms that will govern all Statements of Work entered into under this Agreement.",
    ])
    d.para("NOW, THEREFORE, in consideration of the mutual covenants set out below, the Parties agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Availability" means the percentage of minutes in a calendar month during which the Service Portal is accessible to Customer\'s authorized users, excluding Scheduled Maintenance.')
    d.section("1.2", None, '"Confidential Information" means any non-public business, technical or financial information disclosed by one Party (the "Discloser") to the other Party (the "Recipient") that is marked as confidential or that a reasonable person would understand to be confidential given the nature of the information and the circumstances of disclosure.')
    d.section("1.3", None, '"Scheduled Maintenance" means maintenance of the Service Portal performed between 10:00 p.m. and 4:00 a.m. Pacific Time on Saturdays, or at another time agreed in writing by the Parties.')
    d.section("1.4", None, '"Service Portal" means Service Provider\'s hosted web portal through which Customer submits orders, views inventory positions and receives reports.')
    d.section("1.5", None, '"Statement of Work" or "SOW" means a document that references this Agreement, describes Services, deliverables and fees, and is signed by both Parties. "Services" means the managed services described in each SOW.')

    d.heading("2. Services")
    d.section("2.1", "Statements of Work", "Service Provider will perform the Services described in each SOW in accordance with this Agreement. If there is a conflict between this Agreement and an SOW, this Agreement controls unless the SOW expressly identifies the provision of this Agreement that it overrides.")
    d.section("2.2", "Personnel", "Service Provider is solely responsible for the selection, supervision and compensation of its personnel and subcontractors, and remains responsible for their performance.")
    d.section("2.3", "Change Requests", "Either Party may request changes to the scope of an SOW. No change is binding unless it is documented in a written change order signed by both Parties.")

    d.heading("3. Fees and Payment")
    d.section("3.1", "Fees", 'Customer will pay the fees set out in each SOW (the "Fees"). The Fees under SOW No. 1 are $45,000 per month, or $540,000 per year.')
    d.section("3.2", "Invoicing and Payment", S_C_PAY + " Amounts are stated and payable in U.S. dollars.")
    d.section("3.3", "Taxes", "Fees exclude sales, use, value-added and similar taxes, which are Customer's responsibility, other than taxes based on Service Provider's net income.")

    d.heading("4. Service Levels and Reporting")
    d.section("4.1", "Availability Commitment", S_C_AVAIL)
    d.section("4.2", "Service Credits", S_C_CREDIT + " Service credits are Customer's sole and exclusive monetary remedy for a failure to meet the Availability commitment.")
    d.section("4.3", "Service-Level Reports", S_C_REPORT15)

    d.heading("5. Confidentiality")
    d.section("5.1", "Protection", S_C_CONF)
    d.section("5.2", "Exclusions", "Confidential Information does not include information that (a) is or becomes publicly available through no fault of the Recipient, (b) was known to the Recipient before disclosure without restriction, (c) is independently developed by the Recipient without use of the Discloser's Confidential Information, or (d) is rightfully received from a third party without a duty of confidentiality.")
    d.section("5.3", "Duration", "The obligations in this Article 5 continue during the Term and for three (3) years after its expiration or termination.")

    d.heading("6. Audit")
    d.section("6.1", "Audit Right", S_C_AUDIT)
    d.section("6.2", "Audit Costs", "Customer bears the cost of any audit it conducts. Audits must be conducted in a manner that does not unreasonably interfere with Service Provider's operations.")

    d.heading("7. Insurance")
    d.section("7.1", "Coverage and Certificates", S_C_INS)
    d.section("7.2", "No Limitation", "The insurance requirements in this Article 7 do not limit Service Provider's liability under this Agreement.")

    d.heading("8. Limitation of Liability")
    d.section("8.1", "Exclusion of Certain Damages", "EXCEPT FOR A PARTY'S BREACH OF ARTICLE 5, NEITHER PARTY WILL BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES, OR FOR LOST PROFITS OR REVENUE, ARISING OUT OF THIS AGREEMENT.")
    d.section("8.2", "Cap", "EXCEPT FOR A PARTY'S BREACH OF ARTICLE 5, EACH PARTY'S AGGREGATE LIABILITY ARISING OUT OF THIS AGREEMENT WILL NOT EXCEED THE FEES PAID OR PAYABLE UNDER THIS AGREEMENT IN THE TWELVE (12) MONTHS BEFORE THE EVENT GIVING RISE TO THE CLAIM.")

    d.heading("9. Term and Termination")
    d.section("9.1", "Term", f'This Agreement begins on the Effective Date and continues for an initial term ending {fd(C_INIT_END)} (the "Initial Term"). Thereafter, this Agreement automatically renews for successive renewal terms of one (1) year each (each, a "Renewal Term" and, together with the Initial Term, the "Term"), unless either Party gives notice of non-renewal under Section 9.2.')
    d.section("9.2", "Non-Renewal", S_C_NR90)
    d.section("9.3", "Termination for Cause", "Either Party may terminate this Agreement by written notice if the other Party materially breaches this Agreement and does not cure the breach within thirty (30) days after receiving written notice describing it.")
    d.section("9.4", "Survival", "Articles 3, 5, 6 and 8 and this Section 9.4 survive any expiration or termination of this Agreement.")

    d.heading("10. General Provisions")
    d.section("10.1", "Governing Law", "This Agreement is governed by the laws of the State of Washington, without regard to its conflict-of-laws rules. The state and federal courts located in King County, Washington have exclusive jurisdiction over any dispute arising out of this Agreement.")
    d.section("10.2", "Notices", "Notices under this Agreement must be in writing and delivered by courier or certified mail to the addresses set out above, with a copy by email to legal@northwind.example (for Service Provider) or contracts@contoso.example (for Customer). Notices are effective on receipt.")
    d.section("10.3", "Independent Contractors", "The Parties are independent contractors. Nothing in this Agreement creates a partnership, joint venture or agency relationship between them.")
    d.section("10.4", "Entire Agreement; Amendment", "This Agreement, together with all SOWs, is the entire agreement between the Parties regarding its subject matter and supersedes all prior agreements and understandings. This Agreement may be amended only by a written instrument signed by both Parties.")
    d.section("10.5", "Severability; Waiver", "If any provision of this Agreement is held unenforceable, the remaining provisions remain in effect. A waiver of any breach is not a waiver of any other breach.")

    d.signatures([
        {"company": "Northwind Traders, Inc.", "name": "Maria Delgado", "title": "Chief Operating Officer", "date": date(2024, 3, 27)},
        {"company": "Contoso Ltd", "name": "Elena Vasquez", "title": "Vice President, Global Procurement", "date": date(2024, 3, 28)},
    ])
    d.save(path / f)

    obs = [
        ob(f, cp, "Meet 99.5% monthly Service Portal availability",
           "Keep the Contoso Service Portal available at least 99.5% of each calendar month (excluding Scheduled Maintenance).",
           "Section 4.1", S_C_AVAIL, "Northwind", "Service levels", "Ongoing", risk="Medium"),
        ob(f, cp, "Issue Contoso service credits for missed availability",
           "If monthly Availability falls below 99.5%, credit Contoso 5% of monthly Fees per point (or part) below target, capped at 25%, on the next invoice.",
           "Section 4.2", S_C_CREDIT, "Northwind", "Service levels", "Event-driven",
           triggerEvent="Monthly Availability falls below 99.5% in a calendar month", risk="Medium"),
        ob(f, cp, "Maintain insurance; send Contoso COI by Dec 15",
           "Maintain $2M CGL and $5M tech E&O insurance during the Term and deliver a certificate of insurance to Contoso by December 15 every year.",
           "Section 7.1", S_C_INS, "Northwind", "Insurance", "Recurring", "Annual", ins_next, risk="Medium"),
        ob(f, cp, "Protect Contoso confidential information",
           "Each party must keep the other's Confidential Information confidential, use it only for the Services and share it only on a need-to-know basis (survives 3 years after the Term).",
           "Section 5.1", S_C_CONF, "Both", "Data & confidentiality", "Ongoing", risk="Medium"),
        ob(f, cp, "Cooperate with Contoso audit (30 days' notice)",
           "When Contoso gives at least 30 days' written audit notice (max once per 12 months), cooperate and give reasonable access to records, systems and personnel.",
           "Section 6.1", S_C_AUDIT, "Northwind", "Compliance & audit", "Event-driven",
           triggerEvent="Contoso gives at least 30 days' written notice of an audit (no more than once per 12 months)",
           risk="Medium", isTrap=True, trapType="counterparty-vs-us"),
        ob(f, cp, "Contoso to pay invoices within 45 days",
           "Northwind invoices monthly in arrears; Contoso must pay each undisputed invoice within 45 days after receipt.",
           "Section 3.2", S_C_PAY, "Counterparty", "Payment", "Event-driven",
           triggerEvent="Contoso receives a monthly Northwind invoice", risk="Medium"),
        ob(f, cp, "Send non-renewal notice to Contoso (90 days)",
           "Original MSA term: give written non-renewal notice at least 90 days before the current term ends (would have been 2026-12-31).",
           "Section 9.2", S_C_NR90, "Both", "Notice & renewal", "Recurring", "Annual", notice90, risk="High",
           expected="superseded", reason="Amended by Amendment No. 1 Section 2: notice period is now 120 days (deadline 2026-12-01). Do not track the 90-day version.",
           isTrap=True, trapType="amendment"),
        ob(f, cp, "Deliver quarterly service-level report (15 days)",
           "Original MSA term: quarterly service-level report due 15 days after quarter end (would have been 2027-01-15 for Q4 2026).",
           "Section 4.3", S_C_REPORT15, "Northwind", "Reporting", "Recurring", "Quarterly", report15, risk="Medium",
           expected="superseded", reason="Amended by Amendment No. 1 Section 3: report now due within 10 days after quarter end. Do not track the 15-day version.",
           isTrap=True, trapType="amendment"),
    ]
    man = dict(fileName=f, title="Master Services Agreement", counterparty=cp, northwindRole="Supplier",
               contractType="Customer agreement", effectiveDate=iso(C_EFF), expirationDate=iso(C_CUR_END),
               autoRenews="Yes", noticePeriodDays=90, governingLaw="Washington, USA", contractValue=540000,
               businessUnit="Sales", amends=None)
    return obs, man


def c02(path):
    f = "02-Contoso-MSA-Amendment-1.docx"
    cp = "Contoso Ltd"
    notice120 = C_CUR_END - timedelta(days=120)
    report10 = Q4_END + timedelta(days=10)
    fee_notice = C_NEXT_RENEWAL_START - timedelta(days=60)
    bcp = C_AMD + timedelta(days=60)

    d = Doc("Contoso Ltd  |  Amendment No. 1 to Master Services Agreement  |  Confidential", "NW-MSA-2024-0117-A1", "Amendment No. 1 to Master Services Agreement - Contoso Ltd")
    d.title("Amendment No. 1 to Master Services Agreement", "Agreement No. NW-MSA-2024-0117  |  Amendment No. 1")
    d.para(f'This Amendment No. 1 (this "Amendment") is entered into as of {fd(C_AMD)} (the "Amendment Effective Date") by and '
           f'between Northwind Traders, Inc., a Washington corporation with its principal place of business at {NW_ADDR} '
           f'("Service Provider"), and Contoso Ltd, a Delaware corporation with its principal place of business at 1 Contoso '
           f'Plaza, Redmond, Washington 98052 ("Customer"), and amends the Master Services Agreement between the Parties dated '
           f'as of {fd(C_EFF)} (Agreement No. NW-MSA-2024-0117) (the "Agreement").')
    d.recitals([
        f"The Initial Term of the Agreement ended on {fd(C_INIT_END)}, and the Agreement automatically renewed for a Renewal Term that began on April 1, 2026 and ends on {fd(C_CUR_END)}.",
        "Customer has requested additional lead time for renewal planning and more timely quarterly service-level reporting, and Service Provider has requested a mechanism for annual adjustment of the Fees.",
        "Following the regional network outage review completed by the Parties in July 2026, Customer has also requested an updated business continuity and disaster recovery plan for the Services.",
        "The Parties wish to amend the Agreement as set out in this Amendment.",
    ])
    d.para("NOW, THEREFORE, in consideration of the mutual covenants set out below, the Parties agree as follows:")

    d.heading("1. Definitions")
    d.para('Capitalized terms used but not defined in this Amendment have the meanings given to them in the Agreement. References in this Amendment to "Sections" are to sections of the Agreement unless otherwise stated.')

    d.heading("2. Amendment to Section 9.2 (Non-Renewal)")
    d.para("Section 9.2 of the Agreement is deleted in its entirety and replaced with the following:")
    d.para(f'"9.2 Non-Renewal. {S_C_NR120}"', indent=0.5, italic=False)
    d.para(f"For clarity, for the Renewal Term ending {fd(C_CUR_END)}, notice of non-renewal must be given on or before {fd(notice120)}. If neither Party gives timely notice, the Agreement will renew for a further Renewal Term of one (1) year under Section 9.1.")

    d.heading("3. Amendment to Section 4.3 (Service-Level Reports)")
    d.para("Section 4.3 of the Agreement is deleted in its entirety and replaced with the following:")
    d.para(f'"4.3 Service-Level Reports. {S_C_REPORT10}"', indent=0.5)
    d.para("The amended deadline applies beginning with the report for the calendar quarter ending September 30, 2026. The content and format of each report remain as agreed by the Parties' service managers.")

    d.heading("4. New Section 3.4 (Fee Adjustment)")
    d.para("The following new Section 3.4 is added to the Agreement immediately after Section 3.3:")
    d.para(f'"3.4 Fee Adjustment. {S_C_FEE}"', indent=0.5)
    d.para("An illustrative calculation of the maximum adjusted Fees under SOW No. 1 is set out in Exhibit A to this Amendment. Exhibit A is provided for convenience only, and Section 3.4 controls if there is any inconsistency.")

    d.heading("5. Business Continuity Plan")
    d.para(S_C_BCP + " The plan will be treated as Service Provider's Confidential Information under Article 5 of the Agreement.")

    d.heading("6. Effect of Amendment")
    d.para('Except as expressly modified by this Amendment, the Agreement remains unchanged and in full force and effect. If there is any conflict between this Amendment and the Agreement, this Amendment controls. From the Amendment Effective Date, each reference in the Agreement to "this Agreement" means the Agreement as amended by this Amendment.')

    d.heading("7. Authority")
    d.para("Each Party represents that the individual signing this Amendment on its behalf has been duly authorized to do so and that this Amendment is a binding obligation of that Party.")

    d.heading("8. Governing Law; Counterparts")
    d.para("This Amendment is governed by the law specified in Section 10.1 of the Agreement. This Amendment may be executed in counterparts, including by electronic signature, each of which is an original and all of which together are one instrument.")

    d.heading("9. Entire Agreement")
    d.para("The Agreement, as amended by this Amendment, together with all SOWs, is the entire agreement between the Parties regarding its subject matter. No other modification of the Agreement is intended or implied by this Amendment, and no course of dealing between the Parties modifies the Agreement.")

    d.signatures([
        {"company": "Northwind Traders, Inc.", "name": "Maria Delgado", "title": "Chief Operating Officer", "date": date(2026, 8, 28)},
        {"company": "Contoso Ltd", "name": "Elena Vasquez", "title": "Vice President, Global Procurement", "date": date(2026, 8, 31)},
    ], intro="IN WITNESS WHEREOF, the Parties have executed this Amendment as of the Amendment Effective Date.")

    d.heading("Exhibit A - Illustrative Fee Adjustment (SOW No. 1)")
    d.table([
        ["Item", f"Renewal Term ending {fd(C_CUR_END)}", "Maximum for Renewal Term beginning April 1, 2027"],
        ["Monthly Fees", "$45,000.00", "$46,800.00"],
        ["Annual Fees", "$540,000.00", "$561,600.00"],
        ["Maximum increase", "Not applicable", "4.0%"],
        ["Latest date for written notice of increase", "Not applicable", fd(fee_notice)],
    ], widths=[2.2, 2.0, 2.3])

    d.heading("Exhibit B - Updated Notice Contacts")
    d.table([
        ["Party", "Contact", "Email"],
        ["Service Provider", "Priya Raman, General Counsel", "legal@northwind.example"],
        ["Customer", "Contracts Office, Global Procurement", "contracts@contoso.example"],
    ], widths=[1.6, 2.6, 2.3])

    d.save(path / f)

    obs = [
        ob(f, cp, "Send non-renewal notice to Contoso (120 days)",
           f"If either party does not want the MSA to auto-renew, it must give written non-renewal notice at least 120 days before the current term ends (term ends {iso(C_CUR_END)}, so by {iso(notice120)}). Otherwise the MSA renews for another year.",
           "Section 2 (amends MSA Section 9.2)", S_C_NR120, "Both", "Notice & renewal", "Recurring", "Annual", notice120,
           risk="High", isTrap=True, trapType="amendment"),
        ob(f, cp, "Deliver quarterly service-level report to Contoso",
           "Send Contoso a written service-level report (availability, incidents, credits) within 10 days after each calendar quarter ends.",
           "Section 3 (amends MSA Section 4.3)", S_C_REPORT10, "Northwind", "Reporting", "Recurring", "Quarterly", report10,
           risk="Medium", isTrap=True, trapType="amendment"),
        ob(f, cp, "Send Contoso fee-increase notice 60 days pre-renewal",
           f"To raise Fees (max 4%) for a Renewal Term starting on or after 2027-04-01, give Contoso written notice at least 60 days before that term starts (by {iso(fee_notice)} for the 2027 renewal).",
           "Section 4 (adds MSA Section 3.4)", S_C_FEE, "Northwind", "Notice & renewal", "Recurring", "Annual", fee_notice,
           risk="Medium"),
        ob(f, cp, "Deliver updated BCP/DR plan to Contoso",
           f"Deliver an updated business continuity and disaster recovery plan (with RTO/RPO for the Service Portal) within 60 days after the amendment date (by {iso(bcp)}).",
           "Section 5", S_C_BCP, "Northwind", "Compliance & audit", "Fixed date", "None", bcp, risk="Medium"),
    ]
    man = dict(fileName=f, title="Amendment No. 1 to Master Services Agreement", counterparty=cp, northwindRole="Supplier",
               contractType="Amendment", effectiveDate=iso(C_AMD), expirationDate=iso(C_CUR_END), autoRenews="Yes",
               noticePeriodDays=120, governingLaw="Washington, USA", contractValue=None, businessUnit="Sales",
               amends="01-Contoso-MSA.docx")
    return obs, man


# ---------------------------------------------------------------- 03 Fabrikam
S_F_FEES = ("Provider shall invoice the Monthly Fees in advance on the first day of each calendar month. Customer shall "
            "pay each invoice within thirty (30) days after the invoice date.")
S_F_PRICE = ("Provider may increase the Monthly Fees no more than once in any twelve (12) month period, and no single "
             "increase may exceed five percent (5%) of the Monthly Fees then in effect. Provider shall give Customer at "
             "least sixty (60) days' prior written notice of any increase, and any increase made without such notice is void.")
S_F_UPTIME = ("Provider shall make the Hosting Services available with a Monthly Uptime Percentage of at least 99.9% in "
              "each calendar month.")
S_F_CLAIM = ("To receive a Service Credit, Customer must submit a written claim to Provider within thirty (30) days after "
             "the end of the calendar month in which the Downtime occurred. Customer's failure to submit a claim within "
             "that period waives Customer's right to a Service Credit for that month.")
S_F_RENEW = ("This Agreement does not renew automatically. This Agreement may be renewed or extended only by a written "
             "agreement signed by both Parties before the Expiration Date.")
S_F_TRANS = ("If Customer requests transition assistance by written notice delivered at least sixty (60) days before the "
             "Expiration Date, Provider shall provide up to ninety (90) days of transition assistance at its then-current "
             "professional services rates to support the migration of Customer Data and workloads to Customer or its "
             "designated successor provider.")


def c03(path):
    f = "03-Fabrikam-Cloud-Hosting-Agreement.docx"
    cp = "Fabrikam Inc"
    eff, exp = date(2024, 4, 1), date(2027, 3, 31)
    last_invoice = date(2026, 11, 1)
    fee_due = last_invoice + timedelta(days=30)
    trans = exp - timedelta(days=60)
    months = (exp.year - eff.year) * 12 + (exp.month - eff.month) + 1
    total = 38500 * months

    d = Doc("Fabrikam Inc  |  Cloud Hosting Services Agreement  |  Confidential", "Contract No. FAB-HS-2024-118", "Cloud Hosting Services Agreement - Fabrikam Inc")
    d.title("Cloud Hosting Services Agreement", "Contract No. FAB-HS-2024-118")
    d.para(f'This Cloud Hosting Services Agreement (this "Agreement") is made as of {fd(eff)} (the "Effective Date") between '
           f'Fabrikam Inc, a Nevada corporation with offices at 2200 Fabrikam Way, Reno, Nevada 89501 ("Provider"), and '
           f'Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Customer"). Provider and '
           f'Customer are each a "Party" and together the "Parties."')
    d.recitals([
        "Provider operates enterprise private-cloud hosting facilities in Reno, Nevada and Quincy, Washington.",
        "Customer wishes to host its order-management and warehouse-management applications in a dedicated environment operated by Provider.",
        "Provider is willing to provide those hosting services on the terms of this Agreement.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Customer Data" means all data, including personal information, that Customer or its users store in or process through the Hosting Services.')
    d.section("1.2", None, '"Downtime" means any period of one (1) minute or longer during which the production environment is unavailable to Customer, excluding Scheduled Maintenance and outages caused by Customer.')
    d.section("1.3", None, '"Hosting Services" means the dedicated private-cloud environment, network connectivity, backup and monitoring services described in Exhibit A.')
    d.section("1.4", None, '"Monthly Uptime Percentage" means the total number of minutes in a calendar month minus the minutes of Downtime in that month, divided by the total number of minutes in that month, expressed as a percentage.')
    d.section("1.5", None, '"Scheduled Maintenance" means maintenance announced through Provider\'s customer portal at least five (5) days in advance and performed between 11:00 p.m. and 3:00 a.m. Pacific Time.')
    d.section("1.6", None, '"Service Credit" means a credit against the Monthly Fees calculated under Section 4.2.')

    d.heading("2. Hosting Services")
    d.section("2.1", "Provision of Services", "Provider will provide the Hosting Services described in Exhibit A, including a dedicated environment of 96 virtual CPUs, 768 GB of memory and 40 TB of replicated storage, with nightly backups retained for thirty-five (35) days.")
    d.section("2.2", "Support", "Provider's network operations center is staffed 24 hours a day, 7 days a week. Customer may open support tickets by telephone or through Provider's customer portal.")

    d.heading("3. Fees and Payment")
    d.section("3.1", "Monthly Fees", f'Customer will pay Provider a fixed fee of $38,500 per month for the Hosting Services (the "Monthly Fees"), for aggregate fees of ${total:,} over the Term before any adjustment under Section 3.3.')
    d.section("3.2", "Invoicing and Payment Terms", S_F_FEES)
    d.section("3.3", "Price Increases", S_F_PRICE)
    d.section("3.4", "Late Payment", "Undisputed amounts that remain unpaid fifteen (15) days after their due date bear interest at the lesser of one percent (1%) per month and the maximum rate permitted by law.")

    d.heading("4. Service Level Agreement")
    d.section("4.1", "Uptime Commitment", S_F_UPTIME)
    d.section("4.2", "Service Credits", "If the Monthly Uptime Percentage in any calendar month is below 99.9%, Customer is eligible for a Service Credit equal to ten percent (10%) of the Monthly Fees for that month, or twenty-five percent (25%) of the Monthly Fees if the Monthly Uptime Percentage is below 99.0%.")
    d.section("4.3", "Claim Procedure", S_F_CLAIM)
    d.section("4.4", "Application of Credits", "Approved Service Credits are applied against the next invoice for Monthly Fees. Service Credits are Customer's sole monetary remedy for Downtime but do not limit Customer's right to terminate under Section 6.4.")

    d.heading("5. Customer Data")
    d.section("5.1", "Ownership", "As between the Parties, Customer owns all Customer Data. Provider acquires no rights in Customer Data other than the limited right to host and process it to provide the Hosting Services.")
    d.section("5.2", "Certification", "Provider maintains ISO/IEC 27001 certification for the data centers used to provide the Hosting Services.")

    d.heading("6. Term, Renewal and Transition")
    d.section("6.1", "Term", f'This Agreement begins on the Effective Date and expires on {fd(exp)} (the "Expiration Date"), unless terminated earlier under this Agreement.')
    d.section("6.2", "Renewal", S_F_RENEW)
    d.section("6.3", "Transition Assistance", S_F_TRANS)
    d.section("6.4", "Termination for Cause", "Either Party may terminate this Agreement by written notice if the other Party materially breaches this Agreement and does not cure the breach within thirty (30) days after receiving written notice of it. Customer may also terminate this Agreement by written notice if the Monthly Uptime Percentage is below 99.0% in any three (3) months within a rolling six (6) month period.")

    d.heading("7. Limitation of Liability")
    d.para("NEITHER PARTY WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL OR PUNITIVE DAMAGES ARISING OUT OF THIS AGREEMENT. EACH PARTY'S AGGREGATE LIABILITY UNDER THIS AGREEMENT WILL NOT EXCEED THE MONTHLY FEES PAID OR PAYABLE IN THE TWELVE (12) MONTHS BEFORE THE CLAIM AROSE.")

    d.heading("8. General")
    d.section("8.1", "Governing Law", "This Agreement is governed by the laws of the State of New York. The state and federal courts located in New York County, New York have exclusive jurisdiction over any dispute arising out of this Agreement.")
    d.section("8.2", "Force Majeure", "Neither Party is liable for any delay or failure to perform caused by events beyond its reasonable control, except that this Section does not excuse payment obligations.")
    d.section("8.3", "Notices", "Notices must be in writing and delivered to the addresses set out above, with a copy by email to legal@northwind.example (for Customer) or contracts@fabrikam.example (for Provider).")
    d.section("8.4", "Entire Agreement", "This Agreement, including Exhibit A, is the entire agreement between the Parties regarding its subject matter and may be amended only in a writing signed by both Parties.")

    d.signatures([
        {"company": "Fabrikam Inc", "name": "Ryan Liu", "title": "Senior Vice President, Sales", "date": date(2024, 3, 25)},
        {"company": "Northwind Traders, Inc.", "name": "Aisha Khan", "title": "Chief Information Officer", "date": date(2024, 3, 26)},
    ])
    d.heading("Exhibit A - Hosting Services Description")
    d.table([
        ["Component", "Specification"],
        ["Compute", "96 dedicated virtual CPUs across two availability zones"],
        ["Memory / storage", "768 GB RAM; 40 TB replicated block storage"],
        ["Backups", "Nightly, retained 35 days; monthly, retained 12 months"],
        ["Network", "Redundant 10 Gbps connectivity; private link to Customer's Seattle headquarters"],
        ["Monitoring", "24x7 infrastructure monitoring and alerting"],
    ], widths=[1.8, 4.7])

    d.save(path / f)

    obs = [
        ob(f, cp, "Pay Fabrikam monthly hosting fees (net 30)",
           f"Pay each monthly hosting invoice ($38,500, issued on the 1st of the month) within 30 days after the invoice date; the next payment ({iso(fee_due)}) covers the {iso(last_invoice)} invoice.",
           "Section 3.2", S_F_FEES, "Northwind", "Payment", "Recurring", "Monthly", fee_due, risk="Medium"),
        ob(f, cp, "Fabrikam: 60 days' notice and 5% cap on price increases",
           "Fabrikam must give at least 60 days' written notice of any fee increase; increases are limited to once per 12 months and 5% each, and an increase without notice is void. Northwind should check any increase against these limits.",
           "Section 3.3", S_F_PRICE, "Counterparty", "Payment", "Event-driven",
           triggerEvent="Fabrikam proposes an increase to the Monthly Fees", risk="Medium", isTrap=True, trapType="counterparty-vs-us"),
        ob(f, cp, "Fabrikam to meet 99.9% monthly uptime",
           "Fabrikam must keep the Hosting Services at a Monthly Uptime Percentage of at least 99.9%.",
           "Section 4.1", S_F_UPTIME, "Counterparty", "Service levels", "Ongoing", risk="Medium"),
        ob(f, cp, "Claim Fabrikam service credits within 30 days",
           "If monthly uptime falls below 99.9%, Northwind must submit a written Service Credit claim within 30 days after that month ends or the credit is waived.",
           "Section 4.3", S_F_CLAIM, "Northwind", "Service levels", "Event-driven",
           triggerEvent="Monthly Uptime Percentage falls below 99.9% in a calendar month (claim due 30 days after that month ends)",
           risk="Medium", isTrap=True, trapType="claim-window"),
        ob(f, cp, "Decide on Fabrikam renewal before 2027-03-31 expiry",
           f"The hosting agreement expires {iso(exp)} and renews only by a signed written agreement before then; decide whether to renew or migrate and sign any renewal before expiry.",
           "Section 6.2", S_F_RENEW, "Both", "Notice & renewal", "Fixed date", "None", exp,
           risk="High", isTrap=True, trapType="fixed-expiry"),
        ob(f, cp, "Request Fabrikam transition assistance by deadline",
           f"To get up to 90 days of transition assistance, Northwind must request it in writing at least 60 days before the {iso(exp)} expiration (by {iso(trans)}).",
           "Section 6.3", S_F_TRANS, "Northwind", "Notice & renewal", "Fixed date", "None", trans,
           risk="High", isTrap=True, trapType="notice-window"),
    ]
    man = dict(fileName=f, title="Cloud Hosting Services Agreement", counterparty=cp, northwindRole="Customer",
               contractType="Supplier agreement", effectiveDate=iso(eff), expirationDate=iso(exp), autoRenews="No",
               noticePeriodDays=None, governingLaw="New York, USA", contractValue=total, businessUnit="IT", amends=None)
    return obs, man


# ---------------------------------------------------------------- 04 Tailspin
S_T_EXCL = ("During the Term, Supplier shall not appoint any other distributor of the Products in the Territory, and "
            "Distributor shall not market or sell any Competing Products in the Territory.")
S_T_MIN = ("Distributor shall purchase Products having an aggregate net purchase price of not less than $750,000 during "
           'each Contract Year (the "Minimum Commitment").')
S_T_QRPT = ("Within twenty (20) days after the end of each calendar quarter, Distributor shall deliver to Supplier a "
            "written report showing Net Sales by Product and by state for that quarter and Distributor's inventory of "
            "Products on hand at the end of that quarter.")
S_T_PLAN = ("Within ninety (90) days after the Effective Date, Distributor shall submit to Supplier for approval an "
            "initial marketing plan for the Products in the Territory covering the first eighteen (18) months of the Term.")
S_T_MDF = ("Distributor shall contribute to Supplier's cooperative marketing development fund an amount equal to two "
           "percent (2%) of Distributor's Net Sales of Products during each calendar year, payable on or before January "
           "31 of the following year.")
S_T_COC = ("Distributor shall notify Supplier in writing within thirty (30) days after any Change of Control of "
           "Distributor.")


def c04(path):
    f = "04-Tailspin-Distribution-Agreement.docx"
    cp = "Tailspin Toys"
    eff, exp = date(2026, 7, 1), date(2029, 6, 30)
    plan = eff + timedelta(days=90)
    q_rpt = Q4_END + timedelta(days=20)
    mdf = date(2027, 1, 31)
    cy_end = eff + relativedelta(years=1) - timedelta(days=1)

    d = Doc("Tailspin Toys  |  Exclusive Distribution Agreement  |  Confidential", "Agreement No. TT-NW-DIST-2026-07", "Exclusive Distribution Agreement - Tailspin Toys")
    d.title("Exclusive Distribution Agreement", "Agreement No. TT-NW-DIST-2026-07")
    d.para(f'This Exclusive Distribution Agreement (this "Agreement") is entered into as of {fd(eff)} (the "Effective Date") '
           f'between Tailspin Toys, a California corporation with its principal office at 75 Hangar Road, San Jose, California '
           f'95110 ("Supplier"), and Northwind Traders, Inc., a Washington corporation with its principal office at {NW_ADDR} '
           f'("Distributor"). Supplier and Distributor are each a "Party."')
    d.recitals([
        "Supplier designs and manufactures remote-control aircraft, consumer drones and hobby flight kits.",
        "Distributor operates a wholesale distribution business serving specialty toy and hobby retailers in the Pacific Northwest.",
        "Supplier wishes to appoint Distributor as its exclusive distributor in the Territory, and Distributor wishes to accept that appointment, on the terms of this Agreement.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Change of Control" means (a) the acquisition by any person or group of more than fifty percent (50%) of the voting securities of Distributor, (b) a merger or consolidation of Distributor after which the holders of Distributor\'s voting securities immediately before the transaction hold less than fifty percent (50%) of the voting power of the surviving entity, or (c) the sale of all or substantially all of Distributor\'s assets.')
    d.section("1.2", None, '"Competing Products" means remote-control aircraft, consumer drones and hobby flight kits manufactured by any person other than Supplier.')
    d.section("1.3", None, '"Contract Year" means each twelve (12) month period beginning on July 1 and ending on June 30 during the Term.')
    d.section("1.4", None, '"Net Sales" means the gross amounts invoiced by Distributor to its customers for Products, less returns, credits, trade discounts, freight and sales taxes.')
    d.section("1.5", None, '"Products" means the Supplier products listed in Exhibit A, as updated by written agreement of the Parties.')
    d.section("1.6", None, '"Territory" means the States of Washington, Oregon, Idaho and Montana.')

    d.heading("2. Appointment and Exclusivity")
    d.section("2.1", "Appointment", "Supplier appoints Distributor as its exclusive distributor of the Products to retailers in the Territory for the Term, and Distributor accepts the appointment.")
    d.section("2.2", "Exclusivity", S_T_EXCL)
    d.section("2.3", "Reserved Rights", "Supplier reserves the right to sell Products outside the Territory and to sell directly to the national retail accounts listed in Exhibit A.")

    d.heading("3. Minimum Purchase Commitment and Orders")
    d.section("3.1", "Minimum Annual Purchase Commitment", S_T_MIN)
    d.section("3.2", "Shortfall", "If Distributor does not meet the Minimum Commitment for a Contract Year, Supplier may, as its sole remedy, convert Distributor's appointment to a non-exclusive appointment by written notice given within sixty (60) days after the end of that Contract Year.")
    d.section("3.3", "Orders and Pricing", "Distributor will order Products by purchase order through Supplier's dealer portal. Distributor's purchase price for each Product is Supplier's then-current published distributor price less the discount shown in Exhibit A. Payment terms are those set out in the dealer credit application approved by Supplier for Distributor.")

    d.heading("4. Reporting and Marketing")
    d.section("4.1", "Quarterly Sales and Inventory Reports", S_T_QRPT)
    d.section("4.2", "Initial Marketing Plan", S_T_PLAN)
    d.section("4.3", "Marketing Development Fund", S_T_MDF + " Supplier will make the fund available for co-branded promotions in the Territory under its cooperative marketing guidelines.")

    d.heading("5. Trademarks")
    d.section("5.1", "License", "Supplier grants Distributor a non-exclusive, royalty-free license during the Term to use Supplier's trademarks solely to advertise and sell the Products in the Territory in accordance with Supplier's brand guidelines.")
    d.section("5.2", "Ownership", "All goodwill arising from the use of Supplier's trademarks inures to the benefit of Supplier.")

    d.heading("6. Term and Termination")
    d.section("6.1", "Term", f"This Agreement begins on the Effective Date and continues until {fd(exp)}, unless terminated earlier under this Agreement. Any extension requires a written agreement signed by both Parties.")
    d.section("6.2", "Termination for Cause", "Either Party may terminate this Agreement by written notice if the other Party materially breaches it and does not cure the breach within thirty (30) days after receiving written notice of the breach.")
    d.section("6.3", "Inventory on Termination", "On expiration or termination, Supplier may elect to repurchase Distributor's saleable inventory of Products at Distributor's net purchase price.")

    d.heading("7. Assignment and Change of Control")
    d.section("7.1", "Assignment", "This Agreement may not be assigned by either Party without the prior written consent of the other Party, which may not be unreasonably withheld.")
    d.section("7.2", "Change of Control", S_T_COC + " Supplier may terminate this Agreement by written notice given within sixty (60) days after receiving that notice.")

    d.heading("8. Limitation of Liability")
    d.para("EXCEPT FOR INDEMNIFICATION OBLIGATIONS AND BREACHES OF ARTICLE 5, NEITHER PARTY WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL OR PUNITIVE DAMAGES ARISING OUT OF THIS AGREEMENT.")

    d.heading("9. General")
    d.section("9.1", "Governing Law", "This Agreement is governed by the laws of the State of Delaware, without regard to its conflict-of-laws rules.")
    d.section("9.2", "Notices", "Notices must be in writing and delivered by courier or email to the addresses set out above or later designated by a Party in writing.")
    d.section("9.3", "Relationship", "Distributor is an independent contractor and is not an agent of Supplier.")
    d.section("9.4", "Entire Agreement", "This Agreement, including its Exhibit, is the entire agreement between the Parties regarding its subject matter and supersedes all prior discussions.")

    d.signatures([
        {"company": "Tailspin Toys", "name": "Grace Whitfield", "title": "Chief Commercial Officer", "date": date(2026, 6, 24)},
        {"company": "Northwind Traders, Inc.", "name": "Maria Delgado", "title": "Chief Operating Officer", "date": date(2026, 6, 26)},
    ])
    d.heading("Exhibit A - Products and Pricing")
    d.table([
        ["Product line", "Examples", "Distributor discount"],
        ["SkyRunner RC aircraft", "SkyRunner 450, SkyRunner Trainer", "40% off distributor list"],
        ["Hover consumer drones", "Hover Mini, Hover 4K", "35% off distributor list"],
        ["Hangar hobby kits", "Balsa glider kits, spare parts", "45% off distributor list"],
        ["Reserved national accounts", "Big-box retail chains (direct only)", "Not applicable"],
    ], widths=[1.9, 2.6, 2.0])

    d.save(path / f)

    obs = [
        ob(f, cp, "Meet $750K minimum annual purchase commitment",
           f"Buy at least $750,000 (net purchase price) of Tailspin Products in each Contract Year (July 1 - June 30); the current Contract Year ends {iso(cy_end)}. A shortfall lets Tailspin make the appointment non-exclusive.",
           "Section 3.1", S_T_MIN, "Northwind", "Purchasing & volume", "Recurring", "Annual", cy_end, risk="High"),
        ob(f, cp, "Send Tailspin quarterly sales & inventory report",
           "Within 20 days after each calendar quarter, send Tailspin Net Sales by Product and state plus inventory on hand.",
           "Section 4.1", S_T_QRPT, "Northwind", "Reporting", "Recurring", "Quarterly", q_rpt, risk="Medium"),
        ob(f, cp, "Pay Tailspin marketing fund (2% of Net Sales)",
           "Contribute 2% of the calendar year's Net Sales of Tailspin Products to the co-op marketing fund by January 31 of the following year.",
           "Section 4.3", S_T_MDF, "Northwind", "Payment", "Recurring", "Annual", mdf, risk="Medium"),
        ob(f, cp, "Submit initial marketing plan to Tailspin",
           f"Submit an 18-month marketing plan for the Territory to Tailspin for approval within 90 days after the Effective Date (by {iso(plan)}).",
           "Section 4.2", S_T_PLAN, "Northwind", "Other", "Fixed date", "None", plan, risk="Medium"),
        ob(f, cp, "Observe territory exclusivity (no competing products)",
           "Tailspin may not appoint another distributor in WA/OR/ID/MT, and Northwind may not market or sell Competing Products in the Territory during the Term.",
           "Section 2.2", S_T_EXCL, "Both", "Compliance & audit", "Ongoing", risk="Medium"),
        ob(f, cp, "Notify Tailspin of change of control within 30 days",
           "If Northwind undergoes a Change of Control (over 50% acquisition, merger or sale of substantially all assets), notify Tailspin in writing within 30 days; Tailspin may then terminate.",
           "Section 7.2", S_T_COC, "Northwind", "Notice & renewal", "Event-driven",
           triggerEvent="Change of Control of Northwind (acquisition of >50% of voting securities, merger, or sale of substantially all assets)",
           risk="High", isTrap=True, trapType="event-driven"),
        ob(f, cp, "Pay Tailspin per dealer credit application terms",
           "Pay for each purchase order on the payment terms in the dealer credit application approved by Tailspin; that document isn't in the Contracts library.",
           "Section 3.3", "Payment terms are those set out in the dealer credit application approved by Supplier for Distributor.",
           "Northwind", "Payment", "Event-driven",
           triggerEvent="Northwind places a purchase order with Tailspin (payment terms in the dealer credit application)",
           risk="Medium", expected="hold",
           reason="Protected payment obligation whose terms are only in the dealer credit application, which isn't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms.",
           isTrap=True, trapType="missing-document"),
    ]
    man = dict(fileName=f, title="Exclusive Distribution Agreement", counterparty=cp, northwindRole="Distributor",
               contractType="Partner agreement", effectiveDate=iso(eff), expirationDate=iso(exp), autoRenews="No",
               noticePeriodDays=None, governingLaw="Delaware, USA", contractValue=750000, businessUnit="Sales", amends=None)
    return obs, man


# ---------------------------------------------------------------- 05 Litware
S_L_AFF = ("Licensee shall not permit any Affiliate or other third party to access or use the Software. Licensee shall "
           "not sublicense, rent or lease the Software, use it to provide services to third parties, or reverse engineer "
           "it except to the extent permitted by applicable law.")
S_L_TRUE = ("Within thirty (30) days after each anniversary of the Effective Date, Licensee shall deliver to Licensor a "
            "true-up report certifying the maximum number of Named Users who had access to the Software at any time "
            "during the preceding Support Year.")
S_L_SUPFEE = ("Licensor shall issue its invoice for each Support Year at least forty-five (45) days before the start of "
              "that Support Year, and Licensee shall pay the Support Fee on or before the first day of that Support Year.")
S_L_SUPREN = ("Support Services renew automatically for successive Support Years unless Licensee gives Licensor written "
              "notice of non-renewal at least sixty (60) days before the start of the next Support Year.")
S_L_AUDIT = ("Licensor may, no more than once in any twelve (12) month period and upon at least fifteen (15) business "
             "days' prior written notice, audit Licensee's use of the Software to verify compliance with this Agreement. "
             "Licensee shall cooperate with any such audit and provide reasonable access to relevant records and systems.")
S_L_COSTS = ("Each Party shall bear its own costs and expenses incurred in connection with the negotiation, preparation "
             "and execution of this Agreement.")


def c05(path):
    f = "05-Litware-Software-License-Support.docx"
    cp = "Litware Inc"
    eff = date(2025, 11, 6)
    anniv = eff + relativedelta(years=1)
    trueup = anniv + timedelta(days=30)
    next_sy = eff + relativedelta(years=2)
    sup_notice = next_sy - timedelta(days=60)

    d = Doc("Litware Inc  |  Software License and Support Agreement  |  Confidential", "Agreement No. LW-SLSA-25-0412", "Software License and Support Agreement - Litware Inc")
    d.title("Software License and Support Agreement", "Agreement No. LW-SLSA-25-0412")
    d.para(f'This Software License and Support Agreement (this "Agreement") is entered into as of {fd(eff)} (the "Effective Date") '
           f'between Litware Inc, a California corporation with offices at 900 Capitol Mall, Sacramento, California 95814 '
           f'("Licensor"), and Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Licensee"). '
           f'Licensor and Licensee are each a "Party."')
    d.recitals([
        "Licensor develops and licenses inventory planning and demand forecasting software.",
        "Licensee wishes to license Licensor's software for use by its planning and purchasing teams and to receive related maintenance and support services.",
        "Licensor is willing to grant the license and provide those services on the terms of this Agreement.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Affiliate" means any entity that directly or indirectly controls, is controlled by, or is under common control with a Party.')
    d.section("1.2", None, '"Documentation" means Licensor\'s user guides and technical specifications for the Software.')
    d.section("1.3", None, '"Named User" means an individual employee or contractor of Licensee who is assigned a unique login to the Software.')
    d.section("1.4", None, '"Software" means Licensor\'s Litware Inventory Optimizer Enterprise software, in object code form, including all updates provided under this Agreement.')
    d.section("1.5", None, '"Support Services" means the maintenance and support services described in Section 4.1.')
    d.section("1.6", None, '"Support Year" means each twelve (12) month period beginning on the Effective Date or on an anniversary of the Effective Date.')

    d.heading("2. License")
    d.section("2.1", "Grant", "Subject to this Agreement, Licensor grants Licensee a perpetual, non-exclusive, non-transferable license to install and use the Software for Licensee's internal business purposes by up to two hundred fifty (250) Named Users.")
    d.section("2.2", "Restrictions", S_L_AFF)
    d.section("2.3", "Additional Named Users", "Licensee may license additional Named Users at any time at a one-time fee of $1,500 per Named User, plus the corresponding pro-rated Support Fee.")

    d.heading("3. Fees and True-Up")
    d.section("3.1", "License Fee", 'Licensee has paid the one-time license fee of $420,000 (the "License Fee") concurrently with the execution of this Agreement. Together with the first-year Support Fee of $84,000, total first-year fees under this Agreement are $504,000.')
    d.section("3.2", "Annual True-Up", S_L_TRUE + " Licensor will invoice any Named Users in excess of the licensed quantity at the rate set out in Section 2.3.")
    d.section("3.3", "Taxes", "All fees exclude applicable sales, use and similar taxes, which are payable by Licensee other than taxes based on Licensor's net income.")

    d.heading("4. Support Services")
    d.section("4.1", "Support", "During each Support Year for which Licensee has paid the Support Fee, Licensor will provide updates, error corrections, and telephone and web support between 6:00 a.m. and 6:00 p.m. Pacific Time on business days.")
    d.section("4.2", "Support Fees", 'The annual support fee is $84,000 (the "Support Fee"). ' + S_L_SUPFEE)
    d.section("4.3", "Support Renewal", S_L_SUPREN)
    d.section("4.4", "Reinstatement", "If Licensee allows Support Services to lapse, reinstatement requires payment of the Support Fees for the lapsed period plus a reinstatement fee equal to ten percent (10%) of those Support Fees.")

    d.heading("5. Audit")
    d.section("5.1", "Audit Right", S_L_AUDIT)
    d.section("5.2", "Results", "Any under-licensing identified by an audit will be invoiced in accordance with Section 3.2. Licensor bears the cost of each audit unless the audit reveals under-licensing of more than ten percent (10%).")

    d.heading("6. Warranty")
    d.section("6.1", "Limited Warranty", "Licensor warrants that the Software will perform materially in accordance with the Documentation for ninety (90) days after delivery.")
    d.section("6.2", "Disclaimer", "EXCEPT AS STATED IN SECTION 6.1, THE SOFTWARE IS PROVIDED WITHOUT WARRANTIES OF ANY KIND, AND LICENSOR DISCLAIMS ALL IMPLIED WARRANTIES, INCLUDING MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.")

    d.heading("7. Limitation of Liability")
    d.para("NEITHER PARTY WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL OR CONSEQUENTIAL DAMAGES. LICENSOR'S AGGREGATE LIABILITY UNDER THIS AGREEMENT WILL NOT EXCEED THE FEES PAID BY LICENSEE IN THE TWELVE (12) MONTHS BEFORE THE CLAIM.")

    d.heading("8. Term and Termination")
    d.section("8.1", "Term", "The license granted in Section 2.1 is perpetual unless terminated under Section 8.2. Support Services continue for successive Support Years as described in Section 4.3.")
    d.section("8.2", "Termination for Breach", "Licensor may terminate the license by written notice if Licensee materially breaches Section 2.2 and does not cure the breach within thirty (30) days after receiving written notice of it.")

    d.heading("9. General")
    d.section("9.1", "Governing Law", "This Agreement is governed by the laws of the State of California, without regard to its conflict-of-laws rules.")
    d.section("9.2", "Costs", S_L_COSTS)
    d.section("9.3", "Notices", "Notices must be in writing and sent to the addresses set out above, with a copy by email to legal@northwind.example (for Licensee) or contracts@litware.example (for Licensor).")
    d.section("9.4", "Entire Agreement", "This Agreement is the entire agreement between the Parties regarding the Software and supersedes any purchase order terms or click-through terms.")

    d.signatures([
        {"company": "Litware Inc", "name": "Arjun Mehta", "title": "Director, Contracts", "date": date(2025, 11, 4)},
        {"company": "Northwind Traders, Inc.", "name": "Aisha Khan", "title": "Chief Information Officer", "date": date(2025, 11, 5)},
    ])

    d.save(path / f)

    obs = [
        ob(f, cp, "Submit annual Named User true-up report to Litware",
           f"Within 30 days after each anniversary of the {iso(eff)} Effective Date, certify to Litware the peak number of Named Users in the prior Support Year (next due {iso(trueup)}).",
           "Section 3.2", S_L_TRUE, "Northwind", "Compliance & audit", "Recurring", "Annual", trueup, risk="High"),
        ob(f, cp, "Pay Litware annual support fee",
           f"Pay the $84,000 annual Support Fee on or before the first day of each Support Year (next Support Year starts {iso(next_sy)}); Litware invoices at least 45 days ahead.",
           "Section 4.2", S_L_SUPFEE, "Northwind", "Payment", "Recurring", "Annual", next_sy, risk="Medium"),
        ob(f, cp, "Send Litware support non-renewal notice (60 days)",
           f"Support auto-renews each Support Year; to stop it, give written notice at least 60 days before the next Support Year starts (by {iso(sup_notice)}).",
           "Section 4.3", S_L_SUPREN, "Northwind", "Notice & renewal", "Recurring", "Annual", sup_notice, risk="Medium"),
        ob(f, cp, "No use of Litware software by affiliates or third parties",
           "Do not let any Affiliate or third party access or use the Software, and do not sublicense, rent, offer it as a service or reverse engineer it.",
           "Section 2.2", S_L_AFF, "Northwind", "Compliance & audit", "Ongoing", risk="Medium",
           isTrap=True, trapType="prohibition"),
        ob(f, cp, "Cooperate with Litware license audit",
           "When Litware gives at least 15 business days' written notice (max once per 12 months), cooperate with the license audit and give reasonable access to records and systems.",
           "Section 5.1", S_L_AUDIT, "Northwind", "Compliance & audit", "Event-driven",
           triggerEvent="Litware gives at least 15 business days' written notice of an audit (no more than once per 12 months)",
           risk="Medium", isTrap=True, trapType="counterparty-vs-us"),
        ob(f, cp, "Bear own negotiation costs",
           "Each party pays its own costs of negotiating and signing the agreement.",
           "Section 9.2", S_L_COSTS, "Both", "Other", "Ongoing", risk="Low", expected="exclude",
           reason="Routine boilerplate: the costs were incurred at signing and no post-signature action, date or deliverable exists.",
           isTrap=True, trapType="routine-admin"),
    ]
    man = dict(fileName=f, title="Software License and Support Agreement", counterparty=cp, northwindRole="Licensee",
               contractType="License", effectiveDate=iso(eff), expirationDate=None, autoRenews="Yes",
               noticePeriodDays=60, governingLaw="California, USA", contractValue=504000, businessUnit="IT", amends=None)
    return obs, man
