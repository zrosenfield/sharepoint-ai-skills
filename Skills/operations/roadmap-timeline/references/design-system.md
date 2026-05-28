# Design System — roadmap-timeline

Visual tokens, status colors, and typographic rules for the `roadmap-timeline` skill. The palette name in `report.palette` maps to a `palette-*` class on `<body>`. Token names are shared with the `exec-report` skill — the same four palettes and the same nine base tokens apply here.

---

## Token Vocabulary

| Token | Role |
|---|---|
| `--bg` | Page background |
| `--surface` | Card / panel background |
| `--ink` | Primary text |
| `--ink-muted` | Secondary / label text |
| `--accent` | Primary brand color — on-track blocks, today-line, milestone diamonds |
| `--accent-soft` | Very light tint of accent — planned-phase fill |
| `--negative` | Delayed / blocked status |
| `--border` | Swimlane borders, card borders, ruler lines |
| `--grid` | Track background, subtle separators |

Shape and type tokens are palette-invariant:

| Token | Value |
|---|---|
| `--radius` | `16px` |
| `--radius-sm` | `10px` |
| `--pad` | `28px` (card inner padding) |
| `--gap` | `20px` (between swimlane rows) |
| `--label-col-w` | `120px` (swimlane label column width) |
| `--track-h` | `48px` (swimlane track row height) |
| `--block-h` | `32px` (phase block height within track) |
| `--fs-h2` | `18px` |
| `--fs-body` | `15px` |
| `--fs-small` | `13px` |
| `--fs-tiny` | `11px` |

Font stacks (same as exec-report):
- `--font-display` / `--font-body`: `ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif`
- `--font-mono`: `ui-monospace, "SF Mono", Menlo, monospace` (used for ruler labels)

---

## Palettes

The four palettes are identical to `exec-report`. They are reproduced here for reference.

### `warm-paper` (default for milestone lists)

Cream background, warm near-black ink, terra-cotta accent. Good for onboarding sequences, project plans, and general business timelines.

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

Dark background, warm off-white ink, gold accent. Good for exec roadmap presentations, board decks.

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

Pure white, near-black ink, forest green accent. Good for compliance timelines, print-first plans.

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

### `slate` (default for roadmaps)

Cool gray background, deep blue-gray ink, blue accent. Modern corporate. Best for product roadmaps and migration timelines.

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

| Use case | Recommended palette |
|---|---|
| Product roadmap, sprint plan, migration timeline | `slate` |
| Executive presentation, board deck | `deep-ink` |
| Onboarding sequence, project milestone list | `warm-paper` |
| Compliance timeline, legal plan, print | `clean-white` |

**Default to `slate` for roadmap mode, `warm-paper` for milestones mode** unless the user specifies otherwise.

---

## Status Colors

Status-driven colors are palette-invariant — same values across all four themes. Phase blocks use background colors with adjustments for opacity and border. Milestone diamonds use the solid fill color.

| Status | CSS class | Background | Text / Border | Use for |
|---|---|---|---|---|
| `on-track` | `status-on-track` | `var(--accent)` at 85% opacity | white text | Actively progressing, on schedule |
| `at-risk` | `status-at-risk` | `#d97706` at 85% opacity | white text | Slipping or flagged |
| `delayed` | `status-delayed` | `var(--negative)` at 85% opacity | white text | Behind schedule, blocked |
| `complete` | `status-complete` | `#059669` | white text | Finished |
| `planned` | `status-planned` | `var(--accent-soft)` | `var(--ink-muted)` text, dashed `var(--border)` border | Not yet started |

For milestone diamonds, use the solid fill colors without opacity:

| Status | Diamond fill |
|---|---|
| `on-track` | `var(--accent)` |
| `at-risk` | `#d97706` |
| `delayed` | `var(--negative)` |
| `complete` | `#059669` |
| `planned` | `var(--ink-muted)` |

---

## Today-Line

The today-line uses `var(--accent)` as its color. It is a 2px wide vertical line with a small "Today" label chip at the top. The label chip uses `var(--accent)` background with white text.

---

## Status Dot Colors (milestones mode)

Matches the exec-report status dot palette exactly:

| Class | Color | Use for |
|---|---|---|
| `status-dot--green` | `#059669` | Complete, on track |
| `status-dot--amber` | `#d97706` | At risk |
| `status-dot--red` | `#dc2626` | Delayed, blocked |
| `status-dot--gray` | `#94a3b8` | Planned, not started |
| `status-dot--blue` | `#0284c7` | In review, informational |

---

## Typography Rules

- Report title: `font-weight: 600`, `letter-spacing: -0.01em`
- Report subtitle: `font-size: var(--fs-small)`, `color: var(--ink-muted)`
- Swimlane labels: `font-size: var(--fs-small)`, `font-weight: 500`, `color: var(--ink-muted)`, truncated with ellipsis
- Phase block labels: `font-size: var(--fs-tiny)`, `font-weight: 500`, white text, truncated
- Ruler month labels: `font-family: var(--font-mono)`, `font-size: var(--fs-tiny)`, `color: var(--ink-muted)`
- Milestone card title: `font-weight: 500`
- Milestone date badge: `font-variant-numeric: tabular-nums`, `font-size: var(--fs-small)`
- Group headings: all-caps, `letter-spacing: 0.08em`, `color: var(--ink-muted)`

---

## Motion

All animations respect `prefers-reduced-motion`. With motion disabled, phase blocks appear immediately without fade-in.

Phase blocks animate in with a subtle `opacity: 0 → 1` and `transform: translateY(4px) → none` entrance, staggered by swimlane row index. The today-line fades in after all blocks.
