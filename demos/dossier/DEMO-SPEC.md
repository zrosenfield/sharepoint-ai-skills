# Dossier Demo — Competitive Intelligence Brief

## Demo Prompt

```
Build me a competitor brief for the board meeting. Pull from our Competitors list. Use the deep-ink palette — I want it to feel serious.
```

---

## Setup

**Scenario:** Maya Chen, CEO of Zava Industries, is preparing for a Q2 FY2026 board meeting. The board is expected to pressure-test Zava's competitive positioning — Zava grew 35% YoY to $4.2M in Q2, but the board wants to know how the competitive landscape has shifted. Maya has a SharePoint list called "Competitors" with the four direct competitors Zava is actively tracking. She asks the AI to pull from that list and build a brief she can share as context before the meeting.

---

## Beat-by-Beat Walkthrough

**Beat 1 — Prompt lands, skill activates.**
The AI reads the Competitors list from SharePoint via `list_items`. It pulls all columns: name, type, status, stage, ARR, HQ, employees, primary market, tags, summary, and recent activity fields. No follow-up questions — the data is complete.

**Beat 2 — Mode is auto-determined.**
4 subjects detected. Grid mode is selected automatically (2–8 subjects = grid). No confirmation needed.

**Beat 3 — JSON is constructed and validated.**
The skill builds the JSON document: `report.palette = "deep-ink"`, `report.mode = "grid"`, 4 subject objects with all required fields. Validation passes — key facts are short labels, activity items are ordered most-recent first, all status colors map to valid tokens.

**Beat 4 — HTML renders.**
The skill reads `assets/dossier-template.html`, applies `palette-deep-ink` to `<body>`, injects the page header, 4 competitor cards in `.dossier-grid`, and the footer. Output is a single self-contained HTML file. No external dependencies.

**Beat 5 — The wow moment.**
The rendered page opens to a dark `#0f0e0c` background with four `#1a1916` cards glowing in a 2×2 grid. Gold `#d4a574` accents run through tag pills, activity date separators, and section headings. Each card is dense but airy — 6 key facts in a compact 2-column layout, 4 activity bullets at the bottom, a prose summary in between. It reads like a Goldman Sachs sector brief.

---

## Key Talking Points for the Presenter

**Status dots tell the story at a glance.**
Monday.com has a red dot ("Primary threat") — point to it first. Notion and ClickUp have amber ("Watch closely" / "Aggressive on price"). Coda has blue ("Niche overlap"). The board can read the risk landscape before reading a word.

**Hover effects add depth.**
Cards lift slightly on hover (subtle box-shadow transition). Demonstrate by hovering across all four cards — it signals interactivity and looks polished on a presentation display.

**Deep-ink makes it feel like a real analyst report.**
Tell the audience: "This is the same design system our exec-report skill uses — same palette tokens, same CSS variables. Any skill in the dossier family can use deep-ink, warm-paper, clean-white, or slate. The palette is a single class on `<body>`."

**One-pager mode is one prompt away.**
After showing the grid, suggest: "If I wanted to go deeper on Monday.com before the board session, I'd say: 'Give me a one-pager on Monday.com.' The skill re-renders the same JSON as a full briefing — hero block, two-column key facts, full timeline. Same data, different layout."

**No external dependencies.**
The HTML file is fully self-contained. It runs inside SharePoint's sandboxed iframe with no CDN calls, no web fonts, no external scripts. Show it loading instantly — no network requests.

---

## Presenter Tips

- Open the file in a browser at 1280px width or wider so the 2×2 grid snaps in cleanly.
- The card animation (`fadeUp` stagger, 70ms delay per card) plays on page load — reload the page live to show the staggered entrance.
- Point out the activity section at the bottom of the Monday.com card: "May 2026 — Launched monday CRM with native pipeline and deal management — direct competitive move." That's the kind of signal that triggers a board question.
- If asked about data sourcing: "This pulled directly from Maya's Competitors list in SharePoint. The AI called `list_items`, read every column, and built the brief without any manual copy-paste."
