---
name: setup-client-hub
description: Sets up the Client Hub on the current site, a simple client tracker with three lists (Clients, Projects, Client Activity), their columns, views and colour formatting, and optionally fictional sample data. Use for "set up the client hub", "build the client tracker on this site" or "install the CRM lists".
---

# Set up the client hub

Build three lists on the current site, exactly as specified, so the other client hub skills and the Client 360 page work. This is an unofficial community sample, not a Microsoft template.

## Before you build
1. Check whether lists named **Clients**, **Projects** or **Client Activity** already exist on the site. If any do, stop and say which. Don't change or delete existing lists.
2. Show the plan in one short table (list, number of columns, views) and ask the user to confirm. Ask whether they want the fictional sample data too.

## Lists, in this order
Create each list with the web-address name first (no spaces), then set its display name. Rename the Title column. For every column, use the internal name exactly as written; the display name follows in brackets.

**1. Clients** (address `Clients`). Title becomes **Client**.
- ClientType [Client type]: choice of Managed services, Software
- Products [Products]: multiple choice of Digital Banking, Payments Hub, Card Issuing, Fraud Shield, Open Banking API
- Environments [Environments]: multiple choice of Production, UAT, Sandbox, DR
- Health [Health]: choice of On track, Needs attention, At risk; default On track
- RelationshipManager [Relationship manager]: person
- ImplementationManager [Implementation manager]: person
- MainContact [Main contact], ContactEmail [Contact email], ContactPhone [Contact phone]: single line of text
- AnnualValue [Annual value]: currency
- RenewalDate [Renewal date]: date only
- ServiceDesk [Service desk link]: hyperlink
- About [About]: multiple lines of text
- Views: **All clients** (default, A to Z), **Portfolio** (gallery, Health then Annual value largest first), **Renewals** (Renewal date ascending)

**2. Projects** (address `Projects`). Title becomes **Project**.
- Client [Client]: lookup to Clients, showing Client; required
- ProjectType [Type]: choice of Implementation, Migration, Upgrade, Enhancement
- Status [Status]: choice of Not started, In progress, Blocked, Done; default Not started
- Owner [Owner]: person
- Team [Team]: choice of Implementation, Engineering, Security, Infrastructure
- StartDate [Start date], DueDate [Target date]: date only
- NextMilestone [Next milestone]: single line of text
- Views: **All projects** (default, Target date ascending), **Board** (board grouped by Status), **Due in 30 days** (Status not Done and Target date within 30 days), **Migrations** (Type = Migration)

**3. Client Activity** (address `ClientActivity`, display name **Client Activity**). Title becomes **Summary**.
- Client [Client]: lookup to Clients, showing Client; required
- ActivityType [Type]: choice of Meeting, Call, Email, Decision, Change, Issue
- ActivityDate [Date]: date only; default today
- Notes [Notes]: multiple lines of text
- Owner [Owner]: person
- FollowUp [Follow-up]: choice of None, Open, Done; default None
- NextStep [Next step]: single line of text
- NextStepDue [Due]: date only
- TicketLink [Ticket link]: hyperlink
- Sentiment [Sentiment]: choice of Positive, Neutral, Concerned
- Views: **Timeline** (default, Date newest first), **Open follow-ups** (Follow-up = Open, Due ascending), **My follow-ups** (Follow-up = Open and Owner = me), **Decision log** (Type = Decision, newest first)

## Formatting
Give the choice columns coloured pills: green for On track, Done and Positive; blue for In progress; amber for Needs attention and Open; red for At risk, Blocked and Concerned; grey for everything else. Colour the Due date red when it has passed and Follow-up is still Open.

## Sample data (only if the user said yes)
Add 3 fictional clients (Woodgrove Bank, Fabrikam Payments, Contoso Credit Union), 1 or 2 projects each, and 3 or 4 activity entries each, including at least one overdue open follow-up and one Decision. Never use real company or person names.

## When you're done
List what was created, with links, and say what's left to do by hand: the Mark done quick step, a reminder on Due, the "Log client activity" form, and the Client 360 page. The manual instructions are in SETUP.md in the Client Hub solution kit. Do not execute deployment code from this skill.
