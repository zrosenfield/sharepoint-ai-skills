"""
make-assets.py — 15-skills-rfp-response
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/15-skills-rfp-response/make-assets.py
Or from this folder: python make-assets.py

Assets (5 .docx files — Zava past proposals, 2-4 pages each):
  Zava Cloud Migration Proposal - Contoso 2024.docx
  Zava Data Analytics Platform - Fabrikam 2024.docx
  Zava Enterprise Support Services - Woodgrove 2024.docx
  Zava Security and Compliance Overview - Northwind 2025.docx
  Zava Professional Services and Training - Adatum 2025.docx

RFP questions list is created via Copilot prompt in the demo setup section.
A reference CSV is also generated here for manual import if needed.

Coverage design:
  Cloud Migration question  → pulls from Contoso (primary) + Woodgrove (references)
  Data Security question    → pulls from Northwind (primary) + Fabrikam (compliance certs)
  Support Model question    → pulls from Woodgrove (primary)
  Training question         → pulls from Adatum (primary)
  Analytics question        → pulls from Fabrikam (primary) + Northwind (governance)
"""
import io, os, zipfile, csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def p(name):
    return os.path.join(ASSETS_DIR, name)

# ---------------------------------------------------------------------------
# DOCX helper (same pattern as other make-assets.py files in this repo)
# ---------------------------------------------------------------------------
DOCX_CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

DOCX_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOCX_WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

DOCX_STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
</w:styles>'''

WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def xesc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def wp(text='', bold=False, size=None, align=None):
    ppr = ('<w:pPr><w:jc w:val="' + align + '"/></w:pPr>') if align else ''
    if not text:
        return '<w:p ' + WNS + '>' + ppr + '</w:p>'
    rpr = (('<w:b/>' if bold else '') +
           ('<w:sz w:val="' + str(size) + '"/><w:szCs w:val="' + str(size) + '"/>' if size else ''))
    rpr_tag = ('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''
    return ('<w:p ' + WNS + '>' + ppr + '<w:r>' + rpr_tag +
            '<w:t xml:space="preserve">' + xesc(text) + '</w:t></w:r></w:p>')

def wh1(text):
    return ('<w:p ' + WNS + '><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            '<w:r><w:t>' + xesc(text) + '</w:t></w:r></w:p>')

def wh2(text):
    return ('<w:p ' + WNS + '><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            '<w:r><w:t>' + xesc(text) + '</w:t></w:r></w:p>')

def write_docx(path, paras):
    body = '\n'.join(paras)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>' + body +
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
           '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
           '</w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', DOCX_CONTENT_TYPES)
        z.writestr('_rels/.rels', DOCX_RELS)
        z.writestr('word/_rels/document.xml.rels', DOCX_WORD_RELS)
        z.writestr('word/styles.xml', DOCX_STYLES)
        z.writestr('word/document.xml', doc)
    open(path, 'wb').write(buf.getvalue())
    print('  ' + path)

# ===========================================================================
# Generate proposal documents
# ===========================================================================
print('Generating assets for 15-skills-rfp-response...')

# 1. Cloud Migration Proposal — Contoso 2024
write_docx(p('Zava Cloud Migration Proposal - Contoso 2024.docx'), [
    wh1('Zava Cloud Migration Proposal'),
    wp('Prepared for: Contoso Ltd. | Date: September 2024 | Proposal Reference: ZVA-2024-CM-017'),
    wp('Prepared by: Zava Enterprise Solutions | Account Executive: Marcus Webb'),
    wp(),
    wp('Zava is pleased to present this proposal for a comprehensive cloud migration engagement '
       'for Contoso Ltd. This proposal covers Zava\'s proven migration methodology, delivery '
       'timeline, risk management approach, and commercial model.'),
    wp(),
    wh2('Migration Methodology: The Zava 6-Phase Approach'),
    wp('Zava\'s enterprise cloud migration methodology has been refined across more than 80 '
       'migration engagements over six years. The 6-phase approach is designed to minimize '
       'business disruption while ensuring complete migration of workloads to Azure.'),
    wp('Phase 1 — Discovery & Assessment (Weeks 1-2): Automated discovery of on-premises '
       'workloads using Azure Migrate. Dependency mapping, right-sizing analysis, and '
       'identification of lift-and-shift vs. re-platforming candidates.'),
    wp('Phase 2 — Foundation (Weeks 2-4): Azure Landing Zone deployment, identity and access '
       'management configuration, network topology design, and governance baseline establishment.'),
    wp('Phase 3 — Pilot Migration (Weeks 4-6): Migration of 2-3 non-critical workloads to '
       'validate tooling, runbooks, and rollback procedures before the main migration wave.'),
    wp('Phase 4 — Wave Migration (Weeks 6-12): Batch migration of production workloads, '
       'prioritized by business criticality. Each wave includes pre-migration testing, '
       'migration execution, validation, and cutover. Typical wave size: 15-25 workloads.'),
    wp('Phase 5 — Optimization (Weeks 12-14): Azure Advisor recommendations implementation, '
       'reserved instance purchasing, autoscaling configuration, and cost governance baseline.'),
    wp('Phase 6 — Handover (Weeks 14-16): Operational runbook delivery, team enablement '
       'sessions, 30-day hypercare support, and project closure.'),
    wp('Typical total engagement duration: 12-16 weeks depending on workload complexity and volume.'),
    wp(),
    wh2('Azure Partnership & Certifications'),
    wp('Zava holds Azure Expert MSP designation — the highest tier of Microsoft\'s Managed Service '
       'Provider program. Our team includes 47 Azure-certified engineers, including 12 Azure '
       'Solutions Architects (Expert level). Zava is a Microsoft Inner Circle partner for '
       'Azure migration and modernization.'),
    wp(),
    wh2('Uptime SLAs and Production Commitments'),
    wp('Zava provides a 99.95% uptime SLA for all Azure-hosted workloads under our managed '
       'service agreement. This is backed by our 24/7 Network Operations Center and guaranteed '
       'via contract. SLA credits are applied automatically for any breach — no ticket required.'),
    wp('Measurement: Uptime is calculated monthly excluding scheduled maintenance windows '
       '(maximum 2 hours per month, always outside business hours).'),
    wp(),
    wh2('Client Reference: Woodgrove Bank'),
    wp('In Q1 2024, Zava completed a 14-week cloud migration for Woodgrove Bank, migrating '
       '230 workloads — including two Tier 1 core banking systems — with zero unplanned outages '
       'during cutover. Woodgrove Bank\'s CTO, Amelia Chen, is available as a reference. '
       'Contact your Zava account executive to arrange an introduction.'),
    wp('Key outcomes: 31% reduction in infrastructure operating cost in the first six months, '
       'improvement in P99 API latency from 480ms to 190ms, and full SOC 2 Type II '
       'compliance achieved within 60 days of migration completion.'),
    wp(),
    wh2('Pricing Model'),
    wp('Migration engagements are priced on a fixed-fee basis based on workload count and '
       'complexity tier. Managed services post-migration are priced on a per-workload monthly '
       'basis. Detailed pricing is provided in the accompanying Commercial Appendix.'),
    wp('Zava does not charge for overruns caused by scope that was fully documented in the '
       'Discovery phase. Any scope changes requested after Discovery completion are handled '
       'via a formal change request process.'),
])

# 2. Data Analytics Platform — Fabrikam 2024
write_docx(p('Zava Data Analytics Platform - Fabrikam 2024.docx'), [
    wh1('Zava Data Analytics Platform Proposal'),
    wp('Prepared for: Fabrikam Inc. | Date: November 2024 | Proposal Reference: ZVA-2024-DA-031'),
    wp('Prepared by: Zava Data Solutions | Account Executive: Priya Nair'),
    wp(),
    wp('This proposal outlines Zava\'s data analytics platform capabilities for Fabrikam Inc., '
       'including AI/ML integration, reporting infrastructure, data governance, and compliance '
       'certifications relevant to Fabrikam\'s regulatory environment.'),
    wp(),
    wh2('Analytics Platform Architecture'),
    wp('Zava\'s analytics platform is built on Microsoft Fabric and Azure Synapse Analytics, '
       'providing a unified data lakehouse architecture. All data ingestion, transformation, '
       'and serving layers are managed within the customer\'s own Azure tenant — Zava does not '
       'retain copies of customer data in shared infrastructure.'),
    wp('Core components: Azure Data Factory for ingestion, Synapse Analytics for transformation '
       'and storage, Power BI Premium for visualization, and Azure Machine Learning for '
       'predictive workloads.'),
    wp(),
    wh2('AI/ML Integration'),
    wp('Zava\'s AI layer integrates directly with Azure Machine Learning and Azure OpenAI Service. '
       'Common use cases deployed for clients include: demand forecasting, churn prediction, '
       'anomaly detection on financial transactions, and natural language querying of structured '
       'data via Copilot for Microsoft 365.'),
    wp('All ML models are version-controlled, monitored for drift, and retrained on a schedule '
       'defined with the customer. Model explainability reports are available for all production '
       'models upon request.'),
    wp(),
    wh2('Power BI Dashboards and Self-Service Reporting'),
    wp('Zava delivers a standard set of executive, operational, and analytical dashboards as '
       'part of every analytics engagement. Customers receive 12 pre-built dashboard templates '
       'covering finance, operations, sales performance, and HR analytics. Custom dashboards '
       'are scoped during the design phase.'),
    wp('All dashboards use row-level security to ensure users see only data they are authorized '
       'to access. Single sign-on via Azure Active Directory is standard.'),
    wp(),
    wh2('Data Governance Framework'),
    wp('Zava implements Microsoft Purview as the data governance layer for all analytics '
       'deployments. This provides automated data classification, lineage tracking, access '
       'policy management, and sensitivity labeling. Sensitive fields are automatically detected '
       'and flagged for review before any report or export is permitted.'),
    wp('Data residency: all customer data remains in the customer-specified Azure region. '
       'No cross-region replication without explicit customer authorization.'),
    wp(),
    wh2('Compliance Certifications'),
    wp('Zava maintains the following certifications relevant to Fabrikam\'s environment:'),
    wp('SOC 2 Type II — annual audit, most recent report available under NDA'),
    wp('ISO 27001:2022 — certified since 2019, recertified July 2024'),
    wp('ISO 27701 — privacy extension, certified since 2023'),
    wp('GDPR compliance — Data Processing Agreement available as standard'),
    wp(),
    wh2('Client Reference: Fabrikam Reporting Transformation'),
    wp('Following the implementation of Zava\'s analytics platform, Fabrikam\'s finance team '
       'reduced monthly close reporting time by 60% — from 5 business days to 2 business days. '
       'The self-service reporting capability eliminated 80% of ad hoc data requests previously '
       'routed to the central IT team.'),
    wp(),
    wh2('Support Tiers for Analytics Platform'),
    wp('Analytics platform support is provided under Zava\'s standard support tiers (Gold and '
       'Platinum). Platform-specific SLAs: P1 incidents (platform unavailability) — 15-minute '
       'response, 4-hour resolution target. Full support tier details are available in the '
       'Zava Enterprise Support Services document.'),
])

# 3. Enterprise Support Services — Woodgrove 2024
write_docx(p('Zava Enterprise Support Services - Woodgrove 2024.docx'), [
    wh1('Zava Enterprise Support Services'),
    wp('Prepared for: Woodgrove Bank | Date: January 2024 | Proposal Reference: ZVA-2024-SS-004'),
    wp('Prepared by: Zava Customer Success | Account Executive: James Okafor'),
    wp(),
    wp('This document details Zava\'s enterprise support model, service tier offerings, '
       'SLA commitments, escalation procedures, and customer success outcomes relevant '
       'to Woodgrove Bank\'s requirements.'),
    wp(),
    wh2('Support Tier Overview'),
    wp('Zava offers three support tiers: Silver, Gold, and Platinum. All enterprise migration '
       'clients receive Gold as the minimum tier during and for 12 months following engagement completion.'),
    wp(),
    wp('Silver — $2,500/month'),
    wp('  Business hours support (8am-6pm local time, Mon-Fri)'),
    wp('  P1 response: 4 hours | P2 response: 8 hours | P3 response: 2 business days'),
    wp('  Access to support portal and knowledge base'),
    wp('  Monthly service review report'),
    wp(),
    wp('Gold — $6,500/month'),
    wp('  Extended hours support (7am-9pm local time, Mon-Fri + Sat 9am-5pm)'),
    wp('  P1 response: 1 hour | P2 response: 4 hours | P3 response: 1 business day'),
    wp('  Named Technical Account Manager (shared, up to 3 customers per TAM)'),
    wp('  Bi-weekly service review calls'),
    wp('  Proactive monitoring and alerting'),
    wp('  Access to Zava\'s private beta program for new features'),
    wp(),
    wp('Platinum — $14,000/month'),
    wp('  24/7/365 support, including holidays'),
    wp('  P1 response: 15 minutes | P2 response: 1 hour | P3 response: 4 hours'),
    wp('  Dedicated Technical Account Manager (exclusive to your account)'),
    wp('  Weekly executive business reviews available'),
    wp('  Dedicated escalation hotline — direct to senior engineering'),
    wp('  On-site quarterly reviews included'),
    wp('  Priority access to all new features and roadmap previews'),
    wp(),
    wh2('24/7 Network Operations Center'),
    wp('Zava\'s NOC operates 24 hours a day, 365 days a year from three global locations '
       '(Seattle, Amsterdam, Singapore) to ensure follow-the-sun coverage. All production '
       'environments are monitored continuously with automated alerting. NOC engineers '
       'can initiate P1 incident response without waiting for customer notification.'),
    wp(),
    wh2('Escalation Procedures'),
    wp('P1 incidents (full outage or critical data loss risk): immediate NOC response, '
       'TAM notified within 15 minutes, VP Engineering on-call notified within 30 minutes, '
       'executive bridge call initiated if not resolved within 1 hour.'),
    wp('P2 incidents (significant degradation, workaround available): TAM leads response, '
       'engineering team engaged within 2 hours, customer status updates every 2 hours.'),
    wp('P3 incidents (minor issues, no business impact): standard ticket queue, '
       'daily status updates until resolved.'),
    wp('Post-incident reviews (PIR) are completed within 5 business days for all P1 incidents '
       'and are shared with the customer including root cause analysis and remediation steps.'),
    wp(),
    wh2('Customer Satisfaction Metrics'),
    wp('Zava\'s most recent annual support survey results (Q4 2023, n=214 enterprise customers):'),
    wp('Overall CSAT score: 98.2% (satisfied or very satisfied)'),
    wp('P1 response time compliance: 99.4% within committed SLA'),
    wp('P2 response time compliance: 97.8% within committed SLA'),
    wp('Mean time to resolution (P1): 2.1 hours average across all 2023 P1 incidents'),
    wp('Net Promoter Score (support-specific): +71'),
    wp(),
    wh2('Training and Enablement'),
    wp('All support tiers include access to Zava Academy — our self-paced learning platform '
       'with 200+ courses covering platform administration, troubleshooting, and best practices. '
       'Gold and Platinum customers additionally receive annual instructor-led training credits '
       '(Gold: 20 hours/year; Platinum: 40 hours/year).'),
])

# 4. Security & Compliance Overview — Northwind 2025
write_docx(p('Zava Security and Compliance Overview - Northwind 2025.docx'), [
    wh1('Zava Security & Compliance Overview'),
    wp('Prepared for: Northwind Traders | Date: February 2025 | Proposal Reference: ZVA-2025-SC-008'),
    wp('Prepared by: Zava Security Practice | Account Executive: Keiko Tanaka'),
    wp(),
    wp('This document provides a comprehensive overview of Zava\'s security architecture, '
       'zero-trust implementation, compliance certifications, and incident response procedures '
       'for Northwind Traders\' security evaluation team.'),
    wp(),
    wh2('Security Architecture Overview'),
    wp('Zava\'s security architecture is built on Microsoft\'s Security Development Lifecycle '
       '(SDL) and is aligned to the NIST Cybersecurity Framework. All Zava-managed '
       'infrastructure runs in Azure with security controls enforced via Azure Policy, '
       'Microsoft Defender for Cloud, and Microsoft Sentinel.'),
    wp(),
    wh2('Zero-Trust Implementation'),
    wp('Zava has implemented a full zero-trust architecture across all production systems. '
       'Core pillars of our zero-trust model:'),
    wp('Identity: All access requires multi-factor authentication. Privileged Identity '
       'Management (PIM) enforces just-in-time access for administrative roles — no standing '
       'admin access exists in any production environment. Conditional Access policies enforce '
       'device compliance and location-based controls.'),
    wp('Network: All traffic between services is encrypted and authenticated. No implicit '
       'trust based on network location. Microsegmentation is enforced via Azure Virtual '
       'Networks with deny-by-default NSG rules.'),
    wp('Data: All data classified at ingestion using Microsoft Purview. Sensitivity labels '
       'enforce encryption and access controls automatically. Data Loss Prevention policies '
       'are applied at the Microsoft 365 and Azure Storage layers.'),
    wp('Endpoints: All managed endpoints are enrolled in Microsoft Intune. Non-compliant '
       'devices are blocked from accessing Zava systems via Conditional Access.'),
    wp(),
    wh2('Encryption Standards'),
    wp('Data at rest: AES-256 encryption for all stored data. Azure Storage Service Encryption '
       'and Azure Disk Encryption are enabled by default on all storage resources.'),
    wp('Data in transit: TLS 1.3 enforced for all external communications. TLS 1.2 minimum '
       'for internal service-to-service traffic. TLS 1.0 and 1.1 are disabled at the '
       'tenant level and cannot be re-enabled.'),
    wp('Key management: Azure Key Vault with Hardware Security Module (HSM) backing for all '
       'cryptographic keys. Customer-managed keys (CMK) are available for Platinum support '
       'customers upon request.'),
    wp(),
    wh2('Penetration Testing'),
    wp('Zava conducts annual third-party penetration tests covering network, application, '
       'and social engineering vectors. Tests are performed by an independent security firm '
       '(current vendor: Secureworks). The most recent test was completed in November 2024. '
       'Executive summary reports are available under NDA; full technical reports are available '
       'to customers under a separate NDA agreement with Secureworks.'),
    wp('In addition, Zava participates in the Microsoft Vulnerability Research program and '
       'maintains a responsible disclosure policy for external security researchers.'),
    wp(),
    wh2('Compliance Certifications'),
    wp('FedRAMP Moderate — Authority to Operate (ATO) granted April 2023'),
    wp('HIPAA / HITECH — Business Associate Agreement available as standard'),
    wp('SOC 2 Type II — most recent audit period: January-December 2024, report available under NDA'),
    wp('ISO 27001:2022 — certified since 2019; most recent surveillance audit: October 2024'),
    wp('ISO 27701 — privacy extension, certified since 2023'),
    wp('PCI DSS Level 1 Service Provider — current attestation on file'),
    wp(),
    wh2('Incident Response Procedures'),
    wp('Zava\'s Incident Response Plan (IRP) follows the NIST SP 800-61 framework. '
       'The plan is reviewed and updated quarterly and tested via tabletop exercises twice annually.'),
    wp('Detection: Automated detection via Microsoft Sentinel SIEM with 24/7 SOC monitoring. '
       'Mean time to detect (MTTD) for security incidents: 8 minutes (2024 average).'),
    wp('Containment: On-call security engineer engaged within 15 minutes of confirmed incident. '
       'Automated containment playbooks reduce initial response time for common incident types.'),
    wp('Customer notification: Customers are notified within 2 hours of a confirmed security '
       'incident that may affect their data. Notification includes initial impact assessment, '
       'containment actions taken, and next steps.'),
    wp('Regulatory notification: Zava supports customer obligations under GDPR (72-hour notification), '
       'HIPAA, and applicable US state breach notification laws.'),
    wp(),
    wh2('Security Team'),
    wp('Zava\'s security team comprises 34 dedicated security professionals including:'),
    wp('Chief Information Security Officer: Marcus Reid, CISSP, CISM, 18 years experience'),
    wp('Security Operations: 12 SOC analysts across three shifts (24/7 coverage)'),
    wp('Application Security: 8 AppSec engineers embedded in product delivery teams'),
    wp('GRC: 6 professionals managing compliance, risk, and audit programs'),
    wp('Security certifications held across the team: 14 CISSP, 8 CISM, 11 CEH, 6 OSCP'),
])

# 5. Professional Services & Training — Adatum 2025
write_docx(p('Zava Professional Services and Training - Adatum 2025.docx'), [
    wh1('Zava Professional Services & Training'),
    wp('Prepared for: Adatum Corporation | Date: March 2025 | Proposal Reference: ZVA-2025-PS-012'),
    wp('Prepared by: Zava Professional Services | Account Executive: Sofia Delgado'),
    wp(),
    wp('This proposal details Zava\'s professional services methodology, training programs, '
       'change management approach, and knowledge transfer framework for Adatum Corporation.'),
    wp(),
    wh2('Professional Services Methodology'),
    wp('Zava\'s professional services engagements follow our Accelerated Value Delivery (AVD) '
       'methodology, which combines agile delivery principles with structured governance gates. '
       'AVD is designed to deliver measurable business outcomes within the first 90 days of '
       'engagement while building internal capability for long-term self-sufficiency.'),
    wp('AVD phases:'),
    wp('Mobilize (Week 1-2): Project governance established, stakeholders aligned, success '
       'metrics defined, and delivery team onboarded. Executive sponsor identified and engaged.'),
    wp('Design (Week 2-5): Current state assessment, future state architecture, gap analysis, '
       'and delivery roadmap. Design decisions documented and signed off before build begins.'),
    wp('Build & Validate (Week 5-12): Iterative delivery in 2-week sprints. Each sprint '
       'delivers demonstrable working capability. Customer product owner reviews and accepts '
       'each sprint output before work continues.'),
    wp('Stabilize (Week 12-14): User acceptance testing, performance validation, security '
       'review, and pre-production runbook completion.'),
    wp('Transition (Week 14-16): Go-live, hypercare support, and knowledge transfer completion.'),
    wp(),
    wh2('Training Programs'),
    wp('Zava Academy provides three delivery modalities for all training programs:'),
    wp('Instructor-Led Training (ILT): Delivered by Zava-certified trainers, either on-site '
       'or via virtual classroom. Class sizes capped at 12 participants to ensure hands-on '
       'practice time. All ILT courses include hands-on labs in a dedicated sandbox environment.'),
    wp('Self-Paced Learning: 200+ courses available 24/7 on the Zava Academy platform. '
       'Courses range from 30-minute microlearning modules to full certification preparation '
       'programs (40+ hours). Progress tracking and completion certificates included.'),
    wp('Certification Paths: Zava offers three customer-facing certification levels — '
       'Associate (foundation skills), Professional (advanced administration), and Expert '
       '(architecture and custom development). Certifications are vendor-neutral where possible, '
       'supplemented by Microsoft certification preparation where relevant.'),
    wp('Training satisfaction scores (2024 annual survey, n=892 participants):'),
    wp('  Overall satisfaction: 4.7/5.0'),
    wp('  Instructor quality: 4.8/5.0'),
    wp('  Content relevance: 4.6/5.0'),
    wp('  Lab environment quality: 4.5/5.0'),
    wp(),
    wh2('Change Management Approach'),
    wp('Zava\'s change management practice is aligned to Prosci\'s ADKAR model '
       '(Awareness, Desire, Knowledge, Ability, Reinforcement). Every enterprise engagement '
       'includes a change management workstream from day one, not as an afterthought at go-live.'),
    wp('Key activities by phase:'),
    wp('Pre-implementation: Stakeholder impact assessment, communication plan development, '
       'and sponsor coaching. We identify resistors early and build mitigation plans.'),
    wp('During implementation: Regular change readiness assessments, targeted communication '
       'for impacted groups, and early adopter programs to build internal champions.'),
    wp('Post-go-live: 90-day reinforcement plan, adoption metrics dashboard, and scheduled '
       'check-ins at 30, 60, and 90 days.'),
    wp(),
    wh2('Knowledge Transfer Framework'),
    wp('Zava\'s knowledge transfer (KT) framework is designed to eliminate dependency on '
       'Zava after engagement completion. KT activities begin in Week 1, not Week 14.'),
    wp('Documentation: All architecture decisions, runbooks, and operational procedures '
       'are authored collaboratively with the customer team. No Zava-only documentation exists.'),
    wp('Shadow-then-lead: Customer team members shadow Zava engineers during build, then '
       'lead with Zava support during stabilization, then operate independently post-transition.'),
    wp('Outcomes: Customers who complete Zava\'s full KT program achieve 50% faster '
       'time-to-productivity for their internal teams vs. clients who skip the KT program '
       '(measured at 90 days post-go-live). Internal ticket escalation to Zava drops by '
       'an average of 65% within six months.'),
    wp(),
    wh2('Post-Engagement Support Model'),
    wp('Following engagement completion, Zava\'s customer success team conducts quarterly '
       'business reviews to assess adoption, surface emerging needs, and connect customers '
       'with new platform capabilities. This service is included at no additional cost for '
       'all customers on Gold or Platinum support tiers.'),
    wp('Customer health scoring: Each account receives a monthly health score based on '
       'platform adoption metrics, support ticket trends, and training completion rates. '
       'Accounts with declining health scores receive proactive outreach from the '
       'customer success team.'),
])

# ---------------------------------------------------------------------------
# Reference CSV for RFP questions (for manual import if needed)
# ---------------------------------------------------------------------------
RFP_QUESTIONS = [
    {
        'Title': 'Cloud Migration Approach',
        'Full Question': 'Describe your methodology for migrating enterprise workloads to Azure, including typical timelines, risk mitigation strategies, and references from similar engagements.',
        'Category': 'Technical',
        'Priority': 'Must Answer',
        'Status': 'Open',
        'Draft Response': '',
        'Sources Used': '',
        'Confidence': '',
    },
    {
        'Title': 'Data Security Standards',
        'Full Question': 'Detail your security certifications, data encryption standards, and approach to zero-trust architecture. Include your incident response procedures and most recent third-party audit results.',
        'Category': 'Security',
        'Priority': 'Must Answer',
        'Status': 'Open',
        'Draft Response': '',
        'Sources Used': '',
        'Confidence': '',
    },
    {
        'Title': 'Support Model & SLAs',
        'Full Question': 'What support tiers do you offer? Provide SLA response times, escalation procedures, and customer satisfaction metrics for your enterprise support program.',
        'Category': 'Support',
        'Priority': 'Must Answer',
        'Status': 'Open',
        'Draft Response': '',
        'Sources Used': '',
        'Confidence': '',
    },
    {
        'Title': 'Training & Change Management',
        'Full Question': 'How do you ensure successful adoption post-implementation? Describe your training programs, change management methodology, and knowledge transfer approach.',
        'Category': 'General',
        'Priority': 'Nice to Have',
        'Status': 'Open',
        'Draft Response': '',
        'Sources Used': '',
        'Confidence': '',
    },
    {
        'Title': 'Analytics & Reporting',
        'Full Question': 'Describe your data analytics capabilities, including AI/ML integration, dashboard options, and how you handle data governance and compliance for reporting workflows.',
        'Category': 'Technical',
        'Priority': 'Must Answer',
        'Status': 'Open',
        'Draft Response': '',
        'Sources Used': '',
        'Confidence': '',
    },
]

with open(p('rfp-questions.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Title', 'Full Question', 'Category', 'Priority', 'Status', 'Draft Response', 'Sources Used', 'Confidence'])
    writer.writeheader()
    writer.writerows(RFP_QUESTIONS)
print('  ' + p('rfp-questions.csv'))

print('Done. Files written to:', ASSETS_DIR)
print()
print('Note: The demo creates list items via Copilot prompt in the setup section.')
print('rfp-questions.csv is provided for reference and manual import if needed.')
