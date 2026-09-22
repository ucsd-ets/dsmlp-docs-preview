# Job Modes, Runtime Limits & Configuration

The three job modes differ in what happens when no session is attached, not in
how much compute a job receives. This page also covers the runtime limit that
applies to every container and configuring a launch with environment variables
instead of flags.

## Job Modes

| Mode | Flag | What it provides | The job ends when |
|---|---|---|---|
| Interactive | None (default) | A shell, or Jupyter, in the container | The connection drops, or the runtime limit is reached |
| Background | `-b` | A pod left running; the session stays on the login node | The pod is deleted, or the runtime limit is reached |
| Batch | `-B -- <command>` | No interactive session | The command finishes, or the runtime limit is reached |

```bash
launch-scipy-ml.sh -g 1                        # interactive
launch-scipy-ml.sh -g 1 -c 4 -b                # background, reconnect later
launch-scipy-ml.sh -g 1 -B -- python train.py  # batch, runs and exits
```

### Interactive Pods

Interactive mode is the default.

> [!WARNING]
> An interactive pod is terminated when the connection to the login node drops,
> including when a laptop goes to sleep, its lid is closed, or its wireless
> network drops.

Run work that must survive a disconnection with `-b` or `-B`.

### Background Pods

`-b` creates the pod and returns a prompt on the login node. The session is not
placed inside the pod. The launch output names the pod, as in
`pod/ubellur-27068 created`, and the pod is entered and deleted by that name:

```bash
kubesh ubellur-27068               # enter the pod
kubectl get pods                   # list running pods and their IDs
kubectl delete pod ubellur-27068   # delete the pod
```

Inside, a background pod behaves like an interactive launch, with one
difference: exiting the pod does not stop processes started inside it. Leaving
with `exit` or `CONTROL+D` leaves everything started in the pod running.

> [!WARNING]
> A background pod holds its resources until it is deleted. It does not stop at
> logout, and it does not stop when its work is finished.

Delete pods that are no longer in use.

Backgrounding does not exempt a job from idle culling. The test is whether the
GPU is doing anything, not whether a session is attached. A background pod whose
job finished at 2 AM is culled like any other idle GPU container, as described in
[Background and Batch Jobs](../gpu-access/what-ends-a-session.md#background-and-batch-jobs).

### Backgrounding a Pod Versus Backgrounding a Process

- `-b` backgrounds the pod. The container keeps running after the login-node
  connection ends.
- `&` backgrounds a process inside the shell it is typed in. It returns a
  prompt. It does not make the container outlive the session.

The two can be combined. A long run is usually a background pod with a
backgrounded process inside it:

```bash
launch-scipy-ml.sh -g 1 -c 4 -b     # then: kubesh <pod-id>
python run.py all > log.txt 2>&1 &  # inside the pod
exit
```

Inside the pod, `ps` lists processes and `kill <pid>` stops one. A process
backgrounded with `&` inside an interactive pod, launched without `-b`, ends
with the pod.

`tmux` is sometimes suggested as an alternative to `-b`, and course material
recommends it. It keeps a shell session alive inside a container that already
persists, which is a different purpose from `-b`. Its presence in the standard
images is not confirmed.

### Batch Jobs

`-B` runs a command to completion and exits. A batch job has no Jupyter server,
no shell, and nothing to reconnect to. The command to run follows `--`:

```bash
launch-scipy-ml.sh -g 1 -B -- python ./train.py
```

The launcher confirms submission and names the pod. The pod is then managed with
`kubectl`:

```bash
kubectl get pods                 # Pending until it is scheduled
kubectl describe pod <pod-name>  # show why it is still Pending
kubectl logs <pod-name>          # show what it printed
kubectl delete pod <pod-name>    # delete it when the work is finished
```

`Pending` is a normal status, not an error. A pod stays Pending until the
resources it requested become free, which for a GPU may take several minutes. A
pod that stays Pending and then fails with `0/5 nodes available` usually has a
missing `gpu-class` label rather than a full cluster, as described in
[Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

`kubectl logs` reads from the pod, so its output is unavailable once the pod is
gone. To keep output after the pod ends, write it to a file in the home
directory. The home directory is on the same filesystem as the login node, so
the file outlives the container:

```bash
launch-scipy-ml.sh -g 1 -B -- bash -c 'python ./train.py > out.txt 2>&1'
```

Logging for long runs is covered in
[Checkpointing & Logging Long Runs](checkpointing.md).

### Running a Script Non-Interactively

`-f <script>` runs a script inside the container, prints the job's output to the
terminal that submitted it, and exits. With the launcher's absolute path, a job
can be submitted from a personal machine in one command:

```bash
ssh <user>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -c 8 -m 16 -g 1 \
    -i <image> -f ${HOME}/myproject/run-commands.sh
```

Paths inside the script must be valid inside the container, which is not always
the same as valid on the login node.

`-f` ends the container when the command ends. When GPUs are scarce, several
pieces of work submitted with `-f` each queue for a GPU separately. A background
pod (`-b`) with a shell inside it runs them all on one launch.

## Running Several Jobs at Once

A member may run any number of shell, VS Code, and batch jobs at the same time,
alongside a Datahub session. Nothing has to be stopped before another job is
started, and launching from `dsmlp-login` while a browser session is open is not
a conflict.

Datahub itself allows a member one running session, as described in
[Concurrent Datahub Sessions](../access/datahub-in-the-browser.md#concurrent-datahub-sessions),
so switching to a different course environment in the browser requires stopping
the running session.

### Aggregate Resource Limits

Total CPU, memory, and GPU across everything a member has running must fit
within the Kubernetes limits set on the member's namespace and, where GPUs are
involved, within the reservation system's limits. A launch that would take the
total past them is refused, whatever mix of sessions makes up that total.

When a launch is refused for this reason, stop a pod that is no longer in use
instead of filing a request. `kubectl get pods` lists what is running, and
`kubectl delete pod <pod-id>` stops a pod.

Every running pod holds its resources whether or not it is doing anything. A
pod that holds a GPU draws Service Units for as long as it runs, as described in
[On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

See also: [Limits That Can Stop a Launch](../gpu-access/quotas-and-availability.md#limits-that-can-stop-a-launch)

## The Runtime Limit

Every container has a runtime limit. When the limit is reached, the container
stops, whatever it was doing, and `kubectl get pods` reports `DeadlineExceeded`.

| Setting | Value |
|---|---|
| Default runtime | 6 hours |
| Maximum settable at launch | 12 hours |
| Longer than 12 hours | By request to [datahub@ucsd.edu](mailto:datahub@ucsd.edu), stating the purpose |

On the Research Cluster, the same figures apply, and extension requests go to
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) instead.

The runtime limit is the same in every mode and does not depend on anyone being
attached. `-b` and `-B` do not extend it. They change what the job is attached
to, not how long it may run.

### The `DeadlineExceeded` Status

`DeadlineExceeded` means the container reached its runtime limit. It does not
indicate a fault in the code. Anything written to a home directory survives, and
anything held only in memory is lost. `DeadlineExceeded` and other pod statuses
are listed in
[Error Messages](../reference/error-messages.md).

### Raising the Runtime Limit

The runtime is set by the environment variable `K8S_TIMEOUT_SECONDS`, in
seconds, and is read at launch. To raise the limit to 12 hours, export the
variable in the shell before launching:

```bash
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
launch-scipy-ml.sh -g 1 -b
```

The variable is read at launch and not afterwards. The deadline is fixed when
the pod is created, and a container that is already running cannot be extended.

A personal launch script can carry the setting, as described in
[Copying & Editing a Launch Script](#copying--editing-a-launch-script).

GPU time draws on the workspace's Service Unit budget, as described in
[Service Units & Budgets](../gpu-access/service-units-and-budgets.md). Request
the runtime the work needs rather than the maximum permitted, and stop the
container when the work finishes early.

### Runtime Limit, Idle Culling, and Reservation Window

The runtime limit, idle culling, and the reservation window are separate, and
any one of them can end a container.

| Mechanism | What it measures | Where it is documented |
|---|---|---|
| Runtime limit | Wall-clock time since the pod started, whatever it is doing | [The Runtime Limit](#the-runtime-limit) |
| Idle culling | How long the GPU has been doing nothing | [What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle) |
| Reservation window | The capacity booked, and until when | [End of a Reservation Window](../gpu-access/what-ends-a-session.md#end-of-a-reservation-window) |

Idle culling can end a job well within its runtime limit: a GPU container that
stops using its GPU is reclaimed, after a warning.

Scheduled maintenance is separate from all three. The schedules are published
under [Scheduled Maintenance](../reference/policy.md#scheduled-maintenance), and
the effect on sessions is described in
[Maintenance Closures](../gpu-access/what-ends-a-session.md#maintenance-closures).
Instructional maintenance generally leaves running jobs alone. Research Cluster
maintenance terminates all running jobs. Do not start a 12-hour run that would
overlap a Research Cluster maintenance window.

### Runs Longer Than 12 Hours

Runs longer than 12 hours are arranged by request, not by a flag. Email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu), or
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu) on the Research Cluster,
stating what the job is and roughly how long it needs.

A job that checkpoints can be restarted. Checkpointing is covered in
[Checkpointing & Logging Long Runs](checkpointing.md).

For sustained multi-day work, the mechanism is a reservation rather than a
longer runtime limit, as described in [Reservations](../gpu-access/reservations.md).

## Configuring Without Flags

Every `launch.sh` flag has an environment-variable equivalent, which is how the
wrapper scripts work.

A **wrapper script** is a short file that sets variables and then calls the
launcher. `launch-scipy-ml.sh` and `launch-datascience.sh` each export several
`K8S_*` variables and then `exec launch.sh`. Members can use the same mechanism:

```bash
export K8S_NUM_CPU=8
export K8S_GB_MEM=32
launch-scipy-ml.sh
```

A value given on the command line overrides the variable. A personal default of
8 CPU does not prevent a request for 2 on a particular launch.

Variables, like flags, are read at launch and not afterwards. A variable
exported inside a running container does not change that container.

A variable set in `.bashrc` applies to every launch. A default of 8 CPU and a
GPU class in a shell profile applies to quick launches too, at the cost of
waiting time and Service Units.

### Environment Variables

| Variable | Equivalent to | Notes |
|---|---|---|
| `K8S_NUM_CPU` | `-c` | The reservation differs from the number set. See [Resource Requests and Limits](launch-sh-reference.md#resource-requests-and-limits) |
| `K8S_GB_MEM` | `-m` | As for `K8S_NUM_CPU` |
| `K8S_NUM_GPU` | `-g` | |
| `K8S_DOCKER_IMAGE` | `-i` | |
| `K8S_IMAGE_PULL_POLICY` | `-P` | `Always` while developing an image |
| `K8S_TIMEOUT_SECONDS` | None | Runtime in seconds. See [Raising the Runtime Limit](#raising-the-runtime-limit) |
| `K8S_ENTRYPOINT` | None | What the container runs on start |
| `SPAWN_INTERACTIVE_SHELL` | `-s` / `-S` | Whether a shell is started |
| `PROXY_ENABLED`, `PROXY_PORT` | `-j` / `-J` | Jupyter proxying |
| `K8S_EXPORT_ENV_PREFIX` | None | See [Passing Variables into a Container](#passing-variables-into-a-container) |

### Passing Variables into a Container

`K8S_EXPORT_ENV_PREFIX` passes selected variables into the container. Every
variable in the launching environment whose name carries the prefix arrives
inside the pod with the prefix stripped:

```bash
export K8S_EXPORT_ENV_PREFIX=MYAPP
export MYAPP_TRACKING_URI=http://example.invalid:5000   # arrives as TRACKING_URI
```

This passes a configuration value, such as an experiment-tracking URI or a run
name, to a container without building it into an image or a notebook.

> [!CAUTION]
> Do not pass credentials this way. They are recorded in shell history and in
> the pod's environment, where anything running in the pod can read them.

### Copying & Editing a Launch Script

To launch the same container repeatedly, copy a wrapper script and edit it:

```bash
cp -p "$(which launch-scipy-ml.sh)" "$HOME/my-launch.sh"
nano "$HOME/my-launch.sh"
"$HOME/my-launch.sh"
```

`cp -p` preserves the executable bit. The copy contains a short list of variable
assignments followed by a call to `launch.sh`. Change the values, save the file,
and run it.

A minimal script can also be written from scratch:

```bash
#!/bin/bash
export K8S_NUM_CPU=4
export K8S_GB_MEM=16
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
exec /opt/launch-sh/bin/launch.sh -W DSC180A_FA25_A00 -g 1 -l gpu-class=medium "$@"
```

The final `"$@"` passes anything typed after the script name through to the
launcher, so `./my-launch.sh -b` still works.

Setting variables does not select a workspace. A script for a course workspace
keeps the `-W` flag.

Keep the script in the home directory. The home directory persists between
containers and is visible from both the login node and inside the pod. Anything
written elsewhere in the container does not survive it, as described in
[Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live).

A personal copy of a wrapper is not a supported interface. When ITS changes a
wrapper, such as the image it points at or a default, a copy does not change
with it. Re-copy the wrapper at the start of each term, particularly after a
quarterly image update.

See also: [Pinning a Workspace](../environments/standard-images.md#pinning-a-workspace)
