/* Home - Obligations overview */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, icon = Hub.icon, plural = Hub.plural;
  var HORIZON = 180, SOON = 14;
  var model = null;

  function prepare(data) {
    var obs = data.OBLIGATIONS.rows.map(Hub.model.obligation);
    var contracts = data.CONTRACTS.rows.map(Hub.model.contract);
    var runs = data.RUNLOG.rows.map(Hub.model.run);
    var rules = data.OWNERS.rows.map(Hub.model.rule);
    return { data: data, obs: obs, open: obs.filter(function (o) { return !o.closed; }), contracts: contracts, runs: runs, rules: rules };
  }

  /* ---------- hero + KPIs ---------- */
  function renderHero(m) {
    var t = Hub.date.today();
    var overdue = m.open.filter(function (o) { return o.timing === 'Overdue'; }).length;
    var soon = m.open.filter(function (o) { return o.timing === 'Due soon'; }).length;
    var n = overdue + soon;
    Hub.setHTML('today-label', esc(fmt.long(t)));
    var title, sub;
    if (!m.obs.length) {
      title = 'No obligations yet';
      sub = 'Add a signed contract to the Contracts library and its obligations will appear here once capture has run.';
    } else if (!n) {
      var next = m.open.filter(function (o) { return o.due; }).sort(Hub.byDue)[0];
      title = 'Nothing needs attention in the next ' + SOON + ' days';
      sub = next ? 'The next due date is ' + fmt.date(next.due) + ' \u2014 ' + next.title + '.' : 'No open obligation has a due date.';
    } else {
      title = '<span class="hero__n">' + n + '</span> ' + (n === 1 ? 'obligation needs' : 'obligations need') + ' attention in the next ' + SOON + ' days';
      var parts = [];
      if (overdue) parts.push(plural(overdue, 'is', 'are').replace(/^\d+ /, overdue + ' ') + ' overdue');
      if (soon) parts.push(soon + ' ' + (soon === 1 ? 'falls' : 'fall') + ' due by ' + fmt.date(Hub.date.addDays(t, SOON)));
      sub = parts.join(' and ') + '. ' + plural(m.open.length, 'obligation') + ' open across ' + plural(countContracts(m), 'contract') + '.';
    }
    Hub.setHTML('hero-title', m.obs.length && n ? title : esc(title));
    Hub.setHTML('hero-sub', esc(sub));
    Hub.badge(m.data, 'OBLIGATIONS', m.obs.length, 'obligation');
  }
  function countContracts(m) {
    var base = m.contracts.filter(function (c) { return !c.isAmendment; }).length;
    if (base) return base;
    return Hub.uniq(m.obs.map(function (o) { return Hub.contractKey(o.contract); })).length;
  }

  /* Items held for review get an owner only once confirmed, so say so when that is all the tile is counting
     (and send the tile to the Review page, where they get confirmed). */
  function allHeldForReview(m) {
    var none = m.open.filter(function (o) { return !o.owner; });
    return none.length > 0 && none.every(function (o) { return /needs review/i.test(o.review); }) ? none.length : 0;
  }
  function noOwnerCaption(m) {
    var n = allHeldForReview(m);
    if (!n) return 'Open items with no owner yet. Items held for review get an owner once confirmed.';
    return n === 1 ? 'This one is waiting for review.' : 'All ' + n + ' are waiting for review.';
  }

  function renderKpis(m) {
    var REVIEW_PAGE = Hub.url.page('ReviewQueue.html');
    var count = function (fn) { return m.open.filter(fn).length; };
    var tiles = [
      { kind: 'overdue', label: 'Overdue', pill: Hub.pill('overdue', 'Overdue', 'overdue'), n: count(function (o) { return o.timing === 'Overdue'; }),
        cap: 'Past their due date and still open.', href: Hub.url.view('OBLIGATIONS', [['Timing', 'Overdue']]) },
      { kind: 'soon', label: 'Due in 14 days', pill: Hub.pill('soon', 'Due in 14 days', 'soon'), n: count(function (o) { return o.timing === 'Due soon'; }),
        cap: 'Falling due between today and ' + fmt.short(Hub.date.addDays(Hub.date.today(), SOON)) + '.', href: Hub.url.view('OBLIGATIONS', [['Timing', 'Due soon']]) },
      { kind: 'owner', label: 'Needs an owner', pill: Hub.pill('empty', 'Needs an owner', 'nodate'), n: count(function (o) { return !o.owner; }),
        cap: noOwnerCaption(m), href: allHeldForReview(m) ? REVIEW_PAGE : Hub.url.view('OBLIGATIONS', [['Owner', ''], ['Status', ['Not started', 'In progress']]]),
        go: allHeldForReview(m) ? 'Open Review' : '' },
      { kind: 'review', label: 'Needs review', pill: Hub.pill('review', 'Needs review', 'review'), n: m.obs.filter(function (o) { return /needs review/i.test(o.review); }).length,
        cap: 'Held by capture until someone confirms them.', href: REVIEW_PAGE, go: 'Open Review' }
    ];
    Hub.setHTML('kpis', tiles.map(function (k, i) {
      return '<a class="card kpi kpi--' + k.kind + ' settle" style="--d:' + (i + 1) + '" href="' + esc(k.href) + '" target="_top">' +
        '<span>' + k.pill + '</span>' +
        '<span class="kpi__value">' + k.n + '<span class="sr-only"> ' + esc(k.label.toLowerCase()) + '</span></span>' +
        '<span class="kpi__cap">' + esc(k.cap) + '</span>' +
        '<span class="kpi__go">' + esc(k.go || 'Open in list') + icon('arrow') + '</span></a>';
    }).join(''));
  }

  /* ---------- notice windows ---------- */
  function familyOf(m) {
    var base = m.contracts.filter(function (c) { return !c.isAmendment; });
    return base.map(function (c) {
      var amendments = m.contracts.filter(function (a) { return a.isAmendment && a.amends && Hub.contractKey(a.amends) === c.key; })
        .sort(function (a, b) { return (a.effective || 0) - (b.effective || 0); });
      var noticeFrom = null, notice = c.notice;
      amendments.forEach(function (a) { if (a.notice != null) { notice = a.notice; noticeFrom = a; } });
      var keys = [c.key, Hub.contractKey(c.title)].concat(amendments.map(function (a) { return a.key; }));
      return { c: c, amendments: amendments, notice: notice, noticeFrom: noticeFrom, keys: keys };
    });
  }
  function shortWhat(o) {
    var t = (o.title + ' ' + o.text).toLowerCase();
    if (/non-?renewal/.test(t)) return 'non-renewal notice';
    if (/renewal option|option to renew|exercise[^.]*renew/.test(t)) return 'renewal option closes';
    if (/fee.?increase|price increase/.test(t)) return 'fee-increase notice';
    if (/transition/.test(t)) return 'transition request';
    if (/renew/.test(t)) return 'renewal decision';
    if (/terminat/.test(t)) return 'termination notice';
    if (/change of control/.test(t)) return 'change-of-control notice';
    return Hub.truncate(o.title, 30).toLowerCase();
  }

  function timelineEvents(m) {
    var t = Hub.date.today(), end = Hub.date.addDays(t, HORIZON), evs = [], later = 0, undated = 0;
    var fams = familyOf(m);
    m.open.forEach(function (o) {
      if (o.category.toLowerCase() !== 'notice & renewal') return;
      if (!o.due) { undated++; return; }
      if (o.due > end) { later++; return; }
      evs.push({ kind: o.due < t ? 'past' : 'notice', date: o.due, who: Hub.shortParty(o.counterparty) || 'Contract', what: shortWhat(o), o: o,
        href: Hub.url.disp('OBLIGATIONS', o.id), sub: o.title });
    });
    var brackets = [];
    fams.forEach(function (f) {
      var c = f.c;
      if (!c.expiration || c.expiration < t) return;
      var who = Hub.shortParty(c.counterparty) || c.title;
      if (c.expiration <= end) {
        evs.push({ kind: 'expiry', date: c.expiration, who: who, what: 'contract expires', c: c,
          href: Hub.url.page('Contract360.html', 'contract=' + encodeURIComponent(c.file)), sub: c.title + (/^yes$/i.test(c.autoRenews) ? ' \u00b7 renews automatically' : ' \u00b7 does not auto-renew') });
      }
      if (!/^yes$/i.test(c.autoRenews) || f.notice == null) return;
      var deadline = Hub.date.addDays(c.expiration, -Math.round(f.notice));
      if (deadline > end) return;
      var captured = m.obs.some(function (o) {
        return o.due && o.category.toLowerCase() === 'notice & renewal' && f.keys.indexOf(Hub.contractKey(o.contract)) !== -1 && Math.abs(Hub.date.diff(o.due, deadline)) <= 3;
      });
      if (!captured && deadline >= t) {
        evs.push({ kind: 'derived', date: deadline, who: who, what: 'notice deadline (key terms)', c: c,
          href: Hub.url.page('Contract360.html', 'contract=' + encodeURIComponent(c.file)),
          sub: f.notice + '-day notice before ' + fmt.date(c.expiration) + ' \u2014 not captured as an obligation yet' });
      }
      if (c.expiration <= end) {
        var label = f.notice + '-day notice period';
        if (f.noticeFrom && c.notice != null && c.notice !== f.notice) label += ' (amended from ' + c.notice + ' days)';
        if (deadline < t) label += ' \u00b7 deadline passed ' + fmt.short(deadline);
        brackets.push({ from: deadline < t ? t : deadline, to: c.expiration, label: label, who: who });
      }
    });
    evs.sort(function (a, b) { return a.date - b.date || (a.kind === 'expiry') - (b.kind === 'expiry'); });
    evs.forEach(function (e, i) { e.i = i; });
    return { evs: evs, brackets: brackets, later: later, undated: undated, start: t, end: end };
  }

  function textW(s, size, bold) { return Math.ceil(String(s).length * size * (bold ? 0.58 : 0.53)) + 4; }

  function drawTimeline(tl) {
    var host = Hub.byId('tl-canvas');
    if (!host) return;
    var W = Math.max(680, Math.round((host.clientWidth || 1136)));
    var padL = 24, padR = 24, hasPast = tl.evs.some(function (e) { return e.kind === 'past'; });
    var gutter = hasPast ? 96 : 0, x0 = padL + gutter, x1 = W - padR;
    function X(d) { var n = Hub.date.diff(tl.start, d); return n < 0 ? padL + gutter / 2 - 8 : x0 + (n / HORIZON) * (x1 - x0); }
    var ROW = 44, AXIS = 34, LANE = 28, BR = 30;

    function place(list) {
      var rows = [];
      list.forEach(function (e) {
        var x = X(e.date), w = Math.max(textW(e.who + ' \u00b7 ' + e.what, 12.5, true), textW(fmt.short(e.date) + ' \u00b7 ' + fmt.rel(e.date), 12));
        var anchorEnd = x + w + 10 > W - 8;
        var a = anchorEnd ? x - w - 6 : x - 2, b = anchorEnd ? x + 2 : x + w + 6;
        var r = 0;
        while (rows[r] !== undefined && rows[r] > a - 12) r++;
        rows[r] = b;
        e.x = x; e.row = r; e.anchorEnd = anchorEnd;
      });
      return rows.length;
    }
    var top = tl.evs.filter(function (e) { return e.kind !== 'expiry'; });
    var bottom = tl.evs.filter(function (e) { return e.kind === 'expiry'; });
    var topRows = Math.max(1, place(top)), bottomRows = place(bottom);
    var bRows = [];
    tl.brackets.forEach(function (b) {
      var a = X(b.from), z = X(b.to), lw = textW(b.label, 12), mid = (a + z) / 2;
      var la = Math.max(a, Math.min(mid - lw / 2, z - lw)), lb = la + lw;
      if (lw > z - a) { la = Math.max(8, mid - lw / 2); lb = la + lw; }
      var r = 0;
      while (bRows[r] !== undefined && bRows[r] > Math.min(a, la) - 12) r++;
      bRows[r] = Math.max(z, lb);
      b.a = a; b.z = z; b.row = r; b.lx = Math.max(8, Math.min(la, W - lw - 8));
    });
    var yLabels = AXIS + 12, yLane = yLabels + topRows * ROW + 12, yBr = yLane + LANE + 10;
    var yBottom = yBr + bRows.length * BR + (bRows.length ? 6 : 0), H = yBottom + bottomRows * ROW + 12;
    var laneMid = yLane + LANE / 2;
    var out = [];
    out.push('<svg class="tl-svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-labelledby="tl-svg-title"><title id="tl-svg-title">Timeline of ' +
      plural(tl.evs.length, 'date') + ' in the next ' + HORIZON + ' days. The same dates are listed below in order.</title>');
    out.push('<defs><linearGradient id="tl-lane" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#9AC7F5" stop-opacity=".55"/><stop offset=".55" stop-color="#EAF3FC" stop-opacity="1"/><stop offset="1" stop-color="#8B83DB" stop-opacity=".30"/></linearGradient></defs>');
    // month grid + axis labels
    var m0 = new Date(tl.start.getFullYear(), tl.start.getMonth() + 1, 1);
    for (var d = m0; d <= tl.end; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) {
      var x = X(d);
      out.push('<line x1="' + x + '" x2="' + x + '" y1="' + (AXIS - 6) + '" y2="' + (H - 8) + '" stroke="#E4EAF1" stroke-width="1"/>');
      if (x < x1 - 30 && x - x0 > 48) out.push('<text class="t-axis" x="' + (x + 6) + '" y="' + (AXIS - 12) + '">' + esc(fmt.month(d, d.getMonth() === 0)) + '</text>');
    }
    if (hasPast) out.push('<text class="t-axis" x="' + padL + '" y="' + (AXIS - 12) + '">Past due</text>');
    // lane
    out.push('<rect x="' + x0 + '" y="' + yLane + '" width="' + (x1 - x0) + '" height="' + LANE + '" rx="' + LANE / 2 + '" fill="url(#tl-lane)"/>');
    out.push('<rect x="' + x0 + '" y="' + yLane + '" width="' + Math.max(LANE, X(Hub.date.addDays(tl.start, SOON)) - x0) + '" height="' + LANE + '" rx="' + LANE / 2 + '" fill="#9AC7F5" fill-opacity=".45"><title>Next 14 days</title></rect>');
    if (hasPast) out.push('<rect x="' + padL + '" y="' + yLane + '" width="' + (gutter - 16) + '" height="' + LANE + '" rx="' + LANE / 2 + '" fill="#FBEAEF" stroke="#C25A7C" stroke-dasharray="3 3"/>');
    // today
    out.push('<line x1="' + x0 + '" x2="' + x0 + '" y1="' + (AXIS - 22) + '" y2="' + (H - 8) + '" stroke="#111827" stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round"/>');
    out.push('<text class="t-today" x="' + (x0 + 6) + '" y="' + (AXIS - 12) + '">Today</text>');
    // brackets
    tl.brackets.forEach(function (b) {
      var y = yBr + b.row * BR;
      out.push('<g class="tl-bracket"><path d="M' + b.a + ' ' + (y + 12) + 'v8M' + b.a + ' ' + (y + 16) + 'H' + b.z + 'M' + b.z + ' ' + (y + 12) + 'v8" stroke="#3F3891" stroke-width="1.4" fill="none" stroke-linecap="round"/>' +
        '<rect x="' + (b.lx - 4) + '" y="' + (y - 4) + '" width="' + (textW(b.label, 12) + 8) + '" height="17" rx="4" fill="#FFFFFF" fill-opacity=".92"/>' +
        '<text class="t-bracket" x="' + b.lx + '" y="' + (y + 9) + '">' + esc(b.who + ' \u00b7 ' + b.label) + '</text></g>');
    });
    // events
    function label(e, yTop) {
      var tx = e.anchorEnd ? e.x - 6 : e.x + 6, anchor = e.anchorEnd ? ' text-anchor="end"' : '';
      return '<text class="t-name" x="' + tx + '" y="' + (yTop + 14) + '"' + anchor + '>' + esc(e.who + ' \u00b7 ' + e.what) + '</text>' +
        '<text class="t-date" x="' + tx + '" y="' + (yTop + 31) + '"' + anchor + '>' + esc(fmt.short(e.date) + ' \u00b7 ' + (e.kind === 'past' ? fmt.due(e.date) : fmt.rel(e.date))) + '</text>';
    }
    function mark(e, cy) {
      var x = e.x;
      if (e.kind === 'expiry') return '<g class="tl-mark"><circle cx="' + x + '" cy="' + cy + '" r="6" fill="#FFFFFF" stroke="#111827" stroke-width="2"/><circle cx="' + x + '" cy="' + cy + '" r="2" fill="#111827"/></g>';
      var p = 'M' + x + ' ' + (cy - 7) + 'L' + (x + 7) + ' ' + cy + 'L' + x + ' ' + (cy + 7) + 'L' + (x - 7) + ' ' + cy + 'Z';
      if (e.kind === 'derived') return '<path class="tl-mark" d="' + p + '" fill="#FFFFFF" stroke="#3F3891" stroke-width="1.5" stroke-dasharray="2.5 2"/>';
      if (e.kind === 'past') return '<path class="tl-mark" d="' + p + '" fill="#C25A7C" stroke="#8A1C3F" stroke-width="1.5"/>';
      return '<path class="tl-mark" d="' + p + '" fill="#8B83DB" stroke="#111827" stroke-width="1.4"/>';
    }
    top.forEach(function (e) {
      var yT = yLabels + (topRows - 1 - e.row) * ROW, cy = laneMid - 6;
      out.push('<g class="tl-ev" data-ev="' + e.i + '"><title>' + esc(e.who + ' \u00b7 ' + e.what + ' \u2014 ' + fmt.date(e.date)) + '</title>' +
        '<line class="tl-lead" x1="' + e.x + '" x2="' + e.x + '" y1="' + (yT + 2) + '" y2="' + (cy - 8) + '" stroke="#111827" stroke-opacity=".28"/>' +
        label(e, yT) + mark(e, cy) + '</g>');
    });
    bottom.forEach(function (e) {
      var yT = yBottom + e.row * ROW, cy = laneMid + 6;
      out.push('<g class="tl-ev" data-ev="' + e.i + '"><title>' + esc(e.who + ' \u00b7 ' + e.what + ' \u2014 ' + fmt.date(e.date)) + '</title>' +
        '<line class="tl-lead" x1="' + e.x + '" x2="' + e.x + '" y1="' + (cy + 8) + '" y2="' + (yT + 2) + '" stroke="#111827" stroke-opacity=".28"/>' +
        label(e, yT) + mark(e, cy) + '</g>');
    });
    if (!tl.evs.length) {
      out.push('<text class="t-empty" x="' + (x0 + 16) + '" y="' + (yLane - 14) + '">No notice deadlines or contract expiries in the next ' + HORIZON + ' days.</text>');
    }
    out.push('</svg>');
    host.innerHTML = out.join('');
  }

  var KIND = {
    notice: function () { return Hub.pill('review', 'Notice deadline', 'diamond'); },
    past: function () { return Hub.pill('overdue', 'Past due', 'overdue'); },
    expiry: function () { return Hub.pill('quiet', 'Contract expires', 'ring'); },
    derived: function () { return Hub.pill('empty', 'From key terms', 'dashed'); }
  };
  function renderTimelineList(tl) {
    var ld = Hub.byId('legend-derived'), lp = Hub.byId('legend-past');
    if (ld) ld.hidden = !tl.evs.some(function (e) { return e.kind === 'derived'; });
    if (lp) lp.hidden = !tl.evs.some(function (e) { return e.kind === 'past'; });
    var list = Hub.byId('tl-list');
    if (!list) return;
    if (!tl.evs.length) {
      list.innerHTML = '<li class="state state--inline"><p>Nothing in the next ' + HORIZON + ' days. Notice and renewal obligations, and contract expiry dates from the Contracts library, appear here as they come into range.</p></li>';
    } else {
      list.innerHTML = tl.evs.map(function (e) {
        var subBits = [e.sub, e.kind === 'past' ? fmt.due(e.date) : fmt.rel(e.date)];
        if (e.o) subBits.push(e.o.owner || 'No owner');
        return '<li class="tl-item" data-ev="' + e.i + '">' +
          '<time class="tl-item__date" datetime="' + fmt.iso(e.date) + '"><span class="tl-item__day">' + e.date.getDate() + '</span><span class="tl-item__mon">' + esc(fmt.month(e.date)) + '</span><span class="sr-only"> ' + e.date.getFullYear() + '</span></time>' +
          '<div><a class="tl-item__title" href="' + esc(e.href) + '" target="_top">' + esc(e.who + ' \u00b7 ' + e.what) + '</a>' +
          '<span class="tl-item__sub">' + esc(subBits.filter(Boolean).join(' \u00b7 ')) + '</span></div>' + KIND[e.kind]() + '</li>';
      }).join('');
    }
    var foot = [];
    if (tl.undated === 1) foot.push('1 notice obligation is triggered by an event and has no date.');
    else if (tl.undated) foot.push(tl.undated + ' notice obligations are triggered by events and have no date (for example, a change of control).');
    if (tl.later) foot.push(plural(tl.later, 'more notice date falls', 'more notice dates fall') + ' after ' + fmt.date(tl.end) + '.');
    var f = Hub.byId('tl-foot');
    if (f) f.innerHTML = foot.length ? esc(foot.join(' ')) + ' <a href="' + esc(Hub.url.view('OBLIGATIONS', [['Category', 'Notice & renewal']])) + '" target="_top">See every notice obligation</a>' : '';
  }
  function wireTimelineHover() {
    var list = Hub.byId('tl-list');
    if (!list || list.__wired) return;
    list.__wired = true;
    function hot(e, on) {
      var li = Hub.closest(e.target, '[data-ev]');
      var svg = document.querySelector ? document.querySelector('.tl-svg') : null;
      if (!svg) return;
      Array.prototype.forEach.call(svg.querySelectorAll('.tl-ev.is-hot'), function (g) { g.classList.remove('is-hot'); });
      if (on && li) { var g = svg.querySelector('.tl-ev[data-ev="' + li.getAttribute('data-ev') + '"]'); if (g) g.classList.add('is-hot'); }
    }
    list.addEventListener('mouseover', function (e) { hot(e, true); });
    list.addEventListener('focusin', function (e) { hot(e, true); });
    list.addEventListener('mouseleave', function (e) { hot(e, false); });
    list.addEventListener('focusout', function (e) { hot(e, false); });
  }

  /* ---------- due next ---------- */
  function renderDueNext(m) {
    var rows = m.open.filter(function (o) { return o.due; }).sort(Hub.byDue).slice(0, 10);
    if (!rows.length) {
      Hub.setHTML('due-table', '<div class="state"><svg viewBox="0 0 120 96" aria-hidden="true"><rect x="22" y="18" width="76" height="60" rx="10" fill="#EAF3FC"/><path d="M36 38h48M36 50h34M36 62h40" stroke="#9AC7F5" stroke-width="4" stroke-linecap="round"/></svg>' +
        '<h3>No dated obligations are open</h3><p>' + (m.obs.length ? 'Everything open is event-driven or ongoing.' : 'Obligations appear here after capture runs on a contract.') + '</p></div>');
      return;
    }
    var html = '<table class="table table--stack due-next"><caption class="sr-only">Next ' + rows.length + ' open obligations by due date</caption>' +
      '<colgroup><col class="c-due"><col><col class="c-cp"><col class="c-owner"><col class="c-timing"><col class="c-clause"></colgroup><thead><tr>' +
      '<th scope="col">Due</th><th scope="col">Obligation</th><th scope="col">Counterparty</th><th scope="col">Owner</th><th scope="col">Timing</th><th scope="col">Clause</th></tr></thead><tbody>';
    html += rows.map(function (o) {
      return '<tr><td data-label="Due" class="due-date"><span><strong>' + esc(fmt.short(o.due)) + '</strong><span class="cell-sub">' + esc(fmt.due(o.due)) + '</span></span></td>' +
        '<td class="cell-lead"><a class="cell-title" href="' + esc(Hub.url.disp('OBLIGATIONS', o.id)) + '" target="_top">' + esc(o.title) + '</a></td>' +
        '<td data-label="Counterparty">' + esc(o.counterparty || '\u2014') + '</td>' +
        '<td data-label="Owner">' + Hub.ownerText(o) + '</td>' +
        '<td data-label="Timing"><span>' + Hub.timingPill(o.timing) + Hub.timingNote(o) + '</span></td>' +
        '<td data-label="Clause" class="muted">' + esc(o.clause || '\u2014') + '</td></tr>';
    }).join('');
    Hub.setHTML('due-table', html + '</tbody></table>');
    var all = Hub.byId('due-all');
    if (all) all.setAttribute('href', Hub.url.view('OBLIGATIONS', [['Status', ['Not started', 'In progress']]]));
  }

  /* ---------- workflow health ---------- */
  function renderHealth(m) {
    var last = Hub.lastRuns(m.runs);
    var issues = last.filter(function (l) { return l.issue; });
    var html = '';
    if (issues.length) {
      html += '<div class="wf-issues">' + issues.map(function (l) {
        return '<p class="notice' + (l.issue.level === 'rose' ? ' notice--rose' : '') + '"><svg aria-hidden="true"><use href="#i-warn"></use></svg><span>' + esc(l.issue.text) +
          ' <a href="' + esc(Hub.url.view('RUNLOG', [['Workflow', l.wf.name]])) + '" target="_top">See its runs</a> or check the workflow in <a href="' + esc(Hub.url.page('Settings.html')) + '" target="_top">Settings</a>.</span></p>';
      }).join('') + '</div>';
    } else if (m.runs.length) {
      html += '<p class="wf-ok">' + Hub.pill('ok', 'Running normally', 'check') + '</p>';
    }
    html += '<ul class="wf-list">' + last.map(function (l) {
      var r = l.last;
      return '<li><div><span class="wf-name">' + esc(l.wf.label) + '</span><span class="wf-when">' + esc(l.wf.trigger) + '</span></div>' +
        '<div class="wf-right">' + Hub.outcomePill(r ? r.outcome : '') +
        '<span class="wf-ago">' + (r && r.at ? '<time datetime="' + esc(r.at.toISOString()) + '" title="' + esc(fmt.dateTime(r.at)) + '">' + esc(fmt.ago(r.at)) + '</time>' : 'No runs logged') + '</span></div></li>';
    }).join('') + '</ul>';
    if (!m.runs.length) html = '<p class="muted" style="margin-bottom:16px">No runs logged yet. Each workflow writes a row to the Run Log when it runs.</p>' + html;
    Hub.setHTML('health', html);
  }

  /* ---------- get set up ---------- */
  function renderSetup(m) {
    var steps = [
      { done: m.rules.length > 0, title: 'Add owner routing rules', sub: m.rules.length ? plural(m.rules.length, 'rule') + ' in Obligation Owners' : 'Tell Assign owners who looks after each category.', href: Hub.url.view('OWNERS'), link: 'Open Obligation Owners' },
      { done: m.contracts.length > 0, title: 'Add at least one contract', sub: m.contracts.length ? plural(m.contracts.length, 'file') + ' in Contracts' : 'Upload a signed contract to the Contracts library.', href: Hub.url.view('CONTRACTS'), link: 'Open Contracts' },
      { done: m.runs.some(function (r) { return /^capture/i.test(r.workflow); }), title: 'Capture has run', sub: 'Runs when a contract is added or changed.', href: Hub.url.view('RUNLOG', [['Workflow', 'Capture']]), link: 'See capture runs' },
      { done: m.runs.some(function (r) { return /daily\s*sweep/i.test(r.workflow); }), title: 'Daily sweep has run', sub: 'Updates timing and sends reminders each morning.', href: Hub.url.page('Settings.html'), link: 'Check workflows' }
    ];
    var card = Hub.byId('setup-card');
    var left = steps.filter(function (s) { return !s.done; }).length;
    if (card) card.hidden = left === 0;
    if (!left) return;
    Hub.setHTML('setup-sub', esc((steps.length - left) + ' of ' + steps.length + ' done. A few steps before obligations flow in on their own.'));
    Hub.setHTML('setup', steps.map(function (s) {
      return '<li class="' + (s.done ? 'is-done' : 'is-todo') + '"><svg aria-hidden="true"><use href="#i-' + (s.done ? 'tick' : 'upcoming') + '"></use></svg>' +
        '<div><span class="step-title">' + esc(s.title) + '<span class="sr-only">' + (s.done ? ' (done)' : ' (to do)') + '</span></span><span class="step-sub">' + esc(s.sub) +
        ' <a href="' + esc(s.href) + '" target="_top">' + esc(s.link) + '</a></span></div></li>';
    }).join(''));
  }

  function tuneQuestions(m) {
    var names = Hub.uniq(m.open.map(function (o) { return Hub.shortParty(o.counterparty); }).filter(Boolean));
    if (!names.length || names.some(function (n) { return /contoso/i.test(n); })) return;
    var counts = {};
    m.open.forEach(function (o) { var k = Hub.shortParty(o.counterparty); if (k) counts[k] = (counts[k] || 0) + 1; });
    names.sort(function (a, b) { return counts[b] - counts[a]; });
    var q = 'What do we owe ' + names[0] + ' this quarter?';
    var chips = document.querySelectorAll ? document.querySelectorAll('.chip[data-copy]') : [];
    Array.prototype.forEach.call(chips, function (c) {
      if (/contoso/i.test(c.getAttribute('data-copy'))) { c.setAttribute('data-copy', q); var tx = c.querySelector('.chip__text'); if (tx) tx.textContent = q; }
    });
  }

  function render(data) {
    model = prepare(data);
    model.tl = timelineEvents(model);
    renderHero(model);
    renderKpis(model);
    drawTimeline(model.tl);
    renderTimelineList(model.tl);
    wireTimelineHover();
    renderDueNext(model);
    renderHealth(model);
    renderSetup(model);
    tuneQuestions(model);
  }

  Hub.start({
    lists: ['OBLIGATIONS', 'CONTRACTS', 'RUNLOG', 'OWNERS'],
    render: render,
    onResize: function () { if (model) drawTimeline(model.tl); }
  });
})(window.Hub);
