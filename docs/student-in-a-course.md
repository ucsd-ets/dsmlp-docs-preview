# Using Datahub in a Course

This page covers Datahub for students enrolled in a course that uses it, working
entirely in a web browser at [datahub.ucsd.edu](https://datahub.ucsd.edu).
Readers not enrolled in such a course start at
[Where to Begin](overview.md#where-to-begin).

## Signing In

1. Go to [datahub.ucsd.edu](https://datahub.ucsd.edu) and sign in through
   **UCSD single sign-on** with campus credentials. Duo applies. Datahub has no
   separate credentials.
2. Select the course. A student enrolled in more than one course that uses
   Datahub sees each course listed separately, as described in
   [Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).
3. Select an environment. The instructor determines what appears in this menu.
   Most courses offer one CPU option and, where the course uses them, a GPU
   option.
4. Wait for the environment to start. A launch may take a minute or two, and
   longer when the cluster is busy.

Files are in the file browser on the left and persist between sessions.

## Starting and Stopping Sessions

> [!WARNING]
> Signing out or closing the tab does not stop a session. The container keeps
> running and holding its resources, including its GPU if it has one. The
> control that stops it is **File → Hub Control Panel → Stop My Server**.

Sessions also end on their own when they reach their time limit, and a GPU
session ends when it has been left idle. Saved files persist when a session
ends; unsaved work is lost. Stopping a session is also how a finished GPU is
released.

See also: [Stopping a Session](access/datahub-in-the-browser.md#stopping-a-session)

### One Datahub Session

A member may have a single Datahub session running, so starting a different
course environment requires stopping the running one with
**File → Hub Control Panel → Stop My Server**. The limit applies to Datahub
alone. Work launched from a terminal runs alongside it.

See also: [Concurrent Datahub Sessions](access/datahub-in-the-browser.md#concurrent-datahub-sessions)

## Sign-In and Startup Failures

| Symptom | Usual cause |
|---|---|
| The course is not listed | Enrollment has not yet propagated. The instructor can check the roster. See [Students Enrolled in a Course](access/when-access-starts-and-ends.md#students-enrolled-in-a-course) |
| Sign-in fails at the campus sign-on page | A campus credential or Duo problem rather than a Datahub one. The [ITS Service Desk](https://support.ucsd.edu/) handles it |
| "Spawn failed", or the spinner never completes | A Datahub session may already be running, as described in [One Datahub Session](#one-datahub-session). A stale profile, or a broken package installed into the student's own `.local`, can also prevent a start. The **manual resetter** under the services dropdown is available for these cases. See ["Spawn Failed"](access/sign-in-and-session-problems.md#spawn-failed) |
| Everything loads but the files are missing | The session may be in a different course's workspace than intended. Check which course was selected |

See also: [Sign-In & Session Problems](access/sign-in-and-session-problems.md)

## Working in the Course Environment

### Session Resources

Course sessions typically begin at 2 CPU cores and 4GB RAM dedicated to each
student session. Upper limits are based on class size, demand, and capacity.

See also: [The Browser Session](access/datahub-in-the-browser.md#the-browser-session)

### Directories

Each home directory is private to one student and specific to one course. A
shared area readable by everyone in the course is where datasets and starter
notebooks usually appear. A private area follows the student into every course
taken.

See also: [Where Files Live](workspaces-and-storage/your-files-and-quotas.md#where-files-live)

### Storage Quota

A course home directory holds notebooks and modest data. A large dataset
belongs in the shared area rather than in a personal copy. Quota sizes are
given in
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

### Installing Packages

Python packages may be installed into a student's own environment. System-level
packages cannot be installed, because containers run unprivileged. A system
library a course requires is a request for the instructor to make.

See also: [Root Access and System Packages](environments/customizing-your-environment.md#root-access-and-system-packages)

### Moving Files

Drag and drop in the file browser handles small files. Routes for larger
transfers are described in
[Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md).

## Assignments

Most courses distribute, collect, and grade notebooks using tools built into the
environment. The instructor names which tool the course uses and how work is
fetched and submitted. Report an assignment that will not fetch or submit to the
instructor or TA before opening a ticket.

See also: [Grading](grading/README.md)

## Using a GPU

Where a course offers a GPU option, selecting it is all that is required.

### Service Unit Budget

> [!WARNING]
> Starting a GPU session books capacity and draws on the student's Service Unit
> (SU) budget for the course, whether or not the reservation calendar is used.
> Launching the session is what authorizes that spend, and a session left
> running costs the same as one in use.

A course budget renews each week. An exhausted budget is a matter for the
instructor or TA, who may request an increase. A booking the instructor or TA
makes on a student's behalf is charged to the student's own budget, so it does
not help a student who has run out.

See also: [On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges), [Service Units & Budgets](gpu-access/service-units-and-budgets.md)

### Idle GPU Sessions

A GPU session that stops using its GPU is reclaimed after a period of idleness,
and a warning precedes the shutdown.

See also: [What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle)

### Reservations

A GPU needed at a known time can be reserved in the reservation app at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/). A reservation
guarantees access, not a running job. The notebook is launched as usual and is
placed on the reserved capacity ahead of the walk-up queue.

A booked window that is missed may still be claimed within a short grace
period. After that, the reservation is cancelled, the capacity returns to the
pool, and a cancellation charge is assessed. The same applies when the session
stops partway through a booking and is not restarted within about 30 minutes.
The instructor or TA may waive the charge where warranted. Cancelling at least
24 hours ahead costs nothing; a later cancellation keeps part of the cost.

See also: [Reservations](gpu-access/reservations.md), [The Claim Window](gpu-access/reservations.md#the-claim-window), [The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

### Reservation Events

The reservation system reports on a GPU session with Kubernetes events. Datahub
shows them while a session starts, and `kubectl describe pod` shows them from
the command line. Each is defined in [Reservation Events](reference/reservation-events.md):

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`.
- When it is admitted: `RuntimeGuaranteed`, `OverstayRelinked`,
  `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

## Problems in a Running Session

| Symptom | Cause and remedy |
|---|---|
| The kernel keeps dying on a large dataset | Out of memory. Load less at a time, or ask the instructor whether a larger option is available |
| The notebook is slow and unresponsive | Check what else is open. Every notebook holds its own kernel and its own memory |
| "No space left" when saving | The storage quota is full. See [Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| A session ended while unattended | Expected when a session reaches its time limit or a GPU session is left idle. See [Starting and Stopping Sessions](#starting-and-stopping-sessions) and [Idle GPU Sessions](#idle-gpu-sessions) |
| GPU code reports no device found | The session may not have a GPU. Check which environment was selected |

Problems that require a terminal to diagnose are covered in
[Working from the Command Line](working-from-the-command-line.md).

See also: [Error Messages](reference/error-messages.md)

## Duration of Access

Access is retained for one additional quarter beyond the term in which the
course ran (a Fall course remains available through the end of Winter), and
Summer is not counted against a Spring course. Retrieve anything needed before
that period ends.

See also: [One Additional Quarter](access/when-access-starts-and-ends.md#one-additional-quarter)

## Maintenance and Policy

Datahub may be unavailable during scheduled maintenance for time-sensitive
updates or security patches. The schedule is given in
[Scheduled Maintenance](reference/policy.md#scheduled-maintenance). Rules on
acceptable use and data classification are on
[Policy](reference/policy.md).

## Work That Requires a Terminal

SSH, `launch.sh`, background and batch jobs, VS Code, and GPU classes that a
course menu does not offer are covered in
[Working from the Command Line](working-from-the-command-line.md). Command-line
work uses the same course access. There is no eligibility requirement and
nothing to request.

## Support

Course questions, such as assignments, packages a course needs, and the
environment a course provides, go to the instructor or TA, who are the first
tier of support. Platform matters, such as being unable to sign in or the
service behaving differently than documented, go to the
[ITS Service Desk](https://support.ucsd.edu/) or
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). A ticket names the course, what was
being done, and the exact error, and includes a screenshot.

See also: [Response Targets](reference/getting-help.md#response-targets), [Getting Help](reference/getting-help.md)
