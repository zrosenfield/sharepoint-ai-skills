---
name: style-monochrome
description: Monochrome style tokens and row template for the list-styling skill. Single-hue slate design with a left-aligned large progress number as the hero element, all metadata stacked beside it. Layout uses the progress percentage as the dominant visual element. Use when the user says "monochrome," "single color," "corporate," "tonal," "minimal," or similar.
---

# Monochrome — Style Tokens + Row Template

Single-hue, restrained, corporate. Everything is slate blue. The progress percentage is the HERO — displayed enormous on the left, with metadata stacked to its right. Shade = stage.

**Layout philosophy: Hero number + stacked metadata.** The progress percentage is displayed huge (32px) on the left side of the card as the primary visual anchor. Status, name, and deadline stack vertically to its right. The big number makes each card instantly scannable.

## Badge Tokens

- padding: `5px 14px`
- border-radius: `6px`
- font-size: `11px`
- font-weight: `600`
- text-transform: `uppercase`

### status_colors (shade ramp — lightest = earliest)

| Value | bg | text | border |
|---|---|---|---|
| Draft | `#cbd5e1` | `#334155` | `0px` |
| In Review | `#64748b` | `#ffffff` | `0px` |
| Revising | `#475569` | `#ffffff` | `0px` |
| Approved | `#334155` | `#ffffff` | `0px` |
| Published | `#1e293b` | `#ffffff` | `0px` |
| _fallback | `#e2e8f0` | `#475569` | `0px` |

## Row Card Tokens

- card_border: `1px solid #e2e8f0`
- card_border_radius: `6px`
- card_background: `#ffffff`
- card_margin_bottom: `6px`
- card_shadow: `none`
- left_accent_width: `4px` (thin left border in status shade)
- hero_number_size: `32px`
- hero_number_weight: `800`

---

## Row Template Layout

Hero progress number on the left, metadata stacked right.

```
┃ ┌────────────────────────────────────────────────────┐
┃ │                                                    │
┃ │   72%     API Guide.docx                           │
┃ │           [In Review]  ·  5/15/2026                │
┃ │           ████████████████████░░░░░░               │
┃ │                                                    │
┃ └────────────────────────────────────────────────────┘
↑ 4px left accent in status shade color
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
      "align-items": "center",
      "border": "1px solid #e2e8f0",
      "border-left": "=if([$Status] == 'Draft', '4px solid #cbd5e1', if([$Status] == 'In Review', '4px solid #64748b', if([$Status] == 'Revising', '4px solid #475569', if([$Status] == 'Approved', '4px solid #334155', if([$Status] == 'Published', '4px solid #1e293b', '4px solid #e2e8f0')))))",
      "border-radius": "6px",
      "background-color": "#ffffff",
      "margin-bottom": "6px",
      "padding": "16px 20px",
      "gap": "20px",
      "min-height": "80px"
    },
    "children": [
      {
        "elmType": "div",
        "style": {
          "min-width": "72px",
          "display": "flex",
          "align-items": "center",
          "justify-content": "center"
        },
        "children": [
          {
            "elmType": "span",
            "txtContent": "=toString([$Progress]) + '%'",
            "style": {
              "font-size": "32px",
              "font-weight": "800",
              "color": "=if([$Status] == 'Draft', '#94a3b8', if([$Status] == 'In Review', '#64748b', if([$Status] == 'Revising', '#475569', if([$Status] == 'Approved', '#334155', if([$Status] == 'Published', '#1e293b', '#94a3b8')))))",
              "line-height": "1"
            }
          }
        ]
      },
      {
        "elmType": "div",
        "style": {
          "flex": "1",
          "display": "flex",
          "flex-direction": "column",
          "gap": "8px"
        },
        "children": [
          {
            "elmType": "div",
            "style": {
              "font-size": "14px",
              "font-weight": "600",
              "color": "#1e293b"
            },
            "txtContent": "=if([$FileLeafRef] == '', [$Title], [$FileLeafRef])"
          },
          {
            "elmType": "div",
            "style": {
              "display": "flex",
              "align-items": "center",
              "gap": "10px"
            },
            "children": [
              {
                "elmType": "span",
                "txtContent": "[$Status]",
                "style": {
                  "display": "inline-block",
                  "padding": "4px 12px",
                  "border-radius": "6px",
                  "font-size": "11px",
                  "font-weight": "600",
                  "text-transform": "uppercase",
                  "white-space": "nowrap",
                  "color": "=if([$Status] == 'Draft', '#334155', '#ffffff')",
                  "background-color": "=if([$Status] == 'Draft', '#cbd5e1', if([$Status] == 'In Review', '#64748b', if([$Status] == 'Revising', '#475569', if([$Status] == 'Approved', '#334155', if([$Status] == 'Published', '#1e293b', '#e2e8f0')))))"
                }
              },
              {
                "elmType": "span",
                "txtContent": "·",
                "style": { "color": "#cbd5e1", "font-size": "16px" }
              },
              {
                "elmType": "span",
                "txtContent": "=toLocaleDateString([$Deadline])",
                "style": {
                  "font-size": "12px",
                  "font-weight": "=if([$Deadline] < @now, '700', '400')",
                  "color": "=if([$Deadline] < @now, '#1e293b', '#64748b')"
                }
              },
              {
                "elmType": "span",
                "txtContent": "=if([$Deadline] < @now, '— overdue', '')",
                "style": {
                  "font-size": "11px",
                  "font-weight": "700",
                  "color": "#1e293b"
                }
              }
            ]
          },
          {
            "elmType": "div",
            "style": {
              "width": "100%",
              "height": "4px",
              "background-color": "#e2e8f0",
              "border-radius": "2px",
              "overflow": "hidden"
            },
            "children": [
              {
                "elmType": "div",
                "style": {
                  "width": "=toString([$Progress]) + '%'",
                  "height": "100%",
                  "border-radius": "2px",
                  "background-color": "=if([$Status] == 'Draft', '#94a3b8', if([$Status] == 'In Review', '#64748b', if([$Status] == 'Revising', '#475569', if([$Status] == 'Approved', '#334155', if([$Status] == 'Published', '#1e293b', '#94a3b8')))))"
                }
              }
            ]
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
- ✅ HERO PROGRESS NUMBER (32px, 800 weight) on the left — instantly scannable
- ✅ Hero number color matches the status shade (darker = further along)
- ✅ 4px left accent border in the status shade color
- ✅ All colors from ONE slate-blue hue family — zero red, green, or amber
- ✅ Progress bar fill color matches the status shade (not traffic lights)
- ✅ Overdue is shown through bold text + "— overdue" suffix, NOT red (stays monochrome)
- ✅ No emoji, no icons — pure typography
- ✅ No shadow — flat, corporate, restrained
- ✅ Metadata flows as: name → badge + date inline → progress bar
- ✅ Most restrained style — the opposite of Retro's loudness
