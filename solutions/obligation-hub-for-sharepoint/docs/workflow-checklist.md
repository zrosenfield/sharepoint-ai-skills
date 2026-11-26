# Workflow checklist

For whoever sets up the hub's six AI workflows. Allow about 30 minutes, plus a day to see the scheduled runs. The prompts are in [../workflows/ai-workflow-prompts.md](../workflows/ai-workflow-prompts.md); the Settings page shows the same prompts, filled in for your site.

> SharePoint AI workflows are a preview feature that may not be available in your tenant yet. Each workflow has exactly one trigger, runs one site skill, and runs as the person who creates it.

## 1. Before you start

Tick every line. A missing piece usually shows up as a Failed run in the Run Log.

| Check | Where | Why |
|---|---|---|
| You're signed in as the account that should send messages | Your browser profile | Workflows run as their creator. For anything beyond a demo, use a shared obligations account with edit rights on the site, so messages don't stop when one person leaves |
| The hub's skills are in `AgentAssets/Skills/<skill>/SKILL.md` | AgentAssets library | At least `capture-obligations`, `assign-obligation-owners`, `sweep-obligations`, `obligation-owner-digest`, `obligation-leadership-digest`, plus the quick-step skills `mark-obligation-fulfilled` and `exclude-obligation` |
| `AgentAssets/Config/hub-settings.json` has `ourCompany`, `siteUrl` and `leadershipRecipients` filled in | AgentAssets library | Capture stops with "hub-settings.json missing" without `ourCompany` |
| Obligation Types is seeded (37 rows) | Obligation Types list | Capture classifies against it |
| Obligation Owners has an Any/Any rule with an owner | Obligation Owners list | Without it, nobody is assigned or reminded |
| The time in each prompt matches `timeZone` | The prompts | The prompts say "Pacific time"; change it if yours differs |

## 2. Create the workflows, capture first

Paste each prompt into Copilot in SharePoint on the hub site, one at a time. After each, check the site's AI workflows panel lists it as on.

| # | Workflow | Prompt key | What its first run leaves in **Run Log > Recent runs** |
|---|---|---|---|
| 1a | Capture new contracts | `CAPTURE_NEW` | After your next upload: one **Capture** row, Outcome Succeeded, with Created / Held counts and the fingerprint in Contract version |
| 1b | Capture changed contracts | `CAPTURE_CHANGED` | Usually one **Capture** row, Outcome **Skipped**, Details "content unchanged", a few minutes after an upload. That's the autofill change firing the trigger, and it's expected |
| 2 | Assign owners | `ASSIGN_OWNERS` | Next 7:00 AM: one **Assign owners** row. Succeeded with "No unassigned obligations" is fine |
| 3 | Daily sweep | `DAILY_SWEEP` | Next 6:00 AM: one **Daily sweep** row with open counts in Details |
| 4 | Owner digest | `OWNER_DIGEST` | Next Monday 8:00 AM: one **Owner digest** row |
| 5 | Leadership digest | `LEADERSHIP_DIGEST` | Next Friday 3:00 PM: one **Leadership digest** row. Failed "no leadership recipients configured" means the settings file has none |

Every run writes exactly one row. Two rows for one scheduled run, or none, means something is wrong (see section 6).

## 3. End-to-end test

Use one real-looking contract you know well, or one of the kit's sample contracts on a test site. Do the steps in order.

| Step | Do | Expect | If not |
|---|---|---|---|
| 1 | Upload one new contract to Contracts | Within a few minutes: a **Capture** row, Outcome Succeeded | Check the workflow is on; open the row's Details for the reason |
| 2 | Wait a few more minutes | A second **Capture** row, Outcome **Skipped**, "content unchanged" (from the autofill change). If autofill doesn't run on your tenant, this row may not appear | Two Succeeded rows for one upload means the fingerprint didn't match; tell the kit maintainer |
| 3 | Open Obligations | New items for the contract: confirmed ones in **Open by due date** or **Triggered and ongoing**, held ones in **Needs review**, each with Clause and Source clause filled in | Nothing new: open the Capture row's Details (excluded clauses and errors are listed there) |
| 4 | Confirm one held item: set Review to Confirmed | It now waits for an owner | |
| 5 | Wait for the next 7:00 AM | An **Assign owners** row; the new confirmed items have an Owner; each new owner gets ONE "Action required" message with working links to the items | No owner: the item's category or business unit has no matching rule and there's no Any/Any rule |
| 6 | On a recurring item, run the **Mark fulfilled** quick step and give a link as evidence | Status Fulfilled, FulfilledOn today, Evidence set, Timing Closed; a new item for the next occurrence with Capture key ending "#<next date>"; a **Mark fulfilled** row | No next occurrence: the item's text says "Through <date>" or "Last due <date>" and the next date is past it |
| 7 | Wait for the next 6:00 AM | A **Daily sweep** row; Timing updated (for example Upcoming → Due soon); reminders only for confirmed, owned items due soon or overdue; no duplicate of the occurrence from step 6 | Run the sweep again in chat ("run the daily sweep"): a second run on the same day changes nothing and sends nothing |

## 4. Measure accuracy on the workflow runtime

The skills were scored by running them in chat. The workflow runtime can behave differently, so score it too:
1. On a test site, load the sample contracts with the Capture workflows on (not the pre-captured sample).
2. Wait until every contract has a Capture row.
3. Score the Obligations list against the answer key, following [../evals/README.md](../evals/README.md).

Compare the score with the chat baseline in the evals. A lower workflow score usually means skipped runs, timeouts or partial writes; the Run Log Details name them.

## 5. Pause or resume

- **Pause:** turn the workflow off in the site's AI workflows panel, or ask Copilot "Pause the Daily sweep workflow on this site".
- **Resume:** turn it back on. Missed scheduled runs aren't replayed, but the next sweep catches up on Timing.
- **Capture was paused?** Run the **Re-capture obligations** quick step on every contract added or changed in the meantime.
- **Bulk import:** upload base contracts before their amendments and set **Amends** on each amendment. If they went in together, run Re-capture obligations on the base after its amendment's Capture row appears.

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Capture Failed, "hub-settings.json missing" | The settings file is missing or has no `ourCompany` | Upload `AgentAssets/Config/hub-settings.json` |
| Capture Skipped for a contract you edited | A small edit kept the word count within 0.5% | Run **Re-capture obligations** on it |
| No Run Log row at all | The workflow is off, or it failed before loading the skill | Check the AI workflows panel; re-create it from the prompt |
| Messages come from the wrong person | Workflows run as their creator | Re-create them signed in as the shared account, then turn the old ones off |
| Owners get nothing | Items are held (Needs review) or have no owner | Confirm held items; add routing rules |
| Leadership digest Failed | No recipients in settings | Add `leadershipRecipients` |
