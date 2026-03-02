---
name: brainstorming-design-docs
description: Guides a raw idea through structured brainstorming into a fully fleshed-out design document formatted for SharePoint. Asks clarifying questions one at a time, proposes alternative approaches with trade-offs, builds the design incrementally with user approval, then delivers a complete SharePoint-ready document. Use when a user wants to develop an idea, proposal, project plan, or initiative into a structured doc. Triggers include "help me think through this", "turn this idea into a design doc", "I want to design a new [process/project/feature/solution]", "brainstorm this with me", or when a user describes a rough idea and wants to make it concrete.
---

# Brainstorming to Design Doc

This skill runs a structured dialogue that takes a raw idea and builds it into a complete design document through collaborative, incremental development. Every section gets user approval before moving forward — no surprises at the end.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Core Principles

**Ask one question at a time.** Asking multiple questions at once creates cognitive load and produces vague answers. Work through clarifications sequentially — each answer shapes the next question.

**Prefer multiple choice.** When asking clarifying questions, offer 2–4 options where possible. "Which of these best describes your goal: (a) reduce manual work, (b) improve visibility for stakeholders, or (c) standardize how teams do X?" gets a better answer than "what is your goal?"

**Propose alternatives before committing.** Never design toward a single solution from the start. Generate two or three distinct approaches, present their trade-offs, and recommend one — then get buy-in before building out the detail.

**Cut scope ruthlessly.** Only include what the idea actually needs right now. If a feature, section, or requirement sounds like "it would also be nice to..." it belongs in an open questions section, not in the design.

**Validate incrementally.** Present the design one section at a time and confirm each before moving to the next. A surprise at section six wastes the work of sections two through five.

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

**Standard sections and their purpose:**

**Executive Summary**
One paragraph. States the problem, the proposed solution, and the expected outcome. Written last but presented first in the document — draft a placeholder and return to finalize it once the full design is clear.

**Problem or Opportunity**
Describes the current state: what is happening today, why it is a problem or a missed opportunity, and what the cost of inaction is. Grounded in specifics, not generalities.

**Goals and Success Criteria**
Distinguishes between goals (directional statements of intent) and success criteria (observable or measurable conditions that confirm a goal was met). Pairs each goal with at least one criterion. Cuts goals that cannot be paired with a criterion — they are wishes, not goals.

**Proposed Approach**
The selected approach from Phase 2, elaborated in detail. Covers the key components, how they interact, what happens at each stage, and how the approach addresses the problem.

**Alternatives Considered**
A brief record of the approaches from Phase 2 that were not selected, and why they were set aside. Keeps the document honest and prevents second-guessing later.

**Scope**
Two explicit lists: what is in scope, and what is out of scope. Out-of-scope items are as important as in-scope ones — capturing what this does NOT do prevents scope creep and sets expectations.

**Stakeholders and Dependencies**
Who is involved, who is affected, and who needs to approve or be informed. Identifies any external teams, systems, or decisions this initiative depends on.

**Risks and Mitigations**
The two or three most significant risks, each paired with a mitigation. Risks without mitigations are concerns, not risk entries — if there is no mitigation, note it as an open question instead.

**Timeline and Phases**
A phased breakdown of how this will be executed, with approximate milestones. Does not have to be a precise schedule — directional phases with relative timing ("Phase 1: 4–6 weeks") are enough at the design stage.

**Open Questions and Decisions Needed**
Any unresolved questions, deferred decisions, or items that require input from specific people before implementation can begin. Each entry should identify who needs to answer it.

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

---

## Anti-Patterns to Avoid

**Solving before understanding.** Do not propose approaches or draft any section until Phase 1 is complete and the summary is confirmed.

**Presenting a single approach.** Even when one solution is obvious, propose at least two alternatives. The comparison itself is valuable — it shows the decision was considered.

**Bundling questions.** "What is the problem, who is the audience, and what are the constraints?" is three questions. Ask one. Get the answer. Then ask the next.

**Vague success criteria.** "Improve collaboration" is not a success criterion. "Teams can find relevant documents without asking in chat" is. Push until each goal has a concrete, observable test.

**Designing for every possible future.** Only document what the current initiative will actually do. Features that might be added later go in Open Questions, not in Scope.
