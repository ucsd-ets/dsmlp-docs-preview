# Author Instructions: Tone, Headings, and Structure

Scope: every page under `docs/`. Audience: students, faculty, and researchers at
UC San Diego. Register: technical reference manual. A reader arrives from search
or the sidebar, reads one section, and leaves.

These rules replace the "Second person, present tense" line in CONTRIBUTING.md.
Update that file in the source repository when applying them.

## 1. Voice

**1.1 Third person or imperative mood.** Do not address the reader as "you". Do
not refer to the writers or to ITS as "we", "our", or "us". Name the actor: ITS,
Research IT, the Service Desk, cluster administrators, the instructor, the
workspace manager.

| Current | Rewrite |
|---|---|
| We aim to resolve individual user issues within 1-2 business days. | ITS targets resolution of individual user issues within 1 to 2 business days. |
| Please tell us if it no longer behaves as described. | Report discrepancies to datahub@ucsd.edu. |
| If you still have questions or need additional assistance, email us at ... | Delete. Support routing is on Getting Help. |

**1.2 Remove "please".** An instruction is imperative: "Stop the session before
launching another." A rule is declarative: "Manual job execution on the login
node is prohibited." There are 171 occurrences to remove.

**1.3 No aphorisms, metaphors, wit, sentence fragments, or rhetorical build-up.**
State the fact once, plainly.

| Current | Rewrite |
|---|---|
| `dsmlp-login.ucsd.edu` is the door, not the room. | `dsmlp-login.ucsd.edu` is a login node for launching jobs and transferring files. Running computation on it is prohibited. |
| A tunnel outlives nothing. | Closing a tunnel does not stop the container. Stopping the container does not close the tunnel. |
| A notebook left open over dinner is billed for dinner. | An idle session is charged at the same rate as an active one. |
| SSH. `launch.sh`. Background or batch jobs. VS Code. All of these are covered in ... | SSH access, `launch.sh`, background and batch jobs, and VS Code are covered in ... |
| Retrieving work from the platform is not urgent right up until it is impossible. | Files become unreachable when access ends. Copy them out before that date. |

**1.4 No commentary about the documentation or its drafting.** Delete sentences
of the form "we could not confirm", "this page will state X once it is settled",
"a placeholder here would be worse than the gap", "we would rather say this than
imply otherwise", "the mechanics are undocumented in every source available to
this project". Where a value is genuinely unpublished, use one neutral sentence:
"The overstay rate is not yet published." If nothing can be said about a topic,
omit the section rather than explaining why it is short.

**1.5 Remove draft-process notices.** Delete the "Every page in this directory
is an initial draft..." block from the seven hub pages; the site-wide banner in
`mkdocs.yml` already covers it. Delete every reference to "the draft note above"
or "the note above". The notes they point to no longer exist (6 dangling
references).

**1.6 American spelling throughout** (behavior, license, recognize). Currently
mixed roughly evenly with British spelling.

## 2. Headings

**2.1 A heading is a noun phrase that names the topic.** Not a sentence, an
assertion, a negation, a count, a question, or a metaphor. The reader must be
able to predict the content from the sidebar entry alone.

| Current | Rewrite |
|---|---|
| A Cull Is Not an Error | Effects of Idle Culling |
| Three Clocks, Not One | Runtime Limit, Idle Culling, and Reservation Window |
| Free Is Not the Same as Available | Limitations of the Status Page |
| Is the GPU Actually Doing Anything? | Checking GPU Utilization |
| The Hard Boundary | Root Access and System Packages |
| Two Limits Worth Stating Plainly | Hosting and Data Classification Restrictions |
| What It Is Not For | Prohibited Uses of the Login Node |
| Nothing Is Where the Documentation Says | Missing Formgrader Menu or Assignment List |
| The Second Schedule, Which Does Not Agree | Day-Based Retention Schedule |
| Three Habits to Unlearn | Differences from Slurm Behavior |
| Requests Are Half of Limits | Resource Requests and Limits |
| The Six Requests | Administrative Requests |

**2.2 Page titles are short noun phrases.** No colon subtitles. "Teaching with
Datahub & DSMLP: Scope of Support & Guidelines for Usage" becomes "Teaching with
Datahub and DSMLP". "Error Messages: Symptom → Cause → Fix" becomes "Error
Messages".

**2.3 Use `###` subsections.** There are currently none. All sub-structure is
carried by 579 bold-lede paragraphs, which the sidebar cannot index. Any
bold-lede paragraph a reader might search for ("Signing out does not stop a
session", "Requests are half of limits") becomes a `###` heading with plain
prose beneath it.

**2.4 Delete the hand-maintained `**Contents**` lists** (10 pages). CONTRIBUTING
already prohibits them. The sidebar is generated from headings.

**2.5 Delete the horizontal rule under every heading** (427 instances). The
theme styles headings.

**2.6 Link text matches the target heading exactly.** "Idle Culling" currently
links to a section titled "What Counts as Idle". "Interactive, Background &
Batch Modes" links to "The Three Modes". One storage page is linked as
"Directories, Quotas & Cleaning Up", "Directories and What Each Is For", and
"Quotas, Checking Usage & Cleaning Up".

## 3. Calling Attention

**3.1 Use GitHub alert callouts.** The build already supports them via
`tools/hooks.py`.

```markdown
> [!WARNING]
> `0/5 nodes available` after a GPU request usually indicates a missing
> `gpu-class` label, not a full cluster.
```

Use `[!WARNING]` or `[!CAUTION]` for data loss, budget spend, policy violations,
and irreversible actions. Use `[!NOTE]` for a qualification the reader needs
before acting. The label is the signal. Do not signal importance with bold
sentences, italics, "worth reading twice", "worth stating plainly", or "the step
people miss".

**3.2 Dissolve the "Caveats & Limitations" section** that closes 16 pages. Each
item belongs in the section it qualifies, as a callout or a sentence. A
limitation that applies to the whole page goes in the page introduction.

## 4. Structure and Locatability

**4.1 Every section stands alone.** No "see above", "see below", "as above",
"what follows", "the rest of this page", or "both are covered below" (23
instances). Cross-reference by link to a heading, even within the same page.

**4.2 Page introduction: one or two sentences** stating what the page covers and
any prerequisite. No essay lede, no thesis, no scene-setting ("Long runs fail
quietly. A training job that never reached the GPU...").

**4.3 Paragraph shape: plain declarative sentences.** Drop the current pattern
of bold thesis sentence, elaboration, italic aside. Bold is for UI labels and
menu paths (**File → Hub Control Panel → Stop My Server**) and for a term at
its definition. Italics are not used for asides.

**4.4 Prefer a new sentence to a dash-joined clause.** The aside-after-a-dash
construction carries most of the editorial voice (467 em-dashes).

**4.5 Links go inline in the sentence**, or on one "See also:" line at the end
of a section. Retire the "→ [Link]" line as a paragraph terminator (614 lines).

**4.6 One fact, one place.** The hub pages promise this and the pages break it.
Idle-culling figures appear on 13 pages, the resource-tier table on 3,
"requests are half of limits" on 9, the `-g` versus `-G` warning on 6, and the
"No Sensitive Data / Shared Compute / Appropriate Use" block on 4. State each
once on its owning page. Elsewhere, one sentence and a link, without restating
numbers.

**4.7 Audience pages are routing pages.** `student-in-a-course.md`,
`instructor-or-ta.md`, `student-project.md`, `individual-researcher.md`, and
`faculty-research-lab.md` give one sentence and a link per task. They do not
re-explain mechanisms.

## 5. Source Hygiene

**5.1 No HTML comments in published pages.** Remove the 20 `<!-- FIGURE -->`,
`<!-- TO ADD -->`, and `<!-- UNSETTLED -->` comments. The "Worked Example" on
the Service Units page renders with empty cost cells because every figure is a
comment; remove the example until rates are published.

**5.2 Delete the closing "If you still have questions..." paragraph** from all
37 pages. It is second person and duplicates Getting Help.

## 6. Vocabulary

**6.1 Plain and precise.** No colloquialisms: "catch people out", "the step
people miss", "sit dark", "to hand", "quota'd", "the tidy way", "reach for",
"hand-holding", "on their way out".

**6.2 Expand an acronym on first use on each page:** TSS, TPOC, SU, AD, USS,
P3/P4, OOM.

**6.3 Keep the established terms:** workspace, member, workspace manager, GPU
class, Service Unit. They are consistent and must stay so.

## 7. Page Skeleton

```markdown
# Noun Phrase

One or two sentences: what this page covers and what it assumes.

## Topic

Plain prose. Tables for parallel facts. Numbered steps for procedures.

### Subtopic

> [!WARNING]
> One sentence.

See also: [Exact Target Heading](path.md#anchor)
```

## 8. Acceptance Checks

Run against `docs/` before submitting. Each should return no matches, except
where a quoted UI string requires the word.

```bash
grep -rniE "\b(you|your|we|our|us|please)\b" docs --include=*.md
grep -rn "^\*\*Contents\*\*" docs --include=*.md
grep -rn "^-----" docs --include=*.md
grep -rn "<!--" docs --include=*.md
grep -rniE "(see above|see below|as above|what follows|note above)" docs --include=*.md
grep -rn "If you still have questions" docs --include=*.md
grep -rnE "^#+ .*( Not |Actually|Worth|Simply|Genuinely|\?$)" docs --include=*.md
```

`grep -rc "^### " docs --include=*.md` should be well above zero on every
substantial page.
