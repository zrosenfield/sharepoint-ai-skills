---
name: client-briefing
description: Briefs users on one client in under a minute, covering health, renewal, owners, projects, open and overdue follow-ups, recent decisions and changes, and sentiment. Use for "what's going on with Woodgrove Bank?", "prep me for my call with Woodgrove Bank", "client 360 for Woodgrove Bank" or "catch me up on Woodgrove Bank".
---

# Client briefing

The client hub has three lists on this site. Always read the live lists; never answer from memory.

| List | URL on this site | Key fields (internal names) |
|---|---|---|
| Clients | Lists/Clients | Title (client), ClientType, Products, Environments, Health, RelationshipManager, ImplementationManager, MainContact, ContactEmail, ContactPhone, AnnualValue, RenewalDate, ServiceDesk, About |
| Projects | Lists/Projects | Title (project), Client (lookup), ProjectType, Status, Owner, Team, StartDate, DueDate (target date), NextMilestone |
| Client Activity | Lists/ClientActivity | Title (summary), Client (lookup), ActivityType, ActivityDate, Notes, Owner, FollowUp (None, Open or Done), NextStep, NextStepDue, TicketLink, Sentiment |

## Steps
1. **Find the client.** Match the name against Clients.Title (case-insensitive; partial names are fine). If more than one matches, show them and ask which one. If none match, say so and list the client names.
2. **Read the client row** (all key fields).
3. **Read the client's projects.** Filter Projects to rows whose Client lookup matches the resolved client. Use its actual lookup identity, not a guessed ID.
4. **Read the client's activity** with the same filter on Client Activity, sorted by ActivityDate newest first. Read every matching row, not just the first page.
5. **Work out the facts**, with today's date as the reference:
   - Overdue follow-ups: FollowUp = Open and NextStepDue before today.
   - Due this week: FollowUp = Open and NextStepDue within the next 7 days.
   - Last contact: the newest ActivityDate, and the days since then. More than 60 days means the client has gone quiet.
   - Tone: the number of Concerned entries in the last 30 days. If Sentiment is empty, judge it from the summary and notes and say you did.
   - Renewal: days until RenewalDate. Within 90 days counts as soon.

## Answer format
**{Client}** · {Health} · {ClientType} · {AnnualValue, e.g. $1.25M} · renews {Mon D, YYYY} ({in N days})
Owners: {RelationshipManager} (relationship), {ImplementationManager} (implementation) · Main contact: {MainContact}, {ContactEmail}

**Watch:** 1 to 3 bullets, most urgent first: blocked projects, overdue follow-ups, concerned tone, a renewal within 90 days, or no contact in 60+ days. If nothing needs watching, say "Nothing urgent."
**Projects:** one line each, not Done first: {Status} · {Project} · target {date} · next: {NextMilestone} · {Owner}
**Open follow-ups:** {NextStep}, {Owner}, due {date} (mark overdue ones **overdue**)
**Recent decisions and changes (last 90 days):** {date}: {summary}
**Suggested next step:** one sentence based only on the facts above.

## Rules
- Link each project and activity you mention to its item (DispForm.aspx?ID=).
- Use the field values as they are. Never invent a project, a date or a decision.
- Write dates as "Dec 5"; add the year only when it isn't the current year.
- Keep the whole briefing under 200 words unless the user asks for more.
