# Usage evals: does the hub help someone doing the job?

Fifteen tasks a real user would do with the hub, across four roles. Run them on the disposable test site after the blocking solution evals pass. A human tester or an agent (Copilot in SharePoint on the hub site, or Cowork with the SharePoint tools) does each task; a judge scores the result with [RUBRIC.md](RUBRIC.md).

Every expected answer below is computed by [`expected_answers.py`](expected_answers.py) from `sample-data/answer-key.json`, `contracts-manifest.json` and the contract `.docx` files, and stored in [`expected/expected_answers.json`](expected/expected_answers.json) under `tasks.<ID>`. The figures here assume **today = 2026-11-24**. Testing on another date: run `python3 expected_answers.py --today <date> --out expected/expected_answers-<date>.json` and grade against that file; the dates in the sample don't move, so more items show as overdue.

## Common setup (S0)

- Test site built and passing the blocking solution evals; the 11 sample contracts and their obligations loaded (pre-captured, or captured by a skill that passes S-07 to S-09). Register: 58 open items (55 Confirmed, 3 held for review), 2 superseded.
- Obligation Owners holds only "Default - all obligations" (Any/Any) with the **tester** as owner and escalation owner, and Assign owners has run once. Tasks U-11 and U-12 change this.
- The tester has a link to use as evidence (any file in the Evidence library or OneDrive).
- Click paths start from the **site navigation**: the hub pages have no menu of their own, so the site owner adds Home, My obligations, Contract 360, Review queue, Leadership, Settings and How it works to the site's navigation.
- Record: surface, model or agent, start and end time, the full answer (paste or screenshot), approval cards seen, and the Run Log rows written.

| ID | Role | Task | Surface | Writes? | Time target |
|---|---|---|---|---|---|
| U-01 | Obligation owner | What do I owe this week? | Copilot in SharePoint, or My obligations | No | 1 min |
| U-02 | Contract manager | Which contracts auto-renew in the next 120 days? | Copilot | No | 2 min |
| U-03 | Contract manager | Prepare for the Fabrikam renewal call | Copilot, or Contract 360 | No | 3 min |
| U-04 | Obligation owner | Mark the Contoso insurance certificate fulfilled with evidence | Quick step or Cowork | Yes | 2 min |
| U-05 | Contract manager | Remove a routine clause; confirm capture won't re-add it | Quick steps | Yes | 5 min |
| U-06 | Contract manager | Upload an amendment; confirm the base obligations are superseded | Contracts library + Copilot | Yes | 5 min hands-on, 15 min elapsed |
| U-07 | Leader (CFO) | Find everything Woodgrove can call a default on | Copilot | No | 3 min |
| U-08 | Contract manager | Explain why items were held for review | Copilot, or Review queue | No | 2 min |
| U-09 | Leader | Show exposure by counterparty | Leadership page, or Copilot | No | 2 min |
| U-10 | Obligation owner | What does Proseware owe us, and is anything late? | Copilot | No | 1 min |
| U-11 | Site owner | Which obligations have no owner, and what rule would cover them? | Copilot | No (asks first) | 3 min |
| U-12 | Site owner | Check the lists still match the skills' field names | Cowork | No (asks first) | 3 min |
| U-13 | Obligation owner | Draft the Contoso non-renewal notice; don't send | Cowork | Draft only | 4 min |
| U-14 | Leader | What's overdue and who owns it? | Copilot, or Home | No | 1 min |
| U-15 | Obligation owner | Mark the Litware true-up fulfilled with a past date | Cowork or quick step | Yes | 2 min |

"Time target" is the tester's time from typing the prompt to having a usable answer, including reading it. Agent response time over 60 seconds for a read-only question costs points under Effort.

---

### U-01 · Obligation owner · "What do I owe this week?"
- **Setup:** S0. **Prompt:** `What do I owe this week?` Click path: site navigation → My obligations, then add `#owner=<your name>` to the address (the page can't tell who is signed in), or the Obligations view "My obligations".
- **Expected (`tasks.U-01`):** open, confirmed items where we owe (Party Us or Both), overdue or due by 2026-12-01, overdue first:
  - Overdue: Submit initial marketing plan to Tailspin (04 §4.2, 2026-09-29, 56 days); Deliver updated BCP/DR plan to Contoso (02 §5, 2026-10-31, 24 days); Deliver insurance endorsements to Woodgrove (11 §5.1, 2026-11-14, 10 days).
  - Due 2026-12-01: Send non-renewal notice to Contoso (120 days) (02 §2, Both, High); Pay Fabrikam monthly hosting fees (03 §3.2); Pay monthly base rent to Alpine Ski House (07 §2.1); Pay monthly interest on Woodgrove advances (11 §2.2).
  - A footnote that 19 of your open items are event-driven or ongoing (no date). Optional: Proseware's initial SOC 2 report is overdue on *their* side.
- **Pass:** all 7 items with the right dates and clauses; nothing held, superseded or owed only by a counterparty listed as yours. A calendar-week reading (Mon–Sun) is acceptable only if stated, and caps Correctness at 3.
- **Watch for:** the superseded 90-day Contoso deadline (2026-12-31); overdue items dropped because "this week" was read as future only; dates invented for event-driven items; Proseware's report listed as ours.

### U-02 · Contract manager · "Which contracts auto-renew in the next 120 days?"
- **Setup:** S0. **Prompt:** `Which contracts auto-renew in the next 120 days, and what's the last day to give notice?`
- **Expected (`tasks.U-02`):** window 2026-11-24 to 2027-03-24.
  - **Contoso MSA**: auto-renews; non-renewal notice due **2026-12-01** (120 days, Amendment No. 1 §2 replacing MSA §9.2); the current term ends 2027-03-31 and the next one-year term starts 2027-04-01. The renewal date itself is 7 days outside the window; the notice deadline is inside it, which is what matters.
  - **Litware support**: auto-renews but **outside** the window (notice by 2027-09-07, next Support Year 2027-11-06). Should be excluded or clearly marked as later.
  - Good answers also flag the other decisions in the window: Alpine Ski House lease option closes 2026-12-30; Adventure Works expires 2026-12-31 with no auto-renewal; Fabrikam transition request by 2027-01-30; Contoso fee-increase notice by 2027-01-31.
- **Pass:** Contoso with 2026-12-01 and the clause; Litware not presented as due in the window; no non-auto-renewing contract called auto-renewing.
- **Watch for:** 2026-12-31 or 90 days (the superseded MSA term, `wrongValues`); "no contracts renew in 120 days" with no mention of the notice deadline; Adventure Works described as auto-renewing.

### U-03 · Contract manager · "Prepare me for the Fabrikam renewal call"
- **Setup:** S0. **Prompt:** `Prepare me for my Fabrikam renewal call: key terms, deadlines and open items.` Click path: site navigation → Contract 360 → Fabrikam.
- **Expected (`tasks.U-03`):** Cloud Hosting Services Agreement, supplier agreement, effective 2024-04-01, **expires 2027-03-31 (127 days)**, **does not renew automatically** (§6.2: renewal only by a signed written agreement before expiry), $38,500 a month, $1,386,000 over the term, New York law. Deadlines: next fee payment 2026-12-01 (§3.2); **transition-assistance request by 2027-01-30** (§6.3: at least 60 days before expiry, up to 90 days of help); renewal decision by 2027-03-31 (§6.2). Undated: claim service credits within 30 days after a bad month (§4.3, ours); Fabrikam's 99.9% uptime (§4.1) and 60-day notice with a 5% cap on price increases (§3.3), both theirs.
- **Pass:** both deadlines with clauses; no auto-renewal claim; party right on all six items; a brief a person could take into the call.
- **Watch for:** a non-renewal notice deadline invented by analogy with Contoso; the transition window omitted; Fabrikam's duties shown as ours.

### U-04 · Obligation owner · "Mark the Contoso insurance certificate fulfilled with evidence"
- **Setup:** S0. **Click path:** Obligations → "Maintain insurance; send Contoso COI by Dec 15" → quick step **Mark fulfilled** → paste the evidence link. Or in Cowork: `Mark the Contoso insurance certificate obligation fulfilled. Evidence: <link>.`
- **Expected (`tasks.U-04`):** that item (01 §7.1, due 2026-12-15) becomes Fulfilled, FulfilledOn 2026-11-24, Evidence = the link, Timing Closed. One successor: due **2027-12-15**, CaptureKey `<key>#2027-12-15`, Status Not started, Notes "Next occurrence after #<ID>", owner and risk copied, evidence empty. One Run Log row, Workflow Mark fulfilled, ItemsUpdated 1, ItemsCreated 1. One-line confirmation naming the next due date.
- **Pass:** exactly those writes (compare the other 59 items before and after with `compare_states.py`); no question asked beyond evidence when the link was given.
- **Watch for:** successor on the wrong date (2027-12-14, 2027-12-24); a second successor after the next sweep; other items touched; the Evidence field left empty although a link was given.

### U-05 · Contract manager · "Remove a routine clause and confirm capture won't re-add it"
- **Setup:** S0 plus one planted item: create the Obligations item in `tasks.U-05.plantedItem` (Fourth Coffee §2.1 "Designate a point of contact", CaptureKey `10-…docx|Section 2.1|designate-contact`).
- **Steps:** select it → quick step **Remove obligation** → answer `All contracts`, `routine admin`, `Yes`. Then Contracts → `10-Fourth-Coffee-Facilities-Services-Agreement.docx` → quick step **Re-capture obligations**. Then ask `Will capture add the Fourth Coffee point-of-contact clause back?` Finally repeat the removal request for the same clause in chat.
- **Expected (`tasks.U-05`):** one Exclusions row: Scope All contracts, Category Other, Active Yes, Pattern a one-sentence generalisation plus `Example: "Each Party shall designate a point of contact…"`. The item: Not applicable, Timing Closed, Notes starting "Excluded:". After re-capture: Fourth Coffee has exactly 2 open items (termination-for-convenience notice §4.2; food-safety certificate §3.2, due 2027-03-01); no open §2.1 item; the Capture row's Details lists the excluded clauses (§1.4, 2.1, 2.2, 2.3, 2.5, 5.1). The answer to the question is "No", citing the exclusion. The repeat reuses the exclusion (still 1 row).
- **Pass:** all of the above; three Run Log rows (Exclude, Capture, plus nothing for the repeat or an Exclude row with ItemsCreated 0).
- **Watch for:** the item deleted rather than set Not applicable; a duplicate exclusion; other matching items changed by the quick step (it must change only the selected item); §2.1 back after re-capture.

### U-06 · Contract manager · "Upload an amendment and confirm the base obligations are superseded"
- **Setup:** a site with only `01-Contoso-MSA.docx` captured, so 01 §9.2 (non-renewal, 90 days, due 2026-12-31) and §4.3 (quarterly report, 15 days, due 2027-01-15) are open.
- **Steps:** upload `02-Contoso-MSA-Amendment-1.docx` to Contracts, set **Amends** = `01-Contoso-MSA.docx` and Sample data = Yes. Wait for the Capture new contracts workflow (or run Re-capture on 02). Ask `What changed for Contoso after Amendment 1?`
- **Expected (`tasks.U-06`):** 01 §9.2 and §4.3 become Not applicable, Timing Closed, Notes "Superseded by 02-Contoso-MSA-Amendment-1.docx Section 2" and "… Section 3". Four new items under 02: non-renewal notice 120 days due **2026-12-01** (Both, High); quarterly service-level report due **2027-01-10**; fee-increase notice due 2027-01-31 (adds MSA §3.4); BCP/DR plan due 2026-10-31 (overdue). Run Log: Capture row for 02 with ItemsCreated 4, ItemsUpdated 2, ItemsHeld 0; one extra Capture row Skipped "content unchanged" is normal (the Amends edit fires "file changed"). The chat answer names the old and new deadlines.
- **Pass:** state as above; no open item carries 2026-12-31 or 2027-01-15; `compare_states.py` against a state captured in the other order shows IDENTICAL (S-10).
- **Watch for:** both versions open (duplicate notice); the base items deleted; the "Superseded by" note added twice; the amendment's §2 captured with the 90-day value.

### U-07 · Leader (CFO) · "Find everything Woodgrove can call a default on"
- **Setup:** S0. **Prompt:** `Find everything Woodgrove can call a default on, and what's most urgent.`
- **Expected (`tasks.U-07`):** grounded in Woodgrove §6.1 (quote in `quote61`), mapped to the 7 tracked items:
  - (a) non-payment of principal or interest within 3 Business Days after due: monthly interest (§2.2, next 2026-12-01); repayment at maturity (§2.3, 2029-09-15).
  - (b) breach of §4.1, no cure period: minimum Liquidity of $5,000,000 at all times.
  - (c) breach of Article 3 or 5 continuing 15 days after the Bank's notice: quarterly compliance certificate (§3.1, next 2027-02-14); annual audited financials (§3.2, 2027-10-28); notice of default within 5 Business Days (§3.3, on the event); insurance endorsements (§5.1).
  - (d) a materially incorrect representation: no tracked obligation.
  - **Most urgent:** the §5.1 endorsements were due 2026-11-14 and are **10 days overdue**; they become an Event of Default 15 days after the Bank gives notice. Remedies (§6.2): the Bank may end the commitment and accelerate all advances.
  - Not a default: the closing fees (§2.4) were a condition met at closing.
- **Pass:** all 7 items in the right limb; the overdue endorsements flagged first; §6.1 cited or quoted; cure periods exactly as written.
- **Watch for:** invented cure periods or grace days; liquidity omitted (it's undated); the closing fees called overdue; "no defaults" because nothing is past due *today* except 5.1.

### U-08 · Contract manager · "Explain why items were held"
- **Setup:** S0. **Prompt:** `What's waiting for review, and why was each item held?` Click path: site navigation → Review queue.
- **Expected (`tasks.U-08`):** 3 items, each Confidence Low, because its terms sit in a document that isn't in the Contracts library:
  - Tailspin §3.3 "Pay Tailspin per dealer credit application terms" (ours, payment): the **dealer credit application**.
  - Proseware §7 "Return or delete personal data at termination" (theirs): the **Services Agreement, Section 11.4**.
  - Adventure Works §2.2 "Pay per standard credit terms" (theirs): Northwind's **standard credit terms**.
  - Next step for each: add the document to Contracts and re-capture, or confirm the terms and set Review to Confirmed. Held items aren't assigned or reminded until confirmed.
- **Pass:** 3 of 3 with the right missing document; the next step stated.
- **Watch for:** guessed payment terms; "held because of low confidence" with no reason; held items described as tracked and assigned.

### U-09 · Leader · "Show leadership exposure by counterparty"
- **Setup:** S0. **Click path:** site navigation → Leadership → "By counterparty". Or prompt `Show leadership exposure by counterparty.`
- **Expected (`tasks.U-09`):** 58 open items, **13 High (22%)**, 4 overdue, 3 held. By counterparty (open / High / overdue): Woodgrove Bank 7/4/1; Contoso Ltd 10/2/1; Fabrikam Inc 6/2/0; Tailspin Toys 7/1/1; Proseware Inc 6/1/1; Adventure Works Cycles 5/1/0; Alpine Ski House 5/1/0; Litware Inc 5/1/0; Wide World Importers 5/0/0; Fourth Coffee 2/0/0. Next deadline per counterparty is in the file.
- **Pass:** counts match (the page or answer may also split "we owe" and "they owe"); Woodgrove and Contoso called out; says plainly that dollar exposure and trends aren't available (a known gap).
- **Watch for:** invented dollar amounts or trend arrows; superseded or excluded items counted; held items missing.

### U-10 · Obligation owner · "What does Proseware owe us, and is anything late?"
- **Setup:** S0. **Prompt:** `What does Proseware owe us, and is anything late?`
- **Expected (`tasks.U-10`):** 5 items owed by Proseware: initial SOC 2 Type II report, **due 2026-10-01, 54 days late** (§6.1); annual SOC 2 report by 2027-10-01 (§6.2); breach notice within 48 hours of a personal data breach (§4.1); 30 days' notice before a new sub-processor (§5.2); return or delete personal data at termination (§7, **held**: terms in the missing Services Agreement).
- **Pass:** 5 of 5, the late report flagged with its date, the held item flagged as unconfirmed.
- **Watch for:** our own 15-day objection right (§5.3) listed as theirs; the breach notice given a date.

### U-11 · Site owner · "Which obligations have no owner?"
- **Setup:** load the sample, but before Assign owners runs, delete the Default rule and add one rule "Finance - payments" (Category Payment → tester). Run Assign owners once (`assign owners` in chat, or the 7:00 AM run).
- **Prompt:** `Which obligations have no owner, and what rule would cover them?`
- **Expected (`tasks.U-11`):** 11 payment items were assigned; **44** confirmed open items have no owner: Compliance & audit 13, Notice & renewal 9, Data & confidentiality 4, Purchasing & volume 4, Reporting 4, Service levels 4, Insurance 3, Other 3. The 3 held items are unassigned by design. Suggests an Any/Any default rule (or per-category rules) and creates nothing until the user agrees.
- **Pass:** count and breakdown right; held items explained separately; asks before writing.
- **Watch for:** creating rules unasked; counting held items as needing an owner; payments listed as unowned.

### U-12 · Site owner · "Check the lists still match the skills' field names"
- **Setup:** S0 plus three planted changes (`tasks.U-12`): delete the Obligations view "Triggered and ongoing"; remove the choice "Semi-annual" from Recurrence; rename the Timing column's display name to "When".
- **Prompt (Cowork):** `Check the Obligation Hub lists on <site> still match the skills' field names and views.`
- **Expected:** reports the missing view and the missing choice as problems (with their impact), and the rename as harmless because the internal name `Timing` is unchanged. Offers a repair (setup-obligation-hub only adds what's missing) and changes nothing without approval. `check_schema.py` on a fresh dump shows the same two FAILs.
- **Pass:** exactly the two problems, the rename classed harmless, no unapproved write.
- **Watch for:** the rename reported as breaking; the missing choice not noticed; "fixing" by deleting or recreating the list.

### U-13 · Obligation owner · "Draft the Contoso non-renewal notice; don't send"
- **Setup:** S0, Cowork with Outlook. **Prompt:** `Draft the non-renewal notice for Contoso from the contract and save it as a draft for my review. Don't send it.`
- **Expected (`tasks.U-13`):** an Outlook **draft**, not sent, saying Northwind elects not to renew the Master Services Agreement (No. NW-MSA-2024-0117) under §9.2 as amended by Amendment No. 1 §2, so it ends with the Renewal Term on **2027-03-31**; the notice must be received by **2026-12-01**. It points out that §10.2 requires delivery **by courier or certified mail** to Contoso Ltd, 1 Contoso Plaza, Redmond, Washington 98052, with a copy by email to contracts@contoso.example (Contracts Office, Global Procurement, per Amendment Exhibit B), so the email alone isn't valid notice. Signature left for the user.
- **Pass:** draft only; right clause, dates and delivery method; the user told what's left to do.
- **Watch for:** the email sent; the 90-day period or 2026-12-31; email presented as sufficient notice; invented signatories.

### U-14 · Leader · "What's overdue and who owns it?"
- **Setup:** S0. **Prompt:** `What's overdue and who owns it?` Click path: site navigation → Home → At a glance → Overdue.
- **Expected (`tasks.U-14`):** 4 items, by risk then days overdue: Submit initial marketing plan to Tailspin (Medium, 56 days); Deliver updated BCP/DR plan to Contoso (Medium, 24 days); Deliver insurance endorsements to Woodgrove (Medium, 10 days); Obtain Proseware's initial SOC 2 report (Low, 54 days, Proseware's to deliver: we chase). Owner: the tester for all four.
- **Pass:** 4 of 4 with days overdue and owner; the Proseware item marked as theirs.
- **Watch for:** items due 2026-12-01 counted as overdue; the Proseware report shown as ours; owners invented. Noting that the Woodgrove endorsements can become an Event of Default is a plus, not required.

### U-15 · Obligation owner · "Mark the Litware true-up fulfilled with a past date"
- **Setup:** S0. **Prompt:** `I sent the Litware true-up report on Nov 20. Mark it fulfilled; evidence: <link>.`
- **Expected (`tasks.U-15`):** "Submit annual Named User true-up report to Litware" (05 §3.2, due 2026-12-06) → Fulfilled, **FulfilledOn 2026-11-20** (not today), Evidence = link; successor due **2027-12-06** (30 days after the 2027-11-06 anniversary); no question asked (date and evidence were given); one Run Log row.
- **Pass:** dates exact, zero follow-up questions, one successor.
- **Watch for:** FulfilledOn = today; successor 2027-11-06 (anniversary instead of anniversary + 30); asking for evidence again.

## Recording results

Use the CSV and table templates in [RUBRIC.md](RUBRIC.md#results-template). Keep the raw answers: the judge and the human spot-checker both need them.
