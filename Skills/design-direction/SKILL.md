---
name: design-direction
description: Creates distinctive, intentional visual designs for interfaces, websites, dashboards, reports, slides, forms, email templates, and other visual artifacts. Use whenever Terra, Sol, or another AI agent designs or redesigns a visual surface, especially when the brief is sparse, prior output feels generic or AI-generated, or a set of artifacts risks repeating the same layout. Establishes a brief-specific design logic without turning it into a reusable visual template.
---

# Design Direction

Act as a design lead, not a theme picker. Make every design feel specific to its subject, audience, content, and constraints. Distinctive does not mean loud. It means coherent, purposeful, and difficult to reuse unchanged for an unrelated brief.

Build and render the requested artifact with the runtime's available tools. Do not return implementation code unless the user explicitly asks for it. The deliverable is the working artifact, not a design plan, token list, or code sample.

## 1. Read the brief and the content

Before building, identify:

- the surface, environment, and technical constraints
- the audience, stakes, and primary action or takeaway
- the content hierarchy, density, sequence, and repeated structures
- the subject's own visual vocabulary, materials, language, and tensions
- any existing brand requirements or surrounding product conventions

If the brief is incomplete, infer a sensible direction from the available content. Ask only when a missing decision would materially change the outcome.

## 2. Explore before committing

Generate three genuinely different design directions internally. Vary the underlying logic, not just colors or fonts. Consider different approaches to hierarchy, composition, rhythm, density, typography, imagery, interaction, and motion.

Use runtime-generated entropy when useful to avoid repeating familiar solutions, but do not let randomness override the brief. Every major choice must be defensible from the content or context.

Choose the strongest direction and commit to it. Do not present a style menu unless the user asks for options.

## 3. Create a temporary direction contract

Define a short, brief-specific design logic covering:

- **Hierarchy:** what dominates, supports, and recedes
- **Composition:** how the content shape determines the layout
- **Typography:** the intended voice, contrast, and reading rhythm
- **Color and material:** a restrained palette and surface treatment tied to the subject
- **Motif:** one recognizable idea used selectively
- **Behavior:** interaction and motion that clarify state, sequence, or cause

Treat this as a temporary decision system for the current artifact, not a reusable template.

## 4. Compose from content

Let the content determine the form. Do not begin with a default hero, card grid, dashboard shell, bento layout, or repeated section pattern.

Use containers only when they express real grouping, state, or interaction. Allow related screens, pages, or slides to share a visual language without forcing them into the same composition.

Create emphasis through scale, spacing, alignment, contrast, pacing, and selective detail. Prefer a few strong decisions over many decorative ones.

Use imagery, illustration, diagrams, or generated visuals when they carry meaning or establish the intended atmosphere. Do not use decoration as a substitute for composition.

## 5. Avoid generic AI design

Reject outputs that could be swapped into an unrelated product with only a title change. Avoid habitual purple-blue gradients, excessive glow, floating glass panels, ornamental grids, random pills, uniform rounded cards, icon badges for every heading, fake data, empty hero space, and decorative motion.

Do not imitate a named design style mechanically. Borrow principles only when they support the brief.

## 6. Build the real artifact

Use the runtime to create, execute, and render the artifact. Preserve required functionality and content. When redesigning, improve the experience rather than merely reskinning it.

Meet the quality floor:

- readable hierarchy and clear primary action
- intentional responsive behavior and no accidental overflow
- accessible contrast, focus states, labels, and interaction targets
- concise interface writing without filler or invented claims
- motion that is restrained and respects reduced-motion settings
- complete states for the experience being shown

## 7. Critique the render

Inspect the rendered result or screenshot, preferably in a fresh critic context. Evaluate the artifact itself rather than the effort or implementation.

Ask:

- Is the primary idea obvious at first glance?
- Does the composition follow the content, or fall back to a familiar template?
- Is the design specific to this brief?
- Is anything competing with the main job?
- Does the artifact feel finished at its intended size?

Make at most two critique passes. In each pass, fix only the one or two changes with the greatest effect.

## 8. Subtract and deliver

Remove anything that does not improve meaning, hierarchy, usability, or atmosphere. Challenge every extra container, label, divider, shadow, gradient, border, badge, icon, and repeated treatment.

Deliver the finished artifact and a concise note describing the central design idea and any important constraints. Do not expose internal exploration, entropy, critique, or code unless requested.
