# Demo: exec-report — Zava Industries Q2 FY2026

## DEMO PROMPT

*Attach `data/q2-deals.csv` and `data/q2-projects.csv` before sending.*

```
Build me a Q2 executive summary for Zava from q2-deals.csv and q2-projects.csv.
Audience: exec team (Maya Chen, Raj Patel, Jordan Kim). Warm paper palette.
```

**Fallback prompt** (if files can't be attached — paste inline from `data/q2-deals.csv`):
> "Build me a Q2 executive summary for Zava. Here's our deals data: [paste CSV contents]. Warm paper palette."

---

## Setup

You're Jordan Kim, VP of Sales at Zava Industries, doing Monday morning prep before an all-hands review with Maya and Raj. You have your Q2 numbers in your head (and in a spreadsheet), and you want a finished exec summary in the next two minutes — not a deck, not a wall of text, something they'll actually read.

---

## What Happens — Beat by Beat

**Beat 1: Attach and go (0:00–0:20)**
Attach `q2-deals.csv` and `q2-projects.csv`, type the two-line prompt, and send. The skill reads both files immediately — no back-and-forth because all the data is there. It skips straight to building the JSON.

**Beat 2: The skill narrates its work (0:20–0:45)**
The agent confirms the data in a quick bullet list: "Confirmed Q2 revenue $4.2M, 47 deals, 6 monthly data points, 5 pipeline deals, 6 workstreams." Then it announces the component sequence: hero → KPI row → trend → by-region bar list → QoQ/YoY compare → pipeline table → workstream status → highlights. This is a good moment to point out that the skill is making editorial decisions, not just formatting data.

**Beat 3: The JSON appears (0:45–1:05)**
The agent outputs the full validated JSON document. Point out the structure — `palette: "warm-paper"`, the `blocks` array, the pre-computed SVG coordinates inside the trend block. "This is the consistency layer — the HTML is 100% determined by this JSON."

**Beat 4: The HTML renders (1:05–1:40)**
The agent delivers `zava-q2-fy2026.html` as a file attachment. Open it in the browser. The audience sees the warm-paper report materialize: the hero sentence in large type, the four KPI cards counting up, then the trend line drawing across the chart. The reveal moment is Jun at $1.31M — the line lands at the top of the chart with clear visual separation from the Q1 ghost line below it.

**Beat 5: The wow moment (1:40–2:05)**
Hover over the trend line. The tooltip snaps to each month as you move across: "Jan 2026 · $820K" ... "Jun 2026 · $1.31M". Then scroll down to the workstream status grid. Point out the red dot on ERP vendor selection — the system captured "decision needed this week" and surfaced it in the highlights section as "Action needed." The report isn't just data — it has an opinion.

**Beat 6: The close (2:05–2:20)**
Scroll to the highlights. Read the "Action needed" card out loud: ERP pricing hold, June 15, decide now. Tell the audience: "Maya got this in her inbox two minutes ago. She didn't ask for a deck. She asked the agent."

---

## The "Wow" Beat

The trend tooltip. It's a tiny thing — hover over the SVG, watch the dot activate and the tooltip snap. No chart library. No CDN. This HTML will open inside a SharePoint sandboxed iframe with zero external dependencies and it still does this. That's the technical story in 10 seconds.

The narrative story is the "Action needed" highlight. The skill didn't just format numbers — it read the ERP pricing hold note, understood it was urgent, and surfaced it as a separate call to action. That's the AI adding value, not just formatting.

---

## Presenter Tips

**What to highlight:**
- The hero sentence typography — 22ch max-width enforces the editorial line break naturally. Point at it.
- The KPI cards: four numbers, no more. "A good exec report doesn't have 12 KPIs. It has four."
- The compare section: side-by-side QoQ and YoY panels. "This is the standard ask from a CFO — here it is, zero config."
- The workstream status grid: red dot jumps out. Audiences immediately scan for red. The ERP block is doing its job.

**What to hover/click:**
1. Hover the trend SVG slowly left to right — let the tooltip follow your cursor through each month.
2. Hover over the bar-list region rows — the dimming effect on non-hovered rows is a subtle nice touch.
3. Scroll the page slowly so the bar animations replay in-viewport (works if you refresh and scroll at the right speed).

**Common audience questions:**
- "Can we change the palette?" — Yes, four options, swap one word in the JSON.
- "Can it pull from a SharePoint list?" — Yes, give it a list URL instead of pasting data and it calls `list_items` directly.
- "How long did this take?" — "About 45 seconds from prompt to open-in-browser."

**Pitfalls to avoid:**
- Don't demo with a slow network — the file is fully self-contained and offline-capable once downloaded.
- If the SharePoint chat truncates the HTML output, show the JSON first, then open the pre-built `golden-output.html` as the backup.
