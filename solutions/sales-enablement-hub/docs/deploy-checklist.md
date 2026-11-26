# Post-deploy checklist

Screenshots of what each item should look like are in [setup-walkthrough.md](setup-walkthrough.md).

Sign in as an owner unless the step says otherwise.

## Structure
- [ ] The menu shows Home, Find, Plays, Build a deck and Content team (Publishing Desk, Content Intake, Content Library).
- [ ] Home opens as the site home page. It shows live data (the source badge says live, not snapshot).
- [ ] Find, Plays, Slide gallery and Publishing Desk open and show live data.
- [ ] **Ask for content** on Home and Find opens the Request content form.
- [ ] Deck Templates opens on **Pick a template** tiles with 4 PowerPoint templates. Each card has **Build with this template**.
- [ ] Decks opens on **Start here** (the deck studio) and lists the sample deck.
- [ ] Every library Note column has unlimited length: Decks > Talking points > *Allow unlimited length in document libraries* is Yes.

## Content
- [ ] Content Library: 18 assets with tags, Published on and Expires on dates. One asset expires within 30 days (Proposal Template) and one has expired (Demo Script - Analytics), for the freshness check.
- [ ] Slide Library: 28 slides with role, industry, products, shareability and order. NW-Title-Retail and NW-Title-Manufacturing are present.
- [ ] Content Intake: 4 submissions with Review status Submitted, no validation yet.
- [ ] Solution Plays: 6 plays. Content Requests: 5 rows. Customer Shares: 5 rows. Archive: 2 files.
- [ ] Agent Assets: 5 skills under Skills/ and `publishing-standards.md` under Standards/.

## Governance
- [ ] Content Intake shows the **Approval status** column (Not submitted) and the Actions buttons. The two Pass items show **Submit for approval**. **Run agent review** on one submission sets Validation result and Agent fixes.
- [ ] **Submit for approval** appears only after a Pass, and the approver receives the request.
- [ ] After approval, **Publish to library** moves the file to Content Library.
- [ ] Content Library > **Share with a customer** is hidden for Internal only items.

## Deck builder (end to end)
- [ ] Build a deck > Quarterly business review > **Build with this template**. Copilot says "Used site skill
      build-customer-deck", shows card 1 (industry, customer, goal), then card 2 (slide choices), then an
      **Update item** card. Press **Update**.
- [ ] Choose **Manufacturing**. The deck opens in PowerPoint for the web, and slide 1 is NW-Title-Manufacturing.
- [ ] The new Decks item has all seven columns: Customer, Template, Industry, Meeting goal, Status, Source slides, Talking points.

## Permissions (test with a Sellers account)
- [ ] The seller can read Content Library, Slide Library, Deck Templates and Solution Plays, and can build a deck.
- [ ] The seller gets access denied on Content Intake, Archive and Publishing Desk.
- [ ] In Content Requests and Customer Shares, the seller sees only their own rows.

## Branding
- [ ] The theme is Dark teal (set by hand on the home page), the header is compact with the Northwind header image, and the logo is set.
