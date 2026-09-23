# Setting Up a Research Lab

This page is for faculty arranging Datahub and DSMLP access for a research
group. It covers platform suitability, the routes to capacity, establishing a
lab workspace, storage, GPU allocation and borrowing from Fall 2026, the
researcher-contributed hardware pilot, software, and operating a lab.
Researchers working on their own are covered in
[Research on DSMLP](individual-researcher.md), and course setup in
[Teaching with Datahub and DSMLP](instructor-or-ta.md).

## Platform Suitability

### Suitable Workloads

The platform suits single-node GPU work at every size from a slice of a GPU to
a full H100, interactive analysis, long-running batch jobs, and a shared
software environment that an entire group can rely on. Lab members receive the
same tooling that students use.

### Unsuitable Workloads

The platform has no Slurm scheduler, no MPI, and no multi-node parallelism.
[Research IT](https://research-it.ucsd.edu/computing/index.html) can direct
workloads of that shape to a more appropriate platform, as described in
[Platform Selection](reference/getting-help.md#platform-selection).

### Priority of Instruction

During 10th and Finals Weeks and at major assignment deadlines, coursework is
served ahead of research. A lab workspace with its own quota insulates a group
from most of this effect. A lab working from the shared research pool is
subject to it.

## Routes to Capacity

A lab may combine the three routes to capacity.

| Route | Provides | Cost |
|---|---|---|
| The shared research pool | A baseline allocation, with boosts when capacity frees up, most notably over Summer | None. Access is by request. |
| A lab workspace with its own quota | Guaranteed access up to the group's quota, date-aware so that it can flex around the group's deadlines | None for compute. Storage charges are described in [Cost](#cost). |
| Contributing hardware (pilot) | Exclusive reservation rights over the contributed capacity | Purchase of the hardware, as described in [Contributing Hardware (Pilot)](#contributing-hardware-pilot) |

### Cost

Compute is provided at no charge, and there is no compute recharge or
chargeback mechanism. Storage charges are set out in
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).
Cost recovery for work within a self-supporting program is covered in
[Self-Supporting Programs](reference/policy.md#self-supporting-programs).

## Establishing a Lab Workspace

A workspace anchors a group's roster, storage, container images, GPU access,
and storage and GPU quotas, as described in
[What a Workspace Is and What It Controls](workspaces-and-storage/what-a-workspace-is.md).
Research IT curates lab and research workspaces manually rather than populating
them from a course roster.

### Requesting a Lab Workspace

Request a lab workspace from
[Research IT](https://research-it.ucsd.edu/computing/index.html) or at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu). Include:

- The members of the group, and who besides the PI should be able to manage it
- What the group runs: frameworks, model sizes, and whether GPU memory or GPU
  count is the binding constraint
- The data: how much, where it currently resides, and its classification
- Any recurring deadline patterns

### Workspace Manager Permissions

A workspace manager may view the group's reservations, book on a member's
behalf, cancel members' bookings, and waive a cancellation charge, and may
arrange GPU loans with another group in the same cohort where the cohort allows
them. A booking made on a member's behalf is charged to the member's budget. A
manager may not edit Service Unit budgets, group limits, or the workspace length
cap from the application. Those are administrative actions, requested
by ticket as described in
[Administrative Requests](reference/getting-help.md#administrative-requests).
Privilege tiers are described in [Managing a Group](reference/managing-a-group.md).

## Storage

### Home Directories

Each member's research home directory is established at provisioning, alongside
group shared space and any external mounts. The directories are described in
[Where Files Live](workspaces-and-storage/your-files-and-quotas.md#where-files-live),
and home directory sizes in
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

### Shared Lab Space

Shared lab space holds the datasets that every member works from, in place of a
personal copy for each member. Personal copies of a shared dataset exhaust a
group's allocation, as described in
[Personal Copies of Shared Datasets](workspaces-and-storage/your-files-and-quotas.md#personal-copies-of-shared-datasets).

### External Storage

SDSC Universal Scale Storage and similar storage may be mounted into a group's
containers. Capacity thresholds govern what is mounted where, as described in
[Mounting External Storage](workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage).

### Sharing with Collaborators

Sharing with collaborators inside and outside UC San Diego, through group
permissions and public access, is described in
[Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace)
and
[Sharing with People Who Have No Cluster Account](workspaces-and-storage/moving-and-sharing-data.md#sharing-with-people-who-have-no-cluster-account).

### Data Classification

Data classified P4, such as clinical records or export-controlled information,
may not be used on DSMLP. Data classified P3 may be permitted after review, as
described in [Data Classification](reference/policy.md#data-classification),
which also gives the vetting period. Raise either classification in the initial
workspace request rather than later.

## Compute Allocation

### GPU Classes

GPUs are allocated in five size classes, described in
[GPU Classes](gpu-access/gpu-classes.md). Each workspace is given access to one
or more classes, matching its anticipated work.

### Group Quota

The group quota sets the maximum number of GPUs of each class that a lab may
hold at once, as described in
[What a Quota Is](gpu-access/quotas-and-availability.md#what-a-quota-is).
Quotas are date-aware and can be set week by week or day by day, so a lab's
share can rise for a conference deadline and drop back afterward without a
permanent allocation, as described in
[Date-Based Quota Changes](gpu-access/quotas-and-availability.md#date-based-quota-changes).

### Borrowing and Seniority

Last-minute work may use idle capacity beyond the group's quota, so a group that
has exhausted its share can still obtain GPUs that would otherwise be idle.
Borrowing, including how far ahead it applies, is described in
[Borrowing Beyond Quota](gpu-access/quotas-and-availability.md#borrowing-beyond-quota).

Borrowing carries a seniority. Course workspaces always hold senior borrowing
rights. Hardware contributors are granted junior borrowing rights. A junior
borrower may borrow only the idle capacity above a deeper reserve floor, so it
reaches idle capacity later than a senior borrower does. Seniority applies only
when a reservation is made. Once admitted, a junior borrower's reservation is
protected like any other for its full length.

### Service Unit Budgets

Service Unit budgets divide a group's capacity among its members by the same
mechanism that courses use to divide capacity across a roster, as described in
[Service Units & Budgets](gpu-access/service-units-and-budgets.md). A lab's
budget and length cap start at the same defaults as a course's, and are changed
on the PI's request. See
[Budget Windows & Cadences](gpu-access/service-units-and-budgets.md#budget-windows--cadences).
Budgets are set administratively, and changes are requested by ticket, as
described in
[Administrative Requests](reference/getting-help.md#administrative-requests).

### Cohorts

A cohort is a collection of groups whose quotas may sum to more than the
physical capacity allocated to it, so availability can read zero while a group
still has headroom, as described in
[Cohorts](gpu-access/quotas-and-availability.md#cohorts).

### Manager Reports

Manager reports cover reservations by group, peak simultaneous use by class,
reserved hours, and effective limits, as described in
[What the Reports Cover](reference/managing-a-group.md#what-the-reports-cover).
Three of the four reports display cluster-wide data rather than data for the
group alone.

### Reservation Events

The reservation system reports on each GPU session with Kubernetes events,
shown by `kubectl describe pod`, and by `kubectl get events` after the pod is
gone. Each is defined in [Reservation Events](reference/reservation-events.md):

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`.
- When it is admitted: `RuntimeGuaranteed`, `OverstayRelinked`,
  `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

## Contributing Hardware (Pilot)

A pilot is evaluating the placement of researcher-contributed GPUs or servers
into the cluster. The pilot is expected to continue through Spring 2027, when
ITS will determine whether the capability can be made available to a broader
audience.

### Contributor Entitlements

Contributors receive:

- Exclusive reservation rights over their contributed capacity. The lab's group
  GPU limits match its contribution, and the cohort holding contributor groups
  is not overcommitted, so the lab can always book its own GPUs ahead whenever
  it needs them.
- Access to the school-wide shared pool, like any other research group.
- Access to near-term, otherwise idle capacity across the cluster through
  junior borrowing, as described in
  [Borrowing and Seniority](#borrowing-and-seniority). Borrowing is the route
  by which a lab reaches beyond its own contribution when GPUs would otherwise
  be idle.
- The ability to loan capacity and privileges to other groups temporarily.

### Idle Contributed Capacity

Contributed GPUs that are idle become available to other groups for last-minute
and on-demand use. The reservation system guarantees the contributing lab first
claim on its own capacity.

### Requirements for Contributors

Contributed hardware must conform to the cluster's supported configurations.
Discuss a planned contribution with ITS at the specification stage, well before
purchase and not after delivery.

## Software & Environments

### Standard Images

The standard software images suffice for most groups. They are described in
[Standard Images](environments/standard-images.md#standard-images).

### Lab Images

A lab may build its environment into a custom image so that every member,
including a new arrival, receives the same stack. Derive a lab image from a
standard image where possible, which is the supported path, as described in
[Building & Publishing a Custom Image](environments/building-a-custom-image.md).

### Image Pinning

A workspace may pin an image so that members are not moved by a quarterly
update partway through a project, as described in
[Pinning a Workspace](environments/standard-images.md#pinning-a-workspace).

### Unprivileged Containers

Containers run unprivileged, under each user's own UID, with no root or sudo
inside the container, which constrains how dependencies are installed, as
described in
[Root Access and System Packages](environments/customizing-your-environment.md#root-access-and-system-packages).

## Operating a Lab

### Onboarding

Direct new members to [Research on DSMLP](individual-researcher.md), which
assumes a shell and covers launching, storage, and the GPU model. Brief new
members on three points: the group's storage conventions, the GPU class its work
requires, and the reclaiming of an idle GPU session, described in
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).

### Recommended Practices

- Checkpoint long-running work. Runtime limits, idle culling, and preemption all
  end containers for reasons unrelated to the code they run, as described in
  [Checkpointing & Logging Long Runs](running-jobs/checkpointing.md).
- Book the smallest class that fits. A larger class is not faster for a model
  that fits in a smaller one. It is scarcer and more expensive.
- Shut down containers that nobody is using. An idle container continues to
  hold its CPU, memory, and GPU against the group's quota.
- Cancel unused windows. Canceling at least 24 hours ahead costs nothing. A
  later cancellation, or a missed booking, is charged. See
  [The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty).

### Off-Peak Discounts

Off-peak discounts make work that can run at midday or overnight both cheaper
and faster to obtain, as described in
[Peak & Off-Peak Hours](gpu-access/service-units-and-budgets.md#peak--off-peak-hours).

### Scheduled Maintenance

Datahub may be unavailable during scheduled instructional maintenance for
time-sensitive updates or security patches. Research Cluster maintenance
terminates all running jobs, and long-running work must be checkpointed or
completed before that window. Both schedules are given in
[Scheduled Maintenance](reference/policy.md#scheduled-maintenance), and the
effect on sessions in
[Maintenance Closures](gpu-access/what-ends-a-session.md#maintenance-closures).

### Membership Changes

Members join and leave a lab, and access has an end. Files do not leave with a
departing member. Establish what becomes of a departing member's files. The end
of access is described in
[When Access Starts & Ends](access/when-access-starts-and-ends.md).

## Policy

Conditions of use, including data classification, appropriate use, hosting of
externally available services, and availability and reliability, are set out in
[Policy](reference/policy.md).

## Support

| Service | Contact |
|---|---|
| Research IT and the Research Cluster | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu), [research-it.ucsd.edu](https://research-it.ucsd.edu/computing/index.html) |
| Datahub and DSMLP | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| IT Service Desk | [support.ucsd.edu](https://support.ucsd.edu/) |

ITS response targets are given in
[Response Targets](reference/getting-help.md#response-targets), and all support
routes in [Getting Help](reference/getting-help.md).
