---
name: scrollytelling-story
description: |-
  Creates one interactive HTML scrollytelling explainer: a pinned D3 graphic smoothly rearranges the same data marks as short talk-track steps scroll by. Use when the user says:
    - "create an HTML that explains…"
    - "make a scrolly story about…"
    - "turn this into a scrolling explainer"
    - "make a scrolling data story"
    - "build a scroll-driven explainer"
---
# Scrollytelling Story

## When to use
Use when the user asks for an HTML explainer or a scrollytelling story, including “create an HTML that explains…”, “make a scrolly story about…”, or “turn this into a scrolling explainer.” Apply whether they provide files, lists, data, or only a concept.

## Inputs
- The user's concept, any referenced or selected SharePoint files/lists, and any requested audience or visual style.
- Honor user-defined story length, whether expressed as a step count, word count, reading time, or autoplay duration. If no length is specified, default to 6–15 steps. Clarify conflicting length constraints before building.
- If no data is provided, create clearly labeled illustrative sample data. Keep the default visual style clean and neutral unless the user specifies a style.
- Treat sensitive data as aggregate-only: show totals, shares, or ratios, never individual records or comment text.

## Steps
1. **Ground the story.** Read referenced source files before writing. For a SharePoint list, inspect its schema and sample rows first; use internal field names in live-data selections and verify projected fields. Prefer live SharePoint data using the approved `LiveData` helpers when the source type supports it. At authoring time, call the helper in the workflow and put only its returned fragment in the HTML; the saved renderer must consume supplied results, not fetch data. If a source cannot be live-bound, use its verified contents and state that accurately in the footer rather than implying it refreshes live. Never invent source facts.
2. **Shape the narrative.** Plan sequential steps to fit the requested length; the default 6–15-step range is not a minimum or maximum when the user specifies a length. Use a clear arc: hook; raw data as a plain grid of marks; first pattern; deeper cut (comparison, trend, or breakdown); key insight; and “so what” or call to action. Combine beats for shorter stories and expand meaningful comparisons or explanations for longer ones without padding or inventing facts. Each step gets a short headline and one or two speakable sentences. For a requested word count, budget the visible narrative copy; for reading time, budget that copy using an explicit estimated reading pace. Keep the talk track coherent from beginning to end.
3. **Design one continuous graphic.** Create one set of data marks and preserve each mark's identity across every step. Map each step to an arrangement chosen from: grid; marks sized/colored by value; scatter plot with axes; stacked columns by category; ring/arc; connected network; built-in world or US map; or a word formed from marks. Make transitions smooth (for example, D3 transitions between positions, size, color, and opacity); do not replace the graphic with a sequence of unrelated charts or hard redraws. Use built-in bundled geography for maps, never network loaders.
4. **Keep claims auditable.** Every number in narration, labels, annotations, and charts must be calculated from the source data or the clearly labeled sample dataset. Include a collapsible “Data behind the story” table that provides a text equivalent for every chart/step and identifies the underlying data. For sensitive data, aggregate before rendering and omit identifying records and comments.
5. **Build the page.** Produce exactly one self-contained HTML artifact with a real page title, title screen and “Go” button, scrolling steps, pinned graphic, accessible playback controls, thin progress indicator, collapsible data table, and a footer naming the source (or “Illustrative sample data”). Include pause/resume and speed controls; support Space to pause/resume, arrow keys to move between steps, and manual mouse scrolling to take control. Autoplay should glide through the steps, reach the final step, then stop without restarting. When the user specifies an autoplay duration, fit all transitions and step holds, including the final hold, within that total at normal playback speed; adjust step count and copy for readability unless those are also constrained. Otherwise, pause about nine seconds at each step. User pauses, speed changes, and manual scrolling may change elapsed time. If the reader scrolls manually, cancel or hand off autoplay. Make it responsive at narrow widths and usable in Teams and full-screen mode. Respect `prefers-reduced-motion`: remove/reduce animation and use non-smooth movement while retaining usable controls.
6. **Use approved implementation only.** Follow the SharePoint HTML rules and only approved bundled libraries, primarily D3. Include only the libraries actually used (maximum six manifest entries); no CDNs, external links, images, fonts, network requests, or third-party assets. Escape rendered data and provide accessible labels, keyboard focus, and a non-visual text equivalent.
7. **Validate before delivery.** Check that the story meets the requested step count or narrative word count, or fits the stated reading-time estimate or normal-speed autoplay duration; use 6–15 steps only as the default when no length is specified. Confirm a coherent talk track; each step references the same marks; every displayed number reconciles to the data table; sensitive content is aggregate-only; controls, keyboard behavior, responsive layout, and reduced-motion behavior are accounted for; and autoplay's final-step path clears its timer and stops. Don't claim browser/runtime testing unless it was actually performed.
8. **Save and present.** Honor SharePoint HTML destination rules: use Site Pages HTML creation for page context or page intent, otherwise save as an HTML file in the document library. Create a new artifact, not a replacement for the current page. When exactly one file is created outside Site Pages, open the created file in Preview. Do not create a file for a preview/prototype-only request; render the complete HTML in interactive/HTML Preview instead. Keep the final response brief and link the artifact when one was saved.

## Output format
One complete, self-contained HTML file containing the title screen, scrollytelling sequence, pinned continuously transitioning graphic, playback controls, progress indicator, collapsible data table, and source footer. The final response states what was created and links it when saved; mention any source or live-data limitation plainly.

## Example
For a concept with no supplied dataset, create a small, plausible dataset, label the page footer “Illustrative sample data,” derive every displayed number from that dataset, and build each scroll step by rearranging the same marks. For a supplied SharePoint list, inspect the relevant columns and sample values, bind supported data live, and keep any story claim traceable to the displayed data table.
