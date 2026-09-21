# Setting Up a Research Lab

------------------------------------------------------------------------

This article is for faculty arranging Datahub/DSMLP access for a research group.
It covers whether the platform suits a group's work, the three routes to
capacity, how a lab workspace is established, storage, how GPU allocation and
borrowing work from Fall 2026, the researcher-contributed hardware pilot, and the
practices which keep a group out of difficulty.

Some of what follows is done by the PI or a group manager; some is performed by
our staff on request.

*Researchers working on their own rather than provisioning for others* are
covered by [Research on DSMLP](individual-researcher.md). *Course setup* is
covered by [Teaching with Datahub & DSMLP](instructor-or-ta.md).

## Deciding Whether the Platform Suits the Work

------------------------------------------------------------------------

**Well suited:** single-node GPU work at every size from a 6GB slice to a full
H100; interactive analysis; long-running batch jobs; and a shared software
environment an entire group can rely upon. Lab members receive the same tooling
students use, which makes the barrier for a new rotation student close to nil.

**Not suited:** there is no Slurm scheduler, no MPI, and no multi-node
parallelism. Workloads of that shape belong elsewhere, and
[Research IT](https://research-it.ucsd.edu/computing/index.html) can direct them
to a more appropriate platform.

**Instruction has priority.** During 10th and Finals Weeks and at major
assignment deadlines, coursework is served ahead of research. A lab workspace
with its own quota insulates a group from most of this; a lab working out of the
shared pool experiences it.

**Three routes to capacity**, which may be combined:

| Route | Provides | Cost |
|---|---|---|
| The shared research pool | A baseline allocation, with boosts when capacity frees up — most notably over Summer | None; please request access |
| A lab workspace with its own quota | Guaranteed access up to the group's quota, date-aware so that it may flex around the group's deadlines | None for compute; storage above 1TB is chargeable |
| Contributing hardware *(pilot)* | Exclusive reservation rights over the contributed capacity | Purchase of the hardware — see [below](#contributing-hardware-pilot) |

**Cost.** Compute is provided at no charge. Storage above 1TB is not. There is no
compute recharge or chargeback mechanism. *Work sitting within a self-supporting
program is subject to cost recovery; please contact us to discuss.*

## Establishing a Lab Workspace

------------------------------------------------------------------------

Users are divided into groups called **workspaces**, which anchor all cluster
configuration: rosters, storage, container images, GPU access, and storage and
GPU quotas. Lab and research workspaces are manually curated by Research IT
services rather than auto-populated from a course roster.
→ [What a Workspace Is](workspaces-and-storage/what-a-workspace-is.md)

**To request one**, please contact
[Research IT](https://research-it.ucsd.edu/computing/index.html) or
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu), with:

- Who is in the group, and who besides the PI should be able to manage it
- What the group runs — frameworks, model sizes, and whether GPU memory or GPU
  count is the binding constraint
- The data: how much, where it currently resides, and its classification
- Any recurring deadline shapes we should know about

**Membership.** People join and depart; a departing postdoc's files do not leave
with them, and a new arrival should not require a week to become productive.
→ [Managing a Group](reference/managing-a-group.md)

**What a manager may and may not do.** A manager may view the group's calendar,
book on a member's behalf, and waive a cancellation charge. A manager may **not**
edit Service Unit budgets or group limits from the application; those are
administrative actions. *Requesting a change by ticket is the normal and
sanctioned route.*
→ [The Six Requests](reference/getting-help.md#the-six-requests)

## Storage

------------------------------------------------------------------------

**Per-member storage.** Research home directories are on the order of 100GB each,
established at provisioning. Group shared space and external mounts sit alongside
them. → [Directories, Quotas & Cleaning Up](workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Shared lab space**, for datasets everyone works from — the alternative to every
member holding a personal copy, *which is how a group exhausts its allocation.*

**External storage.** SDSC Universal Scale Storage and similar may be mounted
into a group's containers. Capacity thresholds govern what is mounted where.
→ [Mounting External Storage](workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage)

**Storage above 1TB is chargeable.**

**Sharing outward**, to collaborators inside and outside UC San Diego, with group
permissions and public access.
→ [Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace)

**Data classification is a provisioning question rather than a later one.** **P4**
— clinical records, export-controlled information — may not be used on DSMLP.
**P3** may be permitted after review, and vetting may take 4-6 weeks or longer.
*Please raise either in the first conversation.*
→ [Policy](reference/policy.md)

## Compute Allocation

------------------------------------------------------------------------

**GPU classes.** Five size classes from approximately 6GB to approximately 96GB.
Each workspace is given access to one or more classes, matching anticipated work.
→ [GPU Classes](gpu-access/gpu-classes.md)

**The group quota** sets the maximum number of each GPU class a lab may hold at
once. Quotas are date-aware: staff can set them week-by-week or even day-by-day,
so a lab's share may surge for a conference deadline and drop back afterwards
without a permanent allocation.
→ [Quotas, Cohorts & Availability](gpu-access/quotas-and-availability.md)

**Borrowing beyond the quota.** Quotas are not hard ceilings: last-minute jobs,
under roughly 12 hours ahead, may use idle capacity beyond their group's quota.
If GPUs would otherwise sit dark, a group which has exhausted its share may still
pick them up.

**Borrowing carries a seniority, which matters for hardware contributors.**
Course workspaces always hold **senior** borrowing rights. **Junior** borrowing —
which yields first when a senior borrower or a quota-holder requires the capacity
— is granted to hardware contributors. *Junior capacity is real capacity; it is
simply the first to be given back.*

**Service Unit budgets** divide a group's capacity among its members, by the same
mechanism courses use to divide capacity across a roster. Research budgets
typically apply on a monthly or quarterly basis. *Budgets are set
administratively; please request changes by ticket.*
→ [Service Units & Budgets](gpu-access/service-units-and-budgets.md) ·
[Budget Windows](gpu-access/service-units-and-budgets.md#budget-windows--cadences)

**Cohorts.** A collection of groups may have quotas summing to greater than the
physical capacity allocated to the cohort, allowing groups to flexibly share
access to greater peak capacity. *A consequence worth anticipating: availability
may read zero while a group still has headroom on paper.*
→ [Cohorts](gpu-access/quotas-and-availability.md#cohorts)

**Reports.** Manager reports cover reservations by group, peak simultaneous use
by class, reserved hours, and effective limits. *Note that some display
cluster-wide data rather than only the group itself.*
→ [Managing a Group](reference/managing-a-group.md#what-the-reports-cover)

## Contributing Hardware (Pilot)

------------------------------------------------------------------------

*A pilot project is underway to evaluate placement of researcher-contributed GPUs
and/or servers into the cluster. We expect this pilot to continue through Spring
2027, at which point we will determine if this capability can be made available
to a broader audience.*

Under this scheme, contributors receive:

- **Exclusive reservation rights over their contributed capacity** — the lab's
  group GPU limits match its contribution, and the cohort holding contributor
  groups is not overcommitted, so reservations mean the lab can always book "its"
  GPUs ahead, whenever it needs them;
- **Access to the school-wide shared pool**, like any other research group;
- **Access to near-term otherwise-idle capacity** across the cluster, via the
  borrowing facility at junior priority — the route by which a lab reaches beyond
  its own contribution when GPUs would otherwise sit idle;
- The ability to temporarily **loan** capacity and privileges to other groups.

When the contributed GPUs sit idle, they become available for last-minute and
on-demand use by others — so contributed hardware never sits dark — but the
reservation system guarantees the contributing lab retains first claim on its own
capacity.

**What it requires of a contributor.** Hardware conforming to the cluster's
supported configurations, and a conversation well before purchase. *Please speak
with us at the specification stage rather than after delivery.*

## Software & Environments

------------------------------------------------------------------------

**Standard Software Images** suffice for most groups: `datascience-notebook`,
`scipy-ml-notebook` (CUDA, PyTorch, TensorFlow), and `rstudio-notebook`.
→ [Standard Images](environments/standard-images.md)

**A lab image.** A lab may bake in its environment so that every member receives
the same stack and a new arrival is productive on their first day. *Please derive
from a Standard Image where possible; that is the supported path.*
→ [Building & Publishing a Custom Image](environments/building-a-custom-image.md)

**Pinning.** A workspace may pin an image so that members are not moved by a
quarterly update partway through a project.
→ [Pinning a Workspace](environments/standard-images.md#pinning-a-workspace)

**Containers run unprivileged**, under each user's own UID, with no root or sudo
inside the container. *This shapes how dependencies are installed.*
→ [The Hard Boundary](environments/customizing-your-environment.md#the-hard-boundary)

## Operating a Lab

------------------------------------------------------------------------

**Onboarding.** Please direct new members to
[Research on DSMLP](individual-researcher.md), which assumes a shell and covers
launching, storage, and the GPU model. Three things come from the lab rather than
from the documentation: the group's storage conventions, which GPU class its work
actually requires, and that an idle GPU session is reclaimed.

**Practices which keep a group out of difficulty:**

- **Checkpoint anything long-running.** Runtime limits, idle culling, and
  preemption all end containers for reasons unrelated to the code they run.
  → [Checkpointing](running-jobs/checkpointing.md)
- **Book the smallest class which fits.** A larger class is not faster for a
  model which fits in a smaller one; it is scarcer and more expensive.
- **Shut down what nobody is using.** An idle container continues to hold its
  CPU, memory and GPU against the group's quota.
- **Cancel unused windows.** Cancelling in advance carries no penalty; a no-show
  is charged at up to 50% of the booking.
  → [The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

**Off-peak discounts** make work which can run at midday or overnight both
cheaper and faster to obtain.
→ [Off-Peak Discounts & Rates](gpu-access/service-units-and-budgets.md#peak--off-peak-hours)

**Scheduled Maintenance.** On the instruction side, Datahub may be unavailable
Tuesdays, 6-8AM for time-sensitive updates or security patches; *this work is
generally limited to a subset of worker nodes, in which case running jobs are
unaffected.*

**The Research Cluster window is less frequent and considerably more
disruptive.** Rather than a weekly slot it runs **quarterly, at the break between
terms**, with approximately **7 days' notice — and all running jobs are
terminated.** Anything long-running must be checkpointed or completed before that
window.
→ [Maintenance Closures](gpu-access/what-ends-a-session.md#maintenance-closures)

**Lifecycle.** Members arrive and depart, and access has an end. *Please
establish what becomes of a departing member's files.*
→ [When Access Starts & Ends](access/when-access-starts-and-ends.md)

## Caveats & Limitations

------------------------------------------------------------------------

**No Sensitive Data:** as above — P4 may not be used; P3 may be permitted after
review, with vetting of 4-6 weeks or longer.

**Availability and Reliability:** Datahub and DSMLP were designed with student
workloads in mind, deliberately trading some of the costly redundancy typical of
financial or health settings for additional capacity and capability. As such,
they should not be used to host externally-available services or applications
except as required for coursework or projects. *(This caveat applies primarily to
the compute nodes executing user jobs; critical components such as networking,
file storage, and backups are maintained to Enterprise IT standards.)*

**Appropriate Use:** The campus-wide
[IT Acceptable Use Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html)
applies to use of Datahub and DSMLP.

------------------------------------------------------------------------

- **Research IT / Research Cluster:**
  [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) ·
  [research-it.ucsd.edu](https://research-it.ucsd.edu/computing/index.html)
- **Datahub / DSMLP platform:** [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
- **IT Service Desk:** [support.ucsd.edu](https://support.ucsd.edu/)

We aim to resolve individual user issues within 1-2 business days.
→ [Getting Help](reference/getting-help.md)
