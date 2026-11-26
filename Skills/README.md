# Experimental SharePoint Skills

The skills in this directory are prototypes and incubation candidates. Maintained community skills live in the official [PnP SharePoint Skills repository](https://github.com/pnp/sharepoint-skills).

Each installable skill is stored directly at `Skills/<skill-name>/SKILL.md`, following the [Agent Skills specification](https://agentskills.io/specification).

## Experimental Skills

| Skill | Purpose |
|---|---|
| [`authoring-sharepoint-markdown`](./authoring-sharepoint-markdown/) | Produces SharePoint-compatible Markdown |
| [`assign-obligation-owners`](./assign-obligation-owners/) | Assigns missing primary and escalation owners to confirmed open obligations |
| [`autoresearch`](./autoresearch/) | Performs iterative multi-step research |
| [`brainstorming-design-docs`](./brainstorming-design-docs/) | Turns ideas into structured design documents |
| [`capture-obligations`](./capture-obligations/) | Captures contract obligations and source clauses into the Obligations list |
| [`client-briefing`](./client-briefing/) | Briefs users on a Client Hub client's projects, activity, and follow-ups |
| [`clear-obligation-sample-data`](./clear-obligation-sample-data/) | Removes fictional Obligation Hub sample data after confirmation |
| [`copy-editing`](./copy-editing/) | Runs a structured copy-editing workflow |
| [`crm-change-request`](./crm-change-request/) | Plans and confirms changes to the experimental Client Hub |
| [`decision-log`](./decision-log/) | Extracts structured decision records |
| [`deck-assembly`](./deck-assembly/) | Assembles presentations from existing slide content |
| [`design-direction`](./design-direction/) | Produces distinctive, professionally justified visual direction |
| [`exclude-obligation`](./exclude-obligation/) | Excludes a clause or pattern from future Obligation Hub capture |
| [`executive-summary`](./executive-summary/) | Produces concise leadership summaries |
| [`faq-building`](./faq-building/) | Builds structured FAQ content |
| [`find-expert`](./find-expert/) | Matches knowledge gaps to subject-matter experts |
| [`forest-style`](./forest-style/) | Applies the experimental forest visual system |
| [`gap-analysis`](./gap-analysis/) | Compares documents for gaps and conflicts |
| [`hiring-pipeline-report`](./hiring-pipeline-report/) | Summarizes recruiting pipeline data |
| [`improve-skills`](./improve-skills/) | Iteratively evaluates and improves skills |
| [`ingest-knowledge`](./ingest-knowledge/) | Converts source material into structured knowledge |
| [`kb-admin-report`](./kb-admin-report/) | Reports on knowledge-base health |
| [`linkedin-post-writing`](./linkedin-post-writing/) | Drafts LinkedIn posts |
| [`list-formatting`](./list-formatting/) | Creates SharePoint list-formatting JSON |
| [`log-client-activity`](./log-client-activity/) | Previews and records Client Hub activity after confirmation |
| [`log-knowledge-gap`](./log-knowledge-gap/) | Records unanswered questions and routes them |
| [`mark-obligation-fulfilled`](./mark-obligation-fulfilled/) | Records fulfillment, evidence, and recurring next occurrences |
| [`meeting-notes`](./meeting-notes/) | Converts transcripts into meeting notes |
| [`obligation-hub-guide`](./obligation-hub-guide/) | Answers questions about the Obligation Hub with clause citations and links |
| [`obligation-leadership-digest`](./obligation-leadership-digest/) | Sends a weekly leadership summary of register exposure |
| [`obligation-owner-digest`](./obligation-owner-digest/) | Sends obligation owners their overdue and upcoming work |
| [`project-brief`](./project-brief/) | Develops decision-ready project briefs |
| [`quarterly-expense-report`](./quarterly-expense-report/) | Creates quarterly expense reports |
| [`ralph-loop`](./ralph-loop/) | Applies an iterative self-evaluation loop |
| [`scrollytelling-story`](./scrollytelling-story/) | Creates interactive scrolling explainers with a continuous D3 graphic and user-defined story lengths |
| [`setup-client-hub`](./setup-client-hub/) | Builds the experimental Client Hub lists, columns, and views |
| [`setup-obligation-hub`](./setup-obligation-hub/) | Builds the Obligation Hub lists, columns, views, and related configuration |
| [`site-analyzer`](./site-analyzer/) | Analyzes SharePoint project sites |
| [`style-guidelines`](./style-guidelines/) | Provides a brand-style skill template |
| [`sweep-obligations`](./sweep-obligations/) | Runs daily timing, reminder, and escalation maintenance |
| [`uppababy-brand-review`](./uppababy-brand-review/) | Experimental brand-compliance demo |
| [`weekly-client-review`](./weekly-client-review/) | Reviews Client Hub portfolio health and upcoming work |
| [`youtube-description`](./youtube-description/) | Generates descriptions from video transcripts |

The five Client Hub skills use the list design in [Client Hub for SharePoint](../solutions/client-hub-for-sharepoint/). Install `setup-client-hub` to try building the lists with Copilot, or set up the lists using the kit before using the four day-to-day skills.

The ten Obligation Hub skills use the contract and obligation lists in [Obligation Hub for SharePoint](../solutions/obligation-hub-for-sharepoint/). Install `setup-obligation-hub` to build the hub, then add the capture, routing, fulfillment, reporting, maintenance, and exception skills needed for the scenario.

## Graduated to PnP

These skills are maintained in `pnp/sharepoint-skills`. Their old local copies have been removed to prevent stale or conflicting installations.

| Skill | Maintained version |
|---|---|
| `dossier` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/dossier/dossier) |
| `exec-report` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/exec-report/exec-report) |
| `list-styling` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/list-styling/list-styling) |
| `review-council` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/review-council/review-council) |
| `roadmap-timeline` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/roadmap-timeline/roadmap-timeline) |
| `scorecard-matrix` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/scorecard-matrix/scorecard-matrix) |
| `style-bento` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-bento/style-bento) |
| `style-blueprint` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-blueprint/style-blueprint) |
| `style-figma-clean` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-figma-clean/style-figma-clean) |
| `style-glassmorphism` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-glassmorphism/style-glassmorphism) |
| `style-high-contrast` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-high-contrast/style-high-contrast) |
| `style-monochrome` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-monochrome/style-monochrome) |
| `style-neobrutalism` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-neobrutalism/style-neobrutalism) |
| `style-pastel` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-pastel/style-pastel) |
| `style-retro` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-retro/style-retro) |
| `style-terminal` | [PnP source](https://github.com/pnp/sharepoint-skills/tree/main/Skills/style-terminal/style-terminal) |

## Installing an Experimental Skill

Upload the individual skill folder, not the whole `Skills` directory:

1. Open the SharePoint site's **Agent Assets** library.
2. Open the **Skills** folder.
3. Upload `Skills/<skill-name>/`.

Experimental skills are not guaranteed to remain compatible or stable. Prefer the PnP version whenever one exists.
