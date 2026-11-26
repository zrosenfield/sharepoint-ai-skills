---
name: exclude-obligation
description: Takes one obligation on an Obligation Hub site out of tracking and records its clause, or a general pattern, in the Exclusions list so capture won't add it back, for this contract or for all contracts. Sets the item to Not applicable rather than deleting it and writes one Run Log row. Use from the Remove obligation quick step, or when asked to "remove", "exclude" or "stop tracking" an obligation.
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Exclude obligation

Teach the hub what not to track. The Exclusions list is the hub's memory: `capture-obligations` reads it on every run.

## Inputs
- **The item.** Use the Obligations item the quick step ran on. In chat, find it from what the user said, and if several match, ask which.
- **Exclusions**: rows where `Active` = Yes. For the dedupe check in step 2, also look at inactive rows.

## Steps
1. **Ask in ONE message**, skipping anything the user already answered:
   - Scope: **This contract** or **All contracts**?
   - Reason (a few words)?
   - Remove this item from tracking now, **Yes** or **No**? If No, the item stays, but future captures won't add this clause again.
2. **Dedupe.** Look for an existing exclusion with the same `Scope` (and the same `ContractName` for This contract) whose `Pattern` already covers this clause or kind of clause.
   - If an **active** match exists, reuse it and don't create a row.
   - If an **inactive** match exists, set its `Active` = Yes.
3. **Create the exclusion** if none exists, with these fields:
   - `Title` = "Exclude: <short action>"
   - `Pattern`:
     - This contract: the item's `SourceClause`, verbatim.
     - All contracts: a one-sentence generalized description of the kind of clause, followed by `Example: "<SourceClause>"`. For example: "Clauses requiring the supplier's staff to wear uniforms or badges."
   - `Reason` = the user's reason
   - `Scope` = This contract or All contracts
   - `ContractName` = the item's `ContractName` for This contract; empty for All contracts
   - `Category` = the item's `Category`
   - `Active` = Yes
4. **Remove the item** if the user said Yes. Set `Status` = Not applicable and `Timing` = Closed, and append to `Notes`: "Excluded: <reason> (<today>, <user>)". Prefer this to deleting.
   - Delete only if the user insists **and** nobody has worked on the item. That means `Owner`, `Evidence` and `FulfilledOn` are empty, `Status` was Not started, and `Notes` holds no human-written text.
   - Otherwise explain in one line why you set it to Not applicable instead.
5. **Log.** Write one Run Log row:
   - `Title` = "Exclude - #<ID>"
   - `Workflow` = Exclude
   - `Outcome` = Succeeded
   - `ContractName` = the item's contract
   - `ItemsCreated` = 1 if you created an exclusion row, otherwise 0
   - `ItemsUpdated` = items changed
   - `ItemsHeld` = 0
   - `RunAt` = now
   - `Details` = "<scope>: <reason>; item set to Not applicable / kept / deleted"
6. **Confirm in one line**, for example: "Excluded 'Designate a point of contact' for all contracts (routine admin); the item is now Not applicable."

## Writes
- Exclusions: one row, created or reactivated.
- The selected Obligations item: `Status`, `Timing`, `Notes` (append only). It's deleted only under the rule above.
- Run Log: one row.

## Never
- Exclude or change any other obligation, even one that matches the new pattern. Capture applies the exclusion next time it runs.
- Create a duplicate exclusion.
- Delete an item that a person has worked on.
