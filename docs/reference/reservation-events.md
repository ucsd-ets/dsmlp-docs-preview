# Reservation Events

The reservation system reports what it is doing with a GPU pod through
Kubernetes events on the pod. Each event is a full sentence that says what
happened and what to do.

## Reading the Events

Run these from the login node:

```bash
kubectl describe pod <pod-name>      # the events at the bottom of the output
kubectl get events                   # every recent event in the namespace
kubectl get events --field-selector involvedObject.name=<pod-name>
```

In `kubectl describe pod`, the **From** column reads `gpu-reservation-controller`
for these events. Datahub shows the same events while a session is starting.

Times in event messages are Pacific time, for example
`2026-09-23 17:00:00 PDT`. Timestamps in pod annotations are UTC.

### Events for a Deleted Pod

`Preempted`, `ReservationCancelled`, and `ReservationReassigned` are written
just before the pod is deleted, so `kubectl describe pod` no longer finds the
pod. Read them with `kubectl get events`. Kubernetes keeps events for about an
hour by default. All three are type `Normal`, so
`kubectl get events --field-selector type=Warning` does not show them.

### Repeated Events

An event about a pod that is still waiting is repeated every 30 minutes while
its message stays the same, and written again at once when the message changes.
Each repeat is a separate line. An `OnDemandLeaseDenied` for lack of capacity
names the current time, so its message changes on every retry and it is written
at every retry, usually every 2 to 5 minutes. An event that suggests contacting
support names
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

## Events at a Glance

| Event | Type | Stage | Meaning |
|---|---|---|---|
| [`WaitingForReservation`](#waitingforreservation) | Normal | Waiting | The pod is waiting for its owner's booking to open |
| [`ReservationFull`](#reservationfull) | Warning | Waiting | The booking is open, but the owner's other pods hold its GPUs |
| [`ReservationTooSmall`](#reservationtoosmall) | Warning | Waiting | The pod asks for more GPUs than the booking holds |
| [`OnDemandLeaseDenied`](#ondemandleasedenied) | Warning | Waiting | The reservation app refused an on-demand lease for the pod |
| [`OnDemandLeaseRejected`](#ondemandleaserejected) | Warning | Waiting | The reservation app does not recognize the user, workspace, or class the pod named |
| [`OnDemandAdmissionPaused`](#ondemandadmissionpaused) | Warning | Waiting | On-demand admission is paused for the whole GPU class |
| [`UnknownGpuClass`](#unknowngpuclass) | Warning | Waiting | The pod's `gpu-class` label is not a known class |
| [`NoReservation`](#noreservation) | Warning | Waiting | Nothing matches the pod, and it cannot have an on-demand lease |
| [`AnnotationIgnored`](#annotationignored) | Warning | Waiting | An annotation on the pod was ignored, which changed the outcome |
| [`NoMatchingNode`](#nomatchingnode) | Warning | Waiting | The node or GPU model the pod names is not in its GPU class, so it cannot have an on-demand lease |
| [`WaitingForNode`](#waitingfornode) | Normal | Waiting | The node or GPU model the pod names has no free GPU, so no on-demand lease is requested yet |
| [`RuntimeGuaranteed`](#runtimeguaranteed) | Normal | Admitted | The pod was admitted, and its GPU is guaranteed until the time shown |
| [`ReservationRelinked`](#reservationrelinked) | Normal | Admitted | The running pod was moved onto another reservation, because its lease merged into a booking or its reservation was replaced |
| [`OverstayRelinked`](#overstayrelinked) | Normal | Admitted | The pod was running past its guarantee, and was moved onto a newer booking and is guaranteed again |
| [`BestEffortAdmitted`](#besteffortadmitted) | Normal | Admitted | The pod was admitted with no guarantee and no charge |
| [`Preempted`](#preempted) | Normal | Stopped | The pod was past its guarantee and was stopped to free its GPU |
| [`ReservationCancelled`](#reservationcancelled) | Normal | Stopped | The reservation the pod ran under was cancelled, and the pod was deleted |
| [`ReservationReassigned`](#reservationreassigned) | Normal | Stopped | The booking was given to another user, and the pod was deleted |

## Events While a Pod Waits

A GPU pod waits in `Pending` until the reservation system admits it. While it
waits, `kubectl describe pod` also shows a `FailedScheduling` event from the
Kubernetes scheduler. That scheduler event is normal for every GPU pod that has
not been admitted yet, and does not mean the label is wrong or the cluster is
full. See
[Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

### `WaitingForReservation`

Type `Normal`. The pod matches one of its owner's bookings, and the booking has
not opened yet. The pod is admitted within about 5 minutes of the opening.
Nothing needs to change.

```text
Waiting for your GPU reservation #4127 (1 x medium, 2026-09-23 09:00:00 PDT to 2026-09-23 17:00:00 PDT) to open; this pod will be admitted shortly after it does.
```

[Launching Before the Window Opens](../gpu-access/reservations.md#launching-before-the-window-opens)
gives how far before a booking a pod waits for it, rather than starting on an
on-demand lease.

### `ReservationFull`

Type `Warning`. The pod was waiting for its booking, but when the booking opened
the owner's other pods held its GPUs. The message names those pods when they
are in the same namespace. The pod is admitted if a GPU frees up. On DSMLP, the
reservation system re-checks a waiting pod within about 10 minutes, and a pod
that still does not fit its booking is then given an on-demand lease, charged
separately. Stop one of the named pods with `kubectl delete pod <pod-name>` to
free a GPU for the booking.

An account can hold 1 GPU at a time by default, across all its pods, and a
launch that would take it past that is refused. This event therefore arises
only where ITS has raised the account's GPU limit. See
[Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers).

### `ReservationTooSmall`

Type `Warning`. The pod requests more GPUs than its booking holds, so the
booking can never admit it. Two bookings are never combined for one pod. On
DSMLP this event is not expected: a pod that asks for more GPUs than its booking
holds is given an on-demand lease, charged separately, instead of waiting. See
[Claiming a Booking](../gpu-access/reservations.md#claiming-a-booking).

### `OnDemandLeaseDenied`

Type `Warning`. The pod has no booking open, so the reservation system asked
the reservation app for an on-demand lease, and the app refused. The message
quotes the app's reason word for word, then says whether waiting can help:

```text
On-demand GPU lease for 1 x medium was denied by the reservation service: Only 0 GPU(s) available at 2026-09-23 19:07. The pod stays Pending; the controller will keep retrying.
```

```text
On-demand GPU lease for 1 x medium was denied by the reservation service: This lease costs 1.16667 SU but user 'jsmith' has only 0.5 of 10 SU remaining (currently using 9.5). The pod stays Pending; the controller will keep retrying, and the reservation service expects this to clear by 2026-09-28 00:00:00 PDT.
```

```text
On-demand GPU lease for 1 x medium was denied by the reservation service: GPU class not accessible under this group. Waiting will not change this: the pod stays Pending until its request changes or an administrator changes what refused it. If the reason looks wrong, contact support: datahub@ucsd.edu
```

| Message ends | Meaning | The request is retried |
|---|---|---|
| `will keep retrying.` | The refusal can clear by itself, as GPUs or budget free up | Every 2 to 5 minutes |
| `expects this to clear by <time>.` | The refusal clears at a known time, such as the start of the next budget window | At that time, or every 30 minutes until then |
| `Waiting will not change this: …` | The request itself is refused, whatever else is running | At lengthening intervals, up to every 30 minutes |

In every case the pod stays `Pending`. Nothing fails the pod or deletes it.

| Reason quoted | Meaning | Waiting helps |
|---|---|---|
| `Only N GPU(s) available at …` | The class has too few free GPUs at that time | Yes, unless the pod asks for more GPUs than the class has |
| `Only N GPU(s) available for this group at … (group ceiling: …)` | The workspace already holds its GPU limit for the class. Figures such as `borrowed` and `buffer` in the brackets describe idle capacity the workspace could borrow | Yes, as other members' jobs end, unless the pod asks for more GPUs than the limit and the idle capacity together |
| `Only N GPU(s) available for this cohort at … (cohort ceiling: …)` | The workspaces that share capacity with this one hold all of it. See [Cohorts](../gpu-access/quotas-and-availability.md#cohorts) | Yes, unless the pod asks for more GPUs than the ceiling and the idle capacity together |
| `This lease costs X SU but user '…' has only Y of Z SU remaining …` | The Service Unit (SU) budget cannot cover the lease | Yes, when the budget window renews, unless X is more than Z |
| `This lease costs X SU but the group pool only has …` | The workspace's shared SU pool is spent | Yes, when the budget window renews, unless the lease costs more than the whole pool |
| `User '…' is not a member of group '…'` | The user is not enrolled in the workspace the pod named | No. Launch with `-W` naming a workspace the user belongs to, or ask the instructor or TA to check the roster |
| `GPU class not accessible under this group` | The workspace was not granted this class | No. Use a class the workspace was granted |
| `Exceeds limit of N GPU(s) per reservation` | The pod asks for more GPUs than the class allows in one reservation | No. Launch with fewer GPUs |
| `This lease runs H hours but group '…' limits a single reservation to N hours.` | The lease would be longer than the workspace's length cap | No |
| `Group '…' is not active on …` | The workspace named is outside its active dates on the date named | Only if the workspace's dates have not started yet. The message then names when the refusal clears |

Where the message says waiting will not change the outcome, delete the pod with
`kubectl delete pod <pod-name>` and launch again with the request corrected, for
example with `-W` naming the right workspace, another class, or fewer GPUs.
Where the refusal comes from a workspace setting, such as its class grant or its
length cap, an administrator can change the setting instead. The waiting pod is
then checked again within 30 minutes, and can start without a new launch.

> [!WARNING]
> A pod left `Pending` keeps being retried, whatever its message says. When the
> lease is granted, the pod starts and Service Units are charged, even if nobody
> is waiting for it any more. Delete a pending GPU pod that is no longer wanted.

See also: [Waiting for an On-Demand Lease](../gpu-access/quotas-and-availability.md#waiting-for-an-on-demand-lease)

### `OnDemandLeaseRejected`

Type `Warning`. The reservation app does not recognize the user, the workspace,
or the GPU class the lease request named. The user is the pod's namespace, and
the workspace comes from the pod's `dsmlp/course` label, which `launch.sh` sets
from `-W`, or is `ORG_ON_DEMAND` when the pod names no course. The message
states both, and names any booking the user holds under a different workspace.
Waiting does not fix this. Launch again with the correct `-W` workspace, or
correct the label in a manifest. If the values look right, contact
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

### `OnDemandAdmissionPaused`

Type `Warning`. On-demand admission is paused for the whole GPU class, so no
lease is requested. The message gives one of three causes:

- No nodes of the class are available, for example during maintenance.
- The class has fewer GPUs online than the reservation app expects, for example
  when a node is down.
- Pods that already hold a reservation for the class are still waiting to be
  placed. Pods with a reservation go first. A pod waiting only for a node or
  GPU model it named, while other nodes of the class have room, does not cause
  this pause.

Nothing about the pod needs to change. Leave it in place. The on-demand queue is
ordered by pod creation time, so deleting and recreating the pod moves it to the
back. If the pause lasts, contact
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

### `UnknownGpuClass`

Type `Warning`. The pod's `gpu-class` label names no class the reservation app
knows, so nothing can admit the pod. The message lists the known classes.
Labels are case-sensitive. Correct the label and recreate the pod.

```text
This pod's gpu-class label is Medium, which is not a GPU class the reservation service knows, so no reservation can match it and it cannot be admitted on demand. Known classes: large, medium, small, xlarge, xsmall. Correct the label and recreate the pod; if it is right, contact support: datahub@ucsd.edu
```

### `NoReservation`

Type `Warning`. No booking matches the pod, and the pod does not qualify for an
on-demand lease. The message lists why, and names any booking the user holds for
another class or another workspace. Correct the pod and recreate it, or book a
window for the class. See
[Claiming a Booking](../gpu-access/reservations.md#claiming-a-booking). On
DSMLP, where every pod with a class label qualifies for an on-demand lease, this
event is not expected.

### `AnnotationIgnored`

Type `Warning`. An annotation on the pod was invalid or asked for something
DSMLP does not offer, and ignoring it changed what happens. The common case is a
request for best-effort admission, which is not enabled on DSMLP: the pod is
admitted on an ordinary on-demand lease and charged for it. See
[Best-Effort Reservations](../gpu-access/reservations.md#best-effort-reservations).

### `NoMatchingNode`

Type `Warning`. The pod has no booking and names a node or a GPU model, with
`-n`, `-v`, or a node selector in a manifest, and no node of its GPU class
matches. No on-demand lease is requested. The usual causes are a node number
that does not exist, a node that belongs to another GPU class, a node that is
out of service, and a GPU model that does not back the class. The message
quotes the node selection and names any other GPU class whose nodes it matches.
Correct the node, the model, or the `gpu-class` label, and recreate the pod. The
reservation system checks the pod again about every 5 minutes, so a pod that
names a node out of service starts once the node returns. If the node selection
is right, contact [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

A `medium` pod launched with `-n 30`, when node 30 is a `large` node, records:

```text
This pod's node selector kubernetes.io/hostname=its-dsmlp-n30.ucsd.edu matches none of the N schedulable node(s) of GPU class medium, so it could not start on any of them and no on-demand lease is being requested for it. It does match nodes of GPU class large, so the pod's gpu-class label may be what is wrong. Correct the node selector or affinity and recreate the pod; if it is right, the nodes it names may be cordoned or out of service, so contact support: datahub@ucsd.edu
```

### `WaitingForNode`

Type `Normal`. The pod has no booking and was launched with `-n` or `-v`, or
with a node selector in a manifest, and no node it allows has the GPUs it asks
for free. No on-demand lease is requested until one does, so nothing is charged
while the pod waits. The reservation system checks the pod again about every 5
minutes. Other nodes of the class may be free: launching without `-n` or `-v`
lets the pod use them. A pod that names a node or a GPU model and runs under a
booking gets no such event. It holds the booking while it waits. See
[Node Selection](../running-jobs/launch-sh-reference.md#node-selection).

A 1-GPU `medium` pod launched with `-n 30`, while node 30 has no free GPU,
records:

```text
No node of GPU class medium that this pod's node selector kubernetes.io/hostname=its-dsmlp-n30.ucsd.edu allows has 1 GPU(s) free, so no on-demand lease is being requested yet: one would be charged while the pod waited. It is retried until one of those nodes has room. Widening or removing the node selector or affinity would let it use the class's other nodes.
```

## Events When a Pod Is Admitted

### `RuntimeGuaranteed`

Type `Normal`. The pod was admitted. Its GPU is guaranteed until the time shown,
which is the end of its reservation, extended through any booking that directly
follows it.

```text
GPU access guaranteed for 1h09m59s, until 2026-09-23 10:15:11 PDT. The pod may keep running after that, but can be preempted if reserved capacity is needed.
```

For an on-demand lease, the guaranteed time is the requested runtime plus 10
minutes: a launch with the default 1-hour runtime reads about `1h10m`. The event
is written again each time the pod moves onto another reservation. After the
time shown, the pod keeps running unless its GPU is needed. See
[Overstay](../gpu-access/what-ends-a-session.md#overstay).

### `ReservationRelinked`

Type `Normal`. The running pod was moved onto another of its owner's
reservations, and is guaranteed until the time shown. The pod was not past its
guarantee. The message gives one of two causes:

- An on-demand lease merged into the owner's booking when the booking opened,
  and the lease was released. This usually follows a launch made more than 30
  minutes before a booked window. See
  [Launching Before the Window Opens](../gpu-access/reservations.md#launching-before-the-window-opens).
- The pod's reservation was cancelled or replaced while its window was open,
  usually by an **Extend** in the reservation app, and the pod was carried onto
  another open booking of the same owner instead of being deleted.

```text
Pod re-linked to GPU reservation #4213: the on-demand lease #4198 it started under was merged into it now that the reservation's window has opened, and the lease released. GPU access guaranteed until 2026-09-23 17:00:00 PDT.
```

```text
Pod re-linked to GPU reservation #4213: its previous reservation #4127 was cancelled or replaced. GPU access guaranteed until 2026-09-23 17:00:00 PDT.
```

A new `RuntimeGuaranteed` event comes with it. Nothing needs to change.

### `OverstayRelinked`

Type `Normal`. The pod was running past its guarantee, and has been moved onto
an open booking of the same owner, class, and workspace. It is guaranteed again
until the time shown. The booking is usually one that opened while the pod was
overstaying, or one made by an **Extend** of an on-demand lease whose window
had already ended. A new `RuntimeGuaranteed` event comes with it.

```text
Pod re-linked to GPU reservation #4213; no longer overstay. GPU access guaranteed until 2026-09-23 17:00:00 PDT.
```

### `BestEffortAdmitted`

Type `Normal`. The pod was admitted with no runtime guarantee and no charge.
Best-effort admission is not enabled on DSMLP.

## Events When a Pod Is Stopped

### `Preempted`

Type `Normal`. The pod was running past its guarantee, and its GPU was needed.
The pod was deleted: `SIGTERM`, then a grace period, then a forced stop. A pod
inside its guarantee is never preempted.

```text
Pod preempted to free capacity for reservation(s) starting 2026-09-23 12:00:00 PDT: overstayed its runtime guarantee by 45m03s.
```

The time named is when the booking that needed the GPU starts. The pod can be
stopped up to 15 minutes before that. A second form names headroom instead of a
booking:

```text
Pod preempted to maintain 15% free on-demand capacity headroom for gpu class medium: overstayed its runtime guarantee by 45m03s.
```

Where the message ends "its runtime guarantee could no longer be resolved", the
pod's reservation had already ended or been cancelled. Warning annotations
usually appear on the pod before a preemption. See
[Preemption](../gpu-access/what-ends-a-session.md#preemption) and
[The Termination Warning](../running-jobs/checkpointing.md#the-termination-warning).

### `ReservationCancelled`

Type `Normal`. The reservation the pod ran under was cancelled while its window
was open, and the pod was deleted. There is no warning beforehand.

| Message | Who cancelled |
|---|---|
| `Pod evicted: GPU reservation cancelled by user.` | The reservation's owner |
| `Pod evicted: GPU reservation cancelled by another user.` | A workspace manager, an administrator, or a teammate in team mode |
| `Pod evicted: GPU reservation cancelled by user (reason: superseded).` | An **Extend** replaced the reservation, and the pod could not be moved onto the new one |

Before deleting the pod, the reservation system moves it onto another open
booking of the same owner, where one matches and has room. A pod moved that way
keeps running and records [`ReservationRelinked`](#reservationrelinked) instead.
After an **Extend**, that is the usual outcome, and the `superseded` form above
is the exception.

Cancelling an in-progress booking in the reservation app deletes its pods. The
reservation shows as cancelled in **My Reservations**. For a cancellation that
was not expected, ask the workspace manager.

### `ReservationReassigned`

Type `Normal`. The booking was given to another user while its window was open,
usually because a teammate adopted it in team mode. The pod was deleted so that
the new owner can use the window. The message names the new owner.

```text
Pod evicted: GPU reservation reassigned to mlee.
```

See [Team Mode](../gpu-access/reservations.md#team-mode).

## Waiting With No Event

The reservation system writes no event in these cases. Only the scheduler's
`FailedScheduling` event appears, if any.

| Situation | What to do |
|---|---|
| The pod has no `gpu-class` label. The reservation system never sees it | Recreate the pod with the label. See [Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label) |
| The pod is seconds old, and the scheduler has not yet ruled on it | Wait a minute |
| The scheduler reports a shortage the reservation system cannot fix, such as `Insufficient memory` | Launch with smaller CPU or memory requests |
| The pod asks for 2 or more GPUs, which needs a raised GPU limit, and no single node has that many free | Wait, or ask for fewer GPUs. A pod runs on one node |
| The reservation app cannot be reached | Wait. If it lasts, contact [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |

A termination warning is not an event. It is a set of annotations on the pod.
See
[The Termination Warning](../running-jobs/checkpointing.md#the-termination-warning).
