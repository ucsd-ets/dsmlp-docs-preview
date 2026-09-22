# Software

This page covers software beyond the contents of the standard images: R and
RStudio, MATLAB and GNU Octave, Stata, other licensed software, capabilities
that ITS classes as complex or experimental, and software that members install
themselves. The standard images cover most courses and projects, receive
priority support, and are described in
[Standard Images, Tags, and Pinning](../environments/standard-images.md).

## R and RStudio

R is included in every standard image, alongside Python and Julia, and runs as a
Jupyter kernel. Entering `?command_name` in a cell displays the documentation for
a function.

### Opening RStudio

RStudio does not require a separate sign-in.

1. Start the course environment that includes RStudio.
2. Wait for the JupyterLab launcher to load.
3. Click the RStudio shortcut. RStudio opens in a new tab.

### Personal R Package Library

In a new account, `install.packages()` does not work until a personal package
library exists. Create the library once, in the RStudio Console, during the
first RStudio session:

```r
dir.create("~/R")
dir.create("~/R/library")
.libPaths("~/R/library")
```

The library is stored in the home directory and counts against its quota, as
described in
[Storage Quota](../environments/customizing-your-environment.md#storage-quota).

### RStudio and GPUs

`rstudio-notebook` derives from `datascience-notebook`, the CPU image, rather
than from `scipy-ml-notebook`, and is therefore not GPU-enabled, as described in
[Standard Images](../environments/standard-images.md#standard-images).
A course that needs both RStudio and a GPU requires a custom image or a second
environment.

See also: [Getting Help](getting-help.md)

## MATLAB, Octave & Other Complex Applications

MATLAB can be used on the platform but is not a standard feature. The ITS scope
of support classes MATLAB, as Jupyter kernels or as the Web UI, and GNU Octave
among the capabilities listed in
[Complex & Experimental Capabilities](#complex--experimental-capabilities).
These capabilities are regularly used on the platform but fall outside the
normal bounds of ITS support, and their use in a course is led by the instructor
or the Technical Point of Contact (TPOC).

### MATLAB on the Research Cluster

On the Research Cluster, Research IT documents running MATLAB from a small shell
script that sets a license-file environment variable. The script exports
`MLM_LICENSE_FILE`, points to a MATLAB installation held on the cluster, and runs
MATLAB headless: with `-nojvm -nodisplay -nosplash` for interactive use, and
with `-batch` for a script.

MATLAB runs inside a job and never on the login node, where running computation
is prohibited, as described in
[What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for).
Scripts are made executable with `chmod` before they are run.

Research IT maintains the MATLAB release, the installation directory, and the
license file. Confirm the current paths with Research IT at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) before building a course
around them.

## Stata

Stata runs in the `scipy-ml` container for users with provisioned licensing.
Research IT Services installs Stata into the member's home directory, and the
member then runs it from inside a container as `~/stata-se`.

The platform does not provide Stata licenses, and a license is required before
installation. A holder of a Stata license through a department or project
arranges the installation by writing to
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).

## Licensed Software

Installing licensed software is permitted. Purchasing the license is the
responsibility of the user or the user's sponsoring department. Research IT
Services can assist with the installation. Some versions of some products are
not compatible with a containerized cluster environment.

Before purchasing a license, confirm the following with the relevant contact:

- whether the product can run unprivileged in a container
- whether its license permits that use
- whether a network license server is reachable from the cluster

For research use, the contact is
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu). For a course, the contact
is [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

Licensed data is subject to separate rules, described in
[Restricted & Licensed Datasets](../workspaces-and-storage/datasets.md#restricted--licensed-datasets).

## Complex & Experimental Capabilities

The ITS scope of support names the following capabilities as available on the
cluster but outside normal support.

| Capability | Documentation |
|---|---|
| MATLAB (Jupyter kernels or Web UI), GNU Octave | [MATLAB, Octave & Other Complex Applications](#matlab-octave--other-complex-applications) |
| Spark clusters | ITS publishes no documentation. The only description of a multi-node Spark topology on this platform is a DSC 102 assignment, which is course material rather than documentation. |
| ArcGIS integration | ITS publishes no documentation. |
| Postgres and other persistent services | Launched from Kubernetes manifests and reached by in-cluster service name, as described in [Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md). |
| Background batch processing and analysis pipelines | [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes) |
| Visual Studio Code integration | [Remote Editor Setup](../access/remote-editor-setup.md) |
| Containers not derived from a standard image, and student-built containers | [Building & Publishing a Custom Image](../environments/building-a-custom-image.md) |

### Support Responsibilities

The complex or experimental classification concerns support, not capability.
These capabilities work, and courses use them. Incorporating one into a course
requires the instructor or TPOC to become independently familiar with the
underlying technology and then to serve as primary support for students' use of
it. ITS gives technical guidance but, without an advance agreement, does not
take on implementation or front-line support. The scope of support is published
in
[Complex Customizations & Experimental Features](../instructor-or-ta.md#complex-customizations--experimental-features).

### Feasibility Consultation

Book a 1:1 Consultation at least one full quarter before any planned use of one
of these capabilities, to discuss feasibility. Consultations are described in
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).

## Adding Software Without a Ticket

### Home Directory Installations

A member can install anything that installs into the member's own home
directory: Python packages into a virtual environment with its own Jupyter
kernel, R packages into a personal library, and a custom kernel. The procedures
are in
[Customizing an Environment](../environments/customizing-your-environment.md).

### Operating System Packages

Software that installs into the operating system requires a custom image. A
container has no `sudo` and no flag that grants it, and root is available at
image build time instead, on a different machine, as described in
[Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages).
Building an image is covered in
[Building & Publishing a Custom Image](../environments/building-a-custom-image.md).

### Package Lists

Package lists change with every quarterly image build. The current contents of
each image are published from the image repository, as described in
[Finding the Package List](../environments/standard-images.md#finding-the-package-list).
