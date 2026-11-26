import os, json
from nw_data import SLIDES, TEMPLATES
from nw_pptx import *
os.makedirs("content/slides", exist_ok=True); os.makedirs("content/templates", exist_ok=True)
for (fn, role, title, prods, inds, share, verb, order, d) in SLIDES:
    prs = new_prs(); RENDER[role](prs, title, d); set_props(prs, title, role, ", ".join(prods + inds))
    prs.save("content/slides/" + fn)
# Templates: placeholder slides showing the recipe
for (fn, kind, fmt, recipe, aud, n, best) in TEMPLATES:
    if fmt != "PowerPoint": continue
    prs = new_prs()
    r_title(prs, f"[Customer name]: {kind}", {"sub": "[Meeting date]  |  [Account team]"})
    for i, role in enumerate([r.strip() for r in recipe.split(",")][1:], start=2):
        s = add(prs); chrome(s, role)
        heading(s, f"[{role} slide]", f"Slide {i} of {n}")
        box(s, Inches(0.6), Inches(2.1), W - Inches(1.2), Inches(4.1), "light", MSO_SHAPE.ROUNDED_RECTANGLE)
        text(s, Inches(1.0), Inches(3.6), W - Inches(2), Inches(1), f"Deck Studio fills this with the best approved '{role}' slide from the Slide Library.", 18, "grey", align=PP_ALIGN.CENTER)
        notes(s, f"Recipe step {i}: {role}.")
    set_props(prs, kind + " template", "Template", recipe); prs.save("content/templates/" + fn)
print(len(os.listdir("content/slides")), "slides;", len(os.listdir("content/templates")), "templates")
