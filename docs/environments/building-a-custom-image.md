# Building & Publishing a Custom Image

This page covers building, publishing, and testing a custom image, which a
course builds when a standard image does not meet its needs, most often because
the course requires an operating-system package that cannot be installed from
inside a running container
([Root Access and System Packages](customizing-your-environment.md#root-access-and-system-packages)).
A Python or R package for personal use does not require a custom image and is
covered in [Customizing an Environment](customizing-your-environment.md).

## Choosing a Base Image

Derive a custom image from a standard image. A derived image inherits a working
Jupyter installation, a working kernel set, and the platform's conventions. The
contents of each standard image are listed in
[Standard Images](standard-images.md#standard-images).

| Start from | When |
|---|---|
| `datahub-base-notebook` | A small, well-defined set of tools is being added. It is the smallest image ITS publishes and the fastest to build. |
| `datascience-notebook` | The standard Python, R, and Julia analysis stack is wanted beneath the additions. |
| `scipy-ml-notebook` | CUDA, TensorFlow, or PyTorch is required. |
| `rstudio-notebook` | RStudio is required. The image is not GPU-enabled ([RStudio and GPU Support](standard-images.md#rstudio-and-gpu-support)). |

### Base Image and Build Time

Where build time matters, derive from the smaller base. An image built on
`scipy-ml-notebook` inherits the entire CUDA stack, which adds to the time of
every build during development.

### Custom CUDA Toolkits

`scipy-ml-notebook` already carries a CUDA toolkit with a matching PyTorch and
TensorFlow. A custom CUDA toolkit must be kept compatible with the driver on the
node indefinitely. The supported CUDA version is recorded in the
`scipy-ml-notebook` Dockerfile.

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

RUN apt-get -y install htop

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

## Course Images

ITS configures the repository and build process for a course image.

### Requesting a Course Image

Request a course image in the course request or by updating the course's
support ticket. Include the packages to be added and the email addresses of
everyone who should be able to maintain the repository.

### Branches and Docker Tags

Branches correspond to Docker tags. A push to a `wi24` branch updates
`{image}:wi24`. Updating to a newer base image is a one-line change:

```dockerfile
FROM ghcr.io/ucsd-ets/datascience-notebook:2024.4-stable
```

### Development Branches

1. Create a `dev` or `test` branch and commit to it. The build publishes the
   branch's tag, such as `{image}:test`.
2. Test the branch image as described in
   [Testing a Custom Image on DSMLP](#testing-a-custom-image-on-dsmlp).
3. When the image works, open a pull request into the branch the course uses.
4. Have a team member review the pull request.
5. Merge the pull request. The merge rebuilds the production tag.

### Preserving a Build with a Git Tag

A branch tag is overwritten on every push. A git tag such as `fa24` freezes that
build, and the course can then be pointed at it, as described in
[Pinning a Workspace](standard-images.md#pinning-a-workspace).

### Instructor and ITS Responsibilities

For course-specific customization, the instructor or a designated Technical
Point of Contact leads installation, configuration, and student use. ITS staff
support this work through 1:1 Consultation, described in
[Support & Technical Consultation](../instructor-or-ta.md#support--technical-consultation),
rather than by building the image.

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
an older build. Remove the flag once development is finished.

### First Pull and Node Reuse

A large image must be downloaded to the node a session is placed on before
anything in the session starts, so the first launch on a node is slow. A second
launch on the same node does not download the image again. While iterating,
reuse one node with `-n` and a bare node number, for example `-n 30`.

### Replacing the Notebook Server with a Shell

A final `CMD ["/bin/bash"]` in the Dockerfile suppresses the notebook server
and starts a plain shell instead. A service in the pod is still reachable with
`kubectl port-forward pods/<POD_NAME> <PORT>:8888`, as described in
[Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service).

### Final Test from Datahub

After the production tag is rebuilt, test the image once more from the
**Launch your Environment** spawn page on Datahub, which is the route students
use.
