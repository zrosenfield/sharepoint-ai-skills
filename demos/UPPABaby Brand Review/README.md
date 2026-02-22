# UPPAbaby Brand Compliance Review

This demo shows how to use a custom AI skill to audit marketing content against a brand's guidelines — automatically scoring files across voice, visual identity, messaging, photography, and consistency, then producing a prioritized remediation plan.

The scenario: a brand manager uploads marketing assets to SharePoint and asks the Copilot agent to run a compliance review. The agent scores each file, flags issues by severity, and gives specific, actionable fixes — not vague advice.

---

## Watch the Demo

[![UPPAbaby Brand Compliance Review](https://img.youtube.com/vi/uij1sLuL6NM/0.jpg)](https://youtu.be/uij1sLuL6NM)

---

## What This Demo Shows

- Upload a mix of marketing assets (PowerPoint decks, Word documents, creative briefs) to SharePoint
- Trigger the brand review skill against each file
- AI reads the brand definition reference and evaluates the content against five weighted categories
- AI produces a full scorecard with a compliance rating
- Issues are surfaced as Critical, Major, or Minor with exact remediation steps
- Works across file types: PPTX, DOCX, images, PDFs, and plain text

---

## Demo Files

These files are included in this folder and used during the demo:

| File | Type | Used As |
|------|------|---------|
| `cruz-v3-launch.pptx` | PowerPoint | Launch deck to review for brand compliance |
| `retailer-training-q4.pptx` | PowerPoint | Retailer-facing training deck to review |
| `social-media-content-brief.docx` | Word | Social content brief to review |
| `spring-2026-creative-brief.docx` | Word | Creative brief to review |
| `uppababy-brand-guidelines-ai-extracted.md` | Reference | Brand definition uploaded to SharePoint as the skill's reference document |
| `brand-review.md` | Skill | The brand compliance review skill — upload this to the site's Skills library |

---

## How the Skill Works

The `brand-review.md` skill instructs the agent to:

1. Read the brand definition reference document before doing anything else
2. Identify the file type and infer the intended channel (social, retail, web, internal, etc.)
3. Score the content across five weighted categories:

| Category | Weight |
|----------|--------|
| Voice & Tone | 25% |
| Visual Identity | 25% |
| Messaging Alignment | 20% |
| Photography & Imagery | 15% |
| Brand Consistency | 15% |

4. Calculate an overall weighted score
5. Assign a compliance rating: Exemplary / Compliant / Partially Compliant / Needs Significant Work / Non-Compliant
6. List all issues by severity (🔴 Critical / 🟡 Major / 🟢 Minor) with specific, concrete remediation steps

---

## SharePoint Setup

Before running the demo, the SharePoint site needs:

1. **Brand definition reference** — upload `uppababy-brand-guidelines-ai-extracted.md` to the site's document library at the path `references/brand-definition.md` (or adjust the path in the skill to match where you place it)
2. **Brand review skill** — upload `brand-review.md` to the site's **Agent Assets > Skills** library

---

## Skills Used

| Skill | Description |
|-------|-------------|
| `brand-review.md` (included) | Drives the full brand compliance review — reads the brand definition, evaluates the content, produces the scorecard and remediation plan |

---

## Prerequisites

- Microsoft 365 tenant with Copilot licenses
- SharePoint site with agent enabled
- Brand definition reference uploaded to the site (see Setup above)
- `brand-review.md` uploaded to the site's Skills library
