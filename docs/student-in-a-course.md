# Using Datahub in a Course

------------------------------------------------------------------------

This article describes how students in a course reach the course environment,
what it provides, what a failed sign-in usually means, and the conditions under
which sessions start and stop.

**This article assumes a web browser and nothing else** — no Linux, no terminal,
no command line. Everything described here is done at
[datahub.ucsd.edu](https://datahub.ucsd.edu).

*Courses that require a terminal* — SSH, `launch.sh`, background or batch jobs,
VS Code, or a GPU class the course does not offer in its menu — are covered in
[Working from the Command Line](working-from-the-command-line.md). That is the
same access students already hold, used differently; there is nothing to request.

*For readers not enrolled in a course that uses Datahub*, the
[Overview](overview.md#where-to-begin) gives the starting points.

## Signing In

------------------------------------------------------------------------

1. Go to [datahub.ucsd.edu](https://datahub.ucsd.edu) and sign in through
   **UCSD single sign-on**, with campus credentials. Duo applies. *This is the
   standard campus sign-on — there is nothing Datahub-specific to enter.*
2. Select the course. A student enrolled in more than one course that uses
   Datahub sees each listed separately.
   → [Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)
3. Select an environment. The instructor determines what appears in this menu;
   most courses offer one CPU option and, where the course uses them, a GPU
   option.
4. Wait for the environment to start. A launch may take a minute or two, and
   longer when the cluster is busy.

Files are in the file browser on the left, and persist between sessions.

## Starting and Stopping Sessions

------------------------------------------------------------------------

**Logging out does not stop a session.** Closing the tab or signing out leaves
the container running and holding its resources, including its GPU if it has one.
The control that stops it is **File → Hub Control Panel → Stop My Server**.

Sessions do end on their own when they reach their time limit, and a GPU session
ends when it has been left idle. Saved files survive all of this; unsaved work
does not.

Stopping a session is also how a finished GPU is released, and is the remedy when
the same environment has to start somewhere else — see below.

## When Access Fails

------------------------------------------------------------------------

| Symptom | Usual cause |
|---|---|
| The course is not listed | Enrollment has not propagated. A TSS change appears by 10am the following day; beyond that, the instructor can check the roster |
| Sign-in fails at the campus sign-on page | A campus credential or Duo problem rather than a Datahub one. The [ITS Service Desk](https://support.ucsd.edu/) handles it |
| "Spawn failed", or the spinner never completes | Several causes. A Datahub session may already be running (below); a stale profile, or a broken package installed into the student's own `.local`, can also prevent a start. A **manual resetter** is available under the services dropdown for the latter |
| Everything loads but the files are missing | The session may be in a different course's workspace than intended. Check which one was selected |

**One Datahub session at a time.** A member may have a single Datahub session
running, so starting a different course environment means stopping the one that
is running — **File → Hub Control Panel → Stop My Server**. *That limit is on
Datahub alone: work launched from a terminal runs alongside it.*
→ [One Datahub Session](access/datahub-in-the-browser.md#one-datahub-session)

Further cases are covered in [Sign-In & Session Problems](access/sign-in-and-session-problems.md).

## Working in the Course Environment

------------------------------------------------------------------------

**Resources.** Course sessions typically begin at 2 CPU cores and 4GB RAM
dedicated to each student session. The instructor determines what appears in the
menu, including whether a GPU option is offered. *Upper limits are based on class
size, demand, and capacity.*

**Directories.** Each home directory is private to one student and specific to
one course. A shared area readable by everyone in the course is where datasets
and starter notebooks usually appear, and a private area follows the student into
every course taken. → [Directories, Quotas & Cleaning Up](workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Storage.** Course home directories are typically 5-10GB, depending on class
size — enough for notebooks and modest data, not for a personal copy of a large
dataset, which belongs in the shared area.
→ [Directories, Quotas & Cleaning Up](workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**Installing packages.** Python packages may be installed into a student's own
environment. System-level packages may not: containers run unprivileged under the
member's own UID, and `sudo apt-get` fails by design. A system library a course
requires is a request for the instructor to make.
→ [Customizing an Environment](environments/customizing-your-environment.md)

**Moving files.** Drag and drop works in the file browser for small files; larger
transfers have better routes.
→ [Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md)

## Assignments

------------------------------------------------------------------------

Most courses distribute, collect, and grade notebooks using tools built into the
environment. The instructor names which tool the course uses and how work is
fetched and submitted. → [Grading](grading/README.md)

*An assignment that will not fetch or submit goes to the instructor or TA before
a ticket.* This is a course question first.

## Using a GPU

------------------------------------------------------------------------

Where a course offers a GPU option, selecting it is all that is required.

**A GPU session draws on a budget, whether or not a calendar is opened.**
Starting a GPU session books capacity and draws on the student's **Service Unit
(SU)** budget for the course; launching the session is what authorizes that
spend. A session left running costs the same as one in use.
→ [On-Demand Leases Charge Budget](gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

**An idle GPU session is reclaimed.** A session holding a GPU and no longer using
it — no GPU memory in use, essentially no CPU — is shut down after about **30
minutes**. When the cluster is quiet the allowance is up to **6 hours** instead.
Nothing is culled in its first **45 minutes**, and after heavy work the clock
does not start for up to an hour. A warning precedes the cull. *A cull is not an
error and not a crash.*
→ [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle)

**Booking ahead.** A GPU needed at a known time — Thursday evening, say — can be
reserved. A reservation is a guarantee of *access*, not a running job: the
notebook is launched as usual, and it lands on the reserved capacity ahead of the
walk-up queue. → [Reservations](gpu-access/reservations.md)

**A booked window that is missed** may still be claimed within a short grace
period. Beyond that the reservation is cancelled, the capacity returns to the
pool, and a cancellation charge of up to 50% of the booking is assessed. *An
instructor or TA may waive this charge where warranted.* Releasing a window in
advance carries no penalty; charges cover only time actually used.
→ [The Claim Window](gpu-access/reservations.md#the-claim-window)

**An exhausted budget** is a matter for the instructor or TA. They may book on a
student's behalf, which does not draw that student's budget, and they may request
an increase. → [Service Units & Budgets](gpu-access/service-units-and-budgets.md)

## When Something Goes Wrong

------------------------------------------------------------------------

Matters resolvable from the browser:

| Symptom | Please try |
|---|---|
| The kernel keeps dying on a large dataset | Out of memory. Load less at a time, or ask the instructor whether a larger option is available |
| The notebook is slow and unresponsive | Check what else is open — every notebook holds its own kernel and its own memory |
| "No space left" when saving | The storage quota is full → [Directories, Quotas & Cleaning Up](workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one) |
| A session ended while unattended | Expected; see the time limit and idle culling above |
| GPU code reports no device found | The session may not have a GPU. Check which environment was selected |

Anything requiring a terminal to diagnose is covered in
[Working from the Command Line](working-from-the-command-line.md). Further cases:
[Error Messages](reference/error-messages.md).

## Practical Matters

------------------------------------------------------------------------

**Scheduled Maintenance:** Datahub may be unavailable Tuesdays, 6-8AM for
time-sensitive updates or security patches. *In practice this work is usually
limited to a subset of worker nodes, in which case running jobs are unaffected.*

**How long access lasts:** access is retained for **one additional quarter**
beyond the term the course ran in; a Fall course remains available through the
end of Winter. Summer is not counted against a Spring course. *Please retrieve
anything needed before that period ends.* → [When Access Starts & Ends](access/when-access-starts-and-ends.md)

**Getting help:** course questions — assignments, packages a course needs, the
environment a course provides — go to the instructor or TA, who are the first
tier of support. Platform matters such as being unable to sign in, or the service
behaving differently than documented, go to the
[IT Service Desk](https://support.ucsd.edu/) or
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). We aim to resolve individual user
issues within **1-2 business days**. *A ticket should name the course, what was
being done, the exact error, and include a screenshot.*
→ [Getting Help](reference/getting-help.md)

## Work That Requires a Terminal

------------------------------------------------------------------------

SSH. `launch.sh`. Background or batch jobs. VS Code. A GPU class a course menu
does not offer. All of these are covered in
**[Working from the Command Line](working-from-the-command-line.md)** — the same
course access, used from a terminal. There is no eligibility requirement and
nothing to request.

------------------------------------------------------------------------

If you still have questions or need additional assistance, please ask your
instructor or TA, or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
