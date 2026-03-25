# Metadata at Scale — Demo Script

## Setup

A SharePoint document library pre-loaded with hundreds of contracts. Each document has AI-extracted metadata columns already populated:

- **Risk Level** (choice: High / Medium / Low)
- **Document Type** (choice: e.g. Joint Venture Agreement, Service Agreement, NDA…)
- **Contract Quarter** (text: e.g. Q4 2019)
- **Has Termination Clause** (yes/no)
- **Has Indemnification Clause** (yes/no)
- **Energy Category**, **Continent**, **Complexity** (choice)

Metadata was stamped at upload time using an AI extraction skill. No manual entry.

---

## Recording Script

**[HOOK — no screen]**

> AI can summarize a contract in seconds. But ask it to find every contract in your library that's missing a termination clause — and it falls apart. Not because AI isn't capable. Because it's missing one thing. Let me show you what that is.

---

**[CUT TO: document library overview]**

> So here's a SharePoint document library — this is a contracts repository. Hundreds of contracts. And at first glance this looks like any other document library you've seen before.
>
> Look at these columns.
>
> Risk level. Document type. Contract quarter. Energy category. Continent. Complexity.
>
> This metadata was extracted automatically by AI at upload time — pulled right out of the contract text and stamped onto each document as structured fields.
>
> And I get asked this question a lot.
>
> "If AI is doing the extracting anyway — why bother storing it? Why not just let the AI read the document every time?"
>
> Fair question. Three reasons.
>
> **Scale.** You don't have one contract. You have hundreds. Maybe thousands. Reading every document fresh for every question isn't a chat experience — it's a bill. Metadata turns a reading exercise into a column filter.
>
> **Consistency.** If you ask AI to classify risk level by reading a contract fresh each time, you might get a slightly different answer depending on how the question is phrased that day. Extract it once, stamp it, govern it — and that answer is locked. Stable. Something your legal and compliance teams can actually trust.
>
> **And the big one** — there are entire categories of questions that search simply cannot answer without metadata. Find me all contracts that do not include a termination clause. Think about what that requires. Without metadata, AI has to open every single file, read it in full, check for the clause, and report back. At scale that's slow, expensive, and error-prone. With a metadata column — it's a one-second filter on a checkbox field.
>
> That last category is where most organizations have zero visibility today. Not because the answer isn't in their library — but because no tool could ever ask the question efficiently enough to matter.

---

**[DEMO QUERY 1 — open Copilot chat]**

> Watch this.

### Prompt 1

```
Find all contracts classified as High Risk.
```

> Instead of searching document text — which would miss contracts where the words "high risk" never appear verbatim — the AI filters the Risk column directly. Like a database query. And it returns every single one. Not a best guess. All of them. Complete and auditable.

---

**[DEMO QUERY 2 — continue in same chat]**

> Now here's where it gets interesting.

### Prompt 2

```
Among all High Risk contracts, what percentage include indemnification clauses?
```

> This is the question that breaks every standard AI tool. Because it's actually two problems in sequence — first define the universe, then analyze across it.
>
> Without metadata, you don't have a reliable universe. You have a guess.
>
> With metadata, the AI locks onto every High Risk contract — it knows exactly what's in scope — and then reads those specific documents for indemnification language and calculates the percentage.
>
> That's not a chat experience anymore. That's a business intelligence query. On your document library.

---

**[DEMO QUERY 3 — continue in same chat]**

> One more.

### Prompt 3

```
Retrieve all Joint Venture Agreements signed in Q4 2019.
```

> Type filter. Date filter. Two columns. Instant.
>
> In a standard RAG system, dates are buried in document text in a dozen different formats, and document types get described differently across hundreds of files. This query would be unreliable at best.
>
> Here it's deterministic. The metadata was standardized at ingestion — so retrieval is just a filter.

---

**[CLOSE — pull back to library overview]**

> The difference is this.
>
> Regular AI reads documents and hopes it found the right ones.
>
> Metadata-augmented AI knows the shape of your entire library before it reads a single word — how many documents exist, how they're classified, when they were executed, what risk they carry.
>
> You do the extraction work once. And then every question, every filter, every analysis — runs on that foundation forever.
>
> That's what makes it reliable enough to actually act on.
