---
name: decision-log
description: Extracts and formats Decision Records from video or audio transcripts, capturing the full context of each decision: the problem being solved, options that were considered, who made the call, the rationale, concerns or dissent raised, and any conditions or follow-on actions. Produces structured, durable Decision Records rather than a meeting narrative. Use when a user wants to document the reasoning behind decisions made in a recorded meeting, create an audit trail for a key call, or build a decision log from a transcript. Triggers include "create a decision log from this transcript", "document why we decided X", "extract decisions from this recording", "make a decision record", or when a user wants more than meeting notes — specifically the reasoning, options, and ownership behind each decision.
---

# Decision Log from Transcript

This skill produces structured Decision Records from video or audio transcripts. Unlike meeting notes, which summarize everything that happened, Decision Records focus on the reasoning and accountability behind specific choices — durable artifacts that answer "why did we decide this?" months or years later.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Decision Records vs. Meeting Notes

This skill is not a replacement for meeting notes. Use it when the goal is accountability and traceability, not a summary of the conversation.

A Decision Record captures:
- The specific decision made (stated clearly and unambiguously)
- The problem or situation that triggered the decision
- The options that were considered and why each was or was not selected
- Who made the decision and whether they had the authority to do so
- The rationale — the reasoning behind the chosen option
- Concerns or dissent raised — objections, reservations, and who voiced them
- Conditions or caveats attached to the decision
- Follow-on actions or dependencies unlocked by the decision

Meeting notes capture the flow of conversation. Decision Records capture the logic of choices.

---

## Before Processing: Transcript Triage

Apply the same triage steps as for meeting notes:

**Unlabeled speakers** — If the transcript uses generic labels ("Speaker 1", "Unknown"), stop and ask the user for a name and role mapping before proceeding. Decision Records require named decision-makers.

**Roles and authority** — For each named participant, note their role if stated in the transcript. Role context is critical for assessing who had decision authority. If roles are not stated in the transcript, ask the user.

**Auto-captioning artifacts** — Silently clean filler words, false starts, and transcript mishearings when extracting meaning. Do not preserve artifacts.

**Partial transcripts** — If the transcript appears cut off or begins mid-conversation, note this prominently. A decision without its full context may be misrepresented.

---

## Extraction Pass: Finding Decisions

Work through the transcript looking specifically for decision moments. A decision moment is any point where:
- The group commits to a course of action ("We're going to go with X")
- A single person makes a call ("I'm making the call — we'll do Y")
- Options are explicitly weighed and one is selected
- A previous default or plan is explicitly overturned
- A scope, direction, or timeline is locked down

Do not classify exploratory discussion, brainstorming, or "we should think about X" as decisions. A decision requires a commitment, not just a consideration.

For each decision moment, extract:

1. **The decision** — one sentence, stated as a fact in active voice
2. **The trigger** — what problem, question, or situation made this decision necessary
3. **Options considered** — what alternatives were raised, even briefly; include options that were rejected
4. **Who decided** — the person or group with decision authority; note if the decision was delegated, escalated, or made by consensus
5. **Rationale** — why this option was chosen over the others; use the speaker's own language where it is clear
6. **Concerns and dissent** — objections, reservations, or risks raised during deliberation; include who voiced them; do not omit dissent even if the decision went ahead
7. **Conditions** — any stated caveats or contingencies attached to the decision (e.g., "contingent on legal review", "unless X happens")
8. **Follow-on actions** — immediate next steps that the decision creates; name the owner

If a decision was made quickly and none of these fields were addressed in the transcript, note them as "Not discussed in transcript" rather than leaving them blank or inferring content.

---

## Output Structure

Produce one Decision Record per decision. Order records chronologically as they appeared in the transcript.

```
# Decision Log: [Meeting Name or Topic]

**Source:** [Transcript description, e.g. "Product Review Call — [date]"]
**Participants:** [Names and roles]
**Decisions recorded:** [Count]

---

## Decision [#]: [Short Title]

**Decision:** [One sentence, active voice, stating exactly what was decided]

**Trigger:** [What problem or question made this decision necessary]

**Options Considered:**
- **[Option A]:** [Brief description — one sentence on what this option was and why it was or was not selected]
- **[Option B]:** [Same]
- *(Add additional options as needed. Include the chosen option in this list.)*

**Decided by:** [Name, Role] — [Basis of authority: e.g., "team consensus", "product owner call", "escalated to VP"]

**Rationale:** [Why this option was chosen. Use the decision-maker's own language where it clearly captures the reasoning. One to four sentences.]

**Concerns / Dissent:**
- [Name, Role]: [Concern or objection raised] — [Outcome: addressed, noted, or overruled]
- *(If no concerns were raised, write: "No dissent recorded in transcript.")*

**Conditions:** [Any stated caveats. If none: "None stated."]

**Follow-on Actions:**
| Action | Owner | Deadline |
|--------|-------|----------|
| [Task created by this decision] | [Name] | [Date or "Not set"] |

---

*(Repeat for each decision)*
```

---

## Handling Ambiguous Decision Moments

Transcripts often contain decisions that were implied rather than stated. Handle these cases carefully:

**Implicit agreement** — If all participants appear to agree without an explicit "we decided" statement, note the decision as "reached by apparent consensus" and quote the clearest statement of agreement.

**Revisited decisions** — If a decision was made, then revisited and changed later in the same meeting, produce a single record that shows the evolution: the initial decision, the reason it was reopened, and the final outcome.

**Deferred decisions** — If an option was considered but explicitly deferred, do not create a Decision Record. Add the deferred item to a Pending Decisions list at the end of the log.

**Decisions outside meeting scope** — If a participant references a decision made elsewhere and ratified in this meeting, create a brief record noting it as a ratification, not a new decision.

---

## Pending Decisions

After the Decision Records, append a Pending Decisions section:

```
## Pending Decisions

Items raised in this meeting that require a decision but were not resolved:

- **[Topic]:** [Brief description of what needs to be decided] — Owner: [Name or "TBD"] — Due: [Date or "Not set"]
```

If there are no pending decisions, omit this section.

---

## Quality Checks

Before delivering, verify:

- Every Decision Record has a named decision-maker — not "the group" or "the team" unless the transcript genuinely shows consensus with no individual owner
- Concerns and dissent are recorded honestly — do not soften or omit objections that were raised
- Rationale uses the decision-maker's reasoning as expressed in the transcript, not an interpretation
- Options Considered includes rejected options — a decision with only one option listed may not be complete
- Conditions are captured exactly as stated — do not paraphrase conditional commitments
- Follow-on actions have named owners

---

## Output Format

Deliver:

1. **Complete decision log** — Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Decision count summary** — One line: "X decisions recorded, Y pending"
3. **Gaps to resolve** — Any fields that could not be filled from the transcript (e.g., missing roles, unclear authority, rationale not stated)
