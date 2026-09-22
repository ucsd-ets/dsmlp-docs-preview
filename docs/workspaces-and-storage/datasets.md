# Datasets

This page covers where shared datasets are stored on Datahub and DSMLP, how to
request that a dataset be staged, and the restrictions that apply to protected
and licensed data.

## Where Shared Data Lives

Shared datasets are stored in one of two locations. The location determines
what a dataset's size counts against.

### The `/datasets` Tree

`/datasets` is the cluster-wide dataset tree. It is present in the container
and on the login node. It holds common training corpora, including MNIST,
CIFAR-10, Tiny-ImageNet, ImageNet, Caltech256, and ShapeNet, alongside data
staged for particular courses. ITS places data there on request. Data under
`/datasets` sits outside both the workspace and personal quotas.

### The Workspace `public/` Area

`public/` is the workspace's own shared area and the most common location for
course datasets. The instructor or the course grader account stages data there,
and every member of the workspace can read it. The area is described in
[The Shared Workspace Area](your-files-and-quotas.md#the-shared-workspace-area).

### Choice of Location

The instructor chooses which of the two locations a course uses. Data that
several courses use, or that is too large for a workspace, is usually staged
under `/datasets`. Data specific to one course usually sits in `public/`.

## Finding What Is Available

The catalog of cluster-wide datasets is published at
[datahub.ucsd.edu/hub/datasets](https://datahub.ucsd.edu/hub/datasets). The
tree itself can be browsed from a running environment or from the login node:

```bash
cd /datasets
ls
```

Course data staged under `/datasets` is placed in a directory named for the
workspace ID, `/datasets/<workspace-id>-public/`, and can be located without a
catalog entry.

## Reading Shared Data in Place

Do not copy a shared dataset into a home directory. Copying a shared dataset is
the fastest way to exhaust a quota, and the copy is no closer to the job than
the original, because the same filesystem is visible from the container and
from the login node. Common causes of a full quota are listed in
[Common Causes of a Full Quota](your-files-and-quotas.md#common-causes-of-a-full-quota).

Point code at the shared path instead. A notebook written against a local
machine usually needs one change, to the dataset path, and no other.

Where a run needs a derived subset, store the subset in the home directory, not
the source corpus.

## Asking for a Dataset to Be Staged

Request staging for a large dataset that several people need, rather than
downloading it into each home directory. Email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) with what the data is, its
approximate size, and who needs to read it.

Course dataset distribution of up to 500 GB is accommodated as a matter of
course. Larger corpora are accepted on a space-available basis.

A dataset may be published cluster-wide or scoped to one course. State which in
the request.

Research datasets are handled by Research IT at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).

> [!NOTE]
> Raise confidential or licensed data, and data subject to a data use
> agreement, before it is uploaded. The restrictions are described in
> [Restricted & Licensed Datasets](#restricted--licensed-datasets).

### Small Downloads

Small downloads need no request. `wget` and `curl` are available on the login
node and in the container. Larger transfers are covered in
[Moving & Sharing Data](moving-and-sharing-data.md).

## Restricted & Licensed Datasets

Two separate restrictions apply to datasets. Data classification determines
whether data may be placed on the cluster at all. License terms govern what may
be done with data the campus has already acquired.

### P3 and P4 Data

P3 and P4 are protection levels in the University's data classification. P4
data, such as clinical records or export-controlled material, is prohibited on
Datahub and DSMLP without review or exception, and P3 data may be permitted
after review, as stated in
[Data Classification](../reference/policy.md#data-classification).

Where either level may apply, raise the dataset before any of it reaches the
cluster. For instruction and coursework, email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu). For research, email Research IT at
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).

### Examples of Restricted Data

The University's [classification
levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html)
are the authority. ITS documentation gives these examples:

| Kind of data | Examples |
|---|---|
| Government classified or controlled | CUI, CTI, ITAR, FISMA |
| Health and personal information | PHI/HIPAA, IRB-controlled data, statutory PII |
| Student records | Other students' grades or academic records (FERPA) |
| Contractually protected | Information subject to certain Data Use Agreements |

A TA or grader working with identifiable grades is handling protected data. The
grading tools are built to hold that material and are described in
[Grading](../grading/README.md).

### Licensed and Subscription Data

Some data on the cluster is licensed rather than open. It was acquired under
terms that limit who may read it and what may be done with the results.
Licensed corpora are staged read-only and released to an authorized group
rather than to all users. The Nielsen subscription datasets held for the
Chicago Booth Kilts Center are an example. They are mounted read-only outside
the general `/datasets` tree, as described in
[Mounting External Storage](your-files-and-quotas.md#mounting-external-storage).

License terms usually impose the following conditions:

- Read the data in place. A copy in a home directory is a second copy under the
  same terms, and it consumes quota.
- Do not pass the data on. Access is granted to an individual, not to that
  person's collaborators. Moving the data into a shared or outward-facing
  location is a licensing decision, not a file operation. Sharing outside the
  cluster is covered in
  [Sharing with People Who Have No Cluster Account](moving-and-sharing-data.md#sharing-with-people-who-have-no-cluster-account).
- Delete derived subsets and intermediate files that are no longer needed. They
  inherit the terms of their source.

Where a course or lab has acquired data under license terms, state so in the
request described in
[Asking for a Dataset to Be Staged](#asking-for-a-dataset-to-be-staged), so that
the data is scoped correctly from the start.

### Publishing Restricted Data Externally

Datahub and DSMLP are not for publishing restricted data outward. The platform
is not for externally available services or applications except as required for
coursework or projects, and the limit applies in particular to data held under
license terms. The hosting rule is stated in
[Hosting Externally Available Services](../reference/policy.md#hosting-externally-available-services).

## Dataset Retention After a Course

> [!WARNING]
> Large datasets cannot be archived when a course environment is purged.

Raise the retention of any corpus that must be kept before the term ends.
Archiving is described in
[Archiving on Request](../access/when-access-starts-and-ends.md#archiving-on-request).
