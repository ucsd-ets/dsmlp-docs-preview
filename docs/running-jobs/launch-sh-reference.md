# `launch.sh` Reference

This page lists the options `launch.sh` accepts, the resources it provides by
default, and how the resource values passed to it are applied.
[Job Modes](job-modes-and-limits.md#job-modes) covers work that continues after
a terminal session ends.
[The Runtime Limit](job-modes-and-limits.md#the-runtime-limit) covers how long a
container may run.

## Location and Invocation

`launch.sh` is on the path once a connection to the login node is established.
Its absolute path is `/opt/launch-sh/bin/launch.sh`. Containers run unprivileged
under the member's own UID, and no flag grants root or sudo
([Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages)).

### Wrapper Scripts

Most work goes through a wrapper. `launch-scipy-ml.sh` starts the GPU-capable
image and `launch-datascience.sh` starts the CPU image.
[Standard Images, Tags, and Pinning](../environments/standard-images.md)
describes the images. Each
wrapper sets environment variables and then hands off to `launch.sh`, so every
`launch.sh` flag behaves identically through a wrapper.

Every flag also has an environment-variable equivalent, which is the mechanism
the wrappers use.
[Configuring Without Flags](job-modes-and-limits.md#configuring-without-flags)
covers the equivalents.

### Non-Interactive Submission

A job submitted in one line from a personal machine names the launcher by its
absolute path, because `ssh` runs a non-login shell in which the launcher is not
necessarily on the path.

```bash
ssh <user>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -W DSC40_FA26_001 \
    -c 8 -m 16 -g 1 -l gpu-class=medium \
    -i <image> -f ${HOME}/myproject/run-commands.sh
```

The VS Code `ProxyCommand` in
[Remote Editor Setup](../access/remote-editor-setup.md) uses the same form.

## Defaults and Resource Tiers

### Default Resources

Bare `launch.sh` and the wrappers start containers with different defaults.

| Invocation | CPU | RAM | GPU | Image |
|---|---|---|---|---|
| `launch.sh` | 1 | 1 GB | 0 | `ghcr.io/ucsd-ets/scipy-ml-notebook:stable` |
| `launch-scipy-ml.sh`, `launch-datascience.sh` | 2 | 8 GB | 0 | the wrapper's own image |

Calling `launch.sh` directly instead of a wrapper halves the CPU and leaves one
eighth of the memory. The usual symptom is a process that dies without an error
that explains the cause.

A browser session starts at 2 CPU / 4 GB by default. That figure is a course's
spawn configuration, not a command-line default. See
[The Browser Session](../access/datahub-in-the-browser.md#the-browser-session).
The three sets of figures describe three different things.

### Resource Tiers

Limits apply at three tiers. Confusing the tiers is the usual cause of a job
that does not schedule.

| Tier | Default | Meaning |
|---|---|---|
| A single pod | 8 CPU / 32 GB / 1 GPU | The most any one container receives |
| A namespace, in total | 8 CPU / 64 GB / 1 GPU | Across everything running at once |
| Available on request | up to 32 CPU / 128 GB | On request, with the purpose stated |

`-m 64` is not a valid request for a single container, although 64 GB is the
namespace total. The namespace allowance may be spent across several
containers, not in one.
[Administrative Requests](../reference/getting-help.md#administrative-requests)
covers requests for the third tier.

The GPU default is a limit per account: 1 GPU at a time, across every pod the
account runs. It applies on top of the reservation system's limits, so a booking
for several GPUs, or several overlapping bookings, does not raise it. For
multi-GPU work, the member, or a TA for a course, asks ITS to raise the
account's limit, by ticket to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

An older article or course README that describes 8 CPU / 64 GB / 1 GPU or
8 CPU / 16 GB / 1 GPU as the platform maximum is describing a default. The
8 CPU / 16 GB / 1 GPU figure is out of date.

## Resource Requests and Limits

The value passed to `-c` or `-m` is the **limit**, the most the container may
use. `launch.sh` sets the Kubernetes **request**, the amount the scheduler
reserves and the only amount guaranteed, to half the limit. `-m 32` reserves
16 GB and permits 32 GB. The second 16 GB is available only if the node the pod
runs on has it spare. The same halving applies to CPU.

The halving causes many `OOMKilled` (out-of-memory) reports. It also explains a
job that succeeds on one run and fails on a later run, on a busier node, with no
change to its code. Size a job for the guarantee, not the limit: to guarantee a
model 16 GB, launch it with `-m 32`.

GPUs are not halved. A GPU is assigned to one container exclusively, so its
request and limit are the same number.

## Resource and GPU Selection Flags

| Flag | Effect | Example |
|---|---|---|
| `-c <n>` | CPU cores | `-c 8` |
| `-m <n>` | RAM in GB | `-m 32` |
| `-g <n>` | GPU count | `-g 1` |
| `-l <key=value>` | Apply a pod label. Repeatable | `-l gpu-class=medium` |
| `-v <model>` | GPU model, within the class `-l gpu-class=` names. Use it only for a session launched without a booking | `-v l40s` |

> [!WARNING]
> Launching a GPU session draws on the workspace's Service Unit budget whether
> or not the session was booked ahead, and there is no free exploratory launch.
> See [On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

### GPU Class

`-l gpu-class=<class>` requests a GPU size band, and every GPU request needs it.
[GPU Classes](../gpu-access/gpu-classes.md) lists the classes. `-v` narrows a
class to one GPU model and does not replace the label; see
[Node Selection](#node-selection).

Every GPU class is managed by the reservation system, which admits only pods
that carry the `gpu-class` label. A GPU request that omits the label waits in
`Pending` with no event from the reservation system
([Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label)).

### Workspace and GPU Charges

`-W <workspace>` also sets the pod's `dsmlp/course` and `dsmlp/user` labels.
`dsmlp/course` decides which workspace's Service Unit budget a GPU session is
charged to, and which bookings it can claim. The cluster mounts the workspace
home directory, `public/`, and `private/` only into a pod that carries both
labels; see
[Home Directories in Manifest Pods](kubernetes.md#home-directories-in-manifest-pods).
A GPU launch without `-W` is charged to `ORG_ON_DEMAND`, the default workspace,
and never claims a course booking. See
[Claiming a Booking](../gpu-access/reservations.md#claiming-a-booking) and
[The Default Workspace](../gpu-access/reservations.md#the-default-workspace).

### Team Selection

> [!NOTE]
> `-g` is the GPU count and `-G` is the group flag. `-g 1` requests a GPU and
> `-G 1` does not, and the failure that follows does not point to the
> capitalization.

| Flag | Effect |
|---|---|
| `-G list` | List the teams the account belongs to, with their team IDs. Launches nothing |
| `-G <teamid>` | Launch with that team as the primary group, so its data is visible |
| `-T` | Mount `/teams` |

```bash
launch-scipy-ml.sh -W DSC180A_FA25_A00 -G list       # find the team ID
launch-scipy-ml.sh -W DSC180A_FA25_A00 -G <teamid>   # then launch with it
```

`-G list` is the only way to discover a team ID. Team directory names often
contain brackets, which must be quoted in a `cd` command.

See also: [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

## Image, Workspace, and Placement Flags

| Flag | Effect | Example |
|---|---|---|
| `-i <image>` | Alternate container image | `-i ghcr.io/ucsd-ets/scipy-ml-notebook:2024.4-stable` |
| `-P <policy>` | Image pull policy: `Always`, `IfNotPresent`, or `Never` | `-P Always` |
| `-E` | Add image pull secrets, for a private image. Use with `-i` | |
| `-W <workspace>` | Launch into a workspace, which becomes `$HOME`, and charge GPU time to it | `-W DSC10_FA26_A00` |
| `-M <mntspec>` | Subpath-mount an existing filesystem elsewhere in the pod | |
| `-F <mntspec>` | NFS-mount additional filesystems, as `/mnt:server_fqdn:/path` | |
| `-x` | Patch a writeable directory onto the conda package cache | |
| `-n <node>` | Run on a specific node, by number or hostname. Use it only for a session launched without a booking | `-n 30` |
| `-N <name>` | Give the pod a chosen name | `-N vscode-dsmlp` |
| `-t <toleration>` | Apply a `NoSchedule` toleration. Repeatable | |
| `-A <key=value>` | Apply a pod annotation. Repeatable | |

### Image Pull Policy

For an image under development, pass `-i <image> -P Always`. See
[Building & Publishing a Custom Image](../environments/building-a-custom-image.md).
Without `-P Always`, a node already holding that
tag keeps using its copy.

`-P` passes its value to Kubernetes, which accepts only `Always`,
`IfNotPresent`, and `Never`, with that capitalization. A lowercase value such as
`always` is rejected.

### Mounts and Package Cache

`-x` is used only at the request of ITS. Describe the data to ITS before using
`-M` or `-F`.

### Node Selection

`-n` and `-v` each limit the nodes a session can run on. `-n` names one node.
`-v` names a GPU model, and limits the session to the nodes that carry it.

`-n` takes a bare number: `-n 30`, not `-n n30`. The leading `n` shown on
[The Status Page](../gpu-access/quotas-and-availability.md#the-status-page) is
not part of the value. A pod whose named node is full waits for that node and
does not take the same GPU elsewhere. To choose a GPU size, use
`-l gpu-class=`.

`-v` narrows a GPU class and does not replace it. Pass the class label as well,
and name a model that backs that class in
[GPU Class Sizes](../gpu-access/gpu-classes.md#gpu-class-sizes):

```bash
launch-scipy-ml.sh -W DSC40_FA26_001 -g 1 -l gpu-class=large -v l40s
```

The `-h` summary lists the model names. A pod whose model has no free GPU waits
for one and does not take another model of its class. A GPU launch with `-v`
and no class label waits in `Pending` with no event from the reservation
system; see
[Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

> [!WARNING]
> Use `-n` or `-v` only for a session launched without a booking. A booking is
> charged when it is made, and a session limited to a node or a GPU model
> claims its booking while it waits for that node or model. A busy node or
> model can therefore use up the whole window before the session starts. See
> [The Claim Window](../gpu-access/reservations.md#the-claim-window).

Without a booking, a session limited with `-n` or `-v` is given no on-demand
lease, and is not charged, until a node it allows has a free GPU. It records a
[`WaitingForNode`](../reference/reservation-events.md#waitingfornode) event
while it waits. A session whose `-n` or `-v` matches no node of its GPU class
records a [`NoMatchingNode`](../reference/reservation-events.md#nomatchingnode)
event and is given no lease. The usual causes are a node that does not exist,
is out of service, or belongs to another class, and a model that does not back
the class.

The launch output names the node the pod was assigned to, in a line such as
`INFO pod assigned to node: its-dsmlp-n04.ucsd.edu`. Include that line in a
problem report.

### Pod Names

`-N` gives the pod a name by which it can be deleted later. Give a name to any
pod left running unattended.

## Job Execution Flags

| Flag | Effect |
|---|---|
| `-b` | Background pod: created and left running, with the session returned to the login node |
| `-B` | Batch: queue the job and do not wait for it |
| `-f <script>` | Run a script inside the container non-interactively, then exit |
| `-s` | CLI shell only; do not start Jupyter |
| `-S` | Do not start a container shell |
| `-j` / `-J` | Start / inhibit Jupyter. Starting is the default |
| `-H` | Start an SSH server inside the container, for `ProxyCommand` use |
| `-u` | Send email when the job begins running |
| `-q` / `-Q` | Quiet / verbose |
| `-d` | Dump the pod spec as JSON and do not execute |
| `-h` | Flag summary |
| `--` | End of launcher options |

[Job Modes](job-modes-and-limits.md#job-modes) describes when to use
each of `-b`, `-B`, and `-f`. `-d` prints the specification the cluster would
have received and consumes nothing. Its output shows what a set of flags
actually requests.

### Option Separator

`--` separates the launcher's options from the command's own. Everything after
it is passed into the container untouched.

```bash
launch-scipy-ml.sh -W DSC40_FA26_001 -g 1 -l gpu-class=medium -B -- python train.py --epochs 50 --lr 0.01
```

Without the separator, `launch.sh` reads `--epochs` as one of its own options
and fails with a message about a launcher flag, not about the program being run.

### Help Output and Undocumented Options

The `-h` summary is generated from comments in the launcher's source and does
not list exactly the same flags as this page. It includes options that are not
documented on this page: some are legacy, and some interact with scheduling.
Consult ITS before using an undocumented option.
