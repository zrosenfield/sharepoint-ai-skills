<#
.SYNOPSIS
  Deploys the Northwind Sales Hub sample (site structure, content, pages, permissions, navigation, branding)
  to a SharePoint Online communication site with PnP PowerShell.

.DESCRIPTION
  Reads the declarative definition in ../../site and ../../content and builds the "foundation":
    lists and libraries, columns (with autofill prompts where the tenant supports them), views, folders,
    agent skills, hub assets, sample files and metadata, HTML pages, home page, groups, permissions,
    navigation and header branding.

  The AI layer is created with SharePoint IQ afterwards (see ../../deploy/PLAYBOOK.md, "AI layer only"):
    approvals on Content Intake, quick steps and their Actions buttons, the Pick a template tile cards,
    the Decks "Start here" custom HTML view and the Request content form. These features have no
    supported PnP cmdlet today; the script prints the exact steps that remain.

  STATUS: this route mirrors the steps that built the reference site, but it has not yet been run end to
  end. Run it against a test site first and fix forward (see TODO markers).

.EXAMPLE
  ./Deploy-NorthwindSalesHub.ps1 -SiteUrl https://contoso.sharepoint.com/sites/saleshub -ClientId <entra-app-id> `
      -ApproverEmail content-approvers@contoso.com -ApproverName "Content approvers" -CreateSite
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)] [string] $SiteUrl,
  [Parameter(Mandatory)] [string] $ClientId,          # Entra app registration for PnP PowerShell (Register-PnPEntraIDAppForInteractiveLogin)
  [Parameter(Mandatory)] [string] $ApproverEmail,
  [string] $ApproverName = "Content approvers",
  [string] $OwnerEmail,                               # default Content owner on the sample files; defaults to the signed-in user
  [string] $SiteTitle = "Northwind Sales Hub",
  [switch] $CreateSite,
  [switch] $SkipContent,
  [switch] $PagesOnly,                                # re-render and re-publish pages only (after the IQ form step)
  [string] $RequestFormViewId                         # id of the 'Request content' form view, created by SharePoint IQ (step 07.01)
)
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "../..")
function Read-Json($rel) { Get-Content -Raw -Encoding UTF8 (Join-Path $Root $rel) | ConvertFrom-Json }

# ---------- connect ----------
$uri = [Uri]$SiteUrl
$TenantUrl = "$($uri.Scheme)://$($uri.Host)"
$SitePath = $uri.AbsolutePath.TrimEnd('/')
if ($CreateSite) {
  Connect-PnPOnline -Url $TenantUrl -Interactive -ClientId $ClientId
  if (-not (Get-PnPTenantSite -Identity $SiteUrl -ErrorAction SilentlyContinue)) {
    Write-Host "Creating communication site $SiteUrl" -ForegroundColor Cyan
    New-PnPSite -Type CommunicationSite -Title $SiteTitle -Url $SiteUrl -Lcid 1033 | Out-Null
  }
}
Connect-PnPOnline -Url $SiteUrl -Interactive -ClientId $ClientId
if (-not $OwnerEmail) { $OwnerEmail = (Get-PnPProperty -ClientObject (Get-PnPWeb) -Property CurrentUser).Email }
Set-PnPWeb -Title $SiteTitle -Description "Find, build and share approved Northwind Cloud sales content."

# ---------- tokens ----------
$Tokens = @{
  "{{SiteUrl}}" = $SiteUrl; "{{SitePath}}" = $SitePath; "{{TenantUrl}}" = $TenantUrl; "{{TenantHost}}" = $uri.Host
  "{{SiteTitle}}" = $SiteTitle; "{{ApproverEmail}}" = $ApproverEmail; "{{ApproverName}}" = $ApproverName; "{{OwnerEmail}}" = $OwnerEmail
}
function B64([string]$s) { [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($s)) }
function Resolve-Tokens([string]$text) {
  foreach ($k in $Tokens.Keys) { $text = $text.Replace($k, [string]$Tokens[$k]) }
  # relative dates: {{Today}}, {{Today+30}}, {{Today-12}}
  $text = [regex]::Replace($text, '\{\{Today([+-]\d+)?\}\}', { param($m)
    $n = if ($m.Groups[1].Success) { [int]$m.Groups[1].Value } else { 0 }
    (Get-Date).Date.AddDays($n).ToString("yyyy-MM-dd") + "T12:00:00Z" })
  return $text
}
function Assert-NoTokens([string]$text, [string]$what) {
  $left = [regex]::Matches($text, '\{\{[^}]+\}\}') | ForEach-Object Value | Select-Object -Unique
  if ($left) { Write-Warning "$what still has unresolved tokens: $($left -join ', ')" }
}

# ---------- pages ----------
function Publish-Pages {
  $utf8Bom = New-Object System.Text.UTF8Encoding($true)
  $tmp = Join-Path ([IO.Path]::GetTempPath()) ("nwhub-" + [Guid]::NewGuid())
  New-Item -ItemType Directory $tmp | Out-Null
  foreach ($pg in $site.pages) {
    $html = Resolve-Tokens (Get-Content -Raw -Encoding UTF8 (Join-Path $Root "site/pages/$($pg.file)"))
    Assert-NoTokens $html $pg.file
    $out = Join-Path $tmp $pg.file
    [IO.File]::WriteAllText($out, $html, $utf8Bom)   # UTF-8 with BOM, or a middle dot renders as 'Â·'
    Add-PnPFile -Path $out -Folder "SitePages" -Publish -PublishComment "Deployed" | Out-Null
  }
  Set-PnPHomePage -RootFolderRelativeUrl "SitePages/Home.html"
}
$site = Read-Json "site/site.json"
$tokFile = Join-Path $Root "deploy/tokens.local.json"
if ($PagesOnly) {
  if (Test-Path $tokFile) { (Get-Content -Raw $tokFile | ConvertFrom-Json).PSObject.Properties | ForEach-Object { if (-not $Tokens.ContainsKey($_.Name)) { $Tokens[$_.Name] = $_.Value } } }
  if ($RequestFormViewId) { $Tokens["{{ViewIdB64:Content Requests/Request content}}"] = B64 $RequestFormViewId }
  Publish-Pages
  Write-Host "Pages re-published." -ForegroundColor Green
  return
}

# ---------- lists, columns, views ----------
$defs = $site.lists | Sort-Object order | ForEach-Object { Read-Json $_.definition }

function Get-FieldXml($c, [string[]]$unlimited) {
  $n = [Security.SecurityElement]::Escape($c.internalName); $d = [Security.SecurityElement]::Escape($c.displayName)
  $req = if ($c.required) { "TRUE" } else { "FALSE" }
  $auto = ""
  if ($c.metadataExtractionPrompt) {
    # Autofill (Copilot/Syntex). Same attribute the reference site stores; ignored where autofill is not available. TODO: verify on a tenant with autofill.
    $info = @{ LLM = @{ IsEnabled = $true; Prompt = $c.metadataExtractionPrompt; OverwriteMode = 1 } } | ConvertTo-Json -Compress -Depth 5
    $auto = " AutofillInfo=""$([Security.SecurityElement]::Escape($info))"""
  }
  $def = if ($c.defaultValueFields) { "<Default>$([Security.SecurityElement]::Escape($c.defaultValueFields.defaultValue))</Default>" } else { "" }
  $choices = if ($c.choices) { "<CHOICES>" + (($c.choices | ForEach-Object { "<CHOICE>$([Security.SecurityElement]::Escape($_))</CHOICE>" }) -join "") + "</CHOICES>" } else { "" }
  switch ($c.type) {
    "Text"        { "<Field Type=""Text"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req""$auto />" }
    "Note"        { $u = if ($unlimited -contains $c.internalName) { " UnlimitedLengthInDocumentLibrary=""TRUE""" } else { "" }
                    "<Field Type=""Note"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req"" NumLines=""6"" RichText=""FALSE""$u$auto />" }
    "Choice"      { "<Field Type=""Choice"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req"" Format=""Dropdown""$auto>$def$choices</Field>" }
    "MultiChoice" { "<Field Type=""MultiChoice"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req""$auto>$def$choices</Field>" }
    "Number"      { $min = if ($null -ne $c.min) { " Min=""$($c.min)""" } else { "" }; "<Field Type=""Number"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req""$min$auto />" }
    "Boolean"     { "<Field Type=""Boolean"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"">$(if ($def) { $def } else { '<Default>0</Default>' })</Field>" }
    "DateTime"    { "<Field Type=""DateTime"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req"" Format=""DateOnly""$auto />" }
    "URL"         { $f = if ($c.format -eq "Image") { "Image" } else { "Hyperlink" }; "<Field Type=""URL"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req"" Format=""$f"" />" }
    "User"        { "<Field Type=""User"" Name=""$n"" StaticName=""$n"" DisplayName=""$d"" Required=""$req"" UserSelectionMode=""PeopleOnly"" />" }
    default       { $null }   # QuickSteps (Actions) is created by SharePoint IQ
  }
}

$ListIds = @{}
foreach ($d in $defs) {
  Write-Host "List: $($d.title)" -ForegroundColor Cyan
  $tpl = if ($d.template -eq "DocumentLibrary") { "DocumentLibrary" } else { "GenericList" }
  $list = Get-PnPList -Identity $d.title -ErrorAction SilentlyContinue
  if (-not $list) { $list = Get-PnPList -Identity "$SitePath/$($d.url)" -ErrorAction SilentlyContinue }
  if (-not $list) {
    $list = New-PnPList -Title $d.title -Url $d.url -Template $tpl -OnQuickLaunch:$false
  }
  Set-PnPList -Identity $list -Description $d.description -EnableVersioning $true | Out-Null
  $ListIds[$d.title] = $list.Id.ToString()
  $Tokens["{{ListId:$($d.title)}}"] = $list.Id.ToString()
  $Tokens["{{ListIdB64:$($d.title)}}"] = B64 $list.Id.ToString()
  $existing = Get-PnPField -List $list | ForEach-Object InternalName
  foreach ($c in $d.columns) {
    if ($c.internalName -eq "Title") {
      if ($c.editSchemaXml -match 'DisplayName="([^"]+)"') { Set-PnPField -List $list -Identity Title -Values @{ Title = $Matches[1] } | Out-Null }
      continue
    }
    if ($existing -contains $c.internalName) { continue }
    $xml = Get-FieldXml $c $d.unlimitedLength
    if ($xml) { Add-PnPFieldFromXml -List $list -FieldXml $xml | Out-Null }
  }
  foreach ($f in @($d.unlimitedLength)) { if ($f) { Set-PnPField -List $list -Identity $f -Values @{ UnlimitedLengthInDocumentLibrary = $true } | Out-Null } }
}

foreach ($d in $defs) {
  foreach ($v in @($d.views)) {
    if (-not $v) { continue }
    $fields = @($v.viewFields | Where-Object { $_ -ne "Actions" -or (Get-PnPField -List $d.title -Identity Actions -ErrorAction SilentlyContinue) })
    $view = Get-PnPView -List $d.title -Identity $v.name -ErrorAction SilentlyContinue
    if ($view) { Set-PnPView -List $d.title -Identity $view -Fields $fields | Out-Null }
    else {
      $p = @{ List = $d.title; Title = $v.name; Fields = $fields; SetAsDefault = [bool]$v.isDefaultView }
      if ($v.query) { $p.Query = $v.query }
      $view = Add-PnPView @p
    }
    if ($v.isDefaultView) { Set-PnPView -List $d.title -Identity $view -Values @{ DefaultView = $true } | Out-Null }
    $Tokens["{{ViewId:$($d.title)/$($v.name)}}"] = $view.Id.ToString()
    $Tokens["{{ViewIdB64:$($d.title)/$($v.name)}}"] = B64 $view.Id.ToString()
    if ($v.viewType2) {
      # TILES and CUSTOMHTML views. TODO: confirm ViewType2 is writable through REST on your tenant; if not, create these two views with SharePoint IQ (steps 06.*).
      Invoke-PnPSPRestMethod -Method Merge -Url "$SiteUrl/_api/web/lists(guid'$($ListIds[$d.title])')/views(guid'$($view.Id)')" -Content @{ ViewType2 = $v.viewType2 } | Out-Null
    }
  }
}

# ---------- folders, skills, hub assets ----------
foreach ($f in (Read-Json "site/lists/10-agent-assets.json").folders) { Resolve-PnPFolder -SiteRelativePath "AgentAssets/$($f.path)" | Out-Null }
Get-ChildItem (Join-Path $Root "site/agent-assets") -Recurse -File | ForEach-Object {
  $rel = $_.FullName.Substring((Join-Path $Root "site/agent-assets").Length + 1).Replace('\', '/')
  Add-PnPFile -Path $_.FullName -Folder ("AgentAssets/" + (Split-Path $rel -Parent).Replace('\', '/')) | Out-Null
}
Get-ChildItem (Join-Path $Root "site/hub-assets") -File | ForEach-Object { Add-PnPFile -Path $_.FullName -Folder "HubAssets" | Out-Null }
"nw-header.png", "nw-mark.png" | ForEach-Object { Add-PnPFile -Path (Join-Path $Root "site/branding/$_") -Folder "HubAssets" | Out-Null }

# ---------- sample content ----------
function ConvertTo-PnPValue($name, $val, $fieldType) {
  if ($val -is [string]) { $val = Resolve-Tokens $val }
  switch ($fieldType) {
    "URL"      { if ($val -is [string]) { return $val } ; return "$(Resolve-Tokens $val.Url), $(Resolve-Tokens $val.Description)" }
    "User"     { return $val }
    "Boolean"  { return [bool]$val }
    default    { return $val }
  }
}
if (-not $SkipContent) {
  $seed = Get-Content -Raw -Encoding UTF8 (Join-Path $Root "content/seed.json") | ConvertFrom-Json
  foreach ($d in $defs) {
    $rows = $seed.($d.title); if (-not $rows) { continue }
    $types = @{}; Get-PnPField -List $d.title | ForEach-Object { $types[$_.InternalName] = $_.TypeAsString }
    foreach ($r in $rows) {
      $values = @{}
      foreach ($p in $r.PSObject.Properties) {
        if ($p.Name -eq "file") { continue }
        $values[$p.Name] = ConvertTo-PnPValue $p.Name $p.Value $types[$p.Name]
      }
      if ($r.file) {
        $path = Join-Path $Root ("content/" + $d.title + "/" + $r.file)
        $file = Add-PnPFile -Path $path -Folder $d.url -Values $values
        $Tokens["{{ItemId:$($d.title)/$($r.file)}}"] = $file.ListItemAllFields.Id
      } else {
        Add-PnPListItem -List $d.title -Values $values | Out-Null
      }
    }
  }
}

# ---------- pages (first pass; the Request content link resolves after the IQ form step) ----------
Publish-Pages

# ---------- groups and permissions ----------
$web = Get-PnPWeb -Includes AssociatedOwnerGroup, AssociatedMemberGroup, AssociatedVisitorGroup
$G = @{ "Owners" = $web.AssociatedOwnerGroup; "Content Team" = $web.AssociatedMemberGroup; "Sellers" = $web.AssociatedVisitorGroup }
foreach ($g in $site.groups) {
  $title = Resolve-Tokens $g.title
  Set-PnPGroup -Identity $G[$g.key] -Title $title -Description $g.description | Out-Null
  $G[$g.key] = Get-PnPGroup -Identity $title
}
function Set-Perms($listTitle, $perms) {
  if (-not $perms) { return }
  Set-PnPList -Identity $listTitle -BreakRoleInheritance -CopyRoleAssignments | Out-Null
  foreach ($r in @($perms.remove)) { if (-not $r) { continue }
    $grp, $role = $r.Split(':'); if (-not $role) { $role = if ($grp -eq "Sellers") { "Read" } else { "Edit" } }
    Set-PnPListPermission -Identity $listTitle -Group $G[$grp] -RemoveRole $role | Out-Null }
  foreach ($r in @($perms.grant)) { if (-not $r) { continue }
    $grp, $role = $r.Split(':'); Set-PnPListPermission -Identity $listTitle -Group $G[$grp] -AddRole $role | Out-Null }
  if ($perms.itemLevel) { $l = Get-PnPList -Identity $listTitle; $l.ReadSecurity = $perms.itemLevel.ReadSecurity; $l.WriteSecurity = $perms.itemLevel.WriteSecurity; $l.Update(); Invoke-PnPQuery }
}
foreach ($d in $defs) { Set-Perms $d.title $d.permissions }
$desk = Get-PnPFile -Url "SitePages/PublishingDesk.html" -AsListItem
Set-PnPListItemPermission -List "Site Pages" -Identity $desk.Id -Group $G["Sellers"] -RemoveRole "Read" | Out-Null   # breaks inheritance and removes Sellers

# ---------- navigation and branding ----------
Invoke-PnPSPRestMethod -Method Merge -Url "$SiteUrl/_api/web" -Content @{ QuickLaunchEnabled = $true; MegaMenuEnabled = $true; HorizontalQuickLaunch = $true } | Out-Null
Get-PnPNavigationNode -Location QuickLaunch | ForEach-Object { Remove-PnPNavigationNode -Identity $_.Id -Force }
foreach ($n in $site.navigation.quickLaunch) {
  $node = Add-PnPNavigationNode -Location QuickLaunch -Title $n.title -Url (Resolve-Tokens $n.url) -External
  foreach ($c in @($n.children)) { if ($c) { Add-PnPNavigationNode -Location QuickLaunch -Title $c.title -Url (Resolve-Tokens $c.url) -Parent $node.Id -External | Out-Null } }
}
Set-PnPWebHeader -SiteLogoUrl "$SitePath/HubAssets/nw-mark.png" -SiteThumbnailUrl "$SitePath/HubAssets/nw-mark.png" -HeaderLayout Compact -HeaderEmphasis Strong
Invoke-PnPSPRestMethod -Method Post -Url "$SiteUrl/_api/siteiconmanager/setsitelogo" -Content @{ relativeLogoUrl = "$SitePath/HubAssets/nw-header.png"; type = 2; aspect = 0 } | Out-Null

# ---------- hand-off ----------
$Tokens | ConvertTo-Json | Set-Content -Encoding UTF8 $tokFile
Write-Host ""
Write-Host "Foundation deployed to $SiteUrl" -ForegroundColor Green
Write-Host "Resolved ids saved to deploy/tokens.local.json (git-ignored)."
Write-Host "Next, with Copilot + SharePoint IQ, run the AI layer (deploy/PLAYBOOK.md > 'AI layer only'):" -ForegroundColor Yellow
Write-Host "  - Approvals on Content Intake; quick steps and Actions buttons (phase 05)"
Write-Host "  - Pick a template tiles (phase 06)"
Write-Host "  - Request content form (07.01; its id is formId= in the result's formEditUrl), then the Decks 'Start here' HTML (07.03)"
Write-Host "  - Then: ./Deploy-NorthwindSalesHub.ps1 -SiteUrl ... -ClientId ... -ApproverEmail ... -PagesOnly -RequestFormViewId <id>"
Write-Host "Manual: on the home page, Settings > Change the look > Theme > Dark teal."
