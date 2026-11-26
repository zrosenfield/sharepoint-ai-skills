---
name: assign-obligation-owners
description: Gives each confirmed, open obligation on an Obligation Hub site that has no owner an owner and an escalation owner from the Obligation Owners routing rules, then sends each newly assigned owner one aggregated email or Teams message and writes one Run Log row. Use for the daily Assign owners AI workflow (7:00 AM) or when asked to "assign owners", optionally for one contract.
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Assign obligation owners

Route new, confirmed obligations to the right people, using the routing rules the site owner keeps in Obligation Owners. Runs unattended each morning or in chat.

## Inputs
- **Config** `AgentAssets/Config/hub-settings.json`: `siteUrl`, `timeZone`, `notifyDefault`. If it's missing, use the current site and the defaults, and note this in Details.
- **Obligations** where `Owner` is empty, `Status` = Not started or In progress, and `ReviewState` = Confirmed. Items held for review aren't assigned until someone confirms them. If the user names a contract, also filter on `ContractName`.
- **Obligation Owners**: all rules (`Title`, `Category`, `BusinessUnit`, `Counterparty`, `Owner`, `EscalationOwner`, `Notify`).
- **Contracts** columns `BusinessUnit` and `Counterparty`, only for the files named in the candidates' `ContractName`. Never read contract text.

## Steps
1. **Check for work.** If there are no candidates, log Succeeded with Details "No unassigned obligations" and stop.
2. **Set the business unit.** For each candidate, the business unit is the item's `BusinessUnit`, or the contract's `BusinessUnit` if the item's is empty.
3. **Pick a rule.** A rule matches when all three of these hold, and it has an `Owner`:
   - Its `Counterparty` is empty, or names the item's `Counterparty`. Ignore case and suffixes such as Inc, Ltd and LLC.
   - Its `Category` is Any or equals the item's `Category`.
   - Its `BusinessUnit` is Any or equals the item's business unit.

   The most specific match wins, in this order:
   1. Counterparty match (if there are several, the one that matches more of the other fields)
   2. Category + BusinessUnit
   3. Category
   4. BusinessUnit
   5. Any/Any

   If two rules tie, use the one with the lower ID and note it in Details.
4. **Assign.** Set `Owner` and `EscalationOwner` to the rule's people, and set `BusinessUnit` if it was empty. Resolve each person once and reuse the result. Update in one batch. If nothing matches, leave the item unassigned (it shows in Needs owner) and count it.
5. **Notify.** For each owner who was newly assigned in this run, send ONE aggregated message.
   - **Channel:** the rule's `Notify` (Email, Teams or Both). If that owner's items came from rules with different `Notify` values, use Both.
   - **Subject:** "Action required: N new obligation(s) assigned to you".
   - **Body:** one line per item: `Title` – due date (or "When: <TriggerEvent>" / "Ongoing") – `Counterparty` – `ClauseRef` – link `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`. Sort by due date; undated items go last.
   - **Close with:** "When it's done, open the item and use the Mark fulfilled quick step."
   - Teams carries the same content, shortened to the first 10 items plus a link to the list.
6. **Log.** Write one Run Log row:
   - `Title` = "Assign owners - <today>"
   - `Workflow` = Assign owners
   - `Outcome`: Succeeded; Partial if any update or message failed
   - `ItemsCreated` = 0
   - `ItemsUpdated` = items assigned
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details`: "Assigned N to M owners; K with no matching rule: <titles, up to 5>; messages: …".

In chat, reply with one line: "Assigned N obligations to M owners; K need a routing rule (see Needs owner)."

## Writes
- Obligations: `Owner`, `EscalationOwner` and `BusinessUnit` (only when empty).
- Email and Teams messages to owners assigned in this run.
- Run Log: exactly one row.

## Never
- Change an existing `Owner` or `EscalationOwner`, or assign items with `ReviewState` = Needs review.
- Message anyone about items that weren't assigned in this run.
- Edit routing rules or create people.
