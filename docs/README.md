# Datahub & DSMLP Documentation

------------------------------------------------------------------------

This is the documentation set for UC San Diego's **Datahub** and **Data Science
& Machine Learning Platform (DSMLP)**. It is organized by audience and task, with
the technical detail written once and linked from everywhere it is needed.

Please reach out to our team with any questions or feedback regarding these
guidelines or Datahub/DSMLP as a whole.

- Email: [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
- 1:1 Consultation: <https://ucsd-datahub.youcanbook.me/>

## Start Here

------------------------------------------------------------------------

Each page states its assumptions in its opening lines.

| Page | Intended for | Assumes |
|---|---|---|
| [Overview](overview.md) | Everyone; routes to the appropriate page | Nothing |
| [Using Datahub in a Course](student-in-a-course.md) | Students enrolled in a course that uses Datahub | A web browser |
| [Working from the Command Line](working-from-the-command-line.md) | The same students, when a course requires a terminal | A terminal and `ssh` |
| [Teaching with Datahub & DSMLP](instructor-or-ta.md) | Instructors and TAs | A browser; a shell for customization |
| [Projects & Independent Study](student-project.md) | Student projects, independent study, capstones, clubs and teams | Familiarity with a shell |
| [Research on DSMLP](individual-researcher.md) | Researchers working without a lab workspace | Familiarity with a shell |
| [Setting Up a Research Lab](faculty-research-lab.md) | Faculty provisioning access for a group | Some steps are performed by our staff |

## Technical Documentation

------------------------------------------------------------------------

Detail that applies to more than one audience is documented once, in the subject
area it belongs to, and linked from the audience pages.

| Subject | Covers |
|---|---|
| [Access](access/README.md) | The browser, the login node, remote editors, sign-in problems, and when access starts and ends |
| [Workspaces & Storage](workspaces-and-storage/README.md) | The unit that governs rosters, storage, images, GPU access and quotas — and where files live, how they move, and datasets |
| [Running Jobs](running-jobs/README.md) | `launch.sh`, job modes and runtime limits, watching a job, checkpointing, and Kubernetes |
| [GPU Access](gpu-access/README.md) | GPU classes, reservations, Service Units, quotas and availability, and what ends a session |
| [Environments](environments/README.md) | Standard images and pinning, customization, and building a custom image |
| [Grading](grading/README.md) | Grading tools and interfaces, the notebook workflow through to Canvas, and recovery |
| [Reference](reference/README.md) | Error messages, support routing, the glossary, HPC vocabulary, group management, policy and software |
