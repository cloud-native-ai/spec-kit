# Phase 1 Data Model — Feature 086 Efficient Test Execution (Concurrent by Default)

This feature stores no persistent data. What it needs a model for is the **run-time value surface**: the
inputs the runner resolves, the artifacts a run emits, and the governance records the principle lands in.
Each entity below names its owner (the single definition point) so no field is defined twice.

Conventions: `MUST` rows are validation rules with stable ids `V-NNN`; state machines are `SM-n`.
"Owner" means the file or program that defines the entity, never a copy.

## Entities

### E-1 Test Run (一次测试运行)

The unit every comparison in this feature is expressed in.

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `command` | string | runner `argv` after flag processing | The command actually executed, echoed in the stderr header (FR-005, R-6) |
| `mode` | enum `parallel` \| `serial` | runner | Required; never inferred from the absence of a flag |
| `reason` | enum `explicit` \| `nested` \| `no-xdist` \| absent | runner | Present only when `mode=serial` (contract C-002's three closed values); `mode=parallel` carries no `reason` token at all — the default applying is visible from `mode=parallel` itself |
| `workers` | integer \| `auto` | runner | Resolved value (auto is replaced by the engine's choice at execution time; the record keeps the literal for evidence) |
| `dist` | enum `load` \| `loadfile` \| `loadscope` \| caller-supplied | runner | Default `load` |
| `passes` | list of Pass (E-2) | runner | One element in serial mode; two in parallel mode when a `serial` exception exists, one otherwise |
| `exit_code` | integer | runner | Combined: non-zero if any pass failed (V-006) |
| `names_out` | Failure-Name Set (E-3) \| absent | runner | Written only when `--names-out <file>` is passed |
| `wall_clock_seconds` | number | pytest summary line | Not computed by the runner; taken from the run's own summary |

**Owner**: `scripts/bash/run-tests.sh` (its contract: `contracts/runner-contract-086.contract.md`).

### E-2 Pass (一次运行中的一遍)

| Field | Type | Notes |
|-------|------|-------|
| `selection` | string | `-m "not serial"` (parallel pass), `-m serial` (serial pass), or the caller's own selection (single pass) |
| `workers` | integer \| `auto` | `-n <n>` for the parallel pass, `-n0` for the serial pass |
| `collected` | integer | From the pass's own summary; `0` is legal for the serial pass |
| `failed_names` | list of string | Extracted from `^FAILED ` lines |
| `exit_code` | integer | pytest's own; `5` (no tests collected) is normalized to `0` **for a `serial` pass only** |

**Owner**: same as E-1.

### E-3 Failure-Name Set (失败名清单)

The only legal comparison substrate (FR-007, FR-014, A3).

| Field | Type | Notes |
|-------|------|-------|
| `path` | absolute path | The `--names-out` target |
| `entries` | sorted, de-duplicated list of test ids | One nodeid per line; no counts, no classes |
| `entry_count` | integer | Echoed to stderr as the `<n>` of `# failed-name list written: <path> (<n> entries) passes=<k>` (`STR-002`) so "empty because zero failures" is distinguishable from "not written" (FR-008) |
| `sources` | list of pass indices | Which passes contributed; its size is the `<k>` of `passes=<k>` in the same stderr line, so a two-pass run is auditable (FR-011) |

### E-4 Worker Configuration (进程数配置)

| Field | Type | Domain / rule |
|-------|------|---------------|
| `flag` | integer \| `auto` \| absent | `--workers` value |
| `env` | integer \| `auto` \| absent | `SPECKIT_TEST_WORKERS` (`STR-006`) |
| `effective` | integer \| `auto` | `flag` > `env` > `auto` (V-002) |
| `source` | enum `flag` \| `env` \| `default` | For evidence |

### E-5 Serial Escape Hatch (串行逃生口)

Not a stored value but a closed three-way condition; each branch must be observable from the run's own
output (FR-002, FR-005, FR-006, SC-004).

| Branch | Trigger | Observable |
|--------|---------|-----------|
| `explicit` | `--serial` present (`STR-007`) | `# test runner: mode=serial reason=explicit` |
| `nested` | `PYTEST_XDIST_WORKER` set in the environment | `# test runner: mode=serial reason=nested` |
| `no-xdist` | the interpreter cannot `import xdist` | `# test runner: mode=serial reason=no-xdist` |
| (`default`) | none of the above and xdist is importable | `# test runner: mode=parallel …` |

### E-6 Serial Exception (串行例外)

| Field | Type | Notes |
|-------|------|-------|
| `marker` | literal `serial` | Registered in `[tool.pytest.ini_options].markers` (V-012) |
| `members` | list of node ids | Enumerable by `pytest -m serial --collect-only -q`; the enumeration is the audit surface (FR-011) |
| `reason_class` | enum `parallel-load` \| `shared-state` \| `timeout` | Must be a parallel-specific reason, not "flaky" (A7) |
| `justification` | path + one line | Points at the evidence (measured serial vs parallel cost) |

**Owner**: `pyproject.toml` (registration) + the marked test file (membership); the enumeration command is
owned by `contracts/runner-contract-086.contract.md` C-011 (with C-012 for the disposition rule and C-013 for the combined list).

### E-7 Parallel Engine Availability (并行引擎可用性)

| Field | Type | Notes |
|-------|------|-------|
| `importable` | boolean | Result of `<interpreter> -c 'import xdist'` |
| `version` | string \| absent | Recorded into `test-evidence/` per run when present |
| `interpreter` | absolute path | The one `resolve_python` chose |

### E-8 Test Execution Efficiency Principle (测试执行效率原则)

The governance entity. Its normative body exists **once**.

| Field | Owner | Pointers (must not restate the body) |
|-------|-------|--------------------------------------|
| Rule body: why coverage is insufficient, efficiency as a quality attribute, parallel vs async vs neither, isolation preconditions, measurement, anti-patterns | `shared/guidelines/test-execution-efficiency.md` (`STR-003`, file name `STR-001`) | — |
| Principle entry, template | `templates/constitution-template.md` § `### XIX. Efficient Test Execution (Concurrent by Default)` | pointer to `STR-003` |
| Principle entry, live | `.specify/constitution.md` § `### XX. Efficient Test Execution (Concurrent by Default)` | pointer to `STR-003` |
| Ambient section, template | `templates/instructions-template.md` § `## Test Execution Efficiency (测试执行效率)` | summary + pointer |
| Ambient section, live | `.specify/instructions.md` (generated) | summary + pointer |
| Generator MUST-include entry | `skills/internal/manage-constitution/SKILL.md` (entry 12) | anchor sub-bullet + anchor path |

Constitution version: `1.16.0 → 1.17.0` (MINOR: new principle). Live numbering `XX`, template numbering
`XIX` — independent rosters, both guarded.

### E-9 Budget Ledger Classification (预算台账分类)

| Field | Type | Notes |
|-------|------|-------|
| `command` | string | The recorded full-run command |
| `value_flags` | set of tokens | `VALUE_FLAGS` in `audit-test-budget.py`; extended by `-n`, `--numprocesses`, `--dist`, `--maxprocesses` (FR-024) |
| `classification` | enum `full-run` \| `targeted` \| `non-run` | An explicit-parallel full run MUST classify as `full-run` (FR-024, SC-005) |
| `positional_args` | list | MUST NOT contain a `VALUE_FLAGS` member's value (FR-025) |

**Owner**: `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` (+ `.specify` mirror).

### E-10 Dogfood Evidence Record (dogfood 证据记录)

The records this run must leave for 085 SC-010 (FR-028, SC-008). Field names are 085's; this feature only
supplies values.

| Field | Type | Source |
|-------|------|--------|
| `goal_slug` | string | `.specify/archive/goal-team/trees/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md` |
| `team_slug` | string | `.specify/teams/086-efficient-test-execution/**` (created by the driver after plan U4 per 085 C-008) |
| `agent_concurrency_requested` | integer | `24` (A17) |
| `agent_concurrency_effective` | integer per stage | Recomputed per stage; downgrades named |
| `carrier` | string per stage | Host-native carrier identity (`SDD Requirements Executor` / `general-purpose` / `SDD Executor`) |
| `checkpoints` | list of paths | `<spec-dir>/checkpoints/<NN>-<stage>.md` |
| `actual_concurrency_max` | integer | Max agents dispatched simultaneously in any stage; MUST be `> 1` for SC-008 |

**Owner**: 085's checkpoint protocol (`skills/external/sdd-loop-driver/references/checkpoint-protocol.md`)
and the line state spine; this feature must not restate them.

## Validation Rules

| ID | Rule | Source FR |
|----|------|-----------|
| V-001 | `mode` is always present in the stderr mode line; a run whose mode cannot be determined is a defect | FR-001, FR-005 |
| V-002 | `effective = flag if present else env if valid else auto`; a malformed `flag`/`env` exits non-zero with a named error and MUST NOT fall back to 1 | FR-003 |
| V-003 | If the caller's arguments already contain `-n`/`--numprocesses` (any spelling), the runner injects neither `-n` nor `--dist` | FR-004 |
| V-004 | If `PYTEST_XDIST_WORKER` is set, `mode=serial` and `reason=nested`, regardless of `--workers` | FR-005 |
| V-005 | If the engine is not importable, `mode=serial`, `reason=no-xdist`, the run is complete, and the exit code is pytest's | FR-006 |
| V-006 | `exit_code` is non-zero iff any pass's normalized exit code is non-zero | FR-007 |
| V-007 | `entries` is sorted and de-duplicated across passes; one node id per line; the count is echoed to stderr | FR-007, FR-008 |
| V-008 | A run with zero failures writes a file with zero lines **and** the count line; the two facts are recorded together so an empty list is never read as a missing one | FR-008 |
| V-009 | The `serial` pass's exit code `5` (nothing collected) normalizes to `0`; the same exit code in the parallel pass is a failure | R-3 |
| V-010 | Both carriers of the runner are byte-identical after every change; only `sync-mirrors.py` writes the mirror | FR-009 |
| V-011 | A `serial` exception's `reason_class` is one of `parallel-load`, `shared-state`, `timeout`; the value `flaky` is not admissible | FR-010, A7 |
| V-012 | The `serial` marker is registered in `[tool.pytest.ini_options].markers`; an unregistered marker is a pytest warning and a defect | FR-011 |
| V-013 | New failure names in a parallel run MUST be attributed, one by one, to exactly one of: root-cause fix, named serial exception, pre-existing baseline failure; the count of unattributed names MUST be `0` | FR-010, FR-014 |
| V-014 | Both diff directions are recorded: names added **and** names dropped. A dropped name is never claimed as this feature's fix | FR-014, A3 |
| V-015 | The parallel engine appears only in a dev-only dependency group, with an interpreter marker; the CLI runtime dependency list is byte-identical to the pre-change list | FR-015, FR-016 |
| V-016 | No new `/speckit.*` command, skill entry template or runtime service is introduced | FR-017 |
| V-017 | The owner guideline exists at `shared/guidelines/test-execution-efficiency.md` and contains the six required sections (why coverage is insufficient, the efficiency criterion, parallel vs async vs neither, measurement, declared exceptions, anti-patterns) | FR-018 |
| V-018 | Constitution template and live roster each gain exactly one titled entry, both titles identical, both numbered by their own roster, both carrying a pointer to `STR-003` and no criterion table | FR-019 |
| V-019 | Instructions template and live each gain one ambient section whose body contains **no** level-2 heading from the owner guideline | FR-020 |
| V-020 | `manage-constitution` MUST-include list grows by exactly one entry, and the entry carries the anchor sub-bullet and the anchor path | FR-021 |
| V-021 | Every count/budget guard whose value the principle changes is updated in the same change: live principles `19 → 20`, template `18 → 19`, skill entries `11 → 12`, watchlist `6 → 7`, instruction sections live `33 → 34` / template `32 → 33`, constitution version `1.17.0` | FR-022 |
| V-022 | The new principle states a division of labour with the existing test-related principles (what tests do / when they are written vs what they cost to execute) that a reader can decide without ambiguity | FR-023 |

## State Machines

### SM-1 Mode resolution (per invocation)

```text
start
 ├─ caller args contain -n/--numprocesses? ─────────────────► parallel(caller)      [V-003]
 ├─ PYTEST_XDIST_WORKER set? ──────────────────────────────► serial(reason=nested)  [V-004]
 ├─ --serial present? ─────────────────────────────────────► serial(reason=explicit)
 ├─ <interpreter> -c 'import xdist' fails? ────────────────► serial(reason=no-xdist) [V-005]
 └─ otherwise ────────────────────────────────────────────► parallel(default, -n <effective>, --dist load)
```

Order note: the caller's own `-n` is checked first because FR-004 forbids duplicating it — even a nested
or `--serial` invocation must not append a second worker flag to a command that already has one.

### SM-2 Pass composition

```text
serial(r)      → passes = [ Pass(selection=caller, workers=-n0) ]
parallel       → members = pytest -m serial --collect-only
                 members empty?  → passes = [ Pass(selection=caller, workers=-n <n>) ]
                 members present → passes = [ Pass(selection='-m "not serial"', workers=-n <n>),
                                              Pass(selection='-m serial',        workers=-n0) ]
```

### SM-3 Feature status for Feature 086

```text
Draft --(/speckit.plan: this stage)--> Planned
Planned --(/speckit.implement)--> Implemented | Blocked
```
The transition table itself is owned by `shared/workflow/acceptance-hardening.md` § Feature Status; this
state machine only records which stage owns which edge for Feature 086.
