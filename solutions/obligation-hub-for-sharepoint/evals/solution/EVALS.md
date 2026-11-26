# Solution evals: does the built hub work, and does it look right?

Run these on a **disposable test site** loaded with the 11 fictional sample contracts (see [../README.md](../README.md)). "Blocking" means the hub doesn't ship until the eval passes. Reference date for the sample: **2026-11-24**; the due dates in `sample-data/answer-key.json` assume it.

Scripts in this folder are plain Python 3 (no packages); `check_pages.py` also uses Node if it's on the PATH. Each has `--help`, prints a PASS/FAIL table and exits 0 (pass) or 1 (fail). They were tested against the reference build's data and planted defects (35 test cases, all as expected).

## Eval table

| ID | What it checks | How | Pass criteria | Blocking | Baseline (reference build, 2026-11-24) |
|---|---|---|---|---|---|
| S-01 | Schema conformance: 8 lists and libraries, template, every column's internal name, type, choices, default and DateOnly format, every view, its columns, CAML filter terms and default view; no leftover "All Items" default | `check_schema.py` on dumps (below) | `SCHEMA: PASS`; 0 FAIL. UNVERIFIED rows (dump lacked choices or CAML) must be re-dumped with `includeSchemaXml` / `viewId` | Yes | Not measured on a full live dump. Simulated spec-built dump passes; 8 planted defects all caught |
| S-02 | Assets: `AgentAssets/Config/hub-settings.json` parses and has all 11 keys; 10 skill folders in `AgentAssets/Skills/<name>/SKILL.md`; `SHAREPOINT.md` at the AgentAssets **root**; quick steps "Mark fulfilled", "Remove obligation" (Obligations) and "Re-capture obligations" (Contracts) | Copilot prompt P-2 + checklist | All present, names exact, settings `ourCompany` = the company's legal name | Yes | Reference build had 8 skills under their old names (renamed in v1.0) |
| S-03 | Seeds: Obligation Types has 37 rows (29 Track, 5 Exclude, 3 Hold for review); Obligation Owners has an Any/Any rule with empty Counterparty | Copilot prompt P-3 | Counts exact; no duplicate titles | Yes | 37 rows seeded |
| S-04 | Column formatting on Status, Timing, Risk, ReviewState renders with inline styles (no `sp-css` classes) | Manual: open "All obligations" | Four columns coloured; no rendering error | No | Applied (4/4) |
| S-05 | Data invariants: open items have Timing; Timing agrees with Status; DueDate empty ⇔ Event-driven/Ongoing; Recurrence ⇔ Recurring; superseded items Not applicable + Closed with the note once; held items have a reason; Low confidence held; valid choices; unique CaptureKeys; captured items have clause and quote; Fulfilled has FulfilledOn | `check_invariants.py obligations.json --today <date>` | `INVARIANTS: PASS` (warnings allowed) | Yes | PASS on 60 items; warnings: IsSample stored as both `true` and `"Yes"` in the loader file, 5 titles with long-form dates |
| S-06 | Sample flags: every item, contract and evidence file from the sample has IsSample = Yes; nothing else does | `check_invariants.py ... --sample-manifest ../../sample-data/contracts-manifest.json`; Contracts and Evidence by Copilot prompt P-6 | INV-08 PASS; P-6 lists 0 mismatches | Yes | 60/60 items |
| S-07 | Capture accuracy against the answer key (55 track rows) | `score_capture.py obligations.json` after capturing all 11 contracts | Recall ≥ 0.90, precision ≥ 0.90, each field (Party, Category, TriggerType, Recurrence, DueDate, Clause) ≥ 0.90 | Yes | 55/55 recall and precision, every field 55/55 (blind run, previous skill version) |
| S-08 | Trap handling by trap type | `score_capture.py` (same run) | **amendment 100% and routine-admin 100%** (gating); other types reported, target 100% | Yes (two types) | All 10 trap types 100% |
| S-09 | Held for review: the 3 missing-document rows are open items in Needs review | `score_capture.py` (same run) | Held correctly ≥ 2/3 | Yes | **1/3 with the previous skill** (it excluded 04 §3.3 and 09 §2.2). The reference build shows 3/3 only because two held rows were added by hand per the fix; the fixed skill hasn't been re-run |
| S-10 | Order independence: capturing 01 then 02, 02 then 01, or both at once gives the same final state | Capture into three clean sites or reset between runs; dump Obligations; `compare_states.py A.json B.json --prefix 01 --prefix 02` | `IDENTICAL` for A↔B and A↔C | Yes | Not measured |
| S-11 | Risk calibration: share of open items with Risk = High | `check_invariants.py` (RISK row) | 15–30% High | Yes | 22% (13/58) after recalibration; 47% (27/58) before |
| S-12 | Re-capture is idempotent | Dump; run "Re-capture obligations" on all 11; dump; `compare_states.py before.json after.json --add-fields Owner,Notes` | `IDENTICAL`; 11 Capture rows with ItemsCreated 0 | Yes | Not measured |
| S-13 | Pages, static: tokens filled, live-data manifest first in `<head>` with site URL + list GUID + list URL, scripts and JSON parse, no URL outside the site origin, no forbidden APIs, < 300 KB, links between hub pages resolve | `check_pages.py <filled pages> --site-url <site>` | `PAGES: PASS` | Yes | PASS on the reference build's filled pages; WARN: they still name the retired skills and carry an in-page menu |
| S-14 | Pages, behaviour: each page in four data modes (sample snapshot, live rows, **live but empty list**, unreadable live data): renders, empty state shown, badge text right ("Live · N obligations" / "Sample snapshot · N") | Page tests shipped with the page sources (`dom_stub_test.js dist` and `installed`, after `fixtures.py`) | All checks pass | Yes | 136/136 checks for templates and for filled pages |
| S-15 | Contrast: every text pair ≥ 4.5:1 (large text and UI boundaries ≥ 3:1), translucent layers composited | Page tests: `contrast.py` | All pairs pass | Yes | 57/57 pairs |
| S-16 | Pages live on the site: all 7 published, Home set as the home page, every page reachable from the site navigation (the pages have no menu of their own), badge reads "Live · N obligations" with N = the Obligations item count, in-page links open | Manual on the site (signed in as a member, not the owner) | All 7 pages | Yes | Home verified "Live · 60 obligations"; other pages not individually recorded |
| S-17 | Empty hub on the site: before sample load each page shows its empty state, not errors and not the sample snapshot labelled Live | Manual | 7/7 pages | No | Not measured on site (covered by S-14) |
| S-18 | Responsive and browser render at 1440, 768 and 390 px; keyboard focus visible; reduced motion respected | Page tests `browser_test.py` / `shoot.py` (headless Chromium) + manual keyboard pass | No overflow, no clipped text, focus visible on every control | No | Screenshots taken in the working kit; not scored |
| S-19 | Each AI workflow's first run writes **exactly one** Run Log row (Capture new, Capture changed, Assign owners, Daily sweep, Owner digest, Leadership digest) | Manual: trigger each once; Copilot prompt P-19 | 6 workflows × 1 row, Outcome Succeeded/Skipped/Partial with Details | Yes | **Not measured** |
| S-20 | Capture skips unchanged text: editing a column (e.g. ContractOwner) fires "Capture changed contracts", which logs Skipped "content unchanged" and changes nothing | Dump; edit; wait for the row; dump; `compare_states.py` | Skipped row; `IDENTICAL` | Yes | **Not measured** |
| S-21 | Sweep is idempotent: the second sweep of the day changes nothing and sends nothing | Run the sweep, dump, run again, dump; `compare_states.py a.json b.json --fields Timing,LastReminded,Status,DueDate,Notes` | `IDENTICAL`; second Run Log row "Timing changed 0. Rolled forward 0." and no messages | Yes | **Not measured** |
| S-22 | Roll-forward creates exactly one successor: Mark fulfilled on 07 §2.1 rent (due 2026-12-01) creates `…#2027-01-01`; a sweep afterwards creates none. Also set an item Fulfilled directly in the list: the sweep creates one, the next sweep none | Manual + `check_invariants.py` (INV-09) | One successor per series; INV-09 PASS | Yes | **Not measured** |
| S-23 | Reminder cooldown: an overdue confirmed item with LastReminded = yesterday isn't escalated; with LastReminded 3 days ago it is, once; a due-soon item is reminded once per window | Manual (set LastReminded by hand, run the sweep) | As stated; LastReminded = today only on items in sent messages | Yes | **Not measured** |
| S-24 | Owner routing: rules Any/Any → A, Payment → B, Counterparty "Woodgrove Bank" → C give Woodgrove 7 → C, other payments 9 → B, the other 39 → A; 3 held items unassigned; one message per owner | Manual + Copilot prompt P-24 | Counts exact; most specific rule wins | Yes | **Not measured** (the reference build routed everything to one person) |
| S-25 | Digests: owner digest one message per owner with sections, skips owners with nothing due, second run Skipped; leadership digest sections in order, "Includes sample data." first, no invented metrics, writes nothing but its Run Log row | Manual | As stated | No | **Not measured** |
| S-26 | Quick steps write only their documented fields plus one Run Log row | Usage evals U-04, U-05, U-15, plus `compare_states.py` with `--fields` covering all columns | No other item or field changed | Yes | **Not measured** |
| S-27 | Loop safety: no workflow writes to a Contracts item; no contract gets more than 3 Capture rows in an hour | Manual: Contracts version history; Copilot prompt P-27 | 0 versions by the workflow account; ≤ 3 rows/contract/hour | Yes | **Not measured** |
| S-28 | Clear sample data removes only IsSample = Yes items and files (Obligations, Contracts, Evidence) and "Demo seed" Run Log rows, after one confirmation | Manual on a disposable site with one non-sample contract and obligation planted first | Planted items survive; 0 sample items remain | Yes | **Not measured** |
| S-29 | Design review: Atmospheric Precision rubric below | Two reviewers score the 7 pages | Weighted ≥ 70% (target 80%) and no reject condition | Yes | **Not scored** |

The score_capture gates interact: a run that drops the amendment and re-opens the superseded items still scores recall 93% and precision 96% (both above 0.90), and only the amendment gate fails. Keep all gates.

## Collecting the inputs (Cowork with SharePoint tools, read-only)

- **P-1 Schema dump (S-01).** "On `<site>`, for each of Contracts, Obligations, Obligation Owners, Obligation Types, Exclusions, Run Log, Evidence and AgentAssets: call get_list_schema with includeSchemaXml and includeViews set to true, then get_list_schema with each view's viewId. Save every raw result, unchanged, as one JSON file per call in a folder `schema-dump`. Don't summarise." Then `python3 check_schema.py --dump schema-dump`.
- **Obligations dump (S-05 to S-12, S-20 to S-22).** "Read every item of the Obligations list on `<site>` (all columns, internal names, page through everything) and save the raw items as `obligations.json`." Person columns may come back as objects; the scripts don't need them except where stated.
- **P-2** "On `<site>`, list the AgentAssets root, AgentAssets/Skills and AgentAssets/Config, open hub-settings.json and list the quick steps on Obligations and Contracts. Report anything missing from: <the S-02 list>."
- **P-3** "Count Obligation Types rows by Handling and list duplicate titles; show the Obligation Owners rules."
- **P-6** "List Contracts files and Evidence files with their IsSample value."
- **P-19** "Show the Run Log rows created since `<time>`, grouped by Workflow, with Outcome and Details."
- **P-24** "Count open Obligations by Owner, and list open items with ReviewState Needs review that have an Owner."
- **P-27** "For each Contracts file, list its versions since `<time>` with Modified By; count Capture Run Log rows per contract in the last hour."

## Script reference

| Script | Input | Typical call |
|---|---|---|
| `check_schema.py` | dump files/folders; `--spec` defaults to `schema-spec.json` (or pass the kit's deploy `lists.json`) | `python3 check_schema.py --dump schema-dump --json-out s01.json` |
| `check_invariants.py` | Obligations items JSON | `python3 check_invariants.py obligations.json --today 2026-11-24 --sample-manifest ../../sample-data/contracts-manifest.json` |
| `score_capture.py` | Obligations items JSON, answer key | `python3 score_capture.py obligations.json --key ../../sample-data/answer-key.json` |
| `compare_states.py` | two Obligations snapshots | `python3 compare_states.py a.json b.json --prefix 01 --prefix 02` |
| `check_pages.py` | filled pages folder | `python3 check_pages.py filled-pages --site-url https://<tenant>.sharepoint.com/sites/<site>` |

Common options: `--map SRC=DST` copies a field before checking (for example `--map NewRisk=Risk` when a working file keeps a recalibrated risk in another column); `--json-out` writes machine-readable results; `check_invariants.py --timing-strict` makes stale Timing an error (use right after a sweep); `--utc-offset` (default −8) converts UTC timestamps on DateOnly columns to dates.

### Sample runs you can reproduce from this folder

Against the kit's own pre-captured sample (`sample-data/pre-captured-obligations.json`, the register as loaded on the reference build):

| Command | Result |
|---|---|
| `python3 check_invariants.py ../../sample-data/pre-captured-obligations.json --today 2026-11-24 --sample-manifest ../../sample-data/contracts-manifest.json` | 60 items (58 open); all errors PASS; RISK 13/58 = 22%; WARN INV-08b (IsSample stored as `true` and `"Yes"`), INV-12b (5 long-form dates in titles); `INVARIANTS: PASS` |
| `python3 score_capture.py ../../sample-data/pre-captured-obligations.json` | Recall 55/55, precision 55/55, held 3/3, traps 9/9 excluded and 2/2 superseded, every field 55/55, all 11 gates PASS; `CAPTURE: PASS` |
| `python3 compare_states.py A.json A.json --prefix 01 --prefix 02` | `Compared 12 common items …; 0 difference(s).` `IDENTICAL` |
| `python3 check_pages.py ../../deploy/pages --allow-tokens` | Templates: tokens allowed, scripts parse, no forbidden APIs; `PAGES: PASS (7 pages …)` |
| `python3 check_schema.py --dump <dump of a site built to spec>` | `SCHEMA: PASS (259 checks: 257 pass, 0 fail, 0 warn, 2 unverified)` (simulated dump; the 2 unverified are views whose CAML wasn't dumped) |

The pre-captured sample isn't a capture run: it shows the scripts working, not capture accuracy. Run S-07 to S-09 on items your capture skill wrote.

`schema-spec.json` is the v1.0.0 schema: the live-tested `lists.json` plus `IsSample` on Evidence. If the schema changes, regenerate it and re-run S-01.

## S-29 design review: Atmospheric Precision rubric

Adapted from section 6 of the *Six Design Languages* playbook (design language 01). Two reviewers score each criterion 1–5 across the 7 pages at 1440 px and 390 px, then agree a single score (differences > 1 are discussed, not averaged). Weighted score = Σ (score ÷ 5 × weight).

| Criterion | Weight | 5 looks like | 1 looks like |
|---|---:|---|---|
| Language fidelity | 25% | Depth and light organise every page: calm cloud canvas, soft page-top light, directional shadows, translucency used sparingly and never on tables or forms; graphite text, ice and violet as restrained tints; sits calmly under SharePoint's own navigation; recognisable in grayscale | Default SharePoint/Fluent look, glass on every card, or a consumer-OS clone |
| Usability | 25% | Each page's primary task in ≤ 2 interactions: Home → what's overdue and next; My obligations → my items and the Mark fulfilled path; Review queue → confirm, edit or remove with the clause in view; Contract 360 → terms and notice timeline; Leadership → exposure by counterparty | Primary task buried; dates or parties need a click to see |
| Craft | 20% | 8-point rhythm, deliberate type scale, limited weights, aligned numerals, designed states (loading skeleton, empty, error, Sample vs Live badge) | Inconsistent spacing, default states, misaligned tables |
| Accessibility | 15% | Contrast tests pass, visible focus, logical headings, keyboard reachable, reduced motion honoured, no essential text on translucent layers | Any text below 4.5:1 or a keyboard trap |
| Responsive quality | 10% | Intentional 1440/768/390 compositions; tables reflow to labelled cards | Desktop layout shrunk; horizontal scrolling |
| Performance | 5% | < 300 KB per page, blur only on the nav, short motion | Heavy blur on dense tables, long animations |

**Reject regardless of score** (the playbook's rule): a critical accessibility or functionality failure (any S-15 failure, keyboard trap, a page that errors with live data), or failing the language's pass/fail test: *with effects disabled the page must remain polished, readable and meticulously spaced* (check with reduced transparency and reduced motion on).
