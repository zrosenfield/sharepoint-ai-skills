/* Settings - admin hub */
(function (Hub) {
  'use strict';
  var esc = Hub.esc, fmt = Hub.fmt, plural = Hub.plural;

  function render(data) {
    var runs = data.RUNLOG.rows.map(Hub.model.run);
    var rules = data.OWNERS.rows.map(Hub.model.rule);
    Hub.badge(data, 'RUNLOG', runs.length, 'run logged', 'runs logged');

    Hub.setHTML('meta-owners', esc(rules.length ? plural(rules.length, 'routing rule') : 'No rules yet \u2014 add one'));
    var latest = runs.filter(function (r) { return r.at; }).sort(function (a, b) { return b.at - a.at; })[0];
    Hub.setHTML('meta-runlog', esc(runs.length ? plural(runs.length, 'run') + (latest ? ' \u00b7 last ' + fmt.ago(latest.at) : '') : 'No runs logged yet'));

    if (!rules.length) {
      Hub.setHTML('rules', '<div class="pad" style="padding-bottom:24px"><p class="notice"><svg aria-hidden="true"><use href="#i-warn"></use></svg><span>No routing rules yet. Until you add one, Assign owners leaves every new obligation without an owner and nobody is reminded.</span></p></div>');
    } else {
      Hub.setHTML('rules', '<table class="table table--stack"><caption class="sr-only">Routing rules in Obligation Owners</caption><thead><tr>' +
        '<th scope="col">Rule</th><th scope="col">Category</th><th scope="col">Business unit</th><th scope="col">Counterparty</th><th scope="col">Owner</th><th scope="col">Escalation</th><th scope="col">Notify by</th></tr></thead><tbody>' +
        rules.map(function (r) {
          return '<tr><td class="cell-lead"><a class="cell-title" href="' + esc(Hub.url.disp('OWNERS', r.id)) + '" target="_top">' + esc(r.title || 'Untitled rule') + '</a></td>' +
            '<td data-label="Category">' + esc(r.category) + '</td><td data-label="Business unit">' + esc(r.bu) + '</td>' +
            '<td data-label="Counterparty">' + esc(r.counterparty || 'Any') + '</td><td data-label="Owner">' + (r.owner ? esc(r.owner) : Hub.pill('empty', 'No owner')) + '</td>' +
            '<td data-label="Escalation">' + esc(r.escalation || '\u2014') + '</td><td data-label="Notify by">' + esc(r.notify || 'Both') + '</td></tr>';
        }).join('') + '</tbody></table>');
    }

    Hub.lastRuns(runs).forEach(function (l) {
      l.wf.tokens.forEach(function (token) { lastRun(l, token); });
    });
  }

  function lastRun(l, token) {
    var el = Hub.byId('wf-last-' + token);
    if (!el) return;
    var r = l.last;
    var html = '<span class="label">Last run</span>' + Hub.outcomePill(r ? r.outcome : '') +
      '<span>' + (r && r.at ? '<time datetime="' + esc(r.at.toISOString()) + '">' + esc(fmt.dateTime(r.at)) + '</time> \u00b7 ' + esc(fmt.ago(r.at)) : 'No runs logged yet') + '</span>';
    if (l.count > 1) html += '<span>' + plural(l.count, 'run') + ' logged</span>';
    if (l.wf.tokens.length > 1) html += '<span>Shared with the other capture workflow \u2014 both log as \u201c' + esc(l.wf.name) + '\u201d.</span>';
    if (l.issue) html += '<span class="notice' + (l.issue.level === 'rose' ? ' notice--rose' : '') + '" style="padding:8px 12px"><span>' + esc(l.issue.text) + '</span></span>';
    html += '<a class="link-arrow" href="' + esc(Hub.url.view('RUNLOG', [['Workflow', l.wf.name]])) + '" target="_top">See runs' + Hub.icon('arrow') + '</a>';
    el.innerHTML = html;
    var pre = Hub.byId('prompt-' + token), todo = Hub.byId('prompt-todo-' + token);
    if (pre && todo) todo.hidden = String(pre.textContent || '').indexOf('{{' + 'WORKFLOW_PROMPT_') === -1;
  }

  Hub.start({ lists: ['RUNLOG', 'OWNERS'], render: render });
})(window.Hub);
