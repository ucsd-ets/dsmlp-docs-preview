# Standard Images, Tags, and Pinning

This page covers the standard software images maintained by IT Services (ITS),
their registry names and tags, and pinning a workspace to a fixed image.

## Standard Images

The canonical list of the images ITS maintains, with their current tags, is the
[`ucsd-ets/datahub-docker-stack`](https://github.com/ucsd-ets/datahub-docker-stack)
repository. Three standard images cover most courses and projects, receive
priority support, and serve as the starting point for a custom image. See
[Building & Publishing a Custom Image](building-a-custom-image.md).

| Image | What it adds | GPU |
|---|---|---|
| `datascience-notebook` | Widely used data analysis libraries from the Python, R and Julia communities. The default for most courses. | No |
| `scipy-ml-notebook` | Everything in `datascience-notebook`, plus CUDA/GPU tooling, TensorFlow and PyTorch. | Yes |
| `rstudio-notebook` | Everything in `datascience-notebook`, plus the RStudio development environment. | No |

### RStudio and GPU Support

`rstudio-notebook` is not GPU-enabled. It extends the CPU image,
`datascience-notebook`, not the machine-learning image, `scipy-ml-notebook`. A
course that needs both RStudio and GPUs cannot meet that need by choosing
`rstudio-notebook`. It requires a custom image or a second environment.
Instructors of such a course contact ITS through
[Getting Help](../reference/getting-help.md).

### Opening RStudio

RStudio opens from the JupyterLab launcher and does not require a separate
sign-in. The first RStudio session in a new account requires a personal package
library before `install.packages()` works. The procedure is in
[Installing R Packages](customizing-your-environment.md#installing-r-packages).

## Image Inheritance

```text
quay.io/jupyter/datascience-notebook   Jupyter's Python, R and Julia image
  └── datascience-notebook             + tools, packages and nbgrader
        ├── scipy-ml-notebook          + CUDA, TensorFlow, PyTorch
        └── rstudio-notebook           + RStudio
```

A child image contains everything in its parent. A package in
`datascience-notebook` is also in `scipy-ml-notebook` and `rstudio-notebook`.
The reverse does not hold.

`datascience-notebook` is built on the Jupyter project's
`quay.io/jupyter/datascience-notebook` image, and is the base of the other two
standard images. It is the smallest standard image, and the base to derive
from when build time or image size matters. A custom image built on
`scipy-ml-notebook` inherits the whole CUDA stack whether or not the course uses
it.

### Custom CUDA Images

`scipy-ml-notebook` already carries CUDA with a matching PyTorch and TensorFlow.
A custom CUDA image is rarely needed. A custom CUDA stack must stay compatible
with the driver on the node.
[Building & Publishing a Custom Image](building-a-custom-image.md) covers custom
image builds.
[CUDA Versions](../gpu-access/gpu-hardware.md#cuda-versions) gives the CUDA
versions DSMLP supports.

## Image Names and Tags

Images are published to the GitHub Container Registry and are named
`ghcr.io/ucsd-ets/<image>:<tag>`:

```text
ghcr.io/ucsd-ets/datascience-notebook:stable
ghcr.io/ucsd-ets/scipy-ml-notebook:2024.4-stable
```

The `:stable` tag follows each update. A dated tag such as `:2024.4-stable`
does not. A workspace that must not change partway through a term uses the
dated tag. See [Pinning a Workspace](#pinning-a-workspace).

### Dated Tags

A dated tag names the year and the quarter of the build: `2024.4-stable` is the
Fall 2024 image, and `2023.2-stable` the Spring 2023 image. The
[`datahub-docker-stack`](https://github.com/ucsd-ets/datahub-docker-stack)
repository lists the tags currently published.

### Legacy Image Names

The older `ucsdets/<image>` naming still appears in published articles and in
course repositories. Where a launch command needs a full image name, prefer the
`ghcr.io/ucsd-ets/...` form.

`datahub-base-notebook`, which some published articles and course repositories
name as a base image, is no longer built or updated. Derive from
`datascience-notebook` instead.

## Image Selection for a Session

The image a session runs depends on how the session is launched.

### Datahub Sessions

On Datahub, the workspace determines the image. Its spawn menu offers one or
more configurations, each an image together with CPU, RAM and GPU quantities,
from which students and instructors choose. A course commonly offers a CPU-only
environment for most of the term and a GPU environment for its project.
[What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)
describes workspace settings.

### Command-Line Sessions

From the shell, the wrapper script determines the image unless `-i` overrides
it. Bare `launch.sh` defaults to `ghcr.io/ucsd-ets/scipy-ml-notebook:stable`.
[`launch.sh` Reference](../running-jobs/launch-sh-reference.md) describes
wrapper scripts and flags.

## Finding the Package List

Package lists change with every image build. The current contents are
published from the image repository:

- The [Stable Tag wiki page](https://github.com/ucsd-ets/datahub-docker-stack/wiki/Stable-Tag)
  lists the maintained images. Each has a manifest linking to its conda and
  system package versions.
- The Dockerfile each image was built from is under
  [`datahub-docker-stack/images`](https://github.com/ucsd-ets/datahub-docker-stack/tree/main/images).
  This is also where the CUDA toolkit version in `scipy-ml-notebook` is
  recorded.

For a package or CUDA version that no published image carries, write to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).
[Customizing an Environment](customizing-your-environment.md) covers adding a
package that a standard image lacks.

### Obsolete GPU Inventory

A `cuda.md` file in the `ucsd-ets/dsc200-notebook` repository publishes a table
of GPU models, counts and node names dated Fall 2020. It is not current. Do not
size work from it. GPUs are requested by class label. See
[GPU Classes](../gpu-access/gpu-classes.md).
[GPU Hardware & CUDA](../gpu-access/gpu-hardware.md) gives the specifications of
the cards and slices that can back a class.

## Image Updates

ITS generally updates the standard images ahead of Fall quarter, and again as
needed during the academic year. New package versions are added, old ones are
removed, and behavior occasionally changes with them. An assignment validated in
week 2 against one version of a library can fail against the next.

A workspace may pin its image so that an update does not move a class to
different software partway through a term. Members stay on the build the
course tested until a move is requested. A course that needs a fixed environment
for the duration of a term requests a pinned tag rather than relying on
`:stable`. See [Pinning a Workspace](#pinning-a-workspace).
[What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md)
describes workspace settings.

### Tag Behavior

| Tag form | Behavior |
|---|---|
| `:stable` | Follows each update. Always the current build. |
| A dated tag, e.g. `:2024.4-stable` | Fixed. That build, until a different one is named. |
| A course image branch tag, e.g. `:wi24` | Rebuilt on every push to that branch. Not fixed. |
| A course image git tag, e.g. `:fa24` | Fixed at the tagged commit. |

### Course Image Branch Tags

> [!WARNING]
> A branch tag does not pin an image. The next push overwrites the branch tag,
> so an image set to `wi24` still changes whenever a commit is pushed to `wi24`.

To freeze a course image build, create a git tag and ask that the course use it.
[Course Images](building-a-custom-image.md#course-images) covers course image
branches and tags.

## Pinning a Workspace

Container tags are a system-side course setting, adjusted by ticket in the same
way as resource limits and disk quotas. ITS staff make the change. Email to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) opens a ticket. To pin a
workspace:

1. Identify the workspace and the exact image and tag it should serve.
2. Submit a ticket naming both, before instruction begins, during the setup
   window in which assignments are tested and validated.

[Administrative Requests](../reference/getting-help.md#administrative-requests)
describes the ticket process.
[Instructors, TAs & Course Staff](../access/when-access-starts-and-ends.md#instructors-tas--course-staff)
describes course setup timing.
A pin applied after students have started is possible, but it changes their
environment a second time.

### Pinning from the Command Line

A command-line launch names the image directly, so a fixed tag pins that launch:

```bash
launch.sh -W DSC40_FA26_001 -i ghcr.io/ucsd-ets/datascience-notebook:2024.4-stable
```

This affects only that account's own launches. It does not change the image the
workspace serves to anyone else, and it does not replace a course pin.

### Pin Duration and Security Updates

A pinned image stops receiving package updates, including security fixes to the
software inside it. A pin applies for a term, not indefinitely.

### Platform Maintenance on a Pinned Image

A pin fixes the image only. The node, its drivers and the cluster around it
continue to be maintained. For GPU work, the driver on the node is not part of
the image and is not fixed by a pin.

### Moving Off a Pin

A move to a newer base image requires assignments to be re-validated against
it. Assistance with maintenance following an image update is within
the scope of a 1:1 Consultation. See
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).
