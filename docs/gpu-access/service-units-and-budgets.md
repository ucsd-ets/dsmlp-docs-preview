# Service Units & Budgets

From Fall 2026, GPU time on DSMLP is metered in Service Units (SU), and each
workspace member has a budget of them.

## What a Service Unit Is

A **Service Unit** (SU) is a usage credit for GPU time. Each GPU class carries
an hourly SU rate, and every reservation is priced from that rate. The scheme
follows the HPC allocation model: a budget of credits, drawn down as GPU time
is used and renewed on a cycle. HPC terms and their DSMLP equivalents are
mapped in
[Coming from HPC](../reference/coming-from-hpc.md).

Service Units divide capacity and are not billed. Storage is not measured in
Service Units. Storage charges are covered in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

## What Spends Service Units

| Action | Effect on the member's budget |
|---|---|
| Booking a window | Spends Service Units when the booking is made, priced by the GPU class, the hours, and the number of GPUs |
| Launching a GPU session without a booking | Creates an on-demand lease and spends Service Units. See [On-Demand Lease Charges](#on-demand-lease-charges) |
| A window booked by an instructor, TA, or PI on the member's behalf | Charged to the member's budget, as if the member had booked it. See [Bookings by a Workspace Manager](reservations.md#bookings-by-a-workspace-manager) |
| Cancelling at least 24 hours before the start | Nothing |
| Cancelling later, or during the window | The time used, plus a share of the unused time. See [The Cancellation Penalty](#the-cancellation-penalty) |
| Missing a booked window | Charged as a cancellation at the moment the booking is declared a no-show |
| Running past the end of a reservation | Nothing. See [Overstay](what-ends-a-session.md#overstay) |
| A session with no GPU | Nothing. CPU-only sessions are outside the reservation system |

## On-Demand Lease Charges

Launching a GPU session without a booking creates an **on-demand lease**: a
reservation made on the spot, which draws Service Units exactly as a booked
window would. This applies whether the reservation app is ever opened.

> [!WARNING]
> There is no free exploratory launch. Launching an eligible GPU session is
> what authorizes the spend, and nothing prompts for confirmation.

A lease covers the session's declared runtime plus 10 minutes, and is charged
when it is granted. A session that declares no runtime is given 1 hour, so it
holds a lease of 1 hour 10 minutes. The declared runtime is separate from the
6-hour runtime limit, which stops the pod. When the session ends, the lease is
cancelled and the charge is recalculated:

- The time used is charged in full.
- Unused time in the lease's first 2 hours is free.
- Unused time after the first 2 hours is charged on the scale in
  [The Cancellation Penalty](#the-cancellation-penalty).

A lease of 1 hour 10 minutes ends inside its first 2 hours, so it is charged for
the time used and nothing more. For example, a default launch on one `medium`
GPU at the full rate is charged about 1.17 SU when the lease is granted. If the
session stops after 40 minutes, about 0.67 SU is kept.

A session that runs past the end of its lease draws no further Service Units,
and is no longer protected; see [Overstay](what-ends-a-session.md#overstay). A
longer guarantee comes from [Extend](reservations.md#extend), which is a booking
and is charged like one.

- An unused session is charged at the same rate as a used one. The charge is
  for holding the GPU, not for the work done on it.
- A session that stops using its GPU continues to draw Service Units until
  idle culling reclaims the GPU. Idle culling waits longer on a quiet cluster
  than on a busy one. The thresholds are listed in
  [The Timings](what-ends-a-session.md#the-timings).
- A script that starts a new GPU session on each iteration, or a job restarted
  repeatedly during debugging, is charged on every launch. Nothing stops the
  repeated charges.
- A pod left waiting for a lease starts, and is charged, whenever the lease is
  granted. See
  [Waiting for an On-Demand Lease](quotas-and-availability.md#waiting-for-an-on-demand-lease).

## Limiting the Spend

Stop sessions that are not in use. From the browser, use
**File → Hub Control Panel → Stop My Server**. From a terminal, run
`kubectl delete pod <pod-id>`. The browser procedure is described in
[Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

> [!WARNING]
> Logging out does not stop a session, and closing VS Code does not release a
> pod.

Request the smallest GPU class the work fits in. A larger class is not faster
for a model that fits in a smaller one, and it costs more per hour; see
[What an Hour Costs](#what-an-hour-costs). Class selection is covered in
[Choosing a Class](gpu-classes.md#choosing-a-class).

Check the remaining balance before a long run, not after it; see
[Remaining Balance](#remaining-balance).

A booked window costs no more than an on-demand lease for the same hours.
Booking is described in [Reservations](reservations.md). Off-peak hours are
discounted. See [Peak & Off-Peak Hours](#peak--off-peak-hours).

## The Size of a Budget

Every workspace gives each member 10 SU per week by default, in course and
research workspaces alike, and in `ORG_ON_DEMAND`, the default workspace. The
instructor or researcher can ask for a different figure. The routes for
changing a budget are listed in [Changing a Budget](#changing-a-budget).

At the rates in [What an Hour Costs](#what-an-hour-costs), 10 SU buys 10
GPU-hours of `medium` at the full rate, or 20 off-peak.

A budget belongs to a workspace, not to a person. A person who is a student in
one course, a TA in another, and a member of a lab holds a separate budget in
each, on that workspace's cycle. A reservation draws on the budget of the
workspace it is made under: the workspace chosen in the booking wizard, or, for
an on-demand lease, the workspace the pod's `dsmlp/course` label names.
`launch.sh -W` sets that label, and a pod that names no workspace is charged to
`ORG_ON_DEMAND`. See
[The Default Workspace](reservations.md#the-default-workspace) and
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

A reservation costs the class's rate, times the hours, times the number of GPUs.
The rates in force for Fall 2026:

| Class | SU per GPU per hour | Off-peak |
|---|---|---|
| `extra-small` | 0.25 | 0.125 |
| `small` | 0.5 | 0.25 |
| `medium` | 1 | 0.5 |
| `large` | 2 | 1 |
| `extra-large` | 4 | 2 |

For example, 3 hours of two `medium` GPUs at the full rate costs 6 SU. The
**Rates** page in the reservation app is the authority on current rates; see
[The Rates Page](#the-rates-page). The booking wizard shows a booking's cost
before it is confirmed.

### Peak & Off-Peak Hours

Service Unit rates are discounted by 50% in the off-peak hours, 1 AM to 4 PM
Pacific time. The peak hours run from 4 PM to 1 AM. The discounted hours are
marked on the **Rates** page, which shows them for each day of the week, and by
an amber strip on the booking wizard's timeline. An off-peak window is also more likely to be available. On a
busy deadline evening there is a walk-up queue; at midday there usually is not.

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

**Rates**, in the reservation app's sidebar, charts the rate of every GPU class
for each of the 168 hours of a week. Bar height is the rate; shorter amber bars
are discounted hours. Point at a bar for its exact rate, and use **‹** and
**›** to move between weeks.

**Show rate summary table** lists each class's discount windows. The table can
list a discount window that does not apply in the week shown; the chart is
exact. The Rates page gives rates in `SU/hr` and the booking wizard in
`SU/GPU·h`. Both are per GPU.

## Budget Windows & Cadences

A Service Unit budget renews weekly by default, in every workspace: from
Monday 00:00 to the next Monday 00:00, Pacific time. A workspace can be given a
different window on request. The Dashboard shows the window in force; see
[Anchor Modes](#anchor-modes).

A reservation is charged wholly to the window its start falls in, however far
it runs into the next. A booking made for a later week draws on that week's
budget, not the current one's.

- Unused budget does not carry over to the next window.
- No warning is sent as a budget runs low.
- A reservation is priced when it is booked. A window that renews during a job
  does not change that price.

Whether a course budget continues to renew after the instructional term is not
yet published. Access after the term is described in
[One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter).

### Anchor Modes

The Dashboard labels each workspace's budget with its mode:

| Label | How the budget renews |
|---|---|
| **Weekly** | Each Monday. The default for every workspace |
| **Monthly** | On the first day of each month |
| **Quarterly** | On the first day of January, April, July, and October |
| **Rolling** | It does not renew. Only reservations that have not yet ended count, and their SU returns as each one ends |
| **Since creation** | It never renews |

## Remaining Balance

The **SU Budget** card on the reservation app's **Dashboard** shows one block
for each workspace that has a budget. **Current Window** gives the window's
first day and the day the budget renews. A bar shows the SU committed against
the budget, and a line below it gives the figures:

| Figure | Meaning |
|---|---|
| **Budget** | The budget for this window, including any increase an administrator has applied |
| **Used** | Reservations in this window that have ended |
| **Open** | Reservations in this window that have not yet ended |
| **Cancelled** | SU kept as cancellation penalties |
| **Remaining** | The budget, less Used, Open, and Cancelled |
| **Planned ahead** | SU booked into later windows, which draw on those windows' budgets |

The bar and the figure beside it leave out **Cancelled**, so they do not add up
to **Remaining** when a penalty has been kept. In team mode the block reads
**Team budget**, and a workspace with a pool shows a **Group pool** row. An
increase an administrator applies changes **Budget** without any other notice.

The booking wizard also shows a budget meter above its timeline. There, "used"
means everything charged to that window: ended, open, and kept penalties.

## The Group Pool

A workspace may hold a pool budget alongside its members' own budgets. A
reservation draws on both. The pool also limits workspace managers, and can
refuse a booking when the member's own budget still has room. Pool budgets are
expected to be uncommon in course workspaces. The PI of a research group can
state whether the group has one configured.

## Changing a Budget

Budgets are set administratively. A workspace manager (an instructor, TA, or
PI) may not edit any budget, including that of the workspace they manage.
Manager privileges are listed in
[Managing a Group](../reference/managing-a-group.md).

To change a budget, the manager requests it by ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu), stating the workspace, what the
work is, and the date by which it matters. The request format is described in
[Administrative Requests](../reference/getting-help.md#administrative-requests).

A booking a manager makes on a member's behalf does not add to the member's
budget. It is charged to the member.

## The Cancellation Penalty

Cancelling a booking at least 24 hours before its start costs nothing. Any other
cancellation keeps part of the booking's cost:

1. The time already used is charged in full.
2. The unused time that falls within the next 24 hours is counted. Unused time
   beyond that is free.
3. An exemption of half the used and counted time together, at most 8 hours, is
   free.
4. If the counted time is no more than the exemption, nothing more is charged.
   Otherwise the charge is the cost of the counted time, multiplied by the
   counted time less the exemption, divided by the counted time.

The counted time is priced at the rates of the hours it covers, off-peak
discounts included. Examples on one `medium` GPU at the full rate, where 1 SU is
one hour:

| Situation | SU kept |
|---|---|
| Any booking, cancelled 24 hours or more before its start | 0 |
| A 4-hour booking, cancelled 1 hour before its start | 2 |
| A 12-hour booking, cancelled 1 hour before its start | 6 |
| A 12-hour booking, cancelled 20 hours before its start | 2: only 4 of its hours fall within the next 24 |
| A 24-hour booking, cancelled at its start | 16 |
| A 12-hour booking, cancelled 6 hours in | 6, the time used |
| A 12-hour booking, cancelled 2 hours in | 6: 2 used and 4 of penalty |
| A 48-hour booking, cancelled 10 hours in | 26: 10 used and 16 of penalty |

Two consequences follow. A booking cancelled before it starts keeps half the
cost of its hours that fall within the next 24 hours; where more than 16 of its
hours fall in that span, it keeps all but 8 hours' worth of them. Handing back
the rest of a booking in progress is free only when the rest is no longer than
the time already used, and no more than 8 hours.

A no-show is charged on the same scale, at the moment the booking is declared a
no-show; see [The Claim Window](reservations.md#the-claim-window). An on-demand
lease is charged on the same scale, except that unused time in its first 2 hours
is free; see [On-Demand Lease Charges](#on-demand-lease-charges).

A kept penalty appears on the Dashboard as **Cancelled** and counts against the
budget window until the window renews. A waiver frees it at once. Penalties are
assessed in Service Units. No money is billed.

### Cancelling a Booking

On **My Reservations**, select **Cancel** on the reservation. The dialog states
what the cancellation will cost:

- For a booking that starts within 24 hours:
  `Late cancellation: X SU will be charged for reserved hours within the next 24 h (part is exempt).`
- For a booking in progress: `You will be credited X SU.`, and a warning that
  pods running under the booking will be stopped.
- For a booking more than 24 hours away: no notice, because nothing is charged.

Select **Yes, Cancel** to confirm. Cancelling a booking in progress deletes the
sessions running under it; see
[`ReservationCancelled`](../reference/reservation-events.md#reservationcancelled).

### Cancelling in Advance

A booking cancelled at least 24 hours before its start costs nothing, and the
capacity returns to the pool. Release a window as soon as it is known that it
will not be used.

### Having a Charge Waived

A workspace manager may waive a penalty: for a course, the instructor or TA; for
a lab, the PI. Waiver requests go to the manager. A member cannot waive a
penalty on their own cancellation.

A manager waives a penalty when cancelling a member's booking, with **Waive this
penalty**, or afterwards, with the waive button on the cancelled reservation on
**Group Reservations**. A penalty from a teammate's cancellation in team mode is
waived afterwards in the same way. A manager's waiver clears the member's share
of the penalty. Where the workspace has a pool, only an administrator clears the
pool's share. See [The Group Pool](#the-group-pool).

A waiver is a judgment about circumstances, such as an illness, a booking made
on a member's behalf at the wrong hour, or a cluster problem during the window.
It is not an automatic remedy for a forgotten booking.

Researchers working outside a course have no manager to ask. Where a penalty
was assessed in circumstances that warrant relief, write to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) and describe what happened.

## When a Budget Runs Out

A spent budget blocks the member's bookings and on-demand leases until the
window renews. A pending GPU session waits with an `OnDemandLeaseDenied` event
that quotes the budget; see
[Reservation Events](../reference/reservation-events.md#ondemandleasedenied).

A budget on the default weekly window renews each Monday. In a course, the
instructor or TA can request an increase by ticket. See
[Changing a Budget](#changing-a-budget). A booking the instructor or TA makes on
the member's behalf is charged to the member, so it does not help.

In a research workspace, write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu),
naming the work and the date by which it must be done. Where the deadline
permits, waiting for the budget window to renew is also an option, as described
in [Budget Windows & Cadences](#budget-windows--cadences).
