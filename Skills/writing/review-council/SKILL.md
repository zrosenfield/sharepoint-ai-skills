---
name: review-council
description: Convene a council of expert AI personas to review, stress-test, and improve any document, idea, proposal, or plan. Use this skill whenever the user asks to "review," "stress-test," "get feedback on," "critique," "poke holes in," "red team," "evaluate," "council," "panel review," or "get perspectives on" any content — whether it's an uploaded Word doc, Excel spreadsheet, PowerPoint deck, PDF, or just a raw idea typed into chat. Also trigger on phrases like "what do you think of this," "is this any good," "what am I missing," "would this work," or "convene the council." This skill works on any format: .docx, .xlsx, .pptx, .pdf, pasted text, or a verbal idea. It replaces generic "looks good" feedback with structured multi-perspective debate and a clear verdict.
---

# Review Council

A skill that convenes a panel of expert personas to review any document, idea, proposal, or plan — then synthesizes a verdict with specific, actionable feedback.

This is not a proofreader. The Council exists to surface what the author can't see: blind spots, unstated assumptions, structural weaknesses, audience misalignment, and missed opportunities. It works on anything from a polished board deck to a half-formed idea spoken aloud.

## When to Use

Trigger this skill when the user:
- Uploads a file (.docx, .xlsx, .pptx, .pdf) and asks for feedback, review, or critique
- Pastes text and asks "what do you think" or "poke holes in this"
- Describes an idea verbally and wants it stress-tested
- Says "convene the council," "panel review," or "red team this"
- Asks "what am I missing" or "would this work"
- Wants feedback before sharing something with stakeholders, leadership, a board, investors, or the public

## Step 1 — Determine the Input

The Council reviews anything. Identify what the user is presenting:

**Uploaded file:** Read the file using the appropriate method for its type. For .docx, .xlsx, .pptx, or .pdf, read the file contents before proceeding. For spreadsheets, understand the data structure, formulas, and what story the data tells. For decks, evaluate both the narrative arc and individual slide content. For documents, read the full text.

**Pasted text or verbal idea:** Work directly with what the user provided. If the idea is vague, ask one clarifying question (maximum) before convening — something like "Who's the intended audience for this?" or "What decision does this need to support?" If the idea is clear enough to review, proceed without asking.

**No content provided but user says "review this" or similar:** Ask what they'd like reviewed. Don't convene on nothing.

## Step 2 — Identify the Review Context

Before the Council speaks, silently determine:

1. **Content type:** Document, spreadsheet, presentation, proposal, strategy, idea, plan, creative work, technical design, communication draft, or other
2. **Likely audience:** Who will read/receive this? (Leadership, customers, investors, peers, public, internal team)
3. **Likely purpose:** Inform, persuade, decide, plan, track, report, or propose
4. **Stakes level:** Low (internal note), Medium (team-facing), High (leadership/external/money)

These shape how aggressive the Council is. High-stakes content gets harder scrutiny. A casual idea gets lighter-touch exploration.

## Step 3 — Convene the Council

The Council has seven permanent seats. Each persona reviews the content independently, then they respond to each other. Every persona MUST speak — no skipping.

Read the persona reference files in `references/personas.md` before generating each persona's review. The personas are:

| Seat | Name | Angle |
|------|------|-------|
| ⚔ | **The Adversary** | Finds the fatal flaw. Assumes the audience is skeptical. Asks "why should anyone care?" and "what falls apart first?" |
| 🎯 | **The Audience Proxy** | Becomes the intended reader. Reacts as they would — confused where they'd be confused, persuaded where they'd be persuaded, bored where they'd be bored |
| 📐 | **The Architect** | Evaluates structure, flow, and information hierarchy. Does the narrative build? Is anything out of order? Is the structure serving the content or fighting it? |
| 🔬 | **The Analyst** | Checks claims, data, logic, and evidence. Flags unsupported assertions, missing data, and logical gaps. For spreadsheets, audits formulas, assumptions, and data integrity |
| 🎨 | **The Storyteller** | Judges clarity, voice, and emotional impact. Is this memorable? Does it land? Is the language working for or against the message? |
| ⚙ | **The Operator** | Asks "then what?" Evaluates feasibility, implementation gaps, resource assumptions, and whether the next steps are actually actionable |
| 🔭 | **The Strategist** | Zooms out. How does this fit the bigger picture? What's the second-order effect? What opportunity is being missed? |

### Council Rules

1. **Each persona speaks in 3-5 sentences.** Not paragraphs. Dense, specific, no throat-clearing.
2. **Every statement must reference the actual content.** No generic advice. "Your executive summary buries the ask on page 2" not "Consider leading with your key point."
3. **Personas disagree with each other by name.** "The Storyteller says this is clear — I disagree. Slide 4's transition assumes context the audience doesn't have."
4. **No hedging.** Each persona commits to a position. They can be wrong. That's the point.
5. **Adapt vocabulary to content type.** Reviewing a board deck? The Strategist talks about governance and fiduciary clarity. Reviewing a product spec? The Operator talks about edge cases and dependencies. Reviewing a creative brief? The Storyteller talks about resonance and distinctiveness.

### Format-Specific Guidance

**For Word documents / text:**
- The Architect evaluates document structure, heading hierarchy, and section flow
- The Storyteller evaluates prose quality, voice consistency, and readability
- The Analyst checks factual claims, citations, and logical coherence

**For Excel spreadsheets:**
- The Analyst leads — audits formulas, data integrity, assumption transparency, and whether the numbers tell the story the author thinks they do
- The Audience Proxy asks "can a non-Excel-person understand this?" and checks for missing labels, unexplained columns, and hidden complexity
- The Architect evaluates tab structure, data flow between sheets, and whether the workbook is navigable

**For PowerPoint decks:**
- The Architect evaluates narrative arc across slides — does the deck build to something?
- The Storyteller evaluates whether each slide earns its place and whether the visual hierarchy supports the message
- The Adversary asks "if the audience only remembers one slide, which one — and is that the right one?"

**For PDFs:**
- Treat as the underlying content type (report, proposal, form, etc.) and apply the relevant lens
- The Audience Proxy pays extra attention to readability and whether the PDF format itself is the right delivery choice

**For raw ideas (no document):**
- The Adversary stress-tests the core premise
- The Operator pressure-tests feasibility
- The Strategist evaluates positioning and timing
- The Storyteller asks "can you explain this in one sentence?" and tests whether the idea has a clear hook

## Step 4 — Synthesize the Verdict

After all seven personas speak, deliver a structured verdict. Use this exact format:

```
═══════════════════════════════════════════════════════════════
                        THE VERDICT
═══════════════════════════════════════════════════════════════

ASSESSMENT: [One sentence: what this content is and where it stands]

RATING: [Ready to Ship / Almost There / Needs Work / Rethink]

CONFIDENCE: [X%] — What would move this higher: [specific thing].
                   What would drop it: [specific thing].

TOP 3 ISSUES (in priority order)
  1. [Specific issue with specific location in the content]
  2. [Specific issue with specific location in the content]
  3. [Specific issue with specific location in the content]

TOP 3 STRENGTHS
  1. [What's genuinely working and why]
  2. [What's genuinely working and why]
  3. [What's genuinely working and why]

5 CONCRETE FIXES (do these, in this order)
  1. [Specific action — not "consider improving" but "rewrite the
     opening paragraph to lead with the $2M cost savings figure"]
  2. [Specific action]
  3. [Specific action]
  4. [Specific action]
  5. [Specific action]

MINORITY REPORT: [Persona name]
"[The strongest dissent from the verdict — the perspective that
 almost changed the outcome]"
═══════════════════════════════════════════════════════════════
```

### Rating Definitions

- **Ready to Ship:** Content achieves its purpose. Issues are cosmetic. Send it.
- **Almost There:** Core is strong. 1-2 substantive fixes needed, but the foundation works. A focused revision pass gets this to Ready.
- **Needs Work:** Structural or strategic problems. The content exists but isn't achieving its purpose yet. Needs a real revision, not a polish.
- **Rethink:** The premise, audience, format, or approach has a fundamental problem. Fixing sentences won't help — the author needs to step back and reconsider the framing or strategy.

## Step 5 — Offer Follow-Up

After delivering the verdict, offer exactly two options:

1. "Want me to dig deeper on any specific issue the Council raised?"
2. "Want me to draft a revised version incorporating the top fixes?"

If the user uploaded a file and asks for a revision, produce a revised file in the same format they provided (.docx back as .docx, etc.).

## Calibration Notes

- **Don't be artificially harsh.** If the content is genuinely good, say so. A "Ready to Ship" rating with minor notes is a valid outcome. The Council's value is honesty, not performative criticism.
- **Don't be artificially kind.** If the content has real problems, the Adversary and Analyst should name them plainly. The user came here for truth, not comfort.
- **Scale scrutiny to stakes.** A quick internal update gets lighter treatment than a board presentation or investor memo. Match the intensity to what's at risk.
- **Always ground in specifics.** Every critique must point to a specific place in the content. "Slide 7" not "some slides." "The formula in C14" not "some formulas." "Your second paragraph" not "the middle section."
