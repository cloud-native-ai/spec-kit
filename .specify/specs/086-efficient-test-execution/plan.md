# Implementation Plan: 测试高效执行（默认并发）

**Branch**: `086-efficient-test-execution` | **Date**: 2026-11-06 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `086-efficient-test-execution` → Feature 086 Efficient Test Execution (Concurrent by Default)
**Input**: Specification from `.specify/specs/086-efficient-test-execution/requirements.md` (33 FR / 12 SC / 7 shared strings; validated 2026-11-06, `validate-requirements.py` 0 error / 0 warning)

## Summary

Feature 086 changes **how** the canonical suite runs, not **what** it runs, and then writes that
execution model into the principle layer the framework ships.

Three independent, all-required delivery lines plus one preservation obligation:

1. **Runner execution model** (`scripts/bash/run-tests.sh` and its runtime mirror). The canonical
   runner becomes parallel-by-default when a parallel engine is importable; serial stays a complete,
   always-runnable path behind `--serial`, inside an xdist worker (`PYTEST_XDIST_WORKER` set), or when
   the engine is absent. The script gains an interpreter probe, a worker-count resolver
   (`--workers N|auto` > `SPECKIT_TEST_WORKERS` > `auto`), a "caller already passed `-n`" guard, and a
   two-pass mode for declared serial exceptions. `--names-out`, the `# test runner:` stderr header, the
   exit code and the comment-only `comm -13` discipline survive unchanged; parallel and serial runs stay
   comparable **by name**.
2. **Principle landing**. A new owner guideline `shared/guidelines/test-execution-efficiency.md` holds the
   only definition of the rule (coverage is necessary but not sufficient; execution efficiency is a
   same-tier quality attribute; process parallelism vs async concurrency vs neither; how to measure).
   Constitution (template + live), instructions (template + live) and the generator's MUST-include list
   each carry a **pointer**, never the body.
3. **085 preservation and real-scenario dogfood**. The temporary Goal/Team, stage roles, concurrency
   budget, worktree isolation, integration queue and checkpoints are *used*, not rewritten; this run is
   the evidence 085 SC-010 has been missing.

The measured gap is small and specific: Phase 0 measured 1031.48 s serial vs 201.87 s parallel on the
same tree (5.1×), with exactly **one** new failure name. The plan therefore spends its parallelism-safety
budget on one named exception rather than on a speculative rewrite of every subprocess-using test.

## Technical Context

**Language/Version**: Python `>=3.8` for everything that ships (runner interpreter resolution, `audit-test-budget.py`, new tests; stdlib only, matching Constitution scope discipline). Host measurement environment: CPython **3.14.6** in `.venv`, pytest **9.2.0**, pytest-xdist **3.8.0**, macOS arm64, 18 logical CPUs.
**Primary Dependencies**: `pytest-xdist` as a **dev-only** dependency (`[project.optional-dependencies].dev`, marker `python_version >= "3.9"`). CLI runtime dependency set is unchanged (FR-015, SC-010, 067 RC-08).
**Storage**: N/A — no persistent store, no ledger, no database. Failure-name lists are per-run files under `.specify/.tmp/` (sanctioned temp root) and this spec's `test-evidence/`.
**Testing**: pytest (`tests/contract`, `tests/unit`, `tests/integration`), Tests Mode ON (Constitution IV). Every FR/SC has a carrier; targeted gates at each slice, full suite at implement start (baseline slot) and after review (closure slot).
**Target Platform**: macOS/Linux developer and CI hosts; Python 3.8 hosts (no xdist) are a **normal** path served by the serial fallback.
**Project Type**: code generator / framework — `templates/`, `shared/`, `scripts/`, `skills/`, `tests/`.
**Performance Goals**: the parallel default must beat the recorded serial baseline on the same selection and tree. Recorded observation (not a promise): 1031.48 s → 201.87 s, 5.1×. A further tuning pass compares `-n auto` vs `-n 6` vs `-n 8` and `--dist load` vs `loadfile` under identical commands (A13).
**Constraints**: no new `/speckit.*` command, skill entry template or runtime service (FR-017); no network calls, resident processes or caches (FR-016); no skip/xfail/rerun-luck/selection-shrinking to erase a failure-name diff (FR-010); no rewrite of 067's RC conclusions or of any 085 artifact (FR-027); the "same command minus the parallel arguments is still a complete run" property (067 RC-03) is a hard constraint.
**Scale/Scope**: 33 FR / 12 SC; 1 runner script (+1 mirror), 1 parser script, 1 new owner guideline (+1 mirror), constitution template + live, instructions template + live, 1 generator skill (+1 mirror), ~8 guard/targeted test files, 2 dev docs, `CHANGELOG.md`, feature registry.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.16.0 — every `### <numeral>. <name>` heading, in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design decision cites an FR in this plan; requirements validated 0/0; no implementation claim is made here. |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 086; this stage advances `Draft → Planned` in `features.md` and `features/086.md` only. |
| III | Intent-Driven Development | ✅ Pass | User intent + the 10 clarify rulings drive the design; alternatives are recorded in `research.md` R-1…R-9, not silently chosen. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; `contracts/` owns C-001…C-052; every new behavior has a red leg (mutation table in `contracts/runner-contract-086.contract.md` § Mutation Legs). |
| V | AI Agent Integration Standards | ✅ Pass | No agent definitions or per-tool copies are touched; the 085 carrier observation is recorded, not acted on (A19). |
| VI | Continuous Quality & Observability | ✅ Pass | Every improvement is measured: wall-clock, failure-name diff, exit codes, ledger classification. No symptom suppression: the watch-target resolution is a named serial exception, not a skip (§ Risks R-2). |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan order respected; plan does not implement; `/speckit.tasks` remains the next step. |
| VIII | Code as the Single Source of Truth | ✅ Pass | The runner contract in `contracts/` was derived from the live `scripts/bash/run-tests.sh`; Phase 0 recorded measured facts (18 CPUs, xdist 3.8.0, 19/20 failure names) rather than recalled ones. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One owner guideline, one principle, one instruction section, four parser tokens, one marker. Nine work packages reduce to three disjoint slices and one integration slice (§ Work Packages). |
| X | Documentation Naming & Location Conventions | ✅ Pass | `shared/guidelines/test-execution-efficiency.md` (STR-001) follows the existing guideline naming; spec artifacts use the standard plan-set names. |
| XI | Dogfooding (Self-Application) | ✅ Pass | This feature ships through its own SDD chain; the runner change is exercised by the suite that validates it; framework-source edits are mirrored by `sync-mirrors.py` (Two Hats). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `sync-mirrors.py`, `generate-instructions.sh`, `scan-confirmation-gates.py`, `pre-analyze-check.py`, `decomposition-check.py`, `audit-test-budget.py`; no second engine for any existing predicate (Phase 0 Tool-Reuse Gate, `research.md` R-10). |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Targets Controlled Execution (a 5.1× measured speedup in the inner loop) and Reliable Delivery (name-level failure comparability preserved). |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The rule body lives once in the new owner guideline; constitution, instructions, CHANGELOG and docs site hold pointers only (FR-019, FR-020). Runner contract items that already have an owner (067 RC-01…RC-08) are cited, not restated. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Runner flags, the fallback note and the nested note are defined at first use in `quickstart.md`; the owner guideline states its reader baseline. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The plan carries six named risks with dispositions; the watch-target case is resolved by a declared, enumerable exception rather than a silent patch; implement-time diffs must be attributed item by item (FR-010(a)-(c)). |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory: the owner guideline lands in the existing `shared/guidelines/`; run artifacts use the sanctioned `.specify/.tmp/` root (already git-ignored). |
| XVIII | Grounded Naming | ✅ Pass | `Efficient Test Execution (Concurrent by Default)` is the user's own framing; `test-execution-efficiency.md`, `--serial`, `--workers`, `SPECKIT_TEST_WORKERS`, `pytest-xdist` are fixed by the specification's Shared Strings (STR-001…STR-007), not improvised here. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user-visible surface is one command whose default changes and whose stderr header still describes the command actually executed (FR-005/US3-5); internal pass-splitting is surfaced as a one-line note, not a new interface. |

**Gates Status**: ✅ All 19 gates pass. No ❌ and no ⚠ row, so `## Complexity Tracking` is `N/A`.

**Re-check after Phase 1** (2026-11-06, re-rendered against the design artifacts): unchanged, still 19/19 Pass. The Phase 1 artifacts added no new dependency, no new directory and no new command; they made Principle XIV and Principle VI stricter rather than looser, by pinning (a) the pointer-only shape in `contracts/principle-landing.contract.md` C-021…C-024 and (b) the "no skip, name the exception" rule in `contracts/runner-contract-086.contract.md` C-013.

## Decision Tensions

Record shape, admissibility criteria, rejection forms and the load-bearing threshold are owned by
`shared/guidelines/decision-tension.md` — read from the repository root; this section only carries the
records. Each record is a level-3 sub-section headed `T-NNN`.

### T-001 — The parallel default lives in the runner script, not in pytest configuration

- **decision**: The parallel default is implemented inside `scripts/bash/run-tests.sh`; the repo's pytest configuration stays free of `addopts = -n …`.
- **antithesis**: Put `addopts = "-n auto"` in `[tool.pytest.ini_options]`; when repository-wide behavior is the goal and every entry point (the runner, a bare `pytest`, an IDE run) must move together, it is better — one line changes every caller, and no wrapper can forget it.
- **binding_constraints**:
  - pole_a: The suite must be runnable by the canonical runner without the caller knowing anything about the parallel engine, including on hosts without it.
  - pole_b: A bare `pytest tests/unit` invoked by a developer debugging one file must stay single-process, deterministic and debuggable.
- **discriminating_evidence**: Run `python -m pytest tests/unit/test_audit_test_budget.py -q` with no `-n` in the environment and observe whether more than one worker is created (look for the `bringing up nodes...` banner and `PYTEST_XDIST_WORKER` in a child). Result is binary: one process / many processes.
- **expected_sacrifice**: SC-011 Source ↓ the default's coverage is narrower than repository-wide — a caller that bypasses `scripts/bash/run-tests.sh` (an IDE, a bare `pytest`) does not get the parallel default, so the recorded per-run speedup only holds for runner invocations.
- **revision_trigger**: Two consecutive SDD lines record the same bare-`pytest` bypass (a stage run measuring wall-clock outside the runner) → reopen and move the default into pytest configuration with an explicit `-p no:xdist`-style serial escape.

### T-002 — Unstable-under-parallel tests get a named marker, never a configuration widening

- **decision**: The watch-target self-test is excluded from the parallel pass by a registered `serial` pytest marker and re-run in a serial second pass; the runner combines both passes into one name list and one exit code.
- **antithesis**: Raise that test's own timeout from 60 s to a value that fits under parallel load; when the test's cost is genuine CPU work rather than a scheduling artifact, it is better — the test keeps participating in the parallel run, no second process pool is created, and no new marker vocabulary enters the suite.
- **binding_constraints**:
  - pole_a: A declared exception must be enumerable by name, so a reviewer can list every test that does not run in parallel and the set cannot grow silently.
  - pole_b: The failing signal must stay a **timeout** signal; a timeout widened to fit whichever load happened to occur converts a real regression into a pass.
- **discriminating_evidence**: Run the watch-target self-test alone, unloaded, three times and record the wall-clock spread; then run it inside the parallel pass three times and record how many of six observations exceed 60 s. Binary outcome: parallel-only exceedances exist / they do not.
- **expected_sacrifice**: SC-004 Source ↓ the parallel run pays one extra process-pool start-up for the serial pass, and the runner gains a second code path whose failure modes (zero-collected second pass, mixed exit codes) must themselves be tested.
- **revision_trigger**: The serial pass reports non-zero collected tests for two consecutive closure runs (i.e. the exception set grew), or the watch-target self-test exceeds 60 s in a serial run → reopen: fix the root cause or re-measure the timeout with serial/parallel evidence (A14's fallback form).

### T-003 — The principle is a pointer quartet, not a self-contained constitution clause

- **decision**: The principle's normative body lives only in `shared/guidelines/test-execution-efficiency.md`; the constitution entries and instruction sections carry a short normative reminder plus the owner path.
- **antithesis**: Write the full decision rule (parallel vs async, the measurement ladder, the anti-pattern list) directly into the constitution clause so every downstream project receives the complete text without opening another file; when projects are audited offline or the framework's file set is not available to a reader, it is better — the rule is self-contained and cannot dangle.
- **binding_constraints**:
  - pole_a: A fact must have exactly one definition point, so a threshold changed in the owner must not require editing the constitution, instructions, CHANGELOG and docs site in lockstep.
  - pole_b: A downstream reader who opens only the shipped constitution must still be able to tell what the principle demands and where the detail lives.
- **discriminating_evidence**: Change one criterion value in the owner guideline only, then run the constitution/instructions pointer guards; binary outcome: all pointer guards stay green with zero edits elsewhere / they go red.
- **expected_sacrifice**: SC-002 Source ↓ the shipped constitution is not self-contained: a reader without the framework's `shared/` tree gets a pointer to a path they cannot open, so the contract must require the pointer to name the path explicitly and to state the rule in one sentence.
- **revision_trigger**: A downstream project reports (or a review finds) that the pointer path does not resolve after `specify init` in two independent projects → reopen: inline the minimum deciding text and re-derive the owner as the single definition point for the parts that are not deciding text.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/086-efficient-test-execution/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — measured baseline + decisions R-1…R-10
├── data-model.md        # Phase 1 output — E-1…E-10 runtime entities, V-1…V-22 rules
├── contracts/           # Phase 1 output — 4 files, C-001…C-052 all counted in Phase 1 Summary below
├── quickstart.md        # Phase 1 output — S-0…S-8
├── feature-ref.md       # Phase 1 output — bound Feature 086 and delivery surface
├── test-evidence/       # Stage evidence (clarify-gates.txt, plan-gates.txt, and implementation runs)
├── checkpoints/         # 085 checkpoint records (owned by the driver, read-only for this stage)
├── goal/                # 085 temporary Goal (read-only for this stage)
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

This feature produces a standalone `research.md` because Phase 0 exceeded the inline threshold: it
carries a measured baseline (run timings, versions, CPU count, mirror drift) plus ten decisions, and the
measurements are the evidence every later comparison is judged against.

### Source Code (repository root)

```text
scripts/bash/run-tests.sh                                  # canonical runner: parallel default, --serial, --workers, two-pass
.specify/scripts/bash/run-tests.sh                         # (mirror) byte-identical runtime copy
shared/guidelines/test-execution-efficiency.md             # NEW owner: the rule body, single definition point
.specify/shared/guidelines/test-execution-efficiency.md    # (mirror)
templates/constitution-template.md                         # factory constitution: new principle XIX
.specify/memory/constitution.md                            # live constitution: new principle XX, version 1.17.0
templates/instructions-template.md                         # factory instructions: new ambient section
.specify/instructions.md                                   # live instructions: same section, regenerated
skills/internal/manage-constitution/SKILL.md               # MUST-include list 11 -> 12 entries
.specify/skills/internal/manage-constitution/SKILL.md      # (mirror)
skills/external/sdd-loop-driver/scripts/audit-test-budget.py  # VALUE_FLAGS gains 4 parallel switches
tests/contract/test_sdd_loop_driver_skill.py               # test_c24 watch-target self-test: register `serial` marker
tests/contract/test_run_tests_runner_contract.py           # NEW: runner behavior contract (C-001…C-016)
tests/unit/test_audit_test_budget.py                       # parallel full-run classification rows
tests/contract/test_constitution_double_landing.py         # count pins 19/20/12, watchlist 7
tests/contract/test_fast_fail_discipline.py                # version 1.17.0, counts, section counts 33/34
tests/contract/test_instructions_section_propagation.py    # section count guards
tests/contract/test_instructions_size_budget.py            # 34,816 B budget
tests/contract/test_test_execution_efficiency.py           # NEW: principle landing both-sides guard
pyproject.toml                                             # dev extra: pytest, pytest-xdist (>=3.9 marker), `serial` marker
docs/contribute/dev-setup.md                               # how to run the suite under the new default
CONTRIBUTING.md                                            # parallel default, --serial, SPECKIT_TEST_WORKERS
CHANGELOG.md                                               # 086 entry
.specify/memory/features.md, .specify/memory/features/086.md  # registry + detail (this stage: -> Planned)
```

**Structure Decision**: this is a framework-source change inside the existing layout — no new top-level
or area directory is created. The change concentrates in `scripts/bash/` (the runner), `shared/guidelines/`
(one new owner), the two governance surfaces (`templates/` + `.specify/`), the driver skill's scripts
directory, and `tests/`. Every edited source file that has a runtime or generated copy is listed in the
Mirror Obligations table below; the mirrors are generated by `scripts/python/sync-mirrors.py` (and, for the
live instructions file, by `generate-instructions.sh`), never hand-written.

### Mirror Obligations

**Baseline drift measured before any edit** (2026-11-06, `python3 scripts/python/sync-mirrors.py --check`):
`OK: all per-tool command copies match the source templates`; `templates` 22 files ok; `skills/external`
415 ok; `skills/internal` 138 ok; `agents` 16 ok; `scripts` 121 ok; `shared` 94 ok — **zero pre-existing
drift**. Every Verify cell below therefore reads "no NEW drift", judged against this measured baseline.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/bash/run-tests.sh` | `.specify/scripts/bash/run-tests.sh` (`scripts` pair of `sync-mirrors.py` MIRROR_PAIRS; strict-extras pair) | Run `python3 scripts/python/sync-mirrors.py --write --only scripts/bash`, then `--check`; the `scripts` line must still read `ok` and `diff -q scripts/bash/run-tests.sh .specify/scripts/bash/run-tests.sh` must be silent — judged as no NEW drift against the zero measured above; the source file's own byte-identity is additionally pinned by a test (C-016). |
| `shared/guidelines/test-execution-efficiency.md` (new) | `.specify/shared/guidelines/test-execution-efficiency.md` (`shared` pair) | `python3 scripts/python/sync-mirrors.py --write --only shared/guidelines`, then `--check`: `shared` line `ok`; new file present on both sides with equal byte length (`wc -c` on both paths, equal values, actual numbers recorded in evidence). |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` (`templates` pair, `commands` sub-path excluded) | `sync-mirrors.py --write --only templates/constitution-template.md` then `--check`: `templates` line `ok`, 22 files (count unchanged — no new template file is added). |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` (`templates` pair) | Same `--write`/`--check` route; `templates` line `ok`. |
| `skills/internal/manage-constitution/SKILL.md` | `.specify/skills/internal/manage-constitution/SKILL.md` (`skills/internal` pair) | `sync-mirrors.py --write --only skills/internal/manage-constitution` then `--check`: `skills/internal` line `ok`, 138 files. |
| `.specify/instructions.md` (live) | none — this file is **generated from** `templates/instructions-template.md` by `generate-instructions.sh`; it is not a `sync-mirrors.py` pair | `.specify/scripts/bash/generate-instructions.sh` run once after the template edit; then the section-count guards (`test_instructions_section_propagation.py`, live 34) and the byte-budget guard (`test_instructions_size_budget.py`, ≤ 34,816 B) decide pass. The live file's byte size is measured and recorded in evidence. |
| `.specify/memory/constitution.md` (live) | none — the live constitution is authored in place, not generated | The double-landing guard (`test_constitution_double_landing.py`) and the fast-fail pin guard (`test_fast_fail_discipline.py`) assert the live roster contains the new title, the live count is 20 and the version is 1.17.0 after the edit. |
| `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` | `.specify/skills/external/sdd-loop-driver/scripts/audit-test-budget.py` (`skills/external` pair; note this pair excludes `site` and `internal`) | `sync-mirrors.py --write --only skills/external/sdd-loop-driver` then `--check`: `skills/external` line `ok`, 415 files; `diff -q` on the single pair silent. |

## Execution Premises

Owner of the shape, the `Status` / `Decision` domains and the invalid-row rule:
`shared/workflow/acceptance-hardening.md` § Execution Premises.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | A parallel engine (`pytest-xdist`) is importable in the interpreter the runner resolves, so the parallel default can actually engage on this host | `.venv/bin/python -c "import xdist; print(xdist.__version__)"` → `3.8.0`; `.venv/bin/python -m pytest --version` → `pytest 9.2.0`; Phase 0 parallel run used `-n auto` successfully (`test-evidence/phase0-baseline.md`) | verified | — |
| EP-002 | The host provides more than one logical CPU, so process parallelism converts into wall-clock reduction rather than added start-up cost | `python3 -c "import os; print(os.cpu_count())"` → `18`; `uname -m` → `arm64`; measured 1031.48 s → 201.87 s on the same tree | verified | — |
| EP-003 | The only parallel-only failure is the watch-target self-test; no other test is parallel-unsafe on this tree | `comm -13 <serial names> <parallel names>` returned exactly one line (`tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`); `comm -23` returned none — both re-measured during this plan stage against the stored lists | verified | — |
| EP-004 | xdist workers each receive a distinct pytest `basetemp`, so tests that write into `tmp_path` do not collide across workers | Read at plan time: `xdist/workermanage.py:340-341` sets `option_dict["basetemp"] = str(basetemp / name)` per worker; `xdist/remote.py:400` assigns it. Re-check by observing distinct `tmp_path` prefixes in a parallel run | verified | — |
| EP-005 | `PYTEST_XDIST_WORKER` is present in a worker process' environment and inherited by its subprocesses, so the runner's nested auto-serial guard fires for tests that shell out | `xdist/remote.py:417` sets `os.environ["PYTEST_XDIST_WORKER"] = workerinput["workerid"]` before collection; no cleanup path deletes it. Re-check in the new contract test by spawning a child that echoes the variable | verified | — |
| EP-006 | The Python 3.8 downstream path is reachable with a serial-only fallback, because `pytest-xdist` 3.x requires Python ≥ 3.9 | `pyproject.toml` `requires-python = ">=3.8"`; requirements A15 records xdist 3.x's 3.9 floor; the fallback is exercised by a stubbed-import contract test (C-007) rather than by installing a 3.8 interpreter in this run | verified | — |
| EP-007 | The instructions byte budget (34,816 B) still has room for one more ambient section on the live file | Measured at plan time: `.specify/instructions.md` = 33,357 B (1,459 B headroom); `templates/instructions-template.md` = 28,930 B | verified | — |
| EP-008 | The confirmation-gate scan total has zero integer headroom above its frozen baseline, so the new principle and guideline must add zero gate hits | `python3 .specify/scripts/python/scan-confirmation-gates.py --root . --json` → `total 27`, `violations 0`; the frozen baseline under `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` → `confirmationGates.total = 23` (a pre-existing 4-gate drift, see `research.md` R-8) | verified | — |
| EP-009 | The canonical runner's current serial path writes exactly one `--names-out` line list and one exit code, so a two-pass mode is additive rather than a rewrite | Read at plan time in `scripts/bash/run-tests.sh`: the `--names-out` branch captures the run into `OUT`, keeps `STATUS`, filters `^FAILED` lines through a sort into the target file, then exits with `STATUS` — one list, one code | verified | — |
| EP-010 | The 085 temporary Goal exists and is spec-local, so this run's dogfood evidence has a place to land without touching the global stores | `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md` present; no `.specify/goal/**` write is planned by this stage | verified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `085`: `.specify/memory/features/085.md`, `.specify/specs/085-sdd-temporary-goal-team/verification.md`

Basis for inclusion: Feature 085 owns the temporary Goal/Team, stage-agent, concurrency, worktree-isolation,
integration-queue and checkpoint mechanisms this feature must preserve and must dogfood (FR-027…FR-030).
Basis for exclusion of 067: it owns the runner contract whose conclusions this feature cites but must not
rewrite (RC-01…RC-08); it contributes no `Deferred` section and no open measurement to inherit.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `085:SC-010_status` | `inherited` | `gate:GATE-086` | `this-slice` | 085 measured `SC-010_status=partial` because no full 8-stage driver run with LLM stage agents existed. This feature's own run is that run: its completion gate asserts the spec-local temporary Goal, the per-stage checkpoints, the per-stage carrier/concurrency record and an actual max concurrency above one (`contracts/dogfood-and-preservation.contract.md` C-048…C-051). **`/speckit.tasks` MUST emit a dogfood completion gate bearing exactly the identifier `GATE-086`**; a `task:<T-ID>+test:<path>` carrier naming `tests/contract/test_temp_goal_contract.py` is an equally admissible alternative once such a task row exists. |

No other extracted row exists: 085's detail carries no `## Deferred` section with non-empty items, and its
`verification.md` `deferred_tasks=` value is empty, so the extraction set is exactly one row.

## Document Structure

**Not required.** This is an `execution`-class line (`flow_class-check.py --action lookup --unit-id
"spec:086-efficient-test-execution"` → `flow_class: execution`, `source: declaration`, exit 0). Per
`templates/plan-template.md` § Document Structure's class condition, the four subsections are a required
output for an expression-class line and MUST NOT become a new mandatory section for an execution-class
line. `scripts/python/doc-consistency-check.py --action structure` reports this class as
`not-applicable`.

## Risks and Mitigations

| ID | Risk | Likelihood / impact | Mitigation | Detection |
|----|------|--------------------|-----------|-----------|
| R-1 | A new parallel-only failure appears beyond the recorded one (a shared-path write, a shared fixture, a port) | medium / high | FR-010's open-list discipline: run the full suite in parallel after the runner change and attribute every new name to (a) root-cause fix, (b) named serial exception, or (c) pre-existing baseline failure. No preemptive rewrite of passing tests (A6). | `comm -13` between the new parallel list and the recorded serial baseline |
| R-2 | The `serial` marker becomes a loophole that hides real failures | medium / high | The exception set is a registered marker whose members are enumerable by `pytest -m serial --collect-only -q`; the count is recorded in evidence; a defect in a marked test still fails the serial pass and still reaches the combined exit code | Marker enumeration + combined exit code in `contracts/runner-contract-086.contract.md` C-011, C-013 |
| R-3 | Two-pass mode corrupts the failure-name list (second pass truncated, zero-collected pass misread) | medium / high | Both passes write into one sorted, de-duplicated list; a zero-collected second pass is success (exit 5 normalized); the list's entry count is echoed to stderr (`STR-002`) so an empty list is distinguishable from a missing one | C-008…C-012 + the empty-list discrimination test |
| R-4 | The new principle pushes the live instructions file over the 34,816 B budget | low / medium | Measured headroom 1,459 B before the edit; keep the section to a summary + pointer + ≤ 5 bullets; if the measured post-edit size exceeds the budget, raise it only with the measured value recorded (A-clarify ruling 3) | `test_instructions_size_budget.py` with the measured byte count in its message |
| R-5 | The new guideline or principle adds a confirmation-gate hit (zero headroom) | low / high | Word the principle and guideline with design avoidance (declarative MUSTs, no gate-shaped prompt phrasing); measure with `scan-confirmation-gates.py` before and after and require `total` not to increase (baseline 27 measured this stage) | Gate-scan diff against `.specify/.tmp/086/gate-scan-baseline.json` |
| R-6 | Count guards go red one at a time and get patched piecemeal | high / medium | FR-022: every count/budget guard is updated **in the same change** as the principle lands; the guard values are named in `contracts/principle-landing.contract.md` C-030…C-040 | Guard suite run as one batch at WP-B close |
| R-7 | The parallel default silently disables itself (e.g. the interpreter probe picks a `python3` without xdist) and the speedup never materializes | medium / medium | The stderr header must describe the command **actually executed** and a named mode line must state serial/parallel and why; a silent serial fallback is a test failure (C-005, C-006, C-014) | Header + mode-line assertions in the runner contract test |
| R-8 | 085 artifacts get rewritten in passing (a "small cleanup" of goal/team/checkpoints) | low / very high | Forbidden paths declared per work package; C-041's mechanical check asserts this feature's commits touch no 085 path | `git diff --name-only <stage-base>..<closure-commit> -- .specify/specs/085-sdd-temporary-goal-team .specify/goal .specify/teams` (empty) |
| R-9 | Dev-dependency addition leaks into CLI runtime dependencies | low / high | `pyproject.toml` dev group only; SC-010 checks the runtime dependency set diff is empty; `[tool.hatch.build]` force-include list untouched | Dependency diff command in `quickstart.md` S-7 |

## Complexity Tracking

N/A — Constitution Check has no ❌ or ⚠ row, so there is no violation to justify.

## Work Packages (for the 085 team: concurrent slices)

Nine work packages group into three build slices plus one integration slice. **WP-A and WP-B are disjoint by
file** and can run concurrently under the 085 temporary Team; **WP-C integrates after both** because it
re-runs the full suite and updates the registry. The driver's decomposition/team layer consumes this table;
the plan stage does not implement it.

| WP | Slice | Owned paths (write) | Forbidden paths | Depends on | Purpose |
|----|-------|---------------------|-----------------|-----------|---------|
| WP-A1 | A | `scripts/bash/run-tests.sh`, `.specify/scripts/bash/run-tests.sh` (mirror) | everything else | — | Runner execution model: parallel default, `--serial`, `--workers`/env precedence, no-duplicate-`-n`, nested auto-serial, xdist-missing fallback, two-pass serial exceptions, preserved header/exit/names-out |
| WP-A2 | A | `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`, `.specify/skills/external/sdd-loop-driver/scripts/audit-test-budget.py` (mirror), `tests/unit/test_audit_test_budget.py` | everything else | — | `VALUE_FLAGS` gains `-n`, `--numprocesses`, `--dist`, `--maxprocesses`; explicit-parallel full runs classify as full runs; existing rows reclassify identically |
| WP-A3 | A | `pyproject.toml`, `docs/contribute/dev-setup.md`, `CONTRIBUTING.md` | `[project].dependencies`, `[tool.hatch.build]` | A1 (needs the runner flags documented) | Dev extra with `pytest` + `pytest-xdist` (`python_version >= "3.9"` marker), `serial` marker registration, docs for the new default |
| WP-A4 | A | `tests/contract/test_run_tests_runner_contract.py` (new) | — | A1 | Runner contract test: default parallel, `--serial`, precedence, no duplicate `-n`, nested auto-serial, xdist-missing stub, two-pass names/exit, header truthfulness |
| WP-B1 | B | `shared/guidelines/test-execution-efficiency.md` (new), `.specify/shared/guidelines/test-execution-efficiency.md` (mirror) | — | — | Owner guideline: why coverage is insufficient; parallel vs async vs neither; isolation preconditions; runner contract; measurement; declared serial exceptions; anti-patterns |
| WP-B2 | B | `templates/constitution-template.md`, `.specify/memory/constitution.md`, `templates/instructions-template.md`, `.specify/instructions.md`, `skills/internal/manage-constitution/SKILL.md` + mirror | — | B1 | Principle landing: XIX (template) / XX (live), version 1.16.0 → 1.17.0, Sync Impact Report prepended, instruction section inserted after `## Single-Run Evidence Discipline`, MUST-include 11 → 12, live instructions regenerated by `generate-instructions.sh` |
| WP-B3 | B | `tests/contract/test_constitution_double_landing.py`, `tests/contract/test_fast_fail_discipline.py`, `tests/contract/test_instructions_section_propagation.py`, `tests/contract/test_instructions_size_budget.py`, `tests/contract/test_test_execution_efficiency.py` (new) | — | B1, B2 | Count/budget pins updated in the same change (19→20 live, 18→19 template, 11→12 skill, watchlist 6→7, instruction sections 33→34 live / 32→33 template, version 1.17.0) and the both-sides principle guard with a mutation leg |
| WP-C1 | C (integration) | `tests/contract/test_sdd_loop_driver_skill.py` (watch-target marker), `tests/integration/test_sdd_loop_efficiency_regression.py` (nested runner header/mode assertion) | — | A1, A4, B2 | Parallel safety: register the `serial` marker on the self-test, assert the nested path; attribute every new failure name from the post-change parallel run |
| WP-C2 | C (integration) | `.specify/memory/features.md`, `.specify/memory/features/086.md`, `CHANGELOG.md`, `tests/contract/test_temp_goal_contract.py` (re-run + additive dogfood assertion), `test-evidence/` | `.specify/specs/085-sdd-temporary-goal-team/**`, `.specify/goal/**`, `.specify/teams/**` | A1–A4, B1–B3, C1 | 085 preservation evidence (byte identity + zero new failures in the 085 contract/integration files `test_temp_goal_contract.py`, `test_temp_team_schema.py`, `test_checkpoint_protocol.py`, `tests/integration/test_temp_team_worktree_queue.py`, `tests/integration/test_checkpoint_rollback.py`), SC-010 status per evidence, registry/CHANGELOG, final parallel-vs-serial name diff |

**Merge order**: A1 → (A2, A3 in parallel) → A4; B1 → B2 → B3; C1 after A1+A4+B2; C2 last.
**Concurrency**: A and B are file-disjoint (A touches `scripts/`, `skills/external/`, `pyproject.toml`, docs;
B touches `shared/`, `templates/`, `.specify/memory/constitution.md`, `.specify/instructions.md`,
`skills/internal/`), so the 085 team may run one A agent and one B agent simultaneously. Within A, A2 and A3
are disjoint. C runs alone because it measures the whole tree.

## 085 Carrier Observation (A19b) — recorded, not repaired

The host running this SDD line does not expose Feature 085's stage-agent types. Stage carriers are the
host-native `SDD Requirements Executor` (requirements), `general-purpose` (clarify) and `SDD Executor`
(plan). The persisted temporary Team, per-stage seats, `agent_concurrency_requested: 24`, worktree write
isolation, integration queue and per-stage checkpoints are still created and used by the driver.

This is a **carrier downgrade, not a 085 failure**: the mechanisms under test (goal/team persistence,
concurrency accounting, isolation, checkpoints) are exercised; only the agent *identity* is supplied by the
host. Consequence for evidence: 085 SC-010's "LLM stage agents" clause is satisfied by the host-native
carriers, and the run must record the carrier name per stage so a reviewer can see which identity executed
each stage. The plan does not repair the host's agent roster (out of scope under FR-027/FR-017).

## Phase 1: Design Artifacts Summary

Filled after the artifacts landed on disk. Counts below are taken from the files, not from intent.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Plan | `plan.md` (this file) | 19/19 Constitution Check rows (live roster v1.16.0), 3 decision tensions, 10 execution premises, 1 inherited-blocker row, 9 risks, 9 work packages |
| Research | `research.md` | 8 measured baseline rows (B-1…B-8) + 10 decisions (R-1…R-10) + a 9-row re-measure list |
| Data model | `data-model.md` | 10 entities (E-1…E-10), 22 validation rules (V-1…V-22), 3 state machines |
| Contracts | `contracts/` | 4 files, 52 clause ids: `runner-contract-086.contract.md` C-001…C-016 (16), `budget-ledger-parser.contract.md` C-017…C-020 (4), `principle-landing.contract.md` C-021…C-040 (20), `dogfood-and-preservation.contract.md` C-041…C-052 (12); 7 mutation legs (M-1…M-7) |
| Quickstart | `quickstart.md` | 9 scenarios: S-0 (pre-flight, 4 commands executed at plan time with output pasted) plus S-1…S-8 (route (b), pinned by named tests, premises listed per scenario) |
| Feature ref | `feature-ref.md` | Bound Feature 086, 1 row, delivery surface mapped to FRs |

**Drift from the Phase 0 expectation**: none in artifact count. Two content notes. (a) The watcher
self-test is named `test_c22_watch_target_hook_selftest` (`tests/contract/test_sdd_loop_driver_skill.py:537`),
not `test_c24…` as the dispatch brief's WP-C label suggested; the correct id is used everywhere below and the
discrepancy is disclosed in `research.md` R-9 rather than carried forward. (b) The gate-scan frozen baseline
reads 23 while the live scan reads 27 — a pre-existing drift, recorded as a premise (EP-008) and a criterion
couched as "no increase", not repaired here.

## Disclosed Deviations

1. **Counted rather than sampled Phase 0 evidence.** The serial and parallel full-suite lists used for EP-003
   are the stored Phase 0 artifacts (`.specify/.tmp/086/baseline-failed.txt`, `parallel-failed.txt`), and the
   `comm` diff was re-run during this plan stage against those files. The runs themselves were executed by the
   driver before this stage and are not re-executed here (a full run is a budgeted slot event, not a plan-stage
   action).
2. **Execution premises are all `verified`.** Any `unverified` premise would have needed a re-measurement task;
   the eight values that could have been assumed (xdist version, CPU count, per-worker basetemp, worker env
   variable lifetime, mirror drift, instructions headroom, gate total, 085 goal presence) were all measured or
   read from the named source at plan time, with the command recorded in the Evidence cell.
3. **No `/speckit.research` run.** Phase 0 resolved every unknown from the repository (code, contracts,
   measurements), so no external source evaluation was needed; `research.md` was produced from that pass.
4. **Same-author review.** This plan's Constitution Check and Post-Generation Quality Gate were scored in the
   same run that authored the artifacts, per `shared/workflow/objective-analysis-gate.md` § delegation. The
   delegation result, if a fresh-context reviewer was unavailable, is recorded in `research.md` R-10 with the
   degraded evidence path named.
