---
name: style-figma-clean
description: Figma Clean style tokens for the list-styling skill. Polished professional aesthetic, self-colored badge borders, thin precise progress bars, blue mid-range fills, design-tool precision. Use when the user says "figma," "clean style," "polished," "professional," "design tool look," or similar.
---

# Figma Clean — Style Tokens

Precise, polished, professional. Self-colored borders, thin bars, blue accents, design-tool feel.

## Badge Tokens

- padding: `4px 12px`
- border-radius: `4px`
- font-size: `12px`
- font-weight: `600`
- text-transform: `none`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#6b7280` | `#ffffff` | `1px solid #6b7280` |
| In Review | `#3b82f6` | `#ffffff` | `1px solid #3b82f6` |
| Revising | `#f97316` | `#ffffff` | `1px solid #f97316` |
| Approved | `#22c55e` | `#ffffff` | `1px solid #22c55e` |
| Published | `#16a34a` | `#ffffff` | `1px solid #16a34a` |
| _fallback | `#9ca3af` | `#ffffff` | `1px solid #9ca3af` |

> Signature detail: border color matches the background color (self-colored borders).

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
- progress_label_color: `#374151`

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
- row_padding: `12px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Self-colored subtle borders on badges (border matches bg)
- ✅ Title Case text (no uppercase)
- ✅ Thin precise progress bars (6px)
- ✅ Blue for mid-range progress (not amber)
- ✅ Clean, information-dense, never cluttered
- ✅ Feels like a design tool, not a poster
