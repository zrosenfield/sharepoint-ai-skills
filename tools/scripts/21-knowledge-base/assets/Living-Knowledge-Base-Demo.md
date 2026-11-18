# Living Knowledge Base — SharePoint AI Demo

A self-healing knowledge system that captures not just what your organization knows, but why it knows it — the decisions, tradeoffs, failures, and reasoning that live in people's heads.

Users interact with one surface: the chat panel on the home page. They ask questions, share what they know, or drop files. The AI extracts tacit knowledge and builds a living knowledge base that gets smarter every cycle.

---

## Site Structure

### Lists

**Knowledge Gaps**

| Column | Type |
|---|---|
| Question | Single line of text |
| Topic | Single line of text |
| Asked By | Single line of text |
| Status | Choice: Open, Assigned, Resolved, Verify |
| Assigned Expert | Single line of text |
| Resolved Date | Single line of text |
| KB File | Single line of text |
| Source Type | Choice: Gap, Transcript, Email, Document, Slack, Typed, Verification |

**Expert Directory**

| Column | Type |
|---|---|
| Name | Single line of text |
| Expertise Areas | Single line of text |
| Notes | Single line of text |

### Libraries

**Knowledge Base** — Document library. Markdown files organized by topic. The AI's brain.

**Submissions** — Document library. Drop zone for transcripts, emails, documents, and anything else to be processed into knowledge.

---

## Knowledge Base File Format

Each markdown file in the Knowledge Base library follows this structure. The key difference from a typical wiki: every entry captures not just the fact but the reasoning and history behind it.

```markdown
# [Topic Name]

## [Subtopic]

### Current State
[What is true today. The policy, process, number, or decision in effect.]

### Rationale
[Why it's this way. The reasoning, tradeoffs, constraints, or goals that led to this decision.]

### History
[What came before. Previous approaches, what failed, what changed and when. Include the trigger for change if known.]

### Nuance
[Edge cases, exceptions, gotchas, tribal knowledge. The stuff someone would only know from experience.]

**Source:** [who provided this, when, from what — typed / transcript / email / document]
**Added:** [date]
**Last Verified:** [date — initially same as Added, updated when someone confirms the entry is still accurate]
```

Not every entry needs all four sections. A simple fact might just have Current State and Source. But the Ingest skill should always listen for rationale and history and capture them when present.

The **Last Verified** date is critical to knowledge decay detection. When the AI answers a question using a KB entry whose Last Verified date is older than 90 days, it still answers but also flags the entry for re-verification by creating a Knowledge Gaps item with Status "Verify."

---

## Skills

### Skill 1: Log Knowledge Gap

**Name:** Log Knowledge Gap

**Instructions:**

When you cannot answer a question from the Knowledge Base library:

1. Create an item in the Knowledge Gaps list. Set Question to the user's question, Topic to your best guess at the subject area (match existing KB file names when possible), Asked By to the user's name (ask if you don't know it), and Status to Open.
2. Check the Expert Directory list for anyone whose Expertise Areas match the topic. If found, update Assigned Expert and set Status to Assigned.
3. Tell the user you've logged the gap and who it's been routed to (or that it's unassigned if no expert matched).

---

### Skill 2: Ingest Knowledge

**Name:** Ingest Knowledge

**Instructions:**

When someone shares knowledge — typed, pasted, or by uploading a file to the Submissions library — extract tacit knowledge and add it to the Knowledge Base.

**What to extract:**

Listen for more than facts. Actively look for:
- Decisions and their reasoning ("we went with X because...")
- Tradeoffs acknowledged ("the downside is..." / "we accepted that risk because...")
- Failed approaches ("we tried X and it didn't work because...")
- Changes over time ("we used to do X, then switched to Y when...")
- Edge cases and exceptions ("that works except when..." / "watch out for...")
- Unwritten rules ("technically the policy says X but in practice we...")
- Lessons learned ("if I had to do it again..." / "the thing nobody tells you is...")

**How to structure it:**

1. Check the Knowledge Base library for an existing file on this topic.
2. If a file exists, read it. Add new knowledge under the right heading. If the new information updates, contradicts, or adds context to existing content, note the change — don't silently overwrite. Add a new subsection or append under the existing one.
3. If no file exists, create a new markdown file named with a short slug (e.g., vendor-contracts.md).
4. For each piece of knowledge, use the sections that apply:
   - **Current State** — what's true now
   - **Rationale** — why it's this way
   - **History** — what came before or changed
   - **Nuance** — edge cases, exceptions, gotchas
5. Always include the Source line (who, when, what format), Added date, and Last Verified date (set to today).
6. After ingesting, check the Knowledge Gaps list for Open or Assigned items this knowledge answers. Update matching items: set Status to Resolved, Resolved Date to today, KB File to the filename, and Source Type to match the input format (Transcript, Email, Document, Slack, or Typed).
7. If the new knowledge updates an existing KB entry, also update that entry's Last Verified date to today.

**Important:** When processing transcripts or meeting notes, preserve the conversational context that reveals reasoning. "Dana said we switched to CrowdStrike after the Meridian incident" is more valuable than "Pen testing vendor: CrowdStrike."

---

### Skill 3: Find Expert

**Name:** Find Expert

**Instructions:**

When asked to find experts or review open gaps:

1. Read the Knowledge Gaps list for items with Status Open.
2. Read the Expert Directory list.
3. Match open gaps to experts by comparing the gap's Topic to each expert's Expertise Areas.
4. For each match, update the gap: set Assigned Expert and Status to Assigned.
5. Report what you matched and what remains unmatched.

---

### Skill 4: KB Admin Report

**Name:** KB Admin Report

**Instructions:**

When an admin asks for a knowledge base report, status update, or health check, generate a comprehensive report covering the following areas. Read all files in the Knowledge Base library, all items in the Knowledge Gaps list, and all items in the Expert Directory list.

**1. Corpus Overview**

- Total number of KB files and list of topic names
- For each file: count of sections, count of distinct sources cited, and the date range of entries (oldest Added date to newest Added date)
- Total knowledge entries across all files

**2. Decay Report**

- List every KB entry where Last Verified is older than 90 days
- Group stale entries by topic file
- For each stale entry: show the subtopic name, Last Verified date, days since verification, and the original source person
- Count: total entries, verified within 90 days, stale (90+ days), critical (180+ days)
- Highlight any topic files where more than half of entries are stale

**3. Gap Status**

- Count of Knowledge Gaps by Status (Open, Assigned, Resolved, Verify)
- List all Open and Assigned gaps with their Topic, Asked By, and date
- List all Verify items (decay-triggered re-verification requests)
- Average time from Open to Resolved for completed gaps (if dates allow)
- Topics with the most open gaps — these are the weakest coverage areas

**4. Ingestion Activity**

- Count of resolved gaps by Source Type (Transcript, Email, Document, Slack, Typed, Verification)
- This shows how knowledge is entering the system — are people typing it in, or is it coming from meeting transcripts, emails, etc.
- Identify which source types are most and least used

**5. Expert Coverage**

- List all experts and their expertise areas
- Cross-reference against open gap topics: which gap topics have a matching expert? Which don't?
- Identify expertise areas with no KB file yet (expert registered but no knowledge captured)
- Identify KB topics with no matching expert (knowledge exists but no one owns it)

**6. Recommendations**

Based on the data above, provide 3-5 specific next actions. Prioritize:
- Stale entries that need re-verification (especially in frequently-asked topics)
- Open gaps that have been unassigned the longest
- Topic areas with no expert coverage
- Source type gaps (e.g., if no transcripts have been processed, suggest recording and submitting meeting notes)

---

## Context File

Create `site-context.md` in Site Assets:

```markdown
# Site Context — Living Knowledge Base

You are the knowledge assistant for this team. Your job is to help people find answers and to capture the reasoning behind what this organization knows — not just facts but how decisions were made, what was tried before, and what the edge cases are.

## How You Work

Your knowledge lives in markdown files in the Knowledge Base library. When someone asks a question, check there first. When you answer, include the reasoning and context from the KB, not just the bottom line. If the KB has history on why something is the way it is, share that too.

If you cannot answer, use the Log Knowledge Gap skill to record the question and route it to an expert.

When someone shares knowledge — typed, pasted, or uploaded — use the Ingest Knowledge skill. Extract not just facts but decisions, tradeoffs, failed approaches, and lessons learned. Preserve the human reasoning.

When an admin asks for a report, status, or health check, use the KB Admin Report skill.

## Knowledge Decay Detection

When you answer a question using a KB entry, check that entry's Last Verified date. If it is older than 90 days:

1. Still answer the question — the knowledge is likely still correct.
2. Flag the age to the user: "Note: this information was last verified on [date]. It may be worth confirming it's still current."
3. Create an item in the Knowledge Gaps list with Status "Verify," the topic, and the original source person as Assigned Expert. Set Source Type to Verification.

This ensures the KB doesn't just grow — it stays trustworthy. Entries that get re-confirmed get a fresh Last Verified date. Entries that have changed get updated through the normal ingestion process.

## Rules

- Always check the Knowledge Base before saying you don't know.
- When answering, cite the source so people know where information came from.
- When logging gaps, always check Expert Directory for a routing match.
- When ingesting, always check Knowledge Gaps for items to resolve.
- When ingesting, always set Source Type on resolved gap items (Transcript, Email, Document, Slack, Typed).
- Never silently overwrite existing KB content. Add to it, note changes, preserve history.
- One topic per file. If knowledge spans topics, update both files.
- When answering from stale entries (Last Verified > 90 days), flag the age and create a Verify gap item.
```

---

## Sample Data

### Expert Directory

| Name | Expertise Areas | Notes |
|---|---|---|
| Jordan Lee | vendor contracts, procurement, compliance | 10 years in procurement, built the current vendor assessment framework |
| Priya Sharma | product pricing, licensing, SKU management | Owns the pricing model, led the 2024 pricing restructure |
| Marcus Chen | customer onboarding, implementation, training | Runs all enterprise implementations, designed the 90-day framework |
| Dana Torres | IT infrastructure, networking, security policies | Built the current security architecture, led FedRAMP authorization |
| Alex Rivera | HR policies, benefits, hiring process | HR business partner for engineering, rewrote the interview process in 2024 |

### Knowledge Gaps — Seed Items

| Question | Topic | Asked By | Status | Assigned Expert | Source Type |
|---|---|---|---|---|---|
| What's the SLA for vendor contract renewals? | vendor contracts | Sam K | Open | | Gap |
| How do we handle pricing for multi-year deals over 3 years? | product pricing | Jamie L | Open | | Gap |
| What security certifications do we currently hold? | security policies | Robin M | Open | | Gap |
| What's the onboarding timeline for enterprise customers? | customer onboarding | Taylor P | Assigned | Marcus Chen | Gap |
| Why did we switch from the old interview rubric? | hiring process | Casey N | Open | | Gap |
| What's the policy on vendor contract termination penalties? | vendor contracts | Morgan F | Open | | Gap |
| Verify: Vendor contract renewal process — last verified 2024-08-20 | vendor contracts | System | Verify | Jordan Lee | Verification |
| Verify: Product pricing tier structure — last verified 2024-11-15 | product pricing | System | Verify | Priya Sharma | Verification |

---

## Seed Knowledge Base Files

### customer-onboarding.md

```markdown
# Customer Onboarding

## Enterprise Onboarding Framework

### Current State
Enterprise customers follow a 90-day onboarding in three phases. Phase 1 (Days 1-30): environment setup and data migration. Phase 2 (Days 31-60): configuration and integration. Phase 3 (Days 61-90): training and go-live support. Each customer gets a dedicated implementation lead who owns the project plan and a technical account manager who handles escalations.

### Rationale
The 90-day structure was adopted in Q2 2024 after analyzing completion rates. Customers who onboarded in under 60 days had a 40% higher churn rate at 12 months — they weren't properly configured and hit issues post-launch that eroded trust. The three-phase model forces proper sequencing so configuration is validated before training begins.

### History
Before 2024, onboarding was unstructured — implementation leads ran their own timelines, typically 30-45 days. Completion quality varied widely. The Greenfield Industries implementation in January 2024 was the breaking point: they went live in 28 days, had a critical data mapping error, and escalated to the CEO. That triggered the framework redesign.

### Nuance
The 90-day timeline is for enterprise. Mid-market customers use a compressed 45-day version with phases 1 and 2 combined. Starter tier is self-serve with documentation only. For enterprise customers with complex integrations (more than 3 source systems), Marcus typically extends Phase 2 by 2 weeks — this isn't officially in the framework but is standard practice.

**Source:** Marcus Chen, typed, initial KB seed
**Added:** 2025-01-10
**Last Verified:** 2025-01-10
```

### product-pricing.md

```markdown
# Product Pricing

## Tier Structure

### Current State
Three tiers: Starter ($15/user/month), Professional ($45/user/month), Enterprise ($85/user/month). Annual commitment discount of 15%. Volume discounts above 500 seats: 5% at 500, 10% at 1000, negotiable above 2000. Multi-year agreements (2-3 years) get an additional 10% on top of annual pricing. Terms beyond 3 years require VP approval.

### Rationale
The three-tier model replaced the old per-feature pricing in the 2024 restructure. Per-feature pricing created sales friction — every deal required a custom quote and customers felt nickeled. The tier model simplified the conversation: pick your tier, get everything in it. The 15% annual discount was calibrated to match the cost of monthly billing overhead plus a small incentive.

### History
Original pricing (2021-2023) was per-feature: base platform fee plus add-ons for advanced search, analytics, integrations, etc. Average deal had 4-6 line items. Sales cycle averaged 47 days. After the restructure, sales cycle dropped to 29 days and average deal size increased 22% because customers stopped self-selecting out of features they might need.

### Nuance
The $85 enterprise price is the list price. In practice, almost every enterprise deal lands between $65-75 after volume and multi-year discounts. The sales team knows this but marketing insists on the $85 anchor. Starter tier has no phone support — this is the most common upgrade trigger to Professional. The volume discount at 2000+ seats is intentionally vague in the rate card to force a conversation with the account team.

**Source:** Priya Sharma, typed, initial KB seed
**Added:** 2024-11-15
**Last Verified:** 2024-11-15
```

### vendor-contracts.md

```markdown
# Vendor Contracts

## Renewal Process

### Current State
Contracts are reviewed 90 days before expiration. Procurement initiates a renewal assessment: spend analysis, performance review, and market comparison. Approval: department head for under $100K, VP for $100K+.

### Rationale
The 90-day window was set after we lost leverage on the DataStream renewal in 2023 — we started the review 30 days out, had no time to run a competitive process, and renewed at a 12% increase. The 90-day buffer ensures enough time for a credible alternative evaluation.

### History
Before 2023, renewals were handled ad hoc — the contract owner noticed the date and initiated renewal, sometimes with only weeks to spare. The DataStream incident plus two other late renewals in the same quarter triggered the standardized process.

**Source:** Jordan Lee, typed, initial KB seed
**Added:** 2024-08-20
**Last Verified:** 2024-08-20
```

---

## Submission Corpus

These files go in the Submissions library. Each represents a realistic artifact that the AI should process into the Knowledge Base.

---

### submission-01-security-review-transcript.md

```
Meeting Transcript — Security Policy Review
Date: March 28, 2025
Attendees: Dana Torres, Robin Martinez, Sam Kim

Dana Torres: Alright, let's go through where we are on certifications. As of this month we hold SOC 2 Type II, ISO 27001, and we got our FedRAMP Moderate authorization in January. That was a big lift.

Robin Martinez: The FedRAMP one took what, eight months?

Dana Torres: About ten months end to end. Started the assessment in March last year. The 3PAO engagement alone was four months. But we're authorized now and that opens up the whole federal vertical.

Sam Kim: What about HIPAA?

Dana Torres: We're HIPAA compliant but there's no formal HIPAA certification body the way SOC 2 has one. We have a third-party audit confirming our BAA framework and technical controls meet HIPAA requirements. Last done September 2024.

Robin Martinez: Penetration testing cadence?

Dana Torres: External pen tests annually through CrowdStrike. Last one November 2024, clean report, no critical findings. We do internal vulnerability scanning weekly through Qualys. High or critical gets a 72-hour remediation SLA. Medium gets 30 days.

Robin Martinez: Why CrowdStrike specifically?

Dana Torres: We actually used Rapid7 before 2023. They were fine for standard pen testing but when we started the FedRAMP prep we needed a firm with FedRAMP assessment experience. CrowdStrike had done assessments for three companies in our space and knew the control mapping. We ran both in parallel for one cycle — Rapid7 found 12 issues, CrowdStrike found 19, including three that were specifically relevant to FedRAMP moderate controls. That settled it.

Sam Kim: Network segmentation — can we guarantee tenant isolation?

Dana Torres: Yes. Every customer environment runs in an isolated VPC. No shared compute, no shared storage at the data layer. Control plane is shared but all customer data paths are fully isolated. Architecture since the 2023 redesign.

Robin Martinez: What drove the redesign?

Dana Torres: The Meridian incident. October 2022. A configuration error in the shared environment allowed one tenant's background job to read another tenant's queue. No data was actually exposed — the job errored before processing — but the fact that it was possible was unacceptable. We spent Q1 2023 rebuilding with full VPC isolation. Cost us about $2M in infrastructure and delayed two product launches, but it was the right call. Haven't had a single isolation concern since.

Sam Kim: Data retention after contract termination?

Dana Torres: 30 days. Customer data retained for 30 days post-termination, they can request an export during that window. After 30 days, permanently deleted. Backups purged within 90 days. That's in the MSA template, section 8.3.

Sam Kim: Was it always 30 days?

Dana Torres: It was 90 days originally. We shortened it in 2024 after legal reviewed the liability exposure. Holding customer data longer than necessary after termination creates risk — if there's a breach during that window, we're still responsible. 30 days is enough for any reasonable export request and reduces our exposure window by two thirds.

Robin Martinez: I think that covers the main questions. Thanks Dana.
```

---

### submission-02-pricing-decision-email.md

```
From: Priya Sharma
To: Sales Leadership
Date: March 15, 2025
Subject: RE: Why we don't discount Starter tier

Wanted to put this in writing since it came up again in the deal review.

We do not discount the Starter tier. This is deliberate, not an oversight.

The Starter tier at $15/user/month is already priced below our cost to serve when you include support overhead. We break even at approximately $13/user/month and Starter customers generate the highest support ticket volume per user because they don't have access to the dedicated support channel that Professional gets.

The business case for Starter is conversion. 34% of Starter customers upgrade to Professional within 12 months. The Starter price is an acquisition cost, not a profit center.

If a prospect is pushing hard on Starter pricing, the right move is to show them the Professional tier value — dedicated support alone is worth the delta for any team over 20 users. If they truly can't afford Professional, Starter at list price is still the right answer. Discounting it makes the unit economics negative AND removes the upgrade incentive.

One exception: nonprofit organizations get 25% off any tier including Starter. That's a board-level commitment and it's handled through a separate approval workflow, not through standard deal desk discounting.

Priya

---

From: Priya Sharma
To: Sales Leadership  
Date: March 18, 2025
Subject: RE: RE: Why we don't discount Starter tier

Following up on Jake's question about how we arrived at the tier boundaries.

When we restructured in 2024, we looked at feature usage data across 2,400 customers. There were clear clusters: basic users who used search, storage, and basic workflows (now Starter), power users who needed integrations, advanced analytics, and API access (now Professional), and organizations that needed custom SLAs, SSO, and compliance features (now Enterprise).

The feature bundles aren't arbitrary. We drew the lines where the usage data showed natural breakpoints. The one judgment call was putting API access in Professional instead of Enterprise — the data was ambiguous but we decided broader API access would drive ecosystem growth and make the platform stickier at the mid-market level. That's paying off — API adoption in Professional tier is 3x what it was when API was Enterprise-only.

Priya
```

---

### submission-03-onboarding-retro-transcript.md

```
Meeting Transcript — Onboarding Retrospective: Cascade Corp
Date: April 1, 2025
Attendees: Marcus Chen, Lisa Park, Dev Okafor

Marcus Chen: Let's do the retro on Cascade. They went live last Friday, day 87. Technically within the 90-day window but it was tight. What happened?

Lisa Park: Phase 1 went fine. Standard environment, clean data migration. The issue was Phase 2 — they had five source systems to integrate, not the three they told us during scoping.

Dev Okafor: And two of those were legacy on-prem systems with no modern API. We had to build custom connectors.

Marcus Chen: This is the recurring pattern. Customers understate their integration complexity during sales. By the time we discover the real scope, we're already in Phase 2 with a committed timeline.

Lisa Park: Should we add a technical discovery step before Phase 1 starts? Like a week-long scoping engagement?

Marcus Chen: I've been thinking about this. The problem is sales doesn't want to add time before contract close, and customers don't want to pay for scoping before they've committed. What if we built it into the first week of Phase 1? Call it "Integration Discovery Sprint." Same 90-day timeline, but the first 5 days are dedicated to mapping every system they need to connect, confirming API availability, and flagging anything that needs custom work.

Dev Okafor: That would have caught the Cascade situation on day 5 instead of day 35.

Marcus Chen: Exactly. And then we can adjust the Phase 2 timeline within the overall 90 days instead of scrambling at the end.

Lisa Park: What about the customers where integration discovery reveals they need more than 90 days?

Marcus Chen: Then we have an honest conversation early. A timeline extension on day 5 is a project management conversation. A timeline extension on day 60 is a trust conversation. I'd rather have the first one.

Dev Okafor: The other thing about Cascade — their IT team was unresponsive for two weeks in Phase 2. We couldn't get credentials for the legacy systems. Should we have an escalation path for that?

Marcus Chen: We do, but it's informal. I pinged their VP of Engineering directly. We need to formalize it. Going forward, the kickoff meeting should establish an escalation contact on the customer side — someone with authority to unblock IT resource allocation. Add it to the kickoff template.

Lisa Park: And the training phase — did they feel ready at go-live?

Marcus Chen: Honestly, Phase 3 was compressed because Phase 2 ran long. We did two training sessions instead of the usual four. I'm not thrilled about it. We're going to check in with them at 30 days post-launch and offer supplemental training if needed. But this is exactly why the integration discovery sprint matters — protect Phase 3 by getting accurate scope in Phase 1.

Dev Okafor: One more thing — the custom connectors we built for their legacy systems. Are those reusable?

Marcus Chen: The Oracle connector probably is, it's fairly standard. The AS/400 one is too specific. But let's document both in the integration playbook so the next team doesn't start from zero.
```

---

### submission-04-hiring-process-email.md

```
From: Alex Rivera
To: Engineering Managers
Date: February 20, 2025
Subject: Updated Interview Process — What Changed and Why

Hi all,

The new interview rubric is live as of this week. I know change is annoying so let me explain why we did this.

The old rubric had been in place since 2021. It was designed for a 50-person engineering team doing primarily backend work. We're now 180 engineers across backend, frontend, ML, and platform. The rubric wasn't scaling.

Specific problems:
- The "culture fit" criterion was our highest-variance score. Two interviewers could interview the same candidate and score culture fit 2/5 and 5/5. It was measuring interviewer personality alignment, not anything about the candidate.
- The coding exercise was a single 60-minute live coding session. Our data showed zero correlation between live coding performance and 6-month performance reviews. Literally zero. r = 0.03.
- Senior candidates consistently told us the process felt junior. We were losing Staff+ candidates to competitors with more respect-based processes.

What we changed:
- Replaced "culture fit" with "collaboration signals" — three specific behavioral questions with defined scoring anchors. Interviewers score observable behaviors, not vibes.
- Replaced live coding with a take-home project (48-hour window, scoped to 3-4 hours of work) followed by a 30-minute code review discussion. We're testing the candidate's ability to make decisions, write maintainable code, and explain their reasoning — not their ability to perform under artificial time pressure.
- Added a "system design conversation" for senior roles (L5+). Not whiteboard architecture — an open discussion about a real system they've built, what tradeoffs they made, what they'd do differently. This is where tacit engineering knowledge shows up.

Early results: offer acceptance rate is up from 62% to 78% since the pilot in Q4 2024. The collaboration signals score has much lower variance across interviewers (std dev dropped from 1.4 to 0.6). Take-home completion rate is 91% — higher than I expected.

One thing we're watching: the take-home creates a 48-hour delay in the process. Two candidates have cited this as a reason for declining to continue. We may need to offer an alternative for candidates actively in multiple processes. Not changing it yet but flagging it.

The full rubric and scoring guide is in the shared drive. Please have all interviewers review it before their next panel.

Alex
```

---

### submission-05-vendor-assessment-transcript.md

```
Meeting Transcript — Vendor Assessment Framework Review
Date: March 10, 2025
Attendees: Jordan Lee, Finance VP Sarah Walsh, Legal Counsel Tom Park

Jordan Lee: I want to walk through the vendor assessment framework updates. We've had the current scoring model since 2022 and it needs a refresh.

Sarah Walsh: What's broken?

Jordan Lee: Two things. First, the risk weighting doesn't account for vendor concentration. We have four vendors where we spend over $500K annually and if any of them went down, we'd have a major operational disruption. The current framework treats a $500K vendor the same as a $50K vendor from a risk perspective — it only looks at service quality and price.

Tom Park: That's a legal liability issue too. If we're dependent on a single vendor for a critical function and they fail, our customers will want to know what due diligence we did.

Jordan Lee: Exactly. So the updated framework adds a "criticality tier" classification. Tier 1 is any vendor supporting a customer-facing function or processing customer data. Tier 2 is internal operations that affect delivery. Tier 3 is everything else. Tier 1 vendors get annual business continuity reviews, required backup vendor identification, and contractual right-to-audit clauses.

Sarah Walsh: What's the cost impact of the audit clauses?

Jordan Lee: Minimal for new contracts — we just add the language. For existing contracts, we'll negotiate it in at renewal. Some vendors will push back. Our position is it's non-negotiable for Tier 1. We walked away from the CloudSync renewal last year over this and found a replacement in six weeks. That set the precedent.

Tom Park: The CloudSync situation was actually useful. They were our document conversion provider and refused the audit clause. We moved to DocuParse, who agreed to all terms and actually has better throughput. Sometimes losing a vendor is the right outcome.

Jordan Lee: The second issue is termination penalties. Our standard contract template has a 90-day termination notice period with no penalty. But over the years, sales teams on the vendor side have negotiated custom terms into some contracts. I found three contracts with early termination fees ranging from $25K to $150K that nobody in procurement approved.

Sarah Walsh: How did that happen?

Jordan Lee: Department heads signed vendor agreements directly without routing through procurement. This was before we centralized in 2023. Going forward, any contract with financial commitments over $10K requires procurement sign-off. That's been policy since 2023 but we're still finding legacy agreements that predate it.

Tom Park: Should we do an audit of all active contracts for non-standard terms?

Jordan Lee: Already started. We have 67 active vendor contracts. I've reviewed 41 so far. Found non-standard terms in 8 of them. Most are minor — extended payment terms, auto-renewal clauses we didn't agree to. The three with termination penalties are the worst. I'll have the full audit done by end of April.

Sarah Walsh: What about the vendor that provides our SSO integration? I heard there were issues.

Jordan Lee: AuthBridge. Yes. They had two outages in Q4 that each took our SSO down for about 4 hours. Their SLA says 99.9% uptime and they technically met it over the quarter, but two 4-hour outages in critical windows is different from distributed minor downtime. We're adding a clause for maximum single-incident downtime — no single outage can exceed 2 hours for Tier 1 vendors, regardless of quarterly SLA math. That's a lesson learned from the AuthBridge situation.
```

---

### submission-06-infrastructure-postmortem.md

```
Post-Incident Report — Customer Portal Latency Event
Date: March 22, 2025
Author: Dana Torres
Severity: P2
Duration: 3 hours 42 minutes (14:18 - 17:50 UTC)

Summary:
Customer portal response times degraded to 8-12 seconds (normal: 200-400ms) affecting approximately 2,300 active users. No data loss. Root cause was an unindexed database query introduced in the March 20 release.

Timeline:
- 14:18 — Monitoring alerts on p95 latency exceeding 5s threshold
- 14:25 — On-call engineer confirms degradation, begins investigation
- 14:40 — Initial suspicion: increased traffic from new marketing campaign. Traffic analysis disproves this — request volume is normal, response times are slow
- 15:15 — Database team identifies a full table scan on the customer_events table (4.2M rows) triggered by the new activity feed query. This query was added in the March 20 release
- 15:30 — Decision point: roll back the release or add the index? Team debates. Rolling back removes the activity feed feature that marketing has already announced. Adding the index is faster but we've never hot-indexed a table this size in production
- 15:45 — Decision: add the index. Reasoning: the index can be created with CONCURRENTLY flag in Postgres, which doesn't lock the table. Rollback would take ~20 minutes and has its own risk of introducing state inconsistencies with data written since the release
- 16:00 — Index creation begins. Estimated time: 90 minutes for 4.2M rows
- 17:35 — Index creation completes
- 17:50 — Latency returns to normal. Incident resolved

Root Cause:
The activity feed query was tested against the staging database which has 50K rows in customer_events. At that scale, the full table scan completed in 80ms — well within acceptable range. Production has 4.2M rows. The query plan changes at scale — Postgres optimizer chooses a sequential scan when the table fits in memory at small scale but can't at large scale.

What We're Changing:
1. Pre-release query review: Any new query touching tables with >100K rows requires an EXPLAIN ANALYZE against a production-scale dataset. We're building a shadow database with production-volume synthetic data for this purpose.
2. Staging data scale: Staging will be loaded with production-scale data (anonymized) quarterly. This has been requested for two years but was deprioritized. Not anymore.
3. Release-day monitoring: Tightening the latency alert threshold from 5s to 2s for the first 4 hours after any release. Current 5s threshold meant we didn't catch the gradual degradation until it was severe.

Why the Old Process Missed This:
Our code review process checks for SQL injection, N+1 queries, and missing WHERE clauses. It does not check for missing indexes because index requirements are scale-dependent and our reviewers don't have production table sizes memorized. The pre-release query review process above fills this gap.

Decision Log:
- Chose hot-indexing over rollback: correct decision in retrospect. Index creation was uneventful and faster than estimated. Rollback carried migration state risk.
- Chose CONCURRENTLY flag: correct. No table locks, no additional user impact during index creation.
- Did not pursue read replica failover: discussed and rejected. Read replica was already receiving the same unindexed query. Would have moved the problem, not solved it.
```

---

### submission-07-benefits-slack-thread.md

```
Slack Thread — #hr-questions
Date: March 25, 2025

Casey N: Hey @Alex Rivera quick question — what's the deal with the wellness stipend? I heard it changed.

Alex Rivera: Yeah, we updated it in January. The old policy was $500/year for gym memberships only. New policy is $1,200/year for any wellness-related expense — gym, therapy, meditation apps, ergonomic equipment, nutrition counseling, whatever. Just needs a receipt.

Casey N: Nice. What prompted the change?

Alex Rivera: Utilization data. The gym-only stipend had 23% utilization — most people either already had a gym membership through their own means or didn't go to a gym. We were spending budget on a benefit people didn't use. The expanded definition was based on an employee survey where we asked "what would you actually use a wellness benefit for?" Top answers were therapy/counseling (41%), fitness (28%), ergonomic home office (18%), and meditation/mindfulness apps (13%).

Jordan Lee: Does this affect the vendor relationship with FitCorp? We had a corporate rate with them.

Alex Rivera: We kept the FitCorp partnership as an option but it's no longer the only path. Employees can use FitCorp at the corporate rate OR use the stipend for any other provider. FitCorp usage actually went up slightly because people who weren't using the benefit at all are now engaging with wellness for the first time and some are choosing FitCorp.

Casey N: Is the $1,200 pro-rated if you start mid-year?

Alex Rivera: Yes, pro-rated by quarter. Start in Q2, get $900. Start in Q3, get $600. Unused balance doesn't roll over — use it or lose it by December 31. We considered rollover but finance flagged the accrual liability. The use-it-or-lose-it model keeps the budget predictable.

Sam K: One more — can you split it? Like $600 on therapy and $600 on a standing desk?

Alex Rivera: Absolutely. No minimum per category. The only rules are: must be wellness-related (we have a list of approved categories but it's broad), must have a receipt, and must be for the employee (not family members — that's a tax thing we can't work around without changing the benefit structure).
```

---

### submission-08-compliance-training-doc.md

```
Document: Compliance Training Requirements — Updated March 2025
Author: Jordan Lee

This document summarizes current compliance training requirements and the rationale behind recent changes.

ANNUAL REQUIRED TRAINING

All employees must complete the following annually:
- Information Security Awareness (1 hour)
- Anti-Harassment and Workplace Conduct (45 minutes)
- Data Privacy and GDPR/CCPA (30 minutes)

Additionally by role:
- Customer-facing roles: Customer Data Handling (30 minutes)
- Managers: Inclusive Leadership (1 hour)
- Engineers with production access: Incident Response Protocol (45 minutes)

WHY WE CHANGED THE SECURITY TRAINING

The previous security training was a 15-minute video from 2021 that covered password hygiene and phishing. Completion rate was 94% but our internal phishing simulation click rate stayed flat at 22% — meaning the training wasn't changing behavior.

In Q3 2024 we switched to an interactive module from KnowBe4 that includes simulated phishing scenarios tailored to our actual email patterns. Since the switch, the phishing simulation click rate has dropped to 9%. The training takes longer (1 hour vs 15 minutes) and we got pushback on that. Our response: 45 extra minutes once a year is cheaper than one successful phishing attack. The average cost of a phishing-initiated breach in our industry is $4.2M.

WHY MANAGERS GET EXTRA TRAINING

The Inclusive Leadership module was added in 2024 after our engagement survey showed a 15-point gap between how managers rated their own inclusivity and how their reports rated it. The training focuses on specific behaviors — meeting facilitation, feedback delivery, promotion criteria communication — not abstract concepts. We chose this approach because the research on unconscious bias training shows it doesn't work. Behavioral training with specific practices does.

COMPLIANCE TRAINING EXCEPTIONS

Contractors are exempt from the Inclusive Leadership module but must complete all other training. This is a legal distinction — the module includes exercises about internal promotion processes that don't apply to contractors, and their contracts specify the required training scope.

Employees on leave of more than 90 days get a 30-day grace period upon return to complete overdue training. This was added after we had an employee return from medical leave to find 4 overdue compliance items on day one. That's not how you welcome someone back.
```

---

## Demo Flow

### Scene 1: The Gap
User: "What's our policy on vendor contract SLA requirements?"
AI checks KB, finds vendor-contracts.md but no SLA content. Answers what it can about the renewal process and its history, logs the gap, routes to Jordan Lee.

### Scene 2: Decay Detection
User: "How does our vendor contract renewal process work?"
AI finds the answer in vendor-contracts.md and responds with the full rationale (DataStream incident, 90-day window reasoning). But the Last Verified date is 2024-08-20 — over 200 days ago. AI flags this: "Note: this information was last verified on August 20, 2024. It may be worth confirming it's still current." AI creates a Verify item in Knowledge Gaps assigned to Jordan Lee.

### Scene 3: The Expert Fills the Gap (Typed)
User (as Jordan): "I can answer that SLA question. Our standard SLA for Tier 1 vendors requires 99.5% uptime, 48-hour response for support tickets, and quarterly business reviews. For Tier 2 it's 99% uptime and 5-business-day response. We tightened Tier 1 requirements after the AuthBridge outages in Q4 — their SLA math technically passed but two 4-hour outages in critical windows was unacceptable. So we added a max single-incident downtime clause: no outage can exceed 2 hours regardless of quarterly SLA averages. Tier 3 vendors just need to meet basic contractual commitments, no SLA scoring. And yes — the renewal process is still accurate, no changes since it was documented."
AI ingests the SLA knowledge with full rationale and history, resolves the SLA gap. Also updates the Last Verified date on the existing renewal process entry and resolves the Verify item.

### Scene 4: The Payoff
User: "What uptime do we require from critical vendors, and why is it set at that level?"
AI answers with both the fact AND the reasoning — the AuthBridge incident, the distinction between quarterly SLA math and single-incident impact. Last Verified is now today — no staleness flag.

### Scene 5: Transcript Ingestion
Upload the security review transcript to Submissions.
User: "Process the new transcript in Submissions."
AI extracts certifications, pen testing details (including why CrowdStrike over Rapid7), tenant isolation (including the Meridian incident that drove the redesign), data retention (including why it was shortened from 90 to 30 days). Resolves the security certifications gap. Sets Source Type to Transcript.

### Scene 6: Email Ingestion
Upload the pricing decision email to Submissions.
User: "There's a new email thread in Submissions about pricing. Please process it."
AI extracts the no-discount-on-Starter rationale, the tier boundary logic, the API access decision. Updates product-pricing.md with the reasoning layers. Also refreshes the Last Verified date on the existing pricing entries and resolves the pricing Verify item. Sets Source Type to Email.

### Scene 7: Admin Report
User: "Give me the full knowledge base admin report."
AI runs the KB Admin Report skill and produces:

**Corpus Overview:** X topic files covering customer onboarding, product pricing, vendor contracts, security policies (new), etc. Breakdown of entries per file, source contributors, date ranges.

**Decay Report:** Flags any entries still past 90 days. Shows which were just refreshed by Scenes 3 and 6. Highlights customer-onboarding.md entries last verified January 10 — still stale.

**Gap Status:** Shows resolved gaps (SLA question, security certs, pricing verify), remaining open gaps (hiring process, termination penalties), and how many were decay-triggered verifications vs. organic questions.

**Ingestion Activity:** Breakdown by Source Type — shows that knowledge entered via Typed (Scene 3), Transcript (Scene 5), and Email (Scene 6). Recommends processing Slack threads and documents as well to diversify sources.

**Expert Coverage:** Maps experts to topics. Flags that security policies has no registered expert (Dana Torres should be added). Flags that hiring process has an open gap and Alex Rivera is in the Expert Directory but wasn't auto-matched (expertise areas need updating).

**Recommendations:** Top 3-5 actions: re-verify customer onboarding entries with Marcus Chen, add Dana Torres to Expert Directory for security, update Alex Rivera's expertise areas to include "hiring process" and "interview," process remaining submissions.

### Scene 8: Postmortem Ingestion (Bonus)
Upload the infrastructure postmortem.
User: "We had an incident last week. The postmortem is in Submissions. Add what we learned."
AI creates infrastructure-operations.md with the incident details, the decision to hot-index vs rollback (and why), and the three process changes. Captures the rejected option (read replica failover) and why it was rejected.

### Scene 9: Onboarding Retro (Bonus)
Upload the Cascade onboarding retro transcript.
User: "Process the Cascade retro from Submissions."
AI updates customer-onboarding.md with the Integration Discovery Sprint proposal, the escalation contact formalization, and the lesson about compressed training. Refreshes Last Verified on the onboarding entries. Sets Source Type to Transcript.

---

## Demo Tips

- Scenes 1-4 show the core gap→fill→payoff cycle
- Scene 2 is the decay demo — the AI proactively flags stale knowledge
- Scene 3 does double duty: fills a gap AND re-verifies stale content
- Scenes 5-6 show automated ingestion from different source types
- Scene 7 is the management view — run it after several ingestions to show the system's self-awareness
- Scenes 8-9 show depth of ingestion — postmortems capture decisions and rejected alternatives, retros capture process improvements
- For maximum impact, run Scene 7 twice: once early (lots of stale entries, open gaps) and once after several ingestions (gaps closing, decay resolving, coverage improving)
