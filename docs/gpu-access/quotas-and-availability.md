# Quotas, Cohorts & Availability

This page covers GPU quotas, borrowing beyond quota, cohorts, the symptoms of a
full cluster, and the cluster status page.

## What a Quota Is

A **quota** is the maximum number of GPUs of each class that a workspace may
hold at one time. A quota is not a reservation of hardware, not an individual
allowance, and not a Service Unit budget.

The quota belongs to the workspace, not to the member. Every member of a course
or lab draws on the same ceiling. A launch refused because the workspace is at
its limit means that other members hold the capacity. The quota sets how much
capacity the workspace has, and Service Units divide it fairly between members.
See [Service Units & Budgets](service-units-and-budgets.md).

Quotas are set per GPU class. A workspace at its Medium limit may still have
Small headroom. A workspace is granted particular classes, and a request for a
class it was not granted is refused whatever is idle. Spare capacity in one
class cannot be lent to another, so a busy Medium class says nothing about
Large. The classes are described in
[GPU Classes](gpu-classes.md).

## Date-Based Quota Changes

Quotas are date-aware and can be set week by week or day by day. A course's
share can be raised for the span of a project deadline and revert automatically
afterward. A lab's share can be raised the same way for a conference deadline.

A dated change requires the dates in advance. For courses, the quarterly survey
asks instructors and TAs about assignment scope, GPU sizes, and deadlines. The
answers allow a quota to be raised for week 9 before the surge begins. Course
GPU planning is covered in
[Teaching with Datahub and DSMLP](../instructor-or-ta.md).
For research workspaces, include the date in the request; see
[Requesting a Quota Increase](#requesting-a-quota-increase).

## Borrowing Beyond Quota

Quotas are not hard ceilings, and borrowing is enabled on the cluster.
Last-minute jobs (under roughly 12 hours ahead) may use idle capacity beyond
their group's quota. A group that has exhausted its share can still obtain GPUs
that would otherwise be idle.

Borrowing is opportunistic and carries no guarantee. A group borrows whatever
capacity is idle at the moment it asks.

Borrowing carries a seniority, and course workspaces always hold the senior
tier. A senior borrower is not the first asked to give capacity back. Groups
that contribute hardware to the cluster have a separate arrangement, described
in [Setting Up a Research Lab](../faculty-research-lab.md).

Borrowing does not raise a Service Unit budget. Borrowed GPU time is charged.

### The Reserve Floor

ITS maintains a reserve floor of unborrowable capacity in each GPU class. Idle
capacity is therefore not always available. The status page may show free GPUs
of a class that borrowing will not release, because part of that headroom is
held back.

## Cohorts

A **cohort** is a group of groups. Within a cohort, the member groups' quotas
may sum to more than the physical capacity behind them. This allows each group
a higher peak than a fixed division of the hardware would. Where several groups
in a cohort peak at the same time, availability can read zero while a workspace
still has headroom; see
[Zero Availability With Headroom Remaining](#zero-availability-with-headroom-remaining).

A cohort is not a workspace. Members belong to a workspace, and that workspace
may sit in a cohort alongside groups its members never encounter. Workspaces are
described in
[What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md).

### Zero Availability With Headroom Remaining

The reservation calendar can offer nothing even where a workspace has quota to
spare. This is not a fault. A quota is a ceiling on what a group may hold, not a
set of GPUs held aside for it. For example, a workspace whose Medium quota is
four and which currently holds none can be offered nothing on a Thursday
evening, because the other groups in its cohort hold the hardware, as they are
entitled to.

The quota has not been reduced and the budget is untouched. The same request
often succeeds a few hours later. Bookings are first-come, and quota headroom
does not displace a booking that already exists. Options when nothing is
available:

- Book a different hour rather than a different day. Peak evening demand is the
  constraint. The same window at midday or overnight is more likely to be
  available and is cheaper under
  [Peak & Off-Peak Hours](service-units-and-budgets.md#peak--off-peak-hours).
- Request a smaller class. Classes do not share spare capacity with one
  another, so a full Medium class says nothing about Small.
- Borrow inside 12 hours. Last-minute jobs may pick up capacity that is idle at
  the time, including capacity beyond the group's own quota; see
  [Borrowing Beyond Quota](#borrowing-beyond-quota).

Overcommitment affects what can be obtained, not what is delivered. A GPU that
is obtained is held for the window at the class it was booked at. A cohort does
not make a session slower.

Zero availability is not an outage and does not need a ticket. A cohort that is
consistently unable to work indicates a provisioning problem. Report it to the
instructor, TA, or PI.

### Cohorts Without Overcommitment

Where a set of quotas sums to the physical capacity behind it, the members of
that cohort are guaranteed access up to their full group ceiling through to the
12-hour boundary. Zero availability with headroom remaining does not arise in
such a cohort. Where a cohort is deliberately overcommitted, the group ceiling
is a maximum rather than a guarantee.

The cohort holding hardware contributors is not overcommitted. A lab that
contributes hardware has group limits matching its contribution, so its own
capacity is available when it books. Hardware contribution is covered in
[Setting Up a Research Lab](../faculty-research-lab.md).

## Limits That Can Stop a Launch

Four separate capacity limits can stop the same launch, and they fail in similar
ways.

| Limit | What it caps | Reference |
|---|---|---|
| A single pod | What one container may hold | [Defaults and Resource Tiers](../running-jobs/launch-sh-reference.md#defaults-and-resource-tiers) |
| The namespace | Everything running at once | [Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once) |
| The group quota | What the whole workspace may hold, per class | [What a Quota Is](#what-a-quota-is) |
| The cohort | What the surrounding groups are holding at the moment | [Cohorts](#cohorts) |

A Service Unit budget is a fifth limit, and it is not a capacity limit. It caps
how much GPU time a member may spend, not how many GPUs exist to spend it on.
Remaining budget does not mean a GPU is free, and a free GPU does not mean the
budget covers it.

A GPU quota does not cover storage. Storage quotas are a separate system with
different values; see
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

## When the Cluster Is Full

The table lists the symptoms of a launch that cannot obtain a GPU.

| Symptom | Meaning |
|---|---|
| A session takes a long time to start | The request is waiting for capacity. It has not failed. |
| An `OnDemandLeaseDenied` event | The on-demand lease the launch asked for was not granted, so nothing started. |
| An out-of-capacity message on Datahub | The same condition as `OnDemandLeaseDenied`, reported in the browser. |
| A GPU class shows no availability for a date | The class is fully booked, or capacity has been withdrawn for maintenance. See [Maintenance Closures](what-ends-a-session.md#maintenance-closures). |
| `0/5 nodes available` after a GPU request | Usually a GPU request that omits its class label, not a full cluster. See [Missing or Misspelled Class Label](gpu-classes.md#missing-or-misspelled-class-label). |

Zero availability does not always mean the cluster is full. Two other
conditions produce the same symptom: a request for a class the workspace was
not granted, which is refused whatever is idle, and a cohort that is fully drawn
while one of its groups still has headroom on paper. See
[What a Quota Is](#what-a-quota-is) and
[Zero Availability With Headroom Remaining](#zero-availability-with-headroom-remaining).

### Queue Position and Wait Time

A reservation admits a session ahead of the walk-up queue. The walk-up queue
itself is not visible: the platform reports no queue position, no estimated
wait, and no notification as a turn approaches. A waiting launch shows only
that it is waiting. A GPU needed at a particular time is obtained by booking it
through [Reservations](reservations.md).

### Waiting for Capacity

A launch that carries `-f` releases its GPU when the script ends. The flag runs
the script and ends the container, so a launch that waited for a GPU holds it
only for the length of the script. The flag is covered in
[Job Modes](../running-jobs/job-modes-and-limits.md#job-modes).

## Obtaining Capacity When the Cluster Is Busy

- Check [The Status Page](#the-status-page) before launching. It shows the GPU
  models on each node and how many GPUs are free.
- Book a window instead of retrying. Repeated launches into a full cluster do
  not obtain a GPU, and each on-demand launch that succeeds spends Service
  Units; see
  [On-Demand Lease Charges](service-units-and-budgets.md#on-demand-lease-charges).
  A window booked a day ahead costs the same Service Units and obtains the GPU.
- Move work off peak evening hours. Contention is concentrated in peak evening
  hours, and off-peak hours are discounted under
  [Peak & Off-Peak Hours](service-units-and-budgets.md#peak--off-peak-hours).
- Develop on CPU and train on GPU. A GPU attached to a container is unusable by
  anyone else even while it is idle. PyTorch and TensorFlow both switch between
  CPU and GPU with very little code. Developing on CPU is also the fastest route
  to a session when GPUs are scarce.
- Stop finished sessions with **File → Hub Control Panel → Stop My Server** in
  the browser, or with `kubectl delete pod <pod-id>` from the shell.
- Borrow idle capacity beyond the workspace quota for last-minute work; see
  [Borrowing Beyond Quota](#borrowing-beyond-quota).

> [!WARNING]
> Logging out does not stop a session. A session left running holds its GPU.
> See [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

## The Status Page

[datahub.ucsd.edu/hub/status](https://datahub.ucsd.edu/hub/status) is the live
view of the cluster. It lists the compute nodes, the GPU models on each node,
and how many GPUs on each node are currently free.

The status page may require a signed-in session, so it is not a reliable way to
tell a sign-in problem from a capacity problem. Sign-in problems are covered in
[Sign-In & Session Problems](../access/sign-in-and-session-problems.md).

| Information | Use |
|---|---|
| GPU models | The models named are the values the `-v` flag accepts. Where GPU size matters rather than a specific model, `-l gpu-class=` is the preferred request, because GPU access is granted by class. |
| Node numbers | The `-n` flag takes a bare number: `-n 30`, not `-n n30`. The leading `n` shown on the status page is not part of the value. Pinning a node is not recommended: a pod pinned to a full node waits for that node rather than taking an equivalent GPU elsewhere. |
| Demand over the day | Peak evening demand is predictable and is visible on the status page. |

During instructional maintenance, the status page may show less hardware than
usual. This does not indicate a fault. The maintenance schedule is published under
[Scheduled Maintenance](../reference/policy.md#scheduled-maintenance).

See also: [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

### Limitations of the Status Page

A GPU that the status page shows as free may still not be obtainable. The page
does not reflect any of these conditions:

| Condition | Effect |
|---|---|
| The workspace was not granted the GPU class | A class the workspace was not granted is refused whatever is idle. See [GPU Classes](gpu-classes.md). |
| The reserve floor | Part of the visible headroom in each class is unborrowable capacity that ITS holds back. See [The Reserve Floor](#the-reserve-floor). |
| A cohort | The workspace may sit in a cohort whose groups' quotas together exceed the hardware behind them. See [Cohorts](#cohorts). |
| A reservation | From Fall 2026, a booked window holds hardware that stays idle until its owner launches into it. See [Reservations](reservations.md). |
| The Service Unit budget | The budget is a separate limit. A free GPU does not mean the budget covers it. See [Service Units & Budgets](service-units-and-budgets.md). |

The status page describes hardware, not entitlement, and shows a snapshot. On a
busy evening, availability can change between reading the page and launching.
Booking a window is the alternative to refreshing the page.

Zero availability is not an outage and does not need a ticket. Report a GPU
class that is unobtainable for days rather than hours, or a status page that is
unreachable while datahub.ucsd.edu is up, through
[Getting Help](../reference/getting-help.md).

## Requesting a Quota Increase

Quotas and group limits are set administratively. A workspace manager (an
instructor, TA, or PI) may view them but may not edit them. Manager privileges
are described in
[Managing a Group](../reference/managing-a-group.md).

Send the request by ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu),
naming the work, the GPU class it needs, and the dates it matters on. A request
that names a deadline can be granted for that window alone.

See also: [Administrative Requests](../reference/getting-help.md#administrative-requests)
