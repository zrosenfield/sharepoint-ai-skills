# Deck builder

The goal is a customer deck in minutes, built only from approved slides, with something to say on every slide.

## Seller experience

1. Menu **Build a deck** opens Deck Templates > **Pick a template**: one card per template (First meeting pitch,
   Executive briefing, Technical deep dive, Quarterly business review), with a live preview, Best for line, slide count and
   recipe.
2. **Build with this template** on a card. This quick step asks Copilot to load `build-customer-deck` with that template as the meeting type.
3. **Card 1: the meeting.** Industry (single choice), customer, goal (one sentence).
4. **Card 2: pick your slides.** For each slide role with two or more approved options, choose between up to three slides
   (with the recommendation first). Roles with one option are filled automatically.
5. Copilot assembles the slides in recipe order. It saves `<Customer> - <Meeting type> - <yyyy-mm-dd>.pptx` to
   **Decks** and fills seven columns: Customer, Template, Industry, MeetingGoal, DraftStatus, SourceSlides and
   TalkingPoints. TalkingPoints holds the opening line, the new title for slide 1 and one line per slide.
6. Copilot shows an **Update item** card before it writes the columns. The seller presses **Update** once.

Decks > **Start here** is the deck studio: recent decks with their talking points and a way back to the gallery.
Decks > **Build a deck** (command bar) starts the same flow without a template preselected.

## How it's wired

| Piece | Where |
|---|---|
| Template recipe (slide roles in order) | Deck Templates > Recipe, for example `Title, Agenda, Problem, Solution, Proof, Customer story, Next steps, Close` |
| Approved slides | Slide Library: one slide per file, with Slide role, Industry, Products, Shareability and Order. The Title role prefers `NW-Title-<Industry>`. |
| Rules | `Agent Assets/Skills/build-customer-deck/SKILL.md`: two cards at most, no internal-only slides, no restyling, the customer-story rule, the name-collision rule, and a check of all seven columns before it says "Details saved" |
| Gallery button | Quick step **Build with this template** (Deck Templates). The tiles formatter calls it with `executeQuickStep` and its id. |
| Command bar button | Quick step **Build a deck** (Decks, list-level) |

## Adding a template

1. Build an example deck (the gallery preview shows its first slide).
2. Upload it to Deck Templates and set Template kind, Output format = PowerPoint, Recipe, Audience, Slide count and Best for.
3. Make sure every role in the recipe has at least one approved slide (ideally one per industry for Title, Problem and Customer story).
4. Add the template kind to the **Template** choice column in Decks, and to the skill's Meeting type list.

## Adding slides

Use one slide per `.pptx`. Give every file its **own slide master and layout id range** (see `tools/content-generators/fix_ids.py`).
If the ranges collide, Copilot's merged deck won't open (see [known-issues.md](known-issues.md)). Upload the file, then set
Slide role, Industry, Products, Shareability, Summary and Order. Autofill proposes the first four.
