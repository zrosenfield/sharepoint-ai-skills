#!/usr/bin/env python3
"""Write ordered SharePoint IQ job files for installing the Obligation Hub from Cowork.

Each job file is a JSON array of {"label", "mode": "call", "tool", "arguments"[, "argFiles"]} for a
helper that calls the SharePoint IQ tools one by one (argFiles name local files whose text becomes
that argument, e.g. a skill's SKILL.md). Everything comes from ../spec.json.

    python3 build_jobs.py --site-url https://contoso.sharepoint.com/sites/obligations \
        --site-key <key from get_site_key> --out ../../../../live/obligation-hub-jobs
    # run phase1_lists.json, then discover_sharepoint_lists and save its result, then:
    python3 build_jobs.py ... --lists discover.json --owner-value '<get_user_info formattedValue>'

Phases 1-3 need only the site URL. Phases 4-6 need the list IDs (--lists) and, for Person columns,
your formatted user value (--owner-value, or --owner-email). Generated jobs hold your site key and
list IDs: keep them out of the repository.
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
COLUMN_SPLIT = 13  # Obligations columns per call: one call with all columns and views failed ("too many stages")


def jdump(o):
    return json.dumps(o, ensure_ascii=False)


def find_lists(path, spec, site_rel):
    """Map spec list keys to {id, url} from a discover_sharepoint_lists result (any nesting, any key case)."""
    data = json.load(open(path, encoding="utf-8"))
    found = []

    def walk(o):
        if isinstance(o, dict):
            low = {k.lower(): v for k, v in o.items()}
            lid = low.get("id") or low.get("listid") or low.get("guid")
            title = low.get("title") or low.get("listtitle") or low.get("name")
            url = low.get("serverrelativeurl") or low.get("listurl") or low.get("url") or low.get("rooturl")
            if isinstance(low.get("rootfolder"), dict):
                url = url or low["rootfolder"].get("ServerRelativeUrl") or low["rootfolder"].get("serverRelativeUrl")
            if isinstance(lid, str) and re.fullmatch(r"\{?[0-9a-fA-F-]{36}\}?", lid) and (title or url):
                found.append({"id": lid.strip("{}"), "title": title or "", "url": url or ""})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    out = {}
    for L in spec["lists"]:
        want = (site_rel + "/" + L["url"]).lower()
        for f in found:
            u = re.sub(r"^https?://[^/]+", "", f["url"]).rstrip("/").lower()
            if u.endswith("/forms/allitems.aspx"):
                u = u[: -len("/forms/allitems.aspx")]
            if u == want or (not u and f["title"] == L["title"]):
                out[L["key"]] = {"id": f["id"], "url": site_rel + "/" + L["url"]}
                break
    return out


def column_json(c, company, autofill):
    o = {"internalName": c["internalName"], "displayName": c["displayName"], "type": c["type"]}
    if c.get("choices"):
        o["choices"] = c["choices"]
    if c["type"] in ("DateTime", "URL") and c.get("format"):
        o["format"] = c["format"]
    if c.get("default") is not None:
        o["defaultValueFields"] = {"defaultValue": c["default"]}
    if autofill and c.get("autofillPrompt"):
        o["metadataExtractionPrompt"] = re.sub(r"\.\.(\s|$)", r".\1", c["autofillPrompt"].replace("{{OUR_COMPANY}}", company))
    return jdump(o)


def title_json(L):
    return jdump({"internalName": "Title", "displayName": "Title", "type": "Text",
                  "editSchemaXml": '<Field InternalName="Title" Type="Text" DisplayName="%s" />' % L["titleDisplayName"]})


def view_json(V):
    o = {"name": V["name"], "isNewView": True}
    if V.get("default"):
        o["isDefaultView"] = True
    if V.get("type") == "calendar":
        o["viewType2"] = "MODERNCALENDAR"
        o["viewFields"] = V["fields"]
        o["calendarSettings"] = V["calendar"]
        return jdump(o)
    o["viewFields"] = V["fields"]
    if V.get("query"):
        o["query"] = V["query"]
    if V.get("rowLimit") and V["rowLimit"] != 30:
        o["rowLimit"] = V["rowLimit"]
    return jdump(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default=str(HERE.parent / "spec.json"))
    ap.add_argument("--site-url", required=True, help="absolute site URL, e.g. https://contoso.sharepoint.com/sites/obligations")
    ap.add_argument("--site-key", default="{{SITE_KEY}}", help="the opaque key from get_site_key (default: a {{SITE_KEY}} placeholder)")
    ap.add_argument("--out", required=True, help="output folder for the job files (keep it outside the repository)")
    ap.add_argument("--lists", help="saved discover_sharepoint_lists result; needed for phases 4-6")
    ap.add_argument("--owner-value", help="Person value for you, exactly as get_user_info returns it (formattedValue)")
    ap.add_argument("--owner-email", help="your email; used to build a Person value when --owner-value isn't given")
    ap.add_argument("--company", help="legal name used for 'Us' (default: the sample company with --sample, else required)")
    ap.add_argument("--recipients", default="", help="comma-separated leadership digest recipients (default: --owner-email)")
    ap.add_argument("--sample", action="store_true", help="also write phase5_sample.json (sample contracts, pre-captured obligations, Run Log seed)")
    ap.add_argument("--no-autofill", action="store_true", help="create the Contracts columns without autofill prompts")
    ap.add_argument("--today", help="YYYY-MM-DD used to compute Timing for the sample obligations (default: today)")
    ap.add_argument("--confirmed", action="store_true", help='add "confirmed": true to write jobs (only if your helper has your approval)')
    ap.add_argument("--paths-relative-to", default=os.getcwd(), help="argFiles paths are written relative to this folder (your helper's working folder)")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    site = a.site_url.rstrip("/")
    m = re.match(r"^(https://[^/]+)(/.*)?$", site)
    if not m:
        sys.exit("--site-url must be an absolute https URL")
    site_rel = m.group(2) or ""
    company = a.company or (spec["sampleData"]["company"] if a.sample else None)
    if not company:
        sys.exit("--company is required without --sample")
    out = Path(a.out).resolve()
    (out / "files").mkdir(parents=True, exist_ok=True)
    rel = lambda p: os.path.relpath(str(Path(p).resolve()), a.paths_relative_to).replace("\\", "/")
    by = {L["key"]: L for L in spec["lists"]}
    lurl = lambda k: site_rel + "/" + by[k]["url"]
    autofill = not a.no_autofill
    warnings = []

    def job(label, tool, args, argfiles=None, write=True):
        j = {"label": label, "mode": "call", "tool": tool}
        if write and a.confirmed:
            j["confirmed"] = True
        j["arguments"] = dict({"siteKey": a.site_key}, **args)
        if argfiles:
            j["argFiles"] = argfiles
        return j

    def write(name, jobs):
        (out / name).write_text(json.dumps(jobs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote %s (%d jobs)" % (out / name, len(jobs)))

    # ---- phase 1: lists and columns (no views) --------------------------------------------------
    p1 = []
    for L in spec["lists"]:
        lib = L["template"] == "DocumentLibrary"
        cols = [column_json(c, company, autofill) for c in L["columns"]]
        has_prompts = any("metadataExtractionPrompt" in c for c in cols)
        common = {"listName": L["title"], "templateType": L["template"], "enableApprovals": False, "restriction_to_author": False,
                  "isManualColumnCreation": not (lib and has_prompts), "listDescription": L["description"]}
        label = L["title"] + (" (skip if the site already has it)" if L.get("ifExists") == "reuse" else "")
        if len(cols) > COLUMN_SPLIT:
            first = dict(common, isNewList=True, addNavLink=L["navLink"], columns=[title_json(L)] + cols[:COLUMN_SPLIT - 1], views=[])
            second = dict(common, isNewList=False, addNavLink=False, serverRelativeListUrl=lurl(L["key"]), columns=cols[COLUMN_SPLIT - 1:], views=[])
            p1.append(job("%s columns 1-%d" % (L["title"], COLUMN_SPLIT), "create_or_update_list", first))
            p1.append(job("%s columns %d-%d" % (L["title"], COLUMN_SPLIT + 1, len(cols) + 1), "create_or_update_list", second))
        else:
            p1.append(job(label, "create_or_update_list", dict(common, isNewList=True, addNavLink=L["navLink"], columns=[title_json(L)] + cols, views=[])))
    write("phase1_lists.json", p1)

    # ---- phase 2: views (separate calls; Obligations in two halves) -----------------------------
    p2 = []
    for L in spec["lists"]:
        if not L["views"]:
            continue
        lib = L["template"] == "DocumentLibrary"
        common = {"listName": L["title"], "templateType": L["template"], "enableApprovals": False, "restriction_to_author": False,
                  "isManualColumnCreation": not lib, "isNewList": False, "addNavLink": False, "serverRelativeListUrl": lurl(L["key"]), "columns": []}
        views = [view_json(V) for V in L["views"]]
        chunks = [views[:4], views[4:]] if len(views) > 4 else [views]
        for i, ch in enumerate(chunks):
            p2.append(job("%s views%s" % (L["title"], " (%d of %d)" % (i + 1, len(chunks)) if len(chunks) > 1 else ""), "create_or_update_list", dict(common, views=ch)))
    write("phase2_views.json", p2)

    # ---- phase 3: column formatting ------------------------------------------------------------
    p3 = []
    for f in spec["formats"]:
        fmt = json.load(open(REPO / f["file"], encoding="utf-8"))
        p3.append(job("Format " + f["field"], "apply_column_formatting_v2", {
            "listName": by[f["list"]]["title"], "internalFieldName": f["field"], "customFormatterJson": jdump(fmt), "replaceExistingFillColors": True}))
    write("phase3_formatting.json", p3)

    # ---- phases 4-6 need list IDs ----------------------------------------------------------------
    if not a.lists:
        print("phases 4-6 not written: run phase 1, save the discover_sharepoint_lists result, and run again with --lists <file>")
        return
    ids = find_lists(a.lists, spec, site_rel)
    need = ["agentassets", "obligations", "contracts"]
    miss = [k for k in need if k not in ids]
    if miss:
        sys.exit("couldn't find these lists in %s: %s" % (a.lists, ", ".join(by[k]["title"] for k in miss)))
    if a.owner_value:
        owner = a.owner_value
    elif a.owner_email:
        owner = jdump([{"Key": "i:0#.f|membership|" + a.owner_email, "EntityData": {"Email": a.owner_email}}])
    else:
        owner = "{{OWNER}}"
        warnings.append("Person values are a {{OWNER}} placeholder: pass --owner-value (get_user_info formattedValue) or --owner-email")
    recipients = [x.strip() for x in a.recipients.split(",") if x.strip()] or ([a.owner_email] if a.owner_email else [])

    # ---- phase 4: seeds, folders, skills, site context, settings ---------------------------------
    p4 = []
    trows = spec["seeds"]["obligationTypes"]["rows"]
    keys = ["Title", "Category", "Handling", "DefaultRisk", "DefaultRecurrence", "Description", "Examples"]
    for i in range(0, len(trows), 100):
        p4.append(job("Seed Obligation Types", "create_list_items_v2", {"listUrl": lurl("types"), "items": [
            {"fieldInternalNames": [k for k in keys if r.get(k) not in (None, "")], "values": [str(r[k]) for k in keys if r.get(k) not in (None, "")]} for r in trows[i:i + 100]]}))
    rules = spec["seeds"]["ownerRules"]["rows"] + (spec["seeds"]["ownerRules"]["sampleRows"] if a.sample else [])
    p4.append(job("Seed Obligation Owners", "create_list_items_v2", {"listUrl": lurl("owners"), "items": [
        {"fieldInternalNames": ["Title", "Category", "BusinessUnit", "Owner", "EscalationOwner", "Notify"],
         "values": [r["Title"], r["Category"], r["BusinessUnit"], owner, owner, r["Notify"]]} for r in rules]}))
    AA = spec["agentAssets"]
    aa_full = m.group(1) + lurl("agentassets")
    aa_id = ids["agentassets"]["id"]
    p4.append(job("Folders Skills+Config", "create_folder", {"listFullUrl": aa_full, "listId": aa_id,
                                                              "folders": [{"name": f["path"], "folderColor": f["color"]} for f in AA["folders"]]}))
    skills = [s for s in AA["skills"] if s["upload"]]
    p4.append(job("Skill folders", "create_folder", {"listFullUrl": aa_full, "listId": aa_id, "folders": [
        {"name": s["name"], "relativeFolderPath": AA["skillsRoot"], "folderColor": AA["skillFolderColor"]} for s in skills]}))
    subs = sorted({(s["name"], f.rsplit("/", 1)[0]) for s in skills for f in s["files"] if "/" in f})
    if subs:
        p4.append(job("Skill subfolders", "create_folder", {"listFullUrl": aa_full, "listId": aa_id, "folders": [
            {"name": sub, "relativeFolderPath": AA["skillsRoot"] + "/" + name, "folderColor": AA["skillFolderColor"]} for name, sub in subs]}))
    for s in skills:
        for f in s["files"]:
            src = REPO / AA["skillsRoot"] / s["name"] / f
            if not src.exists():
                warnings.append("missing skill file %s" % src)
                continue
            folder, _, fname = (lurl("agentassets") + "/" + AA["skillsRoot"] + "/" + s["name"] + "/" + f).rpartition("/")
            p4.append(job("Upload skill %s/%s" % (s["name"], f), "upload_file", {"folderServerRelativeUrl": folder, "fileName": fname, "contentType": "text", "overwrite": True},
                          {"content": rel(src)}))
    ctx_src = REPO / AA["siteContext"]["source"]
    if ctx_src.exists():
        p4.append(job("Upload SHAREPOINT.md (AgentAssets root; skip if the site has its own)", "upload_file", {
            "folderServerRelativeUrl": lurl("agentassets"), "fileName": AA["siteContext"]["target"], "contentType": "text", "overwrite": False}, {"content": rel(ctx_src)}))
    else:
        warnings.append("missing %s" % ctx_src)
    tmpl = REPO / AA["settings"]["source"]
    settings = json.load(open(tmpl, encoding="utf-8")) if tmpl.exists() else json.loads(json.dumps(AA["settings"]["defaults"]))
    settings.pop("_tokens", None)
    if "_about" in settings:
        settings["_about"] = "Obligation Hub settings, written by the Cowork installer. Every hub skill reads this file first. Keys starting with _ are ignored."
    settings.update({"ourCompany": company, "siteUrl": site, "leadershipRecipients": recipients})
    sfile = out / "files" / "hub-settings.json"
    sfile.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sfolder, _, sname = (lurl("agentassets") + "/" + AA["settings"]["target"]).rpartition("/")
    p4.append(job("Upload hub-settings.json", "upload_file", {"folderServerRelativeUrl": sfolder, "fileName": sname, "contentType": "text", "overwrite": False}, {"content": rel(sfile)}))
    write("phase4_seeds_folders_uploads.json", p4)

    # ---- phase 5: sample data ----------------------------------------------------------------------
    if a.sample:
        p5 = []
        SD = spec["sampleData"]
        (out / "files" / "contracts").mkdir(exist_ok=True)
        for c in SD["contracts"]["items"]:
            b64 = out / "files" / "contracts" / (c["fileName"] + ".b64")
            b64.write_text(base64.b64encode((REPO / c["file"]).read_bytes()).decode("ascii"), encoding="ascii")
            p5.append(job("Upload " + c["fileName"], "upload_file", {"folderServerRelativeUrl": lurl("contracts"), "fileName": c["fileName"],
                                                                      "contentType": "base64", "overwrite": False}, {"content": rel(b64)}))
        items = []
        for i, c in enumerate(SD["contracts"]["items"], start=1):
            f = dict(c["fields"])
            names, vals = [], []
            for k, v in f.items():
                if k in ("EffectiveDate", "ExpirationDate"):
                    v = v + "T12:00:00Z"
                elif k == "ContractOwner":
                    v = owner
                elif k == "IsSample":
                    v = "1" if v else "0"
                names.append(k)
                vals.append(str(v))
            items.append({"itemId": i, "fieldInternalNames": names, "newValues": vals})
        p5.append(job("Contract key terms (a new library numbers the uploads 1-%d in this order)" % len(items), "update_list_items_v2",
                      {"listUrl": lurl("contracts"), "items": items}))
        obs = json.load(open(REPO / SD["obligations"]["source"], encoding="utf-8"))
        today = a.today or dt.date.today().isoformat()
        soon = (dt.date.fromisoformat(today) + dt.timedelta(days=int(settings.get("dueSoonDays") or 14))).isoformat()
        closed = {"Fulfilled", "Waived", "Not applicable"}
        order = ["Title", "ContractName", "ContractLink", "Counterparty", "ObligationText", "ClauseRef", "SourceClause", "Party", "Category",
                 "TriggerType", "Recurrence", "DueDate", "TriggerEvent", "BusinessUnit", "Status", "Timing", "ReviewState", "Confidence", "Risk",
                 "CaptureKey", "Notes", "IsSample", "Owner", "EscalationOwner"]
        oitems = []
        for o in obs:
            d = o.get("DueDate")
            v = dict(o)
            v["Timing"] = "Closed" if o["Status"] in closed else "No date" if not d else "Overdue" if d < today else "Due soon" if d <= soon else "Upcoming"
            v["ContractLink"] = "%s/%s/%s, %s" % (site, by["contracts"]["url"], o["ContractName"], o["ContractName"])
            v["DueDate"] = d + "T12:00:00Z" if d else None
            v["IsSample"] = "1"
            if o["ReviewState"] == "Confirmed" and o["Status"] not in closed:
                v["Owner"] = v["EscalationOwner"] = owner
            names = [k for k in order if v.get(k) not in (None, "")]
            oitems.append({"fieldInternalNames": names, "values": [str(v[k]) for k in names]})
        for i in range(0, len(oitems), 100):
            p5.append(job("Load pre-captured obligations", "create_list_items_v2", {"listUrl": lurl("obligations"), "items": oitems[i:i + 100]}))
        runs = json.load(open(REPO / SD["runLog"]["source"], encoding="utf-8"))
        rorder = ["Title", "Workflow", "Outcome", "ContractName", "ContractVersion", "ItemsCreated", "ItemsUpdated", "ItemsHeld", "Details", "RunAt"]
        ritems = []
        for r in runs:
            names = [k for k in rorder if r.get(k) not in (None, "")]
            ritems.append({"fieldInternalNames": names, "values": [str(r[k]) for k in names]})
        p5.append(job("Load Run Log demo seed", "create_list_items_v2", {"listUrl": lurl("runlog"), "items": ritems}))
        write("phase5_sample.json", p5)

    # ---- phase 6: quick steps and the Setup Run Log row ----------------------------------------------
    p6 = []
    for s in spec["quickSteps"]:
        L = by[s["list"]]
        p6.append(job("QS " + s["title"], "create_or_update_quick_step", {
            "listId": ids[s["list"]]["id"], "listUrl": lurl(s["list"]), "isDocLib": L["template"] == "DocumentLibrary", "title": s["title"],
            "isActive": True, "condition": s["condition"], "action": {"actionType": s["actionType"], "customPrompt": s["prompt"]}}))
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    p6.append(job("Run Log: Setup row", "create_list_items_v2", {"listUrl": lurl("runlog"), "items": [{
        "fieldInternalNames": ["Title", "Workflow", "Outcome", "ItemsCreated", "ItemsUpdated", "ItemsHeld", "Details", "RunAt"],
        "values": ["Setup - Cowork installer", "Setup", "Succeeded", "0", "0", "0",
                   "Installed with deploy/cowork/build_jobs.py (spec v%s)%s." % (spec["solution"]["version"], ", with sample data" if a.sample else ""), now]}]}))
    write("phase6_quicksteps.json", p6)
    for w in warnings:
        print("WARNING: " + w)


if __name__ == "__main__":
    main()
