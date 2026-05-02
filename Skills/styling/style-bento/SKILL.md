---
name: style-bento
description: Bento style tokens and row template for the list-styling skill. Card layout inspired by bento boxes — distinct compartments separated by thin borders, each section labeled, warm earth tones. Layout is a horizontal row of compartments (name | status | progress | deadline) with visible dividers between each. Use when the user says "bento," "compartment," "warm style," "earth tones," "organized," or similar.
---

# Bento — Style Tokens + Row Template

Warm, organized, compartmentalized. Each row is a card divided into labeled compartments like a bento box — visible dividers, each section has a header label above its content.

**Layout philosophy: Horizontal compartments with dividers.** Not a sidebar split, not a single stack. Four distinct compartments in a row: Name | Status | Progress | Deadline. Each compartment has a tiny uppercase label above the content. The dividers between compartments ARE the design.

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

## Progress Bar Tokens

- progress_track_height: `8px`
- progress_track_bg: `#f3f4f6`
- progress_track_border: `0px`
- progress_track_radius: `4px`
- progress_fill_radius: `4px`
- progress_color_low: `#ef4444`
- progress_color_mid: `#ea580c`
- progress_color_high: `#22c55e`
- progress_label_font_size: `20px`
- progress_label_font_weight: `700`
- progress_label_color: `#1f2937`

## Row Card Tokens

- card_border: `1px solid #e5e7eb`
- card_border_radius: `8px`
- card_background: `#ffffff`
- card_margin_bottom: `8px`
- card_shadow: `0px 1px 3px #0000000d`
- compartment_border: `1px solid #e5e7eb` (dividers between sections)
- compartment_label_color: `#9ca3af`
- compartment_label_size: `9px`
- compartment_label_weight: `600`
- compartment_label_transform: `uppercase`
- compartment_label_spacing: `0.5px`
- overdue_accent: `2px solid #dc2626` (left border accent on overdue cards)

---

## Row Template Layout

Horizontal compartment grid. Each section is a labeled box.

```
┌──────────────────┬───────────┬──────────────────┬──────────────┐
│ DOCUMENT         │ STATUS    │ PROGRESS         │ DEADLINE     │
│                  │           │                  │              │
│ API Guide.docx   │ [In Rev]  │        72%       │ 📅 5/15/2026 │
│                  │           │ ████████████░░░  │ DEADLINE     │
│                  │ On Track  │                  │              │
└──────────────────┴───────────┴──────────────────┴──────────────┘
  ↑ overdue cards get a 2px red left border accent
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
      "border": "1px solid #e5e7eb",
      "border-left": "=if([$Deadline] < @now, '3px solid #dc2626', '1px solid #e5e7eb')",
      "border-radius": "8px",
      "background-color": "#ffffff",
      "margin-bottom": "8px",
      "box-shadow": "0px 1px 3px #0000000d",
      "overflow": "hidden",
      "min-height": "90px"
    },
    "children": [
      {
        "elmType": "div",
        "style": {
          "flex": "2",
          "padding": "14px 16px",
          "display": "flex",
          "flex-direction": "column",
          "gap": "6px",
          "border-right": "1px solid #e5e7eb"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": "DOCUMENT",
            "style": {
              "font-size": "9px",
              "font-weight": "600",
              "color": "#9ca3af",
              "text-transform": "uppercase",
              "letter-spacing": "0.5px"
            }
          },
          {
            "elmType": "div",
            "style": {
              "font-size": "14px",
              "font-weight": "700",
              "color": "#1f2937",
              "line-height": "1.3"
            },
            "txtContent": "=if([$FileLeafRef] == '', [$Title], [$FileLeafRef])"
          }
        ]
      },
      {
        "elmType": "div",
        "style": {
          "flex": "1",
          "padding": "14px 16px",
          "display": "flex",
          "flex-direction": "column",
          "gap": "8px",
          "align-items": "center",
          "justify-content": "center",
          "border-right": "1px solid #e5e7eb"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": "STATUS",
            "style": {
              "font-size": "9px",
              "font-weight": "600",
              "color": "#9ca3af",
              "text-transform": "uppercase",
              "letter-spacing": "0.5px"
            }
          },
          {
            "elmType": "span",
            "txtContent": "[$Status]",
            "style": {
              "display": "inline-block",
              "padding": "4px 10px",
              "border-radius": "4px",
              "font-size": "11px",
              "font-weight": "600",
              "text-transform": "uppercase",
              "white-space": "nowrap",
              "color": "#ffffff",
              "background-color": "=if([$Status] == 'Draft', '#9ca3af', if([$Status] == 'In Review', '#3b82f6', if([$Status] == 'Revising', '#ea580c', if([$Status] == 'Approved', '#16a34a', if([$Status] == 'Published', '#15803d', '#d1d5db')))))"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=if([$Deadline] < @now, '⚠ At Risk', '✓ On Track')",
            "style": {
              "font-size": "10px",
              "font-weight": "500",
              "color": "=if([$Deadline] < @now, '#dc2626', '#16a34a')"
            }
          }
        ]
      },
      {
        "elmType": "div",
        "style": {
          "flex": "1.5",
          "padding": "14px 16px",
          "display": "flex",
          "flex-direction": "column",
          "gap": "6px",
          "align-items": "center",
          "justify-content": "center",
          "border-right": "1px solid #e5e7eb"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": "PROGRESS",
            "style": {
              "font-size": "9px",
              "font-weight": "600",
              "color": "#9ca3af",
              "text-transform": "uppercase",
              "letter-spacing": "0.5px"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=toString([$Progress]) + '%'",
            "style": {
              "font-size": "20px",
              "font-weight": "700",
              "color": "=if([$Progress] < 30, '#ef4444', if([$Progress] < 66, '#ea580c', '#16a34a'))"
            }
          },
          {
            "elmType": "div",
            "style": {
              "width": "100%",
              "height": "8px",
              "background-color": "#f3f4f6",
              "border-radius": "4px",
              "overflow": "hidden"
            },
            "children": [
              {
                "elmType": "div",
                "style": {
                  "width": "=toString([$Progress]) + '%'",
                  "height": "100%",
                  "border-radius": "4px",
                  "background-color": "=if([$Progress] < 30, '#ef4444', if([$Progress] < 66, '#ea580c', '#22c55e'))"
                }
              }
            ]
          }
        ]
      },
      {
        "elmType": "div",
        "style": {
          "flex": "1",
          "padding": "14px 16px",
          "display": "flex",
          "flex-direction": "column",
          "gap": "4px",
          "align-items": "center",
          "justify-content": "center"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": "DEADLINE",
            "style": {
              "font-size": "9px",
              "font-weight": "600",
              "color": "#9ca3af",
              "text-transform": "uppercase",
              "letter-spacing": "0.5px"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=toLocaleDateString([$Deadline])",
            "style": {
              "font-size": "13px",
              "font-weight": "=if([$Deadline] < @now, '700', '500')",
              "color": "=if([$Deadline] < @now, '#dc2626', '#374151')"
            }
          },
          {
            "elmType": "span",
            "txtContent": "=if([$Deadline] < @now, '⚠ OVERDUE', '')",
            "style": {
              "font-size": "10px",
              "font-weight": "700",
              "color": "#dc2626"
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
- ✅ Horizontal compartment layout with VISIBLE DIVIDERS between sections
- ✅ Each compartment has a tiny uppercase label (DOCUMENT, STATUS, PROGRESS, DEADLINE)
- ✅ Labels are 9px, gray, uppercase with letter-spacing — subtle but structured
- ✅ Progress percentage is LARGE (20px) and centered in its compartment
- ✅ Warm earth-tone badge colors (burnt orange, olive green)
- ✅ Overdue cards get a red left-border accent — not the whole border
- ✅ No sidebar — this is a horizontal grid, like bento box compartments
- ✅ Subtle shadow (not hard offset) — organized, not aggressive
- ✅ On Track / At Risk indicator under the status badge
- ✅ Completely different layout from Neobrutalism (compartments vs sidebar) and Glassmorphism (horizontal vs stacked)
