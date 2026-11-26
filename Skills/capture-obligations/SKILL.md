---
name: capture-obligations
description: Reads one contract in the Contracts library of an Obligation Hub site and creates or updates its obligations in the Obligations list, each with the source clause quoted, a due date or trigger, risk and a review state. Handles amendments, exclusions, missing referenced documents and repeat runs, and writes one Run Log row. Use when a contract is added or changed (the two Capture AI workflows), from the Re-capture obligations quick step, or when asked to "capture obligations from this contract" or "re-capture".
license: MIT
metadata:
  solution: obligation-hub-for-sharepoint
  version: "1.0.0"
---

# Capture obligations

Turn one signed contract into register rows: who owes what, by when, upon what. The output is a **contract-management register, not a service-delivery checklist**. Runs unattended (file added or changed) or in chat. Save without asking. This is an unofficial community sample, not a Microsoft template, and it doesn't give legal advice: it records what the contract says.

## Inputs
- **The contract**: the triggering, selected or named file. `ContractName` = its file name with extension.
- **Config** `AgentAssets/Config/hub-settings.json`: `ourCompany`, `siteUrl`, `timeZone`, `dueSoonDays`, `captureHoldBelowConfidence`. If it's missing or has no `ourCompany`, log Failed ("hub-settings.json missing") and stop.
- **Contracts library**, read once when the run starts; related files are judged against this snapshot only. For this file: `Title`, `Counterparty`, `ContractType`, `EffectiveDate`, `ExpirationDate`, `AutoRenews`, `NoticePeriodDays`, `Amends`, `BusinessUnit`, `IsSample`. Autofill may still be empty; the text wins over the columns.
- **Obligation Types**: all rows.
- **Exclusions**: rows where `Active` = Yes and either `Scope` = All contracts, or `Scope` = This contract and `ContractName` = this file (for an amendment, also its base).
- **Obligations**: items whose `ContractName` is this file or a related file.
- **Run Log**: the latest row where `Workflow` = Capture, `ContractName` = this file and `Outcome` = Succeeded or Partial.

"Today" is the current date in `timeZone`. Write every date, in fields and in text, as YYYY-MM-DD.

## Steps

### 1. Gate
1. Folders, non-documents and files that aren't a contract, amendment or contract exhibit: log Skipped ("not a contract") and stop.
2. Read the full text. Find the **related files** (step 2): this file's base and its amendments.
3. **Fingerprint** = `<W>~<R>`, for example `1439~02-Contoso-MSA-Amendment-1.docx`.
   - W = the body text's word count: whitespace-separated tokens containing a letter or digit (not separators like "|"), table cells included, headers and footers ignored. Use a code step if available.
   - R = the related file names, sorted, joined by "," (empty if none).
4. **Skip check.** A manual "Re-capture obligations" request, or any request to capture or re-capture, always runs in full. Otherwise log Skipped ("content unchanged") and stop if the Run Log row's `ContractVersion` has the same fingerprint, or the same R and a W within 0.5% (extractors differ). A value in another format never matches. Column edits (autofill) leave the fingerprint unchanged; small in-place edits may be skipped too: re-capture those.

### 2. Context
- **Parties.** Map each defined role (such as "Licensee") to `ourCompany` or the counterparty. Counterparty name = the `Counterparty` column, else the legal name in the parties block (for an amendment, the base's).
- **Term facts.** Effective date, current term end, renewal length, auto-renewal, notice periods, fiscal year end. Roll an auto-renewing term end forward until the next deadline is on or after today.
- **Base.** This file amends another if `Amends` is set, `ContractType` = Amendment, or the text amends, deletes or replaces clauses of an agreement. The base is the `Amends` value, else the Contracts file with the same counterparty and a matching agreement name, number or date. Read it for unchanged terms such as the term end. A supplement, DPA, SOW or order under a master agreement is **not** an amendment; the master is an incorporated document. If the base isn't in the library, capture the amendment alone and treat the base as a missing document (step 5).
- **Amendments of this file.** Contracts items where `Amends` = this file, or `ContractType` = Amendment with a matching `Counterparty`, or whose file name or `Title` contains "Amend" plus this agreement's name or counterparty. Confirm the last two kinds from the opening paragraph, then read them. The base clauses they delete or replace are **superseded** (step 7).
- **Incorporated documents** (exhibits, SOWs, schedules, a supplement's master). If in the library, read only the parts the clauses point to; never guess a missing one's terms (step 5).

### 3. Discover
Walk every numbered clause sentence by sentence, plus exhibits or annexes with operative terms. A sentence is a candidate if it contains *shall, must, will, agrees to, shall not, may … by notice, within N days, at least N days before, on or before, no later than, each month/quarter/year, upon, if … then*. The title, parties block, recitals, definitions, headings, signature blocks, examples and illustrations never create an item; they may only confirm a date.

### 4. Classify
Give each candidate a **kind**:
- **Duty or prohibition**: to the guardrails.
- **Permission**: keep only if
  - (a) it controls the contract's life: non-renewal, a renewal or extension option, termination for convenience, a transition-assistance request, or a fee increase allowed only with notice;
  - (b) a deadline forfeits our right or money: a credit-claim window, defect notice, objection period or option window; or
  - (c) it's a counterparty right that creates a duty for us (their audit right → our duty to cooperate).

  Don't track termination for cause or after an event, remedies, prepayment, license grants and their scope ("solely to advertise…"; a *shall not* is a prohibition), or discretionary rights with no deadline (our own audit right, sharing feedback).
- **Financial mechanism** (rates, caps, late charges, credit amounts, shortfall remedies): merge into the obligation it modifies, in `ObligationText`. A service credit someone must act on (issue it, or claim it in a window) is that party's own item with the amounts merged in; automatic credits merge into the service level.
- **Fact-or-status**: context only. Representations; present-tense statements without *shall, must* or *will* ("X holds a permit", unlike "X shall maintain insurance"); term statements; anything done at or before signing (fees or deposits paid on execution, conditions to effectiveness).
- **Unclear**: hold it.

**Merge and split.** One item per distinct action plus trigger.
- Merge sub-clauses that only describe content, format or method.
- A standing duty plus its proof is one item dated by the proof (maintain insurance and deliver a certificate yearly).
- Mutual duties of the same kind in one clause: one item, `Party` = Both.
- An obligation in both a clause and an exhibit table: capture it once.

### 5. Guardrails
**EXCLUDE: routine execution and administration**
- Contacts, notice addresses, invoice addresses, invoicing logistics, issuing our own routine invoices
- "Cooperate / act in good faith" and general conduct
- Service descriptions, support hours, security-measure tables, general standards with no trigger, date or deliverable ("responsible for its personnel")
- Uniforms, badges, site access, hours, permitted use, house rules; routine orders, returns, support procedures
- Boilerplate: headings, interpretation, counterparts, e-signature, own costs, governing law, tax allocation, liability caps, assignment consent, entire agreement, severability, force majeure, survival, waivers

**PROTECT: track these even if they look routine**
- **Payment:** what we pay or are paid and when, price or fee-change notices and caps, rebates, fund contributions, true-ups, minimum commitments, repayment.
- **SLA governance:** measurable service levels, issuing or claiming credits, service-level reports.
- **Reporting:** periodic and conditional reports, financial statements, compliance certificates.
- **Insurance and certificates:** maintaining insurance; COIs, endorsements, SOC reports, inspection certificates.
- **Audits:** our duty to cooperate.
- **Event notices:** data breach, default, change of control, discontinuation, sub-processors.
- **Key personnel:** notice or approval before replacing named people.
- **Windows:** renewal, non-renewal, termination-for-convenience, option and transition-request windows; post-closing deliverables.
- **Standing restrictions:** exclusivity, non-compete, license-use limits, most-favoured pricing, financial covenants, confidentiality, data protection (including data return and deletion).

**FALSE MATCHES: never track**
- Cross-references that only restate or point to another clause or document (but see Missing document)
- Duties of people who aren't party to the contract

**Missing document.** If a PROTECT obligation's operative terms sit in a referenced document missing from the Contracts library (payment terms "per the dealer credit application"), create ONE held item: `Confidence` = Low, `ReviewState` = Needs review, `Notes` = "Terms in <document>, which isn't in the Contracts library — add it or confirm the terms". Leave `DueDate` empty; `TriggerType` = Event-driven if the text names an event, else Ongoing. Pure cross-references on non-protected matters, and references to clauses that don't exist, stay untracked: note them in Details.

**Precedence** when rules conflict: active Exclusion > protected-control rule > type `Handling` > the other guardrails (EXCLUDE, FALSE MATCHES, step 4 kinds).
1. An active Exclusions match removes the item, protected or not.
2. Protected-control rule: no type or guardrail excludes a PROTECT obligation; if an Exclude type covers only a clause's routine part, keep the protected part. Missing-document terms → the held item above.
3. Type `Handling`: Exclude → exclude; Hold for review → hold (protected items too, and it beats FALSE MATCHES such as third-party duties); Track → keep, subject to the checks below.

**Retain, hold or exclude.** Retain an item only if it has: (1) who owes it, (2) the action, (3) the trigger, the date or "ongoing", (4) the clause reference, (5) the verbatim source sentence, (6) the category, and (7) no exclusion. If 1, 2, 3 or 5 fails, **hold** it (Low) with the reason; never paraphrase in place of a quote. If 7 fails, **exclude** it: don't write it, list it in Details.

### 6. Fields
- `Title`: ≤ 80 characters, with the deadline cue.
  - Party Us or Both: verb first. "Send non-renewal notice to Contoso (120 days)".
  - Party Counterparty: "<Counterparty>: <verb …>". "Proseware: notify data breach within 48 hours".
- `ObligationText`: 1–2 plain sentences: who, what, by when or upon what, and the consequence if stated. Recurring items state the schedule ("within 10 days after each calendar quarter end"). In a fixed-term contract that doesn't renew automatically, end Ongoing and Recurring items with "Through <term end>." — or "Survives expiry." where a survival clause applies, plus "Last due <date>." if Recurring. Other items get neither.
- `ClauseRef`: the document's own label ("Section 4.3"). For an amendment, add what it changes: "Section 2 (amends MSA Section 9.2)" or "Section 4 (adds MSA Section 3.4)".
- `SourceClause`: the operative sentences verbatim, one contiguous span, without the number or caption.
- `Party`: Us = `ourCompany` must act; Counterparty = the other side must act (we monitor and chase); Both = either party may act, or each must.
- `Category`: the matched type's `Category`, else the best fit among Payment, Reporting, Notice & renewal, Compliance & audit, Service levels, Insurance, Data & confidentiality, Purchasing & volume, Other.
- `TriggerType`:
  - Fixed date: one-time.
  - Recurring: a fixed schedule. A payment is Recurring only if both the invoice date and the payment period are fixed ("invoiced on the 1st, due in 30 days"); "45 days after receipt of each invoice" is Event-driven.
  - Event-driven: waits for an event (each delivery, a breach). `DueDate` is empty; `TriggerEvent` = the event in plain words; the response time goes in `ObligationText`.
  - Ongoing: in force throughout the term. `DueDate` and `TriggerEvent` are empty.
- `Recurrence`: None unless `TriggerType` = Recurring; then Weekly, Monthly, Quarterly, Semi-annual or Annual (if the clause doesn't say, the type's `DefaultRecurrence`).
- `DueDate`: the next unfulfilled occurrence.
  - "Within N days after X" = X + N calendar days; business days (Mon–Fri) only if the clause says so. "At least N days before X" = X − N; for a notice window, the last day notice can be given.
  - N months before or after X = the same day-of-month N months earlier or later, or that month's last day if the day doesn't exist.
  - A date stated in operative text (including an amendment's "for clarity" date) wins over arithmetic; exhibits or examples the contract calls illustrative or "for convenience" only confirm. On a disagreement, use the operative text, set Medium and explain in `Notes`.
  - Recurring: the next occurrence on or after today; earlier ones are assumed done. If the contract or amendment took effect within the last 12 months and an occurrence has passed, append to `Notes`: "Earlier occurrence <date> not tracked; confirm it was done." Capture never rolls items forward; `mark-obligation-fulfilled` and `sweep-obligations` do.
  - Fixed date: keep it even if passed (it shows Overdue).
  - Option window with an opening date: `DueDate` = the closing date; `Notes` = "Window opens <date>; notice before then is invalid."
- **Fixed expiry.** If the term ends on a date without automatic renewal and expiry is within 12 months of today, add one item: "Decide on <counterparty> renewal before <date> expiry", Party Both, Notice & renewal, Fixed date, `DueDate` = the expiry date, Risk High. `ClauseRef` = the term clause stating there's no automatic renewal (else the one stating expiry); `SourceClause` = its term sentences verbatim; slug `decide-renewal`. Skip it if this contract has a renewal or extension option-window item (any run); a transition-assistance window doesn't count.
- `Confidence`:
  - High: actor, action and timing are explicit in the clause or the parties block (defined roles, stated recurring schedules and dates computed from an explicit rule count).
  - Medium: the timing or actor was inferred from another clause or merged clauses, or a stated date disagrees with arithmetic.
  - Low: the actor or action is ambiguous (including duty versus right), the terms are in a missing document or conflict, or the text is unreadable.
- `ReviewState` = Needs review if the item is held, `Confidence` is Low or below `captureHoldBelowConfidence` (default Medium), or `Handling` = Hold for review; otherwise Confirmed. Held items get `Notes` = "Held for review: <reason>" unless the missing-document note applies.
- `Risk`: set by consequence, meaning what happens if the item is missed.
  - **High**: missing it automatically loses a right or money, or starts a legal clock. That covers notice, renewal and option deadlines we must act on; change-of-control and breach notices; and financing covenants, compliance certificates and default notices.
  - **Medium**: other dated or money obligations: payments, reports, certificates and audits.
  - **Low**: ongoing conduct, and counterparty duties we only monitor (other than payments and data).
  - This rule decides. The type's `DefaultRisk` only settles an item the rule leaves open. A counterparty's miss that only gives us a remedy doesn't raise the risk.
  - Expect roughly 15–30% of open items to be High. If more than a third of the open items this run writes come out High, re-check each High item against the rule before writing.
- `Timing`: Closed if `Status` is Fulfilled, Waived or Not applicable; No date if there's no `DueDate`; Overdue if `DueDate` < today; Due soon if within `dueSoonDays` (default 14); otherwise Upcoming. `sweep-obligations` keeps it current.
- `CaptureKey` = `<file name>|<ClauseRef>|<slug>`. The slug is 2–4 lowercase hyphenated words, verb then object (`send-non-renewal-notice`, `deliver-coi`). Keep it stable across runs.

### 7. Amendments
The final state must be the same whichever file is captured first, or if both are present at the first run. A **superseded clause** is a base clause an amendment deletes or replaces; its base item is the base file's item with that `ClauseRef`. The note is "Superseded by <amendment file> <clause>".
- **Base item open** (`Status` = Not started or In progress): set `Status` = Not applicable, `Timing` = Closed and `ReviewState` = Confirmed, and append the note (updated).
- **Base item already Not applicable with this note**: no change; not counted.
- **Base item closed otherwise** (Fulfilled, Waived, or Not applicable without this note): append the note only (updated).
- **Capturing the base and the item doesn't exist**: create it already superseded (the values and note above).
- **Capturing the amendment and the base item doesn't exist**: nothing to do; the base's capture creates it superseded.

Amended and added obligations go under the amendment's file name, with the amended terms plus unchanged base terms; never track a pre-amendment value. Untouched base clauses stay with the base.

### 8. Upsert
Match each extracted item to an existing item of this contract, in order:
1. The same `CaptureKey` series: the key, or key + "#…" (a rolled-forward occurrence).
2. The same `ClauseRef` and `SourceClause`, ignoring whitespace.
3. The same `ClauseRef`, party and action.

On a match, keep the existing `CaptureKey`. Items with an empty `CaptureKey` are people's: never change or duplicate them.
- **New → create** with the fields above, plus `ContractName`; `ContractLink` = the file URL (description = the file name); `Counterparty`; `Status` = Not started; `BusinessUnit` = the Contracts item's `BusinessUnit`; `IsSample` = the contract's `IsSample`. Leave `Owner`, `EscalationOwner`, `FulfilledOn`, `Evidence` and `LastReminded` empty.
- **Update** when the match's source or terms changed, on the series' open item only: `Title`, `ObligationText`, `ClauseRef`, `SourceClause`, `DueDate`, `Recurrence`, `TriggerType`, `TriggerEvent`, `Category`, `Party`, `Counterparty`, `ContractLink`, `Confidence` and `Timing`. Recompute `DueDate` only from changed terms; never move an open item's date because time passed.
- **Unchanged**: skip.
- **No longer found**: an open item whose `CaptureKey` starts with "<file name>|", that isn't superseded and that nothing matched. Set `ReviewState` = Needs review and append "No longer found in latest version (<today>)" to `Notes`, once per item.

Just before writing, re-read the Obligations of this contract (and, for an amendment, its base): a parallel run may have written items. Drop any create whose key now exists, and supersede base items that just appeared. Write in batches.

### 9. Log, then report
Write one Run Log row:
- `Title` = "Capture - <file>"
- `Workflow` = Capture
- `Outcome`: Succeeded; Partial (some writes failed); Failed (couldn't read the file, or no write succeeded); Skipped (unchanged or not a contract)
- `ContractName`, and `ContractVersion` = the fingerprint
- `ItemsCreated`; `ItemsUpdated` (includes superseded and no-longer-found items); `ItemsHeld` = items this run created or updated that are now in Needs review
- `RunAt` = now
- `Details` (≤ 1,000 characters), e.g. "Retained 6 (Us 4, Counterparty 1, Both 1); held 1: 3.3 terms in dealer credit application; excluded 6: 1.4 uniforms, 2.1 contacts…; superseded: <base> §9.2; missing documents: …; errors: …". If `Amends` is empty but the text amends a file, add "set Amends to <base file>".

**In chat only**, finish with one compact table (Obligation | Party | Due or trigger | Clause | Review), the line "Created X, updated Y, held Z, excluded N." and "Owners are assigned by the Assign owners workflow each morning, or say 'assign owners for <contract>'." (That request runs `assign-obligation-owners`.) Don't narrate the steps.

## Writes
- Obligations: creates, and updates only to the fields named in steps 7–8.
- Run Log: exactly one row per run, including Skipped and Failed runs.

## Never
- Write to the Contracts item or file (any write retriggers capture), Obligation Types, Exclusions or Obligation Owners.
- Delete obligations, or overwrite `Owner`, `EscalationOwner`, `BusinessUnit`, `Status` (except when superseding), `FulfilledOn`, `Evidence`, `LastReminded` or `Risk` on existing items. Notes are append-only.
- Invent dates, amounts, clause numbers or quotations.
- Send email or Teams messages.
