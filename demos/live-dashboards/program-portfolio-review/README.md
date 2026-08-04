# Program Portfolio Review

**Shape:** Fan-out: one parent and two independent child lists.

**Point:** The dashboard rolls up schedule and risk information that the parent list cannot see. Change a milestone to `Late`, return to the dashboard, and the program moves.

## Step 1: Create the Lists

Paste into Copilot in SharePoint:

```text
Create three lists on this site for a fictional drone company called Zava, maker of the AeroSight product line.

Create a list called Programs with these columns: Title (single line of text, the program name), Program Code (single line of text), Owner (single line of text), Phase (choice: Concept, Design, Pilot, Production, Sustaining), Target Launch (date), Budget (currency, US dollars), and Status (choice: On Track, At Risk, Critical).

Create a list called Milestones with these columns: Title (single line of text, the milestone name), Program (lookup into the Programs list, showing the Title column), Due Date (date), Actual Date (date, may be empty), Status (choice: Not Started, In Progress, Complete, Late), and Owner (single line of text).

Create a list called Risks with these columns: Title (single line of text, a short risk statement), Program (lookup into the Programs list, showing the Title column), Severity (choice: Low, Medium, High, Critical), Likelihood (choice: Low, Medium, High), Status (choice: Open, Mitigating, Closed), Opened (date), and Owner (single line of text).

Do not add any Person or Group columns anywhere. Do not add any columns beyond the ones listed.
```

## Step 2: Add Sample Data

```text
Fill these three lists with realistic sample data for Zava: 8 programs, about 55 milestones, and about 32 risks, spread so every program has at least four milestones and at least two risks.

The programs should sound like real hardware and software work at a drone company — an AeroSight Pro launch, a thermal payload module, a beyond-visual-line-of-sight certification effort, a battery generation change, a ground station refresh, an optics dual-sourcing effort. Plausible codes, ordinary first and last names for owners, target launch dates across the next fourteen months, budgets between two hundred thousand and four million dollars.

Plant these situations deliberately rather than randomizing:

- One program is genuinely in trouble: four late milestones and two open critical risks. Make this the AeroSight Pro launch.
- One program looks fine on milestones — nothing late — but carries three high-severity open risks.
- Two programs are clean: milestones on or ahead of schedule, only low-severity risks, all mitigating or closed.
- One program has a cluster of milestones all due within the same two weeks.
- The rest are a believable mix.

Completed milestones get an Actual Date near the Due Date. Late ones have an empty Actual Date and a Due Date in the past. Future ones are Not Started or In Progress. Set each program's Status to roughly match its children, but let one program's stored Status say On Track while its children say otherwise.

Write real risk statements. "Single supplier for the gimbal assembly, no qualified second source" is a risk. "Risk 12" is not.
```

Verify that Programs has 8 items and that every program has milestones and risks before continuing.

## Step 3: Build the Dashboard

```text
Build a single HTML page on this site that reads live from the Programs, Milestones and Risks lists and presents a program portfolio review. The page queries the lists on every load and never contains a copied snapshot — edit a milestone in the list, reload, and the page changes.

Art direction. The visual world is an aviation sectional chart: pale, cool, technical paper. Ground the page in a very light blue-grey, not white and not cream. Draw structure with hairlines in a muted violet. Reserve one signal color — amber into red — exclusively for schedule and risk pressure. Nothing else on the page is warm.

Typography. Condensed grotesque for headings and labels, in the spirit of chart annotation — Archivo Narrow or Oswald, falling back to any condensed sans. Clean humanist sans for body. Tabular figures everywhere so dates and dollars align.

The main element is a single shared timeline. One time axis across the top of the whole stack, running from the earliest program start to the latest target launch, with short month labels — three letters and a two-digit year — set at a fixed small size and skipped where they would collide. Draw a vertical hairline at today's date running the full height of the stack, with its small label at the top of that line.

Give each program one row. Draw one thin horizontal rule spanning that program's start to its target launch, positioned against the shared axis. Plot each milestone as a small square of uniform size sitting on the rule, by due date: filled dark for complete, hollow for not started or in progress, amber for late. Plot each open risk as a small triangle of uniform size just below the rule, by the date it was opened, amber for critical and high, neutral for medium and low. Where marks would collide, nudge them vertically so each stays distinct.

No vertical scale of any kind. A row is a line with marks on it. No background washes on rows, no ellipses, no hatched fills.

At the right end of each row, print late milestones and open critical risks in small tabular type. Sort rows so programs with the most late milestones come first, and re-run that sort on every refresh.

Add a small horizontal legend beneath the axis: filled square means complete, hollow square means not started or in progress, amber square means late, amber triangle means open high or critical risk, grey triangle means open medium or low risk.

Below the timeline, place two panels side by side, top-aligned, each only as tall as its content.

The left panel is a portfolio table: program name, stored status, late milestones, open critical, open high, budget. Fit every column within the available width. Make the name column wide enough for the longest name on one or two lines and keep numeric columns narrow with right-aligned tabular figures. No horizontal scrollbar.

The right panel is an open risk grid, severity down and likelihood across, ordered Critical, High, Medium, Low from top to bottom and Low, Medium, High from left to right. Each cell shows a count in the heading face, with its background tinted light to heavy by that count. Empty cells show nothing, not zero. The grid never grows taller than the table beside it. Selecting a cell fills a panel beneath the grid with the full risk statements in that cell, each labelled with its program. Selecting the same cell again clears it.

Across the top, show four figures computed from the children rather than stored: programs behind schedule, late milestones across the portfolio, open critical risks, and total budget in the At Risk and Critical programs. Only pressure figures take the accent color; the budget total is neutral.

Keep the page heading small enough that the heading, summary figures, and at least seven program rows are visible without scrolling. Metadata under each program title — owner, phase, start, launch, status — sits on one line at a small size, fully inside its row.

Build this as a single HTML file with all script inline. Never use an external script file, never reference a CDN, and never modify the script tag or its attributes — leave whatever the sandbox emits exactly as it is.

Never scale, stretch, or compress text to fit a container. Every label is set at a fixed size and takes the width it takes.

Fit all content within the available width. No horizontal scrolling anywhere on the page.

No emoji. No default SharePoint blue. No gradient fills, no floating white cards, no drop shadows, no rounded corners beyond a couple of pixels.

Respect reduced-motion settings. Every interactive element is keyboard reachable with a visible focus state. Show an honest loading state while lists are being read, and if a list comes back empty, name which one and what depends on it.
```

## Step 4: Add Refreshing

Use a separate turn:

```text
Add automatic refreshing. Re-read the Programs, Milestones and Risks lists whenever the page becomes visible again after being in a background tab, and also on a sixty-second interval while in the foreground. Keep the manual refresh control.

A refresh re-reads the data and updates the view in place — it must not reload the page, reset the current selection or filters, or replay the load animation. Only figures whose values changed should animate. Re-run the program sorting on every refresh, not just on first load.

Show a quiet timestamp near the refresh control reading how long ago the data was last read. If a refresh fails, keep the last good data on screen, say the refresh failed and when the data is from, and retry at the next interval.
```

## Present the Demo

1. Open Milestones in a second tab.
2. Change a milestone on a clean program to `Late`.
3. Return to the dashboard.
4. Show that the program re-sorts toward the top.

Nothing stores “this program is behind.” The dashboard computes it from the children on every read.

For a technical audience, explain that the page reads each list once and joins them in the browser by program. A single expanded query across both child lists would multiply rows.

## Optional Automated Version

[`tools/scripts/23-program-portfolio-review/23-program-portfolio-review.demo`](../../../tools/scripts/23-program-portfolio-review/23-program-portfolio-review.demo)
