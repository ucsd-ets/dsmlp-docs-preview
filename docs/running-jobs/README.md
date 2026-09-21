# Running Jobs

Launching containers, the modes a job can run in, watching one, and the
Kubernetes underneath.

------------------------------------------------------------------------

Documented once, and linked from wherever it is needed. *One fact, one anchor: a
flag table documented here is not restated on an audience page.*

**Every page in this directory is an initial draft.** Each opens with a note
naming what its writer could not settle. Please read those before treating any
page as final.

| Page | Covers |
|---|---|
| [`launch.sh` Reference](launch-sh-reference.md) | Every flag, the three resource tiers, and why requests are half of limits. |
| [Job Modes, Runtime Limits & Configuration](job-modes-and-limits.md) | Interactive, background and batch; the 6- and 12-hour limits; running several jobs at once; and configuring by environment variable. |
| [Watching a Running Job](watching-your-job.md) | CPU, memory and the GPU — from the browser, from a shell, and from TensorBoard. |
| [Checkpointing & Logging Long Runs](checkpointing.md) | Writing state an interruption cannot corrupt, and the termination warning. |
| [Kubernetes](kubernetes.md) | `kubectl` in your own namespace, services from a manifest, and the events a session emits. |

---

[← Documentation index](../README.md)
