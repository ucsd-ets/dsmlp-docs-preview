# The Notebook Grading Workflow, End to End

**nbgrader runs inside Datahub, from a shared course grader account.** This page
is the whole loop: create, release, collect, grade, hand back, export. *The
choice of tool comes first:*
[Choosing a Grading Tool](choosing-a-grading-tool.md).

## Before the Term: The Grader Account

------------------------------------------------------------------------

**Each Datahub course is issued one shared nbgrader TA grader account**, and its
credentials go to the instructor before instruction begins. **nbgrader works
only from that account** — an instructor's or TA's own account cannot use it.

Sign in to [datahub.ucsd.edu](https://datahub.ucsd.edu) as the grader account,
launch the course environment, and open **Nbgrader → Formgrader**. *The account
is shared course infrastructure: its local environment must not be reset or
cleaned by hand; raise it in the course ticket instead.*
→ [Which Interface Supports Grading](choosing-a-grading-tool.md#which-interface-supports-grading) ·
[Common Grading Failures & Recovery](grading-failures.md)

## The Shape of It

------------------------------------------------------------------------

Work moves through four directories in the grader's home, each with the same
internal structure:

| Directory | Holds | Created by |
|---|---|---|
| `source/` | The staff version, with solutions and hidden tests | Course staff, when adding an assignment |
| `release/` | The student version, solutions stripped | **Generate** |
| *submitted* | What students turned in | **Collect** |
| `autograded/` | Graded submissions | **Autograde** |

## Creating an Assignment

------------------------------------------------------------------------

In **Manage Assignments**, choose **Add new assignment...**, then:

- **Name it without a file extension.** An assignment called `Assignment_1`
  creates a folder of that name; the notebooks inside it carry `.ipynb`.
- **Use a name unique across every assignment the grader account has created**,
  not merely within the course.
- **Avoid spaces in the name.** A space here is one of the two known causes of a
  failed export at the end of the term.
- **Set the due date, and set the timezone offset.** Due dates are in UTC; set
  **Timezone as UTC offset** to `-0800` for PST, or `-0700` for PDT.

Then open `source/{assignment_id}/` and add the notebook and any supporting
files, **renaming the notebook to match the assignment name**.

## Marking Up Cells

------------------------------------------------------------------------

Open the assignment notebook and turn on the nbgrader cell toolbar —
**Nbgrader → Create Assignment**, or the panel on the right-hand side of the
notebook. *In the classic interface it is **View → Cell Toolbar → Create
Assignment**.* Every cell then carries a grading control.

| Cell type | Use it for |
|---|---|
| **Manually graded answer** | A free response, in one cell |
| **Manually graded task** | Work the student does *across* cells, e.g. process data and plot it |
| **Autograded answer** | Code the student writes, tested later |
| **Autograder tests** | `assert` statements that grade an autograded answer |
| **Read-only** | Anything students must not change, including test cells |

**Every marked cell needs an ID, and a point value where one applies.**

**Solutions and hidden tests are delimited by special comment lines.** The
region between them is replaced when the assignment is generated:

```python
### BEGIN SOLUTION
return sum(values) / len(values)
### END SOLUTION

### BEGIN HIDDEN TESTS
assert mean([2, 4]) == 3
### END HIDDEN TESTS
```

*Without the delimiters the whole cell is released as-is, solutions included.*

**Leave at least one visible test**, or a comment saying hidden tests exist.

**Please do not ask students to copy a read-only or autograded cell.** Copying
one corrupts the notebook's metadata and blocks autograding.
→ [Common Grading Failures & Recovery](grading-failures.md)

**Validate the assignment's own solutions** with the **Validate** button before
releasing. A pop-up reports which cells failed, if any.

## Generating, Releasing & Collecting

------------------------------------------------------------------------

1. **Generate**, from Manage Assignments. This creates `release/`, mirroring
   `source/` with solutions stripped.
2. **Preview the release version** and confirm the hidden tests really are
   hidden.
3. **Release.** The button becomes an "x"; clicking it again un-releases the
   assignment. *Students who already fetched it keep their copy — an un-release
   does not recall it.*
4. **Collect**, after the deadline. A pop-up reports how many submissions came
   in.

*Course materials that are not nbgrader assignments — lecture notebooks, data —
are usually distributed with a `git-pull` link instead.* Its commonest failure
is a student clicking it before signing in.
→ [Datahub in the Browser](../access/datahub-in-the-browser.md)

## Autograding, Manual Grading & Feedback

------------------------------------------------------------------------

**Autograde first, always.** In Manage Assignments, click the submission count
to reach Manage Submissions. Grade one submission with **Autograde**, or all of
them at once with the command line shown under the **Instructions** tab. Results
land in `autograded/`.

**An assignment must be autograded before it can be manually graded.** This
applies to *every* assignment, including ones with no autograded cells at all.

Submissions then show as *graded* or *needs manual grading*; the **Manual
Grading** tab is where the latter are worked through and per-cell comments
added.

**Feedback is two clicks and both are needed.** **Generate Feedback** builds an
HTML breakdown of each student's assignment; **Release Feedback** is what makes
it visible to them.

## The Student Roster

------------------------------------------------------------------------

**The roster updates itself from course enrollment** through the instructional
weeks; it is not maintained by hand.

**Students do not appear in Manage Students until they submit something**, and
then only by username. To get first and last names in, run this from the login
node while signed in as the grader account:

```bash
update-nbgrader -c <course-id>
```

That writes a CSV to the grader account's home directory. Check it, then move it
somewhere the course environment can see — `workspace --list` prints the
course's path — and import it from a terminal *inside* the course environment:

```bash
nbgrader db student import <course-id>-nbgrader-students.csv
```

Formgrader shows the names after the import.

## Exporting the Grades

------------------------------------------------------------------------

**Grade export is manual.** `nbgrader export` produces `grades.csv`, and course
staff upload that CSV to Canvas. There is no automatic route from Datahub to the
Canvas gradebook.

Signed in as the course grader account, open a terminal in the course
environment (**File → New → Terminal**) and run:

```bash
nbgrader export
```

This writes **`grades.csv`** into the course home directory. Download it from
the file browser.

*Only graded work is exported.* Anything still sitting at *needs manual grading*
is omitted, so the grading pass comes first.
→ [Autograding, Manual Grading & Feedback](#autograding-manual-grading--feedback)

## Importing Into Canvas

------------------------------------------------------------------------

In [Canvas](https://canvas.ucsd.edu/), open the course and:

1. Select the **Grades** tab, then **Actions → Import**.
2. Choose the exported `grades.csv`.
3. **Map any assignment Canvas does not recognise.** Canvas offers a
   **--Choose Assignment--** dropdown for each unknown assignment; pick the
   matching Canvas assignment, or create one, and set the points it is worth.
4. Select **Continue**. Canvas shows every student and their new grade, with
   **changes highlighted in red**.
5. Review that screen, then select **Save Changes**.

The highlighted rows are the grades about to change, and that screen is the last
point before Canvas writes them.

For the field order Canvas expects, follow
[Canvas's own gradebook import documentation](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-grades-in-the-Gradebook/ta-p/807).

## What Canvas *Is* Connected To

------------------------------------------------------------------------

**Canvas is how course membership reaches Datahub — not how grades leave it.**

| Canvas does | Canvas does not |
|---|---|
| Carry non-roster auditor and observer access into the course | Receive grades from nbgrader |
| Carry TAs and other course staff added there | Receive grades from Datahub by any automatic route |
| Create teams, from Canvas groups | Serve as the account Datahub is signed in to |

*Enrolled student access comes from TSS course rosters rather than from
Canvas, and the nbgrader roster follows course enrollment on its own.*
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md)

## The Otter & Gradescope Routes

------------------------------------------------------------------------

**Grades reach Canvas through Gradescope**, not through us. A course that needs
automatic grade transfer takes a Gradescope route.
→ [Choosing a Grading Tool](choosing-a-grading-tool.md)

## Caveats & Limitations

------------------------------------------------------------------------

**Export fails for two known reasons:** an assignment created with a space in
its title, and an assignment deleted through the filesystem rather than with
`nbgrader db assignment remove`. Both are fixed by deleting the assignment
properly and re-running the export.
→ [Common Grading Failures & Recovery](grading-failures.md)

**The CSV is student record data.** Once downloaded it leaves the platform and
sits on a local machine; please handle and dispose of it accordingly.
→ [Policy](../reference/policy.md)

**Export before access to the grader account ends**, not after. The grader
account does not stay open indefinitely past the term.
→ [Retrieving Work](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)

**One shared account, several graders:** there is no per-TA identity inside
nbgrader. Please agree who is grading what before two people open the same
submission.

**Assignment file size is capped**, at a default given as 100MB. Raising it
means editing `nbgrader_config.py` in the course environment; please ask us
rather than guessing, given the open question in the draft note above.

**Grading data is student record data**, and access to the grader account ends
at some point after the term. Please export anything that must be kept well
before that, not after. → [Policy](../reference/policy.md) ·
[Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
