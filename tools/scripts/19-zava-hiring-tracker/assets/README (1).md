# Hiring Pipeline Status Report — SharePoint AI Demo

**Demo company:** Zava Industries
**Demo goal:** Show how a SharePoint AI skill can read structured list data and generate a polished HTML report with a Sankey diagram, key metrics, and risk callouts — no code, no BI tool, just a plain-English prompt.

---

## What This Demo Shows

1. Two simple SharePoint lists (Open Roles + Candidates) with realistic hiring data
2. A SharePoint AI skill ("Hiring Pipeline Report") that reads both lists
3. The skill generates a single HTML file output with:
   - Executive summary metrics (open roles, active candidates, avg days in stage, offer rate)
   - A Sankey diagram showing candidate flow across pipeline stages
   - Risk callouts (candidates stuck too long, roles with no candidates, bottleneck stages)
   - Zava Industries corporate branding
4. **Bonus final step:** Take that HTML report and generate a slide from it

## Setup Instructions

### List 1: Open Roles

Create a SharePoint list called **Open Roles** with these columns:

| Column Name     | Type                 |
|-----------------|----------------------|
| Title           | Single line of text   | *(this is the role title)*
| Department      | Choice: Engineering, Marketing, Sales, Operations, Finance, People |
| Hiring Manager  | Single line of text   |
| Priority        | Choice: Critical, High, Normal |
| Target Start    | Date                 |
| Status          | Choice: Open, On Hold, Filled |

Import the sample data from `open-roles.csv`.

### List 2: Candidates

Create a SharePoint list called **Candidates** with these columns:

| Column Name     | Type                 |
|-----------------|----------------------|
| Title           | Single line of text   | *(this is the candidate name)*
| Role            | Single line of text   | *(matches a Title from Open Roles)*
| Current Stage   | Choice: Applied, Phone Screen, Interview, Final Round, Offer, Hired, Rejected, Withdrawn |
| Days in Stage   | Number               |
| Source          | Choice: LinkedIn, Referral, Careers Page, Recruiter, Job Board |
| Recruiter       | Single line of text   |
| Applied Date    | Date                 |
| Notes           | Multiple lines of text |

Import the sample data from `candidates.csv`.

### The Skill: Hiring Pipeline Report

Create a SharePoint AI skill called **Hiring Pipeline Report**.

**Instructions for the skill:**

> See `skill-prompt.md` for the full skill prompt text to paste into the skill instructions.

**Skill configuration:**
- Add both the **Open Roles** list and the **Candidates** list as data sources for the skill.
- The skill output is a single file (HTML).

---

## Demo Flow

### Step 1 — Show the Lists
Open both lists in SharePoint. Scroll through them casually. Point out that this is just normal structured data — nothing fancy, no custom columns, no Power Automate, no dashboards built yet.

### Step 2 — Run the Skill
In Copilot or the skill UI, say:

> **"Give me a status report on our hiring pipeline"**

The skill reads both lists, analyzes the data, and generates an HTML report file.

### Step 3 — Open the Report
Open the generated HTML file. Walk through:
- **Top metrics bar** — open roles, active candidates, avg days in pipeline, offer rate
- **Sankey diagram** — candidate flow from Applied through each stage to Hired/Rejected/Withdrawn
- **Risk callouts** — candidates stuck 10+ days, roles with zero candidates, stages with high drop-off

### Step 4 — The "So What" Moment
Point out: "This is code generation. The AI wrote JavaScript to build this Sankey diagram from your list data. No Power BI. No developer. No template. It read your data, decided what to visualize, and generated the code."

### Step 5 (Bonus) — Generate a Slide
Take the HTML report and ask:

> **"Turn this report into a single executive summary slide"**

This shows the compose-and-reuse loop — AI output becomes AI input.

---

## Demo Tips

- The sample data is designed with intentional bottlenecks and risks so the report has interesting callouts (several candidates stuck in Interview for 12+ days, one Critical role with no candidates, etc.)
- If you want a cleaner Sankey, reduce the candidate count. If you want messier/more realistic, add more rows with varied paths.
- The skill prompt includes Zava branding (colors, logo text, fonts). Swap these for any company's brand to show customization.
