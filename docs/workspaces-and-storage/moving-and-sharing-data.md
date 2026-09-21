# Moving & Sharing Data

Files reach the cluster by one of four routes, chosen mostly by size and by how
often the transfer is repeated. Sharing them splits into two quite different
problems: letting other people on the cluster read a member's files, and getting
data to someone who has no cluster account at all.

| Route | Suits |
|---|---|
| The Jupyter file browser | A handful of small files, once |
| `git` | Code, and anything that will be changed and re-sent |
| `scp` · `sftp` · `rsync` | Data of any size, scripted or repeated |
| Globus | Large transfers, unattended, between institutions |

**All of this happens at the login node.** Moving files is one of the two things
`dsmlp-login` exists for; the other is launching jobs.
→ [The Login Node](../access/the-login-node.md#what-the-login-node-is-for)

**Contents**

- [In the Browser](#in-the-browser)
- [Git](#git)
- [scp, sftp and rsync](#scp-sftp-and-rsync)
- [Landing Files in the Right Directory](#landing-files-in-the-right-directory)
- [Globus](#globus)
- [Downloading from the Internet](#downloading-from-the-internet)
- [Retrieving Work Before Access Ends](#retrieving-work-before-access-ends)
- [Inside the Workspace](#inside-the-workspace)
- [Teams and Canvas Groups](#teams-and-canvas-groups)
- [Asking Us to Change Ownership or Permissions](#asking-us-to-change-ownership-or-permissions)
- [Sharing with People Who Have No Cluster Account](#sharing-with-people-who-have-no-cluster-account)
- [Two Limits Worth Stating Plainly](#two-limits-worth-stating-plainly)

## In the Browser

------------------------------------------------------------------------

The JupyterLab file browser uploads with drag and drop and downloads from the
right-click menu. *It is the right tool for a notebook and a CSV, and the wrong
one past about 64 MB or a few dozen files* — transfers stall and there is no
resume. Where the file is large and the browser is the only route available, zip
it, upload the archive and extract it from a terminal.

## Git

------------------------------------------------------------------------

`git` is installed on the login node and in the standard images, and is the best
route for code. Clone at the login node and the working tree is already there when
the container starts; both see the same filesystem.

```bash
git clone https://github.com/<owner>/<repo>.git
```

*A private repository needs a personal access token or an SSH key*, exactly as on
a local machine. A clone counts against quota like any other files. *Git is the
best option for code and notebooks and a poor one for large data.*

## scp, sftp and rsync

------------------------------------------------------------------------

These run from a terminal on a local machine, not from the cluster, and are what
we recommend for most transfers. On Windows, [WinSCP](https://winscp.net/) offers
the same thing with a window.

```bash
scp /local/path <username>@dsmlp-login.ucsd.edu:~/remote/path            # upload
scp <username>@dsmlp-login.ucsd.edu:~/remote/path /local/path            # download
scp -r <username>@dsmlp-login.ucsd.edu:/directory/to/send /local/where   # directory
```

`sftp` gives an interactive session, which is easier when what is where is not
certain; `rsync` is the one to reach for when the transfer will be repeated,
since it sends only what changed:

```bash
sftp <username>@dsmlp-login.ucsd.edu
rsync -avr <directory> <username>@dsmlp-login.ucsd.edu                   # upload
rsync -avr <username>@dsmlp-login.ucsd.edu:<remote-path> <local-path>    # download
```

*Messages about a pod being created and deleted appear around the transfer.* That
is the cluster starting a short-lived container to serve it, and is not an error.

*The VPN is not required for these — they run over `ssh`, which works from
anywhere.* → [Connecting over SSH](../access/the-login-node.md#connecting-over-ssh)

## Landing Files in the Right Directory

------------------------------------------------------------------------

**This is the step that goes wrong.** On an `scp` to `dsmlp-login`, `~` is the
*personal* area — what appears as `private/` inside a container. It is **not** a
course home, and files left there do not appear where a course notebook expects
them. *Copying the login-node home and taking it for the coursework is the
commonest way to discover the omission later.*

To reach a workspace home, take its path from the workspace listing and use that
instead:

```bash
workspace -l     # prints each workspace and the path to its home directory
```

The paths look like `/dsmlp/workspaces-fs0*/<WORKSPACE>/home/<username>`, with
team directories under the same prefix and `/teams` in place of `/home`.
→ [Directories, Quotas & Cleaning Up](your-files-and-quotas.md#where-files-live)

## Globus

------------------------------------------------------------------------

Globus suits large unattended transfers and transfers between institutions. The
supported route is to run **Globus Connect Personal** inside the environment,
making it an endpoint for transfers in either direction. In a terminal there,
fetch and unpack the client and run its setup — the directory it unpacks into is
named for the version downloaded:

```bash
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar -xvzf globusconnectpersonal-latest.tgz
./globusconnectpersonal-<version>/globusconnectpersonal -setup
```

Setup prints a login link. Globus authenticates through CILogon: choose
**University of California-San Diego**, sign in with AD credentials and Duo,
allow the setup tool, and paste the returned code at the `Enter the auth code:`
prompt. Setup also asks for a recognisable endpoint name. Start the endpoint with
`-start &` and check it on the Globus
[Collections](https://app.globus.org/collections?scope=administered-by-me) page
under **Administered By You**: green is running, red is stopped.

**The endpoint runs only while the environment runs.** A red endpoint means
logging back in, launching the environment, and starting it again — *adding the
start command to `.bash_profile` starts it with every terminal opened there.*

## Downloading from the Internet

------------------------------------------------------------------------

`wget` and `curl` are available on the login node and in the container, and are
the simplest way to pull a public dataset straight onto the cluster. **Please
check the size first:** where the data is large and more than one person needs it,
please ask us to stage it once rather than each person keeping a copy.
→ [Shared Datasets](datasets.md)

## Retrieving Work Before Access Ends

------------------------------------------------------------------------

Retrieving work from the platform is not urgent right up until it is impossible.
**The operative date is the day access ends, not the day the files are purged** —
once the environment stops appearing for a member, the work in it can be
retrieved only by asking us.
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md#what-the-end-of-access-does-and-does-not-do)

**The archive provision does not cover a student's own work.** Archiving covers
instructor and course-wide files, on request. **Student home directories are not
archived**, so anything a student wants to keep has to be copied out before
access ends.

What is worth taking:

- **The course home directory** — notebooks, code, results and figures. No copy
  of it is kept anywhere else.
- **`teams/`**, when a project's shared work lives there.
- **`private/`** — it follows a member between workspaces, but see the open
  question in the note above.
- **`public/`** is usually the instructor's course material rather than a
  member's own work. Large shared datasets are generally better re-obtained from
  their source than copied to a laptop.

*None of this requires a running container.* The container and the login node
share a filesystem, so `ssh` to the login node is enough to collect everything.

**If access has already ended, work that is out of reach is not necessarily
gone.** Please contact us rather than assuming it has been lost. Until the
environment is purged, an archived class can be revived and an archive can be
made available for download, and an instructor can request that an individual
account be reactivated to resolve an Incomplete, an academic integrity matter, or
a hand-off. *The earlier the request, the more likely the answer is yes.*

## Inside the Workspace

------------------------------------------------------------------------

**`public/` is the sanctioned way to share with a whole workspace.** Everything in
it is readable by every member. In a course, the shared **grader account** holds
write permission and stages the material; elsewhere the writer is whoever the
workspace was set up around.
→ [The Shared Workspace Area](your-files-and-quotas.md#the-shared-workspace-area)

**Files staged into `public/` sometimes arrive unreadable**, because they carry
the permissions they had wherever they came from. The published repair, run as
the account that owns the directory, is:

```bash
chmod -R u+rwX,go+rXs,go-w ~/public
```

That removes write permission for everyone else while adding the execute bit on
directories so they can be entered. *It is the only permission recipe our
documentation publishes*; for anything beyond it, please ask.

**`teams/` narrows the audience** from the whole workspace to one group — a
capstone group, a project team, a lab bench.

## Teams and Canvas Groups

------------------------------------------------------------------------

**Course teams come from Canvas group sets.** An instructor either creates a
self-sign-up group set and lets students join, or creates the groups and assigns
students to them. Changes reach the cluster within a few hours rather than
immediately.

Two details catch people out:

- **Canvas will only put students in groups.** An instructor or TA cannot be added
  as a member. The route in is the course's **grader account**, which is enrolled
  as a student and joins the group in the same way.
- **Multiple group sets in one Canvas course may not work correctly.** Please use
  one.

From the command line, the team's data is requested at launch:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -G list      # the teams the account belongs to
launch-scipy-ml.sh -W <WORKSPACE> -G <teamid>  # launch with that team's data
```

*Group storage is provisioned separately from personal storage*, and additional
space is requested from us.
→ [Asking for More Space](your-files-and-quotas.md#asking-for-more-space)

## Asking Us to Change Ownership or Permissions

------------------------------------------------------------------------

**File ownership and permission adjustments are a request we handle.** They sit
alongside resource limits and disk quotas in the list of configuration changes the
Service Desk makes, and a ticket is the documented route when files have ended up
owned by the wrong account or unreadable by the people who need them.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

## Sharing with People Who Have No Cluster Account

------------------------------------------------------------------------

**Globus Project Guest Collections** are the campus mechanism for sharing research
data with named collaborators, at UC San Diego or elsewhere, and for publishing it
openly. A PI requests one from Research IT with a short description of the project
and its intended use; the PI is the collection's Access Manager and may delegate
that role.

**What is shared is a directory and everything below it**, and it may be shared
with one named person by institutional identity or email address, with a Globus
group created for the purpose, with every user logged in to Globus, or with the
public anonymously and with no login at all. The rest of the model:

- **Permissions are set on directories, not on files**, and child directories
  inherit from their parent.
- **Read or read-and-write.** *Write includes delete.*
- **Anything shared publicly should live in a directory named for the fact**, with
  write access to it kept narrow.
- **Files can also be handed out over HTTPS**, as links of the form
  `https://<collectionid>.data.globus.org/<path>` that can be embedded elsewhere.
- **Allocations run a year at a time** — initially 500 GB, somewhat expandable —
  and are reviewed for renewal, with priority to collections in active use.
- **A collection cannot change owner.** Where a project passes to a new PI, a new
  collection is created and permissions reassigned.

**For a one-off send to a person**, the Library's
[rdl-share](https://rdl-share.ucsd.edu) service carries up to 500 GB per message
with no limit on the number of messages, encrypts in transit, and can request
files *from* someone as well as send them. *Executable file types are refused.*

## Two Limits Worth Stating Plainly

------------------------------------------------------------------------

**Datahub and DSMLP are not a hosting platform.** They should not be used to run
externally-available services or applications except as required for coursework or
projects. Sharing data is supported; standing up a public service is not.

**Sharing is a classification decision before it is a technical one.** Licensed
data, protected data, and anything under a data use agreement do not become
shareable by being copied into a shared directory.
→ [Restricted & Licensed Datasets](datasets.md#restricted--licensed-datasets)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
