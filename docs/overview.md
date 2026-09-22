# Datahub and DSMLP Overview

This page describes Datahub and DSMLP and names the starting page for each
audience. It also summarizes standard features, platform constraints, support
contacts, and policy.

## Datahub, DSMLP, and the Research Cluster

UC San Diego's Datahub and Data Science & Machine Learning Platform (DSMLP)
provide thousands of undergraduates, graduate students, and their instructors
with access to Jupyter, RStudio, and other computational resources for scheduled
classes, formal independent study, and student projects. The same cluster runs
research work and, in that context, is also called the **Research Cluster**.

The platforms are used in courses ranging from introductory Data Science
lectures to graduate-level applied machine learning, and in curricula in
Biology, Music, Social Sciences, and Public Health. In AY 2025-26, the platforms
hosted more than 140 classes, 75 instructors, and 18,000 student enrollments.

**Datahub** is the web interface, at
[datahub.ucsd.edu](https://datahub.ucsd.edu). **DSMLP** is the cluster that
runs Datahub sessions, and it is also reachable from a terminal. Datahub and
DSMLP are a single service, and the same files are present in both.

## Where to Begin

Each audience has its own starting page.

| Audience | Starting page | Assumes |
|---|---|---|
| A student enrolled in a course that uses Datahub | [Using Datahub in a Course](student-in-a-course.md) | A web browser and nothing else |
| A student in such a course, where the course requires SSH, `launch.sh`, batch jobs, VS Code, or a GPU class the course menu does not offer | [Working from the Command Line](working-from-the-command-line.md) | A terminal and `ssh` |
| Teaching or assisting with a course | [Teaching with Datahub and DSMLP](instructor-or-ta.md) | A browser for most tasks |
| Undertaking a personal project, independent study, capstone, or club or team project | [Projects & Independent Study](student-project.md) | Familiarity with a shell |
| A graduate student, postdoc, undergraduate, or staff researcher working without a lab workspace | [Research on DSMLP](individual-researcher.md) | Familiarity with a shell |
| Faculty arranging access for a research group | [Setting Up a Research Lab](faculty-research-lab.md) | Some steps are performed by ITS staff |

Coursework and a personal project are two separate workspaces, with different
eligibility, different resources, and different access lifetimes. Coursework is
covered in [Using Datahub in a Course](student-in-a-course.md) and
[Working from the Command Line](working-from-the-command-line.md), and a
personal project in [Projects & Independent Study](student-project.md).

## Workspaces

Users are divided into groups called **workspaces**: one per course, one per
lab, or one general catch-all population. A workspace anchors all cluster
configuration: rosters, storage, container images, GPU access, and storage and
GPU quotas, as described in
[What a Workspace Is and What It Controls](workspaces-and-storage/what-a-workspace-is.md).

A member may belong to several workspaces at once, for example as a TA for one
course, a student in another, and a member of a lab, and chooses the workspace
to work in at launch. A member of more than one workspace has a home directory
in each, as described in
[Belonging to Several Workspaces](workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces).

See also: [Workspaces & Storage](workspaces-and-storage/README.md)

## Standard Features

### Job Environment

All jobs, whether browser-based Jupyter sessions, command-line jobs, or batch
jobs, run in a compute environment derived from the member's account and
workspace together with any job-specific configuration. A course session in the
browser typically begins at 2 CPU cores and 4GB RAM, as described in
[The Browser Session](access/datahub-in-the-browser.md#the-browser-session).
Upper limits are based on class size, demand, and capacity.

### GPUs

GPUs are organized into five classes by size rather than by hardware model.
Each workspace is given access to one or more classes, matching its anticipated
work. The classes are listed in
[GPU Class Sizes](gpu-access/gpu-classes.md#gpu-class-sizes).

### Storage

Each member has a per-user, per-workspace home directory; a shared area readable
by everyone in the workspace; and a per-user, cluster-wide private area
available in every workspace. The directories are listed in
[Where Files Live](workspaces-and-storage/your-files-and-quotas.md#where-files-live),
and the quotas for course and research home directories in
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).
Optional mounts of external storage are available, as described in
[Mounting External Storage](workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage).

### Standard Software Images

Curated images cover the widely used Python, R, and Julia data analysis stacks.
They include a CUDA/GPU-enabled image with TensorFlow and PyTorch, and an
RStudio image. Courses and labs may further customize or pin their own images.
The images are described in
[Standard Images, Tags, and Pinning](environments/standard-images.md).

### Ways to Work

Work is done in a browser, at a terminal over SSH, or in a desktop editor such
as VS Code connected to a cluster container. Each route is described in
[Access](access/README.md).

## GPU Reservations

From Fall 2026, access to GPUs is managed by a reservation system. A booking,
made through a web interface, holds capacity for a specific window, and for the
length of that window sessions are admitted ahead of the walk-up queue. Ad-hoc,
on-demand use without a booking is also supported. Booking is described
in [Reservations](gpu-access/reservations.md). Reservations, per-group quotas,
and Service Unit budgets are the mechanisms that manage contention for GPUs, as
described in [GPU Access](gpu-access/README.md).

> [!WARNING]
> An on-demand launch draws on the Service Unit budget as a booked window does,
> and launching an eligible session authorizes that spend. See
> [On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

## Platform Constraints

### Root Access

Containers run unprivileged, under the member's own UID, with no root or sudo
inside the container, as described in
[Root Access and System Packages](environments/customizing-your-environment.md#root-access-and-system-packages).
`sudo apt-get install` fails by design, and the failure is not a fault to
report.

### Computation on the Login Node

The login node is for launching jobs and moving files, and running computation
on it is prohibited, as described in
[What the Login Node Is For](access/the-login-node.md#what-the-login-node-is-for).

### Idle GPU Sessions

An idle GPU session still holds its GPU, and the session is reclaimed once it
has been idle long enough, as described in
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).

## Support

Questions and feedback go to the contact for the topic.

| Topic | Contact |
|---|---|
| A course a student is enrolled in | The instructor or TA, first |
| Datahub or DSMLP itself | [datahub@ucsd.edu](mailto:datahub@ucsd.edu), or the [ITS Service Desk](https://support.ucsd.edu/) |
| The Research Cluster, or Universal Scale Storage | [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) |
| Which platform is appropriate for a research project | [Research IT](https://research-it.ucsd.edu/computing/index.html) |
| 1:1 Consultation, for instructors, TAs, and Technical Points of Contact (TPOCs) | [ucsd-datahub.youcanbook.me](https://ucsd-datahub.youcanbook.me/) |

Urgent or broadly scoped problems may be escalated through the ITS Service
Desk. A ticket for such a problem states what is affected and how many people,
as described in
[Incidents Affecting More Than One Person](reference/getting-help.md#incidents-affecting-more-than-one-person).
ITS response targets are given in
[Response Targets](reference/getting-help.md#response-targets), the terms of
1:1 Consultation in
[Support & Technical Consultation](instructor-or-ta.md#support--technical-consultation),
and all support routes in [Getting Help](reference/getting-help.md).

## Policy

Conditions of use are set out in [Policy](reference/policy.md).

- Highly sensitive data (P4), such as clinical records or export-controlled
  information, must not be used on Datahub or DSMLP, and legally or
  contractually protected information (P3) may be permitted after review, as
  described in [Data Classification](reference/policy.md#data-classification).
- Datahub and DSMLP system resources are shared among all courses and research
  groups, and demand, in particular for GPUs, may exceed capacity at peak hours
  during 10th and Finals Weeks or at assignment deadlines, as described in
  [Use of Shared Resources](reference/policy.md#use-of-shared-resources).
- Datahub may be unavailable during scheduled maintenance for time-sensitive
  updates or security patches, on the schedule given in
  [Scheduled Maintenance](reference/policy.md#scheduled-maintenance).
- Datahub and DSMLP are not to be used to host externally available services or
  applications except as required for coursework or projects, as described in
  [Hosting Externally Available Services](reference/policy.md#hosting-externally-available-services)
  and [Availability and Reliability](reference/policy.md#availability-and-reliability).
- The campus-wide IT policy on acceptable use applies to Datahub and DSMLP, as
  described in [Appropriate Use](reference/policy.md#appropriate-use).
