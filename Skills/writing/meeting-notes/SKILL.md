---
name: meeting-notes
description: Transforms raw video or audio transcripts into detailed, structured meeting summaries formatted for SharePoint. Handles messy auto-generated transcripts including unlabeled speakers, filler words, and transcript artifacts. Extracts discussion threads, decisions, action items, key quotes, and next steps. Use when a user pastes or shares a meeting transcript and wants polished, shareable notes. Triggers include "summarize this meeting transcript", "create notes from this recording", "turn this transcript into meeting notes", "write up this call", or when a user shares raw transcript text.
---

# Meeting Notes from Transcript

This skill processes raw video or audio transcripts — including auto-generated, messy, or unlabeled ones — into polished, structured meeting summaries ready to publish in SharePoint.

> **Scope:** Produces prose and Markdown only. Does not write code, scripts, or formulas.

---

## Before Processing: Transcript Triage

Video transcripts vary widely in quality. Before extracting content, assess the transcript and handle these common issues:

**Unlabeled or generic speakers**
If the transcript uses labels like "Speaker 1", "Speaker 2", or "Unknown Speaker", stop before processing and ask the user to provide a name mapping. A table format works well:

Ask: "This transcript uses generic speaker labels. Can you tell me who each speaker is? For example: Speaker 1 = [name and role], Speaker 2 = [name and role]."

If the user can only identify some speakers, proceed with those and label unresolved speakers as "Unidentified participant" in the notes.

**Auto-captioning artifacts**
Auto-generated transcripts often contain: repeated words, false starts ("I — I think we should"), filler words ("um", "uh", "like", "you know"), and occasional word substitutions from mishearing. Silently clean these when extracting meaning. Do not preserve transcription artifacts in the notes unless the exact wording is significant.

**Missing timestamps or metadata**
If the transcript has no timestamps, date, or attendee list, note the gaps at the top of the output and ask the user to fill them in before publishing.

**Long tangents and side conversations**
Transcripts capture everything, including off-topic exchanges. Do not include small talk, extended technical troubleshooting unrelated to the meeting purpose, or side conversations that did not produce a decision or action. Summarize lengthy tangents in a single sentence if they consumed significant time.

---

## Extraction Pass

Work through the transcript in a single pass, tagging content into five categories:

**Decisions** — any statement where the group agrees on a course of action, selects an option, or commits to a direction. Indicators: "we decided", "we're going to go with", "let's do", "agreed", "that's what we'll do", "confirmed".

**Action items** — any commitment by a named person to do something by a certain time. Indicators: "I'll", "can you", "who's going to", "by [date]", "let's make sure [person]", "take an action". Capture the owner, the task, and the deadline. If no deadline was stated, mark it as "No deadline set".

**Discussion threads** — the substantive topics the group worked through. Group related exchanges together even if they were not contiguous in the meeting. A topic that was raised, dropped, and returned to later is one thread, not two.

**Key quotes** — statements that are particularly clear, significant, or that capture the essence of a position or decision. Preserve these verbatim (cleaned of artifacts). Limit to four or fewer — if everything seems quotable, nothing is.

**Parking lot items** — questions raised but explicitly deferred, topics someone flagged for a future meeting, or issues that could not be resolved in this session.

---

## Output Structure

Always deliver the notes in this order. Omit a section only if there is genuinely nothing to put in it — do not include empty sections.

---

### Meeting header

```
# [Meeting Title or Topic]

**Date:** [Date]
**Duration:** [Approximate duration if determinable from transcript]
**Attendees:** [Names and roles where known]
**Purpose:** [One sentence: why this meeting was held]
```

If the transcript does not contain this information, include the header with blank fields marked as "[Not provided — please fill in]".

---

### Executive Summary

Two to four sentences capturing the full arc of the meeting: why it was held, what the group worked through, what was resolved, and what remains open. Write this for someone who will not read the rest of the document. It should stand alone.

---

### Discussion Threads

One subsection per major topic. Each subsection:

- Opens with a one-sentence framing of what the group was trying to figure out or accomplish on this topic
- Summarizes the key points raised and any significant disagreements or concerns surfaced
- Closes with the outcome: resolved (and how), deferred, or still open

Scale depth to significance. A topic that took 25 minutes of substantive back-and-forth deserves a full paragraph. A topic that was covered in two minutes gets two to three sentences.

Use this format:

```
## Discussion: [Topic Name]

[Framing sentence]

[Summary of discussion — key points, positions, concerns]

**Outcome:** [Resolved / Deferred / Open — and what that means]
```

---

### Decisions

A numbered list. Each decision is a single clear, unambiguous sentence in active voice. Write decisions as statements of fact, not as meeting summaries ("The team will migrate to the new platform in Q3" not "It was discussed that migration might happen").

If a decision was made with conditions or caveats, include those: "The team will migrate to the new platform in Q3, contingent on security review completion by end of July."

```
## Decisions

1. [Decision stated clearly]
2. [Decision stated clearly]
```

---

### Action Items

A table with four columns. Every row must have an owner and a task. Deadline and notes are filled in where stated; left blank or flagged otherwise.

```
## Action Items

| # | Action | Owner | Deadline | Notes |
|---|--------|-------|----------|-------|
| 1 | [What needs to happen] | [Name] | [Date or "Not set"] | [Any context] |
| 2 | ... | ... | ... | ... |
```

If the same person owns multiple actions, give each its own row. Do not group actions under one owner into a single cell.

---

### Key Quotes

Verbatim statements (cleaned of filler) worth preserving. Use these sparingly — only for statements that are unusually clear, represent an important commitment, or capture a significant position.

Format:

```
## Key Quotes

> "[Quote]" — [Speaker name], [context in a few words if needed]
```

Omit this section entirely if there are no quotes that genuinely warrant preservation.

---

### Next Steps

What happens after this meeting. This is distinct from action items — next steps describe the overall forward motion of the initiative or project, not individual tasks. Write as a short bulleted list.

Include the next meeting date, topic, and expected attendees if mentioned.

---

### Parking Lot

Items that were raised but explicitly deferred or that could not be resolved in this session. Format as a bulleted list, each item with the name of the person who raised it if known.

---

## Quality Checks

Before delivering the notes, verify:

- Every action item has a named owner — not "the team" or "someone"
- Every decision is stated as a fact, not as a description of a discussion
- Discussion thread outcomes are explicit — do not leave a thread summary without stating whether it was resolved
- The executive summary can be read without any other section and still make sense
- No transcript artifacts (false starts, filler words, repeated words) appear in the output
- Speakers are identified by name throughout — no "Speaker 1" in the final notes

---

## Handling Edge Cases

**No decisions were made**
Do not invent decisions. Omit the Decisions section and note in the Executive Summary that the meeting was exploratory or informational.

**No clear action items**
Omit the Action Items table. If the meeting produced commitments that were vague or unowned, list them in Next Steps with a note that owners need to be assigned.

**Transcript is partial or cut off**
Note at the top of the document that the transcript appears incomplete and flag which section of the meeting may be missing.

**Multiple languages or code-switching**
Summarize in the language the user is working in. Note in the header if the meeting was conducted in another language.

**Very short meeting (under 15 minutes)**
Collapse the structure. Use: header, a single Summary section (instead of Executive Summary + Discussion Threads), Decisions, Action Items, and Next Steps. Skip Parking Lot and Key Quotes unless specifically relevant.

---

## Output Format

Deliver:

1. **Complete meeting notes** — full Markdown, ready to paste into a SharePoint Markdown web part or page
2. **Gaps to fill** — a short list of anything that could not be determined from the transcript (missing names, dates, context, unresolved speaker labels)
3. **Publisher note** — one sentence flagging anything the note-taker should verify before sending (e.g., "Please confirm the Q3 deadline for the migration decision with [name]")
