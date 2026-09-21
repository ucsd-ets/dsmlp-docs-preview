/* Search UI for dsmlp-docs.
 *
 * A corrected copy of mkdocs/contrib/search/templates/search/main.js. A file
 * of this name in the theme overrides the plugin's own, which is why this
 * exists rather than a patch. Two changes from upstream, both marked FIX:
 *
 *   1. Titles are NOT escaped again. MkDocs writes them into
 *      search_index.json already HTML-escaped -- 102 of 471 entries in this
 *      corpus contain "&amp;" -- so upstream's escapeHtml(title) produced a
 *      literal "&amp;" on screen. Summaries ARE still escaped: the index
 *      stores `text` raw (0 entries contain "&amp;"), so they need it.
 *
 *   2. Null guards on the two DOM lookups. Upstream dereferences
 *      #mkdocs-search-query and #mkdocs-search-results without checking, so
 *      loading this script on a page that lacks them throws. This theme only
 *      loads it on /search/, but the guards make that a decision rather than
 *      a requirement.
 *
 * Keep in step with upstream when mkdocs is upgraded.
 */

// theme/main.html defines base_url before loading this; the `var` hoist makes
// this a safe default rather than a ReferenceError if it ever does not.
var base_url = base_url || '.';
var min_search_length = 3;

function getSearchTermFromLocation () {
  // FIX 3: upstream reads `q` only. The Decorator's search form posts
  // `search-term` -- a reserved name the hosted search API reads document-wide,
  // so it cannot be renamed to `q`. Both are accepted; `q` keeps older links
  // and hand-typed URLs working.
  var params = new URLSearchParams(window.location.search);
  return params.get('search-term') || params.get('q') || undefined;
}

function joinUrl (base, path) {
  if (path.substring(0, 1) === "/") {
    return path;
  }
  if (base.substring(base.length - 1) === "/") {
    return base + path;
  }
  return base + "/" + path;
}

function escapeHtml (value) {
  return value.replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function formatResult (location, title, summary) {
  // FIX 1: title arrives already escaped from search_index.json; summary does not.
  return '<article><h3><a href="' + joinUrl(base_url, location) + '">' + title +
    '</a></h3><p>' + escapeHtml(summary) + '</p></article>';
}

function displayResults (results) {
  var search_results = document.getElementById("mkdocs-search-results");
  if (!search_results) { return; }  // FIX 2
  while (search_results.firstChild) {
    search_results.removeChild(search_results.firstChild);
  }
  if (results.length > 0) {
    for (var i = 0; i < results.length; i++) {
      var result = results[i];
      var html = formatResult(result.location, result.title, result.summary);
      search_results.insertAdjacentHTML('beforeend', html);
    }
  } else {
    var noResultsText = search_results.getAttribute('data-no-results-text');
    if (!noResultsText) {
      noResultsText = "No results found";
    }
    search_results.insertAdjacentHTML('beforeend', '<p>' + noResultsText + '</p>');
  }
}

function doSearch () {
  var input = document.getElementById('mkdocs-search-query');
  if (!input) { return; }  // FIX 2
  var query = input.value;
  if (query.length > min_search_length) {
    if (!window.Worker) {
      displayResults(search(query));
    } else {
      searchWorker.postMessage({query: query});
    }
  } else {
    displayResults([]);
  }
}

function initSearch () {
  var search_input = document.getElementById('mkdocs-search-query');
  if (!search_input) { return; }  // FIX 2 -- upstream guards the listener but
                                  // then sets .value unguarded just below.
  search_input.addEventListener("keyup", doSearch);
  var term = getSearchTermFromLocation();
  if (term) {
    search_input.value = term;
    doSearch();
  }
}

function onWorkerMessage (e) {
  if (e.data.allowSearch) {
    initSearch();
  } else if (e.data.results) {
    displayResults(e.data.results);
  } else if (e.data.config) {
    min_search_length = e.data.config.min_search_length - 1;
  }
}

if (!window.Worker) {
  console.log('Web Worker API not supported');
  $.getScript(joinUrl(base_url, "search/worker.js")).done(function () {
    init();
    window.postMessage = function (msg) {
      onWorkerMessage({data: msg});
    };
  }).fail(function () {
    console.error('Could not load worker.js');
  });
} else {
  var searchWorker = new Worker(joinUrl(base_url, "search/worker.js"));
  searchWorker.postMessage({init: true});
  searchWorker.onmessage = onWorkerMessage;
}
