---
name: faq-building
description: Builds structured FAQ pages from source material such as documents, process guides, policies, product descriptions, or topic briefs. Anticipates questions from the reader's perspective, groups them into themes, writes clear Q&A pairs, and delivers SharePoint-ready Markdown. Use when a user wants to create an FAQ from an existing document, prepare a help page for a new process or policy, or capture anticipated questions before a launch or rollout. Triggers include "create an FAQ from this", "build a FAQ page", "what questions will people ask about this", "turn this into a FAQ", or when a user wants to surface common questions from a document or topic.
---

# FAQ Building

This skill reads source material and produces structured FAQ pages from the reader's perspective — anticipating what people will actually ask, not just restating what the document says.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Before Starting: Establish Audience and Scope

**Who is asking these questions?**
The audience determines which questions appear and how answers are phrased. Ask if not specified:
- End users encountering a process or product for the first time?
- Employees navigating a policy or change?
- IT or admin personas with technical questions?
- Mixed audience?

**What is the source material?**
Confirm what the FAQ should be built from. Common inputs:
- A policy or procedure document
- A product or feature description
- A project brief or announcement
- A transcript or briefing

**Is there anything out of scope?**
If the source covers more than the FAQ should, confirm what to exclude. For example: "Build a FAQ for the new onboarding process only — not the broader HR policy."

If all three are clear from context, proceed without asking.

---

## Reading the Source: Question Mining

Work through the source with the reader's eye, not the author's. For each section or topic, generate candidate questions by asking:

**Confusion questions** — What in this section would a first-time reader misunderstand? Where is the wording ambiguous?

**"What about me?" questions** — What will readers wonder about their own situation? ("Does this apply to part-time employees?" "What if I already have an account?")

**Process questions** — How do I do this? What happens after? Who do I contact? What if something goes wrong?

**Exception questions** — What are the edge cases? What happens if the normal path doesn't apply?

**Policy and authority questions** — Who decides this? Can this be waived? Is this required or optional?

**Motivation questions** — Why are we doing this? Why does it work this way?

Collect all candidate questions before filtering. It is easier to cut good questions than to invent missing ones.

---

## Organizing the FAQ

Group questions into themes before writing answers. Good themes are:
- Recognizable to the reader (not just categories the author would use)
- Balanced in size — avoid one theme with twelve questions and another with one
- Ordered logically — general and orienting questions first, specific and edge-case questions later

Typical theme patterns:

**For process/procedure FAQs:** Overview → Getting Started → Day-to-Day Use → Troubleshooting → Contacts and Escalation

**For policy FAQs:** What Is This → Who Is Affected → What Changes → Exceptions and Edge Cases → What to Do Next

**For product/feature FAQs:** What Is It → How It Works → How to Get Access → Common Issues → Getting Help

Use the pattern that fits the content. Do not force content into a pattern that does not fit.

Aim for 5–15 questions total. Fewer than five suggests the source material is too thin; more than fifteen suggests the FAQ needs to be split into multiple pages or the questions need pruning.

---

## Writing Q&A Pairs

### Questions

Write questions in the voice of the reader, not the author. Use plain, natural language:
- "How do I request access?" not "What is the access request procedure?"
- "Do I need to do anything before the deadline?" not "What are the pre-deadline requirements?"
- "Can I still use the old system?" not "Is the legacy system still available?"

Use first or second person in questions: "I", "my", "you", "your". Questions starting with "What", "How", "Can", "Do", "When", and "Who" are almost always clearer than questions starting with "Is it possible to" or "In the event that".

### Answers

**Lead with the direct answer.** The first sentence should answer the question. Context and explanation follow.

**Be complete but not exhaustive.** An FAQ answer should resolve the question, not reproduce the source document. If the full answer requires the user to read a linked document, say so — but give them enough to orient first.

**Use the second person.** Write "You will need to..." not "Users are required to..."

**Acknowledge genuine complexity.** If an answer depends on the reader's situation, say so: "If you are a full-time employee, [X]. If you are a contractor, [Y]."

**End with a pointer when relevant.** If the user may need more than the answer provides, end with: "For more detail, see [link/document]" or "Contact [person/team] if your situation is not covered here."

---

## Output Structure

```
# Frequently Asked Questions: [Topic]

*Last updated: [Date if known]*

---

## [Theme 1 Name]

**[Question]**
[Answer]

**[Question]**
[Answer]

---

## [Theme 2 Name]

**[Question]**
[Answer]

---

## Still have questions?

[Contact information, escalation path, or link to additional resources — if available from source material]
```

Use bold for questions rather than heading levels. This renders cleanly in SharePoint and keeps the page scannable.

---

## Quality Checks

Before delivering, verify:

- Every question is written from the reader's perspective, not the author's
- Every answer leads with the direct response — no preamble
- Themes are logically ordered: general before specific, orienting before edge cases
- No question is a duplicate or near-duplicate of another
- No answer sends the reader to the source document without first giving them enough to orient
- "Still have questions?" section includes a real contact path if one exists in the source

---

## Output Format

Deliver:

1. **Complete FAQ page** — Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Coverage note** — A brief list of any questions that came up during question mining but were left out, and why (e.g., "Excluded questions about the legacy system — source material did not address it")
