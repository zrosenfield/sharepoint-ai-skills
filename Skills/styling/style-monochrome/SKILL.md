---
name: style-monochrome
description: Monochrome style tokens for the list-styling skill. Single-hue design using shades of slate blue — light to dark variants replace traffic-light colors. Sophisticated, corporate, design-system aesthetic. Use when the user says "monochrome," "single color," "one hue," "corporate design system," "all blue," "tonal," or similar.
---

# Monochrome — Style Tokens

Sophisticated single-hue design. Every element uses shades of slate blue. No traffic lights. Read the label.

## Badge Tokens

- padding: `5px 14px`
- border-radius: `6px`
- font-size: `11px`
- font-weight: `600`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#cbd5e1` | `#334155` | `0px` |
| In Review | `#64748b` | `#ffffff` | `0px` |
| Revising | `#475569` | `#ffffff` | `0px` |
| Approved | `#334155` | `#ffffff` | `0px` |
| Published | `#1e293b` | `#ffffff` | `0px` |
| _fallback | `#e2e8f0` | `#475569` | `0px` |

> Color logic: lightest = earliest stage, darkest = final stage. Progress through the workflow = progress through the shade ramp.

## Progress Bar Tokens

- progress_track_height: `6px`
- progress_track_bg: `#e2e8f0`
- progress_track_border: `0px`
- progress_track_radius: `3px`
- progress_fill_radius: `3px`
- progress_color_low: `#94a3b8`
- progress_color_mid: `#64748b`
- progress_color_high: `#1e293b`
- progress_label_font_size: `12px`
- progress_label_font_weight: `600`
- progress_label_color: `#475569`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#334155`
- date_normal_weight: `400`
- date_overdue_color: `#1e293b`
- date_overdue_weight: `700`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#94a3b8`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #e2e8f0`
- row_padding: `12px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ All colors from one slate-blue hue family
- ✅ No red/green/amber — shade = stage
- ✅ Lightest badge = earliest stage, darkest = final
- ✅ Progress bar darkens as it fills
- ✅ Overdue uses darkest shade + bold (not red)
- ✅ Feels like a corporate design system
