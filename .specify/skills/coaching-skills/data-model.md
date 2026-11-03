# Coaching Run Data Model

**Owner**: this file owns exactly two normative sections — **§ Optimization claim** and
**§ RunStatus**. The run artifacts and their templates are owned by
`references/prompt-templates.md`; the execution order is owned by `SKILL.md`. Do not
restate the run-artifact schema or the workflow here.

## Entities

- **Run** — `{run_id, trainee, resolved_path, layer, started_at, run_dir}`; one run owns
  the four ordered artifacts in `run_dir`.
- **DispatchRecord** — the `## Dispatch` block in `observation.md`:
  `{mode, dispatched_at, payload_ref, returned, anomaly_line, failure_coordinates}`.
- **Claim** — one per Trainee, not per run: `{trainee_slug, run_id, trainee_path,
  created_at}` stored at the claim path below.
- **RunStatus** — the pair `{run, optimization}` recorded once in
  `improvement-plan.md` § Run Status.

## Optimization claim

**Purpose**: serialize the one write step that changes the Trainee Skill, so two
coaching runs cannot invoke `improve-skills` for the same Trainee concurrently.

**Location**: `<coaching-root>/.claims/<trainee-slug>.claim`

- `<coaching-root>` is the directory that contains the run directories (Spec Kit
  deployments: `.specify/memory/coaching/`; standalone: the directory in which the run
  directory was created).
- `<trainee-slug>` is the lowercase kebab slug of the resolved Trainee name — the same
  slug used in the run-id.
- The claim is a sibling of the run directories, never inside a run directory.

**Content**: one JSON object on one line:

```json
{"trainee_slug":"<slug>","run_id":"<run-id>","trainee_path":"<resolved SKILL.md path>","created_at":"<ISO-8601 UTC>"}
```

**Single timing**: create the claim exactly once per run, after
`improvement-plan.md` is on disk and immediately before invoking `improve-skills`.
No earlier and no later. The claim covers only the optimization write, not the
execution loop.

**Atomic creation**: create `.claims/` if absent (idempotent), then create the claim
file with a single exclusive-create syscall. That syscall is the claim decision; a
read-then-create sequence is forbidden.

```python
import json, os
os.makedirs(claim_dir, exist_ok=True)
data = json.dumps({"trainee_slug": slug, "run_id": run_id,
                   "trainee_path": trainee_path, "created_at": created_at}) + "\n"
fd = os.open(claim_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
try:
    os.write(fd, data.encode())
finally:
    os.close(fd)
```

**Conflict rule**: if `os.open` raises `FileExistsError`, read the existing file and
compare `run_id`:

- same `run_id` → this run already holds the claim; continue (idempotent re-entry).
- different `run_id` → conflict. Do not overwrite, do not delete, do not retry.
  Record `optimization: failed` and name the conflicting `run-id` in
  `improvement-plan.md` § Run Status.

**Release**: after `improve-skills` returns — success or failure — remove the claim
only if its `run_id` still equals this run's `run_id`, in a `finally`-equivalent step.
If removal fails, record `optimization: failed` and name the leftover path.

**Leftover**: a claim whose `run_id` differs from the current run and whose referenced
run directory is missing, or has no `improvement-plan.md`, is a leftover. The current
run MUST NOT reclaim it and MUST NOT scan run directories to decide. Record
`optimization: failed`, name the leftover `run-id`, and leave the file untouched.
Manual recovery: the operator verifies the referenced run is abandoned, removes the
claim file, then reruns the optimization step.

**Crash**: a crash after creation and before release leaves the claim; the next run
handles it by the leftover rule above.

## RunStatus

The two values are recorded once in `improvement-plan.md` § Run Status.

### `run` — Trainee execution verdict

Evaluate `failed` → `partial` → `success`; the first matching value wins.

- **failed** — the coaching run itself cannot close: preflight failed, or any of the
  four required artifacts is missing or unreadable. A missing artifact fails the run
  regardless of the quality of the others.
- **partial** — the four artifacts exist, but the Trainee's primary artifact is absent
  or cannot be verified, or the observation carries no collected evidence, or the
  dispatch failed / timed out / was refused, or the Trainee flow stopped mid-way with
  partial artifacts. A return that claims completion without the Trainee's primary
  artifact is `partial`, never `success`.
- **success** — the four artifacts exist, the dispatch returned completed, the
  Trainee's primary artifact exists, and the Trainee flow reached its declared
  terminal success state.

### `optimization` — optimization attempt verdict

- **applied** — the claim was acquired and `improve-skills` accepted and landed the
  plan.
- **skipped** — optimization was deliberately not attempted; a recorded reason exists.
- **unavailable** — the `improve-skills` entry, its required owner document, or the
  claim location cannot be resolved.
- **failed** — claim conflict, `improve-skills` rejection or error, or claim-release
  failure.

### Combination rule

`run` and `optimization` are independent. `optimization` never changes `run`: an
unavailable, skipped, or failed optimization never turns a completed Trainee
execution into `failed`, and a `run: failed` is never repaired by optimization. The
run report restates both values and names the four artifact paths.

## Consumers

- `SKILL.md` § Optimization — reads § Optimization claim for timing, atomic creation,
  conflict, release, and leftover semantics.
- `SKILL.md` § Run Status and § Degradation Ladder — reads § RunStatus for the verdict
  ladder and the combination rule.
- `references/prompt-templates.md` — the `## Run Status` template records the two
  values; this file owns their domains and combination.
