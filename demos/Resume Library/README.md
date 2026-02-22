# AI-Powered Resume Library in SharePoint

This demo shows how to use AI in a SharePoint document library to automatically extract, organize, and track candidate resumes — turning a raw file drop into a structured hiring pipeline without any manual data entry.

The scenario: a recruiter uploads a batch of resumes and uses the Copilot agent to build a full candidate tracking system from scratch, one prompt at a time.

---

## Watch the Demo

[Watch on YouTube](https://youtu.be/yi4tINldupo)

---

## What This Demo Shows

Upload a set of resume files to a SharePoint document library and let the AI agent:

- Extract candidate names directly from the files into a metadata column
- Recommend and add columns suited to the actual candidate pool
- Categorize each candidate by best-fit department
- Group and filter the library by role or hiring status
- Configure an email alert for new candidates in a specific role
- Add a structured hiring pipeline tracker as a choice column
- Summarize the candidate pool in a table
- Style the library columns for clarity at a glance

No manual data entry. No spreadsheet maintenance. The AI reads the documents and builds the structure around them.

---

## Demo Script

### Prompt 1 — Extract Candidate Names

> Extract the person's name from each file and add them to a candidates name column

AI reads each uploaded resume and writes the candidate's name into a new library column — no manual entry.

---

### Prompt 2 — Suggest Organizational Columns

> Suggest some more columns to organize these resumes

AI recommends metadata columns based on the actual content of the resumes: experience level, skills, education, or whatever is most relevant to the candidate pool.

---

### Prompt 3 — Categorize by Target Role

> Categorize if this candidate is best suited for an HR, Marketing, Finance, Sales, or Engineering role

AI evaluates each resume and assigns a target department, enabling instant filtering across the whole library.

---

### Prompt 4 — Group by Role

> Group the candidates by role

Reorganizes the library view so candidates are clustered by assigned department — no manual sorting.

---

### Prompt 5 — Set Up an Alert

> Send me an email any time a new Engineering candidate is added

AI configures a notification so you're alerted the moment a new Engineering candidate lands in the library.

---

### Prompt 6 — Add a Hiring Status Field

> Add a choice field so we can track whether we've reviewed the candidate, sent them for an interview, have offered, and they accepted or declined

AI adds a structured choice column with the full hiring pipeline: Reviewed, Interview Scheduled, Offered, Accepted, Declined.

---

### Prompt 7 — Summarize the Candidate Pool

> Can you create a table summarizing how many candidates of each type we found so far

AI generates an inline summary table showing candidate counts by target role — instant pipeline visibility without leaving the library.

---

### Prompt 8 — Style the Library Columns

> Can you style the library columns to be clearly differentiated across target role and hiring status

AI applies color formatting so target role and hiring status are immediately readable — no digging through raw text.

---

## Skills Used

No external skills are required for this demo. All actions are performed using the built-in SharePoint Copilot agent against an existing document library.

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `script.md` | Original raw prompts used during the demo recording |

---

## Prerequisites

- Microsoft 365 tenant with Copilot licenses
- SharePoint document library with agent enabled
- A set of resume files uploaded to the library before starting
