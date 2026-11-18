"""
Generate Northwind-MSA-v1.docx and Northwind-MSA-v2.docx for the
04-comparison-report demo.

Changes v1 -> v2 (and who each favours):
  1. Term:               12 months  -> 24 months        (vendor - longer lock-in)
  2. Payment terms:      Net 45     -> Net 30            (vendor - faster payment)
  3. Liability cap:      $500,000   -> $1,000,000        (us - higher recovery ceiling)
  4. Termination notice: 60 days    -> 30 days           (us - easier exit)
  5. SLA uptime:         99.5%      -> 99.9%             (us - better guarantee)
  6. Data residency:     US only    -> US and EU         (us - compliance options)
  7. Non-compete:        24 months  -> 12 months         (us - less restriction)
  8. Insurance:          absent     -> $2M required      (us - vendor must insure)
"""

import zipfile, io, os

# ── OOXML boilerplate ─────────────────────────────────────────────────────────

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
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="word/document.xml"/>
</Relationships>"""

WORD_RELS = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
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


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def p(text='', bold=False, size=None, align=None):
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    ppr = ('<w:pPr><w:jc w:val="' + align + '"/></w:pPr>') if align else ''
    if not text:
        return '<w:p ' + ns + '>' + ppr + '</w:p>'
    rpr = ''
    if bold:
        rpr += '<w:b/>'
    if size:
        rpr += '<w:sz w:val="' + str(size) + '"/><w:szCs w:val="' + str(size) + '"/>'
    rpr_tag = ('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''
    return ('<w:p ' + ns + '>' + ppr + '<w:r>' + rpr_tag +
            '<w:t xml:space="preserve">' + esc(text) + '</w:t></w:r></w:p>')


def h1(text):
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    return ('<w:p ' + ns + '><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')


def h2(text):
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    return ('<w:p ' + ns + '><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')


def document_xml(paragraphs):
    body = '\n'.join(paragraphs)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '  <w:body>\n' + body + '\n'
        '    <w:sectPr>\n'
        '      <w:pgSz w:w="12240" w:h="15840"/>\n'
        '      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>\n'
        '    </w:sectPr>\n'
        '  </w:body>\n'
        '</w:document>'
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


# ── Shared prose ──────────────────────────────────────────────────────────────

PARTIES = (
    'This Master Services Agreement ("Agreement") is entered into as of the Effective Date '
    'between Northwind Traders, Inc., a Delaware corporation ("Service Provider"), '
    'and Contoso Ltd., a Washington corporation ("Client").'
)

RECITALS = (
    'WHEREAS, Service Provider desires to provide certain technology services to Client, '
    'and Client desires to engage Service Provider for such services, the parties agree as follows:'
)

DEFINITIONS = [
    ('"Services" means the software-as-a-service platform and professional services '
     'described in each Statement of Work ("SOW") executed under this Agreement.'),
    ('"Confidential Information" means any non-public information disclosed by either party '
     'that is designated as confidential or that reasonably should be understood to be confidential.'),
    ('"Intellectual Property Rights" means all patents, copyrights, trademarks, trade secrets, '
     'and other proprietary rights.'),
]

SERVICES_BODY = (
    'Service Provider shall perform the Services described in each SOW in a professional '
    'and workmanlike manner, consistent with industry standards. Any changes to the scope '
    'of Services must be agreed in writing by both parties via a Change Order.'
)

IP_BODY = (
    'Each party retains all Intellectual Property Rights in its pre-existing materials. '
    'Work product created solely for Client under a SOW ("Deliverables") is assigned to '
    'Client upon full payment. Service Provider retains ownership of its underlying '
    'platform, tools, and general methodologies.'
)

CONFIDENTIALITY_BODY = (
    "Each party agrees to hold the other's Confidential Information in strict confidence "
    'using at least the same degree of care it uses for its own confidential information, '
    'but no less than reasonable care. Obligations survive termination for three (3) years.'
)

TERMINATION_CAUSE_BODY = (
    'Either party may terminate immediately upon written notice if the other party '
    'materially breaches this Agreement and fails to cure such breach within thirty (30) '
    'days of receiving written notice of the breach.'
)

SECURITY_BODY = (
    'Service Provider shall maintain commercially reasonable administrative, technical, '
    'and physical safeguards designed to protect Client data against unauthorized access, '
    'loss, or destruction.'
)

SLA_REMEDIES_BODY = (
    "If uptime falls below the committed level in any calendar month, Client is eligible "
    "for a service credit equal to five percent (5%) of that month's fees for each full "
    'percentage point below the SLA, up to a maximum of twenty percent (20%) of that '
    "month's fees."
)

GOVLAW_BODY = (
    'This Agreement is governed by the laws of the State of Washington, '
    'without regard to conflict-of-law principles.'
)

ENTIRE_AGREEMENT_BODY = (
    'This Agreement, together with all SOWs and exhibits, constitutes the entire agreement '
    'between the parties and supersedes all prior negotiations, representations, or agreements.'
)

AMENDMENTS_BODY = (
    'No amendment to this Agreement shall be effective unless made in writing and signed '
    'by authorized representatives of both parties.'
)

SEVERABILITY_BODY = (
    'If any provision of this Agreement is held unenforceable, the remaining provisions '
    'shall continue in full force and effect.'
)

SIGNATURES_BLOCK = [
    p('IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.'),
    p(),
    p('NORTHWIND TRADERS, INC.', bold=True),
    p('Signature: _______________________________'),
    p('Name:      _______________________________'),
    p('Title:     _______________________________'),
    p('Date:      _______________________________'),
    p(),
    p('CONTOSO LTD.', bold=True),
    p('Signature: _______________________________'),
    p('Name:      _______________________________'),
    p('Title:     _______________________________'),
    p('Date:      _______________________________'),
]


# ── v1 ────────────────────────────────────────────────────────────────────────

def make_v1():
    paras = [
        p('NORTHWIND TRADERS, INC.', bold=True, size=36, align='center'),
        p('MASTER SERVICES AGREEMENT', bold=True, size=28, align='center'),
        p('Version 1.0  |  Effective Date: January 1, 2025', align='center'),
        p(),
        p(PARTIES),
        p(),
        p(RECITALS),
        p(),
        h1('1. DEFINITIONS'),
    ]
    for d in DEFINITIONS:
        paras.append(p(d))
    paras += [
        p(),
        h1('2. TERM'),
        p(
            'This Agreement commences on the Effective Date and continues for an initial term of '
            'twelve (12) months, unless earlier terminated in accordance with Section 9. '
            'Thereafter, this Agreement shall automatically renew for successive twelve-month '
            'periods unless either party provides written notice of non-renewal at least '
            'sixty (60) days prior to the end of the then-current term.'
        ),
        p(),
        h1('3. SERVICES'),
        p(SERVICES_BODY),
        p(),
        h1('4. FEES AND PAYMENT'),
        p(
            'Client shall pay all undisputed invoices within forty-five (45) days of the invoice '
            'date (Net 45). Invoices not disputed in good faith within fifteen (15) days of '
            'receipt are deemed accepted. Late payments shall accrue interest at one and '
            'one-half percent (1.5%) per month.'
        ),
        p(),
        h1('5. SERVICE LEVELS'),
        h2('5.1 Uptime Commitment'),
        p(
            'Service Provider guarantees ninety-nine point five percent (99.5%) monthly uptime '
            'for the production environment, excluding Scheduled Maintenance Windows. '
            'Uptime is calculated as: ((total minutes - downtime minutes) / total minutes) x 100.'
        ),
        h2('5.2 Remedies'),
        p(SLA_REMEDIES_BODY),
        p(),
        h1('6. DATA HANDLING'),
        h2('6.1 Data Residency'),
        p(
            'All Client data processed under this Agreement shall be stored and processed '
            'exclusively within data centers located in the United States.'
        ),
        h2('6.2 Security'),
        p(SECURITY_BODY),
        p(),
        h1('7. INTELLECTUAL PROPERTY'),
        p(IP_BODY),
        p(),
        h1('8. CONFIDENTIALITY'),
        p(CONFIDENTIALITY_BODY),
        p(),
        h1('9. TERM AND TERMINATION'),
        h2('9.1 Termination for Convenience'),
        p(
            'Either party may terminate this Agreement for any reason by providing sixty (60) '
            "days' prior written notice to the other party."
        ),
        h2('9.2 Termination for Cause'),
        p(TERMINATION_CAUSE_BODY),
        p(),
        h1('10. LIMITATION OF LIABILITY'),
        p(
            'NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL, '
            'SPECIAL, OR EXEMPLARY DAMAGES ARISING OUT OF OR RELATED TO THIS AGREEMENT. '
            "EACH PARTY'S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THIS "
            'AGREEMENT SHALL NOT EXCEED FIVE HUNDRED THOUSAND US DOLLARS ($500,000), '
            'REGARDLESS OF THE FORM OF ACTION.'
        ),
        p(),
        h1('11. NON-COMPETE'),
        p(
            'During the term of this Agreement and for a period of twenty-four (24) months '
            'thereafter, Service Provider shall not directly solicit or engage any employee of '
            "Client who was involved in the management or receipt of the Services without "
            "Client's prior written consent."
        ),
        p(),
        h1('12. GENERAL PROVISIONS'),
        h2('12.1 Governing Law'),
        p(GOVLAW_BODY),
        h2('12.2 Entire Agreement'),
        p(ENTIRE_AGREEMENT_BODY),
        h2('12.3 Amendments'),
        p(AMENDMENTS_BODY),
        h2('12.4 Severability'),
        p(SEVERABILITY_BODY),
        p(),
        h1('SIGNATURES'),
    ] + SIGNATURES_BLOCK
    return paras


# ── v2 ────────────────────────────────────────────────────────────────────────

def make_v2():
    paras = [
        p('NORTHWIND TRADERS, INC.', bold=True, size=36, align='center'),
        p('MASTER SERVICES AGREEMENT', bold=True, size=28, align='center'),
        p('Version 2.0  |  Effective Date: January 1, 2025  |  Revised: March 1, 2025', align='center'),
        p(),
        p(PARTIES),
        p(),
        p(RECITALS),
        p(),
        h1('1. DEFINITIONS'),
    ]
    for d in DEFINITIONS:
        paras.append(p(d))
    paras += [
        p(),
        h1('2. TERM'),
        p(
            'This Agreement commences on the Effective Date and continues for an initial term of '
            'twenty-four (24) months, unless earlier terminated in accordance with Section 9. '
            'Thereafter, this Agreement shall automatically renew for successive twelve-month '
            'periods unless either party provides written notice of non-renewal at least '
            'sixty (60) days prior to the end of the then-current term.'
        ),
        p(),
        h1('3. SERVICES'),
        p(SERVICES_BODY),
        p(),
        h1('4. FEES AND PAYMENT'),
        p(
            'Client shall pay all undisputed invoices within thirty (30) days of the invoice '
            'date (Net 30). Invoices not disputed in good faith within ten (10) days of '
            'receipt are deemed accepted. Late payments shall accrue interest at one and '
            'one-half percent (1.5%) per month.'
        ),
        p(),
        h1('5. SERVICE LEVELS'),
        h2('5.1 Uptime Commitment'),
        p(
            'Service Provider guarantees ninety-nine point nine percent (99.9%) monthly uptime '
            'for the production environment, excluding Scheduled Maintenance Windows. '
            'Uptime is calculated as: ((total minutes - downtime minutes) / total minutes) x 100.'
        ),
        h2('5.2 Remedies'),
        p(SLA_REMEDIES_BODY),
        p(),
        h1('6. DATA HANDLING'),
        h2('6.1 Data Residency'),
        p(
            'All Client data processed under this Agreement shall be stored and processed '
            'within data centers located in the United States or the European Union, as '
            'designated by Client in writing at the time of provisioning.'
        ),
        h2('6.2 Security'),
        p(SECURITY_BODY),
        p(),
        h1('7. INTELLECTUAL PROPERTY'),
        p(IP_BODY),
        p(),
        h1('8. CONFIDENTIALITY'),
        p(CONFIDENTIALITY_BODY),
        p(),
        h1('9. TERM AND TERMINATION'),
        h2('9.1 Termination for Convenience'),
        p(
            'Either party may terminate this Agreement for any reason by providing thirty (30) '
            "days' prior written notice to the other party."
        ),
        h2('9.2 Termination for Cause'),
        p(TERMINATION_CAUSE_BODY),
        p(),
        h1('10. LIMITATION OF LIABILITY'),
        p(
            'NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL, '
            'SPECIAL, OR EXEMPLARY DAMAGES ARISING OUT OF OR RELATED TO THIS AGREEMENT. '
            "EACH PARTY'S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THIS "
            'AGREEMENT SHALL NOT EXCEED ONE MILLION US DOLLARS ($1,000,000), '
            'REGARDLESS OF THE FORM OF ACTION.'
        ),
        p(),
        h1('11. NON-COMPETE'),
        p(
            'During the term of this Agreement and for a period of twelve (12) months '
            'thereafter, Service Provider shall not directly solicit or engage any employee of '
            "Client who was involved in the management or receipt of the Services without "
            "Client's prior written consent."
        ),
        p(),
        h1('12. INSURANCE'),
        p(
            'Service Provider shall maintain, at its own expense, the following insurance '
            'coverages throughout the term of this Agreement: (a) Commercial General Liability '
            'with limits of no less than two million US dollars ($2,000,000) per occurrence; '
            '(b) Professional Liability (Errors & Omissions) with limits of no less than '
            'two million US dollars ($2,000,000) per claim; and (c) Workers Compensation as '
            'required by applicable law. Service Provider shall name Client as an additional '
            'insured on the Commercial General Liability policy and provide certificates of '
            'insurance upon request.'
        ),
        p(),
        h1('13. GENERAL PROVISIONS'),
        h2('13.1 Governing Law'),
        p(GOVLAW_BODY),
        h2('13.2 Entire Agreement'),
        p(ENTIRE_AGREEMENT_BODY),
        h2('13.3 Amendments'),
        p(AMENDMENTS_BODY),
        h2('13.4 Severability'),
        p(SEVERABILITY_BODY),
        p(),
        h1('SIGNATURES'),
    ] + SIGNATURES_BLOCK
    return paras


# ── Generate ──────────────────────────────────────────────────────────────────

out_dir = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(out_dir, exist_ok=True)

write_docx(os.path.join(out_dir, 'Northwind-MSA-v1.docx'), make_v1())
write_docx(os.path.join(out_dir, 'Northwind-MSA-v2.docx'), make_v2())

print('Done.')
