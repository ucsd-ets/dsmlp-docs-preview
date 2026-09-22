# Teaching with Datahub and DSMLP

This page is for instructors and TAs teaching a course on Datahub and DSMLP. It
covers the course request timeline, standard features and customization,
support and technical consultation, and GPU access for a course. Most tasks
require only a browser, and course-specific customization requires a shell.

## Course Timeline

### Requesting a Course

Instructors, TAs, and departmental staff request Datahub and DSMLP access for a
course through the
[Specialized Instructional Computing Course Request](https://support.ucsd.edu/its?id=sc_cat_item_guide&sys_id=dc1afcd51b152910484f968f034bcb8b&sysparm_category=90e152651b19a910484f968f034bcbf0)
form. Submission opens in the 2nd week of the previous term. For Summer and Fall
classes, submission opens in the 2nd week of Spring.

Requests must be submitted 4 weeks before the start of instruction, including
the designation of a Technical Point of Contact (TPOC) where one is required, as
described in [Technical Point of Contact](#technical-point-of-contact). Late
requests receive lower priority and are reviewed as time permits. Setup and
availability to students depend on the complexity of the course and the overall
request load, and for a late request students may not gain access until as late
as 4th week.

### Course Setup and Instructor Access

Course setup and instructor access open 4-5 weeks before the start of
instruction. Earlier setup is available on request. During this period the
instructor, TAs, and other course staff test features, validate assignments, and
make customizations. Availability of 1:1 Consultation for customization is
limited in the final weeks of each term, as described in
[1:1 Consultation](#11-consultation).

### Student Access

Student access follows TSS course rosters. TSS is the system formerly called
TritonLink. Roster loading and the timing of add and drop changes are given in
[Students Enrolled in a Course](access/when-access-starts-and-ends.md#students-enrolled-in-a-course).
Auditors and observers are not on the roster, and their access is
[managed through Canvas](https://support.ucsd.edu/services?id=kb_article_view&sysparm_article=KB0032124).
[Concurrent Enrollment](https://extendedstudies.ucsd.edu/student-resources/registration-policies-and-procedures/concurrent-enrollment)
students receive access through Extended Studies staff.

### Access After the Term

Instructors and students retain access for one additional quarter beyond the
instructional term, ignoring Summer for Spring courses, as described in
[One Additional Quarter](access/when-access-starts-and-ends.md#one-additional-quarter).
Instructors may request that individual accounts remain active longer for
Incomplete grade resolution, academic integrity proceedings, course development
or hand-off, or similar circumstances, as described in
[Extending Access for an Individual](access/when-access-starts-and-ends.md#extending-access-for-an-individual).

Course environments are purged one quarter after account deactivation, that is,
two quarters after the course, excluding Summer. Two things are excluded from
the purge: individual accounts extended on request, and instructor and
course-wide files archived on request. Archiving, reviving a previously
archived class environment, and making an archive available for download are
requests to ITS, described in
[Archiving on Request](access/when-access-starts-and-ends.md#archiving-on-request).

### Independent Study and Research

For-credit independent study, capstones, and similar student projects request
ongoing access through the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form. Direct those
students to [Projects & Independent Study](student-project.md).
[Research IT](https://research-it.ucsd.edu/computing/index.html) connects
faculty, staff, and student researchers with compute platforms for non-credit
research.

## Standard Features & Standard Software Images

Datahub offers a set of curated software environments that are sufficient for
many courses and use cases. These environments, with the session resources,
course file distribution, grading tools, and individual customization support
that accompany them, are the **standard features**. Questions, configuration
assistance, malfunctions, and errors relating to standard features receive
priority support from IT Services through the routes in
[Support & Technical Consultation](#support--technical-consultation).

### Standard Software Images

The standard software images are accessible through web-based Jupyter notebooks
and from the command line. They are described in
[Standard Images](environments/standard-images.md#standard-images).
The `rstudio-notebook` image derives from `datascience-notebook` and is not
GPU-enabled.

### Session Resources

CPU, memory, and NVIDIA GPU allocations are flexible, beginning at 2 CPU cores
and 4GB RAM dedicated to each student session, as described in
[The Browser Session](access/datahub-in-the-browser.md#the-browser-session).
Upper limits are based on class size, demand, and capacity.

### Course Files and Storage

Course-specific file and dataset distribution is available, with the size
limits given in
[Asking for a Dataset to Be Staged](workspaces-and-storage/datasets.md#asking-for-a-dataset-to-be-staged).
Per-student storage allocations are given in
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas),
and course storage generally in
[Workspaces & Storage](workspaces-and-storage/README.md). Inform ITS where
assignments generate significant per-student output.

### Grading Tools

Tools for assignment distribution, collection, and grading, including roster
integration with Canvas, are described in [Grading](grading/README.md).

> [!NOTE]
> Grade export to Canvas is performed manually. The workflow generates a CSV
> file, which the instructor or TA uploads to the Canvas gradebook, as described
> in [Exporting the Grades](grading/notebook-grading-workflow.md#exporting-the-grades).

### Individual Customizations

Minor per-individual customizations within the standard software images receive
limited support, as described in
[Customizing an Environment](environments/customizing-your-environment.md).

## Course-Specific Customization

Instructors may supplement the standard software images by adding language
modules (for example, Python or R libraries), adding system-level packages
(compilers, utilities, and similar), or making more extensive modifications to
meet the needs of a course. The procedure is described in
[Building & Publishing a Custom Image](environments/building-a-custom-image.md).

Highly complex use cases, such as those incorporating clustered services such as
Spark or Postgres, or software not derived from the standard images, are
regularly used within Datahub and DSMLP. They require substantially more time
and expertise from the instructor or TPOC than ordinary customizations, as
described in
[Complex Customizations & Experimental Features](#complex-customizations--experimental-features).

### Technical Point of Contact

The instructor, a designated **Technical Point of Contact** (TPOC), or both
must take the lead in the installation, configuration, and student use of
course-specific features. ITS technical staff support customization through
[1:1 Consultation](#11-consultation).

The instructor or TPOC is expected to have basic familiarity with Unix commands
such as `ssh`, `mkdir`, and `chmod`, and to be proficient with the intended core
platform (for example, Python or R) in a desktop Mac or PC setting. ITS provides
guidance and basic training on the Datahub and DSMLP environment and on
system-specific procedures.

### Pinning an Image

A course may pin a specific image so that students are not moved by a quarterly
update partway through a project, as described in
[Pinning a Workspace](environments/standard-images.md#pinning-a-workspace).

## Support & Technical Consultation

IT Services provides prioritized support for standard features and
functionality through the [Datahub & DSMLP Documentation](README.md), the IT
Service Desk, and 1:1 Consultation. Questions and feedback about Datahub and
DSMLP go to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

### IT Service Desk

The [IT Service Desk](https://support.ucsd.edu/) is reached by phone, web, or
email for the following.

| Category | Examples |
|---|---|
| Outages, errors, or malfunctions | System issues, such as the service or its components being unavailable; user access issues, such as an enrolled student being unable to log in; errors or unexpected behavior within standard features |
| Requests and inquiries | Requests for system-side configuration or adjustments to course setup, such as resource limits, disk quotas, container tags, and file ownership or permissions; straightforward questions about core features, system capabilities, or clarification of documentation |

Effort is prioritized by the number of courses and students affected and the
overall impact on instruction. Note in the ticket where an issue affects a whole
class or falls on an exam. Students route functionality concerns through their
instructor or TA. In-depth questions go to [1:1 Consultation](#11-consultation).

Response targets, including the incident tier for instructors, are given in
[Response Targets](reference/getting-help.md#response-targets). Urgent problems
arising outside business hours may be escalated through the Service Desk.

### 1:1 Consultation

[1:1 Consultation appointments](https://ucsd-datahub.youcanbook.me/) connect
instructors, TAs, and TPOCs with ITS technical experts for real-time guidance or
assistance on standard features, course-specific customizations, and complex or
experimental features. Topics include:

- In-depth questions about the configuration or usage of standard and core
  features
- Discussion not well suited to ticket-based interaction
- Functional or technical issues outside the standard and core features
- First-time use of a custom container derived from a standard software image
- Customization options and the selection of additional packages and tools
- Functional or technical issues with course-specific features, such as build
  errors and version conflicts
- Questions and training on the customization process, such as the use of git,
  GitHub, tags, and Actions, or the installation of language and system packages
- Maintenance following quarterly updates to the standard software images

At Spring 2026 staffing levels, each course may request up to 6 hours of 1:1
Consultation per term. Availability is reduced in the final weeks of each term.

## Complex Customizations & Experimental Features

The compute clusters underlying Datahub and DSMLP can host complex or novel
customizations that fall outside the normal bounds of ITS support. A
customization falls outside those bounds when, for example, installing or
integrating it may exercise untested or seldom-used features of Kubernetes,
Docker, or Linux, or student use of it may require sophisticated technical
expertise or extensive assistance.

Available capabilities considered complex or experimental include:

- Instructor or TA containers not derived from a standard software image
- Student-built customized containers, of any derivation
- Background batch processing and analysis pipelines
- MATLAB (Jupyter kernels or web UI), GNU Octave, or similar complex
  applications
- Spark clusters
- ArcGIS integration
- Postgres and other persistent services

Incorporating these or similar features into coursework requires the instructor
or TPOC to invest significant time before and during instruction, first to
become independently familiar with the underlying technologies and then to serve
as primary support for students' use of them.

ITS provides technical guidance for these features but, without advance
agreement, is not responsible for implementation or usage. Schedule a
[1:1 Consultation](#11-consultation) at least one full quarter before the
planned use to discuss feasibility.

### Visual Studio Code

Visual Studio Code is not among the complex or experimental features. It is
supported and widely used. The supported configuration is Remote-SSH over a
ProxyCommand, as described in
[Remote Editor Setup](access/remote-editor-setup.md).

## GPU Access for a Course

From Fall 2026, GPU access is managed by a reservation system, described in
[GPU Access](gpu-access/README.md).

### Quotas and Service Unit Budgets

A course holds a GPU quota, the number of GPUs of each class it may hold at
once. Its students hold Service Unit (SU) budgets, which divide that capacity
across the roster. Quotas are described in
[Quotas, Cohorts & Availability](gpu-access/quotas-and-availability.md) and
budgets in [Service Units & Budgets](gpu-access/service-units-and-budgets.md).

### Deadlines and the Quarterly Survey

Quotas are date-aware, so a course's share may be raised for the span of a
project deadline and revert afterward, as described in
[Date-Based Quota Changes](gpu-access/quotas-and-availability.md#date-based-quota-changes).
The quarterly survey asks instructors and TAs about assignment scope, GPU sizes,
and deadlines. The responses allow a course's quota to be raised in advance, for
example for week 9. Report assignment deadlines in the survey.

### Course Calendar

As workspace managers, instructors and TAs see the whole course calendar and may
book on behalf of a student whose project has run into trouble.

### Assisting a Student at the Service Unit Limit

Two routes are available, listed with the immediate one first.

1. Book on the student's behalf. The booking takes effect at once and does not
   draw on that student's budget. This is the appropriate route late in the
   evening before a deadline.
2. Request a budget or limit change by ticket to
   [datahub@ucsd.edu](mailto:datahub@ucsd.edu). The change itself is an
   administrative action.

Budgets are described in
[Service Units & Budgets](gpu-access/service-units-and-budgets.md), and the
request in [Administrative Requests](reference/getting-help.md#administrative-requests).

### Waiving a Cancellation Charge

A student who misses a booked window is assessed a cancellation charge.
Instructors and TAs may waive the charge where warranted, as described in
[The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty).

### Manager Reports

Manager reports cover reservations by group, peak simultaneous use by class,
reserved hours, and effective limits, as described in
[What the Reports Cover](reference/managing-a-group.md#what-the-reports-cover).
Some reports display cluster-wide data rather than data for the course alone.

### Advising Students

Two conditions account for most of the student questions that reach course
staff. Launching a GPU session draws on the student's budget whether or not a
calendar is opened, as described in
[On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges),
and a GPU session that stops using its GPU is reclaimed, as described in
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).
Both are covered for students in
[Using Datahub in a Course](student-in-a-course.md), for browser users, and in
[Working from the Command Line](working-from-the-command-line.md), for work that
requires a terminal.

## Maintenance and Policy

Under the
[University of California classification levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html),
highly sensitive P4 data, such as clinical records or export-controlled
information, is prohibited on Datahub and DSMLP, and legally or contractually
protected P3 data may be permitted after review, as described in
[Data Classification](reference/policy.md#data-classification).

Datahub may be unavailable during scheduled maintenance for time-sensitive
updates or security patches. The schedule is given in
[Scheduled Maintenance](reference/policy.md#scheduled-maintenance).

Other conditions of use, covering shared compute resources, availability and
reliability, and appropriate use, are on [Policy](reference/policy.md), which
also covers [Self-Supporting Programs](reference/policy.md#self-supporting-programs).
