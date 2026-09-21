# Getting Help & What to Ask Staff For

Most questions have an obvious home, and sending one to the wrong place mostly
costs a day. This page is the routing table.

## Start With the Right Tier

------------------------------------------------------------------------

**Students in a course start with their instructor or TA.** Course staff are the
first tier of support for anything course-shaped: an assignment, a package the
course needs, an environment that does not contain what the syllabus says it
does, a missing roster entry. They hold the course's own support ticket with us
and can see the course and its roster.

**Platform matters come straight to us.** Being unable to sign in at all, a service
that is down, or behaviour that differs from what this documentation says: those are
ours, whoever reports them.

**Researchers and lab members have no instructor tier**, and should use the table
below directly.

## Where to Send What

------------------------------------------------------------------------

| The question concerns | Please contact |
|---|---|
| A course a student is enrolled in | The instructor or TA, first |
| Datahub or DSMLP itself — access, images, launching, quotas, GPUs | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| The Research Cluster, or Universal Scale Storage | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| An outage, or anything to be tracked as a ticket | The [ITS Service Desk](https://support.ucsd.edu/) |
| Which platform is appropriate for a research project at all | [Research IT](https://research-it.ucsd.edu/computing/index.html) |
| An in-depth conversation, for an instructor, TA or TPOC | [1:1 Consultation](https://ucsd-datahub.youcanbook.me/) |

**`datahub@ucsd.edu` and the Service Desk reach the same people.** Mail to that
address opens a case; the Service Desk is the same queue with a web form in front
of it. *Either route works, and the web form suits screenshots and long pastes.*

**Research IT is the right first stop when the question is "should this be on
DSMLP at all?"** They can weigh a project against the other platforms campus
runs, including capabilities this cluster does not have — a genuine batch
scheduler, MPI, multi-node work — and against what a PI's group is already
using. → [Coming from HPC](coming-from-hpc.md)

## What to Put in the Ticket

------------------------------------------------------------------------

A report we can act on without a round trip contains:

- **The course or workspace**, by name or ID — e.g. COGS 108. *The
  disk-quota-service page displays the ID.*
- **Which system**: `datahub.ucsd.edu` in a browser, or `dsmlp-login` at a
  terminal. They fail in different ways and are diagnosed differently.
- **The environment or container** selected, e.g. `scipy-ml-notebook`.
- **The exact command**, if there was one, copied rather than described.
- **The exact error**, likewise — and a screenshot, which frequently carries
  context the transcription loses.
- **When it happened**, roughly, and whether it happens every time.

**From the command line, two extra lines are worth their weight.** The launch
output names the node the pod landed on
(`INFO pod assigned to node: its-dsmlp-n04.ucsd.edu`), and `kubectl get pods`
gives the pod ID and its status. Please include both.
→ [Error Messages](error-messages.md)

**An incident reaching beyond one person belongs in the first line of the
report.** Effort is prioritized by the number of courses and students affected
and the overall impact on instruction, so "my notebook will not start" and "none
of my 200 students can start a notebook, and the midterm is Thursday" need to be
distinguishable at a glance.

## Response Targets

------------------------------------------------------------------------

**Individual user issues: we aim to resolve within 1-2 business days.** That
applies to everybody — students, project users, researchers and instructors alike.

**Instructors only — incidents affecting multiple courses, many users, or a
critical point in the quarter such as an exam carry a target response time of
30 minutes from first contact to the Service Desk, and a target resolution time
of 8 hours.** *This tier is an instructional commitment. It is reached through an
instructor or TA reporting a broad incident, not by an individual user marking
their own ticket urgent* — a student whose whole class is affected reaches it by
telling the instructor.

**Urgent problems outside business hours may be escalated through the Service
Desk.** That escalation exists and may be asked for; how it is routed is a matter
for the Service Desk.

## 1:1 Consultation

------------------------------------------------------------------------

**[1:1 Consultation appointments](https://ucsd-datahub.youcanbook.me/) are for
instructors, TAs and Technical Points of Contact**, and connect the requester with
ITS technical staff for real-time guidance rather than a ticket exchange. They are
the right form for a customization that needs a conversation, a first custom
container, a build error, or a complex or experimental feature.

*Note that availability is reduced in the final weeks of each term, and that at
Spring 2026 staffing levels each course may request up to 6 hours per term.*
→ [Teaching with Datahub & DSMLP](../instructor-or-ta.md) ·
[Software](software.md)

## The Six Requests

------------------------------------------------------------------------

**None of the things in this section has a self-service control.** There is no
form, no slider and no setting in the interface; each one is an administrative
action somebody else takes.

| The request | Who can grant it | What to include |
|---|---|---|
| **More disk space** | Cluster administrators, by ticket. In a course, the instructor or TA raises it on the course's existing ticket | The workspace ID, the current disk-quota-service reading, what is taking the space, and what has already been cleared |
| **A resource tier above the default** — more than 8 CPU or 32 GB in one container, up to 32 CPU / 128 GB | Cluster administrators, by ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) | What the work is, the CPU and memory it needs and why, whether it is one container or several at once, and how long the raise is needed for |
| **A GPU class the workspace was not granted** | Cluster administrators. The request carries more weight from an instructor or PI than from a member | The workspace, the class needed, the model or dataset whose memory footprint requires it, and the dates it matters on |
| **More Service Units** | Cluster administrators set budgets; a manager may **request** a change but cannot edit one | The workspace, what the work is, by when it must be done, and what the budget has already been spent on |
| **A cancellation penalty waived** | **The workspace manager** — an instructor or TA for a course, a PI for a lab | Which booking, and what happened. A manager's waiver zeroes the member's share; only an administrator grants a full pardon |
| **A longer reservation than the workspace permits** | The instructor or PI for the workspace's own cap; cluster administrators beyond the 48-hour member cap | The length needed, why the work cannot be split into shorter windows, and how it checkpoints |

**One of those six is not a ticket.** A cancellation penalty is waived by the
workspace manager, in the interface, without us being involved.
→ [The Cancellation Penalty](../gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

**And one has a faster alternative than the request itself.** Where a member has
run out of Service Units the evening before a deadline, a manager can **book on
that member's behalf**, which takes effect at once and does not draw the member's
budget at all. → [Service Units & Budgets](../gpu-access/service-units-and-budgets.md)

## Writing the Request

------------------------------------------------------------------------

Four things make a request easy to grant.

**Name the workspace.** Almost every limit on this page belongs to a workspace
rather than to an individual, and a request that does not name one cannot be
acted on. The disk-quota-service page displays the ID; `workspace --list` on the
login node prints every workspace an account belongs to.
→ [Naming a Workspace on the Command Line](../workspaces-and-storage/what-a-workspace-is.md#naming-a-workspace-on-the-command-line)

**Say what the work is.** Not in detail — a sentence. "Fine-tuning a 7B model for
a CSE 251 project" tells us which class, roughly how much memory and how long,
all at once.

**Name the deadline, and name the window.** A request bounded in time is easier to
approve than an open-ended one. Quotas in particular are date-aware — staff can
raise a course's share for exactly the span of a project deadline and let it
revert on its own — so "32 CPU for the week of the 9th" is a stronger ask than
"32 CPU".

**Say what has already been tried.** For a disk quota: that the Jupyter Trash is
empty and no personal copy of a shared dataset is being held. For a GPU class:
that a smaller class does not fit. Those two checks resolve a large share of
requests without a ticket at all.

## Who "Staff" Means

------------------------------------------------------------------------

**The workspace manager** is the instructor or TA in a course, and the PI in a
lab. A manager may view the group calendar, book on a member's behalf, and waive a
cancellation charge. A manager may **not** edit Service Unit budgets or group
limits, however senior they are.

**Cluster administrators** hold everything else, and are reached by ticket.
→ [Managing a Group](managing-a-group.md)

## Also by Request

------------------------------------------------------------------------

The same "no self-service path" applies to several things documented elsewhere:

| The request | Where it is covered |
|---|---|
| A run longer than 12 hours | [Work That Genuinely Needs Longer](../running-jobs/job-modes-and-limits.md#work-that-genuinely-needs-longer) |
| A dataset staged for a course or lab | [Datasets](../workspaces-and-storage/datasets.md#asking-for-a-dataset-to-be-staged) |
| An external filesystem mounted | [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage) |
| A raised group quota, or one raised for a deadline week | [Asking for More](../gpu-access/quotas-and-availability.md#asking-for-more) |
| Access extended beyond the additional quarter | [Extending Access for an Individual](../access/when-access-starts-and-ends.md#extending-access-for-an-individual) |
| Course files archived rather than purged | [Archiving on Request](../access/when-access-starts-and-ends.md#archiving-on-request) |
| An image pinned so a course does not move mid-term | [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace) |
| A P3 dataset reviewed | [Policy](policy.md) |
## Things That Are Not Faults

------------------------------------------------------------------------

Several of the most-reported behaviours are the system working as designed:

| What was seen | What it is |
|---|---|
| A GPU session ended while unattended, with no error | Idle culling → [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| `DeadlineExceeded` | The runtime limit → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| `sudo` refused | Containers run unprivileged → [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary) |
| A course vanished after a quarter | Access is retained one additional quarter → [How Long Access Lasts](../access/when-access-starts-and-ends.md#one-additional-quarter) |
| No capacity available, at a deadline | Contention → [When the Cluster Is Full](../gpu-access/quotas-and-availability.md#when-the-cluster-is-full) |

**A request rather than a report** is a different category again — a quota
increase, a GPU class, a longer window. Those are administrative requests with no
self-service path.
→ [The Six Requests](#the-six-requests)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
