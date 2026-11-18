"""
make-assets.py — 07-auto-tag-everything
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/07-auto-tag-everything/make-assets.py
Or from this folder: python make-assets.py

Key demo narrative:
  - Filter Confidential/Restricted -> 3 results:
      Legal-Contract.docx     -> Confidential
      NDA-Agreement.docx      -> Confidential
      Salary-Bands.docx       -> Restricted
  - Filter Marketing department -> 2 results:
      Marketing-Proposal.docx -> Marketing
      Finance-Report.docx     -> Marketing (Q3 Marketing Campaign ROI Report, prepared by Finance for Marketing)
"""
import io, os, zipfile, struct, zlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def p(name):
    return os.path.join(ASSETS_DIR, name)

# ---------------------------------------------------------------------------
# DOCX helper
# ---------------------------------------------------------------------------
DOCX_CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

DOCX_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOCX_WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

DOCX_STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
</w:styles>'''

WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def xesc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def wp(text='', bold=False, size=None, align=None):
    ppr = ('<w:pPr><w:jc w:val="' + align + '"/></w:pPr>') if align else ''
    if not text:
        return '<w:p ' + WNS + '>' + ppr + '</w:p>'
    rpr = (('<w:b/>' if bold else '') +
           ('<w:sz w:val="' + str(size) + '"/><w:szCs w:val="' + str(size) + '"/>' if size else ''))
    rpr_tag = ('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''
    return ('<w:p ' + WNS + '>' + ppr + '<w:r>' + rpr_tag +
            '<w:t xml:space="preserve">' + xesc(text) + '</w:t></w:r></w:p>')

def wh1(text):
    return ('<w:p ' + WNS + '><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            '<w:r><w:t>' + xesc(text) + '</w:t></w:r></w:p>')

def wh2(text):
    return ('<w:p ' + WNS + '><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            '<w:r><w:t>' + xesc(text) + '</w:t></w:r></w:p>')

def write_docx(path, paras):
    body = '\n'.join(paras)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>' + body +
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
           '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
           '</w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', DOCX_CONTENT_TYPES)
        z.writestr('_rels/.rels', DOCX_RELS)
        z.writestr('word/_rels/document.xml.rels', DOCX_WORD_RELS)
        z.writestr('word/styles.xml', DOCX_STYLES)
        z.writestr('word/document.xml', doc)
    open(path, 'wb').write(buf.getvalue())
    print('  ' + path)

# ===========================================================================
# Generate assets
# ===========================================================================
print('Generating assets for 07-auto-tag-everything...')

# 1. HR-Policy.docx  — HR | Policy | Internal
write_docx(p('HR-Policy.docx'), [
    wh1('Contoso Employee Code of Conduct'),
    wp('Document Type: Policy | Department: Human Resources | Sensitivity: Internal'),
    wp('Version: 4.2 | Effective Date: January 1, 2025 | Owner: Chief People Officer'),
    wp(),
    wp('This Code of Conduct sets out the standards of professional behaviour expected of '
       'all Contoso employees, contractors, and representatives. Violations may result in '
       'disciplinary action up to and including termination.'),
    wp(),
    wh2('1. Workplace Behaviour'),
    wp('All employees are expected to treat colleagues, customers, and partners with respect, '
       'dignity, and professionalism at all times. Contoso is committed to a workplace free '
       'from discrimination, bullying, and intimidation. Offensive language, unwanted physical '
       'contact, and exclusionary behaviour are prohibited regardless of intent.'),
    wp(),
    wh2('2. Anti-Harassment Policy'),
    wp('Harassment of any kind — including but not limited to sexual harassment, racial harassment, '
       'or harassment based on age, disability, religion, gender identity, or sexual orientation '
       '— is strictly prohibited and will be treated as a serious disciplinary matter. '
       'Employees who experience or witness harassment should report it immediately to HR '
       'via the confidential hotline: 1-800-CONTOSO-HR or ethics@contoso.com.'),
    wp(),
    wh2('3. Conflicts of Interest'),
    wp('Employees must disclose any personal or financial interest that could conflict — or '
       'appear to conflict — with their responsibilities at Contoso. This includes board '
       'memberships, significant shareholdings in competitors or suppliers, and personal '
       'relationships with vendors. Disclosures must be submitted to Legal via the '
       'Conflicts of Interest register in SharePoint.'),
    wp(),
    wh2('4. Social Media Use'),
    wp('Employees must not share confidential business information, unreleased product details, '
       'financial data, or customer information on personal social media accounts. '
       'Employees may identify themselves as Contoso employees but must clarify that opinions '
       'are personal and not the views of the company. Refer to the Social Media Policy '
       '(HR-POL-042) for full guidelines.'),
    wp(),
    wh2('5. Disciplinary Procedures'),
    wp('Minor violations: verbal warning, followed by written warning if behaviour continues.'),
    wp('Serious violations: written warning or suspension with pay pending investigation.'),
    wp('Gross misconduct (theft, fraud, violence, data breach): summary dismissal.'),
    wp('All disciplinary matters are handled by HR in accordance with applicable employment law.'),
])

# 2. Marketing-Proposal.docx  — Marketing | Proposal | Internal
write_docx(p('Marketing-Proposal.docx'), [
    wh1('Q3 Brand Awareness Campaign Proposal'),
    wp('Document Type: Proposal | Department: Marketing | Sensitivity: Internal'),
    wp('Prepared by: Angela Morales, Head of Brand | Date: January 2025'),
    wp('Budget Request: $450,000 | Campaign Period: Q3 2025 (July-September)'),
    wp(),
    wp('This proposal requests approval for a $450,000 Q3 brand awareness campaign targeting '
       'enterprise decision-makers in the financial services and manufacturing verticals. '
       'The campaign has three components: digital advertising, an influencer partnership '
       'programme, and trade show presence at two major industry events.'),
    wp(),
    wh2('Component 1: Digital Advertising ($220,000)'),
    wp('Channels: LinkedIn Sponsored Content, Google Display Network, and programmatic retargeting.'),
    wp('Target audience: VP and C-suite in companies with 500+ employees in FS and manufacturing.'),
    wp('Key messages: thought leadership, AI-powered automation, enterprise reliability.'),
    wp('KPIs: 4.5M impressions, 18,000 clicks, 900 MQL conversions.'),
    wp('Agency: Fabrikam Creative Agency (existing MSA in place).'),
    wp(),
    wh2('Component 2: Influencer Partnership ($80,000)'),
    wp('Partner with 3 B2B technology influencers with combined LinkedIn following of 280,000.'),
    wp('Content: 2 sponsored posts each, 1 webinar co-host per influencer.'),
    wp('Expected reach: 560,000 impressions at $0.14 CPM.'),
    wp('Authenticity requirement: influencers must be genuine users of the platform (NFR licences provided).'),
    wp(),
    wh2('Component 3: Trade Show Presence ($150,000)'),
    wp('Event 1: Enterprise Technology Summit, Las Vegas, August 12-14. Booth cost: $85,000.'),
    wp('Event 2: Manufacturing Innovation Conference, Chicago, September 9-11. Booth cost: $65,000.'),
    wp('Expected qualified leads from trade shows: 350 combined.'),
    wp(),
    wh2('ROI Projections'),
    wp('Total campaign cost: $450,000'),
    wp('Projected MQLs generated: 1,250'),
    wp('Projected SQLs (20% conversion): 250'),
    wp('Projected closed won deals (15% of SQL): 37 deals'),
    wp('Average deal value: $42,000 (mid-market) = $1.55M projected revenue'),
    wp('3.4x ROI on campaign spend.'),
    wp(),
    wh2('Approval Required'),
    wp('Marketing VP sign-off: required by February 1, 2025'),
    wp('CFO sign-off for amounts over $100K: required by February 5, 2025'),
    wp('Campaign kick-off: March 1, 2025'),
])

# 3. Legal-Contract.docx  — Legal | Contract | CONFIDENTIAL
write_docx(p('Legal-Contract.docx'), [
    wp('CONFIDENTIAL', bold=True, size=32, align='center'),
    wp('This document is marked CONFIDENTIAL. It may only be accessed by authorised '
       'Legal and Executive team members. Do not distribute, forward, or reproduce '
       'without prior written consent from the Legal department.', align='center'),
    wp(),
    wh1('Software License and Services Agreement'),
    wp('Document Type: Contract | Department: Legal | Sensitivity: CONFIDENTIAL'),
    wp('Parties: Contoso Ltd. ("Licensor") and Trey Research Inc. ("Licensee")'),
    wp('Effective Date: January 15, 2025 | Term: 3 years (ending January 14, 2028)'),
    wp('Contract Reference: LEGAL-2025-0042'),
    wp(),
    wh2('1. License Grant'),
    wp('Contoso Ltd. grants Trey Research Inc. a non-exclusive, non-transferable, worldwide '
       'license to use Contoso CloudSuite Enterprise software for Trey Research\'s internal '
       'business operations only. The license covers up to 1,000 named users. Sublicensing, '
       'resale, and use by third parties are expressly prohibited.'),
    wp(),
    wh2('2. Service Level Agreement'),
    wp('Contoso warrants 99.9% monthly uptime for production instances ("Uptime SLA"). '
       'Downtime is measured monthly excluding scheduled maintenance windows (maximum 4 hours/month). '
       'SLA credits: 10% of monthly fee for each 0.1% below 99.9%; maximum credit 30% of monthly fee.'),
    wp(),
    wh2('3. Intellectual Property Ownership'),
    wp('All intellectual property in the Contoso CloudSuite platform, including source code, '
       'algorithms, UI designs, and documentation, remains the sole property of Contoso Ltd. '
       'Trey Research\'s data and configurations remain the property of Trey Research. '
       'Neither party acquires IP rights in the other party\'s materials through this agreement.'),
    wp(),
    wh2('4. Limitation of Liability'),
    wp('CONFIDENTIAL — FINANCIAL TERMS:'),
    wp('Contoso\'s total aggregate liability under this agreement is capped at $2,000,000 '
       '(two million US dollars), which represents approximately 2 years of contract value. '
       'Neither party shall be liable for indirect, consequential, or punitive damages. '
       'This limitation does not apply to wilful misconduct or breaches of confidentiality.'),
    wp(),
    wh2('5. Confidentiality'),
    wp('Both parties agree to treat the terms of this agreement as confidential. '
       'Neither party may disclose the financial terms, SLA metrics, or specific contractual '
       'provisions to third parties without prior written consent. This obligation survives '
       'termination of the agreement for a period of five (5) years.'),
])

# 4. Finance-Report.docx  — Marketing (department), Report, Internal
#    Explicitly a Marketing department document even though prepared by Finance
write_docx(p('Finance-Report.docx'), [
    wh1('Q3 Marketing Campaign ROI Report'),
    wp('Document Type: Report | Department: Marketing | Sensitivity: Internal'),
    wp('Prepared by: Finance Business Partnering Team | For: Marketing Leadership'),
    wp('Reporting Period: Q3 2025 (July-September) | Date: October 10, 2025'),
    wp(),
    wp('This report is produced by Finance for the Marketing department to analyse the '
       'financial return on Q3 marketing spend. All data is sourced from Salesforce CRM, '
       'Google Analytics, and the Finance general ledger. This is a Marketing department '
       'document; Finance acts as analytical support only.'),
    wp(),
    wh2('Q3 Marketing Spend Summary'),
    wp('Total Q3 marketing spend: $387,500 (approved budget: $400,000, underspend: $12,500)'),
    wp('Digital advertising: $195,000 (50%)'),
    wp('Events and trade shows: $112,000 (29%)'),
    wp('Content and creative: $54,000 (14%)'),
    wp('Tools and technology: $26,500 (7%)'),
    wp(),
    wh2('Pipeline Attribution'),
    wp('Marketing-sourced pipeline generated in Q3: $6.2M'),
    wp('Marketing-influenced pipeline (touched at least once): $11.8M'),
    wp('Marketing-sourced pipeline as % of total new business pipeline: 57%'),
    wp(),
    wh2('Cost Per Lead (CPL)'),
    wp('Total MQLs generated: 1,420'),
    wp('Total SQLs generated: 284 (20% MQL-to-SQL conversion rate)'),
    wp('Cost per MQL: $273'),
    wp('Cost per SQL: $1,365'),
    wp('Industry benchmark for B2B SaaS: CPL $250-350 (Contoso within range)'),
    wp(),
    wh2('Customer Acquisition Cost (CAC)'),
    wp('Closed deals attributed to Q3 marketing: 29 new logos'),
    wp('Average deal value: $41,800'),
    wp('Marketing CAC: $13,362 per customer'),
    wp('LTV:CAC ratio: 8.7:1 (target: 3:1 minimum — well above benchmark)'),
    wp(),
    wh2('Conclusion'),
    wp('Q3 marketing spend delivered a 16.0x return on investment based on closed revenue. '
       'The LinkedIn campaign outperformed all other channels on pipeline-per-dollar. '
       'Recommendation for Q4: increase LinkedIn budget by 20% and reduce print/event spend.'),
])

# 5. NDA-Agreement.docx  — Legal | Contract | CONFIDENTIAL
write_docx(p('NDA-Agreement.docx'), [
    wp('CONFIDENTIAL', bold=True, size=32, align='center'),
    wp('MUTUAL NON-DISCLOSURE AGREEMENT', bold=True, size=28, align='center'),
    wp(),
    wh1('Mutual Non-Disclosure Agreement'),
    wp('Document Type: Contract | Department: Legal | Sensitivity: CONFIDENTIAL'),
    wp('Parties: Contoso Ltd. ("Party A") and Adventure Works Ltd. ("Party B")'),
    wp('Effective Date: February 10, 2025 | NDA Reference: LEGAL-NDA-2025-0019'),
    wp(),
    wp('THIS AGREEMENT IS CONFIDENTIAL. The existence and terms of this NDA, '
       'and any Confidential Information exchanged under it, must not be disclosed '
       'to any third party without prior written consent from both parties.'),
    wp(),
    wh2('1. Definition of Confidential Information'),
    wp('For the purposes of this Agreement, "Confidential Information" means any information '
       'disclosed by either party to the other in connection with the Permitted Purpose, whether '
       'in writing, orally, electronically, or in any other form, that is designated as '
       'confidential or that reasonably should be understood to be confidential given the '
       'nature of the information and the circumstances of disclosure. This includes but is '
       'not limited to: business plans, product roadmaps, financial projections, customer lists, '
       'source code, pricing strategies, and personnel information.'),
    wp(),
    wh2('2. Obligations of Confidentiality'),
    wp('Each party agrees to: (a) hold the other party\'s Confidential Information in strict '
       'confidence; (b) not disclose Confidential Information to any third party without prior '
       'written consent; (c) use Confidential Information solely for the Permitted Purpose; '
       '(d) limit access to Confidential Information to those employees or contractors who '
       'have a genuine need to know and are bound by equivalent confidentiality obligations.'),
    wp(),
    wh2('3. Term'),
    wp('This Agreement is effective for a period of three (3) years from the Effective Date '
       '(i.e., until February 9, 2028). Confidentiality obligations survive expiry or '
       'termination of this Agreement for a further two (2) years.'),
    wp(),
    wh2('4. Exclusions'),
    wp('Obligations under this Agreement do not apply to information that: (a) is or becomes '
       'publicly known through no fault of the receiving party; (b) was already in the '
       'receiving party\'s possession prior to disclosure; (c) is independently developed '
       'by the receiving party without reference to the Confidential Information; '
       '(d) is required to be disclosed by law or court order, provided prompt written '
       'notice is given to the disclosing party.'),
    wp(),
    wh2('5. Remedies'),
    wp('The parties acknowledge that breach of this Agreement would cause irreparable harm '
       'for which monetary damages would be an inadequate remedy. Each party agrees that '
       'the other party is entitled to seek injunctive relief without bond or other security '
       'in addition to any other remedies available at law or in equity.'),
    wp(),
    wp('Signed on behalf of Contoso Ltd.: _______________________  Date: ___________'),
    wp('Signed on behalf of Adventure Works Ltd.: _____________  Date: ___________'),
])

# 6. Salary-Bands.docx  — HR | Report | RESTRICTED
write_docx(p('Salary-Bands.docx'), [
    wp('RESTRICTED - HR AND FINANCE ONLY', bold=True, size=32, align='center'),
    wp('This document is RESTRICTED. Access is limited to HR Business Partners, '
       'Finance Business Partners, and Executives with compensation approval authority. '
       'Do not share with employees, managers, or any other parties.', align='center'),
    wp(),
    wh1('FY2025 Compensation Bands by Level and Role'),
    wp('Document Type: Report | Department: Human Resources | Sensitivity: RESTRICTED'),
    wp('Version: FY2025 v1.0 | Effective: January 1, 2025 | Owner: Total Rewards, HR'),
    wp(),
    wp('This document contains salary ranges for all levels and roles at Contoso. '
       'Ranges reflect base salary only and exclude bonus, equity, and benefits. '
       'All figures are in USD. Ranges are reviewed annually and may be adjusted '
       'for regional cost-of-living. Contact Total Rewards for location-based guidance.'),
    wp(),
    wh2('Individual Contributor (IC) Levels'),
    wp('IC1 — Associate'),
    wp('  Engineering: $72,000 - $95,000'),
    wp('  Marketing:   $58,000 - $78,000'),
    wp('  Sales:       $55,000 - $72,000'),
    wp('  Operations:  $52,000 - $68,000'),
    wp(),
    wp('IC2 — Mid-Level'),
    wp('  Engineering: $95,000 - $125,000'),
    wp('  Marketing:   $78,000 - $102,000'),
    wp('  Sales:       $72,000 - $95,000'),
    wp('  Operations:  $68,000 - $88,000'),
    wp(),
    wp('IC3 — Senior'),
    wp('  Engineering: $125,000 - $160,000'),
    wp('  Marketing:   $102,000 - $132,000'),
    wp('  Sales:       $95,000 - $128,000'),
    wp('  Operations:  $88,000 - $115,000'),
    wp(),
    wp('IC4 — Staff / Senior II'),
    wp('  Engineering: $160,000 - $200,000'),
    wp('  Marketing:   $132,000 - $165,000'),
    wp('  Sales:       $128,000 - $160,000'),
    wp('  Operations:  $115,000 - $145,000'),
    wp(),
    wp('IC5 — Principal'),
    wp('  Engineering: $200,000 - $245,000'),
    wp('  Marketing:   $165,000 - $200,000'),
    wp('  Sales:       $160,000 - $195,000'),
    wp('  Operations:  $145,000 - $178,000'),
    wp(),
    wp('IC6 — Distinguished / Fellow'),
    wp('  Engineering: $245,000 - $310,000'),
    wp('  Marketing:   $200,000 - $250,000'),
    wp('  Sales:       $195,000 - $240,000'),
    wp('  Operations:  $178,000 - $220,000'),
    wp(),
    wh2('Manager (M) Levels'),
    wp('M1 — Manager'),
    wp('  Engineering: $150,000 - $185,000'),
    wp('  Marketing:   $125,000 - $155,000'),
    wp('  Sales:       $120,000 - $150,000'),
    wp('  Operations:  $110,000 - $138,000'),
    wp(),
    wp('M2 — Senior Manager'),
    wp('  Engineering: $185,000 - $225,000'),
    wp('  Marketing:   $155,000 - $190,000'),
    wp('  Sales:       $150,000 - $185,000'),
    wp('  Operations:  $138,000 - $170,000'),
    wp(),
    wp('M3 — Director'),
    wp('  Engineering: $225,000 - $275,000'),
    wp('  Marketing:   $190,000 - $235,000'),
    wp('  Sales:       $185,000 - $230,000'),
    wp('  Operations:  $170,000 - $210,000'),
    wp(),
    wp('M4 — Senior Director / VP'),
    wp('  Engineering: $275,000 - $350,000'),
    wp('  Marketing:   $235,000 - $295,000'),
    wp('  Sales:       $230,000 - $290,000'),
    wp('  Operations:  $210,000 - $265,000'),
    wp(),
    wp('RESTRICTED - HR AND FINANCE ONLY. Do not distribute.'),
])

print('Done. Files written to:', ASSETS_DIR)
