# Obligation Hub: AI workflow setup prompts

Six SharePoint AI workflows keep the hub current. An AI workflow has exactly one trigger, so capture needs two: one for new contracts and one for changed contracts. Each workflow runs **one** site skill from `AgentAssets/Skills/<skill>/SKILL.md` and writes **one** row to the Run Log per run.

To create one, open Copilot in SharePoint on the hub site and paste its prompt. The deploy script also puts each prompt on the hub's Settings page, in its "Setup prompt" box (token `WORKFLOW_PROMPT_<KEY>`), ready to copy.

> **Availability.** SharePoint AI workflows are in early preview and may not be available in your tenant yet. Elsewhere, use the Cowork automations in [../prompts/cowork-prompts.md](../prompts/cowork-prompts.md), section D.

**Time zone.** The prompts say "Pacific time". If your hub uses another time zone (`timeZone` in `AgentAssets/Config/hub-settings.json`), change it in each prompt before you paste it.

| # | Workflow | Trigger | Skill | Can write | Can send |
|---|---|---|---|---|---|
| 1a | Capture new contracts | File added to the Contracts library | [`capture-obligations`](../../../Skills/capture-obligations/) | Obligations, Run Log | Nothing |
| 1b | Capture changed contracts | File changed in the Contracts library | [`capture-obligations`](../../../Skills/capture-obligations/) | Obligations, Run Log | Nothing |
| 2 | Assign owners | Daily at 7:00 AM | [`assign-obligation-owners`](../../../Skills/assign-obligation-owners/) | Obligations (owner fields), Run Log | One email and/or Teams message to each newly assigned owner |
| 3 | Daily sweep | Daily at 6:00 AM | [`sweep-obligations`](../../../Skills/sweep-obligations/) | Obligations (Timing, LastReminded, next occurrences), Run Log | Reminders to owners for items due soon; escalations for overdue items, sent to the escalation owner with the owner cc'd |
| 4 | Owner digest | Mondays at 8:00 AM | [`obligation-owner-digest`](../../../Skills/obligation-owner-digest/) | Obligations (LastReminded), Run Log | One digest to each owner who has items due |
| 5 | Leadership digest | Fridays at 3:00 PM | [`obligation-leadership-digest`](../../../Skills/obligation-leadership-digest/) | Run Log only | One email to `leadershipRecipients`, and optionally one post to `leadershipTeamsChannel` |

Messages go by email, Teams or both, depending on the routing rule's **Notify by** setting (default: `notifyDefault` in `AgentAssets/Config/hub-settings.json`). Workflows run as the person who creates them, so every message comes from that person's mailbox and Teams account.

Before you start, read [../docs/workflow-checklist.md](../docs/workflow-checklist.md). It has the prerequisites, the end-to-end test and how to pause a workflow.

---

## 1a. Capture new contracts (`CAPTURE_NEW`)
- **Trigger:** when a file is added to the Contracts library.
- **Runs:** `capture-obligations` on the file that triggered the run.
- **Sends:** nothing.

```text
Create an AI workflow named "Capture new contracts" on this site. Trigger it when a file is added to the Contracts library. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. Save results without asking for confirmation. Run as me.
```

## 1b. Capture changed contracts (`CAPTURE_CHANGED`)
- **Trigger:** when a file in the Contracts library is changed.
- **Runs:** the same skill, `capture-obligations`, on the changed file.
- **Sends:** nothing.
- **Loop safety:** this trigger also fires when autofill fills a new contract's columns, when someone edits a column, and possibly right after an upload. The skill never writes to the Contracts item, and it skips the run (Run Log Outcome = Skipped, Details "content unchanged") when the text fingerprint matches the last capture. Each skipped run costs one read of the contract text, not a full extraction.
- **Both workflows log `Workflow` = Capture,** so the home page shows them as one "Capture obligations" health row.

```text
Create an AI workflow named "Capture changed contracts" on this site. Trigger it when a file in the Contracts library is changed. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. If the contract text is unchanged since the last capture, log the skip and stop. Save results without asking for confirmation. Run as me.
```

## 2. Assign owners (`ASSIGN_OWNERS`)
- **Trigger:** schedule, every day at 7:00 AM.
- **Runs:** `assign-obligation-owners`.
- **Sends:** one aggregated "Action required" message to each newly assigned owner.

```text
Create an AI workflow named "Assign owners" on this site that runs every day at 7:00 AM Pacific time. For each run, load the site skill assign-obligation-owners from AgentAssets/Skills and follow it for the Obligations list. It may send each newly assigned owner one email or Teams message. Run as me.
```

## 3. Daily sweep (`DAILY_SWEEP`)
- **Trigger:** schedule, every day at 6:00 AM.
- **Runs:** `sweep-obligations`. It reads the Obligations list only, never the contracts.
- **Sends:** "Coming due" reminders to owners and "Overdue" escalations to escalation owners, at most once per item per `reminderCooldownDays`.

```text
Create an AI workflow named "Daily sweep" on this site that runs every day at 6:00 AM Pacific time. For each run, load the site skill sweep-obligations from AgentAssets/Skills and follow it for the Obligations list. It may send reminder and escalation emails or Teams messages. Run as me.
```

## 4. Owner digest (`OWNER_DIGEST`)
- **Trigger:** schedule, every Monday at 8:00 AM.
- **Runs:** `obligation-owner-digest`.
- **Sends:** one digest to each owner with overdue items, items due soon or items due in the next 30 days. Owners with nothing due get nothing.

```text
Create an AI workflow named "Owner digest" on this site that runs every Monday at 8:00 AM Pacific time. For each run, load the site skill obligation-owner-digest from AgentAssets/Skills and follow it for the Obligations list. It may send each owner one email or Teams message. Run as me.
```

## 5. Leadership digest (`LEADERSHIP_DIGEST`)
- **Trigger:** schedule, every Friday at 3:00 PM.
- **Runs:** `obligation-leadership-digest`. It's read-only over Obligations and the Contracts columns.
- **Sends:** one email to `leadershipRecipients`, plus a Teams channel post if `leadershipTeamsChannel` is set.

```text
Create an AI workflow named "Leadership digest" on this site that runs every Friday at 3:00 PM Pacific time. For each run, load the site skill obligation-leadership-digest from AgentAssets/Skills and follow it. It may send one email to the leadership recipients in AgentAssets/Config/hub-settings.json and post to their Teams channel. Run as me.
```

---

## Change behaviour in settings, not prompts
- Thresholds and recipients: `AgentAssets/Config/hub-settings.json`.
- Who owns what: the Obligation Owners list.
- What gets tracked: the Obligation Types and Exclusions lists.

The workflows pick up changes on their next run. Keep the prompts short: the skills hold the logic, so a fixed skill fixes every workflow that uses it.
