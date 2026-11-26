# PnP PowerShell route

`Deploy-NorthwindSalesHub.ps1` builds the foundation from `site/` and `content/`. SharePoint IQ adds the AI layer
afterwards. For that, see the "AI layer only" section in [../PLAYBOOK.md](../PLAYBOOK.md).

## Prerequisites

- PowerShell 7 and PnP.PowerShell 2.x or later: `Install-Module PnP.PowerShell`
- An Entra app registration for interactive sign-in: `Register-PnPEntraIDAppForInteractiveLogin`. Pass its client id as `-ClientId`.
- Site owner on the target site. You also need SharePoint admin if you use `-CreateSite`.

## Run

```powershell
./Deploy-NorthwindSalesHub.ps1 -SiteUrl https://contoso.sharepoint.com/sites/saleshub -ClientId <app-id> `
    -ApproverEmail content-approvers@contoso.com -ApproverName "Content approvers" -CreateSite
# after the SharePoint IQ form step:
./Deploy-NorthwindSalesHub.ps1 -SiteUrl ... -ClientId ... -ApproverEmail ... -PagesOnly -RequestFormViewId <form view id>
```

The script writes the ids it resolved to `deploy/tokens.local.json`. Git ignores this file. The SharePoint IQ steps
and `deploy/tools/render.py` reuse it.

## What it does and doesn't do

| Done by the script | Left to SharePoint IQ or manual |
|---|---|
| Lists, libraries, columns, unlimited-length Note columns, autofill prompts (in the field XML; verify) | Native approvals on Content Intake |
| Default views, Pick a template, Start here (view type set over REST; verify) | Quick steps and the Actions button column |
| Agent Assets folders, skills and standards, HubAssets | Tiles formatter (needs the quick step id) and the Start here HTML (needs the form id) |
| Sample files with metadata, list rows (relative dates) | Request content form |
| Pages (UTF-8 with BOM, published) and home page | Theme: Dark teal (manual) |
| Groups, unique permissions, item-level security, Publishing Desk page permissions | |
| Navigation, logo, header image, compact header | |

**Status:** not yet run end to end. The TODO markers flag the two places most likely to need adjustment: autofill
through the field XML, and setting `ViewType2` over REST.
