# Meeting Briefing Generator Template

Use this structure when the user asks for a meeting briefing, meeting prep, or any pre-meeting analysis. Adapt the `${meetingType}` to whatever the user specifies (e.g., "executive review", "board meeting", "sprint retrospective", "steering committee", "stakeholder update").

## 📋 EXECUTIVE BRIEFING

Write exactly 3 paragraphs for a VP/executive audience:
- **Paragraph 1:** Project status in one breath — what is the project, where does it stand RIGHT NOW (use specific numbers from the data: % tasks complete, budget burn, risk count)
- **Paragraph 2:** The headline story — what's the ONE thing the exec needs to know walking in? What changed since last review? What's the critical tension?
- **Paragraph 3:** Your bottom-line recommendation — should they be worried? What's the ask?

## 📊 KEY METRICS AT A GLANCE

Create a compact table with these metrics pulled from ACTUAL data:

| Metric | Value | Status |
| --- | --- | --- |
| Tasks Complete | X/Y (Z%) | 🔴🟡🟢 |
| Tasks Overdue | N | 🔴🟡🟢 |
| Budget Burned | $X / $Y (Z%) | 🔴🟡🟢 |
| Budget At Risk | categories | 🔴🟡🟢 |
| Open Risks | N (X high severity) | 🔴🟡🟢 |
| Aggregate Risk Score | X/Y | 🔴🟡🟢 |
| Days to Milestone | N | — |

## ❓ 5 ANTICIPATED TOUGH QUESTIONS

Think like a skeptical executive. Based on the data, generate the 5 HARDEST questions someone would ask. These should be the questions that make the presenter uncomfortable.

For EACH question:
1. **The Question** — phrased exactly as an exec would ask it (direct, pointed)
2. **Why They'll Ask It** — what in the data triggers this question (1 sentence)
3. **Suggested Answer** — a 2-3 sentence response backed by SPECIFIC data points (numbers, dates, names)
4. **Supporting Data** — bullet list of the exact data points that support the answer

## 📅 RECOMMENDED AGENDA

Design a structured meeting agenda for 60 minutes:
- Each item needs: time allocation, topic, presenter/owner, objective (inform/discuss/decide)
- Front-load the most critical items
- Include a "Decisions Needed" section — don't let the meeting end without resolving these
- Include 5 min buffer for unexpected discussions

Format as a table: | Time | Topic | Owner | Objective |

## ⚠️ LANDMINE TOPICS — DO NOT BRING UP

Identify 2-4 topics from the data that could DERAIL the meeting if raised:
- Topics with high emotional charge but no resolution path yet
- Negotiations still in progress where premature discussion could harm position
- Issues where the data is too incomplete to have a productive conversation
- For each: explain WHY it's a landmine and WHEN it would be safe to discuss

## ✅ DECISIONS NEEDED IN THIS MEETING

List the 3-5 decisions that MUST be made in this meeting:
- For each decision: state the options, your recommended position, and what data supports it
- Flag any decision that is blocking downstream work

## 📖 PRE-READ MATERIALS

List which documents from the site attendees should review BEFORE the meeting:
- For each document: name, 1-sentence summary of what's in it, and WHY it matters for this meeting
- Rank by priority (must-read vs. nice-to-have)
- Estimate reading time for each

## OUTPUT RULES

- **Lead with the Executive Briefing** — this is the most important section and must never be truncated
- **Tough Questions and Decisions are high-value** — keep these even if you need to shorten other sections
- If running long, abbreviate Pre-Read Materials and Agenda before cutting Tough Questions or Decisions
- Use 🔴🟡🟢 status indicators throughout
- If data is missing or incomplete, say so explicitly and note how it affects confidence
