# Glossary

This page defines terms used across the Datahub and DSMLP documentation, in
alphabetical order. Each entry links to the page that covers the term in full.

## A-C

| Term | Definition | Reference |
|---|---|---|
| Active Directory (AD) | The campus credential set, whose username and password, with Duo, authenticate to both Datahub and the login node. | [Datahub in the Browser](../access/datahub-in-the-browser.md) |
| Anchor mode | The rule that fixes a Service Unit budget window to the calendar, setting the point from which the window is measured. | [Anchor Modes](../gpu-access/service-units-and-budgets.md#anchor-modes) |
| Auditor | A read-only privilege tier held by staff. | [Managing a Group](managing-a-group.md) |
| Background pod (`-b`) | A pod created and left running while the shell returns to the login node. | [Background Pods](../running-jobs/job-modes-and-limits.md#background-pods) |
| Batch job (`-B`) | A job run to completion unattended. | [Batch Jobs](../running-jobs/job-modes-and-limits.md#batch-jobs) |
| Best-effort reservation | A session that runs immediately, without a wait, holds no capacity, and may be preempted from the moment it starts. | [Best-Effort Reservations](../gpu-access/reservations.md#best-effort-reservations) |
| Borrowing | The use of idle GPU capacity beyond a workspace's quota. | [Borrowing Beyond Quota](../gpu-access/quotas-and-availability.md#borrowing-beyond-quota) |
| Budget window | The period a Service Unit budget covers before it renews. | [Budget Windows & Cadences](../gpu-access/service-units-and-budgets.md#budget-windows--cadences) |
| Claim window | The period at the start of a booked reservation within which a session must be started to claim it. | [The Claim Window](../gpu-access/reservations.md#the-claim-window) |
| Cluster status page | The page at [`datahub.ucsd.edu/hub/status`](https://datahub.ucsd.edu/hub/status) that lists the GPU models on each node and how many are free. | [The Status Page](../gpu-access/quotas-and-availability.md#the-status-page) |
| Cohort | A group of workspaces whose quotas may sum to more than the physical capacity behind them, so that availability can read zero while a workspace has headroom. | [Cohorts](../gpu-access/quotas-and-availability.md#cohorts) |
| Container | The isolated environment one job runs in, built from an image and run under the member's own UID without root. | [Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages) |
| Course workspace | A workspace covering one course: its lecture timeslots and the discussion sections associated with them. | [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md) |
| Cull | Short form of idle culling. | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |

## D-G

| Term | Definition | Reference |
|---|---|---|
| Datahub | The browser interface at [`datahub.ucsd.edu`](https://datahub.ucsd.edu), comprising JupyterHub, the environment menu, and the services attached to it. | [Datahub in the Browser](../access/datahub-in-the-browser.md) |
| `datahub-base-notebook` | The smallest image in the standard image hierarchy, below `datascience-notebook`, and the base to derive from when build time matters. | [Standard Images, Tags, and Pinning](../environments/standard-images.md) |
| `datascience-notebook` | The standard CPU image, containing widely used data analysis libraries from the Python, R, and Julia communities. | [Standard Images](../environments/standard-images.md#standard-images) |
| `/datasets` | The cluster-wide directory tree where shared corpora are staged, to be read in place rather than copied. | [Datasets](../workspaces-and-storage/datasets.md) |
| `DeadlineExceeded` | The pod status reported when a container reaches the runtime limit, which does not indicate an error in the code. | [The `DeadlineExceeded` Status](../running-jobs/job-modes-and-limits.md#the-deadlineexceeded-status) |
| disk-quota-service | The service under the **Services** tab at [`datahub.ucsd.edu/hub/spawn`](https://datahub.ucsd.edu/hub/spawn) that reports usage against quota and displays the workspace ID. | [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| DSMLP | The Data Science / Machine Learning Platform, the on-premises cluster of CPU and GPU nodes on which Datahub sessions and command-line jobs run. | [Datahub and DSMLP Overview](../overview.md) |
| `dsmlp-login.ucsd.edu` | The hostname of the login node. | [Connecting over SSH](../access/the-login-node.md#connecting-over-ssh) |
| Duo | The campus two-factor prompt, which applies to both web and SSH access. | [Duo Authentication](../access/the-login-node.md#duo-authentication) |
| GHCR | The GitHub Container Registry, where the standard images are published as `ghcr.io/ucsd-ets/<image>:<tag>`. | [Standard Images, Tags, and Pinning](../environments/standard-images.md) |
| `git-pull` link | A URL that fetches a repository into an environment, commonly used to distribute course materials. | [Sign-In & Session Problems](../access/sign-in-and-session-problems.md) |
| Globus | A transfer service for moving large volumes of data in and out of the platform. | [Moving & Sharing Data](../workspaces-and-storage/moving-and-sharing-data.md) |
| GPU class | A GPU size band, rather than a hardware model, requested with `-l gpu-class=<class>`; each workspace is granted access to one or more classes. | [GPU Classes](../gpu-access/gpu-classes.md) |
| Grader account | The single shared account each course receives for nbgrader and formgrader, which, unlike an instructor's own account, holds write permission on the workspace's `public/` directory. | [Grader Account](../grading/notebook-grading-workflow.md#grader-account) |
| Group manager | Another name for workspace manager. | [Managing a Group](managing-a-group.md) |

## H-L

| Term | Definition | Reference |
|---|---|---|
| Home directory | Per-user, per-workspace storage, of which a member holds a separate one in every workspace they belong to. | [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| Idle culling | The reclaiming of a GPU from a session that has stopped using it. | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| Image | The packaged filesystem a container starts from. | [Standard Images, Tags, and Pinning](../environments/standard-images.md) |
| Jumpbox | Another name for the login node: a machine for launching jobs and moving files, on which running computation is prohibited. | [What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for) |
| JupyterHub / JupyterLab | The hub that spawns a session, and the notebook interface it spawns; replacing `lab` with `tree` in the URL reaches the older Notebook interface. | [Datahub in the Browser](../access/datahub-in-the-browser.md) |
| Kubernetes | The orchestration system on which the platform runs, in which every job is a pod in a per-user namespace. | [Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md) |
| `kubesh <pod-id>` | The command that enters one of an account's own running pods from the login node. | [A Second Shell with `kubesh`](../access/the-login-node.md#a-second-shell-with-kubesh) |
| `launch.sh` | The launcher at `/opt/launch-sh/bin/launch.sh`, which maps command-line parameters into a Kubernetes pod definition. | [`launch.sh` Reference](../running-jobs/launch-sh-reference.md) |
| Launch wrapper | A script such as `launch-scipy-ml.sh` or `launch-datascience.sh` that sets environment variables and then hands off to `launch.sh`. | [Default Resources](../running-jobs/launch-sh-reference.md#default-resources) |
| Limit and request | The two values Kubernetes holds for CPU and memory: the limit is the value passed at launch, and the request is the amount actually reserved. | [Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits) |
| Login node | The host `dsmlp-login.ucsd.edu`, reached by SSH with AD credentials and Duo, whose home directory `~` is the personal area rather than a course home. | [Connecting over SSH](../access/the-login-node.md#connecting-over-ssh) |

## M-P

| Term | Definition | Reference |
|---|---|---|
| Manual resetter | A service under the **services** dropdown at `datahub.ucsd.edu` that stops an account's servers, signs it out, and resets its profile while preserving files. | ["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed) |
| Member | The ordinary privilege tier, held by a student in a course or a member of a lab. | [Managing a Group](managing-a-group.md) |
| Namespace | The per-user Kubernetes namespace that pods run in, and the unit against which one of the resource tiers applies across everything running at once. | [Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers) |
| nbgrader | The in-platform tool for distributing, collecting, and grading assignments, from which grade export to Canvas is manual. | [Grading](../grading/README.md) |
| `NoSchedule` taint | The Kubernetes mechanism that keeps pods off a node unless they carry a matching toleration. | [Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label) |
| Off-peak | The discounted hours outside the peak evening period. | [Peak & Off-Peak Hours](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours) |
| On-demand lease | The reservation the system creates when a GPU session is launched without a booking, which draws on the Service Unit budget as a booked window does. | [On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges) |
| `OOMKilled` | The pod status reported when a container reaches its memory limit. | [Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits) |
| Otter-Grader, Gradescope | Grading tools used on the platform alongside nbgrader. | [Choosing a Grading Tool & Interface](../grading/choosing-a-grading-tool.md) |
| Overstay | Running a session past the end of its guaranteed window, on time the booking does not cover and without protection. | [Overstay](../gpu-access/what-ends-a-session.md#overstay) |
| Pinning | Fixing a workspace to a dated image tag so that its members are not moved by a quarterly image update mid-term. | [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace) |
| Pod | One running container as Kubernetes represents it; `kubectl get pods` lists the pods in an account's own namespace. | [Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md) |
| Pod label (`-l key=value`) | A repeatable attribute attached to a pod at launch, and the means by which `gpu-class` is set. | [Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags) |
| Preemption | The ending of a session because the capacity it held is needed for a booking. | [Preemption](../gpu-access/what-ends-a-session.md#preemption) |
| `private/` | A per-user, cluster-wide directory that appears unchanged in every workspace and draws on the personal quota rather than any workspace's. | [Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live) |
| `public/` | The workspace's shared area, readable by every member, written by the grader account in a course, and drawing on the workspace quota. | [Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live) |
| P3 / P4 | University of California data protection levels: P4 data is prohibited on the platform, and P3 data may be permitted after review. | [Data Classification](policy.md#data-classification) |

## Q-S

| Term | Definition | Reference |
|---|---|---|
| Quota, GPU | The ceiling on how many GPUs of each class a workspace may hold at one time, separate from a Service Unit budget. | [What a Quota Is](../gpu-access/quotas-and-availability.md#what-a-quota-is) |
| Quota, storage | Two separate pools: the workspace pool, covering the workspace home, `public/`, and `teams/`, and the personal pool, covering `private/` and following the member into every workspace. | [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| Research Cluster | The research-facing service supported by Research IT at `rcd-support@ucsd.edu`, whose scheduled maintenance terminates all running jobs. | [Scheduled Maintenance](policy.md#scheduled-maintenance) |
| Reservation | A booked window during which GPU capacity is held and a session is admitted ahead of the walk-up queue; the session is still launched as usual. | [Reservations](../gpu-access/reservations.md) |
| Reserve floor | Capacity that ITS keeps unborrowable in each GPU class, so that idle capacity is not always available. | [The Reserve Floor](../gpu-access/quotas-and-availability.md#the-reserve-floor) |
| Resource tiers | The three levels at which resource limits apply to a job: a single pod, the namespace in total, and what is available on request. | [Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers) |
| `rstudio-notebook` | The standard image that adds the RStudio environment to `datascience-notebook`; it derives from the CPU image and is not GPU-enabled. | [Standard Images](../environments/standard-images.md#standard-images) |
| Runtime limit | The deadline on how long a container may run. | [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| `scipy-ml-notebook` | The standard image that adds CUDA/GPU tooling, TensorFlow, and PyTorch to `datascience-notebook`, and the default image for bare `launch.sh`. | [Standard Images](../environments/standard-images.md#standard-images) |
| Senior and junior borrowing | The seniority attached to borrowed capacity, under which junior borrowing yields first. | [Borrowing Beyond Quota](../gpu-access/quotas-and-availability.md#borrowing-beyond-quota) |
| Service Unit (SU) | A usage credit for GPU time, spent at an hourly rate that each GPU class carries. | [What a Service Unit Is](../gpu-access/service-units-and-budgets.md#what-a-service-unit-is) |
| Slurm compatibility wrappers | The commands `sbatch`, `srun`, `squeue`, and `scancel`, which translate into `launch.sh` and have no Slurm scheduler behind them. | [Slurm Compatibility Wrappers](coming-from-hpc.md#slurm-compatibility-wrappers) |
| Spawn | Starting a browser session from a course's environment menu; a spawn failure is the message returned when the session does not start, and it does not state the cause. | ["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed) |
| Standard image | One of the images ITS maintains, which receive priority support. | [Standard Images](../environments/standard-images.md#standard-images) |

## T-Z

| Term | Definition | Reference |
|---|---|---|
| Team | A group within a workspace, such as a project group, a lab bench, or a capstone team, holding data scoped to some of its members. | [Sections, Teams and Group Data](../workspaces-and-storage/what-a-workspace-is.md#sections-teams-and-group-data) |
| Team mode | A reservation feature in which teammates can act on one another's bookings, including canceling them. | [Team Mode](../gpu-access/reservations.md#team-mode) |
| `teams/` | The directory where team-scoped data appears, drawing on the workspace quota. | [Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live) |
| TPOC (Technical Point of Contact) | The person a course nominates to lead its customization work, a designation for support purposes rather than a privilege tier. | [Managing a Group](managing-a-group.md) |
| TritonLink / TSS | The registration systems from which course rosters populate automatically; auditors and observers are not on them and are added through Canvas. | [Students Enrolled in a Course](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course) |
| Universal Scale Storage (USS) | SDSC storage that can be mounted onto the cluster, supported by Research IT. | [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage) |
| Unprivileged container | A container running under the member's own UID, without root or `sudo`, in a per-user Kubernetes namespace. | [Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages) |
| Workspace | The unit for one course, lab, or catch-all population, which anchors its roster, storage, container images, GPU class access, quotas, and budgets. | [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md) |
| Workspace manager | The privilege tier held by an instructor, a TA, or a PI. | [Managing a Group](managing-a-group.md) |
