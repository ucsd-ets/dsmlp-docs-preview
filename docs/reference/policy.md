# Policy: Acceptable Use, Data Classification & Shared-Resource Courtesy

Three separate obligations sit on everyone who uses Datahub and DSMLP: what the
University permits on the platform, what campus policy permits on any IT
resource, and what colleagues on a shared cluster are entitled to expect. This
page covers all three.

## Data Classification

------------------------------------------------------------------------

**P4 data is prohibited.** Highly-sensitive information such as clinical records
or export-controlled material must not be placed on Datahub or DSMLP. There is no
review path and no exception.

**P3 data may be permitted after review.** Legally or contractually protected
information is *not* categorically excluded. It requires a conversation before
any of it reaches the cluster, and depending on the nature of the data,
**vetting may take 4-6 weeks or longer**.

The University's [classification
levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html)
are the authority on which level applies. The examples our own documentation
gives are:

| Kind of data | Examples |
|---|---|
| Government classified or controlled | CUI, CTI, ITAR, FISMA |
| Health and personal information | PHI/HIPAA, IRB-controlled data, statutory PII |
| Student records | Other students' grades or academic records (FERPA) |
| Contractually protected | Information subject to certain Data Use Agreements |

**Where to raise it.** For instruction and coursework, email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). For research, Research IT at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).
→ [Restricted & Licensed Datasets](../workspaces-and-storage/datasets.md#restricted--licensed-datasets) ·
[Getting Help](getting-help.md)

## Appropriate Use

------------------------------------------------------------------------

**The campus-wide [IT Acceptable Use
Policy](https://adminrecords.ucsd.edu/ppm/docs/135-9.html) applies here as it
does to any campus IT resource**, including its prohibitions on commercial or
political activity, hacking or cyberstalking, and other types of unwelcome
behavior. Nothing about this platform's academic purpose relaxes it.

**Access is granted to an individual, not to that individual's collaborators.**
An account, its home directory and any dataset granted with it are for the
account holder's own use and are not passed on. The workspace's `public/` and
`teams/` areas are the sanctioned route for sharing.
→ [Inside the Workspace](../workspaces-and-storage/moving-and-sharing-data.md#inside-the-workspace)

## Not a Place for Externally-Available Services

------------------------------------------------------------------------

**Datahub and DSMLP should not be used to host externally-available services or
applications, except as required for coursework or projects.**

A compute node can be drained for patching, a pod can be preempted, and a session
has a deadline. *(This caveat applies primarily to the compute nodes executing
user jobs; critical components such as networking, file storage and backups are
maintained to Enterprise IT standards.)*

**A class demo, a project web application, a service an assignment requires:
all in scope.** A production service, a persistent public endpoint, or anything
somebody outside the University would notice going down: not.
→ [Port Forwarding & Reaching Services in a Container](../access/the-login-node.md#reaching-a-notebook-or-a-service)

## Shared-Resource Courtesy

------------------------------------------------------------------------

Every one of these is a request rather than a rule.

**Please stop sessions that are not in use.** GPU cards are assigned to
containers exclusively: a card attached to an idle session is unusable by
anybody else. Stop the session with **File → Hub Control Panel →
Stop My Server**, or delete the pod from the login node. *Logging out, closing
the tab and closing a laptop all leave it running.*
→ [Datahub in the Browser](../access/datahub-in-the-browser.md)

**Please do not treat idle culling as a cleanup service.** The delay before it
acts is measured in hours on a quiet cluster.
→ [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

**Please debug on CPU before requesting a GPU.** Both PyTorch and TensorFlow
switch between CPU and GPU easily, and a CPU-only container is not the scarce
thing. → [Access](../access/README.md)

**Please ask for the smallest thing that works** — the smallest GPU class a model
fits in, the memory a job needs rather than the maximum permitted, the hours it
actually takes. A larger class is not faster for a model that already fits in a
smaller one; it is only scarcer.
→ [GPU Classes](../gpu-access/gpu-classes.md)

**Please do not compute on the login node.** It is a jumpbox for launching jobs
and moving files. Running a training script, a build or a long analysis there is
prohibited.
→ [The Login Node](../access/the-login-node.md)

**Please do not keep a personal copy of a shared dataset.** Read it where it
lives. A per-student copy of a large corpus exhausts a home quota, and multiplied
across a roster it exhausts rather more than that.
→ [Shared Datasets](../workspaces-and-storage/datasets.md)

**Please cancel a booking that will not be used.** Cancelling in advance carries
no penalty, and the capacity returns to the pool.
→ [The Cancellation Penalty](../gpu-access/service-units-and-budgets.md#the-cancellation-penalty)

**Demand for GPUs may exceed capacity** at peak hours during 10th and Finals
Weeks or at assignment deadlines. Work shifted to a daytime or off-peak hour
costs less.
→ [Off-Peak Discounts](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours)

## Self-Supporting Programs

------------------------------------------------------------------------

**Self-supporting programs are welcome**, and there is a cost attached.
[Self-supporting programs](https://blink.ucsd.edu/instructors/academic-info/majors/selfsupport-codes.html)
such as MAS and MBA may use Datahub and DSMLP for coursework or projects, and
[UC policy](https://www.ucop.edu/institutional-research-academic-planning/content-analysis/academic-planning/self-supporting-programs.html)
requires us to recover the associated direct and indirect costs. *Please contact
us at [datahub@ucsd.edu](mailto:datahub@ucsd.edu) to discuss it.*

*Note separately that storage above 1 TB is chargeable. Compute is not.*
→ [Mounting External Storage](../workspaces-and-storage/your-files-and-quotas.md#mounting-external-storage)

## Scheduled Maintenance

------------------------------------------------------------------------

**On the instructional side, maintenance runs Tuesdays, 6-8 AM.** In practice the
work is usually limited to a subset of worker nodes, in which case running jobs
are unaffected — but please do not plan a deadline into that window. Infrequent
'Critical' updates may require downtime outside it, in which case we notify
instructors as soon as is practical.

**The Research Cluster window is different in kind.** It is quarterly, at the
break between terms, comes with about 7 days' notice, and **all running jobs are
terminated**. → [Maintenance Closures](../gpu-access/what-ends-a-session.md#maintenance-closures)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
