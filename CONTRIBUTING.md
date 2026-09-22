# Contributing

Thanks for wanting to improve the DSMLP documentation.

## How changes get made

This repository is a **published snapshot**. The editable source lives in a
private repository maintained by UC San Diego Educational Technology Services,
and every publish overwrites this one wholesale.

That means:

- **Issues are the front door.** [Open one](../../issues/new/choose) and it goes
  straight to the people who maintain the pages.
- **Pull requests here cannot be merged.** We will read yours, port the change
  into the source repository with credit to you, and close the PR with a link
  to the live page. Nothing is lost — it just takes one extra step on our end.
- **Direct commits to this repository are overwritten** on the next publish.

If you maintain DSMLP documentation and need write access to the source, ask in
an issue and we will sort it out.

## What makes a good issue

The page URL, what it says now, and what it should say instead. If something is
simply missing, say what you were trying to do when you needed it — that tells
us more than a topic name does.

## House style

A few conventions the pages follow. Match them if you are proposing wording:

- **"Workspace", not "usage group".** A workspace is the unit a person has
  access to; "usage group" is internal vocabulary and does not appear in
  reader-facing pages.
- **Third person, present tense.** Write about the system and the people who
  use it, not to the reader: "A launch creates a container", not "you launch
  a container". Instructions are imperative: "Stop the session before
  launching another."
- **Headings name a topic.** A noun phrase such as "Idle Culling" or "Stopping
  a Session", not a sentence, a question or a slogan.
- **Warnings are callouts.** `> [!WARNING]` or `> [!CAUTION]` for anything that
  must not be missed, `> [!NOTE]` for a qualification. Importance is not
  signaled with bold sentences.
- **One `#` heading per page, at the top.** It becomes the page title, the
  breadcrumb and the sidebar entry.
- **Link to a section's `README.md`, not its directory.** Write
  `[Grading](../grading/README.md)`, not `[Grading](../grading/)`. Both work
  when read on GitHub; only the first survives the build, and CI fails on the
  second.
- **Don't hand-maintain a table of contents.** `##` and `###` headings are
  collected into the sidebar automatically.

## A note on the draft banner

Pages currently carry a site-wide draft notice. The content is under active
review and some pages describe behavior that has not yet been verified against
a primary source. If a page contradicts what the platform actually does, that is
exactly the kind of issue worth filing.
