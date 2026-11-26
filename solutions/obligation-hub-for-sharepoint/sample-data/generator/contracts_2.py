"""Contracts 06-11."""
from lib import Doc, date, fd, iso, ob, relativedelta, timedelta

NW_ADDR = "4100 Harbor View Drive, Seattle, Washington 98121"
Q4_END = date(2026, 12, 31)

# ---------------------------------------------------------------- 06 Proseware DPA
S_P_BREACH = ("Processor shall notify Controller of any Personal Data Breach without undue delay and in any event within "
              "forty-eight (48) hours after becoming aware of it.")
S_P_SUBNOTICE = ("Processor shall give Controller at least thirty (30) days' prior written notice before engaging any new "
                 "Sub-processor, identifying the Sub-processor, its location and the processing it will perform.")
S_P_OBJ = ("If Controller objects to a new Sub-processor on reasonable data protection grounds, Controller shall notify "
           "Processor of its objection in writing within fifteen (15) days after receiving Processor's notice. If "
           "Controller does not object within that period, the new Sub-processor is deemed approved.")
S_P_SOC1 = ("Processor shall deliver to Controller a copy of its most recent SOC 2 Type II report no later than thirty "
            "(30) days after the DPA Effective Date.")
S_P_SOC2 = ("Thereafter, Processor shall deliver to Controller an updated SOC 2 Type II report on or before October 1 of "
            "each year during the term of this DPA.")


def c06(path):
    f = "06-Proseware-Data-Processing-Agreement.docx"
    cp = "Proseware Inc"
    sa = date(2025, 3, 15)
    eff = date(2026, 9, 1)
    soc1 = eff + timedelta(days=30)
    soc_next = date(2027, 10, 1)

    d = Doc("Proseware Inc  |  Data Processing Agreement  |  Confidential", "DPA-PW-2026-09", "Data Processing Agreement - Proseware Inc")
    d.title("Data Processing Agreement", f"Supplement to the Customer Analytics Services Agreement dated {fd(sa)}")
    d.para(f'This Data Processing Agreement (this "DPA") is entered into as of {fd(eff)} (the "DPA Effective Date") between '
           f'Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Controller"), and Proseware Inc, '
           f'a Washington corporation with offices at 310 West Riverside Avenue, Spokane, Washington 99201 ("Processor"). '
           f'Controller and Processor are each a "Party."')
    d.recitals([
        f'Processor provides customer analytics and loyalty-program services to Controller under the Customer Analytics Services Agreement between the Parties dated {fd(sa)} (the "Services Agreement").',
        "In providing those services, Processor processes personal data relating to Controller's customers and loyalty-program members on Controller's behalf.",
        "The Parties are entering into this DPA to set out their respective data protection commitments for that processing.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Data Protection Laws" means all laws applicable to the processing of Personal Data under this DPA, including the California Consumer Privacy Act, as amended, to the extent applicable.')
    d.section("1.2", None, '"Personal Data" means any information relating to an identified or identifiable natural person that Processor processes on behalf of Controller under the Services Agreement.')
    d.section("1.3", None, '"Personal Data Breach" means a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, Personal Data.')
    d.section("1.4", None, '"Sub-processor" means any third party engaged by Processor to process Personal Data.')

    d.heading("2. Scope and Roles")
    d.section("2.1", "Roles", "Controller determines the purposes and means of processing Personal Data, and Processor processes Personal Data on Controller's behalf as a processor and service provider.")
    d.section("2.2", "Details of Processing", "Annex 1 describes the subject matter, nature and purpose of the processing, the types of Personal Data and the categories of data subjects.")
    d.section("2.3", "Order of Precedence", "If there is a conflict between this DPA and the Services Agreement concerning the processing of Personal Data, this DPA controls.")

    d.heading("3. Security Measures")
    d.section("3.1", "Measures", "The technical and organizational security measures that apply to Processor's processing of Personal Data are set out in Annex 2.")
    d.section("3.2", "Updates", "Processor may update the measures in Annex 2 from time to time, provided that the updated measures do not reduce the overall level of protection of Personal Data.")

    d.heading("4. Personal Data Breach")
    d.section("4.1", "Notification", S_P_BREACH)
    d.section("4.2", "Content of Notice", "The notice will describe, to the extent known, the nature of the Personal Data Breach, the categories and approximate number of data subjects and records concerned, the likely consequences, and the measures taken or proposed to address it.")
    d.section("4.3", "Regulatory Notifications", "As between the Parties, Controller decides whether and how to notify regulators or affected individuals of a Personal Data Breach.")

    d.heading("5. Sub-processors")
    d.section("5.1", "Current Sub-processors", "Controller authorizes the Sub-processors listed in Annex 3 as of the DPA Effective Date.")
    d.section("5.2", "Notice of Changes", S_P_SUBNOTICE)
    d.section("5.3", "Objection", S_P_OBJ)
    d.section("5.4", "Resolution", "If Controller objects, the Parties will discuss the objection in good faith. If the objection is not resolved within thirty (30) days, Controller may terminate the affected services under the Services Agreement without penalty.")

    d.heading("6. Audits and Certifications")
    d.section("6.1", "Initial SOC 2 Report", S_P_SOC1)
    d.section("6.2", "Annual SOC 2 Reports", S_P_SOC2)
    d.section("6.3", "Audits", "If a SOC 2 report does not reasonably address Controller's data protection compliance questions, Controller may, at its own expense and on at least thirty (30) days' notice, conduct an on-site audit of Processor no more than once in any twelve (12) month period.")

    d.heading("7. Return and Deletion")
    d.para("Return and deletion of Personal Data upon termination of the Services Agreement is governed by Section 11.4 of the Services Agreement.")

    d.heading("8. General")
    d.section("8.1", "Term", "This DPA remains in effect for as long as Processor processes Personal Data on behalf of Controller under the Services Agreement.")
    d.section("8.2", "Liability", "Each Party's liability under this DPA is subject to the limitations of liability in the Services Agreement.")
    d.section("8.3", "Governing Law", "This DPA is governed by the laws of the State of Washington.")
    d.section("8.4", "Entire Agreement", "This DPA, together with the Services Agreement, is the entire agreement between the Parties regarding the processing of Personal Data.")

    d.signatures([
        {"company": "Northwind Traders, Inc.", "name": "Priya Raman", "title": "General Counsel", "date": date(2026, 8, 27)},
        {"company": "Proseware Inc", "name": "Hannah Schultz", "title": "Data Protection Officer", "date": date(2026, 8, 28)},
    ], intro="IN WITNESS WHEREOF, the Parties have executed this DPA as of the DPA Effective Date.")

    d.heading("Annex 1 - Details of Processing")
    d.table([
        ["Item", "Description"],
        ["Subject matter", "Customer analytics, segmentation and loyalty-program administration"],
        ["Duration", "The term of the Services Agreement"],
        ["Data subjects", "Controller's retail customers and loyalty-program members"],
        ["Personal Data", "Name, email address, postal address, loyalty ID, purchase history"],
        ["Sensitive data", "None"],
    ], widths=[1.8, 4.7])
    d.heading("Annex 2 - Security Measures (Summary)")
    d.table([
        ["Control area", "Measure"],
        ["Access control", "Role-based access, multi-factor authentication for all administrators"],
        ["Encryption", "AES-256 at rest; TLS 1.2 or higher in transit"],
        ["Logging", "Centralized security logging retained for twelve months"],
        ["Testing", "Annual third-party penetration test"],
    ], widths=[1.8, 4.7])
    d.heading("Annex 3 - Authorized Sub-processors")
    d.table([
        ["Sub-processor", "Service", "Location"],
        ["Contoso Ltd", "Cloud infrastructure hosting", "United States"],
        ["Litware Inc", "Transactional email delivery", "United States"],
        ["Fabrikam Inc", "Encrypted backup storage", "United States"],
    ], widths=[2.0, 2.8, 1.7])

    d.save(path / f)

    obs = [
        ob(f, cp, "Proseware: notify personal data breach within 48 hours",
           "Proseware must notify Northwind of any Personal Data Breach without undue delay and no later than 48 hours after becoming aware of it.",
           "Section 4.1", S_P_BREACH, "Counterparty", "Data & confidentiality", "Event-driven",
           triggerEvent="Proseware becomes aware of a Personal Data Breach", risk="High",
           isTrap=True, trapType="counterparty-vs-us"),
        ob(f, cp, "Object to new Proseware sub-processor within 15 days",
           "When Proseware gives notice of a new Sub-processor, Northwind must send any written objection within 15 days after receiving it, or the Sub-processor is deemed approved.",
           "Section 5.3", S_P_OBJ, "Northwind", "Data & confidentiality", "Event-driven",
           triggerEvent="Northwind receives Proseware's notice of a new Sub-processor", risk="Medium",
           isTrap=True, trapType="event-driven"),
        ob(f, cp, "Proseware: 30 days' notice before new sub-processor",
           "Proseware must give at least 30 days' written notice (identity, location, processing) before engaging any new Sub-processor.",
           "Section 5.2", S_P_SUBNOTICE, "Counterparty", "Data & confidentiality", "Event-driven",
           triggerEvent="Proseware plans to engage a new Sub-processor", risk="Medium"),
        ob(f, cp, "Obtain Proseware's initial SOC 2 Type II report",
           f"Proseware must deliver its most recent SOC 2 Type II report within 30 days after the DPA Effective Date (by {iso(soc1)}); chase if not received.",
           "Section 6.1", S_P_SOC1, "Counterparty", "Compliance & audit", "Fixed date", "None", soc1, risk="Medium"),
        ob(f, cp, "Obtain Proseware's annual SOC 2 Type II report",
           "After the initial report, Proseware must deliver an updated SOC 2 Type II report by October 1 every year.",
           "Section 6.2", S_P_SOC2, "Counterparty", "Compliance & audit", "Recurring", "Annual", soc_next, risk="Medium"),
        ob(f, cp, "Proseware: return or delete personal data at termination",
           "On termination of the Services Agreement, Proseware must return and delete Personal Data as set out in Section 11.4 of the Services Agreement, which isn't in the Contracts library.",
           "Section 7", "Return and deletion of Personal Data upon termination of the Services Agreement is governed by Section 11.4 of the Services Agreement.",
           "Counterparty", "Data & confidentiality", "Event-driven",
           triggerEvent="Termination of the Services Agreement",
           risk="Medium", expected="hold",
           reason="Protected data-return obligation whose terms are only in the Services Agreement (Section 11.4), which isn't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms.",
           isTrap=True, trapType="missing-document"),
    ]
    man = dict(fileName=f, title="Data Processing Agreement", counterparty=cp, northwindRole="Controller",
               contractType="Data processing", effectiveDate=iso(eff), expirationDate=None, autoRenews="No",
               noticePeriodDays=None, governingLaw="Washington, USA", contractValue=None, businessUnit="Legal", amends=None)
    return obs, man


# ---------------------------------------------------------------- 07 Alpine Ski House lease
S_A_RENT = ("Tenant shall pay Monthly Base Rent in advance, without demand, deduction or offset, on or before the first "
            "(1st) day of each calendar month during the Term.")
S_A_DEP = ("If Landlord applies any part of the Security Deposit to cure a default by Tenant, Tenant shall restore the "
           "Security Deposit to its full amount within ten (10) days after Landlord's written demand.")
S_A_REPAIR = ("Tenant shall notify Landlord in writing of any condition in the Premises requiring repair by Landlord "
              "within ten (10) days after Tenant discovers the condition.")
S_A_INS = ("Tenant shall maintain, throughout the Term, commercial general liability insurance with limits of not less "
           "than $2,000,000 per occurrence and property insurance covering Tenant's personal property at full "
           "replacement cost. Tenant shall deliver to Landlord a certificate of insurance evidencing the coverage "
           "required by this Section 5.1, naming Landlord as an additional insured, on or before January 15 of each "
           "calendar year during the Term.")
S_A_OPT = ("Tenant may exercise the renewal option only by delivering written notice to Landlord no earlier than twelve "
           "(12) months and no later than nine (9) months before the Expiration Date. If Tenant does not deliver notice "
           "within that period, the renewal option lapses and is of no further force or effect.")


def c07(path):
    f = "07-Alpine-Ski-House-Office-Lease.docx"
    cp = "Alpine Ski House"
    comm, exp = date(2023, 10, 1), date(2027, 9, 30)
    win_open = exp - relativedelta(months=12)
    win_close = exp - relativedelta(months=9)
    rent_next = date(2026, 12, 1)
    coi_next = date(2027, 1, 15)
    months = (exp.year - comm.year) * 12 + (exp.month - comm.month) + 1

    d = Doc("Alpine Ski House  |  Office Lease - Alpine Commons, Suite 400  |  Confidential", "Lease No. ASH-AC-400-2023", "Office Lease - Alpine Ski House")
    d.title("Office Lease", "Alpine Commons, Suite 400  |  Lease No. ASH-AC-400-2023")
    d.para(f'This Office Lease (this "Lease") is made and entered into as of {fd(comm)} between Alpine Ski House, a Washington '
           f'limited liability company with offices at 2250 Summit Avenue NE, Bellevue, Washington 98004 ("Landlord"), and '
           f'Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Tenant"). Landlord and Tenant are '
           f'each a "Party."')
    d.recitals([
        "Landlord owns the office building known as Alpine Commons, located at 2250 Summit Avenue NE, Bellevue, Washington.",
        "Tenant wishes to lease space in Alpine Commons for its Eastside sales and customer success teams, and Landlord wishes to lease that space to Tenant, on the terms of this Lease.",
    ])
    d.heading("Basic Lease Information")
    d.table([
        ["Item", "Detail"],
        ["Premises", "Suite 400, Alpine Commons, 2250 Summit Avenue NE, Bellevue, Washington 98004"],
        ["Rentable Area", "14,250 rentable square feet"],
        ["Commencement Date", fd(comm)],
        ["Expiration Date", fd(exp)],
        ["Lease Term", f"{months} months"],
        ["Monthly Base Rent", "$42,750.00"],
        ["Annual Base Rent", "$513,000.00"],
        ["Security Deposit", "$85,500.00"],
        ["Permitted Use", "General office use"],
        ["Renewal Option", "One (1) option to extend for five (5) years (Article 6)"],
    ], widths=[1.9, 4.6], label_col=True)
    d.para("In consideration of the rent and covenants in this Lease, the Parties agree as follows:")

    d.heading("1. Premises and Term")
    d.section("1.1", "Premises", "Landlord leases the Premises to Tenant, and Tenant leases the Premises from Landlord, on the terms of this Lease. Tenant may use fifteen (15) unreserved parking spaces in the Alpine Commons garage at no additional charge.")
    d.section("1.2", "Term", 'The term of this Lease begins on the Commencement Date and ends on the Expiration Date (the "Term"), unless extended under Article 6 or terminated earlier under this Lease.')

    d.heading("2. Rent")
    d.section("2.1", "Base Rent", S_A_RENT)
    d.section("2.2", "Gross Lease", "This Lease is a full-service gross lease, and Monthly Base Rent includes Tenant's share of operating expenses, real estate taxes and building insurance for Alpine Commons.")
    d.section("2.3", "Late Charge", "Any installment of rent not received within five (5) days after its due date is subject to a late charge equal to five percent (5%) of the overdue amount.")

    d.heading("3. Security Deposit")
    d.section("3.1", "Deposit", "Tenant deposited the Security Deposit with Landlord upon execution of this Lease. Landlord may hold the Security Deposit with its general funds and is not required to pay interest on it.")
    d.section("3.2", "Application and Restoration", S_A_DEP)

    d.heading("4. Use, Maintenance and Repairs")
    d.section("4.1", "Use", "The Premises may be used only for the Permitted Use.")
    d.section("4.2", "Building Maintenance", "Monthly Base Rent includes the cost of maintaining the roof, structure, building systems and common areas of Alpine Commons.")
    d.section("4.3", "Notice of Repairs", S_A_REPAIR)

    d.heading("5. Insurance")
    d.section("5.1", "Tenant's Insurance", S_A_INS)
    d.section("5.2", "Waiver of Subrogation", "Landlord and Tenant each waive claims against the other for damage to property to the extent the damage is covered by insurance carried, or required by this Lease to be carried, by the waiving Party.")

    d.heading("6. Renewal Option")
    d.section("6.1", "Option", 'Provided Tenant is not in default beyond any applicable cure period, Tenant has one (1) option to extend the Term for a single period of five (5) years (the "Extension Term") at ninety-five percent (95%) of the then-prevailing market rent for comparable office space in Bellevue, Washington.')
    d.section("6.2", "Exercise", S_A_OPT)
    d.section("6.3", "Market Rent", "If the Parties do not agree on market rent within thirty (30) days after Tenant exercises the renewal option, market rent will be determined by a licensed commercial real estate broker jointly selected by the Parties.")

    d.heading("7. Holding Over")
    d.para("If Tenant remains in possession of the Premises after the Expiration Date without a written extension, Tenant is a month-to-month tenant at one hundred fifty percent (150%) of the Monthly Base Rent in effect on the Expiration Date.")

    d.heading("8. General")
    d.section("8.1", "Quiet Enjoyment", "So long as Tenant is not in default, Tenant may peaceably and quietly enjoy the Premises during the Term.")
    d.section("8.2", "Governing Law", "This Lease is governed by the laws of the State of Washington.")
    d.section("8.3", "Notices", "Notices must be in writing and delivered to the addresses set out above, with a copy by email to facilities@northwind.example (for Tenant) or leasing@alpineskihouse.example (for Landlord).")
    d.section("8.4", "Brokers", "Each Party represents that it has dealt with no broker in connection with this Lease other than Wide Horizon Realty, whose commission Landlord will pay under a separate agreement.")
    d.section("8.5", "Entire Agreement", "This Lease, including the Basic Lease Information, is the entire agreement between the Parties regarding the Premises.")

    d.signatures([
        {"company": "Alpine Ski House", "name": "Marcus Lindqvist", "title": "Managing Member", "date": date(2023, 9, 18)},
        {"company": "Northwind Traders, Inc.", "name": "Maria Delgado", "title": "Chief Operating Officer", "date": date(2023, 9, 20)},
    ], intro="IN WITNESS WHEREOF, the Parties have executed this Lease as of the date first written above.")

    d.save(path / f)

    obs = [
        ob(f, cp, "Pay monthly base rent to Alpine Ski House",
           "Pay $42,750 Monthly Base Rent in advance on or before the 1st of every month, without deduction (late charge after 5 days).",
           "Section 2.1", S_A_RENT, "Northwind", "Payment", "Recurring", "Monthly", rent_next, risk="High"),
        ob(f, cp, "Restore security deposit within 10 days of demand",
           "If the landlord uses any of the $85,500 Security Deposit to cure a Northwind default, top it back up within 10 days after the landlord's written demand.",
           "Section 3.2", S_A_DEP, "Northwind", "Payment", "Event-driven",
           triggerEvent="Landlord applies the Security Deposit to a Tenant default and sends a written demand", risk="Low"),
        ob(f, cp, "Exercise lease renewal option (window closes Dec 30)",
           f"To extend the lease for 5 years, deliver written notice no earlier than {iso(win_open)} and no later than {iso(win_close)} (12 to 9 months before the {iso(exp)} expiration). Missing the window forfeits the option.",
           "Section 6.2", S_A_OPT, "Northwind", "Notice & renewal", "Fixed date", "None", win_close,
           risk="High", isTrap=True, trapType="notice-window"),
        ob(f, cp, "Maintain insurance; send landlord COI by Jan 15",
           "Keep $2M CGL and full-replacement property insurance in force and deliver a certificate naming the landlord as additional insured by January 15 each year.",
           "Section 5.1", S_A_INS, "Northwind", "Insurance", "Recurring", "Annual", coi_next, risk="Medium"),
        ob(f, cp, "Report needed repairs to landlord within 10 days",
           "Notify the landlord in writing of any condition in the Premises that needs landlord repair within 10 days after discovering it.",
           "Section 4.3", S_A_REPAIR, "Northwind", "Other", "Event-driven",
           triggerEvent="Northwind discovers a condition in the Premises requiring repair by the landlord", risk="Medium",
           isTrap=True, trapType="event-driven"),
    ]
    man = dict(fileName=f, title="Office Lease", counterparty=cp, northwindRole="Tenant", contractType="Lease",
               effectiveDate=iso(comm), expirationDate=iso(exp), autoRenews="No", noticePeriodDays=None,
               governingLaw="Washington, USA", contractValue=513000, businessUnit="Facilities", amends=None)
    return obs, man


# ---------------------------------------------------------------- 08 Wide World Importers
S_W_FC = ("On or before the fifth (5th) day of each calendar month, Buyer shall provide Supplier with a rolling six (6) "
          "month non-binding forecast of its anticipated requirements for each Product.")
S_W_DISC = ("Supplier shall give Buyer at least ninety (90) days' prior written notice before discontinuing any Product, "
            "and shall accept last-time-buy Purchase Orders for the discontinued Product submitted during that notice period.")
S_W_REVIEW = ("Each year during the Term, the Parties shall meet no later than October 31 to review Product pricing for "
              "the following calendar year.")
S_W_PAY = "Buyer shall pay each undisputed invoice within forty-five (45) days after receipt of the invoice."
S_W_DEFECT = ("Buyer shall notify Supplier in writing of any Defect within fourteen (14) days after delivery of the "
              "affected Products. Products for which Buyer gives no notice of Defect within that period are deemed "
              "accepted, except for latent Defects that could not reasonably have been discovered on inspection.")


def c08(path):
    f = "08-Wide-World-Importers-Supply-Agreement.docx"
    cp = "Wide World Importers"
    eff, exp = date(2025, 6, 1), date(2028, 5, 31)
    fc_next = date(2026, 12, 5)
    review_next = date(2027, 10, 31)

    d = Doc("Wide World Importers  |  Supply Agreement  |  Confidential", "Agreement No. WWI-NW-SA-2025-06", "Supply Agreement - Wide World Importers")
    d.title("Supply Agreement", "Agreement No. WWI-NW-SA-2025-06")
    d.para(f'This Supply Agreement (this "Agreement") is entered into as of {fd(eff)} (the "Effective Date") between Wide World '
           f'Importers, a Washington corporation with offices at 1400 Port of Tacoma Road, Tacoma, Washington 98421 '
           f'("Supplier"), and Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Buyer"). '
           f'Supplier and Buyer are each a "Party."')
    d.recitals([
        "Supplier imports and distributes specialty packaged foods, including olive oils, teas, spices and preserves.",
        "Buyer distributes specialty foods to independent grocers and gift retailers and wishes to purchase Supplier's products for resale.",
        "Buyer has qualified Supplier as an approved vendor following a food-safety and traceability review completed in April 2025.",
        "The Parties wish to set out the terms on which Buyer may purchase those products from Supplier.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Business Day" means Monday through Friday, excluding U.S. federal holidays.')
    d.section("1.2", None, '"Defect" means any failure of a Product to conform to the Specifications, including damaged packaging, incorrect labeling or contamination.')
    d.section("1.3", None, '"Products" means the products listed in Exhibit A.')
    d.section("1.4", None, '"Purchase Order" means a written order for Products issued by Buyer under this Agreement.')
    d.section("1.5", None, '"Specifications" means the specifications for each Product set out in Exhibit A, including a minimum remaining shelf life of nine (9) months upon delivery.')

    d.heading("2. Supply and Ordering")
    d.section("2.1", "Purchase and Sale", "Supplier will sell Products to Buyer, and Buyer may purchase Products, by Purchase Orders issued under this Agreement. Buyer has no minimum purchase obligation. Buyer's anticipated purchases are approximately $1,200,000 per year.")
    d.section("2.2", "Forecasts", S_W_FC)
    d.section("2.3", "Acceptance of Orders", "Each Purchase Order is deemed accepted unless Supplier rejects it in writing within two (2) Business Days after receipt.")
    d.section("2.4", "Delivery", "Products are delivered DAP (Incoterms 2020) to Buyer's distribution center at 1800 Commerce Way, Kent, Washington 98032.")
    d.section("2.5", "Discontinuation", S_W_DISC)

    d.heading("3. Pricing and Payment")
    d.section("3.1", "Prices", "Prices for Products are set out in Exhibit A and remain fixed for each calendar year except as agreed under Section 3.2.")
    d.section("3.2", "Annual Price Review", S_W_REVIEW + " Agreed price changes take effect on January 1 of the following year once documented in an updated Exhibit A signed by both Parties.")
    d.section("3.3", "Invoices and Payment", "Supplier will invoice each shipment upon delivery. " + S_W_PAY)
    d.section("3.4", "Currency and Duties", "All prices are stated in U.S. dollars and include import duties, customs brokerage and ocean freight to the port of Tacoma.")

    d.heading("4. Quality and Acceptance")
    d.section("4.1", "Inspection and Defect Notice", S_W_DEFECT)
    d.section("4.2", "Remedies", "Buyer's remedy for Products properly rejected under Section 4.1 is replacement of the Products or a credit for them, at Buyer's option.")

    d.heading("5. Term and Termination")
    d.section("5.1", "Term", f"This Agreement begins on the Effective Date and expires on {fd(exp)}. The Parties may extend the Term only by written agreement.")
    d.section("5.2", "Termination for Cause", "Either Party may terminate this Agreement by written notice if the other Party materially breaches it and does not cure the breach within thirty (30) days after receiving written notice of the breach.")

    d.heading("6. Limitation of Liability")
    d.para("NEITHER PARTY WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THIS AGREEMENT, EXCEPT FOR LIABILITY ARISING FROM PRODUCT CONTAMINATION OR A PARTY'S GROSS NEGLIGENCE OR WILLFUL MISCONDUCT.")

    d.heading("7. General")
    d.section("7.1", "Governing Law", "This Agreement is governed by the laws of the State of Washington. The state and federal courts in King County, Washington have exclusive jurisdiction.")
    d.section("7.2", "Force Majeure", "Neither Party is liable for delay or failure to perform caused by events beyond its reasonable control, including port closures and shipping embargoes.")
    d.section("7.3", "Notices", "Notices must be in writing and delivered to the addresses set out above, with a copy by email to procurement@northwind.example (for Buyer) or sales@wideworldimporters.example (for Supplier).")
    d.section("7.4", "Independent Contractors", "The Parties are independent contractors, and neither Party has authority to bind the other.")
    d.section("7.5", "Severability", "If any provision of this Agreement is held unenforceable, the remaining provisions remain in full force and effect.")
    d.section("7.6", "Entire Agreement", "This Agreement, including Exhibit A, is the entire agreement between the Parties regarding its subject matter. Terms in any Purchase Order or invoice that conflict with this Agreement have no effect.")

    d.signatures([
        {"company": "Wide World Importers", "name": "Sofia Moreno", "title": "President", "date": date(2025, 5, 28)},
        {"company": "Northwind Traders, Inc.", "name": "Thomas Berg", "title": "Vice President, Procurement", "date": date(2025, 5, 29)},
    ])
    d.heading("Exhibit A - Products, Prices and Specifications")
    d.table([
        ["Product", "Pack", "Unit price", "Minimum shelf life on delivery"],
        ["Cretan extra-virgin olive oil", "12 x 500 ml", "$96.00", "9 months"],
        ["Darjeeling first-flush loose tea", "24 x 100 g", "$148.80", "12 months"],
        ["Smoked paprika", "24 x 70 g", "$62.40", "12 months"],
        ["Seville orange marmalade", "12 x 340 g", "$54.00", "9 months"],
        ["Sicilian sea salt flakes", "24 x 125 g", "$70.80", "24 months"],
        ["Aged balsamic vinegar of Modena", "12 x 250 ml", "$118.80", "12 months"],
    ], widths=[2.4, 1.2, 1.1, 1.8])

    d.save(path / f)

    obs = [
        ob(f, cp, "Wide World: 90 days' notice before discontinuing product",
           "Wide World must give at least 90 days' written notice before discontinuing any Product and accept last-time-buy orders during that period.",
           "Section 2.5", S_W_DISC, "Counterparty", "Purchasing & volume", "Event-driven",
           triggerEvent="Wide World decides to discontinue a Product", risk="Medium",
           isTrap=True, trapType="counterparty-vs-us"),
        ob(f, cp, "Send Wide World rolling 6-month forecast by the 5th",
           "By the 5th of every month, send Wide World a non-binding rolling 6-month forecast for each Product.",
           "Section 2.2", S_W_FC, "Northwind", "Purchasing & volume", "Recurring", "Monthly", fc_next, risk="Medium"),
        ob(f, cp, "Notify Wide World of defects within 14 days of delivery",
           "Inspect each delivery and give written notice of any Defect within 14 days after delivery; otherwise the Products are deemed accepted (except latent Defects).",
           "Section 4.1", S_W_DEFECT, "Northwind", "Other", "Event-driven",
           triggerEvent="Each delivery of Products to Northwind (notice due within 14 days after delivery)", risk="High",
           isTrap=True, trapType="event-driven"),
        ob(f, cp, "Hold annual price review with Wide World by Oct 31",
           "Meet with Wide World by October 31 each year to review next year's Product pricing; agreed changes take effect January 1 via a signed updated Exhibit A.",
           "Section 3.2", S_W_REVIEW, "Both", "Purchasing & volume", "Recurring", "Annual", review_next, risk="Low"),
        ob(f, cp, "Pay Wide World invoices within 45 days",
           "Pay each undisputed Wide World invoice (issued on delivery) within 45 days after receiving it.",
           "Section 3.3", S_W_PAY, "Northwind", "Payment", "Event-driven",
           triggerEvent="Northwind receives a Wide World invoice (issued at each delivery)", risk="Medium"),
    ]
    man = dict(fileName=f, title="Supply Agreement", counterparty=cp, northwindRole="Customer",
               contractType="Supplier agreement", effectiveDate=iso(eff), expirationDate=iso(exp), autoRenews="No",
               noticePeriodDays=None, governingLaw="Washington, USA", contractValue=1200000,
               businessUnit="Procurement", amends=None)
    return obs, man


# ---------------------------------------------------------------- 09 Adventure Works
S_AW_REBATE = ("Reseller shall pay each rebate earned under Section 3.1, together with a statement showing its "
               "calculation, within forty-five (45) days after the end of the applicable calendar quarter.")
S_AW_MFN = ("During the Term, Reseller shall offer Customer prices for the Products that are no less favorable than the "
            "prices Reseller offers to any Similarly Situated Customer.")
S_AW_MFN2 = ("If Reseller offers more favorable prices for a Product to a Similarly Situated Customer, Reseller shall "
             "notify Customer in writing within thirty (30) days and extend the more favorable prices to Customer from "
             "the date they were first offered to the other customer.")


def c09(path):
    f = "09-Adventure-Works-Reseller-Agreement.docx"
    cp = "Adventure Works Cycles"
    eff, exp = date(2024, 1, 1), date(2026, 12, 31)
    rebate_next = Q4_END + timedelta(days=45)
    s_term = (f"This Agreement begins on {fd(eff)} and expires on {fd(exp)}. This Agreement does not renew "
              f"automatically, and any renewal or extension requires a written agreement signed by both Parties.")

    d = Doc("Adventure Works Cycles  |  Reseller Agreement  |  Confidential", "Agreement No. NW-AW-RA-2024-01", "Reseller Agreement - Adventure Works Cycles")
    d.title("Reseller Agreement", "Agreement No. NW-AW-RA-2024-01")
    d.para(f'This Reseller Agreement (this "Agreement") is entered into as of {fd(eff)} (the "Effective Date") between '
           f'Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Reseller"), and Adventure Works '
           f'Cycles, an Oregon corporation with offices at 600 Trailhead Drive, Bend, Oregon 97701 ("Customer"). Reseller '
           f'and Customer are each a "Party."')
    d.recitals([
        'Reseller is an authorized reseller of retail point-of-sale terminals, barcode scanners, receipt printers and related third-party retail software (the "Products").',
        "Customer operates bicycle retail stores in Oregon, Washington and California and wishes to purchase Products from Reseller for use in its stores.",
        "The Parties wish to set out the pricing, rebate and other terms that apply to Customer's purchases.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Definitions")
    d.section("1.1", None, '"Net Purchases" means the total amounts invoiced by Reseller to Customer for Products in a calendar quarter, less returns, credits, taxes and shipping charges.')
    d.section("1.2", None, '"Products" has the meaning given in the Recitals and includes the items listed in Exhibit A, as updated by written agreement of the Parties.')
    d.section("1.3", None, '"Similarly Situated Customer" means any customer of Reseller in the United States that purchases comparable Products in comparable annual volumes on comparable payment and delivery terms.')

    d.heading("2. Purchase of Products")
    d.section("2.1", "Orders", "Customer may order Products by purchase order. Customer anticipates purchases of approximately $800,000 per year but has no minimum purchase commitment.")
    d.section("2.2", "Prices and Payment Terms", "Prices for Products are set out in Exhibit A. Payment terms are set out in Reseller's standard credit terms approved for Customer.")
    d.section("2.3", "Manufacturer Warranties", "Products carry the warranties of their manufacturers. Reseller makes no additional warranty for Products.")
    d.section("2.4", "Delivery and Title", "Products are shipped FOB Reseller's warehouse in Kent, Washington. Title and risk of loss pass to Customer upon delivery to the carrier.")
    d.section("2.5", "Returns", "Customer may return unopened Products within thirty (30) days after delivery for a credit, less a restocking fee of fifteen percent (15%).")

    d.heading("3. Volume Rebate")
    d.section("3.1", "Rebate", "For each calendar quarter in which Customer's Net Purchases exceed $150,000, Customer earns a rebate equal to three percent (3%) of Net Purchases for that quarter.")
    d.section("3.2", "Payment of Rebates", S_AW_REBATE)
    d.section("3.3", "Survival", "Rebates for calendar quarters ending on or before the expiration of this Agreement remain payable after its expiration.")
    d.section("3.4", "Illustration", "Exhibit B illustrates the rebate calculation. Exhibit B is for convenience only, and Section 3.1 controls if there is any inconsistency.")

    d.heading("4. Most Favored Customer Pricing")
    d.section("4.1", "Pricing Commitment", S_AW_MFN)
    d.section("4.2", "Adjustment", S_AW_MFN2)
    d.section("4.3", "Exclusions", "Article 4 does not apply to one-time clearance pricing on discontinued Products or to prices offered under public-sector contracts.")

    d.heading("5. Term")
    d.section("5.1", "Term and Expiration", s_term)
    d.section("5.2", "Effect of Expiration", "Purchase orders accepted by Reseller before expiration will be fulfilled on the terms of this Agreement.")
    d.section("5.3", "Termination for Cause", "Either Party may terminate this Agreement by written notice if the other Party materially breaches it and does not cure the breach within thirty (30) days after receiving written notice of the breach.")

    d.heading("6. Limitation of Liability")
    d.para("NEITHER PARTY WILL BE LIABLE FOR ANY INDIRECT, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THIS AGREEMENT. RESELLER'S AGGREGATE LIABILITY WILL NOT EXCEED THE AMOUNTS PAID BY CUSTOMER UNDER THIS AGREEMENT IN THE TWELVE (12) MONTHS BEFORE THE CLAIM.")

    d.heading("7. General")
    d.section("7.1", "Governing Law", "This Agreement is governed by the laws of the State of Oregon.")
    d.section("7.2", "Notices", "Notices must be in writing and delivered to the addresses set out above, with a copy by email to sales.contracts@northwind.example (for Reseller) or purchasing@adventure-works.example (for Customer).")
    d.section("7.3", "Independent Contractors", "The Parties are independent contractors. Nothing in this Agreement creates a partnership, franchise or agency relationship.")
    d.section("7.4", "Severability; Waiver", "If any provision of this Agreement is held unenforceable, the remaining provisions remain in effect. A waiver of any breach is not a waiver of any other breach.")
    d.section("7.5", "Entire Agreement", "This Agreement, including its Exhibits, is the entire agreement between the Parties regarding its subject matter and supersedes any conflicting purchase order terms.")

    d.signatures([
        {"company": "Northwind Traders, Inc.", "name": "Laura Chen", "title": "Vice President, Sales", "date": date(2023, 12, 18)},
        {"company": "Adventure Works Cycles", "name": "Kevin Park", "title": "Director of Purchasing", "date": date(2023, 12, 20)},
    ])
    d.heading("Exhibit A - Products and Prices")
    d.table([
        ["Product", "Unit price"],
        ["Countertop POS terminal with 15-inch display", "$1,240.00"],
        ["Handheld barcode scanner", "$310.00"],
        ["Thermal receipt printer", "$285.00"],
        ["Retail POS software license (per register, annual)", "$420.00"],
    ], widths=[4.5, 2.0])
    d.heading("Exhibit B - Rebate Illustration")
    d.table([
        ["Quarter (example)", "Net Purchases", "Threshold met?", "Rebate (3%)"],
        ["Quarter A", "$180,000", "Yes", "$5,400"],
        ["Quarter B", "$142,500", "No", "$0"],
        ["Quarter C", "$215,000", "Yes", "$6,450"],
    ], widths=[1.7, 1.6, 1.5, 1.7])

    d.save(path / f)

    obs = [
        ob(f, cp, "Pay Adventure Works quarterly volume rebate",
           "For each quarter with Net Purchases over $150,000, pay Adventure Works a 3% rebate with a calculation statement within 45 days after quarter end (Q4 2026 rebate survives expiry).",
           "Section 3.2", S_AW_REBATE, "Northwind", "Payment", "Recurring", "Quarterly", rebate_next, risk="Medium"),
        ob(f, cp, "Maintain most-favored-customer pricing",
           "During the Term, Northwind's prices to Adventure Works must be no less favorable than prices offered to any Similarly Situated Customer.",
           "Section 4.1", S_AW_MFN, "Northwind", "Compliance & audit", "Ongoing", risk="High"),
        ob(f, cp, "Extend better pricing to Adventure Works within 30 days",
           "If Northwind offers better prices to a Similarly Situated Customer, notify Adventure Works in writing within 30 days and extend those prices retroactively to the date first offered.",
           "Section 4.2", S_AW_MFN2, "Northwind", "Compliance & audit", "Event-driven",
           triggerEvent="Northwind offers more favorable Product pricing to a Similarly Situated Customer", risk="High",
           isTrap=True, trapType="event-driven"),
        ob(f, cp, "Decide on Adventure Works renewal before expiry",
           f"The agreement expires {iso(exp)} with no automatic renewal; any renewal needs a signed written agreement, so decide and negotiate before expiry.",
           "Section 5.1", s_term, "Both", "Notice & renewal", "Fixed date", "None", exp, risk="High",
           isTrap=True, trapType="fixed-expiry"),
        ob(f, cp, "Adventure Works: pay per standard credit terms",
           "Adventure Works pays for its purchase orders on Northwind's standard credit terms approved for it; those terms aren't in the Contracts library.",
           "Section 2.2", "Payment terms are set out in Reseller's standard credit terms approved for Customer.",
           "Counterparty", "Payment", "Event-driven",
           triggerEvent="Adventure Works places a purchase order (payment terms in Northwind's standard credit terms)",
           risk="Medium", expected="hold",
           reason="Protected payment obligation whose terms are only in Northwind's standard credit terms, which aren't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms.",
           isTrap=True, trapType="missing-document"),
    ]
    man = dict(fileName=f, title="Reseller Agreement", counterparty=cp, northwindRole="Reseller",
               contractType="Customer agreement", effectiveDate=iso(eff), expirationDate=iso(exp), autoRenews="No",
               noticePeriodDays=None, governingLaw="Oregon, USA", contractValue=800000, businessUnit="Sales", amends=None)
    return obs, man


# ---------------------------------------------------------------- 10 Fourth Coffee
S_FC_UNIFORM = "Supplier staff shall wear uniforms and visible identification badges while working at the Cafe."
S_FC_POC = ('Each Party shall designate a point of contact for day-to-day communications regarding the Services (each, '
            'a "Point of Contact").')
S_FC_INV = "Invoices shall be sent to accounts.payable@northwind.example."
S_FC_COOP = "The Parties shall cooperate in good faith in the performance of this Agreement."
S_FC_FOOD = ("Supplier shall deliver to Customer a copy of its annual food-safety inspection certificate, issued by an "
             "accredited third-party inspector, by March 1 of each year.")
S_FC_TFC = ("Either Party may terminate this Agreement for convenience by giving the other Party at least sixty (60) "
            "days' prior written notice.")
S_FC_HEAD = "Headings are for convenience only and do not affect the interpretation of this Agreement."
S_FC_BADGE = ("Supplier staff will be issued contractor access badges under Customer's standard visitor and contractor "
              "access procedures.")


def c10(path):
    f = "10-Fourth-Coffee-Facilities-Services-Agreement.docx"
    cp = "Fourth Coffee"
    eff = date(2025, 3, 1)
    food_next = date(2027, 3, 1)
    excl = "Routine administration: no deadline, deliverable or business consequence for a contract manager to track."

    d = Doc("Fourth Coffee  |  Facilities Services Agreement  |  Confidential", "Agreement No. FC-NW-FSA-2025-03", "Facilities Services Agreement - Fourth Coffee")
    d.title("Facilities Services Agreement", "On-Site Cafe Services  |  Agreement No. FC-NW-FSA-2025-03")
    d.para(f'This Facilities Services Agreement (this "Agreement") is entered into as of {fd(eff)} (the "Effective Date") '
           f'between Fourth Coffee, a Washington corporation with offices at 812 Roastery Lane, Seattle, Washington 98134 '
           f'("Supplier"), and Northwind Traders, Inc., a Washington corporation with offices at {NW_ADDR} ("Customer"). '
           f'Supplier and Customer are each a "Party."')
    d.recitals([
        "Supplier operates specialty coffee cafes and provides on-site cafe services to corporate campuses in the Puget Sound region.",
        "Customer wishes to make an on-site cafe available to its employees and visitors at its Seattle headquarters.",
        "The Parties wish to record the arrangements under which Supplier will operate that cafe.",
    ])
    d.para("The Parties therefore agree as follows:")

    d.heading("1. Services")
    d.section("1.1", "Scope", f'The services under this Agreement consist of the operation of an on-site espresso and light-food cafe on the first floor of Customer\'s headquarters at {NW_ADDR} (the "Cafe"), as further described in Exhibit A (the "Services").')
    d.section("1.2", "Commercial Model", "Supplier sells food and beverages directly to Cafe patrons and retains all Cafe sales revenue. Customer makes the Cafe space, utilities and existing fixtures available to Supplier at no charge, and no fees are payable by either Party under this Agreement.")
    d.section("1.3", "Hours", "The Cafe's regular hours are 7:00 a.m. to 3:00 p.m. Pacific Time on Customer business days, or such other hours as the Points of Contact may agree from time to time.")
    d.section("1.4", "Staff Appearance", S_FC_UNIFORM)
    d.section("1.5", "Signage", "Supplier may display its trade name and menu boards at the Cafe counter in a manner consistent with Customer's building signage standards.")

    d.heading("2. Administration")
    d.section("2.1", "Points of Contact", S_FC_POC)
    d.section("2.2", "Catering Orders and Invoices", "Catering orders placed by Customer departments are governed by separate purchase orders. " + S_FC_INV)
    d.section("2.3", "Cooperation", S_FC_COOP)
    d.section("2.4", "Feedback", "Customer may share employee feedback about the Cafe with Supplier's Point of Contact from time to time, and the Points of Contact may meet as they consider useful.")
    d.section("2.5", "Building Access", S_FC_BADGE)

    d.heading("3. Food Safety")
    d.section("3.1", "Permits", "Supplier holds a valid food establishment permit issued by Public Health - Seattle & King County for the Cafe.")
    d.section("3.2", "Annual Inspection Certificate", S_FC_FOOD)

    d.heading("4. Term and Termination")
    d.section("4.1", "Term", "This Agreement begins on the Effective Date and continues until terminated under this Article 4.")
    d.section("4.2", "Termination for Convenience", S_FC_TFC)
    d.section("4.3", "Termination for Cause", "Either Party may terminate this Agreement immediately by written notice if the other Party materially breaches this Agreement and the breach is not capable of cure.")
    d.section("4.4", "Equipment", "On termination, Supplier may remove its own espresso machines, grinders and portable equipment from the Cafe.")

    d.heading("5. General")
    d.section("5.1", "Headings", S_FC_HEAD)
    d.section("5.2", "Governing Law", "This Agreement is governed by the laws of the State of Washington, and the courts of King County, Washington have exclusive jurisdiction.")
    d.section("5.3", "Relationship of the Parties", "The Parties are independent contractors. Supplier's staff are not employees of Customer.")
    d.section("5.4", "Notices", "Notices under this Agreement must be in writing and delivered to the addresses set out above.")
    d.section("5.5", "No Third-Party Beneficiaries", "This Agreement is for the sole benefit of the Parties, and nothing in it confers any right on any other person.")
    d.section("5.6", "Severability", "If any provision of this Agreement is held unenforceable, the remaining provisions continue in effect.")
    d.section("5.7", "Force Majeure", "Neither Party is responsible for any failure to perform caused by events beyond its reasonable control, such as utility outages, severe weather or public-health orders.")
    d.section("5.8", "Entire Agreement; Counterparts", "This Agreement, including its Exhibits, is the entire agreement between the Parties regarding its subject matter. It may be signed in counterparts, including electronically.")

    d.signatures([
        {"company": "Fourth Coffee", "name": "Isabelle Grant", "title": "Regional Operations Manager", "date": date(2025, 2, 24)},
        {"company": "Northwind Traders, Inc.", "name": "Rafael Ortiz", "title": "Director, Workplace and Facilities", "date": date(2025, 2, 26)},
    ])
    d.heading("Exhibit A - Cafe Service Description")
    d.table([
        ["Item", "Description"],
        ["Location", "Level 1 atrium, 4100 Harbor View Drive, Seattle"],
        ["Menu", "Espresso drinks, drip coffee, tea, pastries and grab-and-go sandwiches and salads"],
        ["Seating", "Approximately 40 seats shared with the atrium lounge"],
        ["Payment methods", "Credit and debit cards and mobile wallets; no cash"],
        ["Provided by Customer", "Space, utilities, guest Wi-Fi, existing counters and refrigerated display case"],
    ], widths=[1.8, 4.7])
    d.heading("Exhibit B - Equipment Schedule")
    d.table([
        ["Equipment", "Owner", "Notes"],
        ["Two-group espresso machine", "Supplier", "Removable on termination (Section 4.4)"],
        ["Coffee grinders (3)", "Supplier", "Removable on termination (Section 4.4)"],
        ["Point-of-sale terminal", "Supplier", "Card and mobile-wallet payments only"],
        ["Service counters and casework", "Customer", "Existing building fixtures"],
        ["Refrigerated display case", "Customer", "Existing building fixture"],
    ], widths=[2.4, 1.2, 2.9])

    d.save(path / f)

    obs = [
        ob(f, cp, "Give 60 days' notice to terminate for convenience",
           "Either party can end the cafe agreement for convenience, but only with at least 60 days' prior written notice.",
           "Section 4.2", S_FC_TFC, "Both", "Notice & renewal", "Event-driven",
           triggerEvent="Either party decides to terminate the agreement for convenience", risk="Medium"),
        ob(f, cp, "Obtain Fourth Coffee food-safety certificate by Mar 1",
           "Fourth Coffee must deliver its annual third-party food-safety inspection certificate to Northwind by March 1 each year.",
           "Section 3.2", S_FC_FOOD, "Counterparty", "Compliance & audit", "Recurring", "Annual", food_next, risk="Medium"),
        ob(f, cp, "Supplier staff wear uniforms and badges",
           "Cafe staff wear uniforms and ID badges.", "Section 1.4", S_FC_UNIFORM, "Counterparty", "Other", "Ongoing",
           risk="Low", expected="exclude", reason=excl, isTrap=True, trapType="routine-admin"),
        ob(f, cp, "Designate a point of contact",
           "Each party names a day-to-day point of contact.", "Section 2.1", S_FC_POC, "Both", "Other", "Ongoing",
           risk="Low", expected="exclude", reason=excl, isTrap=True, trapType="routine-admin"),
        ob(f, cp, "Send invoices to accounts payable mailbox",
           "Catering invoices go to accounts.payable@northwind.example.", "Section 2.2", S_FC_INV, "Counterparty", "Other",
           "Ongoing", risk="Low", expected="exclude", reason=excl, isTrap=True, trapType="routine-admin"),
        ob(f, cp, "Cooperate in good faith",
           "The parties cooperate in good faith.", "Section 2.3", S_FC_COOP, "Both", "Other", "Ongoing",
           risk="Low", expected="exclude", reason=excl, isTrap=True, trapType="routine-admin"),
        ob(f, cp, "Issue contractor access badges to cafe staff",
           "Cafe staff receive contractor badges under Northwind's standard access procedures.", "Section 2.5", S_FC_BADGE,
           "Northwind", "Other", "Ongoing", risk="Low", expected="exclude", reason=excl, isTrap=True, trapType="routine-admin"),
        ob(f, cp, "Headings are for convenience only",
           "Interpretive boilerplate; headings do not affect meaning.", "Section 5.1", S_FC_HEAD, "Both", "Other", "Ongoing",
           risk="Low", expected="exclude", reason="Interpretive boilerplate, not an obligation of either party.",
           isTrap=True, trapType="routine-admin"),
    ]
    man = dict(fileName=f, title="Facilities Services Agreement", counterparty=cp, northwindRole="Customer",
               contractType="Supplier agreement", effectiveDate=iso(eff), expirationDate=None, autoRenews="No",
               noticePeriodDays=60, governingLaw="Washington, USA", contractValue=None, businessUnit="Facilities", amends=None)
    return obs, man


# ---------------------------------------------------------------- 11 Woodgrove Bank
S_WB_INT = ("The Borrower shall pay accrued interest on all outstanding Advances monthly in arrears on the first (1st) "
            "day of each calendar month.")
S_WB_REPAY = ("The Borrower shall repay all outstanding Advances, together with accrued and unpaid interest, on the "
              "Maturity Date.")
S_WB_CLOSEFEE = ("As a condition to the effectiveness of this Agreement, the Borrower shall pay the Bank, on the Closing "
                 "Date, a facility fee of $25,000 and the Bank's reasonable legal fees incurred in preparing this Agreement.")
S_WB_CERT = ("Within forty-five (45) days after the end of each fiscal quarter of the Borrower, commencing with the "
             "fiscal quarter ending December 31, 2026, the Borrower shall deliver to the Bank a compliance certificate "
             "signed by its chief financial officer, together with unaudited consolidated financial statements for that "
             "quarter, demonstrating compliance with Section 4.1.")
S_WB_AUD = ("Within one hundred twenty (120) days after the end of each fiscal year of the Borrower, which ends on June "
            "30, commencing with the fiscal year ending June 30, 2027, the Borrower shall deliver to the Bank audited "
            "consolidated financial statements reported on without qualification by an independent certified public "
            "accounting firm.")
S_WB_DEF = ("The Borrower shall notify the Bank in writing within five (5) Business Days after any officer of the "
            "Borrower becomes aware of any Default or Event of Default, describing it and the action the Borrower "
            "proposes to take.")
S_WB_LIQ = "The Borrower shall maintain Liquidity of not less than $5,000,000 at all times."
S_WB_POST = ("Within sixty (60) days after the Closing Date, the Borrower shall deliver to the Bank lender's loss payable "
             "and additional insured endorsements, in form satisfactory to the Bank, under the Borrower's property and "
             "general liability insurance policies.")
S_WB_CTP = ("This Agreement may be executed in counterparts, each of which is an original and all of which together "
            "constitute one instrument.")


def c11(path):
    f = "11-Woodgrove-Bank-Revolving-Credit-Facility.docx"
    cp = "Woodgrove Bank"
    close, mat = date(2026, 9, 15), date(2029, 9, 15)
    post = close + timedelta(days=60)
    cert_next = Q4_END + timedelta(days=45)
    aud_next = date(2027, 6, 30) + timedelta(days=120)
    int_next = date(2026, 12, 1)

    d = Doc("Woodgrove Bank  |  Revolving Credit Facility Letter Agreement  |  Confidential", "Facility No. WB-RCF-26-0915", "Revolving Credit Facility Letter Agreement - Woodgrove Bank")
    d.title("Revolving Credit Facility Letter Agreement", "Woodgrove Bank  |  Commercial Banking Group  |  500 Lexington Avenue, New York, New York 10022")
    d.para(fd(close), align="left")
    d.para(f"Northwind Traders, Inc.\n{NW_ADDR.replace(', Seattle', chr(10) + 'Seattle')}\nAttention: Daniel Okafor, Chief Financial Officer", align="left")
    d.para("Re: $10,000,000 Revolving Credit Facility", bold=True, align="left")
    d.para("Ladies and Gentlemen:", align="left")
    d.para(f'Woodgrove Bank, a national banking association (the "Bank"), is pleased to confirm the terms on which it will make '
           f'available to Northwind Traders, Inc., a Washington corporation (the "Borrower"), a revolving credit facility (the '
           f'"Facility"). This letter agreement (this "Agreement") is effective as of {fd(close)} (the "Closing Date").')
    d.recitals([
        "The Borrower has requested the Facility to finance working capital and general corporate purposes, including seasonal inventory purchases.",
        "The Bank is willing to provide the Facility on the terms and subject to the conditions of this Agreement.",
    ], lead="Background")
    d.para("Accordingly, the Bank and the Borrower agree as follows:")

    d.heading("1. The Facility")
    d.section("1.1", "Commitment", 'Subject to this Agreement, the Bank will make revolving loans (each, an "Advance") to the Borrower from time to time before the Maturity Date in an aggregate principal amount outstanding at any time not exceeding $10,000,000 (the "Commitment").')
    d.section("1.2", "Maturity Date", f'"Maturity Date" means {fd(mat)}.')
    d.section("1.3", "Purpose", "Advances are available for working capital and general corporate purposes of the Borrower.")
    d.section("1.4", "Requests", "The Borrower may request an Advance by written request delivered to the Bank at least one (1) Business Day before the requested funding date.")
    d.section("1.5", "Certain Definitions", '"Business Day" means a day other than a Saturday, Sunday or day on which banks in New York, New York are authorized to close. "Default" means any event that, with notice or lapse of time or both, would become an Event of Default. "Liquidity" means the Borrower\'s unrestricted cash and cash equivalents held in deposit accounts with the Bank.')

    d.heading("2. Interest, Fees and Repayment")
    d.section("2.1", "Interest Rate", "Advances bear interest at one-month Term SOFR plus 2.25% per annum, calculated on the basis of a 360-day year and actual days elapsed.")
    d.section("2.2", "Interest Payments", S_WB_INT)
    d.section("2.3", "Repayment", S_WB_REPAY)
    d.section("2.4", "Closing Fees", S_WB_CLOSEFEE)
    d.section("2.5", "Prepayment", "The Borrower may prepay Advances at any time without premium or penalty.")

    d.heading("3. Reporting Covenants")
    d.section("3.1", "Quarterly Compliance Certificate", S_WB_CERT)
    d.section("3.2", "Annual Audited Financial Statements", S_WB_AUD)
    d.section("3.3", "Notice of Default", S_WB_DEF)

    d.heading("4. Financial Covenant")
    d.section("4.1", "Minimum Liquidity", S_WB_LIQ + " Compliance will be tested on the last day of each fiscal quarter and reported in each compliance certificate.")

    d.heading("5. Post-Closing Obligation")
    d.section("5.1", "Insurance Endorsements", S_WB_POST)

    d.heading("6. Events of Default")
    d.section("6.1", "Events", 'Each of the following is an "Event of Default": (a) the Borrower fails to pay any principal or interest within three (3) Business Days after it is due; (b) the Borrower fails to comply with Section 4.1; (c) the Borrower fails to comply with Article 3 or Article 5 and the failure continues for fifteen (15) days after notice from the Bank; or (d) any representation made by the Borrower in connection with this Agreement proves to have been materially incorrect when made.')
    d.section("6.2", "Remedies", "Upon an Event of Default, the Bank may terminate the Commitment and declare all outstanding Advances and accrued interest immediately due and payable.")

    d.heading("7. Miscellaneous")
    d.section("7.1", "Governing Law", "This Agreement is governed by the laws of the State of New York.")
    d.section("7.2", "Counterparts", S_WB_CTP)
    d.section("7.3", "Entire Agreement", "This Agreement is the entire agreement between the Bank and the Borrower regarding the Facility and supersedes the Bank's summary of terms dated August 4, 2026.")
    d.section("7.4", "Waiver of Jury Trial", "EACH OF THE BANK AND THE BORROWER IRREVOCABLY WAIVES ANY RIGHT TO TRIAL BY JURY IN ANY PROCEEDING ARISING OUT OF THIS AGREEMENT.")
    d.para("Please confirm the Borrower's acceptance of this Agreement by signing below.")

    d.signatures([
        {"company": "Woodgrove Bank", "name": "Jonathan Reyes", "title": "Senior Vice President", "date": close},
        {"company": "Accepted and agreed: Northwind Traders, Inc.", "name": "Daniel Okafor", "title": "Chief Financial Officer", "date": close},
    ], intro="Very truly yours,")

    d.save(path / f)

    obs = [
        ob(f, cp, "Deliver quarterly compliance certificate to Woodgrove",
           f"Within 45 days after each fiscal quarter end (starting with the quarter ending 2026-12-31), deliver a CFO-signed compliance certificate and unaudited quarterly financials (first due {iso(cert_next)}).",
           "Section 3.1", S_WB_CERT, "Northwind", "Reporting", "Recurring", "Quarterly", cert_next, risk="High"),
        ob(f, cp, "Deliver annual audited financials to Woodgrove",
           f"Within 120 days after each June 30 fiscal year end (starting FY ending 2027-06-30), deliver unqualified audited consolidated financial statements (first due {iso(aud_next)}).",
           "Section 3.2", S_WB_AUD, "Northwind", "Reporting", "Recurring", "Annual", aud_next, risk="High"),
        ob(f, cp, "Maintain minimum liquidity of $5,000,000",
           "Keep unrestricted cash held at Woodgrove of at least $5,000,000 at all times (tested each quarter end).",
           "Section 4.1", S_WB_LIQ, "Northwind", "Compliance & audit", "Ongoing", risk="High"),
        ob(f, cp, "Notify Woodgrove of any default within 5 business days",
           "Notify the bank in writing within 5 Business Days after any officer learns of a Default or Event of Default, describing it and the proposed response.",
           "Section 3.3", S_WB_DEF, "Northwind", "Compliance & audit", "Event-driven",
           triggerEvent="Any Northwind officer becomes aware of a Default or Event of Default", risk="High",
           isTrap=True, trapType="event-driven"),
        ob(f, cp, "Pay monthly interest on Woodgrove advances",
           "Pay accrued interest on outstanding Advances monthly in arrears on the 1st of each month.",
           "Section 2.2", S_WB_INT, "Northwind", "Payment", "Recurring", "Monthly", int_next, risk="High"),
        ob(f, cp, "Repay all Woodgrove advances at maturity",
           f"Repay all outstanding Advances plus accrued interest on the Maturity Date ({iso(mat)}).",
           "Section 2.3", S_WB_REPAY, "Northwind", "Payment", "Fixed date", "None", mat, risk="High"),
        ob(f, cp, "Deliver insurance endorsements to Woodgrove",
           f"Post-closing: deliver lender's loss payable and additional insured endorsements on property and liability policies within 60 days after the 2026-09-15 Closing Date (by {iso(post)}).",
           "Section 5.1", S_WB_POST, "Northwind", "Insurance", "Fixed date", "None", post, risk="High"),
        ob(f, cp, "Pay facility and legal fees at closing",
           "Closing-date condition: pay the $25,000 facility fee and the bank's legal fees on the Closing Date.",
           "Section 2.4", S_WB_CLOSEFEE, "Northwind", "Payment", "Fixed date", "None", close, risk="Low",
           expected="exclude",
           reason="Condition to effectiveness satisfied at closing on 2026-09-15 (the facility is in effect); no post-signature action remains.",
           isTrap=True, trapType="condition-precedent"),
        ob(f, cp, "Counterparts clause",
           "Execution mechanics only.", "Section 7.2", S_WB_CTP, "Both", "Other", "Ongoing", risk="Low",
           expected="exclude", reason="Routine boilerplate about how the agreement is signed; no obligation to track.",
           isTrap=True, trapType="routine-admin"),
    ]
    man = dict(fileName=f, title="Revolving Credit Facility Letter Agreement", counterparty=cp, northwindRole="Borrower",
               contractType="Financing", effectiveDate=iso(close), expirationDate=iso(mat), autoRenews="No",
               noticePeriodDays=None, governingLaw="New York, USA", contractValue=10000000, businessUnit="Finance",
               amends=None)
    return obs, man
