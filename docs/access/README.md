# Access

This section covers the three routes onto Datahub and DSMLP (the browser, the
shell, and a remote editor), sign-in and session problems, and when access
starts and ends. Moving between the routes has no eligibility requirement and
requires no request.

| Page | Covers |
|---|---|
| [Datahub in the Browser](datahub-in-the-browser.md) | Signing in, selecting a course and environment, the browser session, concurrent Datahub sessions, stopping a session, and the status and quota pages. |
| [The Login Node](the-login-node.md) | Connecting over SSH, the permitted and prohibited uses of `dsmlp-login`, connecting without a password, tunnels to a notebook or service, and connection failures. |
| [Remote Editor Setup](remote-editor-setup.md) | Connecting VS Code to a container over Remote-SSH, the key pair and host entry, pod lifetime, ending the session, and editor connection failures. |
| [Sign-In & Session Problems](sign-in-and-session-problems.md) | Campus sign-in failures, a missing course, spawn failures, links clicked before sign-in, launches refused by the cluster, the end of course access, and reporting a problem. |
| [When Access Starts & Ends](when-access-starts-and-ends.md) | When access opens for each population, extensions, the duration of research access, the retention timeline, and archiving on request. |

## Access Routes

| Route | Interface | Typical use |
|---|---|---|
| Browser | Jupyter in a browser tab at [datahub.ucsd.edu](https://datahub.ucsd.edu) | Coursework, assignments, and work that finishes in one sitting |
| Shell | `ssh` to the login node, then a launch script | Work that must continue after disconnection, resource requests beyond the course menu, and batch jobs |
| Remote editor | VS Code, attached over SSH | Editing a codebase with local extensions on cluster hardware |

### Browser Access

The browser route covers most coursework. It requires no local installation, no
configuration, and no knowledge of Linux. Signing in and selecting a course and
an environment starts a Jupyter session that contains the account's files. A
session started from `datahub.ucsd.edu` expects the browser window to remain
open while its work runs, and is not the route for work that continues
unattended for hours. Signing in and stopping a session are described in
[Datahub in the Browser](datahub-in-the-browser.md).

### Shell Access

The shell is the route for work that the course menu does not cover. None of
the following uses requires permission.

- Background and batch jobs started from a terminal keep running after a
  disconnect, as described in
  [Working from the Command Line](../working-from-the-command-line.md).
- Resources beyond the course menu, such as more CPU or RAM or a GPU class that
  the course's environments do not include, are requested from the shell, as
  described in [GPU Access](../gpu-access/README.md).
- Large data transfers use `scp`, `sftp`, `rsync`, and `git`, which all run from
  the login node, as described in
  [Moving & Sharing Data](../workspaces-and-storage/moving-and-sharing-data.md).
- A session that will not start because a disk quota is full or a pod is stuck
  is cleared from the shell rather than from the browser, as described in
  [Sign-In & Session Problems](sign-in-and-session-problems.md).

Shell access begins at the login node, which is for launching jobs and moving
files rather than for running work, as described in
[The Login Node](the-login-node.md).

### Remote Editor Access

VS Code attached over Remote-SSH runs a local editor, with local extensions and
a debugger, against cluster hardware. It serves editing across many files and
requires the most setup of the three routes. Closing the editor does not
release the container. Setup is described in
[Remote Editor Setup](remote-editor-setup.md).

## Files, Entitlements, and Concurrency Across Routes

### Files

The login node and the container share a filesystem, and a home directory
follows the account between routes. A file uploaded in the browser is on the
login node, and a file transferred with `scp` is in the notebook. The
directories are described in
[Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live).

### Entitlements

Every route draws on the same workspace, the same quotas, and the same GPU
classes. The shell exposes more of them directly but grants nothing additional.

### Concurrency

A member may have one Datahub session running, alongside any number of shell,
VS Code, and batch jobs, as described in
[Concurrent Datahub Sessions](datahub-in-the-browser.md#concurrent-datahub-sessions).
The limit that applies is the total CPU, memory, and GPU across everything
running at once, as described in
[Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once).

---

[← Documentation index](../README.md)
