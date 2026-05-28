# Component Catalog

All components for the `exec-report` skill. Each entry covers: type string, when to use it, full props schema, HTML markup pattern, and an example JSON block.

CSS class names and token names used here match `assets/report-template.html` and `references/design-system.md` exactly.

---

## `hero`

**When to use:** Always first. Generates the thin `.rpt-header` strip (company name + report label) and the large editorial `.hero` sentence below it. One per report. The hero sentence is the most important line on the page — it should state the main fact in plain language with the key number highlighted.

**Hero sentence rules:**
- Write it as one complete sentence that a reader could take away if they saw nothing else.
- Wrap numbers in `<span class="num">` for tabular-num formatting.
- Wrap the key number and the trend word in `<span class="accent">` to pull them in the palette color.
- Keep it under 22 words — the `max-width:22ch` CSS enforces a natural editorial line break.
- Do not pad it with qualifiers. "ACME Corp closed $4.2M in Q2, up 8% from Q1." is better than "ACME Corp achieved a strong Q2 revenue performance of $4.2M…"

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company` | string | yes | Company or report owner name, shown in header strip |
| `report_label` | string | yes | Report type + period, e.g. `"Q2 FY2026 · Revenue Report"` |
| `sentence_html` | string | yes | The editorial hero sentence with inline `<span>` markup |

**HTML pattern:**
```html
<div class="rpt-header">
  <div class="company">ACME Corp</div>
  <div class="label">Q2 FY2026 · Revenue Report</div>
</div>
<h1 class="hero">
  ACME Corp closed <span class="accent num">$4.2M</span> across
  <span class="num">47</span> deals in Q2 FY2026,
  <span class="accent">up 8%</span> from Q1.
</h1>
```

**Example JSON block:**
```json
{
  "type": "hero",
  "props": {
    "company": "ACME Corp",
    "report_label": "Q2 FY2026 · Revenue Report",
    "sentence_html": "ACME Corp closed <span class=\"accent num\">$4.2M</span> across <span class=\"num\">47</span> deals in Q2 FY2026, <span class=\"accent\">up 8%</span> from Q1."
  }
}
```

---

## `kpi-row`

**When to use:** Immediately after `hero`. Shows 2–4 headline metrics in a grid of cards with large light-weight numbers. These are the numbers the reader should remember. Do not use for more than 4 items — each additional card dilutes attention.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `items` | array | yes | 2–4 KPI objects |

Each item:

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | yes | All-caps tiny label above the value, e.g. `"Total revenue"` |
| `value` | string | yes | Formatted display value, e.g. `"$4.2M"`, `"47"`, `"89%"` |
| `delta` | string | no | Change label, e.g. `"↑ 8% QoQ"`, `"↓ 3 pts"` |
| `delta_dir` | string | no | `"up"` (accent color) or `"down"` (negative color). Omit for neutral. |
| `value_override_style` | string | no | Inline style for the value element — use when the value is a word not a number, e.g. `"font-size:clamp(24px,3vw,36px);font-weight:400"` |

**HTML pattern:**
```html
<section class="kpis">
  <div class="kpi">
    <div class="kpi-label">Total revenue</div>
    <div class="kpi-value">$4.2M</div>
    <div class="kpi-delta up">↑ 8% QoQ</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Deals closed</div>
    <div class="kpi-value">47</div>
    <div class="kpi-delta up">↑ 5 QoQ</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Avg deal size</div>
    <div class="kpi-value">$89K</div>
    <div class="kpi-delta down">↓ 3% QoQ</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Top segment</div>
    <div class="kpi-value" style="font-size:clamp(24px,3vw,36px);font-weight:400">Enterprise</div>
    <div class="kpi-delta">44% of total</div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "kpi-row",
  "props": {
    "items": [
      { "label": "Total revenue",  "value": "$4.2M", "delta": "↑ 8% QoQ",  "delta_dir": "up" },
      { "label": "Deals closed",   "value": "47",    "delta": "↑ 5 QoQ",   "delta_dir": "up" },
      { "label": "Avg deal size",  "value": "$89K",  "delta": "↓ 3% QoQ",  "delta_dir": "down" },
      { "label": "Top segment",    "value": "Enterprise", "delta": "44% of total",
        "value_override_style": "font-size:clamp(24px,3vw,36px);font-weight:400" }
    ]
  }
}
```

---

## `trend`

**When to use:** Values over time — monthly revenue, weekly tickets, quarterly headcount. Renders a pure inline SVG with grid lines, axis labels, hover tooltips, and an optional ghost line showing the prior period. One per report.

**The skill computes all SVG coordinates.** Computation rules:
- ViewBox is always `"0 0 800 220"`.
- Plot area: left `x=60`, right `x=780`, top `y=20`, bottom `y=184`.
- `x_i = 60 + (i / (N-1)) × 720` (round to 1 decimal)
- Combined min/max uses both `data` and `prior_data` (if provided).
- `y_i = 184 − ((v − min) / range) × 164` (round to 1 decimal; if range=0 use y=102)
- Grid lines: pick 4–5 evenly-spaced "nice" values within the data range. Y-axis labels at `x=52`, `text-anchor=end`.
- X-axis labels at `y=204`.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Card heading |
| `sub` | string | no | Subtitle shown below heading, e.g. `"Monthly revenue · ghost line = Q1"` |
| `labels` | array of strings | yes | Period labels; length must match `data` |
| `data` | array of numbers | yes | Current period values. 3–12 entries. |
| `prior_data` | array of numbers | no | Prior period values for ghost line. Same length as `data`. |
| `value_format` | string | no | How to display values in tooltip, e.g. `"${{v}}K"` or `"{{v}}%"`. If omitted, use raw number. |

**Tooltip JS** (goes in `{{INLINE_SCRIPT}}`): embed `TREND_DATA` array with `{xi, yi, label, val}` for each point. See template script comment for full hover implementation pattern.

**HTML pattern (abbreviated):**
```html
<section class="card trend-card">
  <h2>Revenue trend</h2>
  <div class="sub">Monthly revenue · Q2 FY2026</div>
  <div class="trend-wrap">
    <svg id="trend-svg" viewBox="0 0 800 220" preserveAspectRatio="none"
         role="img" aria-label="Monthly revenue trend">
      <g class="grid">
        <line class="trend-grid" x1="60" y1="{{GRID_Y}}" x2="780" y2="{{GRID_Y}}"/>
        <text class="trend-axis-label" x="52" y="{{LABEL_Y}}" text-anchor="end">{{LABEL}}</text>
        <!-- ...repeat for each grid line... -->
      </g>
      <!-- prior ghost line (optional) -->
      <path class="trend-prior" d="M{{x0}},{{y0}} L..."/>
      <!-- current area fill -->
      <path class="trend-area" d="M{{x0}},{{y0}} L... L{{xN}},184 L{{x0}},184 Z"/>
      <!-- current line (animated draw) -->
      <path class="trend-line" d="M{{x0}},{{y0}} L..."/>
      <!-- hover dots (hidden by default, shown by JS) -->
      <g class="dots">
        <circle class="trend-dot" data-i="0" cx="{{x0}}" cy="{{y0}}" r="5"/>
        <!-- ...one per data point... -->
      </g>
      <!-- vertical guideline (moved by JS on hover) -->
      <line class="trend-guideline" id="trend-guideline" x1="{{x0}}" y1="20" x2="{{x0}}" y2="184"/>
      <!-- x-axis labels -->
      <g class="x-labels">
        <text class="trend-axis-label" x="{{x0}}" y="204" text-anchor="middle">{{label0}}</text>
        <!-- ...one per label... -->
      </g>
    </svg>
    <div class="trend-tooltip" id="trend-tooltip"></div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "trend",
  "props": {
    "title": "Monthly Revenue",
    "sub": "Jan–Jun 2026 · ghost line shows Jan–Jun 2025",
    "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "data":   [820, 910, 880, 1050, 1120, 1310],
    "prior_data": [700, 780, 760, 840, 870, 910],
    "value_format": "${{v}}K"
  }
}
```

---

## `bar-list`

**When to use:** Category breakdown where relative size matters — spend by department, revenue by region, pipeline by stage. Renders as labeled rows with animated fill bars. No chart library. Use 3–10 items.

Bar fill animation: each `.seg-fill` carries a `data-share` attribute (0–1). JS on `DOMContentLoaded` sets `transform:scaleX(share)` to trigger the CSS entrance transition. Without JS (or with `prefers-reduced-motion`), bars render at full scale immediately.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Card heading |
| `sub` | string | no | Subtitle below heading |
| `items` | array | yes | 3–10 segment objects, sorted descending |

Each item:

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Row label |
| `amount` | string | yes | Formatted primary value, e.g. `"$1.84M"` |
| `share` | number | yes | 0–1. Proportion of the largest item. Largest item = 1.0. |
| `meta` | string | no | Small secondary line below amount, e.g. `"44% · ↑ 12%"` |

**JS snippet** (goes in `{{INLINE_SCRIPT}}`):
```javascript
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.seg-fill').forEach(function(el) {
    el.style.transform = 'scaleX(' + parseFloat(el.dataset.share || 0) + ')';
  });
});
```

**HTML pattern:**
```html
<section class="card">
  <h2>By region</h2>
  <div class="sub">Revenue share and QoQ change</div>
  <div class="segments">
    <div class="seg-row">
      <span class="seg-name">North America</span>
      <div class="seg-track"><div class="seg-fill" data-share="1.00"></div></div>
      <div class="seg-amt">$1.84M<span class="seg-pct">44% · ↑ 12%</span></div>
    </div>
    <div class="seg-row">
      <span class="seg-name">Europe</span>
      <div class="seg-track"><div class="seg-fill" data-share="0.60"></div></div>
      <div class="seg-amt">$1.10M<span class="seg-pct">26% · ↑ 4%</span></div>
    </div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "bar-list",
  "props": {
    "title": "By region",
    "sub": "Revenue share and QoQ change",
    "items": [
      { "name": "North America", "amount": "$1.84M", "share": 1.00, "meta": "44% · ↑ 12%" },
      { "name": "Europe",        "amount": "$1.10M", "share": 0.60, "meta": "26% · ↑ 4%"  },
      { "name": "Asia Pacific",  "amount": "$790K",  "share": 0.43, "meta": "19% · ↓ 7%"  },
      { "name": "Latin America", "amount": "$340K",  "share": 0.18, "meta": "8% · ↑ 2%"   }
    ]
  }
}
```

---

## `compare`

**When to use:** Structured numeric comparison — QoQ, YoY, plan vs. actual, before vs. after. Renders one or two side-by-side panels, each with a header and metric rows showing current value, prior value, and delta. Use when the comparison table IS the story, not just a supporting detail.

If `panels` has one entry it renders full-width. If two, it renders side by side.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `panels` | array | yes | 1–2 panel objects |

Each panel:

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | yes | Panel header, e.g. `"Quarter over quarter"` |
| `rows` | array | yes | 2–8 comparison rows |

Each row:

| Field | Type | Required | Description |
|---|---|---|---|
| `metric` | string | yes | Metric name, shown muted |
| `a` | string | yes | Current period value |
| `b` | string | yes | Prior period value, shown muted |
| `delta` | string | yes | Change, e.g. `"+8%"`, `"−4"`, `"+3 pt"` |
| `dir` | string | yes | `"up"` or `"down"` — drives color |

**HTML pattern:**
```html
<section class="compare">
  <div class="cmp-block">
    <h3>Quarter over quarter</h3>
    <div class="cmp-rows">
      <div class="cmp-row">
        <span class="ck">Total revenue</span>
        <span class="ca">$4.2M</span>
        <span class="cb">$3.9M</span>
        <span class="cd up">+8%</span>
      </div>
      <div class="cmp-row">
        <span class="ck">Deals closed</span>
        <span class="ca">47</span>
        <span class="cb">42</span>
        <span class="cd up">+5</span>
      </div>
    </div>
  </div>
  <div class="cmp-block">
    <h3>Year over year</h3>
    <div class="cmp-rows">
      <!-- same row structure -->
    </div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "compare",
  "props": {
    "panels": [
      {
        "label": "Quarter over quarter",
        "rows": [
          { "metric": "Total revenue", "a": "$4.2M", "b": "$3.9M", "delta": "+8%",  "dir": "up"   },
          { "metric": "Deals closed",  "a": "47",    "b": "42",    "delta": "+5",   "dir": "up"   },
          { "metric": "Avg deal size", "a": "$89K",  "b": "$93K",  "delta": "−4%",  "dir": "down" },
          { "metric": "Win rate",      "a": "34%",   "b": "31%",   "delta": "+3 pt","dir": "up"   }
        ]
      },
      {
        "label": "Year over year",
        "rows": [
          { "metric": "Total revenue", "a": "$4.2M", "b": "$3.1M", "delta": "+35%", "dir": "up" },
          { "metric": "Deals closed",  "a": "47",    "b": "33",    "delta": "+14",  "dir": "up" },
          { "metric": "Avg deal size", "a": "$89K",  "b": "$94K",  "delta": "−5%",  "dir": "down" }
        ]
      }
    ]
  }
}
```

---

## `table`

**When to use:** Detailed row data — deal pipeline, open projects, vendor spend, candidates. Use when the reader needs to scan individual rows, not just totals. Maximum 15 rows; filter to most important items. One per report.

Cell values may be plain text or a badge. Render a badge as `<span class="tbl-badge tbl-badge--{color}">{text}</span>`. Colors: `green`, `amber`, `red`, `gray`, `blue` — see design-system.md.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Card heading |
| `sub` | string | no | Subtitle |
| `headers` | array of strings | yes | Column labels |
| `rows` | array of arrays | yes | Each inner array is one row; cell count must match headers |

To render a badge cell, use the string `"badge:color:text"`, e.g. `"badge:green:On Track"`.

**HTML pattern:**
```html
<section class="card">
  <h2>Open pipeline</h2>
  <div class="sub">Deals above $200K in late stage</div>
  <div class="data-table-wrap">
    <table class="data-table">
      <thead>
        <tr><th>Account</th><th>Stage</th><th>Value</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>Helix Financial</td>
          <td>Proposal</td>
          <td>$480K</td>
          <td><span class="tbl-badge tbl-badge--green">On Track</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "table",
  "props": {
    "title": "Open pipeline",
    "sub": "Deals above $200K currently in late stage",
    "headers": ["Account", "Owner", "Stage", "Value", "Close date", "Status"],
    "rows": [
      ["Helix Financial",   "Sam Lee",  "Proposal",    "$480K", "Jul 12", "badge:green:On Track"],
      ["Nova Logistics",    "Kai Osei", "Final round", "$310K", "Jul 5",  "badge:amber:At Risk"],
      ["Cedarwood Health",  "Mira Tan", "Negotiation", "$290K", "Jul 20", "badge:green:On Track"]
    ]
  }
}
```

---

## `status-grid`

**When to use:** Health status of multiple workstreams, projects, or milestones — when each item has a clear signal (on track / at risk / blocked / complete). Renders as a clean list inside a card. Use 3–10 items.

Status values: `green`, `amber`, `red`, `gray`, `blue`.

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Card heading |
| `sub` | string | no | Subtitle |
| `items` | array | yes | 3–10 status objects |

Each item:

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Item label |
| `status` | string | yes | `green`, `amber`, `red`, `gray`, or `blue` |
| `value` | string | no | Right-aligned text, e.g. `"On track"`, `"Jul 15"`, `"Blocked"` |

**HTML pattern:**
```html
<section class="card">
  <h2>Go-to-market workstreams</h2>
  <div class="sub">End-of-quarter health by initiative</div>
  <div class="status-list">
    <div class="status-row">
      <span class="status-dot status-dot--green"></span>
      <span class="status-name">Enterprise expansion playbook</span>
      <span class="status-val">Complete</span>
    </div>
    <div class="status-row">
      <span class="status-dot status-dot--amber"></span>
      <span class="status-name">APAC territory rebuild</span>
      <span class="status-val">At risk · Q3</span>
    </div>
    <div class="status-row">
      <span class="status-dot status-dot--red"></span>
      <span class="status-name">ERP vendor selection</span>
      <span class="status-val">Blocked</span>
    </div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "status-grid",
  "props": {
    "title": "Go-to-market workstreams",
    "sub": "End-of-quarter health by initiative",
    "items": [
      { "name": "Enterprise expansion playbook", "status": "green", "value": "Complete"        },
      { "name": "Partner channel enablement",    "status": "green", "value": "On track"        },
      { "name": "APAC territory rebuild",        "status": "amber", "value": "At risk · Q3"   },
      { "name": "ERP vendor selection",          "status": "red",   "value": "Blocked"         },
      { "name": "FY27 quota planning",           "status": "blue",  "value": "In review"       }
    ]
  }
}
```

---

## `highlights`

**When to use:** 3–5 narrative insight cards — bright spots, risks, actions needed, forward look. The editorial counterpart to the data sections. Always place last (or after `status-grid`). Each card has a small all-caps tag and a prose body of 2–4 sentences.

Tags should be concrete and action-oriented: "Bright spot", "Risk", "Action needed", "Watch closely", "Next quarter", "Decision required".

**Props:**

| Field | Type | Required | Description |
|---|---|---|---|
| `items` | array | yes | 3–5 highlight objects |

Each item:

| Field | Type | Required | Description |
|---|---|---|---|
| `tag` | string | yes | Short all-caps label, e.g. `"Risk"`, `"Bright spot"` |
| `body` | string | yes | 2–4 sentence prose. Plain text — no HTML tags. |

**HTML pattern:**
```html
<section class="highlights">
  <div class="highlight">
    <div class="hl-tag">Bright spot</div>
    <div class="hl-body">Enterprise ACV reached an all-time high of $142K, driven by two seven-figure expansions in June.</div>
  </div>
  <div class="highlight">
    <div class="hl-tag">Risk</div>
    <div class="hl-body">APAC missed Q2 by $60K. Three pipeline deals slipped to Q3 due to procurement delays.</div>
  </div>
  <div class="highlight">
    <div class="hl-tag">Action needed</div>
    <div class="hl-body">ERP vendor decision stalled — pricing hold expires June 15. Finance and Ops leads must decide by end of week.</div>
  </div>
</section>
```

**Example JSON block:**
```json
{
  "type": "highlights",
  "props": {
    "items": [
      {
        "tag": "Bright spot",
        "body": "Enterprise ACV reached an all-time high of $142K, driven by two seven-figure expansions in June. The cohort renewing at >120% NRR grew to nine accounts."
      },
      {
        "tag": "Risk",
        "body": "APAC missed Q2 by $60K. Three pipeline deals slipped to Q3 due to procurement delays. Regional leadership meeting scheduled June 10."
      },
      {
        "tag": "Action needed",
        "body": "ERP vendor pricing hold expires June 15. Finance and Ops leads need to decide by end of week to avoid a 12-week delay to go-live."
      },
      {
        "tag": "Next quarter",
        "body": "Q3 pipeline stands at $6.1M (1.5× coverage). Focus areas: close Nova Logistics, activate two new partner channels, complete APAC re-segmentation."
      }
    ]
  }
}
```

---

## Component Limits Summary

| Component | Min | Max items | Max per report |
|---|---|---|---|
| `hero` | — | — | 1 |
| `kpi-row` | 2 items | 4 items | 1 |
| `trend` | 3 data points | 12 data points | 1 |
| `bar-list` | 3 items | 10 items | unlimited |
| `compare` | 1 panel, 2 rows | 2 panels, 8 rows each | unlimited |
| `table` | 1 row | 15 rows | 1 |
| `status-grid` | 3 items | 10 items | unlimited |
| `highlights` | 3 items | 5 items | 1 |
