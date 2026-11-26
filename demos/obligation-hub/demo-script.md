# Obligation Hub for SharePoint: recorded overview demo script

**Presenter:** Zach Rosenfield · **Format:** recorded overview video (YouTube / LinkedIn), target runtime 9:35 · **Site:** https://microsoft.sharepoint-df.com/sites/zachobligationdemo · **Company in the data:** Northwind Traders, Inc. (fictional) · **"Today" in the data:** Tuesday, November 24, 2026

Files in this folder: `demo-script.md` (this kit), `prompt-only.md` (setup and live prompts only), `12-Relecloud-Order-Form.docx` (the contract dropped in on camera), `expected-obligations.md` (what capture should make of it), `Northwind-COI-Contoso-2026.docx` (the evidence given in beat 4), `make_demo_contract.py` (builds and verifies those three), `talk_timing.py` (speaking-time estimate for section 5).

## Assumptions

Decided without Zach's confirmation. Change any of them and the sections that depend on them are named.

1. **Record between Wednesday, November 25 and Monday, November 30, 2026, all beats on one day.** On December 1 the hero deadline becomes Overdue and the story breaks. Numbers in this script hold for any day from November 24 to 29; on November 30 the digest's "next 30 days" section also lists the Alpine Ski House lease option (December 30). The talk track says dates, never "in 7 days", so it survives the shift. (Sections 3, 5)
2. **Zach plays the owner.** Every routing rule on the demo site routes to him, so every assigned item, digest and reminder on screen is his. No fictional owners appear on camera. (Sections 1, 5)
3. **The beat-3 contract is a new counterparty, Relecloud** (a Microsoft sample company), not Proseware. Proseware already has a DPA on the site whose held item points to a missing "Services Agreement"; a Proseware order form could be read as that document and change an existing item mid-demo. (Section 2)
4. **Skill names are the canonical v1.0 names** from the kit plan (`capture-obligations`, `assign-obligation-owners`, `sweep-obligations`, `obligation-owner-digest`, `obligation-leadership-digest`, `mark-obligation-fulfilled`, `exclude-obligation`, `obligation-hub-guide`). The talk track never says a skill name, so a site still on the old names doesn't break the script; only the Settings page shows them. (Section 3, S1)
5. **Stake framing.** Under the Contoso MSA, Northwind is the supplier and Contoso pays $45,000 a month ($540,000 a year, MSA Section 3.1). The accurate line is "renews by default": miss December 1 and Northwind is committed to another $540,000 year on the current terms, decided by the calendar rather than by anyone at Northwind. (Sections 1, 6)
6. **Beat-4 evidence is a pasted link** to the generated sample certificate. That link is the only location that appears in a live prompt; it is the evidence itself, pasted rather than typed.
7. **The kit document is this markdown file** in the repo's `demos/` folder, not a Word document in OneDrive, and the HyperFrames edit prompt is skipped, both as requested.
8. **The site's Owner and Escalation owner columns are Person columns.** The workflows need a person to message, so this departs from the demo-kit "no Person columns" rule; left as built.
9. **Availability is said on camera once** (close) and shown once as a lower third (beat 6). Zach approves the exact wording (section 7.4).

---

## 1. Story

**Arguable sentence.** You don't need a contract-management system to stop missing contract deadlines; you need every date on a named person's list, and a SharePoint site can keep that list.

**Hero item.** *Send non-renewal notice to Contoso Ltd (120 days)*, due **Tuesday, December 1, 2026**. The Contoso Master Services Agreement auto-renews each April 1. The original MSA (Section 9.2) needed 90 days' notice, which points at December 31. Amendment No. 1, signed in late August and effective September 1, 2026, replaced Section 9.2 with 120 days and says so outright: "notice of non-renewal must be given on or before December 1, 2026." The hub tracks the amended date and has closed the 90-day item as superseded.

**Stake.** Miss December 1 and the Contoso MSA renews on April 1, 2027 for another year: a $540,000 commitment made by default, not by decision. Anyone working from the original contract misses the deadline by a month.

**The one story.** A week before a deadline that moved, Northwind's contracts already sit in a SharePoint site that knows the date, who owns it and what to do next. We watch the site answer "what needs attention", take in a new contract on its own, put work in an owner's inbox, take proof when the work is done, answer questions with citations and show leadership the exposure. Then we come back to December 1.

**Cast.** Zach Rosenfield, presenter, VP of Product for SharePoint and Content AI at Microsoft. On the demo site he is also the owner of every routed obligation and the account the workflows run as. Names that appear inside the documents only: Maria Delgado (Northwind COO, signs for Northwind), Priya Raman (Northwind General Counsel, notice contact), Daniel Okafor (Northwind CFO, on the Woodgrove letter), Jordan Ellis (Relecloud VP Sales). All fictional.

**Why this needs SharePoint.** Contracts live in a library, obligations in a list with views and quick steps, each audience gets a page, and AI workflows run on file events and schedules against site skills. Nothing in the demo is a chat-only answer: the site does the work while nobody is in a chat.

---

## 2. Data

### 2.1 What's on the site before recording

Source: the 60 items loaded on the demo site (`loaded_obligations_risk.json`, with `NewRisk` as Risk), the sample answer key and the contracts manifest. All fictional.

| Fact | Value |
|---|---|
| Contract files | 11: ten contracts plus Contoso Amendment No. 1 |
| Obligations | 60 (badge "Live · 60 obligations"); 58 open; 2 Not applicable, both superseded by the Contoso amendment |
| Home hero (Nov 24 to 29) | "10 obligations need attention in the next 14 days": 4 overdue and 6 falling due in the next 14 days (the date shown moves with the recording day), "58 obligations open across 10 contracts" |
| Home tiles | Overdue **4** · Due in 14 days **6** · Needs an owner **3** · Needs review **3** |
| Needs review / no owner | The same 3 items (inferred: every routing rule points to Zach, and Assign owners skips held items), held because their terms are in documents the library doesn't have: Tailspin dealer credit application, Proseware services agreement, Adventure Works standard credit terms |
| Open by timing | Overdue 4 · Due soon 6 · Upcoming 20 · No date 28 (event-driven or ongoing: 48% of open items) |
| Open by risk | High 13 (22%) |
| Open by party | We owe 40 · Owed to us 11 · Mutual 7 |
| Notice windows (180 days) | 6 notice deadlines, the first being Contoso non-renewal, December 1, with the bracket "Contoso · 120-day notice period (amended from 90 days)" |

**Items the run order touches**

| Item | Due | Clause | Role in the demo |
|---|---|---|---|
| Send non-renewal notice to Contoso Ltd (120 days) | 2026-12-01, Due soon, High | 02-Contoso-MSA-Amendment-1.docx, Section 2 (amends MSA Section 9.2) | Hero item, beats 1, 2, 5, 6, 7 |
| Send non-renewal notice to Contoso Ltd (90 days) | 2026-12-31, Not applicable | 01-Contoso-MSA.docx, Section 9.2; Notes "Superseded by 02-Contoso-MSA-Amendment-1.docx Section 2" | Proof the hub read the amendment (beat 2) |
| Deliver certificate of insurance to Contoso Ltd by December 15 | 2026-12-15, Recurring annual, Medium | 01-Contoso-MSA.docx, Section 7.1 | Marked fulfilled with evidence (beat 4) |
| Deliver insurance endorsements to Woodgrove Bank (60 days) | 2026-11-14, Overdue, Medium | 11-Woodgrove-Bank-Revolving-Credit-Facility.docx, Section 5.1 | The live default risk in the Copilot answer (beat 5) |

**Planted patterns and clean controls.** The amendment trap (90 to 120 days) is the hero; its control is the closed 90-day item. Auto-renewal inside 120 days is Contoso (and Relecloud after beat 3); the control is Litware's support non-renewal (September 7, 2027), which auto-renews but is outside the window and must not appear in the first Copilot answer. Adventure Works expires December 31 but does **not** auto-renew, a second control for the same question. The recurring Contoso certificate is the roll-forward pattern; the overdue one-time Woodgrove endorsements are the default-risk pattern.

### 2.2 The new contract for beat 3: `12-Relecloud-Order-Form.docx`

One-page order form, written in full prose by `make_demo_contract.py`. Northwind buys a five-month pilot of Relecloud Fleet Insights (December 1, 2026 to April 30, 2027) for $36,000; it **renews automatically** into 12-month terms at **$96,000 a year** unless either party gives **60 days' notice**. It also has a one-time pilot fee, a quarterly fleet report, a 72-hour security-incident notice Relecloud owes Northwind, one payment clause whose terms are in a document Northwind doesn't have (the Relecloud Rate Card), and seven clauses that must not become obligations.

| # | Expected | Obligation | Party | Due | Risk | Clause |
|---:|---|---|---|---|---|---|
| 1 | Track | Send non-renewal notice to Relecloud (60 days) | Both | 2027-03-01 (April 30 minus 60 days) | High | Section 1.2 |
| 2 | Track | Pay Relecloud pilot fee by December 31, 2026 ($36,000) | Us | 2026-12-31 | Medium | Section 2.1 |
| 3 | Track | Send Relecloud quarterly fleet report (15 days) | Us | 2027-01-15, then quarterly | Medium | Section 3.1 |
| 4 | Track | Relecloud: notify security incident within 72 hours | Counterparty | When Relecloud becomes aware of a Security Incident | High | Section 4.1 |
| 5 | **Hold** | Pay Relecloud renewal and overage fees per Rate Card | Us | No date; Needs review, Confidence Low, "Terms in Relecloud Rate Card, which isn't in the Contracts library" | Medium | Section 2.2 |

Not created: 1.1 service description, 2.3 invoice address, 3.2 project contacts, 4.2 support hours, 5.1 entire agreement, 5.2 governing law, 5.3 counterparts. Expected Run Log row: `Capture - 12-Relecloud-Order-Form.docx`, Succeeded, Created 5, Held 1. The full table with verbatim source sentences, acceptable variations and the optional Contracts column values is in `expected-obligations.md`.

**Verification.** `python make_demo_contract.py` rebuilds both documents and runs 24 checks: every expected and excluded source sentence appears verbatim in the .docx, the date math (2027-03-01, 2027-01-15), the 120-day and 180-day windows, that no new item lands inside 14 days (so the hero stays at 10), one hold, two High items, the one-page length (545 words) and the certificate's limits. Last run: **24 of 24 passed**.

**After capture (beat 3 screen):** hero still 10; "63 obligations open across 11 contracts"; tiles Overdue 4 · Due in 14 days 6 · Needs an owner **8** · Needs review **4**; badge "Live · 65 obligations"; a new timeline diamond "Relecloud · non-renewal notice · Mar 1, 2027". The new items have no owner until Assign owners runs at 7:00 AM.

### 2.3 Evidence for beat 4: `Northwind-COI-Contoso-2026.docx`

A one-page sample certificate of insurance from Humongous Insurance Brokerage (fictional): insured Northwind, holder Contoso Ltd, regarding MSA No. NW-MSA-2024-0117 Section 7.1; commercial general liability $2,000,000 each occurrence and technology E&O $5,000,000 each claim, December 15, 2026 to December 15, 2027. The footer says it is a fictional sample.

### 2.4 Expected screens and answers, computed from the data

**Owner digest email (S3), generated on the recording day.** Subject: "Your obligations this week: 4 overdue, 6 due soon".
- Overdue: Tailspin initial marketing plan (Sep 29) · Proseware initial SOC 2 report (Oct 1) · Contoso BCP/DR plan (Oct 31) · Woodgrove insurance endorsements (Nov 14).
- Due soon: Contoso non-renewal notice (Dec 1) · Fabrikam hosting fee (Dec 1) · Alpine Ski House rent (Dec 1) · Woodgrove interest (Dec 1) · Wide World forecast (Dec 5) · Litware Named User true-up (Dec 6).
- Next 30 days: Deliver certificate of insurance to Contoso Ltd by December 15 (Dec 15).
- Footer: "You also own 25 event-driven or ongoing obligations…" and the Mark fulfilled hint.

**Mark fulfilled (beat 4).** One line, like: "Marked 'Deliver certificate of insurance to Contoso Ltd by December 15' fulfilled on 2026-11-2x (evidence attached). Next occurrence due 2027-12-15 (#nn)." The new item's Capture key is `01-Contoso-MSA.docx|Section 7.1|deliver-coi#2027-12-15`.

**Copilot, "Which contracts auto-renew in the next 120 days?" (after beat 3).** Window: November 24, 2026 to March 24, 2027.
- Must name: **Contoso MSA**, notice by **2026-12-01** (Amendment No. 1, Section 2; renews 2027-04-01) and **Relecloud**, notice by **2027-03-01** (Section 1.2; renews at $96,000).
- Likely also lists the other notice deadlines in the window: Alpine Ski House lease option closes 2026-12-30; Adventure Works renewal decision before its 2026-12-31 expiry (does not auto-renew); Fabrikam transition-assistance request by 2027-01-30; Contoso fee-increase notice by 2027-01-31.
- Must not list as inside the window: Litware support non-renewal (2027-09-07) or Fabrikam's 2027-03-31 renewal decision.

**Copilot, "What could put us in default with Woodgrove right now?"**
- Must say: the **insurance endorsements** were due **2026-11-14** (Section 5.1) and are still open. Under **Section 6.1(c)** a missed Article 3 or Article 5 duty becomes an Event of Default if it continues **15 days after notice from the bank**. Then Woodgrove can terminate the $10,000,000 commitment and call all advances due (Section 6.2).
- Likely also lists the other Events of Default: interest or principal not paid within 3 business days (next interest: December 1); liquidity below $5,000,000 at any time (Section 4.1, no cure period); a materially incorrect representation.
- If it adds that Section 3.3 may already require Northwind to notify the bank within 5 business days, keep it; don't script it.

**Leadership page (beat 6, after beats 3 and 4).** "63 open obligations across 12 contracts; 15 of them high risk and 4 overdue today." Cards: Open 63 · Fulfilled 1 (2 waived or not applicable) · High-risk open 15 (1 due within 14 days or overdue) · Overdue today 4. We owe 43 · Owed to us 12 · Mutual 8. First row of "High-risk open items": Contoso non-renewal, Dec 1. (The page counts the amendment as its own contract, so it says 12 where Home says 11; the talk track doesn't say either number.)

---

## 3. Setup

Do these in order on the recording day unless marked. Every step is a prompt for **Copilot in SharePoint on the hub site** unless it says otherwise; each has a check against the data above and a fallback. No code.

**Recording tip.** Record at native display resolution (4K if you have it), browser zoom 125–150%, 60 fps if possible. Retype each live prompt on every retake so the editor can find the retakes. Turn off notifications. Keep the Copilot pane closed on every tab until the beat opens it.

### S0. Recording day
- **Do:** pick one day between November 25 and November 30, 2026 and record every beat that day.
- **Confirm:** Home shows "Contoso · non-renewal notice · Dec 1" with "in N days", N of 1 or more.
- **Fallback:** none for the date. From December 1 the hero is Overdue; re-plan rather than record.

### S1. The site runs the v1.0 kit
```text
List the site skills in AgentAssets/Skills, the AI workflows on this site with each one's trigger, skill and last run, and the views on the Obligations list.
```
- **Confirm:** the eight working skills above (plus `setup-obligation-hub` and `clear-obligation-sample-data` if installed), six workflows, and the Obligations views including **My obligations** and **Needs review**. Home shows "Live · 60 obligations" and tiles 4 / 6 / 3 / 3.
- **Fallback:** if the skill folders still have the old names (`assign-owners`, `daily-sweep`, `owner-digest`, `leadership-digest`, `mark-fulfilled`), either re-run the installer (`setup-obligation-hub`) or leave them: the talk track never says a skill name. If a page says "Sample snapshot" instead of "Live", reload it; if it persists, re-publish the page.

### S2. Six AI workflows exist and have each run once
Paste each prompt separately (skip any that S1 shows already exist).
```text
Create an AI workflow named "Capture new contracts" on this site. Trigger it when a file is added to the Contracts library. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. Save results without asking for confirmation. Run as me.
```
```text
Create an AI workflow named "Capture changed contracts" on this site. Trigger it when a file in the Contracts library is changed. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. If the contract text is unchanged since the last capture, log the skip and stop. Save results without asking for confirmation. Run as me.
```
```text
Create an AI workflow named "Assign owners" on this site that runs every day at 7:00 AM Pacific time. For each run, load the site skill assign-obligation-owners from AgentAssets/Skills and follow it for the Obligations list. It may send each newly assigned owner one email or Teams message. Run as me.
```
```text
Create an AI workflow named "Daily sweep" on this site that runs every day at 6:00 AM Pacific time. For each run, load the site skill sweep-obligations from AgentAssets/Skills and follow it for the Obligations list. It may send reminder and escalation emails or Teams messages. Run as me.
```
```text
Create an AI workflow named "Owner digest" on this site that runs every Monday at 8:00 AM Pacific time. For each run, load the site skill obligation-owner-digest from AgentAssets/Skills and follow it for the Obligations list. It may send each owner one email or Teams message. Run as me.
```
```text
Create an AI workflow named "Leadership digest" on this site that runs every Friday at 3:00 PM Pacific time. For each run, load the site skill obligation-leadership-digest from AgentAssets/Skills and follow it. It may send one email to the leadership recipients in AgentAssets/Config/hub-settings.json and post to their Teams channel. Run as me.
```
- **Confirm:** Settings → Workflows shows six cards, each with "Last run · Succeeded" (S3 covers the two digests). Home → Workflow health has no "hasn't run yet" banner.
- **Fallback:** open Run Log → Recent runs and read the failed row's Details, then re-paste that prompt. A scheduled workflow that hasn't fired yet is handled in S3.

### S3. Run the Owner digest and Leadership digest workflows once, on the recording day
If you record on Monday, November 30 after 8:00 AM, the scheduled Owner digest has already run; skip its prompt and say "from 8 o'clock this morning" in row 4:07.
```text
Run the Owner digest workflow now.
```
```text
Run the Leadership digest workflow now.
```
- **Confirm:** Zach's inbox has "Your obligations this week: 4 overdue, 6 due soon" with the sections in 2.4 (25 event-driven or ongoing in the footer). Run Log has "Owner digest - <today>" and "Leadership digest - <today>", both Succeeded. Home → Workflow health is all green.
- **Fallback 1** (if a workflow can't be run on demand): "Change the Owner digest workflow to run today at <a time 10 minutes from now> Pacific." When it has run: "Change the Owner digest workflow back to Mondays at 8:00 AM Pacific." Same for the Leadership digest (back to Fridays at 3:00 PM).
- **Fallback 2:** run the skill in chat: "Send the owner digest now." If it logs Skipped ("already sent today"), add "Resend it." The email and Run Log row look the same.

### S4. The Contoso certificate is not yet fulfilled
```text
Show the Contoso certificate of insurance obligations with status, due date, evidence and capture key.
```
- **Confirm:** one item, "Deliver certificate of insurance to Contoso Ltd by December 15", Not started, due 2026-12-15, no evidence; no item due 2027-12-15.
- **Reset between takes of beat 4:**
```text
Set "Deliver certificate of insurance to Contoso Ltd by December 15" back to Not started with Timing Upcoming, clear Fulfilled on and Evidence, delete its 2027-12-15 occurrence, and delete the Mark fulfilled Run Log row for it. Show me what changed.
```
- **Fallback:** if the reset prompt won't delete, delete the 2027 item and edit the three fields in the list by hand (the one manual exception).

### S5. Evidence link on the clipboard
Attach `Northwind-COI-Contoso-2026.docx` to the Copilot chat, then:
```text
Save the attached certificate to the Documents library and give me a link people in my organization can open.
```
- **Confirm:** the link opens the certificate. Copy it to the clipboard right before beat 4.
- **Fallback:** at the "Evidence?" question on camera, attach the file instead of pasting a link. The skill files it in Evidence as `<ID>-<date>-Northwind-COI-Contoso-2026.docx` and links it.

### S6. Relecloud isn't on the site yet
```text
Is 12-Relecloud-Order-Form.docx in Contracts, and are there any Obligations items or Run Log rows for it?
```
- **Confirm:** none. Home tiles 4 / 6 / 3 / 3, Review badge 3, "Live · 60 obligations".
- **Reset between takes of beat 3** (also deletes the Run Log rows, so the re-upload isn't skipped as "content unchanged"):
```text
Delete every Obligations item and Run Log row whose ContractName is 12-Relecloud-Order-Form.docx, then delete that file from Contracts. Show me what you deleted.
```
- **Fallback:** delete the file and filter the Obligations "All obligations" view by ContractName to remove the items by hand.

### S7. Dry run of beat 3 (the day before, or the morning of)
- **Do:** drag `12-Relecloud-Order-Form.docx` into Contracts. Note the clock. Refresh Run Log → Recent runs until the Capture row appears; note the elapsed minutes for the sped-up label. Compare the Obligations items with `expected-obligations.md`. Then run S9 before resetting with S6.
- **Confirm:** "Capture - 12-Relecloud-Order-Form.docx", Succeeded, Created 5, Held 1. Home shows the screen in 2.2 ("Needs review 4", Relecloud diamond on March 1). Review shows the Rate Card item with "Why it was held". Leadership shows 63 open and 15 high risk (it was 13 before the upload).
- **Fallback:** if capture takes more than 10 minutes or fails, use the Re-capture obligations quick step on the file for the take (select the file in Contracts → Re-capture obligations); Copilot shows "Created 5, updated 0, held 1, excluded …" in the pane, then continue on Home. If a must-match point differs (see `expected-obligations.md`), reset and re-run once; if it still differs, change the beat-3 lines to what the screen shows.

### S8. Quick steps are on the list and library
```text
Which quick steps are set up on the Obligations list and the Contracts library, and what prompt does each send?
```
- **Confirm:** Obligations: **Mark fulfilled** ("Mark this obligation fulfilled using the mark-obligation-fulfilled skill.") and **Remove obligation**. Contracts: **Re-capture obligations**.
- **Fallback:**
```text
Add a quick step named "Mark fulfilled" to the Obligations list that sends Copilot: Mark this obligation fulfilled using the mark-obligation-fulfilled skill.
```
```text
Add a quick step named "Re-capture obligations" to the Contracts library that sends Copilot: Re-capture obligations from this contract using the capture-obligations skill. Do a full capture even if the text hasn't changed.
```
If no prompt path works, add them in the list's quick-steps settings (the one UI exception).

### S9. Copilot answers, dry run (while Relecloud from S7 is still captured)
Ask both live prompts from beat 5 in a fresh Copilot pane on Home.
- **Confirm:** the first answer names Contoso (December 1, Amendment No. 1) and Relecloud (March 1) and leaves out Litware. The second names the overdue Woodgrove insurance endorsements and the 15-days-after-notice rule in Section 6.1. Both cite clauses with links.
- **Fallback:** if Copilot answers from the original MSA (December 31), check that `obligation-hub-guide` and `SHAREPOINT.md` are in AgentAssets and ask again in a new pane. If the second answer misses the endorsements twice, use the alternate line in section 5 (beat 5, row 5.3).

### S10. The honest-limits section is on How it works
- **Do:** open the How it works page and find "What this sample doesn't do yet" (event-driven and ongoing obligations aren't watched).
- **Confirm:** the section is visible and names the event-driven gap.
- **Fallback:** show `docs/known-gaps.md` section 1 on GitHub instead, or say the line over the Settings page.

### S11. Tabs, windows and clipboard
- **Do:** one Edge window, signed in as Zach, tabs in this order: (1) Home, (2) Contracts library, "All contracts" view, (3) Run Log, "Recent runs" view, (4) Outlook on the web with the digest email open (search the inbox for "Your obligations this week" so reminder emails stay off screen), (5) Obligations list, "My obligations" view, (6) Leadership, (7) Settings scrolled to Workflows, (8) How it works scrolled to the limits section. A File Explorer window beside the browser showing `12-Relecloud-Order-Form.docx`. Evidence link on the clipboard (S5). The cold-open slide (section 6) open full screen in PowerPoint, recorded as its own clip.
- **Confirm:** click through every tab once; each page shows "Live", Home shows tiles 4 / 6 / 3 / 3, and no Copilot pane is open.
- **Fallback:** if a page loads slowly, reload it before the take, not during.

### S12. Order of operations on recording day
S0 → S1 → S2 → S3 → S4 → S5 → S8 → S10 → S11, then record beats 1–7 in order. S6 and S4 are the resets for retakes. S7 and S9 are the dry run, done the day before or early that morning, followed by the S6 reset.

---

## 4. Smart parts

What the audience doesn't see that makes the answers look earned.

- **`capture-obligations`, amendments.** Reads a contract with its amendments, closes superseded base clauses and tracks only the amended value; that's why Home shows December 1 and the 90-day item is closed.
- **`capture-obligations`, PROTECT and EXCLUDE lists.** Payments, notices, reports, certificates and windows are always kept; contacts, support hours and boilerplate are dropped; that's why the Relecloud capture has five items, not twelve.
- **Missing-document rule.** When a protected obligation's terms sit in a document the library doesn't have, capture makes one held item, Confidence Low, with the reason, instead of guessing; that's the Relecloud Rate Card item.
- **Date rules and verbatim sources.** "At least N days before X" is X minus N, a date stated in the text wins, and every item stores the exact sentence and section; so March 1 and December 1 can be checked by anyone.
- **Capture key and fingerprint.** `<file>|<clause>|<slug>` plus a word-count fingerprint means re-captures update rather than duplicate, and the file-changed workflow skips column edits.
- **Exclusions memory.** The Remove obligation quick step writes a clause or pattern to Exclusions, so capture never adds a removed item back.
- **Obligation Types and risk by consequence.** 37 editable types set track, exclude or hold; v1.0 rates High only when a miss loses a right or money or starts a legal clock, so 13 of 58 open items (22%) are High and "high risk" on Leadership means something.
- **Obligation Owners and `hub-settings.json`.** Routing rules (most specific wins) and settings (due soon = 14 days, reminder cooldown = 3 days, leadership recipients) change behaviour without touching a prompt.
- **`mark-obligation-fulfilled`.** Asks once for evidence and creates the next occurrence with the series key, so the daily sweep never makes a duplicate.
- **`obligation-hub-guide` and `SHAREPOINT.md`.** Copilot answers from the list first, reads the contract only for exact wording, computes timing itself, never estimates a date, and cites clause, quote and link.
- **Run Log.** One row per run feeds Workflow health on Home and "Last run" in Settings, so a failed run is visible without opening anything.
- **Live HTML pages.** Each page reads the lists through a live-data manifest and computes Timing in the browser from today, so the page is right even if the sweep ran yesterday.

---

## 5. Run order

Target runtime: **9:35**. Say-column text is the talk track, written to be spoken; [square brackets] are not spoken. Live prompts are typed on camera (retype on every retake). "Depends on" points to section 3.

| Time | Beat | On screen | Say | Live prompt | Depends on |
|---|---|---|---|---|---|
| 0:00 | 1 · Cold open | Cold-open slide: "Dec 1", "not Dec 31" struck through, the amendment line and $540,000. | Northwind Traders has a contract with Contoso that renews itself every April. To get out, Northwind has to say so by December 1st. Not December 31st. That was the old date. An amendment moved the notice period from 90 days to 120. Anyone reading the original contract misses it by a month. And a $540,000 year renews by default. | — | Slide (section 6) |
| 0:30 | 2 · The hub | Home, top: "10 obligations need attention in the next 14 days", "Live · 60 obligations". | I'm Zach Rosenfield. I lead product for SharePoint and Content AI at Microsoft. Here's my claim. You don't need a contract-management system to stop missing dates like that. You need every date on a named person's list. A SharePoint site can keep that list. This is it. | — | S1, S11 |
| 0:50 | 2 · The hub | Hover the tiles: Overdue 4, Due in 14 days 6, Needs an owner 3, Needs review 3. | It opens on one question. What needs attention? Ten things in the next two weeks. Four overdue. Six coming due. Three are held for review, because the AI wasn't sure and a person should decide. | — | S1 |
| 1:06 | 2 · The hub | Scroll to Notice windows. Point at "Contoso · non-renewal notice · Dec 1" and the bracket "Contoso · 120-day notice period (amended from 90 days)". | This is the part I care about. Every notice deadline for the next six months. Here's Contoso. December 1st. And the bracket says it out loud. 120-day notice, amended from 90. The hub read the amendment with the original contract and closed the old 90-day item. Nobody gets reminded about the wrong date. | — | S1 |
| 1:32 | 2 · The hub | Click the Contoso diamond: the Obligations item with Due 12/1/2026, Clause "Section 2 (amends MSA Section 9.2)", Source clause, Owner Zach Rosenfield. | Click it, and it's an item in a list. A due date. The clause, word for word. An owner. On this demo site, that's me. Nobody typed any of this. So where does it come from? Let me add a contract. | — | S2 (Assign owners) |
| 1:55 | 3 · Drop a contract | Contracts library. Drag `12-Relecloud-Order-Form.docx` from File Explorer into the library. | Procurement just sent a new one. Relecloud, for fleet software. A five-month pilot that turns into a $96,000-a-year subscription, unless someone says no in time. I drop it in the Contracts library. That's my whole job here. | — | S6, S7 |
| 2:12 | 3 · Drop a contract | **Sped-up footage.** Lower third: "Sped up · capture took about N minutes" (N from S7). Cut from the upload to Home after refresh. | Adding a file starts an AI workflow, Capture new contracts. It runs one skill that reads the contract and writes the obligations to the list. We've sped this part up. It takes a few minutes. | — | S2 (Capture new contracts), S7 |
| 2:30 | 3 · Drop a contract | Home: "63 obligations open across 11 contracts", Needs review 4, Needs an owner 8, new diamond "Relecloud · non-renewal notice · Mar 1, 2027". | Back on the overview. Five new obligations. Review went from three to four. And there's a new deadline on the timeline. Relecloud. Non-renewal notice. March 1st. | — | S7 |
| 2:44 | 3 · Drop a contract | Click the Relecloud diamond: item with Due 3/1/2027, Clause "Section 1.2", Source clause (the renewal sentence). | Nobody typed March 1st. The order form says 60 days before the pilot ends on April 30th. The skill did the math, and it kept the sentence the date came from, with the section number. If anyone asks why March 1st, the answer is right here. | — | S7 |
| 3:10 | 3 · Drop a contract | Review page (nav "Review 4"): the Relecloud card, Confidence Low, "Why it was held: Terms in Relecloud Rate Card, which isn't in the Contracts library", Clause 2.2 quoted. | Now the one it held. Section 2.2 says renewal and overage fees follow Relecloud's rate card. We don't have the rate card. So it didn't guess. It made one item, marked it low confidence, and said why. That's the rule I want from AI on contracts. If the terms aren't in front of it, it asks a person. | — | S7 |
| 3:38 | 3 · Drop a contract | Run Log tab, refresh: "Capture - 12-Relecloud-Order-Form.docx", Succeeded, Created 5, Held 1; open Details, which lists the clauses it left out. | And the Run Log keeps the receipt. Five created, one held, and what it left out. Invoices, contacts, support hours, boilerplate. Tomorrow at 7, Assign owners gives the new items owners, by rule. | — | S2 (Assign owners), S11 |
| 3:55 | 4 · Owner's day | Outlook tab: "Your obligations this week: 4 overdue, 6 due soon", from Zach Rosenfield. | Now the owner's side. Every Monday at 8, each owner with something due gets one email. Not a dashboard you have to remember to open. An email. | — | S3, S11 |
| 4:07 | 4 · Owner's day | Scroll the email: Overdue 4, Due soon 6, Next 30 days "Deliver certificate of insurance to Contoso Ltd by December 15", footer. | Here's mine. I ran this week's early, for the recording. Four overdue. Six due soon. Each one with the date, the clause and a link. And one coming up. Contoso needs our certificate of insurance by December 15th. It came from my own mailbox, because workflows run as the person who set them up. In production, you'd set them up with a shared obligations account. | — | S3 |
| 4:37 | 4 · Owner's day | Obligations list, "My obligations" view. Type "certificate" in the list search. Select the Contoso item. Quick steps → **Mark fulfilled**. | Say I sent that certificate this morning. In My obligations, I find it, select it, and run the quick step. Mark fulfilled. | — | S4, S8, S11 |
| 4:52 | 4 · Owner's day | Copilot pane opens with the quick-step prompt and asks "Evidence? Paste a link, attach a file, or say none." Type the reply, paste the link, send. If the reply takes more than about 15 seconds, speed it up and label it. | It asks for proof. I give it the certificate. | Sent it to Contoso this morning. Here's the certificate: [paste link] | S5 |
| 5:10 | 4 · Owner's day | Confirmation: "Marked … fulfilled on 2026-11-2x (evidence attached). Next occurrence due 2027-12-15." | Done. Marked fulfilled today, with the evidence linked. And because this happens every year, it already made next year's item. December 15th, 2027. Same owner. Same clause. | — | S4 |
| 5:28 | 4 · Owner's day | Close the pane, refresh: two Contoso rows, Fulfilled (Dec 15, 2026) and Not started (Dec 15, 2027). | That's the loop. The hub tells you. You do the work. You close it with proof, and when an auditor asks, the proof is one click from the item. And next year is already on somebody's list. | — | S4 |
| 5:50 | 5 · Ask Copilot | Home tab. Open the Copilot pane; start typing prompt 1 while talking. | Questions work the same way. No new app. It's the Copilot already in SharePoint. On this site it reads the list first, and the contract when it needs the exact words. | — | S9 |
| 6:00 | 5 · Ask Copilot | Type prompt 1; the answer streams: Contoso Dec 1 and Relecloud Mar 1 first, then the other notice deadlines, with clause links. If generation takes more than about 20 seconds, speed it up and label it. | Two contracts. Contoso, notice by December 1st, from Amendment Number 1. And Relecloud, the contract I just added, notice by March 1st. It lists the other deadlines before spring too. Every line links to the item and quotes the clause. I can check all of it. And Litware renews too, but its notice date is next September, so it's rightly left off. | Which contracts auto-renew in the next 120 days? | S7, S9 |
| 6:50 | 5 · Ask Copilot | Type prompt 2; the answer names the overdue insurance endorsements, Section 6.1, the 15-day cure after notice, and Section 6.2. Same speed-up rule. | Woodgrove is our ten-million-dollar credit line. It found the live risk. Insurance endorsements, due November 14th, still open. Under Section 6.1, that becomes an event of default fifteen days after the bank sends notice. Then the bank can cancel the line and call every advance. A CFO question, answered from the register and the contract together. | What could put us in default with Woodgrove right now? | S9 |
| 7:45 | 6 · Leadership and how it runs | Leadership page: "63 open obligations across 12 contracts; 15 of them high risk and 4 overdue today"; High-risk open items, Contoso Dec 1 on top. | Leadership gets the same truth at a different altitude. Sixty-three open. Fifteen high risk. Four overdue. Every number is a count from the list. Nobody maintains this dashboard. Top of the high-risk list, Contoso, December 1st. A digest of this goes to leadership every Friday. | — | S3 |
| 8:08 | 6 · Leadership and how it runs | Settings → Workflows: six cards, each with Trigger, Skill and "Last run · Succeeded". Lower third: "AI workflows: preview feature. Not generally available." | Here's how it runs. Six AI workflows. Each has one trigger and runs one skill. Capture, when a contract is added or changed. Assign owners every morning. A daily sweep for reminders and escalations. An owner digest on Monday, a leadership digest on Friday. Every skill is a markdown file on the site. No code. Change a rule, and the next run picks it up. | — | S1, S2 |
| 8:40 | 6 · Leadership and how it runs | How it works → "What this sample doesn't do yet". | One honest limit. It tracks dates. It can't see events. If Northwind changes ownership, nothing tells the hub. Someone has to log it before the 30-day notice to Tailspin runs out. Almost half of these obligations work that way, and the site says so. | — | S10 |
| 9:05 | 7 · Close | Home → Notice windows, Contoso Dec 1 with its owner. End on the closing line, then the end card (section 6). | Back to December 1st. The Contoso notice is on a list, with a name and a date. And it will be in an email every Monday until someone closes it with proof. Every date, a name. The skills, pages and setup prompts are on GitHub, in sharepoint-ai-skills. AI workflows run here in a preview environment, and they're not generally available yet. | — | S1 |

**Alternate line for row 6:50** (if the answer lists the Events of Default but doesn't flag the endorsements): "It lists four ways to default. Look at this one: a missed Article 5 duty. Our insurance endorsements are on the list as overdue since November 14th. The bank's notice starts a fifteen-day clock. That's a CFO question, answered from the register and the contract together."

**Beat 3 if you use the fallback (S7):** replace row 2:12 with "If a workflow is paused or slow, the same skill runs by hand. Select the file, and run the quick step: Re-capture obligations." The Copilot pane then shows the created, held and excluded counts.

### Timing (`python talk_timing.py --write`)

<!-- timing:start -->
Speaking time at 140 words per minute (numbers counted as spoken).

| Beat | Window | Words | Speaking | Slack for clicks, typing and answers |
|---|---:|---:|---:|---:|
| 1 · Cold open | 0:30 | 65 | 0:28 | 0:02 |
| 2 · The hub | 1:25 | 180 | 1:17 | 0:08 |
| 3 · Drop a contract | 2:00 | 241 | 1:43 | 0:17 |
| 4 · Owner's day | 1:55 | 188 | 1:21 | 0:34 |
| 5 · Ask Copilot | 1:55 | 151 | 1:05 | 0:50 |
| 6 · Leadership and how it runs | 1:20 | 155 | 1:06 | 0:14 |
| 7 · Close | 0:30 | 61 | 0:26 | 0:04 |
| **Total** | **9:35** | **1041** | **7:26** | **2:09** |

Talk track: 7:26 of speaking (target 7:00-10:00); planned runtime 9:35. Within budget.
<!-- timing:end -->

---

## 6. Bookends

### Cold-open slide prompt
For Copilot in PowerPoint, or the pptx skill in Cowork:
```text
Create one 16:9 slide in a Copilot dark style: near-black background (#0B0B12) with a soft blue-to-purple glow in the top-right corner. Center a very large "Dec 1" in white, bold. Directly under it, in mid-grey, "not Dec 31" with a thin line struck through it. Above "Dec 1", small uppercase letter-spaced text in light grey: "CONTOSO MASTER SERVICES AGREEMENT · NOTICE OF NON-RENEWAL". At the bottom, one line in light grey: "Amendment No. 1 moved the notice period from 90 to 120 days. Miss it, and a $540,000 year renews by default." No logos, no bullets, no icons, no slide number, no footer. Speaker notes: Northwind Traders has a contract with Contoso that renews itself every April. To get out, Northwind has to say so by December 1st. Not December 31st. That was the old date. An amendment moved the notice period from 90 days to 120. Anyone reading the original contract misses it by a month. And a $540,000 year renews by default.
```
Check: one slide, nothing on it but the date, the struck-through old date and the one-line stake.

### Closing line (returns to the stake)
"Back to December 1st. The Contoso notice is on a list, with a name and a date. And it will be in an email every Monday until someone closes it with proof. Every date, a name."

### Optional end card
Same dark style: "Every date, a name." · "Obligation Hub for SharePoint · experimental sample" · "github.com/zrosenfield/sharepoint-ai-skills".

---

## 7. Assumptions & risks

### 7.1 Availability of what the demo uses

| Feature | Status | Source |
|---|---|---|
| Copilot in SharePoint | General availability rolling out to worldwide tenants from September 30, 2026; everyday capabilities included with the Microsoft 365 Copilot license, "advanced work" uses Copilot Credits | learn.microsoft.com/sharepoint/copilot-in-sharepoint-get-started; SharePoint blog, "SharePoint AI innovations hit GA" (September 25, 2026) |
| Site skills (AgentAssets/Skills/<name>/SKILL.md) | Available with Copilot in SharePoint; skills can't run custom code or connect to external systems | learn.microsoft.com/sharepoint/copilot-in-sharepoint-skills |
| HTML pages in Site Pages | Public preview October 2026; worldwide GA rolling out mid-November to late December 2026 | Microsoft 365 roadmap 569208; message center MC1479517 |
| AI workflows (file-added, file-changed and scheduled triggers that run a site skill, send email and Teams, run as their creator) | Preview only; not generally available yet. Learn lists "skills in scheduled AI automations" as advanced work that uses Copilot Credits | Kit plan platform facts; solution README and `docs/known-gaps.md` section 11; learn.microsoft.com/sharepoint/copilot-in-sharepoint-get-started |
| HTML pages with live list data (live-data manifest) | Verified on the demo site ("Live · 60 obligations") | Kit plan platform fact 6 |
| Quick steps that send a prompt to Copilot | Verified on the demo site | Kit plan platform fact 9 |
| Autofill of the Contracts key-term columns | Optional; never ran on the test tenant within an hour. The demo doesn't depend on it | Kit plan platform fact 7 |

### 7.2 What breaks first, and the fallback

| Risk | Effect on the video | Fallback |
|---|---|---|
| Recording on or after December 1 | Hero item shows Overdue; the cold open is wrong | None. Record by November 30 (S0) |
| Capture is slow (more than 10 minutes) or fails | Beat 3 stalls | Keep recording and cut (disclosed as sped up), or use the Re-capture obligations quick step (S7, alternate line in section 5) |
| Capture result differs (more or fewer items, no hold) | "Five new" or "the one it held" is wrong | Reset (S6) and re-upload once; else say what the screen shows |
| Copilot answers from the original MSA (December 31) | Undercuts the claim | New pane, check `obligation-hub-guide` and `SHAREPOINT.md` (S9); never keep that take |
| Woodgrove answer doesn't flag the endorsements | Beat 5's second payoff is weaker | Retake once; then the alternate line under the run order |
| Mark fulfilled doesn't create the 2027 item | "Next year is already on the list" is false | Reset (S4) and retake; if it repeats, cut that sentence and row 5:28 |
| Digest generated on another day | "in N days" in the email doesn't match Home | Regenerate on the recording day (S3) |
| A workflow shows a failure on Home | Visible red row in Workflow health | Re-run it (S2, S3) before recording; don't scroll to that panel during beat 2 |
| Assign owners runs at 7:00 AM between takes | Relecloud items get owners, "Needs an owner" changes | Record beat 3 in one day; reset with S6 before each take |
| Daily sweep reminders fill the inbox | Clutter in beat 4 | Inbox search for the digest subject (S11) |
| Retaking beat 3 without a reset | Upload is "file changed", capture skips as unchanged | Always run the S6 reset (it deletes the Run Log rows too) |
| Leadership numbers differ from 63 / 15 / 4 (capture rated a Relecloud item differently) | Spoken numbers don't match the screen | Read the numbers from the S7 dry run into row 7:45 before recording |
| Copilot is slow to answer (beat 4 evidence reply, beat 5 prompts) | Dead air | Keep talking over it, or speed up the wait and label it "Sped up" |

### 7.3 Limits I couldn't confirm
- Whether a scheduled AI workflow can be run on demand ("Run the Owner digest workflow now"), and whether the skill run in chat can send mail. S3 has a schedule-change fallback that relies only on creating and changing schedules.
- Whether attaching a file in the Copilot pane works at the "Evidence?" question on the test tenant (S5 fallback).
- How long capture takes on the day; the label in beat 3 uses the time measured in S7.
- That the current How it works page carries the "What this sample doesn't do yet" section (S10).
- `docs/known-gaps.md` section 11 and the solution README describe site skills and HTML pages as preview features, while the public sources in 7.1 describe them as GA or rolling out. Reconcile before publishing; the talk track only makes the AI-workflows claim.
- That `github.com/zrosenfield/sharepoint-ai-skills` is public when the video goes out.

### 7.4 Decisions made on Zach's behalf
- Recording window, Zach as on-screen owner, Relecloud as the new counterparty, canonical skill names, the "renews by default" stake wording (Assumptions 1–5).
- Live prompts: the Home page's own "Which contracts auto-renew in the next 120 days?" chip, and "What could put us in default with Woodgrove right now?" instead of "What can Woodgrove call a default on?", so the answer has to connect the contract to an overdue item.
- The Relecloud contract's terms (five-month pilot, $36,000, $96,000 renewal, 60-day notice, quarterly fleet report, Rate Card hold) chosen so its deadline lands inside both the 120-day question and the 180-day timeline, and nothing lands inside 14 days.
- Beat 4 uses the Obligations "My obligations" list view, not the My obligations page, because quick steps live in the list and the page can't detect the signed-in user.
- Contract 360 is left out: autofill may leave Relecloud's key terms blank on camera.
- On-camera availability line: "AI workflows run here in a preview environment, and they're not generally available yet," plus a lower third in beat 6. 
- Zach's intro line ("I lead product for SharePoint and Content AI at Microsoft") — adjust to his preferred title.

### Alternate angles
- **The amendment nobody read:** start with only the base MSA on the site (Dec 31), drop Amendment No. 1 in on camera, and watch capture close the 90-day item and move the deadline to December 1.
- **The CFO's Monday:** tell it from Woodgrove's $10,000,000 credit line, where an overdue insurance endorsement is fifteen days of bank notice away from an Event of Default.
