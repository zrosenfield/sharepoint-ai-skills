# Design System

Visual tokens for the `exec-report` skill. The palette name in `report.palette` maps to a `palette-*` class on `<body>`. Token names mirror the reference template exactly — use these names when documenting or extending.

---

## Token Vocabulary

| Token | Role |
|---|---|
| `--bg` | Page background |
| `--surface` | Card / KPI card background |
| `--ink` | Primary text |
| `--ink-muted` | Secondary / label text |
| `--accent` | Primary brand color — trend line, bar fill, delta "up", highlight tags |
| `--accent-soft` | Very light tint of accent — trend area fill |
| `--negative` | Negative delta, "down" indicators |
| `--border` | Card and header/footer borders |
| `--grid` | Chart grid lines, subtle row separators |

Shape and type are palette-invariant:

| Token | Value |
|---|---|
| `--radius` | `16px` |
| `--radius-sm` | `10px` |
| `--pad` | `28px` (card inner padding) |
| `--gap` | `20px` (between blocks) |
| `--fs-hero` | `clamp(28px, 4.2vw, 52px)` |
| `--fs-kpi` | `clamp(42px, 5.8vw, 72px)` |
| `--fs-h2` | `18px` |
| `--fs-body` | `15px` |
| `--fs-small` | `13px` |
| `--fs-tiny` | `11px` |

Font stacks:
- `--font-display` / `--font-body`: `ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif`
- `--font-mono`: `ui-monospace, "SF Mono", Menlo, monospace` (used for axis labels)

---

## Palettes

### `warm-paper` (default)

Cream background, warm near-black ink, terra-cotta accent. Editorial feel. Good for finance, ops, and general business reports.

| Token | Value |
|---|---|
| `--bg` | `#faf7f2` |
| `--surface` | `#ffffff` |
| `--ink` | `#1a1814` |
| `--ink-muted` | `#7a7268` |
| `--accent` | `#c8553d` |
| `--accent-soft` | `#f9e6e2` |
| `--negative` | `#b91c1c` |
| `--border` | `#e8e2d8` |
| `--grid` | `#f0ece4` |

### `deep-ink`

Dark background, warm off-white ink, gold accent. High drama. Good for exec briefings, late-night vibes, or any report that needs to stand out.

| Token | Value |
|---|---|
| `--bg` | `#0f0e0c` |
| `--surface` | `#1a1916` |
| `--ink` | `#f2efe8` |
| `--ink-muted` | `#8a857a` |
| `--accent` | `#d4a574` |
| `--accent-soft` | `rgba(212,165,116,0.12)` |
| `--negative` | `#f87171` |
| `--border` | `#2a2925` |
| `--grid` | `#211f1c` |

### `clean-white`

Pure white, near-black ink, forest green accent. Maximum legibility. Good for compliance reports, all-hands, print-first contexts.

| Token | Value |
|---|---|
| `--bg` | `#ffffff` |
| `--surface` | `#f9fafb` |
| `--ink` | `#0a0a0a` |
| `--ink-muted` | `#6b6b6b` |
| `--accent` | `#2d5a3d` |
| `--accent-soft` | `#edf7f1` |
| `--negative` | `#dc2626` |
| `--border` | `#e5e7eb` |
| `--grid` | `#f3f4f6` |

### `slate`

Cool gray background, deep blue-gray ink, blue accent. Modern corporate. Closest to a traditional business dashboard.

| Token | Value |
|---|---|
| `--bg` | `#f1f5f9` |
| `--surface` | `#ffffff` |
| `--ink` | `#0f172a` |
| `--ink-muted` | `#64748b` |
| `--accent` | `#2563eb` |
| `--accent-soft` | `#eff6ff` |
| `--negative` | `#dc2626` |
| `--border` | `#e2e8f0` |
| `--grid` | `#f1f5f9` |

---

## Palette Selection Guide

| Audience / context | Recommended palette |
|---|---|
| General business, finance, operations | `warm-paper` |
| Executive briefing, premium feel | `deep-ink` |
| Compliance, legal, print-heavy | `clean-white` |
| Technical, product, modern corporate | `slate` |

**Default to `warm-paper`** unless the user specifies otherwise or the content clearly calls for a different mood.

---

## Badge Colors (table cells)

These are palette-invariant — same across all four themes.

| Key | Background | Text | Use for |
|---|---|---|---|
| `green` | `#d1fae5` | `#065f46` | On track, complete, approved |
| `amber` | `#fef3c7` | `#92400e` | At risk, pending, review |
| `red` | `#fee2e2` | `#991b1b` | Blocked, delayed, critical |
| `gray` | `#f1f5f9` | `#475569` | Not started, neutral |
| `blue` | `#dbeafe` | `#1e40af` | In review, informational |

---

## Status Dot Colors

| Key | Color | Use for |
|---|---|---|
| `green` | `#059669` | Complete, on track |
| `amber` | `#d97706` | At risk, delayed |
| `red` | `#dc2626` | Blocked, failed |
| `gray` | `#94a3b8` | Not started |
| `blue` | `#0284c7` | In review, pending |

---

## Typography Rules

- KPI values: `font-weight: 300`, `letter-spacing: -0.03em`, `font-variant-numeric: tabular-nums`
- Hero sentence: `font-weight: 400`, `letter-spacing: -0.02em`, `max-width: 22ch`
- Numbers in hero sentence: wrap in `<span class="num">` for tabular-nums treatment
- Accented words in hero: wrap in `<span class="accent">` for the palette's `--accent` color
- Card headings (`h2`): `font-weight: 500`, `letter-spacing: -0.01em`
- Labels and tags: all-caps, `letter-spacing: 0.08em`, `--ink-muted`

---

## Motion

All animations respect `prefers-reduced-motion`. With motion disabled:
- Bars render at full width immediately
- Trend line draws instantly (no dash animation)
- KPI values appear without the rise animation

The CSS `prefers-reduced-motion` block handles this automatically — no JS check needed.
