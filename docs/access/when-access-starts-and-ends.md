# When Access Starts & Ends

Access to Datahub and DSMLP is granted through a workspace rather than to an
individual, and the date it opens depends on the kind of workspace
([What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)).
After a course ends, access ends first, the course environment is purged on a
later date, and instructor and course-wide files are archived only on request.

## Students Enrolled in a Course

Student access follows the course roster in TSS (formerly TritonLink). No
request or form is required. An environment appears for every student enrolled
in a course that uses the platform.

Datahub sign-in uses standard UCSD single sign-on, as described in
[Signing In](datahub-in-the-browser.md#signing-in). `ssh` to the login node
takes the Active Directory username instead, as described in
[Connecting over SSH](the-login-node.md#connecting-over-ssh).

### Roster Loading and Changes

Rosters are loaded into workspaces one business day before the start of the
term. A TSS change, such as an add, a drop, or a section change, is reflected in
Datahub and DSMLP by 10am the day following the change. Report anything still
missing after that time to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

Waitlisted students are enrolled along with the rest of the roster. The
instructor can re-add a student removed from a waitlist as an observer.

### Auditors, Observers, and Concurrent Enrollment

Auditors and observers are not on the TSS roster. The instructor or TA adds them
through Canvas. Obtain the instructor's permission before requesting access as
an auditor.

Concurrent Enrollment students receive access through Extended Studies staff.

### Late Course Requests

Late course requests are lower priority and are reviewed as time permits.
Students in a course that was requested late may not gain access until as late
as 4th week.

## Instructors, TAs & Course Staff

The deadline for course requests and the date course setup and instructor
access open are set out in
[Course Timeline](../instructor-or-ta.md#course-timeline).

Each course receives a shared nbgrader grader account. Formgrader works only
with that account, and instructor and TA accounts cannot be used for it. The
account is described in
[Grader Account](../grading/notebook-grading-workflow.md#grader-account).

### Adding TAs and Course Staff

The instructor adds TAs through Canvas. Departmental staff, co-instructors, and
anyone else who is not a UC San Diego student cannot be added through Canvas. To
have them added to the roster, email [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
or follow up in the course's Service Desk ticket.

### Personal Accounts for Instructors

An instructor who needs access to evaluate the platform, or to develop a course
that does not yet exist, requests a personal account through the ITS Service
Desk instead of waiting for a course to be provisioned.

## Independent Study, Capstones & Special Projects

For-credit independent study and research (for example, 199/299),
thesis-related research, and certain departmentally sponsored student projects
are requested through the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form. The form asks
about the project, its resource requirements, and its sponsorship.
Non-instructional activities such as clubs and personal projects may be approved
case by case, as resources allow.

### Eligibility Limits

| Population | Eligibility through this route |
|---|---|
| Self-supporting programs, such as MBA, MAS, and Extension | Eligible under the terms in [Self-Supporting Programs](../reference/policy.md#self-supporting-programs) |
| Health Sciences departments, such as Medicine, Pharmacy, and Neurosciences | Datahub access may be limited by Health Sciences security restrictions. DSMLP access is unaffected. |
| Non-student researchers, including postdoctoral scholars | Not eligible. Contact Research IT Services. |

### Priority of Student Research Jobs

Student research jobs run at a lower priority than coursework. Contention is
expected during 8th-10th week and finals.

## Research Labs & Individual Researchers

Research IT Services curates lab and research workspaces manually, with the
potential to auto-populate from departmental staff affiliation. Research
workspaces have no roster feed and no fixed calendar. A research workspace opens
when it is provisioned, and its membership changes on request.

Research IT handles platform selection. Support for the Research Cluster and
Universal Scale Storage is through
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).

## Reporting Missing Access

Most reports of missing access concern a roster change that has not yet reached
the time given in [Roster Loading and Changes](#roster-loading-and-changes). A
report made after that time names the course code, the system in use (Datahub
or `dsmlp-login`), and whether the person is enrolled, auditing, or on an
independent study request.

See also: [Sign-In & Session Problems](sign-in-and-session-problems.md) ·
[Getting Help](../reference/getting-help.md)

## One Additional Quarter

Instructors and students retain access for one additional quarter beyond the
instructional term, ignoring Summer for Spring courses. For a Spring course, the
additional quarter is Fall.

| Course taught in | Access retained through | Access ends (current cycle) |
|---|---|---|
| Fall 2026 | Winter 2027 | 20 March 2027 |
| Winter 2027 | Spring 2027 | 19 June 2027 |
| Spring 2027 | Fall 2027 (Summer is not counted) | 18 December 2027 |

> [!NOTE]
> A day-based retention schedule is also in effect and has not been reconciled
> with the quarter-based schedule. It is set out in
> [Day-Based Retention Schedule](#day-based-retention-schedule).

## Extending Access for an Individual

An extension applies to an individual account, not to the course environment.
The workspace keeps its own schedule, and the extension continues the account's
access to it.

### Instructor Requests

An instructor may request that individual accounts stay active longer. The
established reasons are Incomplete grade resolution, academic integrity
proceedings, course development, hand-off to another instructor, and similar
circumstances. Submit the request by ticket or to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) before access lapses.

### Students Continuing Work After a Course

A student continuing work after a course ends submits an
[Independent Study Request](https://go.ucsd.edu/2wc5gH0). The request moves the
work into an independent study context and does not extend the course.

## How Long Research Access Lasts

Independent study and research access is tied to the project rather than to a
term. No expiry is published for it. Report a project that has ended or a change
of sponsorship.

Access to ETS resources is limited to currently registered UC San Diego
students. A change in registration status can therefore end access regardless of
the state of the project.

## Effects of the End of Access

When access ends, the course environment no longer appears among a member's
available environments, and its home directory is no longer reachable from that
account. The files are not deleted at that point. The purge is a separate, later
event, set out in [The Retention Timeline](#the-retention-timeline). Instructor
and course-wide files can be archived on request, as set out in
[Archiving on Request](#archiving-on-request).

> [!WARNING]
> Files in a course environment become unreachable on the date access ends,
> which is earlier than the purge date. Copy them out before access ends. After
> that date, work in the environment can be recovered only on request to ITS.

Methods for copying files out are in
[Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends).

## The Retention Timeline

Course environments are purged one quarter after account deactivation, which is
two quarters after the course, excluding Summer.

| Course taught in | Access ends | Files purged or archived |
|---|---|---|
| Fall 2026 | 20 March 2027 | 19 June 2027 |
| Winter 2027 | 19 June 2027 | 18 September 2027 |
| Spring 2027 | 18 December 2027 | 26 March 2028 |

The purge excludes individual accounts that have been extended on request
([Extending Access for an Individual](#extending-access-for-an-individual)) and
instructor and course-wide files that have been archived
([Archiving on Request](#archiving-on-request)).

The purge is a lifecycle event. It is separate from routine deletion, such as
the Jupyter Trash folder, which empties itself after 7 days.

See also: [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas)

## Archiving on Request

Instructor and course-wide files can be archived for up to 3 years on request.
Request archiving before the environment is purged, and preferably before access
ends. Contact ITS to archive a class, to revive a previously archived class
environment, or to have an archive made available for download.

Large datasets cannot be archived. Alternatives exist for course data that must
be kept beyond its retention window. Raise the need with ITS early rather than
at the purge date.

### Student Home Directories

Student home directories are not archived. Archiving covers instructor and
course-wide files, and an extension covers an individual account. Neither
preserves a student's own work by default. A student who needs to keep
notebooks copies them out of the environment while it is still reachable.

## Day-Based Retention Schedule

A second, day-based retention schedule is also in effect. It counts days from
the last day of class rather than quarters.

| After the last day of class | Event |
|---|---|
| 11 days | The course's Service Desk ticket is closed |
| 45 days | Shared nbgrader/TA access to the course environment is removed |
| 90 days | Instructor and student access to the course environment is removed; instructors retain platform access with a generic environment |

The quarter-based schedule in [One Additional Quarter](#one-additional-quarter)
and [The Retention Timeline](#the-retention-timeline) has no milestone that
removes shared nbgrader/TA access before instructor and student access. For a
Fall or Winter course, the two schedules end instructor and student access
within weeks of each other. For a Spring course, 90 days after the last day of
class falls in Summer, while the quarter-based schedule does not count Summer
and retains access through Fall. The two schedules have not been reconciled.

## Session Length

Access and retention dates do not govern how long a single session runs. A job
runs for 6 hours by default and up to 12 hours when that is requested at launch,
as set out in
[The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit).
For runs longer than 12 hours, contact
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

Sessions holding a GPU are also subject to idle culling, which is not an error
and does not lose saved work. The criteria are in
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).
