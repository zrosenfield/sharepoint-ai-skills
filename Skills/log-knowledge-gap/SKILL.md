---
name: log-knowledge-gap
description: Logs unanswered questions to the Knowledge Gaps list and routes them to a subject matter expert. Triggers when the assistant cannot answer a question from the Knowledge Base library. Checks the Expert Directory for a matching expert and assigns the gap automatically.
---

When you cannot answer a question from the Knowledge Base library:

1. Create an item in the Knowledge Gaps list. Set Question to the user's question, Topic to your best guess at the subject area (match existing KB file names when possible), Asked By to the user's name (ask if you don't know it), and Status to Open. Set Source Type to Gap.
2. Check the Expert Directory list for anyone whose Expertise Areas match the topic. If found, update Assigned Expert and set Status to Assigned.
3. Tell the user you've logged the gap and who it's been routed to (or that it's unassigned if no expert matched).
