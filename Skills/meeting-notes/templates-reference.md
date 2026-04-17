# Meeting Notes — Output Templates

Detailed Markdown templates for each section of the meeting notes output. Referenced from the main skill.

---

## Meeting Header

```
# [Meeting Title or Topic]

**Date:** [Date]
**Duration:** [Approximate duration if determinable from transcript]
**Attendees:** [Names and roles where known]
**Purpose:** [One sentence: why this meeting was held]
```

If the transcript does not contain this information, include the header with blank fields marked as "[Not provided — please fill in]".

---

## Executive Summary

Two to four sentences capturing the full arc of the meeting: why it was held, what the group worked through, what was resolved, and what remains open. Write this for someone who will not read the rest of the document. It should stand alone.

---

## Discussion Threads

One subsection per major topic. Scale depth to significance — a 25-minute topic gets a full paragraph; a 2-minute topic gets two to three sentences.

```
## Discussion: [Topic Name]

[Framing sentence — what the group was trying to figure out]

[Summary — key points, positions, concerns]

**Outcome:** [Resolved / Deferred / Open — and what that means]
```

---

## Decisions

A numbered list of clear, unambiguous statements in active voice. Write decisions as facts, not meeting summaries.

Include conditions or caveats where applicable: "The team will migrate to the new platform in Q3, contingent on security review completion by end of July."

```
## Decisions

1. [Decision stated clearly]
2. [Decision stated clearly]
```

---

## Action Items

A table with four columns. Every row must have an owner and a task.

```
## Action Items

| # | Action | Owner | Deadline | Notes |
|---|--------|-------|----------|-------|
| 1 | [What needs to happen] | [Name] | [Date or "Not set"] | [Any context] |
```

If the same person owns multiple actions, give each its own row.

---

## Key Quotes

Verbatim statements (cleaned of filler) worth preserving. Use sparingly — only for statements that are unusually clear, represent an important commitment, or capture a significant position.

```
## Key Quotes

> "[Quote]" — [Speaker name], [context in a few words if needed]
```

Omit this section entirely if there are no quotes that genuinely warrant preservation.

---

## Next Steps

What happens after this meeting — overall forward motion, not individual tasks. Write as a short bulleted list. Include the next meeting date, topic, and expected attendees if mentioned.

---

## Parking Lot

Items that were raised but explicitly deferred or that could not be resolved in this session. Format as a bulleted list, each item with the name of the person who raised it if known.
