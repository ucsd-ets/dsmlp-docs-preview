# Documentation Review: Tone, Vocabulary, and Structure

Reviewed: all 49 pages under `docs/` (about 67,000 words) at snapshot
`c338a53`. Brief: technical-manual register for students, faculty, and
researchers; no direct address; meaningful neutral headings; explicit warnings;
no narrative framing; sections readable in isolation.

The resulting author instructions are in [STYLE.md](STYLE.md).

## Verdict

The content is technically strong and the terminology is disciplined. The
register is not a manual. It is a well-written essay series: aphoristic,
editorial, and built for linear reading. The pages mostly avoid "you" already,
but they replace it with "we", "please", and an authorial voice that comments
on its own uncertainty. Headings are frequently claims or wordplay rather than
topic labels, all sub-structure is carried by bold paragraphs the sidebar
cannot index, and there is not a single callout on the site.

## What Is Working

- Terminology is consistent and deliberate (workspace, member, workspace
  manager, GPU class, Service Unit), and the glossary backs it.
- Symptom/cause/fix tables, flag tables, and code blocks are correct, specific,
  and well chosen.
- Cross-linking is dense and anchors resolve.
- The pages are largely third-person already, so the voice fix is narrower
  than for typical second-person documentation.
- Technical depth is high, particularly on checkpointing and reservations.

## Findings

### 1. Voice: first-person plural, "please", and authorial commentary

Second person appears 126 times, most of it in the "If you still have
questions..." paragraph that closes 37 pages. The larger problem is first
person: "we", "our", and "us" appear 196 times ("We aim to resolve...",
"Please tell us...", "we have not confirmed...", "our source calls...").
"Please" appears 171 times as a softener before nearly every instruction.

The pages also talk about themselves. Examples: "We are stating that plainly
rather than describing a plausible interface." "A placeholder here would be
worse than the gap." "This page will name the screen as soon as we can confirm
it." "That is very nearly the whole of what we can confirm about it, and this
section is short for that reason." "This is a deliberately conservative
reading, not a statement of policy." These are drafting notes surfaced to
readers.

### 2. Voice: literary devices

Aphorism and wit are the dominant style. "`dsmlp-login.ucsd.edu` is the door,
not the room." "A tunnel outlives nothing." "A silent terminal is success, not
a hang." "A notebook left open over dinner is billed for dinner." "Not drained,
not migrated, not deferred to another node: terminated." Sentence fragments for
rhythm: "SSH. `launch.sh`. Background or batch jobs. VS Code." Wry asides:
"anything with a progress bar", "a lid closing on the way to class". Each is
memorable and each requires reading the surrounding paragraph to decode. A
manual states the fact.

### 3. Headings

Roughly a third of section headings are assertions, negations, counts,
questions, or metaphors rather than topic labels.

- Negation: "A Cull Is Not an Error", "Free Is Not the Same as Available",
  "Length Is Not Runtime", "Two Quotas, Not One", "Three Clocks, Not One",
  "The End of a Window Is Not a Kill", "Not the Same as a Browser Timeout",
  "Not Every Cohort Is Overcommitted", "What It Is Not For", "What Is Not a
  Mount", "What the Reports Are Not", "What Archiving Does Not Cover", "What
  Is Simply Not Here", "Three Things That Are Not Privilege Tiers", "Things
  That Are Not Faults", "The Second Schedule, Which Does Not Agree".
- Counting: "Three Things Worth Knowing Early", "Three Habits to Unlearn",
  "Two Limits Worth Stating Plainly", "Two Practical Consequences".
- Metaphor: "The Hard Boundary", "Rough Edges", "The Shape of It", "The Map".
- Question: "Is the GPU Actually Doing Anything?"
- Colon subtitles on several page titles.

Link text and target headings often disagree. "Idle Culling" points at "What
Counts as Idle". The same storage page is linked under three different names.

### 4. Attention and warnings

The build supports GitHub alert callouts (`tools/hooks.py`) and no page uses
one. Every warning is a bold or italic sentence, and importance is signaled by
phrasing: "worth reading twice", "worth stating plainly", "the step people
miss", "the single most common typo on the platform". Sixteen pages end in a
"Caveats & Limitations" catch-all holding material that belongs in specific
sections. "Backgrounding does not exempt a job from idle culling" sits at the
bottom of the job-modes page rather than under Background Pods.

### 5. Narrative framing and locatability

Every page uses `##` only. There are zero `###` headings outside code fences.
Sub-structure is carried by 579 bold-lede paragraphs, invisible to the sidebar
and to in-page navigation. A reader looking for "signing out does not stop a
session" cannot jump to it. Ten pages compensate with hand-maintained
"Contents" lists, which CONTRIBUTING prohibits.

Pages are written for linear reading: 23 "see above / see below / what
follows" references, essay-style introductions ("There are three ways to run
something. The difference between them is not how much compute a job receives
— it is what happens when nobody is attached."), and a repeated paragraph
template of bold thesis, elaboration, italic aside, arrow link. The 467
em-dashes and 614 arrow-link lines are the typographic footprint of this
pattern.

### 6. Duplication against the stated principle

Six hub pages state "Documented once, and linked from wherever it is needed.
One fact, one anchor: a figure documented here is not restated on an audience
page." The pages do not honor it. Idle-culling figures (30 minutes, 6 hours,
45 minutes) are restated on 13 pages. The resource-tier table appears verbatim
on 3. "Requests are half of limits" is explained on 9. The `-g` versus `-G`
warning appears on 6. The "No Sensitive Data / Shared Compute / Appropriate
Use" block is copied onto 4 pages. When a figure changes it will be wrong
somewhere.

### 7. Process leakage and rendering defects

- Seven hub pages say "Every page in this directory is an initial draft. Each
  opens with a note naming what its writer could not settle." The pages do not
  open with such a note. It was stripped, but 6 references to "the draft note
  above" remain and point at nothing: `reference/coming-from-hpc.md:30`,
  `environments/customizing-your-environment.md:147`,
  `grading/notebook-grading-workflow.md:253`,
  `workspaces-and-storage/moving-and-sharing-data.md:170`,
  `gpu-access/reservations.md:99`, `working-from-the-command-line.md:212`.
- 20 HTML comments (`<!-- FIGURE: ... -->`, `<!-- TO ADD -->`,
  `<!-- UNSETTLED -->`) remain in source. On
  `gpu-access/service-units-and-budgets.md` the "Worked Example" tables render
  with empty cost cells because every figure is a comment.
- The `mkdocs.yml` site-wide draft banner already exists; the per-hub draft
  notice duplicates it.

### 8. Vocabulary and spelling

Vocabulary is generally precise. Colloquialisms recur: "catch people out",
"sit dark", "to hand", "quota'd", "the tidy way", "hand-holding". Spelling is
split between British and American (behaviour/behavior, licence/license,
recognisable) at roughly even counts. Acronyms (TSS, TPOC, USS, SU, AD) are
often used before expansion.

### 9. Conflict with CONTRIBUTING.md

CONTRIBUTING's house style mandates "Second person, present tense. 'You launch
a container', not 'the user will launch a container'." That contradicts the
brief and must change in the source repository alongside the rewrite, or the
next author will revert toward "you".

## Evidence

| Signal | Count |
|---|---|
| Pages / words | 49 / ~67,000 |
| `###` headings outside code fences | 0 |
| Bold-lede paragraphs (`**X.** ...`) | 579 |
| "please" | 171 |
| we / our / us | 196 |
| you / your | 126 (37 in closing boilerplate) |
| Callouts (`[!NOTE]`, `[!WARNING]`) | 0 |
| Hand-maintained Contents lists | 10 |
| Horizontal rules under headings | 427 |
| "→ [link]" lines | 614 |
| Em-dashes | 467 |
| "see above / below / what follows" | 23 |
| "Caveats & Limitations" sections | 16 |
| HTML comment placeholders | 20 |
| Dangling "note above" references | 6 |
| Pages restating idle-cull figures | 13 |

## Pages Needing the Heaviest Rework

In descending order: `access/the-login-node.md`,
`gpu-access/what-ends-a-session.md`, `gpu-access/quotas-and-availability.md`,
`gpu-access/reservations.md`, `gpu-access/service-units-and-budgets.md`,
`reference/coming-from-hpc.md`, `reference/managing-a-group.md`,
`access/when-access-starts-and-ends.md`,
`workspaces-and-storage/moving-and-sharing-data.md`,
`running-jobs/checkpointing.md`.

The audience guides (`student-in-a-course.md`, `instructor-or-ta.md`,
`individual-researcher.md`, `faculty-research-lab.md`) are closest to target
and mostly need de-duplication and the voice fixes.
