# Getting Help

This page lists support contacts by type of question, the contents of a support
ticket, ITS response targets, and the administrative requests that cluster
administrators and workspace managers grant.

## Support Tiers

Students in a course contact their instructor or TA first. Course staff are the
first tier of support for course matters: an assignment, a package the course
needs, an environment that does not contain what the syllabus specifies, or a
missing roster entry. Course staff hold the course's own support ticket with ITS
and can see the course and its roster.

Platform problems go directly to ITS, whoever reports them. Platform problems
include an inability to sign in at all, a service that is down, and behavior
that differs from the documentation.

Researchers and lab members have no instructor tier and use the contacts in
[Support Contacts](#support-contacts) directly.

## Support Contacts

| Question | Contact |
|---|---|
| A course a student is enrolled in | The instructor or TA, first |
| Datahub or DSMLP itself: access, images, launching, quotas, GPUs | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| The Research Cluster, or Universal Scale Storage | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| An outage, or anything to be tracked as a ticket | The [ITS Service Desk](https://support.ucsd.edu/) |
| Which platform is appropriate for a research project | [Research IT](https://research-it.ucsd.edu/computing/index.html) |
| An in-depth conversation, for an instructor, TA, or Technical Point of Contact (TPOC) | [1:1 Consultation](https://ucsd-datahub.youcanbook.me/) |

### Email and the Service Desk

Email to `datahub@ucsd.edu` and a ticket through the Service Desk reach the same
staff. Email to that address opens a case, and the Service Desk web form submits
to the same queue. Either route may be used. The web form is better suited to
screenshots and long pastes.

### Platform Selection

Research IT is the first contact for the question of whether a research project
belongs on DSMLP. Research IT can compare a project against the other platforms
the campus runs, including capabilities DSMLP does not have, such as a full
batch scheduler, MPI, and multi-node work, and against the platforms a PI's
group already uses.

See also: [Coming from HPC](coming-from-hpc.md)

## Contents of a Support Ticket

A ticket that ITS can act on without further questions contains the following
items.

| Item | Detail |
|---|---|
| The course or workspace | By name or ID, for example COGS 108. The disk-quota-service page displays the ID. |
| The system | `datahub.ucsd.edu` in a browser, or `dsmlp-login` at a terminal |
| The environment or container | The one selected, for example `scipy-ml-notebook` |
| The exact command | If there was one, copied rather than described |
| The exact error | Copied rather than described, with a screenshot |
| The time | Approximately when it happened, and whether it happens every time |

### Command-Line Details

A ticket about a problem at the command line also includes the node and the
pod. The launch output names the node the pod was assigned to, for example
`INFO pod assigned to node: its-dsmlp-n04.ucsd.edu`, and `kubectl get pods`
gives the pod ID and its status.

See also: [Error Messages](error-messages.md)

### Incidents Affecting More Than One Person

A report of an incident that affects more than one person states its scope in
the first line. ITS prioritizes effort by the number of courses and students
affected and by the overall impact on instruction. A first line such as "none of
my 200 students can start a notebook, and the midterm is Thursday" distinguishes
a broad incident from an individual report such as "my notebook will not start".

## Response Targets

### Individual User Issues

ITS targets resolution of individual user issues within 1-2 business days. The
target applies to all users: students, project users, researchers, and
instructors.

### Instructor Incident Tier

For instructors only, an incident affecting multiple courses, many users, or a
critical point in the quarter such as an exam carries a target response time of
30 minutes from first contact to the Service Desk and a target resolution time
of 8 hours. The tier is an instructional commitment. An instructor or TA reaches
it by reporting a broad incident. An individual user does not reach it by
marking a ticket urgent, and a student whose whole class is affected reaches it
by telling the instructor.

### Escalation Outside Business Hours

Urgent problems outside business hours may be escalated through the Service
Desk. Escalation may be requested, and the Service Desk determines how it is
routed.

## 1:1 Consultation

1:1 Consultation appointments connect instructors, TAs, and TPOCs with ITS
technical staff for real-time guidance, as described in
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).

## Administrative Requests

None of the requests in this section has a self-service control. The requester
has no form, slider, or setting in the interface for any of them; each is an
administrative action taken by someone else.

| Request | Granted by | Information to include |
|---|---|---|
| More disk space | Cluster administrators, by ticket. In a course, the instructor or TA raises it on the course's existing ticket. | The workspace ID, the current disk-quota-service reading, what is taking the space, and what has already been cleared |
| A resource tier above the default, as described in [Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers) | Cluster administrators, by ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) | What the work is, the CPU and memory it needs and why, whether it is one container or several at once, and how long the raise is needed for |
| A GPU class the workspace was not granted | Cluster administrators. A request from an instructor or PI carries more weight than one from a member. | The workspace, the class needed, the model or dataset whose memory footprint requires it, and the dates it matters on |
| More Service Units | Cluster administrators set budgets. A workspace manager may request a change but cannot edit a budget. | The workspace, what the work is, the date by which it must be done, and what the budget has already been spent on |
| A waived cancellation penalty | The workspace manager: an instructor or TA for a course, a PI for a lab. A manager's waiver zeroes the member's share; only an administrator grants a full pardon. | Which booking, and what happened |
| A longer reservation than the workspace permits | The instructor or PI, for the workspace's own cap; cluster administrators, beyond the 48-hour member cap | The length needed, why the work cannot be split into shorter windows, and how it checkpoints |

### Cancellation Penalty Waivers

A cancellation penalty waiver needs no ticket. The workspace manager grants it
in the interface, without ITS involvement.

See also: [The Cancellation Penalty](../gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

### Booking on a Member's Behalf

When a member has run out of Service Units before a deadline, a workspace
manager can book on that member's behalf instead of requesting more Service
Units. A booking made on a member's behalf takes effect at once and does not
draw on the member's budget.

See also: [Service Units & Budgets](../gpu-access/service-units-and-budgets.md)

## Writing an Administrative Request

An administrative request names the workspace, describes the work, states the
deadline and time window, and lists what has already been tried.

### Naming the Workspace

Almost every limit covered in [Administrative Requests](#administrative-requests)
belongs to a workspace rather than to an individual. A request that does not
name a workspace cannot be acted on. The disk-quota-service page displays the
workspace ID, and `workspace --list` on the login node prints every workspace an
account belongs to.

See also: [Naming a Workspace on the Command Line](../workspaces-and-storage/what-a-workspace-is.md#naming-a-workspace-on-the-command-line)

### Describing the Work

One sentence describing the work is sufficient. "Fine-tuning a 7B model for a
CSE 251 project" indicates the GPU class, the approximate memory, and the
approximate duration.

### Deadline and Time Window

A request bounded in time is easier to approve than an open-ended one. Quotas
are date-aware: cluster administrators can raise a course's share for the span
of a project deadline and let it revert automatically. A request for "32 CPU for
the week of the 9th" is therefore stronger than a request for "32 CPU".

### Checks Before Requesting

For a disk quota, state that the Jupyter Trash is empty and that no personal
copy of a shared dataset is held. For a GPU class, state that a smaller class
does not fit. These two checks resolve a large share of requests without a
ticket.

## Workspace Managers and Cluster Administrators

The **workspace manager** is the instructor or TA in a course, and the PI in a
lab. A manager may view the group calendar, book on a member's behalf, and waive
a cancellation charge. A manager may not edit Service Unit budgets or group
limits, regardless of seniority.

**Cluster administrators** hold all other administrative controls and are
reached by ticket.

See also: [Managing a Group](managing-a-group.md)

## Other Administrative Requests

The requests in this table also have no self-service path.

| Request | Reference |
|---|---|
| A run longer than 12 hours | [Runs Longer Than 12 Hours](../running-jobs/job-modes-and-limits.md#runs-longer-than-12-hours) |
| A dataset staged for a course or lab | [Asking for a Dataset to Be Staged](../workspaces-and-storage/datasets.md#asking-for-a-dataset-to-be-staged) |
| An external filesystem mounted | [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage) |
| A raised group quota, or one raised for a deadline week | [Requesting a Quota Increase](../gpu-access/quotas-and-availability.md#requesting-a-quota-increase) |
| Access extended for an individual beyond the standard end of access | [Extending Access for an Individual](../access/when-access-starts-and-ends.md#extending-access-for-an-individual) |
| Course files archived rather than purged | [Archiving on Request](../access/when-access-starts-and-ends.md#archiving-on-request) |
| An image pinned so a course does not move mid-term | [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace) |
| A P3 dataset reviewed | [Data Classification](policy.md#data-classification) |

## Expected Behaviors Reported as Faults

Several of the most frequently reported behaviors are the system working as
designed.

| Observed behavior | Cause | Reference |
|---|---|---|
| A GPU session ended while unattended, with no error | Idle culling | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| `DeadlineExceeded` | The runtime limit | [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| `sudo` refused | Containers run unprivileged | [Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages) |
| A past course no longer appears | Course access ended on schedule | [One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter) |
| No capacity available at a deadline | Contention | [When the Cluster Is Full](../gpu-access/quotas-and-availability.md#when-the-cluster-is-full) |

A quota increase, a GPU class, or a longer reservation window is an
administrative request rather than a fault report. These requests have no
self-service path and are listed in
[Administrative Requests](#administrative-requests).
