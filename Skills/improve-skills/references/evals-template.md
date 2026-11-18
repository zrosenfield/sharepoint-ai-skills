# Evals: [skill-name]

This file is the persistent eval suite for the **[skill-name]** skill. It is loaded automatically whenever `improve-skills` runs. Edit it directly in SharePoint to update the data source, revise eval criteria, or adjust configuration.

---

## Data Source

- **Library or list:** [Name of the SharePoint library or list that contains the content this skill processes]
- **Sampling method:** newest *(options: newest | random | user-picks)*
- **Items per session:** 3 *(max 5)*

If no library is available, paste sample content directly at the start of each IMPROVE session. Note that here so the AI knows to ask for it: [yes / no — library available]

---

## Eval Criteria

These checks define what a good output looks like for this skill on this content. They are reviewed and updated each session as the data evolves.

| # | Name | Question | Pass | Fail |
|---|------|----------|------|------|
| 1 | [short-label] | [Yes-or-no question about the output] | [Specific description of what "yes" looks like — cite observable evidence] | [What triggers "no"] |
| 2 | [short-label] | [Yes-or-no question about the output] | [Specific description of what "yes" looks like] | [What triggers "no"] |
| 3 | [short-label] | [Yes-or-no question about the output] | [Specific description of what "yes" looks like] | [What triggers "no"] |

Add or remove rows as needed. Three to six evals is the recommended range.

---

## Configuration

- **Runs per experiment:** 3
- **Budget cap:** none *(set a number here to cap total experiment cycles)*

---

## Improvement History

The AI appends a row here after every improvement session.

| Date | Items sampled | Evals revised? | Score | Outcome |
|------|---------------|---------------|-------|---------|
| [YYYY-MM-DD] | Baseline established | No | [X/Y] (Z%) | — |
| [YYYY-MM-DD] | [N] items from [library] | [Yes / No] | [X/Y] (Z%) | Improved |

---

## Notes

Use this section for anything you want the AI to know before running the loop — recent user complaints, new content patterns appearing in the library, known failure modes to investigate, or evals you are considering adding.

[Add free-form notes here.]
