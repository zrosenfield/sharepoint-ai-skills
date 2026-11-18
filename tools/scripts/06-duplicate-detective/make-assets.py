"""
make-assets.py — 06-duplicate-detective
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/06-duplicate-detective/make-assets.py
Or from this folder: python make-assets.py

Key demo narrative:
  - Brand guidelines: 3 versions; "Brand Guide Final.pdf" is most complete (has Jan 2024 update)
  - Sales decks: 2 versions; FINAL has an extra competitive positioning slide
  - Event banners: near-duplicates (slightly different shades)
  - Case study: unique, not a duplicate
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
print('Generating assets for 06-duplicate-detective...')

# ---- BRAND GUIDELINES — 3 versions ----

# 1. Brand-Guidelines-2024.pdf  — VERSION 1: Logo, Colors, Typography. No January 2024 Update.
write_pdf(p('Brand-Guidelines-2024.pdf'),
    'CONTOSO BRAND GUIDELINES 2024 - Version 1',
    [
        'Document: Contoso Brand Guidelines',
        'Version: 1.0 | Published: August 2023',
        'Department: Marketing',
        '',
        '1. LOGO USAGE',
        'The Contoso logo must always be displayed on a white or very light background.',
        'Minimum clear space around the logo equals the cap-height of the letter C.',
        'Do not stretch, skew, recolour, add drop shadows, or alter the logo in any way.',
        'The logo is available in full colour, reversed white, and single-colour black.',
        '',
        '2. COLOR PALETTE',
        'Primary:   #0078D4  Contoso Blue',
        'Secondary: #FFB900  Contoso Gold',
        'Neutral:   #1A1A1A  Dark',
        'Background: #F5F5F5  Light Grey',
        '',
        '3. TYPOGRAPHY',
        'Heading font: Segoe UI Semibold',
        'Body font:    Segoe UI Regular, 11pt',
        'Caption font: Segoe UI Light, 9pt',
        '',
        '-- END OF VERSION 1 --',
        'This document does not include the January 2024 social media update.',
    ]
)

# 2. Brand Guide Final.pdf — MOST COMPLETE: has January 2024 Update section
write_pdf(p('Brand Guide Final.pdf'),
    'CONTOSO BRAND GUIDE FINAL - Most Complete Version',
    [
        'Document: Contoso Brand Guidelines',
        'Version: 2.1 FINAL | Published: March 2024',
        'Department: Marketing',
        '',
        '1. LOGO USAGE',
        'The Contoso logo must always be displayed on a white or very light background.',
        'Minimum clear space around the logo equals the cap-height of the letter C.',
        'Do not stretch, skew, recolour, add drop shadows, or alter the logo in any way.',
        'The logo is available in full colour, reversed white, and single-colour black.',
        '',
        '2. COLOR PALETTE',
        'Primary:   #0078D4  Contoso Blue',
        'Secondary: #FFB900  Contoso Gold',
        'Neutral:   #1A1A1A  Dark',
        'Background: #F5F5F5  Light Grey',
        '',
        '3. TYPOGRAPHY',
        'Heading font: Segoe UI Semibold',
        'Body font:    Segoe UI Regular, 11pt',
        'Caption font: Segoe UI Light, 9pt',
        '',
        '4. DIGITAL AND WEB STANDARDS',
        'All web content must meet WCAG 2.1 AA accessibility standards.',
        'Minimum touch target size: 44x44px for mobile interactions.',
        '',
        '5. JANUARY 2024 UPDATE',
        'This section was added in January 2024 and is not present in earlier versions.',
        '',
        'Social Media Guidelines:',
        '  - Profile images must use the full-colour Contoso logo on white.',
        '  - Cover images should use Contoso Blue as primary background.',
        '  - Post cadence: LinkedIn 4x/week, Twitter/X 5x/week, Instagram 3x/week.',
        '  - Always include alt text on images for accessibility.',
        '',
        'Updated Color Palette — New Accent Color Added January 2024:',
        '  New accent: #E74C3C  Contoso Red (for alerts, urgency CTAs, and error states)',
        '  This accent colour #E74C3C was NOT present in Version 1 or the backup.',
        '',
        '-- THIS IS THE MOST COMPLETE AND CURRENT VERSION --',
    ]
)

# 3. brand_guide_BACKUP.pdf — Older backup: similar to v1 but less content, no digital/web section
write_pdf(p('brand_guide_BACKUP.pdf'),
    'CONTOSO BRAND GUIDE BACKUP - Older Version',
    [
        'Document: Contoso Brand Guidelines',
        'Version: 0.9 BACKUP | Published: April 2023',
        'NOTE: This is an older backup. Do not distribute.',
        '',
        '1. LOGO USAGE',
        'The Contoso logo must always be displayed on a white background.',
        'Do not modify the logo.',
        '',
        '2. COLOR PALETTE',
        'Primary:   #0078D4  Contoso Blue',
        'Secondary: #FFB900  Contoso Gold',
        '',
        '3. TYPOGRAPHY',
        'Use Segoe UI throughout all materials.',
        '',
        '-- END --',
        'This backup does not include Digital/Web Standards section.',
        'This backup does not include the January 2024 update or social media guidelines.',
        'This backup does not include the new accent colour #E74C3C.',
    ]
)

# ---- SALES DECKS — 2 versions ----

# 4. Sales-Deck-Q3.pptx — 3 slides only (no competitive positioning)
write_pptx(p('Sales-Deck-Q3.pptx'), [
    ('Contoso CloudSuite — Q3 Sales Presentation',
     ['Company Overview',
      'Product Demo Highlights',
      'Pricing']),
    ('Product Demo Highlights',
     ['Live demo: workflow automation builder',
      'AI-powered document classification',
      'Real-time dashboard and reporting',
      'One-click integration with Microsoft 365',
      'Mobile app for iOS and Android']),
    ('Pricing',
     ['Starter tier: $12 per user/month (up to 50 users)',
      'Professional tier: $28 per user/month (up to 500 users)',
      'Enterprise tier: custom pricing, volume discounts available',
      'Annual commitment: 15% discount vs monthly billing',
      'Free 30-day trial available — no credit card required']),
])

# 5. Q3 Sales Deck - FINAL.pptx — 4 slides: same 3 PLUS competitive positioning
write_pptx(p('Q3 Sales Deck - FINAL.pptx'), [
    ('Contoso CloudSuite — Q3 Sales Presentation',
     ['Company Overview',
      'Product Demo Highlights',
      'Pricing',
      'Competitive Positioning']),
    ('Product Demo Highlights',
     ['Live demo: workflow automation builder',
      'AI-powered document classification',
      'Real-time dashboard and reporting',
      'One-click integration with Microsoft 365',
      'Mobile app for iOS and Android']),
    ('Pricing',
     ['Starter tier: $12 per user/month (up to 50 users)',
      'Professional tier: $28 per user/month (up to 500 users)',
      'Enterprise tier: custom pricing, volume discounts available',
      'Annual commitment: 15% discount vs monthly billing',
      'Free 30-day trial available — no credit card required']),
    ('Competitive Positioning — Contoso vs. Competitors',
     ['vs. Fabrikam Automation: Contoso wins on SSO, audit logging, enterprise SLA',
      'vs. Northwind Process Suite: Contoso wins on time-to-value (6 weeks vs 6 months)',
      'Contoso NPS: 44 | Fabrikam NPS: 38 | Northwind NPS: 31',
      'ONLY Contoso deck has this competitive positioning slide — use for enterprise deals',
      'Analyst quote: "Contoso leads on ease-of-deployment" — Gartner Magic Quadrant 2024']),
])

# ---- EVENT BANNERS — near-duplicates (slightly different shades) ----

# 6. Event-Banner.png — shade 1
write_png(p('Event-Banner.png'), width=320, height=200, r=200, g=220, b=240)

# 7. event-banner-v2.png — shade 2 (slightly different)
write_png(p('event-banner-v2.png'), width=320, height=200, r=210, g=225, b=245)

# ---- CASE STUDY — unique, not a duplicate ----

# 8. Case-Study-Fabrikam.docx — unique content
write_docx(p('Case-Study-Fabrikam.docx'), [
    wh1('Case Study: Fabrikam Inc.'),
    wp('How Fabrikam Used Contoso CloudSuite to Reduce Operational Costs by 32%'),
    wp('Published: September 2025 | Industry: Manufacturing | Company Size: 3,400 employees'),
    wp(),
    wh2('Challenge'),
    wp('Fabrikam Inc., a global precision manufacturing firm headquartered in Chicago, was '
       'managing procurement, quality control, and supplier workflows across 14 spreadsheets '
       'and three disconnected legacy systems. Manual data entry consumed an estimated 1,800 '
       'hours per month across operations teams. A missed supplier compliance issue in Q1 2024 '
       'resulted in a $230,000 production halt that accelerated the need for change.'),
    wp(),
    wh2('Solution'),
    wp('Fabrikam selected Contoso CloudSuite Enterprise after a competitive evaluation including '
       'Fabrikam Process Suite and Adventure Works Cloud. Key factors in the selection:'),
    wp('  - Fastest deployment timeline (6-week proof-of-value offer)'),
    wp('  - Native Microsoft 365 integration (Fabrikam is a Microsoft shop)'),
    wp('  - Pre-built manufacturing workflow templates covering ISO 9001 compliance'),
    wp('  - Dedicated customer success manager included at Enterprise tier'),
    wp(),
    wp('Deployment was completed in 6 weeks from contract signing to production go-live. '
       'Contoso migrated 50 terabytes (50TB) of historical workflow data from legacy systems '
       'into the CloudSuite platform during a single weekend maintenance window with zero data loss.'),
    wp(),
    wh2('Results'),
    wp('Operational cost reduction: 32% in the first 12 months post-deployment.'),
    wp('Manual data entry hours eliminated: 1,400 hours/month (78% reduction from baseline).'),
    wp('Supplier compliance incidents: reduced from 7 in Q1 2024 to 0 in Q1 2025.'),
    wp('Time to generate procurement reports: reduced from 3 days to 4 hours.'),
    wp('Employee satisfaction with tools (internal survey): increased from 2.9 to 4.4 out of 5.'),
    wp(),
    wh2('Quote'),
    wp('"Contoso CloudSuite transformed how we run operations. The 6-week deployment was the '
       'fastest enterprise software rollout in our company\'s history, and the 32% cost reduction '
       'in year one exceeded our business case projections." — Rachel Torres, COO, Fabrikam Inc.'),
    wp(),
    wp('This case study is unique content and is not a duplicate of any other document in this library.'),
])

print('Done. Files written to:', ASSETS_DIR)
