# PTO Tracker — Step 1: Create the Lists
> Run this prompt from the site-level SharePoint AI chat.
> This creates both lists empty and correctly structured.
> Do this first, before running any of the per-list RALPH loops.

---

## THE PROMPT

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

---

## ✅ Done when
Both lists appear in site contents. No data, no views, no formatting yet — that happens in the next steps.
