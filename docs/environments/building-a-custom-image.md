# Building & Publishing a Custom Image

This page covers building, publishing, and testing a custom image, which a
course builds when a standard image does not meet its needs, most often because
the course requires an operating-system package that cannot be installed from
inside a running container
([Root Access and System Packages](customizing-your-environment.md#root-access-and-system-packages)).
A Python or R package for personal use does not require a custom image. See
[Customizing an Environment](customizing-your-environment.md).

## Choosing a Base Image

Derive a custom image from a standard image. A derived image inherits a working
Jupyter installation, a working kernel set, and the platform's conventions.
[Standard Images](standard-images.md#standard-images) lists the contents of each
standard image.

| Start from | When |
|---|---|
| `datascience-notebook` | The custom image needs neither CUDA nor RStudio. This base is the smallest standard image and the fastest to build, with the standard Python, R, and Julia analysis stack. |
| `scipy-ml-notebook` | The custom image needs CUDA, TensorFlow, or PyTorch. |
| `rstudio-notebook` | The custom image needs RStudio. This base is not GPU-enabled ([RStudio and GPU Support](standard-images.md#rstudio-and-gpu-support)). |

### Base Image and Build Time

Where build time matters, derive from `datascience-notebook` rather than
`scipy-ml-notebook`. An image built on `scipy-ml-notebook` inherits the entire
CUDA stack, which adds to the time of every build during development. See
[Image Inheritance](standard-images.md#image-inheritance).

### Custom CUDA Toolkits

`scipy-ml-notebook` already carries a CUDA toolkit with a matching PyTorch and
TensorFlow. A custom CUDA toolkit must be kept compatible with the driver on the
node indefinitely. The `scipy-ml-notebook` Dockerfile records the toolkit
version that image carries, and
[CUDA Versions](../gpu-access/gpu-hardware.md#cuda-versions) gives the versions
DSMLP supports.

### Experimental Images

An image not derived from a standard image is an experimental case, as is a
student-built container of any derivation. Such images run on the platform, but
they require substantially more of the builder's time and are outside the
standard support tier. Contact ITS through
[Getting Help](../reference/getting-help.md) at least a quarter in advance.

## The Dockerfile

The example repository contains an annotated Dockerfile that serves as the
model for a custom image:

```dockerfile
ARG BASE_CONTAINER=ghcr.io/ucsd-ets/datascience-notebook:stable
FROM $BASE_CONTAINER

# become root to install system packages
USER root

# the base image ships without apt package lists, so update them in the same step
RUN apt-get update && \
    apt-get -y install htop && \
    rm -rf /var/lib/apt/lists/*

# drop back to the notebook user for everything else
USER jovyan

RUN pip install --no-cache-dir networkx scipy
```

### Root Access During the Build

Root is available only under `USER root` in the Dockerfile. Switch back to the
notebook user after the root steps, as the example does with `USER jovyan`. A
container started from the image runs as the member who launched it, not as
root
([Root Access and System Packages](customizing-your-environment.md#root-access-and-system-packages)).

### System Packages

Install system packages with `apt-get` under `USER root`. Put `apt-get update`
at the start of the `RUN` step that runs `apt-get install`. The standard images
ship without apt package lists, so `apt-get install` alone fails with
`E: Unable to locate package` for any package not already installed. End the
step by removing `/var/lib/apt/lists/*`, which keeps the lists out of the image.

### Python Packages

Prefer `pip` to `conda`. pip resolves dependency conflicts more leniently and is
substantially faster. Where a conda package is unavoidable, install conda
packages first and pip packages after them. To install a list of packages from a
file, use `pip install --no-cache-dir -r requirements.txt`.

### R Packages

Prefer `install.packages()` to conda for R packages. Conda packages increase
build time sharply. For a package not on CRAN, fall back to
`conda install -c conda-forge ...`.

### Image Size and Install Time

Each `RUN` step becomes a layer. Concatenate `RUN` steps to keep the image
small. If a conda install takes an unreasonable amount of time, `mamba` performs
the same installation faster.

An image larger than about 15 GB becomes unwieldy to pull and run. The hard
limit is 30 GB.

### Additional Kernels

To offer a second environment as its own notebook kernel, create it as a conda
environment and expose it with `nb_conda_kernels`.

## Building & Publishing

Publish the image to the GitHub Container Registry with GitHub Actions. The
workflow in the example repository, `.github/workflows/docker.yml`, builds the
image on each push and tags it with the branch name. A push to `main` produces
`...:main`.

1. Commit the changes and push them.
2. Follow the workflow run under the repository's **Actions** tab.
3. After a successful run, find the image under **Packages**.

### Public Images

The published image must be public. ITS does not manage credentials for
pulling a private custom image. Publishing from a public GitHub repository is
the simplest way to get a public image, but the repository itself does not have
to be public if the image is.

### Local Builds

Where possible, also build the image locally. A local build and shell give a far
shorter debugging cycle than waiting for a hosted build:

```bash
docker build -t <image-fullname> .
docker run --rm -it <image-fullname> /bin/bash
```

### Failed Builds

Debug a failed build from the last step Docker completed. The build output
prints an intermediate image ID after each successful step. A shell in that
image shows the state the failing command started from.

Two mistakes account for most build failures:

- An install command without `-y`, which waits indefinitely at a prompt.
- Windows CRLF line endings in a file the build reads. `dos2unix` corrects the
  line endings.

`E: Unable to locate package` appears when the `RUN` step does not start with
`apt-get update`, and when the package name is wrong. See
[System Packages](#system-packages).

## Course Images

ITS configures the repository and build process for a course image.

### Requesting a Course Image

Request a course image in the Specialized Instructional Computing Course Request
form, or by updating the course's support ticket. Include the packages to be
added and the email addresses of everyone who should be able to maintain the
repository. See [Requesting a Course](../instructor-or-ta.md#requesting-a-course).

### Branches and Docker Tags

Branches correspond to Docker tags. A push to a `wi24` branch updates
`{image}:wi24`. Updating to a newer base image is a one-line change:

```dockerfile
FROM ghcr.io/ucsd-ets/datascience-notebook:2024.4-stable
```

### Development Branches

1. Create a `dev` or `test` branch and commit to it. The build publishes the
   branch's tag, such as `{image}:test`.
2. Test the branch image. See
   [Testing a Custom Image on DSMLP](#testing-a-custom-image-on-dsmlp).
3. When the image works, open a pull request into the branch the course uses.
4. Have a team member review the pull request.
5. Merge the pull request. The merge rebuilds the production tag.

### Preserving a Build with a Git Tag

A branch tag is overwritten on every push. A git tag such as `fa24` freezes that
build, and the course can then be pointed at it. See
[Pinning a Workspace](standard-images.md#pinning-a-workspace).

### Instructor and ITS Responsibilities

For course-specific customization, the instructor or a designated Technical
Point of Contact leads installation, configuration, and student use. ITS staff
support this work through 1:1 Consultation rather than by building the image.
See
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation).

## Testing a Custom Image on DSMLP

From the login node, launch the custom image into the course workspace:

```bash
launch.sh -i <image>:<tag> -P Always -W <workspace-id>
```

Take the workspace ID from `workspace --list` rather than constructing it
([Listing Workspace IDs](../workspaces-and-storage/what-a-workspace-is.md#listing-workspace-ids)).

The launch prints a URL. Open it and exercise the features the course depends
on. When a launch times out or fails, `kubectl logs <pod-name>` is the first
place to look
([Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md)).

### Forcing a Fresh Pull

`-P Always` forces a fresh pull. Without it, the node may run a cached copy of
an older build. Remove the flag once development is finished. `-P` takes
`Always`, `IfNotPresent`, or `Never`, spelled exactly so. See
[Image Pull Policy](../running-jobs/launch-sh-reference.md#image-pull-policy).

### First Pull and Node Reuse

A large image must be downloaded to the node a session is placed on before
anything in the session starts, so the first launch on a node is slow. A second
launch on the same node does not download the image again. While iterating,
reuse one node with `-n` and a bare node number, for example `-n 30`, in a
session launched without a booking. Do not pin a node for a session that runs
under a booking; see [Node Selection](../running-jobs/launch-sh-reference.md#node-selection).

GitHub often throttles the first download of a new image into the UCSD image
cache. If a launch reports an error pulling the image, try again in an hour or
two.

### Pulling a Large Image Ahead of a Session

A Datahub session or an interactive launch can time out while a large image is
still downloading. A batch job that only runs `sleep 10` lets the download
finish without either timeout. `-B` queues the job and returns without waiting
for it:

```bash
launch.sh -i <image>:<tag> -W <workspace-id> -B -- sleep 10
```

The pull has finished when `kubectl get pods` shows the job as `Completed`. The
pull also fills the UCSD image cache, so a session placed on any node then
downloads the image from campus rather than from GitHub. That download is
faster but not instant. Then launch the session as usual.

### Replacing the Notebook Server with a Shell

A final `CMD ["/bin/bash"]` in the Dockerfile suppresses the notebook server
and starts a plain shell instead. A service in the pod is still reachable with
`kubectl port-forward pods/<POD_NAME> <PORT>:8888`. See
[Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service).

### Final Test from Datahub

After the production tag is rebuilt, test the image once more from the
**Launch your Environment** spawn page on Datahub, which is the route students
use.
