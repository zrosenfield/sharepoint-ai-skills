---
name: log-client-activity
description: Turns meeting notes, an email or a quick note into a Client Activity entry with the right client, type, summary, follow-up and sentiment. Use for "log this", "log a call with Woodgrove Bank", "add these notes to Woodgrove Bank", "we just agreed X with Woodgrove Bank", or when someone pastes notes and names a client.
---

# Log client activity

Write to the **Client Activity** list (Lists/ClientActivity on this site). Client is a lookup to **Clients** (Lists/Clients).

## Steps
1. **Client.** Find the client in Clients.Title. Resolve the lookup value before writing. If the client is unclear or matches more than one row, ask.
2. **Type (ActivityType)**, using exactly one of these:
   - Meeting or Call for a conversation.
   - Email for written correspondence.
   - **Decision** when the notes record an agreement ("agreed", "decided", "approved").
   - **Change** for a configuration or environment change (upgrade, enabled, deployed, raised a limit).
   - **Issue** for an incident, defect or outage.
3. **Date (ActivityDate).** Use the date in the notes, otherwise today.
4. **Summary (Title).** At most 12 words, specific, no client name, e.g. "SSO cutover moved to Dec 5 rehearsal".
5. **Notes.** 2 to 4 plain sentences. Keep names, numbers, dates and asks; drop pleasantries.
6. **Owner.** The current user unless the notes name someone on our team. Resolve the person before writing.
7. **Follow-up.** If the notes contain something we owe the client:
   - Set FollowUp = Open and NextStep to at most 10 words, starting with a verb.
   - Set NextStepDue from the notes. Resolve relative dates such as "Friday" against today. If there is no date, use 5 business days from today and say so.
   - Otherwise set FollowUp = None. If the notes close an earlier open follow-up for this client, offer to mark that one Done.
8. **Sentiment.**
   - Positive: the client is pleased, thankful or enthusiastic.
   - Concerned: the client is worried, frustrated, escalating, evaluating alternatives or at risk.
   - Neutral: anything else.
9. **TicketLink.** Fill it if the notes contain a ticket number or URL.

## Before writing
Show a one-row preview (Client, Type, Date, Summary, Follow-up, Next step, Due, Sentiment) and create the item after the user confirms. If the notes describe two separate activities, preview two rows.

## After writing
- Reply with a link to the new item. Remind the user it appears on Client 360 after a refresh.
- If the entry is Concerned and the client's Health is On track, suggest reviewing Health. Never change Health yourself.
