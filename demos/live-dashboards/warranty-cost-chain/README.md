# Warranty Cost Chain

**Shape:** A four-hop chain across five lists, aggregating cost upward.

**Point:** Warranty cost per customer is not stored anywhere. It exists only after four joins and a multiplication.

## Step 1: Create the Lists

```text
Create five lists on this site for a fictional drone company called Zava, which sells AeroSight aircraft and services them under warranty.

Create a list called Customers with these columns: Title (single line of text, the customer company name), Region (choice: Pacific Northwest, Southwest, Mountain, Midwest), Contract Tier (choice: Standard, Premium, Enterprise), and Customer Since (date).

Create a list called Fleet Units with these columns: Title (single line of text, the tail number), Customer (lookup into the Customers list, showing the Title column), Model (choice: AeroSight One, AeroSight Pro, AeroSight Max), In Service (date), Flight Hours (number), and Retired (yes/no).

Create a list called Parts Catalog with these columns: Title (single line of text, the part name), Part Number (single line of text), Unit Cost (currency, US dollars), and Category (choice: Airframe, Battery, Optics, Avionics, Propulsion).

Create a list called Service Tickets with these columns: Title (single line of text, a short fault description), Fleet Unit (lookup into the Fleet Units list, showing the Title column), Opened (date), Closed (date, may be empty), Category (choice: Airframe, Battery, Optics, Avionics, Software), and Under Warranty (yes/no).

Create a list called Parts Used with these columns: Title (single line of text), Ticket (lookup into the Service Tickets list, showing the Title column), Part (lookup into the Parts Catalog list, showing the Title column), and Quantity (number).

Do not add any Person or Group columns anywhere. Do not add any columns beyond the ones listed.
```

## Step 2: Add Sample Data

```text
Fill these five lists with realistic sample data: 6 customers, 16 fleet units, 12 catalog parts, 28 service tickets, and about 42 parts-used records.

Create six customers that fly survey drones: a survey and mapping firm, a utility, a logistics operator, a forestry company, an infrastructure inspection contractor, and an agricultural services group. Use regions, tiers, and start dates across the last five years.

Use realistic tail numbers in a consistent format, assigned unevenly so one customer holds a large fleet and one holds a single aircraft. Use flight hours between two hundred and four thousand.

Use twelve parts that actually fail on a drone: main rotor arm, generation-three battery pack, optics gimbal assembly, thermal sensor module, GPS and inertial board, landing gear set, electronic speed controller, airframe shell, propeller set, payload mount, avionics harness, and cooling fan. Use unit costs from about forty dollars to about four thousand.

Plant these situations deliberately rather than randomizing:

- The survey and mapping firm has repeated battery failures on its AeroSight Pro units: eight battery-category tickets across four aircraft, all under warranty. This must become the largest cost path by a wide margin.
- One aircraft is a problem child with five tickets while its fleetmates have one or none.
- AeroSight Max units are visibly cleaner than Pro units.
- Leave three Parts Used rows with the Part lookup deliberately empty.
- Mark two fleet units Retired but leave their tickets in place.

Write real fault descriptions. "Battery pack swelling detected during preflight" is a ticket title. "Ticket 14" is not. Use Opened dates across the last eighteen months, close most tickets within two to twenty days, and leave four open.
```

## Step 3: Build the Dashboard

```text
Build a single HTML live-linked page on this site that reads from Customers, Fleet Units, Parts Catalog, Service Tickets and Parts Used and answers one question: where is warranty cost actually going. Every figure is computed by joining parts to tickets to fleet units to customers and multiplying quantity by unit cost — none of it is stored. The page queries on every load and never contains a copied snapshot.

Art direction. The visual world is a parts catalog and an exploded assembly drawing: precise, technical, printed. Ground the page in a very pale warm grey, the tone of good manual stock. Everything structural is a true hairline in graphite. Oxide red is the single accent, spent only on cost concentration. Nothing decorative gets color.

Typography. Headings use a mechanical, slightly squared sans — Space Grotesk, falling back to any geometric sans. Use monospace for every part number, tail number, and currency figure, with tabular figures so money aligns to the digit. Labels are small, uppercase, and widely tracked, like callouts on a drawing.

The main element is a cost flow reading left to right across four stages: part category, ticket category, aircraft model, customer. Ribbon thickness represents dollars. Hovering or focusing any ribbon isolates that path end to end, dims everything else, and prints the exact dollar figure and ticket count in a callout with a leader line. The battery-to-survey-firm path should be unmistakably the fattest ribbon and findable in about a second.

Ribbons vary in weight and in how much oxide red they carry, never in hue. No rainbow category palettes and no pie charts.

Below the flow, place two dense tables. The first ranks fleet units by total warranty cost with tail number, customer, model, flight hours, ticket count, and cost. Mark retired aircraft with a struck-through tail number rather than a badge. The second ranks customers by cost per flight hour.

Add a quiet footnote panel at the bottom that reports the data-integrity gaps honestly: how many Parts Used records have no catalog part and therefore carry no cost, and how much cost is attributed to retired aircraft. Style it as a note on the drawing, not an error.

Across the top, show three figures in large mechanical type: total warranty cost, cost per flight hour across the fleet, and the share of total cost carried by the worst customer.

Animate the ribbons drawing once on load, left to right, and nothing else. At phone width, degrade the flow to a stacked readable form rather than shrinking it into illegibility.

Build this as a single HTML file with all script inline. Never use an external script file, never reference a CDN, and never modify the script tag or its attributes — leave whatever the sandbox emits exactly as it is.

Never scale, stretch, or compress text to fit a container. Every label is set at a fixed size and takes the width it takes.

Fit all content within the available width. No horizontal scrolling anywhere on the page.

No emoji. No default SharePoint blue. No gradient fills, no floating white cards, no drop shadows, no rounded corners beyond a couple of pixels.

Respect reduced-motion settings. Every interactive element is keyboard reachable with a visible focus state. Show an honest loading state while lists are being read, and if a list comes back empty, name which one and what depends on it.
```

## Step 4: Add Refreshing

```text
Add automatic refreshing. Re-read Customers, Fleet Units, Parts Catalog, Service Tickets and Parts Used whenever the page becomes visible again after being in a background tab, and also on a sixty-second interval while in the foreground. Keep the manual refresh control.

A refresh re-reads the data and updates the view in place — it must not reload the page, reset the current selection, or replay the load animation. Recalculate every join, cost, ranking, and integrity note on every refresh.

Show a quiet timestamp near the refresh control reading how long ago the data was last read. If a refresh fails, keep the last good data on screen, say the refresh failed and when the data is from, and retry at the next interval.
```

## Present the Demo

1. Ask where warranty cost per customer is stored. It is not.
2. Hover or focus the fattest ribbon.
3. Show batteries, one customer, one model, and the exact dollar impact.
4. Point out the uncoded parts and retired-aircraft cost note.

For architects, explain that lookup columns work only within one site. If Parts Catalog lived elsewhere, the page could join by part number instead.

## Optional Automated Version

[`tools/scripts/25-warranty-cost-chain/25-warranty-cost-chain.demo`](../../../tools/scripts/25-warranty-cost-chain/25-warranty-cost-chain.demo)
