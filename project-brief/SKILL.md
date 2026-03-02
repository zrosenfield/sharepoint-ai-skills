---
name: project-brief
description: Turns a rough idea, stakeholder request, or email thread into a structured project brief with a clear problem statement, goals, success criteria, scope, stakeholders, and risks. Asks clarifying questions one at a time to fill gaps, then delivers a complete SharePoint-ready brief. Use when a user wants to scope a new project, formalize a request that came in through email or conversation, or create a brief before moving into full design or planning. Triggers include "write a project brief", "turn this email into a brief", "help me scope this project", "I need to document this request", or when a user describes a rough idea and wants a structured starting point.
---

# Project Brief

This skill takes a rough project idea or stakeholder request and turns it into a structured, decision-ready brief. It asks targeted questions to fill gaps, then delivers a document that defines scope, goals, and context clearly enough to move into planning or approvals.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Core Principles

**Ask one question at a time.** A project brief requires specific information. Asking everything at once produces vague answers. Work sequentially — each answer shapes the next question.

**A brief is not a design doc.** A project brief defines what and why, not how. Keep implementation details out unless they directly affect scope or feasibility. The design comes later.

**Force choices.** Vague goals and undefined scope are the most common brief failures. Push until each goal has a success criterion and every scope boundary is explicit.

---

## The Process

### Phase 1 — Understand the Request

Ask the user to describe the project or request in their own words. Do not prompt with structure yet — let them give the raw version.

Then ask clarifying questions one at a time to establish:

**The trigger.** What created this project? A problem that surfaced, an opportunity identified, a stakeholder ask, a regulatory requirement? Understanding the trigger shapes everything else.

**The problem or opportunity.** What is happening today that this project changes or improves? What is the cost of doing nothing?

**The requester and primary owner.** Who is asking for this? Who will own it once it is underway? These may be different people.

**The intended audience or beneficiary.** Who does this project serve? Whose work or experience changes as a result?

**The timeline or urgency.** Is there a hard deadline? A soft target? No date yet? Knowing this determines how much detail the brief needs to support.

Stop and confirm your understanding before moving to Phase 2. Summarize the request in two to three sentences and ask if that captures it accurately.

---

### Phase 2 — Establish Goals and Success Criteria

Ask the user to state the goals of the project. Then for each goal, ask: "How will you know this goal was achieved?"

Push past vague goals. When a goal is not testable, say so and offer a more specific version:
- "Improve collaboration" → "Teams can find shared documents without asking in chat"
- "Reduce manual work" → "The approval process takes under 10 minutes per request, down from 45"
- "Better visibility" → "Leadership can see project status without requesting a status update"

If the user cannot articulate a success criterion for a goal, put the goal in the Open Questions section rather than in Goals. Untestable goals are not goals — they are intentions.

---

### Phase 3 — Define Scope

Scope in and scope out are equally important. Ask explicitly about both.

**In scope:** What will this project produce, cover, or change? Be specific about deliverables, systems, teams, or processes involved.

**Out of scope:** What will this project explicitly not address, even if related? List items people might assume are included but are not. Out-of-scope items prevent future misunderstandings.

**Dependencies:** What does this project require from other teams, systems, or decisions before it can proceed or complete?

---

### Phase 4 — Identify Stakeholders and Risks

**Stakeholders:** Who needs to be informed, involved, or consulted? Who has approval authority? Who might block or slow the project?

**Risks:** What could prevent this project from succeeding? What assumptions is the brief making that could prove false? Keep to the two or three most significant risks. Each risk should be paired with a mitigation or flagged as an open question if no mitigation is known.

---

## Output Structure

Assemble the brief in this order:

```
# Project Brief: [Project Name]

**Date:** [Date]
**Requested by:** [Name and role]
**Owner:** [Name and role]
**Status:** Draft

---

## Problem or Opportunity

[Two to four sentences: what is happening today, why it matters, what the cost of inaction is.
Grounded in specifics, not generalities.]

---

## Goals and Success Criteria

| Goal | Success Criterion |
|------|------------------|
| [Goal stated as an outcome] | [How you will know it was achieved] |
| [Goal stated as an outcome] | [How you will know it was achieved] |

---

## Proposed Approach

[Optional at brief stage — include only if a direction has already been decided or if there is
an obvious and uncontroversial path. If approach is still open, omit and note it in Open Questions.]

---

## Scope

**In scope:**
- [Item]
- [Item]

**Out of scope:**
- [Item]
- [Item]

**Dependencies:**
- [Item]

---

## Stakeholders

| Name / Role | Involvement |
|-------------|------------|
| [Name, Role] | Decision-maker / Contributor / Informed |

---

## Risks

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| [Risk description] | High / Medium / Low | [Mitigation, or "Open question"] |

---

## Timeline

[Brief narrative or table of target dates. Use phases with relative timing if hard dates are
unknown: "Phase 1: 2–3 weeks from kickoff". Omit if no timeline has been discussed.]

---

## Open Questions

- [Question] — Owner: [Name, or "TBD"]
- [Question] — Owner: [Name, or "TBD"]

```

Omit sections that are empty. Do not add placeholder headers for sections with no content.

---

## What to Skip and When

**Small, well-scoped requests:** Combine Problem and Goals into a single section; skip Timeline and Risks unless the requester specifically needs them.

**Requests with no clear owner yet:** Flag ownership as an open question rather than leaving it blank; an ownerless project brief is not actionable.

**Projects that already have an approved approach:** Skip "Proposed Approach" with a note that approach is in the design document.

---

## Quality Checks

Before delivering, verify:

- Every goal in the table has a success criterion — not "TBD"
- Scope out is explicit, not empty — even a single line matters
- Every risk has a mitigation or is flagged as an open question — risks without mitigations belong in Open Questions
- The problem statement explains the cost of inaction, not just the current state
- Stakeholders have named owners, not "relevant teams" or "leadership"

---

## Output Format

Deliver:

1. **Complete project brief** — Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Open items list** — Any information the user still needs to fill in before the brief is ready to share (missing owner, unconfirmed deadline, undefined success criteria, etc.)
