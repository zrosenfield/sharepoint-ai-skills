# Build the Obligation Hub from scratch (one prompt)

**For the person running it.** This prompt rebuilds the whole Obligation Hub (lists, skills, pages, sample data, workflow prompts) on a new SharePoint site without the rest of this kit, for when the setup skill or deploy script isn't an option or to prove the design is reproducible.
- **You need** Cowork with the SharePoint tools, owner rights on a **new, disposable** site, and code execution for the sample contracts. AI workflows, autofill and HTML pages with live list data are preview features that may not be available in your tenant yet.
- **How:** paste everything below the line into a new Cowork conversation and fill in the three `<…>` values. The agent stops at each ⏸ approval point, and every SharePoint write shows an approval card. It won't create the AI workflows (you paste six prompts into Copilot in SharePoint) or use real data.
- **Afterwards,** run the evals in [`evals/`](../evals/README.md). Unofficial community sample, not a Microsoft template.

---

You will build **Obligation Hub for SharePoint** on `<SITE URL, or "a new site named …">` for `<OUR COMPANY LEGAL NAME>` (demo: the fictional Northwind Traders, Inc.). Leadership digest recipients: `<EMAILS, or "none yet">`. Work through sections 1–12 in order. Never delete or overwrite anything you didn't create in this conversation. Use fictional names only.

## 1. Goal and buyer
Post-signature obligation management (who owes what, by when, triggered by what, as legal AI tools such as Harvey and Legora offer) inside Microsoft 365, without a CLM. **Buyer:** a legal-ops or contract-management lead whose signed contracts live in SharePoint. **Users:** obligation owners, contract managers, leaders, the site owner. It replaces a manual-only third-party skill package that had schema conflicts: one schema with fixed internal names, one settings file, automation through AI workflows and quick steps.

## 2. Scope
**In:** capture from contracts and amendments; a quoted register; routing; timing, reminders, escalation, roll-forward; digests; evidence; exclusions; review queue; 7 pages; 11 sample contracts with an answer key; evals.
**Out:** e-signature, CLM or ERP integration; payment checks against AP; SLA measurement; per-contract permissions; dollar exposure and trends; detecting trigger events; scanned paper; sending notices; legal advice.

## 3. Domain model
- **Obligation:** one action plus one trigger, owed by one side under one clause, stored with the clause reference and verbatim source sentence. A contract-management register, not a service checklist.
- **Party**, from our side: *Us* (we act), *Counterparty* (they act; we monitor and chase), *Both* (mutual, or either may act).
- **TriggerType:** *Fixed date* (one-time); *Recurring* (fixed schedule); *Event-driven* (waits for an event: no DueDate, TriggerEvent in plain words); *Ongoing* (all term: no DueDate, no TriggerEvent). A payment is Recurring only if both the invoice date and the payment period are fixed.
- **Recurrence:** None unless Recurring; one item per occurrence, and fulfilling one creates the next (`<base key>#<next due date>`).
- **Status vs Timing:** people set Status. Timing is computed: Closed (Fulfilled, Waived, Not applicable); No date; Overdue (DueDate < today); Due soon (within `dueSoonDays`, 14); else Upcoming.
- **Review hold:** unclear, Low-confidence or Hold-for-review items get ReviewState = Needs review and a reason in Notes; nobody is assigned or reminded until a person confirms them.
- **Capture key upsert:** CaptureKey = `<file name>|<ClauseRef>|<slug>` (verb-first slug). Re-capture matches by key, then clause + source text, then clause + party + action, and updates only capture-owned fields; items without a key are people's and never touched.
- **Exclusions memory:** removing an item records its clause (this contract) or a generalised pattern (all contracts); capture applies active exclusions first, so removed items don't come back.
- **Amendments supersede:** base items whose clause an amendment deletes or replaces become Not applicable, Timing Closed, Notes "Superseded by <amendment file> <section>" (once). Amended terms are captured under the amendment. The final state mustn't depend on which file is captured first.

## 4. Schema (internal names are the contract)
Create each list with its columns in one call and its views in a second call. Rename the built-in Title column's display name as shown. **Open** = Status not Fulfilled, Waived or Not applicable. **Cat** = Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other. **BU** = Sales, Procurement, Finance, Legal, IT, Facilities, Operations.

**Contracts** (library `/Contracts`)
| Column (display) | Type · choices (default) |
|---|---|
| Title (Contract title), Counterparty, GoverningLaw (Governing law), Amends (base file name) | Text |
| ContractType (Contract type) | Choice: Customer agreement, Supplier agreement, Partner agreement, License, Lease, Financing, Data processing, Amendment, Other |
| EffectiveDate, ExpirationDate | Date only |
| AutoRenews (Auto-renews) | Choice: Yes, No, Unclear |
| NoticePeriodDays (Notice period (days)) · ContractValue (Contract value) | Number · Currency |
| ContractSummary (Summary) | Multi-line, under 250 characters |
| ContractOwner (Contract owner) · BusinessUnit (Business unit) | Person · Choice: BU |
| IsSample (Sample data) | Yes/No (No) |

Optional autofill prompts on Counterparty through ContractSummary. Views: **All contracts** (default; DocIcon, LinkFilename, then the columns above from Counterparty to BusinessUnit except GoverningLaw, ContractValue, ContractSummary and Amends; sort Counterparty); **Expiring in 180 days** (ExpirationDate set and ≤ Today+180; DocIcon, LinkFilename, Counterparty, ExpirationDate, AutoRenews, NoticePeriodDays, ContractOwner; sort ExpirationDate).

**Obligations** (list `/Lists/Obligations`, 27 columns)
| Column (display) | Type · choices (default) |
|---|---|
| Title (Obligation), ContractName (Contract), Counterparty, ClauseRef (Clause), TriggerEvent (Trigger event), CaptureKey (Capture key) | Text |
| ObligationText (What must happen), SourceClause (Source clause), Notes | Multi-line plain |
| ContractLink (Contract link), Evidence | Hyperlink |
| Party (Who owes it) | Choice: Us, Counterparty, Both (Us) |
| Category · BusinessUnit (Business unit) | Choice: Cat · Choice: BU |
| TriggerType (Trigger) | Choice: Fixed date, Recurring, Event-driven, Ongoing |
| Recurrence | Choice: None, Weekly, Monthly, Quarterly, Semi-annual, Annual (None) |
| DueDate (Due date), FulfilledOn (Fulfilled on), LastReminded (Last reminded) | Date only |
| Owner, EscalationOwner (Escalation owner) | Person |
| Status | Choice: Not started, In progress, Fulfilled, Waived, Not applicable (Not started) |
| Timing | Choice: Overdue, Due soon, Upcoming, No date, Closed |
| ReviewState (Review) | Choice: Confirmed, Needs review (Needs review) |
| Confidence · Risk | Choice: High, Medium, Low · same (Medium) |
| IsSample (Sample data) | Yes/No (No) |

| View (LinkTitle first) | Filter · sort | Other columns |
|---|---|---|
| Open by due date (**default**, 100 rows) | open AND DueDate set · DueDate ascending | Counterparty, Category, DueDate, Timing, Status, Owner, Party, Risk, ReviewState |
| Triggered and ongoing (100 rows) | open AND DueDate empty · Counterparty | Counterparty, Category, TriggerType, TriggerEvent, Owner, Party, Risk, ReviewState |
| My obligations | Owner = `<Value Type='User'><UserID/></Value>` · DueDate | Counterparty, Category, DueDate, Timing, Status, Risk |
| Needs owner | Owner empty · DueDate | Counterparty, Category, BusinessUnit, DueDate, Risk |
| Needs review | ReviewState = Needs review | Counterparty, ClauseRef, Category, Confidence, DueDate, Notes |
| By contract | grouped by ContractName · DueDate | Category, Party, DueDate, Recurrence, Status, Owner |
| Calendar | modern calendar on DueDate, month | DueDate, Counterparty, Status |
| All obligations | none | Counterparty, Category, DueDate, Timing, Status, Owner, Party, Risk, ReviewState, ContractName, ClauseRef, TriggerType, Recurrence, TriggerEvent, EscalationOwner, BusinessUnit, Confidence, FulfilledOn, Evidence |

Colour Status, Timing, Risk and ReviewState with inline-style column formatting.

- **Obligation Owners:** Title (Rule); Category Any + Cat (Any); BusinessUnit Any + BU (Any); Counterparty text; Owner, EscalationOwner person; Notify (Notify by) Email, Teams, Both (Both). View All rules.
- **Obligation Types:** Title (Obligation type); Category Cat; Handling Track, Exclude, Hold for review (Track); DefaultRisk High, Medium, Low (Medium); DefaultRecurrence as Recurrence (None); Description, Examples multi-line. View All types.
- **Exclusions:** Title (Exclusion); Pattern, Reason multi-line; Scope All contracts, This contract (This contract); ContractName text; Category Cat; Active Yes/No (Yes). View All exclusions.
- **Run Log:** Title (Run); Workflow Capture, Assign owners, Daily sweep, Owner digest, Leadership digest, Mark fulfilled, Exclude, Setup; Outcome Succeeded, Partial, Failed, Skipped; ContractName, ContractVersion text; ItemsCreated, ItemsUpdated, ItemsHeld number; Details multi-line; RunAt date and time. View Recent runs, newest first.
- **Evidence** (library): Title (Evidence title); IsSample Yes/No (No). **AgentAssets** (library): `Skills/<skill-name>/SKILL.md`, `Config/`, and `SHAREPOINT.md` in the root.
- **Settings** `AgentAssets/Config/hub-settings.json`: ourCompany, siteUrl (no trailing slash), timeZone ("Pacific Standard Time"), dueSoonDays 14, escalateAfterDaysOverdue 0, reminderCooldownDays 3, leadershipRecipients [], leadershipTeamsChannel {team, channel}, notifyDefault "Both", captureHoldBelowConfidence "Medium", maxDigestItems 25.
- **Seed Obligation Types** (37 rows, each with a description and example wording): 29 *Track* rows, one per protected control in section 5 (DefaultRisk High for renewal, option and expiry windows, change of control, covenants, default and breach notices, compliance certificates, minimum commitments, true-ups, defect windows); 5 *Exclude* rows (Other, Low): contacts and invoicing logistics; good-faith conduct; legal boilerplate; routine service delivery and site rules; conditions met at signing; 3 *Hold for review*: efforts-based or third-party duties; indemnity claim procedures; record retention and end-of-term data return. Add the routing rule "Default - all obligations" (Any/Any; owner and escalation = the person running setup).

## 5. Skills (10)
Each is `Skills/<name>/SKILL.md` with front matter `name` (= folder) and a third-person `description` (what + when); **prose and Markdown only, no executable code**, under 500 lines. Every skill reads the settings first, writes **exactly one Run Log row per run** (Skipped and Failed too), and writes dates as YYYY-MM-DD.
1. **setup-obligation-hub:** ask once (company, recipients, time zone, autofill); read the site; show a Piece | Now | Will do plan; after one "yes" build only what's missing; stop on conflicts (wrong template or column type); delete nothing but the "All Items" view of a list it just created; list what's left.
2. **capture-obligations** (file added or changed; Re-capture quick step):
   - **Gate:** not a contract → Skipped. Fingerprint `<W>~<R>`: W = body word count (tokens with a letter or digit, table cells in, headers and footers out), R = sorted related file names. Skip "content unchanged" when identical, or same R and W within 0.5%, unless a person asked for capture.
   - **Read:** map defined roles to Us or Counterparty; find the base and amendments; walk every operative sentence (*shall, must, will, within N days, upon*). Keep duties and prohibitions; keep permissions only if they control the contract's life, forfeit a right or money by a deadline, or create our duty; merge financial mechanics into their obligation; drop facts, representations and anything done at signing; hold what's unclear.
   - **Routine-admin EXCLUDE:** contacts, notice and invoice addresses; "cooperate in good faith"; service descriptions and standards with no trigger; uniforms, badges, site access; boilerplate (headings, counterparts, own costs, governing law, liability caps, assignment consent, entire agreement, severability, force majeure, survival, waivers).
   - **Protected controls, always track:** payments, fee-change notices, rebates, true-ups, minimum commitments; SLAs and credits someone must issue or claim; reports and compliance certificates; insurance certificates; audit cooperation; event notices (breach, default, change of control, discontinuation, sub-processors); key personnel; renewal, termination-for-convenience, option and transition windows; post-closing deliverables; exclusivity, use limits, most-favoured pricing, financial covenants, confidentiality, data protection.
   - **Missing document:** a protected obligation whose terms sit in a document that isn't in Contracts → ONE held item (Low, Notes "Terms in <document>, which isn't in the Contracts library — add it or confirm the terms"); never excluded or guessed. Precedence: active Exclusion > protected control > type Handling > other guardrails.
   - **Verification checklist** (retain only if all hold): who owes it; the action; the trigger, date or "ongoing"; the clause reference; the verbatim, contiguous source sentence; the category; no exclusion. Missing 1, 2, 3 or 5 → hold; 7 → exclude and list in Details.
   - **Date rules:** "within N days after X" = X + N calendar days (business days only if stated); "at least N days before X" = X − N, the last day for notice; N months before or after = same day of month, or that month's last day; operative stated dates beat arithmetic, illustrative exhibits only confirm; roll auto-renewing terms forward until the next deadline ≥ today; Recurring = next occurrence ≥ today; passed Fixed dates stay (Overdue); option windows: DueDate = closing date, Notes "Window opens <date>"; a fixed expiry within 12 months with no renewal option gets "Decide on <counterparty> renewal before <date> expiry" (Both, High).
   - **Risk rubric** (consequence of a miss): *High* if it loses a right or money or starts a legal clock (notice, renewal and option deadlines we must act on; change-of-control and breach notices; financing covenants, compliance certificates, default notices); *Medium* for other dated or money obligations; *Low* for ongoing conduct and counterparty duties we only monitor (other than payments and data). Expect 15–30% of open items High.
   - **Write:** Confidence Low (ambiguous, missing document) is always held; titles ≤ 80 characters, verb first. Supersede per section 3; upsert by CaptureKey; re-read just before writing; mark open items no longer found for review. **Never write to Contracts** (it retriggers capture), never send messages, never invent dates, amounts, clauses or quotes.
3. **assign-obligation-owners** (daily 7:00): open, Confirmed, unowned items; the most specific rule wins (counterparty, category + BU, category, BU, Any/Any; ties → lower ID); set Owner and EscalationOwner; one message per newly assigned owner on the rule's Notify channel.
4. **sweep-obligations** (daily 6:00, never reads Contracts): recompute Timing, writing only changes; roll forward Fulfilled or Waived recurring items (never Not applicable) to the next date (month-end clamp), stopping after "Through/Last due <date>" and skipping existing successors; remind Due soon owners once per window; escalate Overdue items to the escalation owner, at most every `reminderCooldownDays`; set LastReminded only for sent messages; skip held items. A second run the same day changes and sends nothing.
5. **obligation-owner-digest** (Mondays 8:00): one message per owner (Overdue, Due soon, Next 30 days; at most 25); skip owners with nothing due and same-day repeats.
6. **obligation-leadership-digest** (Fridays 15:00, read-only): counts; top 10 overdue by risk then days; notice deadlines in 120 days and expiring contracts with no tracked decision; no owner; needs review; fulfilled this week; no invented metrics.
7. **mark-obligation-fulfilled** (quick step): one item; ask once for evidence (link, file or none) unless given; Status Fulfilled, FulfilledOn = the stated date or today, Timing Closed; next occurrence by the sweep's rule; one-line confirmation.
8. **exclude-obligation** (quick step "Remove obligation"): ask scope, reason and remove-now in one message; reuse a matching exclusion; Pattern = the verbatim clause, or a generalisation + `Example: "<clause>"` for all contracts; set the item Not applicable with an "Excluded:" note; never change other items.
9. **obligation-hub-guide** (questions): answer from the lists; compute Timing; never estimate dates; cite ClauseRef, a short quote and `<siteUrl>/Lists/Obligations/DispForm.aspx?ID=<ID>`; read contract text only when needed, citing file and section; flag held and sample items; short answer, then one table; hand changes to the skills above.
10. **clear-obligation-sample-data:** after one confirmation, delete only IsSample = Yes items and files and Run Log rows whose Details start "Demo seed".

Also write `SHAREPOINT.md`: what the site is, where things are, which skill does what.

## 6. AI workflows and quick steps
| Workflow | One trigger | Skill | May send |
|---|---|---|---|
| Capture new contracts | file added to Contracts | capture-obligations | nothing |
| Capture changed contracts | file changed in Contracts | capture-obligations | nothing |
| Assign owners | daily 7:00 AM | assign-obligation-owners | one message per new owner |
| Daily sweep | daily 6:00 AM | sweep-obligations | reminders, escalations |
| Owner digest | Mondays 8:00 AM | obligation-owner-digest | one per owner |
| Leadership digest | Fridays 3:00 PM | obligation-leadership-digest | recipients; optional Teams post |

Prompt for the site owner: "Create an AI workflow named "<name>" on this site. Trigger: <trigger>. For each run, load the site skill <skill> from AgentAssets/Skills and follow it. Save results without asking for confirmation. Run as me." They run as their creator, so use a shared account. **Loop safety:** capture skips unchanged text and never writes to Contracts; every run logs once; digests skip repeats. Quick steps (`{"actionType":"AskKnowledgeAgent","customPrompt":"…"}`): **Mark fulfilled** and **Remove obligation** on Obligations; **Re-capture obligations** on Contracts ("…Do a full capture even if the text hasn't changed.").

## 7. Pages and design
Seven standalone HTML pages in Site Pages, **with no menu of their own** (add them to the site navigation): **Home** (counts, notice windows, timeline, due next, workflow health); **My obligations** (items of the owner in `#owner=`, by Timing); **Contract 360** (terms, notice timeline, obligations by party, amendments, capture history); **Review queue** (held items with quote and reason; confirm, edit, remove); **Leadership** (by category and counterparty with High counts; no trends or dollars); **Settings** (lists, configuration, routing, workflows with last run and prompts); **How it works** (loop, roles, FAQ, known gaps).
- **Design language 01 Atmospheric Precision:** calm, premium; depth and light organise the page. Graphite `#111827` text; ice `#9AC7F5`, cloud `#EAF3FC`, white and restrained violet `#8B83DB` as tints. Neutral sans (Segoe UI Variable), deliberate type scale, few weights, 8-point spacing. Soft directional shadows, fine dividers, a soft page-top light; translucency sparingly, never on tables or forms. Refined cards, quiet segmented controls, pills; short spring motion only to show cause; honour reduced motion. WCAG 2.2 AA (text ≥ 4.5:1, focus, keyboard); designed loading, empty, error and Sample-vs-Live states; 1440/768/390 px layouts. With effects off the page stays polished and readable.
- **Sandbox rules:** one self-contained file per page (inline CSS, JS, SVG), ASCII, under 300 KB; no external URLs, fonts or scripts; no fetch, XMLHttpRequest, WebSocket, import, web storage, cookies, history API, `<link>`, `@import` or `url()` except `#fragments`.
- **Live-data manifest contract:** the first element in `<head>` (before `<meta charset>`) is `<script type="application/json" class="ka-livedata-manifest">` listing each list read as `{"kind":"list","spItemUrl":"list:<siteUrl>/<listId>","webUrl":"<siteUrl>","listId":"<GUID>","listServerRelativeUrl":"<path>"}`. The host injects `window.__LD_RESULTS__` keyed by spItemUrl (match case-insensitively); values are `{format:"rows", content:{headers, rows}}`, maybe as JSON strings. Wait about 800 ms, keep polling, else show a bundled sample snapshot (`data-sample="true"`). The badge reads "Live · N obligations" or "Sample snapshot · N"; a live empty list shows the empty state. Read columns by internal name, falling back to display names; accept person values in any shape.
- Build templates with `{{SITE_URL}}`, `{{PAGES_URL}}`, `{{LISTID_<LIST>}}`, `{{LISTURL_<LIST>}}` and `{{WORKFLOW_PROMPT_<KEY>}}` tokens; fill per site, upload, publish.

## 8. Sample data (fictional, generated by code)
Generate 11 Word contracts for Northwind Traders, Inc. from one data model, so documents and answer key share a source. Reference date 2026-11-24. Traps:
| File | Counterparty (our role) | Traps |
|---|---|---|
| 01-Contoso-MSA | Contoso Ltd (supplier) | 90-day non-renewal and 15-day report, both superseded by 02; credits we issue; COI by Dec 15; audit (their right, our duty); they pay in 45 days |
| 02-Contoso-MSA-Amendment-1 | Contoso (amends 01) | 120-day notice, "for clarity" date 2026-12-01; 10-day report; 4% fee increase on 60 days' notice with an illustrative exhibit; BCP plan (overdue) |
| 03-Fabrikam-Cloud-Hosting-Agreement | Fabrikam Inc (customer) | net 30 on invoices dated the 1st (Recurring); their SLA; our 30-day credit claim; their price notice; fixed expiry 2027-03-31; transition request by 2027-01-30 |
| 04-Tailspin-Distribution-Agreement | Tailspin Toys (distributor) | $750K minimum; quarterly report; marketing fund; marketing plan (overdue); mutual exclusivity; change of control; missing dealer credit application (hold) |
| 05-Litware-Software-License-Support | Litware Inc (licensee) | true-up after each anniversary; support auto-renews, 60-day notice; no affiliate use (prohibition); audit; own costs (routine) |
| 06-Proseware-Data-Processing-Agreement | Proseware Inc (controller) | their breach notice; sub-processor notice and our objection window; initial (overdue) and annual SOC 2; data return in a missing Services Agreement (hold) |
| 07-Alpine-Ski-House-Office-Lease | Alpine Ski House (tenant) | rent; deposit top-up on demand; option 12 to 9 months before 2027-09-30 (closes 2026-12-30); COI by Jan 15; repairs |
| 08-Wide-World-Importers-Supply-Agreement | Wide World Importers (customer) | forecast by the 5th; defect notice; their discontinuation notice; mutual price review; pay per shipment |
| 09-Adventure-Works-Reseller-Agreement | Adventure Works Cycles (reseller) | rebate; most-favoured pricing and price match; fixed expiry 2026-12-31; their payment per our missing credit terms (hold) |
| 10-Fourth-Coffee-Facilities-Services-Agreement | Fourth Coffee (customer) | six routine-admin clauses; their food-safety certificate; termination for convenience |
| 11-Woodgrove-Bank-Revolving-Credit-Facility | Woodgrove Bank (borrower) | interest; repayment 2029-09-15; quarterly certificate; audited financials; $5M liquidity; default notice; endorsements (overdue); closing fees (condition precedent); counterparts |

Answer key in JSON and Markdown: 69 rows (55 track, 3 hold, 9 exclude, 2 superseded) with contractFile, counterparty, title, obligationText, clauseRef, verbatim sourceClause, party, category, triggerType, recurrence, nextDueDate, triggerEvent, risk, expected, reason, isTrap, trapType; plus a contracts manifest. **Verify by code:** every sourceClause appears verbatim in its document, every date recomputes, counts match. Upload with IsSample = Yes and Amends set on 02.

## 9. Build order and approval points
1. Read the site; show the plan. ⏸ **A1:** site, company, recipients, time zone.
2. Lists (columns, then views), formatting, quick steps, seeds, settings. ⏸ **A2:** a schema dump matches section 4.
3. Write the skills and `SHAREPOINT.md`. ⏸ **A3**, then upload.
4. Generate and verify the sample. ⏸ **A4**, then upload (base before amendment) and capture each.
5. Build, check, fill, upload and publish pages; add them to the site navigation; set Home. ⏸ **A5**.
6. Hand over the workflow prompts and first-run test (one Run Log row each). ⏸ **A6**.
7. Run the evals and report. ⏸ **A7:** ship or not.

## 10. Platform facts (don't contradict them)
1. An AI workflow runs one site skill, has exactly one trigger (file added, file changed or schedule), runs as its creator and can send email and Teams; so capture needs two workflows, and "file changed" also fires on column edits and autofill.
2. Many columns plus views in one list call failed ("too many stages"): split them.
3. Person view filters need `<Value Type='User'><UserID/></Value>`; Integer was rejected.
4. Library multi-line columns were capped at 255 characters: keep summaries under 250 or set UnlimitedLengthInDocumentLibrary.
5. Uploaded HTML pages are drafts: publish before setting the home page.
6. Pages get live list data only via a manifest with site URL, list GUID and list URL.
7. Autofill may not run (it hadn't after an hour in testing): never depend on it.
8. Inline-style column formatting works; `sp-css` classes crashed.
9. create_folder needs a folderColor; update_list_items_v2 items use itemId.
10. A list created before its views keeps "All Items": make the intended view default or remove it.
11. Ascending DueDate sorts empty dates first, so the default view excludes them; undated items live in "Triggered and ongoing".
12. `SHAREPOINT.md` goes in the AgentAssets root.

## 11. Quality bar and evals
Run the kit's `evals/` where available, else equivalent checks. **Solution** (`evals/solution/EVALS.md`): schema (`check_schema.py`); invariants (`check_invariants.py`); capture (`score_capture.py`: recall, precision and each field ≥ 0.90, amendment and routine-admin traps 100%, held ≥ 2/3); state comparisons (`compare_states.py`); High risk 15–30%; pages (`check_pages.py`, page tests); workflow runtime; design review ≥ 70%. **Usage** (`evals/usage/USAGE-EVALS.md`): 15 tasks scored with `RUBRIC.md`, ≥ 80%, no 0 on Correctness or Safety.

## 12. Deliverables and acceptance
Deliver: the site (lists, views, formatting, quick steps, seeds, settings); 10 skills and `SHAREPOINT.md`; 7 published pages in the site navigation, Home as home page; six workflow prompts; the sample generator, contracts, manifest and answer key; an eval report; a known-gaps note (undated items aren't watched; no proof standard; accuracy measured on synthetic contracts; deadlines only; snapshot leadership view; My obligations can't detect the user; messages come from the workflow creator; no per-contract permissions; index lists above ~5,000 items).
**Accept** when every blocking solution eval passes, the usage suite scores ≥ 80% with no 0 on Correctness or Safety, and the report says what hasn't been measured.
