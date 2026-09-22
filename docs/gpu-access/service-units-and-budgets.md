# Service Units & Budgets

From Fall 2026, GPU time on DSMLP is metered in Service Units (SU). This page
covers what spends Service Units, hourly rates, budget sizes and renewal
windows, the cancellation penalty, and the routes available when a budget runs
out.

## What a Service Unit Is

A **Service Unit** (SU) is a usage credit for GPU time. Each GPU class carries
an hourly SU rate, and every reservation is priced from that rate. The scheme
follows the HPC allocation model: a budget of credits, drawn down as GPU time
is used and renewed on a cycle. HPC terms and their DSMLP equivalents are
mapped in
[Coming from HPC](../reference/coming-from-hpc.md).

Service Units divide capacity and are not billed. SU budgets divide a course's
GPU-hours evenly across its roster, and divide a shared research pool among
the labs that draw on it. Storage is not measured in Service Units. Storage
charges are covered in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

## What Spends Service Units

Service Units are spent when GPU time is booked or launched, and when a booked
window is missed.

| Action | Effect on the member's budget |
|---|---|
| Booking a window | Spends Service Units, priced by the GPU class and the hours booked |
| Launching a GPU session without a booking | Creates an on-demand lease and spends Service Units. See [On-Demand Lease Charges](#on-demand-lease-charges) |
| Missing a booked window | Charged the cancellation penalty. See [The Cancellation Penalty](#the-cancellation-penalty) |
| A window booked by an instructor, TA, or PI on the member's behalf | Does not draw the member's budget. See [Managing a Group](../reference/managing-a-group.md) |
| Cancelling a booking in advance, or handing back hours in time | No penalty. Charged for the time actually used. See [Cancelling in Advance](#cancelling-in-advance) |

## On-Demand Lease Charges

Launching a GPU session without a booking creates an **on-demand lease**: a
reservation made on the spot, which draws Service Units exactly as a booked
window would. This applies whether or not the reservation calendar is ever
opened.

> [!WARNING]
> There is no free exploratory launch. Launching an eligible GPU session is
> what authorizes the spend, and nothing prompts for confirmation.

- An unused session is charged at the same rate as a used one. The charge is
  for holding the GPU, not for the work done on it.
- A session that stops using its GPU continues to draw Service Units until
  idle culling reclaims the GPU. Idle culling waits longer on a quiet cluster
  than on a busy one. The thresholds are listed in
  [The Timings](what-ends-a-session.md#the-timings).
- A script that starts a new GPU session on each iteration, or a job restarted
  repeatedly during debugging, is charged on every launch. Nothing stops the
  repeated charges.

An on-demand lease cancelled within its first 2 hours carries no penalty, as
described in [Cancelling in Advance](#cancelling-in-advance).

## Limiting the Spend

Stop sessions that are not in use. From the browser, use
**File → Hub Control Panel → Stop My Server**. From a terminal, run
`kubectl delete pod <pod-id>`. The browser procedure is described in
[Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

> [!WARNING]
> Logging out does not stop a session, and closing VS Code does not release a
> pod.

Request the smallest GPU class the work fits in. A larger class is not faster
for a model that fits in a smaller one. Class selection is covered in
[Choosing a Class](gpu-classes.md#choosing-a-class).

Check the remaining balance before a long run, not after it. How to obtain the
balance is described in [Remaining Balance](#remaining-balance).

A booked window costs no more than an on-demand lease. Booking is described in
[Reservations](reservations.md). Off-peak hours are discounted, as described in
[Peak & Off-Peak Hours](#peak--off-peak-hours).

## The Size of a Budget

Budgets are per-workspace and set administratively. For a course, cluster
administrators calculate the per-student budget to evenly divide the course's
weekly peak evening GPU allocation. Budget figures for course and research
workspaces are not yet published. The routes for changing a budget are listed
in [Changing a Budget](#changing-a-budget).

A budget belongs to a workspace, not to a person. A person who is a student in
one course, a TA in another, and a member of a lab holds a separate budget in
each, on that workspace's cycle. The budget drawn is the one belonging to the
workspace launched into: the `-W` flag on the command line, or the environment
picked on the Datahub spawn form. Membership of more than one workspace is
described in
[Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).

### Budgets and Workspace Quotas

A budget limits how much GPU time a member may spend. A workspace's quota,
described in [Quotas, Cohorts & Availability](quotas-and-availability.md),
limits how many GPUs of a class the workspace may hold at once. Either can stop
a launch, for different reasons. Remaining budget does not mean a GPU is free.

A budget window and a workspace quota are independent. A quota can change from
week to week, for example during a deadline surge, without any change to the
budget.

## What an Hour Costs

Each GPU class carries its own hourly rate, so the cost of an hour depends on
the class booked. The classes are listed in
[GPU Classes](gpu-classes.md). The per-class hourly
rates, and whether they vary by term, are not yet published.

A booking's cost is computed from the rate and the hours booked, and is shown
before the booking is confirmed.

### Peak & Off-Peak Hours

Service Unit rates are discounted outside the peak evening hours. An off-peak
window is also more likely to be available. On a busy deadline evening there
is a walk-up queue; at midday there usually is not.

Batch and background jobs, which run unattended, are the work most easily
moved off-peak, for example by starting them overnight. An interactive
debugging session is not easily moved. Job modes are described in
[Job Modes](../running-jobs/job-modes-and-limits.md#job-modes),
and long unattended runs in
[Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md).

Availability that reads zero in the evening often reads differently in the
morning, particularly for a workspace in an overcommitted cohort, as described
in [Cohorts](quotas-and-availability.md#cohorts).

An off-peak booking is otherwise identical to a peak booking. The GPU hardware
is the same, and the runtime guarantee,
[The Claim Window](reservations.md#the-claim-window), and
[The Cancellation Penalty](#the-cancellation-penalty) apply exactly as they do
at peak.

### The Rates Page

The reservation interface publishes the rate schedule as an effective-rate
chart across a full week, so the discounted hours are visible before a window
is booked. The name and location of this view in the interface are not yet
published.

## Budget Windows & Cadences

A Service Unit budget renews on a cycle that depends on the kind of workspace
it belongs to.

| Workspace | Budget window |
|---|---|
| Course | Weekly |
| Research | Monthly or quarterly, where a budget is set at all |

A reservation is priced at the time it is booked. A budget window that renews
during a job does not change that price.

Whether a course budget continues to renew after the instructional term is not
yet published. Access after the term is described in
[One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter).

### Anchor Modes

The anchor modes configured for DSMLP budgets, which fix the calendar point
from which a budget window is measured, are not yet published.

## The Group Pool

A workspace may hold a pool budget alongside its members' individual budgets.
Where one exists, it is a shared reserve for the group rather than an
allocation to any one member. Pool budgets are expected to be uncommon in
course workspaces. The PI of a research group can state whether the group has
one configured.

## Changing a Budget

Budgets are set administratively. A workspace manager (an instructor, TA, or
PI) may not edit any budget, including that of the workspace they manage.
Manager privileges are listed in
[Managing a Group](../reference/managing-a-group.md).

Two routes exist:

1. The manager books on the member's behalf. The booking takes effect
   immediately and does not draw the member's budget.
2. The manager requests a change by ticket to
   [datahub@ucsd.edu](mailto:datahub@ucsd.edu), stating the workspace, what the
   work is, and the date by which it matters. The request format is described
   in [Administrative Requests](../reference/getting-help.md#administrative-requests).

## The Cancellation Penalty

A cancellation penalty of up to 50% of a booking applies to a window that is
abandoned rather than returned. Cancelling in advance carries no penalty, and a
session handed back part-way through is charged for the time it used. A
workspace manager may waive the penalty, as described in
[Having a Charge Waived](#having-a-charge-waived).

| Action | Charge |
|---|---|
| Cancel well in advance | No penalty. Nothing was used, and nothing is charged |
| Hand back the tail of a mostly used session | No penalty. Charged for the hours used |
| Cancel an on-demand lease in its first 2 hours | No penalty |
| Cancel late | Up to 50% of the booking |
| Never claim the window | Up to 50% of the booking, and the window is lost |

An unclaimed reservation is cancelled and its capacity returns to the pool. The
window cannot be recovered for its remainder. An on-demand launch remains
possible, subject to what is free at that moment, and draws on the member's
budget in the same way. Claiming a window is described in
[The Claim Window](reservations.md#the-claim-window).

A charge for hours used is the ordinary cost of the time, not a penalty.
Penalties are assessed in Service Units. No money is billed.

### Cancelling in Advance

An advance cancellation carries no penalty. The capacity returns to the pool,
and the budget keeps what the window would have cost.

The same applies to the unused tail of a session. A container shut down before
its window ends is charged for the time it used, and the remainder returns to
the pool.

An on-demand lease, created by launching without a booking, may be cancelled
within its first 2 hours with no penalty.

Release a window as soon as it is known that it will not be used.

### Having a Charge Waived

A workspace manager may waive the charge: for a course, the instructor or TA;
for a lab, the PI. Waiver requests go to the manager.

A manager's waiver zeroes the member's share of the charge. A full pardon is an
administrator action. In a course the distinction rarely arises, because pool
budgets are expected to be uncommon in course workspaces, as described in
[The Group Pool](#the-group-pool).

A waiver is a judgment about circumstances, such as an illness, a booking made
on a member's behalf at the wrong hour, or a cluster problem during the window.
It is not an automatic remedy for a forgotten booking.

A penalty that results from a teammate cancelling a booking in team mode cannot
be waived by anyone. Team bookings are described in
[Team Mode](reservations.md#team-mode).

Researchers working outside a course have no manager to ask. Where a penalty
was assessed in circumstances that warrant relief, write to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) and describe what happened.

## Remaining Balance

The screen on which a member reads the remaining Service Unit balance is not
yet published. In a course, the instructor or TA holds the group view, can see
the group's reservations, and can book on a member's behalf, as described in
[Managing a Group](../reference/managing-a-group.md).
In a research or project workspace,
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) answers what the workspace's budget
is and what remains of it.

## When a Budget Runs Out

In a course, the instructor or TA can book on the member's behalf, which takes
effect at once and does not draw the member's budget, or can request an
increase by ticket. Both routes are described in
[Changing a Budget](#changing-a-budget).

In a research workspace, write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu),
naming the work and the date by which it must be done. Where the deadline
permits, waiting for the budget window to renew is also an option, as described
in [Budget Windows & Cadences](#budget-windows--cadences).
