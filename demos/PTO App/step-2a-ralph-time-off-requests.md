# PTO Tracker — Step 2a: RALPH Loop for Time Off Requests List
> Navigate to the Time Off Requests list, open the SharePoint AI chat, and paste this prompt.
> The list must already exist (created in Step 1) before running this.
> Make sure the list-formatter skill is installed on this site.

---

## THE PROMPT

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

---

## ✅ Done when
- Both views exist and are visibly formatted
- Approval workflow is active
- 3 skills are created and invocable by name
- 8+ sample data rows are in the list
