# Obligation Hub: quick steps

Quick steps send a fixed prompt to Copilot in SharePoint for the selected item. The skill does the rest: it asks at most one question and confirms in one line. The deploy script and [`setup-obligation-hub`](../../../Skills/setup-obligation-hub/) create them for you. To add them by hand, open the list or library's quick steps settings from its command bar, or ask Copilot in SharePoint to create them (see [SETUP.md](../SETUP.md), step 6), and use the exact titles below. The pages refer to them by these names.

| List or library | Title (exact) | Show when | Runs skill | Asks the user | Writes |
|---|---|---|---|---|---|
| Obligations | **Mark fulfilled** | Status isn't Fulfilled | [`mark-obligation-fulfilled`](../../../Skills/mark-obligation-fulfilled/) | Evidence: a link, a file or "none" (skipped if already given) | The item (Status, FulfilledOn, Evidence); the next occurrence if recurring; Evidence library; Run Log |
| Obligations | **Remove obligation** | Always | [`exclude-obligation`](../../../Skills/exclude-obligation/) | Scope (this contract or all contracts), the reason, and whether to remove it now | Exclusions (one row); the item set to Not applicable; Run Log |
| Contracts | **Re-capture obligations** | Always | [`capture-obligations`](../../../Skills/capture-obligations/) (forced) | Nothing | Obligations (creates and updates); Run Log |

Each quick step's action is **Ask the knowledge agent** (action type `AskKnowledgeAgent`) with the prompt below as the custom prompt. The "Show when" condition for Mark fulfilled is `[$Status] != 'Fulfilled'`.

## Mark fulfilled (Obligations)
```text
Mark this obligation fulfilled using the mark-obligation-fulfilled skill.
```
- Select one item, then the quick step. To give a date other than today, add it in chat: "fulfilled on 2026-11-20".
- For recurring items it creates the next occurrence right away, so the daily sweep won't duplicate it.
- Evidence is optional in this version. See [known gaps](../docs/known-gaps.md#2-no-proof-standard).

## Remove obligation (Obligations)
```text
Remove this obligation from tracking using the exclude-obligation skill.
```
- It records the clause (This contract) or a generalized pattern (All contracts) in Exclusions, so capture won't add it back. Then it sets the item to Not applicable rather than deleting it.
- The Home, Review and How it works pages call this "the Remove quick step". Keep the title starting with "Remove".

## Re-capture obligations (Contracts)
```text
Re-capture obligations from this contract using the capture-obligations skill. Do a full capture even if the text hasn't changed.
```
- Use this after editing Obligation Types or Exclusions, after setting **Amends** on an amendment, or for a contract that was added while the Capture workflows were paused.
- It's safe to repeat. Existing items are updated or skipped, and fields people own (Owner, Status, Evidence, Notes) are never overwritten.

## Check they work
Select one Obligations item: **Mark fulfilled** and **Remove obligation** appear in the command bar. Select one Contracts file: **Re-capture obligations** appears. Try Mark fulfilled first on a sample item, not a real one.
