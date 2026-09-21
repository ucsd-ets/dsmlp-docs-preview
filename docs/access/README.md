# Access

Three ways in — the browser, the shell, and a remote editor — and what to do when
one of them will not let you in.

------------------------------------------------------------------------

There is no eligibility requirement and nothing to request in order to move
between them. Everything on this page is documented once and linked from
wherever it is needed.

**Every page in this directory is an initial draft.** Each opens with a note
naming what its writer could not settle. Please read those before treating any
page as final.

| Page | Covers |
|---|---|
| [Datahub in the Browser](datahub-in-the-browser.md) | Signing in, picking a course and environment, and stopping a session. |
| [The Login Node](the-login-node.md) | `ssh`, what belongs on `dsmlp-login` and what does not, and reaching a service through a tunnel. |
| [Remote Editor Setup](remote-editor-setup.md) | VS Code over Remote-SSH, against a container rather than the login node. |
| [Sign-In & Session Problems](sign-in-and-session-problems.md) | The address, a missing course, a spawn failure, and a launch the cluster refuses. |
| [When Access Starts & Ends](when-access-starts-and-ends.md) | Provisioning dates by population, retention, archiving and purge. |

## The Three Routes

------------------------------------------------------------------------

| Route | Interface | Best for |
|---|---|---|
| **Browser** | [datahub.ucsd.edu](https://datahub.ucsd.edu) — Jupyter in a tab | Coursework, assignments, anything that finishes in one sitting |
| **Shell** | `ssh` to the login node, then a launch script | Work that must outlive the connection, resource requests beyond the course menu, batch jobs |
| **Remote editor** | VS Code, attached over SSH | Editing a real codebase, with local extensions, against cluster hardware |

**The browser covers most coursework.** It requires nothing installed, nothing
configured, and no knowledge of Linux: signing in, selecting a course and
selecting an environment produces a Jupyter session with the account's files in
it. A session started from `datahub.ucsd.edu` expects the browser window to
remain open while its work runs, and is not the route for work that continues
unattended for hours. → [Datahub in the Browser](datahub-in-the-browser.md)

**The shell is the route for anything the course menu does not cover.** Any one
of these is sufficient reason, and none of them requires permission.

- **Work that must outlive the connection.** Background and batch jobs are
  started from a terminal and keep running after a disconnect.
  → [Working from the Command Line](../working-from-the-command-line.md)
- **Resources beyond the course menu** — more CPU or RAM, or a GPU class the
  course's environments do not include. → [GPU Access](../gpu-access/README.md)
- **Moving a lot of data.** `scp`, `sftp`, `rsync` and `git` all run from the
  login node.
  → [Moving & Sharing Data](../workspaces-and-storage/moving-and-sharing-data.md)
- **Cleanup.** A session that will not start because a disk quota is full or a
  pod is stuck is cleared from the shell rather than from the browser.
  → [Sign-In & Session Problems](sign-in-and-session-problems.md)

The shell begins at the login node, which is a jumpbox and not a machine for
running work. → [The Login Node](the-login-node.md)

**A remote editor suits a project that has outgrown a notebook.** Editing across
many files, with local extensions and a debugger, is served by VS Code attached
over Remote-SSH, which runs a local editor against cluster hardware. It takes the
most setup of the three, and **closing the editor does not release the
container**. → [Remote Editor Setup](remote-editor-setup.md)

## What Does Not Change Between Them

------------------------------------------------------------------------

**Files.** The login node and the container share a filesystem, and a home
directory follows the account between routes. A file uploaded in the browser is
on the login node; a file transferred with `scp` is in the notebook.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Entitlements.** The same workspace, the same quotas, the same GPU classes. The
shell exposes more of them directly, but does not grant anything extra.

**Concurrency.** A member may have **one Datahub session** running, alongside any
number of shell, VS Code and batch jobs. The ceiling that binds is the total CPU,
memory and GPU across everything running at once.
→ [One Datahub Session](datahub-in-the-browser.md#one-datahub-session) ·
[Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once)

---

[← Documentation index](../README.md)
