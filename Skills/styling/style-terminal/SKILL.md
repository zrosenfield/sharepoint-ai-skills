---
name: style-terminal
description: Terminal / Hacker style tokens and row template for the list-styling skill. Dark cards with neon text, green/cyan accents, sharp corners, terminal prompt icon, status displayed like CLI output. Use when the user says "terminal," "hacker," "dark mode," "matrix," "developer," "CLI," or similar.
---

# Terminal — Style Tokens + Row Template

Dark backgrounds, neon text, sharp corners. Each row is a dark card that looks like terminal output. Status values render like CLI flags. The progress bar glows neon green.

**Layout philosophy: Dark card with terminal aesthetic.** The entire card has a dark background (#0f172a). All text is bright colored on dark. Status renders like a CLI flag in brackets. The prompt character `>` appears before the document name. Everything feels like you're reading `ls -la` output.

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

## Row Card Tokens

- card_background: `#0f172a` (near-black navy)
- card_border: `1px solid #1e293b`
- card_border_radius: `4px` (slightly rounded — terminals have some softness)
- card_margin_bottom: `4px` (tight spacing — dense like terminal output)
- card_shadow: `none`
- card_padding: `14px 18px`
- prompt_char: `>`
- prompt_color: `#4ade80`
- filename_color: `#e2e8f0`
- separator_color: `#334155`
- overdue_border: `1px solid #ef4444`
- overdue_glow: `0px 0px 8px #ef444433` (subtle red glow for overdue)

---

## Row Template Layout

Dark card with terminal-style content. Single row of data like CLI output.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  > API Guide.docx     [IN REVIEW]   ████░░ 72%  5/15   │
│                                                          │
└──────────────────────────────────────────────────────────┘
  ↑ dark bg (#0f172a), neon text, overdue cards get red glow
```

## rowFormatter JSON

**Adapt before applying.** The column names below (`[$Status]`, `[$Progress]`, `[$Deadline]`) are example placeholders — replace them with the actual internal column names from the user's list. Also update every status value string ('Draft', 'In Review', 'Revising', etc.) to match the user's actual Choice values. Follow list-styling Step 3.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/view-formatting.schema.json",
  "hideSelection": false,
  "hideColumnHeaders": true,
  "rowFormatter": {
    "elmType": "div",
    "style": {
      "display": "flex",
      "flex-direction": "column",
      "gap": "8px",
      "padding": "14px 18px",
      "background-color": "#0f172a",
      "border": "=if([$Deadline] < @now, '1px solid #ef4444', '1px solid #1e293b')",
      "border-radius": "4px",
      "margin-bottom": "4px",
      "box-shadow": "=if([$Deadline] < @now, '0px 0px 8px #ef444433', 'none')",
      "min-height": "60px"
    },
    "children": [
      {
        "elmType": "div",
        "style": {
          "display": "flex",
          "align-items": "center",
          "gap": "14px",
          "flex-wrap": "wrap"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": ">",
            "style": {
              "font-size": "14px",
              "font-weight": "700",
              "color": "#4ade80"
            }
          },
          {
            "elmType": "div",
            "style": {
              "flex": "2",
              "font-size": "14px",
              "font-weight": "600",
              "color": "#e2e8f0"
            },
            "txtContent": "=if([$FileLeafRef] == '', [$Title], [$FileLeafRef])"
          },
          {
            "elmType": "span",
            "txtContent": "[$Status]",
            "style": {
              "display": "inline-block",
              "padding": "4px 12px",
              "border-radius": "2px",
              "font-size": "11px",
              "font-weight": "700",
              "text-transform": "uppercase",
              "white-space": "nowrap",
              "color": "=if([$Status] == 'Draft', '#9ca3af', if([$Status] == 'In Review', '#38bdf8', if([$Status] == 'Revising', '#fb923c', if([$Status] == 'Approved', '#4ade80', if([$Status] == 'Published', '#34d399', '#6b7280')))))",
              "background-color": "=if([$Status] == 'Draft', '#374151', if([$Status] == 'In Review', '#1e3a5f', if([$Status] == 'Revising', '#422006', if([$Status] == 'Approved', '#052e16', if([$Status] == 'Published', '#022c22', '#1f2937')))))",
              "border": "=if([$Status] == 'Draft', '1px solid #4b5563', if([$Status] == 'In Review', '1px solid #0ea5e9', if([$Status] == 'Revising', '1px solid #f97316', if([$Status] == 'Approved', '1px solid #22c55e', if([$Status] == 'Published', '1px solid #10b981', '1px solid #374151')))))"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=toString([$Progress]) + '%'",
            "style": {
              "font-size": "14px",
              "font-weight": "700",
              "color": "#4ade80",
              "min-width": "40px",
              "text-align": "right"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=toLocaleDateString([$Deadline])",
            "style": {
              "font-size": "12px",
              "font-weight": "=if([$Deadline] < @now, '700', '400')",
              "color": "=if([$Deadline] < @now, '#ef4444', '#64748b')"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=if([$Deadline] < @now, '[OVERDUE]', '')",
            "style": {
              "font-size": "11px",
              "font-weight": "700",
              "color": "#ef4444"
            }
          }
        ]
      },
      {
        "elmType": "div",
        "style": {
          "width": "100%",
          "height": "4px",
          "background-color": "#1e293b",
          "border-radius": "0px",
          "overflow": "hidden"
        },
        "children": [
          {
            "elmType": "div",
            "style": {
              "width": "=toString([$Progress]) + '%'",
              "height": "100%",
              "background-color": "=if([$Progress] < 30, '#ef4444', if([$Progress] < 66, '#38bdf8', '#4ade80'))"
            }
          }
        ]
      }
    ]
  }
}
```

---

## Checklist — "I Can't Believe That's SharePoint"

- ✅ Full rowFormatter — NOT default column grid
- ✅ DARK BACKGROUND (#0f172a) on every card — this IS the style
- ✅ Neon green `>` prompt character before every document name
- ✅ Light text on dark (#e2e8f0) for filenames
- ✅ Status badges have dark bg + neon colored text (inverted from normal)
- ✅ Progress percentage is neon green (#4ade80)
- ✅ Progress bar track is dark (#1e293b), fills glow neon (red → cyan → green)
- ✅ Zero border-radius on progress bar — hard edges
- ✅ Overdue shows `[OVERDUE]` in brackets like a CLI flag
- ✅ Overdue cards get a subtle red glow (box-shadow)
- ✅ Tight 4px spacing between cards — dense like terminal output
- ✅ No emoji anywhere — terminals don't have emoji
- ✅ Only style with dark cards — immediately distinguishable from everything else
