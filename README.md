# REPLACE-WITH-THE-NAME-OF-THE-EXPERIMENT

This repository holds one experiment on the HypothesisLoop platform: the code its jobs run and
the files the platform and its agents read.

| File | What it is |
|---|---|
| `README.md` | this page: what is measured, how a trial runs, what to vary |
| `.hypothesisloop/experiment.yaml` | the experiment spec: its name, description, metrics, budget (in H100-hours), length and team |
| `.hypothesisloop/job.yaml` | the base job spec, submitted unedited for every trial |
| `.hypothesisloop/Dockerfile` | the image jobs run in, built from the repository root |
| `pyproject.toml`, `uv.lock` | the Python dependencies the image installs with uv |
| `metrics.py` | how a job reports a metric: `post_metric(fraction_complete, value, "key")` |
| `checkpoint.py` | how a long job saves its state and resumes: `save(path)`, `restore(path)`, `stopping()` |
| `.gitignore` | keeps caches, virtual environments and editor files out of a commit |

`hl repo init DIR` puts these files in a new directory. Fill in each placeholder in capitals, and
`hl repo check` says what is left. `hl platform-experiments start DIR` creates the experiment.

## Branches

Agents clone the branch the experiment names and none commits to it. The baseline is measured on
`hl/<platform experiment>/baseline`. Each agent works on `hl/<platform experiment>/<agent>/<hypothesis>`,
which `hl hypothesis checkout` makes. A job runs the commit `hl job submit` pushes.

## Roles

A baseline agent measures the control. It starts with the planner, and the executors start at the
first baseline job. Researchers own the hypothesis graph and run no job. Executors run the jobs and
are ranked. The `agents` list in the spec sets the team: agent type `researcher` makes researchers,
and any other type makes executors. The executors in the list are how many work at once.

## Models

A model is `<provider>/<model id>`, such as `anthropic/claude-sonnet-5`. `hl models` lists those
served. An agent runs on its entry's model, else its agent type's, else the platform default. A
researcher that names neither runs on `coordinator_model`.

## Jobs on GPUs and on CPUs

A job on GPUs names an accelerator type from `hl capacity` in `.hypothesisloop/job.yaml`, such as
`nvidia.com/gpu.product=NVIDIA-GB10` or `nvidia.com/gpu.product=Tesla-T4`, with
`accelerator_count`. A job on CPU cores deletes those two lines. `uv add torch` puts a CUDA build
of torch in the image on amd64 and arm64 alike, and the image runs on the architecture it was
built for (`hl image set`).

## Long runs

A job keeps its state with `checkpoint.py` under its own prefix of the platform's object store.
A job the platform starts again (a retry, a burst job preempted, a machine taken back) keeps that
prefix, restores its last save and continues. A machine taken back gives no warning, so a job
saves at a steady pace, and `checkpoint_grace_seconds` in the job spec gives it time to save once
more when the platform stops it.

## What is measured

REPLACE-WITH the ranked metric, why it is the goal, and the gate that makes a result wrong. A
trial reports the gate with its other metrics and exits 0 when it ran to the end. One that
breaks the gate ranks nowhere and still counts as a completed trial.

## How one trial runs

    hl job submit .hypothesisloop/job.yaml --hypothesis ID --theory "..." --env KEY=VALUE

REPLACE-WITH what that runs, which code measures and which code is varied, how long a trial takes
and what it costs.

## What to vary

REPLACE-WITH the levers worth trying.

## What must not change

REPLACE-WITH the measurement, the data it is taken on and the gate.
