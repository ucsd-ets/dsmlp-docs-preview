# Building & Publishing a Custom Image

**A custom image is what a course builds when a standard image does not go far
enough** — most often when the course needs an operating-system package, which
cannot be installed from inside a running container.
→ [The Hard Boundary](customizing-your-environment.md#the-hard-boundary)

*A Python or R package for personal use needs no custom image.*
→ [Customizing an Environment](customizing-your-environment.md)

## Choosing a Base Image

------------------------------------------------------------------------

**Derive from a standard image.** An image built on one of ours inherits a
working Jupyter, a working kernel set, and the platform conventions the rest of
this documentation assumes. An image built from scratch is an experimental case
and carries a much heavier support burden.

| Start from | When |
|---|---|
| `datahub-base-notebook` | A small, well-defined set of tools is being added. The smallest image we publish, and the fastest to build. |
| `datascience-notebook` | The standard Python/R/Julia analysis stack is wanted underneath the additions. |
| `scipy-ml-notebook` | CUDA, TensorFlow or PyTorch is genuinely needed. |
| `rstudio-notebook` | RStudio is needed. *It is not GPU-enabled.* |

**Prefer the smaller base where build time matters.** Building on
`scipy-ml-notebook` inherits the entire CUDA stack, and every build during
development pays for it.
→ [Standard Images and What Is in Them](standard-images.md)

## The Dockerfile

------------------------------------------------------------------------

The example repository ships an annotated Dockerfile whose shape is the one to
copy:

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

**`USER root` is the only place root is available.** Switch back to the notebook
user afterwards; the container still runs as the member who launched it, not as
root.

**Prefer `pip` to `conda`.** pip resolves conflicts more forgivingly and is
substantially faster. Where a conda package is unavoidable, install conda
packages first and pip packages after. `pip install --no-cache-dir -r
requirements.txt` reads the list from a file instead.

**For R, prefer `install.packages()` over conda** — conda packages inflate build
time sharply. `conda install -c conda-forge ...` is the fallback for anything
not on CRAN.

**Keep the image small.** Concatenate `RUN` steps, since each one becomes a
layer; if a conda install takes an unreasonable amount of time, `mamba` does the
same job faster. To offer a second environment as its own notebook kernel,
create it as a conda environment and expose it with `nb_conda_kernels`.

## Building & Publishing

------------------------------------------------------------------------

**Publish with GitHub Actions to the GitHub Container Registry.** The example
repository's workflow lives at `.github/workflows/docker.yml`, builds on push,
and **tags the image with the branch name** — pushing to `main` produces
`...:main`. Commit, push, then watch the run under the repository's **Actions**
tab; a successful run leaves the image under **Packages**.

**Build locally as well where possible.** `docker build -t <image-fullname> .`
followed by `docker run --rm -it <image-fullname> /bin/bash` gives a far shorter
debugging loop than waiting on a hosted build. *When a build fails, start from
the last step Docker ran* — the output prints an intermediate image ID after
each successful step, and a shell in that image shows the state the failing
command was working from. Two mistakes account for most failures: an install
command without `-y`, which then waits forever for a prompt, and Windows CRLF
line endings in a file the build reads, which `dos2unix` fixes.

## Course Images

------------------------------------------------------------------------

**Ask for a course image with the course request**, or by updating the course's
support ticket. Please include the packages to be added and the email addresses
of everyone who should be able to maintain the repository.

**We configure the repository and its build process.** Branches correspond to
Docker tags: pushing to a `wi24` branch updates `{image}:wi24`. Updating to a
newer base image is a one-line change:

```dockerfile
FROM ghcr.io/ucsd-ets/datascience-notebook:2024.4-stable
```

**Develop on a branch.** Create `dev` or `test`, commit there, and let the build
publish `{image}:test`. When it works, open a pull request into the branch the
course actually uses, have a team member review it, and merge — that rebuilds
the production tag.

**Preserving a version is a git tag.** A branch tag is overwritten on every
push; a tag such as `fa24` freezes that build, and the course can then be
pointed at it. → [Pinning a Workspace](standard-images.md#pinning-a-workspace)

## Testing It on DSMLP

------------------------------------------------------------------------

From the login node, a custom image launches into the course workspace:

```bash
launch.sh -i <image>:<tag> -P Always -W <workspace-id>
```

**`-P Always` forces a fresh pull.** Without it the node may run a cached copy
of an older build. Drop the flag once development is finished.

*Run `workspace --list` for the workspace ID; do not try to construct it.*
→ [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

The launch prints a URL — open it and exercise the features the course depends
on. When a launch times out or fails, `kubectl logs <pod-name>` is the first
place to look.
→ [Kubernetes](../running-jobs/kubernetes.md)

*Two things shorten the loop.* The first launch on a node downloads the image
and a second on the same node does not, so `-n` with a bare node number
(e.g. `-n 30`) is worth reusing while iterating. And a final
`CMD ["/bin/bash"]` in the Dockerfile suppresses the notebook server in favour
of a plain shell; a service in the pod is still reachable with
`kubectl port-forward pods/<POD_NAME> <PORT>:8888`.
→ [Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service)

Once the production tag is rebuilt, test it one last time the way students will
meet it: from the **Launch your Environment** spawn page on Datahub.

## Caveats & Limitations

------------------------------------------------------------------------

**Instructors lead, we assist:** for course-specific customization the
instructor or a designated Technical Point of Contact takes the lead on
installation, configuration and student use; ITS staff support this through 1:1
Consultation rather than by building the image. *Note that consultation
availability is limited in the final weeks of a term.*

**Not deriving from a standard image is an experimental case**, as are
student-built containers of any derivation. They run on the platform, but they
need substantially more of the builder's time and sit outside the standard
support tier. Please talk to us at least a quarter ahead.

**A first pull is slow:** a large image must be downloaded to whichever node a
session lands on before anything starts.

**CUDA is its own project:** `scipy-ml-notebook` already carries a CUDA toolkit
with a matching PyTorch and TensorFlow. Building a custom one means keeping that
toolkit compatible with the driver on the node, indefinitely. The supported
version is recorded in the `scipy-ml-notebook` Dockerfile, not here.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
