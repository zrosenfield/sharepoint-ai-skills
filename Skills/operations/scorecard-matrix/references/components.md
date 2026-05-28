# Component Catalog

All components for the `scorecard-matrix` skill. Each entry covers: purpose, JSON schema, HTML markup pattern, and computation rules.

CSS class names and token names used here match `assets/scorecard-matrix-template.html` and `references/design-system.md` exactly.

---

## JSON Schema

Full document schema. All fields are required unless marked optional.

```json
{
  "report": {
    "title": "CRM Platform Evaluation",
    "subtitle": "Q2 2026 · Vendor Selection",
    "context": "Evaluating five CRM platforms for the SMB sales team ahead of a July go-live. Scored by the combined IT and RevOps working group.",
    "palette": "warm-paper",
    "footer": "Generated May 28, 2026 · 5 vendors · 6 dimensions"
  },
  "scale": 5,
  "dimensions": [
    { "id": "ease",    "label": "Ease of Use",    "weight": 0.20, "description": "Onboarding speed and daily UX for non-technical reps" },
    { "id": "integ",   "label": "Integration",    "weight": 0.20, "description": "Pre-built connectors to existing stack (Slack, ERP, email)" },
    { "id": "price",   "label": "Pricing",        "weight": 0.20, "description": "Total cost of ownership for 50-seat deployment" },
    { "id": "support", "label": "Support",        "weight": 0.15, "description": "SLA quality, dedicated CSM, response time benchmarks" },
    { "id": "custom",  "label": "Customization",  "weight": 0.15, "description": "Custom objects, workflow builder, API depth" },
    { "id": "privacy", "label": "Data Privacy",   "weight": 0.10, "description": "SOC 2 Type II, GDPR compliance, data residency options" }
  ],
  "entities": [
    {
      "id": "salesforce",
      "label": "Salesforce",
      "scores": {
        "ease":    { "score": 3, "note": "Steep learning curve" },
        "integ":   { "score": 5, "note": "Best-in-class" },
        "price":   { "score": 2, "note": "High TCO" },
        "support": { "score": 4, "note": "Dedicated CSM" },
        "custom":  { "score": 5, "note": "Unlimited depth" },
        "privacy": { "score": 5, "note": "SOC 2 + GDPR" }
      }
    }
  ]
}
```

**Field descriptions:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `report.title` | string | yes | Shown as editorial title |
| `report.subtitle` | string | no | Period, round, or context label |
| `report.context` | string | no | 1–2 sentences shown below title |
| `report.palette` | string | yes | One of: `warm-paper`, `deep-ink`, `clean-white`, `slate` |
| `report.footer` | string | no | Shown in page footer |
| `scale` | integer | yes | `5` or `10` |
| `dimensions[].id` | string | yes | Unique key; used as score object key in entities |
| `dimensions[].label` | string | yes | Column header text |
| `dimensions[].weight` | number | yes | Decimal 0–1; all weights must sum to 1.0 |
| `dimensions[].description` | string | no | What this dimension assesses; shown in weights note |
| `entities[].id` | string | yes | Unique key |
| `entities[].label` | string | yes | Row header (vendor name, candidate name, etc.) |
| `entities[].scores[dim_id].score` | number | yes | Integer in [1, scale] |
| `entities[].scores[dim_id].note` | string | no | Short phrase ≤6 words shown below score |

---

## Computed Fields

The skill must compute these before rendering. They are not stored in the JSON but derived at render time.

### Weighted Total

```
weighted_total = sum over all dimensions d of (scores[d].score × dimensions[d].weight)
```

Round to 2 decimal places. Maximum value = scale × 1.0 = scale.

### Rank

Sort entities by `weighted_total` descending. Assign rank 1 to highest. Ties: both entities share the lower (better) rank number (e.g. two entities tied at rank 2 both get rank 2; the next entity is rank 4).

### Column Average

```
column_avg[d] = average of scores[e][d].score across all entities e
```

Round to 1 decimal place. Shown in the bottom averages row, italicized.

---

## Header Section

The header follows the same thin editorial pattern as exec-report: a `.rpt-header` strip with the evaluation label, then an editorial title block.

**HTML pattern:**

```html
<div class="rpt-header">
  <div class="company">Vendor Evaluation</div>
  <div class="label">Q2 2026 · CRM Selection</div>
</div>
<div class="sc-title-block">
  <h1 class="sc-title">CRM Platform Evaluation</h1>
  <p class="sc-context">Evaluating five CRM platforms for the SMB sales team ahead of a July go-live. Scored by the combined IT and RevOps working group.</p>
</div>
```

---

## Score Matrix Table

The centerpiece. A CSS-heatmapped table inside a horizontally-scrollable wrapper.

### Table Structure

```html
<div class="sc-matrix-wrap">
  <table class="sc-matrix">
    <thead>
      <tr class="sc-thead-row">
        <th class="sc-th-entity" scope="col"></th>
        <!-- One <th> per dimension -->
        <th class="sc-th-dim" scope="col">
          <span class="sc-dim-name">Ease of Use</span>
          <span class="sc-dim-weight">20%</span>
        </th>
        <!-- ... more dimensions ... -->
        <th class="sc-th-total" scope="col">
          <span class="sc-dim-name">Weighted</span>
          <span class="sc-dim-weight">Total</span>
        </th>
        <th class="sc-th-rank" scope="col">Rank</th>
      </tr>
    </thead>
    <tbody>
      <!-- Entity rows -->
      <tr class="sc-entity-row sc-winner" data-entity="salesforce">
        <td class="sc-entity-label">Salesforce</td>
        <!-- Score cells -->
        <td class="sc-score-cell" style="background:#f9e6e2">
          <span class="sc-score">3</span>
          <span class="sc-note">Steep learning curve</span>
        </td>
        <!-- ... more score cells ... -->
        <td class="sc-total-cell">
          <span class="sc-total-value">3.95</span>
        </td>
        <td class="sc-rank-cell">
          <span class="sc-rank-badge sc-rank-1">1st</span>
        </td>
      </tr>
      <!-- ... more entity rows ... -->

      <!-- Averages row -->
      <tr class="sc-avg-row">
        <td class="sc-avg-label">Column avg</td>
        <td class="sc-avg-cell">3.4</td>
        <!-- ... more avg cells ... -->
        <td class="sc-avg-total"></td>
        <td class="sc-avg-rank"></td>
      </tr>
    </tbody>
  </table>
</div>
```

### Winner Row

The entity with `rank = 1` gets class `sc-winner` on its `<tr>`. CSS applies a left accent border and very light accent background tint to distinguish it.

If two entities tie for rank 1, both rows get `sc-winner`.

### Heatmap Cell Style

For each score cell, compute the background hex from the score value, the scale, and the chosen palette. See `references/design-system.md` for the exact hex values per palette tier.

Computation:

```
t = (score - 1) / (scale - 1)

if t < 0.35:   background = LOW_HEX  (palette-specific, cool/negative tint)
elif t >= 0.65: background = HIGH_EX  (palette-specific, accent tint)
else:           background = MID_HEX  (palette-specific, neutral surface)
```

Emit directly as `style="background:{{HEX}}"`. Text color is always `var(--ink)` (inherited), which ensures readability on all tiers.

**Example — warm-paper palette, score=2 on 1–5 scale:**
```
t = (2-1)/(5-1) = 0.25  → LOW tier
background: #fde8e8
```

**Example — warm-paper palette, score=5 on 1–5 scale:**
```
t = (5-1)/(5-1) = 1.0   → HIGH tier
background: #f9e6e2
```

### Rank Badges

Ranks 1–3 get styled pill badges with gold/silver/bronze coloring. Ranks 4+ get a plain pill.

```html
<!-- Rank 1 -->
<span class="sc-rank-badge sc-rank-1">1st</span>

<!-- Rank 2 -->
<span class="sc-rank-badge sc-rank-2">2nd</span>

<!-- Rank 3 -->
<span class="sc-rank-badge sc-rank-3">3rd</span>

<!-- Rank 4+ (plain) -->
<span class="sc-rank-badge sc-rank-n">4th</span>
```

Ordinal suffix rules: 1→1st, 2→2nd, 3→3rd, 4–10→Nth, 11–13→Nth (use "th"), then resume st/nd/rd pattern.

### Averages Row

The final row of `<tbody>`. Italicized and muted to differentiate from entity rows. Shows `column_avg` for each dimension; the total and rank cells are left empty.

```html
<tr class="sc-avg-row">
  <td class="sc-avg-label">Column avg</td>
  <td class="sc-avg-cell">3.4</td>
  <td class="sc-avg-cell">4.2</td>
  <td class="sc-avg-cell">2.8</td>
  <!-- ... -->
  <td class="sc-avg-total"></td>
  <td class="sc-avg-rank"></td>
</tr>
```

---

## Rankings Callout

A small ordered list placed below the matrix. Shows 1st, 2nd, and 3rd place (or all entities if fewer than 4) with their weighted totals and a one-sentence rationale synthesized from the highest- and lowest-scoring dimensions.

**HTML pattern:**

```html
<section class="sc-rankings card">
  <h2>Rankings</h2>
  <div class="sc-rank-list">
    <div class="sc-rank-item">
      <span class="sc-rank-badge sc-rank-1">1st</span>
      <div class="sc-rank-detail">
        <span class="sc-rank-name">Salesforce</span>
        <span class="sc-rank-score">3.95 / 5.00</span>
        <p class="sc-rank-rationale">Leads on Integration and Customization; the steep learning curve keeps Ease of Use at a 3, but strong performance elsewhere carries it to first place.</p>
      </div>
    </div>
    <div class="sc-rank-item">
      <span class="sc-rank-badge sc-rank-2">2nd</span>
      <div class="sc-rank-detail">
        <span class="sc-rank-name">HubSpot</span>
        <span class="sc-rank-score">3.78 / 5.00</span>
        <p class="sc-rank-rationale">Best Ease of Use score in the evaluation; constrained by below-average Customization depth for larger team needs.</p>
      </div>
    </div>
    <div class="sc-rank-item">
      <span class="sc-rank-badge sc-rank-3">3rd</span>
      <div class="sc-rank-detail">
        <span class="sc-rank-name">Zoho CRM</span>
        <span class="sc-rank-score">3.55 / 5.00</span>
        <p class="sc-rank-rationale">Strongest Pricing score across all vendors; loses ground on Support SLA quality and Integration breadth.</p>
      </div>
    </div>
  </div>
</section>
```

**Rationale generation rule:** For each ranked entity, identify the dimension(s) where it scored highest and lowest relative to its peers. Write one sentence: "Leads on [best dimension(s)]; [contrast with weakness or constraint]." Keep it under 30 words.

---

## Dimension Weights Note

A compact reference section showing each dimension, its weight percentage, and the 1-line description of what was assessed. Helps readers understand the scoring methodology.

**HTML pattern:**

```html
<section class="sc-weights-note card">
  <h2>Scoring Methodology</h2>
  <div class="sub">Dimension weights and assessment criteria</div>
  <div class="sc-weights-grid">
    <div class="sc-weight-row">
      <span class="sc-weight-label">Ease of Use</span>
      <span class="sc-weight-pct">20%</span>
      <span class="sc-weight-desc">Onboarding speed and daily UX for non-technical reps</span>
    </div>
    <div class="sc-weight-row">
      <span class="sc-weight-label">Integration</span>
      <span class="sc-weight-pct">20%</span>
      <span class="sc-weight-desc">Pre-built connectors to existing stack (Slack, ERP, email)</span>
    </div>
    <!-- ... more dimensions ... -->
  </div>
</section>
```

---

## Full Example JSON Document

A complete validated document the skill can use as a reference.

```json
{
  "report": {
    "title": "CRM Platform Evaluation",
    "subtitle": "Q2 2026 · SMB Sales Team",
    "context": "Evaluating five CRM platforms for a 50-seat SMB sales team ahead of a July go-live. Scored by the combined IT and RevOps working group using a 1–5 scale.",
    "palette": "warm-paper",
    "footer": "Generated May 28, 2026 · 5 vendors · 6 dimensions"
  },
  "scale": 5,
  "dimensions": [
    { "id": "ease",    "label": "Ease of Use",   "weight": 0.20, "description": "Onboarding speed and daily UX for non-technical reps" },
    { "id": "integ",   "label": "Integration",   "weight": 0.20, "description": "Pre-built connectors to existing stack (Slack, ERP, email)" },
    { "id": "price",   "label": "Pricing",       "weight": 0.20, "description": "Total cost of ownership for 50-seat deployment" },
    { "id": "support", "label": "Support",       "weight": 0.15, "description": "SLA quality, dedicated CSM, response time benchmarks" },
    { "id": "custom",  "label": "Customization", "weight": 0.15, "description": "Custom objects, workflow builder, API depth" },
    { "id": "privacy", "label": "Data Privacy",  "weight": 0.10, "description": "SOC 2 Type II, GDPR compliance, data residency options" }
  ],
  "entities": [
    {
      "id": "salesforce", "label": "Salesforce",
      "scores": {
        "ease":    { "score": 3, "note": "Steep curve" },
        "integ":   { "score": 5, "note": "Best-in-class" },
        "price":   { "score": 2, "note": "High TCO" },
        "support": { "score": 4, "note": "Dedicated CSM" },
        "custom":  { "score": 5, "note": "Unlimited depth" },
        "privacy": { "score": 5, "note": "SOC 2 + GDPR" }
      }
    },
    {
      "id": "hubspot", "label": "HubSpot",
      "scores": {
        "ease":    { "score": 5, "note": "Easiest onboarding" },
        "integ":   { "score": 4, "note": "Good ecosystem" },
        "price":   { "score": 3, "note": "Mid-tier pricing" },
        "support": { "score": 4, "note": "Responsive team" },
        "custom":  { "score": 3, "note": "Limited objects" },
        "privacy": { "score": 4, "note": "GDPR ready" }
      }
    },
    {
      "id": "zoho", "label": "Zoho CRM",
      "scores": {
        "ease":    { "score": 3, "note": "Moderate learning" },
        "integ":   { "score": 3, "note": "Some gaps" },
        "price":   { "score": 5, "note": "Best value" },
        "support": { "score": 3, "note": "Average response" },
        "custom":  { "score": 4, "note": "Good depth" },
        "privacy": { "score": 3, "note": "Adequate" }
      }
    },
    {
      "id": "pipedrive", "label": "Pipedrive",
      "scores": {
        "ease":    { "score": 4, "note": "Clean pipeline UI" },
        "integ":   { "score": 3, "note": "Limited native" },
        "price":   { "score": 4, "note": "Competitive" },
        "support": { "score": 3, "note": "Self-serve focus" },
        "custom":  { "score": 2, "note": "Basic only" },
        "privacy": { "score": 3, "note": "Standard" }
      }
    },
    {
      "id": "dynamics", "label": "MS Dynamics",
      "scores": {
        "ease":    { "score": 2, "note": "Complex setup" },
        "integ":   { "score": 5, "note": "M365 native" },
        "price":   { "score": 2, "note": "Enterprise pricing" },
        "support": { "score": 5, "note": "Premier support" },
        "custom":  { "score": 5, "note": "Power Platform" },
        "privacy": { "score": 5, "note": "Azure compliance" }
      }
    }
  ]
}
```

**Computed values from this document (skill must derive these):**

| Entity | ease×0.20 | integ×0.20 | price×0.20 | support×0.15 | custom×0.15 | privacy×0.10 | Weighted Total | Rank |
|---|---|---|---|---|---|---|---|---|
| Salesforce | 0.60 | 1.00 | 0.40 | 0.60 | 0.75 | 0.50 | **3.85** | 1st |
| HubSpot | 1.00 | 0.80 | 0.60 | 0.60 | 0.45 | 0.40 | **3.85** | 1st (tie) |
| Zoho CRM | 0.60 | 0.60 | 1.00 | 0.45 | 0.60 | 0.30 | **3.55** | 3rd |
| Pipedrive | 0.80 | 0.60 | 0.80 | 0.45 | 0.30 | 0.30 | **3.25** | 4th |
| MS Dynamics | 0.40 | 1.00 | 0.40 | 0.75 | 0.75 | 0.50 | **3.80** | 2nd |

Column averages: ease=3.4, integ=4.0, price=3.2, support=3.8, custom=3.8, privacy=4.0
