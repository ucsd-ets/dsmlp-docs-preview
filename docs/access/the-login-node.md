# The Login Node

`dsmlp-login.ucsd.edu` is a login node for launching jobs and transferring
files. Running computation on it is prohibited.

## Connecting over SSH

Launching containers, requesting GPUs, running jobs that outlive a connection,
and attaching an editor all begin with an SSH connection to the login node:

```bash
ssh <username>@dsmlp-login.ucsd.edu
```

The username is the Active Directory (AD) username, which is the part of the
address before `@ucsd.edu`. The full address is not accepted. The password is
the AD password.

### Duo Authentication

Duo follows the password and is challenged once every 8 hours. A second
connection within that window does not prompt again.

### VPN Requirement

The VPN is not required for SSH to the login node. `ssh` to
`dsmlp-login.ucsd.edu` works from anywhere, on or off campus. The VPN or an SSH
tunnel is required only to reach a port inside a container, such as a Jupyter
server started by a launch script.

See also: [Reaching a Notebook or a Service](#reaching-a-notebook-or-a-service)

## What the Login Node Is For

`dsmlp-login.ucsd.edu` is a jumpbox. It is for launching containers on cluster
nodes, moving files, and managing running work. Running work on it is
prohibited.

| Use | Tools |
|---|---|
| Launching containers | `launch.sh` and its wrappers |
| Moving files in and out | `scp`, `sftp`, `rsync`, `git` |
| Managing running work | `kubectl get pods`, `kubectl delete pod`, and `kubesh` to enter a running container |
| Small housekeeping | Listing directories, checking disk usage, editing a config file, reading a log |

See also: [Prohibited Uses of the Login Node](#prohibited-uses-of-the-login-node)

## Prohibited Uses of the Login Node

Manual job execution on `dsmlp-login` is prohibited by policy. Prohibited work
includes Python scripts, Java projects, notebooks, training runs, and data
conversions.

Running an editor's server component on `dsmlp-login` is not permitted. Running
VS Code directly on the login node is specifically prohibited. The supported
configuration places VS Code in a container, as described in
[Remote Editor Setup](remote-editor-setup.md).

## The Login Node & the Cluster Nodes

Each container is assigned CPU, RAM, and GPU of its own and is isolated from
other users' processes. The login node is shared: the resources one session
uses there are taken from every other user signed in.

Every user passes through the login node. A loaded login node degrades
launching for everyone signed in, not only for one job.

Many CPU cores, tens of gigabytes of memory, and a GPU are available on the
cluster nodes through a launch script.

## Running Work in a Container

After connecting, launch a container and run work in it:

```bash
launch-scipy-ml.sh -W <WORKSPACE>     # GPU-capable image
launch.sh -h                          # print the flag summary
```

Short jobs also run in a container. Starting a container takes seconds.

See also: [Working from the Command Line](../working-from-the-command-line.md)

### Launch Modes

A launch runs in one of three modes, depending on whether the session is
attended:

```bash
launch-scipy-ml.sh -W <WORKSPACE>                    # interactive: a shell in a container
launch-scipy-ml.sh -W <WORKSPACE> -b                 # background: keeps running after a disconnect
launch-scipy-ml.sh -W <WORKSPACE> -B -- python train.py   # batch: runs to completion, then exits
```

See also: [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes)

### Shared Filesystem

The login node and the container share a filesystem. A file copied to the
login node with `scp` is in the container, and a file a job writes is on the
login node once the job is over. No copying step is needed between them.

See also: [Where Files Live](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

## Connecting Without a Password

An SSH key pair removes the password prompt from repeated connections. Generate
a pair on the local machine and install the public key on the login node:

```bash
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub | ssh <username>@dsmlp-login.ucsd.edu \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Naming the key type with `-t` fixes the file name, which the second command
must match. The type a bare `ssh-keygen` picks has changed between OpenSSH
releases.

To verify the key, connect again. A connection that does not ask for the AD
password is using the key. The key's own passphrase is still requested if one
was set.

### Key Pair for a Remote Editor

A remote editor requires a key pair. VS Code connects through a ProxyCommand
that cannot prompt for a password, and the editor's connection terminates
inside the container rather than on the login node. `launch.sh -H` carries the
key installed on the login node into the container at launch. The Windows
commands, the local file permissions, the SSH agent, and the `IdentityFile`
directive are documented in [The Key Pair](remote-editor-setup.md#the-key-pair).

## Running a Launch Script over SSH

A launch script can be invoked directly over SSH. A job is submitted this way
from a script on a local machine rather than by hand:

```bash
ssh <username>@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh <flags>
```

See also: [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

## A Second Shell with `kubesh`

`kubesh`, run on the login node, opens a second shell in a running container
without starting a second container:

```bash
kubectl get pods          # find the pod
kubesh <pod-id>           # enter it
```

This is the supported way to watch a job that is already running. A second
launch starts a second container with its own resources rather than attaching
to the first.

See also: [Watching a Running Job](../running-jobs/watching-your-job.md)

## Reaching a Notebook or a Service

A Jupyter server or any other service listening inside a container is not
directly reachable from a personal machine. Two SSH tunnel forms reach it, and
they target different ports. The two forms are not interchangeable. Using the
wrong form is the usual reason a tunnel does not work.

| To reach | Use |
|---|---|
| A port the launcher published on the login node, such as the port in the Jupyter URL | [Tunnel to a Port on the Login Node](#tunnel-to-a-port-on-the-login-node) |
| A port a service is listening on inside the container, such as TensorBoard or a web app started there | [Tunnel to a Port Inside the Container](#tunnel-to-a-port-inside-the-container) |

### Tunnel to a Port on the Login Node

The output of a launch ends with a URL naming a port on
`dsmlp-login.ucsd.edu`. Forward that port from a second terminal on the local
machine:

```bash
ssh -N -L 8889:dsmlp-login.ucsd.edu:<port> <user>@dsmlp-login.ucsd.edu
```

`http://localhost:8889/user/<username>/tree/` then opens the session, and the
token from the launch output authenticates it. Replacing `tree` with `lab` in
that URL opens JupyterLab, which adds a terminal and an editor.

### Tunnel to a Port Inside the Container

For a service started by hand inside the container, the tunnel targets the
loopback address:

```bash
ssh -N -L localhost:<port>:127.0.0.1:<port> <user>@dsmlp-login.ucsd.edu
```

`localhost:<port>` in a browser then reaches the service.

### Tunnel Terminal Output

`-N` means "no command", so a working tunnel prints nothing. A silent terminal
indicates success, not a hang. Keep the terminal open for as long as the tunnel
is needed. `Ctrl+C` closes the tunnel.

### Closing the Tunnel and the Container

Closing a tunnel does not stop the container. Stopping the container does not
close the tunnel. At the end of a session, quit Jupyter or `exit` the
container, then press `Ctrl+C` in the tunnel's terminal.

> [!WARNING]
> A container that has only been disconnected from may still be running and
> still holding a GPU.

See also: [Job Modes](../running-jobs/job-modes-and-limits.md#job-modes)

### The VPN Alternative

With a connection to the campus VPN, the launch URL works as printed and no
tunnel is required. Either route works. The VPN involves fewer steps to
remember. A tunnel involves less to install and does not route the rest of the
machine's traffic through campus.

The VPN or a tunnel is needed only for container ports, such as a Jupyter
server started by `launch.sh`. Neither is needed for `ssh` to the login node or
for Datahub in a browser.

See also: [Datahub in the Browser](datahub-in-the-browser.md)

## Reaching a Port From the Login Node

Two mechanisms make a port inside a container available on the login node.

### Forwarding with `kubectl port-forward`

`kubectl port-forward` connects the login node to a port inside a pod. It
covers the case where the container publishes nothing itself, such as a custom
image with an overridden entrypoint:

```bash
kubectl port-forward pods/<pod-name> <port>:8888
```

Combined with a
[Tunnel to a Port on the Login Node](#tunnel-to-a-port-on-the-login-node), the
port is reachable from a local machine.

See also: [Building & Publishing a Custom Image](../environments/building-a-custom-image.md)

### Publishing a Port with `IDENTITY_PROXY_PORTS`

Setting `IDENTITY_PROXY_PORTS=1` before launching asks for a container port to
be published on the login node. The launch output then names the port that was
mapped. This is the documented route for TensorBoard and similar dashboards:

```bash
IDENTITY_PROXY_PORTS=1 launch-scipy-ml.sh -g 1
```

This behavior is documented but not confirmed against the current launcher.
Report discrepancies to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

See also: [TensorBoard & Other Dashboards](../running-jobs/watching-your-job.md#tensorboard--other-dashboards)

## Connection Failures

| Symptom | Usual cause |
|---|---|
| Password refused | An incorrect username format. Use `username`, not `username@ucsd.edu`, with the AD password. |
| The connection hangs after the password | Duo approval is still pending on the phone. |
| `Connection timed out` from off campus | A network that blocks outbound SSH, such as a hotel, a conference, or some corporate networks. The VPN is not required for `ssh`, but connecting to it routes around a block of this kind. |
| A host key warning | Do not accept it without checking. Where no change was announced, contact [datahub@ucsd.edu](mailto:datahub@ucsd.edu) before removing the stored key. |
| It connects, but nothing launched will start | The cause is not the connection. See [Sign-In & Session Problems](sign-in-and-session-problems.md). |
| `channel N: open failed: connect failed: Connection refused` on a forwarded port | A wrong remote port number, or a local port already in use. See [Refused Tunnel Connections](#refused-tunnel-connections). |

### Refused Tunnel Connections

A tunnel that refuses the connection, or a browser that does not load the
forwarded page, usually has one of two causes:

- The local port is already in use, often by a tunnel left open in another
  window. `lsof -i :8889` names the process. Stop that process or choose a
  different local port.
- The remote port is wrong. The port in a Jupyter URL is assigned at launch
  and is unlikely to be the same twice. The current launch output carries the
  current port. A command from an earlier session does not.

### Numeric Address Workaround

If the hostname form fails but the login node is reachable, some course guides
substitute the login node's numeric address on both sides of the command.
`nslookup dsmlp-login.ucsd.edu` returns it. This is a workaround for a routing
problem, not the normal connection path. Report cases that require it to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).
