# Obligation Types seed catalogue

The 37 rows `setup-obligation-hub` adds to the Obligation Types list (29 Track, 5 Exclude, 3 Hold for review). The same rows are in the kit's `seed/obligation-types.json`.

How to seed:
- Add a row only if no existing row has the same `Title` (ignore case). Never change or delete existing rows: the site owner may have edited them.
- Copy each value exactly. In `Examples`, separate examples are joined with a space, a vertical bar and a space; the bar is escaped as "\|" in the tables below only so the table renders. Write a plain bar.
- Write the rows in batches.

How capture uses them: `Handling` decides whether a matching clause is tracked, excluded or held for review; `DefaultRecurrence` fills in a missing schedule; `DefaultRisk` only settles an item that `capture-obligations`' risk rule (by consequence) leaves open. The site owner can add or edit types at any time (set Handling to Exclude to stop tracking a kind of clause); capture reads the list on every run.

## Payment

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 1 | Payments we owe | Track | Medium | None | Fees, rent, interest, support fees, repayments or milestone payments we must pay, with amount and due date or schedule. Merge late charges into the same item. | Licensee shall pay the annual fee on or before the first day of each contract year. \| Borrower shall repay all advances on the maturity date. |
| 2 | Payments owed to us | Track | Medium | None | The counterparty's payment terms on our invoices. Party Counterparty, so receivables can be chased. | Customer shall pay each undisputed invoice within thirty (30) days after receipt. |
| 3 | Rebates, fund contributions, true-ups and deposit top-ups | Track | Medium | Quarterly | Calculated payments tied to a period or event: volume rebates, marketing fund contributions, true-up invoices, restoring a security deposit. | Within 45 days after each quarter, pay the rebate earned for that quarter with a calculation statement. |
| 4 | Supplier price-increase limits and notice | Track | Medium | None | The other side may raise what we pay only within a cap and after notice. Counterparty, Event-driven. | Provider may increase fees once per year by up to 5% on 60 days' prior written notice. |

## Reporting

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 5 | Periodic operational report | Track | Medium | Quarterly | Recurring service-level, sales, inventory or usage reports due after each period. | Within 20 days after each calendar quarter, deliver a report of net sales and inventory on hand. |
| 6 | Financial statements and compliance certificates | Track | High | Quarterly | Lender or investor reporting: periodic financial statements and officer-signed compliance certificates. | Within 45 days after each fiscal quarter, deliver a compliance certificate signed by the CFO. |

## Notice & renewal

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 7 | Non-renewal notice before automatic renewal | Track | High | Annual | Last day to stop an auto-renewing contract or service. Due date = term end minus the notice period. | Either party may give notice of non-renewal at least 90 days before the end of the then-current term. |
| 8 | Renewal, extension or transition option window | Track | High | None | A right that lapses unless exercised by a deadline or inside a window (renewal or extension option, transition assistance request). Due date = last day; note when the window opens. | Tenant may exercise the option by notice no earlier than 12 and no later than 9 months before expiration. |
| 9 | Renewal decision before fixed expiry | Track | High | None | A contract that ends on a date without automatic renewal: decide and sign any renewal before expiry. Created when expiry is within 12 months. | This agreement expires on its stated date and may be renewed only by a written agreement signed before then. |
| 10 | Termination for convenience notice | Track | Medium | None | Notice either party must give to end the contract without cause. Event-driven. | Either party may terminate this agreement for convenience on 60 days' prior written notice. |
| 11 | Fee-increase notice we must give | Track | High | Annual | Our price increase at renewal is valid only if notice is given by a deadline. | Supplier may increase fees for a renewal term by giving notice at least 60 days before that term starts. |
| 12 | Change-of-control or assignment notice | Track | High | None | Notice due after a change of control, merger or assignment. Event-driven. | Distributor shall notify Supplier in writing within 30 days after any change of control. |

## Compliance & audit

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 13 | Audit cooperation | Track | Medium | None | The other side's audit right creates our duty to cooperate after their notice. Our own discretionary audit rights are not tracked. | On 30 days' notice, Customer may audit Supplier's records once per year; Supplier shall cooperate. |
| 14 | License usage certification or true-up | Track | Medium | Annual | Periodic certification of users, seats or volumes, and payment for any excess. | Within 30 days after each anniversary, certify the peak number of named users. |
| 15 | Compliance deliverables: certificates, attestations and plans | Track | Medium | None | Reports, certificates or plans due on a date or each year: SOC reports, inspection or permit certificates, continuity or security plans. The other side's delivery is Counterparty. | Processor shall deliver an updated SOC 2 Type II report by October 1 each year. \| Within 60 days, deliver an updated disaster recovery plan. |
| 16 | Restrictive covenants and pricing commitments | Track | Low | None | Standing restrictions to monitor: exclusivity, non-compete, license-use limits, most-favoured pricing and the duty to extend better pricing. | Licensee shall not permit any affiliate or third party to use the software. |
| 17 | Financial covenants and default notices | Track | High | None | Minimum liquidity or ratio covenants, and notifying a lender or counterparty of a default within a set time. | Borrower shall notify the bank within five business days after becoming aware of any default. |
| 18 | Indemnity claim notices and defense procedures | Hold for review | Medium | None | Procedural duties after a third-party claim (prompt notice, defense, cooperation); Legal decides case by case. | The indemnified party shall promptly notify the indemnifying party of any claim. |

## Service levels

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 19 | Service-level commitment | Track | Low | None | Measurable service levels (availability %, response or resolution times), ours or the other side's. Ongoing. | Provider shall maintain monthly availability of at least 99.9%. |
| 20 | Service credits: issue or claim within the window | Track | Medium | None | Credits we must issue after a miss, or credits we must claim before the window closes. | To receive a service credit, Customer must submit a claim within 30 days after the end of the month. |

## Insurance

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 21 | Maintain insurance and deliver certificates | Track | Medium | Annual | Keep required coverage and deliver certificates or endorsements by a date or each year. One item, dated by the certificate. | Maintain general liability insurance and deliver a certificate of insurance by January 15 each year. |

## Data & confidentiality

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 22 | Confidentiality | Track | Low | None | Protect the other side's confidential information during the term and any survival period. Usually Both, Ongoing. | Each party shall hold the other party's confidential information in confidence. |
| 23 | Personal data breach notification | Track | High | None | Notify of a personal data or security breach within a set time. Event-driven. | Processor shall notify Controller of any personal data breach within 48 hours after becoming aware of it. |
| 24 | Sub-processor notice and objection window | Track | Medium | None | The processor's advance notice of new sub-processors, and our window to object. | Controller may object in writing within 15 days after receiving notice of a new sub-processor. |
| 25 | Record retention and end-of-term data return | Hold for review | Medium | None | Keep records for a period, or return or delete data at the end of the contract; often defined in another document. | Upon termination, Processor shall return or delete all personal data within 30 days. |

## Purchasing & volume

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 26 | Minimum purchase or volume commitment | Track | Medium | Annual | Minimum spend or volume per period; a shortfall triggers a remedy. | Distributor shall purchase products of at least $500,000 in each contract year. |
| 27 | Forecasts and periodic commercial reviews | Track | Medium | Monthly | Rolling forecasts and scheduled pricing or business reviews. | By the 5th of each month, provide a rolling six-month forecast. |
| 28 | Product discontinuation and last-time-buy notice | Track | Medium | None | The supplier's notice before discontinuing a product. Counterparty, Event-driven. | Supplier shall give at least 90 days' notice before discontinuing any product. |

## Other

| # | Title | Handling | DefaultRisk | DefaultRecurrence | Description | Examples |
|---|---|---|---|---|---|---|
| 29 | Defect, damage or repair notice window | Track | Medium | None | Notice we must give within a set time after delivery or discovery, or rights are lost. | Buyer shall notify Supplier of any defect within 14 days after delivery. |
| 30 | Post-signing deliverable | Track | Medium | None | A one-time commercial plan or setup task due within a set time after the effective date. | Within 90 days after the effective date, submit an initial marketing plan for approval. |
| 31 | Key personnel continuity | Track | Low | None | Named key people who may not be replaced without notice or approval. | Supplier shall not replace the named account director without Customer's prior written approval. |
| 32 | Contacts, notice addresses and invoicing logistics | Exclude | Low | None | Designating contacts, notice addresses, where invoices go, issuing our own routine invoices. Payment amounts and deadlines are tracked separately. | Each party shall designate a point of contact. \| Invoices shall be sent to the accounts payable mailbox. |
| 33 | Good-faith cooperation and general conduct | Exclude | Low | None | General promises to cooperate or act in good faith, with no action, date or deliverable. | The parties shall cooperate in good faith in the performance of this agreement. |
| 34 | Interpretive and legal boilerplate | Exclude | Low | None | Headings, counterparts, own costs, governing law, entire agreement, severability, force majeure, survival, waivers, liability caps, termination for cause, remedies. | Headings are for convenience only. \| Each party shall bear its own costs. |
| 35 | Routine service delivery and site rules | Exclude | Low | None | Uniforms, badges, site access, hours, permitted use, signage, service descriptions and general performance standards with no measurable level, trigger, date or deliverable. | Supplier staff shall wear uniforms and identification badges. \| Provider will perform the services in a professional manner. |
| 36 | Conditions met at signing | Exclude | Low | None | Payments, deposits or deliverables completed at or before signing, including conditions to effectiveness of an agreement now in effect. | As a condition to effectiveness, Borrower shall pay the facility fee on the closing date. |
| 37 | Efforts-based or third-party duties | Hold for review | Low | None | Reasonable or best efforts duties with no measurable outcome, and duties placed on affiliates, subcontractors or others who did not sign. | Reseller shall use commercially reasonable efforts to promote the products. |

Every row's `Category` is the heading it sits under.
