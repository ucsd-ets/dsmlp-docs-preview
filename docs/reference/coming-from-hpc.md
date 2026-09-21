# Coming from HPC: Vocabulary & Slurm Compatibility

For readers arriving from a Slurm cluster, most habits transfer and a few do not.
This page is the translation table, and the three habits worth unlearning are at
the bottom.

## The Map

------------------------------------------------------------------------

| On an HPC cluster | The nearest thing here | Where it differs |
|---|---|---|
| **Account / project** | [Workspace](../workspaces-and-storage/what-a-workspace-is.md) | A course, a lab, or a catch-all population. It anchors roster, storage, images, GPU classes, quota and budget. Named with `launch.sh -W` |
| **Allocation** | Two separate things | A **group quota** caps how many GPUs of a class a workspace may hold *at once*; a **Service Unit budget** caps how much GPU *time* may be spent. Neither alone is an allocation |
| **Service units / core-hours** | [Service Units & Budgets](../gpu-access/service-units-and-budgets.md) | Genuinely similar: an hourly rate per GPU class, drawn against a budget that renews weekly for courses, monthly or quarterly for research |
| **Partition / queue** | [GPU class](../gpu-access/gpu-classes.md) | A size band, requested as a pod label: `-l gpu-class=medium`. Not a queue, and not a nameable set of nodes |
| **The scheduler** | Kubernetes admission | There is no queue position, no backfill and no observable priority ordering |
| **`sbatch`, `srun`, `squeue`, `scancel`** | [Compatibility wrappers](coming-from-hpc.md#there-is-no-slurm-here) | They ship and they work. They translate into `launch.sh`; there is no Slurm behind them |
| **`sacct`, `sinfo`, `scontrol`** | Nothing | Use `kubectl get pods` and `kubectl describe pod` |
| **`module load`** | Container images | The environment is the image, chosen with `-i` or by the workspace. → [Standard Images](../environments/standard-images.md) |
| **Walltime (`--time`)** | Runtime limit | 6 hours by default, up to 12 if set at launch. Two other clocks can also end a job — see below |
| **`--mem`, `--cpus-per-task`** | `-m`, `-c` | **The number passed is a ceiling, and the reservation is half of it.** This is the expensive one |
| **`--gres=gpu:N`** | `-g N` | Note `-g` is GPU and `-G` is group; they are one keystroke apart |
| **`--exclusive`, whole-node jobs** | No equivalent | `-n` can pin a pod to a named node, but the container is still sized by the resource tiers, on a node shared with other people |
| **MPI, `--nodes`, multi-node** | Nothing | Every job runs in one container on one node |
| **Job arrays** | `--array` | Submits multiple jobs. A concurrency limit such as `%4` is parsed and ignored |
| **Reservation** | [Reservation](../gpu-access/reservations.md) | Genuinely a reservation — but it guarantees *access*, not a running job. The session is still launched as usual |
| **Fairshare** | Service Units, plus borrowing seniority | Different mechanism, similar intent: dividing a contested cluster between groups and between members of a group |
| **Login node** | [`dsmlp-login.ucsd.edu`](../access/the-login-node.md) | Same rule, stated more firmly: it is a jumpbox for launching jobs and moving files, and running work on it is prohibited |
| **Scratch** | *Not documented* | See the draft note above. Please do not assume a scratch area exists |

## Three Habits to Unlearn

------------------------------------------------------------------------

**`--partition` is not a scheduling partition.** It is forwarded as a `gpu-class`
pod label. `--partition medium` asks for a medium-sized GPU; a partition name
that is not a GPU class asks for nothing that exists. The option is accepted
either way, and the failure arrives later as a pod that will not schedule.
→ [Coming from HPC](coming-from-hpc.md#there-is-no-slurm-here)

**The number requested is the ceiling, not the reservation.** `launch.sh` sets
the Kubernetes *request* — what the scheduler guarantees — to half the *limit*
named. `-c 8 -m 32` reserves 4 CPU and 16 GB and permits 8 and 32; the remainder
is available only if the node has it spare. Please size for the guarantee here:
a job that needs 16 GB to be safe is launched with `-m 32`.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**"Pending" does not mean "queued".** With no scheduler arbitrating between
submissions, a pod that stays pending is a pod nothing can currently take —
usually because a GPU request carries no `gpu-class` label, since `medium` and
above sit behind `NoSchedule` taints and a request without the label has nowhere
to land. The failure reads `0/5 nodes available` and says nothing about labels.
→ [Error Messages](error-messages.md)

## Three Clocks, Not One

------------------------------------------------------------------------

A Slurm user expects walltime to be the only thing that ends a job. Here, three
separate limits can, and confusing them is the usual reason a run dies at an hour
nobody expected.

| Clock | What it measures |
|---|---|
| **Runtime limit** | Wall-clock time since the pod started → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| **Idle culling** | How long the GPU has been doing nothing → [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| **The reservation window** | The capacity booked, and until when → [What Ends a Session](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill) |

**Idle culling has no HPC equivalent.** A GPU session that stops using its GPU is
reclaimed after about 30 minutes, whatever its walltime says. *A job that computes
on CPU while a GPU sits loaded but untouched is exactly the shape this catches.*

## There Is No Slurm Here

------------------------------------------------------------------------

**These are translation wrappers around `launch.sh`, not a Slurm installation.**
There is no Slurm scheduler behind them. The consequences:

- **No queue and no scheduling.** A job is submitted to Kubernetes, which places
  it when the resources exist. There is no queue position, no backfill, and no
  observable priority ordering.
- **No multi-node and no MPI.** Every job runs in one container on one node. A
  `--nodes 4` habit has nothing to translate into.
- **No accounting commands.** There is no `sacct`, `sinfo` or `scontrol`.
- **State is local.** The wrappers record what they submitted in
  `~/.slurm-compat/jobs.tsv`, which is how `squeue` knows about submitted jobs. It
  is a file in a home directory, not a cluster database.

**`--partition` is not a scheduling partition.** It is forwarded as a `gpu-class`
pod label — so `--partition medium` asks for a medium GPU class rather than a
queue named "medium", and a partition name that is not a GPU class does not
resolve to one.
→ [GPU Classes](../gpu-access/gpu-classes.md)

## Option Mapping

------------------------------------------------------------------------

| Slurm option | What it becomes here |
|---|---|
| `--job-name` | The job's name |
| `--partition` | `-l gpu-class=<value>` — a GPU class, not a queue |
| `--cpus-per-task` | `-c` |
| `--mem` | `-m`, rounded **up** to whole GB |
| `--gres=gpu:N` | `-g N` |
| `--gres=gpu:<model>:N` | `-g N` plus `-v <model>` |
| `--time` | `K8S_TIMEOUT_SECONDS` — the container's runtime deadline |
| `--output`, `--error` | Output files, with `%j`, `%A`, `%u`, `%x` and `%a` substitutions |
| `--array` | Multiple submissions |

Two options exist here that Slurm does not have:

| Extension | Effect |
|---|---|
| `--image <image>` | The container image, as `launch.sh -i` |
| `--course <workspace>` | The workspace to launch into, as `launch.sh -W` |

**`--time` is still subject to the platform's runtime limits**, so a batch script
asking for 72 hours does not receive 72 hours.
→ [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

## Rough Edges

------------------------------------------------------------------------

**Array concurrency limits are parsed but not enforced.** `--array=1-100%4`
submits all 100; the `%4` is accepted and ignored. Concurrency has to be limited
by other means.

**`sbatch` does not propagate a job's exit status.** A pipeline that checks the
return code of a submission does not learn whether the work succeeded; the job's
own output does.

**The mapping is one-way.** These wrappers translate into `launch.sh`; they do not
translate back. When something goes wrong, the useful diagnostics are the
Kubernetes ones — `kubectl get pods`, `kubectl describe pod`, `kubectl logs` — not
Slurm ones. → [Kubernetes](../running-jobs/kubernetes.md)

## Which to Use

------------------------------------------------------------------------

**The compatibility layer exists to get working submission scripts running
unchanged.** Where it does that, it has done its job.

**New work is better written against `launch.sh`**, in the platform's own
vocabulary — workspaces, GPU classes, background and batch modes — with no
translation layer between the job and the error messages.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)
## What Is Simply Not Here

------------------------------------------------------------------------

**No MPI and no multi-node.** Work that is tightly coupled across nodes belongs
on another platform, and no amount of configuration changes that.

**No genuine scheduler, and no accounting commands.** There is nothing to query
about queue position, and nothing that reports historical usage the way `sacct`
would.

**`sbatch`, `srun`, `squeue` and `scancel` are on the path here.** They are
translation wrappers, described above.

**Where any of that is a requirement**, please talk to
[Research IT](https://research-it.ucsd.edu/computing/index.html) first. They can
weigh the work against the other platforms campus runs and against national
resources. → [Getting Help](getting-help.md)

*What this platform does have, and most HPC clusters do not, is a browser-based
notebook environment sharing one filesystem with the login node, per-user
containers members build themselves, and Kubernetes underneath for those who
want it.* → [Kubernetes](../running-jobs/kubernetes.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
