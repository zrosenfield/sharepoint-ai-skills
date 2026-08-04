# Crew Certification Coverage

**Shape:** Many-to-many through a junction list, plus a multi-value lookup.

**Point:** SharePoint has no native many-to-many field. A junction list stores the relationships and the dashboard pivots them into a matrix that no normal list view can render.

## Step 1: Create the Lists

```text
Create four lists on this site for a fictional drone company called Zava, which flies AeroSight aircraft on commercial contracts.

Create a list called Crew with these columns: Title (single line of text, the crew member's full name), Crew ID (single line of text), Base (choice: Portland, Reno, Tucson, Boise), Role (choice: Pilot, Visual Observer, Maintenance Tech, Instructor), and Active (yes/no).

Create a list called Certifications with these columns: Title (single line of text, the certification name), Code (single line of text), Category (choice: Regulatory, Platform, Payload, Safety), and Renewal Months (number).

Create a list called Crew Certifications with these columns: Title (single line of text), Crew Member (lookup into the Crew list, showing the Title column), Certification (lookup into the Certifications list, showing the Title column), Earned (date), Expires (date), and Level (choice: Certified, Instructor). This list is the link between the other two — one row means one person holds one certification.

Create a list called Missions with these columns: Title (single line of text, the mission name), Customer (single line of text), Mission Date (date), Base (choice: Portland, Reno, Tucson, Boise), Required Certifications (lookup into the Certifications list showing the Title column, allowing multiple values), and Status (choice: Scheduled, Staffed, At Risk).

Do not add any Person or Group columns anywhere. Do not add any columns beyond the ones listed.
```

## Step 2: Add Sample Data

```text
Fill these four lists with realistic sample data: 18 crew members, 10 certifications, about 58 crew certification records, and 12 missions.

The ten certifications should be what a commercial drone operator actually tracks — a remote pilot certificate, a beyond-visual-line-of-sight waiver endorsement, night operations, a thermal payload qualification, a LiDAR payload qualification, type ratings for two AeroSight airframes, battery handling and safety, field maintenance level two, and an instructor endorsement. Use short codes and renewal intervals between twelve and thirty-six months.

Spread eighteen crew across the four bases with ordinary names — mostly pilots, a few visual observers, three maintenance techs, and two instructors.

Title each crew certification row as the person's name, a middle dot, and the certification name. Set Expires by adding the renewal interval to Earned.

Plant these situations deliberately rather than randomizing:

- Tucson has six certifications expiring within the next forty-five days, including two beyond-visual-line-of-sight endorsements.
- Exactly one mission cannot be staffed because nobody at its base holds every required certification. Give it Status At Risk and a date about five weeks out.
- Two crew are one certification short of that mission.
- One certification is held by only a single person company-wide.
- That person's certification expires shortly after the mission date.
- Instructors have broad coverage, so the matrix has dense rows against sparse ones.

The remaining missions are Scheduled or Staffed across the next four months, each requiring two to four certifications. Use real customer scenarios such as a utility transmission-line inspection, forestry survey, or port logistics scan.
```

Before continuing, open the Crew Certifications list and show that each row is only one relationship.

## Step 3: Build the Dashboard

```text
Build a single HTML live-linked page on this site that reads from the Crew, Certifications, Crew Certifications and Missions lists and answers one question: who can we put in the air. The page queries the lists on every load and never contains a copied snapshot.

Art direction. The visual world is a hangar operations board under working light: a deep desaturated slate ground, information sitting on it as dense marks rather than floating cards. Pale bone white for text, muted steel blue for structural lines. Exactly one warm color — sodium-lamp amber — spent only on expiry pressure. Missing coverage is not a color at all; it is an empty cell.

Typography. Headings in an extended or wide sans — Archivo Expanded, falling back to any wide sans or a grotesque with wide letter spacing. Monospace for every axis label and every date. Quiet body face.

The main element is the coverage matrix, full width. Crew run down the rows and certifications across the columns. Held certifications render as large solid marks close to filling their cell. Instructor level shows as a mark with a ring around it. Missing is empty space. Do not draw cell borders; alignment carries the grid.

Amber is binary, not a ramp: a cell is neutral or amber, and amber means the certification expires within sixty days.

Group rows by base, each base under a full-width header set in the heading face with a hairline rule beneath it. Show a count of expiring certifications next to each base header and hide that count when it is zero. Tint a crew member's name amber when any of their certifications expire within sixty days, and use name brightness for nothing else. Mark instructors with a small typographic marker after their role.

Certification column headers are abbreviations. Show the full certification name on hover and keyboard focus.

Give the name and role column enough width for the longest role without truncating, and fit the matrix to the available width so the last certification column is never clipped.

Above the matrix, show the twelve missions as a horizontal strip. Hovering or focusing a mission dims every certification column it does not require and every crew row that fails to qualify. The unstaffable mission should make the board go nearly dark.

Beside the matrix, or below it on narrow screens, show certifications expiring in the next sixty days, soonest first, and every certification held by only one person labelled as a single point of failure. When a mission is selected, add a panel naming the crew who are one certification short and which certification they are missing.

Do not use a red-amber-green palette. Keep the matrix legible at eighteen rows by ten columns without horizontal scrolling on a laptop. On a phone, allow horizontal scrolling with crew names pinned. Animate the matrix filling once on load, sweeping left to right, and animate nothing else. If Crew Certifications is empty, say so and explain that it is the list connecting crew to certifications.

Build this as a single HTML file with all script inline. Never use an external script file, never reference a CDN, and never modify the script tag or its attributes — leave whatever the sandbox emits exactly as it is.

Never scale, stretch, or compress text to fit a container. Every label is set at a fixed size and takes the width it takes.

Fit all content within the available width. No horizontal scrolling anywhere on the page except the explicitly allowed phone-width matrix.

No emoji. No default SharePoint blue. No gradient fills, no floating white cards, no drop shadows, no rounded corners beyond a couple of pixels.

Respect reduced-motion settings. Every interactive element is keyboard reachable with a visible focus state. Show an honest loading state while lists are being read, and if a list comes back empty, name which one and what depends on it.
```

## Step 4: Add Refreshing

```text
Add automatic refreshing. Re-read the Crew, Certifications, Crew Certifications and Missions lists whenever the page becomes visible again after being in a background tab, and also on a sixty-second interval while in the foreground. Keep the manual refresh control.

A refresh re-reads the data and updates the view in place — it must not reload the page, reset the current mission selection or filters, or replay the load animation. Re-run all qualification and expiry calculations on every refresh.

Show a quiet timestamp near the refresh control reading how long ago the data was last read. If a refresh fails, keep the last good data on screen, say the refresh failed and when the data is from, and retry at the next interval.
```

## Present the Demo

1. Show the junction list first.
2. Open the matrix.
3. Select the At Risk mission.
4. Show the two people who are one certification short.
5. Highlight the single point of failure and its expiration date.

The key message: none of this operational answer is stored in one place. Four lists are joined live in the browser.

## Optional Automated Version

[`tools/scripts/24-crew-certification-coverage/24-crew-certification-coverage.demo`](../../../tools/scripts/24-crew-certification-coverage/24-crew-certification-coverage.demo)
