# Demo Tool

Automated demo runner for SharePoint AI Skills. Connects to a live Edge browser via CDP, runs Copilot interactions step-by-step with live pacing controls, slow-types prompts so the audience can follow along, and waits for a complete response before moving on.

## Prerequisites

1. **Node.js 18+** and `npm install` run from the repo root.
2. **Edge** installed at a standard path (`Program Files (x86)\Microsoft\Edge\...` or `%LOCALAPPDATA%\Microsoft\Edge\...`).
   The runner launches Edge automatically with remote debugging if it isn't already running.
   To start it manually (e.g. to pick a specific profile):
   ```powershell
   Start-Process "msedge" "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\edge-debug"
   ```
3. **Sign in to SharePoint** in that Edge window. The runner uses your existing session.

---

## Running a scenario

```
npm start                                   # interactive launcher (recommended)
npm run demo:site-overview                  # run the demo section directly
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

## Record mode (automated end-to-end run for video generation)

Add `--record` to run the demo fully unattended — all `[pause]` steps auto-advance without waiting for a keypress. The runner executes every step, waits for all Copilot responses to complete, and writes a timing log to disk.

```
node tools/run-demo.mjs tools/scripts/04-comparison-report/04-comparison-report.demo --record
```

Add `--clips` instead of (or in addition to) `--record` to split the recording at each `[clip]` marker in the script. Each segment between markers becomes a separate OBS recording file. `--clips` implies `--record` — you don't need both flags.

```
node tools/run-demo.mjs tools/scripts/04-comparison-report/04-comparison-report.demo --clips
```

**What `--record` does:**
- Skips all `[pause]` waits — the demo runs straight through from start to finish
- All automated steps (`[navigate]`, `[open-chat]`, `[prompt]`, `[wait]`, `[screenshot]`) still execute normally
- Writes `recordings/<demo-name>/events.json` with per-step timing data and talking points

**What `--clips` adds on top of `--record`:**
- At each `[clip]` marker in the script, the OBS recording is stopped and a new one immediately started
- Each clip becomes its own OBS output file alongside `events.json` in `recordings/<demo-name>/`
- `events.json` switches to a `clips` array format — each entry has its own `videoFile`, `videoOffsetMs`, and `steps` slice
- Screenshot frame numbers continue globally across clip boundaries

**Claude Code is not required.** This is a plain Node.js command you can run in any terminal. Claude Code was used to build the Remotion video project (`C:\repos\remotion`) but has no role in day-to-day recording.

**Output example** (`recordings/04-comparison-report/events.json`):
```json
{
  "demoName": "04-comparison-report",
  "steps": [
    { "name": "Navigate to …", "durationMs": 7766, "talkingPoints": "Legal just sent over the revised MSA…", "isPause": false },
    { "name": "Wait for Copilot response", "durationMs": 51811, "talkingPoints": "", "isPause": false },
    …
  ]
}
```

### Steps that need a human in record mode

`--record` cannot replace human interaction for:

| Command | Behavior in `--record` |
|---|---|
| `[pause]` | **Auto-advances** (this is the whole point) |
| `[confirm]` | Auto-advances — the UI action is skipped. Run setup manually first if confirm steps are required. |
| `[upload]` | Auto-advances — file won't be attached. Use `[upload-library]` instead if possible. |
| `[login-if-needed]` | Auto-advances — requires you to already be signed in before running. |
| `[clip]` | In `--clips` mode: stops/starts OBS recording. In `--record` mode (no `--clips`): no-op. |

**Recommendation:** run `--setup` manually once before doing a `--record` run so the environment is ready.

### What `--record` captures

Every step produces a timing entry in `recordings/<demo-name>/events.json`. If OBS is connected, the full-motion video is also captured (see OBS section below). Playwright screenshots are intentionally skipped in record and clip mode — OBS is the screen capture source and any Playwright screenshot causes a visible flash in the recording.

### OBS WebSocket integration (optional — for smooth video output)

Requires **OBS Studio 28 or later** (28+ has the WebSocket server built in).

If OBS is open and its WebSocket server is enabled, `--record` will automatically start and stop an OBS recording alongside the demo run.

**One-time OBS setup:**
1. Open OBS → Tools → WebSocket Server Settings
2. Check **Enable WebSocket Server** (port 4455, password optional)
3. Create a scene with a **Window Capture** source pointed at the Edge browser window. Name the scene whatever you like — use `[scene: Name]` in your `.demo` scripts to switch to it.

**Setting the OBS password (persistent):**

Add `obsPassword` to `tools/demo.config.json` so you don't have to set it every time:
```json
{
  "obsPassword": "yourpassword"
}
```

Or pass it inline as an env var for a one-off run:
```
OBS_PASSWORD=yourpassword node tools/run-demo.mjs tools/scripts/04-comparison-report/04-comparison-report.demo --record
```

If no password is set, the runner connects without one (works when OBS has no password configured).

**Running with OBS:**
```
node tools/run-demo.mjs tools/scripts/04-comparison-report/04-comparison-report.demo --record
```

The runner prints `⏺ OBS recording started (WxH @ Nfps)` when it connects — it also auto-corrects any output downscaling so the recording matches your canvas resolution. After the demo, `events.json` gains a `videoFile` field with the absolute path to the recording, and `videoOffsetMs` for Remotion sync. If OBS is not running, the run proceeds normally with screenshots only.

### Generating a video from the recording

See `C:\repos\remotion` for the Remotion video project. Two compositions are available:

| Composition | Source | How to use |
|---|---|---|
| `*-slideshow` | Step screenshots | Works immediately after `--record` |
| `*-video` | OBS full-motion recording | Also requires OBS connected during `--record` |

**Steps:**
1. Copy `recordings/<demo-name>/` into `C:\repos\remotion\public\recordings\<demo-name>\`
2. For the video composition: also copy the OBS recording file to `public/recordings/<demo-name>/recording.mp4`
3. In `src/Root.tsx`, add your demo (follow the pattern for `04-comparison-report`)
4. Run `npm run studio` (from `C:\repos\remotion`) to preview in the browser
5. Run `npm run render` to produce a `.mp4`

**Claude Code is not required** for any of these steps once the Remotion project is set up.

---

## Widget mode (full-screen presentations)

Add `--widget` to open a small floating controller window alongside the demo browser.
Useful when presenting full-screen and you don't want to alt-tab to the terminal.

```
node tools/demo.mjs --widget
node tools/run-demo.mjs tools/scripts/site-overview.demo --widget
```

A separate frameless Edge window (280×265) appears at the left edge of the screen showing:

- **Step counter** — current step and total
- **Step name** — what the runner is about to do
- **Next / Back / Skip buttons** — same actions as keyboard controls in the terminal
- **Elapsed timer** — counts up from when the demo section starts
- **Status** — "Running…" while a step executes, highlighted blue when waiting for input

### Layout modes

Three layout modes are available via icons in the top-right of the widget window.
The selected mode persists across sessions.

| Mode | Icon | Window size | Contents |
|------|------|-------------|----------|
| **Full** | ⊡ | 364 × auto | Step info, all three buttons, timer, status, step list |
| **Slim vertical** | ▐ | 80 × auto | Icon-only buttons stacked vertically, timer |
| **Slim horizontal** | ▬ | 520 × 56 | Single-row bar: buttons, step name, timer |

Clicking any button in the widget is equivalent to pressing that key in the terminal —
both inputs feed the same queue, so you can mix and match freely.

---

## Step controls

When the runner reaches a pause it waits for input from either the terminal or the widget window:

| Terminal key | Widget button | Action |
|---|---|---|
| **Enter** | **Next ▶** | Run / continue the current step |
| **s** | **Skip** | Skip this step and advance |
| **b** | **Back ◀** | Go back and re-run the previous step |
| — | **⏸ Pause** | Pause after the current step finishes (toggles on/off; amber when active) |
| **Ctrl+C** | — | Quit |

The terminal also shows an elapsed timer `[mm:ss]` at each step prompt.

The **Pause** button queues a pause after the step that is currently running finishes. Press it during a long Copilot response to pause automatically when the response is done, without needing a `[pause]` in the script. Press again to cancel.

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
| `[var: NAME = value]` | Define a script variable — use as `${NAME}` anywhere in the script to avoid repeating URLs or site paths |
| `[assert: URL]` | Verify a URL is reachable (HTTP < 400). If it fails, shows a warning box and waits for presenter input before continuing. Use in setup to confirm required files/skills exist. |
| `[navigate: URL]` | Navigate the current tab to a URL |
| `[open-tab: URL]` | Open a new browser tab at the URL and switch all subsequent steps to it |
| `[open-chat]` | Open the Copilot chat pane via the FAB |
| `[prompt: text]` | Slow-type text into the chat input and submit |
| `[wait]` | Wait for Copilot to finish generating a response |
| `[pause]` | Presenter moment — wait for Enter before continuing |
| `[new-chat]` | Click Chat options (…) → New chat to clear the current Copilot conversation |
| `[upload: path]` | Open the Attach menu in the chat input, then wait for the presenter to select the local file in the OS dialog (the OS file picker cannot be automated) |
| `[confirm: message]` | Destructive action required in the browser — shows a warning box and waits for Enter after the user has completed the action |
| `[screenshot: path]` | Save a screenshot to the given path |
| `[scene: Name]` | Switch the OBS program scene (e.g. `[scene: Zoom SPAI]`). No-op if OBS is not connected. |
| `[clip]` | Mark a clip boundary. In `--clips` mode, stops and restarts the OBS recording here. No-op in all other modes. |
| `[click-button: text]` | Click a button by its visible label — searched in the chat frame first, then the full page. Waits 2 seconds before clicking so the UI can settle. Logs a warning (rather than failing) if the button is not found. |
| `[follow-chat-link]` | Navigate to the most-relevant SharePoint link in the current Copilot response. Prefers `.docx`/`.pptx` document links over page links; skips citation-style links, data files (`.xlsx`, `.csv`), and list-item `DispForm` URLs. Useful after a prompt that generates a document to jump straight to the result. |

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

## Configuration

Two gitignored files let you tune the runner per machine without touching committed files.
Copy the `*.example.*` version of each to get started.

### `tools/demo.vars.json` — your SharePoint URLs

Scripts use `${SITE}`, `${LIBRARY}`, etc. as placeholders. Set your real URLs here so
you never have to edit the script files themselves:

```json
{
  "SITE": "https://contoso.sharepoint.com/sites/your-site/"
}
```

`SITE` is the only var most scripts need — all other vars (`LIBRARY`, `LIST`, `SKILLS`) are
defined in each script as `${SITE}relative/path/` and are resolved automatically.
Values in `demo.vars.json` take precedence over `[var:]` declarations inside scripts.

**Multiple sites:** use the `overrides` key to set vars for specific scripts by filename (without `.demo`):

```json
{
  "SITE": "https://contoso.sharepoint.com/sites/demo/",
  "overrides": {
    "brand-review": {
      "SITE": "https://contoso.sharepoint.com/sites/marketing/"
    },
    "metadata-at-scale": {
      "SITE": "https://contoso.sharepoint.com/sites/legal/",
      "LIBRARY": "https://contoso.sharepoint.com/sites/legal/Shared%20Documents/Contracts/"
    }
  }
}
```

Per-script overrides are merged on top of the global vars, so you only need to specify what differs.

### `tools/demo.config.json` — typing speed and other tunables

```json
{
  "typeChunkSize": 5,
  "typeDelayMs": 10
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `typeChunkSize` | `5` | Characters typed per fill() call when slow-typing a prompt |
| `typeDelayMs` | `10` | Milliseconds between fill() calls (controls perceived typing speed) |
| `cdpUrl` | `http://localhost:9222` | CDP endpoint for the Edge/Chrome instance. Override here (or via the `CDP_URL` env var) when using a non-standard debugging port, e.g. `9223` for an InPrivate browser. Per-demo overrides in `demo.config.json` take precedence over the top-level value. |

To type faster, increase `typeChunkSize` or decrease `typeDelayMs`. To type slower (e.g. for a live audience that needs more reading time), decrease `typeChunkSize` or increase `typeDelayMs`.

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

## Local (gitignored) scripts

Scripts that depend on unreleased or experimental features can live in
`tools/scripts/local/`. This folder is gitignored, so nothing in it is
committed or pushed.

Local scripts use the same `.demo` format and the same numbered-folder
convention as committed scripts:

```
tools/scripts/local/
  19-my-experiment/
    19-my-experiment.demo
```

They appear in the interactive launcher (`npm start`) and can be run
directly by path — no special flag needed:

```
node tools/run-demo.mjs tools/scripts/local/19-my-experiment/19-my-experiment.demo
```

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
| `tools/scripts/metadata-at-scale.demo` | AI-extracted metadata enables BI-style queries across a contracts library |
| `tools/scripts/resume-library.demo` | Copilot turns a pile of resume files into a structured hiring pipeline |
| `tools/scripts/list-3-ways.demo` | Three approaches to building a SharePoint list — guided, specified, and autonomous |
| `tools/scripts/citations.demo` | Three-skill pipeline extracts assertions, searches a corpus, and writes citation records |
| `tools/scripts/brand-review.demo` | Custom skill audits marketing assets against brand guidelines with scored remediation |

---

## Output files

| File | Description |
|------|-------------|
| `tools/screenshots/` | Screenshots saved by `[screenshot]` commands |
| `tools/debug-screenshot.png` | Screenshot saved automatically when an error occurs |
