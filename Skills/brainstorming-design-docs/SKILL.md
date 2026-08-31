---
name: brainstorming-design-docs
description: Guides a raw idea through structured brainstorming into a fully fleshed-out design document formatted for SharePoint. Asks clarifying questions one at a time, proposes alternative approaches with trade-offs, builds the design incrementally with user approval, then delivers a complete SharePoint-ready document. Use when a user wants to develop an idea, proposal, project plan, or initiative into a structured doc. Triggers include "help me think through this", "turn this idea into a design doc", "I want to design a new [process/project/feature/solution]", "brainstorm this with me", or when a user describes a rough idea and wants to make it concrete.
---

# Brainstorming to Design Doc

This skill runs a structured dialogue that takes a raw idea and builds it into a complete design document through collaborative, incremental development. Every section gets user approval before moving forward — no surprises at the end.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Core Principles

- **Ask one question at a time.** Work through clarifications sequentially — each answer shapes the next question.
- **Prefer multiple choice.** Offer 2–4 options where possible rather than open-ended questions.
- **Propose alternatives before committing.** Generate two or three approaches with trade-offs, recommend one, get buy-in.
- **Cut scope ruthlessly.** Only what the idea needs now. "Nice to have" goes in Open Questions.
- **Validate incrementally.** Present one section at a time, confirm each before moving on.

---

## The Process

### Phase 1 — Understand the Idea

Start here every time. Ask the user to describe the idea in their own words — one or two sentences. Do not ask follow-up questions yet. Let them give the raw version.

Then ask clarifying questions one at a time to establish:

- **Type of initiative.** Is this a new project, a process change, a product or feature proposal, a content strategy, a solution design, or something else?
- **Problem or opportunity.** What situation is this responding to? What happens today that this changes or improves?
- **Primary audience.** Who will read this doc? (Decision-makers who need to approve it, a team who will build it, or future operators who will maintain it?) This determines the level of detail and the sections to include.
- **Constraints.** Deadlines, budget, technology, team size, existing systems that must be respected?
- **Success criteria.** How will anyone know this worked? What is measurably or observably different six months after this is live?

Stop and confirm your understanding before moving to Phase 2. Summarize the idea back to the user in two to three sentences and ask if the summary is accurate.

---

### Phase 2 — Propose Approaches

Generate **two or three distinct approaches** to the problem or goal. For each approach, describe:

- The core mechanism — how it works at a high level
- The main advantage — what makes this approach attractive
- The main trade-off — what it costs, risks, or sacrifices
- Who it works best for — under what constraints or priorities this approach shines

After presenting the options, make a recommendation and explain the reasoning briefly. Then ask the user which approach to develop, or whether they want a hybrid.

Do not skip this phase even if the idea seems to point toward one obvious solution. Exploring alternatives surfaces hidden assumptions and strengthens the final design.

---

### Phase 3 — Build the Design Doc

Work through the design document one section at a time. After completing each section, share it and ask for one of three responses:

- **Approved** — proceed to the next section
- **Revise** — make changes before moving on
- **Skip** — this section isn't needed for this document

Scale section depth to complexity. Straightforward items get two to four sentences. Nuanced topics that require decision-making or involve risk get more detail. Never pad a simple section to look thorough.

**Standard sections** (see [sections-reference.md](sections-reference.md) for detailed guidance on each):

1. Executive Summary — one paragraph; written last, presented first
2. Problem or Opportunity — current state, why it matters, cost of inaction
3. Goals and Success Criteria — pair each goal with an observable criterion
4. Proposed Approach — selected approach from Phase 2, elaborated
5. Alternatives Considered — approaches not selected and why
6. Scope — explicit in-scope and out-of-scope lists
7. Stakeholders and Dependencies — who is involved, affected, or blocking
8. Risks and Mitigations — top risks paired with mitigations
9. Timeline and Phases — phased breakdown with approximate milestones
10. Open Questions and Decisions Needed — who needs to answer what

---

### Phase 4 — Finalize and Deliver

Once all sections are approved:

1. Write the Executive Summary using the full picture from the completed design.
2. Assemble the full document in the order below.
3. Deliver the complete design doc as SharePoint-ready markdown.
4. List any open questions that need to be resolved before the initiative advances.

If the user wants the document formatted and structured for a specific SharePoint context (wiki, knowledge base, project page), offer to apply the `authoring-sharepoint-markdown` skill to the final output.

---

## Standard Document Order

When assembling the final document, use this section order:

1. Executive Summary
2. Problem or Opportunity
3. Goals and Success Criteria
4. Proposed Approach
5. Alternatives Considered
6. Scope
7. Stakeholders and Dependencies
8. Risks and Mitigations
9. Timeline and Phases
10. Open Questions and Decisions Needed

Omit sections that were skipped during Phase 3. Do not add placeholder headers for sections with no content.

---

## What to Skip and When

Not every design needs every section. Apply judgment:

- **Short-lived or low-stakes initiatives:** Combine Problem, Goals, and Approach into a single narrative section; omit Alternatives Considered and Timeline.
- **Well-scoped technical designs:** Emphasize Scope, Dependencies, and Risks; keep Executive Summary short.
- **Decision memos:** Lead with the Options (from Phase 2) and the Recommendation; compress everything else.
- **Process redesigns:** Emphasize the current-state problem and the before/after contrast; use tables to compare old and new process steps.

If none of the above fits, use the full standard order.

