---
name: ingest-knowledge
description: Extracts tacit knowledge from any input — typed text, transcripts, emails, documents, or Slack threads — and writes it into the Knowledge Base library as structured markdown. Triggers when someone shares knowledge directly, pastes content, or uploads a file to the Submissions library. Resolves matching open Knowledge Gaps items automatically.
---

When someone shares knowledge — typed, pasted, or by uploading a file to the Submissions library — extract tacit knowledge and add it to the Knowledge Base.

## What to Extract

Listen for more than facts. Actively look for:

- Decisions and their reasoning ("we went with X because...")
- Tradeoffs acknowledged ("the downside is..." / "we accepted that risk because...")
- Failed approaches ("we tried X and it didn't work because...")
- Changes over time ("we used to do X, then switched to Y when...")
- Edge cases and exceptions ("that works except when..." / "watch out for...")
- Unwritten rules ("technically the policy says X but in practice we...")
- Lessons learned ("if I had to do it again..." / "the thing nobody tells you is...")

## How to Structure It

1. Check the Knowledge Base library for an existing file on this topic.
2. If a file exists, read it. Add new knowledge under the right heading. If the new information updates, contradicts, or adds context to existing content, note the change — don't silently overwrite. Add a new subsection or append under the existing one.
3. If no file exists, create a new markdown file named with a short slug (e.g., vendor-contracts.md).
4. For each piece of knowledge, use the sections that apply:
   - **Current State** — what's true now
   - **Rationale** — why it's this way
   - **History** — what came before or changed
   - **Nuance** — edge cases, exceptions, gotchas
5. Always include the Source line (who, when, what format), Added date, and Last Verified date (set to today).
6. After ingesting, check the Knowledge Gaps list for Open or Assigned items this knowledge answers. Update matching items: set Status to Resolved, Resolved Date to today, KB File to the filename, and Source Type to match the input format (Transcript, Email, Document, Slack, or Typed).
7. If the new knowledge updates an existing KB entry, also update that entry's Last Verified date to today.

When processing transcripts or meeting notes, preserve the conversational context that reveals reasoning. "Dana said we switched to CrowdStrike after the Meridian incident" is more valuable than "Pen testing vendor: CrowdStrike."
