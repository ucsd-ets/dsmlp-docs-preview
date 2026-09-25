# Customizing an Environment

Packages can be added to a standard image without building a custom one.
Anything installed into a member's own home directory, such as Python packages,
an R library, or a private Jupyter kernel, is available to that member; anything
that installs into the operating system requires a custom image.

## What Can Be Installed

| Change | Possible without a custom image |
|---|---|
| Add a Python package for personal use | Yes, into a virtual environment with its own kernel |
| Add an R package for personal use | Yes, into a personal R library |
| Add a Jupyter kernel | Yes, with `ipython kernel install --user` |
| Add a system package (`apt-get`, a compiler, a system utility) | No. A custom image is required. |
| Change the image for a whole course | No. This requires a custom image or a different standard image. |

### Storage Quota

Personal installs are written to the member's home directory, which is per-user
and per-workspace and is not large. They count against the quota described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

Machine-learning packages in particular can be very large. Build a custom image
rather than installing a private copy of PyTorch, the CUDA libraries, or
similar packages. See
[Building & Publishing a Custom Image](building-a-custom-image.md).

## Installing Python Packages Into a Private Kernel

Install Python packages into a virtual environment with its own Jupyter kernel,
not into the environment the course ships. Installing into the course
environment can break it. ITS supports virtual environments made with
`python3 -m venv`.

1. Open a terminal from the notebook interface (**File → New → Terminal**).

2. Create and activate a virtual environment, then install `ipython` and
   `ipykernel` into it:

    ```bash
    # create a directory and a virtual environment inside it
    mkdir mykernel
    python3 -m venv mykernel

    # activate it; pip now refers to the virtual environment's pip
    source mykernel/bin/activate
    which pip

    pip install ipython ipykernel
    ```

3. Install the packages into the virtual environment:

    ```bash
    pip install scrapy
    ```

4. Register the environment as a Jupyter kernel, then deactivate it:

    ```bash
    # confirm ipython is the virtual environment's copy before registering
    which ipython

    ipython kernel install --user --name=mykernel
    deactivate
    ```

5. Refresh the notebook interface. `mykernel` appears in the launcher, and a
   notebook created with it can import the packages installed into it.

Libraries installed this way are available only to notebooks using that kernel.
A notebook on the course kernel is unaffected by anything installed into a
private one.

### Conda Environments

A member may build a conda environment instead, for example where the course
staff direct it, but ITS does not support conda environments, because they can
conflict with the image's own conda environment. The image's conda environment
is read-only, so `conda install` into it does not work.

An environment used as a Jupyter kernel, whether built with `venv` or with
conda, must be compatible with the versions of JupyterLab and
`jupyterhub-singleuser` that the session runs.

## Installing R Packages

On first use of RStudio, create a personal library from the RStudio Console:

```r
dir.create("~/R")
dir.create("~/R/library")
.libPaths("~/R/library")
```

`install.packages()` then writes to the personal library instead of the system
library, which is not writable.

## Root Access and System Packages

Containers run unprivileged, under the member's own UID, in a per-user
Kubernetes namespace, on a node shared with other users' containers. Root access
and `sudo` are not available. `sudo apt-get install ...` fails by design, not
through misconfiguration. A `sudo` command prints:

```text
sudo: The "no new privileges" flag is set, which prevents sudo from running as root.
```

### Unavailable Operations and Alternatives

| Unavailable operation | Alternative |
|---|---|
| Any `sudo` command | Work in the member's own home directory, which requires no `sudo` |
| `apt-get install` a system package | Install it in a custom image, where root is available at build time |
| Writing to system directories | Install into a virtual environment or a personal R library |
| `conda install` into the image's conda environment, which is read-only | Install into a virtual environment |
| Reaching another user's container or namespace | Share through the workspace's `public/` or `teams/` areas |

### Operations Available Without Root

Members keep full control of their own space. Installing Python packages,
creating a Jupyter kernel, creating an R library, reading and writing anywhere
the member owns, and managing the member's own pods with `kubectl` all work
normally. Direct `kubectl` use is covered in
[Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md).

### System Packages and Custom Images

A system-level package requires a custom image. Root is available inside a
Dockerfile at build time, which is where `USER root` and `apt-get` belong. The
image is built outside the cluster. When the image is later launched on the
cluster, it runs unprivileged under the member's own UID, the same as a standard
image. Building and publishing an image is covered in
[Building & Publishing a Custom Image](building-a-custom-image.md).

### Course-Wide Packages

A package that a whole course needs belongs in the course image, not in
individual per-user installations.

## Recovering a Broken Environment

Installing packages with pip or conda can break a local environment. Two
recoveries apply, in increasing order of severity: a clean kernel and the manual
resetter.

### Clean Kernel

Start a notebook on the **Python3 (clean)** kernel, which ignores everything in
`.local`. If the clean kernel resolves the symptom, the cause is in `.local`.
Moving or deleting `.local/lib` resolves many cases. Occasionally `.local/jupyter`
must be moved or deleted as well.

### Manual Resetter

The manual resetter, described in
["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed), stops
the account's running servers, signs the account out, and resets its profile
while leaving files intact.

### Course Grader Account

Neither recovery applies to the shared course grader account. For that account,
a TA follows up in the course support ticket instead.

> [!WARNING]
> The grader account carries the course's nbgrader state. Clearing its `.local`
> by hand can destroy that state.

Grader account failures are covered in
[Common Grading Failures & Recovery](../grading/grading-failures.md).

### Support for Personal Customizations

Minor customizations within a standard image are a supported feature. ITS staff
cannot debug an arbitrary package tree. Instructors and Technical Points of
Contact (TPOCs) can bring such problems to a 1:1 Consultation, described in
[Getting Help](../reference/getting-help.md).
