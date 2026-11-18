"""
make-assets.py — 02-sort-into-folders
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/02-sort-into-folders/make-assets.py
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
print('Generating assets for 02-sort-into-folders...')

# 1. Q3-revenue-report.xlsx  (Finance)
write_xlsx(p('Q3-revenue-report.xlsx'), 'Q3 Revenue', [
    ['Metric',              'Q3 2025 ($)',  'Target ($)',  'Variance ($)', 'YoY Change'],
    ['Product A Revenue',    1520000,        1400000,        120000,       '14%'],
    ['Product B Revenue',    1830000,        1700000,        130000,       '9%'],
    ['Product C Revenue',     850000,         700000,        150000,       '18%'],
    ['Total Revenue',        4200000,        3800000,        400000,       '11%'],
    ['Cost of Goods Sold',   1470000,        1330000,       -140000,       ''],
    ['Gross Profit',         2730000,        2470000,        260000,       ''],
    ['Gross Margin %',          '65%',          '65%',          '',        ''],
    ['YoY Growth',              '11%',            '',            '',        ''],
    ['vs Target',              '+$400K',           '',            '',       ''],
])

# 2. brand-guidelines-v2.pdf  (Marketing)
write_pdf(p('brand-guidelines-v2.pdf'),
    'CONTOSO BRAND GUIDELINES - Version 2.0',
    [
        'Document: Contoso Brand Guidelines',
        'Version: 2.0 | Updated: March 2025',
        'Department: Marketing | Classification: Internal',
        '',
        '1. LOGO USAGE',
        'The Contoso logo must always appear on a white or light background.',
        'Minimum clear space: equal to the height of the letter "C" on all sides.',
        'Do not stretch, rotate, recolour, or add effects to the logo.',
        'Approved logo files are available in the Brand Assets SharePoint library.',
        '',
        '2. COLOR PALETTE',
        'Primary brand colour:   #0078D4  (Contoso Blue)',
        'Secondary brand colour: #FFB900  (Contoso Gold)',
        'Neutral dark:           #1A1A1A',
        'Neutral light:          #F5F5F5',
        'Use primary blue for headings, CTAs, and primary UI elements.',
        'Use gold as an accent only — never as a background fill.',
        '',
        '3. TYPOGRAPHY',
        'Primary typeface: Segoe UI (all weights)',
        'Heading: Segoe UI Semibold, size 28pt+',
        'Body: Segoe UI Regular, size 11pt, line-height 1.4',
        'Captions: Segoe UI Light, size 9pt',
        'Do not use decorative fonts in official communications.',
        '',
        '4. TONE OF VOICE',
        'Contoso communicates with confidence, clarity, and warmth.',
        'Active voice preferred. Avoid jargon and overly technical language.',
        'Be concise: if you can say it in fewer words, do so.',
        'Accessible reading level: aim for Flesch-Kincaid Grade 9 or below.',
        '',
        '5. DIGITAL AND WEB STANDARDS',
        'All web content must meet WCAG 2.1 AA accessibility standards.',
        'Use Contoso Blue (#0078D4) for hyperlinks on white backgrounds.',
        'Minimum touch target size: 44x44px for mobile.',
        '',
        'For brand support contact: brand@contoso.com',
    ]
)

# 3. onboarding-checklist.docx  (HR)
write_docx(p('onboarding-checklist.docx'), [
    wh1('New Employee Onboarding Checklist'),
    wp('Department: Human Resources | Document Type: Checklist | Audience: New Hires & Managers'),
    wp('Effective Date: January 2025 | Owner: People Operations'),
    wp(),
    wp('This checklist must be completed during the first two weeks of employment. '
       'The hiring manager is responsible for ensuring all items are completed and signed off.'),
    wp(),
    wh2('Before Day 1 — IT Setup'),
    wp('[ ] Laptop ordered and configured with standard build'),
    wp('[ ] Azure AD account created and credentials sent to personal email'),
    wp('[ ] Microsoft 365 licence assigned (E3 standard for all employees)'),
    wp('[ ] Access provisioned: Teams, SharePoint, Outlook, Planner'),
    wp('[ ] VPN client installed and tested'),
    wp('[ ] Security training module assigned in LMS (due by end of Week 1)'),
    wp(),
    wh2('Day 1 — HR Paperwork'),
    wp('[ ] Employment contract signed and filed'),
    wp('[ ] Right to work documentation verified and copied'),
    wp('[ ] Emergency contact form completed'),
    wp('[ ] Payroll direct deposit details submitted to Finance'),
    wp('[ ] Benefits enrollment form completed (health, dental, pension)'),
    wp('[ ] Photo ID badge issued by Reception'),
    wp(),
    wh2('Week 1 — First-Week Meetings'),
    wp('[ ] Welcome meeting with direct manager (Day 1, 9:00 AM)'),
    wp('[ ] HR orientation session (Day 1, 2:00 PM)'),
    wp('[ ] Team introduction call / in-person lunch'),
    wp('[ ] Meet with buddy (assigned below) — informal chat'),
    wp('[ ] Skip-level introduction with department head (by end of Week 1)'),
    wp('[ ] IT orientation: ticketing system, password manager, security practices'),
    wp(),
    wh2('Buddy Assignment'),
    wp('Every new hire is assigned an onboarding buddy for their first 90 days. '
       'The buddy is a peer (not a manager) who provides informal support, answers day-to-day '
       'questions, and helps the new hire build relationships. The buddy should have been with '
       'Contoso for at least 12 months.'),
    wp('Assigned buddy: ___________________________'),
    wp('First buddy coffee chat: ___________________________'),
    wp(),
    wh2('30 / 60 / 90 Day Goals'),
    wp('30-Day Goal: Complete all onboarding training modules. Understand team structure, '
       'current projects, and Q2 priorities. Deliver first independent task with manager sign-off.'),
    wp('60-Day Goal: Own a defined workstream or recurring responsibility. '
       'Identify one process improvement opportunity and propose a solution.'),
    wp('90-Day Goal: Operating independently. Deliver a meaningful output that demonstrates '
       'core role competencies. Complete first performance check-in with manager.'),
])

# 4. server-migration-plan.docx  (IT)
write_docx(p('server-migration-plan.docx'), [
    wh1('IT Infrastructure Server Migration Plan'),
    wp('Project: On-Premises to Azure Migration | Department: Information Technology'),
    wp('Document Type: Migration Plan | Classification: Internal | Version: 1.2'),
    wp('Owner: Tom Okafor, IT Infrastructure Lead | Date: February 2025'),
    wp(),
    wh2('Executive Summary'),
    wp('Contoso IT Infrastructure will migrate 12 on-premises servers to Microsoft Azure '
       'during Q2-Q3 2025. The migration will decommission the Reading data centre, '
       'reduce infrastructure operating costs by an estimated 42%, and improve resilience '
       'through Azure availability zones. All production workloads will be migrated with '
       'a maximum tolerated downtime of 4 hours per server.'),
    wp(),
    wh2('Server Inventory'),
    wp('Total servers in scope: 12'),
    wp('  - Application servers: 4 (PROD-APP-01 through PROD-APP-04)'),
    wp('  - Database servers: 3 (PROD-SQL-01, PROD-SQL-02, PROD-SQL-RO)'),
    wp('  - File/print servers: 2 (PROD-FILE-01, PROD-FILE-02)'),
    wp('  - Domain controllers: 2 (PROD-DC-01, PROD-DC-02)'),
    wp('  - Monitoring server: 1 (PROD-MON-01)'),
    wp(),
    wh2('Migration Phases'),
    wp('Phase 1 — Assessment (March 2025): Azure Migrate assessment of all 12 servers. '
       'Dependency mapping, sizing recommendations, cost modelling. Output: Migration Wave Plan.'),
    wp('Phase 2 — Pilot (April 2025): Migrate 2 non-critical servers (PROD-FILE-02, PROD-MON-01) '
       'to validate tooling, networking, and runbook procedures.'),
    wp('Phase 3 — Production Migration Wave 1 (May 2025): Migrate application and file servers '
       '(PROD-APP-01 through PROD-APP-04, PROD-FILE-01). Planned maintenance window: Saturday 1am-5am.'),
    wp('Phase 4 — Production Migration Wave 2 (June 2025): Migrate database and domain '
       'controller servers. Requires database quiesce and AD replication verification.'),
    wp('Phase 5 — Cutover and Decommission (July 2025): DNS cutover, certificate updates, '
       'decommission on-prem hardware, vacate Reading data centre.'),
    wp(),
    wh2('Risks and Rollback Plan'),
    wp('Risk 1: Application compatibility issues post-migration. Mitigation: full regression '
       'testing in Azure Dev/Test environment before production cutover.'),
    wp('Risk 2: Network latency increase to branch offices. Mitigation: Azure ExpressRoute '
       'circuit to be provisioned before Wave 1.'),
    wp('Rollback Plan: All production servers will be kept powered off (not deleted) for 30 days '
       'post-migration. If critical issues arise, revert DNS and re-power on-prem servers within 2 hours.'),
])

# 5. holiday-party-invite.png  (Marketing / Events)
write_png(p('holiday-party-invite.png'), width=320, height=200, r=180, g=220, b=185)

# 6. sales-commission-structure.xlsx  (Finance)
write_xlsx(p('sales-commission-structure.xlsx'), 'Commission Structure', [
    ['Quota Attainment',    'Commission Rate', 'Example: $500K Quota', 'Commission Earned'],
    ['0% - 99%',            '5%',              '$400,000 (80%)',        '$20,000'],
    ['100% - 119%',         '8%',              '$500,000 (100%)',       '$40,000'],
    ['120%+',               '12%',             '$600,000 (120%)',       '$60,000+'],
    ['', '', '', ''],
    ['Quarterly Accelerators', '', '', ''],
    ['Q1 Multiplier (Jan-Mar)', '1.0x', 'Standard rate applies', ''],
    ['Q2 Multiplier (Apr-Jun)', '1.1x', '10% bonus on commission', ''],
    ['Q3 Multiplier (Jul-Sep)', '1.0x', 'Standard rate applies', ''],
    ['Q4 Multiplier (Oct-Dec)', '1.25x', '25% bonus on commission', ''],
    ['', '', '', ''],
    ['Example: Rep at 110% attainment in Q4', '', '', ''],
    ['Base commission (100% tier)', '$40,000', '', ''],
    ['Top-up (100-110% at 8%)', '$4,000', '', ''],
    ['Q4 multiplier 1.25x', 'Applied to full amount', '', ''],
    ['Total commission earned', '$55,000', '', ''],
])

# 7. password-policy.pdf  (IT)
write_pdf(p('password-policy.pdf'),
    'CONTOSO IT PASSWORD SECURITY POLICY',
    [
        'Document: Password Security Policy',
        'Department: Information Technology',
        'Classification: Internal | Version: 3.1 | Effective: January 2025',
        '',
        '1. PURPOSE',
        'This policy establishes minimum password security standards for all Contoso',
        'systems to protect against unauthorised access and credential-based attacks.',
        '',
        '2. PASSWORD REQUIREMENTS',
        'All user account passwords must meet the following requirements:',
        '  - Minimum length: 12 characters',
        '  - Must contain: uppercase letters, lowercase letters, numbers, special characters',
        '  - Must not contain: username, display name, or common dictionary words',
        '  - Password history: no reuse for last 12 passwords',
        '',
        '3. ROTATION POLICY',
        'Passwords must be changed every 90 days.',
        'Service account passwords must be changed every 180 days.',
        'Privileged admin account passwords must be changed every 60 days.',
        '',
        '4. MULTI-FACTOR AUTHENTICATION',
        'MFA is REQUIRED for all accounts without exception.',
        'Approved MFA methods: Microsoft Authenticator app (preferred), hardware FIDO2 key.',
        'SMS-based OTP is not approved for new enrollments.',
        '',
        '5. PASSWORD STORAGE',
        'All passwords must be stored in the corporate password manager (1Password Teams).',
        'Passwords must never be stored in plaintext, spreadsheets, or email.',
        '',
        '6. BREACH RESPONSE PROCEDURE',
        'If a password is suspected compromised:',
        '  Step 1: Reset the password immediately via Azure AD self-service portal',
        '  Step 2: Report the incident to security@contoso.com within 1 hour',
        '  Step 3: IT Security will review sign-in logs for suspicious activity',
        '  Step 4: If a data breach is confirmed, follow Incident Response Playbook IR-03',
        '',
        'Policy owner: IT Security Team | security@contoso.com',
    ]
)

# 8. product-launch-timeline.pptx  (Marketing)
write_pptx(p('product-launch-timeline.pptx'), [
    ('Product Launch Plan: Contoso CloudSuite v4.0',
     ['Target launch date: Q3 2025 (September 15, 2025)',
      'Prepared by: Marketing, Product, and Sales teams',
      'Status: In planning',
      'Agenda: Pre-Launch Milestones | Launch Week | Post-Launch Metrics']),
    ('Pre-Launch Milestones',
     ['April 30: Feature freeze and release candidate to QA',
      'May 31: Beta program launch — 20 design partner customers',
      'June 30: Beta feedback incorporated, GA build signed off',
      'July 31: Sales enablement training completed (all AEs and SEs)',
      'August 15: PR briefings with tier-1 tech media',
      'August 31: Landing page and in-product upgrade messaging live',
      'September 1: Analyst briefings (Gartner, Forrester)',
      'September 10: Embargo lift for press reviews']),
    ('Launch Week Plan: September 15-19, 2025',
     ['Monday Sept 15: Public announcement — blog post, press release, social media campaign',
      'Monday Sept 15: Email campaign to 45,000 existing customers',
      'Tuesday Sept 16: Live product webinar (target 2,000 registrations)',
      'Wednesday Sept 17: LinkedIn Sponsored Content campaign starts',
      'Thursday Sept 18: Partner enablement webinar for 120 reseller partners',
      'Friday Sept 19: Launch retrospective — war room debrief with all teams',
      'Launch week paid media budget: $120,000']),
    ('Post-Launch Success Metrics',
     ['30 days: 500 new trial sign-ups from launch campaign',
      '30 days: 15% of existing customers viewed upgrade page',
      '60 days: 50 paid conversions from trial cohort',
      '60 days: NPS survey to beta customers — target score 45+',
      '90 days: $2.1M in new ARR attributed to launch campaign',
      '90 days: 3 tier-1 media reviews published',
      'All metrics tracked in marketing dashboard: go/launch-metrics']),
])

print('Done. Files written to:', ASSETS_DIR)
