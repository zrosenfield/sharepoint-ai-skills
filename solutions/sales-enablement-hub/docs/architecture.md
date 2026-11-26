# Architecture

The hub uses only SharePoint building blocks: lists and libraries, autofill, native approvals, quick steps, Copilot
in SharePoint with site skills, HTML pages and custom views. Nothing runs outside SharePoint.

## Building blocks

| Block | Used for |
|---|---|
| Document libraries | Content Intake, Content Library, Slide Library, Deck Templates, Decks, Archive, Agent Assets, HubAssets |
| Lists | Solution Plays, Content Requests, Customer Shares |
| Autofill (`metadataExtractionPrompt`) | First-pass tags on intake (asset type, products, audience, stage, industry, AI summary, suggested shareability, validation) and on slides (role, products, industry, summary) |
| Native approvals | Single human approval on Content Intake |
| Quick steps | Buttons in the Actions column and the command bar. Each one either runs a SharePoint action (move, approval request) or asks Copilot with a prompt that loads a site skill |
| Site skills (`Agent Assets/Skills/*/SKILL.md`) | The agent's instructions for review, publishing, sharing, freshness and deck building |
| HTML pages (`SitePages/*.html`) | Home, Find, Plays, Slide gallery and Publishing Desk. Each page declares the lists it reads in a `ka-livedata-manifest` and falls back to an embedded snapshot |
| Custom HTML view (`CUSTOMHTML`) | Decks > **Start here**, the deck studio landing view |
| Tiles view (`TILES`) | Deck Templates > **Pick a template**, cards with a thumbnail preview and a **Build with this template** button that runs a quick step |
| List form | Content Requests > **Request content** |

## Libraries and lists

| # | Title (URL) | Who works here | Key columns |
|---|---|---|---|
| 1 | Content Intake | Contributors, Content Team | Autofill tags, Requested shareability, Validation result and findings, Agent fixes, Review status, Proposed expiry, Submission notes, approval status |
| 2 | Content Library | Everyone reads it | Asset type, Solution, Products, Audience, Sales stage, Industry, AI summary, Shareability, Published on, Expires on, Featured, Popularity, Views |
| 3 | Slide Library | Deck builder | Slide role (Title, Agenda, Problem, Solution, Proof, Customer story, Pricing, Next steps, Close), Products, Industry, Summary, Shareability, Use verbatim, Order |
| 4 | Deck Templates | Sellers pick from it | Template kind, Output format, Recipe (slide roles in order), Audience, Slide count, Best for |
| 5 | Decks (`Generated Content`) | Sellers | Customer, Template, Industry, Meeting goal, Status, Source slides, Talking points |
| 6 | Solution Plays | Sellers read it | Pitch, Why now, Discovery questions, Objections, Key assets, Featured, Order |
| 7 | Content Requests | Sellers ask, content team answers | Need, Solution, Industry, Priority, Status, Needed by, Delivered asset |
| 8 | Customer Shares | Written by the share skill | Customer, Recipient, Shared copy, Source asset, Shareability, Shared on, Status, Opportunity |
| 9 | Archive | Content Team | Same tags, plus Archived on, Reason, Replaced by |
| 10 | Agent Assets (`AgentAssets`) | Owners | Skills and standards |
| 11 | HubAssets | Pages | Thumbnails, logo, header |

## Flows

### 1. Content lifecycle: intake to publish

1. A contributor uploads to **Content Intake**. Autofill fills the tags, an AI summary and a first-pass validation.
2. **Run agent review** quick step. Copilot loads `review-submission` and checks the file against
   `Standards/publishing-standards.md`:
   - It fixes what is safe as a new version of the same file: retired product names, missing source lines,
     the confidentiality footer, slide titles and alt text, and empty tags.
   - It logs those changes in **Agent fixes**.
   - It sets **Validation result** to Pass or Blocked and writes plain-language findings.
3. **Submit for approval** appears only when Validation result is Pass. It sends a native approval to the default approver.
4. **Publish to library** appears only when the item is approved. It moves the file to Content Library, and
   `publish-approved` sets the Published on and Expires on dates.
5. **Check freshness** (command bar on Content Library). `freshness-check` lists expired and expiring assets, the
   customer shares and decks that depend on them, and proposes archive moves.

### 2. Share with a customer

**Share with a customer** quick step. It is hidden for Internal only content. Copilot loads `prepare-customer-sharing`:

1. It asks for the customer and recipient.
2. It checks Shareability.
3. It creates a **view-only, specific-people** link.
4. It logs the share in **Customer Shares**.

The share log is what Publishing Desk shows. See [sharing-model.md](sharing-model.md).

### 3. Build a deck

Menu **Build a deck** > **Pick a template** tiles > **Build with this template** > two Copilot question cards > the deck is
saved to **Decks** with seven detail columns filled. See [deck-builder.md](deck-builder.md).

## Pages

| Page | Reads | Shows |
|---|---|---|
| Home | Content Library, Solution Plays | Search, Build a deck, featured plays, popular and new content |
| Find | Content Library | Faceted search over approved content (type, solution, product, industry, stage, shareability) |
| Plays | Solution Plays, Content Library | One play at a time: pitch, why now, discovery, objections, key assets, Build a deck |
| Slide gallery (`SlideBuilder.html`) | Slide Library | Every approved slide by role, with thumbnails. Browse only. Building happens in the template gallery. |
| Publishing Desk | Intake, Requests, Library, Shares, Archive | Content team queue: submissions by status, open requests, expiring assets, recent shares. Hidden from Sellers. |
| Decks > Start here | Decks, Deck Templates | The deck studio: recent decks with talking points, and a link to the template gallery |

Pages are generated by `tools/page-builder` from one theme ("Atmospheric Precision": dark night hero, ice-blue and
violet accents, glass cards). They run in a sandboxed iframe, so links use full URLs with `target="_top"`.
