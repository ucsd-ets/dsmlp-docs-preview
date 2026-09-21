# Watching a Running Job

Long runs fail quietly. A training job that never reached the GPU, a process
killed for memory hours ago, a session idle since lunch — none of these announce
themselves. This page covers the three things worth watching, **CPU, memory and
the GPU**, from the browser, from a shell, and from a dashboard on a local
machine. *It is also where the rest of our documentation sends readers for
`nvidia-smi` and for TensorBoard.*

## From the Browser

------------------------------------------------------------------------

**The standard images report their own resource use inside Jupyter.** CPU, memory
and GPU utilization for the running container are displayed in the notebook
interface itself, which is the least effort available and enough for most
coursework. *It sits along the top of the interface rather than at one exact
spot.*
→ [Standard Images](../environments/standard-images.md)

**It does not report whether the code is running on the GPU.** A container with
a card attached shows a card attached whether or not anything is using it — for
that, `nvidia-smi`.

## From a Shell Inside the Container

------------------------------------------------------------------------

Open a terminal in the Jupyter interface, or enter a running pod from the login
node with `kubesh <pod-id>`. Then:

```bash
htop        # CPU and memory, live
nvidia-smi  # the GPU: model, memory in use, and the processes using it
```

**`htop` reports the container, not the cluster.** The figures are the pod's own,
and the numbers to compare them against are the ones requested at launch.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**Please do not run either on `dsmlp-login`.** The login node is a jumpbox for
launching jobs and moving files; `htop` there reports a machine no computing is
happening on, and monitoring loops left running on it affect everyone.
→ [The Login Node](../access/the-login-node.md)

## Is the GPU Actually Doing Anything?

------------------------------------------------------------------------

This is the question `nvidia-smi` exists to answer.

```bash
python -c "import torch; print(torch.cuda.get_device_name(0));"
nvidia-smi
```

**The `python` line settles "no device found".** That message is much more often
an environment problem than a scheduling one — the `rstudio-notebook` image, for
instance, derives from the CPU image and cannot see a card at all.
→ [Standard Images](../environments/standard-images.md) ·
[GPU Classes](../gpu-access/gpu-classes.md)

**`nvidia-smi` reports the model, its memory, and what is using it.** Run again
part-way through a job, memory in use that has not moved and no process listed
against the card mean the job is quietly training on the CPU.

**An idle card is also a card the service takes back.** GPU sessions are reclaimed
after roughly 30 minutes of the card doing nothing. *The test is whether the GPU is
busy, not whether a session is attached* — so a job that never reached the GPU is
on a timer it does not know about.
→ [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

## Memory, & Why Jobs Are Killed

------------------------------------------------------------------------

**`OOMKilled` means the container reached its memory limit**, not that the code
threw an error. It appears in the status column of `kubectl get pods`, and it is
the single most common way a long job ends without a traceback.
→ [Error Messages](../reference/error-messages.md)

**Memory is requested at launch, with `-m`.** Note that `launch.sh` sets the
memory *request* to half the limit named — `-m 32` reserves 16 GB and permits
32 GB — so the upper half of that allowance is available only if the node has
it spare. *An identical job can therefore succeed on Tuesday and be killed on
Thursday.* → [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**Memory use changes over the course of a run.** `htop` at minute two says very
little about a data loader that grows for four hours.

## TensorBoard & Other Dashboards

------------------------------------------------------------------------

**The pattern is always the same:** run the server *inside* the container, then
reach it from a local machine over an SSH tunnel. TensorBoard is the usual case,
and anything else that serves a web page works the same way.

**1. Start the server in the container**, from a JupyterLab terminal or a `kubesh`
shell:

```bash
tensorboard --logdir <log directory> --bind_all --port <port>
```

**2. Tunnel to it from the local machine**, in a second terminal:

```bash
ssh -N -L localhost:<port>:127.0.0.1:<port> <user>@dsmlp-login.ucsd.edu
```

**3. Open `localhost:<port>` in a browser.** *A working tunnel prints nothing* —
a silent terminal is success, not a hang. It stays open for as long as the
dashboard is wanted, and `Ctrl+C` closes it.
→ [Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service)

**A documented alternative publishes the port on the login node instead.** Setting
`IDENTITY_PROXY_PORTS=1` before launching asks for a container port to be mapped:

```bash
IDENTITY_PROXY_PORTS=1 launch-scipy-ml.sh -g 1
```

The launch output then carries a line reading `Identity port map 1: Container port
12345 mapped to dsmlp-login.ucsd.edu:12345`. TensorBoard started on that port is
reached at `dsmlp-login.ucsd.edu` on the same port — from the campus VPN, or
through a tunnel to the login node. *We have not confirmed this against the current
launcher;* please tell us if it no longer behaves as described.

**Some courses distribute a wrapper script** that starts TensorBoard on a course
log directory. Those scripts are course-specific and their paths change every
term; what they do is the three steps above.

## Checking On a Detached Job

------------------------------------------------------------------------

**Exiting a pod does not stop what is running inside it**, which is the point of a
background pod: the work continues after the session that started it has gone.
→ [Interactive, Background & Batch Modes](job-modes-and-limits.md#the-three-modes)

| To find out | Run |
|---|---|
| Which pods exist, and their status | `kubectl get pods` |
| What a batch job printed | `kubectl logs <pod-id>` |
| What is happening inside a background pod | `kubesh <pod-id>`, then `htop` or `nvidia-smi` |
| Which started processes are still going | `ps` inside the pod |

**An unattended run needs its logs in a file.** The crude form is
`python run.py all > log.txt &`; the better one is Python's `logging` module, which
timestamps each line and names the file and function it came from. *Over a run of
several hours, the difference between the two is whether the failure can be placed
in time.*
→ [Kubernetes](kubernetes.md)

**Please checkpoint anything long.** Idle culling, runtime limits and reservation
windows all end sessions for reasons unrelated to the code running in them.
→ [Checkpointing](../running-jobs/checkpointing.md)

## What Is Running Right Now

------------------------------------------------------------------------

**A forgotten session is a session that is still spending.** From a terminal,
`kubectl get pods` lists the pods an account holds; `kubectl delete pod <pod-id>`
stops one. From the browser, **File → Hub Control Panel → Stop My Server**.

*Logging out does not stop a session, closing a laptop does not stop a session,
and closing VS Code does not release a pod.* An idle GPU session is eventually
reclaimed, but the hours before that are charged.
→ [What Ends a Session](../gpu-access/what-ends-a-session.md) ·
[On-Demand Leases Charge Budget](../gpu-access/service-units-and-budgets.md#on-demand-leases-charge-budget)

**Concurrent sessions are allowed**, so `kubectl get pods` may legitimately list
several. What binds is the total across them.
→ [Running Several Jobs at Once](job-modes-and-limits.md#running-several-jobs-at-once)

## Caveats & Limitations

------------------------------------------------------------------------

**Watching a job does not keep it alive.** Attaching to a pod, tailing a log or
leaving `nvidia-smi` running does not exempt a session from idle culling — the test
is GPU activity. → [Idle Culling](../gpu-access/what-ends-a-session.md#what-counts-as-idle)

**A dashboard is not a session.** Closing a tunnel does not stop the container, and
stopping the container does not close the tunnel. A finished session is stopped
with **File → Hub Control Panel → Stop My Server**, or
`kubectl delete pod <pod-id>`, and the tunnel closed *afterwards*. Logging out
stops nothing.

**A GPU session is spending Service Units while it runs**, whether or not it is
doing any work.
→ [Service Units & Budgets](../gpu-access/service-units-and-budgets.md) ·
[Reading Your Balance](../gpu-access/service-units-and-budgets.md#reading-your-balance)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
