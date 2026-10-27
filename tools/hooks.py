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

import html as html_lib
import json
import pathlib
import re
import unicodedata

ALERTS = "NOTE|TIP|IMPORTANT|WARNING|CAUTION"
BLOCKQUOTE = re.compile(r"<blockquote>(.*?)</blockquote>", re.S)
MARKER = re.compile(r"<p>\s*\[!(" + ALERTS + r")\]\s*(?:<br\s*/?>)?\s*", re.I)


# An element that starts a block of its own. Anything else at the start of a
# callout's body is the rest of the paragraph the marker opened.
BLOCK_START = re.compile(r"<(?:p|ul|ol|dl|div|pre|table|blockquote|figure|h[1-6])\b")

# A named callout: the body's first line is a bold label, alone on its line.
#     > [!WARNING]
#     > **Always pass the class label**
#     > Without it, ...
# The label replaces the kind's name; the kind still sets the colour. A bold
# phrase that runs on into the sentence ("**Do not** run ...") is not a label.
NAMED_LABEL = re.compile(
    r"\A<strong>((?:(?!</strong>).)+?)</strong>[ \t]*(?:<br\s*/?>)?[ \t]*(?=\n|</p>|\Z)", re.S)


def _callout(kind: str, inner: str, label: str = "") -> str:
    return (
        f'<div class="docs-note docs-note--{kind.lower()}" role="note">'
        f'<p class="docs-note__label">{label or kind.capitalize()}</p>{inner.strip()}</div>'
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
        label = ""
        named = NAMED_LABEL.match(body)
        if named:
            label = named.group(1).strip()
            body = body[named.end() :].strip()
            if body.startswith("</p>"):
                body = body[len("</p>") :].strip()
        # The marker consumed the opening <p>, so re-open the first paragraph.
        if body and not BLOCK_START.match(body):
            body = "<p>" + body
        out.append(_callout(hit.group(1), body, label))
    return "".join(out)


def on_page_content(html: str, page=None, config=None, files=None) -> str:
    html = BLOCKQUOTE.sub(_split_blockquote, html)
    html = _steps(html)
    html = CAPTION.sub(_caption, html)
    html = GLANCE.sub(_glance, html)
    html = _lead(html, page)
    if config is not None and (config.get("extra") or {}).get("hero"):
        html = _drop_title(html)
    html = _mark_figures(html)
    return _scroll_tables(html, page)


# --------------------------------------------------------------------------
# Page patterns: steps, command captions, glance boxes
# --------------------------------------------------------------------------
#
# Three components from the review site (internal/operating-procedures.md
# names it), written as plain Markdown so a page still reads correctly on
# GitHub, and turned into the components here.
# AUTHORING.md shows each convention; STYLE.md says when to use it. None of
# the three matched anything in the corpus when they were introduced.
#
#   Steps. An ordered list in which EVERY item opens with a bold title alone
#   on its line becomes <ol class="docs-steps">, each title a
#   <span class="docs-step-title">. One item without a title leaves the list
#   as it is; tools/check-style.py warns about such a list.
#
#       1. **Forward the port**
#          Run this from a second terminal:
#
#   Command caption. A paragraph that is only *italic text*, directly above a
#   code block, becomes the block's <figcaption>, in <figure class="docs-command">.
#
#       *Run on the login node*
#       ```bash
#
#   Glance box. A two-column table headed `| At a glance | |` becomes
#   <dl class="docs-glance">, one <dt>/<dd> pair per row.


def _balanced(html: str, start: int, tag: str):
    """The (start, end) of the close tag matching the <tag> opened at start."""
    depth = 0
    for m in re.finditer(rf"<(/?){tag}\b[^>]*>", html[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.start(), start + m.end()
    return None


# The title is alone on its line: a line break, the end of the paragraph, or a
# nested block follows it. "**Do not** press Enter" is not a title.
STEP = re.compile(
    r"\A(<p>)?<strong>((?:(?!</strong>).)+?)</strong>[ \t]*(?:<br\s*/?>)?[ \t]*"
    r"(?=\n|</p>|\Z|" + BLOCK_START.pattern + ")", re.S)


def _step(item: str):
    """A list item's inner HTML as a step, or None if it has no title line."""
    content = item.strip()
    m = STEP.match(content)
    if not m:
        return None
    title, rest = m.group(2).strip(), content[m.end():].strip()
    if m.group(1):                       # a loose item: the title opened a <p>
        rest = rest[len("</p>"):].strip() if rest.startswith("</p>") else "<p>" + rest
    else:                                # a tight item: inline text, then blocks
        block = BLOCK_START.search(rest)
        inline, blocks = (rest[:block.start()], rest[block.start():]) if block else (rest, "")
        rest = (f"<p>{inline.strip()}</p>" if inline.strip() else "") + blocks
    return f'<span class="docs-step-title">{title}</span>{rest}'


def _steps(html: str) -> str:
    out, pos = [], 0
    for m in re.finditer(r"<ol\b[^>]*>", html):
        if m.start() < pos:
            continue                     # inside a list already handled
        close = _balanced(html, m.start(), "ol")
        if not close:
            break
        inner = _steps(html[m.end():close[0]])
        items, steps, i = [], [], 0
        while (li := inner.find("<li", i)) >= 0:
            end = _balanced(inner, li, "li")
            if not end:
                break
            open_end = inner.index(">", li) + 1
            items.append(inner[open_end:end[0]])
            i = end[1]
        steps = [_step(item) for item in items]
        out.append(html[pos:m.start()])
        if items and all(steps):
            out.append('<ol class="docs-steps" role="list">\n'
                       + "\n".join(f"<li>{s}</li>" for s in steps) + "\n</ol>")
        else:
            out.append(m.group(0) + inner + "</ol>")
        pos = close[1]
    out.append(html[pos:])
    return "".join(out)


# With a blank line under the caption, the caption is its own paragraph; without
# one, superfences puts the code block inside the caption's paragraph. GitHub
# renders both as a line above a code block, so both are accepted.
CAPTION = re.compile(
    r"<p><em>((?:(?!</em>)[^<]|<code>[^<]*</code>)+)</em>(\s*</p>)?\s*"
    r"(<pre\b[^>]*>.*?</pre>)(?(2)|\s*</p>)", re.S)


def _caption(match: re.Match) -> str:
    return (f'<figure class="docs-command"><figcaption>{match.group(1).strip()}</figcaption>'
            f"{match.group(3)}</figure>")


GLANCE = re.compile(
    r"<table>\s*<thead>\s*<tr>\s*<th[^>]*>\s*At a glance\s*</th>\s*<th[^>]*>\s*</th>\s*</tr>"
    r"\s*</thead>\s*<tbody>(.*?)</tbody>\s*</table>", re.S | re.I)
GLANCE_ROW = re.compile(r"<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", re.S)


def _glance(match: re.Match) -> str:
    rows = GLANCE_ROW.findall(match.group(1))
    if not rows:
        return match.group(0)
    return ('<dl class="docs-glance">'
            + "".join(f"<div><dt>{k.strip()}</dt><dd>{v.strip()}</dd></div>" for k, v in rows)
            + "</dl>")


# A site that sets extra.hero shows each page's title as the <h1> of
# theme/partials/hero-banner.html, so the body's own leading <h1> would be a
# second one. It is dropped here, after _lead has used it to find the framing
# paragraph. Sites without extra.hero keep it.
_TITLE = re.compile(r"\A\s*<h1\b[^>]*>.*?</h1>\s*", re.S)


def _drop_title(html: str) -> str:
    return _TITLE.sub("", html, count=1)


# --------------------------------------------------------------------------
# Tables that scroll
# --------------------------------------------------------------------------
#
# The Decorator sets overflow-x: hidden on html and body, so a table wider than
# the column is not scrollable: it is cut off at the edge of the screen.
# Measured at 390px wide, 16 pages had a table running past the edge, its last
# columns out of reach. Each table is wrapped in <div class="docs-table">,
# which scrolls sideways instead (theme/css/site.css).
#
# The wrapper is a named region in the tab order, so a keyboard user can focus
# it and scroll it with the arrow keys (WCAG 2.1.1; axe's
# scrollable-region-focusable). Its name is the heading the table sits under,
# numbered when a heading has more than one table, so no two regions on a page
# share a name. Glance tables are already <dl> by now and are not wrapped.

TABLE_OPEN = re.compile(r"<table\b[^>]*>")
TABLE_HEADING = re.compile(r"<h([2-4])\b[^>]*>(.*?)</h\1>", re.S)
HEADERLINK = re.compile(r'<a class="headerlink"[^>]*>.*?</a>', re.S)
WRAPPED = re.compile(r'<div class="docs-table"[^>]*>\s*\Z')


def _table_label(heading_html: str) -> str:
    text = re.sub(r"<[^>]+>", "", HEADERLINK.sub("", heading_html))
    return " ".join(html_lib.unescape(text).split())


def _scroll_tables(html: str, page=None) -> str:
    headings = [(m.start(), _table_label(m.group(2))) for m in TABLE_HEADING.finditer(html)]
    fallback = getattr(page, "title", None) or ""
    out, pos, used = [], 0, {}
    for m in TABLE_OPEN.finditer(html):
        if m.start() < pos:
            continue                     # a table nested in one already wrapped
        close = _balanced(html, m.start(), "table")
        if not close:
            break
        out.append(html[pos:m.start()])
        table = html[m.start():close[1]]
        pos = close[1]
        if WRAPPED.search(html, 0, m.start()):
            out.append(table)
            continue
        under = [text for start, text in headings if start < m.start()]
        label = under[-1] if under else fallback
        name = f"{label} table" if label else "Table"
        used[name] = used.get(name, 0) + 1
        if used[name] > 1:
            name = f"{name} {used[name]}"
        out.append(f'<div class="docs-table" role="region" tabindex="0" '
                   f'aria-label="{html_lib.escape(name, quote=True)}">{table}</div>')
    out.append(html[pos:])
    return "".join(out)


# --------------------------------------------------------------------------
# Lead paragraph and page description
# --------------------------------------------------------------------------
#
# STYLE.md opens every page with a framing paragraph directly under its one
# `#` heading. The build makes that paragraph do two more jobs, so authors
# write it once and nothing else:
#
#   * it gets Bootstrap's `lead` class, the Decorator's own summary style, so a
#     reader sees at once what the page covers;
#   * its text becomes the page's meta description, the snippet search
#     engines and link previews show. Without this every page carried the one
#     site-wide description: 51 of 52 pages, measured.
#
# A description is cut to DESCRIPTION_MAX characters at a sentence end where
# one falls late enough to keep it useful, otherwise at a word, with an
# ellipsis. A page whose heading is not followed by a paragraph keeps the
# site-wide description, and tools/check-html.py reports it.

DESCRIPTION_MAX = 155
DESCRIPTION_MIN_SENTENCE = 70
_LEAD = re.compile(r"(\A\s*<h1\b[^>]*>.*?</h1>\s*)<p>(.*?)</p>", re.S)
_TAG = re.compile(r"<[^>]+>")


def describe(paragraph_html: str) -> str:
    text = " ".join(html_lib.unescape(_TAG.sub("", paragraph_html)).split())
    if len(text) <= DESCRIPTION_MAX:
        return text
    cut = text[:DESCRIPTION_MAX]
    end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if end + 1 >= DESCRIPTION_MIN_SENTENCE:
        return cut[: end + 1]
    return cut[: cut.rfind(" ")].rstrip(",;:") + "\u2026"


def _lead(html: str, page) -> str:
    match = _LEAD.match(html)
    if not match:
        return html
    if page is not None and not page.meta.get("description"):
        page.meta["description"] = describe(match.group(2))
    return f'{match.group(1)}<p class="lead">{match.group(2)}</p>' + html[match.end():]

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
