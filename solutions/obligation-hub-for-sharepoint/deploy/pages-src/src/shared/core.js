/* Obligation Hub - shared data layer and UI helpers (plain JS, no network). */
(function (window, document) {
  'use strict';
  var Hub = window.Hub = {};
  var DAY = 86400000;
  var LIVE_WAIT_MS = 800;     // how long to wait for the host to inject live results
  var LATE_WATCH_MS = 8000;   // keep watching for a late injection, then stop

  /* ---------------- small utilities ---------------- */
  var ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  function esc(v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) { return ESC[c]; }); }
  function clean(v) {
    if (v == null) return '';
    if (typeof v === 'object') {
      if (Array.isArray(v)) return v.map(clean).filter(Boolean).join(', ');
      return clean(v.title || v.Title || v.displayName || v.DisplayName || v.name || v.Name ||
        v.LookupValue || v.lookupValue || v.Label || v.label || v.text || v.value || v.Value || '');
    }
    var s = String(v).replace(/\s+/g, ' ').trim();
    return /^(null|undefined|none;#)$/i.test(s) ? '' : s;
  }
  function lower(v) { return clean(v).toLowerCase(); }
  function readJSONScript(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }
  function byId(id) { return document.getElementById(id); }
  function setHTML(id, html) { var el = typeof id === 'string' ? byId(id) : id; if (el) el.innerHTML = html; return el; }
  function closest(el, sel) {
    while (el && el.nodeType === 1) {
      if (el.matches ? el.matches(sel) : false) return el;
      el = el.parentNode;
    }
    return null;
  }
  function uniq(list) { var seen = {}, out = []; list.forEach(function (x) { var k = String(x).toLowerCase(); if (x && !seen[k]) { seen[k] = 1; out.push(x); } }); return out; }
  function plural(n, one, many) { return n + ' ' + (n === 1 ? one : (many || one + 's')); }
  function truncate(s, n) { s = clean(s); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '\u2026' : s; }
  Hub.esc = esc; Hub.clean = clean; Hub.byId = byId; Hub.setHTML = setHTML; Hub.closest = closest;
  Hub.uniq = uniq; Hub.plural = plural; Hub.truncate = truncate; Hub.readJSONScript = readJSONScript;

  /* ---------------- configuration & URLs ---------------- */
  var cfg = readJSONScript('hub-config') || {};
  cfg.lists = cfg.lists || {};
  function unreplaced(v) { return typeof v !== 'string' || v.indexOf('{{') !== -1; }
  Hub.cfg = cfg;
  Hub.preview = unreplaced(cfg.siteUrl);
  function listInfo(key) { return cfg.lists[key] || {}; }
  function listRoot(key) { return (cfg.origin || '') + (listInfo(key).url || ''); }
  function viewBase(key) { return listRoot(key) + (listInfo(key).library ? '/Forms/AllItems.aspx' : '/AllItems.aspx'); }
  Hub.url = {
    root: listRoot,
    view: function (key, filters) {
      var q = [];
      (filters || []).forEach(function (f, i) {
        var n = i + 1;
        if (Array.isArray(f[1])) q.push('FilterFields' + n + '=' + encodeURIComponent(f[0]) + '&FilterValues' + n + '=' + encodeURIComponent(f[1].join(';#')));
        else q.push('FilterField' + n + '=' + encodeURIComponent(f[0]) + '&FilterValue' + n + '=' + encodeURIComponent(f[1]));
      });
      return viewBase(key) + (q.length ? '?' + q.join('&') : '');
    },
    disp: function (key, id) { return id ? listRoot(key) + (listInfo(key).library ? '/Forms/DispForm.aspx' : '/DispForm.aspx') + '?ID=' + encodeURIComponent(id) : viewBase(key); },
    edit: function (key, id, back) {
      if (!id) return viewBase(key);
      var u = listRoot(key) + (listInfo(key).library ? '/Forms/EditForm.aspx' : '/EditForm.aspx') + '?ID=' + encodeURIComponent(id);
      if (back && !Hub.preview) u += '&Source=' + encodeURIComponent(Hub.url.page(back));
      return u;
    },
    file: function (key, name) { return listRoot(key) + '/' + encodeURIComponent(name).replace(/%2F/g, '/') + '?web=1'; },
    page: function (file, hash) {
      var base = Hub.preview || unreplaced(cfg.pagesUrl) ? file : cfg.pagesUrl + '/' + file;
      return base + (hash ? '#' + hash : '');
    }
  };

  /* ---------------- dates ---------------- */
  function startOfDay(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function validYMD(y, m, d) { return y > 1900 && y < 2200 && m >= 1 && m <= 12 && d >= 1 && d <= 31; }
  function parseDate(v, keepTime) {
    if (v == null || v === '') return null;
    if (v instanceof Date) return isNaN(v.getTime()) ? null : (keepTime ? v : startOfDay(v));
    if (typeof v === 'number') { var dn = new Date(v); return isNaN(dn.getTime()) ? null : (keepTime ? dn : startOfDay(dn)); }
    var s = clean(v), m, d;
    if (!s) return null;
    if ((m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/))) {
      return validYMD(+m[1], +m[2], +m[3]) ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
    }
    if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{1,2}):(\d{2})(?::(\d{2}))?(?:\.\d+)?\s*(Z|[+-]\d{2}:?\d{2})?$/i))) {
      if (!validYMD(+m[1], +m[2], +m[3])) return null;
      if (m[7]) d = new Date(s.replace(' ', 'T').replace(/([+-]\d{2})(\d{2})$/, '$1:$2'));
      else d = new Date(+m[1], +m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0));
      if (isNaN(d.getTime())) return null;
      return keepTime ? d : startOfDay(d);
    }
    if ((m = s.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{2,4})(?:[ ,T]+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp]\.?[Mm]\.?)?)?$/))) {
      var a = +m[1], b = +m[2], y = +m[3], mo = a, da = b, h = m[4] ? +m[4] : 0;
      if (y < 100) y += 2000;
      if (a > 12 && b <= 12) { mo = b; da = a; }
      if (!validYMD(y, mo, da)) return null;
      if (m[7]) { var pm = /p/i.test(m[7]); if (pm && h < 12) h += 12; if (!pm && h === 12) h = 0; }
      d = new Date(y, mo - 1, da, h, m[5] ? +m[5] : 0, m[6] ? +m[6] : 0);
      return keepTime ? d : startOfDay(d);
    }
    if ((m = s.match(/\/Date\((-?\d+)/))) { d = new Date(+m[1]); return keepTime ? d : startOfDay(d); }
    var t = Date.parse(s);
    if (!isNaN(t)) { d = new Date(t); return keepTime ? d : startOfDay(d); }
    return null;
  }
  /* "Today" is the viewer's date. window.__HUB_TODAY__ ('YYYY-MM-DD') is a test hook only; nothing in the pages sets it. */
  function today() {
    var o = window.__HUB_TODAY__ ? parseDate(window.__HUB_TODAY__) : null;
    return o || startOfDay(new Date());
  }
  function now() {
    var t = window.__HUB_TODAY__ ? parseDate(window.__HUB_TODAY__) : null;
    return t ? new Date(t.getTime() + 12 * 3600000) : new Date();
  }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function daysBetween(a, b) { return Math.round((startOfDay(b) - startOfDay(a)) / DAY); }
  function iso(d) { if (!d) return ''; var m = d.getMonth() + 1, x = d.getDate(); return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (x < 10 ? '0' : '') + x; }
  Hub.date = { parse: parseDate, today: today, now: now, addDays: addDays, diff: daysBetween, iso: iso, startOfDay: startOfDay };

  var fmtCache = {};
  function fmt(d, opts) {
    if (!d) return '';
    var k = JSON.stringify(opts);
    if (!fmtCache[k]) { try { fmtCache[k] = new Intl.DateTimeFormat(undefined, opts); } catch (e) { fmtCache[k] = { format: function (x) { return x.toDateString(); } }; } }
    return fmtCache[k].format(d);
  }
  Hub.fmt = {
    date: function (d) { return fmt(d, { day: 'numeric', month: 'short', year: 'numeric' }); },
    short: function (d) { return d && d.getFullYear() === today().getFullYear() ? fmt(d, { day: 'numeric', month: 'short' }) : fmt(d, { day: 'numeric', month: 'short', year: 'numeric' }); },
    long: function (d) { return fmt(d, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); },
    month: function (d, withYear) { return fmt(d, withYear ? { month: 'short', year: 'numeric' } : { month: 'short' }); },
    dateTime: function (d) { return fmt(d, { day: 'numeric', month: 'short', year: 'numeric', hour: 'numeric', minute: '2-digit' }); },
    rel: function (d) {
      if (!d) return '';
      var n = daysBetween(today(), d);
      if (n === 0) return 'today';
      if (n === 1) return 'tomorrow';
      if (n === -1) return 'yesterday';
      return n > 0 ? 'in ' + n + ' days' : Math.abs(n) + ' days ago';
    },
    due: function (d) {
      if (!d) return '';
      var n = daysBetween(today(), d);
      if (n === 0) return 'due today';
      if (n === 1) return 'due tomorrow';
      if (n < 0) return plural(-n, 'day') + ' overdue';
      return 'in ' + n + ' days';
    },
    ago: function (dt) {
      if (!dt) return 'never';
      var ms = now() - dt, min = Math.round(ms / 60000);
      if (ms < 0) return 'just now';
      if (min < 2) return 'just now';
      if (min < 60) return min + ' minutes ago';
      var h = Math.round(min / 60);
      if (h < 24) return plural(h, 'hour') + ' ago';
      var dd = daysBetween(dt, now());
      if (dd <= 1) return 'yesterday';
      return dd + ' days ago';
    },
    money: function (n, raw) {
      if (n == null) return raw ? clean(raw) : '';
      if (raw && /[^\d.,\s-]/.test(clean(raw))) return clean(raw);
      try { return new Intl.NumberFormat(undefined, { style: 'currency', currency: cfg.currency || 'USD', maximumFractionDigits: 0 }).format(n); }
      catch (e) { return String(n); }
    },
    iso: iso
  };

  /* ---------------- value parsers ---------------- */
  function people(v) {
    if (v == null) return [];
    if (Array.isArray(v)) { var all = []; v.forEach(function (x) { all = all.concat(people(x)); }); return uniq(all); }
    if (typeof v === 'object') {
      var n = v.title || v.Title || v.displayName || v.DisplayName || v.name || v.Name || v.LookupValue || v.lookupValue || v.text || v.email || v.Email || v.EMail || v.mail || v.userPrincipalName || '';
      return n ? [String(n).trim()] : [];
    }
    var s = String(v).trim();
    if (!s || /^(null|undefined|\[\]|\{\})$/i.test(s)) return [];
    if (/^[\[{]/.test(s)) { try { return people(JSON.parse(s)); } catch (e) { /* fall through */ } }
    if (s.indexOf(';#') !== -1) {
      return uniq(s.split(';#').map(function (p) { return p.trim(); }).filter(function (p) { return p && !/^\d+$/.test(p); }).map(function (p) { return people(p)[0] || p; }));
    }
    if (s.indexOf('|') !== -1 && /@/.test(s)) s = s.split('|').pop();
    var m = s.match(/^(.*?)\s*<([^>]+)>$/);
    if (m) return [clean(m[1]) || clean(m[2])];
    if (s.indexOf(';') !== -1) return uniq(s.split(';').map(clean).filter(Boolean));
    return [clean(s)];
  }
  function num(v) {
    if (v == null || v === '') return null;
    if (typeof v === 'number') return isFinite(v) ? v : null;
    var s = clean(v).replace(/[^\d.,\-]/g, '');
    if (!s) return null;
    if (/^-?\d{1,3}(,\d{3})+(\.\d+)?$/.test(s) || /^-?\d+(\.\d+)?$/.test(s)) s = s.replace(/,/g, '');
    else if (/^-?\d{1,3}(\.\d{3})+(,\d+)?$/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
    else s = s.replace(/,/g, '');
    var n = parseFloat(s);
    return isFinite(n) ? n : null;
  }
  function yes(v) { return /^(yes|true|1|y|on)$/i.test(clean(v)); }
  Hub.people = people; Hub.num = num; Hub.yes = yes;

  /* ---------------- list schema (internal names + accepted aliases) ---------------- */
  var LISTS = {
    OBLIGATIONS: { label: 'Obligations', fields: {
      ID: ['Id', 'ItemId', 'Item ID'], Title: ['Obligation'], ContractName: ['Contract'], ContractLink: ['Contract link'],
      Counterparty: [], ObligationText: ['What must happen'], ClauseRef: ['Clause'], SourceClause: ['Source clause'],
      Party: ['Who owes it'], Category: [], TriggerType: ['Trigger'], Recurrence: [], DueDate: ['Due date', 'Due'],
      TriggerEvent: ['Trigger event'], Owner: [], EscalationOwner: ['Escalation owner'], BusinessUnit: ['Business unit'],
      Status: [], Timing: [], ReviewState: ['Review', 'Review state'], Confidence: [], Risk: [], FulfilledOn: ['Fulfilled on'],
      Evidence: [], LastReminded: ['Last reminded'], CaptureKey: ['Capture key'], Notes: [], IsSample: ['Sample data'] } },
    CONTRACTS: { label: 'Contracts', fields: {
      ID: ['Id', 'ItemId', 'Item ID'], FileLeafRef: ['Name', 'File name', 'FileName', 'LinkFilename', 'LinkFilenameNoMenu', 'File'],
      Title: ['Contract title'], Counterparty: [], ContractType: ['Contract type'], EffectiveDate: ['Effective date'],
      ExpirationDate: ['Expiration date'], AutoRenews: ['Auto-renews', 'Auto renews'], NoticePeriodDays: ['Notice period (days)', 'Notice period'],
      GoverningLaw: ['Governing law'], ContractValue: ['Contract value', 'Value'], ContractSummary: ['Summary'],
      ContractOwner: ['Contract owner'], BusinessUnit: ['Business unit'], Amends: [], IsSample: ['Sample data'] } },
    RUNLOG: { label: 'Run Log', fields: {
      ID: ['Id', 'ItemId', 'Item ID'], Title: ['Run'], Workflow: [], Outcome: [], ContractName: ['Contract'],
      ContractVersion: ['Contract version'], ItemsCreated: ['Created'], ItemsUpdated: ['Updated'], ItemsHeld: ['Held for review', 'Held'],
      Details: [], RunAt: ['Run at'] } },
    OWNERS: { label: 'Obligation Owners', fields: {
      ID: ['Id', 'ItemId', 'Item ID'], Title: ['Rule'], Category: [], BusinessUnit: ['Business unit'], Counterparty: ['Counterparty (optional)'],
      Owner: [], EscalationOwner: ['Escalation owner'], Notify: ['Notify by'] } }
  };
  Hub.LISTS = LISTS;
  function normKey(s) { return String(s == null ? '' : s).toLowerCase().replace(/_x0020_/g, '').replace(/^odata_+/, '').replace(/[^a-z0-9]/g, ''); }

  function headerMap(key, headers) {
    var fields = (LISTS[key] || {}).fields || {}, map = new Array(headers.length), taken = {};
    var normHeaders = headers.map(normKey);
    Object.keys(fields).forEach(function (f) {
      var i = normHeaders.indexOf(normKey(f));
      if (i !== -1 && map[i] === undefined) { map[i] = f; taken[f] = 1; }
    });
    Object.keys(fields).forEach(function (f) {
      if (taken[f]) return;
      fields[f].some(function (alias) {
        var i = normHeaders.indexOf(normKey(alias));
        if (i !== -1 && map[i] === undefined) { map[i] = f; taken[f] = 1; return true; }
        return false;
      });
    });
    return headers.map(function (h, i) { return map[i] || String(h); });
  }

  function rowsFrom(key, content) {
    if (typeof content === 'string') content = JSON.parse(content);
    if (Array.isArray(content)) content = { rows: content };
    if (!content || typeof content !== 'object') throw new Error('Result has no rows');
    var rows = content.rows || content.value || content.items;
    if (!Array.isArray(rows)) throw new Error('Result rows are not a list');
    var headers = content.headers || content.columns || content.fields || [];
    headers = headers.map(function (h) { return typeof h === 'object' && h ? (h.name || h.internalName || h.title || h.displayName || '') : h; });
    var mapped = headerMap(key, headers);
    return rows.map(function (r) {
      var o = {};
      if (Array.isArray(r)) { r.forEach(function (v, i) { if (i < mapped.length) o[mapped[i]] = v; }); }
      else if (r && typeof r === 'object') {
        var ks = Object.keys(r), km = headerMap(key, ks);
        ks.forEach(function (k, i) { o[km[i]] = r[k]; });
      }
      return o;
    });
  }

  function normLiveKey(k) {
    var s = String(k || '');
    try { s = decodeURIComponent(s); } catch (e) { /* keep raw */ }
    return s.toLowerCase().replace(/[{}]/g, '').replace(/\s+/g, '').replace(/\/+$/, '');
  }
  function findLive(key) {
    var R = window.__LD_RESULTS__;
    if (!R || typeof R !== 'object') return undefined;
    var info = listInfo(key);
    var want = normLiveKey('list:' + (cfg.siteUrl || '') + '/' + (info.id || ''));
    var ks = Object.keys(R), i;
    for (i = 0; i < ks.length; i++) if (normLiveKey(ks[i]) === want) return R[ks[i]];
    var id = normLiveKey(info.id || '');
    if (id && id.length > 8) for (i = 0; i < ks.length; i++) { var nk = normLiveKey(ks[i]); if (nk.slice(-id.length) === id) return R[ks[i]]; }
    return undefined;
  }
  function parseLive(key, raw) {
    if (typeof raw === 'string') raw = JSON.parse(raw);
    if (!raw || typeof raw !== 'object') throw new Error('Empty result');
    var format = String(raw.format || '').toLowerCase();
    if (format !== 'rows') throw new Error(raw.error ? String(raw.error) : 'Unsupported result format "' + (raw.format || 'none') + '"');
    return rowsFrom(key, raw.content);
  }
  function loadList(key) {
    var res = { key: key, label: (LISTS[key] || {}).label || key, live: false, source: 'snapshot', rows: [], error: null };
    var raw = findLive(key);
    if (raw !== undefined && raw !== null) {
      try { res.rows = parseLive(key, raw); res.live = true; res.source = 'live'; return res; }
      catch (e) { res.error = (e && e.message) || 'Unreadable result'; }
    }
    var snap = readJSONScript('snapshot-' + key.toLowerCase());
    if (snap) { try { res.rows = rowsFrom(key, snap); } catch (e2) { res.rows = []; res.error = res.error || 'Sample snapshot unreadable'; } }
    else { res.source = 'none'; }
    return res;
  }
  Hub.loadList = loadList; Hub.rowsFrom = rowsFrom;

  /* ---------------- models ---------------- */
  var CLOSED = /^(fulfilled|waived|not applicable|n\/a)$/i;
  function timingFor(closed, due) {
    if (closed) return 'Closed';
    if (!due) return 'No date';
    var n = daysBetween(today(), due);
    if (n < 0) return 'Overdue';
    if (n <= 14) return 'Due soon';
    return 'Upcoming';
  }
  function normParty(v) {
    var s = lower(v);
    if (!s) return 'Us';
    if (/^(us|we|our|ours|northwind)$/.test(s)) return 'Us';
    if (/both|mutual|either/.test(s)) return 'Both';
    if (/counter|them|supplier|customer|other/.test(s)) return 'Counterparty';
    return clean(v);
  }
  function contractKey(name) {
    var s = clean(name);
    if (!s) return '';
    try { s = decodeURIComponent(s); } catch (e) { /* keep */ }
    s = s.split(/[\\\/]/).pop();
    return s.toLowerCase().replace(/\.(docx?|pdf|rtf|txt|odt)$/i, '').replace(/[\s_]+/g, ' ').trim();
  }
  Hub.contractKey = contractKey;
  Hub.model = {
    obligation: function (r) {
      var status = clean(r.Status) || 'Not started';
      var closed = CLOSED.test(status);
      var due = parseDate(r.DueDate);
      var owners = people(r.Owner);
      return {
        id: clean(r.ID).replace(/\.0+$/, ''), title: clean(r.Title) || 'Untitled obligation', contract: clean(r.ContractName),
        counterparty: clean(r.Counterparty), text: clean(r.ObligationText), clause: clean(r.ClauseRef), source: clean(r.SourceClause),
        party: normParty(r.Party), category: clean(r.Category) || 'Other', triggerType: clean(r.TriggerType),
        recurrence: clean(r.Recurrence), due: due, triggerEvent: clean(r.TriggerEvent), owners: owners, owner: owners.join(', '),
        escalation: people(r.EscalationOwner).join(', '), bu: clean(r.BusinessUnit), status: status, closed: closed,
        timing: timingFor(closed, due), storedTiming: clean(r.Timing), review: clean(r.ReviewState), confidence: clean(r.Confidence),
        risk: clean(r.Risk) || 'Medium', notes: clean(r.Notes), fulfilledOn: parseDate(r.FulfilledOn), sample: yes(r.IsSample)
      };
    },
    contract: function (r) {
      var file = clean(r.FileLeafRef) || clean(r.Title);
      return {
        id: clean(r.ID).replace(/\.0+$/, ''), file: file, title: clean(r.Title) || file.replace(/\.[a-z0-9]+$/i, ''),
        counterparty: clean(r.Counterparty), type: clean(r.ContractType), effective: parseDate(r.EffectiveDate),
        expiration: parseDate(r.ExpirationDate), autoRenews: clean(r.AutoRenews), notice: num(r.NoticePeriodDays),
        law: clean(r.GoverningLaw), value: num(r.ContractValue), valueRaw: clean(r.ContractValue), summary: clean(r.ContractSummary),
        owner: people(r.ContractOwner).join(', '), bu: clean(r.BusinessUnit), amends: clean(r.Amends),
        isAmendment: !!clean(r.Amends) || /amendment/i.test(clean(r.ContractType)), sample: yes(r.IsSample), key: contractKey(file)
      };
    },
    run: function (r) {
      return {
        id: clean(r.ID), title: clean(r.Title), workflow: clean(r.Workflow), outcome: clean(r.Outcome), contract: clean(r.ContractName),
        version: clean(r.ContractVersion), created: num(r.ItemsCreated), updated: num(r.ItemsUpdated), held: num(r.ItemsHeld),
        details: clean(r.Details), at: parseDate(r.RunAt, true)
      };
    },
    rule: function (r) {
      return { id: clean(r.ID), title: clean(r.Title), category: clean(r.Category) || 'Any', bu: clean(r.BusinessUnit) || 'Any',
        counterparty: clean(r.Counterparty), owner: people(r.Owner).join(', '), escalation: people(r.EscalationOwner).join(', '), notify: clean(r.Notify) };
    }
  };
  Hub.timingFor = timingFor;
  Hub.TIMING_ORDER = ['Overdue', 'Due soon', 'Upcoming', 'No date', 'Closed'];
  Hub.byDue = function (a, b) {
    if (a.due && b.due) return a.due - b.due || a.title.localeCompare(b.title);
    if (a.due) return -1;
    if (b.due) return 1;
    return a.title.localeCompare(b.title);
  };
  Hub.matchesContract = function (o, c) {
    var k = contractKey(o.contract || o);
    return !!k && (k === c.key || k === contractKey(c.title));
  };
  Hub.shortParty = function (s) {
    return clean(s).replace(/,?\s+(ltd|limited|inc|incorporated|llc|plc|corp|corporation|co|gmbh|sa|ag|bv|pty)\.?$/i, '');
  };

  /* ---------------- icons & pills ---------------- */
  function icon(name, cls) { return '<svg class="' + (cls || 'i') + '" aria-hidden="true" focusable="false"><use href="#i-' + name + '"></use></svg>'; }
  Hub.icon = icon;
  var TIMING_KIND = { 'Overdue': ['overdue', 'overdue'], 'Due soon': ['soon', 'soon'], 'Upcoming': ['upcoming', 'upcoming'], 'No date': ['nodate', 'nodate'], 'Closed': ['closed', 'check'] };
  Hub.pill = function (kind, label, ic) { return '<span class="pill pill--' + kind + '">' + (ic ? icon(ic) : '') + esc(label) + '</span>'; };
  Hub.timingPill = function (t) { var k = TIMING_KIND[t] || ['nodate', 'nodate']; return Hub.pill(k[0], t, k[1]); };
  Hub.outcomePill = function (o) {
    var s = clean(o);
    if (!s) return Hub.pill('nodate', 'Not run yet', 'nodate');
    if (/succe/i.test(s)) return Hub.pill('ok', s, 'check');
    if (/partial/i.test(s)) return Hub.pill('soon', s, 'soon');
    if (/fail/i.test(s)) return Hub.pill('overdue', s, 'overdue');
    return Hub.pill('nodate', s, 'nodate');
  };
  /* Timing shown is always recalculated for today; say so when the list's stored value (refreshed by the daily sweep) disagrees. */
  Hub.timingNote = function (o) {
    if (!o.storedTiming || o.storedTiming.toLowerCase() === o.timing.toLowerCase()) return '';
    return '<span class="cell-sub timing-note">List says \u201c' + esc(o.storedTiming) + '\u201d until the next daily sweep</span>';
  };
  Hub.riskPill = function (r) { return /high/i.test(r) ? Hub.pill('overdue', 'High risk', 'flag') : ''; };
  /* One definition of the Risk levels. How it works carries the same sentences as static text (a test keeps them identical). */
  Hub.RISK_LEVELS = [
    { level: 'High', text: 'Missing it automatically loses a right or money or starts a legal clock (notice, renewal and option deadlines we must act on; change-of-control and breach notices; financing covenants, compliance certificates and default notices).' },
    { level: 'Medium', text: 'Other dated or money obligations (payments, reports, certificates, audits).' },
    { level: 'Low', text: 'Ongoing conduct, and counterparty duties we only monitor.' }
  ];
  Hub.categoryPill = function (c) { return Hub.pill('quiet', c || 'Other'); };
  Hub.ownerText = function (o) { return o.owner ? esc(o.owner) : Hub.pill('empty', 'No owner'); };

  /* ---------------- hash state (location.hash only; history entries are never written directly) ---------------- */
  Hub.hash = {
    get: function () {
      var h = String(window.location.hash || '').replace(/^#/, ''), out = {};
      h.split('&').forEach(function (part) {
        var i = part.indexOf('=');
        if (i < 1) return;
        var k = part.slice(0, i), v = part.slice(i + 1);
        try { k = decodeURIComponent(k); v = decodeURIComponent(v.replace(/\+/g, ' ')); } catch (e) { /* keep raw */ }
        out[k] = v;
      });
      return out;
    },
    href: function (obj) {
      var parts = [];
      Object.keys(obj).forEach(function (k) { if (obj[k] !== undefined && obj[k] !== null && obj[k] !== '') parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])); });
      return '#' + parts.join('&');
    },
    set: function (obj) { window.location.hash = Hub.hash.href(obj); }
  };

  /* ---------------- badge, notes, errors ---------------- */
  Hub.badge = function (data, primaryKey, count, one, many) {
    var el = byId('data-badge');
    var p = data[primaryKey] || { live: false };
    var keys = Object.keys(data);
    var sampleOthers = keys.filter(function (k) { return k !== primaryKey && !data[k].live; });
    var anyLive = keys.some(function (k) { return data[k].live; });
    var text = (p.live ? 'Live' : 'Sample snapshot') + ' \u00b7 ' + plural(count, one, many);
    if (p.live && sampleOthers.length) text += ' \u00b7 partly sample';
    var detail = keys.map(function (k) { return data[k].label + ': ' + (data[k].live ? 'live list data' : 'sample snapshot'); }).join('; ');
    if (el) {
      el.className = 'badge ' + (p.live ? 'badge--live' : 'badge--sample');
      el.setAttribute('title', detail);
      el.innerHTML = '<span class="badge__dot" aria-hidden="true"></span><span>' + esc(text) + '</span><span class="sr-only">. ' + esc(detail) + '.</span>';
    }
    var notes = [];
    keys.forEach(function (k) {
      if (data[k].error) notes.push('Live data for ' + data[k].label + ' couldn\u2019t be read (' + data[k].error + '), so this page shows the sample snapshot for it.');
    });
    if (!anyLive && !notes.length) notes.push('Showing the sample snapshot \u2014 fictional data bundled with the page. Live list data appears automatically when the site provides it.');
    var n = byId('data-note');
    if (n) {
      n.hidden = !notes.length;
      n.innerHTML = notes.map(function (t) { return '<p>' + esc(t) + '</p>'; }).join('');
    }
    return text;
  };
  Hub.fail = function (err, where) {
    var target = byId(where || 'main');
    var msg = (err && (err.message || String(err))) || 'Unknown error';
    var html = '<div class="state state--error" role="alert"><h2>This view couldn\u2019t be drawn</h2>' +
      '<p>Refresh the page. If it keeps happening, open the lists directly from Site contents or ask the site owner to check the Run Log.</p>' +
      '<details class="disclose"><summary>' + icon('chev') + 'Technical details</summary><p><code>' + esc(msg) + '</code></p></details></div>';
    if (target) {
      if (target.id === 'main') target.innerHTML = '<div class="wrap">' + html + '</div>';
      else target.innerHTML = html;
    }
    if (window.console && console.error) console.error('[Obligation Hub]', err);
  };
  Hub.announce = function (text) { var r = byId('live-region'); if (r) { r.textContent = ''; setTimeout(function () { r.textContent = text; }, 30); } };

  /* ---------------- copy to clipboard ---------------- */
  function selectNode(node) {
    try {
      var sel = window.getSelection && window.getSelection();
      if (!sel || !document.createRange) return false;
      var range = document.createRange(); range.selectNodeContents(node); sel.removeAllRanges(); sel.addRange(range);
      return true;
    } catch (e) { return false; }
  }
  function legacyCopy(text) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0'; ta.style.top = '0';
      document.body.appendChild(ta); ta.select();
      var ok = document.execCommand && document.execCommand('copy');
      document.body.removeChild(ta);
      return !!ok;
    } catch (e) { return false; }
  }
  /* Last resort when the sandbox blocks the clipboard: show the text in a read-only field, focused and selected. */
  function manualCopy(text, btn) {
    var host = btn && btn.parentNode;
    if (!host || !document.createElement) return;
    var box = host.querySelector ? host.querySelector('.copy-manual') : null;
    if (!box) {
      box = document.createElement('div');
      box.className = 'copy-manual';
      box.innerHTML = '<label class="label">Press Ctrl+C (or \u2318C) to copy</label><input class="control" readonly>';
      host.appendChild(box);
    }
    var input = box.querySelector('input');
    input.value = text;
    try { input.focus(); input.select(); } catch (e) { /* ignore */ }
  }
  Hub.copy = function (text, btn, selectTarget) {
    var state = btn && btn.querySelector ? btn.querySelector('.chip__state') : null;
    function done(ok) {
      var msg = ok ? 'Copied' : 'Press Ctrl+C to copy';
      if (!ok) {
        if (selectTarget && !closest(selectTarget, 'button') && selectNode(selectTarget)) { try { selectTarget.focus(); } catch (e) { /* ignore */ } }
        else manualCopy(text, btn);
      }
      if (state) { state.textContent = ok ? 'Copied' : 'Press Ctrl+C'; setTimeout(function () { state.textContent = state.getAttribute('data-idle') || 'Copy'; }, 2400); }
      Hub.announce(msg);
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(legacyCopy(text)); });
        return;
      }
    } catch (e) { /* fall through */ }
    done(legacyCopy(text));
  };
  document.addEventListener('click', function (e) {
    var b = closest(e.target, '[data-copy]');
    if (!b) return;
    e.preventDefault();
    var src = b.getAttribute('data-copy-from');
    var srcEl = src ? byId(src) : null;
    var text = srcEl ? srcEl.textContent : b.getAttribute('data-copy');
    Hub.copy(text, b, srcEl || b.querySelector('.chip__text'));
  });

  /* tooltips: Escape dismisses (WCAG 1.4.13); leaving re-arms */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    var h = closest(document.activeElement, '.hint');
    if (h && h.classList) h.classList.add('is-dismissed');
  });
  function rearm(e) { var h = closest(e.target, '.hint'); if (h && h.classList) h.classList.remove('is-dismissed'); }
  document.addEventListener('focusout', rearm);
  document.addEventListener('mouseout', rearm);

  /* ---------------- links between pages ----------------
     There is no in-page nav bar: SharePoint's site navigation is the primary nav. Static links to other pages
     carry data-page; before install (tokens not replaced) they point at the sibling file instead. */
  function initLinks() {
    var links = document.querySelectorAll ? document.querySelectorAll('[data-page]') : [];
    Array.prototype.forEach.call(links, function (a) {
      if (Hub.preview || unreplaced(cfg.pagesUrl)) a.setAttribute('href', a.getAttribute('data-page'));
    });
  }

  /* ---------------- AI workflows, grouped by Run Log "Workflow" value ----------------
     Capture is two workflows (one trigger each) running the same skill; both log as "Capture",
     so they share one health row here and both Settings cards show its last run. */
  Hub.WORKFLOWS = [
    { name: 'Capture', label: 'Capture obligations', skill: 'capture-obligations', tokens: ['CAPTURE_NEW', 'CAPTURE_CHANGED'], trigger: 'When a contract is added or changed', staleDays: null },
    { name: 'Assign owners', label: 'Assign owners', skill: 'assign-obligation-owners', tokens: ['ASSIGN_OWNERS'], trigger: 'Daily at 7:00 AM', staleDays: 2 },
    { name: 'Daily sweep', label: 'Daily sweep', skill: 'sweep-obligations', tokens: ['DAILY_SWEEP'], trigger: 'Daily at 6:00 AM', staleDays: 2 },
    { name: 'Owner digest', label: 'Owner digest', skill: 'obligation-owner-digest', tokens: ['OWNER_DIGEST'], trigger: 'Mondays at 8:00 AM', staleDays: 8 },
    { name: 'Leadership digest', label: 'Leadership digest', skill: 'obligation-leadership-digest', tokens: ['LEADERSHIP_DIGEST'], trigger: 'Fridays at 3:00 PM', staleDays: 8 }
  ];
  Hub.lastRuns = function (runs) {
    var any = runs.length > 0;   // on a brand-new site the setup checklist covers "never ran"
    return Hub.WORKFLOWS.map(function (w) {
      var k = normKey(w.name), kl = normKey(w.label);
      var mine = runs.filter(function (r) { var rk = normKey(r.workflow); return rk === k || rk === kl || (rk && rk.indexOf(k) === 0); });
      mine.sort(function (a, b) { return (b.at ? b.at.getTime() : 0) - (a.at ? a.at.getTime() : 0); });
      var last = mine[0] || null, issue = null;
      var age = last && last.at ? (now() - last.at) / DAY : null;
      if (last && /fail/i.test(last.outcome)) issue = { level: 'rose', text: w.label + ' failed ' + Hub.fmt.ago(last.at) + '.' };
      else if (w.staleDays && last && age !== null && age > w.staleDays) issue = { level: 'amber', text: w.label + ' hasn\u2019t run for ' + Math.floor(age) + ' days.' };
      else if (w.staleDays && !last && any) issue = { level: 'amber', text: w.label + ' hasn\u2019t run yet.' };
      return { wf: w, last: last, count: mine.length, issue: issue };
    });
  };

  /* ---------------- focus preservation across re-renders ---------------- */
  Hub.keepFocus = function (fn) {
    var a = document.activeElement, key = a && a.getAttribute ? a.getAttribute('data-focus') : null;
    fn();
    if (key && document.querySelector) { var n = document.querySelector('[data-focus="' + key.replace(/"/g, '') + '"]'); if (n && n.focus) n.focus(); }
  };

  /* ---------------- page bootstrap ---------------- */
  Hub.start = function (opts) {
    var data = null;
    function build() {
      data = {};
      opts.lists.forEach(function (k) { data[k] = loadList(k); });
      Hub.data = data;
      draw();
    }
    function draw() {
      try { opts.render(data, Hub.hash.get()); }
      catch (e) { Hub.fail(e); }
    }
    function hasLive() { return window.__LD_RESULTS__ && typeof window.__LD_RESULTS__ === 'object'; }
    function watchLate() {
      var waited = 0, t = setInterval(function () {
        waited += 250;
        if (hasLive()) { clearInterval(t); build(); }
        else if (waited >= LATE_WATCH_MS) clearInterval(t);
      }, 250);
    }
    try { initLinks(); } catch (e) { /* links work without it once installed */ }
    if (opts.lists.length === 0 || hasLive()) build();
    else {
      var waited = 0, t = setInterval(function () {
        waited += 100;
        if (hasLive() || waited >= LIVE_WAIT_MS) { clearInterval(t); build(); if (!hasLive()) watchLate(); }
      }, 100);
    }
    window.addEventListener('hashchange', function () { if (data) Hub.keepFocus(draw); });
    var rt = null;
    window.addEventListener('resize', function () {
      if (!data || !opts.onResize) return;
      clearTimeout(rt); rt = setTimeout(function () { try { opts.onResize(data); } catch (e) { /* ignore */ } }, 160);
    });
  };
})(window, document);
