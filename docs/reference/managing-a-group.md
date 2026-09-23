# Managing a Group

The reservation and workspace system has four privilege tiers. A workspace
manager works on the manager pages of the reservation app at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/).

## The Four Tiers

| Tier | Who holds it | What it is for |
|---|---|---|
| **Member** | A student in a course, a member of a lab | Launching sessions and booking windows against their own budget |
| **Workspace manager** | An instructor, a TA, a PI | Running the workspace on behalf of its members |
| **Auditor** | Read-only staff | Seeing what is happening without changing it |
| **Administrator** | Cluster administrators, in ITS | Everything the platform can do |

The workspace manager tier is also called group manager. The reservation app
shows a manager's role as **User**; the manager pages in the sidebar are what
set a manager apart.

See also: [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)

### Becoming a Manager

In a course workspace whose roster is loaded automatically, the course's owner,
its TAs, and its graders all become workspace managers. In other workspaces an
administrator appoints managers, or an existing manager does in a manager-curated
workspace; see [Roster Curation](#roster-curation).

## What a Manager May Do

A manager's sidebar in the reservation app adds **Group Reservations**,
**Group Members**, and **Reports**, and, where they apply, **GPU Loans** and
**Group Rosters**.

### Viewing the Group's Reservations

**Group Reservations** lists every reservation in the workspaces the manager
manages. Filter by **Username** (an exact match), **GPU Class**, **Group**,
dates, and **Status**, then select **Search**. The **SU** column adds
`(grp: X)` where the charge to the group pool differs from the member's, and
`(orig: X)` where the member's charge has changed since booking, for example
after a cancellation. A red × on a row cancels it, and an amber × waives a
penalty.

### Booking on a Member's Behalf

Select **New Reservation** on **Group Reservations**, then choose the group, the
member, the GPU class, the date, the start time, the duration in whole hours,
and the number of GPUs.

> [!WARNING]
> A booking made on a member's behalf is charged to the member's budget. The
> manager skips only the check that the member can afford it, so the booking
> can leave the member at or over budget. That blocks the member's own bookings
> and on-demand leases until the budget window renews.

A manager's booking also skips the booking horizon and the 48-hour member cap,
and may fall up to 90 days before or after the workspace's active dates. The
group pool, the workspace length cap, the class grants, and the GPU limits
still apply. The row shows **Submitted by** and the manager's username.

### Cancelling and Waiving

A manager can cancel any reservation in a managed workspace with the red × on
**Group Reservations**. Cancelling a booking that is in progress deletes the
member's running sessions, which record a `ReservationCancelled` event. Where a
penalty applies, the dialog states it and offers **Waive this penalty**.

A penalty can also be waived afterwards, with the amber × on the cancelled
reservation. This covers a no-show, the member's own late cancellation, and a
teammate's cancellation in team mode. A manager's waiver clears the member's
share of the penalty. The group pool's share, where the workspace has a pool,
is cleared only by an administrator, and a manager's waiver on a reservation
where only the pool's share remains changes nothing. See
[Having a Charge Waived](../gpu-access/service-units-and-budgets.md#having-a-charge-waived).

### GPU Loans

**GPU Loans** appears where the workspace's cohort allows loans. A loan moves
part of one workspace's GPU limit for a class to another workspace in the same
cohort, for a set of dates.

1. Under **Propose a loan**, choose the manager's own group and the other group.
2. Choose **Offer** to lend GPUs, or **Request** to borrow them.
3. Choose the GPU class, the number of GPUs, and the dates, and select
   **Send proposal**. The chart beside the form shows the effect on both groups.
4. The other group's manager approves or rejects the proposal.

Either side can withdraw a proposal that is awaiting approval, or cancel a loan
in force. A loan's status is **Awaiting approval**, **In force**, **Expired**,
**Rejected**, or **Cancelled**. A loan spans at most 120 days, and both groups
need a GPU limit for the class on every day of it. Approval is refused while
the lending group already holds more GPUs than the loan would leave it, and the
refusal names the first such day. A loan changes GPU limits only. Reservations
already made stand, and no budget changes.

### Roster Curation

In a manager-curated workspace, **Group Rosters** lets a manager add existing
accounts, remove members, and make a member a manager or a manager a member.
Changes apply at once. It cannot create accounts. The rosters of course
workspaces loaded automatically, and of workspaces curated by administrators,
cannot be changed here.

### Acting as a Member

Where an administrator has allowed it for a workspace, a manager can act as one
of its members from **Group Members**, to see the reservation app as that member
sees it. A password or email address cannot be changed while acting as another
user. Select **Exit Impersonation** in the sidebar to return.

### A Manager's Own Bookings

For a manager's own bookings, the member budget is not checked, the booking
horizon and the 48-hour member cap are skipped, and the 90-day allowance around
the active dates applies, as for booking on a member's behalf. The booking wizard selects at
most 48 hours for everyone, so a longer booking is made with
**New Reservation** on **Group Reservations**.

### Extending a Member's Job

The reservation system accepts an **Extend** of a member's job from a workspace
manager, but the manager pages have no **Extend** button. A manager allowed to
act as members can Extend a job while acting as its owner; see
[Acting as a Member](#acting-as-a-member). Otherwise the member extends the job.
See [Extend](../gpu-access/reservations.md#extend).

## Budgets and Limits Set by Administrators

A manager may not edit Service Unit budgets, either a member's or the
workspace's own. Budgets are set administratively. See
[The Size of a Budget](../gpu-access/service-units-and-budgets.md#the-size-of-a-budget).

A manager may not edit group limits or quotas. The number of GPUs of each class
that the workspace may hold at once is a platform-side setting. A manager may
not change the workspace length cap either; see
[Reservation Length Caps](../gpu-access/reservations.md#reservation-length-caps).

A manager may request a change to any of these by ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). The ticket states what the work
is and the dates on which it matters. Requests are covered in
[Administrative Requests](getting-help.md#administrative-requests) and, for
quotas, in
[Requesting a Quota Increase](../gpu-access/quotas-and-availability.md#requesting-a-quota-increase).

## Team Mode Cancellation Charges

When a teammate cancels another member's booking in team mode, the teammate
cannot waive the penalty at the time of cancelling. A manager can waive it
afterwards. See [Cancelling and Waiving](#cancelling-and-waiving).

See also: [Team Mode](../gpu-access/reservations.md#team-mode)

## What the Reports Cover

**Reports** shows four reports for a chosen date range of up to 60 days. The
default range is today and the following 13 days.

| Report | Scope | What it shows |
|---|---|---|
| **Reservations by Group** | Every workspace on the cluster | The number of reservations in each workspace, by the day they start |
| **Max Simultaneous Reservations by GPU Class** | The whole cluster | The most GPUs of each class held at once on each day, counting only reservations that start that day |
| **Reserved Hours by GPU Class** | The whole cluster | GPU-hours reserved, by the day the reservations start |
| **Effective GPU Limits by Group** | The manager's own workspaces | For each day, the physical capacity, the cohort's limit, and the workspace's limit in force |

### Effective Limits

Quotas are date-aware. A course's share may be raised for exactly the span of a
project deadline and revert automatically afterward. The limit in force in a
given week is therefore not necessarily the one quoted at provisioning. The
**Effective GPU Limits by Group** report shows the limit in force on each day.
Date-ranged changes are covered in
[Date-Based Quota Changes](../gpu-access/quotas-and-availability.md#date-based-quota-changes).

## Cluster-Wide Scope

Three of the four reports display data for the whole cluster, not only the
manager's own workspace.

### Reading Cluster-Wide Figures

A total that includes every group on the cluster is not a total for one course.
A peak drawn from the whole cluster is not evidence about one roster.

> [!NOTE]
> Establish what a report is scoped to before quoting a figure from it in a
> ticket or a syllabus.

### Other Groups' Data

Data about other groups in the reports warrants discretion. A manager does not
circulate another department's booking pattern. A manager's own workspace is
visible to others on the same terms. The reports are a planning tool and are
not a public record.

## Uses of the Reports

### Evidence for a Limit Change

The **Max Simultaneous Reservations by GPU Class** and **Reserved Hours by GPU
Class** reports supply the evidence a request to change a limit needs. Both are
cluster-wide, so pair them with **Effective GPU Limits by Group** and the
workspace's own reservations on **Group Reservations**. An example is a
workspace that reached its ceiling every evening of week 7, with a project due
in week 9. A survey of student deadlines a few weeks ahead allows cluster
administrators to raise a quota in advance rather than discover the surge as it
happens. Requests are covered in
[Administrative Requests](getting-help.md#administrative-requests).

### Moving Usage Off Peak

Where reserved hours cluster in the evenings, a manager can tell students that
off-peak time is discounted and generally obtainable. Off-peak discounts are
covered in
[Peak & Off-Peak Hours](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours).

## Limitations of the Reports

The reports are not a bill. Service Units divide capacity and do not cost
money. Storage charges are covered in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

The reports are not a live availability view. What the cluster is holding at
the current moment is shown on the status page, covered in
[The Status Page](../gpu-access/quotas-and-availability.md#the-status-page).

The reports are not controls. A manager's actions are those listed in
[What a Manager May Do](#what-a-manager-may-do). Every other change is
administrative and is requested by ticket.

A report shows contention but does not resolve it. A course whose quota never
fits its roster has a provisioning problem rather than a scheduling one. Report
such a course to ITS during the term rather than after it. Provisioning is
covered for courses in
[Teaching with Datahub and DSMLP](../instructor-or-ta.md)
and for labs in [Setting Up a Research Lab](../faculty-research-lab.md).

Zero availability in a class is not an outage, and a cohort can be fully drawn
while an individual group still has headroom on paper, as described in
[Cohorts](../gpu-access/quotas-and-availability.md#cohorts).

## Grader Account, Teams, and Technical Points of Contact

The shared grader account, teams, and the Technical Point of Contact (TPOC)
designation are not privilege tiers.

### Shared Grader Account

Each course receives one shared grader account for nbgrader and formgrader. It
holds write permission on the workspace's `public/` directory. An instructor's
own account does not inherit its powers. The account is covered in
[Notebook Grading Workflow](../grading/notebook-grading-workflow.md).

### Teams

A team is a Unix group, not a role. `launch.sh -G list` prints the teams an
account belongs to, and `-G <teamid>` launches with that team's data visible.
Team membership changes which files are readable. It does not change what a
member may do. Team storage is covered in
[Team Directories](../workspaces-and-storage/your-files-and-quotas.md#team-directories).

See also: [Team Mode](../gpu-access/reservations.md#team-mode)

### Technical Point of Contact

A TPOC is the person a course nominates to lead its customization work. The
designation is not a permission. It determines whom ITS works with, not what
the TPOC can do in the interface. Consultation appointments open to TPOCs are
covered in
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).
