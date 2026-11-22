---
name: crm-change-request
description: Changes the client hub safely when the team asks for a new field, choice value, view or report, keeping it simple (3 lists, at most 14 columns per list, at most 6 choices per column) and keeping the form and Client 360 working. Use for "add a column", "add a status", "we need to track X", "make a view for Y" or "rename Z".
---

# CRM change request

The hub's promise is "simpler than the spreadsheet". Protect that while saying yes to real needs.

## Decide first
1. **Is it already there?** Check the three lists' schemas (Clients, Projects, Client Activity). Often a view, a filter or an existing choice value solves it.
2. **Prefer the smallest change,** in this order:
   1. A new view.
   2. A new value on an existing choice column.
   3. A new column.
   4. A new list. Only for a genuinely new kind of record, and say why it can't live on an existing list.
3. **Budgets:** at most 14 custom columns per list, at most 6 choices per column, and 3 lists. If a request would break a budget, propose what to retire or combine.

## Making the change
- **New columns:** use plain-language display names and letters-only internal names. Add the column to the list's default view (the Client 360 page reads the default view's fields for lists other than Clients).
- **Choice values:** never rename or remove a value that existing rows use without updating those rows in the same change. Explain the impact first.
- **Client Activity changes:** also update the list's **Log client activity** form, if the site has one, so the new field is asked in the right place, after Owner and before Follow-up.
- **Status, priority and health columns:** give them colored pills that match the hub's palette: green for good, amber for watch, red for at risk, gray for neutral.
- **Fields to show on Client 360:** the page shows a fixed set of fields. Tell the owner the page needs a refresh from the Client Hub solution kit's dashboard template to show a new field. Do not execute deployment code from this skill.

## Confirm and report
Before changing anything, list each change with its type and values and ask for a yes. Afterwards, report what changed, with links, and what the team should do differently.
