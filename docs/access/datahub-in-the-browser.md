# Datahub in the Browser

[datahub.ucsd.edu](https://datahub.ucsd.edu) provides browser-based access to
course environments. It requires a browser, UCSD campus credentials and Duo. No
local installation or command-line experience is needed.

## Signing In

------------------------------------------------------------------------

1. Open [datahub.ucsd.edu](https://datahub.ucsd.edu).
2. Sign in through **UCSD single sign-on**, with campus credentials.
3. Approve the Duo prompt.

**This is the standard campus sign-on**, the same one used by other UCSD
services — there is nothing Datahub-specific to enter. *An account that cannot
get past the campus sign-in page has a credential problem rather than a Datahub
one*, and the [ITS Service Desk](https://support.ucsd.edu/) handles it.

*The Active Directory **username** matters at a different prompt* — `ssh` to the
login node, where the full address is not accepted.
→ [Connecting over SSH](the-login-node.md#connecting-over-ssh)

## Selecting a Course & Environment

------------------------------------------------------------------------

Sign-in is followed by a list of the courses available to the account and,
within a course, the environments configured for it.

**Course.** Each Datahub course appears separately and holds its own files.
Students and instructors enrolled in more than one course select among them
here.
→ [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

**Environment.** The options in this menu are set by the course instructor —
commonly one CPU option, and a GPU option in courses that use them.
Environments not present in the menu are added by the instructor.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

An environment takes one to two minutes to start, and longer while the cluster
is busy. → [The Status Page](../gpu-access/quotas-and-availability.md#the-status-page)

## The Browser Session

------------------------------------------------------------------------

**A browser session starts with 2 CPU cores and 4GB of RAM.** This is the
course spawn configuration, set per course. The defaults applied by the
command-line launch scripts are a separate figure describing a different
object; the two are not reconciled.
→ [Working from the Command Line](../working-from-the-command-line.md)

A session provides JupyterLab: notebooks, a file browser, a text editor and a
terminal. **Files persist between sessions.** Software installation within an
environment, and the conditions under which an installation persists, are
covered separately.
→ [Customizing an Environment](../environments/customizing-your-environment.md)

## One Datahub Session

------------------------------------------------------------------------

**A member may have one Datahub session running at a time.** The limit is on
Datahub itself, and it is a limit of one *session* — not of one environment, and
not of one course. Working in a different course environment means stopping the
running session first.

**The limit does not extend to work launched from a shell.** SSH sessions, VS
Code containers and batch jobs run alongside a Datahub session, and alongside
each other, in any number. *Launching a container from `dsmlp-login` while a
browser session is open is ordinary use, not a conflict.*

**The ceiling that does apply is an aggregate one.** Total CPU, memory and GPU
across everything a member has running must fit within the Kubernetes limits set
on their namespace and, where GPUs are involved, within the reservation system's
limits. A launch is refused when the total would exceed them, whatever mix of
sessions makes up that total.
→ [Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once)

## Stopping a Session

------------------------------------------------------------------------

**Signing out does not stop a session, and neither does closing the browser
tab.** The container continues to run, holding its CPU, its memory, and its GPU
where one is attached.

To stop a session, use **File → Hub Control Panel → Stop My Server**. The
interface may take a short time to reflect the change.

*Where the browser session cannot be reached at all* — a stale profile, a page
that will not load — the **manual-resetter** under the services dropdown at
[datahub.ucsd.edu](https://datahub.ucsd.edu) stops any running servers and resets
the profile, leaving files untouched.
→ [Sign-In & Session Problems](sign-in-and-session-problems.md)

## Status & Quota Pages

------------------------------------------------------------------------

| Page | Location | Contents |
|---|---|---|
| Disk usage | [datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn) → **Services** tab → **disk-quota-service** | Storage in use against the account quota |
| Cluster status | [datahub.ucsd.edu/hub/status](https://datahub.ucsd.edu/hub/status) | Cluster nodes, the GPU models on them, and free GPU counts |

**A full quota prevents a session from starting, and produces no error
message.**

→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one) ·
[The Status Page](../gpu-access/quotas-and-availability.md#the-status-page)

## Sign-In Failures

------------------------------------------------------------------------

Most failures to reach a session resolve to one of three conditions:

- The course does not appear in the course list.
- The disk quota is full.
- A Datahub session is already running.

→ **[Sign-In & Session Problems](sign-in-and-session-problems.md)**

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
