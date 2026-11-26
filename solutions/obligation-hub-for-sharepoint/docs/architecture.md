# Architecture

One SharePoint site holds everything: the lists are the data, the skills are the logic, AI workflows and quick steps run the skills, and the pages and Copilot read the lists. There's no server, database, Power Automate flow or custom code running in the tenant.

## Components

| Component | What it is | Role |
|---|---|---|
| **Contracts** library | Signed contracts and amendments, with key-term columns (optional autofill) | Input. Adding or changing a file triggers capture |
| **Obligations** list | One row per obligation: clause, quote, party, trigger, due date, owner, status, timing, risk, review state | The register. Everything else reads or writes it |
| **Obligation Types** list | 37 kinds of clause, each Track, Exclude or Hold for review | Tells capture what to keep |
| **Exclusions** list | Clauses or patterns people removed | Capture's memory of "don't add this back" |
| **Obligation Owners** list | Routing rules: category + business unit + counterparty → owner, escalation owner, channel | Who gets what |
| **Run Log** list | One row per automated or quick-step run | Health and history |
| **Evidence** library | Proof files | Linked from each fulfilled obligation |
| **AgentAssets** library | `Skills/<name>/SKILL.md`, `Config/hub-settings.json`, `SHAREPOINT.md` | Skills, settings and site context for Copilot |
| **Skills** (10) | Prose instructions in [`../../../Skills/`](../../../Skills/) | All the logic |
| **AI workflows** (6) | One trigger and one skill each | Unattended runs |
| **Quick steps** (3) | Mark fulfilled, Remove obligation, Re-capture obligations | One-click runs on a selected item |
| **Pages** (7) | HTML pages in Site Pages with live list data | Home, My obligations, Review queue, Contract 360, Leadership, How it works, Settings |
| **Site navigation and look** | Eight hub links in the site navigation, the "Obligation Hub" theme, a logo, a compact header (set by the deploy script) | The only navigation between pages; the pages have no menu of their own |
| **Copilot in SharePoint** | Chat on the site, guided by `SHAREPOINT.md` and `obligation-hub-guide` | Questions and ad hoc changes |

## Data flow

1. A contract lands in **Contracts**. The "Capture new contracts" workflow runs `capture-obligations` on it.
2. Capture reads the text, Obligation Types, Exclusions and existing Obligations, then creates or updates items. Clear items are Confirmed; unclear ones go to Needs review. It writes one Run Log row.
3. Autofill (if it runs) fills the key-term columns. That fires "Capture changed contracts", which sees the same text fingerprint and logs Skipped.
4. People confirm held items in the Review queue or the Needs review view.
5. At 7:00 AM `assign-obligation-owners` gives confirmed, unowned items an owner from Obligation Owners and messages each new owner once.
6. At 6:00 AM `sweep-obligations` recomputes Timing, creates next occurrences of fulfilled recurring items, reminds owners of items due soon and escalates overdue ones.
7. Owners act, then use **Mark fulfilled** (`mark-obligation-fulfilled`), which records evidence and creates the next occurrence.
8. Mondays, `obligation-owner-digest` sends each owner their week. Fridays, `obligation-leadership-digest` sends leadership a snapshot.
9. **Remove obligation** (`exclude-obligation`) sets an item to Not applicable and records an Exclusions row, so capture won't add it back.

## Why it's built this way

| Choice | Why |
|---|---|
| **Status is human-set; Timing is computed** | Status records what a person did (Not started, In progress, Fulfilled, Waived, Not applicable). Timing (Overdue, Due soon, Upcoming, No date, Closed) is derived from DueDate, Status and today, and only skills write it. Keeping them apart means automation never claims something was done, and a person never has to maintain a date calculation. Pages and the guide recompute Timing, because the column can be a day behind |
| **Capture never writes to Contracts** | Any write to a Contracts item fires the "file changed" workflow, which would run capture again: a loop. Capture only reads Contracts. It suggests fixes (such as "set Amends to …") in Run Log Details instead |
| **Fingerprint skip** | The "file changed" trigger also fires for autofill and column edits. Capture compares a word-count fingerprint of the text and related files with the last run and skips if nothing changed, so a column edit costs one read, not a full extraction |
| **Held items** | Capture never guesses. Low-confidence items, efforts-based or third-party duties, and terms in a referenced document that isn't in the library go to Needs review with the reason in Notes. Held items aren't assigned or reminded until someone confirms them |
| **Exclusions as memory** | When someone removes an item, the clause (or a general pattern) goes to Exclusions. Re-captures and other contracts respect it, so the same noise doesn't come back |
| **Capture key upsert** | Each item gets a stable key: file name, clause and a short action slug. Re-captures update the matching item instead of creating duplicates, and never touch items people created by hand (empty key). Next occurrences add "#<date>" to the key, so the sweep and Mark fulfilled can't both create the same one |
| **Amendments supersede, never delete** | An amendment's changed clause sets the base item to Not applicable with a "Superseded by" note. The end state is the same whichever file is captured first |
| **One trigger, one skill, one Run Log row** | Each workflow is small and testable. A fix to a skill fixes every workflow and quick step that uses it, and the Run Log shows exactly what ran |
| **Settings in a file, not in prompts** | Thresholds, recipients and the company name live in `hub-settings.json`, routing in Obligation Owners, and what to track in Obligation Types and Exclusions. Changing behaviour never means re-creating a workflow |
| **Lists, not a database** | Site owners can see, filter, edit and export everything with tools they already know, and permissions are the site's |

## Token-cost profile

Workflow and Copilot usage consumes tokens. Where they go:

| Run | Reads | Cost driver | How often |
|---|---|---|---|
| Capture (full) | One contract's text, related files, Obligation Types, Exclusions, that contract's obligations | Contract length. The only step that reads contract text | Once per new contract or changed version |
| Capture (skipped) | The contract text, to fingerprint it | One read, no extraction | Each autofill or column edit |
| Assign owners | Unowned obligations, Obligation Owners, two Contracts columns | Number of new items | Daily; usually tiny |
| Daily sweep | The Obligations list only (selected columns), never contracts | List size | Daily |
| Owner digest | Open, owned obligations | List size | Weekly |
| Leadership digest | Obligations and Contracts columns, never contract text | List size | Weekly |
| Quick steps | One item (Re-capture: one contract) | Small | On demand |

In short: you pay for extraction once per contract version; everything after that reads list rows, not documents.
