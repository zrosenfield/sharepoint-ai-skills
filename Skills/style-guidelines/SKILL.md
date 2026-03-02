# Brand Style Skill — Template

Use this skill whenever creating any visual output, document, web content, presentation, table, list, or interface element for **[Your Organization]**. This skill ensures all outputs are visually consistent with the brand.

> **How to use this template:** Replace every `[placeholder]` and the example values below with your organization's actual brand values. Delete this callout when done.

---

## Brand Identity

[Your Organization] is a [brief description — industry, mission, or community focus]. The brand evokes [core brand feeling or theme — e.g., "innovation and trust" or "warmth and community"]. All outputs should feel **[adjective], [adjective], and [adjective]**.

---

## Color Palette

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Primary** | [Name] | `#000000` | Headers, primary buttons, key UI elements |
| **Accent** | [Name] | `#000000` | Highlights, CTAs, badges |
| **Secondary** | [Name] | `#000000` | Secondary UI, links, icons |
| **Background** | [Name] | `#000000` | Page and card backgrounds |
| **Surface** | White | `#FFFFFF` | Content cards, modals, table rows |
| **Text Primary** | [Name] | `#000000` | Body copy, headings |
| **Text Secondary** | [Name] | `#000000` | Captions, metadata, placeholder text |
| **Border** | [Name] | `#000000` | Dividers, table borders, input outlines |

### Color Usage Rules
- **Never** use [Accent color] as a large background — it should punctuate, not dominate
- [Primary color] is the anchor color and should appear in every layout
- Reserve [Secondary color] for interactive and informational elements

---

## Typography

### Typeface Hierarchy
| Level | Font | Weight | Size | Color |
|-------|------|--------|------|-------|
| Display / Logo | **[Font]** | 800 ExtraBold | 32–48px | Primary |
| H1 | **[Font]** | 700 Bold | 28–36px | Primary |
| H2 | **[Font]** | 600 SemiBold | 22–26px | Text Primary |
| H3 | **[Font]** | 600 SemiBold | 18–20px | Text Primary |
| Body | **[Font]** | 400 Regular | 15–16px | Text Primary |
| Caption / Meta | **[Font]** | 400 Regular | 12–13px | Text Secondary |
| Button / Label | **[Font]** | 700 Bold | 13–14px | Uppercase |

### Typography Rules
- All headings use **[Font] title case** — never lowercase for H1/H2
- Body copy uses **[Font]** for readability
- Line-height for body: `1.6`; for headings: `1.2`

---

## Logo Usage

- **Minimum size**: 120px wide (digital), 1 inch (print)
- **Clear space**: [Define clearspace rule relative to a logo element]
- **Approved backgrounds**: [List approved background colors]
- **Never** stretch, recolor, or add drop shadows to the logo

---

## Iconography

- Use **[line / filled / outline]** icons with [stroke weight] stroke weight
- Icon style: [rounded / sharp] — describe the preferred aesthetic
- Icons should use [Primary color] or [Text Secondary]; [Accent] only for alerts/errors

---

## Spacing & Layout

| Token | Value | Usage |
|-------|-------|-------|
| `space-xs` | 4px | Tight inline gaps |
| `space-sm` | 8px | Component internal padding |
| `space-md` | 16px | Between related elements |
| `space-lg` | 24px | Section spacing |
| `space-xl` | 40px | Major section breaks |
| `space-2xl` | 64px | Page-level sections |

- **Border radius**: `[N]px` for cards/inputs; `[N]px` for buttons; `999px` for pills/badges
- **Grid**: 12-column, `24px` gutters, max-width `1200px`

---

## Component Styles

### Buttons
```
Primary:   bg [Primary]  | text White        | hover: darken 10%
Secondary: bg White      | text [Primary]    | border 2px [Primary] | hover: light bg
Danger:    bg [Danger]   | text White        | hover: darken 10%
Ghost:     bg transparent| text [Primary]    | hover: light bg
```
- Border radius: `[N]px`
- Font: [Font] 700, uppercase, `13px`
- Padding: `10px 20px`

### Cards
- Background: `#FFFFFF`
- Border: `1px solid [Border color]`
- Border radius: `[N]px`
- Box shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Padding: `24px`

### Tables
```
Header row:  bg [Primary]  | text White  | font [Font] uppercase 12px
Even rows:   bg White
Odd rows:    bg [light tint of Background]
Row hover:   bg [light tint of Primary]
Border:      1px solid [Border color]
Cell padding: 12px 16px
```

### Badges & Tags
- Border radius: `999px` (pill)
- Font: [Font] 600, 11px, uppercase
- Padding: `3px 10px`
- Variants: **Primary**, **Accent**, **Neutral** — define bg/text combos per variant

### Alerts / Banners
| Type | Border-left | Background | Text |
|------|------------|------------|------|
| Info | [Secondary] | [light tint] | Text Primary |
| Success | [Success color] | [light tint] | Text Primary |
| Warning | [Warning color] | [light tint] | Text Primary |
| Error | [Danger color] | [light tint] | Text Primary |

All alerts: `4px` left border, `6px` border-radius, `16px` padding

---

## Voice & Tone (for AI-generated content)

- **[Tone quality 1]**: [Description — e.g., "Write as if speaking to a peer, not a customer"]
- **[Tone quality 2]**: [Description — e.g., "Use active verbs and direct language"]
- **[Tone quality 3]**: [Description — e.g., "Reference the mission and values when relevant"]
- **Concise**: Short sentences. No filler. Say what matters.

---

## Do / Don't Summary

| ✅ Do | ❌ Don't |
|-------|---------|
| Use [Primary] as the anchor color | Use [Accent] as a dominant background |
| Maintain generous white space | Crowd elements together |
| Use [Heading font] for all headings | Use decorative or script fonts |
| Keep imagery [describe style] | Use [describe what to avoid] |
