---
name: style-bento
description: Bento style tokens for the list-styling skill. Warm earth-tone colors, compact uppercase badges, medium progress bars, calm organized aesthetic. Use when the user says "bento," "warm style," "earth tones," "muted colors," or similar.
---

# Bento — Style Tokens

Warm, organized, calm. Earth-tone palette, compact badges, tidy compartments.

## Badge Tokens

- padding: `4px 10px`
- border-radius: `4px`
- font-size: `11px`
- font-weight: `600`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#9ca3af` | `#ffffff` | `0px` |
| In Review | `#3b82f6` | `#ffffff` | `0px` |
| Revising | `#ea580c` | `#ffffff` | `0px` |
| Approved | `#16a34a` | `#ffffff` | `0px` |
| Published | `#15803d` | `#ffffff` | `0px` |
| _fallback | `#d1d5db` | `#ffffff` | `0px` |

> Colors lean warm: burnt orange instead of amber, olive green instead of bright green.

## Progress Bar Tokens

- progress_track_height: `8px`
- progress_track_bg: `#f3f4f6`
- progress_track_border: `0px`
- progress_track_radius: `4px`
- progress_fill_radius: `4px`
- progress_color_low: `#ef4444`
- progress_color_mid: `#ea580c`
- progress_color_high: `#22c55e`
- progress_label_font_size: `12px`
- progress_label_font_weight: `600`
- progress_label_color: `#374151`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#374151`
- date_normal_weight: `500`
- date_overdue_color: `#dc2626`
- date_overdue_weight: `700`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#6b7280`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #e5e7eb`
- row_padding: `10px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Warm earth-tone colors (burnt orange, olive green)
- ✅ Compact rectangles with slight rounding — not pills
- ✅ UPPERCASE text
- ✅ No borders on badges
- ✅ Medium progress bars (8px)
- ✅ Tidy and calm — no visual noise
