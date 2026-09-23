# Projects & Independent Study

This page covers access to Datahub and DSMLP for work outside a scheduled
course, and assumes familiarity with a shell. Access through an enrolled course
is separate, follows different rules, and is covered in
[Using Datahub in a Course](student-in-a-course.md) and
[Working from the Command Line](working-from-the-command-line.md).

## Eligibility & Requesting Access

Project access covers for-credit and campus-sponsored work outside a scheduled
course:

- Designated independent study courses: 198/199, 293/298/299
- Independent thesis or dissertation research
- State-supported capstone projects
- Campus-sponsored co-curricular activities, such as projects, workshops,
  clubs, and teams

Non-credit personal projects may be approved on a case-by-case basis as
resources are available. The programs described in
[Self-Supporting Programs](reference/policy.md#self-supporting-programs) are
eligible, subject to the cost recovery set out there.

For non-students, and for research that is not for credit,
[Research IT](https://research-it.ucsd.edu/computing/index.html) can help
connect faculty, staff, and student researchers with compute platforms.
Individual research on the cluster is covered in
[Research on DSMLP](individual-researcher.md).

### Submitting a Request

Request access through the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form. A request states
who is sponsoring the work, what will be run, the resources required, and for
how long. A request that names a faculty sponsor and a concrete workload is
provisioned considerably faster than one that describes the work only in general
terms.

## How Project Access Differs from Course Access

Most of what may be obtained for a course may be obtained for a project, and the
mechanics are the same. Project access differs in priority, support, duration,
and environment configuration.

### Priority Relative to Coursework

Instruction has priority. When the cluster is busy, during 10th and Finals Weeks
and at major assignment deadlines, coursework is served ahead of project work.
Demand is generally lower during the day than in the evening.

### Support Tier

Project work has no instructor or TA as a first tier of support. Support
questions go directly to the ITS Service Desk, whose staff have no prior
knowledge of the project. Project issues carry the same response target as any
other individual user issue, as given in
[Response Targets](reference/getting-help.md#response-targets). Contacts are
listed in [Support](#support).

### Duration of Access

Project access is granted for a defined period rather than tied to an
instructional term. Submit an extension request before access lapses rather
than afterwards. Access periods are covered in
[When Access Starts & Ends](access/when-access-starts-and-ends.md).

### Environment Configuration

No environment is configured on the student's behalf, and no course menu of
environments is offered. A course receives an image selected and tested by its
instructor. A project receives the standard images and whatever is built upon
them, and the project decides what runs and how. Images are covered in
[Environments](environments/README.md).

## Getting Set Up

1. Sign in at [datahub.ucsd.edu](https://datahub.ucsd.edu) for the browser
   route, or `ssh` to the login node for a terminal. Duo applies, and the VPN is
   not required for either route, as described in
   [Connecting over SSH](access/the-login-node.md#connecting-over-ssh). The
   routes are described in [Access](access/README.md).
2. Locate the project workspace. Project access is provisioned as its own
   workspace, with its own home directory, separate from any course the student
   is enrolled in. Where both exist, select the workspace deliberately at launch,
   as described in
   [Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).
3. Launch a container with `launch-scipy-ml.sh` for the GPU-capable image, or
   `launch-datascience.sh` for the CPU image. Launching is covered in
   [Running Jobs](running-jobs/README.md).
4. Place large inputs in shared or external storage rather than in a per-user
   copy. A project home directory is not large. Storage is covered in
   [Workspaces & Storage](workspaces-and-storage/README.md).

The login node is for launching jobs and moving files, not for running work, as
described in
[What the Login Node Is For](access/the-login-node.md#what-the-login-node-is-for).

## Doing the Work

Project work uses the same procedures as course work, documented on these pages.

| Task | Documented in |
|---|---|
| Request CPU, memory, or a GPU | [`launch.sh` Reference](running-jobs/launch-sh-reference.md) |
| Run work that outlives the terminal | [Job Modes](running-jobs/job-modes-and-limits.md#job-modes) |
| Use `sbatch` and related commands | [Slurm Compatibility Wrappers](reference/coming-from-hpc.md#slurm-compatibility-wrappers) |
| Edit in Visual Studio Code | [Remote Editor Setup](access/remote-editor-setup.md) |
| Install packages, or build an image | [Environments](environments/README.md) |
| Move data in and out | [Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md) |
| Share results with collaborators | [Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace) |

### Service Unit Budget

> [!WARNING]
> Launching an eligible GPU session draws on the project's Service Unit budget,
> whether or not the reservation calendar is used, as described in
> [On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

No TA observes a project's consumption or remarks when the budget is nearly
exhausted. The balance is covered in
[Remaining Balance](gpu-access/service-units-and-budgets.md#remaining-balance).

### Idle GPU Sessions

A GPU session that stops using its GPU is reclaimed, as described in
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).

### Missed Reservations

A booked window that is missed is charged, as described in
[The Claim Window](gpu-access/reservations.md#the-claim-window) and
[The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty).
A waiver is a workspace-manager action, and no TA watches a project calendar to
offer one. Canceling at least 24 hours ahead costs nothing; a later cancellation
keeps part of the cost.

### Reservation Events

The reservation system reports on a GPU session with Kubernetes events, shown by
`kubectl describe pod`, by `kubectl get events` after the pod is gone, and by
Datahub while a session starts. Each is defined in
[Reservation Events](reference/reservation-events.md):

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`.
- When it is admitted: `RuntimeGuaranteed`, `OverstayRelinked`,
  `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

### Checkpointing

Checkpoint long-running work, as described in
[Checkpointing & Logging Long Runs](running-jobs/checkpointing.md).

## Troubleshooting

Error messages are listed in [Error Messages](reference/error-messages.md).
Common symptoms in project work are documented on these pages.

| Symptom | Documented in |
|---|---|
| `OOMKilled` | [Resource Requests and Limits](running-jobs/launch-sh-reference.md#resource-requests-and-limits) |
| `DeadlineExceeded` | [The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| `Pending`, with `FailedScheduling` about untolerated taints | Normal while the reservation system decides; the reason is in the reservation event beside it. See [Missing or Misspelled Class Label](gpu-access/gpu-classes.md#missing-or-misspelled-class-label) |
| The session ended unexpectedly | [What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle), or [End of a Reservation Window](gpu-access/what-ends-a-session.md#end-of-a-reservation-window) |
| Reservation-related events in a pod | [Reservation Events](reference/reservation-events.md) |

## Outgrowing Project Access

Work has outgrown project access when it needs capacity beyond what a project
allocation carries, has become a lab's work rather than one person's, needs
multi-day reservations, or needs storage measured in terabytes.

| Situation | Route |
|---|---|
| Independent work on an ongoing basis | [Research on DSMLP](individual-researcher.md) |
| Provisioning for a group | Provisioning belongs with a PI. Refer the PI to [Setting Up a Research Lab](faculty-research-lab.md). |
| Work beyond this cluster | [Research IT](https://research-it.ucsd.edu/computing/index.html) can discuss other platforms. |

## Policy

Highly sensitive data (P4), such as clinical records or export-controlled
information, must not be used on DSMLP, and legally or contractually protected
information (P3) may be permitted after review, as described in
[Data Classification](reference/policy.md#data-classification). Appropriate use,
the sharing of compute resources, and the other conditions of use are set out in
[Policy](reference/policy.md).

## Support

Questions and tickets go to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) or the
[ITS Service Desk](https://support.ucsd.edu/). A ticket includes what was run,
the full error, and the workspace name. Ticket contents are described further in
[Contents of a Support Ticket](reference/getting-help.md#contents-of-a-support-ticket),
and other routes in [Getting Help](reference/getting-help.md).
