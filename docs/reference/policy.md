# Policy

This page states the conditions for using Datahub and DSMLP: data
classification, campus acceptable use, hosting of services, expected practice on
shared resources, self-supporting programs, and scheduled maintenance.

## Data Classification

P3 and P4 are University
[classification levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html).
The University's classification is the authority on which level applies to a
dataset.

### P4 Data

P4 data is prohibited. Highly sensitive information, such as clinical records or
export-controlled material, must not be placed on Datahub or DSMLP. There is no
review path and no exception.

### P3 Data

P3 data may be permitted after review. Legally or contractually protected
information is not categorically excluded, but it must be raised with the
contacts in
[Contacts for Classification Questions](#contacts-for-classification-questions)
before any of it reaches the cluster. Depending on the nature of the data,
vetting may take 4-6 weeks or longer.

### Examples by Kind of Data

ITS documentation gives these examples:

| Kind of data | Examples |
|---|---|
| Government classified or controlled | CUI, CTI, ITAR, FISMA |
| Health and personal information | PHI/HIPAA, IRB-controlled data, statutory PII |
| Student records | Other students' grades or academic records (FERPA) |
| Contractually protected | Information subject to certain Data Use Agreements |

### Contacts for Classification Questions

For instruction and coursework, email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). For research, email Research IT at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu). Restricted and licensed
datasets are covered in
[Restricted & Licensed Datasets](../workspaces-and-storage/datasets.md#restricted--licensed-datasets),
and other support routes in [Getting Help](getting-help.md).

## Appropriate Use

### IT Acceptable Use Policy

The campus-wide
[IT Acceptable Use Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html)
applies to Datahub and DSMLP as it does to any campus IT resource, including its
prohibitions on commercial or political activity, hacking or cyberstalking, and
other types of unwelcome behavior. The platform's academic purpose does not
relax it.

### Individual Access and Sharing

Access is granted to an individual, not to that individual's collaborators. An
account, its home directory, and any dataset granted with it are for the account
holder's own use and are not passed on. The workspace's `public/` and `teams/`
areas are the sanctioned route for sharing, as described in
[Inside the Workspace](../workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace).

## Hosting Externally Available Services

Datahub and DSMLP should not be used to host externally available services or
applications, except as required for coursework or projects. A class demo, a
project web application, or a service an assignment requires is in scope. A
production service, a persistent public endpoint, or anything whose outage
someone outside the University would notice is out of scope. Access to a service
running in a container is described in
[Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service).

### Availability and Reliability

A compute node can be drained for patching, a pod can be preempted, and a
session has a deadline. These conditions apply primarily to the compute nodes
that execute user jobs. Critical components such as networking, file storage,
and backups are maintained to Enterprise IT standards.

## Use of Shared Resources

The practices in this section are requests rather than rules, with the exception
of the prohibition in
[Computation on the Login Node](#computation-on-the-login-node).

### Stopping Unused Sessions

Sessions that are not in use are expected to be stopped. GPU cards are assigned
to containers exclusively, and a card attached to an idle session is unusable by
any other user. Logging out, closing the tab, or closing a laptop leaves a
session running; stop it with **File → Hub Control Panel → Stop My Server**, as
described in
[Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session), or
delete the pod from the login node.

Idle culling is not a substitute for stopping a session. On a quiet cluster, the
delay before it acts is measured in hours. The idle criteria are described in
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).

### Debugging on CPU

Code is expected to be debugged on CPU before a GPU is requested. PyTorch and
TensorFlow both switch easily between CPU and GPU. The ways to start a session
are described in [Access](../access/README.md).

### Sizing Resource Requests

Requests are expected to name the smallest resources that work: the smallest GPU
class a model fits in, the memory a job needs rather than the maximum permitted,
and the hours the job actually takes. A larger GPU class is not faster for a
model that already fits in a smaller one. The classes are described in
[GPU Classes](../gpu-access/gpu-classes.md).

### Computation on the Login Node

Running computation on the login node, such as a training script, a build, or a
long analysis, is prohibited; the login node is for launching jobs and moving
files, as described in
[What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for).

### Personal Copies of Shared Datasets

A shared dataset is expected to be read where it lives rather than copied. A
per-student copy of a large corpus exhausts a home quota. Shared datasets are
described in
[Datasets](../workspaces-and-storage/datasets.md).

### Canceling Unused Bookings

A booking that will not be used is expected to be canceled. Canceling in advance
carries no penalty, and the capacity returns to the pool. Penalties are
described in
[The Cancellation Penalty](../gpu-access/service-units-and-budgets.md#the-cancellation-penalty).

### Peak GPU Demand

Demand for GPUs may exceed capacity at peak hours during 10th and Finals Weeks,
or at assignment deadlines. Work shifted to a daytime or off-peak hour costs
less, as described in
[Peak & Off-Peak Hours](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours).

## Self-Supporting Programs

[Self-supporting programs](https://blink.ucsd.edu/instructors/academic-info/majors/selfsupport-codes.html)
such as MAS and MBA may use Datahub and DSMLP for coursework or projects.
[UC policy](https://www.ucop.edu/institutional-research-academic-planning/content-analysis/academic-planning/self-supporting-programs.html)
requires ITS to recover the associated direct and indirect costs. To discuss
cost recovery, email [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

Charges for storage are set out in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

See also: [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage)

## Scheduled Maintenance

### Instructional Maintenance

Maintenance on the instructional side runs Tuesdays, 6-8 AM. The work is usually
limited to a subset of worker nodes, in which case running jobs are unaffected.
Do not plan a deadline within this window. Infrequent 'Critical' updates may
require downtime outside the window; ITS notifies instructors of such downtime
as soon as is practical.

### Research Cluster Maintenance

The Research Cluster maintenance window is quarterly, at the break between
terms, with about 7 days' notice. All running jobs are terminated. The effect on
sessions is described in
[Maintenance Closures](../gpu-access/what-ends-a-session.md#maintenance-closures).
