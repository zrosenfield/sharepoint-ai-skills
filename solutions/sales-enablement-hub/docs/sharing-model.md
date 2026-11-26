# Sharing model

Three groups. Assign people, or better, security groups.

| Group | Site role | Purpose |
|---|---|---|
| `<Site> Owners` | Full Control | Hub admins: settings, navigation, skills |
| `<Site> Content Team` (the site's Members group, renamed) | Edit | Publishes, reviews and approves content |
| `<Site> Sellers` (the site's Visitors group, renamed) | Read | Browses content, builds decks, requests content, shares with customers |

## Per library or list

| Library or list | Owners | Content Team | Sellers | Notes |
|---|---|---|---|---|
| Content Intake | Full | Edit | **No access** | Unapproved content is invisible to sellers |
| Content Library | Full | Edit | Contribute | Copied from the reference build: sellers need to run the share quick step. Tighten to Read if your quick steps run without it. Versioning keeps history. |
| Slide Library, Deck Templates, Solution Plays | Full | Edit | Read | Inherited |
| Decks | Full | Edit | Contribute | Copilot saves decks as the seller |
| Content Requests | Full | Edit | Contribute, **own items only** | Item-level security (read and edit own) |
| Customer Shares | Full | Edit | Contribute, **own items only** | Each seller sees only their own share log |
| Archive | Full | Edit | **No access** | |
| Agent Assets | Full | **Read** | Read | Only owners change what the agents do |
| Publishing Desk page | Full | Edit | **No access** | Unique permissions on the page; sellers who follow the Content team menu link get access denied |

## Content shareability

Every asset and slide carries **Shareability**:

| Value | Meaning | Enforced by |
|---|---|---|
| Internal only | Never leaves the company | The share quick step is hidden (condition `[$Shareability] != 'Internal only'`). The deck builder never picks these slides. |
| Customer-shareable (NDA) | Customers under NDA | The share skill confirms the customer has an NDA (asks the seller if unknown) |
| Public | Anyone | Still shared with specific-people view links (never "Anyone" links), so every share is logged |

External shares are always **view-only links for specific people**, created by the share skill and logged in
Customer Shares with customer, recipient, source asset, date and status. Expired assets are never shared; the skill points to the replacement. When an asset is replaced or expires,
`publish-approved` and `freshness-check` mark the related shares **Source updated** or **Source expired**.

## What SharePoint does not do (yet)

- There are no per-recipient "opened" alerts or page-level buyer analytics, which Seismic LiveSend and HubSpot
  Documents provide. The share log records intent, not engagement.
- Expiry does not recall copies already shared. `freshness-check` finds them so a person can act.
