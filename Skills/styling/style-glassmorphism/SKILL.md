---
name: style-glassmorphism
description: Glassmorphism (Frosted Glass) style tokens for the list-styling skill. Soft pill badges, no borders, thin progress bars, airy spacing, modern SaaS aesthetic. Use when the user says "glassmorphism," "frosted glass," "glass look," "soft modern," or similar.
---

# Glassmorphism — Style Tokens

Light, breathable, elegant. Pill-shaped badges, no borders, thin bars, generous whitespace.

## Badge Tokens

- padding: `5px 16px`
- border-radius: `14px`
- font-size: `12px`
- font-weight: `600`
- text-transform: `none`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#6b7280` | `#ffffff` | `0px` |
| In Review | `#3b82f6` | `#ffffff` | `0px` |
| Revising | `#f97316` | `#ffffff` | `0px` |
| Approved | `#22c55e` | `#ffffff` | `0px` |
| Published | `#16a34a` | `#ffffff` | `0px` |
| _fallback | `#9ca3af` | `#ffffff` | `0px` |

## Progress Bar Tokens

- progress_track_height: `6px`
- progress_track_bg: `#e5e7eb`
- progress_track_border: `0px`
- progress_track_radius: `3px`
- progress_fill_radius: `3px`
- progress_color_low: `#ef4444`
- progress_color_mid: `#3b82f6`
- progress_color_high: `#22c55e`
- progress_label_font_size: `12px`
- progress_label_font_weight: `500`
- progress_label_color: `#6b7280`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#374151`
- date_normal_weight: `400`
- date_overdue_color: `#dc2626`
- date_overdue_weight: `600`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#9ca3af`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #f3f4f6`
- row_padding: `14px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Pill-shaped badges (14px radius), no borders
- ✅ Title Case text (no uppercase transform)
- ✅ Thin progress bars (6px) with rounded ends
- ✅ Generous whitespace
- ✅ Muted percentage label color
- ✅ Feels like a modern SaaS dashboard
