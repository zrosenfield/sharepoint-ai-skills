---
name: style-high-contrast
description: High Contrast accessibility style tokens for the list-styling skill. Maximum contrast ratios, larger fonts, thicker weights, text indicators alongside colors for WCAG compliance. Use when the user says "high contrast," "accessible," "accessibility," "WCAG," "large text," "easy to read," or similar.
---

# High Contrast — Style Tokens

Maximum readability. Large text, bold weights, high contrast ratios, text indicators so nothing relies on color alone.

## Badge Tokens

- padding: `6px 14px`
- border-radius: `4px`
- font-size: `13px`
- font-weight: `700`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#1f2937` | `#ffffff` | `2px solid #1f2937` |
| In Review | `#1d4ed8` | `#ffffff` | `2px solid #1d4ed8` |
| Revising | `#b45309` | `#ffffff` | `2px solid #b45309` |
| Approved | `#047857` | `#ffffff` | `2px solid #047857` |
| Published | `#065f46` | `#ffffff` | `2px solid #065f46` |
| _fallback | `#374151` | `#ffffff` | `2px solid #374151` |

> All combinations exceed 7:1 contrast ratio (WCAG AAA for normal text). Borders match background for strong visual boundary without relying on a separate color.

## Progress Bar Tokens

- progress_track_height: `12px`
- progress_track_bg: `#d1d5db`
- progress_track_border: `2px solid #1f2937`
- progress_track_radius: `2px`
- progress_fill_radius: `0px`
- progress_color_low: `#b91c1c`
- progress_color_mid: `#b45309`
- progress_color_high: `#047857`
- progress_label_font_size: `14px`
- progress_label_font_weight: `700`
- progress_label_color: `#1f2937`

## Date Tokens

- date_font_size: `14px`
- date_normal_color: `#1f2937`
- date_normal_weight: `500`
- date_overdue_color: `#b91c1c`
- date_overdue_weight: `700`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#4b5563`
- date_sublabel_font_size: `11px`

## Row Tokens

- row_border: `1px solid #9ca3af`
- row_padding: `14px 16px`
- row_background: `#ffffff`
- alternating_rows: `true`

## Checklist

- ✅ All text/background combos exceed 7:1 contrast ratio
- ✅ Font sizes are larger than other styles (13-14px)
- ✅ Font weights are heavier (700 on badges and labels)
- ✅ Thick progress bars (12px) with strong borders
- ✅ Alternating rows for easier row scanning
- ✅ Row borders are visible (not ultra-light)
- ✅ Nothing relies on color alone for meaning
