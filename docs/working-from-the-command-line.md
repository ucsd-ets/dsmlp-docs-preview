# Working from the Command Line

------------------------------------------------------------------------

This article describes how a course environment is reached from a terminal:
launching containers, requesting resources and GPU classes, running work that
outlives a connection, connecting a desktop editor, and interpreting what
happened to a job.

**This article assumes a terminal** and the ability to run `ssh`. It assumes
nothing further — not Kubernetes, not Docker, not Linux administration.

**Command-line access requires nothing additional.** There is no eligibility
requirement, no form, and nothing to request: every student enrolled in a course
that uses Datahub already holds it. It is the environment described in
[Using Datahub in a Course](student-in-a-course.md), reached differently — and
the shell provides what the browser cannot: jobs that survive a disconnect, GPU
classes not offered in the course menu, and a desktop editor.

*For work outside a course*, please see
[Projects & Independent Study](student-project.md).

## Obtaining a Terminal

------------------------------------------------------------------------

Two routes, which are not equivalent.

**In the browser.** JupyterLab provides a terminal. It is suitable for quick
commands inside a session that is already running, and it ends when that session
does.

**Over SSH.** The login node accepts AD credentials, and Duo applies — once
every 8 hours. *The VPN is not required for `ssh`; it is required only to reach a
port inside a container.* This is the route that allows work to be started and
left running after disconnection.
→ [Connecting over SSH](access/the-login-node.md#connecting-over-ssh)

**The login node is not where work runs.** It exists to launch jobs and move
files. A training script, a large `pip install`, or a data conversion belongs
inside a container, not on the login node.
→ [The Login Node](access/the-login-node.md)

**Shell work runs alongside a browser session.** Launching a container from
`dsmlp-login` while a Datahub session is open is ordinary use, and any number of
shell, VS Code and batch jobs may run at once. *The one limit on Datahub is that
a member may have a single Datahub session running.* What binds everything else
is the total CPU, memory and GPU across all of it.
→ [One Datahub Session](access/datahub-in-the-browser.md#one-datahub-session) ·
[Running Several Jobs at Once](running-jobs/job-modes-and-limits.md#running-several-jobs-at-once)

## Launching a Container

------------------------------------------------------------------------

The wrapper scripts are the straightforward path. `launch-scipy-ml.sh` starts the
GPU-capable image; `launch-datascience.sh` starts the CPU image. Both set
defaults and hand off to `launch.sh`.

```bash
launch-scipy-ml.sh          # GPU-capable image, wrapper defaults
launch.sh -h                # the flag summary, from the tool itself
```

**The wrappers and bare `launch.sh` do not provide the same thing.** Bare
`launch.sh` defaults to **1 CPU, 1GB RAM, and no GPU**. The wrappers set **2 CPU
and 8GB** before calling it. *Switching from a wrapper to `launch.sh` directly
therefore produces a smaller container.*

Neither figure is the **2 CPU / 4GB** with which a browser session begins: that
is the course's spawn configuration, while the wrapper figures are command-line
defaults. These are different things and both are correct.

**Requesting resources.**

```bash
launch-scipy-ml.sh -c 4 -m 16 -g 1      # 4 CPU, 16GB RAM, 1 GPU
```

Limits apply at three tiers, and confusing them is the usual cause of a job that
will not schedule:

| Tier | Default | Meaning |
|---|---|---|
| A single pod | 8 CPU / 32GB / 1 GPU | The most any one container receives |
| A namespace, in total | 8 CPU / 64GB / 1 GPU | Across everything running at once |
| Available on request | up to 32 CPU / 128GB | Please ask, and say what for |

*`-m 64` is therefore not a valid single-container request, even though 64GB is
the namespace total.*
→ [The Six Requests](reference/getting-help.md#the-six-requests)

**Requests are half of limits.** `launch.sh` sets the memory *request* to half
the limit named. Requesting 16GB reserves 8GB; up to 16GB may be used, but the
second 8GB is available only if the machine has it spare. *A job that ran
yesterday may therefore be `OOMKilled` today on a busy node.*
→ [`launch.sh` Reference](running-jobs/launch-sh-reference.md)

**Selecting a workspace**, for members of more than one:

```bash
launch-scipy-ml.sh -W DSC102_FA26
```

→ [Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

## Selecting a GPU Class

------------------------------------------------------------------------

The browser offers whichever environments a course has configured. From the shell
a size class is requested directly:

```bash
launch-scipy-ml.sh -g 1 -l gpu-class=medium
```

| Class | Memory | Typically backed by |
|---|---|---|
| `extra-small` | ~6 GB | A slice of an A30 |
| `small` | ~12 GB | RTX 2080Ti, or a slice of an A30 or H100 |
| `medium` | ~24 GB | A30, A5000, or a slice of an H100 or RTX 6000 |
| `large` | ~48 GB | L40S, or a slice of an H100 or RTX 6000 |
| `extra-large` | ~96 GB | A full H100 or RTX PRO 6000 Blackwell |

*Please request the smallest class a model fits within.* A larger class is not
faster for a model that fits in a smaller one; it is scarcer and draws more
budget.

Each workspace is given access to one or more GPU classes, and a class the
workspace was not granted is refused. Adding one is a request for the instructor
to make rather than a fault.

*If a GPU launch remains pending and eventually fails with `0/5 nodes available`,
the usual cause is a missing or misspelled `gpu-class` label.* Medium and above
sit behind scheduling taints, and without the label a pod has nowhere to land.
→ [From Reservation to Running Session](gpu-access/gpu-classes.md#from-reservation-to-running-session)

## Jobs That Outlive the Terminal

------------------------------------------------------------------------

**Interactive** is the default: the launch returns a shell, and the job ends at
disconnection.

**Background** (`-b`) keeps the container running after disconnection, for
reconnection later. It suits a long training run checked on between classes.

**Batch** (`-B`) runs a command to completion with no terminal at all, and exits
when finished.

```bash
launch-scipy-ml.sh -g 1 -b                     # background, reconnect later
launch-scipy-ml.sh -g 1 -B -- python train.py  # batch, runs and exits
```

*The `--` separator matters.* It separates `launch.sh`'s own options from those
of the command being run; without it the launcher attempts to interpret the
program's arguments as its own.

**Returning to a background job.** `-b` returns to the login node with the
container still running. `kubesh` reattaches to it, and is also how one is shut
down when finished — *a backgrounded container continues to hold its resources
until it is stopped.* → [Interactive, Background & Batch Modes](running-jobs/job-modes-and-limits.md#the-three-modes)

Wrappers for `sbatch`, `srun`, `squeue` and `scancel` are provided, so habits
carried from an HPC system largely work. There is no actual Slurm scheduler
behind them, and no MPI or multi-node support. **`--partition` is not a
scheduling partition here** — it is forwarded as a GPU class label.
→ [Coming from HPC](reference/coming-from-hpc.md#there-is-no-slurm-here)

**Runtime.** Jobs default to **6 hours**, and up to **12** may be set at launch.
Longer work is what reservations are for.
→ [The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit)

**Idle culling applies here as well.** A container holding a GPU it has stopped
using is reclaimed after about 30 minutes, up to 6 hours when the cluster is
quiet, and never within its first 45 minutes. *Backgrounding a job does not
exempt it* — the test is whether the GPU is doing anything, not whether a session
is attached. → [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle)

**Please checkpoint long-running work.** Between runtime limits, idle culling and
reservation windows there are several ways for a container to end that have
nothing to do with a fault in the code.
→ [Checkpointing](running-jobs/checkpointing.md)

**Shared resources.** An idle container continues to hold its CPU, its memory and
its GPU. *Please shut down containers that are not in use.*

## Editing in Visual Studio Code

------------------------------------------------------------------------

VS Code is supported and in heavy use. The supported path is **Remote-SSH over a
ProxyCommand**: the ProxyCommand launches the container by way of the login node,
and `launch.sh -H` starts an SSH server inside it for VS Code to attach to.

*Please use one Host entry per course.* Reusing a single entry across courses
causes the host keys to collide, and the resulting failure presents as a security
warning rather than a configuration mistake.

Two further matters: `.vscode-server` grows past a gigabyte and will consume a
course-sized home quota, and `authorized_keys` must be inside the pod.
→ [Remote Editor Setup](access/remote-editor-setup.md)

## Interpreting What Happened to a Job

------------------------------------------------------------------------

| Reported | Meaning |
|---|---|
| `OOMKilled` | Memory. The container exceeded its limit — see the request and limit note above |
| `DeadlineExceeded` | Time. It reached its runtime limit |
| `Pending`, then `0/5 nodes available` | Nothing could schedule it. Usually a GPU class label problem; occasionally the cluster is genuinely full |
| A session ended, with a warning beforehand | Idle culling |

If a GPU session ends and none of the above applies, the cause is usually the
reservation system: the guaranteed window elapsed, or the session was running on
capacity another user had booked. The course instructor or TA can see the course
calendar and advise which. The underlying event codes are documented in
[Kubernetes Events](running-jobs/kubernetes.md#reservation-events), which assumes more
Kubernetes than this article does.
→ [Error Messages](reference/error-messages.md)

## Reservations from the Command Line

------------------------------------------------------------------------

**Launching a GPU session without a reservation creates one, and draws on the
Service Unit budget.** This is as true from the shell as from the browser. There
is no exploratory launch that is free of charge: starting an eligible session is
what authorizes the spend, and *a script that launches in a loop can exhaust a
term's budget in an afternoon.*
→ [On-Demand Leases Charge Budget](gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

The runtime declared at launch matters: it is what is reserved and what is
charged. Please request the time the work needs rather than the maximum
permitted.

How to book, what each class costs, how the cancellation penalty is calculated,
and what happens on overstay are all documented in one place:
→ **[GPU Access](gpu-access/README.md)**

## Custom Images

------------------------------------------------------------------------

Occasionally a course requires a library stack the standard images do not
provide, and occasionally an individual student does. *The latter is rarer than
generally assumed* — please check what the course already provides before
building anything. → [Environments](environments/README.md)

------------------------------------------------------------------------

Please route course questions through the course instructor or TA. Platform
questions go to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) or the
[ITS Service Desk](https://support.ucsd.edu/); we aim to resolve individual user
issues within 1-2 business days. *Please include the course, the exact command
run, and the full error.* → [Getting Help](reference/getting-help.md)
