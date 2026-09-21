# Glossary

Terms used across this documentation set, alphabetically. *Where a term has a
page of its own, the definition here is the one-line form and the link is the
authority.*

## A-C

------------------------------------------------------------------------

**Active Directory (AD)** — the campus credential set. An AD username and
password, with Duo, authenticate to both Datahub and the login node.
→ [Datahub in the Browser](../access/datahub-in-the-browser.md)

**Anchor mode** — how a Service Unit budget window is fixed to the calendar: what
"weekly" is weekly *from*. Which modes are configured here is not settled.
→ [Budget Windows](../gpu-access/service-units-and-budgets.md#budget-windows--cadences)

**Auditor** — a read-only privilege tier held by staff.
→ [Managing a Group](managing-a-group.md)

**Background pod (`-b`)** — a pod created and left running while the shell
returns to the login node. The session is not placed inside it, and exiting a pod
does not stop processes started in it. *Distinct from `&`, which backgrounds a
process rather than a pod.* → [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

**Batch job (`-B`)** — a job run to completion unattended. `-B -- <command>` is
the usual form. → [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

**Best-effort reservation** — a session that runs now, free of a wait, and accepts
preemption from its first tick. It holds nothing and is protected by nothing.
→ [Best-Effort Reservations](../gpu-access/reservations.md#best-effort-reservations)

**Borrowing** — using idle GPU capacity beyond a workspace's quota, available
to work starting under roughly 12 hours ahead. **Course workspaces always borrow
senior**, meaning they are not the first asked to give capacity back.
→ [Quotas, Cohorts & Availability](../gpu-access/quotas-and-availability.md)

**Budget window** — the period a Service Unit budget covers before it renews.
Weekly for courses; monthly or quarterly for research, where one is set at all.
→ [Budget Windows](../gpu-access/service-units-and-budgets.md#budget-windows--cadences)

**Claim window** — the **15 minutes** within which a session must be started on a
booked reservation. Missed, the reservation is cancelled, the capacity returns to
the pool, and the window is gone for its remainder.
→ [The Claim Window](../gpu-access/reservations.md#the-claim-window)

**Cluster status page** — [`datahub.ucsd.edu/hub/status`](https://datahub.ucsd.edu/hub/status),
which lists the GPU models on each node and how many are free.
→ [The Status Page](../gpu-access/quotas-and-availability.md#the-status-page)

**Cohort** — a group of workspaces whose quotas may deliberately sum to more than
the physical capacity behind them, allowing a higher shared peak. A consequence:
availability may read zero while a workspace has headroom on paper.
→ [Cohorts](../gpu-access/quotas-and-availability.md#cohorts)

**Container** — the isolated environment one job runs in, built from an image and
run under the member's own UID without root.
→ [Standard Images](../environments/standard-images.md)

**Course workspace** — a workspace covering one course: its lecture timeslots
together with the discussion sections associated with them. *A discussion
section does not get a workspace of its own.*
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

**Cull** — see *Idle culling*.

## D-G

------------------------------------------------------------------------

**Datahub** — [`datahub.ucsd.edu`](https://datahub.ucsd.edu), the browser front
door: JupyterHub, the environment menu, and the services that hang off it.
→ [Datahub in the Browser](../access/datahub-in-the-browser.md)

**`datahub-base-notebook`** — the smallest standard image, sitting below
`datascience-notebook`. The one to derive from when build time matters.

**`datascience-notebook`** — the standard CPU image: widely-used data analysis
libraries from the Python, R and Julia communities.

**`/datasets`** — the cluster-wide tree where shared corpora are staged, read in
place rather than copied. → [Shared Datasets](../workspaces-and-storage/datasets.md)

**`DeadlineExceeded`** — the pod status meaning the runtime limit was reached. Not
an error in the code. → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

**disk-quota-service** — the service reporting usage against quota, under the
**Services** tab at
[`datahub.ucsd.edu/hub/spawn`](https://datahub.ucsd.edu/hub/spawn). It also
displays the workspace ID. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**DSMLP** — the Data Science / Machine Learning Platform: the on-premises cluster
of CPU and GPU nodes underneath everything in this documentation.

**`dsmlp-login.ucsd.edu`** — the login node. See *Login node*.

**Duo** — the campus two-factor prompt, which applies to both web and SSH access.

**GHCR** — the GitHub Container Registry, where the standard images are published
as `ghcr.io/ucsd-ets/<image>:<tag>`. *The older `ucsdets/<image>` naming is also
in circulation.* → [Standard Images](../environments/standard-images.md)

**`git-pull` link** — a URL that fetches a repository into an environment,
commonly used to distribute course materials. Its commonest failure is being
clicked before the student has signed in.
→ [Sign-In & Session Problems](../access/sign-in-and-session-problems.md)

**Globus** — a transfer service used for moving data in and out at volume.
→ [Moving & Sharing Data](../workspaces-and-storage/moving-and-sharing-data.md)

**GPU class** — a size band rather than a hardware model: `extra-small`, `small`,
`medium`, `large`, `extra-large`, requested with `-l gpu-class=<class>`. Each
workspace is granted access to one or more. → [GPU Classes](../gpu-access/gpu-classes.md)

**Grader account** — the single shared account each course receives for nbgrader
and formgrader. It holds write permission on the workspace's `public/` directory;
an instructor's own account does not. → [Grading](../grading/README.md)

**Group manager** — see *Workspace manager*.

## H-L

------------------------------------------------------------------------

**Home directory** — per-user, per-workspace storage. A member holds a separate
one in every workspace they belong to. Course homes run 5-10 GB; research homes
are on the order of 100 GB. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Idle culling** — reclaiming a GPU from a session that has stopped using it:
roughly 30 minutes of idleness on a busy cluster, up to 6 hours on a quiet one,
never in a session's first 45 minutes. A warning precedes it, and a cull is not a
crash. *CPU-only sessions are not culled by this mechanism.*
→ [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

**Image** — the packaged filesystem a container starts from. See *Standard image*.

**Jumpbox** — what the login node is: a machine for launching jobs and moving
files, not for computing. → [The Login Node](../access/the-login-node.md)

**JupyterHub / JupyterLab** — the hub that spawns a session, and the notebook
interface it spawns. Swapping `lab` for `tree` in the URL reaches the older
Notebook interface.

**Kubernetes** — the orchestration system underneath the platform. Every job is a
pod in a per-user namespace. → [Kubernetes](../running-jobs/kubernetes.md)

**`kubesh <pod-id>`** — the command that enters one of an account's own running
pods from the login node.

**`launch.sh`** — the launcher, at `/opt/launch-sh/bin/launch.sh`, which maps
command-line parameters into a Kubernetes pod definition. Bare, it gives 1 CPU /
1 GB / 0 GPU. → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**Launch wrapper** — `launch-scipy-ml.sh`, `launch-datascience.sh` and their
relatives: scripts that set environment variables and then hand off to
`launch.sh`. They give 2 CPU / 8 GB / 0 GPU.

**Limit and request** — the two numbers Kubernetes holds for CPU and memory. **The
number passed is the limit; the request — what is actually reserved — is half of
it.** GPUs are exempt. → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**Login node** — `dsmlp-login.ucsd.edu`, reached by SSH with AD credentials and
Duo, and requiring the VPN from off campus. It shares a filesystem with the
containers. `~` there is the **personal** area, not any course home.
→ [Connecting over SSH](../access/the-login-node.md#connecting-over-ssh)

## M-P

------------------------------------------------------------------------

**Manual resetter** — a service under the **services** dropdown at
`datahub.ucsd.edu` that stops an account's servers, signs it out and resets its
profile, preserving files. The remedy for a stale profile or a broken package in
an account's own `.local`. → [Sign-In & Session Problems](../access/sign-in-and-session-problems.md)

**Member** — the ordinary privilege tier: a student in a course, a member of a
lab. → [Managing a Group](managing-a-group.md)

**Namespace** — the per-user Kubernetes namespace pods run in, and the unit
one of the three resource tiers is expressed against — 8 CPU / 64 GB / 1 GPU by
default, across everything running at once.

**nbgrader** — the in-platform assignment distribution, collection and grading
tool. Grade export to Canvas is manual. → [Grading](../grading/README.md)

**`NoSchedule` taint** — the Kubernetes mechanism that keeps pods off a node
unless they carry a matching toleration. **`medium` and above carry them**, and a
GPU request with no `gpu-class` label fails with `0/5 nodes available`.
→ [Error Messages](error-messages.md)

**Off-peak** — the discounted hours, which steer usage away from peak evening
demand. → [Off-Peak Discounts](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours)

**On-demand lease** — the reservation the system creates when a GPU session is
launched without a booking having been made. **It draws on the Service Unit
budget exactly as a booked window would**; there is no free exploratory launch.
→ [On-Demand Leases Charge Budget](../gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

**`OOMKilled`** — the pod status meaning the container reached its memory limit.
Frequently caused by the request/limit halving rather than by the number
requested. → [Error Messages](error-messages.md)

**Otter-Grader, Gradescope** — grading tools used on the platform alongside
nbgrader. → [Choosing a Grading Tool](../grading/choosing-a-grading-tool.md)

**Overstay** — a session continuing to run past the end of its guaranteed window.
Nothing stops it; the time is no longer covered by what was booked, and the
session has no protection.
→ [What Ends a Session](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill)

**Pinning** — fixing a workspace to a dated image tag so that its members are not
moved by a quarterly image update mid-term.
→ [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace)

**Pod** — one running container as Kubernetes sees it. Pod IDs look like
`ubellur-27068`, and `kubectl get pods` lists the pods in an account's own
namespace.

**Pod label (`-l key=value`)** — an attribute attached to a pod at launch,
repeatable. This is how `gpu-class` is set.

**Preemption** — a session ending because the capacity it held was needed for
somebody's booking. A capacity outcome, not a fault.
→ [What Ends a Session](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill)

**`private/`** — a per-user, cluster-wide directory. It appears unchanged in
every workspace and draws on the **personal** quota rather than any
workspace's. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**`public/`** — the workspace's shared area, readable by every member and written
by the grader account in a course. Draws on the workspace quota.

**P3 / P4** — University of California data protection levels. **P4 is prohibited
here. P3 may be permitted after review**, and vetting may take 4-6 weeks or
longer. → [Policy](policy.md)

## Q-S

------------------------------------------------------------------------

**Quota, GPU** — the ceiling on how many GPUs of each class a *workspace* may
hold at one time. Date-aware: it can be raised for a deadline week and revert on
its own. Not the same as a Service Unit budget.
→ [Quotas, Cohorts & Availability](../gpu-access/quotas-and-availability.md)

**Quota, storage** — two separate pools. The **workspace** pool covers the
workspace home, `public/` and `teams/`; the **personal** pool covers `private/`
and follows the member into every workspace.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**Research Cluster** — the research-facing service, supported by Research IT at
`rcd-support@ucsd.edu`, with its own maintenance window: quarterly, at the break
between terms, about 7 days' notice, and all running jobs terminated.

**Reservation** — a booked window during which GPU capacity is held and a session
is admitted ahead of the walk-up queue. **A guarantee of access, not a running
job** — the session is still launched as usual.
→ [Reservations](../gpu-access/reservations.md)

**Reserve floor** — capacity ITS keeps unborrowable in each GPU class. *Idle is
therefore not the same as available.*

**Resource tiers** — the three limits that apply to a job: a single pod
(8 CPU / 32 GB / 1 GPU), the namespace in total (8 CPU / 64 GB / 1 GPU), and what
is available on request (up to 32 CPU / 128 GB). **All three are defaults, not
maxima.** → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**`rstudio-notebook`** — `datascience-notebook` plus the RStudio environment.
**Derives from the CPU image and is not GPU-enabled.**

**Runtime limit** — the deadline on a container: **6 hours** by default, up to
**12** if set at launch, longer only by arrangement. One of three clocks
that can end a job. → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

**`scipy-ml-notebook`** — `datascience-notebook` plus CUDA/GPU tooling,
TensorFlow and PyTorch. The default image for bare `launch.sh`.

**Senior and junior borrowing** — the seniority attached to borrowed capacity.
Course workspaces always borrow senior; junior borrowing yields first.

**Service Unit (SU)** — a usage credit for GPU time. Each class carries an hourly
rate, budgets are per-workspace and set administratively, and a reservation's cost
is computed up front. → [Service Units & Budgets](../gpu-access/service-units-and-budgets.md)

**Slurm compatibility wrappers** — `sbatch`, `srun`, `squeue` and `scancel`,
which translate into `launch.sh`. **There is no Slurm scheduler behind them, and
no MPI or multi-node support.** → [Coming from HPC](coming-from-hpc.md#there-is-no-slurm-here)

**Spawn** — starting a browser session from a course's environment menu. A
*spawn failure* is the message returned when it will not start, and it does not
say why. → [Sign-In & Session Problems](../access/sign-in-and-session-problems.md)

**Standard image** — one of the three images IT Services maintains:
`datascience-notebook`, `scipy-ml-notebook` and `rstudio-notebook`. They receive
priority support. → [Standard Images](../environments/standard-images.md)

## T-Z

------------------------------------------------------------------------

**Team** — a group within a workspace, holding data scoped to some of its members
— a project group, a lab bench, a capstone team. `launch.sh -G list` prints the
teams an account belongs to; `-G <teamid>` launches with that team's data
visible. *Note `-g` is GPU count and `-G` is group.*
→ [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

**Team mode** — a reservation feature in which teammates can act on one another's
bookings. **A teammate can cancel another member's booking, and that penalty
cannot be waived.** → [Team Mode](../gpu-access/reservations.md#team-mode)

**`teams/`** — the directory where team-scoped data appears. Draws on the
workspace quota. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**TPOC (Technical Point of Contact)** — the person a course nominates to lead its
customization work. A designation for support purposes rather than a privilege
tier. → [Managing a Group](managing-a-group.md)

**TritonLink / TSS** — the registration systems course rosters auto-populate from.
Auditors and observers are not on them and are added through Canvas.
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md)

**Universal Scale Storage (USS)** — SDSC storage that can be mounted onto the
cluster, supported by Research IT.
→ [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage)

**Unprivileged container** — a container running under the member's own UID with
no root and no `sudo`, in a per-user Kubernetes namespace. `sudo apt-get` fails
by design. → [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary)

**Workspace** — the unit everything hangs off: one per course, lab, or catch-all
population. It anchors roster, storage, container images, GPU class access,
quotas and budgets. Named at launch with `-W`; listed by `workspace --list`.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

**Workspace manager** — the privilege tier held by an instructor, a TA or a PI.
May view the group calendar, book on a member's behalf, and waive a cancellation
charge; may **not** edit Service Unit budgets or group limits.
→ [Managing a Group](managing-a-group.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
