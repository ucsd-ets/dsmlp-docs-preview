# Error Messages

This page lists common error messages and failure symptoms, grouped by where
they appear, with the cause and fix for each. An idle-culled session, a
`DeadlineExceeded` status, and a refused `sudo` are expected platform behavior,
not faults.

## Signing In & Starting a Session

| Symptom | Cause | Fix |
|---|---|---|
| The campus sign-on page returns repeatedly | A campus credential or Duo problem, or another identity signed in to the same browser | Sign out of the other identities, or use a private window. Datahub uses standard UCSD single sign-on, so the [ITS Service Desk](https://support.ucsd.edu/) handles a persistent failure |
| **Spawn failed**, with no explanation | A Datahub session is already running. A member may have one Datahub session at a time. Shell and VS Code sessions do not count toward that limit and are not the cause | Stop the running session with **File → Hub Control Panel → Stop My Server**, or run **manual-resetter** where the session cannot be reached. See [Concurrent Datahub Sessions](../access/datahub-in-the-browser.md#concurrent-datahub-sessions) |
| **Spawn failed**, and nothing else is running | A full disk quota. A full quota prevents a session from starting and produces no message stating the cause | Check **Services → disk-quota-service**, then clear space. See [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| **Spawn failed**, quota is fine | A stale profile | Run **manual-resetter** from the services dropdown. It stops the account's servers, signs the account out, and resets the profile. Files are preserved. See ["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed) |
| **Spawn failed**, shortly after a `pip install` | A package in the account's own `.local` loads ahead of the image's version and breaks the environment | From a terminal, run `mv .local/lib .local/lib.old`. See [Customizing an Environment](../environments/customizing-your-environment.md) |
| The course is not in the list | A provisioning matter, not an access fault. Rosters load one business day before the term, and a TSS change appears by 10am the following day | Ask the instructor or TA to confirm the roster. See [Students Enrolled in a Course](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course) |
| A **504** shortly after a crash | The pod stopped, from an infinite loop or from running out of memory, and the hub has not yet detected it | Run `kubectl delete pod <pod-id>` from the login node, then run **manual-resetter** |
| A course `git-pull` link fails and appears broken | The link was clicked before the student signed in. The link needs a session to redirect into | Sign in, start the environment, then click the link again |
| "database is locked" in a notebook | A stale notebook signature database | From a terminal, run `rm ~/.local/share/jupyter/nbsignatures.db`, then stop and restart the server |

### Stopping a Session

> [!WARNING]
> Closing the tab, closing the laptop, and signing out all leave the container
> running and holding its resources. Stop a session with
> **File → Hub Control Panel → Stop My Server**, as described in
> [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

## Launching From the Command Line

| Symptom | Cause | Fix |
|---|---|---|
| A GPU pod sits at `Pending` with **`0/N nodes are available: … untolerated taint(s)`** | Normal while the reservation system decides on the pod. The reason is in the event from `gpu-reservation-controller` beside it | Read the events in `kubectl describe pod`; see [Reservation Events](reservation-events.md). With no such event and no `gpu-class` label, the label is missing; see [Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label) |
| **"GPU quota exceeded. Wanted 1 but with 1 already in use, the quota of 1 would be exceeded"** | Another pod on the same account already holds the GPU | The earlier pod is usually terminating and clears within a minute or two. If it does not clear, run `kubectl get pods`, then `kubectl delete pod <pod-id>` |
| The launcher rejects one of the program's own options | A missing `--`. The launcher reads everything before `--` as a launcher flag | Place `--` between the launcher flags and the program: `launch-scipy-ml.sh -g 1 -B -- python train.py --epochs 50` |
| A GPU was requested and none arrived | `-G` where `-g` was meant. `-g 1` is one GPU; `-G 1` is a team ID | Use `-g` for the GPU count. The failure does not mention capitalization. See [Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags) |
| An `-n` node selection lands somewhere else | `-n` takes a bare node number | Pass the number alone: `-n 30`, not `-n n30`. The leading `n` on the status page is not part of the value |
| A container starts with far less CPU and memory than expected | `launch.sh` was called directly rather than through a wrapper. Bare `launch.sh` has lower CPU and memory defaults than the wrappers | Use `launch-scipy-ml.sh` or `launch-datascience.sh`, or pass `-c` and `-m`. See [Default Resources](../running-jobs/launch-sh-reference.md#default-resources) |
| **`sudo: ...`**, or any other refusal of `sudo` | Containers run unprivileged, under the member's own UID, with no root. `sudo apt-get` fails by design | Install a system package in a custom image, where root is available at build time. See [Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages) |
| A job keeps running after the pod is exited | Exiting a pod does not stop the processes inside it. `-b` backgrounds the pod, and `&` backgrounds a process | Run `kubectl get pods`, then `kubectl delete pod <pod-id>`. See [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes) |

## Statuses `kubectl get pods` Reports

| Status | What it means | What to do |
|---|---|---|
| **`OOMKilled`** | The container reached its memory limit | Size the job for its guaranteed memory request rather than its limit, as described in [Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits) |
| **`DeadlineExceeded`** | The runtime limit was reached. The status does not indicate an error in the code | The runtime limit is 6 hours by default, or 12 hours if set at launch. See [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| **`Pending`**, at length | The pod cannot currently be scheduled. A GPU pod may be waiting for its booking to open or for an on-demand lease | Run `kubectl describe pod <pod-id>` and read the events at the bottom of the output. Reservation events are listed in [Reservation Events](reservation-events.md) |
| **`Error`** | The status does not identify a cause | Report the pod ID, the node named in the launch output, and the approximate time of the failure, as described in [Getting Help](getting-help.md) |
| The session ended with no status and no error | Almost certainly an idle cull, not a crash. Saved work is preserved | See [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |

## Reservation Events on a Pod

The reservation system writes its own events on GPU pods, such as
`OnDemandLeaseDenied`, `WaitingForReservation`, `UnknownGpuClass`, and
`Preempted`. Each is a full sentence that says what to do.
[Reservation Events](reservation-events.md) lists all 15.

## Booking Refusals in the Reservation App

The reservation app checks a booking when **Next** is selected on the date and
time step, and again on **Confirm Reservation**. A refusal appears at the top of
the page, word for word as in this table. The same messages appear in the
**New Reservation** form on **Group Reservations**. Times in them are Pacific,
on a 24-hour clock.

| Message | Meaning | Fix |
|---|---|---|
| `Reservation must start at least 15 minutes in the future` | The start is less than 15 minutes away. Bookings start on the hour, so at 10:46 the earliest start is 12:00 | Choose a later hour |
| `Reservations may not exceed 48 hours` | The booking is longer than the member cap | Book a shorter window. See [Reservation Length Caps](../gpu-access/reservations.md#reservation-length-caps) |
| `This reservation runs H hours but group 'W' limits a single reservation to N hours.` | The booking is longer than the workspace length cap | Book a shorter window, or request a longer cap by ticket |
| `Group 'W' is for on-demand jobs only; reservations cannot be booked under it.` | The workspace, such as `ORG_ON_DEMAND`, accepts on-demand leases only | Book under a course or lab workspace |
| `Not a member of this group` | The person being booked for is not in the workspace | Ask the instructor or TA to check the roster |
| `Group not active before D`, `Group not active after D` | The start date is outside the workspace's active dates | Choose a date within them |
| `Reservations under this group must start at least N day(s) ahead — not before …` | The workspace requires bookings N days in advance | Choose a later start |
| `Reservations under this group must end within N day(s) — not after …` | The booking ends beyond the booking horizon | Choose an earlier or shorter window. See [The Booking Horizon](../gpu-access/reservations.md#the-booking-horizon) |
| `GPU class not accessible under this group` | The workspace was not granted this class | Choose a class the workspace was granted |
| `Exceeds limit of N GPU(s) per reservation` | Too many GPUs for one reservation of this class | Book fewer GPUs |
| `This reservation costs X SU but you only have Y of Z SU remaining (currently using W).` | The budget cannot cover the booking. "Currently using" counts ended, open, and upcoming bookings and kept penalties. With `in the week starting …`, the booking falls in that later week and draws on its budget. In team mode the message names the team | Book less, or wait for the budget to renew. See [When a Budget Runs Out](../gpu-access/service-units-and-budgets.md#when-a-budget-runs-out) |
| `This reservation costs X SU but the group pool only has …` | The workspace's shared pool cannot cover the booking | Ask the workspace manager. See [The Group Pool](../gpu-access/service-units-and-budgets.md#the-group-pool) |
| `Only N GPU(s) available at …` | The class has too few free GPUs in the hour named, the first hour that fails | Choose another hour, fewer GPUs, or another class |
| `Only N GPU(s) available for this group at … (group ceiling: G)` | The workspace holds its GPU limit for the class in that hour. Figures such as `borrowed` and `buffer` in the brackets describe idle capacity the workspace could borrow | Choose another hour. See [Borrowing Beyond Quota](../gpu-access/quotas-and-availability.md#borrowing-beyond-quota) |
| `Only N GPU(s) available for this cohort at … (cohort ceiling: C)` | The workspaces that share capacity with this one hold all of it in that hour | Choose another hour. See [Cohorts](../gpu-access/quotas-and-availability.md#cohorts) |

### Booking Wizard Warnings

The wizard checks a selection as it is made, and shows a warning below the
timeline while **Next** stays unavailable.

| Warning | Meaning |
|---|---|
| `Only k GPU(s) free across this range — need n.` | Some hour in the selection has too few free GPUs. Move the selection or lower the GPU count |
| `Not enough Service Units — needs X SU but only Y remain in your personal budget.` | The selection costs more than the budget has left. The message can name the team's budget or the group pool instead |
| `Past this group's booking window, which reaches …` | The selection ends beyond the booking horizon |
| `No bookable hours on this day.` | The day is outside the workspace's active dates or booking horizon, or has passed |
| `Start time has passed — choose a later hour.` | The selection starts too soon |
| `You are not assigned to any group. Contact an administrator.` | The account belongs to no workspace. Ask the instructor or TA to check the roster, or write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |

### Extend, Adopt, and Cancel Refusals

| Message | Meaning |
|---|---|
| `Only an active reservation can be continued` | The reservation was already cancelled or replaced, for example by an earlier **Extend**, or because its job ended |
| `Only a job that has already started can be continued; book upcoming windows in the wizard` | **Extend** works only on a running job. Book a future window in the wizard |
| `Only an in-progress booking can be continued` | The booking's window has ended. Book a new window |
| `Only reservations that have not ended may be adopted` | The teammate's booking has already ended |
| `Only active user-scheduled bookings may be adopted` | The reservation is an on-demand lease, or has been cancelled |
| `Already cancelled` | The reservation was cancelled already, for example by a teammate, a workspace manager, or as a no-show |

An **Extend** refused for budget or capacity shows the same messages as a
booking refusal, and changes nothing.

### Reservation App Messages in the Browser

| Symptom | Meaning | Fix |
|---|---|---|
| The app returns to the login page with no message | The session expired, or **Log out everywhere** was used | Sign in again. See [Reservation App Sign-In](../access/sign-in-and-session-problems.md#reservation-app-sign-in) |
| A line of text such as `{"detail":"Invalid OAuth state parameter"}` in the browser tab after signing in | Sign-in failed. The text names the reason | See [Sign-In Errors Shown as Text](../access/sign-in-and-session-problems.md#sign-in-errors-shown-as-text) |
| `HTTP 422` | The app rejected a value in the form, such as a blank field | Fill in every field and try again |

## Errors From Code & Notebooks

### CUDA Out-of-Memory Errors

`RuntimeError: CUDA out of memory` concerns the memory on the GPU card, which is
a separate and much smaller pool than the pod's RAM. It is a different failure
from the `OOMKilled` (out-of-memory) status, which concerns the pod's RAM. Apply
the usual remedies in this order:

1. Reduce the batch size.
2. Restart the kernel. TensorFlow claims nearly all of the card's memory by
   default and does not release it until the process ends, so a notebook that
   ran TensorFlow earlier can leave too little GPU memory for PyTorch later in
   the same session.
3. Move to the next GPU class up if the model does not fit, and request the
   smallest class it fits in. Classes are listed in
   [GPU Classes](../gpu-access/gpu-classes.md).

### PyTorch GPU Detection

`torch.cuda.is_available()` returns `False` when the session has no GPU or is
running `rstudio-notebook`. A session has no GPU when it was launched without
`-g` or started from a CPU-only environment on the course's menu.
`rstudio-notebook` derives from the CPU image and is not GPU-enabled, as
described in
[Standard Images](../environments/standard-images.md#standard-images).
Confirm what a session holds from inside the container:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0));"
```

### Full Storage Quota

"No space left" when saving a notebook, or a "disk quota exceeded" email, means
the storage quota is full. Files deleted in the Jupyter interface move to
`.local/share/Trash`, where they continue to count against the quota until the
automatic purge after 7 days. A deletion in the Jupyter interface therefore
frees no space before that purge. Storage quotas are described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

### Grading Validation and Metadata Errors

"Failed to validate", "the source of the following cell has changed", or
"corrupt metadata" when grading means that a read-only or autograded cell was
copied, edited, or deleted. Recovery is described in
[Common Grading Failures & Recovery](../grading/grading-failures.md).

## Resource Tiers

Confusing the per-pod, per-namespace, and on-request resource tiers is the usual
reason a job does not schedule. The tiers and their figures are listed in
[Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers).
