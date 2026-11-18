"""
Generate policy .docx files for the 03-find-the-needle demo.

Facts that MUST appear verbatim (the demo script references these explicitly):
  Travel-Policy:     $350 per night max hotel rate (international)
                     premium economy for flights over 6 hours
  Expense-Policy:    $75 per day meal reimbursement
                     expense report due by the 5th
  PTO-Policy:        2 weeks notice for PTO requests over 5 days
  Remote-Work-Policy: supporting context for the 7-day international trip question
"""

import zipfile, io, os, sys

sys.path.insert(0, os.path.dirname(__file__))

# ── OOXML helpers (identical to 04-comparison-report/make-assets.py) ─────────

CONTENT_TYPES = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="word/document.xml"/>
</Relationships>"""

WORD_RELS = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    Target="styles.xml"/>
</Relationships>"""

STYLES = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
</w:styles>"""


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def p(text='', bold=False, size=None, align=None):
    ppr = ('<w:pPr><w:jc w:val="' + align + '"/></w:pPr>') if align else ''
    if not text:
        return '<w:p ' + NS + '>' + ppr + '</w:p>'
    rpr = ('<w:b/>' if bold else '') + (
        '<w:sz w:val="' + str(size) + '"/><w:szCs w:val="' + str(size) + '"/>' if size else '')
    rpr_tag = ('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''
    return ('<w:p ' + NS + '>' + ppr + '<w:r>' + rpr_tag +
            '<w:t xml:space="preserve">' + esc(text) + '</w:t></w:r></w:p>')


def h1(text):
    return ('<w:p ' + NS + '><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')


def h2(text):
    return ('<w:p ' + NS + '><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')


def document_xml(paragraphs):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '  <w:body>\n' + '\n'.join(paragraphs) + '\n'
        '    <w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr>\n'
        '  </w:body>\n</w:document>'
    )


def write_docx(path, paragraphs):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', WORD_RELS)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/document.xml', document_xml(paragraphs))
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    print('  Written: ' + path)


# ── Travel Policy ─────────────────────────────────────────────────────────────

def make_travel_policy():
    return [
        p('Contoso Ltd.', bold=True, size=28, align='center'),
        p('CORPORATE TRAVEL POLICY', bold=True, size=32, align='center'),
        p('Policy No. HR-401  |  Effective: January 1, 2025  |  Owner: Finance', align='center'),
        p(),

        h1('1. PURPOSE AND SCOPE'),
        p('This policy establishes guidelines and reimbursement limits for all business travel '
          'undertaken by Contoso Ltd. employees. It applies to domestic and international travel '
          'booked on behalf of the company. Compliance is mandatory; exceptions require written '
          'pre-approval from a VP or above.'),
        p(),

        h1('2. BOOKING REQUIREMENTS'),
        h2('2.1 Advance Booking'),
        p('All flights must be booked at least fourteen (14) days in advance when possible. '
          'Last-minute bookings (fewer than 72 hours before departure) require manager approval '
          'and must be submitted with a business justification.'),
        h2('2.2 Preferred Vendors'),
        p('Employees must use the company travel portal (Contoso Travel Hub) for all bookings. '
          'Bookings made outside the portal are not eligible for reimbursement unless the portal '
          'was unavailable, documented with a screenshot.'),
        h2('2.3 Flight Class'),
        p('Economy class is required for all flights of six (6) hours or fewer. '
          'Premium economy is permitted for flights exceeding six (6) hours. '
          'Business class is not approved for individual contributors; it requires SVP-level '
          'approval and is generally reserved for C-suite travel or trips exceeding twelve (12) '
          'hours with back-to-back business commitments upon arrival.'),
        p(),

        h1('3. ACCOMMODATION'),
        h2('3.1 Hotel Rate Caps'),
        p('Reimbursable hotel rates are capped as follows:'),
        p('  - Domestic (US): $225 per night'),
        p('  - Canada and Mexico: $275 per night'),
        p('  - International (all other countries): $350 per night'),
        p('Rates are for the room only (excluding taxes and incidental charges, which are '
          'reimbursable separately). If rates in the destination city exceed these caps during '
          'a required travel window, employees must submit a rate exception request through '
          'the travel portal before booking.'),
        h2('3.2 Shared Rooms'),
        p('Employees are not required to share hotel rooms. Single-occupancy rooms are standard.'),
        h2('3.3 Alternative Accommodations'),
        p('Airbnb and similar short-term rentals are permitted only for stays of five (5) or more '
          'consecutive nights in the same city, subject to the same nightly rate caps.'),
        p(),

        h1('4. GROUND TRANSPORTATION'),
        p('Rental cars are approved when public transit or ride-share is unavailable or impractical. '
          'Standard or compact vehicle classes are required; SUVs and premium vehicles are not '
          'reimbursable unless no other class is available. Ride-share (Uber/Lyft) is reimbursable '
          'with receipt. Personal vehicle mileage is reimbursed at the current IRS standard rate.'),
        p(),

        h1('5. INTERNATIONAL TRAVEL'),
        h2('5.1 Pre-Travel Checklist'),
        p('Before any international trip, employees must: (a) register the trip in the travel '
          'portal at least five (5) business days before departure; (b) verify visa and passport '
          'validity (passport must be valid for at least six months beyond the return date); '
          '(c) enroll in the Contoso International SOS program if traveling to a Tier 2 or '
          'Tier 3 country.'),
        h2('5.2 Currency and Foreign Exchange'),
        p('Employees should use the corporate travel card for all international purchases. '
          'Cash advances up to $500 USD equivalent are available through Finance with five (5) '
          'business days notice. Currency conversion fees are reimbursable.'),
        h2('5.3 Travel Insurance'),
        p('Contoso provides comprehensive travel insurance for all employees on company-sanctioned '
          'international travel. Coverage includes medical evacuation, trip cancellation, and '
          'lost luggage. Employees should carry the insurance card (available in the travel portal) '
          'at all times during international travel.'),
        p(),

        h1('6. POLICY EXCEPTIONS'),
        p('Exceptions to any provision of this policy must be pre-approved in writing by a '
          'Director or above. Retroactive exceptions are not accepted. Unapproved out-of-policy '
          'expenses will not be reimbursed.'),
        p(),

        h1('7. CONTACT'),
        p('Questions about this policy should be directed to travel@contoso.com or the '
          'Finance Business Partners team in the HR portal.'),
    ]


# ── Expense Policy ────────────────────────────────────────────────────────────

def make_expense_policy():
    return [
        p('Contoso Ltd.', bold=True, size=28, align='center'),
        p('EMPLOYEE EXPENSE REIMBURSEMENT POLICY', bold=True, size=28, align='center'),
        p('Policy No. HR-402  |  Effective: January 1, 2025  |  Owner: Finance', align='center'),
        p(),

        h1('1. PURPOSE'),
        p('This policy outlines the process for submitting, approving, and reimbursing '
          'business expenses incurred by Contoso Ltd. employees in the course of their duties. '
          'All expenses must be legitimate, reasonable, and directly related to business activities.'),
        p(),

        h1('2. ELIGIBLE EXPENSES'),
        h2('2.1 Meals and Entertainment'),
        p('Meal expenses incurred while traveling on company business are reimbursable as follows:'),
        p('  - Breakfast: up to $20'),
        p('  - Lunch: up to $25'),
        p('  - Dinner: up to $30'),
        p('  - Daily meal total (per diem): $75 per day'),
        p('The per diem rate of $75 per day applies when an employee is traveling away from '
          'their primary work location and includes all meals for that calendar day. '
          'Alcohol is not reimbursable unless part of a client entertainment event approved '
          'in advance by a Director or above.'),
        h2('2.2 Client Entertainment'),
        p('Business meals with clients or prospects (not travel meals) require prior approval '
          'from a manager and must include the names and companies of all attendees in the '
          'expense report. Client entertainment meals are reimbursed at actual cost with receipt, '
          'up to $100 per person.'),
        h2('2.3 Office Supplies and Equipment'),
        p('Purchases up to $50 may be expensed without pre-approval. Items between $50 and $250 '
          'require manager approval. Anything above $250 must go through the procurement process.'),
        p(),

        h1('3. EXPENSE REPORT SUBMISSION'),
        h2('3.1 Submission Deadline'),
        p('Expense reports must be submitted no later than the 5th of the month following the '
          'month in which the expense was incurred. For example, expenses incurred in March must '
          'be submitted by April 5th. Late submissions may result in delayed reimbursement and '
          'repeated lateness may be escalated to HR.'),
        h2('3.2 Required Documentation'),
        p('All expenses require an itemized receipt. Credit card statements are not accepted '
          'as sole documentation. For expenses over $25, the business purpose must be noted '
          'in the description field of the expense report.'),
        h2('3.3 Submission Process'),
        p('Expenses must be submitted through the Contoso Expense portal (expense.contoso.com). '
          'Paper expense reports are no longer accepted as of January 1, 2024. '
          'Expenses submitted more than ninety (90) days after the transaction date will not '
          'be reimbursed.'),
        p(),

        h1('4. APPROVAL WORKFLOW'),
        p('Expense reports are routed automatically to the direct manager for approval. '
          'Managers have five (5) business days to approve or reject. Rejected expenses will '
          'include a reason; employees may resubmit with corrections. Finance reviews and '
          'processes approved reports in the next payment cycle.'),
        p(),

        h1('5. PAYMENT'),
        p('Approved reimbursements are paid via direct deposit to the bank account on file '
          'in Workday. Payment is processed in the bi-weekly payroll cycle following approval. '
          'Reimbursements are not subject to tax withholding as long as they are substantiated '
          'with receipts.'),
        p(),

        h1('6. CORPORATE CARD'),
        p('Employees who travel more than four (4) times per year are eligible for a Contoso '
          'corporate travel card. The corporate card must be used for all travel bookings and '
          'incidentals where accepted. Personal expenses charged to the corporate card must be '
          'reimbursed to the company within thirty (30) days.'),
        p(),

        h1('7. NON-REIMBURSABLE EXPENSES'),
        p('The following are explicitly not reimbursable: personal entertainment, fines or '
          'traffic violations, first-class airfare, minibar charges, gym fees, personal '
          'grooming, clothing (except safety equipment required for a job site), and expenses '
          'lacking receipts.'),
        p(),

        h1('8. CONTACT'),
        p('For questions, contact expenses@contoso.com. For portal access issues, contact '
          'IT Help Desk at helpdesk.contoso.com.'),
    ]


# ── Remote Work Policy ────────────────────────────────────────────────────────

def make_remote_work_policy():
    return [
        p('Contoso Ltd.', bold=True, size=28, align='center'),
        p('REMOTE AND HYBRID WORK POLICY', bold=True, size=28, align='center'),
        p('Policy No. HR-403  |  Effective: March 1, 2025  |  Owner: People Operations', align='center'),
        p(),

        h1('1. PURPOSE'),
        p('Contoso Ltd. supports flexible work arrangements that balance employee autonomy '
          'with business needs. This policy defines eligibility, expectations, and equipment '
          'provisions for remote and hybrid employees.'),
        p(),

        h1('2. ELIGIBILITY'),
        p('Remote and hybrid arrangements are available to full-time employees who: '
          '(a) have completed at least ninety (90) days of employment; '
          '(b) are in a role designated as remote-eligible by their manager and HR; and '
          '(c) maintain satisfactory performance standing. '
          'Arrangements are subject to annual review and may be modified based on business needs.'),
        p(),

        h1('3. WORK ARRANGEMENTS'),
        h2('3.1 Hybrid'),
        p('Hybrid employees are expected to be on-site a minimum of two (2) days per week, '
          'typically Tuesday and Thursday unless otherwise agreed with their manager. '
          'Core collaboration hours (10 AM - 3 PM local time) must be observed on in-office days.'),
        h2('3.2 Fully Remote'),
        p('Fully remote employees must be available during their team\'s core hours and are '
          'expected to travel to a Contoso office at least once per quarter for team events, '
          'planning sessions, or other business needs. Travel costs for required on-site visits '
          'are reimbursed per the Corporate Travel Policy (HR-401).'),
        h2('3.3 Working from a Different Country'),
        p('Employees wishing to work remotely from outside their country of employment for '
          'more than fourteen (14) consecutive days must obtain prior written approval from '
          'their manager, HR, and Legal. Tax and immigration implications vary by country and '
          'will be assessed on a case-by-case basis. Unapproved international remote work '
          'may result in disciplinary action.'),
        p(),

        h1('4. HOME OFFICE REQUIREMENTS'),
        p('Remote employees must maintain a dedicated workspace with: reliable broadband internet '
          '(minimum 25 Mbps download), a quiet environment suitable for video calls, and '
          'adequate lighting. Employees are responsible for their internet costs; '
          'a monthly home office stipend of $50 is provided to offset connectivity expenses.'),
        p(),

        h1('5. EQUIPMENT'),
        p('Contoso provides all remote employees with a laptop, headset, and monitor upon '
          'request. Additional peripherals (keyboard, webcam, docking station) may be requested '
          'through IT and are approved at manager discretion up to a $300 one-time budget '
          'per employee. Equipment remains Contoso property and must be returned upon '
          'termination.'),
        p(),

        h1('6. INTERNATIONAL TRAVEL COMBINED WITH REMOTE WORK'),
        p('"Workcations" — combining leisure travel with remote work internationally — are '
          'permitted for up to fourteen (14) consecutive days per calendar year with manager '
          'approval. Employees must ensure they have adequate internet access and remain '
          'available during their standard work hours. The company does not reimburse '
          'personal travel costs associated with workcations. All applicable travel '
          'compliance requirements (visa, tax) remain the employee\'s responsibility.'),
        p(),

        h1('7. PERFORMANCE AND AVAILABILITY'),
        p('Remote employees are held to the same performance standards as on-site employees. '
          'Managers will conduct quarterly check-ins specifically addressing remote work '
          'effectiveness. Persistent availability issues or performance concerns may result '
          'in the arrangement being modified or revoked.'),
        p(),

        h1('8. SECURITY'),
        p('Remote employees must: use Contoso VPN when accessing internal systems; '
          'never use public Wi-Fi without VPN; lock their screen when stepping away; '
          'and comply with all provisions of the Information Security Policy (IT-201). '
          'Violations may result in immediate suspension of remote work privileges.'),
        p(),

        h1('9. CONTACT'),
        p('For remote work arrangement requests, contact your HR Business Partner. '
          'For IT equipment, contact helpdesk.contoso.com.'),
    ]


# ── PTO Policy ────────────────────────────────────────────────────────────────

def make_pto_policy():
    return [
        p('Contoso Ltd.', bold=True, size=28, align='center'),
        p('PAID TIME OFF (PTO) POLICY', bold=True, size=28, align='center'),
        p('Policy No. HR-404  |  Effective: January 1, 2025  |  Owner: People Operations', align='center'),
        p(),

        h1('1. PURPOSE'),
        p('Contoso Ltd. provides Paid Time Off (PTO) to support employee wellbeing and '
          'work-life balance. This policy describes accrual, usage, approval, and carryover '
          'rules for all full-time employees in the United States.'),
        p(),

        h1('2. ACCRUAL'),
        p('PTO accrues on a bi-weekly basis according to the following schedule:'),
        p('  - Years 0-2:   15 days per year (5.77 hours per pay period)'),
        p('  - Years 3-5:   18 days per year (6.92 hours per pay period)'),
        p('  - Years 6+:    22 days per year (8.46 hours per pay period)'),
        p('Accrual begins on the first day of employment. PTO is available for use as it '
          'accrues; employees may not take PTO in advance of accrual without manager approval.'),
        p(),

        h1('3. REQUESTING TIME OFF'),
        h2('3.1 Standard Requests (5 days or fewer)'),
        p('PTO requests of five (5) days or fewer should be submitted in Workday at least '
          'five (5) business days in advance. Managers are expected to respond within '
          'two (2) business days. Approval is generally granted unless there is a significant '
          'business conflict.'),
        h2('3.2 Extended Requests (more than 5 days)'),
        p('PTO requests exceeding five (5) consecutive days require a minimum of two (2) '
          'weeks advance notice to allow for adequate coverage planning. Requests should be '
          'submitted in Workday and discussed with your manager before submission. '
          'Extended requests during peak business periods (Q4, end-of-quarter close) '
          'are subject to additional review and may be adjusted.'),
        h2('3.3 Emergency and Unplanned Absence'),
        p('If you are unable to provide advance notice due to illness or emergency, '
          'notify your manager as soon as possible — ideally before your scheduled start time. '
          'Unplanned absences of more than three (3) consecutive days require a note from '
          'a licensed healthcare provider.'),
        p(),

        h1('4. CARRYOVER AND CASH-OUT'),
        p('Employees may carry over up to ten (10) unused PTO days into the following calendar '
          'year. Any balance above ten (10) days is forfeited on December 31st. '
          'Contoso does not offer PTO cash-out for unused days, except upon termination of '
          'employment, where accrued and unused PTO is paid out per applicable state law.'),
        p(),

        h1('5. HOLIDAYS'),
        p('Contoso observes eleven (11) company holidays per year. Holiday schedules are '
          'published in the HR portal by November 1st of the preceding year. Holidays do not '
          'count against PTO balances. Employees required to work on a company holiday receive '
          'an additional floating holiday, to be used within ninety (90) days.'),
        p(),

        h1('6. BEREAVEMENT LEAVE'),
        p('Employees may take up to five (5) days of paid bereavement leave for the death of '
          'an immediate family member (spouse, child, parent, sibling). Three (3) days are '
          'provided for extended family (grandparent, in-law, aunt/uncle). Bereavement leave '
          'does not count against PTO balances.'),
        p(),

        h1('7. JURY DUTY'),
        p('Employees summoned for jury duty receive full pay for up to ten (10) business days. '
          'Extended jury service beyond ten days is paid at 60% of base salary. '
          'Employees must provide the summons to HR and notify their manager promptly.'),
        p(),

        h1('8. CONTACT'),
        p('For questions about your PTO balance, contact your HR Business Partner or '
          'review your balance in Workday. For policy questions, contact hr@contoso.com.'),
    ]


# ── Generate ──────────────────────────────────────────────────────────────────

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(out_dir, exist_ok=True)

write_docx(os.path.join(out_dir, 'Travel-Policy.docx'), make_travel_policy())
write_docx(os.path.join(out_dir, 'Expense-Policy.docx'), make_expense_policy())
write_docx(os.path.join(out_dir, 'Remote-Work-Policy.docx'), make_remote_work_policy())
write_docx(os.path.join(out_dir, 'PTO-Policy.docx'), make_pto_policy())

print('Done.')
