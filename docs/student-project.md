# Projects & Independent Study

------------------------------------------------------------------------

This article describes access to Datahub/DSMLP for work undertaken outside a
scheduled course: eligibility and how to request access, how project access
differs from course access, and where the technical detail is documented.

**This article assumes familiarity with a shell.** Nobody configures a project
environment on the student's behalf and there is no course menu to select from;
what runs, and how, is the project's own decision.

*Enrollment in a course that uses Datahub* is separate access under different
rules — see [Using Datahub in a Course](student-in-a-course.md) or
[Working from the Command Line](working-from-the-command-line.md).

**The mechanics here are the same as on the course pages.** Most of what may be
obtained for a course may be obtained for a project. Rather than repeat that
material, this article covers what *differs* — eligibility, priority, support,
and how long access lasts — and links to the course pages for how things
actually work.

## Eligibility & Requesting Access

------------------------------------------------------------------------

This path covers for-credit and campus-sponsored work outside a scheduled
course:

- **Designated independent study courses** — 198/199, 293/298/299
- **Independent thesis or dissertation research**
- **State-supported capstone projects**
- **Campus-sponsored co-curricular activities** — projects, workshops, clubs,
  teams

Please request access via the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form. *Non-credit
personal projects may be approved on a case-by-case basis as resources are
available.*

**What a request states.** Who is sponsoring the work; what will be run; the
resources required; and for how long. *A request naming a faculty sponsor and a
concrete workload is provisioned considerably faster than one describing "a
machine learning project".*

*For non-students, and for research that is not for credit*,
[Research IT](https://research-it.ucsd.edu/computing/index.html) can help connect
faculty, staff, and student researchers with compute platforms — see also
[Research on DSMLP](individual-researcher.md).

*Self-supporting programs* are welcome here, but UC policy requires us to recover
associated direct and indirect costs. Please contact us to discuss before
planning around it.

## How Project Access Differs from Course Access

------------------------------------------------------------------------

**Priority relative to coursework.** Instruction comes first. When the cluster is
busy — 10th and Finals Weeks, and at major assignment deadlines — coursework is
served ahead of project work. *Demand is generally lower during the day than in
the evening.*

**Support.** We aim to resolve individual user issues within 1-2 business days,
as for any other user. Project work has no instructor or TA as a first tier:
nothing sits between the project and the Service Desk, and nobody there knows the
project. [Error Messages](reference/error-messages.md) and
[Getting Help](reference/getting-help.md) are the places to start.

**Duration.** Project access is granted for a defined period rather than tied to
an instructional term. *Please submit an extension request before access lapses
rather than afterwards.* → [When Access Starts & Ends](access/when-access-starts-and-ends.md)

**No environment is configured in advance.** A course receives an image selected
and tested by its instructor; a project receives the standard images and whatever
is built upon them. → [Environments](environments/README.md)

## Getting Set Up

------------------------------------------------------------------------

1. **Sign in.** Use [datahub.ucsd.edu](https://datahub.ucsd.edu) for the browser
   route, or `ssh` to the login node for a terminal. Duo applies, once every
   8 hours; *the VPN is not required for either route.* → [Access](access/README.md)
2. **Locate the workspace.** Project access is provisioned as its own workspace,
   separate from any course the student is enrolled in, with its own home
   directory. Where both exist, the workspace is selected deliberately at launch.
   → [Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)
3. **Launch something.** `launch-scipy-ml.sh` for the GPU-capable image,
   `launch-datascience.sh` for the CPU image. → [Running Jobs](running-jobs/README.md)
4. **Place data sensibly.** A project home directory is not large. Large inputs
   belong in shared or external storage rather than a per-user copy.
   → [Workspaces & Storage](workspaces-and-storage/README.md)

**The login node is not where work runs.** It exists to launch jobs and move
files. → [The Login Node](access/the-login-node.md)

## Doing the Work

------------------------------------------------------------------------

The procedures are documented on the course pages; what follows is the routing.

| To | Please see |
|---|---|
| Request CPU, memory, or a GPU | [`launch.sh` Reference](running-jobs/launch-sh-reference.md) |
| Run work that outlives the terminal | [Interactive, Background & Batch Modes](running-jobs/job-modes-and-limits.md#the-three-modes) |
| Use `sbatch` and related commands | [Coming from HPC](reference/coming-from-hpc.md#there-is-no-slurm-here) |
| Edit in Visual Studio Code | [Remote Editor Setup](access/remote-editor-setup.md) |
| Install packages, or build an image | [Environments](environments/README.md) |
| Move data in and out | [Moving & Sharing Data](workspaces-and-storage/moving-and-sharing-data.md) |
| Share results with collaborators | [Inside the Workspace](workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace) |

**Launching a GPU session draws on the project's Service Unit budget**, whether
or not the reservation calendar is ever opened; launching an eligible session is
what authorizes that spend. *No TA observes a project's consumption, and there is
no natural point at which anyone remarks that the budget is nearly exhausted.*
→ [On-Demand Leases Charge Budget](gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget) ·
[Reading Your Balance](gpu-access/service-units-and-budgets.md#reading-your-balance)

Two further matters apply to a first long run:

- **An idle GPU session is reclaimed** after roughly 30 minutes of the card doing
  nothing, up to 6 hours when the cluster is quiet, and never within the
  session's first 45 minutes. → [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle)
- **A booked window that is missed is charged**, at up to 50% of the booking. A
  waiver is possible — it is a workspace-manager action — but no TA is watching a
  project calendar to notice and offer one. Cancelling in advance carries no
  penalty beyond the time actually used.
  → [The Claim Window](gpu-access/reservations.md#the-claim-window)

**Please checkpoint anything long-running.**
→ [Checkpointing](running-jobs/checkpointing.md)

## When Things Go Wrong

------------------------------------------------------------------------

This audience has the least support around it: no instructor, no TA, no lab.

| Symptom | Please start at |
|---|---|
| `OOMKilled` | [`launch.sh` Reference](running-jobs/launch-sh-reference.md) — note that requests are half of limits |
| `DeadlineExceeded` | [The Runtime Limit](running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| `0/5 nodes available` | Usually a `gpu-class` label problem → [From Reservation to Running Session](gpu-access/gpu-classes.md#from-reservation-to-running-session) |
| The session ended unexpectedly | [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle), or [What Ends a Session](gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill) |
| Reservation-related events in a pod | [Kubernetes Events](running-jobs/kubernetes.md#reservation-events) |

In a ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu), *please include what
was run, the full error, and the workspace name.*
→ [Getting Help](reference/getting-help.md)

## Outgrowing Project Access

------------------------------------------------------------------------

The indications: capacity is needed beyond what a project allocation carries; the
work has become a lab's rather than one person's; multi-day reservations are
needed; or storage is measured in terabytes.

- Working independently, on an ongoing basis →
  [Research on DSMLP](individual-researcher.md)
- Provisioning for the group belongs with a PI → please refer them to
  [Setting Up a Research Lab](faculty-research-lab.md)
- Genuinely beyond this cluster →
  [Research IT](https://research-it.ucsd.edu/computing/index.html) can discuss
  other platforms

## Caveats & Limitations

------------------------------------------------------------------------

**No Sensitive Data:** DSMLP is not engineered to protect highly-sensitive data
such as clinical records or export-controlled information ("P4") and must not be
used for such purposes. Legally- or contractually-protected information ("P3")
may be permitted after review; note that vetting may take 4-6 weeks or longer.
→ [Policy](reference/policy.md)

**Shared Compute Resources:** resources are shared among all courses and
projects, and instruction has priority. See above.

**Appropriate Use:** The campus-wide
[IT Acceptable Use Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html)
applies, including prohibitions on commercial or political activity.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
