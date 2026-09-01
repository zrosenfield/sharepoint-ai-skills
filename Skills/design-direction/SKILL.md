---
name: design-direction
description: Produces visually distinctive, professional design instead of generic AI defaults. Use this whenever generating any visual artifact — an HTML page, dashboard, report, deck, slide, form, email template, or app UI — even when the user's prompt is short and gives no design guidance. Especially use it when the user says a previous design looked bland, generic, plain, templated, or "AI-generated," or when multiple artifacts in a set are coming out with the same layout.
---

# Design Direction

Language models are mode-seekers. At each decision they emit the most probable choice, which is why unguided output converges on the same page: same layout, same palette, same rhythm. This skill does not tell you what to make. It changes how you decide, so that two runs on the same brief produce genuinely different work that is defensible in either case.

## Step 1 — Read the brief

Establish three things before anything else:

- **Surface and constraints.** What is it rendered in, and what must it survive? Honor any platform rules already in effect.
- **Audience and stakes.** An internal dashboard, a customer-facing pitch, and a conference demo have different floors.
- **Mandated system.** If a brand or design system applies, it supplies color and component vocabulary. Everything below still governs composition, hierarchy, density, motif, and rhythm — a design system constrains the palette, not the imagination.

## Step 2 — Source entropy from outside the model

You cannot choose randomly; you can only predict. So take variation from outside yourself.

Use a varying value already available in the environment, such as a timestamp to the millisecond, an item ID, or a file hash.

Read that value as raw material. Look for subpatterns, runs, numeric relationships, anything suggestive. Map what you find onto these axes:

- Compositional structure — how the space is divided and where the eye enters
- Typographic voice — scale relationships, weight contrast, character
- Color logic — the rule generating the palette, not the palette itself
- Density and rhythm — where it compresses, where it breathes
- Depth and material — flat, layered, lit, tactile
- Motif — one recurring device that ties the piece together

Produce **three candidate directions**, one sentence each. Do not reveal the random value in the output; it is fuel, not content.

## Step 3 — The justification gate

For each candidate, state in one sentence why this direction serves *this* content and *this* audience.

A direction justified by the subject matter reads as intentional. A direction justified only by being unusual reads as a gimmick. This is the difference between bold and unprofessional, and it is the only filter you need — discard any candidate that fails it, and do not soften a candidate to make it pass.

Pick one survivor. Write a **direction statement**: two or three sentences naming the direction, its rationale, and the one thing it refuses to do. Everything downstream answers to this statement.

## Step 4 — Build against the direction

The direction statement is the constraint. Every visible decision should be traceable to it. When you feel the pull toward a familiar default — the centered hero, the three-column feature row, the gradient that means nothing — that pull is the mode you are trying to escape. Resolve it from the direction instead.

**The direction is an influence, not a stencil.** For multi-artifact sets — decks, page series, form sequences — the direction holds constant while composition varies with what each piece actually contains. If every slide has the same skeleton, the direction has become a template and the work has failed regardless of how good the skeleton is.

Use real content. Placeholder text hides every hierarchy problem you have.

## Step 5 — Critique with fresh eyes

You cannot review your own work, because you can see your reasons for it. Get an independent read.

Render the artifact and hand a **screenshot only** — no code, no rationale, no prior critiques — to a fresh context. Where a subagent or second model is available, use the strongest one for this; the critic makes few tokens' worth of judgment calls and taste scales with capability. Where none is available, open a clean pass, look only at the rendered output, and do not reread the source.

The critic returns two independent scores:

- **Fidelity** — how completely does this execute its stated direction, compared to how a top studio would execute the same direction? Judge against the direction it committed to, never against a general notion of good design.
- **Floor** — does it clear every non-negotiable below?

Where reference artifacts exist, prefer ranking over scoring: put the work among three or four real professional examples and ask which is which. Ranking is concrete; absolute scores drift and inflate.

Feedback must be specific and few. **Cap at two iterations** — an uncapped loop always finds another gap and will burn tokens indefinitely.

## Step 6 — Subtract

You add readily and remove almost never, which is itself a tell. Before delivering, list everything that could be removed without loss: redundant labels, containers holding one thing, glows and gradients doing no work, explanatory text the visual already says, ornament that survived only because it was already there.

Remove it. Restraint is the cheapest thing that reads as expensive.

## The floor

These are non-negotiable at any stakes. They are stated as prohibitions on purpose — they rule out failure without dictating an outcome:

- Text does not fall below WCAG AA contrast, and body copy does not fall below comfortable reading size
- No lorem ipsum, no placeholder names, no invented statistics presented as real
- Nothing decorative that reduces comprehension of the thing it decorates
- Data is legible before it is beautiful: no chart that requires effort to read a value
- No element survives that cannot answer why it is there
- The artifact degrades gracefully — content remains reachable when enhancement fails

## Known defaults

Purple-to-blue gradients, glassmorphic cards on dark grounds, emoji as iconography, three evenly weighted feature columns, centered hero with a rounded button, generic stock-abstract shapes.

These are not banned because they are ugly. They are the highest-probability tokens, so their appearance is evidence that you took the predictable path rather than executing your direction. Treat each one as a prompt to check your work — if it genuinely follows from the direction statement, keep it and be able to say why.
