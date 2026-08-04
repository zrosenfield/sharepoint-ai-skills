# Eval Guide for AI in SharePoint Skills

How to write eval criteria that actually improve your AI in SharePoint skills instead of giving you false confidence.

---

## The Golden Rule

Every eval must be a **yes/no question**. Not a scale. Not a vibe check. Binary.

Why: Scales compound variability. If you have 4 evals scored 1–7, your total score has massive variance across runs. Binary evals give you a reliable signal — especially important in AI in SharePoint where the same agent both generates and scores (no sub-agent isolation).

---

## Good Evals vs Bad Evals

### Tool-output skills (search, file operations, data retrieval)

**Bad evals:**
- "Did the tool return useful results?" (too vague)
- "Rate the relevance 1–10" (scale = unreliable)

**Good evals:**
- "Did the tool return at least one result that directly answers the user's question?" (binary, checkable)
- "Are all returned file names real files that exist in the source?" (binary, verifiable)
- "Did the tool handle the error case by returning a clear error message instead of crashing?" (binary, structural)

### Conversation skills (summarize, explain, draft)

**Bad evals:**
- "Is the response helpful?" (subjective)
- "Does it sound professional?" (vague)

**Good evals:**
- "Does the response directly address the user's stated question without changing the topic?" (binary, checkable)
- "Does the summary contain zero claims not present in the source material?" (binary, verifiable — hallucination check)
- "Is the response under 300 words?" (binary, measurable)
- "Does the response include at least one specific example, number, or quote from the source?" (binary, structural)

### Multi-step workflow skills (research, analysis, planning)

**Bad evals:**
- "Is the workflow complete?" (compared to what?)
- "Did it follow the steps?" (which steps, exactly?)

**Good evals:**
- "Does the output contain all required sections: [list them explicitly]?" (binary, structural)
- "Did the agent use at least 2 different tools/sources before synthesizing?" (binary, countable)
- "Does the final recommendation include a specific action with owner and timeline?" (binary, checkable)
- "Are there zero steps that reference information not gathered in a previous step?" (binary, logical consistency check)

### SharePoint-specific skills (site management, content operations)

**Bad evals:**
- "Did it work correctly?" (too broad)

**Good evals:**
- "Did the skill use the correct SharePoint API endpoint for the requested operation?" (binary, verifiable)
- "Does the output include source attributions with valid SharePoint URLs?" (binary, structural)
- "Did the skill handle the 'item not found' case without returning an unhandled error?" (binary, error handling check)

---

## Common Mistakes

### 1. Too many evals
More than 6 evals and the agent starts optimizing for the test instead of producing good output. Each additional eval dilutes focus.

**Fix:** Pick the 3–6 checks that matter most. If everything passes those, the output is probably good.

### 2. Too narrow / rigid
"Must contain exactly 3 bullet points" or "Must use the word 'because' at least twice" — these create skills that technically pass but produce weird, stilted output.

**Fix:** Evals should check for qualities you care about, not arbitrary structural constraints.

### 3. Overlapping evals
If eval 1 is "Does the response address the question?" and eval 3 is "Is the response relevant to the topic?" — these overlap heavily. You're double-counting the same quality.

**Fix:** Each eval should test something distinct. Map them out: one for accuracy, one for completeness, one for format, one for error handling — not two that both test "relevance."

### 4. Unmeasurable by the agent
"Would a user be satisfied?" — the agent can't reliably answer this. It'll say "yes" almost every time.

**Fix:** Translate subjective qualities into observable signals. "Satisfied" might mean: "Does the response contain a direct answer in the first sentence, not just a preamble?"

### 5. Evals that reward length
"Does the output thoroughly cover the topic?" almost always rewards verbosity. The agent will pad its output to pass.

**Fix:** Pair coverage evals with brevity evals: "Does the output cover X?" AND "Is the output under Y words?"

---

## AI in SharePoint-Specific Considerations

### Self-Scoring Bias
In Claude Code autoresearch, separate agents do execution and scoring. In AI in SharePoint, the same agent does both. This creates a bias toward passing.

**Mitigations:**
1. **Score before analyzing.** Write PASS/FAIL for each eval FIRST, then analyze patterns. Don't let the analysis influence the scoring.
2. **Require explicit evidence.** For each PASS, cite the specific part of the output that satisfies the eval. For each FAIL, cite what's missing or wrong.
3. **Default to FAIL on ambiguity.** When in doubt about whether an eval passes, score it as FAIL. This counteracts the natural bias toward PASS.
4. **Use concrete, greppable evals.** Evals like "contains zero TODO placeholders" are harder to mis-score than "is the code well-structured."

### Multi-Turn State
AI in SharePoint skills run across conversation turns, not in a single execution. This means:
- Eval results from early turns may fade from context in long conversations
- Keep running score summaries compact and structured
- Use the structured results format defined in the main skill to maintain state

---

## Designing Test Inputs

Evals are only as good as the inputs they're tested against.

**Every test input set must include a mix of:**

1. **1–2 typical/happy path inputs** — The skill's bread and butter. What it will see 80% of the time.
2. **1–2 edge cases** — Inputs that stress the skill: very short, very long, ambiguous, unusual format, or minimal context.
3. **1 adversarial input** — Something that commonly trips the skill up or that you *know* is hard.

**Examples by AI in SharePoint skill type:**

| Skill type | Happy path | Edge case | Adversarial |
|---|---|---|---|
| Summarize docs | "Summarize this 3-page report" | "Summarize a single sentence" | "Summarize 10 conflicting documents" |
| Search content | "Find files about Q3 budget" | "Search with a typo in query" | "Find files that were deleted last week" |
| Data analysis | "Chart monthly sales trends" | "Chart with only one data point" | "Chart with missing/null values in every row" |
| Site management | "Create a new page in the site" | "Create a page with special chars in title" | "Create a page when user has read-only permissions" |

If the user only provides happy-path inputs, push back. Ask: "What's the hardest input this skill has to handle? What input would you be most worried about getting wrong?"

---

## Template

Copy this for each eval:

```
EVAL [N]: [Short name]
Question: [Yes/no question about the output]
Pass: [What "yes" looks like — one sentence, specific]
Fail: [What triggers "no" — one sentence, specific]
```

Example:

```
EVAL 1: Direct answer
Question: Does the response contain a direct answer to the user's question in the first two sentences?
Pass: The opening sentences directly state the answer, fact, or recommendation the user asked for
Fail: The response starts with a preamble, hedge, or restates the question before answering
```

---

## The 3-Question Test

Before finalizing an eval, ask:

1. **Could two different agents score the same output and agree?** If not, the eval is too subjective. Rewrite it.
2. **Could the skill game this eval without actually improving?** If yes, the eval is too narrow. Broaden it.
3. **Does this eval test something the user actually cares about?** If not, drop it. Every eval that doesn't matter dilutes the signal from evals that do.
