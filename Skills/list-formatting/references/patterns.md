# SharePoint List Formatting — Pattern Library

Proven, high-value formatter patterns. Load this when the user asks for a specific named pattern, a starting template, or any scenario where a proven design would be the best starting point (card layouts, Gantt charts, KPI dashboards, status pills, progress bars, etc.).

These are starting points — customize column names and values to match the user's actual list.

---

## Pattern: Status Pill with Icon

Turns a choice/text field into a color-coded pill with icon.

Use `sp-field-severity--*` classes or custom background colors. Map each status value to a specific icon and color. Works for: Status, Priority, Risk, Phase, Approval fields.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "display": "flex",
    "align-items": "center",
    "padding": "4px 8px",
    "border-radius": "12px"
  },
  "attributes": {
    "class": "=if(@currentField == 'Done', 'sp-field-severity--good', if(@currentField == 'In Progress', 'sp-field-severity--low', if(@currentField == 'Blocked', 'sp-field-severity--blocked', 'sp-field-severity--warning')))"
  },
  "children": [
    {
      "elmType": "span",
      "attributes": {
        "iconName": "=if(@currentField == 'Done', 'CheckMark', if(@currentField == 'Blocked', 'Blocked', 'Forward'))"
      },
      "style": { "margin-right": "4px" }
    },
    { "elmType": "span", "txtContent": "@currentField" }
  ]
}
```

---

## Pattern: Progress Bar

Renders a percentage field (0–1 decimal) as a horizontal bar with label.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { "display": "flex", "flex-direction": "column", "width": "100%" },
  "children": [
    {
      "elmType": "div",
      "style": {
        "background-color": "#f3f2f1",
        "border-radius": "4px",
        "height": "8px",
        "width": "100%",
        "overflow": "hidden"
      },
      "children": [{
        "elmType": "div",
        "style": {
          "background-color": "=if(@currentField >= 1, '#107c10', if(@currentField >= 0.5, '#0078d4', '#d83b01'))",
          "height": "100%",
          "width": "=toString(@currentField * 100) + '%'"
        }
      }]
    },
    {
      "elmType": "div",
      "txtContent": "=toString(floor(@currentField * 100)) + '%'",
      "style": { "font-size": "12px", "color": "#605e5c", "margin-top": "2px" }
    }
  ]
}
```

---

## Pattern: Due Date with Overdue Highlighting

Colors date fields red (overdue), orange (due within 3 days), or normal.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": {
    "display": "flex",
    "align-items": "center",
    "color": "=if(@currentField <= @now, '#a4262c', if(@currentField <= @now + 259200000, '#d83b01', 'inherit'))",
    "font-weight": "=if(@currentField <= @now, 'bold', 'normal')"
  },
  "children": [
    {
      "elmType": "span",
      "attributes": { "iconName": "Calendar" },
      "style": { "margin-right": "4px" }
    },
    { "elmType": "span", "txtContent": "=toLocaleDateString(@currentField, 'en-US')" }
  ]
}
```

---

## Pattern: Person with Profile Picture

Shows a person field as a circular avatar with name and email link.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { "display": "flex", "align-items": "center" },
  "defaultHoverField": "@currentField",
  "children": [
    {
      "elmType": "img",
      "attributes": { "src": "=getUserImage(@currentField.email, 'small')" },
      "style": {
        "width": "32px", "height": "32px",
        "border-radius": "50%",
        "margin-right": "8px"
      }
    },
    {
      "elmType": "div",
      "style": { "display": "flex", "flex-direction": "column" },
      "children": [
        { "elmType": "span", "txtContent": "@currentField.title", "style": { "font-weight": "600" } },
        {
          "elmType": "a",
          "txtContent": "@currentField.email",
          "attributes": { "href": "='mailto:' + @currentField.email" },
          "style": { "font-size": "12px", "color": "#605e5c" }
        }
      ]
    }
  ]
}
```

---

## Pattern: Traffic Light / RAG Status

Three colored circles indicating Red, Amber, or Green status.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { "display": "flex", "gap": "6px", "align-items": "center" },
  "children": [
    {
      "elmType": "div",
      "style": {
        "width": "14px", "height": "14px", "border-radius": "50%",
        "background-color": "=if(@currentField == 'Red', '#a4262c', '#e0e0e0')"
      }
    },
    {
      "elmType": "div",
      "style": {
        "width": "14px", "height": "14px", "border-radius": "50%",
        "background-color": "=if(@currentField == 'Amber', '#d83b01', '#e0e0e0')"
      }
    },
    {
      "elmType": "div",
      "style": {
        "width": "14px", "height": "14px", "border-radius": "50%",
        "background-color": "=if(@currentField == 'Green', '#107c10', '#e0e0e0')"
      }
    },
    { "elmType": "span", "txtContent": "@currentField", "style": { "margin-left": "6px" } }
  ]
}
```

---

## Pattern: Card Layout (rowFormatter)

Transforms each row into a full-width card. Set `hideColumnHeader` to `true` for a clean look.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json",
  "hideColumnHeader": true,
  "rowFormatter": {
    "elmType": "div",
    "attributes": { "class": "sp-row-card" },
    "style": {
      "display": "flex",
      "flex-direction": "row",
      "align-items": "center",
      "padding": "12px 16px",
      "border-radius": "8px",
      "margin-bottom": "4px",
      "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"
    },
    "children": [
      {
        "elmType": "div",
        "style": { "flex-grow": "1" },
        "children": [
          { "elmType": "div", "txtContent": "[$Title]", "attributes": { "class": "sp-row-title" } },
          { "elmType": "div", "txtContent": "[$Description]", "style": { "color": "#605e5c", "font-size": "13px" } }
        ]
      },
      {
        "elmType": "div",
        "txtContent": "[$Status]",
        "style": { "padding": "4px 12px", "border-radius": "12px" },
        "attributes": {
          "class": "=if([$Status] == 'Done', 'sp-field-severity--good', if([$Status] == 'Blocked', 'sp-field-severity--blocked', 'sp-field-severity--low'))"
        }
      }
    ]
  }
}
```

---

## Pattern: Tile / Gallery View

Uses the tile schema for a grid of cards — great for document libraries and link lists.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/tile-formatting.schema.json",
  "height": 250,
  "width": 280,
  "fillHorizontally": true,
  "formatter": {
    "elmType": "div",
    "style": {
      "display": "flex", "flex-direction": "column",
      "height": "100%", "border-radius": "8px",
      "overflow": "hidden", "border": "1px solid #ededed"
    },
    "children": [
      {
        "elmType": "filepreview",
        "attributes": { "src": "@thumbnail.medium" },
        "style": { "height": "160px", "width": "100%", "object-fit": "cover" }
      },
      {
        "elmType": "div",
        "style": { "padding": "10px", "flex-grow": "1" },
        "children": [
          { "elmType": "div", "txtContent": "[$FileLeafRef]", "style": { "font-weight": "600", "font-size": "14px" } },
          { "elmType": "div", "txtContent": "[$Editor.title]", "style": { "font-size": "12px", "color": "#605e5c" } }
        ]
      }
    ]
  }
}
```

---

## Pattern: Alternating Row Colors

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json",
  "additionalRowClass": "=if(@rowIndex % 2 == 0, 'ms-bgColor-themeLighter', '')"
}
```

---

## Pattern: Conditional Row Highlighting

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/view-formatting.schema.json",
  "additionalRowClass": "=if([$Status] == 'Blocked', 'sp-field-severity--blocked', if([$Status] == 'Done', 'sp-field-severity--good', if([$DueDate] <= @now, 'sp-field-severity--severeWarning', '')))"
}
```

---

## Pattern: Inline Action Buttons

Buttons that update field values inline without opening the edit form.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { "display": "flex", "gap": "8px" },
  "children": [
    {
      "elmType": "button",
      "txtContent": "Approve",
      "style": { "background-color": "#107c10", "color": "white", "border": "none", "padding": "4px 12px", "border-radius": "4px", "cursor": "pointer" },
      "customRowAction": {
        "action": "setValue",
        "actionInput": { "Status": "Approved", "ApprovedBy": "@me" }
      }
    },
    {
      "elmType": "button",
      "txtContent": "Reject",
      "style": { "background-color": "#a4262c", "color": "white", "border": "none", "padding": "4px 12px", "border-radius": "4px", "cursor": "pointer" },
      "customRowAction": {
        "action": "setValue",
        "actionInput": { "Status": "Rejected" }
      }
    }
  ]
}
```

---

## Pattern: Grouped KPI Dashboard (headerFormatter)

Color-coded group headers with item count and aggregate data.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json",
  "groupProps": {
    "headerFormatter": {
      "elmType": "div",
      "style": {
        "display": "flex", "align-items": "center", "padding": "8px 16px",
        "border-radius": "4px", "margin-bottom": "4px"
      },
      "attributes": {
        "class": "=if(@group.fieldData.displayValue == 'Blocked', 'sp-field-severity--blocked', if(@group.fieldData.displayValue == 'Done', 'sp-field-severity--good', 'sp-field-severity--low'))"
      },
      "children": [
        { "elmType": "div", "txtContent": "@group.fieldData.displayValue", "style": { "font-weight": "bold", "flex-grow": "1" } },
        { "elmType": "div", "txtContent": "=toString(@group.count) + ' items'" }
      ]
    }
  }
}
```

---

## Pattern: Data Bar (Number Visualization)

Horizontal bar whose width represents a value relative to a max.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",
  "elmType": "div",
  "style": { "display": "flex", "align-items": "center", "gap": "8px" },
  "children": [
    {
      "elmType": "div",
      "style": {
        "background-color": "#f3f2f1", "border-radius": "3px",
        "height": "10px", "width": "120px", "overflow": "hidden"
      },
      "children": [{
        "elmType": "div",
        "style": {
          "background-color": "ms-bgColor-themePrimary",
          "height": "100%",
          "width": "=toString((@currentField / 100) * 100) + '%'"
        }
      }]
    },
    { "elmType": "span", "txtContent": "=toString(@currentField)" }
  ]
}
```
