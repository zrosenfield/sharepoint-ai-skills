# Design System

Visual tokens for the `scorecard-matrix` skill. Inherits the full palette token system from `exec-report`. Extends it with heatmap color tables for pre-computed cell backgrounds.

---

## Token Vocabulary

Identical to `exec-report/references/design-system.md`. Reproduced here for self-contained reference.

| Token | Role |
|---|---|
| `--bg` | Page background |
| `--surface` | Card / section background |
| `--ink` | Primary text |
| `--ink-muted` | Secondary / label text |
| `--accent` | Primary brand color — winner border, rank badges, highlights |
| `--accent-soft` | Very light tint of accent — HIGH heatmap tier |
| `--negative` | Negative / low signal color |
| `--border` | Card and table borders |
| `--grid` | Row separators, subtle lines |

Shape and type are palette-invariant:

| Token | Value |
|---|---|
| `--radius` | `16px` |
| `--radius-sm` | `10px` |
| `--pad` | `28px` |
| `--gap` | `20px` |
| `--fs-h2` | `18px` |
| `--fs-body` | `15px` |
| `--fs-small` | `13px` |
| `--fs-tiny` | `11px` |

Font stacks:
- `--font-display` / `--font-body`: `ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif`
- `--font-mono`: `ui-monospace, "SF Mono", Menlo, monospace`

---

## Palettes

### `warm-paper` (default)

Cream background, terra-cotta accent. Editorial feel.

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

Dark background, gold accent. High drama for exec briefings.

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

Pure white, forest green accent. Maximum legibility.

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

Cool gray background, blue accent. Modern corporate.

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
| General business, vendor selection, operations | `warm-paper` |
| Executive briefing, competitive intelligence | `deep-ink` |
| Compliance, legal, print-heavy | `clean-white` |
| Technical, product, modern corporate | `slate` |

Default to `warm-paper` unless the user specifies otherwise.

---

## Heatmap Color Reference

### Overview

Heatmap cell backgrounds are pre-computed by the skill and emitted as inline `style="background:{{HEX}}"` attributes. No JavaScript required. Three tiers:

| Tier | Normalized score (t) | Signal |
|---|---|---|
| LOW | t < 0.35 | Below expectations — muted warm-red tint |
| MID | 0.35 ≤ t < 0.65 | Meets bar — neutral surface |
| HIGH | t ≥ 0.65 | Strong performance — accent tint |

Normalization: `t = (score - 1) / (scale - 1)`

### Per-Palette Hex Values

Use the exact hex values below. Do not interpolate or compute colors at render time.

#### `warm-paper`

| Tier | Hex | Description |
|---|---|---|
| LOW | `#fde8e8` | Soft rose — muted negative tint on cream background |
| MID | `#ffffff` | White surface — neutral |
| HIGH | `#f9e6e2` | Light terra-cotta tint — accent-soft |

#### `deep-ink`

| Tier | Hex | Description |
|---|---|---|
| LOW | `#3d1e1e` | Dark muted red — visible on dark background |
| MID | `#1a1916` | Surface color — neutral |
| HIGH | `#2e2418` | Dark gold tint — accent-soft analogue for dark theme |

#### `clean-white`

| Tier | Hex | Description |
|---|---|---|
| LOW | `#fee2e2` | Light red tint — negative signal on white |
| MID | `#f9fafb` | Surface gray — neutral |
| HIGH | `#edf7f1` | Light green tint — accent-soft |

#### `slate`

| Tier | Hex | Description |
|---|---|---|
| LOW | `#fee2e2` | Light red — same as clean-white negative signal |
| MID | `#ffffff` | White surface — neutral |
| HIGH | `#eff6ff` | Light blue tint — accent-soft |

### Quick-Reference Table

| Palette | LOW | MID | HIGH |
|---|---|---|---|
| `warm-paper` | `#fde8e8` | `#ffffff` | `#f9e6e2` |
| `deep-ink` | `#3d1e1e` | `#1a1916` | `#2e2418` |
| `clean-white` | `#fee2e2` | `#f9fafb` | `#edf7f1` |
| `slate` | `#fee2e2` | `#ffffff` | `#eff6ff` |

### Worked Examples

**warm-paper, scale=5:**

| Score | t | Tier | Background |
|---|---|---|---|
| 1 | 0.00 | LOW | `#fde8e8` |
| 2 | 0.25 | LOW | `#fde8e8` |
| 3 | 0.50 | MID | `#ffffff` |
| 4 | 0.75 | HIGH | `#f9e6e2` |
| 5 | 1.00 | HIGH | `#f9e6e2` |

**slate, scale=10:**

| Score | t | Tier | Background |
|---|---|---|---|
| 1–4 | 0.00–0.33 | LOW | `#fee2e2` |
| 5–6 | 0.44–0.56 | MID | `#ffffff` |
| 7–10 | 0.67–1.00 | HIGH | `#eff6ff` |

---

## Rank Badge Colors

Palette-invariant. Same across all four themes.

| Rank | Background | Text | Class |
|---|---|---|---|
| 1st | `#fef3c7` | `#92400e` | `sc-rank-1` (gold) |
| 2nd | `#e5e7eb` | `#374151` | `sc-rank-2` (silver) |
| 3rd | `#fce7d8` | `#7c3a14` | `sc-rank-3` (bronze) |
| 4th+ | `var(--grid)` | `var(--ink-muted)` | `sc-rank-n` (plain) |

---

## Winner Row Highlight

The entity row with `rank = 1` gets class `sc-winner`. CSS applies:
- `border-left: 3px solid var(--accent)` on the row
- `background: var(--accent-soft)` at 30% opacity on the entity label cell only

This creates a subtle left-accent emphasis without overwhelming the heatmap cell backgrounds.

---

## Typography Rules

- Column headers (dimension names): two-line, small caps label + weight percentage below, `letter-spacing: 0.06em`, `--ink-muted`
- Score values: `font-size: 17px`, `font-weight: 500`, `font-variant-numeric: tabular-nums`
- Cell notes: `font-size: var(--fs-tiny)`, `color: var(--ink-muted)`, single line below score
- Weighted total column: `font-weight: 700`, slightly larger (`font-size: 15px`)
- Averages row: `font-style: italic`, `color: var(--ink-muted)`
- Entity labels: `font-weight: 600`, `font-size: var(--fs-body)`

---

## Motion

The page is fully readable with JavaScript disabled. One optional JS enhancement: on palette change (in sample page only), re-applying the palette class is handled by inline JS on the palette switcher buttons. No animation is needed for the matrix table itself — heatmap cells are static inline styles.

All animations respect `prefers-reduced-motion`.
