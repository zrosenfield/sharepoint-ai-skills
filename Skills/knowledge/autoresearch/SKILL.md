---
name: "autoresearch"
description: "Optimize any AI in SharePoint skill by iteratively running it against test inputs, scoring outputs with binary evals, mutating the prompt to fix failures, and keeping improvements. Adapts Karpathy's autoresearch methodology to AI in SharePoint's multi-turn conversation architecture."
metadata:
  author: "Marcus Markiewicz"
  version: "1.0"
  license: "MIT"
---

# Autoresearch for AI in SharePoint Skills

This skill adapts autonomous experimentation loops (Karpathy-style autoresearch) to AI in SharePoint. It doesn't rewrite the skill from scratch, but instwead runs it repeatedly, scoring every output, to improve it. Instead of spawning sub-agents on a local machine, we work within AI in SharePoint's multi-turn conversation using `load_skill` and `create_skill` as our read/write primitives.

---

## The Core Job

Take any existing AI in SharePoint skill, define what "good output" looks like as binary yes/no checks, then run an iterative loop that:

1. Applies the skill's instructions to test inputs and generates outputs
2. Scores every output against eval criteria (binary pass/fail)
3. Analyzes failure patterns and forms a mutation hypothesis
4. Mutates the skill prompt with ONE targeted change
5. Re-runs the skill, re-scores, and decides: keep or discard
6. Repeats until the score ceiling is hit or the user stops

**Output:** An improved skill (saved via `create_skill`) + a structured results log in conversation + a changelog of every mutation attempted.

---

## Before Starting: Gather Context

**STOP. Do not run any experiments until all fields below are confirmed with the user. Ask for any missing fields before proceeding.**

1. **Target skill** — Which skill do you want to optimize? (need the exact skill name as used in `load_skill`)
2. **Test inputs** — What 3–5 different prompts/scenarios should we test the skill with? These must include:
   - 1–2 **typical/happy path** inputs (the skill's bread and butter)
   - 1–2 **edge cases** (very short, very complex, ambiguous, or unusual inputs)
   - 1 **adversarial input** (something that commonly trips the skill up)

   If the user only provides happy-path inputs, push back: "What's the hardest input this skill has to handle?"

3. **Eval criteria** — What 3–6 binary yes/no checks define a good output? (see [references/eval-guide.md](references/eval-guide.md) for how to write good evals)
4. **Runs per experiment** — How many times should we apply the skill per mutation? Default: 3. (In AI in SharePoint, each run is a conversation turn, so 3 balances signal vs speed.)
5. **Budget cap** — Optional. Max number of experiment cycles. Default: no cap (runs until user stops or score ceiling hit).

---

## Step 1: Load and Understand the Target Skill

Before changing anything, load and understand the target skill completely.

1. Use `load_skill(skillName="<target>")` to read the full SKILL.md
2. If the skill references files in `references/`, load those too with `load_skill(skillName="<target>", filePath="references/<file>")`
3. Identify the skill's core job, process steps, and expected output format
4. Note any existing quality checks, anti-patterns, or constraints already in the skill

Do NOT skip this. You need to understand what the skill does before you can improve it.

**Save the original skill text in your working memory.** You'll need it as the baseline to revert to if mutations fail.

---

## Step 2: Build the Eval Suite

Convert the user's eval criteria into structured tests. Every check must be binary — pass or fail, no scales.

**Format each eval as:**

```
EVAL [N]: [Short name]
Question: [Yes/no question about the output]
Pass: [What "yes" looks like — be specific]
Fail: [What triggers "no"]
```

**Rules for good evals:**
- Binary only. Yes or no. No "rate 1–7" scales. Scales compound variability.
- Specific enough to be consistent. "Is the output good?" is too vague. "Does the output contain a direct answer in the first two sentences?" is testable.
- Not so narrow that the skill games the eval. "Contains fewer than 200 words" will make the skill optimize for brevity at the expense of everything else.
- 3–6 evals is the sweet spot. More than that and the skill starts parroting eval criteria instead of actually improving.

Load [references/eval-guide.md](references/eval-guide.md) for detailed examples and the 3-question test.

**Max score calculation:**
```
max_score = [number of evals] × [runs per experiment]
```

Example: 4 evals × 3 runs = max score of 12.

**Present the eval suite to the user for confirmation before proceeding.**

---

## Step 3: Establish Baseline

Run the skill AS-IS before changing anything. This is Experiment #0.

1. Ask the user what to name the optimized version (e.g., `summarize-email-v2`, `search-optimized`)
2. Apply the skill's instructions to each test input. For each:
   - State the test input clearly
   - Generate the output as the skill instructs
   - Present the output to the user
3. Score every output using the eval suite (see "How to Score" below)
4. Record the baseline results in the structured format (see "Results Format")

**CRITICAL: Score honestly.** You are both the generator and the scorer. Default to FAIL on ambiguity. Require explicit evidence for every PASS. See "Mitigating Self-Scoring Bias" below.

**After establishing baseline, confirm the score with the user.** If baseline is already 90%+, the skill may not need optimization — ask whether to continue.

---

## How to Score

Scoring is the most critical step. Because AI in SharePoint doesn't have separate scoring agents, you must be rigorous about self-scoring.

**For each output, score every eval:**

```
TEST INPUT: [the input used]

EVAL 1: [name] → PASS | FAIL
Evidence: [specific quote or observation from the output]
Reason: [one sentence explaining the verdict]

EVAL 2: [name] → PASS | FAIL
Evidence: [specific quote or observation]
Reason: [one sentence]

...

SCORE: [passed]/[total evals]
```

### Mitigating Self-Scoring Bias

Since you generated the output AND are scoring it, follow these rules strictly:

1. **Score ALL evals before analyzing patterns.** Write every PASS/FAIL first. Don't let pattern analysis influence individual scores.
2. **Require explicit evidence.** For every PASS, point to the exact text that satisfies the eval. "The output seems to address it" is NOT evidence. "The first sentence says 'The quarterly revenue was $4.2M' which directly answers the question" IS evidence.
3. **Default to FAIL on ambiguity.** If you're unsure whether an eval passes, score FAIL. This counteracts the natural bias toward PASS.
4. **Announce your bias risk.** Before scoring, state: "I generated this output, so I'm biased toward passing it. I will score strictly." This priming improves calibration.

---

## Step 4: Run the Experiment Loop

This is the core autoresearch loop.

**For each experiment:**

### 4a. Analyze Failures
Look at which evals are failing most. Identify the pattern:
- Is it a formatting issue?
- A missing instruction?
- An ambiguous directive?
- The skill doing too much (or too little)?

### 4b. Form a Hypothesis
Pick **ONE thing to change.** Don't change 5 things at once — you won't know what helped.

**Good mutations:**
- Add a specific instruction that addresses the most common failure
- Reword an ambiguous instruction to be more explicit
- Add an anti-pattern ("Do NOT do X") for a recurring mistake
- Embed high-priority content into sections the agent naturally generates first
- Add or improve an example that shows correct behavior
- Cap or constrain output sections to prevent bloat
- Remove an instruction that causes over-optimization for one thing at the expense of others

**Bad mutations:**
- Rewriting the entire skill from scratch
- Adding 10 new rules at once
- Making the skill longer without a specific reason
- Adding vague instructions like "make it better"
- Simply reordering sections (LLMs follow narrative flow, not section order)

### 4c. Apply the Mutation
State clearly what you changed and why:
```
MUTATION: [what changed — one sentence]
HYPOTHESIS: [why this should help — one sentence]
LOCATION: [which part of the skill was modified]
```

### 4d. Re-Run the Skill
Apply the mutated skill's instructions to the same test inputs. Generate new outputs.

### 4e. Re-Score
Score every output using the same eval suite and scoring protocol.

### 4f. Decide: Keep or Discard

**Minimum delta for keeping:** The improvement must be at least **2 points OR 10% relative improvement** (whichever is smaller) to count as real. A 1-point gain on 3 runs is likely noise.

**Regression check:** Before keeping, compare per-eval scores against the previous best. If ANY individual eval dropped by 2+ points compared to the previous kept version, flag it as a regression — even if the total score improved.

**Decision rules:**
- Score improved by ≥ minimum delta, no regressions → **KEEP**
- Score improved by ≥ minimum delta, with acceptable regressions → **KEEP with regression note**
- Score improved by < minimum delta → **DISCARD** (likely noise)
- Score stayed the same → **DISCARD**, unless the change simplifies the skill (fewer words, clearer structure). Simplification that maintains score is a win.
- Score got worse → **DISCARD**. Revert to the previous version.

### 4g. Log the Result
Record in the structured format (see "Results Format" below).

### 4h. Check for Stuck Directions
If you have **3 consecutive discards targeting the same eval**, stop. Either:
- Try a fundamentally different approach (if adding rules didn't work, try an example instead)
- Move on to improving a different eval
- Try removing or simplifying instructions instead of adding

### 4i. Repeat
Go back to step 4a.

**Continue until:**
- The user stops you
- You hit the budget cap
- You hit 90%+ pass rate for 2 consecutive experiments (diminishing returns)
- You run out of ideas after trying multiple approaches

---

## Advanced Mutation Strategies

Apply these when standard mutations (add instruction, add anti-pattern) aren't working.

### Embed, Don't Reorder
**Problem:** You need content to appear in the output, but it keeps getting truncated or skipped.
**What doesn't work:** Reordering sections. LLMs follow natural narrative flow, not arbitrary section ordering.
**What works:** Embed the high-priority content INTO a section the agent naturally generates first. Merge "Key Recommendation" into "Executive Summary." The agent always generates the opening — if critical content lives there, it can't be truncated.

### Output Truncation Fixes
When output gets cut off:
1. Embed, don't reorder (see above)
2. Cap tables — "Maximum 6 rows" prevents token-budget-consuming mega-tables
3. "Tables only, no prose" — prohibit explanatory paragraphs between tables
4. Specify cut priority — "If running long, cut rows from Section X first. NEVER cut Section Y."
5. Reduce total sections — merge related ones

### Constraint Tightening
When the skill's output is vague or inconsistent:
1. Replace adjectives with specifics — "brief" → "under 100 words"
2. Replace "should" with "MUST" for critical instructions
3. Add a worked example showing the exact expected output format
4. Add explicit anti-patterns with examples of what NOT to produce

---

## Results Format

After each experiment, present results in this structure:

```
═══════════════════════════════════════════
EXPERIMENT [N] — [KEEP / DISCARD]
═══════════════════════════════════════════

Mutation: [what was changed]
Hypothesis: [why this was expected to help]

Per-eval scores:
  EVAL 1 [name]:  [X]/[runs] (prev: [Y]/[runs]) [↑/↓/=]
  EVAL 2 [name]:  [X]/[runs] (prev: [Y]/[runs]) [↑/↓/=]
  ...

Total: [X]/[max] ([percent]%)  |  Previous best: [Y]/[max] ([percent]%)
Delta: [+/-N] points

Regressions: [list any evals that dropped, or "none"]
Decision: [KEEP/DISCARD] — [one sentence reason]

───────────────────────────────────────────
```

### Running Summary

After each experiment, also maintain a running summary table:

```
AUTORESEARCH PROGRESS — [skill name]
═══════════════════════════════════════════
Exp  Score   Rate    Status      Change
───  ─────   ────    ──────      ──────
 0   8/12    67%     baseline    (original)
 1   9/12    75%     KEEP        Added anti-hallucination rule
 2   9/12    75%     DISCARD     Tried output cap (no effect)
 3   11/12   92%     KEEP        Added worked example
═══════════════════════════════════════════
Best: 11/12 (92%)  |  Baseline: 8/12 (67%)  |  Improvement: +25%
```

---

## Step 5: Persist the Improved Skill

When the user is satisfied or the score ceiling is reached:

1. Present the final results summary (baseline → final score, experiments run, keep rate)
2. Show a diff summary of what changed from the original skill
3. Ask the user to confirm they want to save the optimized version
4. Use `create_skill` to save the improved version:
   ```
   create_skill(
     name="<user-chosen-name>",
     description="<updated description reflecting improvements>",
     instructions="<the optimized skill instructions>"
   )
   ```
5. The original skill is NEVER modified. The improved version is saved as a separate skill.

**Present the top 3–5 changes that helped most** (from the experiment log), so the user understands what improved and why.

---

## Step 6: Deliver Final Report

When the loop completes, present:

1. **Score summary:** Baseline → Final score (percent improvement)
2. **Total experiments:** How many mutations were tried
3. **Keep rate:** How many kept vs discarded
4. **Top changes that helped most**
5. **Remaining failure patterns** (what the skill still gets wrong, if anything)
6. **Regressions:** Any evals that got worse during optimization
7. **The improved skill name** (as saved via `create_skill`)
8. **Recommendation:** Whether the user should replace the original or keep both

---

## Context Management

Long optimization sessions will accumulate conversation history. Follow these rules:

1. **Keep score summaries compact.** Use the structured table format, not prose.
2. **Don't re-state the full skill text every turn.** Reference it by name. Only show the mutated portion.
3. **Summarize, don't quote.** When analyzing failures, write a 1–2 sentence summary of the pattern, not the full output.
4. **If the conversation gets long,** present a handoff summary:
   ```
   HANDOFF SUMMARY
   ═══════════════
   Skill: [name]
   Current best score: [X]/[max] ([percent]%)
   Experiments completed: [N]
   Current version: [describe the latest kept mutation]
   Top 3 failing evals: [list with what's been tried for each]
   Last 3 experiments: [keep/discard and why]
   Next to try: [suggestion]
   ```
   Then tell the user: "Start a new conversation, load the autoresearch skill, and paste this summary to continue."

---

## Example: Optimizing a Search-Content Skill

**Setup:**
- Target skill: `search-content`
- Test inputs:
  - Happy path: "Find documents about Q3 budget review"
  - Happy path: "Search for onboarding guides"
  - Edge case: "Find files" (minimal query, no topic specified)
  - Adversarial: "Find the email John sent about the thing last Tuesday"
- Evals:
  1. Returns at least one relevant result? (relevance)
  2. All source attributions have valid URLs? (accuracy)
  3. Handles error/empty cases gracefully? (robustness)
  4. Response under 500 words? (brevity)
- Runs per experiment: 3
- Max score: 12

**Baseline (Experiment 0):**
Applied skill to all 4 inputs × 3 runs. Result: 8/12 (67%).
Per-eval: Relevance 3/3, URLs 2/3, Error handling 1/3, Brevity 2/3.
Common failures: Edge case "Find files" returns results but no error guidance. Adversarial input produces hallucinated results.

**Experiment 1 — KEEP (10/12, 83%):**
Mutation: Added "When the query is vague or lacks specifics, ask a clarifying question before searching. Do NOT guess what the user means."
Per-eval: Relevance 3/3, URLs 2/3, Error handling **3/3** (+2), Brevity 2/3.
Delta: +2 points. No regressions. Error handling went from 1/3 to 3/3.

**Experiment 2 — DISCARD (10/12, 83%):**
Mutation: Added "Always validate URLs exist before including in response."
Per-eval: Relevance 3/3, URLs **3/3** (+1), Error handling 3/3, Brevity **1/3** (-1 regression).
Delta: 0 net (one up, one down). URL validation instruction made responses longer. Discarded.

**Experiment 3 — KEEP (11/12, 92%):**
Mutation: Added anti-pattern: "NEVER fabricate file names, URLs, or metadata. If search returns no results, say so directly — do not invent plausible-sounding results."
Per-eval: Relevance 3/3, URLs **3/3** (+1), Error handling 3/3, Brevity 2/3.
Delta: +1 point, but this was the URLs eval going from 2→3 consistently. No regressions. Kept.

**Final:** Baseline 8/12 (67%) → Final 11/12 (92%). 3 experiments, 2 kept. Saved as `search-content-v2`.

---

## Important Constraints

- **Never modify the original skill.** The optimized version is always saved as a new skill via `create_skill`.
- **One mutation per experiment.** Multiple changes make it impossible to know what helped.
- **Binary evals only.** No scales, no "mostly passes," no partial credit.
- **Evidence required for every score.** No bare PASS/FAIL without citing specific output text.
- **Default to FAIL on ambiguity.** This counteracts self-scoring bias.
- **The user can override any decision.** If they disagree with a keep/discard, follow their judgment.
