"""
make-assets.py — 14-skills-job-postings
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/14-skills-job-postings/make-assets.py
Or from this folder: python make-assets.py

Assets:
  job-postings.csv — 6 rows with deliberate quality variance
    Data matches the prompts in the .demo file — this CSV is for reference/manual import
    The demo creates list items via Copilot prompt (no upload-list command exists)

Quality variance in data:
  1. Senior Software Engineer  — well-written, complete, inclusive
  2. Marketing Rockstar        — biased language, vague, no salary, gendered
  3. Financial Analyst         — decent but wall-of-text requirements, no salary
  4. Sales Development Rep     — good structure but experience mismatch for entry-level
  5. Head of People Operations — good but jargon ("synergize cross-functional")
  6. Operations Coordinator    — two sentences, nothing filled in
"""
import os, csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def p(name):
    return os.path.join(ASSETS_DIR, name)

POSTINGS = [
    {
        'Title': 'Senior Software Engineer',
        'Department': 'Engineering',
        'Description': (
            "We're looking for a Senior Software Engineer to join our platform team. "
            "You'll design and build scalable backend systems using Python and Azure. "
            "Requirements: 5+ years of backend engineering experience, strong Python skills, "
            "experience with cloud infrastructure (Azure preferred), familiarity with React "
            "for occasional front-end work. We value clear communication and collaborative "
            "problem-solving. You'll work with a team that ships regularly and reviews each "
            "other's code carefully."
        ),
        'Salary Range': '$145,000 - $175,000',
        'Remote Policy': 'Hybrid',
        'Status': 'Draft',
    },
    {
        'Title': 'Marketing Rockstar',
        'Department': 'Marketing',
        'Description': (
            "Are you a marketing ninja who lives and breathes social media? We need a rockstar "
            "who is passionate about brand storytelling. He will lead our content calendar and "
            "drive viral campaigns. Must be able to hustle in a fast-paced environment. "
            "Responsibilities include managing all social channels, creating engaging content, "
            "and crushing KPIs."
        ),
        'Salary Range': '',
        'Remote Policy': 'Remote',
        'Status': 'Draft',
    },
    {
        'Title': 'Financial Analyst',
        'Department': 'Finance',
        'Description': (
            "The Financial Analyst will support the FP&A function by building models, preparing "
            "monthly close reports, and contributing to the annual budget process. Requirements: "
            "Bachelor's degree in Finance or Accounting, proficiency in Excel, familiarity with "
            "ERP systems, experience with financial reporting, ability to manage multiple projects "
            "simultaneously, attention to detail, strong communication skills, comfortable with "
            "ambiguity, team player, experience with variance analysis, knowledge of GAAP "
            "accounting principles, experience with SQL a plus, CPA or CFA a plus, 2+ years "
            "in a finance role."
        ),
        'Salary Range': '',
        'Remote Policy': 'Hybrid',
        'Status': 'Draft',
    },
    {
        'Title': 'Sales Development Representative',
        'Department': 'Sales',
        'Description': (
            "Join our sales team as an SDR. You'll prospect into new accounts, qualify inbound "
            "leads, and book meetings for account executives. Requirements: 3-5 years of B2B sales "
            "experience, familiarity with Salesforce, excellent communication skills, ability to "
            "work in a fast-paced environment. This is an entry-level role with a clear path to "
            "Account Executive."
        ),
        'Salary Range': '$52,000 - $62,000 + commission',
        'Remote Policy': 'Remote',
        'Status': 'Under Review',
    },
    {
        'Title': 'Head of People Operations',
        'Department': 'HR',
        'Description': (
            "Zava is looking for a Head of People Operations to lead our HR function through our "
            "next phase of growth. You will synergize cross-functional stakeholder alignment to "
            "drive organizational effectiveness. Responsibilities: oversee recruiting, onboarding, "
            "performance management, benefits administration, and employee relations. Requirements: "
            "8+ years of HR leadership experience, strong employment law knowledge, experience "
            "scaling HR in a growth-stage company. Salary range included — we are serious about "
            "pay transparency."
        ),
        'Salary Range': '$135,000 - $155,000',
        'Remote Policy': 'Hybrid',
        'Status': 'Draft',
    },
    {
        'Title': 'Operations Coordinator',
        'Department': 'Operations',
        'Description': "We need someone to help with operations. Must be detail-oriented.",
        'Salary Range': '',
        'Remote Policy': '',
        'Status': 'Draft',
    },
]

with open(p('job-postings.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Title', 'Department', 'Description', 'Salary Range', 'Remote Policy', 'Status'])
    writer.writeheader()
    writer.writerows(POSTINGS)
print('  ' + p('job-postings.csv'))

print('Done. Files written to:', ASSETS_DIR)
print()
print('Note: The demo creates list items via Copilot prompt in the setup section.')
print('This CSV is provided as a reference and for manual import if needed.')
