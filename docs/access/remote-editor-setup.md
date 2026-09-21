# Remote Editor Setup

VS Code is supported, and heavily used. **The supported configuration is
Remote-SSH over a ProxyCommand**, which connects the editor to a container on a
cluster node rather than to the login node.

*There is one supported path in.* Running VS Code directly on `dsmlp-login` is
not permitted; it consumes significant CPU and memory.
→ [The Login Node](the-login-node.md)

## What a Remote Editor Adds

------------------------------------------------------------------------

**The browser session is the default way in, and it covers most coursework.**
Signing in at [datahub.ucsd.edu](https://datahub.ucsd.edu) produces a Jupyter
session with nothing to install and nothing to configure.
→ [Access](README.md)

**A remote editor keeps the editor on the laptop and runs its working parts in
the container.** VS Code installs a small server component into the container
on first connection. The editor's terminal, debugger, language tooling and
extensions then operate on the container's files and hardware, while the window,
keybindings and settings stay local. The result is an ordinary desktop editing
session against cluster resources.

Where that pays off:

- **A project of many files.** A codebase with modules, tests and configuration
  is edited as a tree, with search, refactoring and git integration across the
  whole of it, rather than one notebook at a time.
- **A script rather than a notebook.** A training run started from the editor's
  terminal, watched from the same window, and stepped through under a debugger
  with a GPU attached.
- **An existing setup.** Extensions, keybindings, themes and settings carry over
  unchanged.
- **A session that outlives the window.** The container keeps running when the
  editor closes; reopening the editor reconnects to the same container, with the
  same files and any processes left running in it.

*It is also the route with the most setup* — an SSH key, an extension and a
config file — and the one where an idle container is easiest to forget, because
nothing on screen is holding it. Both are covered below.

## How It Works

------------------------------------------------------------------------

**Two steps, in order: launch the pod, then connect the editor.**

1. **From the login node**, a launch script starts a container with `-H`, which
   runs an SSH server inside it, and `-N`, which gives the pod a fixed name. The
   container's size, its image and any GPU are chosen here.
2. **From VS Code**, a `Host` entry whose `ProxyCommand` runs the same launcher
   on the login node with the same `-N` name. The launcher finds the pod already
   running under that name and attaches to it rather than starting a second one,
   and the editor's SSH connection is carried through to the SSH server inside.

**The pod outlives the connection.** Closing the editor, or losing the network,
leaves the pod running, and the next connection attaches to it again. A pod
launched with `-H` is not ended by a disconnect.

**The order matters.** If no pod of that name is running when the editor
connects, the `ProxyCommand`'s own launch creates one — at the launcher's default
size, and without a GPU. A session that connects but is unexpectedly small, or
has no GPU in it, is the sign that the launch step was skipped or the pod had
already expired.

**Without the ProxyCommand line, VS Code will try to run on `dsmlp-login`.**

## Prerequisites

------------------------------------------------------------------------

**1. An SSH key pair**, with the public half installed so that neither the login
node nor the container asks for a password. The ProxyCommand runs unattended and
cannot stop to answer one. → *The Key Pair*, below ·
[Connecting over SSH](the-login-node.md#connecting-over-ssh)

**2. The [Remote-SSH extension](https://code.visualstudio.com/docs/remote/ssh)**
in VS Code, and an OpenSSH-compatible client on the local machine. *VS Code does
not support PuTTY.*

**3. The workspace ID.** `workspace --list` on `dsmlp-login` prints the
workspaces the account may enter. *Independent study users, rather than members
of a course, omit `-W` entirely and land in the personal home directory.*

## The Key Pair

------------------------------------------------------------------------

**The pair is generated on the local machine, and the private half never leaves
it.** `ssh-keygen` writes two files — a private key, which stays on the laptop,
and a matching `.pub` public key, which is installed on the far end. *A private
key is the equivalent of a password.*

**Two hops are authenticated, not one.** The `ProxyCommand` authenticates to
`dsmlp-login`; the editor's own connection then authenticates to the SSH server
that `-H` starts inside the container. One pair serves both, and one
installation of the public half covers both — `launch.sh -H` carries it from the
login node into the container.

macOS ships an SSH client. On Windows the OpenSSH client is a Windows optional
feature, and VS Code looks for `ssh` on the `PATH` before falling back to the Git
for Windows install path.
→ [Installing a supported SSH client](https://code.visualstudio.com/docs/remote/troubleshooting#_installing-a-supported-ssh-client)

Generate the pair in a local terminal — **Terminal** on macOS, **PowerShell** on
Windows. The command is the same on both:

```bash
ssh-keygen -t ed25519
```

`ssh-keygen` offers a default location, then asks for a passphrase; an empty
passphrase is accepted. The two files land in the `.ssh` directory of the local
home directory:

| | Private key | Public key |
|---|---|---|
| macOS | `~/.ssh/id_ed25519` | `~/.ssh/id_ed25519.pub` |
| Windows | `C:\Users\<username>\.ssh\id_ed25519` | `C:\Users\<username>\.ssh\id_ed25519.pub` |

*Naming the type with `-t` fixes the file name.* The type a bare `ssh-keygen`
picks has changed between OpenSSH releases and the file name follows the type, so
the names above are the ones the rest of this page refers to.

**SSH refuses a private key other accounts can read**, with
`WARNING: UNPROTECTED PRIVATE KEY FILE!`. On macOS that means `chmod 700 ~/.ssh`
and `chmod 600` on the private key and on `~/.ssh/config`; on Windows, the `.ssh`
directory must be owned by the account with no other user granted access.
→ [Fixing SSH file permission errors](https://code.visualstudio.com/docs/remote/troubleshooting#_fixing-ssh-file-permission-errors)

An SSH agent holds the unlocked key, so a passphrase is entered once per login
rather than at every connection, and VS Code adds the key to a running agent by
itself. On macOS the agent runs by default, and `ssh-add --apple-use-keychain
~/.ssh/id_ed25519` stores the passphrase in the login keychain. On Windows the
service is started from an Administrator PowerShell:

```powershell
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

`ssh-add -l`, run in a local VS Code terminal, lists what the agent holds. *VS
Code has to be restarted after the agent is started*, or it will not find it.
→ [Setting up the SSH Agent](https://code.visualstudio.com/docs/remote/troubleshooting#_setting-up-the-ssh-agent)

**A key made in PuTTYGen will not work as it stands.** PuTTY is not a supported
VS Code client, and a `.ppk` private key has to be saved out through
**Conversions → Export OpenSSH key** first.
→ [Reusing a key generated in PuTTYGen](https://code.visualstudio.com/docs/remote/troubleshooting#_reusing-a-key-generated-in-puttygen)

Microsoft and GitHub each publish a longer walkthrough of the same ground:
→ [Key-Based Authentication in OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement) ·
[Generating a New SSH Key and Adding It to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

*The Microsoft article's "Deploy the public key" section describes a Windows SSH
server and does not apply here.* `dsmlp-login` takes the step below instead.

## Installing the Public Key

------------------------------------------------------------------------

**The public key is installed once, on the login node.** `launch.sh -H` carries
it into the container from there, so nothing is pasted into a running pod.

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

The AD password and Duo are requested once, for that one connection. Check the
result before going any further:

```bash
ssh -i ~/.ssh/id_ed25519 <username>@dsmlp-login.ucsd.edu
```

*A connection that does not ask for the AD password is using the key.* A
passphrase, where one was set, is still requested.

**The container's copy is replaced at every launch**, with a fresh copy of the
login node's. The login node's is therefore the only one worth editing — a key
added by hand inside a running container does not survive the next launch.
*Where the editor will not authenticate after the key has been installed, delete
the pod and launch it again*, so that the copy is remade.
→ *Launching the Pod*, below

*A session launched without `-W` needs nothing further either.* The container's
home directory is the personal one, the key is already in it, and the copy is
skipped.

## The Host Entry

------------------------------------------------------------------------

In VS Code, open **Remote Explorer → SSH targets**, click the gear icon, and edit
the config file in the local home directory — `~/.ssh/config` on macOS,
`C:\Users\USERNAME\.ssh\config` on Windows. *The Command Palette (`F1`) reaches
the same file through **Remote-SSH: Open Configuration File...**.* Add an entry
of this shape:

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

**The key is named twice because two connections are made.** `IdentityFile`
governs the connection from VSCode to the container; the `ProxyCommand` is a separate (second)
`ssh` invocation connecting the VSCode desktop/laptop to the login node. The same file
serves both. → *The Key Pair*, above

*On Windows, write the path with forward slashes* —
`IdentityFile C:/Users/USERNAME/.ssh/id_ed25519` — or double every backslash.

**The entry is written once.** Size, image and GPU are not set here. They are
set at launch, each session, and the entry attaches to whatever pod carries the
name.

## Launching the Pod

------------------------------------------------------------------------

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

**Resources go on this line.** `-c` and `-m` set CPU cores and gigabytes of
memory; `-g 1` with a GPU class the workspace has been granted adds a GPU:

```bash
# more CPU and memory
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b -c 4 -m 8

# a GPU
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b -g 1 -l gpu-class=medium
```

*A connection that drops within a minute of starting something memory-hungry* is
the symptom of a container that is too small — delete it and launch again with
more `-m`.

**Starting a GPU session draws on the GPU Service Unit budget**, and an editor
container is no exception — it spends for as long as it exists, whether or not
anyone is typing. → [On-Demand Leases Charge Budget](../gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md) ·
[GPU Classes](../gpu-access/gpu-classes.md)

## Connecting

------------------------------------------------------------------------

With the pod running, right-click the SSH target in **Remote Explorer** and
connect. *Clicking "details" in the lower right shows the connection progress.*

Reconnecting later, after the editor has been closed or the laptop has slept, is
the same action. The pod is still there and the `ProxyCommand` attaches to it.

## How Long the Pod Lasts

------------------------------------------------------------------------

**An editor pod has the same runtime limit as any other container**: 6 hours by
default, up to 12 hours when `K8S_TIMEOUT_SECONDS` is exported before the
launch. When the deadline is reached the pod stops, the editor loses its
connection, and any processes running in the container end with it.

```bash
export K8S_TIMEOUT_SECONDS=$(( 3600 * 12 ))
launch-scipy-ml.sh -W MYCOURSE -H -N vscode-dsmlp -b
```

**The next connection after an expiry does not restore the pod.** With nothing
running under the name, the `ProxyCommand` starts a default-sized pod of its own.
Please delete that pod and launch again by hand before continuing; a launch that
finds the default pod running attaches to it rather than replacing it.
→ [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

**A GPU editor pod is also subject to idle culling.** Editing code does not use
the GPU. A GPU container that goes about 30 minutes without GPU activity is
reclaimed, a warning first, and nothing is culled in its first 45 minutes.
→ [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

## One Host Entry per Course

------------------------------------------------------------------------

**Please create a separate `Host` entry for each course.** Reusing one entry
across workspaces makes the host keys collide, and the resulting failure presents
as a security warning rather than as a configuration mistake.

**The pod name is per account, not per course.** Two entries that both say
`-N vscode-dsmlp` attach to whichever pod is running under that name, whatever
workspace it was launched in. A distinct name per course — lowercase letters,
digits and hyphens, the same in the entry and on the launch line — keeps them
apart.

## Ending the Session

------------------------------------------------------------------------

**Closing the editor does not release the pod.** It keeps running, holds its CPU
and memory, and holds its GPU where it has one, spending budget for as long as it
exists. That is what makes reconnecting work, and it is also why an editor pod is
the easiest kind to forget.

Please finish every session this way:

```bash
ssh <username>@dsmlp-login.ucsd.edu
kubectl get pods
kubectl delete pod vscode-dsmlp
```

*Idle culling is not a substitute for this.* It applies only to GPU pods, and an
editor container with a stalled process holding the GPU may never qualify. A
CPU-only editor pod is never culled; it runs until its deadline or until it is
deleted. → [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

The running container can also be entered from the login node with
`kubesh vscode-dsmlp`, without opening the editor.

**`.vscode-server` accumulates.** VS Code installs a server component into the
home directory the first time it connects, and **`.vscode-server` grows past a
gigabyte**. On a course home directory that is a serious fraction of the quota,
and the symptom when it fills is not a VS Code error — it is a session that will
not start. → [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

## When It Will Not Connect

------------------------------------------------------------------------

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

*Where none of these apply*, please send us the connection log from the "details"
pane together with the `Host` entry and the launch line — those together are
usually enough to diagnose it in one reply.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
