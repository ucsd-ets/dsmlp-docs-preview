# What Ends a Session

A session ends for one of five causes: idle culling, the runtime limit,
preemption, maintenance, or overstay followed by preemption. None of them is a
crash, and none of them loses saved work.

| Cause | Signal | Details |
|---|---|---|
| Idle culling | The GPU was unused for about 30 minutes | [What Counts as Idle](#what-counts-as-idle) |
| Runtime limit | The pod reached 6 hours, or 12 hours where that was set at launch | [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| Preemption | The capacity was needed for a booking | [Preemption](#preemption) |
| Maintenance | A node was drained, or the Research Cluster maintenance window opened | [Maintenance Closures](#maintenance-closures) |
| Overstay, then preemption | The reservation window closed, the session continued to run, and the capacity was needed for a booking | [Overstay](#overstay) |

## Idle Culling

**Idle culling** is the shutdown of a GPU session that holds a GPU and is not
using it.

### What Counts as Idle

A session that holds a GPU, has no GPU memory in use, and uses essentially no
CPU for about 30 minutes is shut down. When the cluster is quiet, the threshold
is up to 6 hours instead. No session is culled in its first 45 minutes. A
session that has been working hard receives a grace period of up to an hour
after the GPU goes quiet before the idle clock starts.

Idle culling applies to every GPU class. CPU-only sessions are not culled by
this mechanism.

A session is idle only when every condition in this table holds at once. If
any one of them fails, the culler treats the session as busy.

| Signal | Idle means |
|---|---|
| GPU memory | No more than about 150 MiB in use, on every GPU the session holds |
| GPU memory, changing | Any change since the last check counts as activity and restarts the clock |
| CPU | At most about 0.1 cores, taken as the maximum over the last hour |
| Age | The session is at least 45 minutes old. Nothing younger is ever considered idle |

A model loaded on the GPU is not idle, because it holds framebuffer memory. A
session that finished training an hour ago and has been at a shell prompt since
is idle, because it holds no GPU memory.

The CPU condition uses the maximum over the last hour, not the current value. A
job that does a burst of work every forty minutes is not culled between bursts.

### The Timings

| Stage | Duration |
|---|---|
| First 45 minutes | Never culled, whatever the session is doing |
| Grace after the GPU goes quiet | 15 to 60 minutes before the quiet time counts as idle, scaling with how much GPU work the session has already done. A session with two hours or more of GPU activity receives the full hour |
| Normal cull | 30 minutes of idleness |
| When the class is underloaded | 6 hours of idleness |
| Check interval | Every 5 minutes |

The 6-hour threshold is a property of the GPU class, not of the session. It
applies when every node behind the GPU class is under 75% allocated on CPU,
memory, and GPU at the same time. The same idle session can therefore be culled
after 6 hours on a quiet evening and after 30 minutes in week 10. Do not plan
work around the 6-hour threshold.

### Warnings & Pod Status

A session is warned before it is culled. The warning starts when 30 minutes
remain before the cull.

The idle status is recorded on the pod and can be read from the command line:

```bash
kubectl get pods
kubectl describe pod <pod-id>
```

Under `Annotations`, `dsmlp/idle-gpu-status` reads `ok`, `idle` or `warning`, and
`dsmlp/idle-gpu-cull-deadline` gives the time at which the session would be
culled if nothing changes.

The cull deadline is a projection. It is recalculated on every pass, moves as
conditions change, and is removed as soon as the session does GPU work again.

> [!NOTE]
> A missing annotation does not indicate a healthy session. It means the
> session is out of scope, has not yet been checked, or has already been culled.

On a busy cluster, the `idle` status does not appear. With a 30-minute threshold
and a 30-minute warning lead, the status changes directly from `ok` to
`warning`. The `idle` status appears on a quiet cluster, while the 6-hour
threshold applies.

### Effects of Idle Culling

A cull is a deliberate stop, not a crash or a fault in the code. It requires no
report and no fix.

The container is deleted. The home directory, the `private/` area, and the
workspace's shared directories are not.

Anything held only in the session's memory is lost, such as a notebook kernel's
variables or a model trained for two hours and not saved. Checkpoint long runs.

A culled session requires no cleanup before a relaunch.

See also: [Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live), [Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md)

### Background and Batch Jobs

Idle culling tests whether the GPU is in use, not whether a session is attached
to it. The culler treats each of these as an idle session:

- A background pod (`-b`) that was disconnected from three hours ago
- A batch job whose Python process has already exited
- A `nohup`-ed script that is waiting on a download

A job that is computing on the GPU is never culled, however long it runs and
whether or not anyone is watching it. Backgrounding an active training run does
not expose it to idle culling. A GPU session held open for later use is culled.

See also: [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes)

### Inside a Booked Window

A cull does not cancel the reservation. The booked window stands for its
remaining length, and a session may be launched into it again.

Whether a relaunch after a cull must fall within a new claim window is not yet
published. Relaunch promptly after a cull inside a booked window.

See also: [The Claim Window](reservations.md#the-claim-window)

### Browser Inactivity and Disconnection

Some third-party course material gives Datahub an inactivity timeout of 20
minutes, or of 30. Neither figure comes from ITS, and neither describes idle
culling. Idle culling measures whether a GPU is in use, not whether a browser
tab is active.

> [!WARNING]
> Logging out or closing a laptop does not stop a session: it keeps running,
> holding its GPU and drawing on the budget, until it is stopped with
> **File → Hub Control Panel → Stop My Server**.

See also: [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session), [On-Demand Lease Charges](service-units-and-budgets.md#on-demand-lease-charges)

## End of a Reservation Window

The close of a reservation window does not terminate the session running in
it. Where no one else needs the capacity, the session continues to run.

The window defines what was charged for and what is guaranteed. After the
window closes, the session runs without that guarantee.

### The Countdown

A session reports how long its guarantee has left. The countdown appears in the
session itself, not by email. The countdown's lead time and presentation are
not yet published.

A checkpoint written before the window closes survives the end of the window.
From that point, the session can be stopped, extended, or left running.

See also: [Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md)

### Overstay

**Overstay** is running a session past the end of its guaranteed window.

> [!WARNING]
> An overstaying session is not stopped or warned off, and nothing in the
> interface prevents overstay. The time past the window is not covered by the
> booking, and overstay has a cost.

The cost of overstay is not yet published.

An overstaying session runs on capacity that is no longer guaranteed to it.
When that capacity is needed for another booked window, the overstaying session
is the one that yields.

A longer window arranged in advance is the alternative to overstay; see
[Routes to More Time](reservations.md#routes-to-more-time).

Releasing the unused remainder of a window early carries no cancellation
penalty. The charge is for the time actually used, and the remainder returns to
the pool. See [Cancelling in Advance](service-units-and-budgets.md#cancelling-in-advance).

## Preemption

**Preemption** is the ending of a session because its capacity is needed for a
booking. It is a capacity outcome, not a fault.

Preemption occurs in two situations:

- An overstaying session, when a reservation comes due for the capacity it is
  still holding.
- A best-effort session, which accepts preemption from its first tick in
  exchange for running now. See
  [Best-Effort Reservations](reservations.md#best-effort-reservations).

Saved work survives preemption. Anything held only in memory does not. There is
no signal to catch and no opportunity to write data out before the session
ends.

The session records the outcome as a Kubernetes event: `Preempted`, or
`OverstayRelinked` where an overstay was involved.

See also: [Reservation Events](../running-jobs/kubernetes.md#reservation-events)

## Maintenance Closures

Two maintenance regimes apply: instructional maintenance and Research Cluster
maintenance. The schedule for both is published under
[Scheduled Maintenance](../reference/policy.md#scheduled-maintenance). Do not
start a 12-hour run that would overlap an announced maintenance window.

### Instructional Maintenance

Campus policy requires prompt patching of servers. The instructional
maintenance window is reserved for that patching and is not a scheduled outage.

Instructional maintenance usually affects a subset of worker nodes. Scheduling
policy tries to place jobs on nodes that will not be touched, so running work is
generally unaffected. During the window, the platform may operate at reduced
capacity, and, depending on the work being done, the whole cluster can be
briefly inaccessible. A running job can still be terminated, because some
updates require a node to be drained.

Patching is deferred where possible during 10th week and Finals week, unless a
vulnerability requires immediate action. Critical updates occasionally require
work outside the window. ITS notifies instructors and TAs of such work as far in
advance as possible.

### Research Cluster Maintenance

Research Cluster maintenance terminates all running jobs. Jobs are not drained,
migrated, or deferred to another node. A multi-day training run started the day
before is lost when the window opens, together with everything not written to
disk.

Windows are placed to avoid the start and end of a quarter, midterm periods, and
known conference deadlines, and each notice is followed by a reminder shortly
before the day. This placement reflects past practice, not a published
commitment. The notice sent for each window governs.

Research Cluster maintenance notices are sent from
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu), which also answers
questions about them.

### GPU Class Availability During Maintenance

When nodes are taken out of service for planned work, the GPU classes they back
have fewer GPUs, or none, for the duration. A class can therefore show nothing
available on particular dates even though no one has booked it.

A class that shows nothing available on a date may be fully booked or closed for
maintenance. The two cases look identical to a user.

Where a class in regular use shows nothing available across a specific span of
days and no notice has been sent, report it to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) instead of assuming demand.

See also: [When the Cluster Is Full](quotas-and-availability.md#when-the-cluster-is-full)

### Jobs Ending Outside Any Window

Worker nodes are patched on demand, year-round, without user notification. Only
the JupyterHub, login, and file-server components follow the notified schedule.
The worker nodes that run containers are maintained as the need arises.

On-demand patching can end a job cleanly, at no particular time, with no error
from the job and no maintenance announcement. This is not the common case, and
it cannot be scheduled around.
