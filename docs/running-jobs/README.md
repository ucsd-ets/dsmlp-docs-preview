# Running Jobs

Use `launch.sh` on the login node for work the browser does not cover: more CPU
or memory than the course menu offers, a GPU class the menu does not include,
or a job that keeps running after you disconnect. Start here to launch a
container, watch it while it runs, and make a long run resumable after an
interruption.

| Page | Covers |
|---|---|
| [`launch.sh` Reference](launch-sh-reference.md) | Invocation and wrapper scripts, default resources and resource tiers, resource requests and limits, and the resource, GPU, image, workspace, placement, and job execution flags. |
| [Job Modes, Runtime Limits & Configuration](job-modes-and-limits.md) | Interactive, background, and batch job modes; running several jobs at once; the runtime limit and raising it; and configuring a launch with environment variables. |
| [Watching a Running Job](watching-your-job.md) | Monitoring CPU, memory, and GPU use from the browser, from a shell inside the container, and from TensorBoard or another dashboard; memory limits and `OOMKilled`; checking on a detached job; and listing and stopping sessions. |
| [Checkpointing & Logging Long Runs](checkpointing.md) | Causes of an interrupted run, resumable and atomic checkpoints, checkpoint frequency, the termination warning, resuming, and logging for unattended jobs. |
| [Direct Kubernetes Use and Session Events](kubernetes.md) | Scope of support, the namespace and `kubectl`, running a service from a manifest, multi-pod topologies, and the pod and reservation events a session emits. |

---

[← Documentation index](../README.md)
