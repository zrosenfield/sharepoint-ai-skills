---
name: weekly-client-review
description: Runs the Monday portfolio review across every client, covering value needing attention, overdue and this-week follow-ups, blocked or due-soon projects, renewals in the next 90 days, clients gone quiet and clients who sounded concerned. Use for "Monday review", "what needs attention?", "portfolio status", "who needs me this week?" or "my follow-ups".
---

# Weekly client review

Read the three lists live: **Clients** (Lists/Clients), **Projects** (Lists/Projects) and **Client Activity** (Lists/ClientActivity). Read every row, not just the first page. Today's date is the reference.

## Facts to compute
1. **Value needing attention:** the sum of AnnualValue where Health is not On track, with those clients.
2. **Overdue follow-ups:** Client Activity where FollowUp = Open and NextStepDue is before today, oldest first.
3. **Due in the next 7 days:** FollowUp = Open and NextStepDue from today to today + 7.
4. **Projects:** every Blocked project, plus projects that are not Done with a DueDate within 30 days.
5. **Renewals:** clients with a RenewalDate within 90 days.
6. **Gone quiet:** clients whose newest ActivityDate is more than 60 days ago.
7. **Concerned:** clients with at least one Concerned entry in the last 30 days.

If the user says "my" or "me", keep only follow-ups where Owner is the current user, and clients where they are the relationship or implementation manager.

## Answer format
**Portfolio, {today}:** {n} clients · {total annual value} · {value needing attention} needs attention ({clients})
**Overdue ({n}):** {NextStep}, {Client}, {Owner}, due {date} ({k} days late)
**This week ({n}):** {NextStep}, {Client}, {Owner}, due {date}
**Projects to watch:** {Status} · {Project} ({Client}) · target {date} · next: {NextMilestone}
**Renewals in 90 days:** {Client}, {date}, {Health}
**Gone quiet:** {Client}, last contact {date}
**Sounded concerned:** {Client}: the latest concerned summary
**Top 3 actions this week:** three bullets based only on the facts above, most urgent first.

## Rules
- Every number comes from the lists. Show "none" for an empty section rather than leaving it out.
- Link items you name (DispForm.aspx?ID=).
- Keep it scannable: one line per item, and no more than 8 lines per section (then "+N more").
