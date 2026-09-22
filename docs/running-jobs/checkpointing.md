# Checkpointing & Logging Long Runs

A container can stop for reasons unrelated to faulty code: the runtime limit,
idle culling, preemption, and maintenance. This page covers checkpoints a job
can resume from, the termination warning that precedes some of these stops, and
logs for unattended jobs.

## What Can End a Run

| Cause | Warning | Where it is documented |
|---|---|---|
| The runtime limit: 6 hours by default, 12 if set at launch | None; the pod reports `DeadlineExceeded` | [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit) |
| Idle culling, once the GPU stops being used | Yes; a warning comes first, and the status is recorded on the pod | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| Preemption, once a booking needs the capacity | Yes; minutes of notice, readable by the job itself | [End of a Reservation Window](../gpu-access/what-ends-a-session.md#end-of-a-reservation-window) |
| Research Cluster maintenance | Notice in advance, not on the pod; all running jobs are terminated | [Scheduled Maintenance](../reference/policy.md#scheduled-maintenance) |

None of these stops indicates a fault in the code. Instructional maintenance
generally leaves running jobs alone.

> [!WARNING]
> The runtime limit and Research Cluster maintenance are not announced on the
> pod. The runtime limit stops the container at its deadline with no prior
> warning and no signal to catch. Research Cluster maintenance terminates every
> running job. Work that is not on disk before either one arrives is lost.

Preemption and idle culling are announced on the pod, where a running program
can read them. The reservation controller marks a session it may need to stop
minutes before stopping it, as described in
[The Termination Warning](#the-termination-warning). The idle culler records a
status and a projected deadline in the same way, as described in
[Idle Culler Annotations](#idle-culler-annotations).

## Checkpointing

A **checkpoint** is a saved copy of enough state to resume a run, written on a
chosen schedule. For a training run, that usually means the model weights, the
optimizer state, and the epoch or step counter. The full set of components is
listed in
[What a Resumable Checkpoint Contains](#what-a-resumable-checkpoint-contains).
A job that cannot resume from a checkpoint restarts from the beginning after an
interruption.

### Checkpoint Location

Write checkpoints to a home directory. Home persists between containers, and the
container and the login node share a filesystem, so a checkpoint written by a
job is readable from the login node after the pod is gone. A path inside the
container that is not a mounted directory is lost with the pod. Directory
locations are described in
[Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live).

Do not write checkpoints into a shared or course-wide directory unintentionally.
Its quota serves the whole class, not one run.

### Wall-Clock Schedule

Checkpointing on wall-clock time, rather than only at the end of each epoch,
bounds the work an interruption can lose. The runtime limit ends a run
regardless of epoch boundaries, and with per-epoch checkpoints an epoch that
takes 90 minutes loses 90 minutes of work at each interruption. A checkpoint
written every 15 or 30 minutes limits the loss to that interval, at little cost.

### Automatic Resume

A script that finds the newest checkpoint at startup and continues from it
resumes after an interruption without anyone present. A `--resume` flag has to
be supplied by hand at each restart.

### Number of Checkpoints Kept

Checkpoints are large, and home directories have quotas, as described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).
Bound the number of checkpoints kept. The last two and the best one are usually
enough. Delete an old checkpoint only after the new one is complete. A job that
deletes the old checkpoint first can lose all saved progress to one interruption
during the save.

## What a Resumable Checkpoint Contains

A checkpoint that holds only the model weights does not resume the same run.
Each component in this table other than the weights is state the optimizer or
the data pipeline carries. Omitting one shows as a jump in the loss curve at the
point of resume.

| Component | Call | Notes |
|---|---|---|
| Model weights | `model.state_dict()` | Under `torch.compile` the keys gain an `_orig_mod.` prefix. Saving `model._orig_mod.state_dict()`, or stripping the prefix on load, keeps the checkpoint loadable by an uncompiled model |
| Optimizer | `optimizer.state_dict()` | The largest component. Adam and AdamW carry two `fp32` moments, so optimizer state is commonly 2-3× the model in bytes |
| Learning-rate scheduler | `scheduler.state_dict()` | Cheap to save. Without it, a warmup or cosine schedule restarts from the beginning |
| Mixed-precision scaler | `scaler.state_dict()` | `torch.amp.GradScaler` holds an adaptive loss scale. A resume without it re-converges through a few skipped steps |
| Step and epoch counters | Kept by the training script | The position a resume is expressed in |
| Data position | `StatefulDataLoader.state_dict()` | `torchdata`'s drop-in `DataLoader` replacement, which supports mid-epoch resume without replaying batches. It requires the same `num_workers` on load as on save |
| Random number generator state | `torch.get_rng_state()`, `torch.cuda.get_rng_state_all()`, `random.getstate()`, `numpy.random.get_state()` | Needed for a bit-comparable resume of dropout, augmentation, and sampling. It can be omitted where reproducibility does not matter |
| Averaged weights and metric state | Kept by the training script | Exponential moving averages, best-so-far metrics, early-stopping counters |

Store the run's configuration alongside the weights. A checkpoint saved without
its configuration cannot be identified later.

## Atomic Checkpoint Writes

An interruption can end a process while it is writing a checkpoint. Single-file
and sharded checkpoints are protected against this in different ways.

### Single-File Checkpoints

Write a single-file checkpoint to a temporary path, flush it, then rename it.
`os.replace` is atomic within one filesystem, so the visible path always holds
either the complete old checkpoint or the complete new one, never a truncated
file:

```python
import os, torch

def save_atomic(state: dict, path: str) -> None:
    tmp = f"{path}.tmp"
    with open(tmp, "wb") as fh:
        torch.save(state, fh)
        fh.flush()
        os.fsync(fh.fileno())      # the data is durable before the rename
    os.replace(tmp, path)          # atomic, within one filesystem only
    dfd = os.open(os.path.dirname(path) or ".", os.O_RDONLY)
    try:
        os.fsync(dfd)              # and the rename itself is durable
    finally:
        os.close(dfd)
```

A checkpoint written directly to its final path and interrupted during the write
fails to load with `RuntimeError: unexpected EOF`.

### Sharded Checkpoints

A distributed checkpoint is a directory of per-rank shards, and no atomic rename
covers all of them at once. Complete the save, then publish it, in one of two
ways:

- Write into a scratch directory, and rename the directory once every rank has
  finished.
- Write an explicit `DONE` marker last, and have the resume path ignore any
  directory without one.

With `torch.distributed.checkpoint`, the `.metadata` file is written after the
shards, so its absence indicates that a directory is incomplete. Depend on an
explicit marker rather than on `.metadata`.

## Checkpoint Frequency

### The Young/Daly Interval

The Young/Daly interval is `sqrt(2 · C · MTBF)`, where `C` is the wall-clock
cost of one checkpoint and `MTBF` is the mean time between interruptions. It
balances saving so often that the saves dominate the run against saving so
rarely that each interruption costs hours.

### Interval from Checkpoint Cost

Under a reservation system that announces its interruptions, the interval can be
set from `C` alone. A common target is checkpoint overhead below about 5% of step
time, which for a synchronous save means an interval of roughly `20 × C`. That
interval covers interruptions that are not announced, such as a node failure, an
out-of-memory kill, or a collective that times out. Announced interruptions are
covered by the warning described in
[The Termination Warning](#the-termination-warning). A checkpoint written on the
warning limits the loss to one step rather than one interval.

Measure `C` once on the storage the checkpoint is actually written to, and log
the value. Assumed values of `C` are consistently optimistic.

### Asynchronous Checkpoints

Where `C` is large, use asynchronous checkpointing before lengthening the
interval. `torch.distributed.checkpoint` offers `dcp.async_save`, which stages
tensors into CPU buffers and writes them from a background thread while training
continues. The blocking part of the save drops to roughly the staging copy.

Asynchronous saves have two costs:

- Host memory on the order of one checkpoint per rank.
- Only one save may be outstanding at a time. Wait on the previous future before
  issuing the next, or the memory use multiplies.

An asynchronous save that was never flushed is not a checkpoint. Wait on the
outstanding future before exiting on a preemption.

## The Termination Warning

The reservation controller marks a session it may need to stop before stopping
it. The mark is a set of annotations written onto the pod. It appears only while
the session is at risk: a booking is coming due for capacity the session is
holding, and the session is one of the candidates that could supply it.

How far ahead of the earliest possible stop the warning appears, and whether a
minimum notice is guaranteed, is not yet published.

### The Runtime Guarantee

A session inside its runtime guarantee is never stopped, however short of
capacity the cluster is. The mark can still appear during the guarantee, when
the booking that needs the capacity starts after the guarantee ends. The warning
then states that the reclaim is queued for the moment the guarantee ends. A
warning of this kind arrives while the guarantee is still running, which leaves
the most time to checkpoint. The end of a guaranteed window is described in
[End of a Reservation Window](../gpu-access/what-ends-a-session.md#end-of-a-reservation-window).

A job is not stopped at `guaranteed-until`. It keeps running until another
reservation needs the capacity, so exiting at the guarantee gives up run time
that remains available. From `guaranteed-until` onward, the job can be stopped
on notice it does not control. Shorten the checkpoint interval at that point.

### Warning Annotations

Four annotations are relevant to a long-running job:

| Annotation | Value | What it says |
|---|---|---|
| `galends/guaranteed-until` | UTC instant, `YYYY-MM-DDTHH:MM:SSZ` | The end of the protected period. It can move **later** while the session runs, when an abutting follow-on window is booked |
| `galends/termination-warning-at` | UTC instant, same format | The **earliest** moment the session could be stopped. Never earlier than `guaranteed-until`. Present only while the session is at risk |
| `galends/termination-warning-risk` | Decimal between 0 and 1, two places, e.g. `0.33` | The share of the candidates that has to be stopped. `1.00` means all of them |
| `galends/termination-warning-message` | A sentence | The same thing in prose, in the cluster's local timezone. Written to be displayed as it stands, and not to be parsed |

`termination-warning-at` is the earliest possible stop, not a scheduled one. The
shortfall it was computed from may be gone before that moment arrives, in which
case nothing happens and the annotations are removed. Treat the moment as the
start of a period in which the session may be stopped at any time, not as a
countdown to a certain stop.

### Best-Effort Annotations

Every annotation is optional and best-effort. Any of them can be absent at any
moment, and the three warning annotations are removed when the risk clears. The
controller does not read any of them back to decide anything. Each decision is
recomputed from live reservation state. Code that reads the annotations handles
each one being missing, ignores a value that does not parse rather than failing,
and re-reads each value instead of caching it at startup.

### Canceling a Pending Termination

Extending or re-booking the window cancels a pending termination at any point
until the pod is deleted. The controller re-checks every session's live
guarantee before it selects any session to stop, so a reservation recorded
before the selection always takes precedence. Extension is described in
[Continue, Extend & Adopt](../gpu-access/reservations.md#continue-extend--adopt).

## Reading the Warning From Inside a Container

Annotations are visible to the container only when the pod spec projects them.
A downward-API volume projects them and is refreshed as the values change:

```yaml
spec:
  volumes:
    - name: podinfo
      downwardAPI:
        items:
          - path: guaranteed-until
            fieldRef:
              fieldPath: metadata.annotations['galends/guaranteed-until']
          - path: termination-warning-at
            fieldRef:
              fieldPath: metadata.annotations['galends/termination-warning-at']
          - path: termination-warning-risk
            fieldRef:
              fieldPath: metadata.annotations['galends/termination-warning-risk']
          - path: termination-warning-message
            fieldRef:
              fieldPath: metadata.annotations['galends/termination-warning-message']
  containers:
    - name: notebook
      volumeMounts:
        - name: podinfo
          mountPath: /etc/podinfo
          readOnly: true
```

Each file then holds one raw value, with no quoting, no escaping, and no
trailing newline, so `$(cat …)` is the value:

```console
$ cat /etc/podinfo/termination-warning-at; echo
2026-08-21T17:30:16Z
$ cat /etc/podinfo/termination-warning-risk; echo
0.33
```

### Empty Annotation Files

An absent annotation is an empty file, not a missing one. All four files are
created when the pod starts, and the three warning files stay empty while the
session is not at risk. Test for a warning with `-s`, "exists and is not empty".

> [!WARNING]
> `-f` and `-e` are true from the pod's first second. A loop guarded on either
> one exits immediately on every run, and does so silently.

### Downward-API Environment Variables

Downward-API environment variables are not suitable for these annotations. An
environment variable is resolved once when the container starts, and the
annotations are written after that, some of them changing during the run. Only
the volume is refreshed.

### Refresh Delay

The kubelet updates the files on its own sync loop, which adds to the
controller's own cadence. The warning therefore reaches the container some time
into the notice period, not at its start. The worst-case delay between the
controller writing an annotation and the container being able to read it is not
yet published.

Polling every 15 to 30 seconds is sufficient. To watch the files with `inotify`,
watch the directory rather than the file, because the whole set is swapped
atomically behind a symlink.

### Projecting the Whole Annotation Map

`fieldPath: metadata.annotations` with no subscript projects the whole
annotation map into a single file. That file carries every annotation the
session has, including the reservation behind it, its GPU class, and when it was
admitted. Each annotation is on its own line as `key="value"`, with quotes and
escapes that have to be undone. Per-key files need no parser and are sufficient
for checkpointing.

### Idle Culler Annotations

The idle culler publishes its own status in the same way.
`dsmlp/idle-gpu-status` and `dsmlp/idle-gpu-cull-deadline` are annotations on
the same pod, and an additional `fieldRef` for each projects them alongside the
four reservation annotations. A job whose GPU is unused between phases can be
culled on the culler's own timetable, independently of any reservation. Idle
culling is described in
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).

## Acting on the Warning

### Batch Jobs Processed in Units

A batch job that processes work in units, such as shards, epochs, or sweeps,
usually needs only to stop starting new units. Check for the warning between
units, never inside one:

```bash
PODINFO=${PODINFO:-/etc/podinfo}

# -s is the operator that matters here: the file exists and is empty until the
# controller warns this pod, so -f and -e would bail on the first shard.
warned() { [[ -s "$PODINFO/termination-warning-at" ]]; }

for shard in "${SHARDS[@]}"; do
    if warned; then
        cat "$PODINFO/termination-warning-message" >&2
        printf 'stopped before %s; rerun to pick up the rest\n' "$shard" >&2
        exit 75                 # EX_TEMPFAIL, for whatever submitted the job
    fi
    process_shard "$shard"      # each shard commits its own output
done
```

Re-read the file on every pass through the loop, and do not store the result. A
warning can be withdrawn when the window is extended, the incoming booking never
claims its capacity, or the session is re-linked to another reservation. The
file is then empty again. A job that stored the first warning it saw would stop
for a warning that had already been withdrawn. A job that is to continue rather
than hand back its remaining units can make the same test and log the result
instead of acting on it.

### Training Loops

A training loop checkpoints at a step boundary, not from a signal handler. A save
during the backward pass captures inconsistent state, and under distributed
training a save is a collective operation that every rank has to enter in the
same iteration:

```python
from datetime import datetime, timezone
from pathlib import Path

PODINFO = Path("/etc/podinfo")

def _read(name):
    try:
        raw = (PODINFO / name).read_text().strip()
    except OSError:
        return None
    return raw or None

def _instant(name):
    raw = _read(name)
    try:
        return datetime.fromisoformat(raw) if raw else None
    except ValueError:
        return None            # anything unparseable is ignored, not raised on

def stop_expected(lead_seconds):
    """True when a stop is close enough that a checkpoint should be written."""
    now = datetime.now(timezone.utc)
    for key in ("termination-warning-at", "guaranteed-until"):
        instant = _instant(key)
        if instant is not None and (instant - now).total_seconds() <= lead_seconds:
            return True
    return False
```

```python
warned = False

for step, batch in enumerate(loader, start=resume_step):
    train_step(batch)

    urgent = stop_expected(lead_seconds=2 * CHECKPOINT_SECONDS + 60)
    if dist.is_initialized():
        urgent = any_rank(urgent)          # OR-reduced across ranks

    if step % CHECKPOINT_EVERY == 0 or (urgent and not warned):
        save_atomic(state(step), CHECKPOINT_PATH)
    warned = urgent                        # re-arms if the warning is withdrawn
```

The loop depends on four elements:

- `lead_seconds` is derived from the measured cost of a checkpoint, not guessed.
  A save that starts too late to finish produces no usable checkpoint.
- `any_rank` makes the ranks agree. Each pod carries its own annotations, so in
  a multi-pod job only some members may be marked. Losing any one member ends
  the job, and a collective save that only some ranks enter deadlocks. The flag
  is OR-reduced across ranks and acted on as an aggregate.
- `warned` debounces the urgent save. Tracking the current value, rather than
  latching the first warning, makes the urgent save fire once per warning
  episode, and again if the warning clears and returns.
- `guaranteed-until` is a cue in its own right. Past `guaranteed-until` a
  session is preemptible, and a session that enters that state with an hour-old
  checkpoint can lose an hour of work.

### Stopping Voluntarily

For a batch job, stopping voluntarily is a legitimate response and usually the
better one. Checkpointing, exiting cleanly, and letting a submission system
resubmit the job hands back the capacity the incoming booking needs, chooses the
stopping point, and avoids depending on the grace period. For an interactive
session, checkpointing and continuing is usually the better response. The risk
figure is not a certainty, the warning is frequently withdrawn, and a notebook
that checkpoints and continues is usually still running afterwards.

### The Risk Figure

`termination-warning-risk` is a band, not a probability. It describes the share
of the candidate sessions that has to be stopped, on the assumption that the
choice among them is arbitrary. Where selection follows a policy instead, the
number is only an indication. Use it in coarse thresholds, such as "possible"
and "likely". Where checkpoints are cheap, save on any warning and disregard the
risk figure.

### The Grace Period

A preempted pod is deleted in the ordinary way: `SIGTERM`, then a short interval
before the container is stopped. The interval is long enough to flush data
already staged in memory, and not long enough to write out optimizer state. The
time to checkpoint comes from the warning. The grace period begins only after
the decision to stop the pod has been made. Checkpoint on the warning, not from a
`SIGTERM` handler. The grace period configured for launched pods is not yet
published.

## Resuming

### Selecting the Checkpoint to Load

Load the newest complete checkpoint, which is not always the newest path. The
marker written by the save path distinguishes the two, as described in
[Atomic Checkpoint Writes](#atomic-checkpoint-writes). On any load error, fall
back to the previous checkpoint. That fallback is the reason for keeping more
than one checkpoint.

### Restoring State

Restore everything that was saved, in particular the scheduler and the data
position. A resume that restores only the weights is visible in the loss curve.
The components are listed in
[What a Resumable Checkpoint Contains](#what-a-resumable-checkpoint-contains).

### Loading with `torch.load`

`torch.load` defaults to `weights_only=True` from PyTorch 2.6. A checkpoint
holding anything beyond plain tensors and containers needs those types
allowlisted through `torch.serialization.safe_globals`. Use
`torch.serialization.safe_globals` rather than `weights_only=False`, which
permits arbitrary code execution on load. Where only weights are needed,
`safetensors` avoids the issue. `safetensors` stores tensors only, so optimizer
state still goes through `torch.save`.

### Testing the Resume Path

Test the resume path deliberately:

1. Kill a run at a random step.
2. Restart it.
3. Check that the loss curve is continuous across the restart.

## Checkpointing by Job Shape

| Job | Checkpoint size | Handling |
|---|---|---|
| A LoRA or other adapter fine-tune | Tens of MB (the adapter only) | A save takes seconds, so it can be written often and on any warning. Resuming still needs the optimizer, scheduler, and step count alongside the adapter. The base model is referenced by name rather than copied into the checkpoint |
| A full fine-tune on one node | Model, plus 2-3× that in optimizer state | Saved from one rank where the replicas are identical. The termination warning is of most value in this case |
| From-scratch or large-model training across nodes | Hundreds of GB, sharded | `torch.distributed.checkpoint` handles sharded model and optimizer state together. Asynchronous saves suit the periodic schedule. On a warning, one synchronous save at a step boundary is more reliable than an asynchronous save that may not be flushed |
| A run spanning several reservations | Any | Design the run for restart rather than continuity. A run that resumes cleanly from disk can be scheduled across several windows and interrupted between them at almost no cost |
| Inference or a service pod | Nothing to checkpoint | Use the warning to drain the pod: stop accepting work, finish work in flight, and exit |

## Logging

An unattended job can be understood only from its logs, and a job with no log of
its own cannot be debugged after it ends. Output from `print` statements in a
background run goes nowhere that can be read.

### Redirecting Output

The simplest form of logging is a shell redirect:

```bash
python run.py all > log.txt 2>&1 &
```

`2>&1` is needed because `>` alone captures standard output, and tracebacks
arrive on standard error. Add `python -u` as well. Python buffers output to a
file, and without `-u` an interrupted job can lose its last several minutes of
log.

### The `logging` Module

The `logging` module timestamps every line and records which file and function
produced it, which makes the log searchable:

```python
# randdiv.py
import logging
import numpy as np

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    level=logging.INFO,
                    datefmt='%H:%M:%S',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

def myfunc():
    a = np.random.randint(-5, 5)
    b = np.random.randint(-5, 5)
    if b == 0:
        logging.info('zerodivisionerror preempted')
    else:
        return a / b

print([myfunc() for _ in range(100)])
```

A line in `log.txt` then reads
`2022-10-30 23:37:11,815,815 root INFO zerodivisionerror preempted`, which
records when it happened and where it came from. `filemode='a'` appends, so a
resumed run adds to the existing log instead of erasing it.

### Logging Interruptions

Log four values for correlation with an interruption: wall-clock time, the epoch
or step, the path of the last checkpoint written, and whether a termination
warning was present. When a run ends unexpectedly, these values locate the
restart point and show whether the ending was announced.

## Logs That Outlive the Pod

`kubectl logs <pod-name>` reads from the pod, so it stops working once the pod
is deleted. That includes a pod that deletes itself at the end of a batch job,
and a preempted pod. Use it to inspect a pod that is running, not to keep a
record.

A file in a home directory persists after the pod is deleted. For unattended
work, redirect output into one:

```bash
launch-scipy-ml.sh -g 1 -B -- bash -c 'python -u ./train.py > run.log 2>&1'
```

`run.log` is then readable from the login node while the job is still running,
and after it is gone. Batch mode is described in
[Job Modes](job-modes-and-limits.md#job-modes), and monitoring a job in progress
in [Watching a Running Job](watching-your-job.md).
