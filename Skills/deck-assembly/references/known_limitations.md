# Known Limitations — deck-assembly v1

Edge cases and known gaps to share with users when relevant.

---

## Output format

The skill produces an HTML file, not a .pptx file. The HTML can be opened in any browser, shared as a file, or presented full-screen. It cannot be edited in PowerPoint or imported back into a deck tool without manual work.

---

## Image display

Images extracted from source decks are saved to a slide_images folder. The HTML file references them by relative path. The user must keep the slide_images folder in the same directory as the HTML file — if they move the HTML without the folder, images will appear broken.

WMF and EMF format images (used by older Office clip art and some diagrams) are skipped during extraction because browsers cannot display them. If a slide relies heavily on WMF/EMF clip art, those shapes will be absent from the HTML output.

---

## Charts and SmartArt

Chart shapes are detected but their data and rendering cannot be extracted. The HTML shows a placeholder div where the chart was. If chart content matters, the user should screenshot the chart from the source deck and manually add it to the HTML as an image.

SmartArt is similarly replaced with a placeholder. A screenshot-to-image workaround applies here too.

---

## Fonts

The HTML references font families by name from the source deck (e.g., "Calibri Light", "Gill Sans"). If those fonts are not installed on the machine viewing the HTML, the browser substitutes a fallback. The text will reflow and sizing may shift slightly. This is a browser limitation and cannot be avoided without embedding font files.

---

## Colors from theme references

Some text and shape colors in .pptx files are defined as references to a theme color slot rather than as direct RGB values. The extraction script resolves these by reading the theme color scheme from the slide master. If theme resolution fails for a particular element, the color will be null in the JSON and the AI will infer a readable color from context. This inference is approximate — visually verify the output.

---

## Text split across runs

PowerPoint stores text in runs, and a single visible word may be split across two or three runs due to autocorrect history or internal formatting events. This does not affect HTML rendering since all runs are concatenated visually, but text substitutions applied by the AI during HTML generation operate on individual run text fields. A substitution for "Acme Corp" will only match if it falls entirely within one run. If a substitution misses, the user should make it manually in the HTML with a text editor.

---

## Slide positioning accuracy

Shape positions are extracted as percentages of slide dimensions and applied as CSS percentage values. For most slides this produces a faithful approximation. Slides that rely on precise pixel-level alignment or overlapping shapes with specific z-ordering may look slightly different from the original. The AI should stack shapes in the order they appear in the JSON, which generally preserves the intended layering.

---

## Gradient and picture backgrounds

Gradient slide backgrounds are simplified to a solid color using the first gradient stop. Picture backgrounds (where an image fills the entire slide) are not currently extracted and will fall back to a white or inherited solid color. If a slide has an important background image, the user can add it manually to the HTML as a background-image CSS property on the slide div.

---

## Animations and transitions

The HTML presentation has no animations or slide transitions. All content appears statically. This is by design — HTML-based rendering does not attempt to recreate PowerPoint animation sequences.

---

## File size

Decks with many high-resolution images will produce a large slide_images folder. The HTML file itself stays small since it references rather than embeds images. If sharing the output, the user needs to zip both the HTML file and the slide_images folder together.
