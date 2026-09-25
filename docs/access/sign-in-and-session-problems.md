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
environment does not start. How long the failure takes to appear narrows down
the cause:

| When the failure appears | Possible causes |
|---|---|
| Within moments of the start | A full disk quota, or a broken package in `.local/lib` |
| After a long wait | A busy cluster, or a slow download of the environment's image |

A stale profile can also stop a session from starting. The manual resetter
clears it.

### Full Disk Quota

A full disk quota prevents a session from starting and produces no error
message. The quota is shown at
[datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn) → **Services** →
**disk-quota-service**. Storage quotas are described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

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

### Busy Cluster

On a busy cluster, a session can wait for CPU, memory, or a GPU until the start
fails. A GPU session started without a booking also waits for an on-demand
lease, which may not be granted in time. Start the session again later. See
[When the Cluster Is Full](../gpu-access/quotas-and-availability.md#when-the-cluster-is-full).

### Slow Image Download

A session cannot start until its environment's image is on the cluster. When
the image has to be downloaded in full, the start can fail before the download
finishes. A full download of the `scipy-ml-notebook` image can take about 20
minutes. Start the session again later.

### Stale Profile and the Manual Resetter

The **manual resetter** is provided for a stale profile. It stops any running
servers, signs the account out, and resets the profile. Files are preserved.

1. Open [datahub.ucsd.edu](https://datahub.ucsd.edu).
2. Open the **services** dropdown and choose **manual-resetter**.
3. Click reset.

The manual resetter also stops a running session that cannot be reached from
the browser.

### Unexplained Spawn Failures

Report a spawn failure that none of these causes explains, with the time and
the course. See [Reporting a Problem](#reporting-a-problem).

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

## Reservation App Sign-In

The reservation app at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/) uses UCSD single
sign-on, like Datahub, but keeps its own session.

### Expired Reservation App Sessions

A reservation app session ends after 8 hours without use, and 24 hours after
sign-in in any case. The app then returns to its login page with the notice
`Your session has expired. Please sign in again.` A booking that was being made
in the wizard is lost. Sign in again and start the booking again.

**Log out everywhere** ends the session on every device at once. Each other
device shows the same notice at its next request to the app, such as opening
another of the app's pages. The device where **Log out everywhere** was selected
returns to the login page with no notice.

### Sign-In Failure Notices

A failed sign-in returns to the login page with one of these notices:

| Notice | Meaning | Fix |
|---|---|---|
| `Your sign-in attempt expired or was started in another browser window. Please try again.` | Sign-in took more than 10 minutes, or **Back** or **Refresh** was used during it | Start again from the login page |
| `Your sign-in provider did not complete the sign-in. Please try again.` | Campus sign-in did not complete | Start again from the login page. If it happens again, write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| `Your sign-in provider did not return your account details. Please try again, and contact an administrator if this keeps happening.` | Campus sign-in completed but did not pass the account to the app | Start again from the login page. If it happens again, write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| `Your account's domain is not permitted to use this service.` | A non-UCSD account was used | Sign in with a UCSD account |
| `Your account has been deactivated. Contact an administrator if you believe this is a mistake.` | The reservation app account is deactivated | Write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |
| `Sign-in failed. Please try again.` | Sign-in failed for another reason | Start again from the login page. If it happens again, write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |

### Form Errors in the Reservation App

When the app rejects a value sent from a form, the message names the field and
the problem, as `field: problem`. The app joins several problems with `; `. For
example, a blank **GPU Count** in the **New Reservation** form on
**Group Reservations** gives `gpu_count: Input should be a valid integer`.
Correct the named field and try again.

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
