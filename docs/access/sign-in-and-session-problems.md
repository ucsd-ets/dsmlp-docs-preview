# Sign-In & Session Problems

This page covers common failures to reach or start a session on
[datahub.ucsd.edu](https://datahub.ucsd.edu) and their remedies, most of which
are self-service.

## Campus Sign-In Failures

Datahub sign-in is standard UCSD single sign-on. An account that cannot get past
the campus sign-in page has a campus credential problem, not a Datahub problem,
and the [ITS Service Desk](https://support.ucsd.edu/) handles it.

## Missing Course

Sign-in succeeds, but the expected course does not appear. A missing course is a
provisioning matter, not an access fault.

### Roster Loading and TSS Changes

Rosters are loaded into workspaces one business day before the start of the
term, and a TSS change, such as an add, a drop, or a section change, is
reflected in Datahub and DSMLP by 10am the day following the change. A course
that is not listed before those times has not been loaded yet. Report a course
that is still missing after that time to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). Roster provisioning is described in
[Students Enrolled in a Course](when-access-starts-and-ends.md#students-enrolled-in-a-course).

### Roster Checks by Course Staff

The instructor or TA is the first contact for a course matter. Course staff can
see the roster and can tell a student who is not yet enrolled from one who is
enrolled but not provisioned. Auditors, observers, and Extended Studies students
are not on the TSS roster that the automatic setup uses, and the instructor adds
them through Canvas, as described in
[Students Enrolled in a Course](when-access-starts-and-ends.md#students-enrolled-in-a-course).

### Access Outside a Course

No roster grants access for an independent study, a capstone, or a personal
project. Access for this work is obtained by request, as described in
[Projects & Independent Study](../student-project.md).

## "Spawn Failed"

The account is signed in and an environment has been selected, but the
environment does not start. Check four causes in order: a Datahub session
already running, a full disk quota, a stale profile, and a broken package in
`.local`.

### Datahub Session Already Running

A member may have one Datahub session at a time, and shell, VS Code, and batch
jobs do not count toward that limit, as described in
[Concurrent Datahub Sessions](datahub-in-the-browser.md#concurrent-datahub-sessions).
A session left running, for this course or another, must be stopped before a
new one starts. Stop it with **File → Hub Control Panel → Stop My Server**.
Where the running session cannot be reached, use the manual resetter described
in [Stale Profile and the Manual Resetter](#stale-profile-and-the-manual-resetter).

### Full Disk Quota

A full disk quota prevents a session from starting and produces no error
message. The quota is shown at
[datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn) → **Services** →
**disk-quota-service**. Storage quotas are described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

### Stale Profile and the Manual Resetter

The **manual resetter** is provided for a stale profile. It stops any running
servers, signs the account out, and resets the profile. Files are preserved.

1. Open [datahub.ucsd.edu](https://datahub.ucsd.edu).
2. Open the **services** dropdown and choose **manual-resetter**.
3. Click reset.

### Broken Package in `.local`

Packages under `.local/lib/python3.x/site-packages` load ahead of the packages
the image provides, and one incompatible package can stop a notebook from
starting. Move them aside from a terminal:

```bash
ssh USERNAME@dsmlp-login.ucsd.edu
workspace --list                  # the workspaces available to the account
workspace -c COURSE_ID            # enter the course workspace
mv .local/lib .local/lib.old      # move the offending packages aside
```

Install packages into a virtual environment rather than into `.local`.
Installing packages is described in
[Customizing an Environment](../environments/customizing-your-environment.md).

### Unexplained Spawn Failures

The cause of a spawn failure not explained by a running session, a full quota, a
stale profile, or a broken `.local` package is not yet documented. Report such a
failure with the time and the course, as described in
[Reporting a Problem](#reporting-a-problem).

## Links Clicked Before Sign-In

Course materials are often distributed by a link that fetches a repository into
the course environment:

```text
https://datahub.ucsd.edu/hub/user-redirect/git-pull?repo=<url-encoded>&urlpath=tree%2F<dir>%2F&branch=main
```

The most common failure of such a link is a click before sign-in. The link needs
a signed-in session to redirect into. Without one, it fails in a way that
resembles a broken link.

To open the link:

1. Sign in at [datahub.ucsd.edu](https://datahub.ucsd.edu).
2. Start the course environment.
3. Click the link.

Clicking a failed link again after signing in also works.

See also: [Grading](../grading/README.md)

## Launches Refused by the Cluster

### GPU Held by an Existing Pod

A launch that reports an exceeded GPU quota indicates that a pod on the same
account already holds the requested GPU. The earlier pod is usually terminating
and clears within a minute or two. If it does not clear, delete it from the
login node:

```bash
ssh USERNAME@dsmlp-login.ucsd.edu
kubectl get pods
kubectl delete pod <pod-id>
```

### Aggregate Resource Limits

Concurrent sessions are permitted, but their combined CPU, memory, and GPU must
fit within the Kubernetes limits on the namespace and, for GPUs, within the
reservation system's limits. A launch that would take the total past those
limits is refused. The remedy is to stop a session or job that is no longer in
use. No request is required. Running several jobs together is described in
[Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once).

### 504 Error After a Crash

A notebook that exhausts its memory or runs an infinite loop can take its pod
down. The hub then returns a 504 error until it detects the failure and resets.
To recover:

1. Delete the pod with `kubectl delete pod`, as described in
   [GPU Held by an Existing Pod](#gpu-held-by-an-existing-pod). This shortens
   the wait for the hub to reset.
2. Run the manual resetter, as described in
   [Stale Profile and the Manual Resetter](#stale-profile-and-the-manual-resetter).
3. Start the session again.

Error messages and their causes are listed in
[Error Messages](../reference/error-messages.md).

### Sessions Left Running After Sign-Out

> [!WARNING]
> Logging out, closing the tab, and closing a laptop leave the container running
> and holding its resources.

Stop the session with **File → Hub Control Panel → Stop My Server**, as
described in [Stopping a Session](datahub-in-the-browser.md#stopping-a-session).

## End of Course Access

Course access is retained for a period beyond the term the course ran in, as
described in
[One Additional Quarter](when-access-starts-and-ends.md#one-additional-quarter).
After that period, the course no longer appears, and its absence is not a fault.
Files remain retrievable for a period afterward, and an extension can be
requested. Copying files out is described in
[Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends).

## Reporting a Problem

Raise course matters with the instructor or TA first. For platform matters,
email [datahub@ucsd.edu](mailto:datahub@ucsd.edu) or file a ticket with the
[ITS Service Desk](https://support.ucsd.edu/). A report includes the following
details:

- The course
- The system in use (Datahub or `dsmlp-login`)
- The environment name
- The exact command, if there was one
- A screenshot

Response targets for individual issues are listed in
[Response Targets](../reference/getting-help.md#response-targets).
