"""Shared helpers for generating the sample contracts (python-docx)."""
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

TODAY = date(2026, 11, 24)
NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x59, 0x59, 0x59)
BODY_FONT = "Calibri"

__all__ = [
    "TODAY", "date", "timedelta", "relativedelta", "fd", "iso", "Doc", "ob",
]


def fd(d):
    """Long US date, e.g. December 1, 2026."""
    return f"{d:%B} {d.day}, {d.year}"


def iso(d):
    return d.isoformat() if d else None


def _set_font(style_or_run_font, name, size=None, bold=None, color=None):
    f = style_or_run_font
    f.name = name
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if color is not None:
        f.color.rgb = color


def _east_asia(style):
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), BODY_FONT)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]


def _add_field(paragraph, instr):
    def _run_with(el):
        r = paragraph.add_run()
        r.font.size = Pt(8)
        r.font.color.rgb = GREY
        r._r.append(el)
        return r

    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    _run_with(b)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    _run_with(it)
    s = OxmlElement("w:fldChar")
    s.set(qn("w:fldCharType"), "separate")
    _run_with(s)
    r = paragraph.add_run("1")
    r.font.size = Pt(8)
    r.font.color.rgb = GREY
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    _run_with(e)


def _shade(cell, hex_fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcpr.append(shd)


def _repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trpr.append(el)


class Doc:
    """Thin builder that gives every sample contract the same professional look."""

    def __init__(self, header_text, footer_ref, title_meta):
        self.d = Document()
        d = self.d
        sec = d.sections[0]
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(sec, m, Inches(1))
        sec.header_distance = Inches(0.45)
        sec.footer_distance = Inches(0.45)

        normal = d.styles["Normal"]
        _set_font(normal.font, BODY_FONT, 10.5)
        _east_asia(normal)
        pf = normal.paragraph_format
        pf.space_after = Pt(6)
        pf.line_spacing = 1.1

        title = d.styles["Title"]
        _set_font(title.font, BODY_FONT, 18, True, NAVY)
        _east_asia(title)
        title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title.paragraph_format.space_after = Pt(4)

        h1 = d.styles["Heading 1"]
        _set_font(h1.font, BODY_FONT, 11.5, True, NAVY)
        _east_asia(h1)
        h1.paragraph_format.space_before = Pt(10)
        h1.paragraph_format.space_after = Pt(4)
        h1.paragraph_format.keep_with_next = True

        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hr = hp.add_run(header_text)
        hr.font.size = Pt(8)
        hr.font.color.rgb = GREY

        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = fp.add_run(f"{footer_ref}    |    Page ")
        r.font.size = Pt(8)
        r.font.color.rgb = GREY
        _add_field(fp, "PAGE")
        r = fp.add_run(" of ")
        r.font.size = Pt(8)
        r.font.color.rgb = GREY
        _add_field(fp, "NUMPAGES")

        cp = d.core_properties
        cp.title = title_meta
        cp.author = "Northwind Traders, Inc. (sample data)"
        cp.subject = "Sample contract for obligation-management demo (fictional)"

    # ---- blocks -------------------------------------------------------
    def title(self, text, subtitle=None):
        self.d.add_paragraph(text, style="Title")
        if subtitle:
            p = self.d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(14)
            r = p.add_run(subtitle)
            r.font.size = Pt(9.5)
            r.font.color.rgb = GREY

    def para(self, text, bold=False, italic=False, align="justify", indent=None, size=None, space_after=None):
        p = self.d.add_paragraph()
        if align == "justify":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif align == "center":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == "left":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if indent:
            p.paragraph_format.left_indent = Inches(indent)
            p.paragraph_format.right_indent = Inches(indent)
        if space_after is not None:
            p.paragraph_format.space_after = Pt(space_after)
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        return p

    def heading(self, text):
        self.d.add_paragraph(text, style="Heading 1")

    def section(self, num, caption, text):
        """Numbered clause: bold '9.2 Non-Renewal.' lead-in followed by the clause text."""
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        lead = f"{num} {caption}." if caption else f"{num}"
        r = p.add_run(lead)
        r.bold = True
        p.add_run(" " + text)
        return p

    def recitals(self, items, lead="Recitals"):
        self.heading(lead)
        for letter, t in zip("ABCDEFGH", items):
            p = self.d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            p.add_run(f"{letter}.\t{t}")

    def table(self, rows, header=True, widths=None, label_col=False):
        t = self.d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = self.d.styles["Table Grid"]
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.cell(i, j)
                cell.text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                run = p.add_run(str(val))
                run.font.size = Pt(9.5)
                if header and i == 0:
                    run.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    _shade(cell, "1F3864")
                elif label_col and j == 0:
                    run.bold = True
                    _shade(cell, "E8EDF4")
        if header:
            _repeat_header(t.rows[0])
        if widths:
            t.autofit = False
            for j, w in enumerate(widths):
                t.columns[j].width = Inches(w)
            for row in t.rows:
                for j, w in enumerate(widths):
                    row.cells[j].width = Inches(w)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def signatures(self, parties, intro="IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date."):
        """parties: list of dicts with company, name, title, date (date object)."""
        if intro:
            p = self.para(intro)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.keep_with_next = True
        t = self.d.add_table(rows=5, cols=len(parties))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for j, pt in enumerate(parties):
            lines = [
                (pt["company"].upper(), True),
                (f"By: /s/ {pt['name']}", False),
                (f"Name: {pt['name']}", False),
                (f"Title: {pt['title']}", False),
                (f"Date: {fd(pt['date'])}", False),
            ]
            for i, (txt, bold) in enumerate(lines):
                c = t.cell(i, j)
                c.text = ""
                para = c.paragraphs[0]
                para.paragraph_format.space_after = Pt(3)
                para.paragraph_format.keep_with_next = True
                r = para.add_run(txt)
                r.bold = bold
                r.font.size = Pt(10)
        return t

    def page_break(self):
        from docx.enum.text import WD_BREAK
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def save(self, path):
        self.d.save(path)


def ob(contractFile, counterparty, title, obligationText, clauseRef, sourceClause, party,
       category, triggerType, recurrence="None", nextDueDate=None, triggerEvent=None,
       risk="Medium", expected="track", reason=None, isTrap=False, trapType=None):
    return {
        "contractFile": contractFile,
        "counterparty": counterparty,
        "title": title,
        "obligationText": obligationText,
        "clauseRef": clauseRef,
        "sourceClause": sourceClause,
        "party": party,
        "category": category,
        "triggerType": triggerType,
        "recurrence": recurrence,
        "nextDueDate": iso(nextDueDate) if isinstance(nextDueDate, date) else nextDueDate,
        "triggerEvent": triggerEvent,
        "risk": risk,
        "expected": expected,
        "reason": reason,
        "isTrap": isTrap,
        "trapType": trapType,
    }
