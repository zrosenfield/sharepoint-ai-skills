/* My obligations */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, icon = Hub.icon, plural = Hub.plural;
  var VIEWS = [
    { key: 'mine', label: 'Mine' },
    { key: 'all', label: 'All owners' },
    { key: 'unassigned', label: 'Unassigned' }
  ];
  var GROUPS = ['Overdue', 'Due soon', 'Upcoming', 'No date'];
  var GROUP_NOTE = {
    'Overdue': 'Past the due date and still open.',
    'Due soon': 'Due within 14 days.',
    'Upcoming': 'Due later than 14 days from today.',
    'No date': 'Triggered by an event or ongoing \u2014 no fixed date.'
  };

  function signedInName(owners) {
    var ctx = window._spPageContextInfo;
    var name = ctx && (ctx.userDisplayName || ctx.userLoginName);
    if (!name) return null;
    var hit = owners.filter(function (o) { return o.toLowerCase() === String(name).toLowerCase(); })[0];
    return hit || null;
  }

  function card(o) {
    var facts = [
      ['Due', o.due ? '<time datetime="' + fmt.iso(o.due) + '">' + esc(fmt.date(o.due)) + '</time><span class="cell-sub">' + esc(fmt.due(o.due)) + '</span>' : esc(o.triggerType === 'Ongoing' ? 'Ongoing' : 'When triggered')],
      ['Clause', esc(o.clause || '\u2014')],
      ['Owner', o.owner ? esc(o.owner) : Hub.pill('empty', 'No owner')]
    ];
    var detail = o.timing === 'No date' && o.triggerEvent ? '<p class="ob__text"><strong>Trigger:</strong> ' + esc(o.triggerEvent) + '</p>'
      : (o.text ? '<p class="ob__text">' + esc(Hub.truncate(o.text, 170)) + '</p>' : '');
    var id = esc(o.id || Math.random().toString(36).slice(2));
    return '<li><article class="card ob" aria-labelledby="ob-' + id + '">' +
      '<div class="ob__top"><div><h3 class="ob__title" id="ob-' + id + '">' + esc(o.title) + '</h3>' +
      '<span class="ob__who">' + esc([o.counterparty, o.contract].filter(Boolean).join(' \u00b7 ')) + '</span></div>' +
      '<div class="pills">' + Hub.timingPill(o.timing) + '</div></div>' + Hub.timingNote(o) +
      '<dl class="ob__facts">' + facts.map(function (f) { return '<div><dt>' + f[0] + '</dt><dd>' + f[1] + '</dd></div>'; }).join('') + '</dl>' +
      detail +
      '<div class="pills">' + Hub.categoryPill(o.category) + (o.status === 'In progress' ? Hub.pill('upcoming', 'In progress', 'soon') : '') + Hub.riskPill(o.risk) +
      (/needs review/i.test(o.review) ? Hub.pill('review', 'Needs review', 'review') : '') + '</div>' +
      '<div class="ob__actions">' +
      '<a class="btn btn--sm" href="' + esc(Hub.url.disp('OBLIGATIONS', o.id)) + '" target="_top">' + icon('open') + 'Open<span class="sr-only"> ' + esc(o.title) + '</span></a>' +
      '<span class="hint"><a class="btn btn--sm" href="' + esc(Hub.url.edit('OBLIGATIONS', o.id, 'MyObligations.html')) + '" target="_top" aria-describedby="tip-f-' + id + '">' + icon('tick') + 'Mark fulfilled<span class="sr-only"> ' + esc(o.title) + '</span></a>' +
      '<span class="hint__text" role="tooltip" id="tip-f-' + id + '">Opens the item to edit: set Status to Fulfilled and add the Fulfilled on date. Quicker: in the Obligations list, select the item and choose the Mark fulfilled quick step.</span></span>' +
      '<span class="hint"><a class="btn btn--sm btn--quiet" href="' + esc(Hub.url.view('EVIDENCE')) + '" target="_top" aria-describedby="tip-e-' + id + '">' + icon('clip') + 'Add evidence<span class="sr-only"> for ' + esc(o.title) + '</span></a>' +
      '<span class="hint__text" role="tooltip" id="tip-e-' + id + '">Upload the proof (sent notice, report, certificate) to the Evidence library, then paste its link into this item\u2019s Evidence field.</span></span>' +
      '</div></article></li>';
  }

  function render(data, hash) {
    var d = data.OBLIGATIONS;
    var all = d.rows.map(Hub.model.obligation);
    var open = all.filter(function (o) { return !o.closed; });
    var owners = Hub.uniq([].concat.apply([], all.map(function (o) { return o.owners; }))).sort(function (a, b) { return a.localeCompare(b); });
    var view = VIEWS.some(function (v) { return v.key === hash.view; }) ? hash.view : 'mine';
    var person = hash.owner && owners.filter(function (n) { return n.toLowerCase() === hash.owner.toLowerCase(); })[0];
    var unknownPerson = hash.owner && !person ? hash.owner : null;
    if (!person && !unknownPerson) person = signedInName(owners) || owners[0] || '';
    var who = unknownPerson || person;

    Hub.badge(data, 'OBLIGATIONS', all.length, 'obligation');

    var sets = {
      mine: open.filter(function (o) { return who && o.owners.some(function (n) { return n.toLowerCase() === who.toLowerCase(); }); }),
      all: open.filter(function (o) { return o.owners.length; }),
      unassigned: open.filter(function (o) { return !o.owners.length; })
    };
    var keep = { owner: hash.owner || undefined };
    Hub.setHTML('seg', VIEWS.map(function (v) {
      var h = Hub.hash.href({ view: v.key === 'mine' ? undefined : v.key, owner: keep.owner });
      return '<a class="seg__opt" data-focus="seg-' + v.key + '" href="' + esc(h === '#' ? '#view=mine' : h) + '"' + (v.key === view ? ' aria-current="true"' : '') + '>' +
        esc(v.label) + ' <span class="seg__n">' + sets[v.key].length + '</span></a>';
    }).join(''));

    var sel = Hub.byId('person'), field = Hub.byId('person-field'), hint = Hub.byId('person-hint');
    if (sel) {
      var opts = owners.slice();
      if (unknownPerson) opts.unshift(unknownPerson);
      sel.innerHTML = opts.length ? opts.map(function (n) { return '<option' + (n === who ? ' selected' : '') + '>' + esc(n) + '</option>'; }).join('') : '<option>No owners yet</option>';
      sel.disabled = !opts.length;
      if (!sel.__wired) {
        sel.__wired = true;
        sel.addEventListener('change', function () { var h = Hub.hash.get(); Hub.hash.set({ view: h.view, owner: sel.value }); });
      }
    }
    if (field) field.hidden = view !== 'mine';
    if (hint) hint.hidden = view !== 'mine';

    var title = view === 'mine' ? (who ? 'Open obligations for ' + who : 'Your open obligations') : view === 'all' ? 'Open obligations, all owners' : 'Open obligations with no owner';
    var sub = view === 'mine' ? 'Everything ' + (who ? who + ' owns' : 'you own') + ', grouped by when it\u2019s due. Open an item to update it, mark it fulfilled or attach proof.'
      : view === 'all' ? 'Every open obligation that has an owner, grouped by when it\u2019s due.'
      : 'Nobody is being reminded about these yet. Items held for review get an owner once confirmed; for the rest, open one and set an Owner, or add a rule in Obligation Owners.';
    Hub.setHTML('page-title', esc(title));
    var held = view === 'unassigned' ? sets.unassigned.filter(function (o) { return /needs review/i.test(o.review); }).length : 0;
    Hub.setHTML('page-sub', esc(sub) + (held ? ' <a href="' + esc(Hub.url.page('ReviewQueue.html')) + '" target="_top">' + esc(plural(held, 'item is', 'items are') + ' waiting in Review') + '</a>.' : ''));

    var list = sets[view].slice().sort(Hub.byDue);
    var host = Hub.byId('groups');
    if (host) host.setAttribute('aria-busy', 'false');
    if (!all.length) {
      Hub.setHTML('groups', emptyState('No obligations yet', 'Obligations appear here after a contract is added to the Contracts library and capture has run.', Hub.url.view('CONTRACTS'), 'Open Contracts library'));
      return;
    }
    if (!list.length) {
      var msg = view === 'unassigned' ? ['Every open obligation has an owner', 'Nothing is waiting to be assigned.']
        : view === 'mine' ? ['Nothing open for ' + (who || 'you'), unknownPerson ? 'No obligations are assigned to ' + unknownPerson + '. Choose another name above.' : 'No open obligations are assigned to this person right now.']
        : ['No assigned open obligations', 'Owners are set by the Assign owners workflow using the routing rules in Obligation Owners.'];
      Hub.setHTML('groups', emptyState(msg[0], msg[1], view === 'all' ? Hub.url.view('OWNERS') : '', 'Open Obligation Owners'));
      return;
    }
    var html = GROUPS.map(function (g) {
      var items = list.filter(function (o) { return o.timing === g; });
      if (!items.length) return '';
      var gid = 'g-' + g.replace(/\s+/g, '-').toLowerCase();
      return '<section class="group" aria-labelledby="' + gid + '"><div class="group__head">' + Hub.timingPill(g) +
        '<h2 id="' + gid + '"><span class="sr-only">' + esc(g) + ': </span><span class="group__count">' + plural(items.length, 'obligation') + ' \u00b7 ' + esc(GROUP_NOTE[g]) + '</span></h2><span class="group__rule" aria-hidden="true"></span></div>' +
        '<ul class="ob-grid">' + items.map(card).join('') + '</ul></section>';
    }).join('');
    var closed = all.filter(function (o) {
      if (!o.closed) return false;
      if (view === 'unassigned') return !o.owners.length;
      if (view === 'all') return o.owners.length;
      return who && o.owners.some(function (n) { return n.toLowerCase() === who.toLowerCase(); });
    }).length;
    if (closed) html += '<p class="closed-note">' + plural(closed, 'fulfilled or closed item is', 'fulfilled or closed items are') + ' not shown. <a href="' + esc(Hub.url.view('OBLIGATIONS', [['Status', 'Fulfilled']])) + '" target="_top">See fulfilled obligations</a></p>';
    Hub.setHTML('groups', html);
  }

  function emptyState(title, text, href, link) {
    return '<div class="card state"><svg viewBox="0 0 120 96" aria-hidden="true"><defs><linearGradient id="es-g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#9AC7F5" stop-opacity=".5"/><stop offset="1" stop-color="#8B83DB" stop-opacity=".3"/></linearGradient></defs>' +
      '<ellipse cx="60" cy="86" rx="40" ry="5" fill="#111827" opacity=".06"/><rect x="26" y="14" width="68" height="64" rx="12" fill="url(#es-g)"/><path d="M44 46l10 10 22-22" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      '<h2>' + esc(title) + '</h2><p>' + esc(text) + '</p>' + (href ? '<p><a class="link-arrow" href="' + esc(href) + '" target="_top">' + esc(link) + icon('arrow') + '</a></p>' : '') + '</div>';
  }

  Hub.start({ lists: ['OBLIGATIONS'], render: render });
})(window.Hub);
