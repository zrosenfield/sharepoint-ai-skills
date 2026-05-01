---
name: style-neobrutalism
description: Neobrutalism style tokens for the list-styling skill. Bold black borders, saturated colors, uppercase text, chunky progress bars, sharp edges. Use when the user says "neobrutalism," "brutalist," "bold borders," "chunky style," or similar.
---

# Neobrutalism — Style Tokens

Bold, graphic, raw. Thick black borders on everything. Saturated colors. Uppercase. No apologies.

## Badge Tokens

- padding: `4px 12px`
- border-radius: `3px`
- font-size: `11px`
- font-weight: `700`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#9ca3af` | `#000000` | `2px solid #000000` |
| In Review | `#2563eb` | `#ffffff` | `2px solid #000000` |
| Revising | `#f59e0b` | `#000000` | `2px solid #000000` |
| Approved | `#16a34a` | `#ffffff` | `2px solid #000000` |
| Published | `#16a34a` | `#ffffff` | `2px solid #000000` |
| _fallback | `#e5e7eb` | `#000000` | `2px solid #000000` |

> Color logic for unmapped values: green for "done" states, blue for "in progress," amber/orange for "needs work," gray for "not started," red for "blocked."

## Progress Bar Tokens

- progress_track_height: `10px`
- progress_track_bg: `#e5e7eb`
- progress_track_border: `2px solid #000000`
- progress_track_radius: `2px`
- progress_fill_radius: `0px`
- progress_color_low: `#ef4444`
- progress_color_mid: `#f59e0b`
- progress_color_high: `#22c55e`
- progress_label_font_size: `13px`
- progress_label_font_weight: `700`
- progress_label_color: `#1f2937`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#1f2937`
- date_normal_weight: `600`
- date_overdue_color: `#dc2626`
- date_overdue_weight: `700`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#6b7280`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #e5e7eb`
- row_padding: `12px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Every badge has a thick black border
- ✅ Rectangles with slight radius — not pills
- ✅ UPPERCASE text
- ✅ Saturated, not pastel
- ✅ Progress bars are chunky (10px) with black border
- ✅ No drop shadows
