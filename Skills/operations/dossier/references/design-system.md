# Design System

Visual tokens for the `dossier` skill. The palette name in `report.palette` maps to a `palette-*` class on `<body>`. Token names are identical to the `exec-report` skill — the two skills share the same design foundation and palette system.

---

## Token Vocabulary

| Token | Role |
|---|---|
| `--bg` | Page background |
| `--surface` | Card background |
| `--ink` | Primary text |
| `--ink-muted` | Secondary / label text |
| `--accent` | Primary brand color — tag pills, activity dots, quick-take text, status "up" |
| `--accent-soft` | Very light tint of accent — tag pill backgrounds |
| `--negative` | Negative / warning indicators |
| `--border` | Card and header/footer borders |
| `--grid` | Subtle separators, key-fact row dividers |

Shape and type are palette-invariant:

| Token | Value |
|---|---|
| `--radius` | `16px` |
| `--radius-sm` | `10px` |
| `--pad` | `28px` (card inner padding) |
| `--gap` | `20px` (between cards and sections) |
| `--fs-hero` | `clamp(28px, 4.2vw, 52px)` |
| `--fs-h2` | `18px` |
| `--fs-body` | `15px` |
| `--fs-small` | `13px` |
| `--fs-tiny` | `11px` |

Font stacks:
- `--font-display` / `--font-body`: `ui-sans-serif, -apple-system, "Segoe UI", system-ui, sans-serif`
- `--font-mono`: `ui-monospace, "SF Mono", Menlo, monospace` (used for activity dates)

---

## Palettes

### `warm-paper` (default)

Cream background, warm near-black ink, terra-cotta accent. Editorial feel. Good for competitive briefs, account overviews, and general business use.

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

Dark background, warm off-white ink, gold accent. High drama. Good for exec briefings and premium one-pagers.

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

Pure white, near-black ink, forest green accent. Maximum legibility. Good for board bios, compliance contexts, and print-first use.

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

Cool gray background, deep blue-gray ink, blue accent. Modern corporate. Good for technical landscapes, site inventories, and product team use.

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
| Competitive intelligence, account briefs, general business | `warm-paper` |
| Executive briefing, board bios, premium feel | `deep-ink` |
| Compliance, legal, print-heavy | `clean-white` |
| Technical, product, site inventories, modern corporate | `slate` |

**Default to `warm-paper`** unless the user specifies otherwise or the content clearly calls for a different mood.

---

## Status Dot Colors

Status dots appear in card headers and the one-pager hero block. Same values as the exec-report skill.

| Key | Color | Use for |
|---|---|---|
| `green` | `#059669` | Active, complete, strong |
| `amber` | `#d97706` | Watch, at risk, caution |
| `red` | `#dc2626` | Inactive, blocked, critical |
| `gray` | `#94a3b8` | Unknown, neutral, not evaluated |
| `blue` | `#0284c7` | In progress, informational |

CSS classes: `.status-dot--green`, `.status-dot--amber`, `.status-dot--red`, `.status-dot--gray`, `.status-dot--blue`. Same selectors as exec-report.

---

## Tag Pill Styling

Tags use a small pill shape with `--accent-soft` background and `--accent` text. This is palette-aware — the tag color shifts with the palette.

```css
.tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: var(--fs-tiny);
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
}
```

---

## Card Type Pill

The `.card-type-pill` labels the subject's category (e.g., "Competitor", "Prospect"). It uses a neutral muted-background approach — not the accent color — so it reads as metadata, not a status signal.

```css
.card-type-pill {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 20px;
  background: var(--grid);
  color: var(--ink-muted);
  font-size: var(--fs-tiny);
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
}
```

---

## Activity Timeline (One-Pager Mode)

The timeline visual — a vertical connecting line with accent-colored dots — is created entirely with CSS pseudo-elements. No JavaScript.

The connecting line is on `.activity-list::before`:
- `position: absolute; left: 9px; top: 8px; bottom: 8px`
- `width: 2px; background: var(--border)`

Each dot is on `.activity-item::before`:
- `position: absolute; left: -24px; top: 6px`
- `width: 10px; height: 10px; border-radius: 50%`
- `background: var(--accent); border: 2px solid var(--bg)`

The white border on the dot (`border: 2px solid var(--bg)`) creates a clean separation from the connecting line. When the palette changes, `--bg` updates and the border color updates automatically — no extra CSS needed.

---

## Typography Rules

- Card subject names (`.card-name`, `.op-name`): `font-weight: 600`, `letter-spacing: -0.02em`
- One-pager name (`.op-name`): `font-size: clamp(28px, 4vw, 48px)`, same editorial weight as exec-report hero
- Card headings (`h2`): `font-weight: 500`, `letter-spacing: -0.01em`, `font-size: var(--fs-h2)`
- Key fact labels (`<dt>`): 11px, uppercase, `letter-spacing: 0.08em`, `--ink-muted`
- Key fact values (`<dd>`): 14px, `--ink`, regular weight
- Summary text: `font-size: var(--fs-body)`, `line-height: 1.6`, `--ink` — reads like editorial prose
- Activity dates: `font-family: var(--font-mono)`, `font-size: var(--fs-tiny)`, `--ink-muted`
- Quick take text (`.op-quicktake-text`): `font-size: var(--fs-body)`, `color: var(--accent)`, `font-style: italic`

---

## Motion

All animations respect `prefers-reduced-motion`. The only animation in the dossier is a subtle fade-in on cards (`@keyframes fadeUp`). With motion disabled, cards appear immediately at full opacity.

---

## Responsive Breakpoints

- **Desktop (> 820px)**: Grid mode shows 2 cards per row. One-pager uses two-column layout.
- **Mobile (≤ 820px)**: Grid mode shows 1 card per row. One-pager stacks to single column. Page padding reduces to `20px`.
