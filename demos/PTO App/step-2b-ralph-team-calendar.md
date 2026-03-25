# PTO Tracker — Step 2b: RALPH Loop for Team Calendar List
> Navigate to the Team Calendar list, open the SharePoint AI chat, and paste this prompt.
> Run this after Step 2a is complete — sample data here must mirror the Approved 
> items from Time Off Requests.
> Make sure the list-formatter skill is installed on this site.

---

## THE PROMPT

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

   This must exactly reflect the Approved rows in Time Off Requests — 
   the Team Calendar is the source of truth for who is actually confirmed out.

CONSTRAINTS:
- No code
- No People/Person column types
- All name fields are single line of text
- Do not modify the list columns — they already exist

FINAL OUTPUT WHEN COMPLETE:
1. Confirmation of views, formatting, skill, and sample data
2. One demo prompt showcasing the Check Team Availability skill
```

---

## ✅ Done when
- Calendar view and formatted list view both exist
- Rows are color-coded by department
- "Check Team Availability" skill is created
- 5 sample data rows are populated, matching Approved items in Time Off Requests
