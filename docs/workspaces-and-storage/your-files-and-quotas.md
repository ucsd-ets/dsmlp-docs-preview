# Directories, Quotas & Cleaning Up

A session presents several distinct places to keep files, and which one is in
view depends on the route in — browser or terminal — and on the workspace.
Confusing them is the commonest cause of "my files have disappeared"; the files
are almost always intact, in a directory other than the one on screen. Storage is
finite and modest, and running out is usually caused by one of a small number of
things.

**Contents**

- [Where Files Live](#where-files-live)
- [Home Is Per Workspace](#home-is-per-workspace)
- [The Shared Workspace Area](#the-shared-workspace-area)
- [The Personal Area](#the-personal-area)
- [Team Directories](#team-directories)
- [The Container and the Login Node Share a Filesystem](#the-container-and-the-login-node-share-a-filesystem)
- [Two Quotas, Not One](#two-quotas-not-one)
- [Checking Usage](#checking-usage)
- [What Usually Fills a Quota](#what-usually-fills-a-quota)
- [When the Disk Is Full](#when-the-disk-is-full)
- [Asking for More Space](#asking-for-more-space)
- [Storage Outside the Two Pools](#storage-outside-the-two-pools)
- [Mounting External Storage](#mounting-external-storage)
- [What Is Not a Mount](#what-is-not-a-mount)

## Where Files Live

------------------------------------------------------------------------

| Directory | In the notebook file browser | Inside the container | Visible to |
|---|---|---|---|
| Workspace home | the top of the browser | `/home/<username>` | The member |
| Shared workspace area | `/public` | `/home/<username>/public` | Everyone in the workspace |
| Personal area | `/private` | `/home/<username>/private` | The member, in every workspace |
| Team area | `/teams` | `/home/<username>/teams/<team>` | Members of that team |

**Two quota pools sit underneath these four.** The workspace home, `public/` and
`teams/` all draw on the **workspace** quota; `private/` draws on a separate
**personal** quota, which belongs to the account rather than to any course.
→ [Two Quotas, Not One](#two-quotas-not-one)

## Home Is Per Workspace

------------------------------------------------------------------------

**A home directory is specific to one workspace.** A workspace is a course, a
lab, or a catch-all population, and each member has a separate home directory in
every workspace they belong to.
→ [What a Workspace Is](what-a-workspace-is.md)

One account therefore holds several home directories, and "my notebooks are
gone" is usually "I launched the other course".
→ [Belonging to Several Workspaces](what-a-workspace-is.md#belonging-to-several-workspaces)

*Course homes are small* — on the order of 5-10 GB, against roughly 100 GB for a
research account.

## The Shared Workspace Area

------------------------------------------------------------------------

**`public/` is the workspace's common ground**, readable by every member. Course
datasets, starter notebooks and reference material normally appear there.

In a course, the shared **grader account** holds write permission on `public/`
and everyone else reads. *Files staged there by an instructor or TA can land
unreadable* — the published fix is on
[Moving & Sharing Data](moving-and-sharing-data.md#inside-the-workspace).

## The Personal Area

------------------------------------------------------------------------

**`private/` follows the member into every workspace.** It is the one directory
that appears unchanged wherever a session starts, and its contents count against
the personal quota rather than any course's. It holds tooling, credentials,
notes, and projects that outlive a single course.

## Team Directories

------------------------------------------------------------------------

**`teams/` holds data scoped to a group within a workspace** — a lab bench, a
project team, a capstone group. Course teams are created from Canvas group
sets, and membership changes take a few hours to reach the cluster.

From the command line, teams are mounted only when requested:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -G list      # list the teams the account belongs to
launch-scipy-ml.sh -W <WORKSPACE> -G <teamid>  # launch with that team's data
```

**`-G` is the group flag; `-g` is the GPU count.** They are one keystroke apart
and mean entirely different things.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

*Team directory names are generated, not chosen*, and can contain spaces and
brackets — a capstone team directory reads something like
`dsc-180a---a14-[88137]`. Such a name has to be quoted in a `cd` and in any path
written into a script.

## The Container and the Login Node Share a Filesystem

------------------------------------------------------------------------

**A file written in one is visible in the other.** The container a job runs in
and the `dsmlp-login` jumpbox mount the same storage, so a repository cloned at
the login node is already present when the container starts, and output written
inside the container is there to `scp` away after the job ends. There is no
staging step and no copy to schedule.

**What differs is the starting directory.** On `dsmlp-login`, `~` is the
*personal* area — the same directory that appears as `private/` inside a
container. A course home is somewhere else entirely, and does not appear in `~`
at all:

```bash
workspace -l               # list available workspaces and the path to each home
workspace -c <WORKSPACE>   # change to that workspace's home directory
```

The paths look like `/dsmlp/workspaces-fs0*/<WORKSPACE>/home/<username>`, with
team files under the same prefix and `/teams` in place of `/home`. *The directory
may not appear in a listing until it is entered with `cd`.*

## Two Quotas, Not One

------------------------------------------------------------------------

**Storage draws on two separate pools**, and the state of one says nothing about
the other.

| Pool | What counts against it |
|---|---|
| **Workspace** | The workspace home, plus `public/` and `teams/` |
| **Personal** | `private/`, in every workspace |

**Course homes run 5-10 GB**, toward the lower end for very large classes.
**Research homes are on the order of 100 GB**, set when the account is
provisioned. Both are set per workspace rather than per person, so the figure
that applies to a given account is the one the disk quota service reports — not a
number from another course, and not a number from an article.
<!-- FIGURE: confirmed per-workspace course and research quota values -->

*Storage above 1 TB is chargeable.* Compute is not.

## Checking Usage

------------------------------------------------------------------------

**From a browser** — the route that works even when the notebook will not start:
go to [datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn), open the
**Services** tab, and choose **disk-quota-service**. The same service is reachable
from the **Services** menu in the navigation bar once an environment is running.
It reports usage against quota, and displays the workspace ID that terminal
commands need.

**From a terminal**, `du` reports where the space went:

```bash
du -h --max-depth 1
```

Run it in the workspace home first, then in whichever directory turns out to be
the large one.

A "disk quota exceeded" message is sent by email; where one has arrived, the disk
is the cause of whatever else is going wrong.

## What Usually Fills a Quota

------------------------------------------------------------------------

**Deleted files, still present.** Deleting in the Jupyter interface moves the file
to `.local/share/Trash`, where it goes on occupying quota. *Trash is purged
automatically after 7 days*; to reclaim the space sooner, open a terminal, `cd` to
`.local/share/Trash`, and delete the files there with `rm`.

**`.vscode-server`.** Remote editing installs a server into the home directory,
and it grows past 1 GB — a substantial fraction of a course-sized quota, and
invisible in the file browser.
→ [Remote Editor Setup](../access/remote-editor-setup.md)

**Packages installed into `.local`.** Every `pip install` without a virtual
environment lands in the home directory and stays there across sessions. Beyond
the space, a broken package there can stop the environment starting at all.
→ [Customizing an Environment](../environments/customizing-your-environment.md)

**A personal copy of a shared dataset.** Large inputs belong in the workspace's
`public/` area or under `/datasets`, read in place by every member.
→ [Shared Datasets](datasets.md#where-shared-data-lives)

## When the Disk Is Full

------------------------------------------------------------------------

**A full quota can prevent the environment from starting**, which removes the file
browser that would have cleared it. The way back in is the login node:

```bash
ssh <user>@dsmlp-login.ucsd.edu
workspace -l                 # find the workspace ID and its path
workspace -c <WORKSPACE>     # change to that workspace's home
du -h --max-depth 1          # find what is large
rm <files>                   # remove it
```

*The login-node `~` is the personal area, not a course home* — clearing files
there frees the personal pool and does nothing for a full workspace pool. Once
usage drops below the quota, environments start normally again.
→ [The Login Node](../access/the-login-node.md#what-the-login-node-is-for)

## Asking for More Space

------------------------------------------------------------------------

**Students in a course** ask their instructor or TA, who raises it on the
course's existing Service Desk ticket.

**Independent study and project users** may submit a ticket directly.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

**Research accounts** are handled by Research IT, at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu); temporary increases are
possible where the need is bounded.

**Group and team space** is requested from
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). *The FAQ states that groups are
provisioned with 100 GB by default; that figure is unconfirmed.*

Please check that the space is genuinely in use before requesting an increase — an
emptied Trash and a removed dataset copy resolve most requests without a ticket.

## Storage Outside the Two Pools

------------------------------------------------------------------------

**`/datasets` is a shared, staged tree**, present in containers and on the login
node, holding common corpora and course-specific data. It counts against neither
quota and is not member-writable — data is placed there on request.
→ [Shared Datasets](datasets.md)

## Mounting External Storage

------------------------------------------------------------------------

Home directories are sized for code and working files. Data larger than that
model comfortably holds goes on storage that lives elsewhere and is mounted into
the workspace's containers, rather than into a larger home directory.

**External storage is storage the cluster does not own**, attached to a workspace
so that it appears as an ordinary directory to jobs running there. **SDSC
Universal Scale Storage** is the usual example; other shares are handled the same
way. *This is a research and lab arrangement rather than a course one* — a
course's data belongs in the workspace's shared area or in `/datasets`.

Two access paths are documented for Universal Scale Storage shares:

| From | Path |
|---|---|
| `sftp` to the login node, when uploading | `/uss/<sharename>` |
| A shell after logging in | `/dsmlp/teams` |

*Licensed corpora are sometimes staged on the same storage* and mounted
read-only — the Nielsen subscription datasets are the standing example.
→ [Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets)

**Capacity governs where data is placed.** Above a certain volume, data belongs on
external storage and is mounted rather than copied, and the boundary is not one
users set for themselves. *The specific thresholds are not published, and we have
deliberately not invented them here* — please ask, giving the expected volume and
its growth rate, and the reply will say what fits where.

**Research IT provisions and mounts external storage**, at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu), which is also the address for
the Research Cluster and for Universal Scale Storage generally. Please include:

- **What the data is**, and any licensing or classification that travels with it.
  → [Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets)
- **How much there is now, and how fast it grows.**
- **Which workspace should see it**, and who within that workspace needs to write
  as opposed to read.
- **Whether it already exists** on a campus or SDSC service, or is to be acquired.

*Where the question is which platform to use rather than how to provision on this
one*, Research IT will advise on where the work belongs.

## What Is Not a Mount

------------------------------------------------------------------------

**Campus and commercial cloud storage are not mounted into containers.** Google
Drive, OneDrive, and commercial object storage under the University's billing
arrangements are all reasonable places to keep data, but reaching them from a job
is a transfer, not a mount.
→ [Moving & Sharing Data](moving-and-sharing-data.md)

**A mount is not a backup**, and neither is a home directory. Please keep the
authoritative copy of anything irreplaceable on storage whose backup terms are
known.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
