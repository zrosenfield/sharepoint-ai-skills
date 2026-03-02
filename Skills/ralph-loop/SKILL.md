---
name: ralph-loop
description: A self-evaluating iterative agent loop that pursues a goal through structured cycles of Reason, Act, Look, Probe, and Harden until the goal is confidently achieved. Use when a task requires iterative refinement, quality assurance, or when "good enough" isn't good enough. Works for any goal — document generation, data extraction, content processing, analysis, or creative work.
---

# RALPH Loop — Relentless Agentic Loop for Pursued Hardening

## Overview

RALPH is an iterative execution pattern where Claude pursues a goal through structured cycles, self-evaluating after each iteration and only stopping when it is genuinely confident the goal has been fully achieved — or when it has exhausted its configured iteration budget.

The loop is designed to prevent the common failure mode of "close enough" — where an agent produces a reasonable first attempt and stops, leaving gaps, inconsistencies, or missed requirements that a more careful pass would catch.

## The RALPH Cycle

Each iteration follows five phases:

```
┌─────────────────────────────────────────────────┐
│  R  →  A  →  L  →  P  →  H                     │
│  │     │     │     │     │                      │
│  │     │     │     │     └─ HARDEN              │
│  │     │     │     │        Decide: DONE or     │
│  │     │     │     │        loop back to R      │
│  │     │     │     │                            │
│  │     │     │     └─── PROBE                   │
│  │     │     │          Find specific gaps,     │
│  │     │     │          weaknesses, omissions   │
│  │     │     │                                  │
│  │     │     └───────── LOOK                    │
│  │     │                Examine output against  │
│  │     │                success criteria        │
│  │     │                                        │
│  │     └─────────────── ACT                     │
│  │                      Execute the plan,       │
│  │                      produce/refine output   │
│  │                                              │
│  └───────────────────── REASON                  │
│                         Decompose goal,         │
│                         define success criteria, │
│                         plan approach            │
└─────────────────────────────────────────────────┘
```

### Phase Details

#### R — REASON (Iteration 1: Goal Decomposition | Iteration 2+: Gap-Targeted Replanning)

**First iteration:**
- Parse the user's stated goal into a clear, unambiguous objective
- Decompose the goal into **success criteria** — concrete, evaluable conditions that must ALL be true for the goal to be considered achieved
- Each criterion should be specific enough to score on a 1–10 scale
- Plan the execution approach (tools, sequence, dependencies)
- Identify what "done" looks like — the acceptance threshold

**Subsequent iterations:**
- Review the gaps identified in the previous PROBE phase
- Replan specifically to address those gaps
- Do NOT restart from scratch — build on what's already been produced
- Prioritize the lowest-scoring criteria from the previous evaluation

**Output a structured plan:**
```
ITERATION [N] — REASON PHASE
=============================
Goal: [restated goal]
Success Criteria:
  1. [criterion] — [what "10/10" looks like]
  2. [criterion] — [what "10/10" looks like]
  ...
Plan: [what this iteration will do]
Focus Areas: [gaps from previous iteration, or "initial execution" if iteration 1]
```

#### A — ACT (Execute the Plan)

- Execute the plan from the REASON phase
- Use whatever tools are needed (file creation, web search, computation, etc.)
- Produce tangible output (files, content, data, analysis)
- On iteration 2+, modify/enhance existing output rather than regenerating from scratch (unless the PROBE phase determined a fundamental approach change is needed)

#### L — LOOK (Evaluate Against Criteria)

- Examine the output produced in the ACT phase
- Score EACH success criterion on a 1–10 scale
- Be brutally honest — this is where most agents fail by being too generous with themselves
- A score of 10 means "I would bet my reputation that this criterion is perfectly met"
- A score of 7-8 means "solid but there's room for improvement"
- A score below 7 means "this needs more work"

**Output a structured evaluation:**
```
ITERATION [N] — LOOK PHASE
============================
Criterion Scores:
  1. [criterion]: [score]/10 — [brief justification]
  2. [criterion]: [score]/10 — [brief justification]
  ...
Overall Confidence: [weighted average]/10
```

**Scoring calibration guide:**
- 10/10: Flawless. No possible improvement. Would pass expert review.
- 9/10: Excellent. Minor stylistic preferences might differ but substance is complete.
- 8/10: Very good. One small gap or imperfection that most people wouldn't notice.
- 7/10: Good. Meets the requirement but has a noticeable weakness.
- 6/10: Acceptable. Gets the job done but clearly could be better.
- 5/10 or below: Needs significant work. Do not consider stopping.

#### P — PROBE (Find the Gaps)

- For any criterion scoring below the completion threshold, identify EXACTLY what's missing or weak
- Be specific — "the introduction could be better" is useless; "the introduction doesn't establish the business context for the recommendation" is actionable
- Consider edge cases, unstated requirements, and quality dimensions the criteria might not fully capture
- Ask: "If I handed this to the user right now, what would they push back on?"

**Output a structured gap analysis:**
```
ITERATION [N] — PROBE PHASE
=============================
Gaps Found:
  - [Criterion N]: [specific, actionable description of what's missing]
  - [Criterion M]: [specific, actionable description of what's weak]
  ...
Unstated Issues: [anything not captured by criteria but still problematic]
Verdict: [CONTINUE | COMPLETE]
```

#### H — HARDEN (Decide: Done or Iterate)

Apply the completion rules (see below) to determine whether to:
1. **COMPLETE** — Declare the goal achieved, present final output to the user
2. **ITERATE** — Feed the gaps from PROBE back into the next REASON phase

If completing: Present the output with a brief summary of the iterations taken and final confidence scores.
If iterating: Proceed immediately to the next REASON phase with the gap analysis as input.

---

## Completion Rules

The loop terminates when ANY of these conditions are met:

### 1. Confidence Threshold Reached
- ALL criteria score at or above the **completion threshold**
- Default threshold: **9/10**
- Configurable per goal (see Configuration section)

### 2. Max Iterations Reached
- The loop has executed the maximum allowed iterations
- Default: **5 iterations**
- Configurable per goal
- When hitting the cap: Present the best output achieved with honest assessment of remaining gaps

### 3. Diminishing Returns Detected
- The overall confidence score improved by less than **0.5 points** between iterations
- AND the loop has run at least 2 iterations
- This prevents infinite loops on goals where perfection isn't achievable
- When triggered: Explain to the user what's plateauing and why

### 4. Fundamental Blocker Identified
- The PROBE phase identifies an issue that cannot be resolved within the current context (e.g., missing data, tool limitations, ambiguous requirements needing user input)
- When triggered: Present current best output and clearly state what's blocking further progress

---

## Configuration

RALPH can be configured per goal by specifying parameters at the start:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_iterations` | 5 | Hard cap on iteration count |
| `completion_threshold` | 9 | Minimum score (1-10) ALL criteria must reach |
| `strictness` | `high` | `low` (7+), `medium` (8+), `high` (9+), `perfectionist` (10) |
| `verbose` | `true` | Whether to output phase logs (set false for cleaner output) |

**To configure**, the user can say things like:
- "Use RALPH with max 3 iterations" → `max_iterations=3`
- "RALPH this but keep it quick" → `max_iterations=3, strictness=medium`
- "RALPH this to perfection" → `strictness=perfectionist, max_iterations=8`
- "RALPH this" → all defaults

---

## Usage Pattern

When the user invokes RALPH (or when the skill determines RALPH is appropriate), follow this sequence:

### Step 1: Acknowledge and Configure
```
Starting RALPH loop.
Goal: [user's goal]
Configuration: [max_iterations] iterations | threshold: [completion_threshold]/10
```

### Step 2: Execute the Loop
Run RALPH cycles. On each iteration, output the phase logs (if verbose=true) so the user can see the agent's reasoning.

### Step 3: Present Results
When complete, present:
- The final output/deliverable
- A completion summary:
```
RALPH COMPLETE
==============
Iterations: [N] of [max]
Final Confidence: [score]/10
Criteria Met: [N]/[total] at threshold
Termination Reason: [threshold reached | max iterations | diminishing returns | blocker]
```

---

## Anti-Patterns to Avoid

1. **Generous self-scoring**: The most common failure. If in doubt, score LOWER. A 9 should mean you'd genuinely be surprised if the user found a problem with that criterion.

2. **Cosmetic iterations**: Don't waste iterations on formatting tweaks when substance is lacking. Prioritize the lowest-scoring criteria.

3. **Scope creep**: Each iteration should address identified gaps, not invent new requirements. Stick to the success criteria defined in iteration 1 (though PROBE can surface unstated issues that are genuinely important).

4. **Restarting from scratch**: Unless PROBE identifies a fundamental approach problem, iterate on existing output rather than regenerating. Build, don't rebuild.

5. **Ignoring diminishing returns**: If the score barely moved, don't keep grinding. Present what you have and explain the plateau.

---

## Examples of RALPH in Action

### Example 1: Document Generation
```
User: "RALPH: Create a project status report for the SharePoint AI initiative"

RALPH would:
- R: Define criteria (executive summary clarity, data accuracy, completeness of milestones, actionable next steps, appropriate tone)
- A: Generate the report
- L: Score each criterion honestly
- P: "Executive summary buries the lead — revenue impact should be sentence 1, not paragraph 3"
- H: Continue → feed gap back
- R2: Replan to restructure executive summary
- A2: Revise the report
- L2: Re-score — all criteria now 9+
- H2: COMPLETE
```

### Example 2: Data Extraction
```
User: "RALPH: Extract all recipes from these uploaded documents and validate completeness"

RALPH would:
- R: Define criteria (all recipes found, ingredients complete, instructions parseable, measurements standardized, edge cases handled)
- A: Extract recipes
- L: Score — finds 3 recipes missed from a multi-column page
- P: "Multi-column layout caused parser to skip items. Also, 2 recipes have vague measurements like 'a pinch'"
- H: Continue
- ... iterate until extraction is validated
```

### Example 3: Analysis Task
```
User: "RALPH with max 3 iterations: Analyze our competitive landscape in the AI agent space"

RALPH would:
- R: Define criteria (market coverage, competitor accuracy, strategic insight depth, actionable recommendations)
- A: Research and produce analysis
- L: Score honestly
- P: Find gaps in coverage or depth
- H: Iterate up to 3 times, then present best result with honest gap assessment
```

---

## Integration Notes

- RALPH works with any other skill — it's a meta-pattern that wraps around execution
- The ACT phase can invoke any tools or skills needed
- RALPH logs can be saved to files for audit trails if needed
- The pattern works for both simple tasks (2 iterations) and complex tasks (5+ iterations)
- When used inside SharePoint workflows, RALPH can leverage SPO tools during the ACT phase and validate against SharePoint-specific quality criteria
