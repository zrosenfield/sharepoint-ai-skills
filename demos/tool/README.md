# SharePoint AI Demo Runner

Drive live and recorded SharePoint AI demos from a Markdown script file. No typing required — the tool types for you, at a human-readable pace, in your real authenticated Chrome browser.

Built on [Playwriter](https://playwriter.dev), which attaches to your existing Chrome session — so you stay logged in and corporate bot-detection is a non-issue.

---

## Setup

### 1. Install the Playwriter Chrome extension

Install from the [Chrome Web Store](https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe) and make sure it is active (green icon) on the tab you want to automate.

### 2. Install Playwriter CLI

```
npm install -g playwriter
```

### 3. Install tool dependencies

```
cd demos/tool
npm install
```

---

## Running a demo

```
node demos/tool/runner.js path/to/demo.md
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--url <url>` | from frontmatter | Override the starting URL |
| `--speed slow\|normal\|fast` | `normal` | Typing speed |
| `--screenshots <dir>` | `./screenshots` | Where to save screenshots |
| `--session <id>` | *(new)* | Reuse an existing Playwriter session |
| `--no-auto-pause` | — | Disable the automatic ▶ Next pause after each AI prompt |
| `--dry-run` | — | Print the parsed step list without running anything |

**Tip:** Use `--dry-run` to review what the script will do before going live.

---

## Writing a demo script

Demo scripts are Markdown files. They double as human-readable speaker notes and as machine-runnable scripts — same file, both jobs.

### Frontmatter

```yaml
---
title: My Demo
url: https://tenant.sharepoint.com/sites/yoursite
---
```

Optional frontmatter fields:

| Field | Purpose |
|-------|---------|
| `title` | Display name shown in the runner |
| `url` | Starting URL (navigated to before the first step) |
| `selector` | CSS selector for the SharePoint AI input box (override the auto-detect) |
| `speed` | Default typing speed (`slow`, `normal`, `fast`) |
| `screenshots` | Default screenshot output directory |

### Prompts

Any paragraph (separated by blank lines) that is not a directive is typed into the SharePoint AI input box and submitted:

```markdown
Please summarize this document in three bullet points using the forest style.
```

Multi-line paragraphs are joined into a single message.

### Directives

Control flow is expressed as HTML comments — invisible in normal Markdown renderers, parsed by the runner:

| Directive | Effect |
|-----------|--------|
| `<!-- pause -->` | Inject a **▶ Next** button into the browser. Demo advances when the presenter clicks it. |
| `<!-- navigate: https://... -->` | Navigate to a URL |
| `<!-- wait: 3s -->` | Wait 3 seconds (also accepts `500ms`) |
| `<!-- screenshot: caption -->` | Save a screenshot with the given caption as the filename |
| `<!-- speed: slow -->` | Change typing speed from this point onward |
| `<!-- comment: note to self -->` | Ignored entirely — use for speaker notes |

---

## Example script

```markdown
---
title: PTO App Demo
url: https://contoso.sharepoint.com/sites/hr
---

<!-- comment: Open the HR site before starting, have the PTO app visible -->

Please help me submit a time-off request for next Friday.

<!-- pause -->

Actually make it a full week — July 14 through 18.

<!-- wait: 2s -->

Add a note that I'll be at a family reunion and my backup is Jordan.

<!-- screenshot: final request -->
```

---

## How the pause button works

The **▶ Next** button appears automatically in two situations:

1. **After every AI prompt** — the tool types and submits your message, then pauses so you can watch the AI generate its response. Click ▶ Next when you're ready to continue.
2. **At every `<!-- pause -->` directive** — for non-AI moments: navigation, explaining context, or section breaks.

The button is injected directly into your live Chrome tab (bottom-right corner) and removes itself automatically after you click it. No need to switch focus to a terminal window.

For pre-timed recordings without manual pausing, use `--no-auto-pause` and add `<!-- wait: Xs -->` between prompts instead.

---

## Troubleshooting

**`playwriter not found`** — run `npm install -g playwriter`.

**`Could not find SharePoint AI input box`** — right-click the Copilot input, inspect it, copy a unique selector, and add `selector: <your-selector>` to your script's frontmatter.

**Session doesn't connect** — make sure the Playwriter extension is installed and the green icon is visible on the target tab. Try `playwriter session list` to check the state.
