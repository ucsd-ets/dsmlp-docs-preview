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
every 2 to 5 minutes. An event that suggests contacting support names
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
| [`RuntimeGuaranteed`](#runtimeguaranteed) | Normal | Admitted | The pod was admitted, and its GPU is guaranteed until the time shown |
| [`OverstayRelinked`](#overstayrelinked) | Normal | Admitted | The running pod was moved onto a newer reservation and is guaranteed again |
| [`BestEffortAdmitted`](#besteffortadmitted) | Normal | Admitted | The pod was admitted with no guarantee and no charge |
| [`Preempted`](#preempted) | Normal | Stopped | The pod was past its guarantee and was stopped to free its GPU |
| [`ReservationCancelled`](#reservationcancelled) | Normal | Stopped | The reservation the pod ran under was cancelled, and the pod was deleted |
| [`ReservationReassigned`](#reservationreassigned) | Normal | Stopped | The booking was given to another user, and the pod was deleted |

## Events While a Pod Waits

A GPU pod waits in `Pending` until the reservation system admits it. While it
waits, `kubectl describe pod` also shows a `FailedScheduling` event from the
Kubernetes scheduler about untolerated taints. That scheduler event is normal
for every GPU pod that has not been admitted yet, and does not mean the label is
wrong or the cluster is full. See
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

### `ReservationTooSmall`

Type `Warning`. The pod requests more GPUs than its booking holds, so the
booking can never admit it. Two bookings are never combined for one pod. On
DSMLP this event is not expected: a pod that asks for more GPUs than its booking
holds is given an on-demand lease, charged separately, instead of waiting. See
[Claiming a Booking](../gpu-access/reservations.md#claiming-a-booking).

### `OnDemandLeaseDenied`

Type `Warning`. The pod has no booking open, so the reservation system asked
the reservation app for an on-demand lease, and the app refused. The message
quotes the app's reason word for word:

```text
On-demand GPU lease for 2 x medium was denied by the reservation service: Only 1 GPU(s) available at 2026-09-23 19:07. The pod stays Pending; the controller will keep retrying.
```

The request is retried every 2 to 5 minutes for as long as the pod exists. The
message always ends "will keep retrying", including for reasons that waiting
cannot fix.

| Reason quoted | Meaning | Waiting helps |
|---|---|---|
| `Only N GPU(s) available at …` | The class has too few free GPUs at that time | Yes |
| `Only N GPU(s) available for this group at … (group ceiling: …)` | The workspace already holds its GPU limit for the class. Figures such as `borrowed` and `buffer` in the brackets describe idle capacity the workspace could borrow | Yes, as other members' jobs end |
| `Only N GPU(s) available for this cohort at … (cohort ceiling: …)` | The workspaces that share capacity with this one hold all of it. See [Cohorts](../gpu-access/quotas-and-availability.md#cohorts) | Yes |
| `This lease costs X SU but user '…' has only Y of Z SU remaining …` | The Service Unit (SU) budget cannot cover the lease | Yes, when the budget window renews, unless X is more than Z |
| `This lease costs X SU but the group pool only has …` | The workspace's shared SU pool is spent | Yes, when the budget window renews |
| `User '…' is not a member of group '…'` | The user is not enrolled in the workspace the pod named | No. Launch with `-W` naming a workspace the user belongs to, or ask the instructor or TA to check the roster |
| `GPU class not accessible under this group` | The workspace was not granted this class | No. Use a class the workspace was granted |
| `Exceeds limit of N GPU(s) per reservation` | The pod asks for more GPUs than the class allows in one reservation | No. Launch with fewer GPUs |
| `This lease runs H hours but group '…' limits a single reservation to N hours.` | The lease would be longer than the workspace's length cap | No |
| `Group '…' is not active on …` | The workspace is outside its active dates. The message can show `{group.name}` and `{start_date}` in place of the name and date | Only if the workspace's dates have not started yet |

Where waiting cannot help, delete the pod with `kubectl delete pod <pod-name>`.

> [!WARNING]
> A pod left `Pending` keeps being retried. When the lease is granted, the pod
> starts and Service Units are charged, even if nobody is waiting for it any
> more. Delete a pending GPU pod that is no longer wanted.

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
  placed. Pods with a reservation go first.

Nothing about the pod needs to change. Leave it in place. The on-demand queue is
ordered by pod creation time, so deleting and recreating the pod moves it to the
back. If the pause lasts, contact
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

### `UnknownGpuClass`

Type `Warning`. The pod's `gpu-class` label names no class the reservation app
knows, so nothing can admit the pod. The message lists the known classes.
Labels are case-sensitive. Correct the label and recreate the pod.

```text
This pod's gpu-class label is Medium, which is not a GPU class the reservation service knows, so no reservation can match it and it cannot be admitted on demand. Known classes: extra-large, extra-small, large, medium, small. Correct the label and recreate the pod; if it is right, contact support: datahub@ucsd.edu
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

### `OverstayRelinked`

Type `Normal`. The running pod was moved onto a newer reservation, and is
guaranteed again until the time shown. This follows an **Extend** in the
reservation app, a new booking that opened for the same user and class, or an
on-demand lease being merged into the user's booking when the booking opened.
A new `RuntimeGuaranteed` event comes with it.

```text
Pod re-linked to GPU reservation #4213; no longer overstay. GPU access guaranteed until 2026-09-23 17:00:00 PDT.
```

The message says "no longer overstay" even where the pod was still inside its
guarantee.

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
| The pod asks for 2 or more GPUs, and no single node has that many free | Wait, or ask for fewer GPUs. A pod runs on one node |
| The reservation app cannot be reached | Wait. If it lasts, contact [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |

A termination warning is not an event. It is a set of annotations on the pod,
described in
[The Termination Warning](../running-jobs/checkpointing.md#the-termination-warning).
