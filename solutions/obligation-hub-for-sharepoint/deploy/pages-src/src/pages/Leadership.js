/* Leadership - exposure view. Only counts that come straight from the Obligations list; no invented metrics. */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, icon = Hub.icon, plural = Hub.plural;
  var BAR = '#5A87C2', BAR_HI = '#3F3891', TRACK = '#E8EFF7';

  function countBy(list, fn) {
    var m = {};
    list.forEach(function (o) { var k = fn(o) || 'Not set'; m[k] = (m[k] || 0) + 1; });
    return Object.keys(m).map(function (k) { return { key: k, n: m[k] }; }).sort(function (a, b) { return b.n - a.n || a.key.localeCompare(b.key); });
  }
  function barSvg(n, hi, max) {
    var w = max ? (n / max) * 100 : 0, wh = max ? (hi / max) * 100 : 0;
    var grid = [25, 50, 75].map(function (g) { return '<line x1="' + g + '" x2="' + g + '" y1="0" y2="14" stroke="#FFFFFF" stroke-width=".6" vector-effect="non-scaling-stroke"/>'; }).join('');
    return '<svg viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true" focusable="false">' +
      '<rect x="0" y="2" width="100" height="10" rx="0" fill="' + TRACK + '"/>' +
      '<rect x="0" y="2" width="' + w.toFixed(2) + '" height="10" fill="' + BAR + '"/>' +
      (hi ? '<rect x="0" y="2" width="' + wh.toFixed(2) + '" height="10" fill="' + BAR_HI + '"/>' : '') + grid + '</svg>';
  }
  function barTable(id, caption, head, rows, max) {
    return '<table class="bars" id="' + id + '"><caption>' + esc(caption) + '</caption><thead><tr><th scope="col">' + esc(head) + '</th><th scope="col" class="num">Open</th><th scope="col"><span class="sr-only">Chart: high-risk part in dark, the rest in light blue</span></th></tr></thead><tbody>' +
      rows.map(function (r) {
        return '<tr><th scope="row">' + esc(r.key) + '<span class="sub">' + (r.hi ? r.hi + ' high risk' : 'none high risk') + '</span></th><td class="num">' + r.n + '</td><td class="bar">' + barSvg(r.n, r.hi, max) + '</td></tr>';
      }).join('') + '</tbody></table>';
  }
  function sw(color, stroke) { return '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x=".5" y=".5" width="11" height="11" rx="3" fill="' + color + '"' + (stroke ? ' stroke="' + stroke + '"' : '') + '/></svg>'; }

  function render(data) {
    var all = data.OBLIGATIONS.rows.map(Hub.model.obligation);
    var open = all.filter(function (o) { return !o.closed; });
    var t = Hub.date.today();
    Hub.badge(data, 'OBLIGATIONS', all.length, 'obligation');
    var host = Hub.byId('lead');
    if (host) host.setAttribute('aria-busy', 'false');
    if (!all.length) {
      Hub.setHTML('page-sub', 'Nothing to report yet.');
      Hub.setHTML('lead', '<div class="section card state"><svg viewBox="0 0 120 96" aria-hidden="true"><rect x="20" y="58" width="16" height="22" rx="4" fill="#EAF3FC"/><rect x="44" y="40" width="16" height="40" rx="4" fill="#9AC7F5" opacity=".6"/><rect x="68" y="26" width="16" height="54" rx="4" fill="#8B83DB" opacity=".45"/><path d="M14 84h92" stroke="#D3DDE9" stroke-width="2"/></svg>' +
        '<h2>No obligations to report</h2><p>Exposure figures appear once contracts are added and capture has created obligations.</p></div>');
      return;
    }
    var isHigh = function (o) { return /high/i.test(o.risk); };
    var highOpen = open.filter(isHigh);
    var overdue = open.filter(function (o) { return o.timing === 'Overdue'; });
    var contracts = Hub.uniq(open.map(function (o) { return Hub.contractKey(o.contract); }).filter(Boolean)).length;
    var byStatus = {
      notStarted: open.filter(function (o) { return o.status !== 'In progress'; }).length,
      inProgress: open.filter(function (o) { return o.status === 'In progress'; }).length,
      fulfilled: all.filter(function (o) { return /fulfilled/i.test(o.status); }).length,
      other: all.filter(function (o) { return o.closed && !/fulfilled/i.test(o.status); }).length
    };
    Hub.setHTML('page-sub', esc(plural(open.length, 'open obligation') + ' across ' + plural(contracts, 'contract') + '; ' + highOpen.length + ' of them high risk and ' + overdue.length + ' overdue today.'));

    var html = '';
    // headline figures
    var stats = [
      ['Open', open.length, plural(byStatus.inProgress, 'item') + ' in progress'],
      ['Fulfilled', byStatus.fulfilled, byStatus.other ? byStatus.other + ' waived or not applicable' : 'Marked fulfilled in the list'],
      ['High-risk open', highOpen.length, highOpen.filter(function (o) { return o.timing === 'Overdue' || o.timing === 'Due soon'; }).length + ' due within 14 days or overdue'],
      ['Overdue today', overdue.length, overdue.length ? 'Oldest ' + fmt.due(overdue.slice().sort(Hub.byDue)[0].due) : 'Nothing past due']
    ];
    html += '<section class="section" aria-labelledby="s-title"><h2 class="sr-only" id="s-title">Headline figures</h2><div class="stats">' + stats.map(function (s, i) {
      return '<div class="card stat settle" style="--d:' + i + '"><span class="stat__label">' + esc(s[0]) + '</span><span class="stat__value">' + s[1] + '</span><span class="stat__note">' + esc(s[2]) + '</span></div>';
    }).join('') + '</div></section>';

    // what the risk levels mean (the legend for every High / Medium or low split below)
    html += '<section class="section card card--tint risk-key settle" aria-labelledby="rk-title"><h2 id="rk-title">What the risk levels mean</h2>' +
      '<dl class="risk-key__list">' + Hub.RISK_LEVELS.map(function (r) {
        return '<div><dt>' + sw(r.level === 'High' ? BAR_HI : BAR) + esc(r.level) + '</dt><dd>' + esc(r.text) + '</dd></div>';
      }).join('') + '</dl><p class="risk-key__note">Charts show High in dark and Medium and Low together in light blue. Change an item\u2019s Risk in the Obligations list if it doesn\u2019t fit.</p></section>';

    // open vs fulfilled
    var total = open.length + byStatus.fulfilled + byStatus.other;
    var segs = [['Not started', byStatus.notStarted, '#5A87C2'], ['In progress', byStatus.inProgress, '#8B83DB'], ['Fulfilled', byStatus.fulfilled, '#2F7A5C'], ['Waived or not applicable', byStatus.other, '#9CA3AF']];
    var x = 0, rects = segs.map(function (s) { var w = total ? s[1] / total * 100 : 0, r = '<rect x="' + x.toFixed(2) + '" y="0" width="' + Math.max(0, w - (w ? .4 : 0)).toFixed(2) + '" height="16" fill="' + s[2] + '"/>'; x += w; return r; }).join('');
    var openCard = '<section class="card settle" aria-labelledby="ovf-title"><h2 id="ovf-title">Open vs fulfilled</h2><p class="muted" style="font-size:14px;margin-top:2px">Every tracked obligation by status.</p>' +
      '<svg class="split" viewBox="0 0 100 16" preserveAspectRatio="none" aria-hidden="true"><clipPath id="split-c"><rect width="100" height="16" rx="3"/></clipPath><g clip-path="url(#split-c)"><rect width="100" height="16" fill="' + TRACK + '"/>' + rects + '</g></svg>' +
      '<ul class="legend">' + segs.filter(function (s) { return s[1]; }).map(function (s) { return '<li>' + sw(s[2]) + '<span>' + esc(s[0]) + ' <strong>' + s[1] + '</strong></span></li>'; }).join('') + '</ul></section>';

    // we owe vs owed to us
    var party = { Us: 0, Counterparty: 0, Both: 0 };
    open.forEach(function (o) { if (party[o.party] !== undefined) party[o.party]++; });
    var oweCard = '<section class="card settle" style="--d:1" aria-labelledby="owe-title"><h2 id="owe-title">What we owe vs what we\u2019re owed</h2><p class="muted" style="font-size:14px;margin-top:2px">Open obligations by who owes them.</p>' +
      '<div class="owe"><div><strong>' + party.Us + '</strong><span>We owe</span></div><div><strong>' + party.Counterparty + '</strong><span>Owed to us</span></div><div><strong>' + party.Both + '</strong><span>Mutual</span></div></div></section>';
    html += '<div class="section grid-2">' + openCard + oweCard + '</div>';

    // category + counterparty bars
    var cats = countBy(open, function (o) { return o.category; });
    cats.forEach(function (c) { c.hi = open.filter(function (o) { return (o.category || 'Not set') === c.key && isHigh(o); }).length; });
    var cps = countBy(open, function (o) { return Hub.shortParty(o.counterparty); });
    cps.forEach(function (c) { c.hi = open.filter(function (o) { return (Hub.shortParty(o.counterparty) || 'Not set') === c.key && isHigh(o); }).length; });
    var max = Math.max.apply(null, cats.concat(cps).map(function (c) { return c.n; }).concat([1]));
    var key = '<ul class="legend" style="margin:0 0 8px">' + '<li>' + sw(BAR_HI) + 'High risk</li><li>' + sw(BAR) + 'Medium or low risk</li></ul>';
    html += '<div class="section grid-2">' +
      '<section class="card settle" aria-labelledby="cat-title"><div class="card__head"><div><h2 id="cat-title">By category</h2></div><a class="link-arrow" href="' + esc(Hub.url.view('OBLIGATIONS')) + '" target="_top">Open list' + icon('arrow') + '</a></div>' + key +
      barTable('t-cat', 'Open obligations by category, with how many are high risk.', 'Category', cats, max) + '</section>' +
      '<section class="card settle" style="--d:1" aria-labelledby="cp-title"><div class="card__head"><div><h2 id="cp-title">By counterparty</h2></div></div>' + key +
      barTable('t-cp', 'Open obligations by counterparty, with how many are high risk.', 'Counterparty', cps, max) + '</section></div>';

    // next 90 days by month
    var end = Hub.date.addDays(t, 90), buckets = [];
    for (var d = new Date(t.getFullYear(), t.getMonth(), 1); d <= end; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) {
      var from = d < t ? t : d, last = new Date(d.getFullYear(), d.getMonth() + 1, 0), to = last > end ? end : last;
      var n = open.filter(function (o) { return o.due && o.due >= from && o.due <= to; });
      buckets.push({ label: fmt.month(d, d.getMonth() === 0 || buckets.length === 0), range: from.getDate() + '\u2013' + to.getDate(), partial: from.getDate() !== 1 || to.getDate() !== last.getDate(), n: n.length, hi: n.filter(isHigh).length });
    }
    var mmax = Math.max.apply(null, buckets.map(function (b) { return b.n; }).concat([1]));
    var monthCard = '<section class="card settle" aria-labelledby="m-title"><h2 id="m-title" class="card__head">Next 90 days by month</h2>' +
      '<table class="months"><caption>Open obligations due from today to ' + esc(fmt.date(end)) + '. Overdue items are not included.</caption><thead><tr>' + buckets.map(function (b) { return '<th scope="col">' + esc(b.label) + '<small>' + esc(b.partial ? 'Days ' + b.range : 'Whole month') + '</small></th>'; }).join('') + '</tr></thead><tbody><tr>' +
      buckets.map(function (b) {
        var h = Math.round(b.n / mmax * 100), hh = Math.round(b.hi / mmax * 100);
        return '<td><span>' + b.n + '</span><svg viewBox="0 0 40 100" preserveAspectRatio="none" aria-hidden="true"><rect x="0" y="0" width="40" height="100" rx="4" fill="' + TRACK + '"/>' +
          (h ? '<rect x="0" y="' + (100 - h) + '" width="40" height="' + h + '" rx="4" fill="' + BAR + '"/>' : '') + (hh ? '<rect x="0" y="' + (100 - hh) + '" width="40" height="' + hh + '" rx="4" fill="' + BAR_HI + '"/>' : '') + '</svg>' +
          '<span class="sr-only"> due, ' + b.hi + ' high risk</span></td>';
      }).join('') + '</tr></tbody></table>' +
      '<ul class="legend"><li>' + sw(BAR_HI) + 'High risk</li><li>' + sw(BAR) + 'Medium or low risk</li></ul></section>';

    // no history note
    var histCard = '<section class="card card--tint settle" style="--d:1" aria-labelledby="hist-title"><h2 id="hist-title" class="card__head">Trend over time</h2>' +
      '<p class="nohist"><svg aria-hidden="true"><use href="#i-pulse"></use></svg><span>Not shown. The Obligations list keeps each item\u2019s current state only, so there is no history to chart an overdue trend from. The Leadership digest each Friday is the record of how things stood that week.</span></p></section>';
    html += '<div class="section grid-2">' + monthCard + histCard + '</div>';

    // high-risk list
    var hiList = highOpen.slice().sort(Hub.byDue);
    html += '<section class="section card card--flush settle" aria-labelledby="hr-title"><div class="card__head pad"><div><h2 id="hr-title">High-risk open items</h2><p>' + plural(hiList.length, 'item') + ', soonest first.</p></div>' +
      '<a class="link-arrow" href="' + esc(Hub.url.view('OBLIGATIONS', [['Risk', 'High']])) + '" target="_top">Open in list' + icon('arrow') + '</a></div>' +
      (hiList.length ? '<div class="table-wrap"><table class="table table--stack"><caption class="sr-only">High-risk open obligations</caption><thead><tr><th scope="col">Due</th><th scope="col">Obligation</th><th scope="col">Counterparty</th><th scope="col">Owner</th><th scope="col">Timing</th></tr></thead><tbody>' +
        hiList.map(function (o) {
          return '<tr><td data-label="Due" class="nowrap">' + (o.due ? '<strong>' + esc(fmt.short(o.due)) + '</strong>' : '<span class="muted">' + esc(o.triggerType === 'Ongoing' ? 'Ongoing' : 'On trigger') + '</span>') + '</td>' +
            '<td class="cell-lead"><a class="cell-title" href="' + esc(Hub.url.disp('OBLIGATIONS', o.id)) + '" target="_top">' + esc(o.title) + '</a><span class="cell-sub">' + esc(o.category) + '</span></td>' +
            '<td data-label="Counterparty">' + esc(o.counterparty || '\u2014') + '</td><td data-label="Owner">' + Hub.ownerText(o) + '</td><td data-label="Timing"><span>' + Hub.timingPill(o.timing) + Hub.timingNote(o) + '</span></td></tr>';
        }).join('') + '</tbody></table></div>' : '<div class="pad" style="padding-bottom:24px"><p class="muted">No high-risk obligations are open.</p></div>') + '</section>';

    Hub.setHTML('lead', html);
  }

  Hub.start({ lists: ['OBLIGATIONS'], render: render });
})(window.Hub);
