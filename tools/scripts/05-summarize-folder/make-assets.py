"""
make-assets.py — 05-summarize-folder
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/05-summarize-folder/make-assets.py
Or from this folder: python make-assets.py

CRITICAL numbers that must survive into the output so Copilot can surface them:
  - 18% market growth        → market-analysis.docx
  - Three named priorities   → product-priorities.docx
  - $12.5M revenue target    → sales-forecast.xlsx
  - $1.8M renewal risk       → sales-forecast.xlsx
  - $300K budget overage     → budget-request.docx
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

# ---------------------------------------------------------------------------
# XLSX helper
# ---------------------------------------------------------------------------
XLSX_CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>'''

XLSX_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

XLSX_WB_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''

def write_xlsx(path, sheet_name, rows):
    strings = []
    idx_map = {}

    def si(s):
        s = str(s)
        if s not in idx_map:
            idx_map[s] = len(strings)
            strings.append(s)
        return idx_map[s]

    cell_data = []
    for r_idx, row in enumerate(rows):
        crow = []
        for c_idx, val in enumerate(row):
            col_letter = chr(ord('A') + c_idx)
            cell_ref = col_letter + str(r_idx + 1)
            if isinstance(val, (int, float)):
                crow.append((cell_ref, 'n', str(val)))
            else:
                crow.append((cell_ref, 's', str(si(val))))
        cell_data.append(crow)

    ss_items = ''.join('<si><t xml:space="preserve">' + xesc(s) + '</t></si>' for s in strings)
    ss_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
              'count="' + str(len(strings)) + '" uniqueCount="' + str(len(strings)) + '">'
              + ss_items + '</sst>')

    rows_xml = ''
    for r_idx, crow in enumerate(cell_data):
        cells = ''
        for ref, t, v in crow:
            if t == 's':
                cells += '<c r="' + ref + '" t="s"><v>' + v + '</v></c>'
            else:
                cells += '<c r="' + ref + '"><v>' + v + '</v></c>'
        rows_xml += '<row r="' + str(r_idx + 1) + '">' + cells + '</row>'

    sheet_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                 '<sheetData>' + rows_xml + '</sheetData></worksheet>')

    wb_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
              'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
              '<sheets><sheet name="' + xesc(sheet_name) + '" sheetId="1" r:id="rId1"/></sheets>'
              '</workbook>')

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', XLSX_CONTENT_TYPES)
        z.writestr('_rels/.rels', XLSX_RELS)
        z.writestr('xl/_rels/workbook.xml.rels', XLSX_WB_RELS)
        z.writestr('xl/workbook.xml', wb_xml)
        z.writestr('xl/worksheets/sheet1.xml', sheet_xml)
        z.writestr('xl/sharedStrings.xml', ss_xml)
    open(path, 'wb').write(buf.getvalue())
    print('  ' + path)

# ===========================================================================
# Generate assets
# ===========================================================================
print('Generating assets for 05-summarize-folder...')

# 1. market-analysis.docx  — must contain "18%" market growth
write_docx(p('market-analysis.docx'), [
    wh1('Q4 Market Analysis'),
    wp('Prepared by: Strategy & Insights Team | Date: October 2025 | Classification: Internal'),
    wp(),
    wh2('Executive Summary'),
    wp('The addressable market for cloud-based business automation software is growing at '
       '18% year-over-year, driven by accelerating enterprise digital transformation, '
       'increased AI adoption in workflows, and the continued normalization of distributed work. '
       'This 18% growth rate exceeds our prior forecast of 14% and represents a significant '
       'opportunity for Contoso to capture additional market share in Q4 and into FY2026. '
       'Total addressable market (TAM) is estimated at $2.4 billion globally.'),
    wp(),
    wh2('Market Size'),
    wp('Total Addressable Market (TAM): $2.4 billion (2025, global)'),
    wp('Serviceable Addressable Market (SAM): $680 million (English-speaking enterprise, 200+ seats)'),
    wp('Serviceable Obtainable Market (SOM): $82 million (current competitive position)'),
    wp('YoY market growth rate: 18% — up from 14% in Q3 analysis'),
    wp(),
    wh2('Competitive Landscape'),
    wp('Three primary competitors have been identified in our target segment:'),
    wp(),
    wp('1. Fabrikam Automation — Market share 22%. Strong in manufacturing and logistics verticals. '
       'Recently launched an AI-assisted workflow builder. Pricing is 15% below Contoso on average. '
       'Key weakness: poor enterprise SSO support and limited audit logging.'),
    wp(),
    wp('2. Northwind Process Suite — Market share 18%. Focus on financial services and healthcare. '
       'Compliance certifications (FedRAMP, HIPAA) are a differentiator. Heavy services dependency '
       'creates long sales cycles. Net Promoter Score reported at 31 (below our 44).'),
    wp(),
    wp('3. Adventure Works Cloud — Market share 9%. Startup with aggressive pricing and modern UX. '
       'Growing fastest in SMB segment (not our primary target). Lacks enterprise SLA, no dedicated '
       'account management. Risk to watch in FY2026 as they mature upmarket.'),
    wp(),
    wh2('Customer Segments'),
    wp('Segment 1 — Enterprise (1000+ employees): 58% of our revenue. Average contract value $180K/yr. '
       'Churn rate 6%. Growth opportunity: upsell AI module to existing accounts.'),
    wp('Segment 2 — Mid-Market (200-999 employees): 33% of revenue. Average contract value $42K/yr. '
       'Churn rate 11%. Growth opportunity: self-serve onboarding to reduce CAC.'),
    wp('Segment 3 — SMB (<200 employees): 9% of revenue. Low margin, high churn. '
       'Currently being reviewed for strategic fit — may exit this segment in FY2026.'),
    wp(),
    wh2('Key Trends'),
    wp('Trend 1 — Cloud Adoption: 74% of enterprises have migrated or are actively migrating core '
       'workloads to cloud. On-prem deals are declining at 8% per year. Pure cloud-native competitors '
       'are gaining ground in greenfield opportunities.'),
    wp('Trend 2 — AI Integration: Buyers increasingly require native AI capabilities (summarization, '
       'classification, anomaly detection) out of the box. 61% of RFPs in Q3 included AI requirements, '
       'up from 38% in Q3 last year. Our AI module roadmap must accelerate.'),
    wp('Trend 3 — Remote Work Normalization: Demand for async collaboration features remains elevated '
       'post-pandemic. Customers prioritize mobile accessibility and cross-timezone workflow routing.'),
    wp(),
    wh2('Regional Breakdown'),
    wp('North America: 51% of TAM. Strongest growth in financial services and healthcare.'),
    wp('EMEA: 29% of TAM. GDPR compliance features are a purchase requirement. Growth rate 21%.'),
    wp('APAC: 14% of TAM. Fastest growing region at 27% YoY. Currently underpenetrated by Contoso.'),
    wp('LATAM: 6% of TAM. Early stage. Partner-led go-to-market recommended.'),
])

# 2. product-priorities.docx  — must contain the three named priorities
write_docx(p('product-priorities.docx'), [
    wh1('Q4 Product Priorities'),
    wp('Owner: Priya Nair, VP Product | Date: October 1, 2025 | Status: Approved'),
    wp('Audience: Engineering, Design, Customer Success, Sales Engineering'),
    wp(),
    wp('The following three priorities govern all product investment decisions in Q4 2025. '
       'Any work not aligned to one of these three priorities requires VP approval before starting.'),
    wp(),
    wh2('Priority 1: Platform Stability and Performance'),
    wp('Owner: Marcus Webb, Engineering Lead'),
    wp('Objective: Reduce Priority 1 (P1) production incidents by 40% compared to Q3 2025 baseline.'),
    wp(),
    wp('Context: Q3 saw 14 P1 incidents, up from 9 in Q2. Root cause analysis identified three '
       'systemic issues: database connection pool exhaustion under load, a memory leak in the '
       'document processing worker, and insufficient rate limiting on the public API. Customer '
       'satisfaction scores for reliability dropped to 3.8/5, the lowest since Q2 2023.'),
    wp(),
    wp('Success Metrics:'),
    wp('  - P1 incidents in Q4: target <= 8 (40% reduction from Q3 baseline of 14)'),
    wp('  - Mean time to resolution (MTTR): target < 45 minutes (Q3 actual: 72 minutes)'),
    wp('  - API error rate: target < 0.1% (Q3 actual: 0.4%)'),
    wp('  - Customer reliability NPS question score: target 4.2/5'),
    wp(),
    wp('Dependencies: Requires dedicated on-call rotation for the full quarter. '
       'Database team must complete connection pool redesign by October 15.'),
    wp(),
    wh2('Priority 2: Enterprise Expansion'),
    wp('Owner: Lisa Huang, Product Manager — Enterprise'),
    wp('Objective: Launch SSO (Single Sign-On) and audit logging capabilities for the Enterprise tier '
       'by November 15, 2025. These are the top two missing features blocking 8 enterprise deals '
       'currently in legal review.'),
    wp(),
    wp('Context: In Q3, 8 enterprise prospects (combined ACV $1.4M) stalled or were lost because '
       'Contoso lacked SAML/OIDC SSO integration and an immutable audit log meeting SOC 2 Type II '
       'requirements. Competitors Fabrikam and Northwind both offer these features. Delivering '
       'them in Q4 directly unblocks the enterprise sales pipeline.'),
    wp(),
    wp('Success Metrics:'),
    wp('  - SSO (SAML 2.0 and OIDC) GA release: by November 15'),
    wp('  - Audit log (immutable, 12-month retention, exportable): GA by November 15'),
    wp('  - At least 4 of the 8 stalled enterprise deals re-engaged within 2 weeks of GA'),
    wp('  - Zero SSO-related P1 incidents in the first 30 days post-launch'),
    wp(),
    wp('Dependencies: Legal must approve data retention policy for audit logs by October 10. '
       'Security team must complete threat model review for SSO implementation by October 20.'),
    wp(),
    wh2('Priority 3: Mobile-First Redesign'),
    wp('Owner: Angela Morales, Product Manager — Growth'),
    wp('Objective: Ship the new mobile application (iOS and Android) by November 30, 2025. '
       'The redesign replaces the current mobile web experience with a native app featuring '
       'offline mode, push notifications, and a streamlined task completion flow.'),
    wp(),
    wp('Context: 38% of Contoso users access the product on mobile, but mobile session duration '
       'is 4.2 minutes versus 22 minutes on desktop — a signal of poor mobile UX. '
       'The current mobile web app has a 2.1-star rating on the App Store (47 reviews). '
       'Three enterprise customers have cited mobile experience in their renewal risk notes.'),
    wp(),
    wp('Success Metrics:'),
    wp('  - iOS and Android apps shipped to stores by November 30'),
    wp('  - App Store rating >= 4.0 within 30 days of launch (target 500 reviews)'),
    wp('  - Mobile DAU/MAU ratio improvement: from current 18% to target 30% by December 31'),
    wp('  - Mobile task completion rate: target 72% (current: 41%)'),
    wp(),
    wp('Dependencies: Design system components for mobile must be finalized by October 8. '
       'App Store developer accounts must be provisioned by October 1 (IT action item).'),
])

# 3. sales-forecast.xlsx  — must contain $12.5M total, $1.8M renewal risk
write_xlsx(p('sales-forecast.xlsx'), 'Q4 Sales Forecast', [
    ['Category',          'Target ($)',  'Current Pipeline ($)', 'Coverage',  'Notes'],
    ['New Business',       8200000,       10900000,               '133%',      'Strong pipeline; 3 deals closing Oct'],
    ['Renewals',           4300000,       3100000,                '72%',       '$1.8M AT RISK - see at-risk accounts below'],
    ['Upsells',             900000,        720000,                '80%',       'AI module upsell campaign launching Oct 15'],
    ['Professional Svcs',   100000,         85000,                '85%',       ''],
    ['TOTAL Q4 TARGET',   12500000,       14805000,               '118%',      '$12.5M total target for Q4'],
    ['', '', '', '', ''],
    ['AT-RISK RENEWAL ACCOUNTS', '', '', '', ''],
    ['Account',           'ARR ($)',     'Risk Reason',           'Owner',     'Probability'],
    ['Fabrikam Inc.',      750000,        'Budget freeze Q4',      'J. Torres', '40%'],
    ['Northwind Traders',  620000,        'Competitor evaluation', 'S. Park',   '50%'],
    ['Fourth Coffee',      430000,        'Exec sponsor left',     'M. Davis',  '35%'],
    ['TOTAL AT-RISK',     1800000,        '',                      '',          ''],
    ['', '', '', '', ''],
    ['NOTE: $1.8M renewal risk represents potential revenue shortfall if all 3 at-risk', '', '', '', ''],
    ['accounts churn. Recovery plan required before end of October.', '', '', '', ''],
    ['', '', '', '', ''],
    ['PIPELINE BY REP', '', '', '', ''],
    ['Rep Name',          'Quota ($)',   'Pipeline ($)',           'Attainment', 'Forecast'],
    ['Jordan Torres',      1800000,       2400000,                 '133%',       '$1.7M'],
    ['Sarah Park',         1600000,       1900000,                 '119%',       '$1.5M'],
    ['Marcus Davis',       1400000,       1600000,                 '114%',       '$1.3M'],
    ['Aisha Rahman',       1500000,       2100000,                 '140%',       '$1.6M'],
    ['Chris Yamamoto',     1200000,        980000,                  '82%',        '$0.9M'],
])

# 4. budget-request.docx  — must contain $300K overage
write_docx(p('budget-request.docx'), [
    wh1('Q4 Budget Request'),
    wp('Submitted by: Tom Okafor, VP Engineering | Date: October 3, 2025'),
    wp('Reviewed by: Finance BP Angela Morales | Status: Pending CFO Approval'),
    wp(),
    wh2('Summary'),
    wp('Q4 engineering spend is projected to exceed the approved budget by $300,000. '
       'This document explains the drivers of the $300K budget overage, provides a '
       'category-level breakdown, and proposes three mitigation options for CFO review. '
       'Approval is required by October 10, 2025 to avoid halting vendor payments.'),
    wp(),
    wh2('Budget Overview'),
    wp('Approved Q4 budget:       $2,100,000'),
    wp('Projected Q4 spend:       $2,400,000'),
    wp('Variance (overage):         $300,000'),
    wp('Overage as % of budget:       14.3%'),
    wp(),
    wh2('Root Cause Analysis'),
    wp('The $300,000 budget overage has two primary drivers:'),
    wp(),
    wp('Driver 1 — Unplanned Infrastructure Costs ($185,000)'),
    wp('In August, a traffic spike caused by a viral social post drove 8x normal API volume '
       'for 11 days. Auto-scaling incurred $95,000 in unbudgeted Azure compute charges. '
       'Additionally, the database migration to Azure SQL Hyperscale (approved in Q3) '
       'required $90,000 more in data transfer and migration tooling than the original estimate.'),
    wp(),
    wp('Driver 2 — Two Emergency Hires ($115,000)'),
    wp('Following the P1 incident spike in Q3 (14 incidents), executive leadership approved '
       'two out-of-cycle engineering hires: a Site Reliability Engineer and a Senior Database '
       'Engineer. These hires were not in the original Q4 headcount plan. Prorated Q4 cost '
       'including salary, benefits, and equipment: $115,000.'),
    wp(),
    wh2('Spend Breakdown by Category'),
    wp('Headcount (incl. 2 emergency hires):  $1,650,000  (approved: $1,535,000, over by $115,000)'),
    wp('Cloud Infrastructure (Azure):           $480,000  (approved: $295,000, over by $185,000)'),
    wp('Software Licenses:                       $145,000  (approved: $145,000, on budget)'),
    wp('Contractors / Professional Services:     $100,000  (approved: $100,000, on budget)'),
    wp('Travel and T&E:                           $25,000  (approved: $25,000, on budget)'),
    wp('TOTAL PROJECTED:                       $2,400,000  (approved: $2,100,000, over by $300,000)'),
    wp(),
    wh2('Mitigation Options'),
    wp('Option A — Approve full $300K overage (recommended): '
       'Prevents disruption to Q4 roadmap delivery. The two emergency hires directly address '
       'the P1 incident problem that is the top engineering priority for Q4.'),
    wp(),
    wp('Option B — Partial approval of $185K infrastructure overage only: '
       'Would require deferring one emergency hire start date to Q1 2026. Risk: '
       'reduced capacity to hit the 40% P1 reduction target.'),
    wp(),
    wp('Option C — No approval: '
       'Would require freezing contractor payments and delaying one hire. '
       'Estimated impact: $420K in missed Q4 revenue from delayed enterprise features. '
       'Not recommended.'),
    wp(),
    wh2('Recommendation'),
    wp('Finance and Engineering jointly recommend Option A: approve the full $300K overage. '
       'The risk of not approving exceeds the overage amount given the enterprise pipeline '
       'dependency on Q4 feature delivery. Updated FY2026 budget planning will incorporate '
       'a 10% infrastructure contingency reserve to prevent recurrence.'),
])

print('Done. Files written to:', ASSETS_DIR)
