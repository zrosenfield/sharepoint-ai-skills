# Northwind Cloud publishing standards

These rules govern every asset submitted to **Content Intake**. The `review-submission` skill checks each rule and
labels every issue **Fixable** (the agent may correct it) or **Blocker** (a person must resolve it).

| # | Rule | Fixable when | Blocker when |
|---|------|--------------|--------------|
| 1 | Current product names only: Northwind Data Platform, Northwind AI Studio, Northwind Secure Access, Northwind Field Service, Northwind Analytics | A retired name appears: Northwind DataHub -> Northwind Data Platform; SecureGate -> Northwind Secure Access; Northwind Insights -> Northwind Analytics | Never |
| 2 | Every statistic, percentage or ROI claim cites a source on the same slide or page | The source exists elsewhere in the file or in an approved Content Library asset | No source can be found: the claim must be removed or sourced by the owner |
| 3 | No internal pricing, discount levels, roadmap dates, or "Internal only"/"Confidential" text in content whose requested shareability is Customer-shareable or Public | The internal text is a footer or label only and the body is customer-safe | Discounts, internal pricing or roadmap dates appear in the body |
| 4 | A named customer requires the note "Reference approved" and must appear in the Customer Stories reference list (Contoso Health, Tailspin Manufacturing, Woodgrove Financial, Wingtip Retail) | Customer is on the list but the note is missing | Customer is not on the list |
| 5 | Competitor mentions are factual and never disparaging | Wording can be neutralized ("50% lower cost than competitors" -> remove or replace with a sourced Northwind proof point) | Legal claims about a named competitor |
| 6 | Customer-facing files include the line "Northwind Cloud confidential. Subject to change." | Missing: add it to the footer or final slide | Never |
| 7 | No personal data: personal phone numbers, personal email addresses, home addresses | Never | Always: the submitter must remove it |
| 8 | Every slide or section has a title; images have alt text | Missing titles or alt text | Never |
| 9 | Metadata is complete: asset type, solution area, products, audience, sales stage, industry, shareability, proposed expiry, owner | Any field can be inferred from the content | Never |
| 10 | Not a duplicate of an existing Content Library asset | Never | Near-duplicate of a current asset: route to the owner as an update instead |

**Shareability ladder.** Internal only < Customer-shareable (NDA) < Public. The agent may lower requested shareability
(for example Public -> Internal only when internal content is present) and must say so in its findings.
