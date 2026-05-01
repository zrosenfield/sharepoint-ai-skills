---
name: kb-admin-report
description: Generates a comprehensive knowledge base health report covering corpus overview, knowledge decay, gap status, ingestion activity, expert coverage, and recommended next actions. Triggers when an admin asks for a knowledge base report, status update, or health check.
---

When an admin asks for a knowledge base report, status update, or health check, generate a comprehensive report. Read all files in the Knowledge Base library, all items in the Knowledge Gaps list, and all items in the Expert Directory list.

## 1. Corpus Overview

- Total number of KB files and list of topic names
- For each file: count of sections, count of distinct sources cited, and the date range of entries (oldest Added date to newest Added date)
- Total knowledge entries across all files

## 2. Decay Report

- List every KB entry where Last Verified is older than 90 days
- Group stale entries by topic file
- For each stale entry: show the subtopic name, Last Verified date, days since verification, and the original source person
- Count: total entries, verified within 90 days, stale (90+ days), critical (180+ days)
- Highlight any topic files where more than half of entries are stale

## 3. Gap Status

- Count of Knowledge Gaps by Status (Open, Assigned, Resolved, Verify)
- List all Open and Assigned gaps with their Topic, Asked By, and date
- List all Verify items (decay-triggered re-verification requests)
- Average time from Open to Resolved for completed gaps (if dates allow)
- Topics with the most open gaps — these are the weakest coverage areas

## 4. Ingestion Activity

- Count of resolved gaps by Source Type (Transcript, Email, Document, Slack, Typed, Verification)
- This shows how knowledge is entering the system — are people typing it in, or is it coming from meeting transcripts, emails, etc.
- Identify which source types are most and least used

## 5. Expert Coverage

- List all experts and their expertise areas
- Cross-reference against open gap topics: which gap topics have a matching expert? Which don't?
- Identify expertise areas with no KB file yet (expert registered but no knowledge captured)
- Identify KB topics with no matching expert (knowledge exists but no one owns it)

## 6. Recommendations

Based on the data above, provide 3–5 specific next actions. Prioritize:

- Stale entries that need re-verification (especially in frequently-asked topics)
- Open gaps that have been unassigned the longest
- Topic areas with no expert coverage
- Source type gaps (e.g., if no transcripts have been processed, suggest recording and submitting meeting notes)
