---
name: design-inspiration
description: >-
  Applies reusable design languages to websites, applications, dashboards,
  presentations, and interface projects. Use whenever the user asks for visual
  inspiration, a redesign, multiple creative directions, a comparison gallery,
  or a new aesthetic for an existing project — even if they do not name this
  skill. Keeps the source product, content, workflows, accessibility, and
  brand constraints intact while changing the visual system, composition,
  typography, materials, interaction, and motion. Triggers: design
  inspiration, visual directions, art direction, creative redesign, aesthetic,
  multiple concepts, inspiration playbook, and unique designs.
---

# Design Inspiration

Use broad, transferable design languages to influence a project without turning
any single language into a required template.

The detailed six-language source is in
[DESIGN_LANGUAGES.md](references/DESIGN_LANGUAGES.md). It is inspiration for
layout, hierarchy, behavior, typography, materials, and motion—not a license to
copy a designer's existing work or branded assets.

## Live visual references

Use the [Styles gallery](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Styles.html)
and the corresponding
[story pages](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story.html)
to inspect examples of the visual systems. The available reference stories are
[Precision](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Precision.html),
[Exuberant](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Exuberant.html),
[Systems](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Systems.html),
[Typographic](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Typographic.html),
[Disruption](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Disruption.html),
and [Geometric](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Geometric.html).

## Choose the mode

Choose one mode from the request:

| Mode | Use when | Deliver |
|---|---|---|
| **Apply one direction** | The user names or selects a visual language | One coherent implementation |
| **Compare directions** | The user wants options or says "different," "unique," or "inspiration" | Two or more genuinely distinct implementations |
| **Create a hybrid** | The user wants to combine compatible qualities | One named hybrid with an explanation of what it borrows |
| **Explore freely** | No language or style is specified | Several materially different directions derived from the brief |

Do not default to six directions unless a six-way comparison is useful. Two or
three stronger, brief-specific directions are preferable when they resolve a
choice more clearly.

## Workflow

1. **Study the project.**
   Read the source, screenshot, URL, code, design tokens, content, and
   functional requirements. Identify the product's purpose, audience, primary
   task, existing navigation, constraints, and system states.

2. **Preserve the invariant.**
   Keep factual content, information architecture, navigation destinations,
   workflows, data, conversion goals, and brand constraints unchanged unless
   the user explicitly approves a change.

3. **Find the brief-specific visual proposition.**
   State privately what the page should feel like and how that feeling should
   help users complete the main task. A new palette alone is not a direction.

4. **Extract transferable qualities.**
   From the playbook, select qualities at the system level: composition,
   hierarchy, typography, spacing, visual metaphor, components, imagery,
   interaction, and motion. Do not recreate a named designer's recognizable
   work or quote their name as an endorsement.

5. **Prevent template drift.**
   Compare the proposed direction with nearby work in the same project and
   reject repeated structures, familiar section sequences, or cosmetic reskins.
   If changing the title could make the design plausible for an unrelated
   project, revise the visual proposition.

6. **Build the result.**
   Use the project's existing stack and design tokens where practical. Create
   scoped overrides or direction-specific tokens instead of duplicating
   unrelated app logic. Keep the implementation working across desktop, tablet,
   and mobile.

7. **Verify the experience.**
   Check semantic structure, keyboard navigation, visible focus, labels,
   contrast, target sizes, reduced motion, loading and empty states, and
   essential data-heavy views. Test the actual user journey, not only a hero
   section.

8. **For comparisons, run the rubric.**
   Evaluate every direction for distinctiveness, usability, craft,
   accessibility, responsive quality, and performance. Reject any direction
   that fails a critical usability or accessibility requirement before ranking
   the rest.

## Nonnegotiable rules

- Preserve content meaning and functionality.
- Make differences structural or behavioral, not merely color swaps or font
  substitutions.
- Do not copy existing artworks, signature compositions, proprietary UI, or
  branded assets.
- Do not present a named designer as endorsing or authoring the result.
- Do not hide important actions or remove a state merely to improve the visual.
- Do not invent data, testimonials, labels, claims, or workflows.
- Target WCAG 2.2 AA. Preserve readable contrast and support
  `prefers-reduced-motion`.
- Use existing brand requirements where they exist. This skill adds influence;
  it does not override legal, product, or brand constraints.

## Variation methods

Use combinations of these methods rather than treating the playbook's palette
as a fixed theme:

- Recompose the hierarchy and section rhythm.
- Change the dominant visual device.
- Introduce an original visual metaphor tied to the content.
- Replace a report-style card sequence with a workflow, map, timeline, or
  interactive system only when the content supports it.
- Change component behavior and motion grammar.
- Change image or illustration strategy.
- Rebalance typography, scale, density, and spacing.
- Adapt a direction differently to mobile rather than simply shrinking desktop.

## Delivery format

For an implementation, deliver the working result and a concise rationale:

1. Design thesis: what changed and why.
2. Visual system: layout, typography, palette, materials, and interaction.
3. Major usability decisions.
4. Responsive and accessibility treatment.
5. One or two meaningful trade-offs.
6. Screenshot or preview if tooling permits.

For a comparison, also include:

1. A named route or tab for every direction.
2. A one-sentence thesis for each.
3. A short scorecard using the weighted rubric in the playbook.
4. A recommendation for the audience and task, if the user requested it.

Keep the implementation itself as the primary deliverable. Do not stop at mood
boards, token lists, or generic design plans.

## Error handling

| Situation | Response |
|---|---|
| Source material is incomplete | Use sensible assumptions, state them briefly, and preserve confirmed functionality |
| Existing brand rules conflict with the playbook | Follow the brand rules and explain the adaptation |
| A selected direction weakens accessibility | Redesign that direction; do not ship the accessibility failure |
| Multiple directions look too similar | Revise the composition, hierarchy, or interaction grammar; do not add another palette |
| The stack cannot support a requested effect | Use a progressive-enhancement fallback and preserve task completion |
| The project already has a strong brand | Apply the influence through allowed structural and interaction qualities, not recoloring |

## Post-Run Reflection

After completing a multi-step design workflow, review whether the result is
brief-specific, genuinely distinct when alternatives were requested, accessible,
responsive, maintainable, and respectful of existing content. Record reusable
patterns only when they apply beyond this project; do not turn a successful
one-off into a default template.
