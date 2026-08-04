# Live-Linked SharePoint Dashboard Demos

Manual, copy/paste-ready walkthroughs for building live HTML dashboards with Copilot in SharePoint. The guides are the primary demo artifacts; the automated runner is optional.

Run the relational demos in order, then finish with the large-list scenario:

| Demo | Data shape | Manual guide |
|---|---|---|
| Program Portfolio Review | One parent with two independent children | [Setup and prompts](./program-portfolio-review/) |
| Crew Certification Coverage | Many-to-many through a junction list | [Setup and prompts](./crew-certification-coverage/) |
| Warranty Cost Chain | Four joins across five lists | [Setup and prompts](./warranty-cost-chain/) |
| Transaction Pivot | One flat list with 30,000 items | [Setup and prompts](./transaction-pivot/) |

All four target Copilot in SharePoint, use plain-English prompts, avoid Person columns, and use the fictional Zava/AeroSight brand.

## Before Presenting

- Save a copy the moment a page looks presentable. A bad edit can undo several good renders.
- Never say only "make this live." Scope each change to one thing and explicitly freeze everything else.
- Separate data turns from design turns.
- Describe what is visibly wrong and why it matters instead of prescribing pixel values.
- When behavior looks wrong, first ask the agent to explain its current rule.

## Optional Automation

The same scenarios are available as `.demo` scripts for the repository's niche Playwright runner:

- [`23-program-portfolio-review.demo`](../../tools/scripts/23-program-portfolio-review/23-program-portfolio-review.demo)
- [`24-crew-certification-coverage.demo`](../../tools/scripts/24-crew-certification-coverage/24-crew-certification-coverage.demo)
- [`25-warranty-cost-chain.demo`](../../tools/scripts/25-warranty-cost-chain/25-warranty-cost-chain.demo)
- [`26-transaction-pivot.demo`](../../tools/scripts/26-transaction-pivot/26-transaction-pivot.demo)

## Retrofitting an Existing Static Page

Use three turns and verify after each one.

### Turn 1: Diagnose Without Changes

```text
Don't change anything yet. Tell me where the data in this page currently comes from: the exact names of the variables or blocks holding the static data, and the name of the function that takes that data and renders the page. Just report it.
```

### Turn 2: Replace One Source

```text
Make one change and nothing else. Replace only the static data for the [first] list with a live read from the [first] list on this site. Leave the static data for every other list exactly as it is.

Do not change any HTML structure, any CSS, any layout, any rendering logic, or the script tag or its attributes. Everything stays inline in this single file. The rendering function must keep the same input shape it has now — you're changing where the data comes from, not what it looks like.

When the page loads, print the number of records read into the existing footer text so I can confirm it worked.
```

### Turn 3: Replace the Remaining Sources

```text
That worked. Now do the same for the [second] and [third] lists, one at a time, using the identical approach. Same constraints: no structural, styling, or layout changes, and no changes to the rendering logic.
```

If turn 2 changes the layout, revert to the saved copy rather than correcting forward.

## If It Says Scripting Is Unavailable

```text
This page already runs JavaScript successfully — it has a working refresh control, a load timestamp that updates, and live queries against the lists. So inline script is clearly permitted. Don't externalize anything: keep all script inline in this single HTML file, with no external files or CDN references. Do not modify the script tag's attributes — preserve whatever nonce the sandbox emits, exactly as it emits it. Tell me specifically which change you just made that failed, rather than concluding scripting is unavailable.
```

The usual cause is an edit that rewrote the script tag and dropped the sandbox-injected nonce.
