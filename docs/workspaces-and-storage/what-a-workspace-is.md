# What a Workspace Is and What It Controls

Users are divided into **workspaces**: one per course, one per lab, or one
catch-all population such as "Campus Researcher". A workspace anchors the
roster, the storage, the container images on offer, the GPU classes that may be
requested, and the quotas and budgets its members draw against.

## What One Workspace Covers

| Workspace | Covers |
|---|---|
| Course | The whole course: its lecture timeslots and the discussion sections associated with them |
| Lab or research | A research group |
| Catch-all | A population that has no course or lab of its own |

A course is not split across several workspaces, and a discussion section does
not have a workspace of its own. Access that only some students in a course
need, such as a mentor's dataset for one section or a project group's shared
files, is given through teams inside the single course workspace, as described
in [Sections, Teams and Group Data](#sections-teams-and-group-data).

## What the Workspace Controls

| Resource | How the workspace governs it |
|---|---|
| Roster | Course rosters auto-populate from TSS (formerly TritonLink) and Canvas. Lab and research workspace rosters are curated by Research IT Services and have the potential to auto-populate from departmental staff affiliation. |
| Storage | Home directories are per-user and per-workspace. The workspace also holds its shared `public/` area and any `teams/` directories. Home directory quotas are listed in [Workspace and Personal Quotas](your-files-and-quotas.md#workspace-and-personal-quotas). |
| Container images | Each workspace defines one or more Jupyter configurations, each an image plus CPU, RAM, and GPU quantities, and members pick one from a menu. For example, a course might offer a CPU-only environment for most of the quarter and a 1-GPU environment for its projects. |
| GPU class access | Each workspace is granted access to one or more [GPU Classes](../gpu-access/gpu-classes.md) matching the work it was provisioned for. A request for a class the workspace was not granted is refused. |
| Quotas and budgets | Group quotas cap how much of each GPU class the workspace can hold at once. Per-workspace Service Unit budgets divide that capacity between its members: weekly for courses, monthly or quarterly for research. |

The resources in this table stop at the workspace boundary. The `private/`
directory is the exception: it is per-user and cluster-wide, and it appears in
every workspace an account belongs to. Directory scopes are listed in
[Where Files Live](your-files-and-quotas.md#where-files-live).

## Workspace Provisioning

Course workspaces are provisioned from a course request. The submission
deadline is listed in
[Course Timeline](../instructor-or-ta.md#course-timeline).
A quarterly survey asks instructors and TAs about assignment scope, GPU sizes,
and deadlines. From the answers, ITS provisions the workspace, its Datahub
environments, and its GPU class access before the quarter starts. The course
staff timeline is described in
[Instructors, TAs & Course Staff](../access/when-access-starts-and-ends.md#instructors-tas--course-staff).

Research IT Services curates lab and research workspaces manually rather than
generating them from a roster.

### Image Pinning

A workspace may **pin** a container image. Pinning keeps the workspace's
members from being moved by a quarterly image update mid-quarter. The request
is described in
[Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace).

## Who Manages a Workspace

A workspace's **members** are its students or lab members. Its **workspace
managers** are its instructors, TAs, or PI. A workspace manager may view the
group calendar, book on a member's behalf, and waive a cancellation charge. A
workspace manager may not edit Service Unit budgets or group limits, but may
request a change by ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu). The
privilege tiers are described in
[Managing a Group](../reference/managing-a-group.md).

## Belonging to Several Workspaces

An account can belong to several workspaces at once, for example as a TA in one
course, a student in another, and a member of a lab. Each workspace is a
separate context with its own files, as described in
[Per-Workspace Home Directories](#per-workspace-home-directories).

The workspace a session runs in is chosen at every launch. In the browser, it is
chosen from the environment list
([Choosing a Workspace in the Browser](#choosing-a-workspace-in-the-browser)).
On the command line, it is named with `-W`
([Naming a Workspace on the Command Line](#naming-a-workspace-on-the-command-line)).

## Per-Workspace Home Directories

Home directories are per-user and per-workspace. A file saved while working in
one course is not visible from another course's environment or from a lab
environment.

Two locations follow an account across every workspace:

- `private/` is per-user and cluster-wide. It appears in every workspace the
  account belongs to, and it draws on the personal quota rather than the
  workspace's. A file needed in every environment belongs in `private/`.
- The login-node home directory is personal and is not a course home. Files
  placed there by `scp` are not in a course home until they are moved.

`public/` and `teams/` belong to the workspace and count against its quota.
Directory locations and quotas are listed in
[Where Files Live](your-files-and-quotas.md#where-files-live).

## Choosing a Workspace in the Browser

Signing in at `datahub.ucsd.edu` leads to a page listing the environments the
account is entitled to, each named for the course it belongs to. A course that
is not listed may be an enrollment change that has not yet propagated, as
described in [Missing Workspaces](#missing-workspaces).

### Courses with Several Environments

Some courses offer more than one environment, commonly a CPU-only configuration
for ordinary work and a GPU configuration for projects. Which environment to use
is a course decision. Ask the instructor or TA which one to use.

### Datahub Session Limit

A member may run one Datahub session at a time, and starting another means
stopping the first. Shell, VS Code, and batch jobs are not subject to this
limit, in this workspace or another
([Concurrent Datahub Sessions](../access/datahub-in-the-browser.md#concurrent-datahub-sessions)).

## Naming a Workspace on the Command Line

From the login node, name the workspace with `-W`:

```bash
launch-scipy-ml.sh -W <workspace-id>
```

### Launching Without `-W`

A launch without `-W` selects no course and starts in the personal home
directory. This suits independent study and research work, but not work on a
course's files.

### Listing Workspace IDs

The available IDs come from the listing command:

```bash
workspace --list
```

The listing prints each workspace the account belongs to alongside the full path
to its home directory inside that workspace. The listing may include courses
that have ended. The disk-quota-service page under **Services** on
`datahub.ucsd.edu` also displays the ID.

### Workspace IDs and Paths

Do not construct a workspace ID or a workspace path by hand. Both are printed by
`workspace --list`. Workspace filesystem paths are not predictable from the
workspace name, they differ between workspaces, and a workspace directory may be
invisible until it is entered with `cd`.

Older articles show worked examples with an ID built from a subject code, a
term, and a section suffix. Those examples illustrate the flag and are not a
method for deriving an ID.

## Sections, Teams and Group Data

Section-specific and group-specific files in a course workspace are handled
within that workspace by teams:

```bash
launch-scipy-ml.sh -W <workspace-id> -G list
launch-scipy-ml.sh -W <workspace-id> -G <teamid>
```

`-G list` prints the teams the account belongs to. `-G <teamid>` launches with
that team's data visible under `teams/`. The `teams/` directory is described in
[Team Directories](your-files-and-quotas.md#team-directories).

> [!NOTE]
> `-g` is the GPU count and `-G` is the group flag: `-g 1` asks for one GPU, and
> `-G 1` is read as a team ID
> ([Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags)).

## Missing Workspaces

### Pending Roster Updates

A course that does not appear may still be waiting on a roster update. An
enrolled course that is missing is not a fault until the roster timing listed in
[Students Enrolled in a Course](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course)
has passed. Auditors and observers are not on the TSS roster and are added
through Canvas by the instructor or TA.

### Ended Courses

A course that has disappeared, rather than never appeared, has most likely
reached the end of its retention period, as described in
[One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter).
Copying work out is described in
[Retrieving Work Before Access Ends](moving-and-sharing-data.md#retrieving-work-before-access-ends).
