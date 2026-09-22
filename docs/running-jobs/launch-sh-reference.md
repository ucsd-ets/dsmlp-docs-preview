# `launch.sh` Reference

This page lists the options `launch.sh` accepts, the resources it provides by
default, and how the resource values passed to it are applied. Work that
continues after a terminal session ends is covered in
[Job Modes](job-modes-and-limits.md#job-modes), and how long a
container may run in [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit).

## Location and Invocation

`launch.sh` is on the path once a connection to the login node is established.
Its absolute path is `/opt/launch-sh/bin/launch.sh`. Containers run unprivileged
under the member's own UID, and no flag grants root or sudo
([Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages)).

### Wrapper Scripts

Most work goes through a wrapper. `launch-scipy-ml.sh` starts the GPU-capable
image and `launch-datascience.sh` starts the CPU image. The images are described
in [Standard Images, Tags, and Pinning](../environments/standard-images.md). Each
wrapper sets environment variables and then hands off to `launch.sh`, so every
`launch.sh` flag behaves identically through a wrapper.

Every flag also has an environment-variable equivalent, which is the mechanism
the wrappers use. The equivalents are covered in
[Configuring Without Flags](job-modes-and-limits.md#configuring-without-flags).

### Non-Interactive Submission

A job submitted in one line from a personal machine names the launcher by its
absolute path, because `ssh` runs a non-login shell in which the launcher is not
necessarily on the path.

```bash
ssh <user>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -c 8 -m 16 -g 1 \
    -i <image> -f ${HOME}/myproject/run-commands.sh
```

The VS Code `ProxyCommand` described in
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

A browser session starts at 2 CPU / 4 GB. That figure is a course's spawn
configuration, not a command-line default, and is described in
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
containers, not in one. Requests for the third tier are made as described in
[Administrative Requests](../reference/getting-help.md#administrative-requests).

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
| `-v <model>` | Specific GPU model: `1080`, `1080ti`, `2080ti`, `a30`, `a5000`, `a100`, `h100`, `rtxtitan`, `l40s` | `-v l40s` |
| `-l <key=value>` | Apply a pod label. Repeatable | `-l gpu-class=medium` |

> [!WARNING]
> Launching a GPU session draws on the workspace's Service Unit budget whether
> or not the session was booked ahead, and there is no free exploratory launch.
> See [On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

### GPU Class and GPU Model

`-l gpu-class=<class>` requests a GPU size band instead of a named model and is
the usual way to request a GPU. The classes are described in
[GPU Classes](../gpu-access/gpu-classes.md). `-v` names
hardware; `gpu-class` names a size band. Both work. Use one or the other, not
both at once.

Classes medium and above carry `NoSchedule` taints, so a GPU request that omits
the `gpu-class` label has no node to run on and fails with `0/5 nodes available`
after a wait ([Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label)).

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
| `-P <policy>` | Image pull policy: `ifnotpresent`, `always`, `never` | `-P Always` |
| `-E` | Add image pull secrets, for a private image. Use with `-i` | |
| `-W <workspace>` | Launch into a workspace, which becomes `$HOME` | `-W DSC10_FA26_A00` |
| `-M <mntspec>` | Subpath-mount an existing filesystem elsewhere in the pod | |
| `-F <mntspec>` | NFS-mount additional filesystems, as `/mnt:server_fqdn:/path` | |
| `-x` | Patch a writeable directory onto the conda package cache | |
| `-n <node>` | Run on a specific node, by number or hostname | `-n 30` |
| `-N <name>` | Give the pod a chosen name | `-N vscode-dsmlp` |
| `-t <toleration>` | Apply a `NoSchedule` toleration. Repeatable | |
| `-A <key=value>` | Apply a pod annotation. Repeatable | |

### Image Pull Policy

For an image under development, as described in
[Building & Publishing a Custom Image](../environments/building-a-custom-image.md),
pass `-i <image> -P Always`. Without `-P Always`, a node already holding that
tag keeps using its copy.

### Mounts and Package Cache

`-x` is used only at the request of ITS. Describe the data to ITS before using
`-M` or `-F`.

### Node Selection

`-n` takes a bare number: `-n 30`, not `-n n30`. The leading `n` shown on
[The Status Page](../gpu-access/quotas-and-availability.md#the-status-page) is
not part of the value. A pod whose named node is full waits for that node and
does not take an equivalent GPU elsewhere. To choose hardware, use
`-l gpu-class=` or `-v`.

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
launch-scipy-ml.sh -g 1 -B -- python train.py --epochs 50 --lr 0.01
```

Without the separator, `launch.sh` reads `--epochs` as one of its own options
and fails with a message about a launcher flag, not about the program being run.

### Help Output and Undocumented Options

The `-h` summary is generated from comments in the launcher's source and does
not list exactly the same flags as this page. It includes options that are not
documented on this page: some are legacy, and some interact with scheduling.
Consult ITS before using an undocumented option.
