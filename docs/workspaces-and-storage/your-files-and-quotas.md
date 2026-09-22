# Directories, Quotas & Cleaning Up

This page covers the directories available in a session, the workspace and
personal storage quotas, reclaiming space, and external storage mounted into a
workspace.

## Where Files Live

The directory in view depends on the route into the session, browser or
terminal, and on the workspace. Files that appear to be missing are usually
intact in a directory other than the one on screen.

| Directory | In the notebook file browser | Inside the container | Visible to |
|---|---|---|---|
| Workspace home | the top of the browser | `/home/<username>` | The member |
| Shared workspace area | `/public` | `/home/<username>/public` | Everyone in the workspace |
| Personal area | `/private` | `/home/<username>/private` | The member, in every workspace |
| Team area | `/teams` | `/home/<username>/teams/<team>` | Members of that team |

The workspace home, `public/`, and `teams/` draw on the workspace quota.
`private/` draws on a separate personal quota. Both pools are described in
[Workspace and Personal Quotas](#workspace-and-personal-quotas).

## Workspace Home Directories

A home directory is specific to one workspace. A workspace is a course, a lab,
or a catch-all population, as described in
[What a Workspace Is and What It Controls](what-a-workspace-is.md). Each member
has a separate home directory in every workspace the member belongs to.

One account therefore holds several home directories. Notebooks that appear to
be missing are usually in the home directory of another workspace, such as a
different course. Membership of more than one workspace is described in
[Belonging to Several Workspaces](what-a-workspace-is.md#belonging-to-several-workspaces).

Home directory sizes are listed in
[Workspace and Personal Quotas](#workspace-and-personal-quotas).

## The Shared Workspace Area

`public/` is readable by every member of the workspace. Course datasets,
starter notebooks, and reference material normally appear there.

In a course, the shared grader account holds write permission on `public/`, and
all other members have read access. Files staged there by an instructor or TA
can be unreadable. The fix is described in
[Inside the Workspace](moving-and-sharing-data.md#inside-the-workspace).

## The Personal Area

`private/` is the one directory that appears unchanged in every workspace in
which a session starts. Its contents count against the personal quota rather
than against any course's quota. It holds tooling, credentials, notes, and
projects that extend beyond a single course.

## Team Directories

`teams/` holds data scoped to a group within a workspace, such as a lab bench, a
project team, or a capstone group. Course teams are created from Canvas group
sets. Membership changes take a few hours to reach the cluster.

### Mounting Team Data from the Command Line

From the command line, teams are mounted only when requested:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -G list      # list the teams the account belongs to
launch-scipy-ml.sh -W <WORKSPACE> -G <teamid>  # launch with that team's data
```

> [!NOTE]
> `-G` is the group flag and `-g` is the GPU count, as listed in
> [Team Selection](../running-jobs/launch-sh-reference.md#team-selection).

### Team Directory Names

Team directory names are generated, not chosen, and can contain spaces and
brackets. For example, a capstone team directory can be named
`dsc-180a---a14-[88137]`. Quote such a name in a `cd` command and in any path
written into a script.

## Filesystem Shared with the Login Node

The container a job runs in and the login node, `dsmlp-login`, mount the same
storage. A file written in one is visible in the other. A repository cloned on
the login node is present when the container starts, and output written inside
the container remains available to copy with `scp` after the job ends. No
staging or copy step is required.

### Starting Directory on the Login Node

On `dsmlp-login`, `~` is the personal area, the same directory that appears as
`private/` inside a container. A course home directory is in a different
location and does not appear in `~`. The `workspace` command locates it:

```bash
workspace -l               # list available workspaces and the path to each home
workspace -c <WORKSPACE>   # change to that workspace's home directory
```

The paths have the form `/dsmlp/workspaces-fs0*/<WORKSPACE>/home/<username>`.
Team files are under the same prefix, with `/teams` in place of `/home`. The
directory may not appear in a listing until it is entered with `cd`.

## Workspace and Personal Quotas

Storage draws on two separate quota pools. The state of one pool does not
indicate the state of the other.

| Pool | What counts against it |
|---|---|
| Workspace | The workspace home, plus `public/` and `teams/` |
| Personal | `private/`, in every workspace |

The personal quota belongs to the account rather than to any course.

Course home directories are 5-10 GB, toward the lower end for very large
classes. Research home directories are on the order of 100 GB, set when the
account is provisioned. Both values are set per workspace rather than per
person. The value that applies to a given account is the one the disk quota
service reports, as described in [Checking Usage](#checking-usage).

Storage above 1 TB is chargeable. Compute is not.

## Checking Usage

The disk quota service reports usage against quota and displays the workspace
ID that terminal commands require. It is reachable from a browser even when the
notebook does not start:

1. Go to [datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn).
2. Open the **Services** tab.
3. Choose **disk-quota-service**.

Once an environment is running, the same service is available from the
**Services** menu in the navigation bar.

In a terminal, `du` reports where the space is used:

```bash
du -h --max-depth 1
```

Run it in the workspace home first, then in the largest directory it reports.

A "disk quota exceeded" message is sent by email. When that message has
arrived, the full disk is the cause of any other failure in the environment.

## Common Causes of a Full Quota

### Jupyter Trash

Deleting a file in the Jupyter interface moves it to `.local/share/Trash`,
where it continues to count against the quota. Trash is purged automatically
after 7 days. To reclaim the space sooner:

1. Open a terminal.
2. Change to `.local/share/Trash` with `cd`.
3. Delete the files there with `rm`.

### `.vscode-server`

Remote editing installs a server into `.vscode-server` in the home directory.
The directory grows past 1 GB, a substantial fraction of a course-sized quota,
and does not appear in the file browser. Remote editing is described in
[Remote Editor Setup](../access/remote-editor-setup.md).

### Packages in `.local`

Every `pip install` run without a virtual environment installs into `.local` in
the home directory, and the packages remain there across sessions. A broken
package there can also stop the environment from starting. Package installation
is described in
[Customizing an Environment](../environments/customizing-your-environment.md).

### Personal Copies of Shared Datasets

A personal copy of a shared dataset counts against the quota. Large inputs
belong in the workspace's `public/` area or under `/datasets`, where every
member reads them in place, as described in
[Where Shared Data Lives](datasets.md#where-shared-data-lives).

## Recovering from a Full Quota

> [!WARNING]
> A full quota can prevent the environment from starting, which also removes
> the file browser that would otherwise be used to clear it.

Files can then be removed from the login node:

```bash
ssh <user>@dsmlp-login.ucsd.edu
workspace -l                 # find the workspace ID and its path
workspace -c <WORKSPACE>     # change to that workspace's home
du -h --max-depth 1          # find what is large
rm <files>                   # remove it
```

On the login node, `~` is the personal area, not a course home. Removing files
there frees space in the personal pool and has no effect on a full workspace
pool. Once usage drops below the quota, environments start normally again. The
login node is described in
[What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for).

## Asking for More Space

| Requester | Route |
|---|---|
| Students in a course | The instructor or TA, who raises the request on the course's existing Service Desk ticket |
| Independent study and project users | A ticket submitted directly, as described in [Administrative Requests](../reference/getting-help.md#administrative-requests) |
| Research accounts | Research IT, at [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu). Temporary increases are possible where the need is bounded |
| Group and team space | [datahub@ucsd.edu](mailto:datahub@ucsd.edu) |

Before requesting an increase, confirm that the space is in use. Empty the Trash
and remove any personal copy of a shared dataset, as described in
[Common Causes of a Full Quota](#common-causes-of-a-full-quota).

## Storage Outside the Quota Pools

`/datasets` is a shared, staged directory tree, present in containers and on the
login node. It holds common corpora and course-specific data. It counts against
neither quota and is not writable by members. Data is placed there on request,
as described in [Datasets](datasets.md).

## Mounting External Storage

Home directories are sized for code and working files. Larger data goes on
storage hosted elsewhere and mounted into the workspace's containers, rather
than into a larger home directory.

**External storage** is storage the cluster does not own, attached to a
workspace so that it appears as an ordinary directory to jobs running there.
SDSC Universal Scale Storage is the usual example. Other shares are handled the
same way.

External storage is a research and lab arrangement. A course's data belongs in
the workspace's shared area or in `/datasets`.

### Universal Scale Storage

Two access paths are documented for Universal Scale Storage shares:

| From | Path |
|---|---|
| `sftp` to the login node, when uploading | `/uss/<sharename>` |
| A shell after logging in | `/dsmlp/teams` |

Licensed corpora are sometimes staged on the same storage and mounted
read-only. The Nielsen subscription datasets are an example, described in
[Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets).

### Capacity Thresholds

Above a certain volume, data belongs on external storage and is mounted rather
than copied. Users do not set this boundary. The thresholds are not published.
State the expected volume and its growth rate in the request described in
[Requesting External Storage](#requesting-external-storage). The reply states
what fits where.

### Requesting External Storage

Research IT provisions and mounts external storage. Requests go to
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu), which is also the address
for the Research Cluster and for Universal Scale Storage generally. Include in
the request:

- What the data is, and any licensing or classification that applies to it, as
  described in
  [Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets).
- How much data exists now, and how fast it grows.
- Which workspace should see it, and which members of that workspace need to
  write as opposed to read.
- Whether it already exists on a campus or SDSC service, or is to be acquired.

Where the question is which platform to use rather than how to provision on this
one, Research IT advises on where the work belongs.

## Cloud Storage and Backups

### Campus and Commercial Cloud Storage

Campus and commercial cloud storage are not mounted into containers. Google
Drive, OneDrive, and commercial object storage under the University's billing
arrangements can hold data, but a job reaches them by transfer, not by mount.
Transfer methods are described in
[Moving & Sharing Data](moving-and-sharing-data.md).

### Backups

A mount is not a backup, and neither is a home directory. Keep the authoritative
copy of anything irreplaceable on storage whose backup terms are known.
