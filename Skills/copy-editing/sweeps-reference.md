# Sweep Reference — Detailed Look-For Lists and Checklists

Use this reference during each sweep for specific patterns to check.

---

## Sweep 1 — Clarity

Look for:
- Sentences that require re-reading to parse
- Passive voice hiding who does what ("the file is loaded" → "load the file")
- Buried lead — the most important point is halfway through a paragraph
- Assumed knowledge — jargon or acronyms not defined for the intended audience
- Double negatives and hedge stacks

**Common clarity killers in technical docs:**
| Weak | Stronger |
|------|----------|
| "Leverage the functionality" | "Use the feature" |
| "It should be noted that" | [delete — just say the thing] |
| "In order to" | "To" |
| "At this point in time" | "Now" |

**Checklist:**
- [ ] Each sentence makes one point
- [ ] Subject comes before verb in most sentences
- [ ] Acronyms defined on first use
- [ ] No sentence needs to be read twice

---

## Sweep 2 — Voice and Tone

This library's voice is:
- **Direct** — say what you mean, skip the preamble
- **Technically confident** — don't over-explain basics, but don't assume expert depth
- **Action-oriented** — favor imperative constructions ("Open the file", "Paste this into...")
- **Unpretentious** — no inflated language to sound more authoritative

Look for:
- Overly formal phrases that create distance ("Please be advised...", "It is recommended that...")
- Enthusiasm inflation ("incredibly powerful", "seamlessly integrates", "game-changing")
- Hedging that undermines confidence ("might possibly", "could potentially")
- Inconsistent person — don't switch between "you", "the user", and "one" in the same doc

**Checklist:**
- [ ] Tone is consistent start to finish
- [ ] No corporate or marketing filler language
- [ ] Reads like a person wrote it, not a template was filled in
- [ ] Consistent second-person address ("you") throughout

---

## Sweep 3 — So What

The most common failure in technical documentation: describing *what* something is without explaining *why someone would use it* or *what problem it solves*.

Look for:
- Feature descriptions with no benefit statement
- Steps that don't explain what the step accomplishes
- Introductions that describe the document instead of its value ("This README covers...")
- Skill descriptions that say what the skill contains instead of what it does for the user

**Pattern to fix:**
```
Before: "This skill includes four post type templates."
After:  "Four post type templates mean you always start with the right structure — no blank page."
```

**Checklist:**
- [ ] The opening of every major section answers "why does this exist"
- [ ] Each feature or capability is paired with a user benefit
- [ ] The document's opening paragraph tells the reader what they'll be able to do, not just what the doc covers

---

## Sweep 4 — Prove It

Look for:
- Assertions without illustration ("This skill produces better results")
- Vague capability statements with no concrete example ("Works for any goal")
- Instructions that tell but don't show ("Describe what you want and the skill handles the rest")

Fix by adding:
- A concrete example for any claim that could be doubted
- A "for example" or sample input/output where a step is abstract
- Specific scenarios in skill descriptions (the frontmatter `description` field is the main place agents use to decide whether to invoke a skill — make it concrete)

**Checklist:**
- [ ] Every "this does X" statement has an example of X
- [ ] Skill frontmatter descriptions include at least one concrete trigger or use case
- [ ] Abstract instructions have a "for example" companion

---

## Sweep 5 — Specificity

Look for:
- Quantity vagueness ("several", "a few", "many" → use actual numbers when known)
- Scope vagueness ("various features", "different options" → name them)
- Time vagueness ("quickly", "in a moment" → be specific or cut)
- Outcome vagueness ("better results", "improved output" → describe the actual improvement)

**Pattern:**
```
Before: "The RALPH loop runs a few iterations until it's satisfied."
After:  "RALPH runs up to 5 iterations (configurable) and stops when all criteria score 9/10 or above."
```

**Checklist:**
- [ ] Numbers used instead of quantity words wherever the number is known or estimable
- [ ] Named specifics instead of category labels ("the Reason phase" not "one of the phases")
- [ ] Outcome descriptions are measurable or observable

---

## Sweep 6 — Scannability

This matters especially for:
- READMEs (readers skim to decide if this is relevant)
- Skill files (the agent may scan before applying)
- Demo guides (users skip to the step they're on)

Look for:
- Walls of prose where a list or table would serve better
- Long lists that could be grouped under subheadings
- Sections with no heading that run into each other
- Tables where column headers don't match the content
- Heading hierarchy jumps (H2 directly to H4)
- Bolded words mid-sentence that don't add navigation value

**Checklist:**
- [ ] Every major topic has a heading
- [ ] Parallel items are in lists, not buried in paragraphs
- [ ] Tables have clear, matching column headers
- [ ] Document structure is visible from headings alone (no orphan sections)
- [ ] No heading level is skipped

---

## Sweep 7 — Action

Look for:
- Instructions in passive voice ("The file should be saved to...")
- CTAs buried at the end of long paragraphs
- "Getting Started" sections that start with prerequisites instead of the first actual step
- Multiple competing next steps without a recommended path
- Skill files that describe the skill but don't tell the agent how to invoke or apply it

**Checklist:**
- [ ] Every set of instructions uses imperative verbs ("Open", "Paste", "Replace", "Run")
- [ ] The first step is the first action, not a preamble
- [ ] There is one clear "start here" path, with alternatives labeled as such
- [ ] Skill files include explicit invocation guidance (what the user says, what the agent does)
