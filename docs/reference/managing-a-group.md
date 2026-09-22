# Managing a Group

The reservation and workspace system has four privilege tiers. This page
describes each tier, the actions open to a workspace manager and those reserved
to administrators, and the usage reports available to managers.

## The Four Tiers

| Tier | Who holds it | What it is for |
|---|---|---|
| **Member** | A student in a course, a member of a lab | Launching sessions and booking windows against their own budget |
| **Workspace manager** | An instructor, a TA, a PI | Running the workspace on behalf of its members |
| **Auditor** | Read-only staff | Seeing what is happening without changing it |
| **Administrator** | Cluster administrators, in ITS | Everything the platform can do |

The workspace manager tier is also called group manager.

See also: [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)

## What a Manager May Do

A workspace manager has three powers.

### Viewing the Group Calendar

A manager sees the bookings of the whole workspace, not only their own.

### Booking on a Member's Behalf

A booking that a manager makes on a member's behalf takes effect immediately
and does not draw that member's Service Unit budget. Budgets are covered in
[Service Units & Budgets](../gpu-access/service-units-and-budgets.md).

### Waiving a Cancellation Charge

A manager may waive an assessed cancellation charge where the circumstances
warrant relief, for example where a missed window was not the member's fault.
A manager's waiver zeroes the member's share of the charge. A full pardon is an
administrator action. Waivers are covered in
[Having a Charge Waived](../gpu-access/service-units-and-budgets.md#having-a-charge-waived).

## Budgets and Limits Set by Administrators

A manager may not edit Service Unit budgets, either a member's or the
workspace's own. Budgets are set administratively. For a course, cluster
administrators calculate the per-student budget so that it evenly divides the
course's weekly peak evening GPU allocation.

A manager may not edit group limits or quotas. The number of GPUs of each class
that the workspace may hold at once is a platform-side setting.

A manager may request a change to either by ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). The ticket states what the work
is and the dates on which it matters. Requests are covered in
[Administrative Requests](getting-help.md#administrative-requests) and, for
quotas, in
[Requesting a Quota Increase](../gpu-access/quotas-and-availability.md#requesting-a-quota-increase).

## Team Mode Cancellation Charges

When a teammate cancels another member's booking in team mode, the resulting
charge stands. A manager cannot waive it and an administrator cannot pardon
it. It is the only cancellation charge in the system with no route of appeal.

See also: [Team Mode](../gpu-access/reservations.md#team-mode)

## What the Reports Cover

Instructors, TAs, and PIs can view four reports on how the GPU capacity
attached to their workspace is being used.

| Report | What it shows |
|---|---|
| **Reservations by group** | Which groups hold which bookings, and when they fall |
| **Peak simultaneous use by class** | The most GPUs of a class held at once, which shows whether a limit is binding |
| **Reserved hours** | How much time has been committed over a span, compared with how much was available |
| **Effective limits** | A group's limit as it stands on the current date, after any date-ranged change has been applied |

### Effective Limits

Quotas are date-aware. A course's share may be raised for exactly the span of a
project deadline and revert automatically afterward. The limit in force in a
given week is therefore not necessarily the one quoted at provisioning. The
**Effective limits** report shows the limit currently in force. Date-ranged
changes are covered in
[Date-Based Quota Changes](../gpu-access/quotas-and-availability.md#date-based-quota-changes).

## Cluster-Wide Scope

Some of the reports display cluster-wide data, not only the manager's own
workspace.

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

The **Peak simultaneous use by class** and **Reserved hours** reports supply
the evidence a request to change a limit needs. An example is a workspace that
reached its ceiling every evening of week 7, with a project due in week 9. A
survey of student deadlines a few weeks ahead allows cluster administrators to
raise a quota in advance rather than discover the surge as it happens. Requests
are covered in [Administrative Requests](getting-help.md#administrative-requests).

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

The reports are not controls. A manager's powers are the three listed in
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

### Technical Point of Contact

A TPOC is the person a course nominates to lead its customization work. The
designation is not a permission. It determines whom ITS works with, not what
the TPOC can do in the interface. Consultation appointments open to TPOCs are
covered in
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).
