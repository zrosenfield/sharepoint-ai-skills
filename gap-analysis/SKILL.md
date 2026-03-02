---
name: gap-analysis
description: Compares two documents or versions of content and surfaces what is missing, conflicting, changed, or new between them. Produces a structured gap analysis with categorized findings and a summary of implications. Use when a user wants to compare an old and new version of a document, check whether a spec matches an implementation, audit a policy for missing coverage, or identify what changed between two states. Triggers include "compare these two docs", "what's missing from this", "what changed between these versions", "find the gaps", "does this spec match this document", or when a user shares two documents and asks what is different or inconsistent.
---

# Gap Analysis

This skill compares two pieces of content and produces a structured analysis of what differs, what is missing, and what the gaps mean — written in plain language for practical use.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Before Starting: Establish the Comparison Frame

Gap analysis only works if both documents and the comparison direction are clear. Before proceeding, confirm:

**What are the two things being compared?**
Label them clearly from the start. Common pairs:
- Document A (old version) vs. Document B (new version)
- Specification vs. Current implementation description
- Policy vs. Procedure
- Plan vs. Retrospective

**Which is the reference?**
The reference is the document against which the other is measured. Usually: the spec, the standard, the newer version, or the authoritative source. The other document is the subject — the one being evaluated for gaps.

If the user has not specified which is the reference, ask. Getting this backwards produces a useless analysis.

**What is the purpose of the analysis?**
The framing shapes what counts as a gap. Ask if not clear:
- Find coverage gaps (what topics the subject is missing)?
- Find conflicts (where the two documents disagree)?
- Find changes (what is different between versions)?
- All of the above?

---

## Reading Both Documents

Read the reference document first. Build a mental map of its structure and scope:
- What topics does it cover?
- What claims or requirements does it make?
- What sections, components, or elements does it contain?

Then read the subject document. For each element of the reference, evaluate the subject:
- Is this element present?
- If present, does it agree with the reference, or does it differ?
- If it differs, is the difference material or cosmetic?

Also note any elements in the subject that have no counterpart in the reference — these may be additions or scope creep, depending on context.

---

## Four Gap Categories

Classify every finding into one of four categories:

**Missing** — Something in the reference is entirely absent from the subject. The subject makes no mention of it.

Example: The spec requires a data retention policy; the implementation document has no section on retention.

**Conflicting** — Both documents address the same topic, but they say different or incompatible things.

Example: The policy says approvals require two signatories; the procedure shows a single-signatory form.

**Changed** — The subject covers the same topic as the reference but with a meaningful difference in scope, detail, emphasis, or specificity. Not necessarily wrong — may be intentional.

Example: The new version of a process removes a validation step that appeared in the old version.

**Added** — Something appears in the subject that is not in the reference. Flag these for awareness — they may represent intentional additions or unreviewed scope expansion.

Example: The updated procedure includes a new escalation path not described in the policy.

---

## Severity Tagging

For each finding, assign a severity:

**High** — This gap creates ambiguity, risk, contradiction, or incomplete coverage that would block someone trying to follow the documents. Examples: a conflicting requirement, a missing approval step, a scope that no longer matches.

**Medium** — This gap is significant but not blocking. Examples: a topic that is covered in one document but not the other, a meaningful change in approach that is not explained.

**Low** — This gap is informational. Examples: a formatting inconsistency, a minor change in emphasis, an added section that is uncontroversial.

Do not inflate severity to appear thorough. A long list of low-severity gaps is less useful than a short list of high-severity ones.

---

## Output Structure

```
# Gap Analysis: [Reference Document] vs. [Subject Document]

**Reference:** [Document name/version]
**Subject:** [Document name/version]
**Analysis purpose:** [Coverage gaps / Conflicts / Changes / All]
**Date of analysis:** [Date]

---

## Summary

[Two to four sentences: how many gaps were found, which categories had the most, what the overall picture looks like. Lead with the most important finding.]

---

## High-Priority Gaps

| # | Category | Description | Reference location | Subject location |
|---|----------|-------------|-------------------|-----------------|
| 1 | Missing / Conflicting / Changed / Added | [Clear description of the gap] | [Section or element in reference] | [Section or element in subject, or "Not present"] |

---

## Medium-Priority Gaps

| # | Category | Description | Reference location | Subject location |
|---|----------|-------------|-------------------|-----------------|
| ... | ... | ... | ... | ... |

---

## Low-Priority Gaps

| # | Category | Description | Reference location | Subject location |
|---|----------|-------------|-------------------|-----------------|
| ... | ... | ... | ... | ... |

---

## Implications and Recommended Actions

[For each high-priority gap, one to two sentences on what action is needed. Medium gaps: one sentence each. Low gaps: summarize as a group.]

---

## What Was Not Compared

[Brief note on any sections, appendices, or topics that were excluded from the analysis and why. "Not applicable" if everything was in scope.]
```

Omit a priority section entirely if it has no findings.

---

## Writing Gap Descriptions

Every gap description should be:

**Specific** — Say exactly what is missing or conflicting, not just that something differs. "The subject does not include a rollback procedure" is better than "The subject is missing some operational content."

**Referenced** — Name the section or element in each document. "Section 3.2 of the reference requires X; the subject has no equivalent section" is more useful than "X is missing."

**Neutral** — Describe the gap, not a judgment about it. Some gaps are intentional; others are oversights. The analysis surfaces them; the decision about what to do belongs to the reader.

**Consequential** — For high and medium findings, one sentence explaining what the gap means in practice makes the analysis actionable. "Without a conflict resolution process, two teams following these documents could reach incompatible conclusions."

---

## Quality Checks

Before delivering, verify:

- The reference and subject are correctly identified — analysis is directional
- Every high-priority finding has a description specific enough that someone could address it without re-reading the source documents
- No findings are duplicated across categories
- The Implications section links back to the high-priority findings — no new gaps appear there
- The "What Was Not Compared" section is honest about scope

---

## Output Format

Deliver:

1. **Complete gap analysis** — Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Gap count by category** — A one-line summary: "Found X missing, Y conflicting, Z changed, W added — N high-priority"
