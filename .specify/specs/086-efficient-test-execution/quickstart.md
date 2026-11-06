# Quickstart — Feature 086 Efficient Test Execution (Concurrent by Default)

Nine scenarios. `S-0` was **executed** at plan time and its real output is pasted below. `S-1`…`S-8` are
scenarios against behavior that does not exist until implement lands, so each is route **(b)**: pinned by a
named test or contract clause, with its premises listed explicitly so the next phase re-probes them instead
of inheriting them.

Reader baseline: a maintainer of this repository who wants to run the suite, understand why it is fast now,
and check a claim. Nothing here assumes you have read the rest of the spec.

## Premises common to every scenario

- Repository root is the working directory. The canonical runner is `scripts/bash/run-tests.sh` and its
  runtime mirror is `.specify/scripts/bash/run-tests.sh`.
- The interpreter is chosen by the runner (`SPECKIT_PYTHON`, then `.venv/bin/python`, then `python3`, then
  `python`). On this host it resolves to `.venv/bin/python` (CPython 3.14.6).
- `pytest` and `pytest-xdist` are installed for that interpreter. On this host: pytest 9.2.0, xdist 3.8.0
  (`research.md` B-6).
- Nothing in these scenarios writes outside `.specify/.tmp/` (the sanctioned temporary root) and
  `.specify/specs/086-efficient-test-execution/test-evidence/`.
- A **full run** takes about 3–17 minutes depending on mode. Scenarios S-1/S-2/S-3/S-8 use a small
  `--workers 2` selection where possible so they are cheap to repeat.

## S-0 — Pre-flight (EXECUTED at plan time)

Run these four before anything else; they establish the starting facts every later comparison rests on.

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
.venv/bin/python -m pytest --version
.venv/bin/python -c "import os; print('logical_cpu', os.cpu_count())"
python3 scripts/python/sync-mirrors.py --check
python3 .specify/scripts/python/scan-confirmation-gates.py --root . --json | python3 -c "import json,sys; d=json.load(sys.stdin); print('total', d['total'], 'violations', len(d['violations']))"
```

Actual output on 2026-11-06 (pasted, not transcribed):

```text
pytest 9.2.0
logical_cpu 18
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (415 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (16 files)
ok    scripts/ == .specify/scripts/ (121 files)
ok    shared/ == .specify/shared/ (94 files)
total 27 violations 0
```

Premises this output rests on: `.venv` exists and is the runner's first resolved interpreter; `sync-mirrors.py`
compares exactly the six pairs listed in its `MIRROR_PAIRS`; `scan-confirmation-gates.py` accepts `--root` and
`--json` and prints a top-level `total`. Expected results stated here are the measured ones, so a later run
that disagrees is drift to investigate, not a scenario failure.

## S-1 — Default run is parallel (route b)

```bash
bash scripts/bash/run-tests.sh --workers 2 --names-out .specify/.tmp/086/s1-names.txt -q tests/unit -k audit
```

Expected: stderr carries `# test runner: mode=parallel`, the run exits with pytest's own code, and the name
list file exists with a `# failed-name list written: … (<n> entries)` line.

**Pinned by**: `tests/contract/test_run_tests_runner_contract.py` (contract C-001, C-002, C-013, C-014).
**Premises**: the runner accepts `--workers`; `tests/unit -k audit` selects a small subset; the mode line
starts with `# test runner: mode=`.

## S-2 — Explicit serial is a complete run (route b)

```bash
bash scripts/bash/run-tests.sh --serial --names-out .specify/.tmp/086/s2-names.txt -q tests/unit -k audit
```

Expected: stderr carries `# test runner: mode=serial reason=explicit`; the same selection runs; the name list
is written; the exit code semantics are unchanged. A serial run MUST NOT be labelled degraded.

**Pinned by**: contract C-004; mutation leg M-1 (deleting the `--serial` branch must fail the test).

## S-3 — Precedence, and a named error instead of a silent fallback (route b)

```bash
SPECKIT_TEST_WORKERS=3 bash scripts/bash/run-tests.sh --workers 2 -q tests/unit -k audit   # flag wins -> 2
SPECKIT_TEST_WORKERS=abc bash scripts/bash/run-tests.sh -q tests/unit -k audit             # named error, non-zero
bash scripts/bash/run-tests.sh -n 4 --workers 8 -q tests/unit -k audit                    # caller's -n wins, no second -n
```

Expected: (1) the executed command contains `-n 2`; (2) the run exits non-zero and stderr names the bad value;
(3) the executed command contains `-n 4` exactly once and no `--dist` was appended.

**Pinned by**: contract C-007, C-008, C-009; mutation legs M-2, M-3.
**Premises**: `SPECKIT_TEST_WORKERS` (`STR-006`) is the exact variable name; the runner's argument scan
recognises `-n 4` (separated) as a caller-supplied worker count.

## S-4 — Nested auto-serial (route b)

```bash
PYTEST_XDIST_WORKER=gw3 bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/s4-names.txt -q tests/unit -k audit
```

Expected: stderr carries `# test runner: mode=serial reason=nested`; no second worker pool is started; the
name list is valid.

**Pinned by**: contract C-005; mutation leg M-4. **Premises**: the guard keys on the environment variable, not
on a process-tree walk; xdist sets that variable in worker processes before collection (`research.md` R-4).

## S-5 — Scheduling and worker-count measurement (route b, an experiment, not an assertion)

Run the same selection four ways and compare failure names and wall clock:

```bash
bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/s5-auto-names.txt  -q            # -n auto, --dist load
bash scripts/bash/run-tests.sh --workers 6 --names-out .specify/.tmp/086/s5-n6-names.txt -q
bash scripts/bash/run-tests.sh --workers 8 --names-out .specify/.tmp/086/s5-n8-names.txt -q
bash scripts/bash/run-tests.sh --workers 8 --dist loadfile --names-out .specify/.tmp/086/s5-lf-names.txt -q
comm -3 <(sort .specify/.tmp/086/s5-auto-names.txt) <(sort .specify/.tmp/086/s5-n8-names.txt)
```

Expected: recorded, not predicted — the purpose is evidence for assumption A13. A change to the default
(worker cap, `load` → `loadfile`) is admissible only with this evidence attached and with every new failure
name attributed per contract C-045/C-047.

**Pinned by**: contract C-001 (default is `-n auto` + `--dist load`), `plan.md` § Risks R-1.
**Premises**: the four commands share one selection (no `tests/`-narrowing argument); `comm -3` output is the
symmetric difference; wall clock is read from each run's own pytest summary line.

## S-6 — The `serial` exception is enumerable (route b)

```bash
.venv/bin/python -m pytest -m serial --collect-only -q | tail -5
grep -rn "pytest.mark.serial" tests/contract/test_sdd_loop_driver_skill.py
```

Expected: exactly one collected node id, `tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`;
the marker is registered in `[tool.pytest.ini_options].markers`, so no `PytestUnknownMarkWarning` appears.

**Pinned by**: contract C-010, C-011, C-012, C-044; mutation legs M-5, M-17.
**Premises**: the marker name is the literal `serial`; the test id is `test_c22_watch_target_hook_selftest`
(`research.md` R-9 corrects the brief's `test_c24` label); marker registration lives in `pyproject.toml`.

## S-7 — Dependency boundary holds (route b)

```bash
.venv/bin/python -c "import tomllib,sys; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['dependencies'])"
.venv/bin/python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project'].get('optional-dependencies',{}))"
```

Expected: the runtime `dependencies` list is unchanged from the pre-change list
(`typer`, `rich`, `httpx[socks]`, `platformdirs`, `readchar`, `truststore>=0.10.4; python_version >= '3.10'`);
the dev extra contains `pytest` and `pytest-xdist` with a `python_version >= "3.9"` marker.

**Pinned by**: requirements FR-015/SC-010, 067 RC-08, contract C-052's sibling obligation in `plan.md` WP-A3.
**Premises**: `tomllib` requires Python ≥ 3.11 (true for `.venv` 3.14.6; a 3.8 interpreter would need `tomli`
or a text read — this scenario is documented as host-specific for that reason).

## S-8 — Name-level comparison between serial and parallel (route b)

```bash
bash scripts/bash/run-tests.sh --serial --names-out .specify/.tmp/086/s8-serial.txt -q
bash scripts/bash/run-tests.sh            --names-out .specify/.tmp/086/s8-parallel.txt -q
comm -13 .specify/.tmp/086/s8-serial.txt .specify/.tmp/086/s8-parallel.txt   # new names -> MUST be empty after attribution
comm -23 .specify/.tmp/086/s8-serial.txt .specify/.tmp/086/s8-parallel.txt   # dropped names -> recorded, never claimed as a fix
```

Expected: the first `comm` prints nothing (zero new failure names); the second is recorded verbatim in
`test-evidence/`. Both commands' wall clock is recorded.

**Pinned by**: requirements SC-001/SC-006, contract C-047; this is the same procedure Phase 0 already ran
(`research.md` B-4, B-5), which produced exactly one new name at that time.

**Premises**: the baseline for the closure comparison is the **implementation-start** baseline slot, not the
Phase 0 lists (A9); both runs use the same `--names-out` discipline and the same selection; the serial run's
duration is ~17 minutes on this host, so run it once and consume the record.

## What "done" looks like

| Scenario | Route | Evidence lands in |
|----------|-------|-------------------|
| S-0 | executed | this file (`S-0` output block) |
| S-1, S-2, S-3, S-4, S-6, S-7 | (b) pinned | `tests/contract/test_run_tests_runner_contract.py`, `tests/unit/test_audit_test_budget.py` |
| S-5 | (b) experiment | `test-evidence/` (the four runs' names + wall clock + the `comm -3` output) |
| S-8 | (b) comparison | `test-evidence/` (both lists, both `comm` outputs) |
