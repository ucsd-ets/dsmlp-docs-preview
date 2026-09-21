# When Access Starts & Ends

Access is granted through a
[workspace](../workspaces-and-storage/what-a-workspace-is.md) rather than to an
individual: when it opens depends on what kind of workspace it is, and it does
not end with the last final of the term. Three distinct things happen after a
course ends, on three different dates — **access ends**, then the **environment
is purged**, and, only if someone asks, some of it is **archived**.

**Contents**

- [Students Enrolled in a Course](#students-enrolled-in-a-course)
- [Instructors, TAs & Course Staff](#instructors-tas--course-staff)
- [Independent Study, Capstones & Special Projects](#independent-study-capstones--special-projects)
- [Research Labs & Individual Researchers](#research-labs--individual-researchers)
- [If Access Does Not Arrive](#if-access-does-not-arrive)
- [One Additional Quarter](#one-additional-quarter)
- [Extending Access for an Individual](#extending-access-for-an-individual)
- [How Long Research Access Lasts](#how-long-research-access-lasts)
- [What the End of Access Does, and Does Not, Do](#what-the-end-of-access-does-and-does-not-do)
- [The Retention Timeline](#the-retention-timeline)
- [Archiving on Request](#archiving-on-request)
- [What Archiving Does Not Cover](#what-archiving-does-not-cover)
- [The Second Schedule, Which Does Not Agree](#the-second-schedule-which-does-not-agree)
- [Session Length Is a Different Clock](#session-length-is-a-different-clock)

## Students Enrolled in a Course

------------------------------------------------------------------------

**Student access follows the TSS course roster** — the system formerly called
TritonLink. **Rosters are loaded into workspaces one business day before the
start of the term.** There is nothing to request and no form to submit: an
environment appears for every student enrolled in a course that uses the
platform.

**A TSS change is reflected in Datahub and DSMLP by 10am the day following the
change** — an add, a drop, a section change. *Please report anything still
missing beyond that timeframe to* [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

Waitlisted students are enrolled along with the rest of the roster, and a
student removed from a waitlist can be re-added by the instructor as an observer.

**Auditors and observers are not on the TSS roster** and are added
through Canvas by the instructor or TA. Please obtain the instructor's
permission before requesting access as an auditor. Concurrent Enrollment
students receive access by way of Extended Studies staff.

Where the course itself was requested late, the whole schedule moves: late
requests are lower priority and reviewed as time permits, and students may not
gain access until as late as 4th week.

*Datahub sign-in is standard UCSD single sign-on; `ssh` to the login node takes
the Active Directory username instead.*
→ [Datahub in the Browser](datahub-in-the-browser.md#signing-in) ·
[Connecting over SSH](the-login-node.md#connecting-over-ssh)

## Instructors, TAs & Course Staff

------------------------------------------------------------------------

**Course setup and instructor access open 4-5 weeks prior to the start of
instruction**, and earlier setup is available on request. That window is the
time for testing features, validating assignments and making customizations.
*Note that 1:1 Consultation availability is limited in the final weeks of each
term.*

**The request itself is due 4 weeks before instruction begins**, through the
Specialized Instructional Computing Course Request form, which opens the 2nd
week of the previous term.

TAs are added through Canvas by the instructor. Departmental staff,
co-instructors and anyone else who is not a UC San Diego student cannot be added
that way — email [datahub@ucsd.edu](mailto:datahub@ucsd.edu), or follow up in
the course's Service Desk ticket, and we will add them to the roster.

Each course also receives a shared nbgrader grader account, the only account
formgrader works with — instructor and TA accounts cannot be used for it.
→ [The Notebook Grading Workflow](../grading/notebook-grading-workflow.md#before-the-term-the-grader-account)

Instructors seeking access for their own exploration — evaluating the platform,
or developing a course that does not exist yet — request a personal account
through the ITS Service Desk rather than waiting for a course to be provisioned.

## Independent Study, Capstones & Special Projects

------------------------------------------------------------------------

For-credit independent study and research (e.g. 199/299), thesis-related
research, and certain departmentally-sponsored student projects are requested
through the **Independent Study Request** form, at
<https://go.ucsd.edu/2wc5gH0>. The form asks about the project, its resource
requirements, and its sponsorship. Non-instructional activities such as clubs
and personal projects may be approved case by case, as resources allow.

Three eligibility limits govern this route:

- **Self-supporting programs** (e.g. MBA, MAS, Extension) are welcome; cost
  recovery applies — please contact us to discuss.
- **Health Sciences departments** (e.g. Medicine, Pharmacy, Neurosciences) may
  have limited Datahub access owing to Health Sciences security restrictions.
  DSMLP access is unaffected.
- **Non-student researchers, including postdoctoral scholars**, are not eligible
  by this route and should contact Research IT Services.

*Note that student research jobs run at a lower priority than coursework, and
contention is to be expected during 8th-10th week and finals.*

## Research Labs & Individual Researchers

------------------------------------------------------------------------

**Lab and research workspaces are curated manually** by Research IT Services,
with the potential to auto-populate from departmental staff affiliation. There
is no roster feed and no fixed calendar: a research workspace opens when it is
provisioned, and its membership changes when someone asks for it to change.

Research IT handles platform selection;
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) covers the Research Cluster
and Universal Scale Storage.

## If Access Does Not Arrive

------------------------------------------------------------------------

The commonest report is a roster change that has not yet reached 10am the
following day. Beyond that, a report should name the course code, the system in
use (Datahub or `dsmlp-login`), and whether the person is enrolled, auditing, or
on an independent study request.
→ [Sign-In & Session Problems](sign-in-and-session-problems.md) ·
[Getting Help](../reference/getting-help.md)

## One Additional Quarter

------------------------------------------------------------------------

**Instructors and students retain access for one additional quarter** beyond the
instructional term, ignoring Summer for Spring courses. A course environment
therefore stays reachable for roughly twice the length of the course itself.

| Course taught in | Access retained through | For the current cycle, ends |
|---|---|---|
| Fall 2026 | Winter 2027 | 20 March 2027 |
| Winter 2027 | Spring 2027 | 19 June 2027 |
| Spring 2027 | Fall 2027 — *Summer is not counted* | 18 December 2027 |

*Summer is the exception.* A Spring course is not retained through Summer and
then through Fall; Summer is skipped, and the additional quarter is Fall.

## Extending Access for an Individual

------------------------------------------------------------------------

**Instructors may request that individual accounts stay active longer.** The
established reasons are Incomplete grade resolution, academic integrity
proceedings, course development, hand-off to another instructor, and similar
circumstances. Requests go by ticket or to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). *Please make the request before
access lapses rather than after: reviving an environment is more work than
keeping one open.*

Students continuing work after a course ends submit an
[Independent Study Request](https://go.ucsd.edu/2wc5gH0). That is the documented
route for continuing a project past the course that started it, and it moves the
work into an independent study context rather than extending the course.

*Extending an individual account is not the same as extending the course
environment.* The workspace still follows its own schedule; what an extension
buys is the account's continued access to it.

## How Long Research Access Lasts

------------------------------------------------------------------------

**Independent study and research access is tied to the project, not to a term.**
There is no roster to fall off and no quarter boundary to cross, and we do not
publish an expiry for it. *Please report a project that has ended or a change of
sponsorship. Access to ETS resources is limited to currently registered UC San
Diego students, so a change in registration status can end access independently
of the state of the project.*

## What the End of Access Does, and Does Not, Do

------------------------------------------------------------------------

**Losing access is not the same as losing the files.** When access ends the
course environment stops appearing among a member's available environments and
its home directory is no longer reachable from that account, but the files
themselves are not deleted at that moment: the purge is a separate, later event,
and instructor and course-wide files can be archived on request.

The operative date is therefore the end of access rather than the purge date.
**Anything worth keeping should be copied out before then**; once access has
ended, work in the environment can be recovered only by asking us.
→ [Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)

## The Retention Timeline

------------------------------------------------------------------------

**Course environments are purged one quarter after account deactivation** — that
is, two quarters after the course, again excluding Summer.

| Course taught in | Access ends | Files purged or archived |
|---|---|---|
| Fall 2026 | 20 March 2027 | 19 June 2027 |
| Winter 2027 | 19 June 2027 | 18 September 2027 |
| Spring 2027 | 18 December 2027 | 26 March 2028 |

Two things are excluded from the purge: **individual accounts that have been
extended** on request, and **instructor and course-wide files that have been
archived**.

## Archiving on Request

------------------------------------------------------------------------

**Instructor and course-wide files can be archived for up to 3 years**, on
request. Please ask before the environment is purged, and ideally before access
ends, while it is still possible to see what is worth keeping. Contact ITS to
archive a class, to revive a previously archived class environment, or to have an
archive made available for download.

**Large datasets cannot be archived**, owing to storage limitations.
*Alternatives exist for course data that must outlive its retention window;
please raise it with us early rather than at the purge date, as they take
arranging.*

## What Archiving Does Not Cover

------------------------------------------------------------------------

**Student home directories are not archived.** The archive provision covers
instructor and course-wide files, and an extension covers an individual account;
neither preserves a student's own work by default. A student keeping their own
notebooks copies them out of the environment while it is still reachable.

*Purge is a lifecycle event, not everyday housekeeping.* Routine deletion —
including the Jupyter Trash folder, which empties itself after 7 days — is a
different subject entirely.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

## The Second Schedule, Which Does Not Agree

------------------------------------------------------------------------

**A second retention schedule is currently in effect and published**, counted in
days from the last day of class rather than in quarters:

| After the last day of class | What happens |
|---|---|
| 11 days | The course's Service Desk ticket is closed |
| 45 days | Shared nbgrader/TA access to the course environment is removed |
| 90 days | Instructor and student access to the course environment is removed; instructors retain platform access with a generic environment |

**Which of the two governs a given course cannot be stated here.** For a Fall
or Winter course the difference is a matter of weeks. For a **Spring** course it
is not: 90 days after a Spring course ends falls in Summer, and the quarter-based
rule does not count Summer at all, so the two schedules point months apart.

**The 45-day milestone has no counterpart in the quarter-based schedule.**
Nothing there removes the shared grader account or TA access ahead of everyone
else's. *For a TA with regrades, an Incomplete, or an academic integrity matter
outstanding, it is the earliest milestone on either schedule.*

Until the conflict is settled, the earlier of the two dates is the operative one
for anyone depending on continued access: grading, Incomplete resolution and
file retrieval fall on the day-based clock, and an individual extension covers a
longer need. *This is a deliberately conservative reading, not a statement of
policy.*

## Session Length Is a Different Clock

------------------------------------------------------------------------

None of the above is about how long a single session runs. **A job runs for 6
hours by default and up to 12 hours when that is requested at launch**; beyond 12
hours, contact [datahub@ucsd.edu](mailto:datahub@ucsd.edu).
→ [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

Sessions holding a GPU are also subject to idle culling, which is not an error
and does not lose saved work.
→ [What Ends a Session](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
