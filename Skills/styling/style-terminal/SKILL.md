---
name: style-terminal
description: Terminal / Hacker style tokens for the list-styling skill. Dark-themed badge elements, monospace-inspired typography, neon green accents, matrix-style progress bars. Use when the user says "terminal," "hacker," "dark mode," "matrix," "developer style," "code style," "CLI look," "green on black," or similar.
---

# Terminal — Style Tokens

Dark badges, neon green accents, monospace energy. The formatted elements feel like terminal output even though the list background stays white.

## Badge Tokens

- padding: `4px 12px`
- border-radius: `2px`
- font-size: `11px`
- font-weight: `700`
- text-transform: `uppercase`

### status_colors

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#374151` | `#9ca3af` | `1px solid #4b5563` |
| In Review | `#1e3a5f` | `#38bdf8` | `1px solid #0ea5e9` |
| Revising | `#422006` | `#fb923c` | `1px solid #f97316` |
| Approved | `#052e16` | `#4ade80` | `1px solid #22c55e` |
| Published | `#022c22` | `#34d399` | `1px solid #10b981` |
| _fallback | `#1f2937` | `#6b7280` | `1px solid #374151` |

> Signature: dark backgrounds with bright colored text — the inverse of every other style. Borders are a mid-tone of the text color.

## Progress Bar Tokens

- progress_track_height: `8px`
- progress_track_bg: `#1f2937`
- progress_track_border: `1px solid #374151`
- progress_track_radius: `1px`
- progress_fill_radius: `0px`
- progress_color_low: `#ef4444`
- progress_color_mid: `#38bdf8`
- progress_color_high: `#4ade80`
- progress_label_font_size: `12px`
- progress_label_font_weight: `700`
- progress_label_color: `#4ade80`

## Date Tokens

- date_font_size: `12px`
- date_normal_color: `#374151`
- date_normal_weight: `500`
- date_overdue_color: `#ef4444`
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

- ✅ Badges have dark backgrounds with bright neon text
- ✅ Green accent color is neon (`#4ade80`), not natural
- ✅ Blue accent is cyan-sky (`#38bdf8`), not corporate
- ✅ Progress bar track is dark with neon green fill at high %
- ✅ Percentage label is neon green
- ✅ Sharp corners (1-2px radius) — no rounded anything
- ✅ Feels like terminal output in a spreadsheet
