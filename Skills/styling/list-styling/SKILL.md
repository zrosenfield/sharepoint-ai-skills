---
name: list-styling
description: Apply a visual style theme to any SharePoint list or document library using column formatting, view formatting, row templates, and tile layouts. Use this skill whenever the user asks to style, theme, or visually transform a list or library. The goal is "I can't believe that's SharePoint" impact — not just color swaps, but fully art-directed views. This skill works with any style token file.
---

# List Styling Engine

Transform SharePoint lists and document libraries into fully art-directed views. This is not a color palette swap — it's a complete visual redesign using every formatting capability SharePoint provides.

**The bar: "I can't believe that's SharePoint."**

## Formatting Capabilities — Use ALL of These

SharePoint provides four levels of formatting. A properly styled view uses MULTIPLE levels together. Do not stop at column formatting.

### Level 1: Column Formatting
Per-column rendering. Controls how individual cell values display.
- Status badges, progress bars, date compositions
- Applied via: Column header → Column settings → Format this column → Advanced mode

### Level 2: View Formatting (additionalRowClass)
Adds CSS classes to existing rows. Lightweight — doesn't change layout.
- Alternating row colors, conditional row highlighting (overdue tinting)
- Applied via: View dropdown → Format current view → Advanced mode

### Level 3: Row Template (rowFormatter)
**REPLACES the entire row layout.** This is the power move. Instead of SharePoint's default column grid, you define the complete HTML structure of each row.
- Full card layouts with sidebars, composed metadata, multi-section rows
- Can combine multiple columns into a single visual composition
- Applied via: View dropdown → Format current view → Advanced mode (uses `rowFormatter` key instead of `additionalRowClass`)

### Level 4: Tile Formatting
Gallery/card view layouts. Each item renders as a card instead of a row.
- Standalone card designs with headers, bodies, footers, progress indicators
- Applied via: Gallery view → Format current view → Advanced mode

**Rule: Every style MUST use at least Level 1 + Level 3. Level 3 (rowFormatter) is what creates the "I can't believe it" impact. Column formatting alone is a 3/10.**

---

## The Style Application Workflow

### Step 1: Read the list schema — required before generating any JSON
Know the columns, their internal names, types, and Choice values. Get this from SHAREPOINT.md if available, or ask the user. **Do not generate any JSON until you have the actual column names and Choice values.**

### Step 2: Read the style token file
Load the matching `style-{name}/SKILL.md`. It contains design tokens and a `rowFormatter` reference template. The column names in that template (`[$Status]`, `[$Progress]`, `[$Deadline]`) are **example placeholders** that almost certainly do not match the user's list.

### Step 3: Map the user's columns to the template

The style file's rowFormatter uses reference column names: `[$Title]`, `[$FileLeafRef]`, `[$Status]`, `[$Progress]`, `[$Deadline]`. These are examples — the user's list will likely have different column names.

**Before applying the rowFormatter, you MUST adapt it:**

1. Identify which column in the user's list serves each role:
   - **Name/Title role**: The item or document name (e.g., `[$Title]`, `[$FileLeafRef]`, `[$ProjectName]`)
   - **Status role**: A Choice column with workflow states (e.g., `[$Status]`, `[$Phase]`, `[$Stage]`)
   - **Progress role**: A Number column 0-100 (e.g., `[$Progress]`, `[$Completion]`, `[$PercentComplete]`)
   - **Deadline role**: A DateTime column (e.g., `[$Deadline]`, `[$DueDate]`, `[$TargetDate]`)

2. Find-and-replace all `[$ReferenceName]` values in the rowFormatter JSON with the actual internal column names.

3. Update the status_colors `if()` expressions to use the actual Choice values from the user's list. If they use "Active" instead of "In Review", or "Complete" instead of "Published", remap accordingly using the same color logic from the style tokens.

4. If the user's list has ADDITIONAL columns not covered by the style template (e.g., Owner, Priority, Category), decide where to surface them:
   - In the sidebar/panel area alongside existing metadata
   - In the main content area replacing the "Open Item" button
   - As additional inline elements in the metadata row

5. If the user's list is MISSING a column the template expects (e.g., no Deadline column), remove that section from the rowFormatter rather than letting it error.

**The style's rowFormatter is a reference implementation. Adapt it to the user's data — do not paste it verbatim.**

### Step 4: Generate formatters — in this order

**A. Row Template (rowFormatter) — DO THIS FIRST**
This is the centerpiece. The style token file defines the row layout structure. Generate the complete `rowFormatter` JSON that composes all columns into the styled row design.

**B. Column Formatters — FOR COLUMNS NOT HANDLED BY rowFormatter**
If the row template covers Status, Progress, and Deadline inline, you may not need separate column formatters for those. But any column NOT included in the rowFormatter still needs its own formatter.

**C. View Formatting — IF the style uses alternating rows or row highlighting**
Add `additionalRowClass` only if the style specifies it AND only if you're NOT using a `rowFormatter` (the two conflict — `rowFormatter` replaces the row entirely, so `additionalRowClass` has no effect when `rowFormatter` is active).

**D. Tile Formatting — IF the user wants a gallery/card view**
Generate tile formatting for card-based layouts.

### Step 5: Create a custom view
Tell the user to create a new view named after the style (e.g., "Neobrutalism") so the formatting doesn't affect the default "All Items" view.

### Step 6: Apply and verify

---

## rowFormatter Structure

This is the most powerful tool. It replaces the entire row with a custom layout.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/view-formatting.schema.json",
  "hideSelection": false,
  "hideColumnHeaders": true,
  "rowFormatter": {
    "elmType": "div",
    "style": { ... },
    "children": [ ... ]
  }
}
```

**Key behaviors:**
- `hideColumnHeaders: true` — hides the default column headers since the row template defines its own layout
- Access any column value with `[$InternalColumnName]`
- Can compose multiple columns into a single visual element
- Supports all the same style properties as column formatters
- Can include buttons, links, icons, conditional elements

**Layout patterns the style file can define:**
- **Card row**: Full-width card per item with sidebar + main content
- **Split row**: Left panel (metadata) + right panel (details)
- **Compact row**: Single line with composed inline elements
- **Summary card**: Tile-style card within a list view

---

## SharePoint JSON Formatting Reference

### Supported
- `elmType`: `div`, `span`, `a`, `img`, `svg`, `path`, `button`
- All CSS properties via inline `style` object
- `border-radius`, `text-transform`, `box-shadow`, `overflow`, `gap` — all work
- Colors: hex only (`#ffffff`)
- Emoji in `txtContent` — works for icons
- `customRowAction` with `action: "defaultClick"` — makes elements clickable to open the item
- `forEach` — iterate over multi-value fields
- Expressions: `@currentField`, `[$ColumnName]`, `@now`, `@me`, `@rowIndex`
- `toString()`, `Number()`, `toLocaleDateString()`, `if()`, `indexOf()`, `substring()`

### NOT Supported
- `backdrop-filter`, gradients, `rgb()`/`rgba()`/`hsl()`
- Custom CSS classes in column formatters (only built-in SP classes in `additionalRowClass`)
- CSS variables, hover pseudo-states
- Nested `if()` beyond ~10 levels

### Common Mistakes
- Forgetting `$schema`
- Display names vs internal names (spaces → `_x0020_`)
- Case-sensitivity on Choice values
- Number column stores 0.72 not 72
- Trailing commas (invalid JSON)
- Using `additionalRowClass` WITH `rowFormatter` (they conflict — rowFormatter wins)

---

## What "11/10 Ambition" Looks Like

The difference between "formatted" and "I can't believe that's SharePoint":

| Formatted (3/10) | Styled (7/10) | Art-Directed (11/10) |
|---|---|---|
| Colored status pills | Status badges with style-specific shape/border | Full row template with composed status + progress + deadline in a card layout |
| Default progress bar colors | Styled progress bar (height, border, colors) | Progress bar integrated into the row card with contextual coloring and inline label |
| Date string | Date with overdue coloring | Composed deadline block with icon, date, sublabel, and conditional overdue treatment — all positioned within the row card |
| Default row grid | Alternating row colors | Complete row template that recomposes the entire layout into the style's signature pattern |
| No view changes | Custom view name | Custom view with rowFormatter + style-specific header treatment |

**The token file defines the row template. The engine generates it. RALPH iterates until it hits 11/10.**

---

## Application Instructions

**Creating a styled view:**
1. Go to the list/library
2. Click "Add view" → name it after the style (e.g., "Neobrutalism")
3. Select columns to include: the columns identified in your Step 3 mapping
4. Save the view
5. Click the view dropdown → "Format current view" → "Advanced mode"
6. Paste the rowFormatter JSON
7. For any columns NOT covered by the rowFormatter, apply individual column formatters

**Important:** Always create a new view. Never modify "All Items" or "All Documents" directly.
