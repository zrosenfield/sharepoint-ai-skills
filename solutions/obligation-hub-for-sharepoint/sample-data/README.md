# Sample data

Everything here is **fictional**. The company that owns the hub is **Northwind Traders, Inc.** Its counterparties are Contoso Ltd, Fabrikam Inc, Tailspin Toys, Litware Inc, Proseware Inc, Alpine Ski House, Wide World Importers, Adventure Works Cycles, Fourth Coffee and Woodgrove Bank. All of these are fictional sample company names. The people, addresses, amounts and clauses are invented too. Don't use this data as a model contract.

## What's here

| File | What it is |
|---|---|
| `contracts/*.docx` | 11 short Word contracts (roughly 900 to 1,450 words each): an MSA and its amendment, cloud hosting, distribution, software licence and support, data processing, office lease, supply, reseller, facilities services and a revolving credit facility. |
| `contracts-manifest.json` | Each contract's key terms (counterparty, type, Northwind's role, effective and expiry dates, auto-renewal, notice period, governing law, value, business unit, and what it amends). The deploy script writes these to the Contracts library columns. |
| `answer-key.json`, `answer-key.md` | What a correct capture should produce, row by row: 69 rows across the 11 documents. 55 should be tracked, 3 held for review, 9 excluded and 2 superseded. The `.md` version has summary tables and the conventions. |
| `pre-captured-obligations.json` | 60 obligations captured from these contracts by the `capture-obligations` skill in the kit's test run. The deploy script loads them (`preCapturedSample: true`), so the hub is populated before any workflow runs. Of the 60, 55 are confirmed and open, 3 are held in Needs review, and 2 are Not applicable because the amendment superseded them. |
| `run-log-seed.json` | 13 Run Log rows to go with them: 11 Capture runs, one Assign owners run and one Daily sweep run. Every `Details` value starts with **"Demo seed"**, so you can tell them from real runs. |
| `generator/` | The Python that writes the contracts, the manifest and the answer key. |

The deploy script marks every sample contract and obligation with **IsSample = Yes**. It makes the person running it the contract owner, and the owner and escalation owner of the 55 confirmed open obligations. The 3 held and 2 closed items stay unowned. The two example routing rules (Finance - payments, Legal - notices and renewals) also point at that person.

## Planted traps

The contracts include 33 deliberate traps. The answer key's `isTrap` and `trapType` columns mark them, and `answer-key.md` says how each should be handled.

| Trap type | Rows | What a correct capture does |
|---|---:|---|
| amendment | 4 | Reads the amendment with the base contract. Tracks the amended values (120-day non-renewal notice, 10-day report) and treats the original clauses as superseded. |
| notice-window | 2 | Computes the window from the expiry date and tracks its closing date (lease renewal option; Fabrikam transition request). |
| claim-window | 1 | Tracks Northwind's duty to claim a Fabrikam service credit within 30 days, even though the SLA is Fabrikam's. |
| event-driven | 6 | Tracks the duty with a plain-language trigger event and no due date (change of control, repairs, defects, sub-processor objection, price match, default notice). |
| counterparty-vs-us | 5 | Assigns the right party. An audit right can create a duty for Northwind to cooperate; the other side's notices are tracked as Counterparty. |
| fixed-expiry | 2 | Treats a fixed end date with no auto-renewal as a renewal decision date. |
| prohibition | 1 | Tracks a standing restriction as an Ongoing compliance obligation. |
| routine-admin | 8 | Creates nothing for administrative boilerplate. |
| condition-precedent | 1 | Doesn't track a closing fee that was paid at signing. |
| missing-document | 3 | Holds an item for review when its terms are in a document that isn't in the library. |

The capture skill was tuned on these same 11 contracts, so a good score here doesn't prove it works on real paper. See the kit's known gaps.

## Dates

Every date is relative to a reference "today" of **2026-11-24**. On that day, the sample has 4 overdue obligations, 6 due in the next 14 days, 20 later ones and 28 with no date (event-driven or ongoing). Two more are closed.

- The deploy script recomputes each obligation's **Timing** when it loads it, so Overdue, Due soon and Upcoming are right for the day you install. Later, the daily sweep keeps them right.
- With `shiftDatesToToday: true`, the deploy script moves **every sample date** forward by the number of days between 2026-11-24 and your install date. That covers the due dates, the contract effective and expiry dates, and the Run Log times (never into the future). The hub then looks the way it did on the reference day. The default is `false`, because **the text inside the Word files doesn't move**. With shifted dates, the list says one date while the contract's clause says another, and a re-capture would bring back the original dates.

## Regenerate

Run `python3 generator/build.py` from this folder. It needs `python-docx` and `python-dateutil`. The generator is deterministic, with its "today" fixed in `generator/lib.py`, so it rebuilds `contracts/`, `contracts-manifest.json`, `answer-key.json` and `answer-key.md`, then self-checks them.

`pre-captured-obligations.json` and `run-log-seed.json` aren't generated. They're the output of a capture run. If you change the contracts, re-capture them on a test site (Re-capture obligations quick step), export the Obligations and Run Log rows into these files with the same field names, and keep "Demo seed" at the start of each `Details`.

## Remove it

- Use the **`clear-obligation-sample-data`** skill ("clear the sample data"). It finds only items and files with IsSample = Yes, plus Run Log rows whose Details start with "Demo seed", shows the counts, asks first, and moves them to the recycle bin.
- Or remove the whole hub with `deploy/remove-obligation-hub.js`.
