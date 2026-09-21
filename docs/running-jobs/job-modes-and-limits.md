# Job Modes, Runtime Limits & Configuration

There are three ways to run something. The difference between them is not how much
compute a job receives — it is what happens when nobody is attached. A container
also has a deadline, and there is a tidier way to configure one than retyping
eight flags every morning.

**Contents**

- [The Three Modes](#the-three-modes)
- [Background Pods](#background-pods)
- [Backgrounding a Pod Versus Backgrounding a Process](#backgrounding-a-pod-versus-backgrounding-a-process)
- [Batch Jobs](#batch-jobs)
- [Running a Script Without a Terminal at All](#running-a-script-without-a-terminal-at-all)
- [Running Several Jobs at Once](#running-several-jobs-at-once)
- [The Runtime Limit](#the-runtime-limit)
- [Raising It to 12 Hours](#raising-it-to-12-hours)
- [Three Different Clocks](#three-different-clocks)
- [Work That Genuinely Needs Longer](#work-that-genuinely-needs-longer)
- [Configuring Without Flags](#configuring-without-flags)
- [The Variables](#the-variables)
- [Copying & Editing a Launch Script](#copying--editing-a-launch-script)

## The Three Modes

------------------------------------------------------------------------

| Mode | Flag | What it provides | The job ends when |
|---|---|---|---|
| Interactive | *(default)* | A shell, or Jupyter, in the container | The connection drops, or the runtime limit is reached |
| Background | `-b` | A pod left running; the session stays on the login node | The pod is deleted, or the runtime limit is reached |
| Batch | `-B -- <command>` | Nothing interactive at all | The command finishes, or the runtime limit is reached |

```bash
launch-scipy-ml.sh -g 1                        # interactive
launch-scipy-ml.sh -g 1 -c 4 -b                # background, reconnect later
launch-scipy-ml.sh -g 1 -B -- python train.py  # batch, runs and exits
```

**Interactive is the default, and it is tied to the connection.** A foreground pod
is terminated when the connection to the login node drops — which includes a
laptop going to sleep, a wifi network dropping, and a lid closing on the way to
class. Work that has to survive that runs under `-b` or `-B`.

## Background Pods

------------------------------------------------------------------------

**`-b` creates the pod and returns a prompt.** The session is not placed inside the
pod, and the prompt is still the login node's, which is not how `&` behaves. The
launch output names the pod, as in `pod/ubellur-27068 created`, and that name is
how it is entered, left, and removed:

```bash
kubesh ubellur-27068               # enter the pod
kubectl get pods                   # list running pods, if the ID is not to hand
kubectl delete pod ubellur-27068   # stop it
```

Once inside, a background pod looks exactly like an interactive launch, with one
difference. **Exiting a pod does not stop processes started inside it.** Leaving by
typing `exit` or pressing `CONTROL+D` leaves everything started in the pod running.

**A background pod holds its resources until it is deleted.** It does not stop at
logout, and it does not stop when the work is finished. *Please delete pods that
are no longer in use:* a GPU attached to an idle container is unusable by anyone
else. → [What Ends a Session](../gpu-access/what-ends-a-session.md)

## Backgrounding a Pod Versus Backgrounding a Process

------------------------------------------------------------------------

- **`-b` backgrounds the pod.** The container keeps running after the login-node
  connection ends.
- **`&` backgrounds a process** inside whatever shell it is typed in. It returns a
  prompt; it does not make the container outlive the session.

They compose. The usual shape of a long run is a background pod with a
backgrounded process inside it:

```bash
launch-scipy-ml.sh -g 1 -c 4 -b     # then: kubesh <pod-id>
python run.py all > log.txt 2>&1 &  # inside the pod
exit
```

Inside the pod, `ps` lists processes and `kill <pid>` stops one. *A process
backgrounded with `&` inside an interactive (non-`-b`) pod dies with the pod.*

`tmux` is sometimes suggested as an alternative to `-b`, and course material
recommends it. It solves a different problem — keeping a *shell session* alive
inside a container that is already going to survive — and we have not confirmed it
is present in the standard images.

## Batch Jobs

------------------------------------------------------------------------

**`-B` is for work that runs and finishes.** No Jupyter, no shell, nothing to
reconnect to. It takes something to run, after `--`:

```bash
launch-scipy-ml.sh -g 1 -B -- python ./train.py
```

The launcher confirms submission and names the pod. From there:

```bash
kubectl get pods                 # Pending until it is scheduled
kubectl describe pod <pod-name>  # why it is still Pending
kubectl logs <pod-name>          # what it printed
kubectl delete pod <pod-name>    # when the work is finished
```

`Pending` is normal rather than an error. A pod stays Pending until what it asked
for becomes free, which for a GPU may be several minutes. A pod that stays Pending
and then fails with `0/5 nodes available` usually has a missing `gpu-class` label
rather than a full cluster to blame.
→ [When the Label Is Missing](../gpu-access/gpu-classes.md#when-the-label-is-missing)

`kubectl logs` reads from the pod, so it is gone when the pod is. Output that has
to be readable tomorrow goes to a file in a home directory instead — home is the
same filesystem the login node sees, so the log outlives the container:

```bash
launch-scipy-ml.sh -g 1 -B -- bash -c 'python ./train.py > out.txt 2>&1'
```

→ [Checkpointing & Logging](checkpointing.md)

## Running a Script Without a Terminal at All

------------------------------------------------------------------------

**`-f <script>` runs a script inside the container and then exits**, dumping the
job's output to the terminal that submitted it. With the launcher's absolute path,
that is one-line submission from a personal machine:

```bash
ssh <user>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -c 8 -m 16 -g 1 \
    -i <image> -f ${HOME}/myproject/run-commands.sh
```

*Paths inside the script must be valid inside the container*, which is not always
the same as valid on the login node. `-f` ends the container when the command ends,
so several pieces of work behind a scarce GPU queue once each under `-f`; `-b` and
a shell inside the pod run them on one launch.

## Running Several Jobs at Once

------------------------------------------------------------------------

**Concurrent sessions are normal use.** A member may have any number of shell, VS
Code and batch jobs running at the same time, alongside a Datahub session. Nothing
has to be stopped before something else is started, and launching from
`dsmlp-login` while a browser session is open is not a conflict.

**One limit is on Datahub itself:** a member may have **one Datahub session**
running, so switching to a different course environment in the browser means
stopping the one that is running.
→ [One Datahub Session](../access/datahub-in-the-browser.md#one-datahub-session)

**The ceiling that binds everything else is aggregate.** Total CPU, memory and GPU
across everything a member has running must fit within the Kubernetes limits set
on their namespace and, where GPUs are involved, within the reservation system's
limits. A launch that would take the total past them is refused, whatever mix of
sessions makes up that total.

*The remedy is to stop something no longer in use rather than to file a request.*
`kubectl get pods` lists what is running and `kubectl delete pod <pod-id>` stops
one. **Every running pod draws resources whether or not it is doing anything**, and
a GPU-holding pod draws Service Units for as long as it lives.
→ [On-Demand Leases Charge Budget](../gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget) ·
[The Other Ceilings](../gpu-access/quotas-and-availability.md#the-other-ceilings)

## The Runtime Limit

------------------------------------------------------------------------

A container has a deadline. When it is reached the container stops, whatever it
was doing, and `kubectl get pods` reports `DeadlineExceeded`.

| | |
|---|---|
| Default runtime | **6 hours** |
| Maximum settable at launch | **12 hours** |
| Longer than that | Email [datahub@ucsd.edu](mailto:datahub@ucsd.edu) and say what for |

*On the Research Cluster the same figures apply, and extension requests go to*
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) *instead.*

**`DeadlineExceeded` is not a fault in the code.** It means the container reached
its limit. Anything written to a home directory survives; anything held only in
memory does not.
→ [Error Messages](../reference/error-messages.md)

**Every mode has the same runtime limit.** `-b` and `-B` do not extend it; they
change what the job is attached to, not how long it may run.

## Raising It to 12 Hours

------------------------------------------------------------------------

The runtime is set by an environment variable, `K8S_TIMEOUT_SECONDS`, read at
launch. It is exported in the shell before launching:

```bash
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
launch-scipy-ml.sh -g 1 -b
```

**The variable is read at launch and not afterwards.** A container that is already
running cannot be extended; the deadline is fixed when the pod is created.

A launch script of one's own carries the setting without retyping.
→ [Copying & Editing a Launch Script](#copying--editing-a-launch-script)

**Asking for 12 hours is not free.** GPU time draws on the workspace's Service
Unit budget. Please request the time the work actually needs rather than the
maximum permitted, and shut the container down when it finishes early.
→ [Service Units & Budgets](../gpu-access/service-units-and-budgets.md)

## Three Different Clocks

------------------------------------------------------------------------

Most confusion about how long a job may run comes from these being conflated. They
are separate, and any one of them can end a container.

| Clock | What it measures | Where it is documented |
|---|---|---|
| **Runtime limit** | Wall-clock time since the pod started, whatever it is doing | This page |
| **Idle culling** | How long the GPU has been doing nothing | [What Ends a Session](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| **The reservation window** | The capacity booked, and until when | [The End of a Window Is Not a Kill](../gpu-access/what-ends-a-session.md#the-end-of-a-window-is-not-a-kill) |

**The runtime limit does not depend on anyone being attached.** Interactive,
background (`-b`) and batch (`-B`) jobs all get the same deadline.

**Idle culling can end a job well inside its runtime limit** — a GPU container
that stops using its GPU is reclaimed after about 30 minutes, though nothing is
culled in its first 45 minutes and a quiet cluster is far more generous. A warning
comes first, and a cull is not a crash.

**Maintenance is a fourth, separate matter.** Instructional maintenance runs
Tuesdays 6-8 AM and generally leaves running jobs alone. The Research Cluster
window is quarterly, at the break between terms, with about 7 days' notice, and
**all running jobs are terminated**. Please do not start a 12-hour run into it.
→ [Maintenance Closures](../gpu-access/what-ends-a-session.md#maintenance-closures)

## Work That Genuinely Needs Longer

------------------------------------------------------------------------

**Runs beyond 12 hours are handled by request rather than by flag.** Write to us,
and say what the job is and roughly how long it needs.

A job that checkpoints can be restarted, and a restartable job is easier to
schedule, easier to recover after a maintenance window, and less costly when
something goes wrong at hour nine.
→ [Checkpointing & Logging](checkpointing.md)

**For sustained multi-day work, a reservation is the mechanism**, not a longer
deadline. → [Reservations](../gpu-access/reservations.md)

## Configuring Without Flags

------------------------------------------------------------------------

Every `launch.sh` flag has an environment-variable equivalent. It is how the
wrapper scripts work, and it is the tidy alternative to retyping eight flags every
morning.

**A wrapper script is a short file that sets variables and then calls the
launcher.** `launch-scipy-ml.sh` and `launch-datascience.sh` each export a
handful of `K8S_*` variables and then `exec launch.sh`. That is the whole
mechanism, and it is available to members as well.

```bash
export K8S_NUM_CPU=8
export K8S_GB_MEM=32
launch-scipy-ml.sh
```

**Flags win.** A value given on the command line overrides the variable, so a
personal default of 8 CPU does not prevent a request for 2 today.

*Variables are read at launch and not afterwards*, exactly like flags. Nothing
exported inside a running container changes that container.

## The Variables

------------------------------------------------------------------------

| Variable | Equivalent to | Notes |
|---|---|---|
| `K8S_NUM_CPU` | `-c` | The reservation is half the number set |
| `K8S_GB_MEM` | `-m` | Likewise |
| `K8S_NUM_GPU` | `-g` | |
| `K8S_DOCKER_IMAGE` | `-i` | |
| `K8S_IMAGE_PULL_POLICY` | `-P` | `Always` while developing an image |
| `K8S_TIMEOUT_SECONDS` | *(no flag)* | Runtime in seconds; see [Raising It to 12 Hours](#raising-it-to-12-hours) |
| `K8S_ENTRYPOINT` | *(no flag)* | What the container runs on start |
| `SPAWN_INTERACTIVE_SHELL` | `-s` / `-S` | Whether a shell is started |
| `PROXY_ENABLED`, `PROXY_PORT` | `-j` / `-J` | Jupyter proxying |
| `K8S_EXPORT_ENV_PREFIX` | *(no flag)* | See below |

**`K8S_EXPORT_ENV_PREFIX` passes chosen variables into the container.** Set the
prefix, and anything in the launching environment carrying it arrives inside the
pod with the prefix stripped:

```bash
export K8S_EXPORT_ENV_PREFIX=MYAPP
export MYAPP_TRACKING_URI=http://example.invalid:5000   # arrives as TRACKING_URI
```

*This is the tidy way to hand a container a configuration value* — an
experiment-tracking URI, a run name — without baking it into an image or a
notebook. *Please do not pass credentials this way:* they end up in shell history
and in the pod's environment, where anything running in the pod can read them.

## Copying & Editing a Launch Script

------------------------------------------------------------------------

Launching the same container every day is a case for copying a wrapper and editing
it:

```bash
cp -p "$(which launch-scipy-ml.sh)" "$HOME/my-launch.sh"
nano "$HOME/my-launch.sh"
"$HOME/my-launch.sh"
```

**`cp -p` preserves the executable bit**, which is the step people miss. Inside is
a short list of variable assignments followed by a call to `launch.sh`; the
numbers can be changed, saved, and run.

A minimal script written from scratch works just as well:

```bash
#!/bin/bash
export K8S_NUM_CPU=4
export K8S_GB_MEM=16
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
exec /opt/launch-sh/bin/launch.sh -W DSC180A_FA25_A00 -g 1 -l gpu-class=medium "$@"
```

**`"$@"` at the end is what keeps the script useful.** It passes anything typed
after the script name through to the launcher, so `./my-launch.sh -b` still works.

*A script like this belongs in a home directory.* Home persists between containers
and is visible from both the login node and inside the pod; anything written
elsewhere in the container does not survive it.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

## Caveats & Limitations

------------------------------------------------------------------------

**Backgrounding does not exempt a job from idle culling.** The test is whether the
GPU is doing anything, not whether a session is attached. A background pod whose
job finished at 2 AM is culled like any other idle GPU container.
→ [Backgrounding Does Not Exempt a Job](../gpu-access/what-ends-a-session.md#backgrounding-does-not-exempt-a-job)

**A personal script is not a supported interface.** If we change a wrapper — the
image it points at, a new default — a copy of it does not change with it. *Please
re-copy at the start of each term*, particularly after a quarterly image update.
→ [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace)

**A course workspace still needs `-W`.** Setting variables does not select a
workspace; a script for a course keeps the `-W` in it.

**A variable left in `.bashrc` applies to every launch.** A default of 8 CPU and a
GPU class in a shell profile means the quick launches ask for that too, at the cost
of waiting time and Service Units.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
