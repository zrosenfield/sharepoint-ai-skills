# Demo Spec — roadmap-timeline

## Demo Prompt

```
Generate an H2 roadmap for Zava from our Roadmap Items list. Use the slate palette.
```

---

## Setup

**Presenter:** Raj Patel, CTO of Zava Industries (or a PM filling in for him)
**Audience:** Executive team heading into a board meeting
**Context:** Zava just closed a strong Q2 FY2026. The board wants to see the H2 plan — what's in flight, what's coming, and where the risks are. Raj has all the roadmap data in a SharePoint list called "Roadmap Items." He types one sentence and hands the screen to the board.

---

## Beat-by-Beat Narrative

**Beat 1 — The ask (0:00–0:20)**
Raj opens the Zava Ops SharePoint site and navigates to the Copilot agent panel. He explains: "We've got 14 items across Platform, Integrations, and Go-to-Market all in our Roadmap Items list. I want a single visual I can drop into the board deck right now."

He types the demo prompt and hits send.

**Beat 2 — Data pull (0:20–0:40)**
The agent reads the Roadmap Items list — all 14 rows — without asking any follow-up questions. It confirms it found 3 swimlanes, 10 phase blocks, and 4 milestones, and that today (July 14) falls 13 days into the H2 window.

**Beat 3 — The reveal (0:40–1:20)**
A polished HTML roadmap appears. The board sees it immediately:
- The **month ruler** (Jul · Aug · Sep · Oct · Nov · Dec) stretches across the top
- Three color-coded swimlane rows fill the chart
- The **"Today" chip** (blue pill, 7% from the left) anchors where Zava stands right now
- The **amber Partner Program Launch** block in Go-to-Market catches every eye

**Beat 4 — Walk the chart (1:20–2:10)**
Raj points out the key details:

- **Platform row:** API v3 (blue, on track) and SOC 2 Audit (blue, on track) are both live. The API v3 Beta diamond at Aug 1 marks when 20 external customers get access.
- **Integrations row:** Salesforce Deep Integration is underway; HubSpot and Zapier 2.0 queue up behind it in lighter planned blocks.
- **Go-to-Market row:** Self-Serve Onboarding v2 is shipping. **Partner Program Launch is amber — flagged.** Jordan Kim owns the remediation. Enterprise Tier GA is the big Q4 bet.

**Beat 5 — The wow (2:10–2:30)**
Raj hovers over the amber Partner Program Launch block. A tooltip appears: "At risk · Jordan Kim · Aug 1 – Sep 30." He says: "One prompt, one SharePoint list, board-ready in under 30 seconds." He copies the HTML into the board deck.

---

## The "Wow" Beat

The audience sees a beautiful horizontal roadmap — professional enough for a board deck — generated from a SharePoint list with a single sentence. The today-line at 7% left visually confirms Zava is just two weeks into H2, making every planned block feel immediate and real. The amber Partner Program block is the natural conversation starter: it's visible at a glance and tells the board exactly where the risk lives.

---

## Presenter Tips

- **Point out the today-line first.** It anchors the audience in the present moment and makes the chart feel live, not static.
- **Call out the amber block explicitly.** Say "amber means at-risk" — don't assume the audience reads status colors. The contrast with the blue on-track blocks makes the risk pop.
- **Hover over blocks for tooltips.** The rich tooltip (title, dates, owner, status) shows the board this isn't just a pretty picture — the data is all there.
- **Zoom in on the planned blocks.** The lighter dashed-border planned blocks in Q4 (Enterprise Tier, FY27 Planning, Zapier 2.0) signal forward planning without overpromising.
- **Mention the milestone diamonds.** Point to the API v3 Beta diamond (Aug 1) and the SOC 2 Report diamond (Sep 15) — these are the tangible proof points the board will ask about.
- **Timing note:** The demo runs comfortably in 2 minutes. If you have 3, use the extra minute to demonstrate what a re-prompt looks like ("Mark Partner Program as delayed") so the audience sees the output is fully editable.
