# Known gaps

What the Obligation Hub doesn't do yet, stated plainly. Read this before you show the hub to anyone who might rely on it. Figures come from the reference build: 11 fictional sample contracts, 60 obligations, 58 of them open, on 2026-11-24.

The hub tracks deadlines that contracts state. It doesn't give legal advice, doesn't prove anything was done, and doesn't replace a contract lifecycle management (CLM) system.

| # | Gap | Workaround today | Roadmap fix |
|---|---|---|---|
| 1 | Nearly half the open obligations have no date, and nothing watches for their trigger | Review "Triggered and ongoing" with each owner every month | Event intake and periodic attestations |
| 2 | No proof standard | Attach evidence by habit; check the Evidence library | Evidence required for High risk, fulfilment sign-off, retention label |
| 3 | Capture accuracy measured on synthetic contracts only | Confirm every item for your first contracts; run the evals | Accuracy eval on 100+ real contracts, including scans |
| 4 | Deadline tracking only | Keep payments in AP/ERP and service levels in your monitoring tools | E-signature intake and calendar holds |
| 5 | Leadership view is a snapshot | Keep the Friday digests; compare by hand | Trends and dollar exposure |
| 6 | The My obligations page can't tell who's signed in | Use the list view "My obligations", or the page's `#owner=` link | Signed-in-user detection |
| 7 | Messages come from whoever set up the workflows, and workflows are still maturing | Set them up as a shared account; check the Run Log | Service account for workflows |
| 8 | Everyone with site access sees every contract | One hub per confidentiality boundary | Per-contract permissions |
| 9 | Pages load whole lists | Index Status, DueDate and Owner above ~5,000 items | Indexes for scale |
| 10 | Autofill may not run; amendments don't update the base contract's summary | Fill key terms by hand if needed | None planned in the hub |
| 11 | Preview platform features | Use a test site where the preview features are on, or Cowork | Platform general availability |
| 12 | Risk ratings were too often High | Fixed in v1.0 | Done: risk by consequence |

---

## 1. Event-driven and ongoing obligations aren't watched
**What it means.** 48% of open obligations in the sample (28 of 58) have no due date. They're event-driven ("notify within 48 hours of a data breach", "notify within 30 days after a change of control") or ongoing ("maintain insurance", "don't compete"). The hub records them, cites the clause, gives them an owner and shows them in the "Triggered and ongoing" view. Nothing detects the event itself, so no reminder fires when it happens.

**Why it matters.** Some of the costliest misses are event-driven: breach notices, change-of-control notices, default notices. A register that looks complete can give false comfort about these.

**Workaround today.** Owners hear about them in their assignment message and the owner digest footer ("You also own N event-driven or ongoing obligations"). Review the "Triggered and ongoing" view with each owner monthly. Make sure the people who'd see the event (security, finance, corporate development) know the hub exists.

**Roadmap fix.** Event intake (a simple "an event happened" form or mail rule that matches open event-driven items and dates them) and periodic attestations (owners confirm each quarter that ongoing duties were met).

## 2. No proof standard
**What it means.** The Mark fulfilled quick step accepts "none" as evidence. Nobody signs off a fulfilment. The Run Log is an ordinary, editable list, not a tamper-evident audit trail. Evidence files sit in a normal library with no retention label.

**Why it matters.** An auditor, lender or regulator asks "show me". Status = Fulfilled with no evidence is a claim, not proof.

**Workaround today.** Ask owners to always attach a link or file, especially for High risk items. Check the Evidence library and the `Evidence` column in the "All obligations" view. If you need retention, apply a retention label to the Evidence library yourself.

**Roadmap fix.** Require evidence for High risk items, add a fulfilment sign-off by the escalation owner, and apply a retention label to Evidence.

## 3. Capture accuracy is measured on synthetic contracts only
**What it means.** `capture-obligations` was scored on 11 fictional Word contracts it was tuned on: 55 of 55 tracked obligations found, with no false extras, and every trap passed. That's a tuning result, not a measure of real-world accuracy. Real paper is untested: scanned PDFs, exhibits and SOWs, handwritten changes, and referenced documents that aren't in the library.

**Why it matters.** A missed obligation is invisible. You won't know it's missing unless someone reads the contract.

**Workaround today.** For your first contracts, have someone who knows them check every captured item against the text and confirm held items in the Needs review view. Run the evals in [`../evals/`](../evals/README.md) on a sample of your own contracts. Low-confidence items and terms in missing documents are always held for review.

**Roadmap fix.** An accuracy evaluation on 100 or more real contracts, including scans, with a published recall and precision.

## 4. Deadline tracking only
**What it means.** The hub tracks what's due and when. It doesn't check that payments were made against accounts payable or an ERP, doesn't measure service-level performance, and doesn't connect to e-signature, CLM or ERP systems. Contracts arrive only when someone puts them in the Contracts library.

**Why it matters.** A "pay within 45 days" item can be marked fulfilled while the payment is late. A signed contract that never reaches the library is never captured.

**Workaround today.** Keep payment matching in AP and service-level reporting in your monitoring tools. Make "upload to Contracts" part of your signing checklist.

**Roadmap fix.** E-signature intake (signed contracts land in the library automatically) and calendar holds for notice deadlines. Payment matching and SLA measurement aren't planned.

## 5. The leadership view is a snapshot
**What it means.** The Leadership page and the Friday digest show counts and lists as of today. They don't show trends over time or dollar exposure.

**Why it matters.** Leaders ask "is it getting better?" and "how much is at stake?". The hub can't answer either yet.

**Workaround today.** Keep the weekly digests and compare them by hand. Contract values are in the Contracts library's `ContractValue` column.

**Roadmap fix.** Trends from weekly snapshots and dollar exposure from contract values.

## 6. The My obligations page can't tell who's signed in
**What it means.** The HTML page shows one owner's items, chosen by a `#owner=<email>` link. It can't detect the person viewing it.

**Why it matters.** People expect "my" to mean them. Anyone can view anyone's list (they already can in the list itself).

**Workaround today.** Use the Obligations list view "My obligations", which does filter on the signed-in user, or bookmark the page with your own `#owner=` link. Owner messages link straight to each item.

**Roadmap fix.** Signed-in-user detection on the page.

## 7. Who messages come from, and workflow reliability
**What it means.** AI workflows run as the person who created them, so every reminder, escalation and digest comes from that person's mailbox and Teams account. If that person leaves or loses access, the messages stop. AI workflows are also still in preview, so runs can fail: check the Run Log.

**Why it matters.** A reminder system that silently stops is worse than none, because people stop checking.

**Workaround today.** Create the workflows while signed in as a shared obligations account with edit rights on the site. Check the Run Log ("Recent runs") weekly; the Home page shows failures and workflows that haven't run on schedule. See [workflow-checklist.md](workflow-checklist.md).

**Roadmap fix.** A service account for workflows, so messages don't depend on one person.

## 8. Everyone with site access sees every contract
**What it means.** Contracts, obligations and evidence inherit the site's permissions. There's no per-contract or per-business-unit security.

**Why it matters.** Some contracts (M&A, executive, litigation) can't be visible to everyone who handles routine obligations.

**Workaround today.** Keep sensitive contracts out, or run a separate hub on a separate site for each confidentiality boundary.

**Roadmap fix.** Per-contract permissions that flow to the contract's obligations and evidence.

## 9. Scale
**What it means.** The pages load the whole Obligations list in the browser. Above about 5,000 obligations, list views hit SharePoint's view threshold and pages get slower.

**Why it matters.** A large portfolio (hundreds of contracts with amendments) can reach that size.

**Workaround today.** Before you pass 5,000 items, index `Status`, `DueDate` and `Owner` in the Obligations list settings, and expect slower pages.

**Roadmap fix.** Indexes created at setup, and pages that query only what they show.

## 10. Autofill and contract summaries
**What it means.** The Contracts library's key-term columns (counterparty, dates, renewal, notice period, value, summary) use SharePoint autofill. On the test tenant, autofill never ran within an hour, and key terms were filled by hand. An amendment's autofill describes the amendment; it doesn't rewrite the base contract's summary or dates.

**Why it matters.** The Contracts views ("Expiring in 180 days") and Contract 360 page show these columns, so they can be empty or out of date.

**Workaround today.** Capture never depends on autofill: it reads the contract text, rolls renewal terms forward and applies amendments itself, so the Obligations list is right even when the columns are empty. Fill the key columns by hand for contracts that matter, and set **Amends** on amendments.

**Roadmap fix.** None planned in the hub; it depends on the platform's autofill.

## 11. Preview platform features
**What it means.** SharePoint AI workflows, HTML pages with live list data, and Copilot site skills are preview features that may not be available in your tenant yet. 

**Why it matters.** On most production tenants today, the hub's lists, views, formatting and quick steps work, but the automation and pages may not.

**Workaround today.** Evaluate on a test site where the preview features are available, or use the Cowork automations in [../prompts/cowork-prompts.md](../prompts/cowork-prompts.md) as a personal layer.

**Roadmap fix.** Follows the platform's general availability.

## 12. Risk ratings (fixed in v1.0)
**What it means.** Before v1.0, each item took its type's default risk, and 47% of open sample items came out High (27 of 58), which made High meaningless.

**Fix in v1.0.** `capture-obligations` now rates risk by consequence. High means a miss automatically loses a right or money or starts a legal clock: notice, renewal and option deadlines we must act on; change-of-control and breach notices; financing covenants, compliance certificates and default notices. Medium covers other dated or money obligations. Low covers ongoing conduct and counterparty duties we only monitor. The target is roughly 15–30% of open items High. Existing items keep their risk until someone changes it, because capture never overwrites `Risk`.
