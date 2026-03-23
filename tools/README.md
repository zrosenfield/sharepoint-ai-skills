# Demo Tool

Automated demo runner for SharePoint AI Skills. Connects to a live Edge browser via CDP, runs Copilot interactions step-by-step with live pacing controls, slow-types prompts so the audience can follow along, and waits for a complete response before moving on.

## Prerequisites

1. **Node.js 18+** and `npm install` run from the repo root.
2. **Edge with remote debugging enabled.** Run once before starting a demo session:

   ```powershell
   Start-Process "msedge" "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\edge-debug"
   ```

3. **Sign in to SharePoint** in that Edge window. The runner uses your existing session.

---

## Running a scenario

```
npm run demo:site-overview                  # run the demo section (default)
npm run demo:site-overview:setup            # run the setup section
npm run demo:site-overview:reset            # run the reset/teardown section

node tools/run-demo.mjs tools/scripts/site-overview.demo
node tools/run-demo.mjs tools/scripts/site-overview.demo --setup
node tools/run-demo.mjs tools/scripts/site-overview.demo --reset
```

To use a different CDP port:
```
CDP_URL=http://localhost:9223 node tools/run-demo.mjs tools/scripts/site-overview.demo
```

---

## Step controls

When the runner reaches a step it prints the step name and waits for a keypress:

| Key | Action |
|-----|--------|
| **Enter** | Run the current step |
| **s** | Skip this step and advance |
| **b** | Go back and re-run the previous step |
| **?** | Show help |
| **Ctrl+C** | Quit |

The terminal also shows an elapsed timer `[mm:ss]` at each step prompt.

---

## Script format (`.demo` files)

Scripts live in `tools/scripts/`. Each script is a plain text file with three optional sections.

### Sections

```
[section: setup]
... steps to validate and prepare the environment ...

[section: demo]
... the main demo steps ...

[section: reset]
... steps to clean up after the demo ...
```

If no section markers are present, all steps belong to `demo`.

Run `--setup` or `--reset` to execute those sections instead of the demo.

### Lines and commands

| Syntax | Meaning |
|--------|---------|
| `# text` | Comment / section title (displayed when the step runs) |
| Plain text | **Talking point** — displayed to the presenter before the next command |
| `[command]` | Automated action |
| `[command: value]` | Automated action with an argument |

Talking points are word-wrapped at 72 characters and printed to the terminal before the step executes. They are cues for the presenter, not shown in the browser.

### Commands

| Command | Description |
|---------|-------------|
| `[navigate: URL]` | Navigate the browser to a URL |
| `[open-chat]` | Open the Copilot chat pane via the FAB |
| `[prompt: text]` | Slow-type text into the chat input and submit |
| `[wait]` | Wait for Copilot to finish generating a response |
| `[pause]` | Presenter moment — wait for Enter before continuing |
| `[new-chat]` | Click Chat options (…) → New chat to clear the current Copilot conversation |
| `[upload: path]` | Open the Attach menu in the chat input, then wait for the presenter to select the local file in the OS dialog (the OS file picker cannot be automated) |
| `[confirm: message]` | Destructive action required in the browser — shows a warning box and waits for Enter after the user has completed the action |
| `[screenshot: path]` | Save a screenshot to the given path |

---

## The `[confirm]` command

Use `[confirm]` when a step requires the presenter to click a button in the SharePoint UI that cannot be automated — typically a delete confirmation, a dialog accept, or a permission grant.

```
[prompt: Delete the test list called "Demo Output"]
[wait]
[confirm: Click "Delete" in the SharePoint confirmation dialog to complete the deletion]
```

The runner displays a prominent warning box in the terminal, waits for the presenter to complete the action in the browser, then continues when they press Enter. This ensures destructive actions are always human-confirmed rather than automated.

---

## Setup and reset sections

Each script can define setup and reset sections alongside the main demo.

**Setup** (`--setup`): Steps that validate the environment before the demo. Typically:
- Navigate to the site and verify it loads
- Open the chat pane and confirm it shows a fresh session
- Check that expected content (documents, lists) is present
- Pause to let the presenter confirm everything looks right

**Reset** (`--reset`): Steps that restore the site to its pre-demo state. Typically:
- Delete any content created during the demo (using `[confirm]` for destructive steps)
- Navigate back to the home page
- Close or clear the chat pane

Example workflow for a demo day:
```
npm run demo:find-content:setup    # verify environment before the audience arrives
npm run demo:find-content          # run the demo
npm run demo:find-content:reset    # clean up after
```

---

## How it works

### CDP connection

The runner connects to the already-running Edge instance via Playwright's `chromium.connectOverCDP()`. It reuses the existing browser session and pages — no new window is opened, and your sign-in state is preserved.

### Slow typing

Prompts are typed into the Copilot chat input character-by-character at ~40ms per character — fast enough not to drag, slow enough for the audience to read what's being entered.

### Chat pane handling

Before clicking the FAB, the runner checks whether the chat iframe (`[data-automationid="ChatODSPFrame"]`) is already visible:

- **Already open** → skips the FAB entirely.
- **Not open** → clicks the FAB, then clicks **"Open chat"** in the popup menu.
- **Popup lacks "Open chat"** (pane was open but iframe hadn't rendered yet) → presses Escape to dismiss and re-checks.

### Waiting for a complete response

After submitting a prompt the runner watches the DOM for Copilot's generation lifecycle:

1. Wait for the **Stop** button (`[aria-label*="Stop"]`) to appear — confirms generation started.
2. Wait for the Stop button to **disappear** — confirms generation finished.
3. **Fallback**: if the Stop button never appears, poll for new Like/Dislike feedback buttons — these only appear on completed responses.

---

## Adding a new scenario

To generate a demo script with an AI, see **[demo-builder.md](demo-builder.md)** — a self-contained prompt context that defines the full script format, all commands, and worked examples. Paste it into Claude (or any AI), describe the demo you want, and get a ready-to-run `.demo` file back.



Create a new `.demo` file in `tools/scripts/` and add npm shortcuts in `package.json`. A minimal script:

```
# My Demo Title

[section: setup]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

[open-chat]

Verify the chat pane opens successfully before proceeding.

[pause]

[section: demo]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]

Introduction talking point — say this to the audience before clicking anything.

[pause]

[open-chat]

[prompt: Tell me about this site]

[wait]

Narrate the response here.

[screenshot: tools/screenshots/my-demo.png]

[section: reset]

[navigate: https://microsoft.sharepoint-df.com/teams/ZachDemos/]
```

---

## Relation to `demos/tool/`

The repo also contains `demos/tool/` — an earlier demo runner built on the [Playwriter](https://playwriter.dev) Chrome extension CLI. The two tools overlap significantly but differ in architecture:

| | `tools/` (this tool) | `demos/tool/` |
|---|---|---|
| Browser connection | Playwright CDP (Edge or Chrome) | Playwriter Chrome extension |
| Pause mechanism | Terminal keypress (Enter/s/b/?) | In-browser ▶ Next button |
| Script format | `.demo` files with `[command]` blocks | Markdown with `<!-- directive -->` comments |
| Response detection | Watches Stop button / feedback buttons | None (fixed waits) |
| Setup/reset sections | Yes | No |
| Back / skip | Yes | No |
| File upload | Yes (assisted — OS dialog) | No |

`tools/` is the canonical runner for this repo. `demos/tool/` is preserved for reference.

---

## Available scripts

| Script | Demo |
|--------|------|
| `tools/scripts/site-overview.demo` | Copilot summarizes the site's content and lists |
| `tools/scripts/page-summarization.demo` | Copilot summarizes the current page and extracts key takeaways |
| `tools/scripts/find-content.demo` | Copilot finds documents and lists without the user knowing folder structure |

---

## Output files

| File | Description |
|------|-------------|
| `tools/screenshots/` | Screenshots saved by `[screenshot]` commands |
| `tools/debug-screenshot.png` | Screenshot saved automatically when an error occurs |
