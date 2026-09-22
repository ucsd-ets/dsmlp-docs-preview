# Remote Editor Setup

VS Code is supported through one configuration, Remote-SSH over a ProxyCommand,
which connects the editor to a container on a cluster node rather than to the
login node. Running VS Code directly on `dsmlp-login` is not permitted, as
described in [The Login Node](the-login-node.md).

## What a Remote Editor Adds

The browser session is the default route onto the platform and covers most
coursework. Signing in at [datahub.ucsd.edu](https://datahub.ucsd.edu) opens a
Jupyter session with nothing to install or configure. The routes are described
in [Access](README.md).

A remote editor keeps the editor on the local machine and runs its working
parts in the container. VS Code installs a server component into the container
on first connection. The editor's terminal, debugger, language tooling, and
extensions then operate on the container's files and hardware, while the
window, keybindings, and settings stay local.

A remote editor suits the following work:

| Work | Remote editor behavior |
|---|---|
| A project of many files | A codebase with modules, tests, and configuration is edited as a tree, with search, refactoring, and git integration across the whole of it, rather than one notebook at a time |
| A script rather than a notebook | A training run is started from the editor's terminal, watched from the same window, and stepped through under a debugger with a GPU attached |
| An existing setup | Extensions, keybindings, themes, and settings carry over unchanged |
| A session that outlives the window | The container keeps running when the editor closes. Reopening the editor reconnects to the same container, with the same files and any processes left running in it |

A remote editor is the route with the most setup: an SSH key, an extension, and
a config file, as listed in [Prerequisites](#prerequisites). Its container keeps
running with nothing on screen and is deleted by hand, as described in
[Ending the Session](#ending-the-session).

## Launch and Connection Sequence

A session has two steps, performed in order: launch the pod, then connect the
editor.

1. From the login node, a launch script starts a container with `-H`, which
   runs an SSH server inside it, and `-N`, which gives the pod a fixed name. The
   container's size, image, and any GPU are chosen at this step.
2. From VS Code, the `ProxyCommand` of a `Host` entry runs the same launcher on
   the login node with the same `-N` name. The launcher finds the pod already
   running under that name and attaches to it rather than starting a second
   one. The editor's SSH connection is carried through to the SSH server inside
   the container.

Without the `ProxyCommand` line, VS Code attempts to run on `dsmlp-login`, where
running VS Code is not permitted.

### Disconnection and Reconnection

A pod launched with `-H` is not ended by a disconnect. Closing the editor or
losing the network leaves the pod running, and the next connection attaches to
it again.

### Connecting Without a Running Pod

If no pod of that name is running when the editor connects, the
`ProxyCommand`'s own launch creates one at the launcher's default size and
without a GPU. A session that connects but is unexpectedly small, or has no GPU,
indicates that the launch step was skipped or that the pod had already expired.

## Prerequisites

1. An SSH key pair, with the public key installed so that neither the login node
   nor the container asks for a password. The `ProxyCommand` runs unattended and
   cannot answer a password prompt. Key generation is covered in
   [The Key Pair](#the-key-pair), and the SSH connection to the login node in
   [Connecting over SSH](the-login-node.md#connecting-over-ssh).
2. The [Remote-SSH extension](https://code.visualstudio.com/docs/remote/ssh) in
   VS Code, and an OpenSSH-compatible client on the local machine. VS Code does
   not support PuTTY.
3. The workspace ID. `workspace --list` on `dsmlp-login` prints the workspaces
   the account may enter. Independent study users, who are not members of a
   course, omit `-W` and land in the personal home directory.

## The Key Pair

The key pair is generated on the local machine. `ssh-keygen` writes two files: a
private key and a matching `.pub` public key. The private key is the equivalent
of a password and never leaves the local machine. The public key is installed
on the login node.

### Login Node and Container Authentication

The `ProxyCommand` authenticates to `dsmlp-login`. The editor's own connection
then authenticates to the SSH server that `-H` starts inside the container. One
key pair serves both connections, and one installation of the public key covers
both, because `launch.sh -H` carries it from the login node into the container.

### SSH Client on macOS and Windows

macOS ships an SSH client. On Windows, the OpenSSH client is a Windows optional
feature, and VS Code looks for `ssh` on the `PATH` before falling back to the
Git for Windows install path. Client installation is described in
[Installing a supported SSH client](https://code.visualstudio.com/docs/remote/troubleshooting#_installing-a-supported-ssh-client).

### Generating the Key Pair

Generate the pair in a local terminal: **Terminal** on macOS, **PowerShell** on
Windows. The command is the same on both:

```bash
ssh-keygen -t ed25519
```

`ssh-keygen` offers a default location, then asks for a passphrase. An empty
passphrase is accepted. The two files are written to the `.ssh` directory of
the local home directory:

| | Private key | Public key |
|---|---|---|
| macOS | `~/.ssh/id_ed25519` | `~/.ssh/id_ed25519.pub` |
| Windows | `C:\Users\<username>\.ssh\id_ed25519` | `C:\Users\<username>\.ssh\id_ed25519.pub` |

Naming the type with `-t` fixes the file name. The type a bare `ssh-keygen`
picks has changed between OpenSSH releases, and the file name follows the type.
Every command on this page uses the `id_ed25519` file names.

### Private Key File Permissions

SSH refuses a private key that other accounts can read, with
`WARNING: UNPROTECTED PRIVATE KEY FILE!`. On macOS, the fix is `chmod 700 ~/.ssh`
and `chmod 600` on the private key and on `~/.ssh/config`. On Windows, the
`.ssh` directory must be owned by the account, with no other user granted
access. The fix is described in
[Fixing SSH file permission errors](https://code.visualstudio.com/docs/remote/troubleshooting#_fixing-ssh-file-permission-errors).

### SSH Agent

An SSH agent holds the unlocked key, so a passphrase is entered once per login
rather than at every connection. VS Code adds the key to a running agent by
itself. On macOS, the agent runs by default, and
`ssh-add --apple-use-keychain ~/.ssh/id_ed25519` stores the passphrase in the
login keychain. On Windows, start the service from an Administrator PowerShell:

```powershell
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

`ssh-add -l`, run in a local VS Code terminal, lists what the agent holds.
Restart VS Code after starting the agent; otherwise VS Code does not find it.
Agent setup is described in
[Setting up the SSH Agent](https://code.visualstudio.com/docs/remote/troubleshooting#_setting-up-the-ssh-agent).

### Keys Generated in PuTTYGen

A key made in PuTTYGen does not work as generated. PuTTY is not a supported VS
Code client. Save a `.ppk` private key out through
**Conversions → Export OpenSSH key** before use, as described in
[Reusing a key generated in PuTTYGen](https://code.visualstudio.com/docs/remote/troubleshooting#_reusing-a-key-generated-in-puttygen).

### Microsoft and GitHub Guides

Microsoft and GitHub each publish a longer walkthrough of key setup:
[Key-Based Authentication in OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement)
and
[Generating a New SSH Key and Adding It to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
The "Deploy the public key" section of the Microsoft article describes a Windows
SSH server and does not apply to `dsmlp-login`, where the public key is
installed as described in [Installing the Public Key](#installing-the-public-key).

## Installing the Public Key

The public key is installed once, on the login node. `launch.sh -H` carries it
into the container, so nothing is pasted into a running pod.

From macOS:

```bash
cat ~/.ssh/id_ed25519.pub | ssh <username>@dsmlp-login.ucsd.edu \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

From Windows, in PowerShell:

```powershell
$USER_AT_HOST="<username>@dsmlp-login.ucsd.edu"
$PUBKEYPATH="$HOME\.ssh\id_ed25519.pub"
$pubKey=(Get-Content "$PUBKEYPATH" | Out-String); ssh "$USER_AT_HOST" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '${pubKey}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

The Active Directory (AD) password and Duo are requested once, for that
connection. Verify the key before continuing:

```bash
ssh -i ~/.ssh/id_ed25519 <username>@dsmlp-login.ucsd.edu
```

A connection that does not ask for the AD password is using the key. A
passphrase, if one was set, is still requested.

### Key Copy in the Container

Every launch replaces the container's copy of `authorized_keys` with a fresh
copy of the login node's. The login node's copy is the only one to edit. A key
added by hand inside a running container does not survive the next launch.

If the editor does not authenticate after the key has been installed, delete the
pod and launch it again so that the copy is remade, as described in
[Launching the Pod](#launching-the-pod).

A session launched without `-W` needs no further step. Its container home
directory is the personal one, the key is already in it, and the copy is
skipped.

## The Host Entry

In VS Code, open **Remote Explorer → SSH targets**, click the gear icon, and
edit the config file in the local home directory: `~/.ssh/config` on macOS,
`C:\Users\USERNAME\.ssh\config` on Windows. The Command Palette (`F1`) opens the
same file through **Remote-SSH: Open Configuration File...**. Add an entry of
this form:

```
Host MYCOURSE
  User USERNAME
  IdentityFile ~/.ssh/id_ed25519
  ProxyCommand ssh -i ~/.ssh/id_ed25519 USERNAME@dsmlp-login.ucsd.edu /opt/launch-sh/bin/launch.sh -W MYCOURSE -H -N vscode-dsmlp
```

| Part | What it does |
|---|---|
| `-i ~/.ssh/id_ed25519` | The client-side private key used to authenticate to both the login node and the container |
| `/opt/launch-sh/bin/launch.sh` | The same launcher run by hand, called by absolute path |
| `-W MYCOURSE` | The course workspace, so the course files are there |
| `-H` | Connects to the SSH server inside the container — this is what VS Code attaches to |
| `-N vscode-dsmlp` | The pod's name. It must match the name used at launch |

The entry is written once. Size, image, and GPU are not set in it. They are set
at each launch, and the entry attaches to whatever pod carries the name, as
described in [Launching the Pod](#launching-the-pod).

### Key Paths in the Entry

The entry names the key twice, once for each connection. `IdentityFile` governs
the connection from VS Code to the container. The `ProxyCommand` is a separate
`ssh` invocation that connects the local machine to the login node. The same
key file serves both, as described in [The Key Pair](#the-key-pair).

On Windows, write the path with forward slashes, as in
`IdentityFile C:/Users/USERNAME/.ssh/id_ed25519`, or double every backslash.

## Launching the Pod

Each session begins on the login node:

```bash
ssh <username>@dsmlp-login.ucsd.edu
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b
```

| Flag | What it does |
|---|---|
| `-W MYCOURSE` | The same workspace as the `Host` entry |
| `-H` | Starts an SSH server inside the container |
| `-N vscode-dsmlp` | Names the pod. The `Host` entry finds it by this name |
| `-b` | Returns the prompt once the pod is scheduled; the pod keeps running |

The launcher reports the pod's progress and the node it lands on, then returns.

### Resource Flags

Resources are set on the launch line. `-c` and `-m` set CPU cores and gigabytes
of memory. `-g 1`, with a GPU class the workspace has been granted, adds a GPU:

```bash
# more CPU and memory
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b -c 4 -m 8

# a GPU
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b -g 1 -l gpu-class=medium
```

A connection that drops within a minute of starting a memory-intensive process
indicates a container that is too small. Delete the pod and launch again with a
larger `-m`.

> [!WARNING]
> Starting a GPU session draws on the GPU Service Unit budget, and an editor
> container spends for as long as it exists, whether or not the editor is in
> use. See [On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges).

The launch flags are documented in
[`launch.sh` Reference](../running-jobs/launch-sh-reference.md), and the GPU
classes in [GPU Classes](../gpu-access/gpu-classes.md).

## Connecting

With the pod running, right-click the SSH target in **Remote Explorer** and
connect. Clicking **details** in the lower right shows the connection progress.

Reconnecting after the editor has been closed or the laptop has slept is the
same action. The pod is still running, and the `ProxyCommand` attaches to it.

## Pod Lifetime

An editor pod has the same runtime limit as any other container, 6 hours by
default and up to 12 hours when set at launch, as described in
[The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit).
When the limit is reached, the pod stops, the editor loses its connection, and
any processes running in the container end with it. A 12-hour limit is set by
exporting `K8S_TIMEOUT_SECONDS` before the launch:

```bash
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b
```

### Reconnecting After Expiry

The next connection after the pod expires does not restore it. With nothing
running under the name, the `ProxyCommand` starts a default-sized pod of its
own. Delete that pod, as described in [Ending the Session](#ending-the-session),
and launch again by hand before continuing. A launch that finds the default pod
running attaches to it rather than replacing it.

### Idle Culling of GPU Editor Pods

A GPU editor pod is subject to idle culling. Editing code does not use the GPU.
A GPU container that stops using its GPU is reclaimed after a warning, as
described in
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).

## Host Entries for Multiple Courses

Create a separate `Host` entry for each course. Reusing one entry across
workspaces makes the host keys collide, and the failure presents as a security
warning rather than as a configuration error.

### Pod Name Scope

The pod name is scoped to the account, not to the course. Two entries that both
specify `-N vscode-dsmlp` attach to whichever pod is running under that name,
whatever workspace it was launched in. Give each course a distinct pod name made
of lowercase letters, digits, and hyphens, and use the same name in the entry
and on the launch line.

## Ending the Session

> [!WARNING]
> Closing the editor does not release the pod. The pod keeps running and holds
> its CPU and memory, and its GPU where it has one, spending budget for as long
> as it exists.

End every session by deleting the pod from the login node:

```bash
ssh <username>@dsmlp-login.ucsd.edu
kubectl get pods
kubectl delete pod vscode-dsmlp
```

Idle culling does not replace this step. It applies only to GPU pods, and an
editor container with a stalled process holding the GPU may never qualify. A
CPU-only editor pod is never culled. It runs until its runtime limit is reached
or until it is deleted. The idle conditions are described in
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).

The running container can also be entered from the login node with
`kubesh vscode-dsmlp`, without opening the editor.

### Growth of `.vscode-server`

VS Code installs a server component into the home directory the first time it
connects, and `.vscode-server` grows past a gigabyte. On a course home
directory, that is a large fraction of the quota. When the quota fills, the
symptom is a session that does not start, not a VS Code error. Home directory
quotas are described in
[Workspace and Personal Quotas](../workspaces-and-storage/your-files-and-quotas.md#workspace-and-personal-quotas).

## Editor Connection Failures

| Symptom | Usual cause |
|---|---|
| A password prompt that VS Code cannot answer | The public key is not installed on the login node, or `-i` names a key that host does not hold |
| `Permission denied (publickey)` once the pod has launched | `IdentityFile` names the wrong key, or the pod's copy of `authorized_keys` is older than the key. Delete the pod and launch again |
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` | Local file permissions on the private key |
| A passphrase requested at every reconnection | No agent is running locally, or VS Code was not restarted after it was started |
| A host key mismatch or security warning | Two courses sharing one `Host` entry |
| It connects, but the session is small or has no GPU | No pod was running under the name, so the ProxyCommand started a default one. Delete it and launch by hand |
| It connects, but to another course's files | Two `Host` entries sharing one pod name |
| It connects, but the course files are not there | A missing or misspelled `-W` on the launch line, so the session is in the personal home |
| The connection drops within a minute | The container is too small — delete it and launch again with more `-m` |
| The connection ends after hours of use | The runtime limit, or idle culling on a GPU pod. Launch again |
| Nothing starts, and several sessions are already running | The aggregate CPU, memory and GPU ceiling → [Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once) |

Where none of these apply, send the connection log from the **details** pane,
the `Host` entry, and the launch line to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).
