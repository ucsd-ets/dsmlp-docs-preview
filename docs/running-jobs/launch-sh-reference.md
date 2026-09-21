# `launch.sh` Reference

This is the authoritative list of what `launch.sh` accepts, what it provides by
default, and what the numbers passed to it mean. Work that outlives a terminal
session is covered in [Interactive, Background & Batch Modes](job-modes-and-limits.md#the-three-modes); how long a container may run, in
[The Runtime Limit](job-modes-and-limits.md#the-runtime-limit).

## Where It Lives & How to Call It

------------------------------------------------------------------------

`launch.sh` is on the path once a connection to the login node is established,
and its absolute path is `/opt/launch-sh/bin/launch.sh`.

**Most work goes through a wrapper.** `launch-scipy-ml.sh` starts the GPU-capable
image and `launch-datascience.sh` the CPU one. Each sets environment variables and
then hands off to `launch.sh`, so every flag below behaves identically through a
wrapper. → [Standard Images](../environments/standard-images.md)

**The absolute path is what makes non-interactive submission work.** `ssh` runs a
non-login shell, in which the launcher is not necessarily on the path, so a job
submitted in one line from a personal machine names the launcher in full:

```bash
ssh <user>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -c 8 -m 16 -g 1 \
    -i <image> -f ${HOME}/myproject/run-commands.sh
```

*This is also the form the VS Code `ProxyCommand` uses.*
→ [Remote Editor Setup](../access/remote-editor-setup.md)

## Defaults & The Three Resource Tiers

------------------------------------------------------------------------

**Bare `launch.sh` and the wrappers do not produce the same container.**

| Invocation | CPU | RAM | GPU | Image |
|---|---|---|---|---|
| `launch.sh` | 1 | 1 GB | 0 | `ghcr.io/ucsd-ets/scipy-ml-notebook:stable` |
| `launch-scipy-ml.sh`, `launch-datascience.sh` | 2 | 8 GB | 0 | the wrapper's own image |

*Switching from a wrapper to `launch.sh` directly halves the CPU and leaves an
eighth of the memory, and the symptom is usually a process that dies rather than
an error that explains itself.* **A browser session begins at 2 CPU / 4 GB**,
which is neither figure above — that is a course's spawn configuration rather than
a command-line default. The three numbers describe three different things and all
three are correct.

Limits then apply at three tiers, and confusing them is the usual cause of a job
that will not schedule:

| Tier | Default | Meaning |
|---|---|---|
| A single pod | 8 CPU / 32 GB / 1 GPU | The most any one container receives |
| A namespace, in total | 8 CPU / 64 GB / 1 GPU | Across everything running at once |
| Available on request | up to 32 CPU / 128 GB | Please ask, and say what for |

*`-m 64` is therefore not a valid single-container request even though 64 GB is
the namespace total — that allowance may be spent across several containers, not
in one.* Where an older article or a course README describes 8 CPU / 64 GB / 1 GPU,
or 8 CPU / 16 GB / 1 GPU, as the platform "maximum", it is describing a default,
and in the second case an out-of-date one.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

## Requests Are Half of Limits

------------------------------------------------------------------------

**The number passed is the ceiling, not the reservation.** `launch.sh` sets the
Kubernetes *request* — what the scheduler reserves, and what is actually
guaranteed — to half the *limit* named. `-m 32` reserves 16 GB and permits 32 GB;
the second 16 GB is available only if the node the pod landed on has it spare. The
same halving applies to CPU.

*This is the cause of a whole class of `OOMKilled` reports, and of the case where a
job that ran yesterday fails today on a busier node with no change to the code
that runs in it.* Sizing for the guarantee rather than the ceiling means asking for
32 where a model needs 16 GB to be safe. GPUs are not halved — a GPU is assigned
to one container exclusively, so its request and limit are the same number.

## Flags: Resources & GPU Selection

------------------------------------------------------------------------

| Flag | Effect | Example |
|---|---|---|
| `-c <n>` | CPU cores | `-c 8` |
| `-m <n>` | RAM in GB | `-m 32` |
| `-g <n>` | GPU count | `-g 1` |
| `-v <model>` | Specific GPU model: `1080`, `1080ti`, `2080ti`, `a30`, `a5000`, `a100`, `h100`, `rtxtitan`, `l40s` | `-v l40s` |
| `-l <key=value>` | Apply a pod label. Repeatable | `-l gpu-class=medium` |

`-l gpu-class=<class>` requests a GPU size band rather than a named model, which
is the usual way to ask for a GPU. Medium and above sit behind `NoSchedule`
taints, so a GPU request that omits the label has nowhere to land and fails with
`0/5 nodes available` after a wait. *`-v` and `gpu-class` are two mechanisms at
two layers — `-v` names hardware, `gpu-class` names a size band. Both work; please
use one or the other, not both at once.*
→ [GPU Classes](../gpu-access/gpu-classes.md)

**`-g` is GPU, `-G` is group.** This is the single most common typo on the
platform: `-g 1` requests a GPU, `-G 1` does not, and the failure that follows is
not obviously about capitalization.

| Flag | Effect |
|---|---|
| `-G list` | List the teams the account belongs to, with their team IDs. Launches nothing |
| `-G <teamid>` | Launch with that team as the primary group, so its data is visible |
| `-T` | Mount `/teams` |

```bash
launch-scipy-ml.sh -W DSC180A_FA25_A00 -G list       # find the team ID
launch-scipy-ml.sh -W DSC180A_FA25_A00 -G <teamid>   # then launch with it
```

*`-G list` is the only way to discover a team ID*, and team directory names often
contain brackets, which need quoting in a `cd`. → [Belonging to Several
Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

## Flags: Image, Workspace & Placement

------------------------------------------------------------------------

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

`-i <image> -P Always` is the pair for developing an image: without it, a node
already holding that tag keeps using its copy. *`-x` is for use only at our
request*, and please describe the data to us before reaching for `-M` or `-F`.
→ [Building a Custom Image](../environments/building-a-custom-image.md)

**`-n` takes a bare number.** `-n 30`, not `-n n30` — the leading `n` on the
[status page](../gpu-access/quotas-and-availability.md#the-status-page) is not part of the value. Pinning a
node is rarely useful: a pod whose named node is full waits for that node rather
than taking an equivalent GPU elsewhere. `-l gpu-class=` or `-v` is the flag for
choosing hardware.

The launch output names the node the pod landed on, in a line reading
`INFO pod assigned to node: its-dsmlp-n04.ucsd.edu`; please include it in a problem
report. `-N` gives the pod a name it can be deleted by later, which is what
anything left running unattended needs.

## Flags: How the Job Runs

------------------------------------------------------------------------

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

→ [Interactive, Background & Batch Modes](job-modes-and-limits.md#the-three-modes) explains when each of `-b`, `-B` and `-f` is right.
*`-d` reports what was actually requested*: it prints the specification the cluster
would have received, and consumes nothing.

**`--` separates the launcher's options from the command's own.** Everything after
it is passed into the container untouched.

```bash
launch-scipy-ml.sh -g 1 -B -- python train.py --epochs 50 --lr 0.01
```

Without the separator, `launch.sh` reads `--epochs` as one of its own options and
fails, with a message about a launcher flag rather than about the program being
run.

## Caveats & Limitations

------------------------------------------------------------------------

**`-h` and this page do not list quite the same flags.** The help output is
generated from comments in the launcher's own source, and a few options appear
there which we do not document — some legacy, some interacting with scheduling in
ways that need a conversation first. Please ask us about an undocumented option
rather than experimenting with it on a deadline.

**No root, no sudo, and no flag that grants either.** Containers run unprivileged,
under the member's own UID.
→ [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary)

Flags are not the only way to configure a launch. Every one has an
environment-variable equivalent — the mechanism the wrappers use, and the
alternative to retyping eight flags a day.
→ [Configuring Without Flags](job-modes-and-limits.md#configuring-without-flags)

**Launching a GPU session draws on the workspace's Service Unit budget**, booked
ahead or not. There is no free exploratory launch.
→ [On-Demand Leases Charge Budget](../gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
