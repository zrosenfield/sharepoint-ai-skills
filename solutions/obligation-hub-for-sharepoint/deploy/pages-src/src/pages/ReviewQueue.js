/* Review queue */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, icon = Hub.icon, plural = Hub.plural;
  var RANK = { low: 0, medium: 1, high: 2 };
  var FILTERS = [{ key: 'all', label: 'All' }, { key: 'low', label: 'Low confidence' }, { key: 'medium', label: 'Medium' }];

  function confidence(c) {
    var k = (c || '').toLowerCase(), n = k in RANK ? RANK[k] + 1 : 0;
    return '<span class="conf"><span class="conf__meter" aria-hidden="true"><i class="' + (n >= 1 ? 'on' : '') + '"></i><i class="' + (n >= 2 ? 'on' : '') + '"></i><i class="' + (n >= 3 ? 'on' : '') + '"></i></span>' +
      '<span>Confidence: <strong>' + esc(c || 'Not set') + '</strong></span></span>';
  }

  function item(o) {
    var id = esc(o.id || Math.random().toString(36).slice(2));
    var when = o.due ? fmt.date(o.due) + ' (' + fmt.due(o.due) + ')' : (o.triggerEvent || (o.triggerType === 'Ongoing' ? 'Ongoing \u2014 no date' : 'No date'));
    var captured = [['Who owes it', o.party], ['Category', o.category], ['Trigger', [o.triggerType, o.recurrence && o.recurrence !== 'None' ? o.recurrence : ''].filter(Boolean).join(' \u00b7 ')], [o.due ? 'Due' : 'When', when]];
    return '<li><article class="card rq-item" aria-labelledby="rq-' + id + '">' +
      '<div><h3 class="rq-item__title" id="rq-' + id + '">' + esc(o.title) + '</h3>' +
      '<p class="rq-item__who">' + esc([o.counterparty, o.contract].filter(Boolean).join(' \u00b7 ')) + '</p>' +
      '<div class="pills">' + confidence(o.confidence) + Hub.riskPill(o.risk) + '</div>' +
      '<div class="rq-why"><strong>Why it was held</strong>' + esc(o.notes || 'Capture didn\u2019t record a reason. Check the clause and the captured fields.') + '</div>' +
      '<dl class="rq-captured">' + captured.map(function (c) { return '<div><dt>' + c[0] + '</dt><dd>' + esc(c[1] || '\u2014') + '</dd></div>'; }).join('') + '</dl></div>' +
      '<div class="rq-clause"><h4>Clause' + (o.clause ? ' \u00b7 ' + esc(o.clause) : '') + '</h4>' +
      (o.source ? '<blockquote class="quote">' + esc(o.source) + '</blockquote>' : '<p class="muted" style="margin-top:8px">No clause text was stored. Open the contract to check it.</p>') +
      (o.text ? '<p class="muted" style="margin-top:12px;font-size:14px"><strong>Captured as:</strong> ' + esc(o.text) + '</p>' : '') + '</div>' +
      '<div class="rq-actions">' +
      '<a class="btn btn--sm btn--primary" href="' + esc(Hub.url.edit('OBLIGATIONS', o.id, 'ReviewQueue.html')) + '" target="_top">' + icon('tick') + 'Accept<span class="sr-only">: ' + esc(o.title) + '</span></a>' +
      '<a class="btn btn--sm" href="' + esc(Hub.url.edit('OBLIGATIONS', o.id, 'ReviewQueue.html')) + '" target="_top">' + icon('edit') + 'Edit<span class="sr-only">: ' + esc(o.title) + '</span></a>' +
      '<span class="hint"><a class="btn btn--sm" href="' + esc(Hub.url.disp('OBLIGATIONS', o.id)) + '" target="_top" aria-describedby="tip-x-' + id + '">' + icon('block') + 'Exclude<span class="sr-only">: ' + esc(o.title) + '</span></a>' +
      '<span class="hint__text" role="tooltip" id="tip-x-' + id + '">Opens the item in the Obligations list. Select it and use the Remove obligation quick step \u2014 it takes the obligation out of tracking and records the clause in Exclusions so capture won\u2019t add it back.</span></span>' +
      '</div></article></li>';
  }

  function render(data, hash) {
    var all = data.OBLIGATIONS.rows.map(Hub.model.obligation);
    var queue = all.filter(function (o) { return /needs review/i.test(o.review); });
    queue.sort(function (a, b) {
      var ra = RANK[(a.confidence || '').toLowerCase()], rb = RANK[(b.confidence || '').toLowerCase()];
      ra = ra === undefined ? -1 : ra; rb = rb === undefined ? -1 : rb;
      return ra - rb || Hub.byDue(a, b);
    });
    Hub.badge(data, 'OBLIGATIONS', all.length, 'obligation');
    var f = FILTERS.some(function (x) { return x.key === hash.confidence; }) ? hash.confidence : 'all';
    var counts = { all: queue.length };
    FILTERS.forEach(function (x) { if (x.key !== 'all') counts[x.key] = queue.filter(function (o) { return (o.confidence || '').toLowerCase() === x.key; }).length; });
    var seg = Hub.byId('seg');
    if (seg) {
      seg.hidden = !queue.length;
      seg.innerHTML = FILTERS.map(function (x) {
        return '<a class="seg__opt" data-focus="seg-' + x.key + '" href="' + (x.key === 'all' ? '#confidence=all' : Hub.hash.href({ confidence: x.key })) + '"' + (x.key === f ? ' aria-current="true"' : '') + '>' + esc(x.label) + ' <span class="seg__n">' + counts[x.key] + '</span></a>';
      }).join('');
    }
    Hub.setHTML('page-sub', esc(queue.length ? plural(queue.length, 'item is', 'items are') + ' waiting. Capture holds anything it isn\u2019t sure about \u2014 check the clause, then accept, edit or exclude each one.'
      : 'Capture holds anything it isn\u2019t sure about. When it does, the items appear here.'));
    var list = f === 'all' ? queue : queue.filter(function (o) { return (o.confidence || '').toLowerCase() === f; });
    var host = Hub.byId('queue');
    if (host) host.setAttribute('aria-busy', 'false');
    if (!queue.length) {
      Hub.setHTML('queue', '<div class="card state">' +
        '<svg viewBox="0 0 160 120" aria-hidden="true" style="width:160px;height:120px"><defs><linearGradient id="rq-g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#9AC7F5" stop-opacity=".55"/><stop offset="1" stop-color="#8B83DB" stop-opacity=".35"/></linearGradient></defs>' +
        '<ellipse cx="80" cy="108" rx="54" ry="6" fill="#111827" opacity=".06"/><rect x="34" y="30" width="72" height="66" rx="12" fill="#FFFFFF" stroke="#D3DDE9"/><rect x="48" y="20" width="72" height="66" rx="12" fill="url(#rq-g)"/>' +
        '<path d="M66 54l10 10 22-22" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="128" cy="26" r="4" fill="#8B83DB" opacity=".6"/><circle cx="30" cy="58" r="3" fill="#9AC7F5"/></svg>' +
        '<h2>Nothing waiting for review</h2><p>Every captured obligation has been confirmed. New items appear here when capture isn\u2019t sure about a clause.</p></div>');
      return;
    }
    if (!list.length) {
      Hub.setHTML('queue', '<div class="card state state--inline"><p>No ' + esc(f) + '-confidence items. <a href="#confidence=all">Show all ' + queue.length + '</a></p></div>');
      return;
    }
    Hub.setHTML('queue', '<ul class="rq">' + list.map(item).join('') + '</ul>' +
      '<p class="muted" style="margin-top:24px;font-size:14px"><a href="' + esc(Hub.url.view('OBLIGATIONS', [['ReviewState', 'Needs review']])) + '" target="_top">Open the same items in the Obligations list</a></p>');
  }

  Hub.start({ lists: ['OBLIGATIONS'], render: render });
})(window.Hub);
