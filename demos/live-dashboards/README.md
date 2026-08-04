# Live-Linked SharePoint Dashboard Demos

Four demos showing how a single-file HTML page can read SharePoint lists live and calculate views that are not stored in any one list.

| Demo | Data shape | Main point |
|---|---|---|
| Program Portfolio Review | One parent with two child lists | Roll up milestones and risks into a live portfolio view |
| Crew Certification Coverage | Many-to-many through a junction list | Pivot relationships into a coverage matrix |
| Warranty Cost Chain | Four joins across five lists | Calculate warranty cost per customer |
| Transaction Pivot | One flat list with 30,000 items | Read once and pivot locally without repeated round trips |

The executable scripts are:

- `tools/scripts/23-program-portfolio-review/23-program-portfolio-review.demo`
- `tools/scripts/24-crew-certification-coverage/24-crew-certification-coverage.demo`
- `tools/scripts/25-warranty-cost-chain/25-warranty-cost-chain.demo`
- `tools/scripts/26-transaction-pivot/26-transaction-pivot.demo`

## Prompting Rules

- Save a copy as soon as a page reaches a presentable state.
- Never ask to "make this live." Scope each change narrowly and freeze everything else.
- Separate data changes from design changes.
- Describe the observed problem and its consequence rather than prescribing pixel values.
- When behavior looks wrong, ask the agent to explain its current rule before changing it.
- Keep all script inline in one HTML file. Do not introduce external scripts or CDNs.
- Do not modify the sandbox-generated script tag or its attributes.
- Require keyboard access, visible focus, reduced-motion support, honest loading states, and named empty-list errors.

## Refresh Pattern

For demos 1 through 3, refresh when the page becomes visible and every 60 seconds while it remains in the foreground. Preserve current selections and filters, keep the last good data after failures, and show when the data was last read.

Demo 4 refreshes only when the page becomes visible. Re-reading 30,000 rows every minute is unnecessary.

## Demo Notes

### Program Portfolio Review

Open Milestones in a second tab and change a clean program's milestone to `Late`. Returning to the dashboard should move that program upward because the ordering is computed from child records.

### Crew Certification Coverage

Show the Crew Certifications junction list before showing the matrix. The contrast demonstrates why many-to-many data is difficult to interpret in a normal list view.

### Warranty Cost Chain

Ask where warranty cost per customer is stored. It is not: the dashboard joins parts, tickets, aircraft, and customers, then multiplies quantity by unit cost.

### Transaction Pivot

Pause while the load counter passes 5,000 records. The list-view threshold limits server-side views; it does not prevent a client from paging through the complete list.

## Retrofitting a Static Page

Use three separate turns:

1. Ask where the current static data is stored and which function renders it. Make no changes.
2. Replace one static source with one live list read while preserving the rendering input shape and all HTML and CSS.
3. Repeat for each remaining list, one at a time.

If an edit changes the layout, revert to the saved copy instead of correcting forward.

## Script Policy Troubleshooting

If the agent claims scripting is unavailable, point out the page's existing working JavaScript, refresh control, or live list reads. Require it to preserve the current inline script tag exactly. A rewritten tag can lose the sandbox-provided nonce and cause a valid script to be blocked.
