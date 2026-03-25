# PTO Tracker — Step 3: Home Page
> Navigate to the site home page and open it in Edit mode.
> Use the SharePoint page editing experience (Viva Connections / page canvas).
> This is NOT a RALPH loop — paste this as a single instruction to the page AI.

---

## THE PROMPT

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

---

## ✅ Done when
- Page has a visible hero with "PTO Tracker" title
- Both quick action buttons are present
- Team Calendar and My Requests views are embedded
- Manager panel shows pending count
- Page is published
