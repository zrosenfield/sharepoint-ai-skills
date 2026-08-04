---
name: deck-assembly
description: Assembles a new HTML presentation by selecting content from existing PowerPoint source decks and rendering it in a polished Copilot-themed design. Use when the user wants to build a new deck from content in other decks — triggers include "make a new deck using slides from," "combine these decks," "take the roadmap from this deck and the intro from that one," or "assemble a presentation for this customer." Produces a self-contained HTML file that opens in any browser, navigates with arrow keys, and looks like a premium dark-themed Microsoft AI briefing deck.
---

# Deck Assembly

This skill reads content from PowerPoint decks and generates a complete HTML presentation. The visual output is always the Copilot dark theme — you never try to replicate the source deck's visual style. Instead you extract the content (numbers, quotes, key facts, speaker info) and choose the right visual treatment for each piece of information.

Do not generate Python scripts. Your output is the complete HTML file, delivered as text.

---

## The Core Principle

**Every piece of content has a natural visual form. Your job is to find it.**

A number is not text — it is a stat card or a statement slide. A quote is not a bullet — it is a quote slide. A name and title is not a paragraph — it is a profile slide. Before you decide to use bullets, ask whether the content is actually better shown as a number, a card, a bar, or a single focused visual.

When in doubt: **fewer words, bigger visual.**

---

## Content Pattern Recognition

Read these rules before making any slide type decisions. Apply them strictly.

### Numbers and percentages — always visual, never textual

If source content contains a number, percentage, dollar figure, ratio, or ranked score — regardless of how it appears in the source — it must become a visual element. It is never a bullet point.

| What you see in the source | What you use |
|---|---|
| One dominant number + 1–2 lines of context | `slide-statement` — number fills the slide |
| Two numbers being compared | `slide-stat cols-2` — one card each |
| Three or four numbers compared | `slide-stat cols-3` or `cols-4` |
| Percentages with category labels (survey, breakdown) | `slide-two-col` with `.bar-metric` rows |
| A before/after pair | `slide-stat cols-2` with contrasting card styles |

### Slide density signals the layout

Count the meaningful content items on the source slide — not counting the title.

| Content density | Layout to use |
|---|---|
| Title only, or ≤ 3 words total | `slide-section` or `slide-logo` |
| 1 number + 1–2 lines | `slide-statement` |
| 2–4 numbers or metrics | `slide-stat` |
| 1 person's name + role | `slide-profile` |
| 1 quoted sentence + attribution | `slide-quote` |
| 3–6 **named** capabilities, features, pillars, or roadmap items | `feature-grid` slide — **never bullets** |
| 3–5 parallel observations with no individual names | `slide-content` with bullet dots |
| 2 related but distinct blocks of content | `slide-two-col` |
| A photograph or image reference | `slide-image` |
| A brand mark or logo | `slide-logo` |

**The critical distinction:** If each item has its own name ("Copilot Pages", "Agent Marketplace", "Agentic Identity"), it is a named feature and must be a `feature-card`. If the items are observations or takeaways without individual names, bullets are acceptable.

### The bullet point is the last resort

Only use `slide-content` with bullets when the content is genuinely a list of parallel observations that have no individual names and cannot be better shown as numbers, cards, or a quote.

Ask yourself these questions in order before using bullets:
1. Does this slide have a headline number? → `slide-stat` or `slide-statement`
2. Does each item have its own name/title? → `feature-grid` with `feature-card` items
3. Is one item a quote? → `slide-quote`
4. Are there exactly two themes? → `slide-two-col`

Only if all four answers are "no" should you use bullets.

A slide that says "34% experts, 81% with AI, 87% AI alone" → three stat cards, not bullets.

A slide listing "Copilot Pages, Copilot Actions, Agent Marketplace, SharePoint+" → feature cards with icons, not bullets.

### Text that looks short is probably visual

PowerPoint speakers routinely put only 3–8 words on a slide because those words are meant to be the visual anchor for what they're saying, not a transcription. A slide with just "The Frontier Firm" is a `slide-section`. A slide with just "45%" and a caption sentence is a `slide-statement`. Do not pad these out into bullets.

---

## Slide Type Reference

Read `templates/copilot-theme.html`. That file defines every component, its CSS class names, and example HTML for each slide type. When generating the output, copy the HTML structure from that file exactly — do not improvise class names or invent new patterns.

**slide-title** — Deck opener. Badge pill + two-line H1 + subtitle. One or two orbs. Use for the first slide and dramatic section openers only.

**slide-stat** — One to four metric cards. Each card: large number + short label. Use `cols-1` through `cols-4`. Make one card `.hi` (highlighted, darker background, accent border) to indicate the most important or the "after" state. Use `grad-text` on the number you want to emphasize most; white on the others.

**slide-statement** — Single giant number dominates the entire slide. No card. Use for the one number that is the whole point of a slide. 160–180px, `grad-text`, short description below.

**slide-section** — Section break. Eyebrow label + accent bar + large left-aligned H2. Minimal. Use between major sections of the deck.

**slide-content** — Title + three to five bullet items with gradient dot markers. Use `<strong>` for the key phrase in each bullet. Keep bullets short — under 12 words each. This is the fallback only.

**slide-quote** — Giant gradient quotation mark, large centered quote text, attribution. Use for any attributed statement you find in the source.

**slide-profile** — Circular avatar ring + name + role + company. Use for speaker intros and customer spotlights. Use initials in the avatar when no photo is available.

**slide-two-col** — Title + two-column layout. Left column: bullets or bar metrics. Right column: a stat card, a second set of metrics, or supporting content. Use when you have two related but distinct ideas.

**feature-grid slide** — A plain `<div class="slide">` (no named slide class) with inline `display:flex;flex-direction:column;gap:28px` containing a title, optional subtitle, and a `<div class="feature-grid cols-N">`. Each item is a `<div class="feature-card [hi]">` with a `.feature-icon` (emoji), `.feature-name`, and `.feature-desc`. For roadmap slides, add a `.date-chip` above the icon. Use `cols-2` for 4 items (2×2), `cols-3` for 6 items (2×3), `cols-5` for a horizontal strip of 5 capabilities or milestones. Alternate `.hi` cards for visual rhythm.

**slide-logo** — Brand mark fills the slide. Extra-dark background. Use for company spotlights, logo reveals, or when a source slide has essentially nothing except a logo.

**slide-image** — Full-bleed image with dark overlay, text anchored to bottom. Use when the source references a photo, team shot, or the slide title alone suggests a visual moment ("The team", "Our journey", etc.). Use `class="img-bg placeholder"` when no actual image is available, and note this to the user.

---

## Visual Components Available Within Slides

These components can be composed inside any slide type. Use them to add visual richness without breaking the design system.

**`.bar-metric`** — A label, percentage value, and a horizontal fill bar. Use inside `col-card` or `slide-two-col` when content includes category-level percentages (e.g., talent breakdown, survey results by group). The bar width is set inline: `style="width: 75%"`.

**`.tag` / `.tag.accent`** — Small pill chip for category or status labels. Use inside stat cards to label "Before" vs "After" or category names.

**`.callout-num`** — A very large number (120px) used inline within a slide rather than inside a card. Useful when you want a number to dominate a content slide without a full card wrapper.

**`.divider`** — Thin horizontal separator. Use inside cards to separate two metrics stacked vertically.

**Gradient text** — Apply `class="grad-text"` to any text element to get the blue-to-lavender number gradient. Apply `class="brand-text"` for the purple-to-blue gradient. Use these on numbers, key words in titles, and the logo mark.

---

## Workflow

### Phase 1 — Read source content

Read each uploaded .pptx file. For each slide, extract: the title, all body text, every number or percentage you see (even if it is buried in a sentence), any quotes with attribution, speaker names and roles, and any source/attribution lines.

After reading, confirm: how many decks, how many slides, and list the most striking data points (top numbers, most quotable lines, speaker names).

### Phase 2 — Plan

Propose a numbered slide plan. For each entry: slide type, source, and a 1-line summary of what it will show. Explicitly call out where you are choosing a stat, statement, or bar layout because a number was present.

Wait for written confirmation before generating HTML.

### Phase 3 — Generate HTML

Generate the complete file. Start with the full boilerplate and CSS from `templates/copilot-theme.html` — every line. Then write the slide divs.

For each slide, copy the HTML structure for that type from the template and fill in the content. Do not abbreviate the CSS. Do not invent class names.

Deliver the complete file. Tell the user to save it as `.html` — no other files needed unless the deck uses `slide-image` with real photos, in which case the image files go in the same folder.

---

## Hard constraints

Never put a percentage, number, dollar amount, or ratio in a bullet point.

Never generate a slide that is only text when a number from that same slide could anchor a stat card or statement.

Never use `slide-content` for a source slide whose items each have their own name — those are feature cards.

Never use `slide-content` for a source slide that contains one dominant idea — find the visual form of that idea instead.

Never add statistics you did not find in the source material.

Do not proceed past Phase 2 without explicit user confirmation.
