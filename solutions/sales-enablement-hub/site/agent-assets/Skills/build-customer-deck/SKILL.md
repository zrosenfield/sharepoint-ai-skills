---
name: build-customer-deck
description: Builds a customer deck from a Deck Templates template and approved Slide Library slides, using interactive question cards, and saves it to the Decks library with the seller's talking points. Use when someone says "build a deck", "make a deck for <customer>", presses Build a deck in Decks, or presses Build with this template on a template.
---

# Build a customer deck

Collect the brief with **interactive question cards** (your ask_user_question tool), never a plain-text list of
options. Two cards at most, then build. Keep every message short.

## Card 1: the meeting
If the seller started from a template (the selected Deck Templates file, or they named one), that template is the
meeting type: do not ask for it. Otherwise include it as the first question.
- **Meeting type** (single choice): First meeting pitch, Executive briefing, Technical deep dive, Quarterly business
  review. Use each template's Best for line as the option description.
- **Industry** (single choice): Healthcare, Financial services, Retail, Manufacturing, Public sector, Cross-industry.
- **Customer** (free text): "Which customer is this for?"
- **Goal** (free text): "What should this meeting achieve? One sentence."
If the card cannot take free text, ask for the customer and goal in one short line after it.

## Card 2: pick your slides
1. Load the recipe from **Deck Templates** (Template kind = the meeting type): slide roles in order.
2. For each role, find the approved options in **Slide Library**: matching Slide role, never Shareability
   **Internal only**, nothing expired. Rank them: the industry first, then Cross-industry, then fit to the goal. For the Title role always use the
   industry's title slide when one exists (NW-Title-<Industry>); fall back to the corporate title only if none does.
3. Show one card with **one single-choice question per role that has two or more options** (max 4 questions; if
   more roles qualify, keep the 4 with the most options). Header = the role. Options = up to 3 slides, label = slide
   title, description = its one-line summary. Put your recommendation first and mark it "(recommended)".
   Roles with one option are filled automatically; say so in one line above the card.
4. If the seller skips the card, use your recommendations.

## Build
1. Assemble the chosen slides in recipe order in one PowerPoint file. Copy them as they are: do not restyle,
   rewrite or re-theme them, and do not offer a visual redesign. Do not include the template's cover slide.
   If the recommended customer story is from the same customer, keep it only when the goal is expansion and frame
   it as "your results so far"; otherwise recommend another story from the same industry.
2. Save to the **Decks** library (Generated Content) as `<Customer> - <Meeting type> - <today yyyy-mm-dd>.pptx`.
   If that name is taken, add ` - <2-3 word goal>` to the name; do not ask.
3. **Fill in the deck's details. This step is required, not optional.** Right after saving, update the file's
   columns in one write:

   | Column (internal name) | Value |
   |---|---|
   | Customer | the customer name |
   | Template | the meeting type |
   | Industry | the industry picked on card 1 |
   | MeetingGoal | the goal, one sentence |
   | DraftStatus | Draft |
   | SourceSlides | one plain text string: every slide file name in deck order, without .pptx, comma separated, e.g. `NW-Title-Retail, NW-Agenda-Standard, NW-Proof-Platform` |
   | TalkingPoints | plain text, short lines (below) |

   Talking points:
   - `Opening:` one sentence the seller says first, tailored to the customer and goal.
   - `New title:` the title to type on slide 1.
   - One line per slide: `<n>. <slide title>: <the one thing to say>`.
   - `Skipped:` anything left out and why (omit if nothing).
4. **Check it.** Read the item back and check all seven columns by name: Customer, Template, Industry,
   MeetingGoal, DraftStatus, SourceSlides, TalkingPoints. Any that is empty or missing (SourceSlides most often):
   write just those again, once, then read back again. Never finish while any of the seven is empty. If a write
   still fails, say which column in one line and paste its value into your reply so nothing is lost.
5. Reply with the deck link, the Opening line and the New title, and remind the seller to retitle slide 1.
   Say "Details saved" only after step 4 passed.
