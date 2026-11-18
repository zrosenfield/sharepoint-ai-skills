"""
make-assets.py — 01-messy-folder-cleanup
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/01-messy-folder-cleanup/make-assets.py
Or from this folder: python make-assets.py
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
# PDF helper
# ---------------------------------------------------------------------------
def write_pdf(path, title, lines):
    font_obj = b'1 0 obj\n<</Type/Font/Subtype/Type1/BaseFont/Helvetica/Encoding/WinAnsiEncoding>>\nendobj\n'
    res_obj  = b'2 0 obj\n<</Font<</F1 1 0 R>>>>\nendobj\n'

    safe_title = title.replace('(', r'\(').replace(')', r'\)')
    cmds = ['BT', '/F1 14 Tf', '50 750 Td', '(' + safe_title + ') Tj', '0 -20 Td', '/F1 11 Tf']
    for ln in lines:
        safe = ln.replace('\\', '\\\\').replace('(', r'\(').replace(')', r'\)')
        cmds.append('(' + safe + ') Tj')
        cmds.append('0 -16 Td')
    cmds.append('ET')
    stream = '\n'.join(cmds).encode()

    stream_len = str(len(stream)).encode()
    stream_obj = b'4 0 obj\n<</Length ' + stream_len + b'>>\nstream\n' + stream + b'\nendstream\nendobj\n'
    page_obj  = (b'3 0 obj\n<</Type/Page/Parent 5 0 R/MediaBox[0 0 612 792]'
                 b'/Resources 2 0 R/Contents 4 0 R>>\nendobj\n')
    pages_obj = b'5 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n'
    cat_obj   = b'6 0 obj\n<</Type/Catalog/Pages 5 0 R>>\nendobj\n'

    header = b'%PDF-1.4\n'
    body = header + font_obj + res_obj + stream_obj + page_obj + pages_obj + cat_obj
    xref_offset = len(body)

    pos = len(header)
    offsets = []
    for obj in [font_obj, res_obj, stream_obj, page_obj, pages_obj, cat_obj]:
        offsets.append(pos)
        pos += len(obj)

    xref = b'xref\n0 7\n0000000000 65535 f \n'
    for off in offsets:
        xref += (str(off).zfill(10) + ' 00000 n \n').encode()
    trailer = (b'trailer\n<</Size 7/Root 6 0 R>>\nstartxref\n' +
               str(xref_offset).encode() + b'\n%%EOF\n')
    open(path, 'wb').write(body + xref + trailer)
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

# ---------------------------------------------------------------------------
# PPTX helper
# ---------------------------------------------------------------------------
PPTX_CONTENT_TYPES_TMPL = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  {slide_overrides}
</Types>'''

PPTX_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''

def make_pptx_slide(title, bullets):
    bullet_xml = ''
    for b in bullets:
        bullet_xml += ('<a:p><a:r><a:t>' + xesc(b) + '</a:t></a:r></a:p>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<p:cSld><p:spTree>'
        '<p:sp><p:nvSpPr><p:cNvPr id="1" name="Title"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        '<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
        '<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>'
        '<a:p><a:r><a:t>' + xesc(title) + '</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Content"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        '<p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr>'
        '<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>' + bullet_xml + '</p:txBody></p:sp>'
        '</p:spTree></p:cSld></p:sld>'
    )

def write_pptx(path, slides):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        slide_overrides = ''
        prs_slide_refs = ''
        for i, (title, bullets) in enumerate(slides):
            n = i + 1
            slide_xml = make_pptx_slide(title, bullets)
            z.writestr('ppt/slides/slide' + str(n) + '.xml', slide_xml)
            z.writestr('ppt/slides/_rels/slide' + str(n) + '.xml.rels',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
            slide_overrides += ('<Override PartName="/ppt/slides/slide' + str(n) + '.xml" '
                                'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
            prs_slide_refs += '<p:sldId id="' + str(256 + i) + '" r:id="rId' + str(n) + '"/>'

        ct = PPTX_CONTENT_TYPES_TMPL.replace('{slide_overrides}', slide_overrides)
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', PPTX_RELS)

        slide_rels = ''
        for i in range(len(slides)):
            slide_rels += ('<Relationship Id="rId' + str(i + 1) + '" '
                           'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
                           'Target="slides/slide' + str(i + 1) + '.xml"/>')
        prs_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    + slide_rels + '</Relationships>')
        z.writestr('ppt/_rels/presentation.xml.rels', prs_rels)

        prs_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
                   ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                   '<p:sldMasterIdLst/>'
                   '<p:sldIdLst>' + prs_slide_refs + '</p:sldIdLst>'
                   '<p:sldSz cx="9144000" cy="6858000"/>'
                   '</p:presentation>')
        z.writestr('ppt/presentation.xml', prs_xml)

    open(path, 'wb').write(buf.getvalue())
    print('  ' + path)

# ---------------------------------------------------------------------------
# PNG helper
# ---------------------------------------------------------------------------
def write_png(path, width=320, height=200, r=230, g=230, b=230):
    raw = []
    for _ in range(height):
        row = b'\x00' + bytes([r, g, b] * width)
        raw.append(row)
    raw_data = b''.join(raw)
    compressed = zlib.compress(raw_data)

    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')
    open(path, 'wb').write(sig + ihdr + idat + iend)
    print('  ' + path)

# ===========================================================================
# Generate assets
# ===========================================================================
print('Generating assets for 01-messy-folder-cleanup...')

# 1. meeting notes jan.docx
write_docx(p('meeting notes jan.docx'), [
    wh1('Team Retrospective — January 2025'),
    wp('Date: January 14, 2025'),
    wp('Attendees: Sarah Chen, Marcus Webb, Priya Nair, Tom Okafor, Lisa Huang'),
    wp(),
    wh2('Q4 2024 Review'),
    wp('The team reviewed Q4 performance against OKRs. Overall delivery was 87% of committed items. '
       'Three initiatives slipped to Q1 due to resourcing constraints and a late dependency from the '
       'platform team. Customer satisfaction scores averaged 4.3/5, up from 4.1 in Q3.'),
    wp(),
    wh2('Action Items'),
    wp('The following three action items were agreed by the full team:'),
    wp(),
    wp('Action Item 1: Hire 2 senior engineers by end of February 2025. Owner: Sarah Chen (Engineering '
       'Manager). The team is understaffed for the Q2 roadmap commitments. JDs to be posted by January 21.'),
    wp(),
    wp('Action Item 2: Move daily standup from 9:00 AM to 10:00 AM Pacific effective January 20, 2025. '
       'Owner: Marcus Webb (Scrum Master). Reason: two team members joining from London timezone, '
       'existing 9 AM slot is too early for productive participation.'),
    wp(),
    wp('Action Item 3: Deliver Q2 roadmap draft to stakeholders by February 15, 2025. '
       'Owner: Priya Nair (Product Manager). Must include capacity planning given new hire timeline. '
       'Review session with leadership scheduled for February 18.'),
    wp(),
    wh2('Other Discussion'),
    wp('Tom Okafor raised concerns about technical debt in the billing module. Team agreed to allocate '
       '20% of Q1 sprint capacity to debt reduction. Lisa Huang to track progress in the engineering '
       'health dashboard.'),
    wp(),
    wp('Next retrospective: February 11, 2025 at 2:00 PM Pacific.'),
])

# 2. FINAL budget v3 (2).xlsx
write_xlsx(p('FINAL budget v3 (2).xlsx'), 'Annual Budget', [
    ['Category',        'Q1 ($)',  'Q2 ($)',  'Q3 ($)',  'Q4 ($)',  'Total ($)'],
    ['Headcount',        185000,    195000,    195000,    205000,    780000],
    ['Software Licenses', 18000,     18000,     18000,     18000,     72000],
    ['Travel',            12000,     14000,     10000,     16000,     52000],
    ['Marketing',         22000,     28000,     30000,     26000,    106000],
    ['Contingency',        8000,      8000,      8000,      6000,     30000],
    ['TOTAL',            245000,    263000,    261000,    271000,   1040000],
])

# 3. deck for sarah.pptx
write_pptx(p('deck for sarah.pptx'), [
    ('Enterprise Partnership Proposal',
     ['Prepared for: Sarah Chen, VP Strategic Alliances, Fabrikam Inc.',
      'Presented by: Contoso Solutions',
      'Date: January 2025',
      'Agenda: Product Overview | ROI Analysis | Proposed Engagement | Next Steps']),
    ('Product Overview: Contoso CloudSuite',
     ['End-to-end cloud management platform for enterprise workloads',
      'Key modules: Infrastructure Automation, Cost Governance, Security Posture',
      'Deployed by 340+ enterprise customers across 28 countries',
      'ISO 27001 certified | SOC 2 Type II | FedRAMP Moderate',
      'Average time-to-value: 6 weeks from signed agreement to production']),
    ('ROI Analysis for Fabrikam Inc.',
     ['Based on Fabrikam current environment: 1,200 managed cloud resources',
      'Estimated savings Year 1: $820,000 through rightsizing and policy automation',
      'Estimated savings Year 2-3: $1.1M per year as adoption matures',
      '3-year NPV: $2.4M at 8% discount rate',
      'Payback period: 7 months',
      'Comparable customer: Northwind Traders achieved 34% cost reduction in 9 months']),
    ('Next Steps',
     ['Sign mutual NDA by January 31, 2025',
      'Schedule 2-hour technical discovery call with Fabrikam IT architecture team',
      'Contoso to deliver tailored proof-of-concept proposal by February 14, 2025',
      'Target pilot start: March 1, 2025 (30-day proof of value)',
      'Decision checkpoint: April 1, 2025',
      'Contact: partnerships@contoso.com | +1-800-CONTOSO']),
])

# 4. IMG_4021.png
write_png(p('IMG_4021.png'), width=320, height=200, r=220, g=222, b=225)

# 5. Untitled document.docx
write_docx(p('Untitled document.docx'), [
    wh1('Vendor Onboarding Guide'),
    wp('Version: Draft 1.0 | Last Updated: January 2025 | Owner: Procurement & IT Operations'),
    wp(),
    wp('This guide covers the end-to-end process for onboarding a new external vendor to Contoso\'s '
       'systems and processes. All steps must be completed before a vendor can receive payment or '
       'access any Contoso systems.'),
    wp(),
    wh2('1. Account Setup'),
    wp('1.1 Vendor Registration: The procurement team must register the vendor in Coupa (vendor portal) '
       'using the vendor\'s legal entity name, tax ID (EIN/VAT), and primary billing address.'),
    wp('1.2 Banking Details: Vendor must submit ACH or wire transfer details via the secure Coupa supplier '
       'portal. Do not accept banking details by email.'),
    wp('1.3 W-9 / W-8BEN: Collect completed tax form from vendor. US entities provide W-9; foreign '
       'entities provide W-8BEN. File in SharePoint under Procurement > Vendors > Tax Forms.'),
    wp(),
    wh2('2. System Access'),
    wp('2.1 If the vendor requires access to Contoso internal systems (e.g., project management tools, '
       'shared drives, or test environments), submit an IT Access Request ticket via the ServiceNow '
       'portal at least 5 business days before access is needed.'),
    wp('2.2 All vendor users must complete the Contoso Acceptable Use Policy acknowledgment before '
       'receiving system credentials. The AUP form is available in ServiceNow.'),
    wp('2.3 Vendor accounts are created as external guest accounts in Azure AD and scoped to the '
       'minimum required permissions. Access is reviewed quarterly and revoked upon contract end.'),
    wp(),
    wh2('3. First Week Checklist'),
    wp('[ ] Vendor receives welcome email with key contacts and escalation paths'),
    wp('[ ] Kick-off meeting scheduled with project sponsor and vendor account manager'),
    wp('[ ] Non-Disclosure Agreement (NDA) signed and filed'),
    wp('[ ] Master Service Agreement (MSA) or Statement of Work (SOW) fully executed'),
    wp('[ ] Vendor added to relevant Slack channels (external designation required)'),
    wp('[ ] Data sharing agreement completed if vendor will handle personal data'),
    wp(),
    wh2('4. Key Contacts'),
    wp('Procurement Lead: Angela Morales — angela.morales@contoso.com'),
    wp('IT Access Requests: ServiceNow Portal — https://contoso.service-now.com'),
    wp('Legal / Contract Review: contracts@contoso.com'),
    wp('Accounts Payable: ap@contoso.com | payment terms Net-30 from invoice receipt'),
    wp('Security Compliance: security@contoso.com — contact for DPA or data handling questions'),
])

# 6. asdfgh.pdf — Cloud Migration Services Agreement (KEY FILE for demo)
write_pdf(p('asdfgh.pdf'),
    'CLOUD MIGRATION SERVICES AGREEMENT',
    [
        'This Cloud Migration Services Agreement ("Agreement") is entered into as of',
        'February 1, 2025, between:',
        '',
        'VENDOR: Northwind Traders, Inc., a Delaware corporation',
        '  ("Northwind Traders" or "Service Provider")',
        '  1400 Harbor Boulevard, Wilmington, DE 19801',
        '',
        'CLIENT: Contoso Ltd., an England and Wales limited company',
        '  ("Contoso" or "Client")',
        '  1 Microsoft Way, Reading, RG6 1WG, United Kingdom',
        '',
        '1. SCOPE OF SERVICES',
        'Northwind Traders agrees to provide cloud migration services to migrate',
        "Contoso's on-premises infrastructure to Microsoft Azure. Services include:",
        '  (a) Discovery and assessment of existing on-premises workloads (Weeks 1-4)',
        '  (b) Migration architecture design and Azure Landing Zone configuration (Weeks 5-8)',
        '  (c) Pilot migration of non-production workloads (Weeks 9-12)',
        '  (d) Production workload migration in three waves (Weeks 13-22)',
        '  (e) Post-migration optimisation and handover (Weeks 23-26)',
        '',
        '2. TIMELINE',
        'The cloud migration engagement shall be completed within six (6) months',
        'from the Commencement Date of February 1, 2025, with a target completion',
        'date of July 31, 2025.',
        '',
        '3. CONTRACT VALUE AND PAYMENT SCHEDULE',
        'Total contract value: USD $180,000 (one hundred and eighty thousand US dollars)',
        '  - Milestone 1 (Assessment complete):        $36,000  due Week 4',
        '  - Milestone 2 (Architecture approved):      $27,000  due Week 8',
        '  - Milestone 3 (Pilot migration complete):   $27,000  due Week 12',
        '  - Milestone 4 (Production migration wave 1): $36,000  due Week 16',
        '  - Milestone 5 (Production migration wave 2): $27,000  due Week 20',
        '  - Milestone 6 (Final handover and sign-off): $27,000  due Week 26',
        '',
        '4. GOVERNING LAW',
        'This Agreement shall be governed by the laws of the State of Delaware.',
        '',
        'Signed on behalf of Northwind Traders, Inc.: _______________________',
        'Signed on behalf of Contoso Ltd.: _______________________',
    ]
)

print('Done. Files written to:', ASSETS_DIR)
