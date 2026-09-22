# Moving & Sharing Data

This page covers transferring files to and from the cluster, sharing files
within a workspace, and sharing data with people who have no cluster account.

## Transfer Routes

Files reach the cluster by one of four routes, chosen by size and by how often
the transfer is repeated.

| Route | Suited to |
|---|---|
| The Jupyter file browser | A few small files, transferred once |
| `git` | Code, and anything that will be changed and re-sent |
| `scp`, `sftp`, `rsync` | Data of any size, scripted or repeated |
| Globus | Large unattended transfers, and transfers between institutions |

Transfers run through the login node, `dsmlp-login`. Moving files and launching
jobs are its two purposes, as described in
[What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for).

## In the Browser

The JupyterLab file browser uploads files by drag and drop and downloads them
from the right-click menu. It suits a small number of small files, such as a
notebook and a CSV file. Above about 64 MB, or beyond a few dozen files,
transfers stall, and an interrupted transfer cannot be resumed. Where a file is
large and the browser is the only available route, compress it into a zip
archive, upload the archive, and extract it from a terminal.

## Git

`git` is installed on the login node and in the standard images. It is the
recommended route for code and notebooks and is poorly suited to large data. A
repository cloned on the login node is already present when the container
starts, because the two share a filesystem.

```bash
git clone https://github.com/<owner>/<repo>.git
```

A private repository requires a personal access token or an SSH key, as on a
local machine. A clone counts against quota like any other files.

## scp, sftp and rsync

`scp`, `sftp`, and `rsync` run from a terminal on the local machine, not from
the cluster. ITS recommends them for most transfers. On Windows,
[WinSCP](https://winscp.net/) provides the same function through a graphical
interface.

```bash
scp /local/path <username>@dsmlp-login.ucsd.edu:~/remote/path            # upload
scp <username>@dsmlp-login.ucsd.edu:~/remote/path /local/path            # download
scp -r <username>@dsmlp-login.ucsd.edu:/directory/to/send /local/where   # directory
```

`sftp` opens an interactive session, which is easier when the location of the
files is not known in advance. `rsync` sends only what has changed, which suits
a transfer that will be repeated.

```bash
sftp <username>@dsmlp-login.ucsd.edu
rsync -avr <directory> <username>@dsmlp-login.ucsd.edu                   # upload
rsync -avr <username>@dsmlp-login.ucsd.edu:<remote-path> <local-path>    # download
```

These tools run over `ssh` and do not require the VPN, as described in
[Connecting over SSH](../access/the-login-node.md#connecting-over-ssh).

### Pod Messages During a Transfer

Messages about a pod being created and deleted appear around the transfer. They
come from the short-lived container the cluster starts to serve the transfer and
do not indicate an error.

## Landing Files in the Right Directory

> [!WARNING]
> On `dsmlp-login`, `~` is the personal area, which appears as `private/` inside
> a container. It is not a course home directory. Files sent to `~` with `scp` do
> not appear where a course notebook expects them, and a copy of the login-node
> home does not include the coursework.

To transfer to or from a workspace home directory, take its path from the
workspace listing:

```bash
workspace -l     # prints each workspace and the path to its home directory
```

Workspace home paths have the form
`/dsmlp/workspaces-fs0*/<WORKSPACE>/home/<username>`. Team directories use the
same prefix, with `/teams` in place of `/home`. The directory layout is
described in [Where Files Live](your-files-and-quotas.md#where-files-live).

## Globus

Globus suits large unattended transfers and transfers between institutions. The
supported method is to run Globus Connect Personal inside the environment, which
makes the environment an endpoint for transfers in either direction.

### Globus Connect Personal Setup

In a terminal inside the environment, download and unpack the client and run its
setup. The directory the archive unpacks into is named for the version
downloaded.

```bash
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar -xvzf globusconnectpersonal-latest.tgz
./globusconnectpersonal-<version>/globusconnectpersonal -setup
```

Setup prints a login link. Globus authenticates through CILogon.

1. Open the login link and choose **University of California-San Diego**.
2. Sign in with Active Directory (AD) credentials and Duo.
3. Allow the setup tool, and paste the returned code at the
   `Enter the auth code:` prompt.
4. Enter a recognizable endpoint name when setup asks for one.
5. Start the endpoint with `-start &`.
6. Check the endpoint on the Globus
   [Collections](https://app.globus.org/collections?scope=administered-by-me)
   page under **Administered By You**. Green indicates that the endpoint is
   running; red indicates that it is stopped.

### Endpoint Availability

The endpoint runs only while the environment runs. To restart a stopped (red)
endpoint, log back in, launch the environment, and start the endpoint again.
Adding the start command to `.bash_profile` starts the endpoint with every
terminal opened in the environment.

## Downloading from the Internet

`wget` and `curl` are available on the login node and in the container. They are
the simplest way to download a public dataset directly onto the cluster. Check
the size of a dataset before downloading it. Where the data is large and more
than one person needs it, request that it be staged once instead of each person
keeping a copy, as described in
[Asking for a Dataset to Be Staged](datasets.md#asking-for-a-dataset-to-be-staged).

## Retrieving Work Before Access Ends

Files become unreachable when access ends, not when they are purged. Copy them
out before access ends. Once the environment no longer appears for a member, the
work in it can be retrieved only by request to ITS. The effects of the end of
access are described in
[Effects of the End of Access](../access/when-access-starts-and-ends.md#effects-of-the-end-of-access).

> [!WARNING]
> Student home directories are not archived. Archiving covers instructor and
> course-wide files, on request. Copy out anything a student needs to keep before
> access ends.

### Directories to Copy

- The course home directory: notebooks, code, results, and figures. No copy of
  it is kept anywhere else.
- `teams/`, when a project's shared work is kept there.
- `private/`. It follows a member between workspaces. Its retention after
  access ends is not published.

`public/` usually holds the instructor's course material rather than a member's
own work. Re-obtain large shared datasets from their source rather than copying
them to a laptop.

A running container is not required. The container and the login node share a
filesystem, so an `ssh` connection to the login node is enough to collect every
directory.

### Recovery After Access Ends

Work that is out of reach after access ends is not necessarily lost. Contact ITS
before treating it as lost. Until the environment is purged, ITS can revive an
archived class, make an archive available for download, or reactivate an
individual account at an instructor's request to resolve an Incomplete, an
academic integrity matter, or a hand-off. A request made earlier is more likely
to be granted.

## Inside the Workspace

The `public/` directory is the sanctioned way to share files with a whole
workspace. Every member can read everything in it. In a course, the shared
grader account holds write permission and stages the material. In other
workspaces, the person the workspace was set up around holds write permission.
The directory is described in
[The Shared Workspace Area](your-files-and-quotas.md#the-shared-workspace-area).

`teams/` shares files with one group within the workspace instead of the whole
workspace, such as a capstone group, a project team, or a group within a lab.

### Unreadable Files in `public/`

Files staged into `public/` can arrive unreadable, because they keep the
permissions they had at their source. To repair them, run the following as the
account that owns the directory:

```bash
chmod -R u+rwX,go+rXs,go-w ~/public
```

The command removes write permission for everyone other than the owner and adds
the execute bit on directories so that they can be entered. Other permission
changes are made by the Service Desk on request, as described in
[Ownership and Permission Changes](#ownership-and-permission-changes).

## Teams and Canvas Groups

Course teams are created from Canvas group sets. An instructor either creates a
self-sign-up group set for students to join, or creates the groups and assigns
students to them. Changes are not immediate; they reach the cluster within a few
hours.

Canvas places only students in groups, so an instructor or TA cannot be added as
a member. Course staff join a group through the course's grader account, which is
enrolled as a student and joins groups in the same way.

Multiple group sets in one Canvas course may not work correctly. Use one group
set per course.

Group storage is provisioned separately from personal storage. Additional space
is requested from ITS, as described in
[Asking for More Space](your-files-and-quotas.md#asking-for-more-space).

### Team Data on the Command Line

From the command line, the team's data is requested at launch:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -G list      # the teams the account belongs to
launch-scipy-ml.sh -W <WORKSPACE> -G <teamid>  # launch with that team's data
```

## Ownership and Permission Changes

The Service Desk adjusts file ownership and permissions on request, alongside
resource limits and disk quotas, as listed in
[Administrative Requests](../reference/getting-help.md#administrative-requests).
Submit a ticket when files are owned by the wrong account or are unreadable by
the people who need them.

## Sharing with People Who Have No Cluster Account

Two services deliver data to people outside the cluster: Globus Project Guest
Collections for sharing with collaborators and for publication, and rdl-share
for one-off transfers.

### Globus Project Guest Collections

A **Globus Project Guest Collection** is the campus mechanism for sharing
research data with named collaborators, at UC San Diego or elsewhere, and for
publishing it openly. A PI requests one from Research IT with a short
description of the project and its intended use. The PI is the collection's
Access Manager and may delegate that role.

A collection shares a directory and everything below it. The directory may be
shared with any of the following:

- One named person, by institutional identity or email address
- A Globus group created for the purpose
- Every user logged in to Globus
- The public, anonymously and with no login

| Aspect | Rule |
|---|---|
| Permission scope | Permissions are set on directories, not on files. Child directories inherit from their parent. |
| Access levels | Read, or read and write. Write access includes delete. |
| Public data | Anything shared publicly belongs in a directory named to indicate that it is public, with write access to it kept narrow. |
| HTTPS links | Files can also be distributed over HTTPS, as links of the form `https://<collectionid>.data.globus.org/<path>` that can be embedded elsewhere. |
| Allocation | Allocations run one year at a time, start at 500 GB, and can be expanded somewhat. They are reviewed for renewal, with priority to collections in active use. |
| Ownership | A collection cannot change owner. When a project passes to a new PI, a new collection is created and permissions are reassigned. |

### One-Off Transfers with rdl-share

For a one-off transfer to a person, the Library's
[rdl-share](https://rdl-share.ucsd.edu) service carries up to 500 GB per
message, with no limit on the number of messages. It encrypts data in transit
and can request files from a person as well as send them. It refuses executable
file types.

## Hosting and Data Classification Restrictions

Datahub and DSMLP are not a hosting platform. They should not be used to run
externally available services or applications except as required for coursework
or projects. Sharing data is supported; running a public service is not.

Sharing data requires a classification decision before any technical step.
Licensed data, protected data, and data under a data use agreement do not become
shareable by being copied into a shared directory. These categories are
described in
[Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets).
