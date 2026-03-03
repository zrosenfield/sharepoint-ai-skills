# SharePoint List Formatting — Complete Technical Reference

This reference contains everything you need to generate correct, beautiful SharePoint list formatters. Read this before generating any formatter JSON.

## Table of Contents

1. [Formatting Scopes](#1-formatting-scopes)
2. [JSON Schema and Structure](#2-json-schema-and-structure)
3. [Element Types (elmType)](#3-element-types)
4. [Properties Reference](#4-properties-reference)
5. [Expressions and Operators](#5-expressions-and-operators)
6. [Special Tokens and Variables](#6-special-tokens-and-variables)
7. [Available CSS Classes](#7-available-css-classes)
8. [Fluent UI Icons](#8-fluent-ui-icons)
9. [Actions (customRowAction)](#9-actions)
10. [Advanced Features](#10-advanced-features)
11. [Formatter Pattern Library](#11-formatter-pattern-library)
12. [Column Type Considerations](#12-column-type-considerations)
13. [Common Pitfalls](#13-common-pitfalls)

---

## 1. Formatting Scopes

SharePoint offers four distinct formatting scopes. Each uses a slightly different JSON structure.

### Column Formatting
Customizes how a single column's cells render in list view.
- Schema: `https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json`
- Applied via: Column header > Column Settings > Format this column > Advanced mode
- Root element: An `elm` object (typically a `div`)
- `@currentField` references the value of the column being formatted

### View Formatting (Row-level)
Customizes entire rows or applies conditional classes to rows.
- Simple row class schema: `https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json`
- Full row formatter schema: `https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json`
- Applied via: View dropdown > Format current view > Advanced mode
- Two approaches:
  - `additionalRowClass`: Adds CSS class(es) to each row conditionally (preserves column formatting)
  - `rowFormatter`: Completely overrides row rendering with custom layout
- Additional top-level properties: `hideSelection`, `hideColumnHeader`, `hideFooter`

### Group Header/Footer Formatting
Customizes grouped view headers and footers.
- Schema: `https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json`
- Applied via: View formatting (same place as row formatting)
- Uses `groupProps` object with `headerFormatter` and/or `footerFormatter`
- Access group data with `@group` token

### Form Formatting
Customizes the list item new/edit/display form.
- Configures header, footer, and body sections
- Can conditionally show/hide columns
- Applied via: List Settings > Form settings, or the form's edit icon

---

## 2. JSON Schema and Structure

Every formatter starts with a `$schema` declaration and an element tree.

### Column Format Structure
```
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { ... },
  "attributes": { ... },
  "txtContent": "...",
  "children": [ ... ]
}
```

### View Format with additionalRowClass
```
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json",
  "additionalRowClass": "=if([$Status] == 'Done', 'sp-field-severity--good', '')"
}
```

### View Format with rowFormatter
```
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json",
  "hideSelection": false,
  "hideColumnHeader": false,
  "rowFormatter": {
    "elmType": "div",
    "children": [ ... ]
  }
}
```

### View Format with Tile Layout (tileProps)
```
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/tile-formatting.schema.json",
  "height": 250,
  "width": 300,
  "hideSelection": false,
  "fillHorizontally": true,
  "formatter": {
    "elmType": "div",
    "children": [ ... ]
  }
}
```

### Group Header/Footer Format
```
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json",
  "groupProps": {
    "hideFooter": false,
    "headerFormatter": { "elmType": "div", ... },
    "footerFormatter": { "elmType": "div", ... }
  }
}
```

---

## 3. Element Types

The `elmType` property accepts these values:

| elmType | Description |
|---------|-------------|
| `div` | Block container element. Most common wrapper. |
| `span` | Inline container element. Good for text alongside other inline elements. |
| `a` | Hyperlink element. Requires `href` attribute. |
| `img` | Image element. Requires `src` attribute. Subject to domain restrictions. |
| `svg` | SVG container for vector graphics. Use with `path` children. |
| `path` | SVG path element. Requires `d` attribute for the path data. |
| `button` | Clickable button. Requires `customRowAction` to define what happens on click. |
| `p` | Paragraph element. |
| `filepreview` | Special element for document library thumbnails. Set `src` to `@thumbnail.medium` (or small/large). Shows file type brand icon overlay. |

---

## 4. Properties Reference

### txtContent
Sets the text content of the element. Can be a static string or an expression.
- `"txtContent": "@currentField"` — shows field value
- `"txtContent": "='Status: ' + @currentField"` — concatenated text
- If `txtContent` is set, `children` are ignored

### style
Object of CSS property/value pairs. Values can be strings or expressions.

Key allowed style properties (partial list of most useful ones):
- Layout: `display`, `flex-direction`, `flex-wrap`, `justify-content`, `align-items`, `flex-grow`, `flex-shrink`, `position`, `top`, `right`, `bottom`, `left`, `z-index`, `overflow`
- Sizing: `width`, `height`, `min-width`, `max-width`, `min-height`, `max-height`
- Spacing: `margin`, `margin-top/right/bottom/left`, `padding`, `padding-top/right/bottom/left`
- Background: `background-color`, `background-image`, `fill`, `opacity`
- Border: `border`, `border-radius`, `border-top/right/bottom/left`, `box-shadow`
- Text: `color`, `font-size`, `font-weight`, `font-family`, `text-align`, `text-decoration`, `text-overflow`, `text-transform`, `line-height`, `letter-spacing`, `white-space`, `word-break`, `-webkit-line-clamp`
- SVG: `stroke`, `fill-opacity`
- Transform: `transform` (only `translate()` supported)

**Note**: `float` is deprecated. Use flexbox instead.

### attributes
Object of HTML attribute/value pairs. Allowed attribute names:
- `href`, `rel`, `src`, `class`, `target`, `title`, `role`
- `iconName` — renders a Fluent UI icon by name
- `d` — SVG path data
- `aria` — accessibility attributes
- `data-interception` — controls link behavior (`off` to open in new context)
- `viewBox`, `preserveAspectRatio` — SVG attributes
- `draggable`

### children
Array of child element objects. Allows arbitrary nesting depth.

### forEach
Duplicates the element for each value in a multi-value field or array.
- Syntax: `"forEach": "iteratorName in @currentField"` or `"forEach": "iteratorName in [$FieldName]"`
- Access iterator value like a field: `[$iteratorName]`, `[$iteratorName.title]`, etc.
- Access index with `loopIndex` operator
- Cannot be on the root element
- Works with multi-person, multi-choice, and multi-lookup fields

### debugMode
Set to `true` to output error messages and warnings to browser console.

---

## 5. Expressions and Operators

### Excel-Style Expressions (Preferred)
Begin with `=` sign. More readable and recommended for SharePoint Online.

```
=if(@currentField == 'Done', 'sp-field-severity--good', '')
=if([$DueDate] <= @now, '#ff0000', '#00ff00')
=if([$Progress] <= 0.3, 'Low', if([$Progress] <= 0.7, 'Medium', 'High'))
='mailto:' + @currentField.email
=toString([$Number] * 100) + '%'
=if(@me == [$AssignedTo.email], '', 'none')
```

### Available Operators

**Arithmetic**: `+`, `-`, `*`, `/`, `%` (modulus)
**Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
**Logical**: `&&`, `||`
**Conditional**: `?` (ternary), `if(condition, trueVal, falseVal)`

**String operations**:
- `toString()` — convert to string
- `toLowerCase`, `toUpperCase` — case conversion
- `indexOf(haystack, needle)` — find position (-1 if not found)
- `lastIndexOf(text, search)` — last position
- `startsWith(text, prefix)`, `endsWith(text, suffix)` — boolean tests
- `substring(text, start, end)` — extract portion
- `replace(text, search, replacement)` — first occurrence
- `replaceAll(text, search, replacement)` — all occurrences
- `padStart(text, length, padChar)`, `padEnd(text, length, padChar)` — padding
- `split(text, separator)` — returns array
- `join(array, separator)` — array to string
- `length` — count of items in array/multi-value (NOT string length)

**Number operations**:
- `Number()` — convert to number
- `abs`, `floor`, `ceiling` — rounding
- `pow(base, exp)` — exponentiation
- `cos`, `sin` — trigonometry (radians)
- `toLocaleString()` — locale-aware number display

**Date operations**:
- `Date(string)` — parse string to date
- `getDate(date)` — day of month (1-31)
- `getMonth(date)` — month (0-based: 0=Jan, 11=Dec)
- `getYear(date)` — full year
- `addDays(date, days)` — add/subtract days
- `addMinutes(date, minutes)` — add/subtract minutes
- `toLocaleDateString()`, `toLocaleTimeString()`, `toLocaleString()` — locale-aware display
- `toDateString()` — short date format like "Wed Aug 03 2022"

**Array operations**:
- `appendTo(array, value)` — return new array with value added
- `removeFrom(array, value)` — return new array with value removed
- `indexOf(array, value)` — find index in array
- `join(array, separator)` — concatenate with separator
- `length` — count items

**Image operations**:
- `getUserImage(email, size)` — returns URL to user's profile photo. Sizes: `'small'`/`'s'`, `'medium'`/`'m'`, `'large'`/`'l'`
- `getThumbnailImage(fieldName, width, height)` — for thumbnail column

---

## 6. Special Tokens and Variables

| Token | Description |
|-------|-------------|
| `@currentField` | Value of the column being formatted. In rowFormatter, always resolves to Title. |
| `@currentField.title` | Display name from a Person field |
| `@currentField.email` | Email from a Person field |
| `@currentField.id` | User ID from a Person field |
| `@currentField.picture` | Profile picture URL from a Person field |
| `@currentField.department` | Department from a Person field |
| `@currentField.jobTitle` | Job title from a Person field |
| `@currentField.lookupValue` | Display text from a Lookup field |
| `@currentField.lookupId` | ID from a Lookup field |
| `@currentField.desc` | Description from a Hyperlink field |
| `@me` | Current user's email address |
| `@now` | Current date/time (evaluated when view loads) |
| `@rowIndex` | Zero-based index of the current row in the view |
| `@window.innerWidth` | Browser window width in pixels |
| `@window.innerHeight` | Browser window height in pixels |
| `[$FieldInternalName]` | Value of another column in the same row |
| `[$FieldName.title]` | Person sub-property from another column |
| `[$FieldName.email]` | Person email sub-property from another column |
| `[$FieldName.lookupValue]` | Lookup display text from another column |
| `@thumbnail.small` | Small thumbnail URL (document library) |
| `@thumbnail.medium` | Medium thumbnail URL (document library) |
| `@thumbnail.large` | Large thumbnail URL (document library) |
| `@currentWeb` | Current site URL |
| `@group.fieldData` | Current group's field value (in groupProps) |
| `@group.fieldData.displayValue` | Display value for the group field |
| `@group.count` | Number of items in the group |
| `@aggregates` | Array of column aggregates (in groupProps) |
| `@columnAggregate.type` | Aggregate function name (in footerFormatter) |
| `@columnAggregate.value` | Aggregate result value |
| `@columnAggregate.columnDisplayName` | Column display name for aggregate |

**Internal field name rules**: Spaces in field names become `_x0020_`. For example, a field named "Due Date" is referenced as `[$Due_x0020_Date]`. Special characters are similarly encoded.

---

## 7. Available CSS Classes

SharePoint provides built-in CSS classes that respect the site theme. Always prefer these over hardcoded colors.

### Severity / Status Classes (apply to parent div)
- `sp-field-severity--good` — green background (success/done)
- `sp-field-severity--low` — pale blue (in progress/info)
- `sp-field-severity--warning` — yellow/orange (warning/in review)
- `sp-field-severity--severeWarning` — darker orange (urgent/overdue)
- `sp-field-severity--blocked` — red background (blocked/critical)

### Theme Background Classes (ms-bgColor-*)
- `ms-bgColor-themePrimary`, `ms-bgColor-themeSecondary`, `ms-bgColor-themeTertiary`
- `ms-bgColor-themeDark`, `ms-bgColor-themeDarker`, `ms-bgColor-themeDarkAlt`
- `ms-bgColor-themeLight`, `ms-bgColor-themeLighter`, `ms-bgColor-themeLighterAlt`
- `ms-bgColor-neutralPrimary`, `ms-bgColor-neutralLight`, `ms-bgColor-neutralLighter`
- `ms-bgColor-white`, `ms-bgColor-black`
- `ms-bgColor-red`, `ms-bgColor-green`, `ms-bgColor-blue`, `ms-bgColor-orange`, `ms-bgColor-yellow`, `ms-bgColor-teal`, `ms-bgColor-purple`

### Contextual Background Classes (sp-css-backgroundColor-*)
- `sp-css-backgroundColor-BgPeach`, `sp-css-backgroundColor-BgGold`
- `sp-css-backgroundColor-BgLavender`, `sp-css-backgroundColor-BgMint`
- `sp-css-backgroundColor-successBackground50`, `sp-css-backgroundColor-warningBackground50`
- `sp-css-backgroundColor-errorBackground50`, `sp-css-backgroundColor-blockingBackground50`
- `sp-css-backgroundColor-blueBackground37`
- `sp-css-backgroundColor-noBackground` (transparent)

### Text Color Classes
- `ms-fontColor-themePrimary`, `ms-fontColor-themeSecondary`
- `ms-fontColor-neutralPrimary`, `ms-fontColor-neutralSecondary`, `ms-fontColor-neutralTertiary`
- `ms-fontColor-white`, `ms-fontColor-black`
- `ms-fontColor-red`, `ms-fontColor-green`, `ms-fontColor-blue`
- `sp-css-color-GreenFont`, `sp-css-color-YellowFont`, `sp-css-color-RedFont`, `sp-css-color-DarkRedFont`

### Font Size Classes
- `ms-fontSize-12`, `ms-fontSize-14`, `ms-fontSize-16`, `ms-fontSize-18`, `ms-fontSize-20`, `ms-fontSize-24`, `ms-fontSize-28`, `ms-fontSize-32`, `ms-fontSize-42`, `ms-fontSize-68`
- `sp-field-fontSize--small`, `sp-field-fontSize--standard`, `sp-field-fontSize--large`

### Font Weight Classes
- `ms-fontWeight-regular`, `ms-fontWeight-semibold`, `ms-fontWeight-bold`

### Border Classes
- `ms-borderColor-themePrimary`, `ms-borderColor-neutralLight`
- `sp-css-borderColor-neutralLight`, `sp-css-borderColor-neutralSecondary`
- `sp-field-borderAllRegular` — adds borders all around
- `sp-field-borderAllSolid` — solid border style

### Card and Row Layout Classes
- `sp-row-card` — standard card styling for rowFormatter
- `sp-row-title` — title text in card layout
- `sp-row-listPadding` — standard list padding
- `sp-row-button` — button styling in card layout
- `sp-card-container` — tile/card container
- `sp-card-defaultClickButton` — clickable card area
- `sp-card-subContainer` — inner card section

### Quick Action Classes
- `sp-field-quickActions` — styles an element as a quick action icon/button

---

## 8. Fluent UI Icons

Use the `iconName` attribute to show any Fluent UI icon. Icons render as font glyphs and inherit text color.

### Commonly Used Icons by Category

**Status/Severity**: `CheckMark`, `Cancel`, `Warning`, `Error`, `ErrorBadge`, `Info`, `StatusCircleCheckmark`, `StatusCircleErrorX`, `Blocked`, `Completed`, `CompletedSolid`

**Navigation/Action**: `Forward`, `Back`, `ChevronRight`, `ChevronDown`, `ChevronUp`, `More`, `MoreVertical`, `Link`, `OpenInNewWindow`, `OpenInNewTab`

**Communication**: `Mail`, `Phone`, `Chat`, `Comment`, `Send`, `SkypeMessage`, `Video`

**People**: `Contact`, `ContactCard`, `People`, `Group`, `AddFriend`, `UserFollowed`

**Files/Documents**: `Document`, `Page`, `FileCode`, `PDF`, `ExcelDocument`, `WordDocument`, `PowerPointDocument`, `OneNoteLogo`, `Folder`, `FolderOpen`, `Attach`

**Calendar/Time**: `Calendar`, `Clock`, `DateTime`, `ScheduleEventAction`, `Event`

**Data/Charts**: `BarChartVertical`, `BarChart4`, `LineChart`, `PieDouble`, `AreaChart`, `DonutChart`

**Editing**: `Edit`, `EditNote`, `Delete`, `Add`, `Remove`, `Save`, `Undo`, `Redo`, `Copy`, `Paste`

**Trending**: `StockUp`, `StockDown`, `SortUp`, `SortDown`, `Trending12`, `Market`

**Misc Useful**: `FavoriteStar`, `FavoriteStarFill`, `Heart`, `HeartFill`, `Like`, `LikeSolid`, `Pin`, `Pinned`, `Flag`, `FlagFill`, `Emoji2`, `LocationDot`, `Home`, `Settings`, `Search`, `Filter`, `Refresh`

Full icon list: https://developer.microsoft.com/en-us/fluentui#/styles/web/icons

---

## 9. Actions (customRowAction)

Buttons can trigger actions via `customRowAction`. Available actions:

| Action | What It Does |
|--------|-------------|
| `defaultClick` | Same as clicking the list item (opens item/file) |
| `share` | Opens the sharing dialog |
| `delete` | Opens delete confirmation |
| `editProps` | Opens item properties in edit mode |
| `openContextMenu` | Opens the item's right-click context menu |
| `setValue` | Updates field values inline without opening edit form |
| `executeFlow` | Launches a Power Automate flow by ID |
| `embed` | Opens a callout with embedded content (URL in iframe) |

### setValue Example Pattern
```json
{
  "elmType": "button",
  "txtContent": "Approve",
  "customRowAction": {
    "action": "setValue",
    "actionInput": {
      "Status": "Approved",
      "ApprovedBy": "@me"
    }
  }
}
```

### executeFlow Example Pattern
```json
{
  "elmType": "button",
  "txtContent": "Start Process",
  "customRowAction": {
    "action": "executeFlow",
    "actionParams": "{\"id\":\"YOUR-FLOW-GUID-HERE\", \"headerText\":\"Start Process\", \"runFlowButtonText\":\"Run\"}"
  }
}
```

---

## 10. Advanced Features

### Custom Hover Cards (customCardProps)
Add a rich hover card to any element:
```json
{
  "elmType": "div",
  "txtContent": "@currentField",
  "customCardProps": {
    "openOnEvent": "hover",
    "directionalHint": "bottomCenter",
    "isBeakVisible": true,
    "formatter": {
      "elmType": "div",
      "style": { "padding": "16px", "width": "200px" },
      "children": [
        { "elmType": "div", "txtContent": "='Details for: ' + @currentField", "style": { "font-weight": "bold" } },
        { "elmType": "div", "txtContent": "[$Description]" }
      ]
    }
  }
}
```

Directional hints: `bottomCenter`, `bottomAutoEdge`, `bottomLeftEdge`, `bottomRightEdge`, `topCenter`, `topAutoEdge`, `leftCenter`, `rightCenter`, etc.

### Inline Editing (inlineEditField)
Make a field editable directly in the view:
```json
{
  "elmType": "div",
  "inlineEditField": "[$FieldName]",
  "txtContent": "[$FieldName]"
}
```

### Column Formatter Reference (columnFormatterReference)
Reuse another column's formatter:
```json
{
  "columnFormatterReference": "[$FieldName]"
}
```

### File Preview (filepreview)
Show document thumbnails in libraries:
```json
{
  "elmType": "filepreview",
  "attributes": { "src": "@thumbnail.medium" },
  "style": { "width": "100%", "height": "150px" }
}
```

### Default Hover Field
Show profile cards for people or file hover cards:
```json
{
  "defaultHoverField": "[$Editor]"
}
```

### Tile Layout (tileProps)
For gallery/card views, use tileProps to define tile dimensions:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/tile-formatting.schema.json",
  "height": 300,
  "width": 350,
  "hideSelection": false,
  "fillHorizontally": true,
  "formatter": {
    "elmType": "div",
    "style": {
      "display": "flex",
      "flex-direction": "column",
      "height": "100%",
      "border": "1px solid #ededed",
      "border-radius": "8px",
      "overflow": "hidden"
    },
    "children": [ ... ]
  }
}
```

---

## 11. Formatter Pattern Library

These are proven, high-value patterns. Use them as starting points and customize for the user's specific columns.

### Pattern: Status Pill with Icon
Turns a choice/text field into a color-coded pill with icon.
- Use `sp-field-severity--*` classes or custom background colors
- Map each status value to a specific icon and color
- Works for: Status, Priority, Risk, Phase, Approval fields

### Pattern: Progress Bar
Renders a percentage field as a horizontal bar.
- Use a parent div with background color for the track
- Use a child div with width set to `=toString(@currentField * 100) + '%'` and a fill color
- Optionally show the percentage as text overlay

### Pattern: Due Date with Overdue Highlighting
Colors date fields based on proximity to today.
- Red if `[$DueDate] <= @now` (overdue)
- Orange if `[$DueDate] <= @now + 259200000` (3 days = 3*86400000)
- Green if further out
- Show calendar icon alongside

### Pattern: Person with Profile Picture
Shows a person field as avatar + name.
- Use `getUserImage([$Person.email], 'small')` for the photo
- Display as circular image with name beside it
- Add `defaultHoverField` for profile card on hover

### Pattern: Traffic Light / RAG Status
Three colored circles (Red, Amber, Green) based on field value.
- Use SVG circles or colored div elements
- Map values: "Red"/"High"/"Critical" → red, "Amber"/"Medium"/"Warning" → yellow, "Green"/"Low"/"On Track" → green

### Pattern: Data Bar (Number Visualization)
Horizontal bar whose width represents a number value.
- Set the bar width as a percentage of max value
- Use theme colors for the fill
- Good for scores, completion, capacity, budget usage

### Pattern: Card Layout (rowFormatter)
Transforms the entire row into a card.
- Use rowFormatter with flexbox layout
- Include title, subtitle, metadata fields, and action buttons
- Add hover effect with box-shadow transition
- Set `hideColumnHeader: true` for cleaner look

### Pattern: Tile / Gallery View
Uses tileProps for card grid.
- Great for document libraries, link lists, and image-heavy lists
- Include filepreview for thumbnails or image fields for photos
- Add metadata overlay at bottom of tile

### Pattern: Alternating Row Colors
Simple view format using additionalRowClass:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json",
  "additionalRowClass": "=if(@rowIndex % 2 == 0, 'ms-bgColor-themeLight', '')"
}
```

### Pattern: Conditional Row Highlighting
Highlight entire rows based on status or date:
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json",
  "additionalRowClass": "=if([$Status] == 'Blocked', 'sp-field-severity--blocked', if([$Status] == 'Done', 'sp-field-severity--good', ''))"
}
```

### Pattern: Inline Action Buttons
Buttons that update field values without opening edit form:
- "Approve/Reject" buttons that set Status and ApprovedBy fields
- "Assign to Me" button that sets a person field to @me
- "Mark Complete" button that sets Status to Done and CompletedDate to @now

### Pattern: Grouped KPI Dashboard
Use groupProps with headerFormatter:
- Show group icon, name, and count
- Display aggregate values (sum, average, count)
- Color-code headers based on group values or thresholds

### Pattern: Emoji/Icon Rating
Display number values as star ratings or emoji:
- Use forEach on a generated array or conditional icon rendering
- Fill stars gold up to the rating value, empty after

### Pattern: Gantt Chart Column
Use SVG bars positioned based on start/end dates:
- Calculate bar position and width from date math
- Show task name overlay
- Color by status or category

### Pattern: Heat Map
Color cells based on value intensity:
- Use calculated RGB values based on min/max range
- Or map ranges to predefined color classes

---

## 12. Column Type Considerations

Each column type has specific quirks:

| Column Type | Access Pattern | Notes |
|------------|---------------|-------|
| Text/Choice | `@currentField` | Direct string value |
| Number | `@currentField` | Numeric value, use in math |
| Currency | `@currentField` | Number with locale formatting via toLocaleString |
| Date/Time | `@currentField` | Date object, compare with @now, use Date() for parsing |
| Yes/No | `@currentField` | Returns 1 (yes) or 0 (no), NOT true/false |
| Person | `@currentField.title`, `.email`, `.id`, `.picture`, `.department`, `.jobTitle` | Object with sub-properties |
| Multi-Person | `forEach` + iterator | Use forEach to loop; length for count |
| Lookup | `@currentField.lookupValue`, `.lookupId` | Object with sub-properties |
| Multi-Lookup | `forEach` + iterator | Use forEach to loop |
| Multi-Choice | `forEach` + iterator | Use forEach to loop; or join() for display |
| Hyperlink | `@currentField`, `@currentField.desc` | URL value and optional description |
| Image/Picture | `@currentField` | URL to image |
| Location | `@currentField.DisplayName`, `.Street`, `.City`, `.State`, `.CountryOrRegion`, `.Latitude`, `.Longitude` | Rich location object |
| ContentType | `@currentField` | Content type name string |
| Calculated | Varies | Result type determines access pattern |

### Document Library Special Fields
- `[$FileLeafRef]` — File name with extension
- `[$FileRef]` — Full server-relative path
- `[$File_x0020_Type]` — File extension
- `[$ContentType]` — Content type name
- `[$Modified]` — Last modified date
- `[$Editor]` — Last modified by (person)
- `[$Created]` — Created date
- `[$Author]` — Created by (person)
- `[$FileSizeDisplay]` — File size
- `@thumbnail.small/medium/large` — Thumbnail URLs

---

## 13. Common Pitfalls

1. **Field internal names vs display names**: Always use internal names in `[$...]` references. Spaces become `_x0020_`, special characters are encoded. When unsure, ask the user for the internal name or tell them how to find it (List Settings > click column name > look at URL parameter `Field=`).

2. **@currentField in rowFormatter**: Inside a rowFormatter, `@currentField` always resolves to the Title field. Use `[$FieldInternalName]` to reference specific columns.

3. **Person field is an object**: Don't use `[$AssignedTo]` directly for display — use `[$AssignedTo.title]` for name, `[$AssignedTo.email]` for email.

4. **Yes/No returns 0 or 1**: Not `true`/`false`. Use `=if(@currentField == 1, 'Yes', 'No')`.

5. **Date comparison uses milliseconds**: `@now` returns epoch milliseconds. Adding days means adding `numberOfDays * 86400000`.

6. **length is not for strings**: The `length` operator returns array count (for multi-value fields). For string length, use the `indexOf` workaround: there is no native string length function.

7. **External images blocked**: Images from external domains are blocked by default. Prefer Fluent UI icons, SVG paths, or theme classes for reliable visuals. If the user needs external images, they must allowlist the domain in SharePoint admin.

8. **additionalRowClass and rowFormatter are mutually exclusive**: If you specify rowFormatter, additionalRowClass is ignored.

9. **float is deprecated**: Use CSS flexbox (`display: flex`, `flex-direction`, `justify-content`, `align-items`) instead.

10. **Schema matters**: Using the wrong schema can cause the formatter to silently fail. Column formatters use the column-formatting schema, view formatters use view-formatting or row-formatting schema.

11. **Maximum JSON size**: Very complex formatters may hit size limits. Keep formatters focused and efficient. If you need extreme complexity, consider splitting across column formatters + a lighter view formatter.

12. **Theme classes vs hardcoded colors**: Always prefer theme classes (`ms-bgColor-themePrimary`, `sp-field-severity--good`) over hex colors. Theme classes adapt to the site's theme and dark mode.
