# Rebuild the 4 PowerPoint templates as real example decks: a designed cover + the real approved slides.
import os, json, zipfile, re, shutil, glob
from nw_data import SLIDES, TEMPLATES
from nw_pptx import *
from pptx.util import Inches, Pt
PREF = {"Customer story": "NW-Story-Contoso.pptx", "Pricing": "NW-Pricing-Packages.pptx"}
def candidates(role):
    c = [s for s in SLIDES if s[1] == role and "Internal" not in s[5]]
    c.sort(key=lambda s: (0 if s[0] == PREF.get(role) else 1, 0 if "Cross-industry" in s[4] else 1, s[7], s[0]))
    return c
def pick(recipe):
    used, out = set(), []
    for role in recipe:
        for s in candidates(role):
            if s[0] not in used:
                used.add(s[0]); out.append(s); break
    return out
def cover(prs, kind, best, chosen):
    s = add(prs)
    box(s, 0, 0, W, H, "111827")
    box(s, 0, H - Inches(0.06), W, Inches(0.06), "9AC7F5")
    logo(s, Inches(0.6), Inches(0.55), dark=True)
    text(s, Inches(0.6), Inches(1.55), Inches(6), Inches(0.4), "DECK TEMPLATE  \u00B7  EXAMPLE", 13, "9AC7F5", True)
    text(s, Inches(0.6), Inches(2.0), Inches(12), Inches(1.0), kind, 48, "FFFFFF", True)
    text(s, Inches(0.6), Inches(3.05), Inches(11), Inches(0.9), best, 18, "C7D2E3")
    n = len(chosen); gap = Inches(0.12); tw = min(Inches(1.9), int((W - Inches(1.2) - gap * (n - 1)) / n)); th = int(tw * 9 / 16)
    y = Inches(4.55)
    for i, sl in enumerate(chosen):
        x = Inches(0.6) + i * (tw + gap)
        p = "thumbs/" + sl[0].replace(".pptx", ".jpg")
        if os.path.exists(p): s.shapes.add_picture(p, x, y, tw, th)
        text(s, x, y + th + Inches(0.08), tw, Inches(0.3), sl[1], 10, "9AA6B8")
    text(s, Inches(0.6), H - Inches(0.75), Inches(12), Inches(0.35),
         "%d approved slides in this order. Build a deck with this template and Copilot swaps in the best ones for your customer." % n, 12, "9AA6B8")
    notes(s, "Example of the %s template. Each slide after this cover is a real approved slide from the Slide Library." % kind)
BASE = 2147483648
def fix(path, k):
    off = BASE + 10000 * (k + 1)
    src = zipfile.ZipFile(path); out = path + ".tmp"; dst = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    def ren(m): return '%sid="%d"' % (m.group(1), off + (int(m.group(2)) - BASE))
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename == "ppt/presentation.xml" or re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", item.filename):
            t = data.decode("utf-8")
            t = re.sub(r'(<p:sldMasterId )id="(\d+)"', ren, t); t = re.sub(r'(<p:sldLayoutId )id="(\d+)"', ren, t)
            data = t.encode("utf-8")
        dst.writestr(item, data)
    dst.close(); src.close(); shutil.move(out, path)
order = sorted(glob.glob("content/slides/*.pptx")) + sorted(glob.glob("content/templates/*.pptx"))
report = {}
for (fn, kind, fmt, recipe, aud, n, best) in TEMPLATES:
    if fmt != "PowerPoint": continue
    roles = [r.strip() for r in recipe.split(",")]
    chosen = pick(roles)
    prs = new_prs(); cover(prs, kind, best, chosen)
    for sl in chosen:
        RENDER[sl[1]](prs, sl[2], sl[8])
    set_props(prs, kind + " template", "Template", recipe)
    path = "content/templates/" + fn; prs.save(path)
    fix(path, [os.path.basename(p) for p in order].index(fn))
    report[fn] = [sl[0] for sl in chosen]
json.dump(report, open("example_decks.json", "w"), indent=1)
for k, v in report.items(): print(k, len(v), v)
