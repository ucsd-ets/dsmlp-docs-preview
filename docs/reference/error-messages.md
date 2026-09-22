# Error Messages

This page lists common error messages and failure symptoms, grouped by where
they appear, with the cause and fix for each. An idle-culled session, a
`DeadlineExceeded` status, and a refused `sudo` are expected platform behavior,
not faults.

## Signing In & Starting a Session

| Symptom | Cause | Fix |
|---|---|---|
| The campus sign-on page returns repeatedly | A campus credential or Duo problem, or another identity signed in to the same browser | Sign out of the other identities, or use a private window. Datahub uses standard UCSD single sign-on, so the [ITS Service Desk](https://support.ucsd.edu/) handles a persistent failure |
| **Spawn failed**, with no explanation | A Datahub session is already running. A member may have one Datahub session at a time. Shell and VS Code sessions do not count toward that limit and are not the cause | Stop the running session with **File → Hub Control Panel → Stop My Server**, or run **manual-resetter** where the session cannot be reached. See [Concurrent Datahub Sessions](../access/datahub-in-the-browser.md#concurrent-datahub-sessions) |
| **Spawn failed**, and nothing else is running | A full disk quota. A full quota prevents a session from starting and produces no message stating the cause | Check **Services → disk-quota-service**, then clear space. See [Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas) |
| **Spawn failed**, quota is fine | A stale profile | Run **manual-resetter** from the services dropdown. It stops the account's servers, signs the account out, and resets the profile. Files are preserved. See ["Spawn Failed"](../access/sign-in-and-session-problems.md#spawn-failed) |
| **Spawn failed**, shortly after a `pip install` | A package in the account's own `.local` loads ahead of the image's version and breaks the environment | From a terminal, run `mv .local/lib .local/lib.old`. See [Customizing an Environment](../environments/customizing-your-environment.md) |
| The course is not in the list | A provisioning matter, not an access fault. Rosters load one business day before the term, and a TSS change appears by 10am the following day | Ask the instructor or TA to confirm the roster. See [Students Enrolled in a Course](../access/when-access-starts-and-ends.md#students-enrolled-in-a-course) |
| A **504** shortly after a crash | The pod stopped, from an infinite loop or from running out of memory, and the hub has not yet detected it | Run `kubectl delete pod <pod-id>` from the login node, then run **manual-resetter** |
| A course `git-pull` link fails and appears broken | The link was clicked before the student signed in. The link needs a session to redirect into | Sign in, start the environment, then click the link again |
| "database is locked" in a notebook | A stale notebook signature database | From a terminal, run `rm ~/.local/share/jupyter/nbsignatures.db`, then stop and restart the server |

### Stopping a Session

> [!WARNING]
> Closing the tab, closing the laptop, and signing out all leave the container
> running and holding its resources. Stop a session with
> **File → Hub Control Panel → Stop My Server**, as described in
> [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

## Launching From the Command Line

| Symptom | Cause | Fix |
|---|---|---|
| The pod sits at `Pending`, then fails with **`0/5 nodes available`** | A GPU request with a missing or misspelled `gpu-class` label | Add `-l gpu-class=<class>`, and check the spelling of `gpu-class` and of the class name. See [Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label) |
| **"GPU quota exceeded. Wanted 1 but with 1 already in use, the quota of 1 would be exceeded"** | Another pod on the same account already holds the GPU | The earlier pod is usually terminating and clears within a minute or two. If it does not clear, run `kubectl get pods`, then `kubectl delete pod <pod-id>` |
| The launcher rejects one of the program's own options | A missing `--`. The launcher reads everything before `--` as a launcher flag | Place `--` between the launcher flags and the program: `launch-scipy-ml.sh -g 1 -B -- python train.py --epochs 50` |
| A GPU was requested and none arrived | `-G` where `-g` was meant. `-g 1` is one GPU; `-G 1` is a team ID | Use `-g` for the GPU count. The failure does not mention capitalization. See [Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags) |
| An `-n` node selection lands somewhere else | `-n` takes a bare node number | Pass the number alone: `-n 30`, not `-n n30`. The leading `n` on the status page is not part of the value |
| A container starts with far less CPU and memory than expected | `launch.sh` was called directly rather than through a wrapper. Bare `launch.sh` has lower CPU and memory defaults than the wrappers | Use `launch-scipy-ml.sh` or `launch-datascience.sh`, or pass `-c` and `-m`. See [Default Resources](../running-jobs/launch-sh-reference.md#default-resources) |
| **`sudo: ...`**, or any other refusal of `sudo` | Containers run unprivileged, under the member's own UID, with no root. `sudo apt-get` fails by design | Install a system package in a custom image, where root is available at build time. See [Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages) |
| A job keeps running after the pod is exited | Exiting a pod does not stop the processes inside it. `-b` backgrounds the pod, and `&` backgrounds a process | Run `kubectl get pods`, then `kubectl delete pod <pod-id>`. See [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes) |

## Statuses `kubectl get pods` Reports

| Status | What it means | What to do |
|---|---|---|
| **`OOMKilled`** | The container reached its memory limit | Size the job for its guaranteed memory request rather than its limit, as described in [Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits) |
| **`DeadlineExceeded`** | The runtime limit was reached. The status does not indicate an error in the code | The runtime limit is 6 hours by default, or 12 hours if set at launch. See [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| **`Pending`**, at length | The pod cannot currently be scheduled. It is waiting for resources to become available and does not hold a place in a queue | Run `kubectl describe pod <pod-id>` and read the events at the bottom of the output |
| **`Error`** | The status does not identify a cause | Report the pod ID, the node named in the launch output, and the approximate time of the failure, as described in [Getting Help](getting-help.md) |
| The session ended with no status and no error | Almost certainly an idle cull, not a crash. Saved work is preserved | See [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |

## Errors From Code & Notebooks

### CUDA Out-of-Memory Errors

`RuntimeError: CUDA out of memory` concerns the memory on the GPU card, which is
a separate and much smaller pool than the pod's RAM. It is a different failure
from the `OOMKilled` (out-of-memory) status, which concerns the pod's RAM. Apply
the usual remedies in this order:

1. Reduce the batch size.
2. Restart the kernel. TensorFlow claims nearly all of the card's memory by
   default and does not release it until the process ends, so a notebook that
   ran TensorFlow earlier can leave too little GPU memory for PyTorch later in
   the same session.
3. Move to the next GPU class up if the model does not fit, and request the
   smallest class it fits in. Classes are listed in
   [GPU Classes](../gpu-access/gpu-classes.md).

### PyTorch GPU Detection

`torch.cuda.is_available()` returns `False` when the session has no GPU or is
running `rstudio-notebook`. A session has no GPU when it was launched without
`-g` or started from a CPU-only environment on the course's menu.
`rstudio-notebook` derives from the CPU image and is not GPU-enabled, as
described in
[Standard Images](../environments/standard-images.md#standard-images).
Confirm what a session holds from inside the container:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0));"
```

### Full Storage Quota

"No space left" when saving a notebook, or a "disk quota exceeded" email, means
the storage quota is full. Files deleted in the Jupyter interface move to
`.local/share/Trash`, where they continue to count against the quota until the
automatic purge after 7 days. A deletion in the Jupyter interface therefore
frees no space before that purge. Storage quotas are described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

### Grading Validation and Metadata Errors

"Failed to validate", "the source of the following cell has changed", or
"corrupt metadata" when grading means that a read-only or autograded cell was
copied, edited, or deleted. Recovery is described in
[Common Grading Failures & Recovery](../grading/grading-failures.md).

## Resource Tiers

Confusing the per-pod, per-namespace, and on-request resource tiers is the usual
reason a job does not schedule. The tiers and their figures are listed in
[Resource Tiers](../running-jobs/launch-sh-reference.md#resource-tiers).
