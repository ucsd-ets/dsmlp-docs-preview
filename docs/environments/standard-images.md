# Standard Images, Tags & Pinning

**IT Services maintains three standard software images.** They cover the great
majority of courses and projects, they receive priority support, and each one is
a starting point for a custom image where it does not go far enough.
→ [Building & Publishing a Custom Image](building-a-custom-image.md)

## The Three Standard Images

------------------------------------------------------------------------

| Image | What it adds | GPU |
|---|---|---|
| **`datascience-notebook`** | Widely-used data analysis libraries from the Python, R and Julia communities. The default for most courses. | No |
| **`scipy-ml-notebook`** | Everything in `datascience-notebook`, plus CUDA/GPU tooling, TensorFlow and PyTorch. | Yes |
| **`rstudio-notebook`** | Everything in `datascience-notebook`, plus the RStudio development environment. | **No** |

**`rstudio-notebook` is not GPU-enabled.** It extends the CPU image, not the
machine-learning one. A course that needs both RStudio and GPUs cannot get there
by choosing `rstudio-notebook`, and needs a custom image or a second
environment. Please bring such a course to us.
→ [Getting Help](../reference/getting-help.md)

Reaching RStudio itself is a click in the JupyterLab launcher rather than a
separate sign-in. *Note that the first RStudio session in a new account needs a
personal package library created before `install.packages()` will work.*
→ [Customizing an Environment](customizing-your-environment.md)

## How They Inherit

------------------------------------------------------------------------

```text
datahub-base-notebook          Jupyter and common data science tooling
  └── datascience-notebook     + additional Python and R packages
        ├── scipy-ml-notebook  + CUDA, TensorFlow, PyTorch
        └── rstudio-notebook   + RStudio
```

**`datahub-base-notebook` sits below `datascience-notebook`.** It is the
smallest image we maintain and the one to derive from when build time or image
size matters. A custom image built on `scipy-ml-notebook` inherits the whole
CUDA stack whether or not the course uses it.

**A child image has everything its parent has.** If a package is in
`datascience-notebook` it is also in `scipy-ml-notebook` and
`rstudio-notebook`; the reverse does not hold.

## Names & Tags

------------------------------------------------------------------------

Images are published to the GitHub Container Registry and are named
`ghcr.io/ucsd-ets/<image>:<tag>`:

```text
ghcr.io/ucsd-ets/datascience-notebook:stable
ghcr.io/ucsd-ets/scipy-ml-notebook:2024.4-stable
```

**`:stable` follows the quarterly update; a dated tag such as
`:2024.4-stable` does not.** A workspace that must not move partway through a
term names the dated tag instead.
→ [Pinning a Workspace](#pinning-a-workspace)

*The older `ucsdets/<image>` naming still appears in published articles and in
course repositories.* Where a launch command needs a full image name, prefer the
`ghcr.io/ucsd-ets/...` form.

## Which Image a Session Runs

------------------------------------------------------------------------

**On Datahub, the workspace decides.** Its spawn menu offers one or more
configurations — an image together with CPU, RAM and GPU quantities — from which
students and instructors choose. A course commonly offers a CPU-only environment
for most of the term and a GPU environment for its project.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

**From the shell, the wrapper decides**, unless `-i` overrides it. Bare
`launch.sh` defaults to `ghcr.io/ucsd-ets/scipy-ml-notebook:stable`.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

## Finding the Package List

------------------------------------------------------------------------

**We do not publish package lists in this documentation**; they change with
every quarterly image build. The current contents are published from the image
repository:

- The [Stable Tag wiki page](https://github.com/ucsd-ets/datahub-docker-stack/wiki/Stable-Tag)
  lists the maintained images; each has a manifest linking to its conda and
  system package versions.
- The Dockerfile each image was built from is under
  [`datahub-docker-stack/images`](https://github.com/ucsd-ets/datahub-docker-stack/tree/main/images).
  This is also where the CUDA toolkit version in `scipy-ml-notebook` is
  recorded.

*A package missing from a standard image is a customization question rather than
a lookup.* → [Customizing an Environment](customizing-your-environment.md)

## The Quarterly Rebuild

------------------------------------------------------------------------

**Our standard images are rebuilt every quarter.** New package versions arrive,
old ones go, and behaviour occasionally changes with them. An assignment
validated in week 2 against one version of a library can fail against the next.

**A workspace may therefore pin its image**, so that a quarterly update does not
move a class to different software partway through a term. Members stay on the
build the course tested until a move is requested.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

| Tag form | Behaviour |
|---|---|
| `:stable` | Follows the quarterly update. Always the current build. |
| A dated tag, e.g. `:2024.4-stable` | Fixed. That build, until a different one is named. |
| A course image branch tag, e.g. `:wi24` | Rebuilt on every push to that branch. **Not fixed.** |
| A course image git tag, e.g. `:fa24` | Fixed at the tagged commit. |

**A branch tag is not a pin.** The branch tag is overwritten by the next push,
so an image that is "pinned to `wi24`" still changes whenever somebody commits
to `wi24`. To freeze a build, create a git tag and ask that the course use it.
→ [Building & Publishing a Custom Image](building-a-custom-image.md)

## Pinning a Workspace

------------------------------------------------------------------------

**Ask us by ticket**, naming the workspace and the exact image and tag it should
serve. Container tags are a system-side course setting, adjusted the same way as
resource limits and disk quotas.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

**Pin before instruction begins**, during the setup window in which assignments
are tested and validated in any case. *Pinning after students have started is
possible, but it changes their environment a second time rather than sparing
them a change.*
→ [When Access Starts & Ends](../access/when-access-starts-and-ends.md#instructors-tas--course-staff)

**From the shell, a fixed tag is the pin.** A command-line launch names the image
directly:

```bash
launch.sh -i ghcr.io/ucsd-ets/datascience-notebook:2024.4-stable
```

*This affects only that account's own launches.* It does not change what the
workspace hands to anyone else, and it is not a substitute for asking for a
course pin.

## Caveats & Limitations

------------------------------------------------------------------------

**No GPU in the RStudio image:** `rstudio-notebook` derives from
`datascience-notebook`.

**Obsolete GPU inventories are still in circulation:** a `cuda.md` file in the
`ucsd-ets/dsc200-notebook` repository publishes a table of GPU models, counts
and node names dated **Fall 2020**. It is not current, and work should not be
sized from it. The current model is GPU *classes*, requested by label.
→ [GPU Classes](../gpu-access/gpu-classes.md)

**A custom CUDA image is rarely worth building:** `scipy-ml-notebook` already
carries CUDA with a matching PyTorch and TensorFlow. A custom CUDA stack has to
stay compatible with the driver on the node.
→ [Building & Publishing a Custom Image](building-a-custom-image.md)

**Quarterly updates move `:stable`:** courses that need a fixed environment for
the duration of a term should ask for a pinned tag rather than assume stability.

**A pin freezes the bad along with the good:** a pinned image stops receiving
package updates, including security fixes to the software inside it. A pin is for
a term, not indefinitely.

**Pinning does not freeze the platform:** a pin fixes the image; the node, its
drivers and the cluster around it continue to be maintained. *This matters most
for GPU work, where the driver on the node is not part of the image.*

**Moving off a pin needs re-validation:** a move to a newer base image calls for
assignments to be re-validated against it. Assistance with maintenance following
a quarterly image update is one of the things a 1:1 Consultation is for.
→ [Getting Help](../reference/getting-help.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
