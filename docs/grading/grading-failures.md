# Common Grading Failures & Recovery

This page lists common grading failures by symptom, with the cause and the
recovery for each.

| Symptom | Section |
|---|---|
| "Failed to validate", "source of the following cell has changed", corrupt metadata | [Validation & Metadata Errors](#validation--metadata-errors) |
| `nbgrader export` fails | [Export Failures](#export-failures) |
| "Database locked" | [Database Locked Error](#database-locked-error) |
| Stale courses in the assignment list | [Stale Courses in the Assignment List](#stale-courses-in-the-assignment-list) |
| A broken grader environment after a package install | [Broken Grader Environment After a Package Install](#broken-grader-environment-after-a-package-install) |
| A submission or a student is missing | [Missing Submissions & Missing Students](#missing-submissions--missing-students) |
| An assignment cannot be manually graded | [Manual Grading Before Autograding](#manual-grading-before-autograding) |
| Large files did not come through | [Assignment File Size Cap](#assignment-file-size-cap) |
| No Formgrader, no assignment list | [Missing Formgrader Menu or Assignment List](#missing-formgrader-menu-or-assignment-list) |
| A distribution link does nothing | [Unresponsive Distribution Links](#unresponsive-distribution-links) |
| An assignment name is rejected as a duplicate | [Duplicate Assignment Names](#duplicate-assignment-names) |

## Validation & Metadata Errors

A student cannot validate, the notebook reports that "the source of the
following cell has changed", a submission cannot be autograded because its
metadata is corrupt, or validation fails with a message about a required field.

The cause is a read-only or autograded cell that was copied, edited, or
deleted. nbgrader restores read-only cells from the original, and copies of
them break the mapping between the notebook and the assignment. This is
upstream nbgrader behavior, not a platform fault, and no platform-side fix
exists.

### Recovering the Notebook

The student performs these steps:

1. Rename the existing notebook, adding `-corrupted` to the filename, and
   download a copy as a fallback.
2. Re-fetch the assignment from the assignment list. The student's files then
   hold both copies.
3. Open both notebooks and copy the answers into the fresh notebook.
4. Re-submit.

The grader then re-collects the assignment in Formgrader.

### Preventing Copied Cells

Do not ask students to copy cells the course provided. State in the assignment
that adding cells is permitted and that duplicating the provided cells is not.

See also: [Notebook Grading Workflow](notebook-grading-workflow.md)

## Export Failures

An `nbgrader export` failure typically occurs at the end of the term. Two
causes are known, both related to how an assignment was named or removed:

- A space in the assignment title. Name assignments without spaces.
- An assignment deleted through the filesystem rather than with
  `nbgrader db assignment remove`. The database and the directories then
  disagree.

To recover, delete the assignment with `nbgrader db assignment remove` and run
the export again, as described in
[Exporting the Grades](notebook-grading-workflow.md#exporting-the-grades).

## Grader Environment Failures

### Database Locked Error

To clear a "Database locked" error:

1. From a terminal in the course environment, run:

    ```bash
    rm ~/.local/share/jupyter/nbsignatures.db
    ```

2. Close the terminal.
3. Stop the server with **File → Hub Control Panel → Stop My Server**.
4. Start the server again.

### Stale Courses in the Assignment List

Old courses appear in the assignment list because nbgrader caches previously
used courses. To remove an old course, delete its directory from the cache:

```bash
cd ~/.local/share/jupyter/nbgrader_cache
ls -al
rm -r <old_course_directory>
```

### Broken Grader Environment After a Package Install

For an individual account, the standard fixes are clearing `.local`, described
in
[Recovering a Broken Environment](../environments/customizing-your-environment.md#recovering-a-broken-environment),
and running the manual resetter, described in
["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed). For
the shared grader account, raise the problem in the course support ticket
instead.

> [!WARNING]
> The shared grader account holds the course's nbgrader state. Clearing that
> account's environment by hand can destroy the course's grading.

## Missing Submissions & Missing Students

### Student Missing from Manage Students

Students appear in **Manage Students** only after they have submitted
something, and then by username alone. Names are imported separately, as
described in [The Student Roster](notebook-grading-workflow.md#the-student-roster).

### Uncollected Submissions

When a student reports a submission and nothing was collected, confirm three
things with the student:

- The student clicked **Submit** rather than only saving.
- The assignment appears in the student's list of submitted assignments.
- The student is looking at the same assignment that was collected.

Repeat submissions are permitted. Only the most recent submission is available
to course staff, including a late one.

### Manual Grading Before Autograding

An assignment cannot be manually graded until it has been autograded. Every
assignment must go through the autograder first, including an assignment with
no autograded cells.

### Assignment File Size Cap

A default cap on assignment file size can keep large files from coming
through. Raising the cap requires changing the nbgrader configuration in the
course environment. Request the change from ITS rather than editing the
configuration directly.

## Missing Formgrader Menu or Assignment List

A missing Formgrader menu has two causes. Check them in order of likelihood:

1. The account. nbgrader works only from the shared course grader account,
   never from an instructor's or TA's own account.
2. The interface. NBClassic does not carry the nbgrader extension. The
   interfaces that support grading are listed in
   [Interface Support for nbgrader](choosing-a-grading-tool.md#interface-support-for-nbgrader).

## Unresponsive Distribution Links

A `git-pull` distribution link clicked before signing in fails silently. Sign
in at [datahub.ucsd.edu](https://datahub.ucsd.edu) first, then click the link
again. The sign-in steps are in
[Signing In](../access/datahub-in-the-browser.md#signing-in).

## Duplicate Assignment Names

An assignment name is rejected as a duplicate when it is not unique. nbgrader
requires assignment names to be unique across every assignment the grader
account has created, not only within one course.

## Opening a Support Ticket

Instructors and TAs open a ticket for any problem that touches the shared
grader account, the course database, or a deadline. Incidents at a critical
point in the term are handled with more urgency than routine requests. State
the critical timing in the ticket. Support contacts and response targets are
listed in [Getting Help](../reference/getting-help.md).

Students contact the course instructor or TA first. The instructor or TA can
reproduce the problem and escalate it to ITS with the course context attached.
