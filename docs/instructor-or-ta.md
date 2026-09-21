# Teaching with Datahub & DSMLP: Scope of Support & Guidelines for Usage

------------------------------------------------------------------------

UC San Diego's Datahub and Data Science & Machine Learning Platform (DSMLP)
provide thousands of undergraduates, graduate students, and their instructors
with access to Jupyter, RStudio, and other advanced computational resources for
scheduled classes, formal independent study, and student projects.

The platforms are used in courses ranging from introductory Data Science
lectures, to graduate-level applied machine-learning, to curricula in Biology,
Music, Social Sciences, and Public Health. Over AY 2025-26, more than 140
classes, 75 instructors, and 18,000 student enrollments were hosted.

This article describes the instructional request process and timeline; the
curated Standard Software Images and how to customize them; options for support
and technical consulting; how GPU access is managed for a course from Fall 2026;
and finally, a few pertinent caveats and conditions including important
limitations on use of sensitive/protected data.

**One article for both instructors and TAs.** Where a task is restricted to one
role, it is noted. Most of what follows is done in a browser; customization
requires a shell and someone prepared to use it.

Please reach out to our team with any questions or feedback regarding these
guidelines or Datahub/DSMLP as a whole.

- Email: [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
- 1:1 Consultation: <https://ucsd-datahub.youcanbook.me/>

## Course Timeline: Requesting Access & Important Dates

------------------------------------------------------------------------

Instructors, TAs, and departmental staff may request Datahub/DSMLP access via the
[Specialized Instructional Computing Course Request](https://support.ucsd.edu/its?id=sc_cat_item_guide&sys_id=dc1afcd51b152910484f968f034bcb8b&sysparm_category=90e152651b19a910484f968f034bcbf0)
form beginning the 2nd week of the previous term. (For Summer/Fall classes,
submission opens the 2nd week of Spring.)

**Requests must be submitted 4 weeks prior to the start of instruction**; this
includes designation of a Technical Point of Contact when required (see below).
*Late requests are given lower priority and will be reviewed as time permits.
Setup and ultimate availability to students will depend upon individual
complexity and overall request load; students may not gain access until as late
as 4th week.*

**Course setup** and **instructor access** opens 4-5 weeks prior to the start of
instruction. The instructor, TAs, and other course staff should begin testing
features, validating assignments, and making desired customizations. Earlier
setup is available upon request. *Note that 1:1 Consulting support for
customization (discussed below) is limited in the final weeks of each term.*

**Student access** follows TSS course rosters — the system formerly called
TritonLink. **Rosters are loaded into workspaces one business day before the
start of the term**, and a subsequent add/drop is reflected by 10am the day
following the change. Non-roster auditor and observer access
[is managed through Canvas](https://support.ucsd.edu/services?id=kb_article_view&sysparm_article=KB0032124);
[Concurrent Enrollment](https://extendedstudies.ucsd.edu/student-resources/registration-policies-and-procedures/concurrent-enrollment)
students receive access by way of Extended Studies staff.

<!-- TO ADD: per-quarter Key Dates & Events table (requests open, setup begins,
     submission deadline, students receive access, access ends, files purged).
     Generate it from the campus academic calendar rather than by hand: the
     previous published version had one quarter's student-access date falling
     after instruction began, and two of three deadlines falling inside the
     stated four-week requirement. -->

Instructors and students **retain access for one additional quarter** beyond the
instructional term(s), ignoring Summer for Spring courses. Instructors may
request individual accounts remain active longer to facilitate Incomplete grade
resolution, academic integrity proceedings, course development or hand-off, or
similar circumstances.

<!-- UNSETTLED: a second, day-based retention schedule is also in effect
     (ticket closed at 11 days; shared nbgrader/TA access removed at 45 days;
     instructor and student access removed at 90 days). For Fall and Winter
     courses the two land within weeks of each other; for SPRING courses they
     are irreconcilable, because the quarter-based scheme skips Summer. The
     45-day TA/grader milestone has no counterpart here at all, so as published
     a TA loses access on a clock this article never mentions. Resolve before
     publication. -->

**Course environments are purged one quarter after account deactivation**, i.e.
after two quarters excluding Summer, except for: individual accounts extended as
above; and instructor/course-wide files which can be archived for up to 3 years
upon request. Please contact ITS to revive a previously archived class
environment, or to make an archive available for download. *(Note: large datasets
cannot be archived due to storage limitations; contact ITS to discuss alternate
options.)* → [When Access Starts & Ends](access/when-access-starts-and-ends.md)

For-credit **Independent study, capstones, and similar student projects** may
request ongoing access via the
[Independent Study Request](https://go.ucsd.edu/2wc5gH0) form — please direct
those students to [Projects & Independent Study](student-project.md).
[Research IT](https://research-it.ucsd.edu/computing/index.html) can help connect
faculty, staff, and student researchers with compute platforms for non-credit
research.

## Standard Features & Standard Software Images

------------------------------------------------------------------------

Datahub offers a set of curated software environments which are sufficient for
many courses and use cases. Questions, configuration assistance, malfunctions,
and errors relating to these **standard features** receive priority support from
IT Services via a number of channels (see below):

- **[Standard Software Images](environments/standard-images.md)** accessible via
  web-based Jupyter notebooks as well as text/CLI:
  - **datascience-notebook** includes widely-used libraries for data analysis
    from the Julia, Python, and R communities.
  - **scipy-ml-notebook** supplements 'datascience-notebook' with CUDA/GPU
    enabled tools such as TensorFlow and PyTorch for deep learning applications.
  - **rstudio-notebook** extends 'datascience-notebook' with the
    [RStudio](https://en.wikipedia.org/wiki/RStudio) development environment.
    *Note that this image derives from 'datascience-notebook' and is therefore
    not GPU-enabled.*

- Flexible CPU, memory, and NVidia GPU allocations, beginning at 2 CPU cores and
  4GB RAM dedicated to each student session. *Upper limits based on class size,
  demand, and capacity.*

- Course-specific file/dataset distribution (up to 500GB, with larger corpora
  accepted on a space-available basis) and up to 10GB storage per student.
  *Allocations at the lower end of that range are used for very large classes;
  please tell us where assignments generate significant per-student output.*
  → [Workspaces & Storage](workspaces-and-storage/README.md)

- Tools for [assignment distribution / collection / grading](grading/README.md), including
  roster integration with Canvas.

  **Grade export to Canvas is performed manually.** The workflow generates a CSV
  file which the instructor or TA uploads to the Canvas gradebook.
  → [Exporting the Grades](grading/notebook-grading-workflow.md#exporting-the-grades)

- Limited support for per-individual
  [minor customizations](environments/customizing-your-environment.md) within our
  standard software images.

## Course-Specific Customization

------------------------------------------------------------------------

Instructors may
[supplement standard software images](environments/building-a-custom-image.md)
through addition of language modules (e.g. Python or R libraries), new
system-level packages (compilers, utilities, etc.), or more extensive
modifications to meet the specific needs of their course.

As experts in their curriculum and subject area, the instructor and/or a
designated **Technical Point of Contact** ("TPOC") must take the lead in the
installation, configuration, and student use of the new course-specific features.
*ITS technical staff provide support for customization via 1:1 Consultation (see
below).*

The instructor and/or TPOC is expected to have basic familiarity with Unix
commands such as 'ssh', 'mkdir' and 'chmod' and should be proficient using the
intended core platform (e.g. Python or R) in a desktop Mac/PC setting. *ITS will
provide guidance and basic training regarding the Datahub/DSMLP environment and
any system-specific procedures.*

*Note that 1:1 Consultation availability is limited in the final weeks of each
term.*

Highly complex use cases (e.g. those incorporating clustered services such as
Spark or Postgres, or software not deriving from our Standard Images) are
regularly utilized within Datahub/DSMLP, but will require substantially more time
and expertise from the instructor/TPOC than ordinary customizations. *See
"Complex Customizations & Experimental Features" below for guidance.*

A course may also **pin** a specific image so that students are not moved by a
quarterly update partway through a project.
→ [Pinning a Workspace](environments/standard-images.md#pinning-a-workspace)

## Support & Technical Consultation

------------------------------------------------------------------------

IT Services provides prioritized support for **standard features** and
functionality via several routes:

**[Online Documentation](README.md)** offers general information about Datahub
and usage of the platform's various features, as well as documentation for known
issues, workarounds, and limitations of the environment.

The **[IT Service Desk](https://support.ucsd.edu/)** can be reached by Phone,
Web, or Email for assistance with:

- Outages, Errors, or Malfunctions, e.g.:
  - System issues (e.g. the service or components are unavailable)
  - User access issues (e.g. an enrolled student can't login)
  - Errors or unexpected behavior within standard features *(effort is
    prioritized by the number of courses/students affected and overall impact on
    instruction)*

  *We ask that students route functionality concerns through their Instructor or
  TA.*

- Requests & Inquiries:
  - Requests for system-side configuration or adjustments to course setup, e.g.
    resource limits, disk quotas, container tags, file ownership/permissions
  - Straightforward questions about core features, system capabilities,
    clarification of documentation, etc.; in-depth support available via 1:1
    Consultation.

**Response targets:**

| | |
|---|---|
| Individual user issues | We aim to resolve within **1-2 business days** |
| Incidents affecting multiple courses, many users, or critical points in the quarter (e.g. exams) | Target **response time of 30 minutes** from first contact to Service Desk, and a target **resolution time of 8 hours** |

*Effort is prioritized by the number of courses and students affected. Please
note in the ticket where an issue affects a whole class or falls on an exam.*
Urgent problems arising outside business hours may be escalated through the
Service Desk.

**[1:1 Consultation appointments](https://ucsd-datahub.youcanbook.me/)** connect
instructors, TAs, and Technical Points of Contact with ITS technical experts for
real-time guidance or assistance on standard features, course-specific
customizations, and complex/experimental features.

Possible topics include:

- In-depth questions regarding Standard/Core Feature configuration or usage
- Discussion not well-suited to ticket-based interaction
- Functional or technical issues outside of the Standard/Core features
- First-time use of a custom container derived from a standard software image
- Reviewing customization options and selection of additional packages/tools
- Resolving functional or technical issues pertaining to course-custom features,
  e.g. build errors, version conflicts
- Questions/training regarding our customization process, e.g. use of git,
  Github, tags, Actions, etc., or installation of language and system packages
- Assistance with maintenance following quarterly Standard Software Image updates

*Note that 1:1 Consultation availability is reduced in the final weeks of each
term, and staffing levels limit courses to a maximum number of hours per term
(see "Caveats and Limitations" below.)*

## Complex Customizations & Experimental Features

------------------------------------------------------------------------

The compute clusters underpinning Datahub and DSMLP are capable of hosting
complex or novel customizations which fall outside ITS' normal bounds of support
for a variety of reasons, e.g. installing or integrating them may exercise
untested or seldomly-used features of Kubernetes, Docker, or Linux, or student
use of the new features may require sophisticated technical expertise or
hand-holding.

Examples of available capabilities considered complex or experimental include:

- Instructor/TA containers not derived from a Standard Software Image
- Student-built customized containers (of any derivation)
- Background batch processing and analysis pipelines
- Matlab (Jupyter kernels or Web UI), GNU Octave, or similar complex applications
- Spark clusters
- ArcGIS integration
- Postgres and other persistent services

Incorporation of these or similar features into coursework will require the
instructor and/or TPOC to invest significant time ahead of and during
instruction, first to become independently familiar with the underlying
technologies and then to serve as primary support for their students'
activities.

ITS is eager to provide technical guidance for innovation within our services,
but without advance agreement cannot become responsible for implementation or
usage. We recommend scheduling a 1:1 Consultation with us at least **one full
quarter** in advance of the planned use to discuss feasibility.

*Visual Studio Code is not among these.* It is supported and in heavy use, via
Remote-SSH over a ProxyCommand.
→ [Remote Editor Setup](access/remote-editor-setup.md)

## GPU Access for a Course

------------------------------------------------------------------------

From Fall 2026, GPU access is managed by a reservation system. The mechanics are
documented in [GPU Access](gpu-access/README.md); what follows is what a course needs.

**A course holds a GPU quota** — how many of each class it may hold at once —
and its students hold **Service Unit (SU) budgets** which divide that capacity
across the roster. Quotas are date-aware: a course's share may be raised for
exactly the span of a project deadline and revert on its own afterwards.
→ [Quotas, Cohorts & Availability](gpu-access/quotas-and-availability.md)

**Please tell us the deadlines.** The quarterly survey asks instructors and TAs
about assignment scope, GPU sizes, and — crucially — deadlines. Those responses
are what allow us to raise a course's quota for week 9 in advance rather than
discover the surge as it occurs.

**Managing the course calendar.** As workspace managers, instructors and TAs see
the whole course calendar and may book on behalf of a student whose project has
run into trouble.

**Assisting a student who has reached their SU limit.** Two routes; the immediate
one first:

1. **Book on the student's behalf.** This takes effect at once and does not draw
   that student's budget. This is the appropriate action late in the evening
   before a deadline.
2. **Request a budget or limit change** by ticket to
   [datahub@ucsd.edu](mailto:datahub@ucsd.edu). The change itself is an
   administrative action, but requesting it is a normal and sanctioned route.

→ [Service Units & Budgets](gpu-access/service-units-and-budgets.md) ·
[The Six Requests](reference/getting-help.md#the-six-requests)

**Waiving a cancellation charge.** A student who misses a booked window is
assessed a cancellation charge of up to 50% of the booking. Instructors and TAs
may waive this charge where warranted.
→ [The Cancellation Penalty](gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

**Reports.** Manager reports cover reservations by group, peak simultaneous use
by class, reserved hours, and effective limits. *Note that some of these display
cluster-wide data rather than only the course itself.*
→ [Managing a Group](reference/managing-a-group.md#what-the-reports-cover)

**Advising students.** Two facts account for most of what reaches course staff:
launching a GPU session draws on the student's budget whether or not a calendar
is opened, and an idle GPU session is reclaimed after roughly 30 minutes. Both
are covered on the student pages —
[Using Datahub in a Course](student-in-a-course.md) for browser users, and
[Working from the Command Line](working-from-the-command-line.md) for anything
requiring a terminal.

## Caveats & Limitations

------------------------------------------------------------------------

We ask all Datahub/DSMLP users to understand and abide by the following:

**No Sensitive Data:** Datahub is not engineered to protect highly-sensitive data
such as clinical records or export-controlled information ("P4" per
[University of California classification levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html))
and must not be used for such purposes. Legally- or contractually- protected
information ("P3") may be permitted after review; note that depending on the
nature of the data, vetting may take 4-6 weeks or longer.

**Shared Consulting Resources:** at Spring 2026 staffing levels, each course may
request up to 6 hours of 1:1 Consulting services.

**Scheduled Maintenance:** Datahub may be unavailable Tuesdays, 6-8AM for
installation of time-sensitive updates or security patches. *In practice this
work is generally limited to a subset of worker nodes, in which case running jobs
are unaffected.* Infrequent 'Critical' updates may require downtime outside of this
timeframe, in which case we will notify instructors as soon as practical and
attempt to minimize impact on coursework and long-running jobs.

**Shared Compute Resources:** Datahub and DSMLP system resources are shared among
all courses assigned to Datahub and DSMLP. Demand for resources, in particular
for GPUs, may exceed capacity at peak hours during 10th and Finals Weeks or at
assignment deadlines. *From Fall 2026, reservations, per-course quotas and
Service Unit budgets are the mechanisms by which equitable access is provided in
such situations.*

**Self-Supporting Programs:**
["Self-supporting" programs](https://blink.ucsd.edu/instructors/academic-info/majors/selfsupport-codes.html)
(e.g. MAS, MBA, etc.) are welcome to utilize DSMLP/Datahub for coursework or
projects, but
[UC policy](https://www.ucop.edu/institutional-research-academic-planning/content-analysis/academic-planning/self-supporting-programs.html)
requires us to recover associated direct and indirect costs. Please contact us to
discuss.

**Availability and Reliability:** Datahub and DSMLP were designed with student
workloads in mind, deliberately trading some of the costly redundancy typical of
financial or health settings for additional capacity and capability. As such,
they should not be used to host externally-available services or applications
except as required for coursework or projects. *(This caveat applies primarily to
the compute nodes executing student jobs; critical components such as networking,
file storage, and backups are maintained to Enterprise IT standards.)*

**Appropriate Use:** The campus-wide
[IT Acceptable Use Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html)
applies to use of Datahub and DSMLP, including prohibitions on commercial or
political activity, hacking or cyberstalking, and other types of unwelcome
behavior.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu), submit a ticket, or call the
[ITS Service Desk](https://support.ucsd.edu/).
