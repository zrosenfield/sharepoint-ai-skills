# Answer key - sample contract obligations (Northwind Traders demo kit)

Reference date ("today"): **2026-11-24** (Pacific time). All companies, people and contracts are fictional. Machine-readable version: `answer-key.json` (same rows, same order).

## Summary

- Rows: **69** in total: **55 track**, **3 hold**, **9 exclude**, **2 superseded**, across **11** documents.
- Trap rows (isTrap = true): **33** (19 of them are tracked obligations; the rest are hold/exclude/superseded).

### Tracked obligations by category

| Category | Track rows |
|---|---:|
| Compliance & audit | 13 |
| Payment | 11 |
| Notice & renewal | 9 |
| Data & confidentiality | 4 |
| Purchasing & volume | 4 |
| Reporting | 4 |
| Service levels | 4 |
| Insurance | 3 |
| Other | 3 |

### Tracked obligations by party and trigger type

| Party | Track rows |  | Trigger type | Track rows |
|---|---:|---|---|---:|
| Northwind | 39 |  | Recurring | 21 |
| Counterparty | 9 |  | Event-driven | 18 |
| Both | 7 |  | Fixed date | 9 |
|  |  |  | Ongoing | 7 |

### Due-date distribution (track rows, relative to today)

| Bucket | Rows | Obligations |
|---|---:|---|
| Overdue | 4 | Submit initial marketing plan to Tailspin (2026-09-29); Obtain Proseware's initial SOC 2 Type II report (2026-10-01); Deliver updated BCP/DR plan to Contoso (2026-10-31); Deliver insurance endorsements to Woodgrove (2026-11-14) |
| Next 14 days | 6 | Send non-renewal notice to Contoso (120 days) (2026-12-01); Pay Fabrikam monthly hosting fees (net 30) (2026-12-01); Pay monthly base rent to Alpine Ski House (2026-12-01); Pay monthly interest on Woodgrove advances (2026-12-01); Send Wide World rolling 6-month forecast by the 5th (2026-12-05); Submit annual Named User true-up report to Litware (2026-12-06) |
| 15-120 days | 12 | Maintain insurance; send Contoso COI by Dec 15 (2026-12-15); Exercise lease renewal option (window closes Dec 30) (2026-12-30); Decide on Adventure Works renewal before expiry (2026-12-31); Deliver quarterly service-level report to Contoso (2027-01-10); Maintain insurance; send landlord COI by Jan 15 (2027-01-15); Send Tailspin quarterly sales & inventory report (2027-01-20); Request Fabrikam transition assistance by deadline (2027-01-30); Send Contoso fee-increase notice 60 days pre-renewal (2027-01-31); Pay Tailspin marketing fund (2% of Net Sales) (2027-01-31); Pay Adventure Works quarterly volume rebate (2027-02-14); Deliver quarterly compliance certificate to Woodgrove (2027-02-14); Obtain Fourth Coffee food-safety certificate by Mar 1 (2027-03-01) |
| Later (>120 days) | 8 | Decide on Fabrikam renewal before 2027-03-31 expiry (2027-03-31); Meet $750K minimum annual purchase commitment (2027-06-30); Send Litware support non-renewal notice (60 days) (2027-09-07); Obtain Proseware's annual SOC 2 Type II report (2027-10-01); Deliver annual audited financials to Woodgrove (2027-10-28); Hold annual price review with Wide World by Oct 31 (2027-10-31); Pay Litware annual support fee (2027-11-06); Repay all Woodgrove advances at maturity (2029-09-15) |
| No date | 25 | Event-driven and ongoing obligations |

Buckets: Overdue = due before today; Next 14 days = today through 2026-12-08; 15-120 days = 2026-12-09 through 2027-03-24; Later = after 2027-03-24.

### Traps and what a correct extraction does

| Trap type | Rows | Correct handling |
|---|---:|---|
| amendment | 4 | Read the amendment with the base contract. Track the amended values (120-day non-renewal notice, 10-day report) from file 02 and treat the original MSA clauses (90 days, 15 days) as superseded, not as separate live obligations. |
| notice-window | 2 | Compute the window from the expiry date and track the closing date (lease option: opens 2026-09-30, closes 2026-12-30; Fabrikam transition request by 2027-01-30). Missing the window forfeits the right. |
| claim-window | 1 | Track Northwind's duty to claim the Fabrikam service credit within 30 days after month end, even though the SLA itself is Fabrikam's obligation. |
| event-driven | 6 | Capture with triggerType Event-driven, a plain-language triggerEvent and no due date (change of control, repairs, defects, sub-processor objection, MFN price match, default notice). |
| counterparty-vs-us | 5 | Assign the right party. A counterparty right (an audit) can create a Northwind duty to cooperate; counterparty duties (breach notice, price-increase notice, discontinuation notice) are tracked as Counterparty so Northwind can hold them to it. |
| fixed-expiry | 2 | A fixed end date with no auto-renewal is itself a tracked decision date (Adventure Works 2026-12-31, Fabrikam 2027-03-31). |
| prohibition | 1 | A standing restriction (no affiliate use of Litware software) is tracked as an Ongoing compliance obligation with no date. |
| routine-admin | 8 | Do not create obligations for administrative boilerplate (points of contact, invoice address, good-faith cooperation, headings, uniforms, access badges, counterparts, own costs). |
| condition-precedent | 1 | A closing-date fee that was a condition to effectiveness was satisfied at signing; do not track it as an overdue payment. |
| missing-document | 3 | A protected obligation (payment terms, data return) whose terms are only in a referenced document missing from the Contracts library: create one open item held for review (ReviewState Needs review, Confidence Low) rather than excluding it or guessing its terms. |

### Conventions used in this key

- `party` is from Northwind's point of view: Northwind = our obligation; Counterparty = the other side's obligation we monitor; Both = mutual (e.g., either party may give non-renewal notice). If your list uses "Us", map Northwind to Us.
- `nextDueDate` for Recurring rows is the next occurrence on or after today; earlier occurrences are assumed fulfilled. Overdue rows are one-time (Fixed date) obligations whose date has passed and are assumed not yet done (Contoso BCP plan, Tailspin marketing plan, Proseware initial SOC 2 report, Woodgrove insurance endorsements).
- Event-driven and Ongoing rows have no date; Event-driven rows carry a `triggerEvent`.
- `sourceClause` is verbatim text from the .docx (straight ASCII quotes; compare after collapsing whitespace). Clause numbers and captions are in `clauseRef`, not in `sourceClause`.
- Superseded rows carry the date the original clause would have produced, so a scorer can recognise (and penalise) an extraction that tracks the pre-amendment value.
- Hold rows are expected as open items with ReviewState "Needs review" (Confidence Low) and no due date. They are scored separately (held correctly x/y), not as tracked obligations and not as extras. The tables above count track rows only.
- The manifest records each document's own text (MSA notice period 90 days; Amendment notice period 120 days). The amendment controls, so the effective Contoso notice period is 120 days.
- Boilerplate that is neither an obligation nor a listed trap (governing law, limitation of liability, entire agreement, termination-for-cause rights) is not listed; an extractor should not create rows for it.

## Documents

| File | Counterparty | Northwind role | Type | Effective | Expires | Auto-renews | Notice (days) | Value (USD) | Words |
|---|---|---|---|---|---|---|---:|---:|---:|
| 01-Contoso-MSA.docx | Contoso Ltd | Supplier | Customer agreement | 2024-04-01 | 2027-03-31 | Yes | 90 | 540,000 | 1439 |
| 02-Contoso-MSA-Amendment-1.docx | Contoso Ltd | Supplier | Amendment | 2026-09-01 | 2027-03-31 | Yes | 120 |  | 916 |
| 03-Fabrikam-Cloud-Hosting-Agreement.docx | Fabrikam Inc | Customer | Supplier agreement | 2024-04-01 | 2027-03-31 | No |  | 1,386,000 | 1179 |
| 04-Tailspin-Distribution-Agreement.docx | Tailspin Toys | Distributor | Partner agreement | 2026-07-01 | 2029-06-30 | No |  | 750,000 | 1095 |
| 05-Litware-Software-License-Support.docx | Litware Inc | Licensee | License | 2025-11-06 |  | Yes | 60 | 504,000 | 1025 |
| 06-Proseware-Data-Processing-Agreement.docx | Proseware Inc | Controller | Data processing | 2026-09-01 |  | No |  |  | 990 |
| 07-Alpine-Ski-House-Office-Lease.docx | Alpine Ski House | Tenant | Lease | 2023-10-01 | 2027-09-30 | No |  | 513,000 | 972 |
| 08-Wide-World-Importers-Supply-Agreement.docx | Wide World Importers | Customer | Supplier agreement | 2025-06-01 | 2028-05-31 | No |  | 1,200,000 | 965 |
| 09-Adventure-Works-Reseller-Agreement.docx | Adventure Works Cycles | Reseller | Customer agreement | 2024-01-01 | 2026-12-31 | No |  | 800,000 | 907 |
| 10-Fourth-Coffee-Facilities-Services-Agreement.docx | Fourth Coffee | Customer | Supplier agreement | 2025-03-01 |  | No | 60 |  | 886 |
| 11-Woodgrove-Bank-Revolving-Credit-Facility.docx | Woodgrove Bank | Borrower | Financing | 2026-09-15 | 2029-09-15 | No |  | 10,000,000 | 931 |

## Answer key by contract

### 01-Contoso-MSA.docx - Master Services Agreement (Contoso Ltd)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Meet 99.5% monthly Service Portal availability | Northwind | Service levels | Ongoing | None |  | Medium | Section 4.1 |  | Keep the Contoso Service Portal available at least 99.5% of each calendar month (excluding Scheduled Maintenance). |
| 2 | track | Issue Contoso service credits for missed availability | Northwind | Service levels | Event-driven | None |  | Medium | Section 4.2 |  | Monthly Availability falls below 99.5% in a calendar month |
| 3 | track | Maintain insurance; send Contoso COI by Dec 15 | Northwind | Insurance | Recurring | Annual | 2026-12-15 (15-120 days) | Medium | Section 7.1 |  | Maintain $2M CGL and $5M tech E&O insurance during the Term and deliver a certificate of insurance to Contoso by December 15 every year. |
| 4 | track | Protect Contoso confidential information | Both | Data & confidentiality | Ongoing | None |  | Medium | Section 5.1 |  | Each party must keep the other's Confidential Information confidential, use it only for the Services and share it only on a need-to-know basis (survives 3 years after the Term). |
| 5 | track | Cooperate with Contoso audit (30 days' notice) | Northwind | Compliance & audit | Event-driven | None |  | Medium | Section 6.1 | counterparty-vs-us | Contoso gives at least 30 days' written notice of an audit (no more than once per 12 months) |
| 6 | track | Contoso to pay invoices within 45 days | Counterparty | Payment | Event-driven | None |  | Medium | Section 3.2 |  | Contoso receives a monthly Northwind invoice |
| 7 | superseded | Send non-renewal notice to Contoso (90 days) | Both | Notice & renewal | Recurring | Annual | 2026-12-31 | High | Section 9.2 | amendment | Amended by Amendment No. 1 Section 2: notice period is now 120 days (deadline 2026-12-01). Do not track the 90-day version. |
| 8 | superseded | Deliver quarterly service-level report (15 days) | Northwind | Reporting | Recurring | Quarterly | 2027-01-15 | Medium | Section 4.3 | amendment | Amended by Amendment No. 1 Section 3: report now due within 10 days after quarter end. Do not track the 15-day version. |

### 02-Contoso-MSA-Amendment-1.docx - Amendment No. 1 to Master Services Agreement (Contoso Ltd)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Send non-renewal notice to Contoso (120 days) | Both | Notice & renewal | Recurring | Annual | 2026-12-01 (Next 14 days) | High | Section 2 (amends MSA Section 9.2) | amendment | If either party does not want the MSA to auto-renew, it must give written non-renewal notice at least 120 days before the current term ends (term ends 2027-03-31, so by 2026-12-01). Otherwise the MSA renews for another year. |
| 2 | track | Deliver quarterly service-level report to Contoso | Northwind | Reporting | Recurring | Quarterly | 2027-01-10 (15-120 days) | Medium | Section 3 (amends MSA Section 4.3) | amendment | Send Contoso a written service-level report (availability, incidents, credits) within 10 days after each calendar quarter ends. |
| 3 | track | Send Contoso fee-increase notice 60 days pre-renewal | Northwind | Notice & renewal | Recurring | Annual | 2027-01-31 (15-120 days) | Medium | Section 4 (adds MSA Section 3.4) |  | To raise Fees (max 4%) for a Renewal Term starting on or after 2027-04-01, give Contoso written notice at least 60 days before that term starts (by 2027-01-31 for the 2027 renewal). |
| 4 | track | Deliver updated BCP/DR plan to Contoso | Northwind | Compliance & audit | Fixed date | None | 2026-10-31 (Overdue) | Medium | Section 5 |  | Deliver an updated business continuity and disaster recovery plan (with RTO/RPO for the Service Portal) within 60 days after the amendment date (by 2026-10-31). |

### 03-Fabrikam-Cloud-Hosting-Agreement.docx - Cloud Hosting Services Agreement (Fabrikam Inc)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Pay Fabrikam monthly hosting fees (net 30) | Northwind | Payment | Recurring | Monthly | 2026-12-01 (Next 14 days) | Medium | Section 3.2 |  | Pay each monthly hosting invoice ($38,500, issued on the 1st of the month) within 30 days after the invoice date; the next payment (2026-12-01) covers the 2026-11-01 invoice. |
| 2 | track | Fabrikam: 60 days' notice and 5% cap on price increases | Counterparty | Payment | Event-driven | None |  | Medium | Section 3.3 | counterparty-vs-us | Fabrikam proposes an increase to the Monthly Fees |
| 3 | track | Fabrikam to meet 99.9% monthly uptime | Counterparty | Service levels | Ongoing | None |  | Medium | Section 4.1 |  | Fabrikam must keep the Hosting Services at a Monthly Uptime Percentage of at least 99.9%. |
| 4 | track | Claim Fabrikam service credits within 30 days | Northwind | Service levels | Event-driven | None |  | Medium | Section 4.3 | claim-window | Monthly Uptime Percentage falls below 99.9% in a calendar month (claim due 30 days after that month ends) |
| 5 | track | Decide on Fabrikam renewal before 2027-03-31 expiry | Both | Notice & renewal | Fixed date | None | 2027-03-31 (Later (>120 days)) | High | Section 6.2 | fixed-expiry | The hosting agreement expires 2027-03-31 and renews only by a signed written agreement before then; decide whether to renew or migrate and sign any renewal before expiry. |
| 6 | track | Request Fabrikam transition assistance by deadline | Northwind | Notice & renewal | Fixed date | None | 2027-01-30 (15-120 days) | High | Section 6.3 | notice-window | To get up to 90 days of transition assistance, Northwind must request it in writing at least 60 days before the 2027-03-31 expiration (by 2027-01-30). |

### 04-Tailspin-Distribution-Agreement.docx - Exclusive Distribution Agreement (Tailspin Toys)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Meet $750K minimum annual purchase commitment | Northwind | Purchasing & volume | Recurring | Annual | 2027-06-30 (Later (>120 days)) | High | Section 3.1 |  | Buy at least $750,000 (net purchase price) of Tailspin Products in each Contract Year (July 1 - June 30); the current Contract Year ends 2027-06-30. A shortfall lets Tailspin make the appointment non-exclusive. |
| 2 | track | Send Tailspin quarterly sales & inventory report | Northwind | Reporting | Recurring | Quarterly | 2027-01-20 (15-120 days) | Medium | Section 4.1 |  | Within 20 days after each calendar quarter, send Tailspin Net Sales by Product and state plus inventory on hand. |
| 3 | track | Pay Tailspin marketing fund (2% of Net Sales) | Northwind | Payment | Recurring | Annual | 2027-01-31 (15-120 days) | Medium | Section 4.3 |  | Contribute 2% of the calendar year's Net Sales of Tailspin Products to the co-op marketing fund by January 31 of the following year. |
| 4 | track | Submit initial marketing plan to Tailspin | Northwind | Other | Fixed date | None | 2026-09-29 (Overdue) | Medium | Section 4.2 |  | Submit an 18-month marketing plan for the Territory to Tailspin for approval within 90 days after the Effective Date (by 2026-09-29). |
| 5 | track | Observe territory exclusivity (no competing products) | Both | Compliance & audit | Ongoing | None |  | Medium | Section 2.2 |  | Tailspin may not appoint another distributor in WA/OR/ID/MT, and Northwind may not market or sell Competing Products in the Territory during the Term. |
| 6 | track | Notify Tailspin of change of control within 30 days | Northwind | Notice & renewal | Event-driven | None |  | High | Section 7.2 | event-driven | Change of Control of Northwind (acquisition of >50% of voting securities, merger, or sale of substantially all assets) |
| 7 | hold | Pay Tailspin per dealer credit application terms | Northwind | Payment | Event-driven | None |  | Medium | Section 3.3 | missing-document | Protected payment obligation whose terms are only in the dealer credit application, which isn't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms. |

### 05-Litware-Software-License-Support.docx - Software License and Support Agreement (Litware Inc)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Submit annual Named User true-up report to Litware | Northwind | Compliance & audit | Recurring | Annual | 2026-12-06 (Next 14 days) | High | Section 3.2 |  | Within 30 days after each anniversary of the 2025-11-06 Effective Date, certify to Litware the peak number of Named Users in the prior Support Year (next due 2026-12-06). |
| 2 | track | Pay Litware annual support fee | Northwind | Payment | Recurring | Annual | 2027-11-06 (Later (>120 days)) | Medium | Section 4.2 |  | Pay the $84,000 annual Support Fee on or before the first day of each Support Year (next Support Year starts 2027-11-06); Litware invoices at least 45 days ahead. |
| 3 | track | Send Litware support non-renewal notice (60 days) | Northwind | Notice & renewal | Recurring | Annual | 2027-09-07 (Later (>120 days)) | Medium | Section 4.3 |  | Support auto-renews each Support Year; to stop it, give written notice at least 60 days before the next Support Year starts (by 2027-09-07). |
| 4 | track | No use of Litware software by affiliates or third parties | Northwind | Compliance & audit | Ongoing | None |  | Medium | Section 2.2 | prohibition | Do not let any Affiliate or third party access or use the Software, and do not sublicense, rent, offer it as a service or reverse engineer it. |
| 5 | track | Cooperate with Litware license audit | Northwind | Compliance & audit | Event-driven | None |  | Medium | Section 5.1 | counterparty-vs-us | Litware gives at least 15 business days' written notice of an audit (no more than once per 12 months) |
| 6 | exclude | Bear own negotiation costs | Both | Other | Ongoing | None |  | Low | Section 9.2 | routine-admin | Routine boilerplate: the costs were incurred at signing and no post-signature action, date or deliverable exists. |

### 06-Proseware-Data-Processing-Agreement.docx - Data Processing Agreement (Proseware Inc)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Proseware: notify personal data breach within 48 hours | Counterparty | Data & confidentiality | Event-driven | None |  | High | Section 4.1 | counterparty-vs-us | Proseware becomes aware of a Personal Data Breach |
| 2 | track | Object to new Proseware sub-processor within 15 days | Northwind | Data & confidentiality | Event-driven | None |  | Medium | Section 5.3 | event-driven | Northwind receives Proseware's notice of a new Sub-processor |
| 3 | track | Proseware: 30 days' notice before new sub-processor | Counterparty | Data & confidentiality | Event-driven | None |  | Medium | Section 5.2 |  | Proseware plans to engage a new Sub-processor |
| 4 | track | Obtain Proseware's initial SOC 2 Type II report | Counterparty | Compliance & audit | Fixed date | None | 2026-10-01 (Overdue) | Medium | Section 6.1 |  | Proseware must deliver its most recent SOC 2 Type II report within 30 days after the DPA Effective Date (by 2026-10-01); chase if not received. |
| 5 | track | Obtain Proseware's annual SOC 2 Type II report | Counterparty | Compliance & audit | Recurring | Annual | 2027-10-01 (Later (>120 days)) | Medium | Section 6.2 |  | After the initial report, Proseware must deliver an updated SOC 2 Type II report by October 1 every year. |
| 6 | hold | Proseware: return or delete personal data at termination | Counterparty | Data & confidentiality | Event-driven | None |  | Medium | Section 7 | missing-document | Protected data-return obligation whose terms are only in the Services Agreement (Section 11.4), which isn't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms. |

### 07-Alpine-Ski-House-Office-Lease.docx - Office Lease (Alpine Ski House)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Pay monthly base rent to Alpine Ski House | Northwind | Payment | Recurring | Monthly | 2026-12-01 (Next 14 days) | High | Section 2.1 |  | Pay $42,750 Monthly Base Rent in advance on or before the 1st of every month, without deduction (late charge after 5 days). |
| 2 | track | Restore security deposit within 10 days of demand | Northwind | Payment | Event-driven | None |  | Low | Section 3.2 |  | Landlord applies the Security Deposit to a Tenant default and sends a written demand |
| 3 | track | Exercise lease renewal option (window closes Dec 30) | Northwind | Notice & renewal | Fixed date | None | 2026-12-30 (15-120 days) | High | Section 6.2 | notice-window | To extend the lease for 5 years, deliver written notice no earlier than 2026-09-30 and no later than 2026-12-30 (12 to 9 months before the 2027-09-30 expiration). Missing the window forfeits the option. |
| 4 | track | Maintain insurance; send landlord COI by Jan 15 | Northwind | Insurance | Recurring | Annual | 2027-01-15 (15-120 days) | Medium | Section 5.1 |  | Keep $2M CGL and full-replacement property insurance in force and deliver a certificate naming the landlord as additional insured by January 15 each year. |
| 5 | track | Report needed repairs to landlord within 10 days | Northwind | Other | Event-driven | None |  | Medium | Section 4.3 | event-driven | Northwind discovers a condition in the Premises requiring repair by the landlord |

### 08-Wide-World-Importers-Supply-Agreement.docx - Supply Agreement (Wide World Importers)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Wide World: 90 days' notice before discontinuing product | Counterparty | Purchasing & volume | Event-driven | None |  | Medium | Section 2.5 | counterparty-vs-us | Wide World decides to discontinue a Product |
| 2 | track | Send Wide World rolling 6-month forecast by the 5th | Northwind | Purchasing & volume | Recurring | Monthly | 2026-12-05 (Next 14 days) | Medium | Section 2.2 |  | By the 5th of every month, send Wide World a non-binding rolling 6-month forecast for each Product. |
| 3 | track | Notify Wide World of defects within 14 days of delivery | Northwind | Other | Event-driven | None |  | High | Section 4.1 | event-driven | Each delivery of Products to Northwind (notice due within 14 days after delivery) |
| 4 | track | Hold annual price review with Wide World by Oct 31 | Both | Purchasing & volume | Recurring | Annual | 2027-10-31 (Later (>120 days)) | Low | Section 3.2 |  | Meet with Wide World by October 31 each year to review next year's Product pricing; agreed changes take effect January 1 via a signed updated Exhibit A. |
| 5 | track | Pay Wide World invoices within 45 days | Northwind | Payment | Event-driven | None |  | Medium | Section 3.3 |  | Northwind receives a Wide World invoice (issued at each delivery) |

### 09-Adventure-Works-Reseller-Agreement.docx - Reseller Agreement (Adventure Works Cycles)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Pay Adventure Works quarterly volume rebate | Northwind | Payment | Recurring | Quarterly | 2027-02-14 (15-120 days) | Medium | Section 3.2 |  | For each quarter with Net Purchases over $150,000, pay Adventure Works a 3% rebate with a calculation statement within 45 days after quarter end (Q4 2026 rebate survives expiry). |
| 2 | track | Maintain most-favored-customer pricing | Northwind | Compliance & audit | Ongoing | None |  | High | Section 4.1 |  | During the Term, Northwind's prices to Adventure Works must be no less favorable than prices offered to any Similarly Situated Customer. |
| 3 | track | Extend better pricing to Adventure Works within 30 days | Northwind | Compliance & audit | Event-driven | None |  | High | Section 4.2 | event-driven | Northwind offers more favorable Product pricing to a Similarly Situated Customer |
| 4 | track | Decide on Adventure Works renewal before expiry | Both | Notice & renewal | Fixed date | None | 2026-12-31 (15-120 days) | High | Section 5.1 | fixed-expiry | The agreement expires 2026-12-31 with no automatic renewal; any renewal needs a signed written agreement, so decide and negotiate before expiry. |
| 5 | hold | Adventure Works: pay per standard credit terms | Counterparty | Payment | Event-driven | None |  | Medium | Section 2.2 | missing-document | Protected payment obligation whose terms are only in Northwind's standard credit terms, which aren't in the Contracts library: hold one item (Needs review, Low) until someone adds the document or confirms the terms. |

### 10-Fourth-Coffee-Facilities-Services-Agreement.docx - Facilities Services Agreement (Fourth Coffee)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Give 60 days' notice to terminate for convenience | Both | Notice & renewal | Event-driven | None |  | Medium | Section 4.2 |  | Either party decides to terminate the agreement for convenience |
| 2 | track | Obtain Fourth Coffee food-safety certificate by Mar 1 | Counterparty | Compliance & audit | Recurring | Annual | 2027-03-01 (15-120 days) | Medium | Section 3.2 |  | Fourth Coffee must deliver its annual third-party food-safety inspection certificate to Northwind by March 1 each year. |
| 3 | exclude | Supplier staff wear uniforms and badges | Counterparty | Other | Ongoing | None |  | Low | Section 1.4 | routine-admin | Routine administration: no deadline, deliverable or business consequence for a contract manager to track. |
| 4 | exclude | Designate a point of contact | Both | Other | Ongoing | None |  | Low | Section 2.1 | routine-admin | Routine administration: no deadline, deliverable or business consequence for a contract manager to track. |
| 5 | exclude | Send invoices to accounts payable mailbox | Counterparty | Other | Ongoing | None |  | Low | Section 2.2 | routine-admin | Routine administration: no deadline, deliverable or business consequence for a contract manager to track. |
| 6 | exclude | Cooperate in good faith | Both | Other | Ongoing | None |  | Low | Section 2.3 | routine-admin | Routine administration: no deadline, deliverable or business consequence for a contract manager to track. |
| 7 | exclude | Issue contractor access badges to cafe staff | Northwind | Other | Ongoing | None |  | Low | Section 2.5 | routine-admin | Routine administration: no deadline, deliverable or business consequence for a contract manager to track. |
| 8 | exclude | Headings are for convenience only | Both | Other | Ongoing | None |  | Low | Section 5.1 | routine-admin | Interpretive boilerplate, not an obligation of either party. |

### 11-Woodgrove-Bank-Revolving-Credit-Facility.docx - Revolving Credit Facility Letter Agreement (Woodgrove Bank)

| # | Expected | Title | Party | Category | Trigger | Recurrence | Next due | Risk | Clause | Trap | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | track | Deliver quarterly compliance certificate to Woodgrove | Northwind | Reporting | Recurring | Quarterly | 2027-02-14 (15-120 days) | High | Section 3.1 |  | Within 45 days after each fiscal quarter end (starting with the quarter ending 2026-12-31), deliver a CFO-signed compliance certificate and unaudited quarterly financials (first due 2027-02-14). |
| 2 | track | Deliver annual audited financials to Woodgrove | Northwind | Reporting | Recurring | Annual | 2027-10-28 (Later (>120 days)) | High | Section 3.2 |  | Within 120 days after each June 30 fiscal year end (starting FY ending 2027-06-30), deliver unqualified audited consolidated financial statements (first due 2027-10-28). |
| 3 | track | Maintain minimum liquidity of $5,000,000 | Northwind | Compliance & audit | Ongoing | None |  | High | Section 4.1 |  | Keep unrestricted cash held at Woodgrove of at least $5,000,000 at all times (tested each quarter end). |
| 4 | track | Notify Woodgrove of any default within 5 business days | Northwind | Compliance & audit | Event-driven | None |  | High | Section 3.3 | event-driven | Any Northwind officer becomes aware of a Default or Event of Default |
| 5 | track | Pay monthly interest on Woodgrove advances | Northwind | Payment | Recurring | Monthly | 2026-12-01 (Next 14 days) | High | Section 2.2 |  | Pay accrued interest on outstanding Advances monthly in arrears on the 1st of each month. |
| 6 | track | Repay all Woodgrove advances at maturity | Northwind | Payment | Fixed date | None | 2029-09-15 (Later (>120 days)) | High | Section 2.3 |  | Repay all outstanding Advances plus accrued interest on the Maturity Date (2029-09-15). |
| 7 | track | Deliver insurance endorsements to Woodgrove | Northwind | Insurance | Fixed date | None | 2026-11-14 (Overdue) | High | Section 5.1 |  | Post-closing: deliver lender's loss payable and additional insured endorsements on property and liability policies within 60 days after the 2026-09-15 Closing Date (by 2026-11-14). |
| 8 | exclude | Pay facility and legal fees at closing | Northwind | Payment | Fixed date | None | 2026-09-15 | Low | Section 2.4 | condition-precedent | Condition to effectiveness satisfied at closing on 2026-09-15 (the facility is in effect); no post-signature action remains. |
| 9 | exclude | Counterparts clause | Both | Other | Ongoing | None |  | Low | Section 7.2 | routine-admin | Routine boilerplate about how the agreement is signed; no obligation to track. |
