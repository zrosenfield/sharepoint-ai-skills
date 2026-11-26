/*!
 * Obligation Hub for SharePoint: remove script (v1.0). Unofficial and unsupported.
 *
 * Moves the Obligation Hub to the site recycle bin, where you can restore it for 93 days:
 *   - the lists and libraries Contracts, Obligations, Obligation Owners, Obligation Types, Exclusions,
 *     Run Log and Evidence (with everything in them, including their quick steps and autofill settings)
 *   - the 7 hub pages in Site Pages (Home.html, MyObligations.html, Contract360.html, ReviewQueue.html,
 *     Leadership.html, Settings.html, HowItWorks.html); the home page goes back to SitePages/Home.aspx
 *     if it was SitePages/Home.html
 *   - the hub's skill folders in AgentAssets/Skills, AgentAssets/Config/hub-settings.json, and
 *     AgentAssets/SHAREPOINT.md only if it is the hub's (it mentions "Obligation Hub")
 *   - the hub's links in the site navigation (only links with the hub's titles and addresses; links
 *     can't go to the recycle bin, so these are deleted)
 * It never touches the AgentAssets library itself, other skills, other lists, pages or navigation links,
 * or the site's theme, logo and header (change those in Settings > Change the look).
 * It shows exactly what it found and asks once before it changes anything.
 * Run it the same way as the deploy script: site home page, F12, Console, paste, Enter.
 */
(async function obligationHubRemove() {
  "use strict";

  const OPTIONS = {
    assetsBaseUrl: "https://raw.githubusercontent.com/zrosenfield/sharepoint-ai-skills/master" // only used to read spec.json
  };
  const SPEC_EMBEDDED = /*REMOVE-SPEC-BEGIN*/{"solution":{"name":"obligation-hub-for-sharepoint","title":"Obligation Hub for SharePoint","short":"obligation-hub","version":"1.0.0","status":"experimental","kitPath":"solutions/obligation-hub-for-sharepoint","referenceDate":"2026-11-24","logTag":"Obligation Hub"},"lists":[{"key":"contracts","title":"Contracts","url":"Contracts","description":"Signed contracts and amendments. Key terms fill in automatically; adding or changing a contract starts obligation capture.","ifExists":"refuse"},{"key":"obligations","title":"Obligations","url":"Lists/Obligations","description":"Every tracked contract obligation: who owes what, by when, and what triggers it.","ifExists":"refuse"},{"key":"owners","title":"Obligation Owners","url":"Lists/Obligation Owners","description":"Routing rules used to assign new obligations. The most specific matching rule wins.","ifExists":"refuse"},{"key":"types","title":"Obligation Types","url":"Lists/Obligation Types","description":"What counts as a trackable obligation. Capture uses this to classify, keep or exclude.","ifExists":"refuse"},{"key":"exclusions","title":"Exclusions","url":"Lists/Exclusions","description":"Clauses or obligation patterns that should not be tracked.","ifExists":"refuse"},{"key":"runlog","title":"Run Log","url":"Lists/Run Log","description":"Every automated run: what it did and whether it worked. Failures show on the home page.","ifExists":"refuse"},{"key":"evidence","title":"Evidence","url":"Evidence","description":"Proof that obligations were fulfilled. Linked from each obligation's Evidence field.","ifExists":"refuse"},{"key":"agentassets","title":"AgentAssets","url":"AgentAssets","description":"Site skills for Copilot in SharePoint and AI workflows (Skills/<skill-name>/SKILL.md).","ifExists":"reuse"}],"agentAssets":{"list":"agentassets","skillsRoot":"Skills","siteContext":{"target":"SHAREPOINT.md","marker":"Obligation Hub"},"settings":{"target":"Config/hub-settings.json"}},"pages":[{"name":"Home","target":"SitePages/Home.html"},{"name":"MyObligations","target":"SitePages/MyObligations.html"},{"name":"Contract360","target":"SitePages/Contract360.html"},{"name":"ReviewQueue","target":"SitePages/ReviewQueue.html"},{"name":"Leadership","target":"SitePages/Leadership.html"},{"name":"Settings","target":"SitePages/Settings.html"},{"name":"HowItWorks","target":"SitePages/HowItWorks.html"}],"site":{"navigation":{"nodes":[{"title":"Overview","target":"page:Home"},{"title":"My obligations","target":"page:MyObligations"},{"title":"Contracts","target":"list:contracts"},{"title":"Obligations","target":"list:obligations"},{"title":"Review","target":"page:ReviewQueue"},{"title":"Leadership","target":"page:Leadership"},{"title":"How it works","target":"page:HowItWorks"},{"title":"Settings","target":"page:Settings"}]}},"removal":{"lists":["contracts","obligations","owners","types","exclusions","runlog","evidence"],"pages":["SitePages/Home.html","SitePages/MyObligations.html","SitePages/Contract360.html","SitePages/ReviewQueue.html","SitePages/Leadership.html","SitePages/Settings.html","SitePages/HowItWorks.html"],"skills":["capture-obligations","assign-obligation-owners","sweep-obligations","obligation-owner-digest","obligation-leadership-digest","mark-obligation-fulfilled","exclude-obligation","obligation-hub-guide","clear-obligation-sample-data","setup-obligation-hub"],"files":["Config/hub-settings.json","SHAREPOINT.md"],"resetWelcomePageFrom":"SitePages/Home.html","resetWelcomePageTo":"SitePages/Home.aspx","navigation":"Only the hub navigation links (same title and address as site.navigation.nodes) are removed.","notRemoved":["AI workflows (delete them in the site's AI workflows panel; they fail once the lists are gone)","The AgentAssets library and its Skills and Config folders","Other skills and files in AgentAssets","The site theme, logo and header layout (change them in Settings > Change the look)","Anything you added or changed by hand outside the hub lists"]}}/*REMOVE-SPEC-END*/;

  const tag = "%c[Obligation Hub]";
  const css = "color:#0f6cbd;font-weight:700";
  const log = (m) => console.log(tag + " " + m, css);
  const warn = (m) => console.warn("[Obligation Hub] " + m);
  const onSite = typeof location !== "undefined" && /^https:/.test(location.origin || "");
  const pc = (typeof window !== "undefined" && window._spPageContextInfo) || null;
  const guessPath = (pc && pc.webServerRelativeUrl) || (onSite ? ((location.pathname.match(/^\/(sites|teams)\/[^/]+/i) || [""])[0]) : "");
  let base = (onSite ? location.origin : "") + (guessPath === "/" ? "" : guessPath);
  let digest = "";

  async function call(method, path, body, opt) {
    opt = opt || {};
    const headers = { Accept: opt.text ? "*/*" : "application/json;odata=nometadata" };
    if (method !== "GET") headers["X-RequestDigest"] = digest;
    if (body !== undefined) headers["Content-Type"] = "application/json;odata=verbose";
    if (method === "MERGE" || method === "DELETE") { headers["X-HTTP-Method"] = method; headers["IF-MATCH"] = "*"; }
    const res = await fetch(base + path, {
      method: method === "GET" ? "GET" : "POST", headers, credentials: "same-origin",
      body: body === undefined ? undefined : JSON.stringify(body)
    });
    const text = await res.text();
    if (opt.allowMissing && (res.status === 404 || /FileNotFoundException|does not exist/i.test(text))) return null;
    if (!res.ok) throw new Error(method + " " + path.split("?")[0] + " failed (" + res.status + "): " + text.slice(0, 300));
    if (opt.text) return text;
    return text ? JSON.parse(text) : {};
  }
  const q = (s) => "'" + String(s).replace(/'/g, "''") + "'";
  const norm = (u) => { let s = String(u || "").replace(/^https?:\/\/[^/]+/i, ""); try { s = decodeURIComponent(s); } catch (e) { /* keep */ } return s.replace(/\/+$/, "").toLowerCase(); };
  const fileApi = (p) => "/_api/web/GetFileByServerRelativePath(decodedurl=" + q(p) + ")";
  const folderApi = (p) => "/_api/web/GetFolderByServerRelativePath(decodedurl=" + q(p) + ")";

  try {
    if (!onSite) throw new Error("Run this from the browser console on a page of your SharePoint site.");
    const ctxRes = await fetch(base + "/_api/contextinfo", { method: "POST", credentials: "same-origin", headers: { Accept: "application/json;odata=nometadata" } });
    if (!ctxRes.ok) throw new Error("Couldn't get a request digest from " + base + " (" + ctxRes.status + ").");
    const ctx = JSON.parse(await ctxRes.text());
    digest = ctx.FormDigestValue; base = (ctx.WebFullUrl || base).replace(/\/+$/, "");
    const web = await call("GET", "/_api/web?$select=Title,ServerRelativeUrl");
    const webRel = web.ServerRelativeUrl === "/" ? "" : web.ServerRelativeUrl;
    const perms = await call("GET", "/_api/web/effectiveBasePermissions");
    if ((Number(perms.Low) & 0x800) === 0) throw new Error("You don't have permission to delete lists on " + base + ". Ask a site owner to run this.");

    let SPEC = SPEC_EMBEDDED;
    try {
      const res = await fetch(OPTIONS.assetsBaseUrl.replace(/\/+$/, "") + "/solutions/obligation-hub-for-sharepoint/deploy/spec.json", { credentials: "omit", cache: "no-store" });
      if (res.ok) {
        const s = JSON.parse(await res.text());
        if (s && s.solution && s.solution.name === "obligation-hub-for-sharepoint" && Array.isArray(s.lists)) SPEC = s;
      }
    } catch (e) { /* use the embedded copy */ }
    if (!SPEC) throw new Error("No spec available: the kit's spec.json couldn't be fetched and none is embedded in this copy.");
    const R = SPEC.removal;
    const byKey = {};
    SPEC.lists.forEach((L) => { byKey[L.key] = L; });

    // ---- Find what's here -----------------------------------------------------------------------
    const lists = [];
    for (const key of R.lists) {
      const L = byKey[key];
      const found = await call("GET", "/_api/web/GetList(@u)?@u=" + encodeURIComponent(q(webRel + "/" + L.url)) + "&$select=Id,Title,ItemCount,Description", undefined, { allowMissing: true });
      if (found) lists.push(Object.assign(found, { url: webRel + "/" + L.url, sameDescription: (found.Description || "") === L.description }));
    }
    const pages = [];
    for (const p of R.pages) {
      const path = webRel + "/" + p;
      const f = await call("GET", fileApi(path) + "?$select=Name,Exists", undefined, { allowMissing: true });
      if (f && f.Exists !== false && f.Name) pages.push(path);
    }
    const aaList = byKey[SPEC.agentAssets.list];
    const aa = await call("GET", "/_api/web/GetList(@u)?@u=" + encodeURIComponent(q(webRel + "/" + aaList.url)) + "&$select=Id&$expand=RootFolder", undefined, { allowMissing: true });
    const skills = [], files = [], kept = [];
    if (aa) {
      const root = (aa.RootFolder && aa.RootFolder.ServerRelativeUrl) || (webRel + "/" + aaList.url);
      for (const name of R.skills) {
        const path = root + "/" + SPEC.agentAssets.skillsRoot + "/" + name;
        const f = await call("GET", folderApi(path) + "?$select=Exists,Name", undefined, { allowMissing: true });
        if (f && f.Exists !== false && f.Name) skills.push(path);
      }
      const settingsPath = root + "/" + SPEC.agentAssets.settings.target;
      const s = await call("GET", fileApi(settingsPath) + "?$select=Name,Exists", undefined, { allowMissing: true });
      if (s && s.Exists !== false && s.Name) files.push(settingsPath);
      const ctxPath = root + "/" + SPEC.agentAssets.siteContext.target;
      const body = await call("GET", fileApi(ctxPath) + "/$value", undefined, { allowMissing: true, text: true });
      if (body != null) {
        if (body.indexOf(SPEC.agentAssets.siteContext.marker) >= 0) files.push(ctxPath);
        else kept.push(ctxPath + " (it doesn't mention \"" + SPEC.agentAssets.siteContext.marker + "\", so it isn't the hub's)");
      }
    }
    const nav = [];
    if (SPEC.site && SPEC.site.navigation) {
      const hub = SPEC.site.navigation.nodes.map((n) => {
        const [kind, ref] = n.target.split(":");
        const pg = kind === "page" ? SPEC.pages.find((x) => x.name === ref) : null;
        return { title: n.title.toLowerCase(), url: norm(webRel + "/" + (pg ? pg.target : byKey[ref].url)) };
      });
      for (const coll of ["TopNavigationBar", "QuickLaunch"]) {
        const r = await call("GET", "/_api/web/navigation/" + coll + "?$select=Id,Title,Url", undefined, { allowMissing: true });
        for (const n of (r && r.value) || []) {
          if (hub.some((h) => h.title === String(n.Title).toLowerCase() && h.url === norm(n.Url))) nav.push({ coll, id: n.Id, title: n.Title });
        }
      }
    }
    const welcome = (await call("GET", "/_api/web/rootfolder?$select=WelcomePage")).WelcomePage || "";
    const resetHome = welcome.toLowerCase() === R.resetWelcomePageFrom.toLowerCase();

    if (!lists.length && !pages.length && !skills.length && !files.length && !nav.length) {
      log("No Obligation Hub lists, pages or files found on " + base + ". Nothing to remove.");
      return { removed: [], kept };
    }
    const lines = []
      .concat(lists.map((l) => "- " + l.Title + " (" + l.ItemCount + " items)" + (l.sameDescription ? "" : "  <- description differs from the hub's; check it's yours")))
      .concat(pages.map((p) => "- " + p.slice(webRel.length + 1)))
      .concat(skills.map((p) => "- " + p.slice(webRel.length + 1) + " (skill folder)"))
      .concat(files.map((p) => "- " + p.slice(webRel.length + 1)))
      .concat(nav.length ? ["- " + nav.length + " hub links in the site navigation (" + nav.map((n) => n.title).join(", ") + "); links are deleted, not recycled"] : []);
    const ok = (typeof confirm === "function") ? confirm("Move these to the recycle bin on " + web.Title + "?\n\n" + lines.join("\n") +
      (resetHome ? "\n\nThe home page goes back to " + R.resetWelcomePageTo + "." : "") +
      "\n\nYou can restore them from Site contents > Recycle bin for 93 days.") : true;
    if (!ok) { log("Cancelled. Nothing was changed."); return { cancelled: true }; }

    // ---- Remove (home page first, so the site never points at a recycled page) -------------------------
    const removed = [], failed = [];
    const attempt = async (label, fn) => { try { await fn(); removed.push(label); log("Recycled " + label); } catch (e) { failed.push(label + ": " + e.message.slice(0, 200)); warn("Couldn't recycle " + label + ": " + e.message.slice(0, 200)); } };
    if (resetHome) {
      try {
        await call("MERGE", "/_api/web/rootfolder", { __metadata: { type: "SP.Folder" }, WelcomePage: R.resetWelcomePageTo });
        log("Home page set back to " + R.resetWelcomePageTo);
      } catch (e) { failed.push("home page reset: " + e.message.slice(0, 200)); }
    }
    for (const n of nav) {
      try { await call("DELETE", "/_api/web/navigation/" + n.coll + "/GetById(" + n.id + ")"); removed.push("navigation link " + n.title); }
      catch (e) { failed.push("navigation link " + n.title + ": " + e.message.slice(0, 200)); }
    }
    if (nav.length) log("Removed " + nav.length + " hub links from the site navigation");
    for (const l of lists) await attempt(l.Title, () => call("POST", "/_api/web/lists(guid'" + l.Id + "')/recycle"));
    for (const p of pages) await attempt(p.slice(webRel.length + 1), () => call("POST", fileApi(p) + "/recycle"));
    for (const p of skills) await attempt(p.slice(webRel.length + 1), () => call("POST", folderApi(p) + "/recycle"));
    for (const p of files) await attempt(p.slice(webRel.length + 1), () => call("POST", fileApi(p) + "/recycle"));

    log("Done. Restore anything from Site contents > Recycle bin.");
    log("Not removed by this script:");
    R.notRemoved.concat(kept).forEach((m) => console.log("  - " + m));
    if (failed.length) { warn("These weren't removed:"); failed.forEach((m) => warn("- " + m)); }
    return { removed, failed, kept, homeReset: resetHome };
  } catch (e) {
    console.error("[Obligation Hub] Stopped: " + e.message);
    return { error: e.message };
  }
})();
