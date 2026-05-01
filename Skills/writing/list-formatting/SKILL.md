---
name: list-formatting
description: Create beautiful, functional SharePoint list and library formatters using JSON. Use this skill whenever the user asks to style, format, beautify, or customize the appearance of a SharePoint list, library, view, column, or form. Trigger phrases include "style my list", "format my list", "make my list pretty", "make my library beautiful", "style my library", "customize my view", "format my columns", "card layout", "tile view", "add icons to my list", "color code my list", "conditional formatting", "progress bars", or any mention of SharePoint JSON formatting. Also trigger when the user references specific formatting patterns like status indicators, data bars, people cards, Gantt charts, KPI dashboards, or hover cards in a SharePoint context. This skill produces English-language instructions only — no code generation. It teaches the agent what is possible and how to describe formatters so a downstream tool can apply them.
---

<!--
  SharePoint List Formatting Skill
  Created by Zach Rosenfield (github.com/zrosenfield)

  Built with knowledge from:
  - Microsoft Learn: SharePoint declarative customization docs
    https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/column-formatting
    https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/view-list-formatting
    https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/formatting-syntax-reference
  - PnP List Formatting Samples (MIT License)
    https://pnp.github.io/List-Formatting/
    https://github.com/pnp/List-Formatting

  Sharing is Caring!
-->

# SharePoint List Formatting Skill

## Step 1: Load Additional References (if needed)

Scan the user's request and read any reference files that apply before responding:

| If the request involves… | Read… |
|---|---|
| Colors, icons, status indicators, severity styling, theme classes, font styling, background colors, any visual decoration | `references/visual.md` |
| Buttons, Power Automate flows, hover cards, tile/gallery layouts, inline editing, group header/footer formatting, file previews | `references/advanced.md` |
| A named pattern (status pill, progress bar, card layout, Gantt, KPI dashboard, etc.), or the user asks for a template, example, or starting point | `references/patterns.md` |

For open-ended "make it pretty" requests, read all three. When in doubt, read the file.

---

## Step 2: Think Big Before You Build

When the user asks to "make it pretty", "style my view", or gives any open-ended visual request — **do not default to incremental tweaks**. Treat it as an invitation to fundamentally reimagine the experience.

Before touching JSON, ask yourself: *What is the most dramatically better version of this list?*

**Default to transformation, not decoration:**
- Prefer a `rowFormatter` card layout over adding row highlight colors
- Prefer a tile/gallery view over a plain list with styled columns
- Prefer rich column formatters (status pills, avatar+name, progress bars, due date urgency) over plain text with background colors
- Propose a **complete visual system** — not isolated column tweaks

**Name your vision first.** Before producing JSON, describe what you're building in one sentence. This lets the user redirect before you build the wrong thing.

**Propose the boldest option, then offer alternatives.** Lead with the most dramatic transformation. Mention a simpler fallback if they want something lighter.

---

## Formatting Scopes

Four distinct scopes — pick the right one, or combine them:

- **Column formatting** — Styles a single column's cells. Applied via: Column Settings > Format this column > Advanced mode. `@currentField` is the column's value.
- **View formatting (row-level)** — Styles entire rows or transforms the view layout. Applied via: View dropdown > Format current view > Advanced mode. Two approaches: `additionalRowClass` (conditional CSS class per row) or `rowFormatter` (full custom row layout).
- **Group header/footer formatting** — Uses `groupProps` with `headerFormatter`/`footerFormatter`. Access group data with `@group` token.
- **Form formatting** — Customizes new/edit/display form layout, headers, footers, and conditional show/hide.

## JSON Schemas

Always include the correct `$schema`:

| Formatter type | Schema |
|---|---|
| Column formatting | `https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json` |
| View with `rowFormatter` | `https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json` |
| View with `additionalRowClass` only | `https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json` |
| Tile/gallery view | `https://developer.microsoft.com/json-schemas/sp/v2/tile-formatting.schema.json` |

## Element Types (elmType)

| elmType | Description |
|---------|-------------|
| `div` | Block container. Most common wrapper. |
| `span` | Inline container. Good for text alongside other elements. |
| `a` | Hyperlink. Requires `href` attribute. |
| `img` | Image. Requires `src`. Subject to domain restrictions. |
| `svg` / `path` | Vector graphics. `path` requires `d` attribute. |
| `button` | Clickable button. Requires `customRowAction`. |
| `filepreview` | Document library thumbnail. Set `src` to `@thumbnail.medium`. |

## Key Properties

- **`txtContent`** — Text content of the element (string or expression). If set, `children` are ignored.
- **`style`** — CSS property/value pairs. Supports layout (`display`, `flex-*`, `position`), sizing, spacing, background, border, text, and `transform: translate()`. Use flexbox; `float` is deprecated.
- **`attributes`** — HTML attributes: `href`, `src`, `class`, `target`, `title`, `role`, `iconName` (Fluent UI icon), `d` (SVG path), `data-interception`.
- **`children`** — Array of child element objects. Ignored if `txtContent` is set.
- **`forEach`** — `"iteratorName in @currentField"` — duplicates element for each value in a multi-value field. Cannot be on the root element.
- **`debugMode`** — Set `true` to log errors to browser console.

## Expressions

Prefer Excel-style (`=` prefix). Examples:
```
=if(@currentField == 'Done', 'sp-field-severity--good', '')
=if([$DueDate] <= @now, '#a4262c', 'inherit')
='mailto:' + @currentField.email
=toString(floor(@currentField * 100)) + '%'
```

**Operators**: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, ternary `?`

**String**: `toString()`, `toLowerCase`, `toUpperCase`, `indexOf`, `startsWith`, `endsWith`, `substring`, `replace`, `replaceAll`, `padStart`, `padEnd`, `split`, `join`, `length` (array count only — not string length)

**Number**: `Number()`, `abs`, `floor`, `ceiling`, `pow`, `cos`, `sin`, `toLocaleString()`

**Date**: `Date()`, `getDate`, `getMonth` (0-based), `getYear`, `addDays`, `addMinutes`, `toLocaleDateString()`, `toLocaleString()`

**Array**: `appendTo`, `removeFrom`, `indexOf`, `join`, `length`

**Images**: `getUserImage(email, size)` — sizes: `'small'`/`'s'`, `'medium'`/`'m'`, `'large'`/`'l'`

## Special Tokens

| Token | Description |
|-------|-------------|
| `@currentField` | Column value. In `rowFormatter`, always resolves to Title — use `[$FieldName]` instead. |
| `@currentField.title` / `.email` / `.id` / `.picture` / `.department` / `.jobTitle` | Person field sub-properties |
| `@currentField.lookupValue` / `.lookupId` | Lookup field sub-properties |
| `@currentField.desc` | Hyperlink description |
| `@me` | Current user's email |
| `@now` | Current date/time (epoch ms) |
| `@rowIndex` | Zero-based row index |
| `[$FieldInternalName]` | Another column's value. Spaces → `_x0020_`. |
| `[$FieldName.title]` / `.email` / `.lookupValue` | Sub-properties from another column |
| `@thumbnail.small` / `.medium` / `.large` | Document library thumbnail URLs |
| `@currentWeb` | Current site URL |
| `@group.fieldData.displayValue` / `@group.count` | Group header/footer tokens |

## Column Types

| Type | Access | Notes |
|------|--------|-------|
| Text / Choice | `@currentField` | Direct string |
| Number / Currency | `@currentField` | Use in math; `toLocaleString()` for display |
| Date/Time | `@currentField` | Compare with `@now`; 1 day = 86400000ms |
| Yes/No | `@currentField` | Returns `1` or `0`, not true/false |
| Person | `@currentField.title`, `.email`, `.picture` | Object |
| Multi-Person / Multi-Choice / Multi-Lookup | `forEach` | Use forEach to iterate |
| Lookup | `@currentField.lookupValue`, `.lookupId` | Object |
| Hyperlink | `@currentField` (URL), `@currentField.desc` | |
| Location | `@currentField.DisplayName`, `.City`, `.Latitude`, `.Longitude` | |

**Document library fields**: `[$FileLeafRef]` (filename), `[$FileRef]` (full path), `[$File_x0020_Type]` (extension), `[$Editor]` (modified by), `[$FileSizeDisplay]`, `@thumbnail.medium`.

## Common Pitfalls

1. **Internal vs display names**: Use internal names in `[$...]`. Spaces → `_x0020_`. Find via List Settings > column URL parameter `Field=`.
2. **`@currentField` in rowFormatter**: Always resolves to Title. Use `[$FieldName]` for other columns.
3. **Person fields are objects**: Use `.title` or `.email`, not the field reference directly.
4. **Yes/No is 0/1**: Not true/false. `=if(@currentField == 1, 'Yes', 'No')`.
5. **Date math in ms**: `@now + 259200000` = 3 days from now.
6. **`length` is not string length**: It counts array items (multi-value fields only).
7. **External images blocked**: Use Fluent UI icons, SVG, or theme classes instead.
8. **`additionalRowClass` + `rowFormatter` are mutually exclusive**: rowFormatter wins.
9. **Wrong schema silently fails**: Match schema to formatter type exactly.

---

## Your Role

1. **Understand the context**: Ask what columns exist, their types, and what visual outcome they want.
2. **Recommend the right scope(s)**: Column, view, group, or form formatting — or a combination.
3. **Generate valid JSON**: Always include the correct `$schema`. Use Excel-style expressions.
4. **Explain what it does**: Briefly describe the formatter and any columns it requires.

## Interaction Pattern

1. Ask what kind of list it is and what columns it has.
2. Name your vision and propose 2–3 approaches ranked bold-to-simple (e.g., "Best: full card layout with status pills and avatars. Lighter: conditional row colors + styled status column.").
3. Generate the formatter(s) once the user confirms.
4. Provide the JSON and instructions for where to apply it.

## Common Scenarios

**Task/project lists**: Lead with a rowFormatter card layout — status pills, due date urgency, progress bars, person avatars.

**Document libraries**: Lead with a tile/gallery view using `filepreview` thumbnails, file type icons, and modified-by fields.

**Contact/people lists**: Card layouts with `getUserImage` profile pictures, email/phone action buttons.

**Status/tracking lists**: Traffic light indicators, data bars, KPI aggregate footers.

**Link/resource lists**: Tile layouts with icons and category sections.

**Event/calendar lists**: Cards with date badges, countdown formatting, registration status.
