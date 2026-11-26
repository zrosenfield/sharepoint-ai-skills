# Column formatting

Four ready-made column formats for the **Obligations** list. They show values as rounded, coloured pills using the same colours as the hub pages. The deploy script and the Cowork job files apply them for you. Use these files only if you're setting up by hand.

| List | Column (internal name) | Display name | File | Shows |
|---|---|---|---|---|
| Obligations | `Status` | Status | [Status.json](Status.json) | Not started (grey), In progress (blue), Fulfilled (green), Waived (violet), Not applicable (grey) |
| Obligations | `Timing` | Timing | [Timing.json](Timing.json) | ▲ Overdue (rose), ◑ Due soon (amber), ○ Upcoming (blue), No date (grey), ✓ Closed (green) |
| Obligations | `Risk` | Risk | [Risk.json](Risk.json) | High (rose), Medium (amber), Low (green) |
| Obligations | `ReviewState` | Review | [ReviewState.json](ReviewState.json) | ◎ Needs review (violet), Confirmed (green) |

**To apply one by hand:** open the Obligations list, select the column header, then **Column settings > Format this column > Advanced mode**. Paste the file's contents and select **Save**.

Notes:
- They use inline styles only. An earlier build that used SharePoint's `sp-css` class names crashed the formatter.
- An empty cell shows nothing. Any value not listed falls back to grey.
- Every text and background pair meets WCAG AA contrast (4.5:1 or better).
- Formatting is cosmetic. No skill depends on it, so if a format fails to apply, the hub still works.
