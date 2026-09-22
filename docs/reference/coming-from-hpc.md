# Coming from HPC

This page maps high-performance computing (HPC) and Slurm vocabulary to its
equivalents on DSMLP and describes the Slurm compatibility wrappers. It assumes
familiarity with a Slurm cluster.

## HPC Terms and Their Equivalents

| On an HPC cluster | The nearest equivalent | Where it differs |
|---|---|---|
| Account / project | [What a Workspace Is and What It Controls](../workspaces-and-storage/what-a-workspace-is.md) | A workspace covers a course, a lab, or a catch-all population. It controls the roster, storage, images, GPU classes, quota, and budget. It is named with `launch.sh -W`. |
| Allocation | Group quota and Service Unit budget | A group quota caps how many GPUs of a class a workspace may hold at once. A Service Unit budget caps how much GPU time may be spent. Neither alone is an allocation. |
| Service units / core-hours | [Service Units & Budgets](../gpu-access/service-units-and-budgets.md) | Service Units are similar to core-hours. Each GPU class has an hourly rate, drawn against a budget that renews weekly for courses and monthly or quarterly for research. |
| Partition / queue | [GPU Classes](../gpu-access/gpu-classes.md) | A GPU class is a size band, requested as a pod label: `-l gpu-class=medium`. It is not a queue and not a nameable set of nodes. |
| The scheduler | Kubernetes admission | There is no queue position, no backfill, and no observable priority ordering. |
| `sbatch`, `srun`, `squeue`, `scancel` | [Slurm Compatibility Wrappers](#slurm-compatibility-wrappers) | The commands are installed and working. They translate into `launch.sh`, with no Slurm scheduler behind them. |
| `sacct`, `sinfo`, `scontrol` | No equivalent | Use `kubectl get pods` and `kubectl describe pod`. |
| `module load` | Container images | The environment is the container image, chosen with `-i` or set by the workspace, as described in [Standard Images, Tags, and Pinning](../environments/standard-images.md). |
| Walltime (`--time`) | [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) | The runtime limit is 6 hours by default, up to 12 hours if set at launch. Idle culling and the end of a reservation window can also end a job, as described in [Runtime Limit, Idle Culling, and Reservation Window](#runtime-limit-idle-culling-and-reservation-window). |
| `--mem`, `--cpus-per-task` | `-m`, `-c` | The number passed is the limit, not the amount reserved, as described in [Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits). |
| `--gres=gpu:N` | `-g N` | `-g` is the GPU count and `-G` is the group flag, as described in [Resource and GPU Selection Flags](../running-jobs/launch-sh-reference.md#resource-and-gpu-selection-flags). |
| `--exclusive`, whole-node jobs | No equivalent | `-n` can place a pod on a named node, but the container is still sized by the resource tiers and runs on a node shared with other users. |
| MPI, `--nodes`, multi-node | No equivalent | Every job runs in one container on one node. |
| Job arrays | `--array` | `--array` submits multiple jobs. A concurrency limit such as `%4` is parsed and ignored. |
| Reservation | [Reservations](../gpu-access/reservations.md) | A reservation guarantees access, not a running job. The session is still launched as usual. |
| Fairshare | Service Units and borrowing seniority | The mechanism differs. Service Units and borrowing seniority divide a contested cluster between workspaces and between members of a workspace, as described in [Service Units & Budgets](../gpu-access/service-units-and-budgets.md) and [Borrowing Beyond Quota](../gpu-access/quotas-and-availability.md#borrowing-beyond-quota). |
| Login node | [The Login Node](../access/the-login-node.md) | The same rule applies. The login node is a jumpbox for launching jobs and moving files, and running computation on it is prohibited. |
| Scratch | No documented equivalent | Not documented. |

## Differences from Slurm Behavior

Three Slurm conventions behave differently on DSMLP.

### The `--partition` Option

`--partition` is not a scheduling partition. It is forwarded as a `gpu-class`
pod label, so `--partition medium` requests the `medium` GPU class rather than
a queue named "medium". A partition name that is not a GPU class requests
nothing that exists. The option is accepted either way, and the failure appears
later as a pod that does not schedule. The classes are described in
[GPU Classes](../gpu-access/gpu-classes.md).

### Memory and CPU Limits

The value passed to `-m` or `-c`, or to `--mem` or `--cpus-per-task` through
the wrappers, is the limit, not the amount the scheduler guarantees. The
guaranteed request and how to size a job for it are described in
[Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits).

### Pending Pods

A pending pod is not queued. With no scheduler arbitrating between
submissions, a pod stays pending when nothing can currently take it.
`0/5 nodes available` after a GPU request usually means the request carries no
`gpu-class` label, as described in
[Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label).
The message is also listed in [Error Messages](error-messages.md).

## Runtime Limit, Idle Culling, and Reservation Window

Three separate limits can end a job: the runtime limit, idle culling, and the
end of a reservation window.

| Limit | What it measures | Where it is documented |
|---|---|---|
| Runtime limit | Wall-clock time since the pod started | [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| Idle culling | How long the GPU has been doing nothing | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| Reservation window | The capacity booked, and until when | [End of a Reservation Window](../gpu-access/what-ends-a-session.md#end-of-a-reservation-window) |

Idle culling has no HPC equivalent. A GPU session that stops using its GPU is
reclaimed regardless of its runtime limit.

## Slurm Compatibility Wrappers

`sbatch`, `srun`, `squeue`, and `scancel` are installed as translation wrappers
around `launch.sh`. There is no Slurm scheduler behind them.

| Slurm feature | Behavior of the wrappers |
|---|---|
| Queue and scheduling | A job is submitted to Kubernetes, which places it when the resources exist. There is no queue position, no backfill, and no observable priority ordering. |
| Multi-node jobs and MPI | Not supported. Every job runs in one container on one node, and `--nodes` has no equivalent. |
| Accounting commands | There is no `sacct`, `sinfo`, or `scontrol`. |
| Job state | The wrappers record what they submitted in `~/.slurm-compat/jobs.tsv`, which is how `squeue` knows about submitted jobs. The file is in a home directory and is not a cluster database. |

## Option Mapping

| Slurm option | Equivalent |
|---|---|
| `--job-name` | The job's name |
| `--partition` | `-l gpu-class=<value>`, a GPU class rather than a queue |
| `--cpus-per-task` | `-c` |
| `--mem` | `-m`, rounded up to whole GB |
| `--gres=gpu:N` | `-g N` |
| `--gres=gpu:<model>:N` | `-g N` plus `-v <model>` |
| `--time` | `K8S_TIMEOUT_SECONDS`, the container's runtime deadline |
| `--output`, `--error` | Output files, with `%j`, `%A`, `%u`, `%x` and `%a` substitutions |
| `--array` | Multiple submissions |

### Platform-Specific Options

The wrappers accept two options that Slurm does not have.

| Option | Effect |
|---|---|
| `--image <image>` | The container image, as `launch.sh -i` |
| `--course <workspace>` | The workspace to launch into, as `launch.sh -W` |

### Requested Runtime

`--time` is subject to the platform's runtime limits. A batch script that asks
for 72 hours does not receive 72 hours. The limits are described in
[The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit).

## Limitations of the Slurm Wrappers

### Array Concurrency Limits

Array concurrency limits are parsed but not enforced. `--array=1-100%4` submits
all 100 jobs, and the `%4` is accepted and ignored. Concurrency must be limited
by other means.

### Exit Status

`sbatch` does not propagate a job's exit status. A pipeline that checks the
return code of a submission does not learn whether the work succeeded. The
job's own output shows that.

### Diagnostic Commands

The wrappers translate into `launch.sh` and do not translate back. Diagnose a
failed job with the Kubernetes commands `kubectl get pods`,
`kubectl describe pod`, and `kubectl logs`, not with Slurm commands. Direct use
of Kubernetes is described in
[Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md).

## Choosing Between the Slurm Wrappers and `launch.sh`

Use the Slurm wrappers to run existing submission scripts unchanged. Write new
work against `launch.sh`, using workspaces, GPU classes, and background and
batch modes directly, as described in
[`launch.sh` Reference](../running-jobs/launch-sh-reference.md).

## Unsupported HPC Features

MPI, multi-node jobs, a job scheduler, and accounting commands are not
available, as described in
[Slurm Compatibility Wrappers](#slurm-compatibility-wrappers). Nothing reports
historical usage the way `sacct` does. Work that is tightly coupled across
nodes belongs on another platform.

Where any of these is a requirement, contact
[Research IT](https://research-it.ucsd.edu/computing/index.html) first.
Research IT can compare the work against the other platforms the campus runs
and against national resources.

See also: [Platform Selection](getting-help.md#platform-selection)

## Features Uncommon on HPC Clusters

DSMLP provides a browser-based notebook environment that shares one filesystem
with the login node, per-user containers that members build themselves, and
Kubernetes underneath for direct use. Most HPC clusters do not provide these.
Direct use of Kubernetes is described in
[Direct Kubernetes Use and Session Events](../running-jobs/kubernetes.md).
