# Obligation Hub evals

Two families of evals decide whether a build of the Obligation Hub is ready to show or hand over:

| Family | Question | Where |
|---|---|---|
| **Solution** (S-01 … S-29) | Does the built hub work, and does it look right? Schema, data invariants, capture accuracy against the answer key, pages, workflow runtime, design review | [solution/EVALS.md](solution/EVALS.md) and its scripts |
| **Usage** (U-01 … U-15) | Does it help someone doing the job? Fifteen real tasks for obligation owners, contract managers, leaders and site owners, scored with a rubric | [usage/USAGE-EVALS.md](usage/USAGE-EVALS.md), [usage/RUBRIC.md](usage/RUBRIC.md), [usage/expected/expected_answers.json](usage/expected/expected_answers.json) |

The scripts are Python 3 with no extra packages (Node optional, for parsing page scripts). They read JSON you export from the site; none of them calls SharePoint.

## Where to run them

On a **disposable test site** only, never on a hub people use: the evals load fictional sample data, plant defects, delete routing rules and clear data. Use a new site such as `/sites/obligationhub-eval-<yyyymmdd>`. SharePoint AI workflows, autofill and HTML pages with live list data are preview features that may not be available in your tenant yet; the runtime evals S-19 to S-27 need AI workflows, and everything else runs wherever Copilot in SharePoint or Cowork with the SharePoint tools runs. Use a second disposable site (or clear and reload) for the capture-order test S-10 and for U-06.

## Order

1. **Before upload:** page checks on the filled pages: S-13 (`check_pages.py`), S-14 and S-15 (the page tests shipped with the page sources).
2. **Build the empty hub** (setup skill, deploy script or [../prompts/build-from-scratch.md](../prompts/build-from-scratch.md)), then S-01 to S-04 and **S-17 (empty hub pages) before any sample data**.
3. **Load the sample by capture:** upload the 11 contracts from `sample-data/contracts` (base before amendment) and let the Capture workflows run, or run Re-capture on each. Export Obligations, then S-05 to S-09 and S-11 (`check_invariants.py`, `score_capture.py`). Then S-12 (re-capture all; compare) and S-10 on the second site.
4. **Pages on the site:** S-16.
5. **Workflow runtime:** S-19 to S-27, in this order: capture workflows (S-19, S-20, S-27), assign owners (S-24), sweep (S-21, S-22, S-23), digests (S-25), quick steps (S-26).
6. **Design review:** S-29.
7. **Usage evals:** reset to the common setup S0, then read-only tasks first (U-01, U-02, U-03, U-07, U-08, U-09, U-10, U-14), then writing tasks (U-04, U-15, U-05, U-13), then U-11 and U-12 (they change routing and schema), and U-06 on the second site. Score with the rubric (LLM judge plus 20% human spot-check).
8. **Last:** S-28 (clear sample data), then delete the test site.

If the reference date isn't 2026-11-24, regenerate the usage answers first: `python3 usage/expected_answers.py --today <date> --out usage/expected/expected_answers-<date>.json`, and run `check_invariants.py --today <date>`.

## What "ship" means

A build ships when **all blocking solution evals pass** (every row marked Blocking = Yes in [solution/EVALS.md](solution/EVALS.md)) **and** the usage suite scores **≥ 80%** with no task scoring 0 on Correctness or Safety. Publish the results file with the build, and keep [../docs/known-gaps.md](../docs/known-gaps.md) in step with what the evals found.

## Baseline: the reference build (2026-11-24)

| Eval | Result | Notes |
|---|---|---|
| S-07 capture accuracy | **Recall 55/55, precision 55/55**, every field 55/55 | Blind run of the previous capture skill over the 11 samples: the same contracts the skill was tuned on |
| S-08 traps | 10 of 10 trap types at 100% (amendment 4/4, routine-admin 8/8) | Same run |
| S-09 held for review | **1/3 before the fix** (fails the 2/3 gate) | The previous skill excluded 04 §3.3 and 09 §2.2. The reference build shows 3/3 because two held rows were added by hand to match the fixed rule; **the fixed skill has not been re-run** |
| S-11 risk | **22% High (13/58 open) after recalibration**; 47% (27/58) before | The consequence rubric in the capture skill reproduces all 58 recalibrated values (checked by `expected_answers.py --site-obligations`) |
| S-05 / S-06 invariants | PASS on 60 items | Warnings: IsSample stored as both `true` and `"Yes"` in the loader file; 5 titles with long-form dates |
| S-13 static pages | PASS (7/7) | WARN: the reference build's pages still name the retired skills (built before the rename) and carry an in-page menu (the pages now rely on SharePoint's site navigation) |
| S-14 / S-15 page tests | **Pass**: 136/136 DOM-stub checks for templates and for filled pages; 57/57 contrast pairs | |
| S-16 live data | "Live · 60 obligations" seen on Home | Other pages not individually recorded |
| S-04, S-03 | Formatting applied to 4/4 columns; 37 types seeded | |

The scripts themselves were tested against the reference build's data and planted defects: 35/35 test cases behaved as expected (schema checker catches all 8 planted schema defects; the invariant checker catches 10 planted violations; score and compare match the original kit scripts' numbers).

## Not yet measured

- **Workflow runtime** (S-19 to S-27): no workflow has been run end to end against these evals. AI workflows are a preview feature and still maturing, so expect some failed runs and read the Run Log.
- **Real contracts.** All accuracy numbers come from 11 synthetic Word contracts the capture skill was tuned on. Scans, exhibits, SOWs, missing referenced documents and long agreements are untested.
- **The fixed capture skill** (missing-document holds, consequence risk rubric): not re-run blind; S-07 to S-11 need a fresh run.
- **Order independence** (S-10), **re-capture idempotency** (S-12) and **clear sample data** (S-28).
- **S-01 on a full live dump**: only early-build dumps were saved; the checker was proven on simulated dumps.
- **Design review** (S-29) and **all usage evals** (U-01 to U-15): not scored yet.
