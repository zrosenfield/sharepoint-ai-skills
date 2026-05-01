---
name: style-retro
description: Retro Memphis style tokens for the list-styling skill. Bright contrasting colors (hot pink, electric blue, yellow, teal), colored borders instead of black, playful and bold. Use when the user says "retro," "memphis," "80s style," "90s style," "colorful," "playful," "fun style," "bright colors," or similar.
---

# Retro Memphis — Style Tokens

Bright, playful, bold. Hot pink, electric blue, sunshine yellow. Colored borders. The fun one.

## Badge Tokens

- padding: `5px 14px`
- border-radius: `6px`
- font-size: `12px`
- font-weight: `700`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#fbbf24` | `#1f2937` | `2px solid #d97706` |
| In Review | `#3b82f6` | `#ffffff` | `2px solid #7c3aed` |
| Revising | `#f472b6` | `#ffffff` | `2px solid #db2777` |
| Approved | `#2dd4bf` | `#1f2937` | `2px solid #0d9488` |
| Published | `#a78bfa` | `#ffffff` | `2px solid #7c3aed` |
| _fallback | `#e5e7eb` | `#374151` | `2px solid #9ca3af` |

> Color logic: every status gets its own DISTINCT color — no two statuses share a hue. Borders are a darker shade of a contrasting or complementary color, not the same hue. Draft is yellow with amber border. In Review is blue with purple border. Revising is hot pink. Approved is teal. Published is lavender.

## Progress Bar Tokens

- progress_track_height: `10px`
- progress_track_bg: `#fef3c7`
- progress_track_border: `2px solid #d97706`
- progress_track_radius: `5px`
- progress_fill_radius: `3px`
- progress_color_low: `#f472b6`
- progress_color_mid: `#3b82f6`
- progress_color_high: `#2dd4bf`
- progress_label_font_size: `13px`
- progress_label_font_weight: `700`
- progress_label_color: `#7c3aed`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#374151`
- date_normal_weight: `500`
- date_overdue_color: `#db2777`
- date_overdue_weight: `700`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#7c3aed`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #e5e7eb`
- row_padding: `12px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Every status has a completely different hue — no repeats
- ✅ Borders are colored (not black) and use a contrasting/darker shade
- ✅ Hot pink, electric blue, teal, yellow, lavender all present
- ✅ Progress bar track is warm-tinted (light yellow) with colored border
- ✅ Progress fills are pink → blue → teal (not red → amber → green)
- ✅ Percentage label is purple
- ✅ Feels playful and bold — like an 80s design poster
