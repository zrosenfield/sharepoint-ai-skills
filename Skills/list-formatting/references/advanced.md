# SharePoint List Formatting — Advanced Features Reference

Actions, hover cards, inline editing, tile layouts, and other advanced capabilities. Load this when the request involves buttons, Power Automate flows, hover cards, tile/gallery views, inline editing, group header/footer formatting, or file previews.

---

## Actions (customRowAction)

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

## Custom Hover Cards (customCardProps)

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

---

## Inline Editing (inlineEditField)

Make a field editable directly in the view:
```json
{
  "elmType": "div",
  "inlineEditField": "[$FieldName]",
  "txtContent": "[$FieldName]"
}
```

---

## Column Formatter Reference (columnFormatterReference)

Reuse another column's formatter:
```json
{
  "columnFormatterReference": "[$FieldName]"
}
```

---

## File Preview (filepreview)

Show document thumbnails in libraries:
```json
{
  "elmType": "filepreview",
  "attributes": { "src": "@thumbnail.medium" },
  "style": { "width": "100%", "height": "150px" }
}
```

---

## Default Hover Field

Show profile cards for people or file hover cards:
```json
{
  "defaultHoverField": "[$Editor]"
}
```

---

## Tile Layout (tileProps)

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

## Group Header/Footer Formatting

Use `groupProps` in a view formatter to style grouped view headers and footers.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/sp/v2/row-formatting.schema.json",
  "groupProps": {
    "hideFooter": false,
    "headerFormatter": {
      "elmType": "div",
      "style": { "display": "flex", "align-items": "center", "padding": "8px" },
      "children": [
        { "elmType": "div", "txtContent": "@group.fieldData.displayValue", "style": { "font-weight": "bold" } },
        { "elmType": "div", "txtContent": "=toString(@group.count) + ' items'" }
      ]
    },
    "footerFormatter": {
      "elmType": "div",
      "txtContent": "=@columnAggregate.columnDisplayName + ': ' + toString(@columnAggregate.value)"
    }
  }
}
```

Group tokens:
- `@group.fieldData` — the field value being grouped on
- `@group.fieldData.displayValue` — human-readable display value
- `@group.count` — number of items in the group
- `@aggregates` — array of column aggregates
- `@columnAggregate.type` — aggregate function name (in footerFormatter)
- `@columnAggregate.value` — aggregate result
- `@columnAggregate.columnDisplayName` — column display name
