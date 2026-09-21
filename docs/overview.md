# Datahub & DSMLP: Overview

------------------------------------------------------------------------

UC San Diego's **Datahub** and **Data Science & Machine Learning Platform
(DSMLP)** provide thousands of undergraduates, graduate students, and their
instructors with access to Jupyter, RStudio, and other advanced computational
resources for scheduled classes, formal independent study, and student projects.
The same cluster carries research work, where it is also referred to as the
**Research Cluster**.

The platforms are used in courses ranging from introductory Data Science
lectures, to graduate-level applied machine-learning, to curricula in Biology,
Music, Social Sciences, and Public Health. Over AY 2025-26, more than 140
classes, 75 instructors, and 18,000 student enrollments were hosted.

**Datahub** is the web interface, at
[datahub.ucsd.edu](https://datahub.ucsd.edu). **DSMLP** is the cluster beneath
it, and is also reachable from a terminal. They are not separate services, and
the same files are present in both.

Please reach out to our team with any questions or feedback.

- Email: [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
- 1:1 Consultation (instructors, TAs, and Technical Points of Contact):
  <https://ucsd-datahub.youcanbook.me/>

## Changing in Fall 2026: GPU Reservations

------------------------------------------------------------------------

From Fall 2026, access to GPUs is managed by a **reservation system**. A web
interface books a specific window — *"Tuesday 9am-7pm, 4× X-Large"* — and for the
length of that window the capacity is held and sessions are admitted ahead of the
walk-up queue. Ad-hoc, on-demand use continues to be supported.

**On-demand launches draw on the Service Unit budget exactly as a booked window
would.** Launching an eligible session is what authorizes that spend. Anyone
using GPUs at all should read
[On-Demand Leases Charge Budget](gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)
before the first launch of the term.

## Where to Begin

------------------------------------------------------------------------

| Audience | Please see | Which assumes |
|---|---|---|
| A student enrolled in a course that uses Datahub | **[Using Datahub in a Course](student-in-a-course.md)** | A web browser and nothing else |
| That same student, where the course requires SSH, `launch.sh`, batch jobs, VS Code, or a GPU class the course menu does not offer | **[Working from the Command Line](working-from-the-command-line.md)** | A terminal and `ssh` |
| Teaching or assisting with a course | **[Teaching with Datahub & DSMLP](instructor-or-ta.md)** | A browser for most tasks |
| Undertaking a personal project, independent study, capstone, or club or team project | **[Projects & Independent Study](student-project.md)** | Familiarity with a shell |
| A graduate student, postdoc, undergraduate, or staff researcher working without a lab workspace | **[Research on DSMLP](individual-researcher.md)** | Familiarity with a shell |
| Faculty arranging access for a research group | **[Setting Up a Research Lab](faculty-research-lab.md)** | Some steps are performed by our staff |

*Coursework and a personal project are two separate workspaces*, with different
eligibility, different resources, and different access lifetimes. Please read the
course pages for coursework and the project page for the project.

## Workspaces

------------------------------------------------------------------------

Users are divided into groups called **workspaces**: one per course, lab, or
general catch-all population. Workspaces anchor all cluster configuration:
rosters, storage, container images, GPU access, and storage and GPU quotas.

A member may belong to several workspaces at once — a TA for one course, a
student in another, a member of a lab — and picks the context to work in at
launch time. A member of more than one workspace has a home directory in each.
→ [Workspaces & Storage](workspaces-and-storage/README.md)

## Standard Features

------------------------------------------------------------------------

**Job environment.** All jobs, whether web/Jupyter, CLI, or batch, present a
compute environment derived from the member's account and workspace context
together with any job-specific configuration. Course sessions typically begin at
2 CPU cores and 4GB RAM; upper limits are based on class size, demand, and
capacity.

**GPUs**, organized into five classes by size rather than by hardware model, from
approximately 6GB to approximately 96GB. Each workspace is given access to one or
more classes, matching anticipated work.
→ [GPU Classes](gpu-access/gpu-classes.md)

**Storage.** A per-user, per-workspace home directory; a shared area readable by
everyone in the workspace; and a per-user, cluster-wide private area available
in every workspace. Course home directories are typically 5-10GB; research
accounts are substantially larger. Optional mounts of external storage are
available.
→ [Directories, Quotas & Cleaning Up](workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Standard Software Images** — curated environments covering the widely-used
Python, R, and Julia data analysis stacks, a CUDA/GPU-enabled image with
TensorFlow and PyTorch, and an RStudio image. Courses and labs may further
customize or pin their own.
→ [Standard Images](environments/standard-images.md)

**Three ways to work**: in a browser, at a terminal over SSH, or with a desktop
editor such as VS Code connected to a cluster container.
→ [Access](access/README.md)

## Three Things Worth Knowing Early

------------------------------------------------------------------------

**Containers run unprivileged**, under the member's own UID, with no root or sudo
inside the container. `sudo apt-get install` will not work; this is by design and
is not a fault to report. → [The Hard Boundary](environments/customizing-your-environment.md#the-hard-boundary)

**The login node is not for computing.** It exists to launch jobs and move files.
→ [The Login Node](access/the-login-node.md)

**An idle GPU session still holds its GPU**, and is reclaimed once it has been
idle long enough.
→ [Idle Culling](gpu-access/what-ends-a-session.md#what-counts-as-idle)

## Support

------------------------------------------------------------------------

| Topic | Please contact |
|---|---|
| A course a student is enrolled in | The instructor or TA, first |
| Datahub or DSMLP itself | [datahub@ucsd.edu](mailto:datahub@ucsd.edu), or the [IT Service Desk](https://support.ucsd.edu/) |
| The Research Cluster, or Universal Scale Storage | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| Which platform is appropriate for a research project | [Research IT](https://research-it.ucsd.edu/computing/index.html) |

We aim to resolve individual user issues within **1-2 business days**. Urgent or
broadly-scoped problems may be escalated through the IT Service Desk; *a ticket
should say plainly what is affected and how many people.*
→ [Getting Help](reference/getting-help.md)

## Caveats & Limitations

------------------------------------------------------------------------

**No Sensitive Data:** Datahub is not engineered to protect highly-sensitive data
such as clinical records or export-controlled information ("P4" per
[University of California classification levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html))
and must not be used for such purposes. Legally- or contractually-protected
information ("P3") may be permitted after review; note that depending on the
nature of the data, vetting may take 4-6 weeks or longer.
→ [Policy](reference/policy.md)

**Shared Compute Resources:** Datahub and DSMLP system resources are shared among
all courses and research groups. Demand for resources, in particular for GPUs,
may exceed capacity at peak hours during 10th and Finals Weeks or at assignment
deadlines. From Fall 2026, reservations, per-group quotas and Service Unit
budgets are the mechanisms by which that contention is managed.
→ [GPU Access](gpu-access/README.md)

**Scheduled Maintenance:** Datahub may be unavailable Tuesdays, 6-8AM for
installation of time-sensitive updates or security patches. *In practice this
work is usually limited to a subset of worker nodes, in which case running jobs
are unaffected.* Infrequent 'Critical' updates may require downtime outside of
this timeframe.

**Availability and Reliability:** Datahub and DSMLP were designed with student
workloads in mind, deliberately trading some of the costly redundancy typical of
financial or health settings for additional capacity and capability. As such,
they should not be used to host externally-available services or applications
except as required for coursework or projects. *(This caveat applies primarily to
the compute nodes executing user jobs; critical components such as networking,
file storage, and backups are maintained to Enterprise IT standards.)*

**Appropriate Use:** The campus-wide
[IT Acceptable Use Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html)
applies to use of Datahub and DSMLP, including prohibitions on commercial or
political activity, hacking or cyberstalking, and other types of unwelcome
behavior.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
