/*!
 * Obligation Hub for SharePoint: deploy script (v1.0)
 *
 * UNOFFICIAL AND UNSUPPORTED. A personal side project, not a Microsoft product, not reviewed or
 * supported by Microsoft. Read it before you run it, try it on a test site first, use at your own risk.
 *
 * What it does, on the site you run it from:
 *   - creates 7 lists and libraries: Contracts, Obligations, Obligation Owners, Obligation Types,
 *     Exclusions, Run Log, Evidence (and AgentAssets if the site doesn't have it yet)
 *   - adds their columns, views (Open by due date, Triggered and ongoing, My obligations, Calendar...)
 *     and the colour formatting for Status, Timing, Risk and Review
 *   - seeds Obligation Types (37 rows) and a default routing rule that makes you the owner
 *   - uploads the hub's site skills to AgentAssets/Skills, SHAREPOINT.md to the AgentAssets root and
 *     AgentAssets/Config/hub-settings.json
 *   - optionally loads fictional sample data: 11 Word contracts, 60 pre-captured obligations and
 *     13 Run Log rows labelled "Demo seed", all flagged IsSample = Yes
 *   - optionally uploads and publishes 7 HTML pages to Site Pages (Home, My obligations, Contract 360,
 *     Review queue, Leadership, Settings, How it works), and optionally makes Home.html the home page
 *   - if you're a site owner: adds the hub links to the site navigation (the pages have no navigation
 *     of their own), applies the "Obligation Hub" theme, sets the hub logo and a compact header
 *   - prints the finishing touches that have no REST API: 6 AI workflows, 3 quick steps, autofill
 *
 * What it needs: permission to create lists on the site (site owner, or a member with edit rights).
 * The site's look (navigation, theme, logo, header) needs a site owner and is skipped for anyone else. No tenant admin, no app registration, no PowerShell.
 * It runs in your browser as you, using SharePoint's own REST API, so it can only do what you can
 * already do by hand. It reads the kit's files (spec, pages, skills, sample contracts) from
 * assetsBaseUrl; a copy of the spec is embedded, so the lists still get built if that fetch fails.
 *
 * How to run: open the site's home page, press F12 (or Ctrl+Shift+I), open the Console tab, paste
 * this whole file and press Enter. If the browser asks you to type "allow pasting", do that first.
 * Undo: run remove-obligation-hub.js the same way (it moves everything to the site recycle bin).
 */
(async function obligationHubDeploy() {
  "use strict";

  // ---- Options: change these before you paste if you like -------------------------------------
  const OPTIONS = {
    assetsBaseUrl: "https://raw.githubusercontent.com/zrosenfield/sharepoint-ai-skills/master", // repo root
    sampleData: true,          // 11 fictional contracts (with key terms) and 2 example routing rules
    preCapturedSample: true,   // with sampleData: 60 obligations + 13 Run Log rows, so the hub is full before any workflow runs
    shiftDatesToToday: false,  // move every sample date by (today - 2026-11-24); the text inside the Word files doesn't move
    pages: true,               // upload the 7 hub pages to Site Pages
    publishPages: true,        // publish them (uploaded pages are drafts until published)
    setHome: false,            // make SitePages/Home.html the site's home page (changes what everyone lands on)
    siteChrome: true,          // the site's look (site owners only): hub links in the site navigation, theme, logo, compact header
    replaceNavigation: false,  // with siteChrome: also remove the site's default Documents, Pages and Site contents links (never other links)
    applyTheme: true,          // with siteChrome: apply the "Obligation Hub" theme
    setLogo: true,             // with siteChrome: upload the hub logo to Site Assets and make it the site logo
    compactHeader: true,       // with siteChrome: compact header, no background emphasis
    companyName: "",           // your legal name as written in your contracts; "" = Northwind Traders, Inc. with sample data, otherwise you're asked
    leadershipEmails: [],      // who gets the Friday leadership digest; [] = you
    pagesOnly: false,          // true = only (re)install the pages and the site's look on a site that already has the hub lists
    resume: false              // true = continue a run that stopped part-way (reuses hub lists, skips what already exists)
  };

  const SPEC_EMBEDDED = /*SPEC-BEGIN*/{"$comment":"Obligation Hub for SharePoint: the single source of truth for deploy-obligation-hub.js (which embeds a copy), remove-obligation-hub.js and cowork/build_jobs.py. Paths are relative to the repository root; list URLs are site-relative; {{TOKENS}} are filled at install time. Change this file first, then run node deploy/sync-embedded-spec.js to refresh the embedded copies.","solution":{"name":"obligation-hub-for-sharepoint","title":"Obligation Hub for SharePoint","short":"obligation-hub","version":"1.0.0","status":"experimental","kitPath":"solutions/obligation-hub-for-sharepoint","referenceDate":"2026-11-24","logTag":"Obligation Hub"},"tokens":[{"token":"{{OUR_COMPANY}}","meaning":"Legal name of the company that owns the hub, as written in its contracts.","kind":"text","usedIn":["Config/hub-settings.json","autofill prompts"]},{"token":"{{SITE_URL}}","meaning":"Absolute site URL, no trailing slash.","kind":"url","usedIn":["Config/hub-settings.json","pages","sample obligations ContractLink"]},{"token":"{{LEADERSHIP_EMAILS}}","meaning":"Leadership digest recipients (defaults to the installer).","kind":"text","usedIn":["Config/hub-settings.json"]},{"token":"{{CURRENT_USER}}","meaning":"The person running the installer (Person fields).","kind":"text","usedIn":["Obligation Owners seed","sample contracts ContractOwner","sample obligations Owner"]}],"lists":[{"key":"contracts","title":"Contracts","url":"Contracts","template":"DocumentLibrary","baseTemplate":101,"description":"Signed contracts and amendments. Key terms fill in automatically; adding or changing a contract starts obligation capture.","navLink":true,"titleDisplayName":"Contract title","ifExists":"refuse","builtInView":"All Documents","columns":[{"internalName":"Counterparty","displayName":"Counterparty","type":"Text","required":false,"autofillPrompt":"The legal name of the other party to this contract, i.e. the party that is not {{OUR_COMPANY}}. Use the name exactly as written in the parties block."},{"internalName":"ContractType","displayName":"Contract type","type":"Choice","choices":["Customer agreement","Supplier agreement","Partner agreement","License","Lease","Financing","Data processing","Amendment","Other"],"required":false,"autofillPrompt":"Classify the document from {{OUR_COMPANY}}'s point of view: Customer agreement if {{OUR_COMPANY}} provides goods or services to the other party; Supplier agreement if {{OUR_COMPANY}} buys from them; Partner agreement for distribution, reseller or alliance deals; License, Lease, Financing or Data processing when that is the main subject; Amendment if the document amends an earlier agreement; otherwise Other."},{"internalName":"EffectiveDate","displayName":"Effective date","type":"DateTime","required":false,"format":"DateOnly","autofillPrompt":"The effective date of this agreement (or of this amendment). Return only the date."},{"internalName":"ExpirationDate","displayName":"Expiration date","type":"DateTime","required":false,"format":"DateOnly","autofillPrompt":"The date the current term ends. If the contract states a term length instead of an end date, compute the end date from the effective date. Leave empty if the agreement has no fixed end."},{"internalName":"AutoRenews","displayName":"Auto-renews","type":"Choice","choices":["Yes","No","Unclear"],"required":false,"autofillPrompt":"Yes if the term renews automatically unless a party gives notice; No if it simply expires or renews only by mutual agreement; Unclear otherwise."},{"internalName":"NoticePeriodDays","displayName":"Notice period (days)","type":"Number","required":false,"autofillPrompt":"The number of days of advance written notice required to prevent renewal or to terminate at the end of the term. Convert months to days (1 month = 30 days). Empty if none."},{"internalName":"GoverningLaw","displayName":"Governing law","type":"Text","required":false,"autofillPrompt":"The governing law jurisdiction, e.g. 'Washington, USA'."},{"internalName":"ContractValue","displayName":"Contract value","type":"Currency","required":false,"autofillPrompt":"The total or annual contract value in US dollars if stated; empty if not stated."},{"internalName":"ContractSummary","displayName":"Summary","type":"Note","required":false,"richText":false,"unlimitedLength":true,"autofillPrompt":"Two plain-language sentences, under 250 characters in total: what the contract is for and the most important dates or commitments."},{"internalName":"ContractOwner","displayName":"Contract owner","type":"User","required":false},{"internalName":"BusinessUnit","displayName":"Business unit","type":"Choice","choices":["Sales","Procurement","Finance","Legal","IT","Facilities","Operations"],"required":false},{"internalName":"Amends","displayName":"Amends","type":"Text","required":false},{"internalName":"IsSample","displayName":"Sample data","type":"Boolean","default":"0","required":false}],"views":[{"name":"All contracts","default":true,"fields":["DocIcon","LinkFilename","Counterparty","ContractType","EffectiveDate","ExpirationDate","AutoRenews","NoticePeriodDays","ContractOwner","BusinessUnit"],"query":"<OrderBy><FieldRef Name='Counterparty'/></OrderBy>","rowLimit":30,"type":"list","replacesBuiltInView":true},{"name":"Expiring in 180 days","default":false,"fields":["DocIcon","LinkFilename","Counterparty","ExpirationDate","AutoRenews","NoticePeriodDays","ContractOwner"],"query":"<Where><And><IsNotNull><FieldRef Name='ExpirationDate'/></IsNotNull><Leq><FieldRef Name='ExpirationDate'/><Value Type='DateTime'><Today OffsetDays='180'/></Value></Leq></And></Where><OrderBy><FieldRef Name='ExpirationDate'/></OrderBy>","rowLimit":30,"type":"list"}]},{"key":"obligations","title":"Obligations","url":"Lists/Obligations","template":"GenericList","baseTemplate":100,"description":"Every tracked contract obligation: who owes what, by when, and what triggers it.","navLink":true,"titleDisplayName":"Obligation","ifExists":"refuse","builtInView":"All Items","columns":[{"internalName":"ContractName","displayName":"Contract","type":"Text","required":false},{"internalName":"ContractLink","displayName":"Contract link","type":"URL","required":false,"format":"Hyperlink"},{"internalName":"Counterparty","displayName":"Counterparty","type":"Text","required":false},{"internalName":"ObligationText","displayName":"What must happen","type":"Note","required":false,"richText":false},{"internalName":"ClauseRef","displayName":"Clause","type":"Text","required":false},{"internalName":"SourceClause","displayName":"Source clause","type":"Note","required":false,"richText":false},{"internalName":"Party","displayName":"Who owes it","type":"Choice","choices":["Us","Counterparty","Both"],"default":"Us","required":false},{"internalName":"Category","displayName":"Category","type":"Choice","choices":["Payment","Reporting","Notice & renewal","Compliance & audit","Service levels","Insurance","Data & confidentiality","Purchasing & volume","Other"],"required":false},{"internalName":"TriggerType","displayName":"Trigger","type":"Choice","choices":["Fixed date","Recurring","Event-driven","Ongoing"],"required":false},{"internalName":"Recurrence","displayName":"Recurrence","type":"Choice","choices":["None","Weekly","Monthly","Quarterly","Semi-annual","Annual"],"default":"None","required":false},{"internalName":"DueDate","displayName":"Due date","type":"DateTime","required":false,"format":"DateOnly"},{"internalName":"TriggerEvent","displayName":"Trigger event","type":"Text","required":false},{"internalName":"Owner","displayName":"Owner","type":"User","required":false},{"internalName":"EscalationOwner","displayName":"Escalation owner","type":"User","required":false},{"internalName":"BusinessUnit","displayName":"Business unit","type":"Choice","choices":["Sales","Procurement","Finance","Legal","IT","Facilities","Operations"],"required":false},{"internalName":"Status","displayName":"Status","type":"Choice","choices":["Not started","In progress","Fulfilled","Waived","Not applicable"],"default":"Not started","required":false,"formatter":"formats/Status.json"},{"internalName":"Timing","displayName":"Timing","type":"Choice","choices":["Overdue","Due soon","Upcoming","No date","Closed"],"required":false,"formatter":"formats/Timing.json"},{"internalName":"ReviewState","displayName":"Review","type":"Choice","choices":["Confirmed","Needs review"],"default":"Needs review","required":false,"formatter":"formats/ReviewState.json"},{"internalName":"Confidence","displayName":"Confidence","type":"Choice","choices":["High","Medium","Low"],"required":false},{"internalName":"Risk","displayName":"Risk","type":"Choice","choices":["High","Medium","Low"],"default":"Medium","required":false,"formatter":"formats/Risk.json"},{"internalName":"FulfilledOn","displayName":"Fulfilled on","type":"DateTime","required":false,"format":"DateOnly"},{"internalName":"Evidence","displayName":"Evidence","type":"URL","required":false,"format":"Hyperlink"},{"internalName":"LastReminded","displayName":"Last reminded","type":"DateTime","required":false,"format":"DateOnly"},{"internalName":"CaptureKey","displayName":"Capture key","type":"Text","required":false},{"internalName":"Notes","displayName":"Notes","type":"Note","required":false,"richText":false},{"internalName":"IsSample","displayName":"Sample data","type":"Boolean","default":"0","required":false}],"views":[{"name":"Open by due date","default":true,"fields":["LinkTitle","Counterparty","Category","DueDate","Timing","Status","Owner","Party","Risk","ReviewState"],"query":"<Where><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Fulfilled</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Waived</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Not applicable</Value></Neq><IsNotNull><FieldRef Name='DueDate'/></IsNotNull></And></And></And></Where><OrderBy><FieldRef Name='DueDate' Ascending='TRUE'/></OrderBy>","rowLimit":100,"type":"list"},{"name":"Triggered and ongoing","default":false,"fields":["LinkTitle","Counterparty","Category","TriggerType","TriggerEvent","Owner","Party","Risk","ReviewState"],"query":"<Where><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Fulfilled</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Waived</Value></Neq><And><Neq><FieldRef Name='Status'/><Value Type='Choice'>Not applicable</Value></Neq><IsNull><FieldRef Name='DueDate'/></IsNull></And></And></And></Where><OrderBy><FieldRef Name='Counterparty'/></OrderBy>","rowLimit":100,"type":"list"},{"name":"My obligations","default":false,"fields":["LinkTitle","Counterparty","Category","DueDate","Timing","Status","Risk"],"query":"<Where><Eq><FieldRef Name='Owner'/><Value Type='User'><UserID/></Value></Eq></Where><OrderBy><FieldRef Name='DueDate' Ascending='TRUE'/></OrderBy>","rowLimit":30,"type":"list"},{"name":"Needs owner","default":false,"fields":["LinkTitle","Counterparty","Category","BusinessUnit","DueDate","Risk"],"query":"<Where><IsNull><FieldRef Name='Owner'/></IsNull></Where><OrderBy><FieldRef Name='DueDate'/></OrderBy>","rowLimit":30,"type":"list"},{"name":"Needs review","default":false,"fields":["LinkTitle","Counterparty","ClauseRef","Category","Confidence","DueDate","Notes"],"query":"<Where><Eq><FieldRef Name='ReviewState'/><Value Type='Choice'>Needs review</Value></Eq></Where>","rowLimit":30,"type":"list"},{"name":"By contract","default":false,"fields":["LinkTitle","Category","Party","DueDate","Recurrence","Status","Owner"],"query":"<GroupBy Collapse='FALSE'><FieldRef Name='ContractName'/></GroupBy><OrderBy><FieldRef Name='DueDate'/></OrderBy>","rowLimit":30,"type":"list"},{"name":"Calendar","default":false,"fields":["LinkTitle","DueDate","Counterparty","Status"],"query":"","rowLimit":30,"type":"calendar","calendar":{"startDateField":"DueDate","endDateField":"DueDate","titleField":"Title","defaultLayout":"month"}},{"name":"All obligations","default":false,"fields":["LinkTitle","Counterparty","Category","DueDate","Timing","Status","Owner","Party","Risk","ReviewState","ContractName","ClauseRef","TriggerType","Recurrence","TriggerEvent","EscalationOwner","BusinessUnit","Confidence","FulfilledOn","Evidence"],"query":"","rowLimit":30,"type":"list","replacesBuiltInView":true}]},{"key":"owners","title":"Obligation Owners","url":"Lists/Obligation Owners","template":"GenericList","baseTemplate":100,"description":"Routing rules used to assign new obligations. The most specific matching rule wins.","navLink":false,"titleDisplayName":"Rule","ifExists":"refuse","builtInView":"All Items","columns":[{"internalName":"Category","displayName":"Category","type":"Choice","choices":["Any","Payment","Reporting","Notice & renewal","Compliance & audit","Service levels","Insurance","Data & confidentiality","Purchasing & volume","Other"],"default":"Any","required":false},{"internalName":"BusinessUnit","displayName":"Business unit","type":"Choice","choices":["Any","Sales","Procurement","Finance","Legal","IT","Facilities","Operations"],"default":"Any","required":false},{"internalName":"Counterparty","displayName":"Counterparty (optional)","type":"Text","required":false},{"internalName":"Owner","displayName":"Owner","type":"User","required":false},{"internalName":"EscalationOwner","displayName":"Escalation owner","type":"User","required":false},{"internalName":"Notify","displayName":"Notify by","type":"Choice","choices":["Email","Teams","Both"],"default":"Both","required":false}],"views":[{"name":"All rules","default":true,"fields":["LinkTitle","Category","BusinessUnit","Counterparty","Owner","EscalationOwner","Notify"],"query":"","rowLimit":30,"type":"list","replacesBuiltInView":true}]},{"key":"types","title":"Obligation Types","url":"Lists/Obligation Types","template":"GenericList","baseTemplate":100,"description":"What counts as a trackable obligation. Capture uses this to classify, keep or exclude.","navLink":false,"titleDisplayName":"Obligation type","ifExists":"refuse","builtInView":"All Items","columns":[{"internalName":"Category","displayName":"Category","type":"Choice","choices":["Payment","Reporting","Notice & renewal","Compliance & audit","Service levels","Insurance","Data & confidentiality","Purchasing & volume","Other"],"required":false},{"internalName":"Handling","displayName":"Handling","type":"Choice","choices":["Track","Exclude","Hold for review"],"default":"Track","required":false},{"internalName":"DefaultRisk","displayName":"Default risk","type":"Choice","choices":["High","Medium","Low"],"default":"Medium","required":false},{"internalName":"DefaultRecurrence","displayName":"Default recurrence","type":"Choice","choices":["None","Weekly","Monthly","Quarterly","Semi-annual","Annual"],"default":"None","required":false},{"internalName":"Description","displayName":"Description","type":"Note","required":false,"richText":false},{"internalName":"Examples","displayName":"Example wording","type":"Note","required":false,"richText":false}],"views":[{"name":"All types","default":true,"fields":["LinkTitle","Category","Handling","DefaultRisk","DefaultRecurrence","Description"],"query":"<OrderBy><FieldRef Name='Category'/></OrderBy>","rowLimit":30,"type":"list","replacesBuiltInView":true}]},{"key":"exclusions","title":"Exclusions","url":"Lists/Exclusions","template":"GenericList","baseTemplate":100,"description":"Clauses or obligation patterns that should not be tracked.","navLink":false,"titleDisplayName":"Exclusion","ifExists":"refuse","builtInView":"All Items","columns":[{"internalName":"Pattern","displayName":"Clause or pattern","type":"Note","required":false,"richText":false},{"internalName":"Reason","displayName":"Reason","type":"Note","required":false,"richText":false},{"internalName":"Scope","displayName":"Scope","type":"Choice","choices":["All contracts","This contract"],"default":"This contract","required":false},{"internalName":"ContractName","displayName":"Contract","type":"Text","required":false},{"internalName":"Category","displayName":"Category","type":"Choice","choices":["Payment","Reporting","Notice & renewal","Compliance & audit","Service levels","Insurance","Data & confidentiality","Purchasing & volume","Other"],"required":false},{"internalName":"Active","displayName":"Active","type":"Boolean","default":"1","required":false}],"views":[{"name":"All exclusions","default":true,"fields":["LinkTitle","Scope","ContractName","Category","Reason","Active"],"query":"","rowLimit":30,"type":"list","replacesBuiltInView":true}]},{"key":"runlog","title":"Run Log","url":"Lists/Run Log","template":"GenericList","baseTemplate":100,"description":"Every automated run: what it did and whether it worked. Failures show on the home page.","navLink":false,"titleDisplayName":"Run","ifExists":"refuse","builtInView":"All Items","columns":[{"internalName":"Workflow","displayName":"Workflow","type":"Choice","choices":["Capture","Assign owners","Daily sweep","Owner digest","Leadership digest","Mark fulfilled","Exclude","Setup"],"required":false},{"internalName":"Outcome","displayName":"Outcome","type":"Choice","choices":["Succeeded","Partial","Failed","Skipped"],"required":false},{"internalName":"ContractName","displayName":"Contract","type":"Text","required":false},{"internalName":"ContractVersion","displayName":"Contract version","type":"Text","required":false},{"internalName":"ItemsCreated","displayName":"Created","type":"Number","required":false},{"internalName":"ItemsUpdated","displayName":"Updated","type":"Number","required":false},{"internalName":"ItemsHeld","displayName":"Held for review","type":"Number","required":false},{"internalName":"Details","displayName":"Details","type":"Note","required":false,"richText":false},{"internalName":"RunAt","displayName":"Run at","type":"DateTime","required":false,"format":"DateTime"}],"views":[{"name":"Recent runs","default":true,"fields":["LinkTitle","Workflow","Outcome","ContractName","ItemsCreated","ItemsUpdated","ItemsHeld","RunAt"],"query":"<OrderBy><FieldRef Name='Created' Ascending='FALSE'/></OrderBy>","rowLimit":30,"type":"list","replacesBuiltInView":true}]},{"key":"evidence","title":"Evidence","url":"Evidence","template":"DocumentLibrary","baseTemplate":101,"description":"Proof that obligations were fulfilled. Linked from each obligation's Evidence field.","navLink":false,"titleDisplayName":"Evidence title","ifExists":"refuse","builtInView":"All Documents","columns":[{"internalName":"IsSample","displayName":"Sample data","type":"Boolean","default":"0","required":false}],"views":[]},{"key":"agentassets","title":"AgentAssets","url":"AgentAssets","template":"DocumentLibrary","baseTemplate":101,"description":"Site skills for Copilot in SharePoint and AI workflows (Skills/<skill-name>/SKILL.md).","navLink":false,"titleDisplayName":"Asset title","ifExists":"reuse","builtInView":"All Documents","columns":[],"views":[]}],"agentAssets":{"list":"agentassets","folders":[{"path":"Skills","color":"DARK_BLUE"},{"path":"Config","color":"DARK_BLUE"}],"skillFolderColor":"LIGHT_BLUE","skillsRoot":"Skills","skills":[{"name":"capture-obligations","purpose":"Capture obligations from a contract (AI workflows: file added, file changed; quick step Re-capture obligations).","files":["SKILL.md"],"upload":true},{"name":"assign-obligation-owners","purpose":"Route unowned obligations with the Obligation Owners rules (AI workflow: daily 7 AM).","files":["SKILL.md"],"upload":true},{"name":"sweep-obligations","purpose":"Timing, roll-forward, reminders and escalation (AI workflow: daily 6 AM).","files":["SKILL.md"],"upload":true},{"name":"obligation-owner-digest","purpose":"Monday digest per owner (AI workflow: Mondays 8 AM).","files":["SKILL.md"],"upload":true},{"name":"obligation-leadership-digest","purpose":"Friday leadership digest (AI workflow: Fridays 3 PM).","files":["SKILL.md"],"upload":true},{"name":"mark-obligation-fulfilled","purpose":"Quick step Mark fulfilled: fulfil, evidence, next occurrence.","files":["SKILL.md"],"upload":true},{"name":"exclude-obligation","purpose":"Quick step Remove obligation: exclusion row, item set to Not applicable.","files":["SKILL.md"],"upload":true},{"name":"obligation-hub-guide","purpose":"Answers questions about the hub in Copilot in SharePoint.","files":["SKILL.md"],"upload":true},{"name":"clear-obligation-sample-data","purpose":"Removes items and files flagged IsSample = Yes, after confirmation.","files":["SKILL.md"],"upload":true},{"name":"setup-obligation-hub","purpose":"Installer for Copilot in SharePoint and Cowork. Not uploaded by the deploy script: the hub is already built.","files":["SKILL.md","references/formatting.md","references/obligation-types.md","references/quick-steps.md","references/schema.md"],"upload":false}],"siteContext":{"source":"solutions/obligation-hub-for-sharepoint/assets/SHAREPOINT.md","target":"SHAREPOINT.md","marker":"Obligation Hub","note":"Goes in the AgentAssets root, not in Skills/. Not overwritten if a different SHAREPOINT.md is there."},"settings":{"source":"solutions/obligation-hub-for-sharepoint/assets/hub-settings.template.json","target":"Config/hub-settings.json","defaults":{"ourCompany":"{{OUR_COMPANY}}","siteUrl":"{{SITE_URL}}","timeZone":"Pacific Standard Time","dueSoonDays":14,"escalateAfterDaysOverdue":0,"reminderCooldownDays":3,"leadershipRecipients":["{{LEADERSHIP_EMAILS}}"],"leadershipTeamsChannel":{"team":"","channel":""},"notifyDefault":"Both","captureHoldBelowConfidence":"Medium","maxDigestItems":25},"overwrite":false}},"formats":[{"list":"obligations","field":"Timing","file":"solutions/obligation-hub-for-sharepoint/formats/Timing.json"},{"list":"obligations","field":"Status","file":"solutions/obligation-hub-for-sharepoint/formats/Status.json"},{"list":"obligations","field":"Risk","file":"solutions/obligation-hub-for-sharepoint/formats/Risk.json"},{"list":"obligations","field":"ReviewState","file":"solutions/obligation-hub-for-sharepoint/formats/ReviewState.json"}],"seeds":{"obligationTypes":{"list":"types","source":"solutions/obligation-hub-for-sharepoint/seed/obligation-types.json","matchOn":"Title","rows":[{"Title":"Payments we owe","Category":"Payment","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Fees, rent, interest, support fees, repayments or milestone payments we must pay, with amount and due date or schedule. Merge late charges into the same item.","Examples":"Licensee shall pay the annual fee on or before the first day of each contract year. | Borrower shall repay all advances on the maturity date."},{"Title":"Payments owed to us","Category":"Payment","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"The counterparty's payment terms on our invoices. Party Counterparty, so receivables can be chased.","Examples":"Customer shall pay each undisputed invoice within thirty (30) days after receipt."},{"Title":"Rebates, fund contributions, true-ups and deposit top-ups","Category":"Payment","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Quarterly","Description":"Calculated payments tied to a period or event: volume rebates, marketing fund contributions, true-up invoices, restoring a security deposit.","Examples":"Within 45 days after each quarter, pay the rebate earned for that quarter with a calculation statement."},{"Title":"Supplier price-increase limits and notice","Category":"Payment","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"The other side may raise what we pay only within a cap and after notice. Counterparty, Event-driven.","Examples":"Provider may increase fees once per year by up to 5% on 60 days' prior written notice."},{"Title":"Periodic operational report","Category":"Reporting","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Quarterly","Description":"Recurring service-level, sales, inventory or usage reports due after each period.","Examples":"Within 20 days after each calendar quarter, deliver a report of net sales and inventory on hand."},{"Title":"Financial statements and compliance certificates","Category":"Reporting","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"Quarterly","Description":"Lender or investor reporting: periodic financial statements and officer-signed compliance certificates.","Examples":"Within 45 days after each fiscal quarter, deliver a compliance certificate signed by the CFO."},{"Title":"Non-renewal notice before automatic renewal","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"Annual","Description":"Last day to stop an auto-renewing contract or service. Due date = term end minus the notice period.","Examples":"Either party may give notice of non-renewal at least 90 days before the end of the then-current term."},{"Title":"Renewal, extension or transition option window","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"None","Description":"A right that lapses unless exercised by a deadline or inside a window (renewal or extension option, transition assistance request). Due date = last day; note when the window opens.","Examples":"Tenant may exercise the option by notice no earlier than 12 and no later than 9 months before expiration."},{"Title":"Renewal decision before fixed expiry","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"None","Description":"A contract that ends on a date without automatic renewal: decide and sign any renewal before expiry. Created when expiry is within 12 months.","Examples":"This agreement expires on its stated date and may be renewed only by a written agreement signed before then."},{"Title":"Termination for convenience notice","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Notice either party must give to end the contract without cause. Event-driven.","Examples":"Either party may terminate this agreement for convenience on 60 days' prior written notice."},{"Title":"Fee-increase notice we must give","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"Annual","Description":"Our price increase at renewal is valid only if notice is given by a deadline.","Examples":"Supplier may increase fees for a renewal term by giving notice at least 60 days before that term starts."},{"Title":"Change-of-control or assignment notice","Category":"Notice & renewal","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"None","Description":"Notice due after a change of control, merger or assignment. Event-driven.","Examples":"Distributor shall notify Supplier in writing within 30 days after any change of control."},{"Title":"Audit cooperation","Category":"Compliance & audit","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"The other side's audit right creates our duty to cooperate after their notice. Our own discretionary audit rights are not tracked.","Examples":"On 30 days' notice, Customer may audit Supplier's records once per year; Supplier shall cooperate."},{"Title":"License usage certification or true-up","Category":"Compliance & audit","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Annual","Description":"Periodic certification of users, seats or volumes, and payment for any excess.","Examples":"Within 30 days after each anniversary, certify the peak number of named users."},{"Title":"Compliance deliverables: certificates, attestations and plans","Category":"Compliance & audit","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Reports, certificates or plans due on a date or each year: SOC reports, inspection or permit certificates, continuity or security plans. The other side's delivery is Counterparty.","Examples":"Processor shall deliver an updated SOC 2 Type II report by October 1 each year. | Within 60 days, deliver an updated disaster recovery plan."},{"Title":"Restrictive covenants and pricing commitments","Category":"Compliance & audit","Handling":"Track","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Standing restrictions to monitor: exclusivity, non-compete, license-use limits, most-favoured pricing and the duty to extend better pricing.","Examples":"Licensee shall not permit any affiliate or third party to use the software."},{"Title":"Financial covenants and default notices","Category":"Compliance & audit","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"None","Description":"Minimum liquidity or ratio covenants, and notifying a lender or counterparty of a default within a set time.","Examples":"Borrower shall notify the bank within five business days after becoming aware of any default."},{"Title":"Service-level commitment","Category":"Service levels","Handling":"Track","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Measurable service levels (availability %, response or resolution times), ours or the other side's. Ongoing.","Examples":"Provider shall maintain monthly availability of at least 99.9%."},{"Title":"Service credits: issue or claim within the window","Category":"Service levels","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Credits we must issue after a miss, or credits we must claim before the window closes.","Examples":"To receive a service credit, Customer must submit a claim within 30 days after the end of the month."},{"Title":"Maintain insurance and deliver certificates","Category":"Insurance","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Annual","Description":"Keep required coverage and deliver certificates or endorsements by a date or each year. One item, dated by the certificate.","Examples":"Maintain general liability insurance and deliver a certificate of insurance by January 15 each year."},{"Title":"Confidentiality","Category":"Data & confidentiality","Handling":"Track","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Protect the other side's confidential information during the term and any survival period. Usually Both, Ongoing.","Examples":"Each party shall hold the other party's confidential information in confidence."},{"Title":"Personal data breach notification","Category":"Data & confidentiality","Handling":"Track","DefaultRisk":"High","DefaultRecurrence":"None","Description":"Notify of a personal data or security breach within a set time. Event-driven.","Examples":"Processor shall notify Controller of any personal data breach within 48 hours after becoming aware of it."},{"Title":"Sub-processor notice and objection window","Category":"Data & confidentiality","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"The processor's advance notice of new sub-processors, and our window to object.","Examples":"Controller may object in writing within 15 days after receiving notice of a new sub-processor."},{"Title":"Minimum purchase or volume commitment","Category":"Purchasing & volume","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Annual","Description":"Minimum spend or volume per period; a shortfall triggers a remedy.","Examples":"Distributor shall purchase products of at least $500,000 in each contract year."},{"Title":"Forecasts and periodic commercial reviews","Category":"Purchasing & volume","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"Monthly","Description":"Rolling forecasts and scheduled pricing or business reviews.","Examples":"By the 5th of each month, provide a rolling six-month forecast."},{"Title":"Product discontinuation and last-time-buy notice","Category":"Purchasing & volume","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"The supplier's notice before discontinuing a product. Counterparty, Event-driven.","Examples":"Supplier shall give at least 90 days' notice before discontinuing any product."},{"Title":"Defect, damage or repair notice window","Category":"Other","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Notice we must give within a set time after delivery or discovery, or rights are lost.","Examples":"Buyer shall notify Supplier of any defect within 14 days after delivery."},{"Title":"Post-signing deliverable","Category":"Other","Handling":"Track","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"A one-time commercial plan or setup task due within a set time after the effective date.","Examples":"Within 90 days after the effective date, submit an initial marketing plan for approval."},{"Title":"Key personnel continuity","Category":"Other","Handling":"Track","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Named key people who may not be replaced without notice or approval.","Examples":"Supplier shall not replace the named account director without Customer's prior written approval."},{"Title":"Contacts, notice addresses and invoicing logistics","Category":"Other","Handling":"Exclude","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Designating contacts, notice addresses, where invoices go, issuing our own routine invoices. Payment amounts and deadlines are tracked separately.","Examples":"Each party shall designate a point of contact. | Invoices shall be sent to the accounts payable mailbox."},{"Title":"Good-faith cooperation and general conduct","Category":"Other","Handling":"Exclude","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"General promises to cooperate or act in good faith, with no action, date or deliverable.","Examples":"The parties shall cooperate in good faith in the performance of this agreement."},{"Title":"Interpretive and legal boilerplate","Category":"Other","Handling":"Exclude","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Headings, counterparts, own costs, governing law, entire agreement, severability, force majeure, survival, waivers, liability caps, termination for cause, remedies.","Examples":"Headings are for convenience only. | Each party shall bear its own costs."},{"Title":"Routine service delivery and site rules","Category":"Other","Handling":"Exclude","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Uniforms, badges, site access, hours, permitted use, signage, service descriptions and general performance standards with no measurable level, trigger, date or deliverable.","Examples":"Supplier staff shall wear uniforms and identification badges. | Provider will perform the services in a professional manner."},{"Title":"Conditions met at signing","Category":"Other","Handling":"Exclude","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Payments, deposits or deliverables completed at or before signing, including conditions to effectiveness of an agreement now in effect.","Examples":"As a condition to effectiveness, Borrower shall pay the facility fee on the closing date."},{"Title":"Efforts-based or third-party duties","Category":"Other","Handling":"Hold for review","DefaultRisk":"Low","DefaultRecurrence":"None","Description":"Reasonable or best efforts duties with no measurable outcome, and duties placed on affiliates, subcontractors or others who did not sign.","Examples":"Reseller shall use commercially reasonable efforts to promote the products."},{"Title":"Indemnity claim notices and defense procedures","Category":"Compliance & audit","Handling":"Hold for review","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Procedural duties after a third-party claim (prompt notice, defense, cooperation); Legal decides case by case.","Examples":"The indemnified party shall promptly notify the indemnifying party of any claim."},{"Title":"Record retention and end-of-term data return","Category":"Data & confidentiality","Handling":"Hold for review","DefaultRisk":"Medium","DefaultRecurrence":"None","Description":"Keep records for a period, or return or delete data at the end of the contract; often defined in another document.","Examples":"Upon termination, Processor shall return or delete all personal data within 30 days."}]},"ownerRules":{"list":"owners","matchOn":"Title","rows":[{"Title":"Default - all obligations","Category":"Any","BusinessUnit":"Any","Counterparty":"","Owner":"{{CURRENT_USER}}","EscalationOwner":"{{CURRENT_USER}}","Notify":"Both"}],"sampleRows":[{"Title":"Finance - payments","Category":"Payment","BusinessUnit":"Any","Counterparty":"","Owner":"{{CURRENT_USER}}","EscalationOwner":"{{CURRENT_USER}}","Notify":"Both"},{"Title":"Legal - notices and renewals","Category":"Notice & renewal","BusinessUnit":"Any","Counterparty":"","Owner":"{{CURRENT_USER}}","EscalationOwner":"{{CURRENT_USER}}","Notify":"Both"}],"note":"Always adds the Any/Any default rule for the installer (unless one exists); the two example rules only with sample data."}},"pages":[{"name":"Home","title":"Obligations","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/Home.template.html","target":"SitePages/Home.html","home":true},{"name":"MyObligations","title":"My obligations","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/MyObligations.template.html","target":"SitePages/MyObligations.html","home":false},{"name":"Contract360","title":"Contract 360","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/Contract360.template.html","target":"SitePages/Contract360.html","home":false},{"name":"ReviewQueue","title":"Review queue","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/ReviewQueue.template.html","target":"SitePages/ReviewQueue.html","home":false},{"name":"Leadership","title":"Leadership","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/Leadership.template.html","target":"SitePages/Leadership.html","home":false},{"name":"Settings","title":"Settings","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/Settings.template.html","target":"SitePages/Settings.html","home":false},{"name":"HowItWorks","title":"How it works","template":"solutions/obligation-hub-for-sharepoint/deploy/pages/HowItWorks.template.html","target":"SitePages/HowItWorks.html","home":false}],"pageTokens":[{"token":"{{SITE_URL}}","value":"siteUrl","kind":"url"},{"token":"{{SITE_URL_ORIGIN}}","value":"origin","kind":"url"},{"token":"{{PAGES_URL}}","value":"siteUrl + /SitePages","kind":"url"},{"token":"{{LISTID_OBLIGATIONS}}","value":"listId:obligations","kind":"guid"},{"token":"{{LISTID_CONTRACTS}}","value":"listId:contracts","kind":"guid"},{"token":"{{LISTID_RUNLOG}}","value":"listId:runlog","kind":"guid"},{"token":"{{LISTID_OWNERS}}","value":"listId:owners","kind":"guid"},{"token":"{{LISTURL_OBLIGATIONS}}","value":"listUrl:obligations","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_CONTRACTS}}","value":"listUrl:contracts","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_RUNLOG}}","value":"listUrl:runlog","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_OWNERS}}","value":"listUrl:owners","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_TYPES}}","value":"listUrl:types","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_EXCLUSIONS}}","value":"listUrl:exclusions","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_EVIDENCE}}","value":"listUrl:evidence","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{LISTURL_AGENTASSETS}}","value":"listUrl:agentassets","kind":"path","encoding":"server-relative, each path segment percent-encoded (spaces as %20), no trailing slash"},{"token":"{{WORKFLOW_PROMPT_CAPTURE_NEW}}","value":"workflowPrompt:CAPTURE_NEW","kind":"html-text","encoding":"HTML-escape & < >"},{"token":"{{WORKFLOW_PROMPT_CAPTURE_CHANGED}}","value":"workflowPrompt:CAPTURE_CHANGED","kind":"html-text","encoding":"HTML-escape & < >"},{"token":"{{WORKFLOW_PROMPT_ASSIGN_OWNERS}}","value":"workflowPrompt:ASSIGN_OWNERS","kind":"html-text","encoding":"HTML-escape & < >"},{"token":"{{WORKFLOW_PROMPT_DAILY_SWEEP}}","value":"workflowPrompt:DAILY_SWEEP","kind":"html-text","encoding":"HTML-escape & < >"},{"token":"{{WORKFLOW_PROMPT_OWNER_DIGEST}}","value":"workflowPrompt:OWNER_DIGEST","kind":"html-text","encoding":"HTML-escape & < >"},{"token":"{{WORKFLOW_PROMPT_LEADERSHIP_DIGEST}}","value":"workflowPrompt:LEADERSHIP_DIGEST","kind":"html-text","encoding":"HTML-escape & < >"}],"site":{"navigation":{"placement":"top","nodes":[{"title":"Overview","target":"page:Home"},{"title":"My obligations","target":"page:MyObligations"},{"title":"Contracts","target":"list:contracts"},{"title":"Obligations","target":"list:obligations"},{"title":"Review","target":"page:ReviewQueue"},{"title":"Leadership","target":"page:Leadership"},{"title":"How it works","target":"page:HowItWorks"},{"title":"Settings","target":"page:Settings"}],"targets":"page:<Name> = the page in Site Pages; list:<key> = the list or library root (opens its default view)","collection":"Communication sites: the top navigation (TopNavigationBar). Team sites: the site navigation (QuickLaunch) switched to horizontal.","replaceable":[{"title":"Documents","urlPattern":"/Shared(%20| )Documents(/|$)"},{"title":"Pages","urlPattern":"/SitePages(/Forms/[^/]*)?/?$"},{"title":"Site contents","urlPattern":"/_layouts/15/viewlsts\\.aspx"}],"note":"The site navigation is the hub's only navigation; the pages have no in-page nav. Nodes with the same title and address are never added twice; other custom nodes are never removed."},"header":{"layout":"compact","headerLayout":2,"emphasis":"none","headerEmphasis":0},"theme":{"name":"Obligation Hub","basedOn":"Atmospheric Precision: graphite #111827 text, ice blue #9AC7F5 and cloud #EAF3FC accents, violet #8B83DB tertiary, white background","palette":{"themePrimary":"#2F4A6D","themeLighterAlt":"#F5F9FE","themeLighter":"#EAF3FC","themeLight":"#CFE3F9","themeTertiary":"#9AC7F5","themeSecondary":"#46648C","themeDarkAlt":"#2A4262","themeDark":"#233853","themeDarker":"#1A293D","neutralLighterAlt":"#F9FAFB","neutralLighter":"#F3F4F6","neutralLight":"#E5E7EB","neutralQuaternaryAlt":"#DDE1E7","neutralQuaternary":"#D1D5DB","neutralTertiaryAlt":"#C4C9D1","neutralTertiary":"#9CA3AF","neutralSecondary":"#4B5563","neutralPrimaryAlt":"#374151","neutralPrimary":"#111827","neutralDark":"#0B1220","black":"#030712","white":"#FFFFFF"},"accents":{"graphite":"#111827","ice":"#9AC7F5","cloud":"#EAF3FC","violet":"#8B83DB"},"contrast":{"themePrimary on white (links, buttons)":9.05,"white on themePrimary (button text)":9.05,"themeDarkAlt on white (hover)":10.22,"themeSecondary on white":6.07,"neutralPrimary on white (body text)":17.74,"neutralSecondary on white (secondary text)":7.56,"themePrimary on themeLighter (selected nav)":8.07,"neutralPrimary on neutralLighter (header band)":16.12},"note":"Applied with the ThemeManager REST API by the deploy script (site owner). There is no SharePoint IQ tool for it; on the Cowork path pick a theme by hand or run the deploy script with pagesOnly: true."},"logo":{"png":"solutions/obligation-hub-for-sharepoint/deploy/assets/obligation-hub-logo.png","svg":"solutions/obligation-hub-for-sharepoint/deploy/assets/obligation-hub-logo.svg","target":"SiteAssets/obligation-hub-logo.png"},"manual":["Navigation: Settings (gear) > Change the look > Navigation: Site navigation visible, horizontal; then Edit on the site navigation and add the links in the order of site.navigation.nodes.","Header: Settings > Change the look > Header: Layout Compact, Background (emphasis) None.","Logo: Settings > Change the look > Header > Site logo > Change, and upload deploy/assets/obligation-hub-logo.png.","Theme: Settings > Change the look > Theme. A custom theme palette can only be applied by script (deploy-obligation-hub.js with pagesOnly: true, or a tenant admin adding it as a company theme); otherwise pick the closest built-in blue theme."]},"quickSteps":[{"list":"obligations","title":"Mark fulfilled","condition":"[$Status] != 'Fulfilled'","actionType":"AskKnowledgeAgent","prompt":"Mark this obligation fulfilled using the mark-obligation-fulfilled skill.","skill":"mark-obligation-fulfilled"},{"list":"obligations","title":"Remove obligation","condition":"true","actionType":"AskKnowledgeAgent","prompt":"Remove this obligation from tracking using the exclude-obligation skill.","skill":"exclude-obligation"},{"list":"contracts","title":"Re-capture obligations","condition":"true","actionType":"AskKnowledgeAgent","prompt":"Re-capture obligations from this contract using the capture-obligations skill. Do a full capture even if the text hasn't changed.","skill":"capture-obligations"}],"workflows":[{"key":"CAPTURE_NEW","name":"Capture new contracts","trigger":"fileAdded","triggerText":"When a file is added to the Contracts library","skill":"capture-obligations","runAs":"creator","runLogWorkflow":"Capture","sends":"Nothing","prompt":"Create an AI workflow named \"Capture new contracts\" on this site. Trigger it when a file is added to the Contracts library. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. Save results without asking for confirmation. Run as me."},{"key":"CAPTURE_CHANGED","name":"Capture changed contracts","trigger":"fileChanged","triggerText":"When a file in the Contracts library is changed","skill":"capture-obligations","runAs":"creator","runLogWorkflow":"Capture","sends":"Nothing","prompt":"Create an AI workflow named \"Capture changed contracts\" on this site. Trigger it when a file in the Contracts library is changed. For each run, load the site skill capture-obligations from AgentAssets/Skills and follow it for the file that triggered the run. If the contract text is unchanged since the last capture, log the skip and stop. Save results without asking for confirmation. Run as me."},{"key":"ASSIGN_OWNERS","name":"Assign owners","trigger":"schedule","triggerText":"Every day at 7:00 AM Pacific","skill":"assign-obligation-owners","runAs":"creator","runLogWorkflow":"Assign owners","sends":"One message to each newly assigned owner","prompt":"Create an AI workflow named \"Assign owners\" on this site that runs every day at 7:00 AM Pacific time. For each run, load the site skill assign-obligation-owners from AgentAssets/Skills and follow it for the Obligations list. It may send each newly assigned owner one email or Teams message. Run as me.","schedule":"Daily 07:00 Pacific"},{"key":"DAILY_SWEEP","name":"Daily sweep","trigger":"schedule","triggerText":"Every day at 6:00 AM Pacific","skill":"sweep-obligations","runAs":"creator","runLogWorkflow":"Daily sweep","sends":"Reminders to owners; escalations to escalation owners","prompt":"Create an AI workflow named \"Daily sweep\" on this site that runs every day at 6:00 AM Pacific time. For each run, load the site skill sweep-obligations from AgentAssets/Skills and follow it for the Obligations list. It may send reminder and escalation emails or Teams messages. Run as me.","schedule":"Daily 06:00 Pacific"},{"key":"OWNER_DIGEST","name":"Owner digest","trigger":"schedule","triggerText":"Every Monday at 8:00 AM Pacific","skill":"obligation-owner-digest","runAs":"creator","runLogWorkflow":"Owner digest","sends":"One digest per owner with items due","prompt":"Create an AI workflow named \"Owner digest\" on this site that runs every Monday at 8:00 AM Pacific time. For each run, load the site skill obligation-owner-digest from AgentAssets/Skills and follow it for the Obligations list. It may send each owner one email or Teams message. Run as me.","schedule":"Mondays 08:00 Pacific"},{"key":"LEADERSHIP_DIGEST","name":"Leadership digest","trigger":"schedule","triggerText":"Every Friday at 3:00 PM Pacific","skill":"obligation-leadership-digest","runAs":"creator","runLogWorkflow":"Leadership digest","sends":"One email to leadershipRecipients (and optional Teams post)","prompt":"Create an AI workflow named \"Leadership digest\" on this site that runs every Friday at 3:00 PM Pacific time. For each run, load the site skill obligation-leadership-digest from AgentAssets/Skills and follow it. It may send one email to the leadership recipients in AgentAssets/Config/hub-settings.json and post to their Teams channel. Run as me.","schedule":"Fridays 15:00 Pacific"}],"autofill":{"list":"contracts","columns":["Counterparty","ContractType","EffectiveDate","ExpirationDate","AutoRenews","NoticePeriodDays","GoverningLaw","ContractValue","ContractSummary"],"optional":true,"note":"Autofill may not run on every tenant; capture reads the contract text itself and never depends on it.","copilotPrompt":"Turn on autofill for the Contracts library on this site. Use these existing columns and extraction prompts, keep values that are already filled in (don't overwrite), and don't create new columns:\n- Counterparty: The legal name of the other party to this contract, i.e. the party that is not {{OUR_COMPANY}}. Use the name exactly as written in the parties block.\n- ContractType: Classify the document from {{OUR_COMPANY}}'s point of view: Customer agreement if {{OUR_COMPANY}} provides goods or services to the other party; Supplier agreement if {{OUR_COMPANY}} buys from them; Partner agreement for distribution, reseller or alliance deals; License, Lease, Financing or Data processing when that is the main subject; Amendment if the document amends an earlier agreement; otherwise Other.\n- EffectiveDate: The effective date of this agreement (or of this amendment). Return only the date.\n- ExpirationDate: The date the current term ends. If the contract states a term length instead of an end date, compute the end date from the effective date. Leave empty if the agreement has no fixed end.\n- AutoRenews: Yes if the term renews automatically unless a party gives notice; No if it simply expires or renews only by mutual agreement; Unclear otherwise.\n- NoticePeriodDays: The number of days of advance written notice required to prevent renewal or to terminate at the end of the term. Convert months to days (1 month = 30 days). Empty if none.\n- GoverningLaw: The governing law jurisdiction, e.g. 'Washington, USA'.\n- ContractValue: The total or annual contract value in US dollars if stated; empty if not stated.\n- ContractSummary: Two plain-language sentences, under 250 characters in total: what the contract is for and the most important dates or commitments."},"sampleData":{"referenceDate":"2026-11-24","flagColumn":"IsSample","company":"Northwind Traders, Inc.","generator":"solutions/obligation-hub-for-sharepoint/sample-data/generator/build.py","contracts":{"list":"contracts","manifest":"solutions/obligation-hub-for-sharepoint/sample-data/contracts-manifest.json","items":[{"fileName":"01-Contoso-MSA.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/01-Contoso-MSA.docx","fields":{"Title":"Master Services Agreement","Counterparty":"Contoso Ltd","ContractType":"Customer agreement","EffectiveDate":"2024-04-01","ExpirationDate":"2027-03-31","AutoRenews":"Yes","NoticePeriodDays":90,"GoverningLaw":"Washington, USA","ContractValue":540000,"ContractSummary":"Master Services Agreement between Northwind Traders and Contoso Ltd, with Northwind as supplier. Runs to 31 March 2027 and renews automatically unless notice is given 90 days before renewal; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Sales","IsSample":true}},{"fileName":"02-Contoso-MSA-Amendment-1.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/02-Contoso-MSA-Amendment-1.docx","fields":{"Title":"Amendment No. 1 to Master Services Agreement","Counterparty":"Contoso Ltd","ContractType":"Amendment","EffectiveDate":"2026-09-01","ExpirationDate":"2027-03-31","AutoRenews":"Yes","NoticePeriodDays":120,"GoverningLaw":"Washington, USA","ContractSummary":"Amends the Master Services Agreement with Contoso Ltd, effective 1 September 2026. Runs to 31 March 2027 and renews automatically unless notice is given 120 days before renewal; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Sales","Amends":"01-Contoso-MSA.docx","IsSample":true}},{"fileName":"03-Fabrikam-Cloud-Hosting-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/03-Fabrikam-Cloud-Hosting-Agreement.docx","fields":{"Title":"Cloud Hosting Services Agreement","Counterparty":"Fabrikam Inc","ContractType":"Supplier agreement","EffectiveDate":"2024-04-01","ExpirationDate":"2027-03-31","AutoRenews":"No","GoverningLaw":"New York, USA","ContractValue":1386000,"ContractSummary":"Cloud Hosting Services Agreement between Northwind Traders and Fabrikam Inc, with Northwind as customer. Runs to 31 March 2027 and does not renew automatically; governed by the law of New York, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"IT","IsSample":true}},{"fileName":"04-Tailspin-Distribution-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/04-Tailspin-Distribution-Agreement.docx","fields":{"Title":"Exclusive Distribution Agreement","Counterparty":"Tailspin Toys","ContractType":"Partner agreement","EffectiveDate":"2026-07-01","ExpirationDate":"2029-06-30","AutoRenews":"No","GoverningLaw":"Delaware, USA","ContractValue":750000,"ContractSummary":"Exclusive Distribution Agreement between Northwind Traders and Tailspin Toys, with Northwind as distributor. Runs to 30 June 2029 and does not renew automatically; governed by the law of Delaware, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Sales","IsSample":true}},{"fileName":"05-Litware-Software-License-Support.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/05-Litware-Software-License-Support.docx","fields":{"Title":"Software License and Support Agreement","Counterparty":"Litware Inc","ContractType":"License","EffectiveDate":"2025-11-06","AutoRenews":"Yes","NoticePeriodDays":60,"GoverningLaw":"California, USA","ContractValue":504000,"ContractSummary":"Software License and Support Agreement between Northwind Traders and Litware Inc, with Northwind as licensee. Effective 6 November 2025 with no fixed end; renews automatically unless notice is given 60 days before renewal; California law.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"IT","IsSample":true}},{"fileName":"06-Proseware-Data-Processing-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/06-Proseware-Data-Processing-Agreement.docx","fields":{"Title":"Data Processing Agreement","Counterparty":"Proseware Inc","ContractType":"Data processing","EffectiveDate":"2026-09-01","AutoRenews":"No","GoverningLaw":"Washington, USA","ContractSummary":"Data Processing Agreement between Northwind Traders and Proseware Inc, with Northwind as controller. Effective from 1 September 2026 with no fixed end date and does not renew automatically; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Legal","IsSample":true}},{"fileName":"07-Alpine-Ski-House-Office-Lease.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/07-Alpine-Ski-House-Office-Lease.docx","fields":{"Title":"Office Lease","Counterparty":"Alpine Ski House","ContractType":"Lease","EffectiveDate":"2023-10-01","ExpirationDate":"2027-09-30","AutoRenews":"No","GoverningLaw":"Washington, USA","ContractValue":513000,"ContractSummary":"Office Lease between Northwind Traders and Alpine Ski House, with Northwind as tenant. Runs to 30 September 2027 and does not renew automatically; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Facilities","IsSample":true}},{"fileName":"08-Wide-World-Importers-Supply-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/08-Wide-World-Importers-Supply-Agreement.docx","fields":{"Title":"Supply Agreement","Counterparty":"Wide World Importers","ContractType":"Supplier agreement","EffectiveDate":"2025-06-01","ExpirationDate":"2028-05-31","AutoRenews":"No","GoverningLaw":"Washington, USA","ContractValue":1200000,"ContractSummary":"Supply Agreement between Northwind Traders and Wide World Importers, with Northwind as customer. Runs to 31 May 2028 and does not renew automatically; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Procurement","IsSample":true}},{"fileName":"09-Adventure-Works-Reseller-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/09-Adventure-Works-Reseller-Agreement.docx","fields":{"Title":"Reseller Agreement","Counterparty":"Adventure Works Cycles","ContractType":"Customer agreement","EffectiveDate":"2024-01-01","ExpirationDate":"2026-12-31","AutoRenews":"No","GoverningLaw":"Oregon, USA","ContractValue":800000,"ContractSummary":"Reseller Agreement between Northwind Traders and Adventure Works Cycles, with Northwind as reseller. Runs to 31 December 2026 and does not renew automatically; governed by the law of Oregon, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Sales","IsSample":true}},{"fileName":"10-Fourth-Coffee-Facilities-Services-Agreement.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/10-Fourth-Coffee-Facilities-Services-Agreement.docx","fields":{"Title":"Facilities Services Agreement","Counterparty":"Fourth Coffee","ContractType":"Supplier agreement","EffectiveDate":"2025-03-01","AutoRenews":"No","NoticePeriodDays":60,"GoverningLaw":"Washington, USA","ContractSummary":"Facilities Services Agreement between Northwind Traders and Fourth Coffee, with Northwind as customer. Effective from 1 March 2025 with no fixed end date and does not renew automatically; governed by the law of Washington, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Facilities","IsSample":true}},{"fileName":"11-Woodgrove-Bank-Revolving-Credit-Facility.docx","file":"solutions/obligation-hub-for-sharepoint/sample-data/contracts/11-Woodgrove-Bank-Revolving-Credit-Facility.docx","fields":{"Title":"Revolving Credit Facility Letter Agreement","Counterparty":"Woodgrove Bank","ContractType":"Financing","EffectiveDate":"2026-09-15","ExpirationDate":"2029-09-15","AutoRenews":"No","GoverningLaw":"New York, USA","ContractValue":10000000,"ContractSummary":"Revolving Credit Facility Letter Agreement between Northwind Traders and Woodgrove Bank, with Northwind as borrower. Runs to 15 September 2029 and does not renew automatically; governed by the law of New York, USA.","ContractOwner":"{{CURRENT_USER}}","BusinessUnit":"Finance","IsSample":true}}]},"obligations":{"list":"obligations","source":"solutions/obligation-hub-for-sharepoint/sample-data/pre-captured-obligations.json","matchOn":"CaptureKey","owner":"Owner and EscalationOwner = the installer when ReviewState is Confirmed and Status is open; held (Needs review) and closed items stay unowned.","timing":"Timing is recomputed at load time from DueDate, Status and dueSoonDays."},"runLog":{"list":"runlog","source":"solutions/obligation-hub-for-sharepoint/sample-data/run-log-seed.json","matchOn":"Title","label":"Demo seed"},"dateShift":"Optional: shift every sample date by (today - referenceDate). Dates inside the Word files do not move."},"removal":{"lists":["contracts","obligations","owners","types","exclusions","runlog","evidence"],"pages":["SitePages/Home.html","SitePages/MyObligations.html","SitePages/Contract360.html","SitePages/ReviewQueue.html","SitePages/Leadership.html","SitePages/Settings.html","SitePages/HowItWorks.html"],"skills":["capture-obligations","assign-obligation-owners","sweep-obligations","obligation-owner-digest","obligation-leadership-digest","mark-obligation-fulfilled","exclude-obligation","obligation-hub-guide","clear-obligation-sample-data","setup-obligation-hub"],"files":["Config/hub-settings.json","SHAREPOINT.md"],"resetWelcomePageFrom":"SitePages/Home.html","resetWelcomePageTo":"SitePages/Home.aspx","navigation":"Only the hub navigation links (same title and address as site.navigation.nodes) are removed.","notRemoved":["AI workflows (delete them in the site's AI workflows panel; they fail once the lists are gone)","The AgentAssets library and its Skills and Config folders","Other skills and files in AgentAssets","The site theme, logo and header layout (change them in Settings > Change the look)","Anything you added or changed by hand outside the hub lists"]}}/*SPEC-END*/;
  const FORMATS_EMBEDDED = /*FORMATS-BEGIN*/{"Timing":{"$schema":"https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json","elmType":"div","style":{"display":"flex","align-items":"center","height":"100%"},"children":[{"elmType":"span","txtContent":"=if(@currentField=='Overdue','▲ ',if(@currentField=='Due soon','◑ ',if(@currentField=='Upcoming','○ ',if(@currentField=='Closed','✓ ','')))) + @currentField","style":{"display":"=if(@currentField=='','none','inline-block')","padding":"2px 10px","border-radius":"12px","font-size":"12px","font-weight":"600","line-height":"18px","background-color":"=if(@currentField=='Overdue','#FBE4EA',if(@currentField=='Due soon','#FDF1D6',if(@currentField=='Upcoming','#EAF3FC',if(@currentField=='No date','#F1F3F6',if(@currentField=='Closed','#E6F2EC','#F1F3F6')))))","color":"=if(@currentField=='Overdue','#8A1538',if(@currentField=='Due soon','#6B4100',if(@currentField=='Upcoming','#1E3A5F',if(@currentField=='No date','#374151',if(@currentField=='Closed','#1F5135','#374151')))))"}}]},"Status":{"$schema":"https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json","elmType":"div","style":{"display":"flex","align-items":"center","height":"100%"},"children":[{"elmType":"span","txtContent":"@currentField","style":{"display":"=if(@currentField=='','none','inline-block')","padding":"2px 10px","border-radius":"12px","font-size":"12px","font-weight":"600","line-height":"18px","background-color":"=if(@currentField=='Not started','#F1F3F6',if(@currentField=='In progress','#EAF3FC',if(@currentField=='Fulfilled','#E6F2EC',if(@currentField=='Waived','#EEECFB',if(@currentField=='Not applicable','#F1F3F6','#F1F3F6')))))","color":"=if(@currentField=='Not started','#374151',if(@currentField=='In progress','#1E3A5F',if(@currentField=='Fulfilled','#1F5135',if(@currentField=='Waived','#3F3A8C',if(@currentField=='Not applicable','#374151','#374151')))))"}}]},"Risk":{"$schema":"https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json","elmType":"div","style":{"display":"flex","align-items":"center","height":"100%"},"children":[{"elmType":"span","txtContent":"@currentField","style":{"display":"=if(@currentField=='','none','inline-block')","padding":"2px 10px","border-radius":"12px","font-size":"12px","font-weight":"600","line-height":"18px","background-color":"=if(@currentField=='High','#FBE4EA',if(@currentField=='Medium','#FDF1D6',if(@currentField=='Low','#E6F2EC','#F1F3F6')))","color":"=if(@currentField=='High','#8A1538',if(@currentField=='Medium','#6B4100',if(@currentField=='Low','#1F5135','#374151')))"}}]},"ReviewState":{"$schema":"https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json","elmType":"div","style":{"display":"flex","align-items":"center","height":"100%"},"children":[{"elmType":"span","txtContent":"=if(@currentField=='Needs review','◎ ','') + @currentField","style":{"display":"=if(@currentField=='','none','inline-block')","padding":"2px 10px","border-radius":"12px","font-size":"12px","font-weight":"600","line-height":"18px","background-color":"=if(@currentField=='Needs review','#EEECFB',if(@currentField=='Confirmed','#E6F2EC','#F1F3F6'))","color":"=if(@currentField=='Needs review','#3F3A8C',if(@currentField=='Confirmed','#1F5135','#374151'))"}}]}}/*FORMATS-END*/;

  const tag = "%c[Obligation Hub]";
  const css = "color:#0f6cbd;font-weight:700";
  const log = (m) => console.log(tag + " " + m, css);
  const warn = (m) => console.warn("[Obligation Hub] " + m);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const manual = [];     // finishing touches and things to do by hand
  const missing = [];    // kit files that couldn't be fetched
  const created = [];    // what this run created, for the failure report
  let step = "starting";

  const onSite = typeof location !== "undefined" && /^https:/.test(location.origin || "");
  const pc = (typeof window !== "undefined" && window._spPageContextInfo) || null;
  const guessPath = (pc && pc.webServerRelativeUrl) || (onSite ? ((location.pathname.match(/^\/(sites|teams)\/[^/]+/i) || [""])[0]) : "");
  let base = (onSite ? location.origin : "") + (guessPath === "/" ? "" : guessPath);
  let digest = "";

  async function refreshDigest() {
    const res = await fetch(base + "/_api/contextinfo", {
      method: "POST", credentials: "same-origin", headers: { Accept: "application/json;odata=nometadata" }
    });
    if (!res.ok) throw new Error("Couldn't get a request digest from " + base + " (" + res.status + "). Open the site's home page and try again.");
    const ctx = JSON.parse(await res.text());
    digest = ctx.FormDigestValue;
    return ctx;
  }

  async function call(method, path, body, opt) {
    opt = opt || {};
    for (let attempt = 0; attempt < 6; attempt++) {
      const headers = { Accept: opt.text ? "*/*" : "application/json;odata=nometadata" };
      if (method !== "GET") headers["X-RequestDigest"] = digest;
      if (body !== undefined && !opt.raw) headers["Content-Type"] = "application/json;odata=verbose";
      if (method === "MERGE" || method === "DELETE") { headers["X-HTTP-Method"] = method; headers["IF-MATCH"] = "*"; }
      const res = await fetch(base + path, {
        method: method === "GET" ? "GET" : "POST", headers, credentials: "same-origin",
        body: body === undefined ? undefined : (opt.raw ? body : JSON.stringify(body))
      });
      if (res.status === 429 || res.status === 503) {
        const wait = Number(res.headers.get("Retry-After")) || 5;
        warn("SharePoint asked us to slow down; waiting " + wait + " s");
        await sleep(wait * 1000);
        continue;
      }
      const text = await res.text();
      if (res.status === 403 && /security validation/i.test(text) && attempt === 0) { await refreshDigest(); continue; }
      if (opt.allowMissing && (res.status === 404 || /FileNotFoundException|does not exist|ArgumentException.*List/i.test(text))) return null;
      if (!res.ok) {
        const err = new Error(method + " " + path.split("?")[0] + " failed (" + res.status + "): " + text.slice(0, 400));
        err.status = res.status; err.body = text;
        throw err;
      }
      if (opt.text) return text;
      return text ? JSON.parse(text) : {};
    }
    throw new Error("SharePoint kept throttling the request; wait a few minutes and run the script again with resume: true.");
  }

  const q = (s) => "'" + String(s).replace(/'/g, "''") + "'";
  const xml = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const htmlText = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const encPath = (p) => p.split("/").map(encodeURIComponent).join("/");
  const lp = (L) => "/_api/web/lists(guid'" + L.id + "')";
  const fileApi = (serverRel) => "/_api/web/GetFileByServerRelativePath(decodedurl=" + q(serverRel) + ")";
  const folderApi = (serverRel) => "/_api/web/GetFolderByServerRelativePath(decodedurl=" + q(serverRel) + ")";
  const replaceAll = (s, find, value) => s.split(find).join(value);
  const clean = (o) => { for (const k of Object.keys(o)) if (o[k] === null || o[k] === undefined || o[k] === "") delete o[k]; return o; };

  async function pool(items, size, fn) {
    const out = new Array(items.length);
    let next = 0;
    const worker = async () => { while (next < items.length) { const i = next++; out[i] = await fn(items[i], i); } };
    await Promise.all(Array.from({ length: Math.min(size, items.length) }, worker));
    return out;
  }

  // Kit files come from GitHub (or wherever assetsBaseUrl points). No cookies are sent there.
  const assetUrl = (path) => OPTIONS.assetsBaseUrl.replace(/\/+$/, "") + "/" + encPath(path);
  async function fetchAsset(path, kind) {
    try {
      const res = await fetch(assetUrl(path), { method: "GET", credentials: "omit", cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      return kind === "binary" ? await res.arrayBuffer() : await res.text();
    } catch (e) {
      missing.push(path + " (" + (e && e.message ? e.message : e) + ")");
      return null;
    }
  }

  try {
    // ---- 1. Where are we, who are you, what can you do? ------------------------------------------
    step = "checking the site and your permissions";
    if (!onSite) throw new Error("Run this from the browser console on a page of your SharePoint site.");
    const ctx = await refreshDigest();
    base = (ctx.WebFullUrl || base).replace(/\/+$/, "");
    const origin = base.match(/^https?:\/\/[^/]+/)[0];
    const web = await call("GET", "/_api/web?$select=Title,ServerRelativeUrl,WebTemplate");
    const me = await call("GET", "/_api/web/currentuser?$select=Id,Title,Email,UserPrincipalName");
    const perms = await call("GET", "/_api/web/effectiveBasePermissions");
    const low = Number(perms.Low);
    const has = (bit) => ((low >>> 0) & bit) !== 0;
    // ManageLists for the lists; AddListItems for files and pages (the .html pages are files in Site Pages,
    // so "add and customize pages", which most modern sites switch off, isn't needed); ManageWeb for the home page.
    const ADD_ITEMS = 0x2, MANAGE_LISTS = 0x800, MANAGE_WEB = 0x40000000;
    if (!OPTIONS.pagesOnly && !has(MANAGE_LISTS)) {
      throw new Error("You don't have permission to create lists on " + base + ". Ask a site owner to make you an owner or member, or run this on a site you own.");
    }
    if (OPTIONS.pages && !has(ADD_ITEMS)) {
      throw new Error("You can't add files or pages on " + base + ". Ask a site owner to make you a member, or set pages: false.");
    }
    if (OPTIONS.setHome && !has(MANAGE_WEB)) {
      throw new Error("Only a site owner can change the home page. Set setHome: false, or ask a site owner to run this.");
    }
    const webRel = web.ServerRelativeUrl === "/" ? "" : web.ServerRelativeUrl;
    // The site's look (navigation, theme, logo, header) needs a site owner; for anyone else it's skipped and listed as a finishing touch.
    const chromeOn = !!OPTIONS.siteChrome && has(MANAGE_WEB);

    // ---- 2. The spec: from the kit if reachable, otherwise the embedded copy ----------------------
    step = "reading the kit's spec";
    let SPEC = SPEC_EMBEDDED;
    const specText = await fetchAsset("solutions/obligation-hub-for-sharepoint/deploy/spec.json", "text");
    if (specText) {
      try {
        const s = JSON.parse(specText);
        if (s && s.solution && s.solution.name === "obligation-hub-for-sharepoint" && Array.isArray(s.lists)) SPEC = s;
      } catch (e) { warn("The kit's spec.json didn't parse; using the copy in this script."); }
    }
    if (!SPEC) throw new Error("No spec: the kit's spec.json couldn't be fetched and this copy of the script has none embedded.");
    log((SPEC === SPEC_EMBEDDED ? "Using the spec embedded in this script" : "Using spec.json from " + OPTIONS.assetsBaseUrl) + " (v" + SPEC.solution.version + ")");
    const listUrl = (L) => webRel + "/" + L.url;
    const byKey = {};
    SPEC.lists.forEach((L) => { byKey[L.key] = Object.assign({}, L); });
    const LISTS = SPEC.lists.map((L) => byKey[L.key]);

    // ---- 3. What's already here? -----------------------------------------------------------------
    step = "checking for existing hub lists";
    for (const L of LISTS) {
      const found = await call("GET", "/_api/web/GetList(@u)?@u=" + encodeURIComponent(q(listUrl(L))) + "&$select=Id,Title,ItemCount,ListItemEntityTypeFullName,BaseTemplate&$expand=RootFolder", undefined, { allowMissing: true });
      if (found) {
        L.existing = true; L.id = found.Id; L.entity = found.ListItemEntityTypeFullName;
        L.serverUrl = (found.RootFolder && found.RootFolder.ServerRelativeUrl) || listUrl(L);
      }
    }
    if (OPTIONS.pagesOnly) {
      const need = ["obligations", "contracts", "runlog", "owners"].filter((k) => !byKey[k].existing);
      if (need.length) throw new Error("pagesOnly needs the hub lists, but these aren't on " + base + ": " + need.map((k) => byKey[k].title).join(", ") + ". Install the hub first.");
    } else if (!OPTIONS.resume) {
      const clash = LISTS.filter((L) => L.existing && L.ifExists !== "reuse");
      if (clash.length) {
        throw new Error("Already on this site: " + clash.map((L) => L.title + " (" + listUrl(L) + ")").join(", ") +
          ". Nothing was changed. Run this on a site without the Obligation Hub, run remove-obligation-hub.js first, or set resume: true to finish a run that stopped part-way.");
      }
    }

    // ---- 4. Settings you choose --------------------------------------------------------------------
    const withSample = !OPTIONS.pagesOnly && !!OPTIONS.sampleData;
    const withPreCaptured = withSample && !!OPTIONS.preCapturedSample;
    let company = String(OPTIONS.companyName || "").trim();
    if (!company && !OPTIONS.pagesOnly) {
      if (withSample) company = SPEC.sampleData.company;
      else if (typeof prompt === "function") company = String(prompt("Your company's legal name, exactly as it appears in your contracts (it decides which obligations are yours):", "") || "").trim();
    }
    if (!company && !OPTIONS.pagesOnly) { log("Cancelled: no company name. Nothing was changed."); return { cancelled: true }; }
    const myEmail = me.Email || me.UserPrincipalName || "";
    const recipients = (OPTIONS.leadershipEmails && OPTIONS.leadershipEmails.length) ? OPTIONS.leadershipEmails.slice() : (myEmail ? [myEmail] : []);

    // ---- 5. Fetch the kit's files (nothing is written yet) -----------------------------------------
    step = "fetching the kit's files";
    const AA = SPEC.agentAssets;
    const kit = SPEC.solution.kitPath;
    const skillFiles = [];
    if (!OPTIONS.pagesOnly) {
      for (const s of AA.skills.filter((x) => x.upload)) for (const f of s.files) skillFiles.push({ skill: s.name, file: f, path: AA.skillsRoot + "/" + s.name + "/" + f });
    }
    const pagesToDo = OPTIONS.pages ? SPEC.pages.slice() : [];
    const fetched = { skills: {}, pages: {}, formats: {}, contracts: {} };
    let siteContext = null, settingsTemplate = null, sampleObligations = null, sampleRunLog = null;
    await pool(skillFiles, 6, async (sf) => { fetched.skills[sf.path] = await fetchAsset(sf.path, "text"); });
    await pool(pagesToDo, 4, async (p) => { fetched.pages[p.name] = await fetchAsset(p.template, "text"); });
    if (!OPTIONS.pagesOnly) {
      siteContext = await fetchAsset(AA.siteContext.source, "text");
      settingsTemplate = await fetchAsset(AA.settings.source, "text");
      await pool(SPEC.formats, 4, async (f) => {
        const t = await fetchAsset(f.file, "text");
        try { fetched.formats[f.field] = t ? JSON.parse(t) : null; } catch (e) { fetched.formats[f.field] = null; }
      });
      if (withSample) await pool(SPEC.sampleData.contracts.items, 4, async (c) => { fetched.contracts[c.fileName] = await fetchAsset(c.file, "binary"); });
      if (withPreCaptured) {
        const o = await fetchAsset(SPEC.sampleData.obligations.source, "text");
        const r = await fetchAsset(SPEC.sampleData.runLog.source, "text");
        try { sampleObligations = o ? JSON.parse(o) : null; } catch (e) { missing.push(SPEC.sampleData.obligations.source + " (didn't parse)"); }
        try { sampleRunLog = r ? JSON.parse(r) : null; } catch (e) { missing.push(SPEC.sampleData.runLog.source + " (didn't parse)"); }
      }
    }
    const SITE = SPEC.site || null;
    const logoBytes = chromeOn && SITE && OPTIONS.setLogo ? await fetchAsset(SITE.logo.png, "binary") : null;
    const nSkills = AA.skills.filter((x) => x.upload && x.files.every((f) => fetched.skills[AA.skillsRoot + "/" + x.name + "/" + f])).length;
    const nPages = pagesToDo.filter((p) => fetched.pages[p.name]).length;
    const nContracts = Object.keys(fetched.contracts).filter((k) => fetched.contracts[k]).length;
    const nTypes = SPEC.seeds.obligationTypes.rows.length;

    // ---- 6. One question, then go ------------------------------------------------------------------
    const toCreate = LISTS.filter((L) => !L.existing).map((L) => L.title);
    const look = !SITE || !OPTIONS.siteChrome ? "" : !chromeOn ? "- Site look (navigation, theme, logo, header): skipped, it needs a site owner\n"
      : "- Site look: " + SITE.navigation.nodes.length + " hub links in the site navigation" + (OPTIONS.replaceNavigation ? " (replacing the Documents, Pages and Site contents links)" : "") +
        (OPTIONS.applyTheme ? ", the Obligation Hub theme" : "") + (OPTIONS.setLogo ? ", the hub logo" : "") + (OPTIONS.compactHeader ? ", a compact header" : "") + "\n";
    const plan = OPTIONS.pagesOnly
      ? "Obligation Hub will upload " + nPages + " pages to Site Pages" + (OPTIONS.publishPages ? " and publish them" : "") +
        (OPTIONS.setHome ? ", and make Home.html the site's home page" : "") + " on:\n\n" + web.Title + "\n" + base + "\n\n" + look
      : "Obligation Hub will set up on:\n\n" + web.Title + "\n" + base + "\n\n" +
        "- Create: " + (toCreate.join(", ") || "nothing new (resuming)") + "\n" +
        "- Columns, views, formatting, " + nTypes + " obligation types and a routing rule that makes you the owner\n" +
        "- Upload " + nSkills + " skills, SHAREPOINT.md and Config/hub-settings.json to AgentAssets\n" +
        "- Company (\"Us\" in contracts): " + company + "\n" +
        "- Leadership digest to: " + (recipients.join(", ") || "nobody yet") + "\n" +
        (withSample ? "- Fictional sample data: " + nContracts + " contracts" +
          (withPreCaptured && sampleObligations ? ", " + sampleObligations.length + " obligations" : "") +
          (withPreCaptured && sampleRunLog ? ", " + sampleRunLog.length + " Run Log rows" : "") + " (flagged IsSample), with you as owner\n" : "") +
        (nPages ? "- " + nPages + " pages in Site Pages" + (OPTIONS.publishPages ? ", published" : "") + (OPTIONS.setHome ? "; Home.html becomes the home page" : "") + "\n" : "") +
        look +
        (missing.length ? "\n" + missing.length + " kit files couldn't be fetched and will be skipped (listed at the end).\n" : "");
    const go = (typeof confirm === "function") ? confirm(plan + "\n\nUnofficial, unsupported. Everything runs as you. Continue?") : true;
    if (!go) { log("Cancelled. Nothing was changed."); return { cancelled: true }; }
    log("Deploying to " + base + " as " + me.Title);

    const shift = (() => {
      if (!OPTIONS.shiftDatesToToday) return 0;
      const t = new Date();
      return Math.round((Date.UTC(t.getFullYear(), t.getMonth(), t.getDate()) - Date.parse(SPEC.sampleData.referenceDate + "T00:00:00Z")) / 86400000);
    })();
    const day = (s) => s ? new Date(Date.parse(String(s).slice(0, 10) + "T12:00:00Z") + shift * 86400000).toISOString().slice(0, 10) : null;
    const iso = (s) => s ? day(s) + "T12:00:00Z" : null;
    const counts = { listsCreated: 0, columns: 0, views: 0, formats: 0, types: 0, rules: 0, files: 0, contracts: 0, obligations: 0, runLog: 0, pages: 0, published: 0 };

    async function entityType(L) {
      if (!L.entity) L.entity = (await call("GET", lp(L) + "?$select=ListItemEntityTypeFullName")).ListItemEntityTypeFullName;
      return L.entity;
    }
    async function addItem(L, fields) {
      return call("POST", lp(L) + "/items", clean(Object.assign({ __metadata: { type: await entityType(L) } }, fields)));
    }
    async function existingValues(L, field) {
      const r = await call("GET", lp(L) + "/items?$select=" + field + "&$top=5000");
      return new Set((r.value || []).map((x) => String(x[field] == null ? "" : x[field]).toLowerCase()));
    }
    async function uploadFile(folderServerRel, name, content, overwrite) {
      return call("POST", folderApi(folderServerRel) + "/Files/AddUsingPath(decodedurl=" + q(name) + ",overwrite=" + (overwrite ? "true" : "false") + ")", content, { raw: true });
    }
    async function ensureFolder(serverRel) {
      try { await call("POST", "/_api/web/folders", { __metadata: { type: "SP.Folder" }, ServerRelativeUrl: serverRel }); }
      catch (e) { if (!/already exists/i.test(e.message)) throw e; }
    }

    if (!OPTIONS.pagesOnly) {
      // ---- 7. Lists and libraries ------------------------------------------------------------------
      step = "creating lists";
      for (const L of LISTS) {
        if (L.existing) { log((L.ifExists === "reuse" ? "Using the existing " : "Resuming with the existing ") + L.title); continue; }
        const leaf = L.url.split("/").pop();
        const made = await call("POST", "/_api/web/lists", {
          // With the site's look on, the hub's own navigation links replace the per-list links (no duplicates).
          __metadata: { type: "SP.List" }, BaseTemplate: L.baseTemplate, Title: leaf, Description: L.description, OnQuickLaunch: !!L.navLink && !chromeOn
        });
        L.id = made.Id; L.created = true; counts.listsCreated++;
        created.push((L.baseTemplate === 101 ? "library " : "list ") + L.title);
        const info = await call("GET", lp(L) + "?$select=Id,ListItemEntityTypeFullName&$expand=RootFolder");
        L.entity = info.ListItemEntityTypeFullName;
        L.serverUrl = (info.RootFolder && info.RootFolder.ServerRelativeUrl) || listUrl(L);
        if (L.title !== leaf) await call("MERGE", lp(L), { __metadata: { type: "SP.List" }, Title: L.title });
        log("Created " + L.title);
      }
      // Rename the built-in Title column on the hub's own lists (never on a library the site already had).
      for (const L of LISTS) {
        if (L.titleDisplayName && (L.created || L.ifExists !== "reuse")) {
          await call("MERGE", lp(L) + "/fields/getbyinternalnameortitle('Title')", { __metadata: { type: "SP.Field" }, Title: L.titleDisplayName });
        }
      }

      // ---- 8. Columns ------------------------------------------------------------------------------
      step = "adding columns";
      const fieldXml = (c, L) => {
        const n = xml(c.internalName);
        let a = '<Field Name="' + n + '" StaticName="' + n + '" DisplayName="' + n + '"' + (c.required ? ' Required="TRUE"' : "");
        let inner = "";
        switch (c.type) {
          case "Choice": case "MultiChoice":
            a += ' Type="' + c.type + '" FillInChoice="FALSE"' + (c.type === "Choice" ? ' Format="Dropdown"' : "");
            if (c.default) inner += "<Default>" + xml(c.default) + "</Default>";
            inner += "<CHOICES>" + c.choices.map((x) => "<CHOICE>" + xml(x) + "</CHOICE>").join("") + "</CHOICES>";
            break;
          case "User": a += ' Type="User" UserSelectionMode="PeopleOnly" UserSelectionScope="0"'; break;
          case "Currency": a += ' Type="Currency" LCID="1033" Decimals="0"'; break;
          case "Number": a += ' Type="Number" Decimals="0"'; break;
          case "Boolean": a += ' Type="Boolean"'; inner += "<Default>" + (c.default === "1" ? "1" : "0") + "</Default>"; break;
          case "DateTime": a += ' Type="DateTime" Format="' + (c.format === "DateTime" ? "DateTime" : "DateOnly") + '"'; if (c.default) inner += "<Default>" + xml(c.default) + "</Default>"; break;
          case "URL": a += ' Type="URL" Format="' + (c.format === "Image" ? "Image" : "Hyperlink") + '"'; break;
          case "Note":
            a += ' Type="Note" NumLines="6" RichText="FALSE"';
            if (L.baseTemplate === 101 || c.unlimitedLength) a += ' UnlimitedLengthInDocumentLibrary="TRUE"';
            break;
          default: a += ' Type="Text" MaxLength="255"';
        }
        return a + (inner ? ">" + inner + "</Field>" : " />");
      };
      for (const L of LISTS) {
        if (!L.columns.length) continue;
        const have = new Set(((await call("GET", lp(L) + "/fields?$select=InternalName")).value || []).map((f) => f.InternalName));
        let added = 0;
        for (const c of L.columns) {
          if (have.has(c.internalName)) continue;
          await call("POST", lp(L) + "/fields/createfieldasxml", {
            parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: fieldXml(c, L), Options: 0 }
          });
          if (c.displayName !== c.internalName) {
            await call("MERGE", lp(L) + "/fields/getbyinternalnameortitle(" + q(c.internalName) + ")", { __metadata: { type: "SP.Field" }, Title: c.displayName });
          }
          added++; counts.columns++;
        }
        log(L.title + ": " + added + " columns added" + (added < L.columns.length ? ", " + (L.columns.length - added) + " already there" : ""));
      }

      // ---- 9. Views ----------------------------------------------------------------------------------
      // The built-in "All Items"/"All Documents" view becomes the spec's "all" view, so its AllItems.aspx
      // address (which the pages link to) keeps working and there's no duplicate. The spec's default
      // view (e.g. "Open by due date", which leaves out undated items) is made the default.
      step = "adding views";
      const CAL_STYLES = '<CalendarViewStyle Title="Day" Type="day" Template="CalendarViewdayChrome" Sequence="1" Default="FALSE" />' +
        '<CalendarViewStyle Title="Week" Type="week" Template="CalendarViewweekChrome" Sequence="2" Default="FALSE" />' +
        '<CalendarViewStyle Title="Month" Type="month" Template="CalendarViewmonthChrome" Sequence="3" Default="TRUE" />';
      for (const L of LISTS) {
        if (!L.views.length) continue;
        const views = (await call("GET", lp(L) + "/views?$select=Id,Title,DefaultView,ServerRelativeUrl")).value || [];
        const byTitle = (t) => views.find((v) => v.Title === t);
        let added = 0;
        for (const V of L.views) {
          const have = byTitle(V.name);
          if (have) { V.id = have.Id; continue; }
          const builtIn = V.replacesBuiltInView ? byTitle(L.builtInView) : null;
          if (builtIn) {
            const vp = lp(L) + "/views(guid'" + builtIn.Id + "')";
            await call("MERGE", vp, { __metadata: { type: "SP.View" }, Title: V.name, ViewQuery: V.query || "", RowLimit: V.rowLimit || 30 });
            await call("POST", vp + "/ViewFields/RemoveAllViewFields");
            for (const f of V.fields) await call("POST", vp + "/ViewFields/AddViewField(" + q(f) + ")");
            builtIn.Title = V.name; V.id = builtIn.Id; added++; counts.views++;
            continue;
          }
          if (V.type === "calendar") {
            const C = V.calendar;
            const fields = [C.startDateField].concat(C.endDateField !== C.startDateField ? [C.endDateField] : [], V.fields.filter((f) => f !== C.startDateField && f !== C.endDateField));
            const titleRefs = ["CalendarMonthTitle", "CalendarWeekTitle", "CalendarWeekLocation", "CalendarDayTitle", "CalendarDayLocation"]
              .map((t) => '<FieldRef Name="' + xml(C.titleField) + '" Type="' + t + '" />').join("");
            let id = "";
            try {
              const v = await call("POST", lp(L) + "/views/add", {
                parameters: {
                  __metadata: { type: "SP.ViewCreationInformation" }, Title: V.name, ViewFields: { results: fields }, Query: V.query || "",
                  RowLimit: V.rowLimit || 30, SetAsDefaultView: false, PersonalView: false, Paged: true, ViewTypeKind: 1,
                  ViewType2: "MODERNCALENDAR", ViewData: titleRefs, CalendarViewStyles: CAL_STYLES
                }
              });
              id = v.Id;
              const chk = await call("GET", lp(L) + "/views(guid'" + id + "')?$select=ViewType2");
              if (chk.ViewType2 !== "MODERNCALENDAR") {
                await call("MERGE", lp(L) + "/views(guid'" + id + "')", { __metadata: { type: "SP.View" }, ViewType2: "MODERNCALENDAR", ViewData: titleRefs, CalendarViewStyles: CAL_STYLES });
              }
              V.id = id; added++; counts.views++;
            } catch (e) {
              if (id) { try { await call("DELETE", lp(L) + "/views(guid'" + id + "')"); } catch (e2) { /* leave it */ } }
              manual.push("Calendar view: open " + L.title + " > + Add view > Calendar, name it \"" + V.name + "\", start and end date = Due date, title = Title (the REST call was refused: " + e.message.slice(0, 120) + ")");
            }
            continue;
          }
          const v = await call("POST", lp(L) + "/views/add", {
            parameters: {
              __metadata: { type: "SP.ViewCreationInformation" }, Title: V.name, ViewFields: { results: V.fields }, Query: V.query || "",
              RowLimit: V.rowLimit || 30, SetAsDefaultView: !!V.default, PersonalView: false, Paged: true, ViewTypeKind: 1
            }
          });
          V.id = v.Id; added++; counts.views++;
        }
        const def = L.views.find((V) => V.default && V.id);
        if (def) {
          const now = (await call("GET", lp(L) + "/views(guid'" + def.id + "')?$select=DefaultView")).DefaultView;
          if (!now) await call("MERGE", lp(L) + "/views(guid'" + def.id + "')", { __metadata: { type: "SP.View" }, DefaultView: true });
        }
        log(L.title + ": " + added + " views");
      }

      // ---- 10. Column formatting -------------------------------------------------------------------
      step = "applying column formatting";
      for (const f of SPEC.formats) {
        const L = byKey[f.list];
        const json = fetched.formats[f.field] || (FORMATS_EMBEDDED && FORMATS_EMBEDDED[f.field]);
        if (!json) { manual.push("Paste " + f.file + " into " + L.title + " > " + f.field + " > Column settings > Format this column > Advanced mode"); continue; }
        try {
          await call("MERGE", lp(L) + "/fields/getbyinternalnameortitle(" + q(f.field) + ")", { __metadata: { type: "SP.Field" }, CustomFormatter: JSON.stringify(json) });
          counts.formats++;
        } catch (e) { manual.push("Paste " + f.file + " into " + L.title + " > " + f.field + " > Column settings > Format this column > Advanced mode"); }
      }
      log("Formatting applied to " + counts.formats + " columns");

      // ---- 11. Seeds: what to track, who owns it ---------------------------------------------------
      step = "seeding Obligation Types and Obligation Owners";
      const T = byKey[SPEC.seeds.obligationTypes.list];
      const haveTypes = await existingValues(T, "Title");
      for (const row of SPEC.seeds.obligationTypes.rows) {
        if (haveTypes.has(String(row.Title).toLowerCase())) continue;
        await addItem(T, row); counts.types++;
      }
      const O = byKey[SPEC.seeds.ownerRules.list];
      const rules = (await call("GET", lp(O) + "/items?$select=Title,Category,BusinessUnit,Counterparty&$top=5000")).value || [];
      const hasDefault = rules.some((r) => r.Category === "Any" && r.BusinessUnit === "Any" && !r.Counterparty);
      const ruleRows = (hasDefault ? [] : SPEC.seeds.ownerRules.rows).concat(withSample ? SPEC.seeds.ownerRules.sampleRows : []);
      for (const r of ruleRows) {
        if (rules.some((x) => String(x.Title).toLowerCase() === String(r.Title).toLowerCase())) continue;
        await addItem(O, {
          Title: r.Title, Category: r.Category, BusinessUnit: r.BusinessUnit, Counterparty: r.Counterparty,
          OwnerId: me.Id, EscalationOwnerId: me.Id, Notify: r.Notify
        });
        counts.rules++;
      }
      log("Seeded " + counts.types + " obligation types and " + counts.rules + " routing rules (you own them; change them in Obligation Owners)");

      // ---- 12. AgentAssets: skills, site context, settings -----------------------------------------
      step = "uploading skills and settings to AgentAssets";
      const A = byKey[AA.list];
      const aaRoot = A.serverUrl || listUrl(A);
      for (const f of AA.folders) await ensureFolder(aaRoot + "/" + f.path);
      for (const s of AA.skills.filter((x) => x.upload)) {
        const files = s.files.map((f) => ({ f, text: fetched.skills[AA.skillsRoot + "/" + s.name + "/" + f] }));
        if (files.some((x) => x.text == null)) { manual.push("Upload the skill folder Skills/" + s.name + "/ from the kit to AgentAssets/Skills (it couldn't be fetched)"); continue; }
        const dir = aaRoot + "/" + AA.skillsRoot + "/" + s.name;
        await ensureFolder(dir);
        for (const x of files) {
          const parts = x.f.split("/");
          const name = parts.pop();
          let folder = dir;
          for (const p of parts) { folder += "/" + p; await ensureFolder(folder); }
          await uploadFile(folder, name, x.text, true); counts.files++;
        }
      }
      if (siteContext) {
        const target = aaRoot + "/" + AA.siteContext.target;
        const current = await call("GET", fileApi(target) + "/$value", undefined, { allowMissing: true, text: true });
        if (current != null && current.indexOf(AA.siteContext.marker) < 0) {
          manual.push("AgentAssets already has a SHAREPOINT.md that isn't the hub's; it was left alone. Add the hub section from " + AA.siteContext.source + " to it by hand.");
        } else { await uploadFile(aaRoot, AA.siteContext.target, siteContext, true); counts.files++; }
      } else manual.push("Upload " + AA.siteContext.source + " to the AgentAssets library root as SHAREPOINT.md");
      let settings;
      try { settings = settingsTemplate ? JSON.parse(settingsTemplate) : null; } catch (e) { settings = null; }
      if (!settings || typeof settings !== "object") settings = JSON.parse(JSON.stringify(AA.settings.defaults));
      delete settings._tokens;
      if ("_about" in settings) settings._about = "Obligation Hub settings, filled in by deploy-obligation-hub.js on " + new Date().toISOString().slice(0, 10) + ". Every hub skill reads this file first. Keys starting with _ are ignored.";
      settings.ourCompany = company;
      settings.siteUrl = base;
      settings.leadershipRecipients = recipients;
      const settingsJson = JSON.stringify(settings, null, 2) + "\n";
      if (/\{\{[A-Z0-9_]+\}\}/.test(settingsJson)) warn("hub-settings.json still has a {{TOKEN}}; edit AgentAssets/Config/hub-settings.json by hand.");
      const settingsPath = aaRoot + "/" + AA.settings.target;
      const settingsFolder = settingsPath.slice(0, settingsPath.lastIndexOf("/"));
      const existingSettings = await call("GET", fileApi(settingsPath) + "?$select=Name", undefined, { allowMissing: true });
      if (existingSettings && existingSettings.Name) {
        manual.push("Kept your existing " + AA.settings.target + " (not overwritten). Check ourCompany, siteUrl and leadershipRecipients in it.");
      } else { await uploadFile(settingsFolder, settingsPath.split("/").pop(), settingsJson, false); counts.files++; }
      created.push(counts.files + " files in AgentAssets");
      log("AgentAssets: " + counts.files + " files uploaded (skills, SHAREPOINT.md, Config/hub-settings.json)");

      // ---- 13. Sample contracts --------------------------------------------------------------------
      if (withSample) {
        step = "uploading the sample contracts";
        const C = byKey[SPEC.sampleData.contracts.list];
        const cRoot = C.serverUrl || listUrl(C);
        for (const item of SPEC.sampleData.contracts.items) {
          const bytes = fetched.contracts[item.fileName];
          if (!bytes) continue;
          const path = cRoot + "/" + item.fileName;
          const there = await call("GET", fileApi(path) + "?$select=Name", undefined, { allowMissing: true });
          if (there && there.Name && OPTIONS.resume) continue;
          await uploadFile(cRoot, item.fileName, bytes, false);
          const li = await call("GET", fileApi(path) + "/ListItemAllFields?$select=Id");
          const f = item.fields;
          await call("MERGE", lp(C) + "/items(" + li.Id + ")", clean({
            __metadata: { type: await entityType(C) },
            Title: f.Title, Counterparty: f.Counterparty, ContractType: f.ContractType, EffectiveDate: iso(f.EffectiveDate),
            ExpirationDate: iso(f.ExpirationDate), AutoRenews: f.AutoRenews, NoticePeriodDays: f.NoticePeriodDays,
            GoverningLaw: f.GoverningLaw, ContractValue: f.ContractValue, ContractSummary: f.ContractSummary,
            ContractOwnerId: me.Id, BusinessUnit: f.BusinessUnit, Amends: f.Amends, IsSample: true
          }));
          counts.contracts++;
        }
        if (counts.contracts) created.push(counts.contracts + " sample contracts");
        log("Sample contracts: " + counts.contracts + " uploaded with their key terms" + (shift ? " (dates moved " + shift + " days)" : ""));
      }

      // ---- 14. Pre-captured obligations and Run Log rows ---------------------------------------------
      if (withPreCaptured && sampleObligations) {
        step = "loading the pre-captured sample obligations";
        const Ob = byKey[SPEC.sampleData.obligations.list];
        const C = byKey[SPEC.sampleData.contracts.list];
        const have = OPTIONS.resume ? await existingValues(Ob, "CaptureKey") : new Set();
        const soon = Number(settings.dueSoonDays) || 14;
        const t = new Date();
        const today = new Date(Date.UTC(t.getFullYear(), t.getMonth(), t.getDate())).toISOString().slice(0, 10);
        const soonDate = new Date(Date.parse(today + "T00:00:00Z") + soon * 86400000).toISOString().slice(0, 10);
        const closed = ["Fulfilled", "Waived", "Not applicable"];
        for (const o of sampleObligations) {
          if (have.has(String(o.CaptureKey).toLowerCase())) continue;
          const due = day(o.DueDate);
          const timing = closed.indexOf(o.Status) >= 0 ? "Closed" : !due ? "No date" : due < today ? "Overdue" : due <= soonDate ? "Due soon" : "Upcoming";
          const owned = o.ReviewState === "Confirmed" && closed.indexOf(o.Status) < 0;
          const link = origin + encPath((C.serverUrl || listUrl(C)) + "/" + o.ContractName);
          await addItem(Ob, {
            Title: o.Title, ContractName: o.ContractName,
            ContractLink: { __metadata: { type: "SP.FieldUrlValue" }, Url: link, Description: o.ContractName },
            Counterparty: o.Counterparty, ObligationText: o.ObligationText, ClauseRef: o.ClauseRef, SourceClause: o.SourceClause,
            Party: o.Party, Category: o.Category, TriggerType: o.TriggerType, Recurrence: o.Recurrence, DueDate: iso(o.DueDate),
            TriggerEvent: o.TriggerEvent, BusinessUnit: o.BusinessUnit, Status: o.Status, Timing: timing, ReviewState: o.ReviewState,
            Confidence: o.Confidence, Risk: o.Risk, CaptureKey: o.CaptureKey, Notes: o.Notes, IsSample: true,
            OwnerId: owned ? me.Id : null, EscalationOwnerId: owned ? me.Id : null
          });
          counts.obligations++;
          if (counts.obligations % 20 === 0) log("Obligations: " + counts.obligations + " of " + sampleObligations.length);
        }
        if (counts.obligations) created.push(counts.obligations + " sample obligations");
        if (sampleRunLog) {
          const R = byKey[SPEC.sampleData.runLog.list];
          const haveRuns = OPTIONS.resume ? await existingValues(R, "Title") : new Set();
          let runShift = shift * 86400000;
          const latest = Math.max.apply(null, sampleRunLog.map((r) => Date.parse(r.RunAt) || 0));
          while (latest + runShift > Date.now() && runShift > -864000000) runShift -= 86400000;
          if (!OPTIONS.shiftDatesToToday) runShift = 0;
          for (const r of sampleRunLog) {
            if (haveRuns.has(String(r.Title).toLowerCase())) continue;
            await addItem(R, {
              Title: r.Title, Workflow: r.Workflow, Outcome: r.Outcome, ContractName: r.ContractName, ContractVersion: r.ContractVersion,
              ItemsCreated: r.ItemsCreated, ItemsUpdated: r.ItemsUpdated, ItemsHeld: r.ItemsHeld, Details: r.Details,
              RunAt: r.RunAt ? new Date(Date.parse(r.RunAt) + runShift).toISOString().replace(/\.000Z$/, "Z") : null
            });
            counts.runLog++;
          }
          if (counts.runLog) created.push(counts.runLog + " Demo seed Run Log rows");
        }
        log("Pre-captured sample: " + counts.obligations + " obligations, " + counts.runLog + " Run Log rows");
      } else if (withPreCaptured) {
        manual.push("The pre-captured sample obligations couldn't be fetched, so the Obligations list is empty. After you create the Capture workflows, run the Re-capture obligations quick step on each sample contract.");
      } else if (withSample && !withPreCaptured) {
        manual.push("The sample contracts were uploaded before your Capture workflows existed, so nothing captures them yet. After you create the workflows, select each sample contract and run the Re-capture obligations quick step (base contracts before amendments).");
      }
    }

    // ---- 15. Pages: fill tokens, upload, publish -------------------------------------------------------
    const pageUrls = {};
    const published = {};
    if (pagesToDo.length) {
      step = "uploading the pages";
      const L = (k) => byKey[k];
      const tokenValue = (t) => {
        const v = t.value;
        if (v === "siteUrl") return base;
        if (v === "origin") return origin;
        if (v === "siteUrl + /SitePages") return base + "/SitePages";
        if (v.indexOf("listId:") === 0) return L(v.slice(7)).id || "";
        if (v.indexOf("listUrl:") === 0) { const X = L(v.slice(8)); return encPath(X.serverUrl || listUrl(X)); }
        if (v.indexOf("workflowPrompt:") === 0) { const w = SPEC.workflows.find((x) => x.key === v.slice(15)); return w ? htmlText(w.prompt) : ""; }
        return "";
      };
      const values = SPEC.pageTokens.map((t) => [t.token, tokenValue(t)]);
      const emptyToken = values.find((x) => !x[1]);
      if (emptyToken) throw new Error("Couldn't work out a value for " + emptyToken[0] + "; is the list it points to missing?");
      const folder = webRel + "/SitePages";
      for (const p of pagesToDo) {
        let html = fetched.pages[p.name];
        if (!html) { manual.push("Page " + p.name + " wasn't uploaded (its template couldn't be fetched). Use deploy/cowork/fill_pages.py and upload it by hand."); continue; }
        for (const [tok, val] of values) html = replaceAll(html, tok, val);
        const left = html.match(/\{\{[A-Z0-9_]+\}\}/g);
        if (left) warn(p.name + ": unfilled tokens " + Array.from(new Set(left)).join(", "));
        const name = p.target.split("/").pop();
        await uploadFile(folder, name, html, true);
        counts.pages++;
        created.push("page " + p.target);
        const path = folder + "/" + name;
        pageUrls[p.name] = origin + encPath(path);
        if (OPTIONS.publishPages) {
          try { await call("POST", fileApi(path) + "/CheckIn(comment='',checkintype=1)"); }
          catch (e) { if (!/not checked out|isn't checked out|is not checked out|SPFileCheckOutException|-2147024730/i.test(e.message)) warn(p.name + ": check-in said " + e.message.slice(0, 160)); }
          try { await call("POST", fileApi(path) + "/Publish(comment='')"); }
          catch (e) { if (!/minor version|not enabled|already published|cannot be published|draft version|-2146232832|versioning/i.test(e.message)) warn(p.name + ": publish said " + e.message.slice(0, 160)); }
          const st = await call("GET", fileApi(path) + "?$select=Level,UIVersionLabel", undefined, { allowMissing: true });
          if (st && Number(st.Level) === 1) { published[p.name] = true; counts.published++; }
          else manual.push("Open " + pageUrls[p.name] + " and click Publish (it's still a draft, so visitors can't see it).");
        }
      }
      log("Pages: " + counts.pages + " uploaded" + (OPTIONS.publishPages ? ", " + counts.published + " published" : " (drafts; publish them before others can see them)"));

      // ---- 16. Home page (optional, only once Home is published) ----------------------------------
      const home = pagesToDo.find((p) => p.home);
      if (OPTIONS.setHome && home) {
        if (published[home.name]) {
          step = "setting the home page";
          await call("MERGE", "/_api/web/rootfolder", { __metadata: { type: "SP.Folder" }, WelcomePage: home.target });
          log(home.target + " is now the site's home page");
        } else manual.push("Home page not changed: publish " + home.target + " first, then Settings > Site information or the page's '...' menu > Make homepage.");
      }
    }

    // ---- 16b. The site's look: navigation, theme, logo, header (site owners) --------------------------
    // The site navigation is the hub's only navigation (the pages have none of their own). Each part is
    // cosmetic, so a refusal is reported as a finishing touch instead of stopping the run.
    const chrome = { navAdded: 0, navRemoved: 0, theme: false, logo: false, header: false, collection: "" };
    if (SITE && OPTIONS.siteChrome && !chromeOn) {
      manual.push("The site's look needs a site owner, so it was skipped. Ask an owner to run this script with pagesOnly: true, or set it by hand: " + SITE.manual.join(" "));
    } else if (chromeOn && SITE) {
      step = "setting the site navigation";
      const N = SITE.navigation;
      const comm = /^SITEPAGEPUBLISHING$/i.test(web.WebTemplate || "");
      chrome.collection = comm ? "TopNavigationBar" : "QuickLaunch";
      const navApi = "/_api/web/navigation/" + chrome.collection;
      const norm = (u) => { let s = String(u || "").replace(/^https?:\/\/[^/]+/i, ""); try { s = decodeURIComponent(s); } catch (e) { /* keep */ } return s.replace(/\/+$/, "").toLowerCase(); };
      try {
        let nodes = (await call("GET", navApi + "?$select=Id,Title,Url")).value || [];
        if (OPTIONS.replaceNavigation) {
          const pats = N.replaceable.map((r) => new RegExp(r.urlPattern, "i"));
          for (const n of nodes.filter((x) => pats.some((p) => p.test(x.Url || "") || p.test(norm(x.Url))))) {
            await call("DELETE", navApi + "/GetById(" + n.Id + ")");
            chrome.navRemoved++;
          }
          if (chrome.navRemoved) nodes = (await call("GET", navApi + "?$select=Id,Title,Url")).value || [];
        }
        for (const n of N.nodes) {
          let url = "";
          const [kind, ref] = n.target.split(":");
          if (kind === "page") {
            const pg = SPEC.pages.find((x) => x.name === ref);
            const path = webRel + "/" + pg.target;
            const there = pageUrls[pg.name] || (await call("GET", fileApi(path) + "?$select=Name", undefined, { allowMissing: true }));
            if (!there) { manual.push("Navigation link \"" + n.title + "\" skipped: " + pg.target + " isn't on the site (install the pages first)."); continue; }
            url = encPath(path);
          } else {
            const X = byKey[ref];
            if (!X.id) continue;
            url = encPath(X.serverUrl || listUrl(X));
          }
          if (nodes.some((x) => String(x.Title).toLowerCase() === n.title.toLowerCase() && norm(x.Url) === norm(url))) continue;
          await call("POST", navApi, { __metadata: { type: "SP.NavigationNode" }, Title: n.title, Url: url, IsExternal: false });
          chrome.navAdded++;
        }
        if (!comm) await call("MERGE", "/_api/web", { __metadata: { type: "SP.Web" }, HorizontalQuickLaunch: true });
        log("Site navigation: " + chrome.navAdded + " hub links added" + (chrome.navRemoved ? ", " + chrome.navRemoved + " default links removed" : "") + (comm ? "" : " (shown across the top)"));
      } catch (e) { manual.push("Site navigation: " + SITE.manual[0] + " (the REST call was refused: " + e.message.slice(0, 120) + ")"); }
      if (OPTIONS.compactHeader) {
        step = "setting the header layout";
        try {
          await call("MERGE", "/_api/web", { __metadata: { type: "SP.Web" }, HeaderLayout: SITE.header.headerLayout, HeaderEmphasis: SITE.header.headerEmphasis });
          chrome.header = true;
        } catch (e) { manual.push(SITE.manual[1] + " (the REST call was refused: " + e.message.slice(0, 120) + ")"); }
      }
      if (OPTIONS.applyTheme) {
        step = "applying the theme";
        try {
          await call("POST", "/_api/ThemeManager/ApplyTheme", { name: SITE.theme.name, themeJson: JSON.stringify({ palette: SITE.theme.palette }) });
          chrome.theme = true;
        } catch (e) { manual.push(SITE.manual[3] + " (the REST call was refused: " + e.message.slice(0, 120) + ")"); }
      }
      if (OPTIONS.setLogo) {
        step = "setting the site logo";
        try {
          if (!logoBytes) throw new Error("the logo file couldn't be fetched");
          const sa = await call("POST", "/_api/web/lists/EnsureSiteAssetsLibrary");
          const saInfo = await call("GET", "/_api/web/lists(guid'" + sa.Id + "')?$select=Id&$expand=RootFolder");
          const saRoot = (saInfo.RootFolder && saInfo.RootFolder.ServerRelativeUrl) || (webRel + "/SiteAssets");
          const name = SITE.logo.target.split("/").pop();
          await uploadFile(saRoot, name, logoBytes, true);
          await call("POST", "/_api/siteiconmanager/setsitelogo", { relativeLogoUrl: saRoot + "/" + name, type: 0, aspect: 1 });
          chrome.logo = true;
        } catch (e) { manual.push(SITE.manual[2] + " (" + e.message.slice(0, 120) + ")"); }
      }
      log("Site look: " + [chrome.header && "compact header", chrome.theme && "Obligation Hub theme", chrome.logo && "logo"].filter(Boolean).join(", "));
    }

    // ---- 17. A Run Log row for this install ----------------------------------------------------------
    if (!OPTIONS.pagesOnly) {
      step = "writing the Setup row to the Run Log";
      const R = byKey.runlog;
      await addItem(R, {
        Title: "Setup - deploy script", Workflow: "Setup", Outcome: missing.length || manual.length ? "Partial" : "Succeeded",
        ItemsCreated: counts.types + counts.rules + counts.obligations + counts.runLog, ItemsUpdated: 0, ItemsHeld: 0,
        Details: "deploy-obligation-hub.js v" + SPEC.solution.version + " run by " + me.Title + ". Lists created " + counts.listsCreated +
          ", columns " + counts.columns + ", views " + counts.views + ", formats " + counts.formats + ", types " + counts.types +
          ", rules " + counts.rules + ", AgentAssets files " + counts.files + ", sample contracts " + counts.contracts +
          ", sample obligations " + counts.obligations + ", Demo seed runs " + counts.runLog + ", pages " + counts.pages +
          " (published " + counts.published + "), navigation links " + chrome.navAdded + ", theme " + (chrome.theme ? "yes" : "no") +
          ", logo " + (chrome.logo ? "yes" : "no") + ". Not fetched: " + missing.length + ". Manual steps: " + manual.length + ".",
        RunAt: new Date().toISOString().replace(/\.\d{3}Z$/, "Z")
      });
    }

    // ---- 18. Done: links and finishing touches -------------------------------------------------------
    log("Done. Open these:");
    console.table(LISTS.filter((X) => X.id).map((X) => ({ list: X.title, url: origin + encPath(X.serverUrl || listUrl(X)) })));
    if (Object.keys(pageUrls).length) console.table(Object.keys(pageUrls).map((k) => ({ page: k, published: !!published[k], url: pageUrls[k] })));
    if (missing.length) { warn("These kit files couldn't be fetched from " + OPTIONS.assetsBaseUrl + " and were skipped:"); missing.forEach((m) => warn("- " + m)); }
    if (manual.length) { warn("A few things need a click by hand:"); manual.forEach((m) => warn("- " + m)); }
    if (!OPTIONS.pagesOnly) {
      log("Finishing touches (no REST API for these; see the kit's SETUP.md):");
      console.log("1. AI workflows (one trigger each; they run as the person who creates them). Open Copilot in SharePoint on this site and paste each prompt, Capture first:");
      SPEC.workflows.forEach((w, i) => console.log("   1." + (i + 1) + " " + w.name + " (" + w.triggerText + "):\n" + w.prompt + "\n"));
      console.log("2. Quick steps. In each list's quick steps settings add these, action \"Ask Copilot\" (AskKnowledgeAgent), with the exact title and prompt:");
      SPEC.quickSteps.forEach((s) => console.log("   - " + byKey[s.list].title + " > \"" + s.title + "\" (show when " + s.condition + "): " + s.prompt));
      console.log("3. Autofill (optional; capture never depends on it). Paste this into Copilot in SharePoint on this site:\n" +
        replaceAll(SPEC.autofill.copilotPrompt, "{{OUR_COMPANY}}", company).replace(/\.\.(\s|$)/g, ".$1"));
      if (!OPTIONS.setHome && pageUrls.Home) console.log("4. Home page (optional): open " + pageUrls.Home + ", check it, then run this script with pagesOnly: true, setHome: true, or use the page's Make homepage.");
    }
    return {
      site: base, lists: LISTS.filter((X) => X.id).map((X) => ({ key: X.key, title: X.title, id: X.id, url: X.serverUrl || listUrl(X), created: !!X.created })),
      counts, pages: pageUrls, published: Object.keys(published), siteLook: chrome, missing, manualSteps: manual
    };
  } catch (e) {
    console.error("[Obligation Hub] Stopped while " + step + ": " + e.message);
    if (created.length) {
      console.error("[Obligation Hub] Created before it stopped: " + created.join("; ") +
        ".\nFix the problem and run the script again with resume: true to finish, or run remove-obligation-hub.js to remove it all (it goes to the recycle bin).");
    } else console.error("[Obligation Hub] Nothing was created.");
    return { error: e.message, step, created };
  }
})();
