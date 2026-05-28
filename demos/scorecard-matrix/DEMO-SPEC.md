# Demo Spec — scorecard-matrix

**Scenario:** Zava Industries CRM Evaluation  
**Duration:** 2–3 minutes  
**Presenter:** VP Sales Jordan Kim needs to present a vendor recommendation to CEO Maya Chen and the exec team.

---

## DEMO PROMPT

```
I need a CRM evaluation scorecard for the exec team. We're replacing our legacy Salesforce setup — we've outgrown it and the sales team is frustrated. Here are our scores across the five shortlisted vendors on a 1–5 scale:

Dimensions and weights:
- Ease of Use: 20%
- Integration Depth: 25%
- Pricing Fit: 20%
- Support Quality: 15%
- Customization: 10%
- Data Privacy: 10%

Vendor scores:
| Vendor      | Ease | Integration | Pricing | Support | Custom | Privacy | Notes                        |
|-------------|------|-------------|---------|---------|--------|---------|------------------------------|
| HubSpot     | 5    | 4           | 4       | 4       | 3      | 4       | Best UX; limited deep custom |
| Salesforce  | 3    | 5           | 2       | 4       | 5      | 5       | Powerful but overbuilt for stage |
| Pipedrive   | 4    | 3           | 5       | 3       | 3      | 3       | Simple; weak enterprise features |
| Close.io    | 4    | 3           | 4       | 5       | 3      | 3       | Great support; limited integrations |
| Freshsales  | 4    | 4           | 4       | 3       | 3      | 4       | Good value; newer ecosystem  |

Use the clean-white palette — this is going straight into the board deck. Can you build the scorecard?
```

---

## Setup

**Who:** Jordan Kim, VP Sales at Zava Industries. Zava just closed a strong Q2 FY2026 ($4.2M revenue) and is pushing past 150 employees. The sales team has been running on a patchwork of spreadsheets and a legacy Salesforce instance that was never properly configured. Jordan's team spent the last three weeks scoring five CRM vendors — now she needs to turn that raw data into a decision document she can drop into the exec deck for Maya Chen.

**What she has:** A raw table of scores she's been tracking in a Teams chat. She pastes it into the AI alongside her weights and a one-line description of the context.

**What she needs in return:** A polished, standalone HTML scorecard she can send to the exec team before the Thursday review meeting.

---

## Beat-by-Beat Walkthrough

**Beat 1 — Data parsing (0:00–0:20)**  
The skill immediately recognizes the pasted table as a complete data source. No interview needed — it has vendors, dimensions, weights, and scores. It parses the six weighted dimensions (weights sum to 1.0: 0.20+0.25+0.20+0.15+0.10+0.10), confirms the 1–5 scale, and identifies the clean-white palette.

**Beat 2 — JSON construction + validation (0:20–0:50)**  
The skill builds the JSON document internally: five entities, six dimensions, 30 scored cells. It computes weighted totals for each vendor and assigns ranks. HubSpot surfaces at 4.10 — highest weighted total. Salesforce lands at 3.85 (second) despite its perfect integration and customization scores, dragged down by the 2/5 on pricing. Freshsales comes in as the dark horse at 3.75 (third). All validation checks pass.

**Beat 3 — HTML render (0:50–1:30)**  
The skill replaces all template placeholders and renders the full scorecard. The matrix table appears with clean-white palette (white background, forest-green accent). Heatmap backgrounds are pre-baked inline: Salesforce's pricing cell glows red (#fee2e2), HubSpot's ease cell glows green (#edf7f1). The HubSpot row carries the winner highlight — a forest-green left accent border and a faint green tint on the label cell.

**Beat 4 — Rank badges + callout (1:30–2:00)**  
Below the matrix, a Rankings callout shows the top three in descending order with gold/silver/bronze pill badges. HubSpot's rationale reads: "Leads on Ease of Use and earns strong marks across Integration, Pricing, and Support — the most balanced scorecard in the evaluation." Salesforce's entry notes the pricing penalty. Freshsales gets a "dark horse" note.

**Beat 5 — Methodology section (2:00–2:30)**  
The Scoring Methodology card at the bottom lists all six dimensions with their weights and descriptions — giving the exec team full transparency on how the numbers were derived.

---

## The "Wow" Beat

**At 1:00 — the matrix lands.**

The audience sees the full heatmap grid in one shot:
- Salesforce's pricing cell is **red** — score 2, visually obvious penalty
- HubSpot's ease cell is **green** — score 5, the only cell with that color in that column
- HubSpot row has a **forest-green left border** and subtle tinted background — winner at a glance
- Gold `1st` badge, silver `2nd`, bronze `3rd` — no ambiguity about the recommendation

The presenter can point directly at the visual contrast: "See how Salesforce's pricing cell is the only red one across HubSpot's row? That's why, even with perfect integration and customization scores, it can't catch HubSpot under our weighting."

---

## Presenter Tips

1. **Point to the Salesforce pricing cell first.** It's the most dramatic contrast — a lone red cell in a sea of greens and neutrals. Say: "Salesforce scores 5/5 on integration and customization, but that 2 on pricing, weighted at 20%, costs them the top slot."

2. **Show the winner row highlight.** The green left border on HubSpot is subtle but clear. Say: "The scorecard automatically highlights the recommended vendor — no manual formatting needed."

3. **Reference the column averages row.** The italic "Column avg" row at the bottom shows Integration and Pricing both average 3.8. Say: "Integration depth is the highest-weighted dimension at 25% — that's where HubSpot and Salesforce separate from the pack."

4. **Use the Methodology section.** When an exec asks "why did you weight integration so high?", flip to the bottom card. The 1-line description for each dimension answers the question directly.

5. **Suggest deep-ink for drama.** If the audience is small and the room is dark, say: "This also renders in a dark exec theme — same data, higher contrast. Want to see it?" (Switch `palette-clean-white` to `palette-deep-ink` on the body tag to demo.)

6. **Show it took one paste.** Scroll back up to the prompt. The entire scorecard — 30 scored cells, computed totals, heatmap, rank badges, methodology — came from one pasted table.
