# Column formatting

Four Obligations columns get coloured pills: `Status`, `Timing`, `Risk` and `ReviewState`. The same colours are used on the hub pages, so keep them.

## How to build each format

Apply column formatting to the column (not a view format), replacing any existing format on that column. Build it as a column-formatting definition with:
- An outer box (a div) that is a flex row, items centred vertically, full cell height.
- One inner text element (a span) that shows the value, with an optional prefix symbol from the tables below.
- **Inline styles only** on the span: display inline-block (hidden when the value is empty), padding 2px 10px, border radius 12px, font size 12px, font weight 600, line height 18px, and the background and text colours from the tables below.
- Don't use the SharePoint `sp-css` class names. They crashed the formatter in an earlier build; inline styles worked.
- Any value not listed (including empty) falls back to background `#F1F3F6` and text `#374151`.

The colour choice is an if-chain on the current field value: for each value in the table, if the cell equals that value, use its colours; otherwise check the next value; finally use the fallback.

## Status

| Value | Prefix | Background | Text |
|---|---|---|---|
| Not started | none | `#F1F3F6` (light grey) | `#374151` (slate) |
| In progress | none | `#EAF3FC` (light blue) | `#1E3A5F` (navy) |
| Fulfilled | none | `#E6F2EC` (light green) | `#1F5135` (dark green) |
| Waived | none | `#EEECFB` (light violet) | `#3F3A8C` (indigo) |
| Not applicable | none | `#F1F3F6` (light grey) | `#374151` (slate) |

## Timing

| Value | Prefix | Background | Text |
|---|---|---|---|
| Overdue | ▲ then a space | `#FBE4EA` (light rose) | `#8A1538` (burgundy) |
| Due soon | ◑ then a space | `#FDF1D6` (light amber) | `#6B4100` (brown) |
| Upcoming | ○ then a space | `#EAF3FC` (light blue) | `#1E3A5F` (navy) |
| No date | none | `#F1F3F6` (light grey) | `#374151` (slate) |
| Closed | ✓ then a space | `#E6F2EC` (light green) | `#1F5135` (dark green) |

## Risk

| Value | Prefix | Background | Text |
|---|---|---|---|
| High | none | `#FBE4EA` (light rose) | `#8A1538` (burgundy) |
| Medium | none | `#FDF1D6` (light amber) | `#6B4100` (brown) |
| Low | none | `#E6F2EC` (light green) | `#1F5135` (dark green) |

## ReviewState (display name "Review")

| Value | Prefix | Background | Text |
|---|---|---|---|
| Needs review | ◎ then a space | `#EEECFB` (light violet) | `#3F3A8C` (indigo) |
| Confirmed | none | `#E6F2EC` (light green) | `#1F5135` (dark green) |

## Check it worked

Open the Obligations list's "Open by due date" view. Status, Timing, Risk and Review show as rounded pills in these colours. An empty cell shows nothing. If a format fails to apply, report the column and carry on; formatting is cosmetic and no skill depends on it.

The kit also ships the same four formats as ready-made column-formatting files in `solutions/obligation-hub-for-sharepoint/formats/`, for site owners who prefer to paste them in by hand.
