# Error Messages: Symptom → Cause → Fix

Most failures on this platform have one of about a dozen causes, and the message
displayed rarely names the cause behind it. This page is organized by where the
problem appears.

*Three things reported as errors are not errors at all: an idle-culled session, a
`DeadlineExceeded` container, and a refused `sudo`. Each is the system working as
designed, and each is covered below.*

## Signing In & Starting a Session

------------------------------------------------------------------------

| Symptom | Cause | Fix |
|---|---|---|
| The campus sign-on page returns repeatedly | A campus credential or Duo problem, or another identity signed in to the same browser | Sign out of the others, or use a private window. *Datahub uses standard UCSD single sign-on, so a persistent failure here is one for the [ITS Service Desk](https://support.ucsd.edu/)* |
| **Spawn failed**, with no explanation | A Datahub session is already running. *A member may have one; shell and VS Code sessions are not part of that limit and are not the cause* | **File → Hub Control Panel → Stop My Server**, or manual-resetter where the session cannot be reached. → [One Datahub Session](../access/datahub-in-the-browser.md#one-datahub-session) |
| **Spawn failed**, and nothing else is running | A full disk quota. A full quota stops a session starting and says nothing about why | Check **Services → disk-quota-service**, then clear space. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one) |
| **Spawn failed**, quota is fine | A stale profile | Run **manual-resetter** from the services dropdown. It stops the account's servers, signs the account out and resets the profile; files are preserved |
| **Spawn failed**, shortly after a `pip install` | A package in the account's own `.local` is loading ahead of the image's and breaking the environment | From a terminal, `mv .local/lib .local/lib.old`. → [Customizing an Environment](../environments/customizing-your-environment.md) |
| The course is not in the list | Provisioning, not access. Rosters load one business day before the term; a TSS change appears by 10am the following day | Ask the instructor or TA to confirm the roster. → [Sign-In & Session Problems](../access/sign-in-and-session-problems.md) |
| A **504** shortly after a crash | The pod died — an infinite loop, or out of memory — and the hub has not noticed yet | `kubectl delete pod <pod-id>` from the login node, then run manual-resetter |
| A course `git-pull` link fails and looks broken | It was clicked before the student had signed in. The link needs a session to redirect into | Sign in, start the environment, then click it again |
| "database is locked" in a notebook | A stale notebook signature database | From a terminal: `rm ~/.local/share/jupyter/nbsignatures.db`, then stop and restart the server |

**Nothing about logging out stops a session.** Closing the tab, closing the
laptop and signing out all leave the container running and holding its resources.
Use **File → Hub Control Panel → Stop My Server**.

## Launching From the Command Line

------------------------------------------------------------------------

| Symptom | Cause | Fix |
|---|---|---|
| The pod sits at `Pending`, then fails with **`0/5 nodes available`** | A GPU request with a missing or misspelled `gpu-class` label. `medium` and above sit behind `NoSchedule` taints, so a request without the label has nowhere to land | Add `-l gpu-class=<class>` and check the spelling of both halves. → [GPU Classes](../gpu-access/gpu-classes.md) |
| **"GPU quota exceeded. Wanted 1 but with 1 already in use, the quota of 1 would be exceeded"** | Another pod on the same account already holds the GPU | Usually the old pod is on its way out and clears in a minute or two. If not: `kubectl get pods`, then `kubectl delete pod <pod-id>` |
| The launcher rejects one of the *program's own* options | A missing `--`. Everything before it is read as a launcher flag | `launch-scipy-ml.sh -g 1 -B -- python train.py --epochs 50` |
| A GPU was requested and none arrived | `-G` where `-g` was meant. `-g 1` is one GPU; `-G 1` is a team ID | The commonest typo on the platform, and the failure never mentions capitalization |
| An `-n` node selection lands somewhere else | `-n` takes a bare node number | `-n 30`, not `-n n30`. The leading `n` on the status page is not part of the value |
| A container starts with far less CPU and memory than expected | `launch.sh` was called directly rather than a wrapper. Bare `launch.sh` is 1 CPU / 1 GB / 0 GPU; the wrappers set 2 CPU / 8 GB | Use `launch-scipy-ml.sh` or `launch-datascience.sh`, or pass `-c` and `-m`. → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md) |
| **`sudo: ...`** — any refusal at all | Containers run unprivileged, under the member's own UID, with no root. `sudo apt-get` fails by design | A system package needs a custom image, where root is available at build time. → [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary) |
| A job keeps running after the pod is exited | Exiting a pod does not stop the processes inside it, and `-b` backgrounds the *pod* while `&` backgrounds a *process* | `kubectl get pods` and `kubectl delete pod <pod-id>`. → [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes) |

## Statuses `kubectl get pods` Reports

------------------------------------------------------------------------

| Status | What it means | What to do |
|---|---|---|
| **`OOMKilled`** | The container reached its memory limit | See below — the cause is usually not the number requested |
| **`DeadlineExceeded`** | The runtime limit was reached. Not an error in the code | 6 hours by default, 12 if set at launch. → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| **`Pending`**, at length | Nothing can currently take the pod. It is waiting for resources to exist, not holding a place in a queue | `kubectl describe pod <pod-id>` and read the events at the bottom |
| **`Error`** | Unspecified. Our own published table says as much | Send us the pod ID, the node from the launch output, and roughly when. → [Getting Help](getting-help.md) |
| The session ended with no status and no error | Almost certainly an idle cull. Not a crash; saved work survives | → [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |

**`OOMKilled` on a pod at the figure it was launched with.** The number passed is
the limit; the request — what Kubernetes actually reserves and guarantees — is
half of it. `-m 32` reserves 16 GB and permits 32 GB, and the remaining 16 GB is
available only if the node the pod landed on has it spare.

A job that ran on one node is killed on a busier one with no change to the code.
Please size for the guarantee rather than the ceiling: work that needs 16 GB to
be safe is launched with `-m 32`. The same halving applies to CPU. GPUs are
exempt — a GPU is assigned to one container exclusively, so its request and its
limit are the same number.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

## Errors From Code & Notebooks

------------------------------------------------------------------------

**`RuntimeError: CUDA out of memory`** is not the same failure as `OOMKilled`.
That one is the pod's RAM; this one is the memory on the GPU card, which is a
separate and much smaller pool. The usual remedies, in order:

1. **A smaller batch size.** Free and immediate.
2. **Restart the kernel.** TensorFlow claims nearly all of the card's memory by
   default and does not give it back until the process ends, so a notebook that
   ran TensorFlow earlier can starve PyTorch later in the same session.
3. **The next GPU class up**, if the model genuinely does not fit. Please ask for
   the smallest class it does fit in. → [GPU Classes](../gpu-access/gpu-classes.md)

**`torch.cuda.is_available()` returns `False`.** Either the session has no GPU —
launched without `-g`, or started from a CPU-only environment on the course's
menu — or it is running `rstudio-notebook`, which derives from the CPU image and
is **not** GPU-enabled. What a session actually holds is confirmed from inside
the container:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0));"
```

→ [Standard Images](../environments/standard-images.md)

**"No space left" when saving a notebook**, or a "disk quota exceeded" email. The
storage quota is full. Note that deleting files in the Jupyter interface moves
them to `.local/share/Trash`, where they go on occupying quota until the
automatic purge after 7 days — so a delete that appears to free nothing has in
fact freed nothing.
→ [Quotas, Checking Usage & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**"Failed to validate", "the source of the following cell has changed", or
"corrupt metadata" when grading.** A read-only or autograded cell was copied,
edited or deleted. → [Common Grading Failures & Recovery](../grading/grading-failures.md)

## The Three Resource Tiers

------------------------------------------------------------------------

Three separate tiers apply, and confusing them is the usual reason a job will not
schedule:

| Tier | Default | Meaning |
|---|---|---|
| A single pod | 8 CPU / 32 GB / 1 GPU | The most any one container receives |
| The namespace, in total | 8 CPU / 64 GB / 1 GPU | Across everything running at once |
| Available on request | up to 32 CPU / 128 GB | Please ask, and say what for |

**These are defaults, not ceilings.** *And `-m 64` is not a valid
single-container request even though 64 GB is the namespace total: it may be
spent across several containers, not in one.*
→ [The Six Requests](getting-help.md#the-six-requests)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
