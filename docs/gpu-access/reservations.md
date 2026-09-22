# Reservations

From Fall 2026, every GPU session on DSMLP runs on a reservation, either booked
ahead of time or created when the session launches. This page covers the
reservation types, the claim window, length caps, best-effort reservations, and
team mode.

## Reservation Types

| Type | When it starts | What it costs | What protects it |
|---|---|---|---|
| Booked window | At the booked window; see [The Claim Window](#the-claim-window) | Service Units, computed up front | A runtime guarantee for the length of the window |
| On-demand lease | At launch, if capacity is idle | Service Units, as for a booked window | It is a reservation and is treated as one |
| Best-effort | At launch | Free; the Service Unit treatment is not yet published | Nothing |

## Booking Ahead

A **reservation** is a booking of a GPU class for a window of time. During the
window the capacity is held, and a session launched into it is admitted ahead
of the walk-up queue.

A reservation guarantees access, not a running job. Nothing starts
automatically when the window opens. A notebook, a shell session, or a batch
job is launched in the usual way and lands on the held capacity, as described
in [From Reservation to Running Session](gpu-classes.md#from-reservation-to-running-session).
A booked window in which no session is launched is charged, as described in
[The Claim Window](#the-claim-window).

## Launching Without a Booking

> [!WARNING]
> Launching an eligible GPU session without a booking creates an on-demand
> lease and charges the member's Service Unit budget as a booked window would;
> there is no free exploratory launch. See
> [On-Demand Lease Charges](service-units-and-budgets.md#on-demand-lease-charges).

An on-demand lease draws on whatever capacity is idle at the moment of launch.
Off-peak, the lease is granted close to instantaneously, and it is the usual
route for day-to-day work.

### Availability and Denied Leases

On a busy deadline evening, reserved users are admitted first, and an
on-demand request may wait or be refused
([When the Cluster Is Full](quotas-and-availability.md#when-the-cluster-is-full)).
A session that did not start because its lease was denied reports the
`OnDemandLeaseDenied` event, listed under
[Reservation Events](../running-jobs/kubernetes.md#reservation-events).

### Cancelling an On-Demand Lease

The first 2 hours of an on-demand lease are penalty-free on cancellation
([The Cancellation Penalty](service-units-and-budgets.md#the-cancellation-penalty)).
A lease started and stopped within that period is charged for the time used and
nothing more.

## Choosing Between Booking and Launching

| Situation | Route |
|---|---|
| A GPU is needed on Thursday evening | Book a window |
| A twenty-minute experiment, now, at 11am | Launch without a booking. Daytime capacity is generally idle |
| A run that will take two days | Book a window after checking [Reservation Length Caps](#reservation-length-caps) |
| Work whose answer is not needed today, done cheaply | Run it off-peak; see [Peak & Off-Peak Hours](service-units-and-budgets.md#peak--off-peak-hours) |
| Work that can start now and accept being interrupted | Use a best-effort reservation; see [Best-Effort Reservations](#best-effort-reservations) |

## What a Booking Names

A booking names a GPU class, a number of GPUs, and a window of time, for
example "Tuesday 9am-7pm: 4× `extra-large`". It is made through the reservation
web interface and holds that capacity until the window ends. The booking form
is the authority on booking conventions and refuses a window it cannot accept.
The classes are described in
[GPU Classes](gpu-classes.md).

## The Claim Window

A booked window must be claimed within 15 minutes of its start. Claiming a
reservation means starting a session on its capacity.

> [!WARNING]
> If no session launches inside the claim window, the reservation is treated as
> a no-show. It is cancelled, the capacity returns to the pool, and the window is
> lost for the rest of its length. A no-show is also charged, as described in
> [The Cancellation Penalty](service-units-and-budgets.md#the-cancellation-penalty)
> and [Having a Charge Waived](service-units-and-budgets.md#having-a-charge-waived).

The claim window is measured from the start of a window already held. It does
not govern how far ahead a booking may be made.

### Claiming a Window

Claiming is launching. There is no separate confirmation step. A notebook, a
shell session, or a batch job starts in the usual way, and the session landing
on the reservation claims it.

The claim window runs during the launch itself. Pulling a large custom image,
or the first launch of a term, is not instant. A window cannot be claimed
before it starts.

## Reservation Length Caps

Two ceilings apply to the length of one reservation.

| Cap | Applies to |
|---|---|
| 48 hours | An ordinary member's reservation |
| 168 hours | Every reservation. No one exceeds it, administrators included |

### Workspace Length Caps

A workspace's own cap may be shorter than either ceiling. Each workspace sets
one, matched to the work it was provisioned for: course workspaces use short
caps, and research workspaces can permit multi-day windows well beyond them. A
booking refused for its length has met a workspace setting rather than a
platform limit. Requests about the workspace cap go to the PI or instructor.

See also: [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)

## Reservation Length and Session Runtime

A reservation's length and a session's runtime are separate limits. A long
booking does not by itself grant a long-running session.

A reservation holds GPU capacity for a window of time: a 48-hour booking holds
the hardware across those 48 hours. A session, the pod a launch creates, runs
for 6 hours by default and up to 12 hours where that is set at launch, as
described in
[The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit);
runs beyond 12 hours are requested from
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

A run that writes its progress to durable storage at intervals can be picked up
again; a single uninterruptible process cannot
([Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md)).

Idle culling applies to a session for its whole life, however long the
reservation behind it, and a reserved GPU that stops being used is reclaimed
like any other
([What Counts as Idle](what-ends-a-session.md#what-counts-as-idle)).

## The Booking Horizon

Bookings are accepted within a rolling window that has a minimum and a maximum
distance ahead and moves forward with the date. Neither bound is yet published.
The booking form is the authority on how far ahead a window may be placed.

See also: [Borrowing Beyond Quota](quotas-and-availability.md#borrowing-beyond-quota)

## Planning a Long Window

Book the GPU class the work needs rather than the largest one available. Class
selection is covered in [GPU Classes](gpu-classes.md),
and booking costs in [Service Units & Budgets](service-units-and-budgets.md).

Unused time can be released. Releasing the remainder of a booking after the
work finishes carries no cancellation penalty: the charge is for the time
actually used, and the remainder returns to the pool
([Cancelling in Advance](service-units-and-budgets.md#cancelling-in-advance)).

## Best-Effort Reservations

A best-effort reservation starts immediately and carries no guarantee. An
ordinary reservation holds capacity and protects the session for the length of
the window. A best-effort reservation holds nothing: it runs on spare capacity
and releases that capacity as soon as a session with a claim on it arrives.

Best-effort is a deliberate choice to run without the guarantee. It differs
from the default on-demand lease described in
[Launching Without a Booking](#launching-without-a-booking).

Idle culling, the runtime limit, and the workspace's GPU class grants apply to
a best-effort session as they do to any other. Best-effort is not a route
around a Service Unit budget. The options for a member whose budget is
insufficient are in
[When a Budget Runs Out](service-units-and-budgets.md#when-a-budget-runs-out).

### Preemption

> [!WARNING]
> A best-effort session can be preempted at any point in its life, including
> immediately after it starts, and the preemption may arrive without a signal
> the running code can catch. Only work already saved to disk survives.

There is no protected initial period and no point after which a best-effort
session is safe from preemption. The session records the ending as a
`Preempted` Kubernetes event, which distinguishes a preemption from a program
crash ([Reservation Events](../running-jobs/kubernetes.md#reservation-events)).

### Suitable Uses

- Work that checkpoints. A training run that resumes from disk loses minutes to
  a preemption rather than hours
  ([Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md)).
- Attended work: debugging, a first pass over a dataset, or checking that a
  model builds and a batch runs. Losing the container costs a re-launch.
- Spare capacity that nobody has booked, such as capacity at eleven in the
  morning.

Best-effort is unsuitable for work with a deadline. A reservation is the only
mechanism on the platform that guarantees a GPU at a particular time.

## Team Mode

Team mode lets members of a team act on one another's reservations. A teammate
can cancel another member's booking, and the penalty for that cancellation
cannot be waived
([Having a Charge Waived](service-units-and-budgets.md#having-a-charge-waived)).

Other team mode mechanics are not yet documented. Contact
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) before planning work that depends
on team mode.

### Team Data and the `-G` Flag

The `launch.sh -G` flag controls which team data is visible, not reservations.
`-G list` prints the teams an account belongs to, and `-G <teamid>` launches
with that team's data visible under `teams/`. No connection between this flag
and team mode in the reservation system is documented. Team data is described
in
[Sections, Teams and Group Data](../workspaces-and-storage/what-a-workspace-is.md#sections-teams-and-group-data).

> [!NOTE]
> `-g` is the GPU count and `-G` is the group flag: `-g 1` asks for one GPU,
> and `-G 1` does not. See
> [Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags).

## Continue, Extend & Adopt

Continue, Extend, and Adopt are operations in the reservation system's
vocabulary that act on a reservation already held. Their mechanics are not yet
documented.

No reservation exceeds the absolute ceiling in
[Reservation Length Caps](#reservation-length-caps). GPU time draws Service
Units, and a longer booking is a larger charge, however the extra time is
arranged.

## Routes to More Time

Book the full time the work requires at the outset. Time released early is
charged only for the hours used, as described in
[Planning a Long Window](#planning-a-long-window). A run that checkpoints can
resume from disk after a window ends, as described in
[Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md).

### Running Past the Window

There is no hard kill when a window closes, and an in-session countdown runs.
Past the window the time is no longer guaranteed, the session has no protection
once the capacity is wanted, and overstay has a cost
([Overstay](what-ends-a-session.md#overstay)). The cost of overstay is not yet
published.

### Bookings by a Workspace Manager

An instructor, TA, or PI can book on a member's behalf, and that booking does
not draw the member's budget. For a project that has outgrown its budget, a
workspace manager can request a change by ticket
([Managing a Group](../reference/managing-a-group.md)).

## What Governs How Much Is Held

A workspace has a quota per GPU class, the most of that class the whole
workspace may hold at once
([Quotas, Cohorts & Availability](quotas-and-availability.md)). Separately,
each member has a Service Unit budget that meters the member's own share
([Service Units & Budgets](service-units-and-budgets.md)).

A workspace quota is not a hard ceiling; the conditions for exceeding it are in
[Borrowing Beyond Quota](quotas-and-availability.md#borrowing-beyond-quota).
Availability can also read zero while a workspace still has headroom under its
quota, as described in [Cohorts](quotas-and-availability.md#cohorts).
