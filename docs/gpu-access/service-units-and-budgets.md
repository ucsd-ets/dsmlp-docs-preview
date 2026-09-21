# Service Units & Budgets

From Fall 2026, GPU time on DSMLP is metered in **Service Units**. This page
covers what they are, what spends them, what an hour costs, what a cancellation
costs, and what happens when a budget is exhausted.

**Contents**

- [What a Service Unit Is](#what-a-service-unit-is)
- [What Spends Them, & What Does Not](#what-spends-them--what-does-not)
- [On-Demand Leases Charge Budget](#on-demand-leases-charge-budget)
- [Limiting the Spend](#limiting-the-spend)
- [The Size of a Budget](#the-size-of-a-budget)
- [What an Hour Costs](#what-an-hour-costs)
- [Peak & Off-Peak Hours](#peak--off-peak-hours)
- [The Rates Page](#the-rates-page)
- [A Worked Example](#a-worked-example)
- [Budget Windows & Cadences](#budget-windows--cadences)
- [Anchor Modes](#anchor-modes)
- [The Group Pool](#the-group-pool)
- [Changing a Budget](#changing-a-budget)
- [The Cancellation Penalty](#the-cancellation-penalty)
- [Cancelling in Advance](#cancelling-in-advance)
- [Having a Charge Waived](#having-a-charge-waived)
- [Reading Your Balance](#reading-your-balance)
- [When a Budget Runs Out](#when-a-budget-runs-out)

## What a Service Unit Is

------------------------------------------------------------------------

**A Service Unit (SU) is a usage credit for GPU time.** Each GPU class carries
an hourly SU rate, and every reservation is priced from that rate. The
arrangement is the familiar HPC allocation: a budget of credits, drawn down as
the machine is used, renewed on a cycle.
→ [Coming from HPC](../reference/coming-from-hpc.md)

**Service Units divide capacity; they do not bill for it.** Compute on DSMLP is
not chargeable. SU budgets are how a course's GPU-hours are divided evenly across
its roster rather than going to whoever books first, and how a shared research
pool divides among the labs drawing on it. *Storage above 1 TB is chargeable,
which is a separate matter and not measured in Service Units.*

**A reservation's cost is computed up front.** What a window will cost is
visible before it is confirmed, rather than afterwards. *That figure is the last
checkpoint before the spend.*

## What Spends Them, & What Does Not

------------------------------------------------------------------------

**Booking a window** spends them, priced by the class and the hours booked.

**Launching without a booking spends them too.** A launch with no reservation
creates one and charges for it. There is no free exploratory launch, and nothing
stops to ask: launching an eligible session is what authorizes the spend.

**Missing a booked window** spends up to 50% of it for nothing.
→ [The Cancellation Penalty](#the-cancellation-penalty)

**A window a manager books for a member does not.** An instructor, TA or PI may
book on a member's behalf, and that booking does not draw the member's budget.
*This is the fastest route for a student who has run out the evening before a
deadline.* → [Managing a Group](../reference/managing-a-group.md)

**Hours handed back in time do not.** Cancelling in advance carries no penalty,
and the charge is for the time actually used — as it is for an on-demand lease
cancelled inside its first two hours.

## On-Demand Leases Charge Budget

------------------------------------------------------------------------

**Starting a GPU session spends Service Units, whether or not the reservation
calendar is ever opened.** Launching without a booking creates a reservation on
the spot and draws Service Units exactly as a booked window would. **There is no
free exploratory launch.**

- **An unused session costs what a used one costs.** The charge is for holding
  the GPU, not for the work done on it. A notebook left open over dinner is
  billed for dinner.
- **Idle culling limits the charge; it does not prevent it.** A training run
  that finishes at midnight goes on drawing until the culler takes the card
  back — about 30 minutes on a busy night, and up to 6 hours on a quiet one.
  → [What Ends a Session](what-ends-a-session.md#the-timings)
- **A loop that relaunches is the expensive case.** A script that starts a fresh
  GPU session on each iteration, or a job restarted repeatedly during debugging,
  draws every time. Nothing stops it.
- **Service Units meter GPU time.** A CPU-only session is a different matter; it
  is GPU capacity that is scarce and budgeted.

## Limiting the Spend

------------------------------------------------------------------------

**Please stop sessions that are not in use.** From the browser,
**File → Hub Control Panel → Stop My Server**. From a terminal,
`kubectl delete pod <pod-id>`. *Logging out does not stop a session, and closing
VS Code does not release a pod.*
→ [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session)

**Please ask for the smallest GPU class the work fits in.** A larger class is
not faster for a model that fits in a smaller one, and it costs more per hour.
→ [Choosing a Class](gpu-classes.md#choosing-a-class)

**A balance is readable before a long run rather than after it.**
→ [Reading Your Balance](#reading-your-balance)

**A booked window is not more expensive than an on-demand one** — it is the same
spend, made deliberately — and off-peak hours are discounted.
→ [Reservations](reservations.md)

## The Size of a Budget

------------------------------------------------------------------------

**Budgets are per-workspace and set administratively.** For a course, cluster
administrators calculate the per-student budget to evenly divide the course's
weekly peak evening GPU allocation. A manager — an instructor, TA or PI — may
**not** edit a budget, but may request a change by ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

**Budgets belong to workspaces, not to people.** A student in one course, a TA in
another and a member of a lab holds a separate budget in each, on whatever cycle
each of them uses. *The budget drawn is the one belonging to the workspace
launched into* — the `-W` flag on the command line, or the environment picked on
the Datahub spawn form.
→ [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

<!-- FIGURE: a typical per-student weekly SU budget for a course workspace -->

## What an Hour Costs

------------------------------------------------------------------------

**Each GPU class carries its own hourly rate**, so the cost of an hour follows
the class booked. *Please book the smallest class the work fits in:* a larger
class is not faster for a model that already fits in a smaller one, and it is
scarcer.
→ [GPU Classes](gpu-classes.md)

**The hour of the day matters too.** Off-peak hours are discounted, to steer
usage away from peak evening demand.

<!-- FIGURE: the per-class hourly SU rate table, and whether it varies by term -->

## Peak & Off-Peak Hours

------------------------------------------------------------------------

**Off-peak discounts steer usage away from peak evening hours.** The quiet hours
are cheaper in Service Units than the evening ones.

**A shifted window is both cheaper and likelier to be granted.** On a busy
deadline evening the walk-up queue is real; at midday it usually is not.

**Work that moves easily is work that runs unattended.** A batch or background
job started overnight is the natural off-peak candidate; an interactive
debugging session is not.
→ [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes) ·
[Checkpointing & Logging](../running-jobs/checkpointing.md)

**A quiet cluster is more forgiving about idle sessions.** Where a GPU class is
under 75% allocated, an idle session may be left alone for up to 6 hours rather
than the usual 30 minutes.
→ [What Ends a Session](what-ends-a-session.md#the-timings)

**Availability that reads zero in the evening often reads differently in the
morning**, particularly for a workspace that sits in an overcommitted cohort.
→ [Cohorts](quotas-and-availability.md#cohorts)

*A discount changes the price, not the hardware.* An off-peak Medium is the same
Medium, and a discounted window is still a booking: the claim window, the
cancellation penalty and the runtime guarantee all apply exactly as they do at
peak.

## The Rates Page

------------------------------------------------------------------------

**The reservation interface publishes the rate schedule** as an effective-rate
chart across a full week, so the cheap hours are visible before a window is
committed to. *It is the only price-planning surface in the system.*

<!-- FIGURE: where the Rates page sits in the interface, and its exact name -->

## A Worked Example

------------------------------------------------------------------------

*Every figure in this example is a placeholder. The shape of the calculation is
right; the numbers are not published yet.* **Do not quote them; there are none.**

A member books one **Medium** GPU for **four hours**, Thursday 7-11 PM.

**When the booking is confirmed**, the cost is computed up front:

| | |
|---|---|
| Hourly rate, Medium, at that hour | <!-- FIGURE: peak hourly SU rate, Medium --> SU |
| Hours booked | 4 |
| Committed cost | <!-- FIGURE: 4 × the rate --> SU |

**Then one of four things happens.**

**All four hours are used.** The full committed cost is charged, and no penalty
applies.

**The booking is cancelled on Wednesday.** No penalty, and no charge — nothing
was used. The four hours return to the pool, where somebody else can book them.

**Two hours are used and the session shuts down.** The charge is for **two
hours** — <!-- FIGURE: 2 × the rate --> SU — and no penalty applies. The
remaining two hours return to the pool. *Handing back the tail of a session
carries no penalty; abandoning it does.*

**Nothing launches.** At 7:15 PM the reservation is cancelled, the capacity
returns to the pool, and a penalty of **up to 50% of the committed cost** —
at most <!-- FIGURE: half of the committed cost --> SU — is charged against the
member's budget. *The window is irrevocable: arriving at 7:30 does not recover
it, and neither does the rest of the evening.*
→ [The Claim Window](reservations.md#the-claim-window)

**The same four hours moved off-peak.** Booked for Wednesday 10 AM rather than
Thursday 8 PM:

| | Thursday, 8 PM | Wednesday, 10 AM |
|---|---|---|
| Hourly rate, Medium | <!-- FIGURE: peak rate --> SU | <!-- FIGURE: off-peak rate --> SU |
| Hours | 4 | 4 |
| Committed cost | <!-- FIGURE --> SU | <!-- FIGURE --> SU |
| Likelihood of getting it at all | Contested | Usually free |

**The cost is computed at booking**, so the comparison can be made in the
interface before anything is confirmed.

## Budget Windows & Cadences

------------------------------------------------------------------------

A Service Unit budget is not a one-off grant. It renews, and the cycle it renews
on depends on the kind of workspace it belongs to.

| Workspace | Budget window |
|---|---|
| **Course** | Weekly |
| **Research** | Monthly or quarterly, where a budget is set at all |

**A course's week is the planning unit.** Cluster administrators calculate the
per-student budget to evenly divide the course's weekly peak evening GPU
allocation. *A member's budget is, in effect, a share of the busiest hours of one
week.*

**A renewal is not a top-up.** A reservation is priced at the time it is booked,
and a budget window turning over mid-job does not change that price.

<!-- FIGURE: the SU budget figures themselves, for a course and for research -->

## Anchor Modes

------------------------------------------------------------------------

**A budget's "anchor mode" is how its window is fixed to the calendar** — what
"weekly" is weekly *from*. The reservation system supports more than one, among
them a rolling mode that does not reset on a calendar boundary.

*We are not yet in a position to say which modes DSMLP configures, or exactly
what a rolling window measures over.* The cadence table above is the reliable
part; the budget display itself is the authority on when a window turns over.

## The Group Pool

------------------------------------------------------------------------

**A workspace may hold a pool budget alongside its members' individual ones.**
Where it exists, it is a shared reserve for the group rather than an allocation
to any one member.

*Pooled budgets are expected to be uncommon in instruction.* Whether a research
group has one configured is a question for its PI.

## Changing a Budget

------------------------------------------------------------------------

**Budgets are set administratively.** A manager — an instructor, TA or PI — may
not edit a budget, not even their own group's, and no amount of privilege in the
interface changes that.
→ [Managing a Group](../reference/managing-a-group.md)

**Two routes exist.**

1. **A manager books on the member's behalf.** Immediate, and it does not draw
   the member's budget.
2. **A manager requests a change** by ticket to
   [datahub@ucsd.edu](mailto:datahub@ucsd.edu). Please include the workspace,
   what the work is, and the date by which it matters.

→ [The Six Requests](../reference/getting-help.md#the-six-requests)

## The Cancellation Penalty

------------------------------------------------------------------------

**A cancellation penalty of up to 50% of a booking applies to a window that is
abandoned rather than returned.** Cancelling in advance carries no penalty, and a
session handed back part-way through is charged for the time it used.

| Action | What it costs |
|---|---|
| Cancel well in advance | **No penalty.** Nothing was used, and nothing is charged |
| Hand back the tail of a session mostly used | **No penalty.** Charged for the hours used |
| Cancel an on-demand lease in its first 2 hours | **No penalty** |
| Cancel late | **Up to 50%** of the booking |
| Never claim the window at all | **Up to 50%** of the booking, and the window is gone |

**A no-show costs in two currencies.** Alongside the SU charge, the capacity is
gone for the rest of the window. *An on-demand launch remains possible*, subject
to what is free at that moment, and it draws on the member's budget in the same
way.

**Being charged for the hours used is not a penalty.** It is the ordinary cost of
the time. *A penalty is assessed against Service Units, not money* — nothing is
billed.

## Cancelling in Advance

------------------------------------------------------------------------

**An advance cancellation carries no penalty.** The capacity returns to the pool,
and the budget keeps what the window would have cost.

**The same applies to the unused tail of a session.** A container shut down
before its window ends is charged for the time it used, and the remainder goes
back to the pool.

**An on-demand lease has a two-hour grace.** A lease created by launching
without a booking may be cancelled inside its first two hours with no penalty.

*Please release a window as soon as it is known that it will not be used.*

## Having a Charge Waived

------------------------------------------------------------------------

**A workspace manager may waive the charge** — for a course, the instructor or
TA; for a lab, the PI. *Requests go to the manager: the control is theirs, not
ours.*

**A manager's waiver zeroes the member's share of the charge.** A full pardon is
an administrator action. *In a course this distinction rarely arises, since
pooled SU budgets are expected to be uncommon in instruction.*

A waiver is a judgement about circumstances — an illness, a booking made on a
member's behalf at the wrong hour, a cluster problem during the window — and not
an automatic remedy for a forgotten booking.

**One penalty cannot be waived by anyone:** where a teammate cancels a booking
in team mode, the resulting charge stands.
→ [Team Mode](reservations.md#team-mode)

**Researchers working outside a course have no manager to ask.** Where a penalty
was assessed in circumstances that warrant relief, write to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) and say what happened.

## Reading Your Balance

------------------------------------------------------------------------

**Where a member reads their balance is not documented.** From Fall 2026 GPU time
is metered in Service Units, drawn from a per-workspace budget — but the screen on
which the remainder is displayed is not named in any source available to this
project, and we will not guess at a URL.

*This page will name the screen as soon as we can confirm it.* In the meantime:

- **In a course**, the instructor or TA holds the group view. They can see the
  group's reservations and can book on a member's behalf when that member has run
  short. → [Managing a Group](../reference/managing-a-group.md)
- **In a research or project workspace**,
  [datahub@ucsd.edu](mailto:datahub@ucsd.edu) answers what a workspace's budget is
  and what remains of it.

**The price of a booking is visible before it is made**, so the cost of a window
is visible at the moment of confirmation even where the running total is not.

## When a Budget Runs Out

------------------------------------------------------------------------

**In a course, the instructor or TA is the route.** They have two, and the
immediate one is first:

1. **They book on the member's behalf.** This takes effect at once and does not
   draw the member's budget.
2. **They request an increase** by ticket to
   [datahub@ucsd.edu](mailto:datahub@ucsd.edu). The change itself is an
   administrative action; asking for it is a normal and sanctioned route.

**In a research workspace, write to us** at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu), naming the work and the date by
which it must be done. *Waiting for the window to renew is also a legitimate
answer where a deadline permits it.*

## Caveats & Limitations

------------------------------------------------------------------------

**A budget is not a quota.** A budget limits how much GPU time a member may
spend. A workspace's quota limits how many GPUs of a class it may hold at once.
Either can stop a launch, they stop it for different reasons, and budget
remaining does not mean a GPU is free.
→ [Group Quotas & Availability](quotas-and-availability.md)

**A budget window and a workspace quota are unrelated clocks.** A quota can
change week by week for reasons of its own — a deadline surge, for instance —
without anything happening to the budget.

**An idle session still occupies the window that was paid for.** Idle culling
will eventually end it, but until it does, the hours are spent. *Please shut down
sessions that are not in use.*
→ [What Ends a Session](what-ends-a-session.md)

**Access to a course workspace outlasts the course by one quarter**, but nothing
says a budget continues to renew through that period. *Budget beyond the
instructional term is not documented as continuing.*
→ [One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
