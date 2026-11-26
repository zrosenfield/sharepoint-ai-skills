from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from nw_data import BRAND, DISCLAIMER, PRODUCTS, CUSTOMERS
W, H = Inches(13.333), Inches(7.5)
C = lambda k: RGBColor.from_string(BRAND.get(k, k))
FONT, FONT_B = "Segoe UI", "Segoe UI Semibold"

def new_prs():
    p = Presentation(); p.slide_width, p.slide_height = W, H; return p

def box(s, x, y, w, h, fill=None, shape=MSO_SHAPE.RECTANGLE, line=None):
    sh = s.shapes.add_shape(shape, x, y, w, h)
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = C(fill)
    else: sh.fill.background()
    if line: sh.line.color.rgb = C(line); sh.line.width = Pt(1)
    else: sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def text(s, x, y, w, h, t, size=18, color="ink", bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=None):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = anchor
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        r = p.add_run(); r.text = ln; f = r.font; f.size = Pt(size); f.color.rgb = C(color); f.bold = bold
        f.name = font or (FONT_B if bold else FONT)
    return tb

def logo(s, x, y, dark=False):
    b = box(s, x, y, Inches(0.42), Inches(0.42), "teal", MSO_SHAPE.ROUNDED_RECTANGLE)
    b.text_frame.text = "N"; r = b.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = C("FFFFFF"); r.font.name = FONT_B
    b.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    text(s, x + Inches(0.55), y + Inches(0.04), Inches(3), Inches(0.4), "Northwind Cloud", 14, "FFFFFF" if dark else "navy", True)

def chrome(s, role, dark=False, internal=False):
    if not dark:
        box(s, 0, 0, W, Inches(0.12), "teal")
    text(s, Inches(0.6), H - Inches(0.45), Inches(8), Inches(0.3), DISCLAIMER, 9, "B8C4D6" if dark else "grey")
    text(s, W - Inches(3.6), H - Inches(0.45), Inches(3), Inches(0.3), role.upper(), 9, "B8C4D6" if dark else "grey", True, PP_ALIGN.RIGHT)
    if internal:
        b = box(s, W - Inches(3.4), Inches(0.35), Inches(2.8), Inches(0.45), "coral", MSO_SHAPE.ROUNDED_RECTANGLE)
        text(s, W - Inches(3.4), Inches(0.42), Inches(2.8), Inches(0.35), "INTERNAL ONLY", 13, "FFFFFF", True, PP_ALIGN.CENTER)

def heading(s, t, kicker=None):
    if kicker: text(s, Inches(0.6), Inches(0.45), Inches(9), Inches(0.35), kicker.upper(), 12, "teal", True)
    text(s, Inches(0.6), Inches(0.8), Inches(11.5), Inches(1.0), t, 32, "navy", True)

def notes(s, t): s.notes_slide.notes_text_frame.text = t

def add(prs): return prs.slides.add_slide(prs.slide_layouts[6])

def r_title(prs, title, d, **k):
    s = add(prs); box(s, 0, 0, W, H, "navy")
    box(s, 0, H - Inches(2.2), W, Inches(2.2), "0F2A4D")
    box(s, Inches(0.6), Inches(2.55), Inches(1.2), Inches(0.08), "teal")
    logo(s, Inches(0.6), Inches(0.6), dark=True)
    text(s, Inches(0.6), Inches(2.85), Inches(11), Inches(2), title, 44, "FFFFFF", True)
    text(s, Inches(0.6), Inches(4.75), Inches(9), Inches(0.5), k.get("customer_line") or d.get("sub", ""), 20, "9FE3E2")
    chrome(s, "Title", dark=True)
    notes(s, "Open with the customer's goal, not our logo. One sentence on why we asked for this time.")
    return s

def r_agenda(prs, title, d, **k):
    s = add(prs); heading(s, title, "Agenda"); chrome(s, "Agenda")
    for i, it in enumerate(d["items"]):
        y = Inches(2.1) + i * Inches(0.92)
        c = box(s, Inches(0.8), y, Inches(0.62), Inches(0.62), "teal" if i == 0 else "sky", MSO_SHAPE.OVAL)
        text(s, Inches(0.8), y + Inches(0.1), Inches(0.62), Inches(0.45), str(i + 1), 18, "FFFFFF" if i == 0 else "navy", True, PP_ALIGN.CENTER)
        text(s, Inches(1.7), y + Inches(0.1), Inches(9), Inches(0.5), it, 22, "ink")
    notes(s, "Confirm the agenda and ask what they would add. Keep to time.")
    return s

def cards(s, items, y=Inches(3.0), h=Inches(2.9), accent="teal"):
    n = len(items); gap = Inches(0.35); w = (W - Inches(1.2) - gap * (n - 1)) / n
    for i, (a, b) in enumerate(items):
        x = Inches(0.6) + i * (w + gap)
        box(s, x, y, w, h, "light", MSO_SHAPE.ROUNDED_RECTANGLE)
        box(s, x + Inches(0.35), y + Inches(0.4), Inches(0.5), Inches(0.08), accent)
        text(s, x + Inches(0.35), y + Inches(0.65), w - Inches(0.7), Inches(0.6), a, 22, "navy", True)
        text(s, x + Inches(0.35), y + Inches(1.35), w - Inches(0.7), h - Inches(1.5), b, 16, "ink")

def r_problem(prs, title, d, **k):
    s = add(prs); heading(s, title, "The challenge"); chrome(s, "Problem")
    text(s, Inches(0.6), Inches(1.95), Inches(11), Inches(0.6), d["lead"], 20, "grey")
    cards(s, d["pains"], accent="coral")
    notes(s, "Ask which of these three hurts most today, then go deep on that one. Use their words in the follow-up.")
    return s

def r_solution(prs, title, d, **k):
    p = d["product"]; info = PRODUCTS[p]
    s = add(prs); heading(s, p, info["sol"]); chrome(s, "Solution")
    text(s, Inches(0.6), Inches(1.75), Inches(11), Inches(0.6), info["tag"], 22, "teal", True)
    cards(s, info["caps"])
    notes(s, f"{p}: tie each capability to a pain they named. Offer a 10-minute demo of the first capability if time allows.")
    return s

def r_proof(prs, title, d, **k):
    s = add(prs); heading(s, title, "Proof"); chrome(s, "Proof")
    n = len(d["stats"]); w = (W - Inches(1.2)) / n
    for i, (a, b) in enumerate(d["stats"]):
        x = Inches(0.6) + i * w
        text(s, x, Inches(2.5), w - Inches(0.3), Inches(1.4), a, 66, "teal", True)
        text(s, x, Inches(3.95), w - Inches(0.4), Inches(1.0), b, 20, "ink")
    text(s, Inches(0.6), Inches(6.35), Inches(12), Inches(0.4), d["source"], 11, "grey")
    notes(s, "Use these numbers verbatim with the source line. Do not round up or combine them.")
    return s

def r_story(prs, title, d, **k):
    c = d["customer"]; info = CUSTOMERS[c]
    s = add(prs); heading(s, c, f"Customer story | {info['ind']}"); chrome(s, "Customer story")
    box(s, Inches(0.6), Inches(1.95), Inches(6.6), Inches(4.2), "navy", MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, Inches(1.0), Inches(2.25), Inches(5.9), Inches(2.6), "\u201C" + info["quote"] + "\u201D", 24, "FFFFFF", True)
    text(s, Inches(1.0), Inches(5.05), Inches(5.9), Inches(0.8), info["who"], 14, "9FE3E2")
    for i, (a, b) in enumerate(info["outcomes"]):
        y = Inches(1.95) + i * Inches(1.45)
        text(s, Inches(7.7), y, Inches(2.4), Inches(0.9), a, 40, "teal", True)
        text(s, Inches(10.0), y + Inches(0.2), Inches(2.8), Inches(0.9), b, 16, "ink")
    text(s, Inches(7.7), Inches(6.35), Inches(5), Inches(0.3), "Reference approved. Product: " + info["prod"], 10, "grey")
    notes(s, f"{c} is reference-approved. Offer a reference call only through the customer reference program.")
    return s

def r_pricing(prs, title, d, **k):
    internal = d.get("internal", False)
    s = add(prs); heading(s, title, "Packaging"); chrome(s, "Pricing", internal=internal)
    cards(s, [(a, b + "\n\n" + c) for a, b, c in d["tiers"]], accent="coral" if internal else "gold")
    notes(s, "Internal guidance only. Never show this slide to a customer." if internal else "Show packages, not prices. Route price questions to a quote.")
    return s

def r_next(prs, title, d, **k):
    s = add(prs); heading(s, title, "Next steps"); chrome(s, "Next steps")
    box(s, Inches(0.9), Inches(3.05), W - Inches(1.8), Inches(0.06), "sky")
    n = len(d["steps"]); w = (W - Inches(1.2)) / n
    for i, (when, what, why) in enumerate(d["steps"]):
        x = Inches(0.6) + i * w
        box(s, x + Inches(0.3), Inches(2.85), Inches(0.45), Inches(0.45), "teal", MSO_SHAPE.OVAL)
        text(s, x + Inches(0.3), Inches(3.55), w - Inches(0.5), Inches(0.4), when, 14, "teal", True)
        text(s, x + Inches(0.3), Inches(3.95), w - Inches(0.5), Inches(0.6), what, 24, "navy", True)
        text(s, x + Inches(0.3), Inches(4.6), w - Inches(0.5), Inches(1.0), why, 16, "ink")
    notes(s, "Agree owners and a date for step one before the meeting ends.")
    return s

def r_close(prs, title, d, **k):
    s = add(prs); box(s, 0, 0, W, H, "navy"); logo(s, Inches(0.6), Inches(0.6), dark=True)
    text(s, Inches(0.6), Inches(2.7), Inches(11), Inches(1.2), title, 54, "FFFFFF", True)
    text(s, Inches(0.6), Inches(4.0), Inches(11), Inches(0.6), k.get("contact") or "Your Northwind account team", 20, "9FE3E2")
    chrome(s, "Close", dark=True)
    notes(s, "Recap the one next step and who owns it.")
    return s

RENDER = {"Title": r_title, "Agenda": r_agenda, "Problem": r_problem, "Solution": r_solution, "Proof": r_proof,
          "Customer story": r_story, "Pricing": r_pricing, "Next steps": r_next, "Close": r_close}

def set_props(prs, title, subject="", keywords=""):
    cp = prs.core_properties; cp.title = title; cp.author = "Northwind Cloud Sales Enablement"; cp.subject = subject; cp.keywords = keywords
