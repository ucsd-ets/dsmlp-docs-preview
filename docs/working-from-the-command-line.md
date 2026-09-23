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
editor. Work outside a course is covered in
[Projects & Independent Study](student-project.md).

## Obtaining a Terminal

A terminal is available in the browser or over SSH. The two routes are not
equivalent.

### JupyterLab Terminal

JupyterLab provides a terminal inside a running browser session. It is suitable
for quick commands, and it ends when the session ends.

### SSH to the Login Node

The login node accepts Active Directory (AD) credentials, as described in
[Connecting over SSH](access/the-login-node.md#connecting-over-ssh). Duo
applies, at the interval given in
[Duo Authentication](access/the-login-node.md#duo-authentication). The VPN is
not required for `ssh` and is required only to reach a port inside a container,
as described in [VPN Requirement](access/the-login-node.md#vpn-requirement).
SSH is the route that allows work to be started and left running after
disconnection.

### Use of the Login Node

The login node is for launching jobs and moving files, as described in
[What the Login Node Is For](access/the-login-node.md#what-the-login-node-is-for).
A training script, a large `pip install`, or a data conversion runs inside a
container, not on the login node.

### Concurrent Browser and Shell Sessions

Launching a container from `dsmlp-login` while a Datahub session is open is
ordinary use. A member may have one Datahub session running at a time, as
described in
[Concurrent Datahub Sessions](access/datahub-in-the-browser.md#concurrent-datahub-sessions).
Shell, VS Code, and batch jobs are not limited by it, and any number of them
may run at once. The limit on all of them together is the total CPU, memory,
and GPU across everything running, as described in
[Running Several Jobs at Once](running-jobs/job-modes-and-limits.md#running-several-jobs-at-once).

## Launching a Container

The wrapper scripts set defaults and hand off to `launch.sh`.
`launch-scipy-ml.sh` starts the GPU-capable image, and `launch-datascience.sh`
starts the CPU image. The flags are listed in
[`launch.sh` Reference](running-jobs/launch-sh-reference.md).

```bash
launch-scipy-ml.sh          # GPU-capable image, wrapper defaults
launch.sh -h                # the flag summary, from the tool itself
```

### Default Resources

Bare `launch.sh` starts a smaller container than the wrappers do, so switching
from a wrapper to `launch.sh` directly reduces the CPU and memory a container
receives. Neither set of defaults matches the resources a browser session
starts with, which come from the course's spawn configuration. The command-line
defaults and the browser figure describe different things. All three are given
in [Default Resources](running-jobs/launch-sh-reference.md#default-resources).

### Requesting Resources

Resources are requested with flags at launch:

```bash
launch-scipy-ml.sh -c 4 -m 16 -g 1      # 4 CPU, 16GB RAM, 1 GPU
```

Limits apply at three tiers: a single pod, a namespace in total, and a higher
tier available on request. Confusing the tiers is the usual cause of a job that
will not schedule. A single container cannot request the namespace's full
memory total. The figures for each tier are given in
[Resource Tiers](running-jobs/launch-sh-reference.md#resource-tiers). A request
for the third tier states what the resources are for and is made as described
in [Administrative Requests](reference/getting-help.md#administrative-requests).

### Requests and Limits

The memory named at launch is a limit, not a guarantee. A job that ran on one
day can be `OOMKilled` (out-of-memory) on a busier node without reaching that
limit. The amount `launch.sh` guarantees is described in
[Resource Requests and Limits](running-jobs/launch-sh-reference.md#resource-requests-and-limits).

### Selecting a Workspace

A member of more than one workspace selects the workspace with `-W`, as
described in
[Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).

```bash
launch-scipy-ml.sh -W DSC102_FA26
```

Pass `-W` on a GPU launch even with only one workspace. It decides which
workspace's budget the session is charged to, and which bookings it can claim;
see [Reservations from the Command Line](#reservations-from-the-command-line).

## Selecting a GPU Class

The browser offers the environments a course has configured. From the shell, a
GPU class is requested directly:

```bash
launch-scipy-ml.sh -g 1 -l gpu-class=medium
```

The classes and their memory sizes are listed in
[GPU Class Sizes](gpu-access/gpu-classes.md#gpu-class-sizes). Request the
smallest class the model fits within, as described in
[Choosing a Class](gpu-access/gpu-classes.md#choosing-a-class). A larger class
is not faster for a model that fits in a smaller one, and it is scarcer and
draws more budget.

### Workspace Class Grants

Each workspace is granted one or more GPU classes, and a request for a class
the workspace was not granted is refused. The refusal is not a fault. Adding a
class is a request for the instructor to make, as described in
[Workspace Class Grants](gpu-access/gpu-classes.md#workspace-class-grants).

### Pending GPU Launches

A GPU launch waits in `Pending` until the reservation system admits it. The
reason for a wait is in the events that `kubectl describe pod` shows; see
[Reservation Events](#reservation-events). A pending GPU pod with no event from
the reservation system is usually missing its `gpu-class` label. See
[Missing or Misspelled Class Label](gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

## Job Modes and Limits

`launch.sh` runs a container in one of three modes, described in
[Job Modes](running-jobs/job-modes-and-limits.md#job-modes).

| Mode | Flag | Behavior |
|---|---|---|
| Interactive | None (default) | The launch returns a shell, and the job ends at disconnection |
| Background | `-b` | The container keeps running after disconnection, for reconnection later |
| Batch | `-B` | A command runs to completion with no terminal, and the job exits when it finishes |

```bash
launch-scipy-ml.sh -g 1 -b                     # background, reconnect later
launch-scipy-ml.sh -g 1 -B -- python train.py  # batch, runs and exits
```

### Option Separator

The `--` separator divides `launch.sh`'s own options from those of the command
being run. Without it, the launcher attempts to interpret the program's
arguments as its own. The separator is described in
[Option Separator](running-jobs/launch-sh-reference.md#option-separator).

### Reattaching to a Background Job

`-b` returns to the login node with the container still running. `kubesh`
reattaches to the container, and is also how it is shut down when finished. A
backgrounded container holds its resources until it is stopped, as described in
[Background Pods](running-jobs/job-modes-and-limits.md#background-pods).

### Slurm Compatibility Wrappers

Wrappers for `sbatch`, `srun`, `squeue`, and `scancel` are provided, so habits
carried from an HPC system largely work. No Slurm scheduler runs behind them,
and there is no MPI or multi-node support, as described in
[Slurm Compatibility Wrappers](reference/coming-from-hpc.md#slurm-compatibility-wrappers).
`--partition` is not a scheduling partition. It is forwarded as a GPU class
label, as described in
[The `--partition` Option](reference/coming-from-hpc.md#the---partition-option).

### Runtime Limit

Jobs default to 6 hours, and up to 12 hours may be set at launch, as described
in [The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit).
A booking does not lift the runtime limit. See
[Reservation Length and Session Runtime](gpu-access/reservations.md#reservation-length-and-session-runtime).

### Idle Culling

A container holding a GPU it has stopped using is reclaimed. Backgrounding a
job does not exempt it. The test is whether the GPU is doing anything, not
whether a session is attached. The criteria are given in
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).

### Checkpointing

Runtime limits, idle culling, and reservation windows can each end a container
without any fault in the code. Checkpoint long-running work, as described in
[Checkpointing & Logging Long Runs](running-jobs/checkpointing.md).

### Unused Containers

An idle container continues to hold its CPU, its memory, and its GPU. Shut down
containers that are not in use.

## Editing in Visual Studio Code

Visual Studio Code (VS Code) is supported through Remote-SSH over a
ProxyCommand. The ProxyCommand launches the container by way of the login node,
and `launch.sh -H` starts an SSH server inside it for VS Code to attach to.
Setup is described in [Remote Editor Setup](access/remote-editor-setup.md).

Use one Host entry per course. Reusing a single entry across courses causes the
host keys to collide, and the resulting failure presents as a security warning
rather than a configuration error, as described in
[Host Entries for Multiple Courses](access/remote-editor-setup.md#host-entries-for-multiple-courses).

`.vscode-server` grows past a gigabyte and can use up a course-sized home
quota, as described in
[Growth of `.vscode-server`](access/remote-editor-setup.md#growth-of-vscode-server).
`authorized_keys` must be inside the pod, as described in
[Key Copy in the Container](access/remote-editor-setup.md#key-copy-in-the-container).

## Interpreting Job Outcomes

| Reported | Meaning |
|---|---|
| `OOMKilled` | The container exceeded its memory limit. See [Requests and Limits](#requests-and-limits) |
| `DeadlineExceeded` | The job reached its runtime limit. See [Runtime Limit](#runtime-limit) |
| `Pending`, with `FailedScheduling` about untolerated taints | A GPU job waiting for the reservation system. The reason is in the reservation event beside it. See [Pending GPU Launches](#pending-gpu-launches) |
| A session ended, with a warning beforehand | Idle culling. See [Idle Culling](#idle-culling) |

If a GPU session ends and none of these statuses applies, the usual cause is
the reservation system: the session was past its guarantee and was preempted,
or its reservation was cancelled or given to a teammate. `kubectl get events`
shows which, for about an hour afterwards; see
[Reservation Events](#reservation-events). Error text, causes, and fixes are
listed in [Error Messages](reference/error-messages.md).

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

Booking, the cost of each class, the cancellation penalty, and overstay are
documented in [GPU Access](gpu-access/README.md).

### Reservation Events

The reservation system reports on a GPU session with Kubernetes events, shown by
`kubectl describe pod`, and by `kubectl get events` after the pod is gone. Each
is defined in [Reservation Events](reference/reservation-events.md):

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`.
- When it is admitted: `RuntimeGuaranteed`, `OverstayRelinked`,
  `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

## Custom Images

A course, or occasionally an individual student, may require a library stack
the standard images do not provide. Check what the course already provides
before building an image. Standard and custom images are covered in
[Environments](environments/README.md).

## Support

Course questions go to the course instructor or TA. Platform questions go to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or the
[ITS Service Desk](https://support.ucsd.edu/). A ticket includes the course, the
exact command run, and the full error. ITS response targets are listed in
[Response Targets](reference/getting-help.md#response-targets), and support
routing in [Getting Help](reference/getting-help.md).
