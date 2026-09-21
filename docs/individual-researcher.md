# Research on DSMLP

------------------------------------------------------------------------

This article describes use of the cluster by researchers working without a lab
workspace behind them — graduate students, postdocs, undergraduate researchers,
staff researchers, and faculty who have not yet established a group. It covers
what the platform is suited to, how to obtain access, how to run substantial
work, how GPU time is allocated from Fall 2026, and where research support is
routed.

**This article assumes familiarity with a shell.**

*Provisioning for a group* is covered in
[Setting Up a Research Lab](faculty-research-lab.md). *For-credit coursework and
capstones* are covered in
[Projects & Independent Study](student-project.md).

**DSMLP, Datahub, and the Research Cluster are the same cluster.** All three
names are in circulation, and nothing about the work changes depending on which
name a given article uses.

## What the Platform Is Suited To

------------------------------------------------------------------------

**Well suited:** interactive analysis, single-node GPU work at every size from a
6GB slice to a full H100, fine-tuning, long-running batch jobs, and the broad
middle of research computing which does not require a supercomputer. The cluster
has operated since 2017 and carries both instruction and what we describe as the
long tail of research.

**Not suited:** the cluster is explicitly *not* an HPC system. There is **no
Slurm scheduler** and **no MPI or multi-node support**. Work requiring
tightly-coupled multi-node parallelism belongs on another platform, and
[Research IT](https://research-it.ucsd.edu/computing/index.html) can direct
researchers to a more appropriate one. *`sbatch`-style wrappers are provided for
familiarity, but they are a compatibility layer rather than a scheduler.*
→ [Coming from HPC](reference/coming-from-hpc.md#there-is-no-slurm-here) ·
[Coming from HPC](reference/coming-from-hpc.md)

**Where the capacity comes from.** Without a lab workspace, researchers draw on a
school-wide shared research GPU pool: a baseline allocation, with occasional
boosts when capacity frees up, most notably over the summer when instructional
hardware would otherwise idle. Service Unit budgets divide the shared pool
equitably among the researchers drawing on it.

**Obtaining access.** Please request access through
[Research IT](https://research-it.ucsd.edu/computing/index.html), or
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) for the Research Cluster.
*Please describe the work, its approximate resource requirements, and the
timeframe.*

## The Working Environment

------------------------------------------------------------------------

**Signing in.** `ssh` to the login node with AD credentials; Duo applies, once
every 8 hours. *The VPN is not required for `ssh` — only for reaching a port
inside a container.* The browser route at
[datahub.ucsd.edu](https://datahub.ucsd.edu) is also available and is often the
quickest way to inspect something. → [Access](access/README.md)

**The login node is for launching jobs and moving files, not for computing.** It
is the one host every user passes through.
→ [The Login Node](access/the-login-node.md)

**Launching.**

```bash
launch-scipy-ml.sh -c 8 -m 32 -g 1 -l gpu-class=large
```

Bare `launch.sh` defaults to 1 CPU and 1GB; the wrapper scripts set 2 CPU and
8GB. A namespace permits **8 CPU / 64GB / 1 GPU** in total by default, with a
per-pod default of **8 CPU / 32GB / 1 GPU**; up to **32 CPU / 128GB** is
available on request. *Please ask.*
→ [`launch.sh` Reference](running-jobs/launch-sh-reference.md) ·
[The Six Requests](reference/getting-help.md#the-six-requests)

**Memory requests are half of limits.** `-m 32` reserves 16GB and permits 32GB.
The remainder is available only if the node has it spare, so *an identical job
may be `OOMKilled` on a busy afternoon and complete at midnight.* Please size for
the guarantee rather than the ceiling.

**Storage.** Research home directories are substantially larger than course ones
— on the order of 100GB — and are set up when access is provisioned. Beyond that
there is shared space, and optional mounts of external storage such as SDSC
Universal Scale Storage. → [Workspaces & Storage](workspaces-and-storage/README.md) ·
[Mounting External Storage](workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage)

**Software.** The Standard Software Images cover most requirements. Where they do
not, a custom image may be built; deriving from a standard image rather than
starting afresh is the supported path.
→ [Environments](environments/README.md)

**Containers run unprivileged**, under the member's own UID, with no root or sudo
inside the container, isolated within per-user Kubernetes namespaces. Dependency
installation has to work within that constraint.
→ [The Hard Boundary](environments/customizing-your-environment.md#the-hard-boundary)

## Running Substantial Work

------------------------------------------------------------------------

**Job modes.** Interactive for exploration; background (`-b`) for work which
should survive a disconnect; batch (`-B`) for runs which should simply
complete. → [Interactive, Background & Batch Modes](running-jobs/job-modes-and-limits.md#the-three-modes)

**Runtime.** Jobs default to 6 hours, and up to 12 may be set at launch. Longer
work is what reservations are for.
→ [The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit)

**Please checkpoint.** Between runtime limits, idle culling, reservation windows
and preemption there are several ways for a container to stop which have nothing
to do with the code it is running.
→ [Checkpointing](running-jobs/checkpointing.md)

**Observing a job.** → [Watching a Running Job](running-jobs/watching-your-job.md)

**Interpreting what happened.** A session emits Kubernetes Events with
reservation-specific reasons — `RuntimeGuaranteed`, `Preempted`,
`OnDemandLeaseDenied`, `OverstayRelinked`, `ReservationReassigned`.
→ [Kubernetes Events](running-jobs/kubernetes.md#reservation-events)

**Kubernetes directly** is available to advanced users.
→ [Kubernetes](running-jobs/kubernetes.md)

## Obtaining GPU Time

------------------------------------------------------------------------

Fall 2026 changes how GPU access is allocated. The full model is documented in
[GPU Access](gpu-access/README.md); what follows is what a researcher needs in order to
plan.

**Please select the smallest class the model fits within.** Five classes from
approximately 6GB to approximately 96GB. A larger class is not faster for a model
which fits in a smaller one; it is scarcer, and more expensive.
→ [GPU Classes](gpu-access/gpu-classes.md)

**Multi-day windows.** Research workspaces can permit multi-day reservations well
beyond the short caps that course groups use, so that a multi-day fine-tuning run
can be booked against guaranteed hardware. Member reservations cap at 48 hours,
within an absolute ceiling of 168 hours which nobody exceeds.
→ [Reservation Length Caps](gpu-access/reservations.md#reservation-length-caps)

**Borrowing covers the night before a deadline.** When a baseline is exhausted
and capacity would otherwise sit idle within roughly the next 12 hours, that
capacity may still be picked up.
→ [Quotas, Cohorts & Availability](gpu-access/quotas-and-availability.md)

**Launching without a reservation creates one and draws on the researcher's
budget.** There is no free exploratory launch. *A script which relaunches in a
loop can exhaust a budget window quickly, and nothing will intervene.*
→ [On-Demand Leases Charge Budget](gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

**Budget cycles.** Research SU budgets, if set, typically apply on a monthly or
quarterly basis rather than weekly.
→ [Budget Windows](gpu-access/service-units-and-budgets.md#budget-windows--cadences) ·
[Reading Your Balance](gpu-access/service-units-and-budgets.md#reading-your-balance)

**Returning capacity.** Releasing a window well in advance, or handing back the
tail of a session mostly used, carries no cancellation penalty — charges cover
the time actually used, and the remainder returns to the pool. Missing a window
without cancelling is the expensive case, at up to 50% of the booking, and an
individual researcher has no instructor to request a waiver from.
→ [The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

**Off-peak discounts** help steer usage away from peak evening hours. Work which
can run at midday or overnight costs less and waits less.
→ [Off-Peak Discounts & Rates](gpu-access/service-units-and-budgets.md#peak--off-peak-hours)

**Idle culling applies to research sessions as it does to any other**, on every
GPU class: roughly 30 minutes of an idle card, up to 6 hours when the cluster is
quiet, never within the first 45 minutes.
→ [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle)

## Data

------------------------------------------------------------------------

**Moving data.** Browser upload for small files; `scp`, `sftp`, `rsync`, `git`,
and Globus for substantial volumes.
→ [Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md)

**Sharing data.** With collaborators, with a group, or publicly, together with
the permission model beneath.
→ [Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace)

**Restricted and licensed datasets.** Some data available on the cluster carries
usage terms. → [Restricted & Licensed Datasets](workspaces-and-storage/datasets.md#restricted--licensed-datasets)

**Data classification** matters here more than anywhere else on the cluster.
**P4** — clinical records, export-controlled information — must not be used on
DSMLP at all. **P3** — legally or contractually protected information — **may be
permitted after review**, and vetting may take 4-6 weeks or longer.
→ [Policy](reference/policy.md)

## Publishing & Reproducibility

------------------------------------------------------------------------

Reproducibility is largely a container question: an image tag, the code, and a
checkpoint constitute a far better artifact than a home directory.
→ [Building & Publishing a Custom Image](environments/building-a-custom-image.md)

Access does not last indefinitely, and files do not survive its lapse. *Please
retrieve anything required before then.*
→ [Retrieving Work Before Access Ends](workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)

## Support

------------------------------------------------------------------------

Support routing differs for research users:

| Subject of the question | Please contact |
|---|---|
| The Research Cluster, Universal Scale Storage, research allocations | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| Datahub or DSMLP itself — the platform, images, launching | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| Which platform is appropriate for a given body of work | [Research IT](https://research-it.ucsd.edu/computing/index.html) |

We aim to resolve individual user issues within **1-2 business days**. Urgent or
broadly-scoped problems may be escalated through the
[IT Service Desk](https://support.ucsd.edu/); *please state plainly what is
affected.* → [Getting Help](reference/getting-help.md)

## Beyond DSMLP

------------------------------------------------------------------------

Work requiring tightly-coupled multi-node computation, MPI, a genuine batch
scheduler, or capacity at a scale this cluster does not carry belongs elsewhere;
[Research IT](https://research-it.ucsd.edu/computing/index.html) can connect
researchers with campus and national resources. A group large enough to warrant
its own guaranteed capacity is a matter for its PI, who should read
[Setting Up a Research Lab](faculty-research-lab.md).

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) or
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).
