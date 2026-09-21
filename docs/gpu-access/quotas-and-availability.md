# Quotas, Cohorts & Availability

**A quota is a ceiling on how much of the cluster a workspace may hold at
once.** It is not a reservation of hardware, it is not an individual allowance,
and it is not the same thing as a Service Unit budget. This page covers quotas,
the cohort mechanism that makes availability read zero while a quota has room,
what a full cluster looks like, and what the status page can and cannot tell you.

**Contents**

- [What a Quota Is](#what-a-quota-is)
- [Quotas Move with the Calendar](#quotas-move-with-the-calendar)
- [Borrowing Beyond Quota](#borrowing-beyond-quota)
- [The Reserve Floor](#the-reserve-floor)
- [Cohorts](#cohorts)
- [Zero Availability With Headroom Remaining](#zero-availability-with-headroom-remaining)
- [Not Every Cohort Is Overcommitted](#not-every-cohort-is-overcommitted)
- [The Other Ceilings](#the-other-ceilings)
- [When the Cluster Is Full](#when-the-cluster-is-full)
- [What the Platform Does Not Report](#what-the-platform-does-not-report)
- [What Actually Helps](#what-actually-helps)
- [Waiting for Capacity](#waiting-for-capacity)
- [The Status Page](#the-status-page)
- [Free Is Not the Same as Available](#free-is-not-the-same-as-available)
- [Asking for More](#asking-for-more)

## What a Quota Is

------------------------------------------------------------------------

**Per-group quotas set the maximum number of each GPU class a workspace may hold
at one time.**

**The quota belongs to the workspace, not to the member.** Everyone in a course
or lab draws on the same ceiling. A launch refused because the workspace is at
its limit means the capacity is being held by other members — Service Units are
the mechanism that divides it fairly between them, and the quota is the
mechanism that decides how much there is to divide.
→ [Service Units & Budgets](service-units-and-budgets.md)

**Quotas are per class.** A workspace at its Medium limit may still have Small
headroom.
→ [GPU Classes](gpu-classes.md)

## Quotas Move with the Calendar

------------------------------------------------------------------------

**Quotas are date-aware.** Staff can set them week by week, or day by day, so a
course's share may surge for exactly the span of a project deadline and revert
on its own afterwards. A lab's share can be raised the same way for a conference
deadline.

**Dated changes depend on the dates being known in advance.** For courses, the
quarterly survey asks instructors and TAs about assignment scope, GPU sizes, and
deadlines; those answers are what allow a quota to be raised for week 9 ahead of
the surge rather than during it. For research, please write to us with the date.
→ [Teaching with Datahub & DSMLP](../instructor-or-ta.md)

## Borrowing Beyond Quota

------------------------------------------------------------------------

**Quotas are not hard ceilings, and borrowing is enabled on the cluster.**
Last-minute jobs — under roughly 12 hours ahead — may use idle capacity beyond
their group's quota. A group that has exhausted its share can still pick up GPUs
that would otherwise sit dark.

**Borrowing is opportunistic, not a guarantee.** What a group borrows is
whatever happens to be idle at the moment it asks.

**Borrowing carries a seniority, and course workspaces always hold the senior
tier.** A senior borrower is not the first asked to give capacity back. *Groups
that contribute hardware to the cluster have their own arrangement, described on*
[Setting Up a Research Lab](../faculty-research-lab.md).

**Borrowing does not raise a budget.** A borrowed GPU-hour is still a GPU-hour,
and it is still charged.

## The Reserve Floor

------------------------------------------------------------------------

**ITS maintains a reserve floor of unborrowable capacity in each GPU class.**

*The practical consequence: idle is not the same as available.* The cluster
status page may show free cards of a class that borrowing will not release, since
some of that headroom is deliberately held back.

## Cohorts

------------------------------------------------------------------------

**A cohort is a group of groups.** Within one, the member groups' quotas may sum
to more than the physical capacity sitting behind them, which allows each group a
higher peak than a fixed carve-up of the hardware would.

Where several groups in a cohort peak at the same time, the effect below follows.

*A cohort is not the same thing as a workspace.* Members belong to a workspace;
that workspace may in turn sit in a cohort, alongside groups its members never
encounter.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

## Zero Availability With Headroom Remaining

------------------------------------------------------------------------

**The calendar can offer nothing at all even where a workspace has quota to
spare.** That is not a fault.

**A quota is a ceiling on what a group may hold, not a set of cards held aside
for it.** A workspace whose Medium quota is four, and which currently holds none,
can still be offered nothing at all on a Thursday evening: the other groups in
the cohort are holding the hardware, and they are entitled to.

Nothing has been taken away and nothing is broken. The quota has not been
reduced, the budget is untouched, and the same request will very often succeed a
few hours later. Options when nothing is available:

- **The calendar is first-come.** Headroom on paper does not displace a booking
  that already exists.
- **A different hour rather than a different day.** Peak evening demand is the
  constraint; the same window at midday or overnight is both more likely to be
  available and cheaper.
  → [Peak & Off-Peak Hours](service-units-and-budgets.md#peak--off-peak-hours)
- **A smaller class.** Classes do not share spare capacity with one another, so a
  full Medium says nothing about Small. → [GPU Classes](gpu-classes.md)
- **Borrowing, inside twelve hours.** Last-minute jobs may pick up capacity that
  is idle at the time, including capacity beyond the group's own quota.

**Overcommitment affects what can be obtained, not what is delivered.** A GPU
that is obtained is held for the window and at the class it was booked at.
Nothing about a cohort makes a session slower.

**Zero availability is not an outage.** A contested evening is not a ticket.
*Please report a cohort that is consistently unable to work to the instructor, TA
or PI: a quota that never fits is a provisioning problem.*

## Not Every Cohort Is Overcommitted

------------------------------------------------------------------------

**Where a set of quotas sums to the physical capacity behind it**, the members of
that cohort are guaranteed access up to their full group ceiling through to the
12-hour boundary. The effect described above does not arise there.

**The cohort holding hardware contributors is not overcommitted.** A lab that
contributes hardware has group limits matching its contribution, so its own
capacity is there when it books it.
→ [Setting Up a Research Lab](../faculty-research-lab.md)

## The Other Ceilings

------------------------------------------------------------------------

Four separate ceilings can stop the same launch, and they fail in similar ways.

| Limit | What it caps | Where it is documented |
|---|---|---|
| **A single pod** | What one container may hold — a 1-GPU default | [`launch.sh` Reference](../running-jobs/launch-sh-reference.md#defaults--the-three-resource-tiers) |
| **The namespace** | Everything running at once | [Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once) |
| **The group quota** | What the whole workspace may hold, per class | This page |
| **The cohort** | What the surrounding groups are holding right now | [Cohorts](#cohorts) |

**A Service Unit budget is a fifth, and it is not a capacity limit at all.** It
caps how much GPU time a member may spend, not how many GPUs exist to spend it
on. *Budget remaining does not mean a card is free, and a free card does not mean
the budget covers it.*

**A quota is about GPUs, not storage.** Storage quotas are a different system
with different numbers.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

## When the Cluster Is Full

------------------------------------------------------------------------

**GPUs are the scarcest thing on this platform, and at a deadline they run out.**

| What appears | What it is |
|---|---|
| A session that takes a long time to start | The request is waiting for capacity. It has not failed |
| An `OnDemandLeaseDenied` event | The on-demand lease the launch asked for was not granted, so nothing started |
| An out-of-capacity message on Datahub | The same thing, from the browser |
| A GPU class showing no availability for a date | Either it is fully booked, or capacity has been withdrawn for maintenance → [Maintenance Closures](what-ends-a-session.md#maintenance-closures) |
| `0/5 nodes available` alongside a GPU request | **Usually not a full cluster.** A GPU request that omits its class label has nowhere to land, because medium and above sit behind `NoSchedule` taints → [When the Label Is Missing](gpu-classes.md#when-the-label-is-missing) |

**The last row is worth reading twice.** A GPU request that omits its class label
produces a message that reads exactly like exhaustion, and it is fixed by
correcting the launch line rather than by waiting for capacity that was never the
problem.

## What the Platform Does Not Report

------------------------------------------------------------------------

**There is no queue that can be watched.** A reservation admits a session ahead of
the walk-up queue, so the queue is a real thing — but there is no position number,
no estimated wait, and no notification as a turn approaches. A launch that is
waiting looks exactly like a launch that is waiting, and that is all the
information there is.

**We would rather say this than imply otherwise.** *A GPU needed at a particular
time is obtained by reservation rather than by patience.*
→ [Reservations](reservations.md)

**Zero availability does not always mean the cluster is full.** Two of the
reservation model's ordinary behaviours produce the same symptom:

- **Classes are not interchangeable.** A busy Medium says nothing about Large,
  and spare capacity in one class cannot be lent to another. A workspace is
  granted particular classes, and a class it was not granted is refused whatever
  is idle.
- **A cohort can be fully drawn while one of its groups still has headroom on
  paper.** → [Cohorts](#cohorts)

## What Actually Helps

------------------------------------------------------------------------

**Look before launching.** The cluster status page shows per-node GPU models and
how many GPUs are free, which is the closest thing to a live answer that exists.
→ [The Status Page](#the-status-page)

**Retrying does not help; booking does.** Repeatedly launching into a full cluster
is the one approach that reliably does not work, and on-demand launches draw
Service Units each time they succeed. A window booked a day ahead costs the same
units and yields the card.
→ [On-Demand Leases Charge Budget](service-units-and-budgets.md#on-demand-leases-charge-budget)

**Work moved off the evening is cheaper and easier to place.** Peak evening hours
are where contention lives, and off-peak hours are discounted.
→ [Peak & Off-Peak Hours](service-units-and-budgets.md#peak--off-peak-hours)

**Develop on CPU and train on GPU.** A GPU card attached to a container is unusable
by anyone else even while it sits idle. PyTorch and TensorFlow both switch between
CPU and GPU with very little code. *This is also the fastest route to a session
when GPUs are scarce.*

**Shut down finished sessions.** Logging out does not stop a session, and a session
left running holds its GPU. **File → Hub Control Panel → Stop My Server**
in the browser; `kubectl delete pod <pod-id>` from the shell.

**Late work can borrow.** Within roughly 12 hours, idle capacity beyond a group's
quota may still be picked up, and course workspaces always borrow senior.
→ [Borrowing Beyond Quota](#borrowing-beyond-quota)

## Waiting for Capacity

------------------------------------------------------------------------

**A launch that is waiting for a GPU gives the card straight back if it carries
`-f`.** The flag runs the script and ends the container, so a launch that waited
ten minutes for a card holds it only for the length of the script.
→ [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

## The Status Page

------------------------------------------------------------------------

**[datahub.ucsd.edu/hub/status](https://datahub.ucsd.edu/hub/status) is the live
view of the cluster.** It lists the compute nodes, the GPU models on each of them,
and how many GPUs on each node are currently free.

*It appears to require a signed-in session.* It is therefore not the tool for
diagnosing a sign-in problem as opposed to a capacity problem.
→ [Sign-In & Session Problems](../access/sign-in-and-session-problems.md)

It answers three further questions:

- **The GPU models available to request.** The models named are what the `-v` flag
  accepts. *`-l gpu-class=` is the better request where size matters rather than a
  specific card* — classes are how GPU access is granted.
- **The node numbers, for `-n`.** `-n` takes a bare number — `-n 30`, not `-n n30`;
  the leading `n` on the status page is not part of the value. *Pinning a node is
  usually a mistake*: a full node makes the pod wait for that node rather than
  take an equivalent GPU elsewhere.
  → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)
- **The rhythm of demand.** Peak evening demand is real and predictable, and the
  status page is the cheapest way to read it.

**Maintenance shows here too.** Instructional maintenance runs Tuesdays, 6-8 AM
and is generally limited to a subset of worker nodes, so the status page may show
less hardware than usual on a Tuesday morning without anything being wrong.
→ [Maintenance Closures](what-ends-a-session.md#maintenance-closures)

## Free Is Not the Same as Available

------------------------------------------------------------------------

**A GPU the status page shows as free may still not be obtainable**, for
several reasons that the page cannot see. This is the most common way it misleads
people.

- **Each workspace is granted particular GPU classes**, and a class it was not
  granted is refused whatever is idle. → [GPU Classes](gpu-classes.md)
- **A reserve floor of unborrowable capacity is held back** in each class, so some
  visible headroom is deliberately not on offer.
  → [The Reserve Floor](#the-reserve-floor)
- **A workspace may sit in a cohort** whose groups' quotas together exceed the
  hardware behind them. → [Cohorts](#cohorts)
- **Capacity may be reserved for someone else.** From Fall 2026 a booked window
  holds hardware that is idle right up until its owner launches into it.
  → [Reservations](reservations.md)
- **The Service Unit budget is a separate limit.** A free card does not spend
  itself. → [Service Units & Budgets](service-units-and-budgets.md)

**The status page describes hardware, not entitlement**, and it is a snapshot. On
a contested evening the picture changes between reading it and launching; a booked
window is the alternative to refreshing.

*Zero availability is not an outage, and does not need a ticket.* **Please do tell
us if a whole class is unobtainable for days rather than hours**, or if the status
page itself is unreachable while `datahub.ucsd.edu` is up.
→ [Getting Help](../reference/getting-help.md)

## Asking for More

------------------------------------------------------------------------

**Quotas and group limits are set administratively.** A manager — an instructor,
TA or PI — may view them but may not edit them.
→ [Managing a Group](../reference/managing-a-group.md)

**Please ask by ticket to** [datahub@ucsd.edu](mailto:datahub@ucsd.edu), naming
the work, the GPU class it needs, and the dates it matters on. A request that
names a deadline can be granted for that window alone.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

**Where quotas sum to the hardware behind them, the ceiling is a guarantee.**
Groups in that position have guaranteed access up to their full group ceiling
through to the 12-hour boundary. Where a cohort is deliberately overcommitted,
the ceiling is a maximum rather than a promise.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
