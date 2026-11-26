/* How it works - static explainer; reads Obligations only for the badge and one live figure. */
(function (Hub) {
  'use strict';
  function render(data) {
    var all = data.OBLIGATIONS.rows.map(Hub.model.obligation);
    var open = all.filter(function (o) { return !o.closed; });
    var contracts = Hub.uniq(all.map(function (o) { return Hub.contractKey(o.contract); }).filter(Boolean)).length;
    Hub.badge(data, 'OBLIGATIONS', all.length, 'obligation');
    Hub.setHTML('site-stat', all.length
      ? Hub.esc((data.OBLIGATIONS.live ? 'Right now this site tracks ' : 'In the sample data, the hub tracks ') + Hub.plural(open.length, 'open obligation') + ' from ' + Hub.plural(contracts, 'contract') + '.')
      : Hub.esc('No obligations have been captured on this site yet.'));
  }
  Hub.start({ lists: ['OBLIGATIONS'], render: render });
})(window.Hub);
