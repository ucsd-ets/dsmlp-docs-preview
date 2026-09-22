# Direct Kubernetes Use and Session Events

This page covers direct use of the Kubernetes cluster beneath `launch.sh` for
cases the launcher does not handle, chiefly running more than one pod at a time
and running something other than a notebook, and the events a session emits.
It assumes working knowledge of Kubernetes.

## Scope of Support

`launch.sh` is the supported path for ordinary work. It sets up the home
directory, the workspace, group membership, and resource limits correctly. A
hand-written manifest does none of this. Use `launch.sh` wherever it can do the
job.

ITS supports the platform, not arbitrary Kubernetes. Before substantial work on
a set of hand-written manifests begins, describe to ITS what the manifests are
meant to do. A supported route often exists. Requests to ITS are described in
[Administrative Requests](../reference/getting-help.md#administrative-requests).

## The Namespace & `kubectl`

Each account has its own Kubernetes namespace. `kubectl` on the login node
operates inside that namespace and can see and change its pods and nothing else.

```bash
kubectl get pods                    # list the pods in the namespace
kubectl describe pod <pod-name>     # show why a pod is Pending, or what stopped it
kubectl logs <pod-name>             # print a pod's output
kubectl logs <pod-name> -f          # follow a pod's output
kubectl get events                  # list what the cluster has done to the pods
kubectl delete pod <pod-name>       # stop a pod
kubesh <pod-name>                   # open a shell inside a pod
```

### Diagnosing a Launch

`kubectl describe pod` is the first command to run when a launch misbehaves.
Its output carries the scheduling messages that the launcher's own output
summarizes away. Among them, `0/5 nodes available` after a GPU request usually
indicates a missing `gpu-class` label, as described in
[Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label).

### Shell Access to a Pod

`kubectl exec -it <pod-name> bash` is the general form of `kubesh`. It is the
form to use for a pod that `launch.sh` did not create.

## Running a Service From a Manifest

Some coursework requires a database rather than a notebook. The database is
launched from a manifest on the login node and reached from a notebook by
service name. The notebook and the service are separate pods in one namespace
and reach each other over the cluster network.

The pattern is the same for each service. For Redis:

```bash
kubectl create -f launch/redis.yaml   # start it
kubectl get pods                      # wait for READY
kubectl delete -f launch/redis.yaml   # stop it when the work is done
```

### Service Addresses

From a notebook spawned in the usual way, connect to the service by name.

| Service | Reached at |
|---|---|
| Redis | `my-redis`, port `6379` |
| PostgreSQL | `my-postgres` |
| Neo4j | `bolt://my-neo4j:7687` |
| MongoDB | `mongodb://my-mongo` |
| Cassandra | A 3-pod StatefulSet that takes 5-10 minutes to reach `3/3` ready |

A Redis connection from Python:

```python
import redis
r = redis.Redis(host='my-redis', port=6379, db=0)
```

### Service Readiness

A pod can exist before it is serving. Connect after the pod reports `READY`,
not a few seconds after `kubectl create`. Cassandra takes several minutes to
become ready, and `kubectl get statefulset` and `kubectl logs cassandra-0 -f`
report its progress.

### Stopping a Service

> [!WARNING]
> Nothing created with `kubectl create` is cleaned up on logout. Anything
> started by hand must be stopped by hand.

`kubectl delete -f <manifest>` removes what a manifest created. Run
`kubectl get pods` at the end of a session to see what is still running.

### Resource Limits for Manifest Pods

Pods created from a manifest draw on the same limits as every other pod in the
namespace. The namespace's totals cover everything running at once, so a
database pod and a notebook pod share one allowance. A shared allowance is the
usual reason the second pod does not schedule. Limits on concurrent pods are
described in
[Running Several Jobs at Once](job-modes-and-limits.md#running-several-jobs-at-once).

### Privileges in Manifest Pods

Containers started from a manifest are unprivileged, like every other container
on the platform, so a manifest that expects to run as root or to mount a host
path does not work
([Root Access and System Packages](../environments/customizing-your-environment.md#root-access-and-system-packages)).

### Launch Templates

ITS maintains the launch templates for the courses that use them. Do not modify
them without first checking with ITS. A locally edited copy is the usual reason
a service that works for the rest of the class fails for one member.

## Multi-Pod Topologies

A course may provide a cluster rather than a container. Spark is the standard
example. The cluster is spawned by launching the course environment from
`datahub.ucsd.edu`, not by running a script, and its pods are found with
`kubectl`:

```bash
kubectl get pods                              # find spark-master-XXX-XXX
kubectl exec -it <spark-master-XXX-XXX> bash  # open a shell in the master pod
```

Work inside the master pod proceeds as in any other pod. A job is submitted to
the cluster at its in-cluster address, for example
`spark://spark-master-svc:7077`.

### Stopping a Multi-Pod Cluster

> [!WARNING]
> Logging out does not stop the cluster. It keeps running and holding its
> resources until it is stopped with **File → Hub Control Panel → Stop My Server**.

See also: [Stopping a Session](../access/datahub-in-the-browser.md#stopping-a-session)

## Reading Events

Events record what the cluster did to a pod and why.

```bash
kubectl get events                        # everything recent in the namespace
kubectl describe pod <pod-name>           # the events attached to one pod
kubectl get events --field-selector involvedObject.name=<pod-name>
```

`kubectl describe pod` is usually the most useful of the three. It lists the
events at the bottom of the pod's own description, next to the resource
requests and the node assignment.

### Event Retention

Kubernetes retains events for a limited window, so a session that ended
overnight may have no events left to show by morning. For unattended work, a
log file is the durable record, not the event stream. Logging is covered in
[Checkpointing & Logging Long Runs](checkpointing.md).

## Ordinary Pod Events

Most events are unrelated to reservations. The reason strings in this table
are standard Kubernetes vocabulary and mean the same here as on any Kubernetes
cluster.

| Reason | Meaning |
|---|---|
| `Scheduled` | The scheduler picked a node. The pod is about to start. |
| `FailedScheduling` | No node could take the pod. `0/5 nodes available` alongside a GPU request usually indicates a missing or misspelled `gpu-class` label ([Missing or Misspelled Class Label](../gpu-access/gpu-classes.md#missing-or-misspelled-class-label)). |
| `Pulling`, `Pulled` | The image is being fetched. A large custom image can spend minutes in this state. |
| `Started`, `Killing` | `Started`: the container started. `Killing`: the container is being stopped. |
| `OOMKilled` (pod status) | The memory limit was reached. Memory requests and limits are described in [Resource Requests and Limits](launch-sh-reference.md#resource-requests-and-limits). |
| `DeadlineExceeded` (pod status) | The runtime limit was reached. See [The Runtime Limit](job-modes-and-limits.md#the-runtime-limit). |

## Reservation Events

Five reason strings come from the reservation system rather than from
Kubernetes. They record what the scheduling and reservation model did to a GPU
session.

| Reason | Related behavior |
|---|---|
| `RuntimeGuaranteed` | The guaranteed portion of a session. There is no hard kill at the end of a window; there is an in-session countdown. See [The Countdown](../gpu-access/what-ends-a-session.md#the-countdown). |
| `Preempted` | The capacity was taken for another booking. A best-effort reservation accepts this from its first tick. See [Preemption](../gpu-access/what-ends-a-session.md#preemption). |
| `OnDemandLeaseDenied` | An on-demand lease, the reservation that launching without a booking creates, was not granted. See [Launching Without a Booking](../gpu-access/reservations.md#launching-without-a-booking) and [On-Demand Lease Charges](../gpu-access/service-units-and-budgets.md#on-demand-lease-charges). |
| `OverstayRelinked` | Overstay: a session running on past a guaranteed window. Overstay has a cost. See [Overstay](../gpu-access/what-ends-a-session.md#overstay). |
| `ReservationReassigned` | The reservation behind the session is no longer the one it started with. See [Reservations](../gpu-access/reservations.md). |

Each row names the behavior an event relates to and is not a definition of the
event. The precise trigger for each reservation event is not yet published.

## Reading an Event Alongside the Session

Events are read together with the pod's status and the job's own logs.

| Observation | Interpretation |
|---|---|
| The session ended with no event and no error | The session was most likely idle-culled. A warning comes first, saved work survives, and the ending is not a crash. See [What Ends a Session](../gpu-access/what-ends-a-session.md). |
| The session never started | The cause is a scheduling problem. The events at the bottom of the `kubectl describe pod` output show it. |
| The session ended mid-run with a reservation event | The ending is a capacity outcome rather than a fault. Checkpointing addresses this case; see [Checkpointing & Logging Long Runs](checkpointing.md). |
| The session ended mid-run with no event or error anywhere | Report it to ITS with the pod name, the node from the launch output, and the approximate time. See [Support Contacts](../reference/getting-help.md#support-contacts). |

[Error Messages](../reference/error-messages.md) covers
why a session ended without assuming Kubernetes knowledge.
