#!/usr/bin/env node
/*
 * Keeps the copies embedded in the browser scripts identical to deploy/spec.json and formats/*.json.
 *   node deploy/sync-embedded-spec.js          rewrite the embedded copies
 *   node deploy/sync-embedded-spec.js --check  exit 1 if a copy is out of date (for CI or a pre-commit check)
 * Run it from anywhere; paths are relative to this file. Edit spec.json first, never the embedded copy.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const DEPLOY = __dirname;
const KIT = path.resolve(DEPLOY, "..");
const REPO = path.resolve(KIT, "..", "..");
const check = process.argv.includes("--check");

const spec = JSON.parse(fs.readFileSync(path.join(DEPLOY, "spec.json"), "utf8"));
const formats = {};
for (const f of spec.formats) formats[f.field] = JSON.parse(fs.readFileSync(path.join(REPO, f.file), "utf8"));

const removeSpec = {
  solution: spec.solution,
  lists: spec.lists.map((L) => ({ key: L.key, title: L.title, url: L.url, description: L.description, ifExists: L.ifExists })),
  agentAssets: {
    list: spec.agentAssets.list, skillsRoot: spec.agentAssets.skillsRoot,
    siteContext: { target: spec.agentAssets.siteContext.target, marker: spec.agentAssets.siteContext.marker },
    settings: { target: spec.agentAssets.settings.target }
  },
  pages: spec.pages.map((p) => ({ name: p.name, target: p.target })),
  site: spec.site ? { navigation: { nodes: spec.site.navigation.nodes } } : null,
  removal: spec.removal
};

function embed(file, pairs) {
  const p = path.join(DEPLOY, file);
  let src = fs.readFileSync(p, "utf8");
  for (const [name, value] of pairs) {
    const re = new RegExp("(/\\*" + name + "-BEGIN\\*/)[\\s\\S]*?(/\\*" + name + "-END\\*/)");
    if (!re.test(src)) throw new Error(file + ": markers " + name + "-BEGIN/END not found");
    src = src.replace(re, (m, a, b) => a + JSON.stringify(value) + b);
  }
  const before = fs.readFileSync(p, "utf8");
  if (before === src) return false;
  if (check) { console.error(file + " is out of date; run node deploy/sync-embedded-spec.js"); return true; }
  fs.writeFileSync(p, src);
  console.log("updated " + file);
  return true;
}

const stale = [
  embed("deploy-obligation-hub.js", [["SPEC", spec], ["FORMATS", formats]]),
  embed("remove-obligation-hub.js", [["REMOVE-SPEC", removeSpec]])
].some(Boolean);
if (check) process.exit(stale ? 1 : 0);
if (!stale) console.log("embedded copies already match spec.json");
