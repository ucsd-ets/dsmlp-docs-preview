# Research on DSMLP

This page covers DSMLP for researchers working without a lab workspace:
graduate students, postdocs, undergraduate researchers, staff researchers, and
faculty who have not yet established a group. It assumes familiarity with a
shell.

[Setting Up a Research Lab](faculty-research-lab.md) covers provisioning for a
group. [Projects & Independent Study](student-project.md) covers for-credit
coursework and capstones.

## What the Platform Is Suited To

DSMLP, Datahub, and the Research Cluster are the same cluster. The work does not
change with the name an article uses.

### Suitable Work

The cluster suits interactive analysis, single-node GPU work at every GPU class
size, fine-tuning, long-running batch jobs, and the broad
range of research computing that does not require a supercomputer. It has
operated since 2017 and carries both instruction and research.

### Unsupported HPC Features

DSMLP is not a high-performance computing (HPC) system. It has no Slurm
scheduler and no MPI or multi-node support. The `sbatch`-style wrappers are a
compatibility layer rather than a scheduler. See
[Slurm Compatibility Wrappers](reference/coming-from-hpc.md#slurm-compatibility-wrappers).
[Coming from HPC](reference/coming-from-hpc.md) covers HPC vocabulary and Slurm
compatibility. Routing for work that requires
these features is in [Beyond DSMLP](#beyond-dsmlp).

## Obtaining Access

Request access through
[Research IT](https://research-it.ucsd.edu/computing/index.html), or through
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) for the Research Cluster.
Describe the work, its approximate resource requirements, and the timeframe.

## The Working Environment

### Signing In

Connect with `ssh` to the login node using Active Directory (AD) credentials.
Duo applies. The VPN is not required for `ssh`, only for reaching a port inside
a container. [Connecting over SSH](access/the-login-node.md#connecting-over-ssh)
describes both.

The browser route at [datahub.ucsd.edu](https://datahub.ucsd.edu) is also
available and is often the quickest way to inspect something.
[Access](access/README.md) describes the routes onto the cluster.

### The Login Node

The login node is for launching jobs and moving files, not for computation. See
[What the Login Node Is For](access/the-login-node.md#what-the-login-node-is-for).
It is the one host every user passes through.

### Launching a Job

A GPU job is launched with a wrapper script, for example:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -c 8 -m 32 -g 1 -l gpu-class=large
```

`workspace --list` prints the ID to use for `<WORKSPACE>`; see
[Listing Workspace IDs](workspaces-and-storage/what-a-workspace-is.md#listing-workspace-ids).

Bare `launch.sh` and the wrapper scripts start with different default resources.
See [Default Resources](running-jobs/launch-sh-reference.md#default-resources).
Limits apply per pod and per namespace, and larger allocations are available on
request. See
[Resource Tiers](running-jobs/launch-sh-reference.md#resource-tiers) and
[Administrative Requests](reference/getting-help.md#administrative-requests).
[Resource Requests and Limits](running-jobs/launch-sh-reference.md#resource-requests-and-limits)
describes how the memory requested with `-m` relates to the amount guaranteed.
[`launch.sh` Reference](running-jobs/launch-sh-reference.md) describes the
launcher.

### Storage

Research home directories are substantially larger than course ones and are
set up when access is provisioned.
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas)
gives the sizes. Shared space is also available, as are optional mounts of
external storage such as SDSC Universal Scale Storage. See
[Mounting External Storage](workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage).
[Workspaces & Storage](workspaces-and-storage/README.md) describes the storage
layout.

### Software

The standard software images cover most requirements. Where they do not, a
custom image may be built. Deriving it from a standard image, rather than
starting from nothing, is the supported path.
[Environments](environments/README.md) covers images.

### Root Access

Containers run unprivileged, with no root or sudo access, and dependency
installation has to work within that constraint. See
[Root Access and System Packages](environments/customizing-your-environment.md#root-access-and-system-packages).

## Running Substantial Work

### Job Modes

| Mode | Use |
|---|---|
| Interactive | Exploration |
| Background (`-b`) | Work that must survive a disconnect |
| Batch (`-B`) | Runs that should run to completion |

[Job Modes](running-jobs/job-modes-and-limits.md#job-modes) describes the modes.

### Runtime Limit

Jobs default to 6 hours, and up to 12 hours may be set at launch. A booking
does not lift the limit. See
[Reservation Length and Session Runtime](gpu-access/reservations.md#reservation-length-and-session-runtime).
[The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit)
describes the limit.

### Checkpointing

Checkpoint long-running work. The runtime limit, idle culling, the end of a
reservation window, and preemption can each stop a container independently of
the code it is running.
[Checkpointing & Logging Long Runs](running-jobs/checkpointing.md) describes the
methods.

### Monitoring and Session Events

[Watching a Running Job](running-jobs/watching-your-job.md) covers observing a
running job.

The reservation system reports on a GPU session with Kubernetes events, shown by
`kubectl describe pod`, and by `kubectl get events` after the pod is gone.
[Reservation Events](reference/reservation-events.md) defines each:

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`, `NoMatchingNode`, `WaitingForNode`.
- When it is admitted: `RuntimeGuaranteed`, `ReservationRelinked`,
  `OverstayRelinked`, `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

Direct use of Kubernetes is available to advanced users. See
[Direct Kubernetes Use and Session Events](running-jobs/kubernetes.md).

## Obtaining GPU Time

[GPU Access](gpu-access/README.md) describes the GPU allocation model in effect
from Fall 2026.

### The Shared Research GPU Pool

Researchers without a lab workspace draw on a school-wide shared research GPU
pool. The pool provides a baseline allocation, with occasional boosts when
capacity frees up, most notably over the summer, when instructional hardware
would otherwise be idle. Service Unit (SU) budgets divide the shared pool
equitably among the researchers drawing on it.

### Choosing a GPU Class

Select the smallest GPU class the model fits within. Five classes are available. A larger class is not faster for a
model that fits in a smaller one. It is scarcer and more expensive.
[GPU Classes](gpu-access/gpu-classes.md) describes the classes.
[Workloads by GPU Class](gpu-access/workloads-by-gpu-class.md) gives examples of
research work at each class, and the cards and slices behind it.

### Multi-Day Reservations

A research workspace starts with the same length cap as a course workspace.
Cluster administrators can raise it on the researcher's request, so that a
multi-day fine-tuning run can be booked against guaranteed hardware. A member's
own booking caps at 48 hours unless the workspace is in researcher mode. See
[Reservation Length Caps](gpu-access/reservations.md#reservation-length-caps).

### Borrowing

When a baseline allocation is exhausted, idle capacity may still be available
through borrowing. See
[Borrowing Beyond Quota](gpu-access/quotas-and-availability.md#borrowing-beyond-quota).

### Launching Without a Reservation

> [!WARNING]
> Launching a GPU session without a reservation creates one and draws on the
> researcher's SU budget. A script that relaunches in a loop can exhaust a
> budget window quickly, and nothing intervenes.

[On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges)
describes the charges.
A launch holds a lease of 1 hour 10 minutes; for longer, use
[Extend](gpu-access/reservations.md#extend) in the reservation app at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/).

### Budget Windows

A research SU budget starts with the same size and weekly window as a course
budget, and either can be changed on the researcher's request. See
[Budget Windows & Cadences](gpu-access/service-units-and-budgets.md#budget-windows--cadences).
See [Remaining Balance](gpu-access/service-units-and-budgets.md#remaining-balance).

### Cancellations and Missed Windows

Releasing a window at least 24 hours in advance costs nothing. A later
cancellation, or handing back the end of a session, keeps the time used and
usually part of the unused time. A window missed without cancelling is charged, and an
individual researcher has no instructor from whom to request a waiver.
[The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty)
describes the charge.

### Off-Peak Hours

Off-peak discounts apply outside the peak evening hours. Work that can run at
midday or overnight costs less and waits less.
[Peak & Off-Peak Hours](gpu-access/service-units-and-budgets.md#peak--off-peak-hours)
describes peak and off-peak pricing.

### Idle Culling

Idle culling reclaims a GPU session that stops using its GPU, on every GPU class
and for research sessions as for any other. See
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).

## Data

### Moving Data

Browser upload suits small files. `scp`, `sftp`, `rsync`, `git`, and Globus
handle substantial volumes. For the transfer routes, see
[Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md).

### Sharing Data

[Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace)
describes sharing data with collaborators, with a group, or publicly, and the
permission model beneath it.

### Restricted and Licensed Datasets

Some data available on the cluster carries usage terms. See
[Restricted & Licensed Datasets](workspaces-and-storage/datasets.md#restricted--licensed-datasets).

### Data Classification

P4 data, such as clinical records and export-controlled information, must not be
used on DSMLP. P3 data, which is legally or contractually protected information,
may be permitted after review.
[Data Classification](reference/policy.md#data-classification) describes the
classification levels and the review.

## Publishing & Reproducibility

### Reproducible Artifacts

An image tag, the code, and a checkpoint make a better reproducibility artifact
than a home directory. See
[Building & Publishing a Custom Image](environments/building-a-custom-image.md).

### End of Access

> [!WARNING]
> Access does not last indefinitely, and files do not survive its lapse.
> Retrieve required files before access ends.

[Retrieving Work Before Access Ends](workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)
describes retrieval.

## Support

Support for research users is routed by subject.

| Subject of the question | Contact |
|---|---|
| The Research Cluster, Universal Scale Storage, research allocations | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| Datahub or DSMLP itself: the platform, images, launching | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| Which platform is appropriate for a given body of work | [Research IT](https://research-it.ucsd.edu/computing/index.html) |

Urgent or broadly scoped problems may be escalated through the
[ITS Service Desk](https://support.ucsd.edu/), with a plain statement of what is
affected. See [Response Targets](reference/getting-help.md#response-targets).
[Getting Help](reference/getting-help.md) describes support routing in full.

## Beyond DSMLP

Work requiring tightly coupled multi-node computation, MPI, a batch scheduler, or
capacity at a scale the cluster does not carry belongs on another platform.
[Research IT](https://research-it.ucsd.edu/computing/index.html) can connect
researchers with campus and national resources. A group large enough to warrant
its own guaranteed capacity is a matter for its PI. See
[Setting Up a Research Lab](faculty-research-lab.md).
