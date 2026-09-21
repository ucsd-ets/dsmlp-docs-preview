"""MkDocs build hooks.

GitHub alert callouts (`> [!NOTE]`) are not native to Python-Markdown, which
renders them as a blockquote with a literal "[!NOTE]" in the body text.

This is harder than the kramdown equivalent for a specific reason worth
recording: Python-Markdown merges consecutive blank-line-separated blockquotes
into ONE <blockquote> with several <p> children, where GitHub and kramdown keep
them separate. So this cannot simply match a blockquote -- it has to split
inside one at every [!TYPE] paragraph, or the second and third callout get
silently swallowed into the first.
"""

import json
import pathlib
import re
import unicodedata

ALERTS = "NOTE|TIP|IMPORTANT|WARNING|CAUTION"
BLOCKQUOTE = re.compile(r"<blockquote>(.*?)</blockquote>", re.S)
MARKER = re.compile(r"<p>\s*\[!(" + ALERTS + r")\]\s*(?:<br\s*/?>)?\s*", re.I)


def _callout(kind: str, inner: str) -> str:
    return (
        f'<div class="docs-note docs-note--{kind.lower()}">'
        f'<p class="docs-note__label">{kind.capitalize()}</p>{inner.strip()}</div>'
    )


def _split_blockquote(match: re.Match) -> str:
    inner = match.group(1)
    hits = list(MARKER.finditer(inner))
    if not hits:
        return match.group(0)

    out = []
    head = inner[: hits[0].start()].strip()
    if head:
        out.append(f"<blockquote>{head}</blockquote>")

    for i, hit in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(inner)
        body = inner[hit.end() : end].strip()
        # The marker consumed the opening <p>, so re-open the first paragraph.
        if body and not body.startswith("<"):
            body = "<p>" + body
        out.append(_callout(hit.group(1), body))
    return "".join(out)


def on_page_content(html: str, page=None, config=None, files=None) -> str:
    html = BLOCKQUOTE.sub(_split_blockquote, html)
    return _mark_figures(html)

# --------------------------------------------------------------------------
# GitHub-compatible heading anchors
# --------------------------------------------------------------------------
#
# The docs are authored as vanilla GFM and previewed on GitHub, so in-page
# anchors are written the way GitHub generates them. GitHub and Python-Markdown
# disagree on one rule:
#
#   GitHub DELETES punctuation. Python-Markdown REPLACES it with the separator
#   and collapses runs. For "Peak & Off-Peak Hours":
#
#       GitHub          ->  peak--off-peak-hours
#       Python-Markdown ->  peak-off-peak-hours
#
# Measured on import of the dsmlp-doc-revise content: 34 cross-page anchor
# links were broken by exactly this, every one a heading containing "&" or ",".
#
# Installed from on_config rather than declared in mkdocs.yml, because a
# `!!python/name:` reference would need the project root on PYTHONPATH and
# mkdocs does not add it. Hook modules are loaded by path, so this always works.

_HTML_TAG = re.compile(r"<[!/a-z].*?>", re.I)
_STRIP_PUNCT = re.compile(r"[^\w\s-]", re.UNICODE)


# Ids the Decorator chrome owns. A canvas heading that slugs to one of these
# collides with the shell, and the shell wins: base.min.css carries
# `#search{position:absolute!important}` for its own search panel, so a page
# with an `# Search` heading had its <h1> yanked out of flow and the body text
# rendered underneath it. Measured on this site's own /search/ page.
#
# Covers the template's ids plus the Cascade CMS variants, since a page that
# renders correctly here should not break if the chrome is ever swapped for
# the CMS-emitted one.
CHROME_IDS = frozenset({
    "main-content", "uc-emergency", "navbar", "search", "q", "search-scope",
    "cse-site-search", "cse-search-box", "search-m", "q-m", "search-scope-m",
    "search-term-label", "tdr_login", "tdr_footer_feedback",
})

# Prefix applied to a heading id that would otherwise collide. This is the one
# place the site deliberately diverges from GitHub's anchors: a link written as
# `#search` will not resolve here. `mkdocs build --strict` and
# tools/check-links.py both fail on such a link, so it cannot pass unnoticed.
COLLISION_PREFIX = "doc-"


def github_slugify(value, separator="-"):
    """Slugify a heading the way github-slugger does, avoiding chrome ids."""
    text = unicodedata.normalize("NFKC", str(value))
    text = _HTML_TAG.sub("", text)
    text = text.strip().lower()
    text = _STRIP_PUNCT.sub("", text)
    slug = text.replace(" ", separator)
    if slug in CHROME_IDS:
        return COLLISION_PREFIX + slug
    return slug


def on_config(config):
    toc = config["mdx_configs"].setdefault("toc", {})
    toc["slugify"] = github_slugify
    return config


# --------------------------------------------------------------------------
# Unpublished figures
# --------------------------------------------------------------------------
#
# The drafts mark a number nobody has published yet with an HTML comment:
#
#     | Committed cost | <!-- FIGURE: 4 x the rate --> SU |
#     The charge is for **two hours** -- <!-- FIGURE: 2 x the rate --> SU --
#
# Python-Markdown passes comments straight through, so a browser renders those
# as "Committed cost |  SU" and "for two hours --  SU --": a worked example with
# the number silently missing, reading as a typo rather than as a gap.
#
# That was tolerable while each page opened with a note explaining it. The
# importer now strips those notes, so the gap has to be visible on the page
# itself. 19 of these markers sit in page bodies, several inline in tables and
# mid-sentence.

# The colon and the description are both optional: two markers in the set
# are a bare `<!-- FIGURE -->` with no detail at all.
FIGURE = re.compile(r"<!--\s*FIGURE\s*:?\s*(.*?)\s*-->", re.S)


def _figure(match):
    detail = " ".join(match.group(1).split())
    detail = detail.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    detail = detail.replace('"', "&quot;")
    title = f"Not yet published: {detail}" if detail else "Not yet published"
    return f'<span class="docs-figure" title="{title}">figure not published</span>' 


def _mark_figures(html):
    return FIGURE.sub(_figure, html)


# --------------------------------------------------------------------------
# Search index cleanup
# --------------------------------------------------------------------------
#
# `toc` is configured with permalink: true, which appends a pilcrow anchor to
# every heading. Useful on the page (CSS hides it until hover), but the search
# plugin indexes rendered text, so the character lands in the index and then in
# the result summaries a reader sees:
#
#     "Datahub & DSMLP Documentation ¶ This is the documentation set for ..."
#
# Measured on this corpus: 49 of 471 entries. Titles are unaffected.
#
# Stripping it here rather than in on_page_content keeps the anchors in the
# published HTML, which is the point of having them.

PERMALINK_CHARS = "¶§\U0001f517"
_PERMALINK_RUN = re.compile(r"\s*[" + PERMALINK_CHARS + r"]\s*")


def on_post_build(config, **kwargs):
    index_path = pathlib.Path(config["site_dir"]) / "search" / "search_index.json"
    if not index_path.is_file():
        return

    data = json.loads(index_path.read_text(encoding="utf-8"))
    cleaned = 0
    for doc in data.get("docs", []):
        for field in ("text", "title"):
            value = doc.get(field)
            if value and any(c in value for c in PERMALINK_CHARS):
                doc[field] = _PERMALINK_RUN.sub(" ", value).strip()
                cleaned += 1
    if cleaned:
        index_path.write_text(json.dumps(data), encoding="utf-8")
