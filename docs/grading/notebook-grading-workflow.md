# Notebook Grading Workflow

nbgrader runs inside Datahub from a shared course grader account. This page
covers the nbgrader workflow from creating an assignment to importing grades
into Canvas; the choice of grading tool is covered in
[Choosing a Grading Tool & Interface](choosing-a-grading-tool.md).

## Grader Account

Each Datahub course is issued one shared nbgrader TA grader account, and its
credentials go to the instructor before instruction begins. nbgrader works only
from that account. An instructor's or TA's own account cannot use it.

To open Formgrader:

1. Sign in to [datahub.ucsd.edu](https://datahub.ucsd.edu) as the grader
   account.
2. Launch the course environment.
3. Open **Nbgrader → Formgrader**.

The interfaces that support nbgrader are listed in
[Interface Support for nbgrader](choosing-a-grading-tool.md#interface-support-for-nbgrader).

The grader account is shared course infrastructure. Its local environment must
not be reset or cleaned by hand. Request any reset or cleanup in the course
ticket. Known failures of the grader environment and their recovery are listed
in [Common Grading Failures & Recovery](grading-failures.md).

### Multiple Graders

There is no per-TA identity inside nbgrader. Agree on who is grading which
submissions before two people open the same submission.

## Assignment Directories

Work moves through four directories in the grader account's home directory,
each with the same internal structure:

| Directory | Holds | Created by |
|---|---|---|
| `source/` | The staff version, with solutions and hidden tests | Course staff, when adding an assignment |
| `release/` | The student version, solutions stripped | **Generate** |
| *submitted* | What students turned in | **Collect** |
| `autograded/` | Graded submissions | **Autograde** |

## Creating an Assignment

1. In **Manage Assignments**, choose **Add new assignment...**.
2. Enter a name that follows the rules in [Assignment Names](#assignment-names).
3. Set the due date and the **Timezone as UTC offset**: `-0800` for PST, or
   `-0700` for PDT. Due dates are in UTC.
4. Open `source/{assignment_id}/` and add the notebook and any supporting files.
5. Rename the notebook to match the assignment name.

### Assignment Names

- Omit the file extension. An assignment called `Assignment_1` creates a folder
  of that name; the notebooks inside it carry `.ipynb`.
- Use a name that is unique across every assignment the grader account has
  created, not only within the course.
- Do not use spaces. A space in the name is one of the two known causes of a
  failed export at the end of the term, described in
  [Export Failures](#export-failures).

### Assignment File Size Limit

Assignment file size is capped at 100MB by default. Raising the limit requires
editing `nbgrader_config.py` in the course environment. Contact ITS at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) before raising it.

## Marking Up Cells

Open the assignment notebook and turn on the nbgrader cell toolbar with
**Nbgrader → Create Assignment** or the panel on the right-hand side of the
notebook. In the classic interface, the toolbar is under
**View → Cell Toolbar → Create Assignment**. Every cell then carries a grading
control.

| Cell type | Use |
|---|---|
| **Manually graded answer** | A free response, in one cell |
| **Manually graded task** | Work the student does across cells, such as processing data and plotting it |
| **Autograded answer** | Code the student writes, tested later |
| **Autograder tests** | `assert` statements that grade an autograded answer |
| **Read-only** | Anything students must not change, including test cells |

Every marked cell needs an ID, and a point value where one applies.

### Solution and Hidden Test Regions

Special comment lines delimit solutions and hidden tests. The region between
them is replaced when the assignment is generated:

```python
### BEGIN SOLUTION
return sum(values) / len(values)
### END SOLUTION

### BEGIN HIDDEN TESTS
assert mean([2, 4]) == 3
### END HIDDEN TESTS
```

> [!WARNING]
> Without the delimiters, the whole cell is released as-is, solutions included.

Leave at least one visible test, or a comment stating that hidden tests exist.

### Copying Read-Only and Autograded Cells

Do not ask students to copy a read-only or autograded cell. Copying one corrupts
the notebook's metadata and blocks autograding. Recovery is covered in
[Common Grading Failures & Recovery](grading-failures.md).

### Validating Solutions

Before releasing, validate the assignment's own solutions with the
**Validate** button. A pop-up reports which cells failed, if any.

## Generating, Releasing & Collecting

1. Select **Generate** in **Manage Assignments**. This creates `release/`,
   mirroring `source/` with solutions stripped.
2. Preview the release version and confirm that the hidden tests are hidden.
3. Select **Release**. The button becomes an "x"; clicking it again un-releases
   the assignment. Un-releasing does not recall copies that students have
   already fetched.
4. Select **Collect** after the deadline. A pop-up reports how many submissions
   came in.

### Distributing Other Course Materials

Course materials that are not nbgrader assignments, such as lecture notebooks
and data, are usually distributed with a `git-pull` link. The most common
failure of the link is a student clicking it before signing in. Signing in is
covered in [Datahub in the Browser](../access/datahub-in-the-browser.md).

## Autograding, Manual Grading & Feedback

An assignment must be autograded before it can be manually graded. This applies
to every assignment, including one with no autograded cells.

### Autograding

In **Manage Assignments**, click the submission count to open
**Manage Submissions**. Grade one submission with **Autograde**, or grade all of
them at once with the command line shown under the **Instructions** tab.
Results are written to `autograded/`.

### Manual Grading

After autograding, each submission shows as **graded** or
**needs manual grading**. Submissions that need manual grading are worked
through in the **Manual Grading** tab, where per-cell comments are also added.

### Feedback

Returning feedback takes two steps, and both are required.
**Generate Feedback** builds an HTML breakdown of each student's assignment.
**Release Feedback** makes it visible to the student.

## The Student Roster

The nbgrader roster updates from course enrollment through the instructional
weeks. It is not maintained by hand.

### Adding Student Names

Students do not appear in **Manage Students** until they submit something, and
then only by username. To add first and last names:

1. From the login node, signed in as the grader account, run:

    ```bash
    update-nbgrader -c <course-id>
    ```

    This writes a CSV to the grader account's home directory.

2. Check the CSV.
3. Move it to a location the course environment can see. `workspace --list`
   prints the course's path.
4. From a terminal inside the course environment, import it:

    ```bash
    nbgrader db student import <course-id>-nbgrader-students.csv
    ```

Formgrader shows the names after the import.

## Exporting the Grades

Grade export is manual. `nbgrader export` produces `grades.csv`, and course
staff upload that CSV to Canvas. There is no automatic route from Datahub to the
Canvas gradebook.

> [!NOTE]
> Only graded work is exported. Submissions still at **needs manual grading**
> are omitted. Complete
> [Autograding, Manual Grading & Feedback](#autograding-manual-grading--feedback)
> before exporting.

1. Sign in as the course grader account and open a terminal in the course
   environment (**File → New → Terminal**).
2. Run:

    ```bash
    nbgrader export
    ```

    This writes `grades.csv` into the course home directory.

3. Download `grades.csv` from the file browser.

### Export Failures

Export fails for two known reasons: an assignment created with a space in its
title, and an assignment deleted through the filesystem rather than with
`nbgrader db assignment remove`. In both cases, delete the assignment properly
and run the export again. Recovery is covered in
[Common Grading Failures & Recovery](grading-failures.md).

### Exporting Before Access Ends

Access to the grader account ends after the term. Export grades and any other
grading data that must be kept well before that date, following
[Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends).

### Handling the Exported CSV

The exported CSV, like other grading data, is student record data. Once
downloaded, it leaves the platform and is stored on a local machine. Handle and
dispose of it in line with [Policy](../reference/policy.md).

## Importing Into Canvas

In [Canvas](https://canvas.ucsd.edu/), open the course, then:

1. Select the **Grades** tab, then **Actions → Import**.
2. Choose the exported `grades.csv`.
3. Map any assignment Canvas does not recognize. Canvas offers a
   **--Choose Assignment--** dropdown for each unknown assignment. Pick the
   matching Canvas assignment, or create one, and set the points it is worth.
4. Select **Continue**. Canvas shows every student and their new grade, with
   changes highlighted in red.
5. Review that screen, then select **Save Changes**.

The highlighted rows are the grades about to change. The review screen is the
last point before Canvas writes them.

The field order Canvas expects is given in the
[Canvas gradebook import documentation](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-grades-in-the-Gradebook/ta-p/807).

## Scope of the Canvas Integration

Canvas carries course membership into Datahub and creates teams from Canvas
groups. It does not receive grades from nbgrader or from Datahub by any
automatic route, and a Canvas account is not the account used to sign in to
Datahub.

Enrolled student access comes from TSS course rosters; auditors, observers, TAs,
and other course staff are added through Canvas, as described in
[Students Enrolled in a Course](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course).

## The Otter & Gradescope Routes

On the Otter and Gradescope routes, grades reach Canvas through Gradescope, not
through Datahub. A course that needs automatic grade transfer uses a Gradescope
route. The routes are compared in
[Choosing a Grading Tool & Interface](choosing-a-grading-tool.md).
