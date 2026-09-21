# Common Grading Failures & Recovery

**Most grading failures have one of about six causes.** This page is arranged by
symptom.

| Symptom | Section |
|---|---|
| "Failed to validate", "source of the following cell has changed", corrupt metadata | [Validation & metadata errors](#validation--metadata-errors) |
| `nbgrader export` fails | [Export failures](#export-failures) |
| "Database locked" | [The grader environment itself](#the-grader-environment-itself) |
| Stale courses in the assignment list | [The grader environment itself](#the-grader-environment-itself) |
| No Formgrader, no assignment list | [Nothing is where the documentation says](#nothing-is-where-the-documentation-says) |
| A submission or a student is missing | [Missing submissions & missing students](#missing-submissions--missing-students) |

## Validation & Metadata Errors

------------------------------------------------------------------------

**Symptom.** A student cannot validate; the notebook reports that *the source of
the following cell has changed*; a submission cannot be autograded because its
metadata is corrupt; or validation fails with a message about a required field.

**Cause.** A read-only cell or an autograded cell was **copied**, edited or
deleted. nbgrader restores read-only cells from the original, and copies of them
break the mapping between the notebook and the assignment. *This is an upstream
nbgrader behaviour, not a platform fault, and there is no fix on our side.*

**Recovery**, done by the student:

1. Rename the existing notebook, adding `-corrupted` to the filename, and
   download a copy as a fallback.
2. Re-fetch the assignment from the assignment list. Both copies are now in
   their files.
3. Open both, and copy the answers across into the fresh notebook.
4. Re-submit.

Then, as grader: **re-collect the assignment** in Formgrader.

**Prevention.** Please do not ask students to copy cells the course provided,
and state plainly in the assignment that adding cells is fine but duplicating
the given ones is not.
→ [The Notebook Grading Workflow](notebook-grading-workflow.md)

## Export Failures

------------------------------------------------------------------------

**Symptom.** `nbgrader export` fails, typically at the end of the term.

**Two known causes**, both about how an assignment was named or removed:

- **A space in the assignment title.** Name assignments without spaces.
- **An assignment deleted through the filesystem** rather than with
  `nbgrader db assignment remove`, leaving the database and the directories
  disagreeing.

**Recovery.** Delete the assignment properly and run the export again.
→ [Exporting the Grades](notebook-grading-workflow.md#exporting-the-grades)

## The Grader Environment Itself

------------------------------------------------------------------------

**"Database locked".** From a terminal in the course environment:

```bash
rm ~/.local/share/jupyter/nbsignatures.db
```

Close the terminal, stop the server with **File → Hub Control Panel → Stop My
Server**, and start it again.

**Old courses cluttering the assignment list.** nbgrader caches previously used
courses:

```bash
cd ~/.local/share/jupyter/nbgrader_cache
ls -al
rm -r <old_course_directory>
```

**A broken grader environment after a package install.** Clearing `.local` and
running the manual resetter are the standard fixes for an individual account,
but the shared grader account holds the course's nbgrader state, and clearing it
by hand can take grading with it. **Raise it in the course support ticket
instead.**
→ [Customizing an Environment](../environments/customizing-your-environment.md)

## Missing Submissions & Missing Students

------------------------------------------------------------------------

**A student is not in Manage Students.** Students appear only once they have
submitted something, and then by username alone. Names have to be imported
separately.
→ [The Notebook Grading Workflow](notebook-grading-workflow.md)

**A student says they submitted and nothing was collected.** Three things to
confirm with them: that they clicked **Submit** rather than only saving; that
the assignment appears in their list of submitted assignments; and that they are
looking at the same assignment that was collected. *Repeat submissions are
fine — only the most recent one is available to course staff, including a late
one.*

**An assignment cannot be manually graded.** It has not been autograded yet.
Every assignment must go through the autograder first, including one with no
autograded cells in it at all.

**Large files did not come through.** There is a default cap on assignment file
size. Raising it means changing the nbgrader configuration in the course
environment — please ask us rather than editing it blind.

## Nothing Is Where the Documentation Says

------------------------------------------------------------------------

**No Formgrader menu.** Two causes, in order of likelihood:

- **The wrong account.** nbgrader works only from the shared course grader
  account, never from an instructor's or TA's own account.
- **The wrong interface.** NBClassic does not carry the nbgrader extension.
  → [Which Interface Supports Grading](choosing-a-grading-tool.md#which-interface-supports-grading)

**A distribution link does nothing.** A `git-pull` link clicked before signing
in fails silently. Sign in at [datahub.ucsd.edu](https://datahub.ucsd.edu)
first, then click the link again.
→ [Datahub in the Browser](../access/datahub-in-the-browser.md)

**An assignment name is rejected as a duplicate.** nbgrader requires assignment
names to be unique across every assignment the grader account has created, not
just within one course.

## When to Open a Ticket

------------------------------------------------------------------------

**Instructors and TAs:** anything touching the shared grader account, the course
database, or a deadline. *Incidents at a critical point in the term are handled
with more urgency than routine requests — please say so in the ticket.*
→ [Getting Help](../reference/getting-help.md)

**Students:** please go to the course instructor or TA first. They can reproduce
the problem and escalate it to us with the course context attached.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
