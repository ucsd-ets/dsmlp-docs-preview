# Kubernetes: Direct Use & the Events a Session Emits

`launch.sh` is a front end to Kubernetes, and Kubernetes is available underneath
it. This page covers the cases the launcher does not — chiefly running more than
one pod at a time, and running something that is not a notebook — and the events a
session emits along the way.

**This is not the supported path for ordinary work.** Where `launch.sh` can do the
job, please use it: it sets up the home directory, the workspace, group membership
and resource limits correctly, and a hand-written manifest does none of that.

*This page assumes more Kubernetes than the rest of this documentation set.*
Readers who arrive from a search asking why a session ended will find
[Error Messages](../reference/error-messages.md) the friendlier page.

## The Namespace & `kubectl`

------------------------------------------------------------------------

**Each account has its own Kubernetes namespace**, and `kubectl` on the login node
operates inside it. It can see and change that namespace's pods and nothing else.

```bash
kubectl get pods                    # pods in the namespace
kubectl describe pod <pod-name>     # why one is Pending, or what killed it
kubectl logs <pod-name>             # its output
kubectl logs <pod-name> -f          # follow it
kubectl get events                  # what the cluster has been doing to them
kubectl delete pod <pod-name>       # stop one
kubesh <pod-name>                   # a shell inside one
```

**`kubectl describe pod` is the first thing to run when a launch misbehaves.** It
carries the scheduling messages — including the `0/5 nodes available` that usually
means a missing `gpu-class` label — that the launcher's own output summarizes away.

`kubectl exec -it <pod-name> bash` is the general form of `kubesh`, and the form
for a pod that `launch.sh` did not create.

## Running a Service From a Manifest

------------------------------------------------------------------------

**Some coursework needs a database rather than a notebook.** These are launched
from manifests on the login node and then reached *from* a notebook by service
name — the notebook and the service are separate pods in one namespace, and they
find each other over the cluster network.

The pattern is the same for each:

```bash
kubectl create -f launch/redis.yaml   # start it
kubectl get pods                      # wait for READY
kubectl delete -f launch/redis.yaml   # stop it when the work is done
```

Then, from a notebook spawned in the usual way, connect by service name:

| Service | Reached at |
|---|---|
| Redis | `my-redis`, port `6379` |
| PostgreSQL | `my-postgres` |
| Neo4j | `bolt://my-neo4j:7687` |
| MongoDB | `mongodb://my-mongo` |
| Cassandra | A 3-pod StatefulSet; **5-10 minutes** to reach `3/3` ready |

```python
import redis
r = redis.Redis(host='my-redis', port=6379, db=0)
```

A pod that exists is not a pod that is serving, so connections are made after
`READY` rather than a few seconds after `kubectl create`. Cassandra in particular
takes several minutes; `kubectl get statefulset` and `kubectl logs cassandra-0 -f`
report its progress.

**Please do not modify the launch templates without checking with us first.** The
manifests are maintained by us for the courses that use them, and a locally edited
copy is the usual reason a service that works for the rest of the class fails for
one member.

## Multi-Pod Topologies

------------------------------------------------------------------------

**A course may provide a cluster rather than a container.** Where that happens —
Spark is the standing example — the cluster is spawned by launching the course
environment from `datahub.ucsd.edu`, not by running a script, and the pieces are
found with `kubectl`:

```bash
kubectl get pods                              # find spark-master-XXX-XXX
kubectl exec -it <spark-master-XXX-XXX> bash  # get into the master
```

Work inside the master pod is ordinary work; a job is submitted to the cluster by
its in-cluster address, e.g. `spark://spark-master-svc:7077`.

**Logging out does not stop the cluster.** It keeps running, and keeps holding its
resources, until it is stopped — **File → Hub Control Panel → Stop My Server**.
*This is the single most common way a class exhausts its own capacity.*

## Reading Events

------------------------------------------------------------------------

Events are the cluster's account of what it did to a pod and why.

```bash
kubectl get events                        # everything recent in the namespace
kubectl describe pod <pod-name>           # the events attached to one pod
kubectl get events --field-selector involvedObject.name=<pod-name>
```

**`kubectl describe pod` is usually the right one.** It puts the events at the
bottom of the pod's own description, next to the resource requests and the node
assignment, which is the context that makes them interpretable.

*Events repay a prompt look.* Kubernetes retains them for a limited window, so a
session that ended overnight may have nothing left to show by morning. For
unattended work, a log file is the durable record, not the event stream.
→ [Checkpointing & Logging](checkpointing.md)

## Ordinary Pod Events

------------------------------------------------------------------------

Most of what appears has nothing to do with reservations.

| Reason | What it means |
|---|---|
| `Scheduled` | The scheduler picked a node. The pod is about to start |
| `FailedScheduling` | Nothing could take it. `0/5 nodes available` alongside a GPU request is usually a missing or misspelled `gpu-class` label |
| `Pulling`, `Pulled` | The image is being fetched. A large custom image can spend minutes here |
| `Started`, `Killing` | The container started; the container is being stopped |
| `OOMKilled` *(as a pod status)* | Memory limit reached — see the request/limit halving on the [`launch.sh` reference](launch-sh-reference.md#requests-are-half-of-limits) |
| `DeadlineExceeded` *(as a pod status)* | The runtime limit was reached → [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit) |

*The reason strings in the first six rows are Kubernetes' own, not ours* — they
mean here what they mean on any cluster.

## Reservation Events

------------------------------------------------------------------------

**Five reason strings come from the reservation system rather than from Kubernetes
itself.** They are how a GPU session accounts for what the scheduling and
reservation model did to it.

| Reason | The behaviour it relates to |
|---|---|
| `RuntimeGuaranteed` | The guaranteed portion of a session. There is no hard kill at the end of a window; there is an in-session countdown → [The Countdown](../gpu-access/what-ends-a-session.md#the-countdown) |
| `Preempted` | The capacity was taken for someone else's booking. A best-effort reservation accepts this from its first tick → [Preemption](../gpu-access/what-ends-a-session.md#preemption) |
| `OnDemandLeaseDenied` | An on-demand lease — the reservation that launching without booking creates — was not granted → [Launching Without a Booking](../gpu-access/reservations.md#launching-without-a-booking) |
| `OverstayRelinked` | Overstay: running on past a guaranteed window, which has a cost → [Overstay](../gpu-access/what-ends-a-session.md#overstay) |
| `ReservationReassigned` | The reservation behind the session is no longer the one it started with → [Reservations](../gpu-access/reservations.md) |

**The second column is context, not a definition.** Each entry points at the
behaviour we are confident the event concerns; the precise trigger for each is not
yet documented, and where the two disagree, the linked page is the one to trust.

## Reading an Event Alongside the Session

------------------------------------------------------------------------

Events are most useful in combination with the pod's status and the job's own logs.

- **A session that ended with no event and no error** was most likely idle-culled.
  A warning comes first, saved work survives, and it is not a crash.
  → [What Ends a Session](../gpu-access/what-ends-a-session.md)
- **A session that never started** is a scheduling problem, and
  `kubectl describe pod` will say so in the events at the bottom.
- **A session that ended mid-run, with a reservation event**, is a capacity
  outcome rather than a fault. It is also the case checkpointing exists for.
- **A session that ended mid-run with nothing anywhere** is worth reporting to us.
  Please include the pod name, the node from the launch output, and roughly when.

## Caveats & Limitations

------------------------------------------------------------------------

**Anything started by hand has to be stopped by hand.** Nothing created with
`kubectl create` is cleaned up on logout. `kubectl delete -f <manifest>` removes
what a manifest created; `kubectl get pods` at the end of a session shows what is
still there.

**Manifest pods draw on the same limits.** A namespace's totals cover everything
running at once, so a database pod and a notebook pod share one allowance — which
is usually why the second one will not schedule.
→ [Running Several Jobs at Once](job-modes-and-limits.md#running-several-jobs-at-once)

**Containers are unprivileged here too.** A manifest that expects to run as root,
or to mount a host path, will not work.
→ [The Hard Boundary](../environments/customizing-your-environment.md#the-hard-boundary)

**We support the platform, not arbitrary Kubernetes.** Please tell us what a set of
hand-written manifests is meant to do before the work goes deep — there is often a
supported route, and where there is not, we would rather know early.
→ [The Six Requests](../reference/getting-help.md#the-six-requests)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
