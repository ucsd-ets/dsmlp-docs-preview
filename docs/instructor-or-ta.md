# Teaching with Datahub and DSMLP

This page is for instructors and TAs teaching a course on Datahub and DSMLP.
Most course tasks need only a browser; course-specific customization needs a
shell.

## Course Timeline

### Requesting a Course

Request Datahub and DSMLP access for a course through the
[Specialized Instructional Computing Course Request](https://support.ucsd.edu/its?id=sc_cat_item_guide&sys_id=dc1afcd51b152910484f968f034bcb8b&sysparm_category=90e152651b19a910484f968f034bcbf0)
form. Instructors, TAs, and departmental staff can submit it. Submission opens
in the 2nd week of the previous term. For Summer and Fall classes, submission
opens in the 2nd week of Spring.

The request is due 4 weeks before the start of instruction. Where the course
needs a Technical Point of Contact (TPOC), name one in the request. See
[Technical Point of Contact](#technical-point-of-contact). A late request gets
lower priority and is reviewed as time permits. Setup time and the date your
students get access depend on the complexity of the course and on the overall
request load. After a late request, your students may not get access until as
late as 4th week.

### Course Setup and Instructor Access

Course setup and instructor access open 4-5 weeks before the start of
instruction. You can request earlier setup. During this period, you and the
other course staff test features, validate assignments, and make
customizations. 1:1 Consultation for customization is limited in the final
weeks of each term. See [1:1 Consultation](#11-consultation).

### Student Access

Student access follows TSS course rosters. TSS is the system formerly called
TritonLink.
[Students Enrolled in a Course](access/when-access-starts-and-ends.md#students-enrolled-in-a-course)
gives when rosters load and when add and drop changes take effect. Auditors and
observers are not on the roster, and their access is
[managed through Canvas](https://support.ucsd.edu/services?id=kb_article_view&sysparm_article=KB0032124).
[Concurrent Enrollment](https://extendedstudies.ucsd.edu/student-resources/registration-policies-and-procedures/concurrent-enrollment)
students get access through Extended Studies staff.

### Access After the Term

You and your students keep access for one additional quarter beyond the
instructional term, ignoring Summer for Spring courses. See
[One Additional Quarter](access/when-access-starts-and-ends.md#one-additional-quarter).
The instructor can request that individual accounts stay active longer, for
Incomplete grade resolution, academic integrity proceedings, course development
or hand-off, or similar circumstances. See
[Extending Access for an Individual](access/when-access-starts-and-ends.md#extending-access-for-an-individual).

Course environments are purged one quarter after account deactivation, that is,
two quarters after the course, excluding Summer. The purge skips two things:
individual accounts extended on request, and instructor and course-wide files
archived on request. Ask ITS to archive files, to revive a previously archived
class environment, or to make an archive available for download. See
[Archiving on Request](access/when-access-starts-and-ends.md#archiving-on-request).

### Independent Study and Research

Students in for-credit independent study, capstones, and similar projects
request ongoing access through the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form. Direct those
students to [Projects & Independent Study](student-project.md). For non-credit
research, [Research IT](https://research-it.ucsd.edu/computing/index.html)
connects faculty, staff, and student researchers with compute platforms.

## Standard Features & Standard Software Images

Datahub offers a set of curated software environments that are sufficient for
many courses and use cases. These environments, with the session resources,
course file distribution, grading tools, and individual customization support
that accompany them, are the **standard features**. IT Services gives priority
support for questions, configuration help, malfunctions, and errors in the
standard features.
[Support & Technical Consultation](#support--technical-consultation) lists the
routes.

### Standard Software Images

You and your students can use the standard software images through web-based
Jupyter notebooks and from the command line.
[Standard Images](environments/standard-images.md#standard-images) describes
them. The `rstudio-notebook` image derives from `datascience-notebook` and is
not GPU-enabled.

### Session Resources

CPU, memory, and NVIDIA GPU allocations are flexible, beginning at 2 CPU cores
and 4GB RAM dedicated to each student session. Upper limits depend on class
size, demand, and capacity. See
[The Browser Session](access/datahub-in-the-browser.md#the-browser-session).

### Course Files and Storage

Course-specific file and dataset distribution is available.
[Asking for a Dataset to Be Staged](workspaces-and-storage/datasets.md#asking-for-a-dataset-to-be-staged)
gives the size limits.
[Workspace and Personal Quotas](workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas)
gives the storage each student gets, and
[Workspaces & Storage](workspaces-and-storage/README.md) covers course storage
in general. Tell ITS when assignments generate significant output for each
student.

### Grading Tools

[Grading](grading/README.md) covers the tools for distributing, collecting, and
grading assignments, including roster integration with Canvas.

> [!NOTE]
> Grade export to Canvas is manual. The workflow generates a CSV file, which you
> upload to the Canvas gradebook. See
> [Exporting the Grades](grading/notebook-grading-workflow.md#exporting-the-grades).

### Individual Customizations

Minor customizations that individuals make within the standard software images
get limited support. See
[Customizing an Environment](environments/customizing-your-environment.md).

## Course-Specific Customization

The instructor can supplement the standard software images to meet the needs
of a course: add language modules (for example, Python or R libraries), add
system-level packages (compilers, utilities, and similar), or make more
extensive modifications.
[Building & Publishing a Custom Image](environments/building-a-custom-image.md)
gives the procedure.

Highly complex use cases, such as clustered services like Spark or Postgres,
or software not derived from the standard images, are in regular use on
Datahub and DSMLP. They need substantially more time and
expertise from the instructor or TPOC than ordinary customizations. See
[Complex Customizations & Experimental Features](#complex-customizations--experimental-features).

### Technical Point of Contact

The instructor, a designated **Technical Point of Contact** (TPOC), or both
must lead the installation, configuration, and student use of course-specific
features. ITS technical staff support customization through
[1:1 Consultation](#11-consultation).

The instructor or TPOC needs basic familiarity with Unix commands such as
`ssh`, `mkdir`, and `chmod`, and proficiency with the intended core platform
(for example, Python or R) in a desktop Mac or PC setting. ITS gives guidance
and basic training on the Datahub and DSMLP environment and on system-specific
procedures.

### Pinning an Image

You can ask ITS to pin a specific image for your course, so that an image
update partway through a project does not move your students. See
[Pinning a Workspace](environments/standard-images.md#pinning-a-workspace).

## Support & Technical Consultation

IT Services gives priority support for standard features and functionality
through the [Datahub & DSMLP Documentation](README.md), the IT Service Desk,
and 1:1 Consultation. Send questions and feedback about Datahub and DSMLP to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).

### IT Service Desk

Contact the [IT Service Desk](https://support.ucsd.edu/) by phone, web, or
email for the following.

| Category | Examples |
|---|---|
| Outages, errors, or malfunctions | System issues, such as the service or its components being unavailable; user access issues, such as an enrolled student being unable to log in; errors or unexpected behavior within standard features |
| Requests and inquiries | Requests for system-side configuration or adjustments to course setup, such as resource limits, disk quotas, container tags, and file ownership or permissions; straightforward questions about core features, system capabilities, or clarification of documentation |

Effort is prioritized by the number of courses and students affected and by
the overall impact on instruction. Say in the ticket when an issue affects a
whole class or falls on an exam. Students route functionality concerns through
you. Take in-depth questions to [1:1 Consultation](#11-consultation).

[Response Targets](reference/getting-help.md#response-targets) gives the
response targets, including the incident tier for instructors. You can
escalate urgent problems that arise outside business hours through the Service
Desk.

### 1:1 Consultation

Instructors, TAs, and TPOCs can book
[1:1 Consultation appointments](https://ucsd-datahub.youcanbook.me/) with ITS
technical experts for real-time guidance or help with standard features,
course-specific customizations, and complex or experimental features. Topics
include:

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
- Maintenance following updates to the standard software images

At Spring 2026 staffing levels, each course can request up to 6 hours of 1:1
Consultation per term. Availability is reduced in the final weeks of each term.

## Complex Customizations & Experimental Features

The compute clusters underlying Datahub and DSMLP can host complex or novel
customizations that fall outside the normal bounds of ITS support. A
customization falls outside those bounds when, for example, installing or
integrating it may exercise untested or seldom-used features of Kubernetes,
Docker, or Linux, or when student use of it may need sophisticated technical
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

Incorporating these or similar features into coursework takes significant time
from the instructor or TPOC before and during instruction: first to become
independently familiar with the underlying technologies, and then to serve as
primary support for students' use of them.

ITS gives technical guidance for these features but, without advance agreement,
is not responsible for implementation or usage. Schedule a
[1:1 Consultation](#11-consultation) at least one full quarter before the
planned use to discuss feasibility.

### Visual Studio Code

Visual Studio Code is not among the complex or experimental features. It is
supported and widely used. The supported configuration is Remote-SSH over a
ProxyCommand. See [Remote Editor Setup](access/remote-editor-setup.md).

## GPU Access for a Course

From Fall 2026, a reservation system manages GPU access. See
[GPU Access](gpu-access/README.md). Its web app is at
[reserve.dsmlp.ucsd.edu](https://reserve.dsmlp.ucsd.edu/).

### Quotas and Service Unit Budgets

A course holds a GPU quota, the number of GPUs of each class it may hold at
once. Its students hold Service Unit (SU) budgets, which divide that capacity
across the roster. The instructor can request, by ticket, a change to the
course workspace's defaults, including its weekly budget, its booking horizon,
and its length cap. See
[Quotas, Cohorts & Availability](gpu-access/quotas-and-availability.md) and
[Service Units & Budgets](gpu-access/service-units-and-budgets.md).

### Deadlines and the Quarterly Survey

Quotas are date-aware, so a course's share can rise for the span of a project
deadline and revert afterward. See
[Date-Based Quota Changes](gpu-access/quotas-and-availability.md#date-based-quota-changes).
The quarterly survey asks you about assignment scope, GPU sizes, and
deadlines. Your responses allow a course's quota to rise in advance, for
example for week 9. Report assignment deadlines in the survey.
[Workloads by GPU Class](gpu-access/workloads-by-gpu-class.md) gives examples
of course work at each GPU size.

### Course Calendar

As a workspace manager, you see every reservation in the course on the
reservation app's **Group Reservations** page. You can book on a student's
behalf, cancel a student's booking, and waive penalties. See
[Managing a Group](reference/managing-a-group.md). In a course whose roster is
loaded automatically, the instructor, TAs, and graders are all workspace
managers.

### Assisting a Student at the Service Unit Limit

Request a budget change by ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). The change itself is an
administrative action. Students normally book their own windows. The other
route is to book on the student's behalf. Your booking goes through even when
the student's budget is spent, though not past the group pool or the workspace
length cap.

> [!WARNING]
> A booking you make on a student's behalf is charged to that student's budget.
> It skips only the check that the student can afford it, so it can leave the
> student over budget and block their own bookings and on-demand sessions until
> the budget renews the following Monday.

See [Service Units & Budgets](gpu-access/service-units-and-budgets.md) and
[Administrative Requests](reference/getting-help.md#administrative-requests).

### Waiving a Cancellation Charge

A student who misses a booked window is assessed a cancellation charge. You
can waive the charge where warranted, on the **Group Reservations** page, when
cancelling or afterwards. See
[Having a Charge Waived](gpu-access/service-units-and-budgets.md#having-a-charge-waived).

### Manager Reports

Manager reports cover reservations by group, peak simultaneous use by class,
reserved hours, and effective limits. See
[What the Reports Cover](reference/managing-a-group.md#what-the-reports-cover).
Three of the four reports display cluster-wide data rather than data for your
course alone.

### Reservation Events

The reservation system reports on each student's GPU session with Kubernetes
events. Datahub shows them while a session starts, and `kubectl describe pod`
shows them from the command line. A student's question often quotes one.
[Reservation Events](reference/reservation-events.md) defines each one:

- While a session waits: `WaitingForReservation`, `ReservationFull`,
  `ReservationTooSmall`, `OnDemandLeaseDenied`, `OnDemandLeaseRejected`,
  `OnDemandAdmissionPaused`, `UnknownGpuClass`, `NoReservation`,
  `AnnotationIgnored`, `NoMatchingNode`, `WaitingForNode`.
- When it is admitted: `RuntimeGuaranteed`, `ReservationRelinked`,
  `OverstayRelinked`, `BestEffortAdmitted`.
- When it is stopped: `Preempted`, `ReservationCancelled`,
  `ReservationReassigned`.

### Advising Students

Two conditions account for most of the student questions that reach you.
Launching a GPU session draws on the student's budget, even if no calendar is
opened. See
[On-Demand Lease Charges](gpu-access/service-units-and-budgets.md#on-demand-lease-charges).
A GPU session that stops using its GPU is reclaimed. See
[What Counts as Idle](gpu-access/what-ends-a-session.md#what-counts-as-idle).
For students, [Using Datahub in a Course](student-in-a-course.md) covers both
for browser users, and
[Working from the Command Line](working-from-the-command-line.md) covers them
for work that requires a terminal.

## Maintenance and Policy

Under the
[University of California classification levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html),
highly sensitive P4 data, such as clinical records or export-controlled
information, is prohibited on Datahub and DSMLP. Legally or contractually
protected P3 data may be permitted after review. See
[Data Classification](reference/policy.md#data-classification).

Datahub may be unavailable during scheduled maintenance for time-sensitive
updates or security patches.
[Scheduled Maintenance](reference/policy.md#scheduled-maintenance) gives the
schedule.

[Policy](reference/policy.md) gives the other conditions of use, covering shared
compute resources, availability and reliability, and appropriate use. It also
covers [Self-Supporting Programs](reference/policy.md#self-supporting-programs).
