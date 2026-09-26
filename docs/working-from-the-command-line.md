# Working from the Command Line

This page covers reaching a course environment from a terminal: launching
containers, requesting resources and GPU classes, running jobs that continue
after disconnection, connecting Visual Studio Code, and interpreting what
happened to a job. It assumes a terminal and the `ssh` command, and no
knowledge of Kubernetes, Docker, or Linux administration.

## Access

Every student enrolled in a course that uses Datahub already has command-line
access. No form or request is required. The shell reaches the same environment
as [Using Datahub in a Course](student-in-a-course.md) and adds jobs that
survive a disconnect, GPU classes not offered in the course menu, and a desktop
editor. [Projects & Independent Study](student-project.md) covers work outside
a course.

## Obtaining a Terminal

A terminal is available in the browser or over SSH. The two routes are not
equivalent.

### JupyterLab Terminal

JupyterLab provides a terminal inside a running browser session. It is suitable
for quick commands, and it ends when the session ends.

### SSH to the Login Node

The login node accepts Active Directory (AD) credentials. See
[Connecting over SSH](access/the-login-node.md#connecting-over-ssh). Duo
applies. [Duo Authentication](access/the-login-node.md#duo-authentication)
gives the interval. The VPN is not required for `ssh` and is required only to
reach a port inside a container. See
[VPN Requirement](access/the-login-node.md#vpn-requirement).
SSH is the route that allows work to be started and left running after
disconnection.

### Use of the Login Node

The login node is for launching jobs and moving files. See
[What the Login Node Is For](access/the-login-node.md#what-the-login-node-is-for).
A training script, a large `pip install`, or a data conversion runs inside a
container, not on the login node.

### Concurrent Browser and Shell Sessions

Launching a container from `dsmlp-login` while a Datahub session is open is
ordinary use. A member may have one Datahub session running at a time. See
[Concurrent Datahub Sessions](access/datahub-in-the-browser.md#concurrent-datahub-sessions).
Shell, VS Code, and batch jobs are not limited by it, and any number of them
may run at once. The limit on all of them together is the total CPU, memory,
and GPU across everything running. See
[Running Several Jobs at Once](running-jobs/job-modes-and-limits.md#running-several-jobs-at-once).

## Launching a Container

The wrapper scripts set defaults and hand off to `launch.sh`.
`launch-scipy-ml.sh` starts the GPU-capable image, and `launch-datascience.sh`
starts the CPU image.
[`launch.sh` Reference](running-jobs/launch-sh-reference.md) lists the flags.

```bash
launch-scipy-ml.sh -W DSC40_FA26_001  # GPU-capable image, wrapper defaults
launch.sh -h                          # the flag summary, from the tool itself
```

### Default Resources

Bare `launch.sh` starts a smaller container than the wrappers do, so switching
from a wrapper to `launch.sh` directly reduces the CPU and memory a container
receives. Neither set of defaults matches the resources a browser session
starts with, which come from the course's spawn configuration. The command-line
defaults and the browser figure describe different things.
[Default Resources](running-jobs/launch-sh-reference.md#default-resources)
gives all three.

### Requesting Resources

Resources are requested with flags at launch:

```bash
launch-scipy-ml.sh -W DSC40_FA26_001 -c 4 -m 16 -g 1 -l gpu-class=medium   # 4 CPU, 16GB RAM, 1 GPU
```

Limits apply at three tiers: a single pod, a namespace in total, and a higher
tier available on request. Confusing the tiers is the usual cause of a job that
will not schedule. A single container cannot request the namespace's full
memory total.
[Resource Tiers](running-jobs/launch-sh-reference.md#resource-tiers) gives the
figures for each tier. A request for the third tier states what the resources
are for. See
[Administrative Requests](reference/getting-help.md#administrative-requests).

### Requests and Limits

The memory named at launch is a limit, not a guarantee. A job that ran on one
day can be `OOMKilled` (out-of-memory) on a busier node without reaching that
limit.
[Resource Requests and Limits](running-jobs/launch-sh-reference.md#resource-requests-and-limits)
describes the amount `launch.sh` guarantees.

### Selecting a Workspace

A member of more than one workspace selects the workspace with `-W`. See
[Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).

```bash
launch-scipy-ml.sh -W DSC40_FA26_001
```

Pass `-W` on a GPU launch even with only one workspace. It decides which
workspace's budget the session is charged to, and which bookings it can claim;
see [Reservations from the Command Line](#reservations-from-the-command-line).

## Selecting a GPU Class

The browser offers the environments a course has configured. From the shell, a
GPU class is requested directly:

```bash
launch-scipy-ml.sh -W DSC40_FA26_001 -g 1 -l gpu-class=medium
```

[GPU Class Sizes](gpu-access/gpu-classes.md#gpu-class-sizes) lists the classes
and their memory sizes. Request the smallest class the model fits within. See
[Choosing a Class](gpu-access/gpu-classes.md#choosing-a-class). A larger class
is not faster for a model that fits in a smaller one, and it is scarcer and
draws more budget.
[Workloads by GPU Class](gpu-access/workloads-by-gpu-class.md) gives examples of
the work each class suits.

`-v` limits a session to one GPU model within its class, and is for a session
launched without a booking only; see
[Node Selection](running-jobs/launch-sh-reference.md#node-selection).

### Workspace Class Grants

Each workspace is granted one or more GPU classes, and a request for a class
the workspace was not granted is refused. The refusal is not a fault. Adding a
class is a request for the instructor to make. See
[Workspace Class Grants](gpu-access/gpu-classes.md#workspace-class-grants).

### Pending GPU Launches

A GPU launch waits in `Pending` until the reservation system admits it. The
reason for a wait is in the events that `kubectl describe pod` shows; see
[Reservation Events](#reservation-events). A pending GPU pod with no event from
the reservation system is usually missing its `gpu-class` label. See
[Missing or Misspelled Class Label](gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

## Job Modes and Limits

`launch.sh` runs a container in one of three modes. See
[Job Modes](running-jobs/job-modes-and-limits.md#job-modes).

| Mode | Flag | Behavior |
|---|---|---|
| Interactive | None (default) | The launch returns a shell, and the job ends at disconnection |
| Background | `-b` | The container keeps running after disconnection, for reconnection later |
| Batch | `-B` | A command runs to completion with no terminal, and the job exits when it finishes |

```bash
launch-scipy-ml.sh -W DSC40_FA26_001 -g 1 -l gpu-class=medium -b                     # background, reconnect later
launch-scipy-ml.sh -W DSC40_FA26_001 -g 1 -l gpu-class=medium -B -- python train.py  # batch, runs and exits
```

### Option Separator

The `--` separator divides `launch.sh`'s own options from those of the command
being run. Without it, the launcher attempts to interpret the program's
arguments as its own.
[Option Separator](running-jobs/launch-sh-reference.md#option-separator)
describes the separator.

### Reattaching to a Background Job

`-b` returns to the login node with the container still running.
`kubesh <pod-id>` reattaches to it. Leaving with `exit` stops neither the
container nor the processes started in it. `kubectl delete pod <pod-id>` stops
both.
A backgrounded container holds its resources until you delete it. See
[Background Pods](running-jobs/job-modes-and-limits.md#background-pods) and
[Checking On a Detached Job](running-jobs/watching-your-job.md#checking-on-a-detached-job).

### Slurm Compatibility Wrappers

Wrappers for `sbatch`, `srun`, `squeue`, and `scancel` are provided, so habits
carried from an HPC system largely work. No Slurm scheduler runs behind them,
and there is no MPI or multi-node support. See
[Slurm Compatibility Wrappers](reference/coming-from-hpc.md#slurm-compatibility-wrappers).
`--partition` is not a scheduling partition. It is forwarded as a GPU class
label. See
[The `--partition` Option](reference/coming-from-hpc.md#the---partition-option).

### Runtime Limit

Jobs default to 6 hours, and up to 12 hours may be set at launch. See
[The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit).
A booking does not lift the runtime limit. See
[Reservation Length and Session Runtime](gpu-access/reservations.md#reservation-length-and-session-runtime).

### Idle Culling

A container holding a GPU it has stopped using is reclaimed. Backgrounding a
job does not exempt it. The test is whether the GPU is doing anything, not
whether a session is attached.
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle)
gives the criteria.

### Checkpointing

Runtime limits, idle culling, and reservation windows can each end a container
without any fault in the code. Checkpoint long-running work. See
[Checkpointing & Logging Long Runs](running-jobs/checkpointing.md).

### Unused Containers

An idle container continues to hold its CPU, its memory, and its GPU. Shut down
containers that are not in use.

## Editing in Visual Studio Code

Visual Studio Code (VS Code) is supported through Remote-SSH over a
ProxyCommand. The ProxyCommand launches the container by way of the login node,
and `launch.sh -H` starts an SSH server inside it for VS Code to attach to.
[Remote Editor Setup](access/remote-editor-setup.md) describes the setup.

Use one Host entry per course. Reusing a single entry across courses causes the
host keys to collide, and the resulting failure presents as a security warning
rather than a configuration error. See
[Host Entries for Multiple Courses](access/remote-editor-setup.md#host-entries-for-multiple-courses).

`.vscode-server` grows past a gigabyte and can use up a course-sized home
quota. See
[Growth of `.vscode-server`](access/remote-editor-setup.md#growth-of-vscode-server).
Each launch copies the login node's `authorized_keys` into the container, so
you install the key once, on the login node. See
[Key Copy in the Container](access/remote-editor-setup.md#key-copy-in-the-container).

## Interpreting Job Outcomes

| Reported | Meaning |
|---|---|
| `OOMKilled` | The container exceeded its memory limit. See [Requests and Limits](#requests-and-limits) and [Memory Limits and `OOMKilled`](running-jobs/watching-your-job.md#memory-limits-and-oomkilled) |
| `DeadlineExceeded` | The job reached its runtime limit. See [Runtime Limit](#runtime-limit) |
| `Pending`, with a `FailedScheduling` event | A GPU job waiting for the reservation system. The reason is in the reservation event beside it. See [Pending GPU Launches](#pending-gpu-launches) |
| A session ended, with a warning beforehand | Idle culling. See [Idle Culling](#idle-culling) |

If a GPU session ends and none of these statuses applies, the usual cause is
the reservation system: the session was past its guarantee and was preempted,
or its reservation was cancelled or given to a teammate. `kubectl get events`
shows which, for about an hour afterwards; see
[Reservation Events](#reservation-events).
[Error Messages](reference/error-messages.md) lists error text, causes, and
fixes.

## Reservations from the Command Line

> [!WARNING]
> Launching a GPU session without a reservation creates one and draws on the
> Service Unit budget, from the shell as from the browser. There is no
> exploratory launch that is free of charge. Starting an eligible session
> authorizes the spend, and a script that launches in a loop can exhaust a
> term's budget. See
> [On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

A launch without a booking holds an on-demand lease of 1 hour 10 minutes and
is charged for the time the session uses within it. For a longer guarantee,
open the reservation app at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/) once the session is
running and use [Extend](gpu-access/reservations.md#extend).

`-W` decides which workspace a GPU launch is charged to, and which bookings it
can claim. A GPU launch without `-W` is charged to `ORG_ON_DEMAND`, the default
workspace, and never claims a course booking. See
[Claiming a Booking](gpu-access/reservations.md#claiming-a-booking).

[GPU Access](gpu-access/README.md) covers booking, the cost of each class, the
cancellation penalty, and overstay.

### Reservation Events

The reservation system reports on a GPU session with Kubernetes events, shown by
`kubectl describe pod`, and by `kubectl get events` after the pod is gone.
[Reservation Events](reference/reservation-events.md) defines each one:

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`, `NoMatchingNode`, `WaitingForNode`.
- When it is admitted: `RuntimeGuaranteed`, `ReservationRelinked`,
  `OverstayRelinked`, `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

## Custom Images

A course, or occasionally an individual student, may require a library stack
the standard images do not provide. Check what the course already provides
before building an image. [Environments](environments/README.md) covers
standard and custom images.

## Support

Course questions go to the course instructor or TA. Platform questions go to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or the
[ITS Service Desk](https://support.ucsd.edu/). A ticket includes the course, the
exact command run, and the full error.
[Response Targets](reference/getting-help.md#response-targets) lists ITS
response targets. [Getting Help](reference/getting-help.md) covers support
routing.
