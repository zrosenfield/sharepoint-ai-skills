---
name: executive-summary
description: Distills long documents, reports, meeting transcripts, or briefing materials into tight one-page executive summaries formatted for SharePoint. Surfaces the core situation, key findings or decisions, recommendations, and what the reader needs to do or know. Use when a user wants to condense a long document for a leadership audience, create a TL;DR for a report, or produce a standalone summary someone can read in under two minutes. Triggers include "summarize this for leadership", "write an exec summary", "make this into a one-pager", "TL;DR this document", or when a user shares a long document and asks for a shorter version.
---

# Executive Summary

This skill distills long source material — documents, reports, transcripts, data briefings — into tight, standalone executive summaries for leadership or decision-making audiences. The output can be read in under two minutes and stands alone without the source.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Before Starting: Clarify Audience and Purpose

An executive summary is written for a specific reader with a specific need. Before drafting, establish two things:

**Who is reading this?**
Ask the user if they have not specified. The answer shapes tone, level of detail, and what counts as essential:
- Senior leadership (need: orient quickly, understand stakes, make a call)
- Peer colleagues (need: understand conclusions, check their own understanding)
- External stakeholders (need: see the key points without internal context)

**What do you need the reader to do?**
Every executive summary should leave the reader knowing what to do next. Ask if not clear from the source:
- Approve or reject something?
- Be informed and take no action?
- Prepare for a conversation or meeting?
- Act on a recommendation?

If both are clear from context, proceed without asking.

---

## Reading the Source Material

Work through the source in a single pass, tagging:

**The core situation** — What is this document about? What is the problem, opportunity, or question it addresses?

**Key findings or conclusions** — What does the source establish as true, confirmed, or resolved? For data reports: what the numbers show. For proposals: what was recommended. For meeting transcripts: what was decided.

**Recommendations or decisions** — What course of action is proposed or taken? If there are multiple options, which one is preferred and why?

**What the reader needs to know or do** — The ask. What action, approval, or awareness is this summary driving toward?

**Critical risks, caveats, or open questions** — Anything that could change the picture. Flag these even if they are buried in the source.

Discard everything that does not bear on one of these five categories. Background context earns its place only if the reader cannot understand the situation without it.

---

## Output Structure

Deliver the summary in this order. Every section must be short. If a section has nothing meaningful to say, omit it rather than padding.

---

### Header

```
# [Document Title or Topic] — Executive Summary

**Prepared from:** [Source document type, e.g. "Q3 Performance Report", "Design Review Transcript"]
**Date:** [Date of source or date of summary]
**Audience:** [Who this is written for]
**Purpose:** [What this summary asks the reader to do or know]
```

Fill in what is available. Mark unknowns as "[Not provided]".

---

### Situation

One to three sentences. What is happening, why it matters, and why the reader is looking at this now. This is context — not findings.

---

### Key Findings

The two to five most important things the source establishes. Write each as a clear, direct statement of fact or conclusion. Use a bulleted list.

Do not soften findings. "Revenue declined 18% in Q3" is better than "Revenue performance showed some softening in the third quarter."

---

### Recommendation (or Decision)

One to three sentences. What should happen next — or, for retrospective documents, what was decided. State it directly. If the source proposes multiple options, state which is recommended and the primary reason.

If the source presents options without a recommendation, list the options briefly and note that a decision is still needed.

---

### Risks or Open Questions

Optional. Include only if there are genuine risks or unresolved questions that would change the reader's response to the recommendation. Keep to two or three bullets. Label clearly: which are risks, which are open questions.

Omit this section if the situation is clear and the recommendation is unambiguous.

---

### Next Steps

What the reader needs to do, by when, and who else is involved. Write as a short bulleted list. If the only next step is "read the full document", that is not an executive summary — go back and find the actual ask.

---

## Length and Tone

**Target length:** 200–400 words for the body. If it runs longer, cut — every sentence that could be removed should be.

**Tone:** Clear, direct, confident. Write for a reader who is busy and senior. Avoid:
- Passive voice when the actor matters ("The team decided" not "It was decided")
- Hedging language that buries the point ("It may be worth considering...")
- Jargon without definition
- Preamble before the finding ("This document describes the results of a study that examined...")

**Tense:** Use present tense for current state and recommendations. Use past tense for completed events.

---

## Quality Checks

Before delivering, confirm:

- The summary can be read without the source document and still make complete sense
- Every section earns its place — nothing is filler
- The recommendation or decision is stated directly, not implied
- Risks are flagged honestly, not buried or omitted to make the summary look cleaner
- The reader knows exactly what to do after reading it

---

## Output Format

Deliver:

1. **Complete executive summary** — Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Source note** — One sentence indicating what was used as input and any gaps (e.g., "Summarized from Q3 report; financial appendix was not included in the source provided")
