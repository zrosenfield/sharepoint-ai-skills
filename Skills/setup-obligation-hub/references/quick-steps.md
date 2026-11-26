# Quick steps

Three quick steps let people act on an item without typing a prompt. Each one sends a fixed prompt to Copilot in SharePoint for the selected item, and the named skill does the rest. The pages and messages refer to them by these exact titles.

Create each one as an active quick step whose action is "ask the knowledge agent" (action type `AskKnowledgeAgent`) with the prompt below as its custom prompt. On a library, mark it as a document-library quick step. If a quick step with the same title already exists on that list, leave it as it is and report it as skipped.

| List or library | Title (exact) | Show when | Custom prompt (exact) | Runs skill |
|---|---|---|---|---|
| Obligations | Mark fulfilled | Status is not Fulfilled (condition: `[$Status] != 'Fulfilled'`) | Mark this obligation fulfilled using the mark-obligation-fulfilled skill. | `mark-obligation-fulfilled` |
| Obligations | Remove obligation | Always (condition: `true`) | Remove this obligation from tracking using the exclude-obligation skill. | `exclude-obligation` |
| Contracts | Re-capture obligations | Always (condition: `true`) | Re-capture obligations from this contract using the capture-obligations skill. Do a full capture even if the text hasn't changed. | `capture-obligations` |

## What each one does

- **Mark fulfilled.** Asks once for evidence (a link, a file or "none"), sets Status = Fulfilled, FulfilledOn and Evidence, and creates the next occurrence of a recurring item. To give a date other than today, the person adds it in chat: "fulfilled on 2026-11-20".
- **Remove obligation.** Asks once for the scope (this contract or all contracts), the reason, and whether to remove the item now. Records an Exclusions row so capture won't add the clause back, then sets the item to Not applicable rather than deleting it. Keep the title starting with "Remove"; the pages call it "the Remove quick step".
- **Re-capture obligations.** Forces a full capture of the selected contract. Use it after editing Obligation Types or Exclusions, after setting Amends on an amendment, or for a contract added while the Capture workflows were paused. It's safe to repeat: existing items are updated or skipped, and fields people own (Owner, Status, Evidence, Notes) are never overwritten.

## Check it worked

Select one item in Obligations: Mark fulfilled and Remove obligation appear in the command bar or the item's menu. Select a file in Contracts: Re-capture obligations appears. Don't run them as a test on real items.
