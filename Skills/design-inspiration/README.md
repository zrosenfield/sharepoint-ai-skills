# Design Inspiration

Design Inspiration helps an agent derive original visual directions from
transferable design systems without freezing one template or copying a named
designer's recognizable work. It is intended for websites, applications,
dashboards, presentations, and interface projects.

The skill keeps the project invariant—content, data, navigation, workflows,
brand constraints, accessibility—and varies the visual system: composition,
hierarchy, typography, materials, imagery, interaction, and motion.

## Use it

Ask for a design that is not a fixed template:

- "Design this page using an atmospheric, precision-focused direction."
- "Create three genuinely different redesigns of this application."
- "Combine typographic impact with geometric wit, but keep the workflow usable."
- "Use Design Inspiration on this page and build the strongest direction."

The skill can apply one language, compare several directions, create a hybrid,
or explore freely. It does not assume that six options are always best: two or
three brief-specific directions are preferable when they produce a clearer
choice.

## Live visual references

The [Zach Adoption Demo Styles gallery](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Styles.html)
shows the corresponding visual families in a live SharePoint page.

| Style | Live story page | When to use it |
|---|---|---|
| **Signature** | [Story](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story.html) | A baseline visual identity and the project's default art direction |
| **Atmospheric Precision** | [Story-Precision](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Precision.html) | Premium SaaS, dashboards, productivity and product showcases |
| **Exuberant Expression** | [Story-Exuberant](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Exuberant.html) | Launches, consumer products, communities and expressive AI tools |
| **Interactive Systems** | [Story-Systems](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Systems.html) | AI interfaces, data stories, research and interactive explainers |
| **Typographic Impact** | [Story-Typographic](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Typographic.html) | Editorial platforms, events, institutions and knowledge products |
| **Controlled Disruption** | [Story-Disruption](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Disruption.html) | Storytelling, culture, independent brands and experimental launches |
| **Geometric Wit** | [Story-Geometric](https://microsoft.sharepoint-df.com/sites/zachadoptiondemo/SitePages/Story-Geometric.html) | Education, clear AI applications and explanatory visual systems |

Use the story pages as visual references, not as templates. Reinterpret the
transferable qualities for the user's actual content, stack, brand constraints,
and task completion path.

## How the skill works

1. Study the source page, screenshot, URL, code, content, audience, and
   accessibility constraints.
2. Preserve facts and essential workflows.
3. Choose a brief-specific visual proposition instead of applying a palette
   alone.
4. Extract transferable layout, composition, behavior, imagery, typography,
   and motion qualities from the playbook.
5. Rebuild the project with scoped design tokens and the existing stack.
6. Verify desktop, tablet, mobile, keyboard, focus, contrast, empty states,
   loading states, and reduced motion.
7. For comparisons, score each option and recommend it only if it fits the
   audience and primary task.

## Source

The detailed design language reference is in
[references/DESIGN_LANGUAGES.md](references/DESIGN_LANGUAGES.md). It defines the
six languages, variation dimensions, accessibility requirements, a review
rubric, and iteration prompts.

## Install

Upload the `design-inspiration` folder to the SharePoint AgentAssets `Skills`
library, or copy it into another Agent Skills-compatible skill location.

## What it does not do

- It does not copy existing websites or a named designer's recognizable work.
- It does not turn a successful project into a reusable fixed template.
- It does not swap a palette, font, and border radius while preserving the same
  wireframe.
- It does not invent data or claims.
- It does not ship an experience that fails accessibility or task usability.
