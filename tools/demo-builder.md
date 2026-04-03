# Demo Builder — AI Generation Guide

Use this document as context when asking an AI to generate a `.demo` script for the SharePoint AI Skills demo runner. Paste it into your prompt, describe the demo you want, and the AI will produce a ready-to-run `.demo` file.

---

## What you're generating

A `.demo` file is a plain-text script that drives a live SharePoint Copilot demo end-to-end. It contains:

- **Talking points** — plain prose the presenter reads aloud while the step runs
- **Commands** — `[bracketed]` instructions the tool executes automatically
- **Sections** — `[section: setup]`, `[section: demo]`, `[section: reset]` that separate pre-flight, live demo, and cleanup steps

The tool types prompts into the SharePoint Copilot chat at a human-readable pace, waits for responses to finish, and pauses between steps for the presenter to advance.

---

## File format

```
# Script Title
# One-line description of what this demo shows.

[section: setup]
... setup steps ...

[section: demo]
... demo steps ...

[section: reset]
... reset steps ...
```

### Rules

- The **first two `#` lines** become the title and description shown in the launcher UI. Always include both.
- **Talking points** are plain paragraphs. They print to the presenter's terminal before the next command runs. Write them as spoken cues — what the presenter should say or point out.
- **Commands** are `[command]` or `[command: value]` on their own line.
- Talking points between two commands belong to the command that follows them.
- Blank lines are ignored.
- A talking point with no following command becomes an implicit `[pause]`.

---

## All supported commands

### Variables

```
[var: SITE = https://microsoft.sharepoint-df.com/teams/YourSite/]
```
Defines a script variable. Use `${SITE}` (or any name) anywhere else in the script — in `[navigate]`, `[prompt]`, `[open-tab]`, talking points, wherever. Variables are resolved before anything runs, so you can define them once at the top and change a single line to point the whole script at a different site.

```
# Example
[var: SITE = https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[navigate: ${SITE}]
[prompt: Tell me about ${SITE}]
```

---

### Assertions (setup only)

```
[assert: https://tenant.sharepoint.com/teams/site/Agent%20Assets/Skills/my-skill.md]
```
Checks that the URL is reachable (HTTP status < 400). If the check fails, shows a warning box and pauses so the presenter can decide whether to abort or continue anyway. Use in `[section: setup]` to confirm required files — skill definitions, reference documents, corpus uploads — exist before running the demo.

```
# Example: verify skills are installed before the demo
[var: SKILLS = https://microsoft.sharepoint-df.com/teams/ZachDemos/Agent%20Assets/Skills/]

[assert: ${SKILLS}brand-review.md]
[assert: ${SKILLS}citation-finder.md]
```

URL-encode spaces as `%20` in asset library paths (e.g., `Agent%20Assets`).

---

### Navigation

```
[navigate: https://microsoft.sharepoint-df.com/teams/YourSite/]
```
Navigates the **current tab** to the given URL and waits for the page to load. Always include the trailing slash. Use the full URL.

```
[open-tab: https://microsoft.sharepoint-df.com/teams/AnotherSite/]
```
Opens a **new browser tab** at the given URL and switches the demo runner to it — all subsequent commands (navigate, open-chat, prompt, etc.) target the new tab. The original tab stays open but is no longer the active target. Useful for showing two sites side by side or jumping to a second environment mid-demo.

---

### Chat pane

```
[open-chat]
```
Opens the Copilot chat pane via the FAB (floating action button) in the bottom-right corner. Skipped automatically if the pane is already open.

```
[new-chat]
```
Clicks the `…` (Chat options) menu at the top-right of the chat pane and selects **New chat**. Clears the conversation history. Use this at the start of setup or between demo segments that need a clean context.

---

### Prompts and responses

```
[prompt: Your question or instruction here]
```
Slow-types the text into the Copilot chat input and submits it. The text is typed character-by-character so the audience can read it as it appears.

```
[wait]
```
Waits for Copilot to finish generating its response. Always place a `[wait]` after every `[prompt]`. The tool watches for the Stop button to appear then disappear; falls back to polling for feedback buttons.

---

### Presenter flow

```
[pause]
```
Pauses the demo and waits for the presenter to press Enter before continuing. Use between steps where the presenter needs to narrate, point something out, or let the audience absorb a response.

```
[pause: Optional label for the step list]
```
Same as `[pause]` but the label appears in the step list shown before the demo starts.

---

### Select items in a list or library

```
[select: 1]
[select: 1-3]
[select: all]
```
Selects items in the currently visible SharePoint list or document library by their visible position (1-indexed). `1-3` selects the first three items; `all` clicks the Select All checkbox in the header. Use before prompts that operate on selected files, or to set up a demo state.

---

### File upload

```
[upload: path/to/local/file.pdf]
```
Opens the Attach menu in the chat input, then displays a prompt asking the presenter to select the file in the OS file dialog. The OS-native file picker cannot be automated — the tool opens it and waits for the presenter to complete the selection before continuing.

---

### Destructive actions (human-in-the-loop)

```
[confirm: Click "Delete" in the SharePoint confirmation dialog]
```
Shows a prominent warning box in the terminal and waits for the presenter to complete a destructive action in the browser (delete confirmation, dialog accept, permission grant) before continuing. Use whenever a delete or irreversible action is required.

---

### Screenshots

```
[screenshot: tools/screenshots/my-demo-result.png]
```
Saves a screenshot of the current browser state. Use at the end of key moments. Screenshots are excluded from git automatically.

---

## Section responsibilities

| Section | Flag | Purpose |
|---------|------|---------|
| `[section: setup]` | `--setup` | Pre-flight check before the audience arrives. Navigate to the site, open the chat pane, confirm expected content is present, start a new chat. End with a `[pause]` for the presenter to confirm everything looks right. |
| `[section: demo]` | *(default)* | The live demo. Navigate, open chat, send prompts, wait for responses, pause to narrate. |
| `[section: reset]` | `--reset` | Post-demo cleanup. Navigate back to the home page, delete anything created during the demo (using `[confirm]` for destructive steps), start a new chat. |

All three sections are optional. If no section markers are present, everything is treated as `[section: demo]`.

---

## Talking point style guide

- Write in second person present tense: *"Notice how Copilot..."*, *"Point out the left nav..."*
- Keep each talking point to 2–4 sentences — one thought per block.
- Talking points before `[open-chat]` set scene context. Talking points after `[wait]` help the presenter narrate the response.
- Do not write talking points before `[navigate]` — the presenter is watching the browser load, not reading the terminal.
- For setup sections, write talking points as verification cues: *"Confirm the chat pane shows a fresh session..."*

---

## Complete example — read-only demo

```
# Site Overview
# Shows how Copilot understands the structure and content of a SharePoint site.

[section: setup]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[open-chat]

[new-chat]

Confirm the chat pane shows "Hello" with prompt suggestions and no prior
conversation. If a previous chat is visible, run [new-chat] again.

[pause]

[section: demo]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

Welcome to the demo site. This is a purpose-built SharePoint environment
with a wide variety of lists, libraries, and content. Take a moment to
point out the left nav and the page layout.

[pause]

[open-chat]

The Copilot pane loads in the sidebar — no plugins, no configuration.
This is the standard experience available in any SharePoint site.

[prompt: Tell me about this site]

[wait]

Copilot has read the site and summarized what's here. This is grounded
in the actual site content — lists, libraries, pages — not a generic
description. Point out the inventory breakdown.

[pause]

[prompt: What kinds of lists does this site have?]

[wait]

Notice how Copilot can break down the inventory further without needing
to navigate anywhere. The presenter can keep asking follow-ups naturally.

[screenshot: tools/screenshots/site-overview-final.png]

[section: reset]

This demo is read-only. Navigate back to the home page and start a new
chat to reset for the next run.

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[new-chat]
```

---

## Complete example — demo with file upload

```
# Document Review with Upload
# Shows how Copilot can analyze a local document uploaded to the chat.

[section: setup]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[open-chat]

[new-chat]

Confirm the chat pane is ready. Verify the local file to upload exists
at the path you'll use in the [upload] command below.

[pause]

[section: demo]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

Today we're going to upload a document directly into the Copilot chat
and ask it to analyze the content. This works for PDFs, Word docs, and
other common file types.

[pause]

[open-chat]

[upload: C:/Users/Demo/Documents/quarterly-report.pdf]

The file is now attached. Copilot can read and reason about its contents
without the file needing to live in SharePoint first.

[prompt: Summarize the key findings in this document]

[wait]

Copilot has read the uploaded document and extracted the key points.
This is grounded in the actual file content.

[pause]

[prompt: What are the top three risks mentioned?]

[wait]

Follow-up questions work on the uploaded document just like any other
Copilot conversation. The document stays in context for the session.

[screenshot: tools/screenshots/document-review-final.png]

[section: reset]

[new-chat]
```

---

## Complete example — demo with content creation and reset

```
# Create a List from a Prompt
# Demonstrates Copilot creating a SharePoint list based on a natural language request.

[section: setup]

Verify the site is accessible and that there is no list named "Project
Tracker" already present from a previous demo run. If one exists, delete
it before proceeding.

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[open-chat]

[new-chat]

[pause]

[section: demo]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

One of the most powerful Copilot capabilities in SharePoint is creating
structured content from a simple description. Let's create a list.

[pause]

[open-chat]

[prompt: Create a project tracker list with columns for project name, owner, status, due date, and priority]

[wait]

Copilot has drafted the list structure. Point out that it chose
appropriate column types automatically — choice columns for status and
priority, date for due date.

[pause]

Now let's accept and create it. Copilot will scaffold the list in this
site directly from the chat.

[prompt: Create this list in the current site]

[wait]

The list has been created. Navigate to the site contents to show it.

[screenshot: tools/screenshots/list-created.png]

[section: reset]

Navigate to the new list and delete it to restore the site to its
original state.

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/_layouts/15/viewlsts.aspx]

Find the "Project Tracker" list in Site Contents, open its settings,
and delete it.

[confirm: Delete the "Project Tracker" list from Site Contents → List Settings → Delete this list]

[new-chat]
```

---

## How to ask an AI to build a demo

Paste this entire document into your conversation, then describe what you want:

> **Example prompt:**
> "Using the demo format above, create a `.demo` script for a SharePoint site called `https://microsoft.sharepoint-df.com/teams/MyTeam/`. The demo should show how Copilot can find documents related to onboarding, then summarize the most recent one. The site has a library called 'HR Documents' with onboarding guides. Include setup and reset sections."

The AI should return a complete, ready-to-run `.demo` file. Save it to `tools/scripts/your-demo-name.demo` and it will appear in the launcher automatically.
