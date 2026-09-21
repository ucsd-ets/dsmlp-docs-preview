# The Login Node

`dsmlp-login.ucsd.edu` is the door, not the room. Every user of the platform
passes through this one host on the way to somewhere else, and it is sized for
that job and no other. This page covers reaching it, what belongs on it, and how
to reach the work it starts.

**Contents**

- [Connecting over SSH](#connecting-over-ssh)
- [The Host at the Other End](#the-host-at-the-other-end)
- [What the Login Node Is For](#what-the-login-node-is-for)
- [What It Is Not For](#what-it-is-not-for)
- [The Login Node & the Cluster Nodes](#the-login-node--the-cluster-nodes)
- [What to Do Instead](#what-to-do-instead)
- [Connecting Without a Password](#connecting-without-a-password)
- [Running One Command Without Staying](#running-one-command-without-staying)
- [A Second Shell with `kubesh`](#a-second-shell-with-kubesh)
- [Reaching a Notebook or a Service](#reaching-a-notebook-or-a-service)
- [Reaching a Port From the Login Node](#reaching-a-port-from-the-login-node)
- [The VPN Alternative](#the-vpn-alternative)
- [When the Connection Fails](#when-the-connection-fails)

## Connecting over SSH

------------------------------------------------------------------------

The shell route begins with one command. Everything else — launching containers,
requesting GPUs, running jobs that outlive a connection, attaching an editor —
follows from it.

```bash
ssh <username>@dsmlp-login.ucsd.edu
```

The credentials are the **Active Directory username** — the name in front of
`@ucsd.edu`, not the full address — and the AD password.

**Duo follows, and is challenged once every 8 hours.** A second connection inside
that window does not prompt again.

**The VPN is not required for SSH.** `ssh` to `dsmlp-login.ucsd.edu` works from
anywhere, on or off campus. *What does need the VPN — or an SSH tunnel — is
reaching a port inside a container*, such as a Jupyter server started by a launch
script. → [Reaching a Notebook or a Service](#reaching-a-notebook-or-a-service)

## The Host at the Other End

------------------------------------------------------------------------

**`dsmlp-login.ucsd.edu` is a jumpbox, not a compute machine.** Its purpose is
launching containers on cluster nodes, moving files, and managing what is
running. Running work on it is prohibited.

A connection is therefore followed by a launch:

```bash
launch-scipy-ml.sh -W <WORKSPACE>     # GPU-capable image
launch.sh -h                          # the flag summary, from the tool itself
```

→ [Working from the Command Line](../working-from-the-command-line.md)

**The login node and the container share a filesystem.** A file copied to the
login node with `scp` is in the container, and a file a job writes is on the
login node once the job is over.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

## What the Login Node Is For

------------------------------------------------------------------------

- **Launching containers.** `launch.sh` and its wrappers.
- **Moving files in and out.** `scp`, `sftp`, `rsync`, `git`.
- **Managing running work.** `kubectl get pods`, `kubectl delete pod`,
  `kubesh` to step into a running container.
- **Small housekeeping.** Listing directories, checking disk usage, editing a
  config file, reading a log.

## What It Is Not For

------------------------------------------------------------------------

**Running code.** Python scripts, Java projects, notebooks, training runs, data
conversions, anything with a progress bar. Manual job execution on
`dsmlp-login` is **prohibited by policy**.

**Running an editor's server component.** Running VS Code directly on
`dsmlp-login` is specifically not permitted; it consumes significant CPU and
memory. The supported configuration places VS Code in a container instead.
→ [Remote Editor Setup](remote-editor-setup.md)

## The Login Node & the Cluster Nodes

------------------------------------------------------------------------

**Containers get dedicated resources; the login node is shared ground.** Each
container is assigned CPU, RAM and GPU of its own and is isolated from other
users' processes. The login node is not: what one session takes there comes out
of what everyone else signed in has.

**Everyone passes through it.** A loaded login node does not slow one job — it
degrades launching for everyone signed in.

**The cluster nodes carry the resources.** Many CPU cores, tens of gigabytes of
memory and a GPU are all on the other side of a launch script.

## What to Do Instead

------------------------------------------------------------------------

Three shapes, depending on whether the session is attended.

```bash
launch-scipy-ml.sh -W <WORKSPACE>                    # interactive: a shell in a container
launch-scipy-ml.sh -W <WORKSPACE> -b                 # background: keeps running after a disconnect
launch-scipy-ml.sh -W <WORKSPACE> -B -- python train.py   # batch: runs to completion, then exits
```

→ [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

**Short jobs are launched too.** The overhead of starting a container is seconds.

**The filesystem is shared**, so there is no copying step: files moved to the
login node are already in the container, and files the container writes are
already on the login node.

## Connecting Without a Password

------------------------------------------------------------------------

An SSH key pair removes the password prompt from repeated connections. Generate
a pair on the local machine and install the public half on the login node:

```bash
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub | ssh <username>@dsmlp-login.ucsd.edu \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

*Naming the type with `-t` fixes the file name*, which the second command has to
match; the type a bare `ssh-keygen` picks has changed between OpenSSH releases.

Connect again to check. *A connection that does not ask for the AD password is
using the key* — the key's own passphrase is still requested where one was set.

**A key pair is a prerequisite, not a convenience, for a remote editor.** VS Code
connects through a ProxyCommand that cannot stop to ask for a password, and the
editor's own connection terminates inside the container rather than on the login
node — `launch.sh -H` carries the key installed above into the container at
launch. *The Windows commands, the local file permissions, the SSH agent and the
`IdentityFile` directive are on the editor page* rather than here.
→ [Remote Editor Setup](remote-editor-setup.md#the-key-pair)

## Running One Command Without Staying

------------------------------------------------------------------------

A launch script can be invoked directly over SSH, which is how a job is submitted
from a script on a local machine rather than by hand:

```bash
ssh <username>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh <flags>
```

→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

## A Second Shell with `kubesh`

------------------------------------------------------------------------

**A second shell in a running container comes from `kubesh`**, run on the login
node, rather than from a second container:

```bash
kubectl get pods          # find the pod
kubesh <pod-id>           # step into it
```

*This is the supported way to watch a job that is already running* — a second
launch would start a second container, with its own resources, rather than
attaching to the first.
→ [Watching a Running Job](../running-jobs/watching-your-job.md)

## Reaching a Notebook or a Service

------------------------------------------------------------------------

A container's Jupyter server, and anything else listening inside it, is not
directly reachable from a personal machine. Two SSH tunnels solve that, and they
solve two different problems. **They are not interchangeable, and conflating them
is the usual reason a tunnel "does not work".**

| To reach | Use |
|---|---|
| A port the launcher published **on the login node** — the Jupyter URL | Form 1 |
| A port something is listening on **inside the container** — TensorBoard, a web app started there | Form 2 |

**Form 1 — a port on the login node.** The output of a launch ends with a URL
naming a port on `dsmlp-login.ucsd.edu`. That port is forwarded from a second
terminal on the local machine:

```bash
ssh -N -L 8889:dsmlp-login.ucsd.edu:<port> <user>@dsmlp-login.ucsd.edu
```

`http://localhost:8889/user/<username>/tree/` then opens the session, and the
token from the launch output authenticates it. *Swapping `tree` for `lab` in that
URL gives JupyterLab*, which adds a terminal and an editor.

**Form 2 — a port inside the container.** For a service started by hand, the
tunnel targets the loopback address:

```bash
ssh -N -L localhost:<port>:127.0.0.1:<port> <user>@dsmlp-login.ucsd.edu
```

`localhost:<port>` in a browser then reaches it.

**`-N` means "no command", so a working tunnel prints nothing.** A silent terminal
is success, not a hang. It stays open for as long as the tunnel is wanted, and
`Ctrl+C` closes it.

## Reaching a Port From the Login Node

------------------------------------------------------------------------

**`kubectl port-forward` connects the login node to a port inside a pod**, which
covers the case where the container publishes nothing itself — a custom image with
an overridden entrypoint, for instance:

```bash
kubectl port-forward pods/<pod-name> <port>:8888
```

Combined with Form 1, it is reachable from a local machine.
→ [Building a Custom Image](../environments/building-a-custom-image.md)

**`IDENTITY_PROXY_PORTS=1` before launching** asks for a container port to be
published on the login node, and the launch output then names the port that was
mapped. This is the documented route for TensorBoard and similar dashboards:

```bash
IDENTITY_PROXY_PORTS=1 launch-scipy-ml.sh -g 1
```

*We have not confirmed this against the current launcher* — please tell us if it
no longer behaves as described.
→ [Watching a Running Job](../running-jobs/watching-your-job.md#tensorboard--other-dashboards)

## The VPN Alternative

------------------------------------------------------------------------

**Connected to the campus VPN, the launch URL works as printed** — no tunnel
required. Either route works: the VPN is less to remember, the tunnel is less to
install and does not route the rest of a machine's traffic through campus.

**One of the two is needed, and only for container ports.** A port inside a
container is not reachable from a personal machine on its own, so a Jupyter
server started by `launch.sh` needs either the VPN or a tunnel. *Neither is
needed for `ssh` to the login node, and neither is needed for Datahub in a
browser.* → [Datahub in the Browser](datahub-in-the-browser.md)

## When the Connection Fails

------------------------------------------------------------------------

| Symptom | Usual cause |
|---|---|
| Password refused | The username. Use `username`, not `username@ucsd.edu`, with the AD password |
| The connection hangs after the password | Waiting on Duo — approval is still pending on the phone |
| `Connection timed out` from off campus | A network that blocks outbound SSH — a hotel, a conference, some corporate networks. *The VPN is not required for `ssh`, but connecting to it does route around a block of this kind* |
| A host key warning | Please do not accept it blindly. Where no change was announced, ask us before removing the stored key |
| It connects, but nothing launched will start | Not a connection problem → [Sign-In & Session Problems](sign-in-and-session-problems.md) |
| `channel N: open failed: connect failed: Connection refused` on a forwarded port | The port number, or a local port already in use — see below |

**A tunnel that refuses the connection, or a browser that will not load.** Two
usual causes.

- **The local port is already in use** — often by a tunnel left open in another
  window. `lsof -i :8889` names the process; stopping it, or choosing a different
  local port, clears the collision.
- **The remote port is wrong.** The port in a Jupyter URL is assigned at launch
  and is unlikely to be the same twice. The launch output carries the current one;
  yesterday's command does not.

**If the hostname form fails but the login node is reachable**, some course guides
substitute the login node's numeric address on both sides of the command.
`nslookup dsmlp-login.ucsd.edu` gives it. *This is a workaround for a routing
problem, not the normal path* — please let us know where it is needed.

**A tunnel outlives nothing.** Closing it does not stop a container, and stopping
a container does not close it. The order at the end of a session is to quit
Jupyter or `exit` the container, *then* `Ctrl+C` the tunnel; a container that has
merely been disconnected from may still be running and still holding a GPU.
→ [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
