---
name: improve-skills
description: Sets up persistent eval suites for any AI in SharePoint skill and runs self-healing improvement loops on demand. Use this when setting up evals for a skill for the first time, or when the user says "improve [skill-name]", "fix [skill-name]", or "run evals for [skill-name]" to fix a skill that has drifted, started failing, or needs to handle new patterns.
---

# Improve Skills — Self-Healing Skill Optimizer

This skill does two things:

1. **SETUP** — Walk through creating an eval suite for a target skill. The evals are saved permanently inside that skill's own `references/evals.md` so they're always there when you need them.
2. **IMPROVE** — Load those stored evals and run an iterative improvement loop, updating the skill in place when something better is found.

---

## Detect the Mode

Choose the mode based on what the user said and what already exists.

**Use SETUP when:**
- The user says "set up evals for [skill]", "I want to improve [skill] someday", or similar
- The target skill has no `references/evals.md` yet

**Use IMPROVE when:**
- The user says "improve [skill]", "fix [skill]", "run evals for [skill]", or simply "improve-skills"
- The target skill already has `references/evals.md`

If the mode is unclear, ask: "Do you want to set up evals for the first time, or run the improvement loop against existing evals?"

---

## SETUP Mode — One-Time Eval Walkthrough

Guide the user through five questions in sequence. Do not move to the next question until the current one is confirmed.

### Question 1: Target Skill

Ask which skill they want to set up evals for, and confirm the exact skill name.

Load the skill using `load_skill` so you can read it before continuing. Summarize what the skill does in two or three sentences so the user can confirm you understand it correctly.

### Question 2: Data Source

Explain that instead of fixed test cases, the skill will pull real items from a SharePoint library or list every time it runs. This keeps tests grounded in current data and lets the skill adapt as the content evolves.

Ask:

- **Which library or list** on this site contains the content this skill processes? (For example: "Meeting Recordings", "Proposals Library", "Posts".)
- **How should items be sampled?** Options: newest items (default), random selection, or the user hand-picks specific items each session.
- **How many items per session?** Default is three. Maximum is five. More than five overwhelms the conversation and slows the loop without adding meaningful signal.

If the user wants to provide sample text directly instead of pointing at a library, accept that — note it in the data source field as "user-provided samples" and remind them they will need to paste content at the start of each IMPROVE session.

**If the library is empty when IMPROVE runs later**, the skill must stop immediately, tell the user the library has no content, and ask them to either add real items or paste sample text to continue.

### Question 3: Eval Criteria

Explain that you need three to six binary yes-or-no checks that define what a good output looks like for this skill on this kind of content. Before writing evals, read two or three items from the data source so the evals are grounded in what the content actually looks like — not a hypothetical version of it.

Share these rules for writing good evals:

- **Binary only.** Every eval must be yes or no — no scales, no partial credit, no "mostly passes."
- **Specific enough to be consistent.** "Is the output good?" is too vague. "Does the output include a direct recommendation in the first paragraph?" is testable.
- **Not so narrow the skill games it.** Avoid checks that only measure length or surface formatting, because the skill will optimize for those at the expense of everything else.
- **Three to six is the sweet spot.** More than six and the skill starts parroting the eval criteria rather than actually improving.

For each eval, capture:
- **Name** — a short label used in the results table
- **Question** — the yes-or-no check, phrased as a question
- **Pass** — a specific description of what "yes" looks like
- **Fail** — what triggers "no"

Work collaboratively with the user to write these. Propose drafts based on your reading of the skill, then refine together.

### Question 4: Configuration

Ask three things:

- How many items should be sampled per session? (Default: 3. Max: 5.)
- How many times should the skill be run per mutation cycle? (Default: 3. More runs reduce noise but take longer.)
- Is there a cap on total experiment cycles? (Default: none — the loop runs until the score ceiling is hit or the user stops it.)

### Question 5: Confirm and Save

Present the complete eval suite in the format shown in `references/evals-template.md`. Read that file now so you use the correct format.

Ask the user to confirm or make corrections. Then save the eval suite by calling `create_skill` with the target skill name and the file path `references/evals.md`.

Tell the user: "Evals saved. Anytime you want to improve this skill, just say 'improve [skill-name]' and I'll load these evals and run the loop automatically."

---

## IMPROVE Mode — Self-Healing Loop

### Step 1: Load Everything

Load two things before proceeding:

1. The current version of the target skill using `load_skill`
2. Its eval suite using `load_skill` with the file path `references/evals.md`

Parse the eval suite to extract: the data source configuration, the eval criteria, the configuration (items per session, runs per experiment, budget cap), and the improvement history table.

If `references/evals.md` does not exist, tell the user and switch to SETUP mode.

### Step 2: Sample Live Data

Pull fresh items from the data source every session — do not reuse items from a previous run.

Read items from the library or list specified in `evals.md` using the configured sampling method (newest, random, or user-picks). Pull the configured number of items (default: three, max: five).

**If the library is empty:** Stop immediately. Tell the user the library has no content and ask them to either add items or paste sample text directly. Do not proceed until you have real input to work with.

**If the user provides sample text instead of a library:** Accept the pasted content as this session's inputs. Note that these are user-provided samples, not live library data.

Present the sampled items to the user with a brief summary of each (title and a one-sentence description of the content). Ask: "Are these representative of what this skill typically handles? If not, tell me what's missing and I'll adjust." Wait for confirmation before continuing.

### Step 3: Check Eval Relevance

Before running a single experiment, look at the sampled items and ask whether the stored evals still reflect what good output looks like for *this* content.

Check for:

- **Evals that no longer apply.** If the data has changed in a way that makes a stored eval untestable or irrelevant, flag it. Example: an eval checking for deadline extraction is meaningless if today's transcripts contain no dates.
- **Patterns the evals miss.** If you notice something consistently present in the live data that no eval captures — a structural element, a type of content, a failure mode visible just from reading the inputs — name it. Ask the user whether to add an eval for it.
- **Evals that need tightening.** If a stored eval was written for a simpler version of the content and the real data is now more complex, flag that the eval may be too easy to pass and may not catch real failures.

Present your assessment concisely: which evals still look right, which look stale, and what (if anything) seems missing. Ask the user to confirm, update, or leave the evals as-is before proceeding.

If evals are updated, save the revised `references/evals.md` before running the loop.

### Run the RALPH Loop

Each iteration of the loop follows five phases: Reason, Act, Look, Probe, Harden.

---

#### R — REASON

On the **first iteration** (baseline), do not mutate anything yet. State clearly that you are establishing a baseline with the unmodified skill. Confirm the eval suite with the user and ask them to flag any corrections before you begin scoring.

On **subsequent iterations**, review the failure patterns identified in the previous Probe phase. Identify the single highest-impact gap and form one mutation hypothesis. Do not try to fix multiple things at once — you cannot know what helped if you change several things simultaneously.

Present your reasoning:

- What gap are you targeting this iteration?
- What change do you think will fix it, and why?
- What type of mutation is it? (Adding an instruction, adding an anti-pattern, adding an example, tightening a constraint, or removing something that is causing harm.)

---

#### A — ACT

Apply the current skill's instructions to each sampled item and generate an output for each.

On iteration one, apply the unmodified skill exactly as written.
On subsequent iterations, apply the version with your mutation applied.

State each item's title or label clearly before generating its output so the results are easy to follow.

---

#### L — LOOK

Score every output against every eval criterion. Follow this scoring protocol exactly:

First, announce your bias before scoring: "I generated these outputs so I'm naturally biased toward passing them. I will score strictly and require explicit evidence for every pass."

Second, score all evals across all inputs before analyzing patterns. Do not let what you see in the pattern analysis change individual scores retroactively.

Third, require explicit evidence for every pass. You must cite the specific text in the output that satisfies the eval. "The output seems to address it" is not evidence. "The second sentence says X, which directly answers the question" is evidence.

Fourth, default to fail on ambiguity. If you are unsure whether an eval passes, score it as fail.

Present each scored output in this structure: the input label, then each eval with its verdict, the evidence you are citing, and a one-sentence reason. End each input's scores with its subtotal.

After all inputs are scored, present the aggregate total score and the percentage of the maximum possible score.

The maximum possible score equals the number of evals multiplied by the number of runs per experiment multiplied by the number of sampled items this session.

---

#### P — PROBE

Look across all scored outputs and identify failure patterns:

- Which eval is failing most consistently across inputs?
- Is the failure about formatting, a missing instruction, an ambiguous directive, or the skill doing too much or too little?
- Are there failure modes that the evals do not capture but that you noticed?

Identify one mutation to try next. Be specific about what part of the skill you would change and why you believe it will help.

If you have had three consecutive experiments targeting the same eval with no improvement, stop and try a fundamentally different mutation type. If adding instructions has not worked, try adding an example. If examples have not worked, try removing or simplifying something instead.

---

#### H — HARDEN

Decide whether to keep or discard this experiment's mutation.

**Minimum threshold to keep:** The score must improve by at least two points, or by at least ten percent relative to the previous best, whichever is smaller. A one-point gain across three runs is likely noise.

**Regression check:** Before keeping, check whether any individual eval dropped compared to the previous kept version. If any eval dropped by two or more points, flag it as a regression — even if the total score went up.

Apply these rules:
- Score improved by the minimum threshold with no regressions → keep
- Score improved by the minimum threshold with minor regressions → keep with a regression note
- Score improved by less than the minimum threshold → discard (likely noise)
- Score unchanged but the skill is now shorter or clearer → keep (simplification that holds score is a win)
- Score got worse → discard and revert to the previous version

If keeping: update your working version of the skill with the mutation applied.
If discarding: revert to the version before this mutation.

Present a compact experiment log entry and an updated running progress table after every experiment. See `references/evals-template.md` for the format.

---

### When to Stop the Loop

Stop the improvement loop when any of these conditions are met:

- **Score ceiling:** All evals are passing at ninety percent or better for two consecutive experiments
- **Budget cap:** The configured maximum number of experiments has been reached
- **Diminishing returns:** The score improved by fewer than two points across the last two experiments, and you have already run at least three experiments
- **User stops:** The user says stop, that's enough, looks good, or anything similar

---

### Save the Improved Skill

When the loop terminates:

1. Present the final results summary — baseline score, final score, and percent improvement
2. List the top changes that helped, in order of impact
3. List any evals that are still failing and what patterns remain
4. Ask the user to confirm before saving: "Ready to save the improved version?"
5. Save the improved skill by calling `create_skill` with the target skill name. This replaces the original — SharePoint versioning preserves the history so nothing is lost.
6. Append a new row to the improvement history table in `references/evals.md` and save it back using `create_skill`

---

## Important Constraints

- **One mutation per experiment.** Multiple simultaneous changes make it impossible to know what helped.
- **Binary evals only.** No scales, no partial credit, no "mostly passes."
- **Explicit evidence required for every pass.** No bare verdicts.
- **Default to fail on ambiguity.** This counteracts the natural bias toward passing output you generated yourself.
- **Never skip the baseline.** Even if the skill was improved recently, always run a fresh baseline before mutating.
- **Always sample fresh.** Never reuse items from a previous session — the whole point is testing against current data.
- **Never proceed with an empty library.** Stop and surface the problem to the user rather than falling back silently to hypothetical inputs.
- **Check eval relevance every session.** What success looks like changes as the data changes. An eval that was right six months ago may be wrong today.
- **Evals travel with the skill.** Always save the updated history and any revised evals back to `references/evals.md` at the end of every session.
- **The user can override any decision.** If they disagree with a keep or discard, follow their judgment.
