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
Silently clean transcription artifacts (filler words, false starts, repetitions, mishearings) when extracting meaning. Do not preserve them in the notes unless the exact wording is significant.

**Missing timestamps or metadata**
If the transcript has no timestamps, date, or attendee list, note the gaps at the top of the output and ask the user to fill them in before publishing.

**Long tangents and side conversations**
Transcripts capture everything, including off-topic exchanges. Do not include small talk, extended technical troubleshooting unrelated to the meeting purpose, or side conversations that did not produce a decision or action. Summarize lengthy tangents in a single sentence if they consumed significant time.

---

## Extraction Pass

Work through the transcript in a single pass, tagging content into five categories:

**Decisions** — any statement where the group agrees on a course of action, selects an option, or commits to a direction.

**Action items** — any commitment by a named person to do something by a certain time. Capture the owner, the task, and the deadline. If no deadline was stated, mark it as "No deadline set".

**Discussion threads** — the substantive topics the group worked through. Group related exchanges together even if they were not contiguous in the meeting — a topic raised, dropped, and returned to later is one thread.

**Key quotes** — statements that capture the essence of a position or decision. Preserve verbatim (cleaned of artifacts). Limit to four or fewer.

**Parking lot items** — questions raised but explicitly deferred, or issues that could not be resolved in this session.

---

## Output Structure

Always deliver the notes in this order. Omit a section only if there is genuinely nothing to put in it — do not include empty sections. See [templates-reference.md](templates-reference.md) for Markdown templates for each section.

1. **Meeting header** — title, date, duration, attendees, purpose (mark unknowns as "[Not provided — please fill in]")
2. **Executive summary** — two to four standalone sentences covering why, what, resolved, and open
3. **Discussion threads** — one subsection per topic: framing sentence, summary, outcome (Resolved / Deferred / Open). Scale depth to significance.
4. **Decisions** — numbered list of clear, unambiguous statements in active voice
5. **Action items** — table with columns: #, Action, Owner, Deadline, Notes. One row per action, even for same owner.
6. **Key quotes** — verbatim (cleaned), sparingly. Omit if none warrant preservation.
7. **Next steps** — overall forward motion, not individual tasks
8. **Parking lot** — deferred items with the person who raised them

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
