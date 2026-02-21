---
name: forest-style
description: Applies the forest-style brand system to any visual output, document, web content, presentation, table, list, or interface element. Enforces the color palette, typography, spacing, component styles, and voice guidelines to ensure consistent brand expression. Use this skill whenever creating or reviewing content that must conform to forest-style brand standards.
---

# Forest-Style Brand Skill

Use this skill whenever creating any visual output, document, web content, presentation, table, list, or interface element for the forest-style brand. This skill ensures all outputs are visually consistent with the brand.

---

## Brand Identity

The forest-style brand is rooted in the Pacific Northwest. It evokes the natural beauty of Central Oregon — mountains, forests, rivers — and a sense of warmth, purpose, and community care. All outputs should feel **grounded, approachable, and inspired by the outdoors**.

---

## Color Palette

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Primary** | Forest Green | `#1A5C38` | Headers, primary buttons, key UI elements, nav bars |
| **Accent** | Canyon Red | `#C0392B` | Highlights, CTAs, badges, borders |
| **Sky** | Oregon Blue | `#4A9CC7` | Secondary UI, links, icons, info states |
| **Earth** | Meadow Green | `#5A8A3C` | Secondary backgrounds, tags, progress bars |
| **Background** | Warm Cream | `#F5F0E8` | Page backgrounds, card backgrounds |
| **Surface** | White | `#FFFFFF` | Content cards, modals, table rows |
| **Text Primary** | Deep Forest | `#1A2E1A` | Body copy, headings |
| **Text Secondary** | Slate | `#5C6B5C` | Captions, metadata, placeholder text |
| **Border** | Soft Sage | `#C8D8C0` | Dividers, table borders, input outlines |

### Color Usage Rules
- **Never** use Canyon Red as a large background — it should punctuate, not dominate
- Forest Green is the primary brand color and should anchor every layout
- Warm Cream replaces pure white for backgrounds to maintain warmth
- Reserve Oregon Blue for interactive and informational elements (links, tooltips, info banners)

---

## Typography

### Typeface Hierarchy
| Level | Font | Weight | Size | Color |
|-------|------|--------|------|-------|
| Display / Logo | **Montserrat** | 800 ExtraBold | 32–48px | Forest Green |
| H1 | **Montserrat** | 700 Bold | 28–36px | Forest Green |
| H2 | **Montserrat** | 600 SemiBold | 22–26px | Deep Forest |
| H3 | **Montserrat** | 600 SemiBold | 18–20px | Deep Forest |
| Body | **Open Sans** | 400 Regular | 15–16px | Deep Forest |
| Body Strong | **Open Sans** | 600 SemiBold | 15–16px | Deep Forest |
| Caption / Meta | **Open Sans** | 400 Regular | 12–13px | Slate |
| Button / Label | **Montserrat** | 700 Bold | 13–14px | Uppercase |

### Typography Rules
- All headings use **Montserrat uppercase or title case** — never lowercase for H1/H2
- Body copy uses **Open Sans** for maximum readability
- Letter-spacing on display text: `0.05em`
- Line-height for body: `1.6`; for headings: `1.2`

---

## Logo Usage

- **Minimum size**: 120px wide (digital), 1 inch (print)
- **Clear space**: Equal to the height of the letter "C" in the wordmark on all sides
- **Approved backgrounds**: Warm Cream, White, Forest Green (use reversed white version)
- **Never** stretch, recolor, or add drop shadows to the logo
- **Never** place the logo on busy photography without an overlay

---

## Iconography

- Use **line icons** (2px stroke weight) for UI elements
- Icon style: rounded caps and joins — avoid sharp or angular styles
- Icons should use Forest Green or Slate; Canyon Red only for alerts and errors
- Nature-themed icons preferred where contextually appropriate: mountains, trees, rivers, compass

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

- **Border radius**: `6px` for cards/inputs; `4px` for buttons; `999px` for pills/badges; `0px` for tables
- **Grid**: 12-column, `24px` gutters, max-width `1200px`
- Always use ample white space — avoid dense, cluttered layouts

---

## Component Styles

### Buttons

| Variant | Background | Text | Border | Hover |
|---------|-----------|------|--------|-------|
| Primary | Forest Green `#1A5C38` | White | — | Darken 10% |
| Secondary | White | Forest Green | 2px Forest Green | Warm Cream bg |
| Danger | Canyon Red `#C0392B` | White | — | Darken 10% |
| Ghost | Transparent | Forest Green | — | Warm Cream bg |

- Border radius: `4px`
- Font: Montserrat 700, uppercase, 13px, letter-spacing `0.08em`
- Padding: `10px 20px`

### Cards
- Background: `#FFFFFF`
- Border: `1px solid #C8D8C0` (Soft Sage)
- Border radius: `6px`
- Box shadow: `0 2px 8px rgba(26, 46, 26, 0.08)`
- Padding: `24px`
- Hover state: shadow deepens to `0 4px 16px rgba(26, 46, 26, 0.14)`

### Tables

| Element | Style |
|---------|-------|
| Header row | bg Forest Green, text White, Montserrat 600 uppercase 12px |
| Even rows | bg White |
| Odd rows | bg `#F9F6F1` (very light warm cream) |
| Row hover | bg `#EEF4E8` (light sage tint) |
| Border | 1px solid Soft Sage `#C8D8C0` |
| Cell padding | 12px 16px |

### Lists
- **Unordered**: Custom bullet — small filled circle in Canyon Red, 6px, vertically centered
- **Ordered**: Numbers in Forest Green, bold
- **Checklist**: Forest Green fill with white checkmark on checked state
- List item line-height: `1.7`
- Nested list indent: `20px`

### Forms & Inputs
- Border: `1.5px solid Soft Sage`
- Border radius: `6px`
- Focus border: `2px solid Forest Green` with `box-shadow: 0 0 0 3px rgba(26,92,56,0.15)`
- Label: Montserrat 600, 13px, Deep Forest, uppercase
- Placeholder: Slate `#5C6B5C`
- Error state: Canyon Red border with small red error message below

### Badges & Tags
- Border radius: `999px` (pill)
- Font: Montserrat 600, 11px, uppercase
- Padding: `3px 10px`

| Variant | Background | Text |
|---------|-----------|------|
| Green | `#DFF0E4` | Forest Green |
| Red | `#FADEDC` | Canyon Red |
| Blue | `#D6EAF5` | Oregon Blue |
| Neutral | `#E8EDE8` | Slate |

### Navigation / Headers
- Background: Forest Green `#1A5C38`
- Text: White, Montserrat 600
- Active item: bottom border `3px solid Canyon Red`
- Hover: opacity 0.85
- Logo: always top-left; minimum 40px height in nav

### Alerts / Banners

| Type | Left Border | Background | Text |
|------|------------|------------|------|
| Info | Oregon Blue `#4A9CC7` | `#EBF5FB` | Deep Forest |
| Success | Meadow Green `#5A8A3C` | `#EAF5EC` | Deep Forest |
| Warning | `#E8A020` | `#FEF6E4` | Deep Forest |
| Error | Canyon Red `#C0392B` | `#FADEDC` | Deep Forest |

All alerts: `4px` left border, `6px` border-radius, `16px` padding, `14px` body text

### Dividers / Separators
- Default: `1px solid #C8D8C0`
- Heavy section break: `2px solid #C8D8C0`
- Decorative accent: `3px solid Canyon Red`, `40px wide`, centered (for section titles)

---

## Imagery & Illustration Guidelines

- **Photography**: Prioritize Pacific Northwest landscapes — Cascades, high desert, rivers, forests
- **Tone**: Natural light, warm/golden tones; avoid cold blue filters
- **People**: Diverse, community-focused, authentic — avoid overly polished stock imagery
- **Illustration style**: Flat geometric with slight warmth; nature icons using bold shapes and the brand color palette
- **Image overlays**: Use `rgba(26, 46, 26, 0.45)` Forest Green overlay when placing text over photos

---

## Voice & Tone

- **Warm and community-first**: Write as if speaking to a neighbor, not a customer
- **Action-oriented**: Use active verbs — "Connect," "Build," "Grow," "Catalyze"
- **Grounded**: Reference the place, the region, and the people when relevant
- **Inclusive**: Avoid jargon; write at an accessible reading level
- **Concise**: Short sentences. No filler. Say what matters.

---

## Do / Don't Summary

| ✅ Do | ❌ Don't |
|-------|---------|
| Use Forest Green as the anchor color | Use Canyon Red as a dominant background |
| Maintain generous white space | Crowd elements together |
| Use Montserrat for all headings | Use decorative or script fonts |
| Apply Warm Cream for page backgrounds | Use pure white everywhere |
| Use rounded, friendly icon styles | Use sharp or aggressive icon styles |
| Keep imagery warm and natural | Use cold, corporate stock photography |
| Uppercase labels and button text | Use all-lowercase for headings |
