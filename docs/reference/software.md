# Software: R, RStudio, MATLAB, Stata & Licensed Software

**Most software questions are answered by the standard images**, which cover the
great majority of courses and projects and receive priority support. What is on
this page is the rest: the things that are here but are not simply *in* an image,
and the things people ask for that we cannot yet answer.
→ [Standard Images and What Is in Them](../environments/standard-images.md)

## R and RStudio

------------------------------------------------------------------------

**R comes in every standard image**, alongside Python and Julia, and works as a
Jupyter kernel like any other. `?command_name` in a cell brings up the
documentation for a function.

**RStudio is a click, not a separate sign-in.** Start the course environment that
includes RStudio, wait for the JupyterLab launcher to load, and click the RStudio
shortcut; it opens in a new tab.

**The first RStudio session in a new account needs a personal package library
before `install.packages()` will work.** Run this once, in the RStudio Console:

```r
dir.create("~/R")
dir.create("~/R/library")
.libPaths("~/R/library")
```

*That directory lives in the home directory and counts against its quota like
anything else.* → [Customizing an Environment](../environments/customizing-your-environment.md)

**`rstudio-notebook` is not GPU-enabled.** It derives from
`datascience-notebook`, the CPU image, rather than from `scipy-ml-notebook`. A
course that needs both RStudio and a GPU needs a custom image or a second
environment. → [Getting Help](getting-help.md)

## MATLAB, Octave & Other Complex Applications

------------------------------------------------------------------------

**MATLAB is possible here and is not a standard feature.** Our published scope of
support classes MATLAB — as Jupyter kernels or as the Web UI — together with GNU
Octave among *complex or experimental* capabilities: regularly used on the
platform, outside ITS' normal bounds of support, and requiring the instructor or
TPOC to lead rather than to be led.

**On the Research Cluster, the documented pattern is a licence-file environment
variable and a shell script.** Research IT's guidance has users write a small
script that exports `MLM_LICENSE_FILE`, points at a MATLAB installation held on
the cluster, and runs MATLAB headless — `-nojvm -nodisplay -nosplash` for
interactive use, with `-batch` for a script.

**Two things in that guidance carry over whatever the details turn out to be.**
*MATLAB runs from inside a job, never on the login node* — the login node is a
jumpbox and computing on it is prohibited. And scripts are made executable with
`chmod` before they are run.
→ [The Login Node](../access/the-login-node.md)

**Please confirm the current paths with Research IT before building a course
around them.** Write to [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu); the
release, the installation directory and the licence file are held by the people
who maintain them rather than by this page.

## Stata

------------------------------------------------------------------------

**Stata runs in the `scipy-ml` container, for users with provisioned licensing.**
Research IT Services installs it into the member's home directory, and it is then
run from inside a container as `~/stata-se`.

*Licensing comes first and is not something the platform provides.* Holders of a
Stata licence through a department or project write to
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) to arrange the installation.

## Licensed Software Generally

------------------------------------------------------------------------

**Installing licensed software is permitted, and buying it is not our part.** The
purchase of a licence is the responsibility of the user or their sponsoring
department; Research IT Services can assist with the installation, and some
versions of some products are simply not compatible with a containerized cluster
environment.

**Ask before the purchase, not after.** Whether a given product can run
unprivileged in a container, whether its licence permits it, and whether a
network licence server is reachable from the cluster are all questions with real
answers. Write to
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) for research use, or
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) for a course.

*Licensed **data** is a separate matter with separate rules.*
→ [Restricted & Licensed Datasets](../workspaces-and-storage/datasets.md#restricted--licensed-datasets)

## Complex & Experimental Capabilities

------------------------------------------------------------------------

The cluster can host a good deal more than the standard images, and our scope of
support names these explicitly as available but outside normal support:

| Capability | What we can point to |
|---|---|
| MATLAB (Jupyter kernels or Web UI), GNU Octave | The section above |
| Spark clusters | Nothing published by us. A DSC 102 assignment is the only description anywhere of a multi-node Spark topology on this platform, and it is course material rather than documentation |
| ArcGIS integration | Nothing published by us |
| Postgres and other persistent services | Launched from Kubernetes manifests and reached by in-cluster service name → [Kubernetes](../running-jobs/kubernetes.md) |
| Background batch processing and analysis pipelines | → [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes) |
| Visual Studio Code integration | → [Remote Editor Setup](../access/remote-editor-setup.md) |
| Containers not derived from a standard image, and student-built containers | → [Building & Publishing a Custom Image](../environments/building-a-custom-image.md) |

**"Complex or experimental" is a statement about support, not about capability.**
These things work and courses use them. What changes is who does the work:
incorporating one requires the instructor or TPOC to become independently familiar
with the underlying technology and then to serve as primary support for their
students' use of it. *We are glad to give technical guidance; without an advance
agreement we cannot take on implementation or front-line support.*

**Please book a 1:1 Consultation at least one full quarter ahead** of any planned
use, to discuss feasibility.
→ [1:1 Consultation](https://ucsd-datahub.youcanbook.me/) ·
[Teaching with Datahub & DSMLP](../instructor-or-ta.md)

## Adding Software Without a Ticket

------------------------------------------------------------------------

**Anything that installs into a member's own home directory, that member can
install.** Python packages into a virtual environment with its own Jupyter
kernel, R packages into a personal library, a custom kernel.
→ [Customizing an Environment](../environments/customizing-your-environment.md)

**Anything that installs into the operating system needs a custom image.** There
is no `sudo` in a container and no flag that grants one; root is available at
image *build* time instead, which is a different moment and a different machine.
→ [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary) ·
[Building & Publishing a Custom Image](../environments/building-a-custom-image.md)

**We do not publish package lists in this documentation.** They change with every
quarterly image build. The current contents are published from the image
repository itself.
→ [Standard Images](../environments/standard-images.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
