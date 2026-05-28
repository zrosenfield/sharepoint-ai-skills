# Component Catalog

All HTML patterns for the `dossier` skill. CSS class names and token names match `assets/dossier-template.html` and `references/design-system.md` exactly.

---

## Rendering Modes

The dossier supports two layouts. Both share the same CSS custom properties (palette tokens) and component primitives.

### Grid Mode (2–8 subjects)

Wraps all subject cards in a `.dossier-grid` container. Cards are rendered side by side, two per row on desktop, one on mobile. All cards in a row share the same height via CSS grid.

### One-Pager Mode (1 subject)

Renders a full-width briefing document. Uses a hero block, two-column key-facts + tags section, full summary, and an activity timeline.

---

## Page Header

Used in both modes. Renders as a thin strip with the report title on the left and an optional subtitle on the right.

```html
<div class="rpt-header">
  <div class="rpt-title">Competitor Landscape — Q2 2026</div>
  <div class="rpt-subtitle">4 companies · Project management SaaS</div>
</div>
```

If no subtitle, omit the `.rpt-subtitle` element entirely.

---

## Grid Mode: Card Shell

The `.dossier-grid` wrapper uses `display: grid` with `repeat(auto-fit, minmax(400px, 1fr))`. Each `.dossier-card` is a self-contained surface.

```html
<div class="dossier-grid">
  <!-- one .dossier-card per subject -->
</div>
```

---

## Grid Mode: Full Card

Each card contains a header, key facts, tags, summary, and activity. Render all sections for every card.

```html
<article class="dossier-card" id="acme-corp">

  <!-- Card header -->
  <div class="card-header">
    <div class="card-header-main">
      <h2 class="card-name">Acme Corp</h2>
      <span class="card-type-pill">Competitor</span>
    </div>
    <span class="status-dot status-dot--green" title="Active"></span>
  </div>

  <!-- Key facts -->
  <dl class="key-facts">
    <div class="kf-row">
      <dt class="kf-label">HQ</dt>
      <dd class="kf-value">Austin, TX</dd>
    </div>
    <div class="kf-row">
      <dt class="kf-label">Founded</dt>
      <dd class="kf-value">2019</dd>
    </div>
    <div class="kf-row">
      <dt class="kf-label">ARR</dt>
      <dd class="kf-value">~$40M est.</dd>
    </div>
    <div class="kf-row">
      <dt class="kf-label">Stage</dt>
      <dd class="kf-value">Series B</dd>
    </div>
  </dl>

  <!-- Tags -->
  <div class="tags">
    <span class="tag">CRM</span>
    <span class="tag">Series B</span>
    <span class="tag">APAC</span>
  </div>

  <!-- Summary -->
  <p class="card-summary">
    Acme Corp is a workflow automation platform targeting mid-market operations teams.
    Founded in 2019, the company grew 60% YoY to reach an estimated $40M ARR by Q1 2026.
    Their differentiation is a no-code rules engine that competes directly with our Workflow
    Studio feature.
  </p>

  <!-- Activity -->
  <ul class="card-activity">
    <li class="activity-item">
      <span class="activity-date">Apr 2026</span>
      <span class="activity-text">Raised $28M Series B led by Lightspeed Ventures.</span>
    </li>
    <li class="activity-item">
      <span class="activity-date">Feb 2026</span>
      <span class="activity-text">Launched Acme Flows, a visual automation builder targeting operations teams.</span>
    </li>
  </ul>

</article>
```

**Card header notes:**
- `.card-name` renders at ~20px semibold. Keep the name short enough to fit on one line.
- `.card-type-pill` is the category label. Rendered in muted background + ink text. One pill per card.
- `.status-dot` is optional. Use `status-dot--green`, `--amber`, `--red`, `--gray`, or `--blue`. Include a `title` attribute with the status text for accessibility. If no status, omit the dot entirely.

**Key facts notes:**
- Use `<dl>` / `<dt>` / `<dd>` semantics. Each `.kf-row` holds one `<dt>` + `<dd>` pair.
- Labels (`<dt>`) are 11px, uppercase, `--ink-muted`. Values (`<dd>`) are 14px, `--ink`.
- Render 2–6 rows. No sentences in values.

**Tags notes:**
- Each `.tag` is a small pill: `--accent-soft` background, `--accent` text.
- Render 1–6 tags. If a tag is a status word (e.g., "Active"), prefer the status dot instead.

**Activity notes:**
- Use `<ul>` with `<li class="activity-item">`. Each item: date span + text span.
- Most recent first. 0–5 items. If empty, omit the `<ul>` entirely.
- `.activity-date` uses `--font-mono`, `--ink-muted`, 11px.

---

## One-Pager Mode: Full Layout

For a single subject, renders as a full-width briefing document with four sections.

### 1. One-Pager Hero Block

Uses the same thin `.rpt-header` strip as the page header, followed by a subject-level header. Not a dark banner.

```html
<div class="op-hero">
  <div class="op-hero-meta">
    <span class="card-type-pill">Competitor</span>
    <span class="status-dot status-dot--amber" title="Watch"></span>
  </div>
  <h1 class="op-name">Acme Corp</h1>
  <p class="op-tagline">Workflow automation platform · Austin, TX · Series B</p>
</div>
```

`.op-tagline` is a single descriptive line — compose it from the most important 2–3 key facts. This lets the reader grasp the subject at a glance before diving into the structured sections.

### 2. Two-Column Section (Key Facts + Tags/Quick Take)

```html
<div class="op-two-col">

  <!-- Left: Key facts card -->
  <section class="card op-facts-card">
    <h2>Key Facts</h2>
    <dl class="key-facts">
      <div class="kf-row">
        <dt class="kf-label">HQ</dt>
        <dd class="kf-value">Austin, TX</dd>
      </div>
      <div class="kf-row">
        <dt class="kf-label">Founded</dt>
        <dd class="kf-value">2019</dd>
      </div>
      <div class="kf-row">
        <dt class="kf-label">ARR</dt>
        <dd class="kf-value">~$40M est.</dd>
      </div>
      <div class="kf-row">
        <dt class="kf-label">Stage</dt>
        <dd class="kf-value">Series B</dd>
      </div>
      <div class="kf-row">
        <dt class="kf-label">Employees</dt>
        <dd class="kf-value">~180</dd>
      </div>
    </dl>
  </section>

  <!-- Right: Tags + Quick Take -->
  <div class="op-right-col">
    <section class="card op-tags-card">
      <h2>Tags</h2>
      <div class="tags">
        <span class="tag">CRM</span>
        <span class="tag">Series B</span>
        <span class="tag">No-code</span>
        <span class="tag">Mid-market</span>
      </div>
    </section>
    <section class="card op-quicktake-card">
      <h2>Quick Take</h2>
      <p class="op-quicktake-text">
        Most credible no-code workflow competitor in the mid-market — watch their Flows product closely heading into H2 2026.
      </p>
    </section>
  </div>

</div>
```

### 3. Summary Section

```html
<section class="card op-summary-card">
  <h2>Overview</h2>
  <p class="op-summary">
    Acme Corp is a workflow automation platform targeting mid-market operations teams.
    Founded in 2019, the company grew 60% YoY to reach an estimated $40M ARR by Q1 2026,
    making it one of the fastest-growing players in the no-code automation space.
    Their core product, Acme Flows, competes directly with our Workflow Studio on visual
    rule-building, but lacks enterprise SSO and audit logging — gaps they are reportedly
    closing in a Q3 2026 release. The recent Series B positions them to accelerate both
    product development and go-to-market in APAC.
  </p>
</section>
```

### 4. Activity Timeline

The timeline is purely CSS — a left border line created with `::before` on `.activity-list`, and accent-colored dots with `::before` on each `.activity-item`. No JavaScript required.

```html
<section class="card op-timeline-card">
  <h2>Recent Activity</h2>
  <ol class="activity-list">
    <li class="activity-item">
      <div class="activity-date">Apr 2026</div>
      <div class="activity-text">Raised $28M Series B led by Lightspeed Ventures, bringing total funding to $44M.</div>
    </li>
    <li class="activity-item">
      <div class="activity-date">Feb 2026</div>
      <div class="activity-text">Launched Acme Flows, a visual automation builder targeting operations teams.</div>
    </li>
    <li class="activity-item">
      <div class="activity-date">Jan 2026</div>
      <div class="activity-text">Hired former Salesforce VP of Product as Chief Product Officer.</div>
    </li>
    <li class="activity-item">
      <div class="activity-date">Nov 2025</div>
      <div class="activity-text">Announced partnership with Workday for HR workflow integrations.</div>
    </li>
  </ol>
</section>
```

**Timeline CSS mechanics** (defined in the template — do not inline):

The connecting line is drawn by `.activity-list::before` as a 2px vertical border on the left side. Each `.activity-item::before` renders a 10px circle (accent color, white border) positioned to sit on the line. The `.activity-date` sits above the `.activity-text` in a flex column layout. No JavaScript — the timeline is fully correct without JS.

---

## Page Footer

```html
<div class="rpt-footer">
  <div>Prepared May 28, 2026 · Confidential</div>
</div>
```

If no footer text, render the element with both sides empty.

---

## Component Limits Summary

| Element | Min | Max |
|---|---|---|
| Subjects (grid mode) | 2 | 8 |
| Subjects (one-pager mode) | 1 | 1 |
| `key_facts` per subject | 2 | 6 |
| `tags` per subject | 1 | 6 |
| `activity` items per subject | 0 | 5 |
| Summary length | 2 sentences | 5 sentences |
