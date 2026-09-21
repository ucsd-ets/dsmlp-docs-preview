# Customizing an Environment

**Packages can be added to a standard image without building a custom one.**
Anything that installs into a member's own home directory is available to that
member: Python packages, an R library, a private Jupyter kernel. Anything that
installs into the operating system is not.

## What Can Be Installed

------------------------------------------------------------------------

| Change | Possible without a custom image? |
|---|---|
| Add a Python package for personal use | **Yes** — into a virtual environment with its own kernel |
| Add an R package for personal use | **Yes** — into a personal R library |
| Add a Jupyter kernel | **Yes** — `ipython kernel install --user` |
| Add a system package (`apt-get`, a compiler, a system utility) | **No** — this needs a custom image |
| Change the image for a whole course | **No** — this is a custom image, or a different standard one |

## Installing Python Packages Into a Private Kernel

------------------------------------------------------------------------

**Install into a virtual environment rather than over the top of the course
environment.** Installing into the environment the course ships is how people
break it.

Open a terminal from the notebook interface (**File → New → Terminal**), then:

```bash
# create a directory and a virtual environment inside it
mkdir mykernel
python3 -m venv mykernel

# activate it; pip now refers to the virtual environment's pip
source mykernel/bin/activate
which pip

pip install ipython ipykernel
```

Install the packages themselves:

```bash
pip install scrapy
```

Then register the environment as a Jupyter kernel and leave:

```bash
# confirm ipython is the virtual environment's copy before registering
which ipython

ipython kernel install --user --name=mykernel
deactivate
```

Refresh the notebook interface. **`mykernel` now appears in the launcher**, and
a notebook created with it can import whatever was installed into it.

*Libraries installed this way are available only to notebooks using that
kernel.* A notebook on the course kernel is unaffected by anything installed
into a private one.

## Installing R Packages

------------------------------------------------------------------------

**A personal library is created on first use of RStudio**, from the RStudio
Console:

```r
dir.create("~/R")
dir.create("~/R/library")
.libPaths("~/R/library")
```

`install.packages()` then writes there rather than attempting the system
library, which is not writable.

## The Hard Boundary

------------------------------------------------------------------------

**There is no root and no `sudo`.** Containers run unprivileged, under the
member's own UID, in a per-user Kubernetes namespace, on a node shared with other
people's containers. `sudo apt-get install ...` fails by design rather than
through misconfiguration.

**The container and the login node share a filesystem.** A file written in one is
visible in the other. Root inside a container would reach across that shared
filesystem to files belonging to other people — which is why there is none.

| Not available | What works instead |
|---|---|
| `sudo` anything | Nothing needs `sudo`; work happens in the member's own home directory |
| `apt-get install` a system package | Put it in a custom image, where root *is* available at build time |
| Write to system directories | Install into a virtual environment or a personal R library |
| Reach another user's container or namespace | Share through the workspace's `public/` or `teams/` areas |

**Members keep full control of their own space.** Installing Python packages,
creating a Jupyter kernel, creating an R library, reading and writing anywhere
they own, and managing their own pods with `kubectl` all work normally.
→ [Kubernetes](../running-jobs/kubernetes.md)

**A system-level package therefore means a custom image.** Root is available
inside a Dockerfile at build time — that is where `USER root` and `apt-get`
belong — and the resulting image still runs as the member, not as root.
**Build time and run time are different moments:** root is available while the
image is being built, somewhere that is not our cluster; when that image is later
launched here, it runs unprivileged, under the member's own UID, exactly like a
standard image.

*On this platform, "I need a system package" and "I need a custom image" are the
same sentence.*
→ [Building & Publishing a Custom Image](building-a-custom-image.md)

**Course-wide needs are not per-user customizations.** A package the whole class
needs belongs in the course image rather than in 200 individual installations.

## When It Breaks

------------------------------------------------------------------------

*Installing packages with pip or conda can break a local environment.* Two
recoveries, in increasing order of severity:

**A clean notebook.** Start a notebook on the **Python3 (clean)** kernel, which
ignores everything in `.local`. If that fixes the symptom, `.local` is the
cause: moving or deleting `.local/lib` resolves many cases, and occasionally
`.local/jupyter` as well.

**The manual resetter.** At [datahub.ucsd.edu](https://datahub.ucsd.edu), open
the services dropdown and choose **manual-resetter**. It stops running servers,
signs the account out and resets its profile, *leaving files intact*.
→ [Sign-In & Session Problems](../access/sign-in-and-session-problems.md)

**Neither recovery applies to the shared course grader account.** A TA follows
up in the course support ticket instead — the grader account carries the
course's nbgrader state, and clearing its `.local` by hand can take grading with
it. → [Common Grading Failures & Recovery](../grading/grading-failures.md)

## Caveats & Limitations

------------------------------------------------------------------------

**Conda is unsettled:** see the draft note above. Until it is resolved, the
`venv` route documented here is the one we can support without qualification.

**Personal installs count against the quota:** everything above lands in the
member's home directory, which is per-user and per-workspace and is not large.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**Support for per-individual customization is limited:** minor customizations
within a standard image are a supported feature, but ITS staff cannot debug an
arbitrary package tree. Instructors and TPOCs can bring these to a 1:1
Consultation. → [Getting Help](../reference/getting-help.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
