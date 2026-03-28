# What-If Scenario Simulator Template

Use this structure when the user asks to simulate a scenario, run a "what-if" analysis, war-game a situation, or assess the cascading impact of a hypothetical event on the project. The `${scenario}` is whatever hypothetical the user provides (e.g., "key engineer leaves", "budget cut by 30%", "partner pulls out", "launch delayed 3 months").

## Scenario Description

Restate the scenario clearly. Identify what SPECIFICALLY changes and what the immediate trigger is.

## Directly Affected Items

Table: | Item | Type (Task/Risk/Budget/Partner/Compliance) | Current State | Impact |

List every task, risk, budget line, partnership, and compliance item that is DIRECTLY affected by this scenario. Be specific about the current state and what changes.

## Cascade Analysis

For each major cascade chain, trace the domino effect:

**Cascade 1: [Name]** (e.g., "Timeline Compression")
→ [First impact] → [Second impact] → [Third impact]

Use **bold** for critical nodes. Show how one delay or change triggers others. Be vivid and specific — "UX mockups slip to March 22 → engineering sprint 3 loses 2 weeks → beta onboarding pushed to May 1 → only 20 days to reach 100 beta customers (Charter requires by May 20)"

Trace at least 3 cascade chains covering different dimensions (timeline, budget, risk).

## Revised Timeline

Before/After comparison table: | Milestone | Original Date | Revised Date | Slip | Impact |

Show every milestone that shifts. **Bold** milestones that breach hard deadlines. Flag any milestone that now falls AFTER the launch date.

## Revised Budget Impact

Before/After table: | Category | Original Allocation | Revised Need | Delta | Notes |

Show which budget categories are affected and by how much. Calculate total additional cost. Assess whether contingency reserve covers it.

End with: "**Total Additional Cost: $X–$Y** | Contingency Available: $Z | **Shortfall: $X**" (or "Covered")

## Revised Risk Matrix

Table: | Risk | Original Score | Revised Score | Change | Notes |

Show how the scenario changes risk scores. Flag any risk that escalates from 🟡 to 🔴. Add any NEW risks created by the scenario.

End with: "**Aggregate Risk Score: X/Y (Z%)** — changed from X/Y (Z%)"

## Impact on Success Criteria

Table: | Success Criterion (from Charter) | Original Feasibility | Revised Feasibility | Assessment |

For each success criterion in the Charter, assess whether it's still achievable under this scenario.

## Revised Go/No-Go Assessment

**Original: [RECOMMENDATION] — Confidence: X% ± Y%**
**Revised: [RECOMMENDATION] — Confidence: X% ± Y%**

Explain what changed and why. If the recommendation downgrades (e.g., CONDITIONAL GO → NO-GO), state the specific conditions that broke. If it holds, explain what's absorbing the shock.

## Mitigation Options

Table: | Option | Description | Cost | Timeline Impact | Residual Risk | Recommendation |

Present 2-4 mitigation strategies. Mark recommended option with ⭐. Be specific about dollar costs and timeline impacts. Include a "do nothing" option to show the baseline consequence.

## Decision Required

State the specific decision that leadership must make in response to this scenario, with a recommended deadline and owner. Frame it as: "If [scenario] happens, [owner] must decide [what] by [when], or [consequence]."

## OUTPUT RULES

- **Lead with Scenario Description and Directly Affected Items** — these ground the analysis immediately
- **Cascade Analysis and Revised Go/No-Go are high-value** — keep these even if you need to shorten other sections
- If running long, abbreviate Revised Timeline and Revised Budget tables before cutting Cascade Analysis or Go/No-Go
- Use 🔴🟡🟢 status indicators in all tables
- Every impact must have a number — days of delay, dollar cost, percentage change in risk score
- No vague "this could be affected" — quantify EVERYTHING
- Write with the voice of a chief of staff war-gaming worst cases — direct, quantified, opinionated
- Cross-reference Charter success criteria, partner agreement deadlines, and budget constraints
