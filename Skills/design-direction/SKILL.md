---
name: design-direction
description: >-
  Creates a distinctive visual direction for interfaces, pages, dashboards,
  slides, forms, and other visual artifacts. Use when the user asks to "make
  this look good," "redesign this," "make it more visual," "create a polished
  visual," or produce something bold, expressive, immersive, or memorable.
  Prevents report-page fallback, repeated layout grammar, cosmetic reskins,
  decorative UI, and invented content. Do not use for content-only editing,
  analytical questions, functional code changes, or minor formatting requests
  without a visual-design goal.
---
# Design Direction

Prevent visually polished work from collapsing into the same reusable design with different content.

## Decision rules

- Before choosing a layout, identify one brief-specific visual proposition that makes the artifact memorable. It must affect the dominant composition, hierarchy, scale, sequence, or interaction—not only color, type, or decoration.
- Do not refine the first plausible direction. Use the creative seed to consider materially different visual propositions, then choose the one that best expresses the brief rather than the one that is easiest to implement.
- Treat "bold" as a decisive visual idea, not as more gradients, decoration, motion, or color.
- When recent related artifacts are available in context, identify the closest one before committing to a direction.
- Treat repetition in structure, information sequence, primary visualization, composition, palette, typography, or component grammar as a collision signal.
- If a result differs from the closest related artifact mainly through color, type, decoration, or reordered cards, revise the underlying structure.
- Let the content determine which differences matter. Do not satisfy variety by mechanically changing a fixed number of dimensions.
- Preserve required content, claims, functionality, brand constraints, and accessibility. Variety is not permission to alter meaning.

## Creative entropy

Before selecting a direction, obtain a non-semantic seed from the runtime, such as a request identifier, session identifier, or current timestamp. Do not pretend that a model-generated string is random.

Privately use the seed to disrupt the most obvious choices in composition, hierarchy, rhythm, material, imagery, and interaction. Look for patterns or associations in the seed only as a way to reach less probable ideas.

The seed is inspiration, not a specification. Discard any interpretation that conflicts with the brief, content, accessibility, brand constraints, or usability. Do not reveal the seed in the artifact or describe it as part of the design rationale.

If the runtime exposes no external value, proceed from the brief without inventing fake randomness and rely on the collision checks below.

## Failure checks

Reject or revise an artifact when any of these are true:

- Its dominant structure is a vertical stack of titled report sections.
- Cards, panels, and containers are the primary visual idea rather than a consequence of the content.
- Its most memorable quality is that it looks clean, professional, polished, or editorial.
- Every section has similar visual weight, producing no deliberate focal moment.
- The visual concept could be removed without changing how the artifact communicates.
- Changing the title would make it plausible for an unrelated brief.
- It repeats a familiar hero, metric strip, chart region, timeline, and recommendation sequence without the content requiring that sequence.
- It defaults to warm-paper editorial styling, dark recommendation slabs, purple-blue gradients, floating glass panels, bento grids, or uniform rounded cards because they are convenient.
- It repeats the palette, title treatment, card grammar, or data sequence of a nearby artifact without a content-driven reason.
- Containers, pills, badges, icons, grids, imagery, or motion are decorative rather than communicating grouping, state, sequence, or meaning.
- Empty hero space or oversized titles displace useful information.
- It invents claims, data, labels, interactions, or states that the source does not support.
- Placeholder text or fake data appears in the delivered artifact.
- Visual novelty weakens legibility, contrast, focus visibility, touch targets, responsive behavior, or reduced-motion support.

Do not replace one recurring template with a prescribed menu of alternate templates. Avoid choosing a named visual form merely because it appears in these instructions.

## Delivery

Build and render the finished artifact. Do not return exploratory directions, token lists, implementation code, or a generic design plan unless the user asks for them.

When context includes related outputs, briefly name the structural collision that was avoided. If a tool fails or produces no result, state that plainly and do not invent a completed artifact.
