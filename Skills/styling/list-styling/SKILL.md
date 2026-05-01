---
name: list-styling
description: Apply a visual style theme to any SharePoint list or document library using column formatting, view formatting, and row formatting. Use this skill whenever the user asks to "style a list," "theme a library," "apply a look," "make this list look like X," "format this list," or mentions any specific style name like Neobrutalism, Glassmorphism, Bento, or Figma Clean. Also trigger when the user says "apply the brutalist style," "give it a frosted glass look," "make it bento-style," or any request to change the visual appearance of a SharePoint list or library. This skill works with any style definition skill — it reads the style token file and generates SharePoint JSON formatting.
---

# List Styling Engine

Apply visual style themes to SharePoint lists and document libraries. This skill contains ALL the logic, formatting syntax, and template patterns. It pairs with a lightweight style token file (e.g., `style-neobrutalism/SKILL.md`) that defines only the colors, shapes, and typography for that specific style.

## Workflow

### Step 1: Identify the Style

If the user names a style, read the matching style token file from the skills library:
- `style-neobrutalism/SKILL.md`
- `style-glassmorphism/SKILL.md`
- `style-bento/SKILL.md`
- `style-figma-clean/SKILL.md`

If unclear, ask: "Which style would you like to apply?"

### Step 2: Read the List Schema

You need to know:
- Column names and their internal names
- Column types (Choice, Number, DateTime, Text)
- Choice values for any Choice columns (e.g., Draft, In Review, Approved)

Get this from SHAREPOINT.md if available, or ask the user.

### Step 3: Generate Formatters

Read the style token file. Use the tokens to fill in the template patterns below. Generate one formatter per styled column.

### Step 4: Apply

For each formatter, tell the user:

**Column formatting:**
"Go to the **[Column Name]** column header → Column settings → Format this column → Advanced mode → paste this JSON."

**View formatting:**
"Go to the view dropdown → Format current view → Advanced mode → paste this JSON."

Provide the complete, ready-to-paste JSON. No code blocks with commentary — just the JSON.

### Step 5: Verify

Ask the user to refresh and confirm.

---

## Template Patterns

Use these templates. Replace every `{token}` with the value from the style token file.

### Status Badge (Choice Column)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "display": "flex",
    "align-items": "center"
  },
  "children": [
    {
      "elmType": "span",
      "txtContent": "@currentField",
      "style": {
        "display": "inline-block",
        "padding": "{badge_padding}",
        "border-radius": "{badge_border_radius}",
        "font-size": "{badge_font_size}",
        "font-weight": "{badge_font_weight}",
        "text-transform": "{badge_text_transform}",
        "white-space": "nowrap",
        "border": "{CONDITIONAL: build from status_colors map — each status gets its border value}",
        "color": "{CONDITIONAL: build from status_colors map — each status gets its text color}",
        "background-color": "{CONDITIONAL: build from status_colors map — each status gets its bg color}"
      }
    }
  ]
}
```

**Building conditionals from the status_colors map:**

The style token file has a `status_colors` map like:
```
Draft:       bg=#9ca3af, text=#000000, border=2px solid #000000
In Review:   bg=#2563eb, text=#ffffff, border=2px solid #000000
```

Turn this into nested `if` expressions:
```
"=if(@currentField == 'Draft', '#9ca3af', if(@currentField == 'In Review', '#2563eb', ...))"
```

Always include a fallback color at the end for unmapped values.

### Progress Bar (Number Column, 0-100)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "display": "flex",
    "align-items": "center",
    "gap": "8px"
  },
  "children": [
    {
      "elmType": "div",
      "style": {
        "width": "100px",
        "height": "{progress_track_height}",
        "background-color": "{progress_track_bg}",
        "border": "{progress_track_border}",
        "border-radius": "{progress_track_radius}",
        "overflow": "hidden"
      },
      "children": [
        {
          "elmType": "div",
          "style": {
            "width": "=toString(@currentField) + '%'",
            "height": "100%",
            "border-radius": "{progress_fill_radius}",
            "background-color": "=if(@currentField < 30, '{progress_color_low}', if(@currentField < 66, '{progress_color_mid}', '{progress_color_high}'))"
          }
        }
      ]
    },
    {
      "elmType": "span",
      "txtContent": "=toString(@currentField) + '%'",
      "style": {
        "font-size": "{progress_label_font_size}",
        "font-weight": "{progress_label_font_weight}",
        "color": "{progress_label_color}"
      }
    }
  ]
}
```

### Date with Overdue (DateTime Column)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "display": "flex",
    "flex-direction": "column",
    "gap": "2px"
  },
  "children": [
    {
      "elmType": "div",
      "style": {
        "display": "flex",
        "align-items": "center",
        "gap": "6px"
      },
      "children": [
        {
          "elmType": "span",
          "txtContent": "=toLocaleDateString(@currentField)",
          "style": {
            "color": "=if(@currentField < @now, '{date_overdue_color}', '{date_normal_color}')",
            "font-weight": "=if(@currentField < @now, '{date_overdue_weight}', '{date_normal_weight}')",
            "font-size": "{date_font_size}"
          }
        }
      ]
    },
    {
      "elmType": "span",
      "txtContent": "=if(@currentField < @now, 'OVERDUE', '{date_sublabel}')",
      "style": {
        "color": "=if(@currentField < @now, '{date_overdue_color}', '{date_sublabel_color}')",
        "font-size": "{date_sublabel_font_size}",
        "font-weight": "=if(@currentField < @now, '700', '400')",
        "text-transform": "uppercase"
      }
    }
  ]
}
```

### View Formatting (Row Styling)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/view-formatting.schema.json",
  "additionalRowClass": "{row_class_expression}"
}
```

If the style uses alternating rows:
```json
"additionalRowClass": "=if(@rowIndex % 2 == 0, 'ms-bgColor-neutralLighter', '')"
```

If the style does not use alternating rows, skip view formatting entirely.

---

## SharePoint Formatting Rules

These are hard constraints. Never violate them.

### Supported
- `elmType`: `div`, `span`, `a`, `img`, `svg`, `path`, `button`
- Inline styles only (no custom CSS classes — only built-in SP classes via `additionalRowClass`)
- `border-radius` — works fine
- `text-transform` — `uppercase`, `lowercase`, `capitalize`
- `box-shadow` — works but can be inconsistent
- Colors: hex (`#ffffff`) or named (`red`)
- Expressions: `@currentField`, `[$ColumnInternalName]`, `@now`, `@me`, `@rowIndex`
- Operators: `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`
- Functions: `if()`, `toString()`, `Number()`, `toLocaleDateString()`, `indexOf()`, `substring()`

### NOT Supported — Never Use These
- `backdrop-filter` (no blur effects)
- `background` with gradients (use `background-color` with solid hex only)
- `rgb()`, `rgba()`, `hsl()` color values (hex only)
- Custom CSS classes in column formatters
- CSS variables (`var(--x)`)
- `hover` pseudo-states in column formatters
- Nested `if` beyond ~10 levels (will break)

### Common Mistakes
- Forgetting `$schema` — always include it
- Using display names instead of internal column names — internal names use `_x0020_` for spaces
- Case-sensitivity on Choice values — `"Draft"` ≠ `"draft"` ≠ `"DRAFT"`
- Using `Number` column for progress when the column stores 0.72 not 72 — check and multiply by 100 if needed

---

## Column Type → Formatter Mapping

| Column Type | Formatter Pattern | Required? |
|---|---|---|
| Choice (Status) | Status Badge | Yes — highest visual impact |
| Number (Progress) | Progress Bar | Yes — second highest impact |
| DateTime (Deadline) | Date with Overdue | Yes |
| Single Line of Text (Title/Name) | Usually skip — default is fine | No |
| Person | Skip — default rendering is fine | No |
| Multi-line Text | Skip unless style has card-cell pattern | No |

---

## Rules

1. **Always read the style token file first.** Never invent tokens.
2. **Every color, radius, border, and font value comes from the style tokens.** Do not freestyle.
3. **Handle missing columns gracefully.** If the list lacks a column type, skip it.
4. **Ask for Choice values if not known.** Status colors are mapped to specific values — you need the exact strings.
5. **Keep formatters independent.** Each column formatter works standalone.
6. **Provide ready-to-paste JSON.** No explanations mixed into the JSON itself.
7. **Include $schema in every formatter.**
