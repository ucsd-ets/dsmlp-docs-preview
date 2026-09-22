# Watching a Running Job

This page covers monitoring the CPU, memory, and GPU use of a running job from
the browser, from a shell inside the container, and from a dashboard on a local
machine. It also covers checking on detached jobs and stopping sessions.

## Monitoring from the Browser

The standard images, listed in
[Standard Images, Tags, and Pinning](../environments/standard-images.md), display
CPU, memory, and GPU utilization for the running container in the Jupyter
interface. The display appears along the top of the interface rather than at one
fixed position.

The display does not show whether code is running on the GPU. A container with a
GPU attached shows the GPU as attached whether or not any process is using it.
The check for GPU use is described under
[Checking GPU Utilization](#checking-gpu-utilization).

## Monitoring from a Shell Inside the Container

Open a terminal in the Jupyter interface, or enter a running pod from the login
node with `kubesh <pod-id>`, and run:

```bash
htop        # CPU and memory, live
nvidia-smi  # the GPU: model, memory in use, and the processes using it
```

`htop` reports the pod's own figures, not the cluster's. Compare them against
the resources requested at launch, which are described in
[`launch.sh` Reference](../running-jobs/launch-sh-reference.md).

Do not run `htop` or `nvidia-smi` on `dsmlp-login`, and do not leave a
monitoring loop running there. The login node is for launching jobs and moving
files, as described in
[What the Login Node Is For](../access/the-login-node.md#what-the-login-node-is-for).
`htop` run on the login node reports the login node, not the container in which
the job runs.

## Checking GPU Utilization

Run these commands inside the container:

```bash
python -c "import torch; print(torch.cuda.get_device_name(0));"
nvidia-smi
```

The `python` command diagnoses a "no device found" message. That message is much
more often an environment problem than a scheduling one. For example, the
`rstudio-notebook` image derives from the CPU image and cannot see a GPU, as
listed under
[Standard Images](../environments/standard-images.md#standard-images).
Requesting a GPU is covered in [GPU Classes](../gpu-access/gpu-classes.md).

`nvidia-smi` reports the GPU model, its memory, and the processes using it. Run
it again partway through a job. If the memory in use has not changed and no
process is listed against the GPU, the job is training on the CPU.

### Idle Culling and Monitoring

A GPU session that stops using its GPU is reclaimed by idle culling. Attaching
to a pod, tailing a log, or leaving `nvidia-smi` running does not exempt a
session from idle culling. The criteria are listed under
[What Counts as Idle](../gpu-access/what-ends-a-session.md#what-counts-as-idle).

## Memory Limits and `OOMKilled`

The `OOMKilled` (out of memory) status means the container reached its memory
limit, not that the code threw an error. It appears in the status column of
`kubectl get pods`. It is the most common way a long job ends without a
traceback. The status and its usual cause are described in
[Error Messages](../reference/error-messages.md).

Memory is requested at launch with `-m`.
[Resource Requests and Limits](../running-jobs/launch-sh-reference.md#resource-requests-and-limits)
describes how that value sets the memory request and limit, and why an identical
job can succeed on one run and be killed on another.

Memory use changes over the course of a run. An `htop` reading taken in the
first minutes of a run says little about a data loader whose memory grows over
several hours.

## TensorBoard & Other Dashboards

A dashboard runs as a server inside the container and is reached from a local
machine over an SSH tunnel. TensorBoard is the usual case. Any other service
that serves a web page is reached the same way.

1. Start the server in the container, from a JupyterLab terminal or a `kubesh`
   shell:

    ```bash
    tensorboard --logdir <log directory> --bind_all --port <port>
    ```

2. Open a tunnel to it from a second terminal on the local machine:

    ```bash
    ssh -N -L localhost:<port>:127.0.0.1:<port> <user>@dsmlp-login.ucsd.edu
    ```

3. Open `localhost:<port>` in a browser.

A working tunnel prints nothing. A silent terminal indicates success, not a
hang. Keep the tunnel's terminal open for as long as the dashboard is needed.
`Ctrl+C` closes the tunnel. The tunnel forms are described in
[Reaching a Notebook or a Service](../access/the-login-node.md#reaching-a-notebook-or-a-service).

Some courses distribute a wrapper script that starts TensorBoard on a course log
directory. These scripts are course-specific, and their paths change every
term. Such a script performs the same three steps.

### Closing the Tunnel and the Container

Closing a tunnel does not stop the container. Stopping the container does not
close the tunnel. At the end of a session, stop the session with
**File → Hub Control Panel → Stop My Server** or `kubectl delete pod <pod-id>`,
then close the tunnel. Logging out does not stop the session, as described in
[Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

### Publishing a Port with `IDENTITY_PROXY_PORTS`

As an alternative to a tunnel into the container, setting
`IDENTITY_PROXY_PORTS=1` before launching requests that a container port be
mapped to the login node.

> [!NOTE]
> This option is documented but has not been verified against the current
> launcher. Report discrepancies to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).

```bash
IDENTITY_PROXY_PORTS=1 launch-scipy-ml.sh -g 1
```

The launch output then includes a line reading
`Identity port map 1: Container port 12345 mapped to dsmlp-login.ucsd.edu:12345`.
TensorBoard started on that port is reached at `dsmlp-login.ucsd.edu` on the
same port, from the campus VPN or through a tunnel to the login node. VPN
requirements are described under
[Connecting over SSH](../access/the-login-node.md#connecting-over-ssh).

## Checking On a Detached Job

Exiting a background pod does not stop the work running inside it. The work
continues after the session that started it has ended, as described in
[Job Modes](job-modes-and-limits.md#job-modes).

| To find out | Run |
|---|---|
| Which pods exist, and their status | `kubectl get pods` |
| What a batch job printed | `kubectl logs <pod-id>` |
| What is happening inside a background pod | `kubesh <pod-id>`, then `htop` or `nvidia-smi` |
| Which started processes are still running | `ps` inside the pod |

Checkpoint long runs. Idle culling, the runtime limit, and the end of a
reservation window each end sessions regardless of the code running in them.
Checkpointing is described in
[Checkpointing & Logging Long Runs](../running-jobs/checkpointing.md).

### Logging an Unattended Run

Write the output of an unattended run to a file. Redirecting output, as in
`python run.py all > log.txt &`, records it without timestamps. Python's
`logging` module timestamps each line and names the file and function it came
from, so a failure during a run of several hours can be placed in time.

See also: [Direct Kubernetes Use and Session Events](kubernetes.md)

## Listing and Stopping Sessions

These commands and controls list and stop the sessions an account holds:

| Task | Command or control |
|---|---|
| List the pods an account holds | `kubectl get pods`, from a terminal |
| Stop a pod | `kubectl delete pod <pod-id>`, from a terminal |
| Stop a browser session | **File → Hub Control Panel → Stop My Server** |

> [!WARNING]
> Logging out or closing a laptop does not stop a session, and closing VS Code
> does not release a pod.

Stopping a browser session is described in
[Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session).

A GPU session spends Service Units while it runs, whether or not it is doing any
work, as described in
[On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges).
A GPU session that stops using its GPU is eventually reclaimed by idle culling,
as described in [What Ends a Session](../gpu-access/what-ends-a-session.md), and
is charged until it is reclaimed. The balance is covered under
[Remaining Balance](../gpu-access/service-units-and-budgets.md#remaining-balance).

Several jobs may run at once, so `kubectl get pods` can list more than one pod.
Resource limits apply to the total across them, as described in
[Running Several Jobs at Once](job-modes-and-limits.md#running-several-jobs-at-once).
