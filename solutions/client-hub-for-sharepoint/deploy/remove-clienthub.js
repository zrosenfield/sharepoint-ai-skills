/*!
 * Client Hub for SharePoint: remove script (v1.0). Unofficial and unsupported.
 * Moves the Client Hub lists (Clients, Projects, Client Activity) and SitePages/Client360.html to the
 * site recycle bin, where you can restore them for 93 days. Run it the same way as the deploy script.
 */
(async function clientHubRemove() {
  "use strict";
  const pc = (typeof window !== "undefined" && window._spPageContextInfo) || null;
  const guessPath = (pc && pc.webServerRelativeUrl) || ((location.pathname.match(/^\/(sites|teams)\/[^/]+/i) || [""])[0]);
  let base = location.origin + (guessPath === "/" ? "" : guessPath);
  let digest = "";
  async function call(method, path, opt) {
    const headers = { Accept: "application/json;odata=nometadata" };
    if (method !== "GET") headers["X-RequestDigest"] = digest;
    const res = await fetch(base + path, { method: method === "GET" ? "GET" : "POST", headers, credentials: "same-origin" });
    const text = await res.text();
    if (opt && opt.allowMissing && (res.status === 404 || /FileNotFoundException|does not exist/i.test(text))) return null;
    if (!res.ok) throw new Error(method + " " + path.split("?")[0] + " failed (" + res.status + "): " + text.slice(0, 300));
    return text ? JSON.parse(text) : {};
  }
  const q = (s) => "'" + String(s).replace(/'/g, "''") + "'";
  const ctx = await call("POST", "/_api/contextinfo");
  digest = ctx.FormDigestValue; base = ctx.WebFullUrl || base;
  const web = await call("GET", "/_api/web?$select=Title,ServerRelativeUrl");
  const webRel = web.ServerRelativeUrl === "/" ? "" : web.ServerRelativeUrl;
  const targets = ["ClientActivity", "Projects", "Clients"];
  const found = [];
  for (const t of targets) {
    const l = await call("GET", "/_api/web/GetList(@u)?@u=" + encodeURIComponent(q(webRel + "/Lists/" + t)) + "&$select=Id,Title,ItemCount", { allowMissing: true });
    if (l) found.push(l);
  }
  if (!found.length) { console.log("[Client Hub] No Client Hub lists found on " + base + ". Nothing to remove."); return; }
  const ok = confirm("Move these to the recycle bin on " + web.Title + "?\n\n" + found.map((l) => "- " + l.Title + " (" + l.ItemCount + " items)").join("\n") + "\n- SitePages/Client360.html (if present)");
  if (!ok) { console.log("[Client Hub] Cancelled."); return; }
  for (const l of found) { await call("POST", "/_api/web/lists(guid'" + l.Id + "')/recycle"); console.log("[Client Hub] Recycled " + l.Title); }
  const page = webRel + "/SitePages/Client360.html";
  const welcome = await call("GET", "/_api/web/rootfolder?$select=WelcomePage");
  const f = await call("GET", "/_api/web/GetFileByServerRelativeUrl(" + q(page) + ")?$select=Name", { allowMissing: true });
  if (f) {
    if (/client360\.html$/i.test(welcome.WelcomePage || "")) {
      const res = await fetch(base + "/_api/web/rootfolder", { method: "POST", credentials: "same-origin",
        headers: { Accept: "application/json;odata=nometadata", "Content-Type": "application/json;odata=verbose", "X-RequestDigest": digest, "X-HTTP-Method": "MERGE", "IF-MATCH": "*" },
        body: JSON.stringify({ __metadata: { type: "SP.Folder" }, WelcomePage: "SitePages/Home.aspx" }) });
      if (res.ok) console.log("[Client Hub] Home page set back to SitePages/Home.aspx");
    }
    await call("POST", "/_api/web/GetFileByServerRelativeUrl(" + q(page) + ")/recycle");
    console.log("[Client Hub] Recycled Client360.html");
  }
  console.log("[Client Hub] Done. Restore anything from Site contents > Recycle bin.");
})().catch((e) => console.error("[Client Hub] Stopped: " + e.message));
