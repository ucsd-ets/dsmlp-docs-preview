# Checkpointing & Logging Long Runs

Between the runtime limit, idle culling, reservation windows and the occasional
maintenance closure, there are several ways for a container to stop that have
nothing to do with faulty code. A job that cannot resume is restarted from zero,
and a job with no log of its own cannot be debugged after the fact.

**Contents**

- [What Can End a Run](#what-can-end-a-run)
- [Checkpointing](#checkpointing)
- [What a Resumable Checkpoint Contains](#what-a-resumable-checkpoint-contains)
- [Writing One an Interruption Cannot Corrupt](#writing-one-an-interruption-cannot-corrupt)
- [How Often to Write One](#how-often-to-write-one)
- [The Termination Warning](#the-termination-warning)
- [Reading the Warning From Inside a Container](#reading-the-warning-from-inside-a-container)
- [Acting on the Warning](#acting-on-the-warning)
- [Resuming](#resuming)
- [Checkpointing by Job Shape](#checkpointing-by-job-shape)
- [Logging](#logging)
- [Logs That Outlive the Pod](#logs-that-outlive-the-pod)

## What Can End a Run

------------------------------------------------------------------------

| Cause | Warning | Where it is documented |
|---|---|---|
| The runtime limit — 6 hours by default, 12 if set at launch | None; the pod reports `DeadlineExceeded` | [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit) |
| Idle culling, once the GPU stops being used | Yes; a warning comes first, and the status is recorded on the pod | [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| Preemption, once a booking needs the capacity | Yes; minutes of notice, readable by the job itself | [What Ends a Session](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill) |
| Research Cluster maintenance, quarterly at the term break | About 7 days' notice; **all running jobs are terminated** | [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit) |

*None of these is a fault, and none of them is avoidable by asking.* Instructional
maintenance, on Tuesday mornings, generally leaves running jobs alone.

**Two of the four announce themselves on the pod, where a running program can
read them.** The reservation controller marks a session it may need to stop,
minutes before it stops it; the idle culler records a status and a projected
deadline in the same way. The rest of this page is in two halves: writing a
checkpoint worth resuming from, and using that notice when it arrives.

## Checkpointing

------------------------------------------------------------------------

A checkpoint carries enough state to resume, written on a chosen schedule. For a
training run that usually means the model weights, the optimizer state, and the
epoch or step counter.

**Home is the place to write it.** Home persists between containers, and the
container and the login node share a filesystem, so a checkpoint written by a job
is readable from the login node after the pod is gone. *A path inside the
container that is not a mounted directory dies with the pod* — which is the event
being checkpointed against.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

Checkpointing on wall-clock time rather than only on epochs bounds what an
interruption costs: a limit of 6 hours does not know what an epoch is, and an
epoch that takes 90 minutes loses 90 minutes each time. Something written every 15
or 30 minutes costs very little.

A script that looks for the newest checkpoint and continues from it survives an
interruption nobody was present for; a `--resume` flag has to be remembered.

Checkpoints are large and home directories are quota'd, so the number kept is
worth bounding — the last two and the best one is usually enough. *The old one is
deleted after the new one is complete, not before.* Pruning eagerly is what turns
one badly timed interruption into total loss.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

## What a Resumable Checkpoint Contains

------------------------------------------------------------------------

**A checkpoint holding only model weights resumes a different run.** Everything
below is state the optimizer or the data pipeline carries, and omitting any of it
shows up as a jump in the loss curve at the point of resume.

| Component | Call | Notes |
|---|---|---|
| Model weights | `model.state_dict()` | Under `torch.compile` the keys gain an `_orig_mod.` prefix. Saving `model._orig_mod.state_dict()`, or stripping the prefix on load, keeps the checkpoint loadable by an uncompiled model |
| Optimizer | `optimizer.state_dict()` | The large one: Adam and AdamW carry two `fp32` moments, so optimizer state is commonly 2-3× the model in bytes |
| Learning-rate scheduler | `scheduler.state_dict()` | Cheap, and the one most often forgotten. Without it a warmup or cosine schedule restarts from the beginning |
| Mixed-precision scaler | `scaler.state_dict()` | `torch.amp.GradScaler` holds an adaptive loss scale; a resume without it re-converges through a few skipped steps |
| Step and epoch counters | Kept by the training script | The anchor a resume is expressed in |
| Data position | `StatefulDataLoader.state_dict()` | `torchdata`'s drop-in `DataLoader` replacement, which supports mid-epoch resume without replaying batches. It requires the same `num_workers` on load as on save |
| Random number generator state | `torch.get_rng_state()`, `torch.cuda.get_rng_state_all()`, `random.getstate()`, `numpy.random.get_state()` | Needed for a bit-comparable resume — dropout, augmentation, sampling. Skipping it is reasonable where reproducibility does not matter, and worth skipping deliberately rather than by accident |
| Averaged weights and metric state | Kept by the training script | Exponential moving averages, best-so-far metrics, early-stopping counters |

*The run's configuration belongs next to the weights.* A checkpoint that cannot be
identified six weeks later is half a checkpoint.

## Writing One an Interruption Cannot Corrupt

------------------------------------------------------------------------

The failure mode these interruptions create is precisely a process disappearing
mid-write. Two rules cover it.

**A single-file save is written to a temporary path, flushed, then renamed.**
`os.replace` is atomic within one filesystem, so the visible path is always either
the complete old checkpoint or the complete new one, and never a truncated file:

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

Skipping this is how a run ends up with `RuntimeError: unexpected EOF` from the
only checkpoint it had.

**A sharded save is completed, then published.** A distributed checkpoint is a
directory of per-rank shards, and there is no atomic rename covering "all of them
landed". The equivalents are to write into a scratch directory and rename the
*directory* once every rank has finished, or to write an explicit `DONE` marker
last and have the resume path ignore any directory without one. With
`torch.distributed.checkpoint`, the `.metadata` file is written after the shards,
so its absence is a reasonable signal that a directory is incomplete — but an
explicit marker is the thing to depend on.

## How Often to Write One

------------------------------------------------------------------------

The classical answer is the Young/Daly interval: checkpoint every
`sqrt(2 · C · MTBF)`, where `C` is the wall-clock cost of one checkpoint and
`MTBF` is the mean time between interruptions. It balances saving so often that
the saving dominates against saving so rarely that each interruption costs hours.

**Under a reservation system that announces its interruptions, the cadence can be
set from `C` alone.** A common target is checkpoint overhead below about 5% of
step time, which for a synchronous save means an interval of roughly `20 × C`.
That covers the interruptions nothing warns about — a node failure, an out-of-memory
kill, a collective that times out. The termination warning covers the announced
ones, and is what turns "lose up to one interval" into "lose up to one step".

*`C` is worth measuring once on the storage actually being written to, and
logging.* Every figure in this section is expressed in terms of it, and the
assumed value is consistently optimistic.

**Where `C` is large, asynchronous checkpointing is the answer before a longer
interval is.** `torch.distributed.checkpoint` offers `dcp.async_save`, which
stages tensors into CPU buffers and writes them from a background thread while
training continues, dropping the blocking part of the save to roughly the staging
copy. Two costs come with it: host memory on the order of one checkpoint per rank,
and the requirement to keep one outstanding save at a time — the previous future
is waited on before the next is issued, or the memory multiplies. *An asynchronous
save that was never flushed is not a checkpoint*, so the outstanding future is
waited on before exiting on a preemption.

## The Termination Warning

------------------------------------------------------------------------

**A session the controller may need to stop is marked as such before it is
stopped.** The mark is a set of annotations written onto the pod, and it appears
only while the session is genuinely at risk — a booking is coming due for capacity
this session is holding, and this session is one of the candidates that could
supply it.

**A session inside its runtime guarantee is never stopped**, however short the
cluster is. The mark can still appear while the guarantee is running, when the
booking that wants the capacity falls after the guarantee ends — it then says that
the reclaim is queued for the moment the protection lapses. That is the most
useful warning of the lot to a job that checkpoints, because it arrives while
there is still plenty of time to act on it.
→ [What Ends a Session](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill)

Four of the annotations matter to a long-running job:

| Annotation | Value | What it says |
|---|---|---|
| `galends/guaranteed-until` | UTC instant, `YYYY-MM-DDTHH:MM:SSZ` | The end of the protected period. It can move **later** while the session runs, when an abutting follow-on window is booked |
| `galends/termination-warning-at` | UTC instant, same format | The **earliest** moment the session could be stopped. Never earlier than `guaranteed-until`. Present only while the session is at risk |
| `galends/termination-warning-risk` | Decimal between 0 and 1, two places, e.g. `0.33` | The share of the candidates that has to be stopped. `1.00` means all of them |
| `galends/termination-warning-message` | A sentence | The same thing in prose, in the cluster's local timezone. Written to be displayed as it stands, and not to be parsed |

**`termination-warning-at` is the earliest possible stop, not a scheduled one.**
The shortfall it was computed from may be gone before it arrives, in which case
nothing happens and the annotations are removed again. A job that counts down to
it and declares itself dead is wrong; a job that treats the moment as the start of
"may be stopped at any time" is right.

**Extending or re-booking the window cancels a pending termination**, and does so
right up until the pod is deleted. The controller re-checks every session's live
guarantee before it selects anything, so a reservation that lands first always
wins. → [Continue, Extend & Adopt](../gpu-access/reservations.md#continue-extend--adopt)

<!-- FIGURE: how far ahead of the earliest stop the warning appears, and whether any minimum notice is guaranteed -->

## Reading the Warning From Inside a Container

------------------------------------------------------------------------

**Annotations are not visible to the container unless the pod spec projects
them.** A downward-API volume does that, and it is refreshed as the values change:

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

Each file then holds one value, raw — no quoting, no escaping, no trailing
newline, so `$(cat …)` is the value:

```console
$ cat /etc/podinfo/termination-warning-at; echo
2026-08-21T17:30:16Z
$ cat /etc/podinfo/termination-warning-risk; echo
0.33
```

**An absent annotation is an empty file, not a missing one.** All four files are
created when the pod starts, and the three warning files stay empty for as long as
the session is not at risk — which is most of most runs. A test for one of them
uses `-s`, "exists and is not empty"; `-f` and `-e` are true from the pod's first
second, so a loop guarded on either bails immediately, every time, and does so
silently.

*Environment variables are the wrong mechanism here.* A downward-API environment
variable is resolved once when the container starts, and every value on this page
is written after that and some of them change during the run. Only the volume is
refreshed.

**The refresh is not instant.** The kubelet updates the files on its own sync
loop, which adds to the controller's own cadence — so the warning reaches the
container some way into the notice period, not at the start of it. Polling every
15 to 30 seconds is ample; watching the files with `inotify` needs the *directory*
watched rather than the file, since the whole set is swapped atomically behind a
symlink.

<!-- FIGURE: the worst-case delay between the controller writing an annotation and the container being able to read it -->

*Projecting the whole annotation map into a single file is also possible*, with
`fieldPath: metadata.annotations` and no subscript. That file carries every
annotation the session has — the reservation behind it, its GPU class, when it was
admitted — one per line as `key="value"`, with quotes and escapes that have to be
undone. The per-key files above avoid the parser and are enough for checkpointing.

**The idle culler publishes its own status the same way.** `dsmlp/idle-gpu-status`
and `dsmlp/idle-gpu-cull-deadline` are annotations on the same pod, and an
additional `fieldRef` for each projects them alongside the four above. A job whose
GPU goes quiet between phases is at risk from the culler on a timetable of its
own, entirely separately from any reservation.
→ [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

## Acting on the Warning

------------------------------------------------------------------------

**A batch job that processes work in units — shards, epochs, sweeps — usually
needs nothing more than to stop starting new ones.** The check goes between units,
never inside one:

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

**The test is re-read every time round the loop, and no result is remembered.**
Warnings are withdrawn — the window gets extended, the incoming booking never
claims its capacity, the session is re-linked to another reservation — and the
file goes empty again. A job that recorded the first warning it saw would stop for
one that had already been called off. *Where a job would rather carry on than
hand back its remaining units*, the same test is worth making and logging rather
than acting on; only the response changes.

**A training loop checkpoints at a step boundary and not from a signal handler.**
Saving mid-backward captures inconsistent state, and under distributed training a
save is a collective operation every rank has to enter in the same iteration:

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
        urgent = any_rank(urgent)          # see below

    if step % CHECKPOINT_EVERY == 0 or (urgent and not warned):
        save_atomic(state(step), CHECKPOINT_PATH)
    warned = urgent                        # re-arms if the warning is withdrawn
```

Four things in that loop earn their place:

- **The lead time is derived from the measured cost of a checkpoint**, not
  guessed. A save that starts too late to finish is worth no more than one that
  never started.
- **`any_rank` makes the ranks agree.** Each pod carries its own annotations, so
  in a multi-pod job only some members may be marked — but losing any one member
  ends the job, and a collective save that only some ranks enter deadlocks. The
  flag is OR-reduced across ranks and acted on as an aggregate.
- **`warned` debounces.** Tracking the current value rather than latching makes
  the urgent save fire once per episode, and fire again if the warning clears and
  returns.
- **The guarantee ending is a cue in its own right.** Past `guaranteed-until` a
  session is preemptible, and entering that state on an hour-old checkpoint is a
  self-inflicted loss.

**Stopping voluntarily is a legitimate response, and for a batch job usually the
better one.** Checkpointing, exiting cleanly and letting a submission system
resubmit hands back the capacity the incoming booking wanted, picks the stopping
point, and skips the scramble in the grace period entirely. *For an interactive
session the opposite holds*: the risk figure is not a certainty, the warning is
frequently withdrawn, and a notebook that checkpoints and carries on will usually
still be there afterwards.

**The risk figure is a band, not a probability.** It describes what share of the
candidate sessions has to be stopped, on the assumption that the choice among them
is arbitrary; where selection follows a policy instead, the number is only an
indication. Thresholding it coarsely — "possible", "likely" — is the sound use of
it. Where checkpoints are cheap, ignoring it and saving on any warning at all is
sounder still.

## Resuming

------------------------------------------------------------------------

The save path gets the attention; the resume path is where the defects are.

- **The newest *complete* checkpoint is the one to load**, which is not always the
  newest path. The marker written in the save path is what distinguishes them, and
  falling back to the previous checkpoint on any load error is the entire reason
  for keeping more than one.
- **Everything that was saved has to be restored** — in particular the scheduler
  and the data position. A resume that restores only weights is visible in the
  loss curve.
- **`torch.load` defaults to `weights_only=True` from PyTorch 2.6.** A checkpoint
  holding anything beyond plain tensors and containers needs those types
  allowlisted through `torch.serialization.safe_globals`. That is the thing to
  reach for rather than `weights_only=False`, which permits arbitrary code
  execution on load. Where only weights are needed, `safetensors` avoids the
  question — though it stores tensors only, so optimizer state still goes through
  `torch.save`.
- **The resume path is tested deliberately.** A run killed at a random step,
  restarted, and checked for a continuous loss curve establishes that it works.
  Preemption will run this test eventually; better that it is not the first time.

## Checkpointing by Job Shape

------------------------------------------------------------------------

| Job | Checkpoint size | What follows from it |
|---|---|---|
| A LoRA or other adapter fine-tune | Tens of MB — the adapter only | The cost of a save is seconds, so it can be written often and on any warning. Resuming still needs the optimizer, scheduler and step count alongside the adapter; the base model is referenced by name rather than copied into the checkpoint |
| A full fine-tune on one node | Model, plus 2-3× that in optimizer state | Saved from one rank where the replicas are identical. This is the case where the warning pays for itself most clearly |
| From-scratch or large-model training across nodes | Hundreds of GB, sharded | `torch.distributed.checkpoint` handles sharded model and optimizer state together. Asynchronous saves suit the periodic cadence; on a warning, one synchronous save at a step boundary beats racing an asynchronous one that may not get flushed |
| A run spanning several reservations | Any | Designed for restart rather than continuity. A run that resumes cleanly from disk can be scheduled across several windows and interrupted between them at almost no cost |
| Inference or a service pod | Nothing to checkpoint | The warning is used to drain: stop accepting work, finish what is in flight, exit |

## Logging

------------------------------------------------------------------------

An unattended job can only be understood from its logs. Output from `print`
statements in a background run goes nowhere anyone can read it, and a failed trial
costs hours rather than seconds. **The crude version is a redirect**, and it is
much better than nothing:

```bash
python run.py all > log.txt 2>&1 &
```

*The `2>&1` matters* — `>` alone captures standard output, and tracebacks arrive
on standard error. *`python -u` is worth adding too*, since Python buffers output
to a file and an interrupted job can otherwise lose its last several minutes of
log.

**The better version is the `logging` module.** It timestamps every line and
records which file and function produced it, which is the difference between a log
that can be searched and a wall of text:

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
`2022-10-30 23:37:11,815,815 root INFO zerodivisionerror preempted` — naming when
it happened and where it came from. `filemode='a'` appends, so a resumed run adds
to the record instead of erasing it.

Four things are worth correlating with an interruption: wall-clock time, the epoch
or step, the path of the last checkpoint written, and whether a termination
warning was present. When a run ends unexpectedly, those four lines locate the
restart point and say whether the ending was announced.

## Logs That Outlive the Pod

------------------------------------------------------------------------

**`kubectl logs <pod-name>` reads from the pod**, so it stops working the moment
the pod is deleted — including when the pod deletes itself at the end of a batch
job, and including a preemption. It is for looking at something now, not for
keeping a record.

A file in a home directory outlives everything. For unattended work, please
redirect into one:

```bash
launch-scipy-ml.sh -g 1 -B -- bash -c 'python -u ./train.py > run.log 2>&1'
```

`run.log` is then readable from the login node while the job is still running, and
after it is gone.
→ [Interactive, Background & Batch Modes](job-modes-and-limits.md#the-three-modes) · [Watching a Running Job](watching-your-job.md)

## Caveats & Limitations

------------------------------------------------------------------------

**A deadline gives no warning at all.** The runtime limit stops the container at
its appointed second with nothing beforehand and nothing to catch, and the
Research Cluster maintenance window terminates every running job that is in it.
Neither is announced on the pod, so neither can be prepared for in the moment:
whatever matters has to be on disk before either arrives.
→ [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit)

**The grace period is not a checkpointing window.** A preempted pod is deleted the
ordinary way — `SIGTERM`, then a short interval before the container is stopped —
which is long enough to flush something already staged in memory and nowhere near
long enough to write an optimizer state out. *The warning is what buys the time;
the grace period is what is left after the decision has been made.* A strategy
resting on the signal handler is a strategy resting on the wrong one of the two.
<!-- FIGURE: the termination grace period actually configured for launched pods -->

**The guarantee is not a deadline either.** Past `guaranteed-until` a job is not
stopped — it keeps running until somebody else's reservation needs the capacity.
Exiting at the guarantee gives up time that was there for the taking. Tightening
the checkpoint cadence at that point is the response, since from that instant the
job is stoppable on notice it does not control.

**Every one of these annotations is optional and best-effort.** Any of them can be
absent at any moment, the warning trio disappears when the risk clears, and none
of them is read back by the controller to decide anything — the decision is
recomputed from live reservation state each time. Code that reads them handles
each one missing, ignores a value that does not parse rather than failing, and
never caches at startup what it can re-read.

**Please do not checkpoint into a shared or course-wide directory**
unintentionally — it is quota'd for the class, not for one run.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
