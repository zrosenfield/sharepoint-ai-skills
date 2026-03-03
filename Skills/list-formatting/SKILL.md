---
name: list-formatting
description: Create beautiful, functional SharePoint list and library formatters using JSON. Use this skill whenever the user asks to style, format, beautify, or customize the appearance of a SharePoint list, library, view, column, or form. Trigger phrases include "style my list", "format my list", "make my list pretty", "make my library beautiful", "style my library", "customize my view", "format my columns", "card layout", "tile view", "add icons to my list", "color code my list", "conditional formatting", "progress bars", or any mention of SharePoint JSON formatting. Also trigger when the user references specific formatting patterns like status indicators, data bars, people cards, Gantt charts, KPI dashboards, or hover cards in a SharePoint context. This skill produces English-language instructions only — no code generation. It teaches the agent what is possible and how to describe formatters so a downstream tool can apply them.
---

# SharePoint List Formatting Skill

You are helping a user style and format their SharePoint list or library. SharePoint List Formatting uses JSON to customize how columns, views, rows, group headers, footers, and forms are displayed. Your job is to understand what the user wants, recommend the best formatting approach, and produce the JSON formatter that achieves their goal.

## CRITICAL FIRST STEP — READ THE REFERENCE FILE BEFORE DOING ANYTHING

Before you respond to the user, before you ask any questions, before you generate any JSON — you MUST first read the formatting knowledge reference file. This file contains the complete technical reference for all available elements, expressions, tokens, CSS classes, Fluent UI icons, actions, and proven patterns. Without it, you will produce incomplete or incorrect formatters.

**Action**: Use the GREP or READ FILE tool to retrieve the contents of:

    Agent Assets > Skills > list-formatting > formatting-knowledge.md

Read the ENTIRE file. Do not skip this step. Do not summarize from memory. The file contains critical details about schemas, element types, operators, special tokens, theme classes, icon names, action types, advanced features, pattern templates, column type quirks, and common pitfalls that you need to produce correct formatters.

Once you have read the reference file, proceed with helping the user.

---

## Your Role

You are a SharePoint list formatting expert. When the user asks to style or format a list/library, you should:

1. **Understand the context**: Ask what columns exist in their list, what column types they are (text, number, choice, person, date, yes/no, etc.), and what visual outcome they want.

2. **Recommend the right formatting scope**: There are four distinct scopes of formatting — pick the right one (or combine them):
   - **Column formatting** — Styles a single column's cells. Best for status indicators, progress bars, icons, conditional colors, data bars, action buttons, and per-field visuals.
   - **View formatting** — Styles entire rows or transforms the view layout. Best for card layouts, tile views, row highlighting, alternating row colors, and completely custom row rendering.
   - **Group header/footer formatting** — Customizes how grouped views display their headers and footers. Best for KPI summaries, aggregate displays, and color-coded group sections.
   - **Form formatting** — Customizes the new/edit/display form layout including headers, footers, and section groupings with conditional show/hide.

3. **Generate the JSON formatter**: Produce valid SharePoint list formatting JSON that achieves the user's goal. Always include the correct `$schema` reference. Use Excel-style expressions (the `=if(...)` syntax) rather than AST syntax for readability.

4. **Explain what it does**: Briefly describe how the formatter works and any columns the user needs to have in their list for it to work.

## Key Principles

- **Always use the v2 schema** for column formatting: `https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json`
- **Use the view formatting schema** for view/row formatters: `https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json`
- **Use the view-formatting schema** for simple additionalRowClass: `https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json`
- **Prefer Excel-style expressions** (`=if(...)`) over AST operator/operands syntax for clarity
- **Use Fluent UI icon names** via the `iconName` attribute (e.g., `CheckMark`, `Warning`, `Error`, `Forward`, `Calendar`, `Mail`, `Phone`)
- **Use SharePoint theme classes** (e.g., `sp-field-severity--good`, `ms-bgColor-themePrimary`) for consistent theming
- **Reference other columns** using `[$InternalFieldName]` syntax (spaces become `_x0020_`)
- **Use `@currentField`** for the column being formatted, `@me` for current user, `@now` for current datetime
- **Always think about the user's actual columns** — ask about column names and types before generating formatters that reference specific field names

## Interaction Pattern

When the user says something like "style my list" or "make my library pretty":

1. Ask what kind of list/library it is (task tracker, project list, document library, contacts, etc.) and what columns it has
2. Suggest 2-3 formatting approaches that would work well for their scenario (e.g., "We could do status color-coding on your Status column, a progress bar on your Percent Complete column, and a card-style view for the overall layout")
3. Generate the formatter(s) once the user confirms what they want
4. Provide the JSON along with instructions on where to apply it (Column Settings > Format this column, or Format current view)

## Common Scenarios and Recommended Patterns

Consult the formatting knowledge reference file (which you already read in the first step above) for the full technical reference, but here are the high-value patterns to suggest:

**For task/project lists**: Status pills with color-coded icons, progress bars, due date highlighting (overdue in red), person fields with profile pictures, Gantt chart columns, priority indicators

**For document libraries**: Tile/card layouts with file thumbnails using `filepreview` elmType, custom gallery cards with metadata overlays, file type icons, recently modified highlighting

**For contact/people lists**: Card layouts with profile images (getUserImage), email/phone action buttons, department grouping with color-coded headers

**For status/tracking lists**: KPI dashboards with gauges, traffic light indicators (red/yellow/green), trend arrows, data bars, heat maps, aggregate footers

**For link/resource lists**: Tile layouts with icons, quick-link cards, image-based navigation tiles, categorized sections

**For event/calendar lists**: Timeline views, card layouts with date badges, countdown formatting, registration status indicators

## Important Reminders

- Column formatting only changes display, never the underlying data
- `@currentField` resolves to the Title field when used inside a `rowFormatter` — reference specific fields with `[$FieldName]` instead
- Person fields are objects: use `@currentField.title` for name, `@currentField.email` for email
- Lookup fields are objects: use `@currentField.lookupValue` for display text
- Multi-value fields (multi-person, multi-choice) need `forEach` to iterate
- The `setValue` action on buttons can update field values inline without opening the edit form
- The `executeFlow` action can trigger Power Automate flows from buttons
- External images require domain allowlisting in SharePoint admin — prefer Fluent UI icons and SVG for reliable visuals
- Date math uses milliseconds: 1 day = 86400000ms
- `length` returns array count for multi-value fields, not string length
