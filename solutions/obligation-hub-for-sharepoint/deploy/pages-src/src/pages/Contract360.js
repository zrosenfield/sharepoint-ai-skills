/* Contract 360 */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, icon = Hub.icon, plural = Hub.plural;
  var state = { query: '', current: null, contracts: [], obs: [], runs: [], fam: null };
  var PARTY = [
    { key: 'Us', title: 'We owe', note: 'Our duties under this contract.' },
    { key: 'Counterparty', title: 'They owe', note: 'Their duties we hold them to.' },
    { key: 'Both', title: 'Both parties', note: 'Mutual duties and rights either side can use.' }
  ];

  function label(c) {
    return (c.isAmendment ? '\u21b3 ' : '') + (c.counterparty ? c.counterparty + ' \u2014 ' : '') + c.title;
  }
  function sortContracts(list) {
    return list.slice().sort(function (a, b) {
      var ka = (a.isAmendment ? Hub.contractKey(a.amends) : a.key), kb = (b.isAmendment ? Hub.contractKey(b.amends) : b.key);
      var ba = list.filter(function (x) { return x.key === ka; })[0] || a, bb = list.filter(function (x) { return x.key === kb; })[0] || b;
      return (ba.counterparty || ba.title).localeCompare(bb.counterparty || bb.title) || ba.file.localeCompare(bb.file) ||
        (a.isAmendment - b.isAmendment) || ((a.effective || 0) - (b.effective || 0));
    });
  }
  function matches(c, q) {
    if (!q) return true;
    var hay = (c.counterparty + ' ' + c.title + ' ' + c.file + ' ' + c.type).toLowerCase();
    return q.toLowerCase().split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }

  function renderPicker() {
    var sel = Hub.byId('c-select'), count = Hub.byId('c-search-count');
    if (!sel) return;
    var list = state.contracts.filter(function (c) { return matches(c, state.query); });
    var cur = state.current;
    var html = '';
    if (!state.contracts.length) html = '<option>No contracts yet</option>';
    else {
      if (!list.length) html = '<option value="">No contracts match</option>';
      else if (!cur || list.indexOf(cur) === -1) html = '<option value="">Choose from ' + plural(list.length, 'match', 'matches') + '\u2026</option>';
      html += list.map(function (c) { return '<option value="' + esc(c.file) + '"' + (c === cur ? ' selected' : '') + '>' + esc(label(c)) + '</option>'; }).join('');
    }
    sel.innerHTML = html;
    sel.disabled = !state.contracts.length;
    if (count) count.textContent = state.query ? (list.length ? plural(list.length, 'contract') + ' of ' + state.contracts.length + ' match' : 'No contracts match \u201c' + state.query + '\u201d') : '';
    if (!sel.__wired) {
      sel.__wired = true;
      sel.addEventListener('change', function () { if (sel.value) Hub.hash.set({ contract: sel.value }); });
      var input = Hub.byId('c-search');
      if (input) {
        input.addEventListener('input', function () { state.query = input.value.trim(); renderPicker(); });
        input.addEventListener('keydown', function (e) {
          if (e.key !== 'Enter') return;
          var first = state.contracts.filter(function (c) { return matches(c, state.query); })[0];
          if (first) { e.preventDefault(); Hub.hash.set({ contract: first.file }); }
        });
      }
    }
  }

  function family(c) {
    var base = c.isAmendment ? (state.contracts.filter(function (x) { return x.key === Hub.contractKey(c.amends); })[0] || null) : c;
    var root = base || c;
    var amendments = state.contracts.filter(function (a) { return a.isAmendment && Hub.contractKey(a.amends) === root.key; })
      .sort(function (a, b) { return (a.effective || 0) - (b.effective || 0); });
    var notice = root.notice, noticeFrom = null, expiration = root.expiration, autoRenews = root.autoRenews;
    amendments.forEach(function (a) {
      if (a.notice != null && a.notice !== notice) { notice = a.notice; noticeFrom = a; }
      if (a.expiration) expiration = a.expiration;
      if (a.autoRenews) autoRenews = a.autoRenews;
    });
    return { root: root, base: base, amendments: amendments, members: [root].concat(amendments), notice: notice, noticeFrom: noticeFrom, expiration: expiration, autoRenews: autoRenews };
  }

  /* With no #contract, open the contract whose next notice deadline, renewal decision or expiry comes soonest. */
  function defaultContract(allObs) {
    var t = Hub.date.today(), best = null, bestDate = null;
    state.contracts.filter(function (c) { return !c.isAmendment; }).forEach(function (c) {
      var f = family(c), dates = [];
      if (f.expiration && f.expiration >= t) dates.push(f.expiration);
      if (f.expiration && /^yes$/i.test(f.autoRenews) && f.notice != null) {
        var dl = Hub.date.addDays(f.expiration, -Math.round(f.notice));
        if (dl >= t) dates.push(dl);
      }
      allObs.forEach(function (o) {
        if (!o.closed && o.due && o.due >= t && /notice/i.test(o.category) && f.members.some(function (m) { return Hub.matchesContract(o, m); })) dates.push(o.due);
      });
      dates.sort(function (a, b) { return a - b; });
      if (dates.length && (!bestDate || dates[0] < bestDate)) { best = c; bestDate = dates[0]; }
    });
    return best || state.contracts.filter(function (c) { return !c.isAmendment; })[0] || state.contracts[0] || null;
  }

  /* Sits directly under the summary: a base contract names its amendments (Amends = this file); an amendment links back to its base. */
  function amendNote(c, f) {
    var html = '';
    if (c.isAmendment) {
      if (f.base) html = 'Amends <a href="' + esc(Hub.hash.href({ contract: f.base.file })) + '">' + esc(f.base.title) + '</a>';
      else if (c.amends) html = 'Amends \u201c' + esc(c.amends) + '\u201d, which isn\u2019t in the Contracts library.';
    } else if (f.amendments.length) {
      var names = f.amendments.map(function (a) {
        return '<a href="' + esc(Hub.hash.href({ contract: a.file })) + '">' + esc(a.title) + '</a>' + (a.effective ? ' (' + esc(fmt.date(a.effective)) + ')' : '');
      });
      var many = names.length > 1;
      html = 'Amended by ' + (many ? names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1] : names[0]) + '. The terms below reflect the amendment' + (many ? 's' : '') +
        ' where they differ' + (c.summary ? '; the summary above describes the original document.' : '.');
    }
    return html ? '<p class="c-amend" id="c-amend">' + icon('layers') + '<span>' + html + '</span></p>' : '';
  }

  function termRow(label, value, small) {
    return '<div><dt>' + esc(label) + '</dt><dd>' + (value || '<span class="muted">Not recorded</span>') + (small ? '<small>' + esc(small) + '</small>' : '') + '</dd></div>';
  }

  /* ---------- mini notice timeline ---------- */
  function drawMini() {
    var host = Hub.byId('mini'), c = state.current, f = state.fam;
    if (!host || !c) return;
    var t = Hub.date.today();
    var start = c.effective && c.effective < t ? c.effective : Hub.date.addDays(t, -30);
    var exp = f.expiration;
    var end = exp ? (exp > Hub.date.addDays(t, 60) ? exp : Hub.date.addDays(t, 60)) : Hub.date.addDays(t, 365);
    var W = Math.max(300, host.clientWidth || 900), pad = 8, laneY = 58, H = 124, narrow = W < 640;
    if (narrow) H = 160;
    function X(d) { var span = end - start || 1; return Math.round(pad + ((d - start) / span) * (W - 2 * pad)); }
    var deadline = exp && /^yes$/i.test(f.autoRenews) && f.notice != null ? Hub.date.addDays(exp, -Math.round(f.notice)) : null;
    var obs = state.obs.filter(function (o) { return !o.closed && o.due && o.due >= start && o.due <= end; });
    var out = ['<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-labelledby="mini-t"><title id="mini-t">Contract term from ' +
      esc(c.effective ? fmt.date(c.effective) : 'start') + (exp ? ' to ' + esc(fmt.date(exp)) : ' with no fixed end date') + '. Key dates are listed below.</title>'];
    out.push('<defs><linearGradient id="mini-g" x1="0" x2="1"><stop offset="0" stop-color="#9AC7F5" stop-opacity=".45"/><stop offset="1" stop-color="#8B83DB" stop-opacity=".28"/></linearGradient></defs>');
    out.push('<rect x="' + pad + '" y="' + (laneY - 7) + '" width="' + (W - 2 * pad) + '" height="14" rx="7" fill="#EAF3FC"/>');
    var termEnd = exp ? X(exp) : W - pad;
    out.push('<rect x="' + X(start) + '" y="' + (laneY - 7) + '" width="' + Math.max(14, termEnd - X(start)) + '" height="14" rx="7" fill="url(#mini-g)"/>');
    if (!exp) out.push('<path d="M' + (W - pad - 18) + ' ' + (laneY - 5) + 'l8 5-8 5" fill="none" stroke="#374151" stroke-width="1.5"/>');
    if (deadline && exp) out.push('<rect x="' + X(deadline) + '" y="' + (laneY - 7) + '" width="' + Math.max(2, X(exp) - X(deadline)) + '" height="14" fill="#8B83DB" fill-opacity=".45"><title>Notice period</title></rect>');
    obs.forEach(function (o) { out.push('<line x1="' + X(o.due) + '" x2="' + X(o.due) + '" y1="' + (laneY - 16) + '" y2="' + (laneY - 9) + '" stroke="#374151" stroke-width="1.5" stroke-linecap="round"><title>' + esc(o.title + ' \u2014 ' + fmt.date(o.due)) + '</title></line>'); });
    var tx = X(t);
    out.push('<line x1="' + tx + '" x2="' + tx + '" y1="18" y2="' + (laneY + 12) + '" stroke="#111827" stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round"/>');
    var labels = [];
    function lab(x, y, a, b, anchor) { labels.push('<text class="m-lab" x="' + x + '" y="' + y + '" text-anchor="' + anchor + '">' + esc(a) + '</text>' + (b ? '<text class="m-sub" x="' + x + '" y="' + (y + 15) + '" text-anchor="' + anchor + '">' + esc(b) + '</text>' : '')); }
    function anchorFor(x) { return x < W * 0.2 ? 'start' : x > W * 0.8 ? 'end' : 'middle'; }
    lab(tx, 12, 'Today', '', anchorFor(tx));
    if (c.effective) { out.push('<circle cx="' + X(c.effective) + '" cy="' + laneY + '" r="5" fill="#111827"/>'); lab(X(c.effective), laneY + 28, 'Effective', fmt.date(c.effective), 'start'); }
    if (exp) { out.push('<circle cx="' + X(exp) + '" cy="' + laneY + '" r="6" fill="#FFFFFF" stroke="#111827" stroke-width="2"/><circle cx="' + X(exp) + '" cy="' + laneY + '" r="2" fill="#111827"/>'); lab(X(exp), laneY + 28, 'Expires', fmt.date(exp), 'end'); }
    if (deadline) {
      var dx = X(deadline);
      out.push('<path d="M' + dx + ' ' + (laneY - 8) + 'l8 8-8 8-8-8z" fill="#8B83DB" stroke="#111827" stroke-width="1.4"/>');
      var dText = fmt.date(deadline) + ' \u00b7 ' + (deadline < t ? 'passed' : fmt.rel(deadline));
      if (narrow) {
        out.push('<line x1="' + dx + '" x2="' + dx + '" y1="' + (laneY + 10) + '" y2="' + (laneY + 62) + '" stroke="#3F3891" stroke-width="1" stroke-dasharray="2 3"/>');
        lab(dx, laneY + 78, 'Notice deadline', dText, dx > W * 0.6 ? 'end' : 'start');
      } else {
        var mid = c.effective && exp ? (X(c.effective) + X(exp)) / 2 : W / 2;
        lab(Math.min(Math.max(dx, mid - 60), W - 200), laneY + 28, 'Notice deadline', dText, Math.abs(dx - X(exp)) < 220 ? 'end' : 'middle');
      }
    }
    out.push(labels.join(''), '</svg>');
    host.innerHTML = out.join('');
  }

  function keyDates() {
    var c = state.current, f = state.fam, t = Hub.date.today(), items = [];
    var dot = '<svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="4.5" fill="#111827"/></svg>';
    var ring = '<svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="4.5" fill="#FFFFFF" stroke="#111827" stroke-width="2"/></svg>';
    var dia = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 .8 11.2 6 6 11.2.8 6z" fill="#8B83DB" stroke="#111827" stroke-width="1.2"/></svg>';
    if (c.effective) items.push(dot + '<span><strong>Effective</strong> ' + esc(fmt.date(c.effective)) + '</span>');
    if (f.expiration && /^yes$/i.test(f.autoRenews) && f.notice != null) {
      var dl = Hub.date.addDays(f.expiration, -Math.round(f.notice));
      items.push(dia + '<span><strong>Notice deadline</strong> ' + esc(fmt.date(dl)) + ' \u00b7 ' + (dl < t ? 'passed' : esc(fmt.rel(dl))) + ' (' + f.notice + ' days before expiry)</span>');
    }
    if (f.expiration) items.push(ring + '<span><strong>Expires</strong> ' + esc(fmt.date(f.expiration)) + ' \u00b7 ' + (f.expiration < t ? 'passed' : esc(fmt.rel(f.expiration))) + '</span>');
    else items.push(ring + '<span><strong>No fixed end date</strong></span>');
    var n = state.obs.filter(function (o) { return !o.closed && o.due; }).length;
    if (n) items.push('<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 2v8" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg><span>' + plural(n, 'dated obligation') + ' (ticks above the line)</span>');
    return '<ul class="mini-list" aria-label="Key dates">' + items.map(function (i) { return '<li>' + i + '</li>'; }).join('') + '</ul>';
  }

  function oblItem(o, c) {
    var fromAmend = !Hub.matchesContract(o, c);
    var when = o.closed ? o.status + (o.fulfilledOn ? ' ' + fmt.date(o.fulfilledOn) : '') + (o.due ? ' \u00b7 was due ' + fmt.date(o.due) : '')
      : o.due ? fmt.date(o.due) + ' \u00b7 ' + fmt.due(o.due) : (o.triggerType === 'Ongoing' ? 'Ongoing' : 'When: ' + (o.triggerEvent || 'triggered by an event'));
    return '<li><div><a class="obl__title" href="' + esc(Hub.url.disp('OBLIGATIONS', o.id)) + '" target="_top">' + esc(o.title) + '</a>' +
      '<span class="obl__meta">' + esc([when, o.clause, o.recurrence && o.recurrence !== 'None' ? o.recurrence : ''].filter(Boolean).join(' \u00b7 ')) + '</span>' +
      '<div class="pills">' + Hub.categoryPill(o.category) + Hub.riskPill(o.risk) + (/needs review/i.test(o.review) ? Hub.pill('review', 'Needs review', 'review') : '') +
      (fromAmend ? Hub.pill('quiet', 'From ' + (o.contract || 'amendment')) : '') + '</div></div>' +
      '<div class="obl__right">' + Hub.timingPill(o.timing) + '<span>' + (o.owner ? esc(o.owner) : Hub.pill('empty', 'No owner')) + '</span></div>' +
      (o.source ? '<details class="disclose"><summary>' + icon('chev') + 'Source clause' + (o.clause ? ' \u00b7 ' + esc(o.clause) : '') + '</summary><blockquote class="quote">' + esc(o.source) + '</blockquote></details>' : '') +
      '</li>';
  }

  function render(data, hash) {
    state.contracts = sortContracts(data.CONTRACTS.rows.map(Hub.model.contract).filter(function (c) { return c.file; }));
    var allObs = data.OBLIGATIONS.rows.map(Hub.model.obligation);
    var runs = data.RUNLOG.rows.map(Hub.model.run);
    Hub.badge(data, 'CONTRACTS', state.contracts.length, 'contract');
    var want = hash.contract ? hash.contract.toLowerCase() : '';
    var cur = want ? state.contracts.filter(function (c) { return c.file.toLowerCase() === want || c.key === Hub.contractKey(want) || c.title.toLowerCase() === want; })[0] : null;
    if (!want) cur = defaultContract(allObs);
    state.current = cur;
    renderPicker();
    var host = Hub.byId('c360');
    if (host) host.setAttribute('aria-busy', 'false');

    if (!state.contracts.length) {
      Hub.setHTML('page-title', 'Contracts');
      Hub.setHTML('c360', '<div class="card state"><svg viewBox="0 0 120 96" aria-hidden="true"><rect x="30" y="12" width="56" height="70" rx="10" fill="#EAF3FC" stroke="#D3DDE9"/><path d="M42 32h32M42 44h24M42 56h28" stroke="#9AC7F5" stroke-width="4" stroke-linecap="round"/></svg>' +
        '<h2>No contracts yet</h2><p>Upload a signed contract to the Contracts library. Key terms fill in automatically and capture adds its obligations.</p>' +
        '<p><a class="btn btn--primary" href="' + esc(Hub.url.view('CONTRACTS')) + '" target="_top">' + icon('upload') + 'Open Contracts library</a></p></div>');
      return;
    }
    if (!cur) {
      Hub.setHTML('page-title', 'Contract not found');
      Hub.setHTML('c360', '<div class="card state"><h2>We couldn\u2019t find \u201c' + esc(hash.contract) + '\u201d</h2><p>It may have been renamed or removed. Choose a contract above.</p></div>');
      return;
    }
    var f = state.fam = family(cur);
    var keys = f.members.map(function (m) { return m.key; });
    state.obs = allObs.filter(function (o) { return f.members.some(function (m) { return Hub.matchesContract(o, m); }); });
    if (cur.isAmendment) state.obs = allObs.filter(function (o) { return Hub.matchesContract(o, cur); });
    state.obs.sort(Hub.byDue);
    var myRuns = runs.filter(function (r) { var k = Hub.contractKey(r.contract); return k && (cur.isAmendment ? k === cur.key : keys.indexOf(k) !== -1); })
      .sort(function (a, b) { return (b.at ? b.at.getTime() : 0) - (a.at ? a.at.getTime() : 0); });

    Hub.setHTML('page-title', esc(cur.counterparty || cur.title));
    Hub.setHTML('page-sub', esc('Key terms, notice dates, every obligation and the capture history for the ' + cur.title + '.'));

    var open = state.obs.filter(function (o) { return !o.closed; });
    var noticeSmall = f.noticeFrom && cur.notice != null && f.noticeFrom !== cur ? 'Set by ' + (f.noticeFrom.title || 'amendment') + '; originally ' + cur.notice + ' days' : '';
    var notice = (cur.isAmendment ? cur.notice : f.notice);
    var exp = cur.isAmendment ? cur.expiration : f.expiration;
    var terms = '<dl class="terms">' +
      termRow('Counterparty', esc(cur.counterparty)) +
      termRow('Contract type', esc(cur.type)) +
      termRow('Effective', cur.effective ? esc(fmt.date(cur.effective)) : '') +
      termRow('Expires', exp ? esc(fmt.date(exp)) : '<span class="muted">No fixed end date</span>', exp ? (exp < Hub.date.today() ? 'Expired' : fmt.rel(exp)) : '') +
      termRow('Auto-renews', esc(cur.isAmendment ? cur.autoRenews : f.autoRenews)) +
      termRow('Notice period', notice != null ? esc(notice + ' days') : '', cur.isAmendment ? '' : noticeSmall) +
      termRow('Contract value', cur.value != null || cur.valueRaw ? esc(fmt.money(cur.value, cur.valueRaw)) : '') +
      termRow('Governing law', esc(cur.law)) +
      termRow('Contract owner', esc(cur.owner)) +
      termRow('Business unit', esc(cur.bu)) +
      termRow('Open obligations', String(open.length), plural(state.obs.length - open.length, 'closed', 'closed')) +
      (cur.isAmendment ? termRow('Amends', f.base ? '<a href="' + esc(Hub.hash.href({ contract: f.base.file })) + '">' + esc(f.base.title) + '</a>' : esc(cur.amends)) : '') +
      '</dl>';

    var html = '<section class="card settle" aria-labelledby="c-title">' +
      '<div class="c-hero"><div><h2 id="c-title">' + esc(cur.title) + '</h2><p class="c-hero__file">' + esc(cur.file) + '</p>' +
      '<div class="pills">' + (cur.type ? Hub.pill('quiet', cur.type) : '') + (/^yes$/i.test(f.autoRenews) ? Hub.pill('review', 'Auto-renews', 'review') : '') +
      (cur.isAmendment ? Hub.pill('quiet', 'Amendment') : '') + (f.amendments.length && !cur.isAmendment ? Hub.pill('quiet', plural(f.amendments.length, 'amendment')) : '') + (cur.sample ? Hub.pill('nodate', 'Sample data') : '') + '</div></div>' +
      '<div class="btn-row"><a class="btn btn--primary" href="' + esc(Hub.url.file('CONTRACTS', cur.file)) + '" target="_top">' + icon('doc') + 'Open contract</a>' +
      '<a class="btn" href="' + esc(Hub.url.disp('CONTRACTS', cur.id)) + '" target="_top">' + icon('edit') + 'Properties</a></div></div>' +
      (cur.summary ? '<p class="c-summary">' + esc(cur.summary) + '</p>' : '') + amendNote(cur, f) + terms +
      '<div class="mini"><h3 class="sr-only">Term and notice timeline</h3><div id="mini"></div>' + keyDates() + '</div></section>';

    var groups = PARTY.map(function (p) {
      var items = state.obs.filter(function (o) { return o.party === p.key; });
      if (!items.length) return '';
      return '<div class="party"><div class="party__head"><h3>' + esc(p.title) + ' <span class="muted">(' + items.length + ')</span></h3><p>' + esc(p.note) + '</p></div>' +
        '<ul class="obl">' + items.map(function (o) { return oblItem(o, cur); }).join('') + '</ul></div>';
    }).join('');
    var others = state.obs.filter(function (o) { return PARTY.every(function (p) { return p.key !== o.party; }); });
    if (others.length) groups += '<div class="party"><div class="party__head"><h3>Other</h3></div><ul class="obl">' + others.map(function (o) { return oblItem(o, cur); }).join('') + '</ul></div>';
    var listLink = Hub.url.view('OBLIGATIONS', [['ContractName', cur.file]]);
    var oblCard = '<section class="card settle" style="--d:1" aria-labelledby="o-title"><div class="card__head"><div><h2 id="o-title">Obligations</h2><p>' +
      esc(state.obs.length ? plural(state.obs.length, 'obligation') + (f.amendments.length && !cur.isAmendment ? ', including those added by amendments' : '') + ', grouped by who owes them.' : '') + '</p></div>' +
      '<a class="link-arrow" href="' + esc(listLink) + '" target="_top">Open in list' + icon('arrow') + '</a></div>' +
      (groups || '<div class="state state--inline"><p>No obligations captured for this contract yet. Capture runs when the file is added or changed \u2014 check the capture history, or select the file in Contracts and use the Re-capture obligations quick step.</p></div>') + '</section>';

    var amendCard = '';
    if (!cur.isAmendment) {
      amendCard = '<section class="card settle" style="--d:2" aria-labelledby="a-title"><h2 id="a-title" class="card__head">Amendments</h2>' +
        (f.amendments.length ? '<ul class="amend">' + f.amendments.map(function (a) {
          var bits = [a.effective ? 'Effective ' + fmt.date(a.effective) : '', a.notice != null && a.notice !== cur.notice ? 'Notice period ' + (cur.notice != null ? cur.notice + ' \u2192 ' : '') + a.notice + ' days' : ''].filter(Boolean);
          return '<li><a class="amend__title" href="' + esc(Hub.hash.href({ contract: a.file })) + '">' + esc(a.title) + '</a><span class="amend__sub">' + esc(bits.join(' \u00b7 ')) + '</span></li>';
        }).join('') + '</ul>' : '<p class="muted">No amendments. Upload one to Contracts and set <strong>Amends</strong> to this file name.</p>') + '</section>';
    } else {
      amendCard = '<section class="card settle" style="--d:2" aria-labelledby="a-title"><h2 id="a-title" class="card__head">Amends</h2>' +
        (f.base ? '<p><a class="link-arrow" href="' + esc(Hub.hash.href({ contract: f.base.file })) + '">' + esc(f.base.title) + icon('arrow') + '</a></p><p class="muted" style="margin-top:8px">Open the base contract to see the combined view.</p>' : '<p class="muted">The base contract \u201c' + esc(cur.amends) + '\u201d isn\u2019t in the library.</p>') + '</section>';
    }
    var histCard = '<section class="card settle" style="--d:3" aria-labelledby="h-title"><h2 id="h-title" class="card__head">Capture history</h2>' +
      (myRuns.length ? '<ul class="rows">' + myRuns.map(function (r) {
        var counts = [r.created != null ? r.created + ' created' : '', r.updated ? r.updated + ' updated' : '', r.held ? r.held + ' held for review' : ''].filter(Boolean).join(' \u00b7 ');
        return '<li><div class="pills">' + Hub.outcomePill(r.outcome) + '<span class="muted" style="font-size:13px">' + esc(r.workflow || 'Run') + (r.at ? ' \u00b7 <time datetime="' + esc(r.at.toISOString()) + '">' + esc(fmt.dateTime(r.at)) + '</time>' : '') + '</span></div>' +
          (f.amendments.length && !cur.isAmendment ? '<p class="muted" style="font-size:13px;margin-top:6px">' + esc(r.contract) + '</p>' : '') +
          (counts ? '<p style="margin-top:6px;font-weight:600;font-size:14px">' + esc(counts) + '</p>' : '') +
          (r.details ? '<p class="muted" style="margin-top:4px;font-size:14px">' + esc(r.details) + '</p>' : '') + '</li>';
      }).join('') + '</ul>' : '<p class="muted">No capture runs logged for this contract yet.</p>') +
      '<p class="muted" style="margin-top:16px;font-size:14px">Runs from <em>Capture new contracts</em> and <em>Capture changed contracts</em> both appear here as Capture. To capture this contract again, select it in <a href="' + esc(Hub.url.view('CONTRACTS')) + '" target="_top">Contracts</a> and use the <strong>Re-capture obligations</strong> quick step.</p>' +
      '<div class="card__foot"><a class="link-arrow" href="' + esc(Hub.url.view('RUNLOG', [['ContractName', cur.file]])) + '" target="_top">Open Run Log' + icon('arrow') + '</a></div></section>';

    html += '<div class="section grid-main"><div>' + oblCard + '</div><aside class="side" aria-label="Amendments and capture history">' + amendCard + histCard + '</aside></div>';
    Hub.setHTML('c360', html);
    drawMini();
  }

  Hub.start({ lists: ['CONTRACTS', 'OBLIGATIONS', 'RUNLOG'], render: render, onResize: drawMini });
})(window.Hub);
