# What a Workspace Is and What It Controls

Almost everything the cluster knows about a piece of work, it knows through a
**workspace**. Users are divided into workspaces — one per course, one per lab,
or one catch-all population (e.g. "Campus Researcher") — and the workspace
anchors the roster, the storage, the container images on offer, the GPU classes
that may be requested, and the quotas and budgets drawn against.

Students rarely meet the concept directly: signing in and picking a course
brings up the right environment. It matters the moment something is missing,
since in practice everything that can be missing is attached to a workspace.

## What One Workspace Covers

------------------------------------------------------------------------

**A course workspace covers the whole course** — its lecture timeslots together
with the discussion sections associated with them. A course is not split across
several workspaces, and a discussion section does not get one of its own.

*Where a course does need to give some students access that others do not
have — a mentor's dataset for one section, a project group's shared files — that
is done with **teams** inside the single course workspace, not with a second
workspace.* → [Sections, Teams and Group Data](#sections-teams-and-group-data)

**A lab or research workspace** covers a research group, and **a catch-all
workspace** covers a population that has no course or lab of its own.

## What the Workspace Controls

------------------------------------------------------------------------

| The workspace anchors | What that means in practice |
|---|---|
| **The roster** | Course rosters auto-populate from TSS (formerly TritonLink) and Canvas. Lab and research workspaces are curated by Research IT Services, with the potential to auto-populate from departmental staff affiliation. |
| **Storage** | Home directories are per-user *and* per-workspace, along with the workspace's shared `public/` area and any `teams/` directories. Course homes run 5-10 GB depending on class size; research homes are on the order of 100 GB. |
| **Container images** | Each workspace defines one or more Jupyter configurations — an image plus CPU, RAM and GPU quantities — and members pick one from a menu. A course might offer a CPU-only environment for most of the quarter and a 1-GPU environment for its projects. |
| **GPU class access** | Each workspace is granted access to one or more [GPU classes](../gpu-access/gpu-classes.md) matching the work it was provisioned for. Requesting a class the workspace was not granted is refused. |
| **Quotas and budgets** | Group quotas cap how much of each GPU class the workspace can hold at once, and per-workspace Service Unit budgets divide that between its members — weekly for courses, monthly or quarterly for research. |

**The `private/` directory is the exception.** It is per-user and cluster-wide,
and it appears in every workspace an account belongs to. Everything else in the
table above stops at the workspace boundary.
→ [Directories, Quotas & Cleaning Up](your-files-and-quotas.md#where-files-live)

## How a Workspace Comes Into Being

------------------------------------------------------------------------

**Course workspaces are provisioned from a course request**, submitted at least
4 weeks before instruction begins. A quarterly survey asks instructors and TAs
about assignment scope, GPU sizes and deadlines; from those answers we provision
the workspace, its Datahub environments and its GPU class access before the
quarter starts.
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md#instructors-tas--course-staff)

**Lab and research workspaces are curated manually** by Research IT Services
rather than generated from a roster.

A workspace may also **pin** a container image, so that its members are not
moved by a quarterly image update mid-quarter.
→ [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace)

## Who Manages a Workspace

------------------------------------------------------------------------

A workspace's **members** are its students or lab members. Its **managers** are
its instructors, TAs or PI. A manager may view the group calendar, book on a
member's behalf, and waive a cancellation charge; a manager may **not** edit
Service Unit budgets or group limits, though they may request a change by ticket
to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).
→ [Managing a Group](../reference/managing-a-group.md)

## Belonging to Several Workspaces

------------------------------------------------------------------------

An account can belong to several workspaces at once — a TA for one course, a
student in another, a member of a lab — and each is a separate context with its
own files. **Which context a session runs in is chosen at launch, every time.**

## More Than One Home Directory

------------------------------------------------------------------------

**Home directories are per-user *and* per-workspace.** A file saved while
working in one course is not visible from another course's environment, and not
visible from a lab environment either.

Two things follow an account everywhere:

- **`private/`** is per-user and cluster-wide. It appears in every workspace the
  account belongs to, and it draws on the personal quota rather than the
  workspace's. *A file needed in every environment goes here.*
- **The login-node home directory** is personal, not a course's. Files placed
  there by `scp` are not in a course home until they are moved.

`public/` and `teams/` belong to the workspace and count against its quota.
→ [Directories and What Each Is For](your-files-and-quotas.md#where-files-live)

## Choosing a Workspace in the Browser

------------------------------------------------------------------------

Signing in at `datahub.ucsd.edu` leads to a page listing the environments the
account is entitled to, named for the course they belong to.

**Some courses offer more than one environment** — commonly a CPU-only
configuration for ordinary work and a GPU configuration for projects. Which to
use is a course decision; students should ask the instructor or TA rather than
guessing. *A course that is not listed at all may be an enrollment change that
has not propagated yet.*
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course)

**One Datahub session at a time.** A member may run one Datahub session, and
starting another means stopping the first. *That limit is on Datahub alone — it
does not stop a shell, VS Code or batch job from running at the same time, in
this workspace or another.*
→ [One Datahub Session](../access/datahub-in-the-browser.md#one-datahub-session)

## Naming a Workspace on the Command Line

------------------------------------------------------------------------

From the login node, name the workspace with `-W`:

```bash
launch-scipy-ml.sh -W <workspace-id>
```

**Omitting `-W` selects no course** — the launch lands in the personal home
directory instead, which suits independent study and research work but not work
on a course's files.

The available IDs come from the listing command:

```bash
workspace --list
```

The listing prints each workspace the account belongs to alongside the full path
to its home directory inside that workspace. *Note that it may include courses
that have ended.* The disk-quota-service page under **Services** on
`datahub.ucsd.edu` also displays the ID.

**The ID is not something to construct by hand, and neither is the path.**
Workspace filesystem paths are not predictable from the workspace name, they
differ between workspaces, and the directory may be invisible until it is entered
with `cd`. *Older articles show worked examples with an ID built from a subject
code, a term and a section suffix; those are illustrative of the flag, not a way
to derive an ID.*

## Sections, Teams and Group Data

------------------------------------------------------------------------

A workspace covers a whole course, so section-specific or group-specific files
are handled *within* it, by teams:

```bash
launch-scipy-ml.sh -W <workspace-id> -G list
launch-scipy-ml.sh -W <workspace-id> -G <teamid>
```

`-G list` prints the teams the account belongs to; `-G <teamid>` launches with
that team's data visible under `teams/`.

**`-g` is GPUs and `-G` is groups.** They are one keystroke apart and do
entirely different things: `-g 1` asks for one GPU, `-G 1` will be read as a
team ID.

→ [Team Directories](your-files-and-quotas.md#team-directories)

## When a Workspace Is Missing

------------------------------------------------------------------------

A course that does not appear may still be waiting on a roster update. Rosters
are loaded one business day before the term starts, and a TSS change is reflected
by 10am the day following the change — so an enrolled course is not a fault until
that time has passed. Auditors and observers are not on the TSS roster at all and
are added through Canvas by the instructor or TA.
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md)

A course that has *disappeared* rather than never appeared has most likely
reached the end of its retention period.
→ [One Additional Quarter](../access/when-access-starts-and-ends.md#one-additional-quarter) ·
[Retrieving Work](moving-and-sharing-data.md#retrieving-work-before-access-ends)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
