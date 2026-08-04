# Transaction Pivot: 30,000 Items

**Shape:** One flat list with no relationships.

**Point:** Page through the list once, hold the records in the browser, and re-pivot all 30,000 records without another server round trip.

Unlike the other demos, this one assumes the Transactions list already exists.

## Step 1: Check the Data

Before presenting, determine:

- Whether expenses are negative or every Amount is positive.
- Whether Tags is comma-delimited, semicolon-delimited, or freeform.

If Tags is freeform prose, remove it from the dashboard's dimension choices.

## Step 2: Inspect and Prepare the List

```text
Look at the Transactions list on this site and tell me its exact internal column names, its total item count, and the earliest and latest values in the Date column. Then report which columns are indexed.

Add indexes to the Date column, the Category column, and the Merchant column if they are not already indexed.

Also tell me whether Amount contains negative values and whether Tags appears comma-delimited, semicolon-delimited, or freeform.

Do not change any data, do not add or remove columns, and do not create any views.
```

Verify the item count and internal names before building the page.

## Step 3: Build the Dashboard

```text
Build a single HTML live-linked page on this site that reads the full Transactions list and lets someone pivot across all thirty thousand records interactively. The interaction has to feel instant once the data is in.

How it loads. Read the list in pages, requesting only these columns and no others: Transaction ID, Date, Category, Subcategory, Merchant, Amount, Payment Method, Status and Tags. Do not request Description, and do not request Created, Modified, Created By or Modified By.

Hold every record in memory in the browser after loading and do all filtering, grouping, and aggregation there. Never go back to the list to answer a pivot — one read, then everything is local.

Show the load happening rather than hiding it behind a spinner. Display a running count of records loaded against the total, and let the dashboard render and remain usable while pages are still arriving. A viewer should watch the number climb past five thousand and keep going.

How amounts work. Before rendering, check whether Amount contains negative values. If it does, negatives are money out and positives are money in. If everything is positive, infer direction from Category, treating income, salary, refund, transfer in, interest, and dividend as money in and everything else as money out. State which convention was detected in small type in the footer.

Art direction. The visual world is banknote engraving and ledger stock. Ground the page in a deep saturated ink green — a real color, not a neutral dark — with type in warm bone cream. Structure is fine cream hairlines, never boxes or borders. A single copper accent is spent only on money coming in, so the page reads as a field of green outflow with occasional copper. No red anywhere and no green-to-red spectrum.

Typography. Headline figures use a high-contrast serif with the authority of a banknote denomination — Playfair Display or Fraunces, falling back to any high-contrast serif. Every other figure uses monospace with tabular figures. Labels are small, uppercase, widely tracked, and cream at reduced opacity.

The main element is a spend river that re-splits on demand. Make it full width: a stacked area chart of spending over the entire date range, split by the currently selected dimension. Above it, provide dimension controls for Category, Subcategory, Merchant, Payment Method, and Tags. Clicking a different dimension re-splits the river, and the bands animate from the old shape into the new rather than cutting. Cap the split at the top eight values by total with an Everything else band.

Dragging across the river selects a time window that filters everything else immediately. Dragging outside clears it.

Below, add a pivot grid. Let the user choose one row dimension and one column dimension from the same list, with the cell value switchable between total amount, transaction count, and average amount. Keep it dense and monospaced with no cell borders. Use alignment and a subtle green-value ramp to carry magnitude. Include row and column totals. Cap at the top twenty-five rows with an Everything else row. Clicking a column header sorts by it. Clicking a cell drills through to the underlying transactions in a panel showing merchant, date, and amount.

Add filters down the side, collapsing above the grid on narrow screens: Status, Payment Method, and a text box matching Merchant as the user types. Every filter applies instantly across all records and updates the visible record count. Show Clear all only while something is filtered.

Across the top, show three engraved figures reflecting the current filters and time selection: total out, total in, and net. Animate the digits when the selection changes.

Performance floor. Typing in the Merchant filter must stay smooth against thirty thousand records — debounce it and never re-render the whole grid per keystroke. Make the pivot grid navigable by arrow keys. Reduced-motion makes the river re-split instantly instead of animating. At phone width, keep the river full-bleed and let the grid scroll horizontally with row labels pinned. If loading fails partway, keep what arrived, say how many records are missing, and offer to retry.

Build this as a single HTML file with all script inline. Never use an external script file, never reference a CDN, and never modify the script tag or its attributes — leave whatever the sandbox emits exactly as it is.

Never scale, stretch, or compress text to fit a container. Every label is set at a fixed size and takes the width it takes.

Fit all content within the available width. No horizontal scrolling anywhere except the explicitly allowed phone-width pivot grid.

No emoji. No default SharePoint blue. No gradient fills, no floating white cards, no drop shadows, no rounded corners beyond a couple of pixels.

Respect reduced-motion settings. Every interactive element is keyboard reachable with a visible focus state. Show an honest loading state while the list is being read, and if it comes back empty, name the list and the views that depend on it.
```

## Step 4: Add Focus-Based Refreshing

Do not add a 60-second interval for this demo.

```text
Add automatic refreshing when the page becomes visible again after being in a background tab. Keep the manual refresh control.

A refresh re-reads the Transactions list in pages and updates the view in place — it must not reload the page, reset the current filters, time selection, row dimension, column dimension, or metric, or replay the initial load animation.

Show a quiet timestamp near the refresh control reading how long ago the data was last read. If a refresh fails, keep the last good data on screen, say the refresh failed and when the data is from, and offer to retry.

Do not add an interval refresh. Re-reading thirty thousand rows every sixty seconds is unnecessary.
```

## Present the Demo

1. Open on the load counter.
2. Pause as it passes 5,000 records.
3. Let it reach the complete count.
4. Switch repeatedly among dimensions and show the river reshaping instantly.
5. Change the pivot dimensions and drill into a cell.

The list-view threshold governs what the server will sort and filter in a view. It does not prevent a client from paging through the complete list. Once loaded, every pivot is local.

For architects, emphasize that requesting nine narrow columns while omitting Description and system columns dramatically reduces payload.

## Optional Automated Version

[`tools/scripts/26-transaction-pivot/26-transaction-pivot.demo`](../../../tools/scripts/26-transaction-pivot/26-transaction-pivot.demo)
