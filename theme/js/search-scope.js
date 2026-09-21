/* Routes the chrome search box by its scope selector.
 *
 * The Decorator's search form posts `search-scope` and `search-term`. Two of
 * the three scopes are campus-wide and belong to the hosted search API; only
 * "this-site" is ours. Rather than intercept the form's submit -- which would
 * mean site JavaScript bound to a chrome element -- the form posts here and
 * this decides where the query actually goes.
 *
 * Loaded in <head> on /search/ only, so a campus-scoped query leaves before
 * the page fetches the ~800KB lunr index it will not use.
 *
 * act.ucsd.edu/cwp/tools/search-redir is a 301 that forwards both parameters
 * to www.ucsd.edu/search unchanged, so they are passed through as given.
 */
(function () {
  'use strict';

  var CAMPUS_REDIRECT = 'https://act.ucsd.edu/cwp/tools/search-redir';
  var SITE_SCOPE = 'this-site';

  var params = new URLSearchParams(window.location.search);
  var scope = params.get('search-scope');

  // No scope, or ours: stay here and let the lunr UI handle it.
  if (!scope || scope === SITE_SCOPE) {
    return;
  }

  var term = params.get('search-term') || params.get('q') || '';
  var out = new URLSearchParams();
  out.set('search-scope', scope);
  out.set('search-term', term);

  // replace() so Back returns to the page the search started from rather than
  // bouncing through this one.
  window.location.replace(CAMPUS_REDIRECT + '?' + out.toString());
})();
