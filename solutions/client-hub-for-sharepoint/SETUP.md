# Manual setup (site owner, no admin)

This builds the same Client Hub as the script, by hand. Everything here is standard SharePoint that a site owner, or a member with Edit permission, can do. Plan on 45 to 60 minutes. Pieces marked *optional* can be skipped.

> Unofficial, personal and unsupported. Not a Microsoft product. See the [README](README.md).

## 1. Pick the site

Use a site whose members are exactly the people who should see client data. The lists inherit the site's permissions. A new Team site or Communication site is the cleanest choice. If your organisation uses sensitivity labels, label the site the way your policy says.

## 2. Create the three lists

On the site, choose **New > List > Blank list**. Create them in this order, because Projects and Client Activity look up Clients.

When you add a Lookup column, pick **Clients** as the source and **Client** (the renamed Title) as the column to show. Turn on **Enforce relationship behaviour > Restrict delete** if you want to stop someone deleting a client that still has history.

### 2.1 Clients

Create a blank list named **Clients**. Description: *One row per client: profile, owners, main contact, value and renewal.*

Rename the **Title** column to **Client**. Then add these columns. Type the internal name first, save, then rename it to the display name. This keeps the internal name clean, which the formatting and the Copilot skills rely on.

| Internal name | Display name | Type | Choices | Default | Required |
|---|---|---|---|---|---|
| ClientType | Client type | Choice | Managed services, Software |  |  |
| Products | Products | Choice (allow multiple selections) | Digital Banking, Payments Hub, Card Issuing, Fraud Shield, Open Banking API |  |  |
| Environments | Environments | Choice (allow multiple selections) | Production, UAT, Sandbox, DR |  |  |
| Health | Health | Choice | On track, Needs attention, At risk | On track |  |
| RelationshipManager | Relationship manager | Person |  |  |  |
| ImplementationManager | Implementation manager | Person |  |  |  |
| MainContact | Main contact | Single line of text |  |  |  |
| ContactEmail | Contact email | Single line of text |  |  |  |
| ContactPhone | Contact phone | Single line of text |  |  |  |
| AnnualValue | Annual value | Currency |  |  |  |
| RenewalDate | Renewal date | Date (no time) |  |  |  |
| ServiceDesk | Service desk link | Hyperlink |  |  |  |
| About | About | Multiple lines of text |  |  |  |

**Views**

| View | Columns, in order | Filter | Sort / layout |
|---|---|---|---|
| All clients (default) | Client, Health, Client type, Relationship manager, Annual value, Renewal date, Products, Main contact, Contact email, Contact phone, Implementation manager, Environments, Service desk link, About |  | Client A to Z |
| Portfolio | Client, Health, Client type, Annual value, Renewal date, Relationship manager, Products |  | Gallery. Health, then Annual value (largest first) |
| Renewals | Client, Renewal date, Annual value, Health, Relationship manager, Main contact |  | Renewal date, earliest first |

### 2.2 Projects

Create a blank list named **Projects**. Description: *Implementations, migrations (MFA, SSO, platform), upgrades and enhancements, linked to a client.*

Rename the **Title** column to **Project**. Then add these columns. Type the internal name first, save, then rename it to the display name. This keeps the internal name clean, which the formatting and the Copilot skills rely on.

| Internal name | Display name | Type | Choices | Default | Required |
|---|---|---|---|---|---|
| Client | Client | Lookup (to Clients, show Client) |  |  | Yes |
| ProjectType | Type | Choice | Implementation, Migration, Upgrade, Enhancement |  |  |
| Status | Status | Choice | Not started, In progress, Blocked, Done | Not started |  |
| Owner | Owner | Person |  |  |  |
| Team | Team | Choice | Implementation, Engineering, Security, Infrastructure |  |  |
| StartDate | Start date | Date (no time) |  |  |  |
| DueDate | Target date | Date (no time) |  |  |  |
| NextMilestone | Next milestone | Single line of text |  |  |  |

**Views**

| View | Columns, in order | Filter | Sort / layout |
|---|---|---|---|
| All projects (default) | Project, Client, Status, Type, Owner, Team, Target date, Next milestone, Start date |  | Target date |
| Board | Project, Client, Owner, Target date, Next milestone, Status |  | Board view grouped by Status, sorted by Target date |
| Due in 30 days | Project, Client, Status, Target date, Owner, Next milestone | Status is not Done **and** Target date is less than or equal to [Today]+30 | Target date |
| Migrations | Project, Client, Status, Target date, Owner, Next milestone | Type is Migration | Target date |

### 2.3 Client Activity

Create a blank list named **ClientActivity**, then rename it **Client Activity** (this keeps the web address free of spaces). Description: *The client timeline: meetings, calls, emails, decisions, changes and issues, each with an optional follow-up.*

Rename the **Title** column to **Summary**. Then add these columns. Type the internal name first, save, then rename it to the display name. This keeps the internal name clean, which the formatting and the Copilot skills rely on.

| Internal name | Display name | Type | Choices | Default | Required |
|---|---|---|---|---|---|
| Client | Client | Lookup (to Clients, show Client) |  |  | Yes |
| ActivityType | Type | Choice | Meeting, Call, Email, Decision, Change, Issue |  |  |
| ActivityDate | Date | Date (no time) |  | Today |  |
| Notes | Notes | Multiple lines of text |  |  |  |
| Owner | Owner | Person |  |  |  |
| FollowUp | Follow-up | Choice | None, Open, Done | None |  |
| NextStep | Next step | Single line of text |  |  |  |
| NextStepDue | Due | Date (no time) |  |  |  |
| TicketLink | Ticket link | Hyperlink |  |  |  |
| Sentiment | Sentiment | Choice | Positive, Neutral, Concerned |  |  |

**Views**

| View | Columns, in order | Filter | Sort / layout |
|---|---|---|---|
| Timeline (default) | Summary, Client, Type, Date, Owner, Follow-up, Next step, Due, Sentiment, Notes, Ticket link |  | Date, newest first |
| Open follow-ups | Next step, Due, Follow-up, Client, Owner, Summary, Date | Follow-up is Open | Due, earliest first |
| My follow-ups | Next step, Due, Follow-up, Client, Summary, Date | Follow-up is Open **and** Owner is [Me] | Due, earliest first |
| Decision log | Summary, Client, Date, Owner, Notes | Type is Decision | Date, newest first |
To build a view, go to **All items > Create new view**, choose List, Gallery or Board, then use **Edit current view** for the columns, filter and sort. Delete the original **All Items** view once your default view is set.

## 3. Formatting (paste-in JSON)

For each column, open the column menu, choose **Column settings > Format this column > Advanced mode**, paste the file's contents, and save.

| List | Column | File |
|---|---|---|
| Clients | Health | [formats/health-pill.json](formats/health-pill.json) |
| Projects | Status | [formats/status-pill.json](formats/status-pill.json) |
| Client Activity | Follow-up | [formats/follow-up-pill-and-mark-done.json](formats/follow-up-pill-and-mark-done.json) (pill plus a **Mark done** button) |
| Client Activity | Sentiment | [formats/sentiment-pill.json](formats/sentiment-pill.json) |
| Client Activity | Due | [formats/due-date-overdue.json](formats/due-date-overdue.json) (red when overdue and still open) |

For the **Portfolio** cards, switch to the Portfolio view, choose **Format current view > Advanced mode**, and paste [formats/portfolio-gallery-cards.json](formats/portfolio-gallery-cards.json).

## 4. Sample data (optional)

The files in [sample-data](sample-data) are fictional. The quickest way in:

1. Open a list in **grid view** (**Edit in grid view**).
2. Copy rows from the CSV opened in Excel and paste them in. Do Clients first; the Client column in the other two lists has to match a client name exactly.
3. Multi-choice columns (Products, Environments) are separated by `; ` in the CSV. Grid view may need you to pick them by hand.
4. Fill in the Person columns (owners) yourself; the sample data has no people in it.

The dates are fixed around November 2026. Change a few of them so you can see overdue follow-ups and upcoming renewals.

## 5. Finishing touches

1. **Quick step: Mark done** (where Quick steps are available). In Client Activity, choose **Add column > Quick steps**, add a step named "Mark done" that sets **Follow-up = Done**, and show it in the Open follow-ups view.
2. **Reminder.** On the **Due** column menu, choose **Set a reminder** (for example, 1 day before) to get an email before a follow-up is due. It uses a standard Power Automate flow, not a premium one.
3. **Rule** (optional). **Automate > Create a rule > When a column changes**. For example, when Follow-up changes, notify the owner.
4. **Form** (optional). On Client Activity, choose **Forms > New form** and call it "Log client activity". Add Client, Type, Date, Summary, Notes, Follow-up, Next step, Due and Ticket link. Where branching is available, show Next step and Due only when Follow-up is Open. Share the form link with the team.

## 6. Client 360 page

**Option 1: a normal page with dynamic filtering.** This works everywhere.

1. **New > Page** and choose a two-column section.
2. Left: a **List** web part showing **Clients** (All clients view, compact).
3. Right: a **List** web part showing **Projects**. Edit its properties, turn on **Dynamic filtering**, and set:
   - Column in Projects to filter: **Client**
   - List containing the filter value: **Clients**
   - Column containing the filter value: **Client**
4. Below: a **List** web part showing **Client Activity** (Timeline view), with the same dynamic filtering on **Client**.
5. Add a third List web part with the **Open follow-ups** view, unfiltered, so the page also works as a Monday to-do list.
6. Publish. If you want it as the landing page, use **Promote > Make homepage**.

Clicking a client on the left now filters its projects and timeline. If **Client** isn't offered in the dynamic filtering column list in your tenant, add a filtered view per key client instead.

**Option 2: the HTML dashboard** (optional, experimental). [deploy/client360.template.html](deploy/client360.template.html) shows KPIs, a client picker, the profile, projects, timeline and follow-ups. The deploy script fills it in and uploads it to Site Pages for you. Rendering HTML alone is not enough for live data: its hosting viewer must supply live list results. Otherwise it shows the deployment-time sample snapshot, or empty data when samples were disabled. Check the live/snapshot badges and do not treat a snapshot as current client data.

Some tenants download the HTML file instead of rendering it. Use Option 1 if HTML rendering or the experimental live-data integration is unavailable.

## 7. Visual timeline view (optional)

A view on Client Activity that puts every client's calls, decisions, changes and issues on one timeline. Open follow-ups show as flags on their due date (red when overdue), and each client's renewal date is pinned on its row. You can filter by type, switch between 3, 6 and 12 months, and click a client to focus on it.

It's an HTML list view, so it needs HTML list view support in your tenant. People who open it don't need a Copilot licence. If creation fails, the script attempts to remove the view and reports a manual step; the core lists remain usable.

**Option 1: let the script add it.** The deploy script adds it when `timelineView` is `true`, which is the default. It fills in your site's list addresses so the view can receive live rows from Client Activity and Clients. As with Client 360, check the live/snapshot status before treating the displayed data as current.

**Option 2: ask Copilot to build one.** The person building it needs a Microsoft 365 Copilot licence. In Client Activity, choose **Add view > Dashboard**, where available, name it "Visual timeline", then ask Copilot in SharePoint something like:

> "Make this a timeline with one row per Client. Plot each entry on its Date, coloured by Type. Show open follow-ups as flags on their Due date, red when overdue. Add filters for Type and a 3, 6 or 12-month range."

Copilot builds its own version, so it won't look exactly like the script's, but it reads the same list.

[deploy/timeline.template.html](deploy/timeline.template.html) is the page the script uses, if you want to read or change it. The script fills in its three placeholders (`__MANIFEST__`, `__SNAPSHOT__` and `__CONFIG__`). Client 360 links to the view when the script successfully creates it.

## 8. Copilot in SharePoint skills (optional)

Needs a Microsoft 365 Copilot licence and Copilot in SharePoint availability. Follow the [skill installation instructions](../../Skills/README.md#installing-an-experimental-skill): upload each individual folder linked below into **Agent Assets > Skills**. Where **Settings > Site skills** is available, that is another entry point.

| Skill | Try asking |
|---|---|
| [client-briefing](../../Skills/client-briefing/) | "Prep me for my Woodgrove Bank call." |
| [log-client-activity](../../Skills/log-client-activity/) | "Log this: Fabrikam IT approved the rate-limit exception. Follow up Nov 27." |
| [weekly-client-review](../../Skills/weekly-client-review/) | "Run my Monday client review." |
| [crm-change-request](../../Skills/crm-change-request/) | "Add a Region column to Clients: West, Central, East." |
| [setup-client-hub](../../Skills/setup-client-hub/) | "Set up the client hub on this site." |

The skills refer to the lists by name, so keep the list names and internal column names as they are.
