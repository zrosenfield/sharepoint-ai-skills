# AI-Powered PTO Tracker in SharePoint

This demo shows how to build a fully functional PTO Tracker solution in SharePoint using AI — two structured lists, approval workflows, color-coded views, custom AI skills, and a polished home page, all created through natural language prompts.

The scenario: starting from a blank SharePoint site, the AI agent builds a complete time-off management solution step by step — no manual list configuration, no Power Automate flows built by hand, no page layouts assembled from scratch.

---

## Watch the Demo

[Watch on YouTube](https://youtu.be/-1k20y_lHe4)

---

## What This Demo Shows

Starting from an empty site, the AI builds:

- Two structured lists (Time Off Requests and Team Calendar) with all columns correctly typed
- An approval workflow that routes requests to the right manager and updates status automatically
- Color-coded views — by status for managers, by department for the team calendar
- Four AI skills employees and managers can invoke by name from the chat panel
- A complete set of realistic sample data across six employees and multiple departments
- A published home page with a hero, quick action buttons, embedded list views, and a pending approvals panel

---

## Demo Script

### Step 1 — Create the Lists

> Run from the site-level SharePoint AI chat.

```
Please create two lists on this site:

LIST 1: "Time Off Requests"
Columns:
- Title — rename to "Employee Name" (single line of text)
- Leave Type — choice: Vacation, Sick, Personal, Bereavement, Unpaid — default: Vacation
- Start Date — date only
- End Date — date only
- Total Days — number
- Manager — single line of text
- Department — choice: Sales, Engineering, Marketing, HR, Finance, Operations
- Status — choice: Pending, Approved, Rejected — default: Pending
- Request Notes — multiple lines of text, optional
- Manager Notes — multiple lines of text, optional

LIST 2: "Team Calendar"
Columns:
- Title — rename to "Employee Name" (single line of text)
- Department — choice: Sales, Engineering, Marketing, HR, Finance, Operations
- Out From — date only
- Out Through — date only
- Leave Type — choice: Vacation, Sick, Personal, Bereavement, Unpaid
- Coverage Contact — single line of text

Please confirm both lists are created before I move on.
```

Both lists are created empty with the correct column structure. No data or formatting yet.

---

### Step 2a — Configure the Time Off Requests List (RALPH Loop)

> Navigate to the Time Off Requests list and open the SharePoint AI chat.

```
RALPH with max 5 iterations:

GOAL: Make the Time Off Requests list on this site fully configured, beautifully
formatted, populated with realistic sample data, and ready to demo. The list structure
already exists — do not recreate columns. Focus entirely on views, formatting,
skills, sample data, and approval workflow.

SUCCESS CRITERIA — score each 1–10, do not declare complete until all are 8 or higher:

1. APPROVAL WORKFLOW
   An approval workflow is configured on this list:
   - When a new item is added with Status = Pending, an approval request is
     sent to the person named in the Manager column
   - When approved, Status updates to Approved
   - When rejected, Status updates to Rejected

2. "BY STATUS" VIEW — FORMATTED
   A view called "By Status" exists that:
   - Groups items by Status
   - Sorts within each group by Start Date ascending
   - Shows columns in this order: Employee Name, Leave Type, Start Date,
     End Date, Total Days, Department, Manager, Status
   Use the list-formatter skill to apply row-level color formatting:
   - Pending rows = yellow
   - Approved rows = green
   - Rejected rows = red
   The formatting must be applied and visible — not just described.

3. "UPCOMING" VIEW — FORMATTED
   A second view called "Upcoming" exists that:
   - Shows only Approved items with Start Dates in the next 60 days
   - Sorts by Start Date ascending, no grouping
   Use the list-formatter skill to give this view a visually distinct treatment
   from "By Status" — something that emphasizes the date range and makes
   upcoming time off easy to scan at a glance.

4. SKILLS ARE CREATED
   Create the following skills on this site:

   SKILL 1 — "Request Time Off"
   When invoked, this skill:
   - Asks the employee for their name, dates, and leave type if not already provided
   - Checks the Team Calendar list for coverage conflicts on those dates
   - Checks the Time Off Policies library for applicable notice requirements
     and blackout dates
   - Warns the employee if a conflict or policy issue exists
   - If clear, creates a new item in Time Off Requests with Status = Pending
   - Confirms the submission and states who will receive the approval request

   SKILL 2 — "Review Pending Requests"
   When invoked, this skill:
   - Queries Time Off Requests for all items where Status = Pending
   - Sorts results by Start Date ascending
   - Flags any request where Start Date is within 5 business days (short notice)
   - Flags any date overlaps between multiple pending requests in the same department
   - Returns a clean formatted summary: employee name, dates, leave type,
     department, and any flags

   SKILL 3 — "Policy Check"
   When invoked, this skill:
   - Accepts a natural language question about PTO policy
   - Reads the Time Off Policies document library on this site
   - Returns a direct plain-English answer with the relevant rule cited
   - If the answer is not found in the policy documents, says so clearly

5. SAMPLE DATA — TIME OFF REQUESTS
   The list contains at least 8 items with this data mix:
   - Employees: use these names across the data — Jordan Lee (Sales, manager: Sarah Kim),
     Morgan Chen (Marketing, manager: David Park), Alex Patel (Sales, manager: Sarah Kim),
     Taylor Kim (Marketing, manager: David Park), Sam Rivera (Engineering, manager: Rachel Torres),
     Casey Wong (Engineering, manager: Rachel Torres)
   - Leave types: mix of Vacation, Sick, Personal (at least one each)
   - Statuses: at least 3 Pending, 3 Approved, 1 Rejected
   - Dates: mix of March 2026 (past) and April–May 2026 (upcoming)
   - At least one scenario where two people from the same department have
     overlapping Pending requests during the same week — this should be
     Morgan Chen and Sam Rivera both requesting the week of April 14
   - Total Days must be correctly calculated for every row
   - At least one item has a rejection with a Manager Notes explanation

CONSTRAINTS:
- No code
- No People/Person column types
- All name fields are single line of text
- Do not modify the list columns — they already exist

FINAL OUTPUT WHEN COMPLETE:
1. Confirmation of workflow, views, formatting, and skills created
2. Full sample data as a table
3. Two demo prompts — one employee perspective, one manager perspective
```

Done when both views are visible and formatted, the approval workflow is active, 3 skills are created, and 8+ sample rows are populated.

---

### Step 2b — Configure the Team Calendar List (RALPH Loop)

> Navigate to the Team Calendar list and open the SharePoint AI chat.
> Run after Step 2a is complete.

```
RALPH with max 4 iterations:

GOAL: Make the Team Calendar list on this site fully configured, beautifully formatted,
and populated with sample data that mirrors all Approved time off from the
Time Off Requests list. The list structure already exists — focus on views,
formatting, and sample data only.

SUCCESS CRITERIA — score each 1–10, do not declare complete until all are 8 or higher:

1. "TEAM AVAILABILITY" CALENDAR VIEW
   A calendar view called "Team Availability" exists on this list:
   - Uses Out From as the start date
   - Uses Out Through as the end date
   - Displays Employee Name on each calendar event
   - Is set as the default view

2. DEFAULT LIST VIEW — FORMATTED BY DEPARTMENT
   The default list view (or a view called "By Department") exists and:
   - Shows columns in this order: Employee Name, Department, Out From,
     Out Through, Leave Type, Coverage Contact
   - Sorts by Out From ascending
   Use the list-formatter skill to color-code rows by Department:
   - Sales = blue
   - Marketing = purple
   - Engineering = teal
   - HR = orange
   - Finance = green
   - Operations = gray
   The formatting must be applied and visible — not just described.
   The result should look like a color-coded team schedule, easy to
   read at a glance.

3. SKILL — "Check Team Availability"
   Create a skill called "Check Team Availability" on this site.
   When invoked, this skill:
   - Accepts a date, week, or date range as input
     (e.g., "next week", "April 14", "the week of May 4")
   - Queries the Team Calendar list for all entries overlapping that period
   - Groups results by Department
   - Flags any department where more than one person is out simultaneously
   - Returns a plain-English summary: who is out, what dates, what department,
     and any coverage concerns

4. SAMPLE DATA — TEAM CALENDAR
   The list is populated with entries that correspond to all Approved items
   in the Time Off Requests list. Use this exact data:

   | Employee Name | Department | Out From | Out Through | Leave Type | Coverage Contact |
   |---|---|---|---|---|---|
   | Jordan Lee | Sales | 3/24/2026 | 3/27/2026 | Vacation | Alex Patel |
   | Alex Patel | Sales | 3/10/2026 | 3/11/2026 | Sick | Jordan Lee |
   | Taylor Kim | Marketing | 3/31/2026 | 3/31/2026 | Personal | Morgan Chen |
   | Casey Wong | Engineering | 3/6/2026 | 3/8/2026 | Bereavement | Sam Rivera |
   | Morgan Chen | Marketing | 3/18/2026 | 3/18/2026 | Sick | Taylor Kim |

CONSTRAINTS:
- No code
- No People/Person column types
- All name fields are single line of text
- Do not modify the list columns — they already exist

FINAL OUTPUT WHEN COMPLETE:
1. Confirmation of views, formatting, skill, and sample data
2. One demo prompt showcasing the Check Team Availability skill
```

Done when the calendar view and color-coded list view both exist, the skill is created, and 5 sample rows are populated matching the Approved items from Step 2a.

---

### Step 3 — Build the Home Page

> Navigate to the site home page and open it in Edit mode.
> This is a single prompt — not a RALPH loop.

```
Please build out this page as the home page for a PTO Tracker solution.
The site has two lists (Time Off Requests and Team Calendar) and a
Time Off Policies document library already set up.

Build the page with these sections in order:

SECTION 1 — Hero
A hero banner at the top of the page with the title "PTO Tracker" and a
subtitle: "Request time off, check team availability, and manage approvals —
all in one place." Use a clean, professional look.

SECTION 2 — Quick Actions
Two prominent buttons side by side:
- "Request Time Off" — clicking this opens the SharePoint AI chat and
  pre-fills the message "Request Time Off" to invoke that skill
- "Check Team Availability" — clicking this opens the SharePoint AI chat
  and pre-fills "Check Team Availability"

SECTION 3 — Team Calendar
An embedded view of the Team Calendar list using the "Team Availability"
calendar view so visitors can immediately see who is out.
Label this section "Team Schedule".

SECTION 4 — My Requests
An embedded view of the Time Off Requests list filtered to show only
the current user's submissions (where Employee Name = current user).
Show the "By Status" view.
Label this section "My Requests".

SECTION 5 — Manager Panel
A section labeled "Pending Approvals" that shows a count of items in the
Time Off Requests list where Status = Pending, with a button or link
labeled "Review Pending" that opens the Time Off Requests list
in the "By Status" view.

The page should look polished and intentional — clear section headings,
good spacing, not a default blank SharePoint page. Publish when complete.
```

Done when the hero, quick action buttons, embedded list views, and manager panel are all visible and the page is published.

---

## Skills Used

- **list-formatter** — required for Steps 2a and 2b. Must be installed on the site before running those prompts.

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `step-1-create-lists.md` | Prompt to create both lists with correct column structure |
| `step-2a-ralph-time-off-requests.md` | RALPH loop to configure the Time Off Requests list |
| `step-2b-ralph-team-calendar.md` | RALPH loop to configure the Team Calendar list |
| `step-3-home-page.md` | Single prompt to build and publish the home page |

---

## Prerequisites

- Microsoft 365 tenant with Copilot licenses
- SharePoint site with agent enabled
- `list-formatter` skill installed on the site before running Steps 2a or 2b
