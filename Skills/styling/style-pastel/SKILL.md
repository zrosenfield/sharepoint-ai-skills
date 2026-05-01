---
name: style-pastel
description: Pastel style tokens for the list-styling skill. Soft candy colors with light tinted badge backgrounds and dark text — the inverse of solid-fill badges. Friendly, approachable, warm. Use when the user says "pastel," "soft colors," "candy," "light badges," "friendly style," "approachable," or similar.
---

# Pastel — Style Tokens

Soft, friendly, approachable. Light tinted backgrounds with dark colored text. The inverse of bold-fill badges.

## Badge Tokens

- padding: `5px 14px`
- border-radius: `10px`
- font-size: `12px`
- font-weight: `600`
- text-transform: `none`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#f1f5f9` | `#64748b` | `1px solid #e2e8f0` |
| In Review | `#dbeafe` | `#1d4ed8` | `1px solid #bfdbfe` |
| Revising | `#fff7ed` | `#c2410c` | `1px solid #fed7aa` |
| Approved | `#dcfce7` | `#15803d` | `1px solid #bbf7d0` |
| Published | `#d1fae5` | `#047857` | `1px solid #a7f3d0` |
| _fallback | `#f3f4f6` | `#6b7280` | `1px solid #e5e7eb` |

> Signature detail: background is the lightest tint of the hue, text is a dark shade of the same hue, border is a mid-tint. All three from the same color family per status.

## Progress Bar Tokens

- progress_track_height: `8px`
- progress_track_bg: `#f1f5f9`
- progress_track_border: `0px`
- progress_track_radius: `4px`
- progress_fill_radius: `4px`
- progress_color_low: `#fca5a5`
- progress_color_mid: `#93c5fd`
- progress_color_high: `#86efac`
- progress_label_font_size: `12px`
- progress_label_font_weight: `500`
- progress_label_color: `#64748b`

## Date Tokens

- date_font_size: `13px`
- date_normal_color: `#475569`
- date_normal_weight: `400`
- date_overdue_color: `#dc2626`
- date_overdue_weight: `600`
- date_sublabel: `DEADLINE`
- date_sublabel_color: `#94a3b8`
- date_sublabel_font_size: `10px`

## Row Tokens

- row_border: `1px solid #f1f5f9`
- row_padding: `12px 16px`
- row_background: `#ffffff`
- alternating_rows: `false`

## Checklist

- ✅ Badge backgrounds are light tints, NOT solid fills
- ✅ Badge text is a dark shade of the same hue as the background
- ✅ Badge borders are a mid-tint — subtle, not bold
- ✅ Progress bar fills are pastel (light red, light blue, light green)
- ✅ Everything feels soft and friendly
- ✅ Good for HR, onboarding, or people-facing sites
