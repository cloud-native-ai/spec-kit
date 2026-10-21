# Implementation Plan: 066-loop-state-awareness-a

**Branch**: `065-loop-interruption-recovery` | **Date**: 2026-10-21 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `066-loop-state-awareness-a` → Feature 065 SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）
**Input**: Specification from `.specify/specs/066-loop-state-awareness-a/requirements.md`

## Summary

Deliver slice A of Feature 065: a deterministic, read-only state-awareness snapshot for one SDD line. A single `loop-state.py --action snapshot` call aggregates the state spine, the Line Registry entry, the pid/status/log/heartbeat carriers, the watchbeat marker, stage artifacts, git commits, and any available watcher verdict, then emits one JSON document containing `loop_state`, `verdict_source`, an independent `completion`, every interruption finding, stale-signal attribution, and exactly one advisory `recovery_action`.

The design has six load-bearing properties:

1. **Watcher verdict is borrowed, never re-derived.** When a watch target is available, `loop_state` is the watcher verdict verbatim (`verdict_source=watcher`). Only when no watcher/probe verdict exists does an independent, fixed-priority derived map produce `loop_state` (`verdict_source=derived`); that map is not a copy of the watcher state machine and produces no watcher exit codes.
2. **Completion is a separate verdict.** `completion` answers "positive completion evidence + artifacts present", so a sentinel with missing artifacts yields `loop_state` unchanged (for example `DONE`) and `completion=incomplete`, with action `retry`. It never rewrites `loop_state`.
3. **Interruptions annotate; they do not set state.** The eight closed forms are evidence comments with pointers; only the watcher or the derived map may set `loop_state`.
4. **Attribution is envelope-first.** Only carriers whose own `line=`/`run=`/`stage=` envelope proves `own` participate in evaluation; `stale-run`/`foreign`/`unattributed` carriers only enter `stale_signals[]`. Legacy attribution is allowed only for a single active line.
5. **Nothing is guessed and nothing is written.** Missing inputs are `missing`/`unknown`; no zero defaults; thresholds come from their existing owners (explicit input → probe → spine → stage map → watcher `--help`); snapshot has no write path except an explicit `--out`.
6. **Output is reproducible.** Except for `evaluated_at`, the same input yields the same JSON: the snapshot carries no elapsed/age numbers, and every list has a pinned order.

Slice A does not implement `recover` or `check-spine` execution, does not write the state spine, does not take the recovery lock, and does not modify `watch-target.sh`, the four-carrier format, Registry semantics, stage prompts, or any `/speckit.*` command. The parent umbrella plan is blocked and is not an input to this plan.

## Technical Context

**Language/Version**: Python 3.8+ standard library only (local measurement: Python 3.9.6). Bash is reused only to run the existing `watch-target.sh --once`; no new shell implementation.
**Primary Dependencies**: none added. Reused engines: `scripts/watch-target.sh` (verdict owner and threshold owner), `scripts/line-registry.py` (Registry semantics and entry format), `git` (commit and working-tree evidence), `scripts/python/sync-mirrors.py` (generated runtime mirror).
**Storage**: read-only filesystem evidence — state spine, Registry entry, pid/status/log/heartbeat carriers, watchbeat marker, spec artifacts, git object database. No database, no daemon, no resident service. The only write path is an explicit `--out <path>` that refuses the state directory and the repo worktree.
**Testing**: pytest via `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest` (pytest 9.1.1; the repo `.venv` has no pytest — an environment fact, not a product requirement). If that interpreter is unavailable, the suites run with any Python 3.8+ that has pytest; the machine-local path is a measured runner, not a product contract. Suites: `tests/unit/`, `tests/contract/`, `tests/integration/`, plus the engine's stdlib `--self-test`.
**Target Platform**: macOS/Linux driver and execution hosts. Remote topology runs the same engine on the evidence host under the same identity, or consumes a caller-collected `--probe` snapshot; unreachable evidence is `remote-unreachable`, never `DEAD`.
**Project Type**: framework external skill (source + scripts + references), its generated runtime mirror, one documentation entry, and tests.
**Performance Goals**: one bounded watcher `--once`, O(evidence files) reads, and O(stage paths) bounded git queries per call. No network polling, no background process, no resident state.
**Constraints**: read-only snapshot; no watcher semantic or exit-code change; no Registry/lease/ownership change; no stage-prompt or `/speckit.*` change; thresholds referenced from owners, never copied; no push/merge/kill/delete; deterministic output except `evaluated_at`.
**Scale/Scope**: one line × one stage per invocation; multi-line callers loop per line. Slice scope is 25 FR definitions and 8 success criteria; 8 interruption forms; 6 recovery actions; 1 new engine action (`snapshot`) plus its self-test; 1 new owner reference; 1 new docs section; 3 new test files plus one existing contract-test update.

## Design Completeness Gates

| Gate | What must be complete | Evidence | Status |
|------|-----------------------|----------|--------|
| G1 Technical Context | Every field answered from measured code/docs; no unresolved clarification marker | Technical Context above; `research.md` § 0–2 (measured watcher, Registry, carrier and test baselines) | ✅ |
| G2 Constitution Check | One row per constitution principle, dynamically derived; Fail/Partial justified | 16-row table below, re-checked after Phase 1 | ✅ |
| G3 Structure & Mirrors | Real directories, every mirror/generated copy listed, verify criterion measured against baseline | Project Structure + Mirror Obligations; baseline 26-file pair, 0 drift | ✅ |
| G4 Phase 1 Artifacts | data-model, contracts, quickstart and feature-ref landed; counts backfilled from disk | Phase 1 Design Artifacts Summary; `test-evidence/plan-stage-status.json` | ✅ |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design clause in `contracts/` maps to a slice FR or SC; `feature-ref.md` carries the coverage matrix; the two interpreted edges (A-P1 stale-run guard, A-P2 Registry dispatch evidence) are recorded as assumptions for the next clarify, not silent overrides |
| II | Feature-Centric Development | ✅ Pass | Slice A stays bound to Feature 065; the feature row/detail record the slice-A plan, the already-Planned status and the queued slices; no new Feature ID or row |
| III | Intent-Driven Development | ✅ Pass | Requirements state the what/why; `research.md` records decisions, rejected alternatives and measured facts before the how |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; each implementation phase starts with its red contract/unit test; clause-numbered contracts, named fixtures, three mutation drills; existing 108-test targeted baseline recorded |
| V | AI Agent Integration Standards | ✅ Pass | No provider, tier or `AGENT_CONFIG` change; the engine is CLI-agnostic and consumes the existing watcher |
| VI | Continuous Quality & Observability | ✅ Pass | Versioned JSON envelope, evidence pointers, deterministic output, docs entry; quality commands are runnable with any Python 3.8+ pytest; no speculative subsystem or resident service |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan chain; decomposition gate re-ran `proceed` for 25 FR; the Feature Index is re-validated without a status regression (already Planned) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 measured the watcher help/defaults, attribution code, Registry entry fields and carrier formats; the stricter stage-envelope rule is explicitly subordinate to a verbatim watcher verdict (`contracts/awareness-rules.md` RUL-01) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One one-shot CLI action, no daemon/scheduler/runtime platform; `recover`/`check-spine` execution deliberately deferred to later slices |
| X | Documentation Naming & Location Conventions | ✅ Pass | New owner reference uses lowercase path semantics `references/state-awareness.md`; the existing docs page is updated in place; no reserved name or nested README |
| XI | Dogfooding (Self-Application) | ✅ Pass | The slice itself runs through SDD; two hats named; source edit + generated mirror + docs, not a `.specify`-only patch |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the existing watcher, Registry read model, git and the `sync-mirrors.py` Tool record; `.specify/memory/tools/` has no state-awareness Tool, so writing the engine is the expected outcome |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Controlled Execution (evidence-based next action), Change Validation (completion/artifact/commit evidence) and Learning Capture (reproducible snapshot); no new scoring system |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | `watch-model.md`/`watch-target.sh` own watch verdicts and thresholds; `stage-prompts.md` owns U4/stall defaults; `efficiency-model.md` §3 owns plan artifacts; the new owner reference is the single runtime prose owner of the awareness projection and reaches the others by reference; the plan/data-model/contracts are design projections that cite the requirements, not runtime owners; CMP-04 pins the map against the U4 and plan-owned sources |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `recovery_detail` and the docs entry follow `.specify/shared/guidelines/user-facing-comprehension.md`; docs assertions pin the entry, call shape and read-only boundary |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Missing evidence stays `missing`/`unknown`; `UNKNOWN` resolves to `stop`, never a guessed `resume`; the three mutation drills are a mandatory implementation gate (CMP-08), not a claim that they have already run |

**Gates Status**: ✅ All gates pass. No ❌ or ⚠ row; Complexity Tracking is N/A.

**Re-check after Phase 1** (2026-10-21, after the artifacts landed and two fresh-context read-only reviews): the 16 rows remain ✅ Pass. The review fixed the `--no-sentinel` D4/D5 branch, added the `legacy-stale` stale reason, made the stale-run guard a single predicate, added the watchbeat writer verification route, clarified the I7 annotation versus the out-of-scope `check-spine` validator, added the reserved `recover` envelope shape, removed the Feature-status transition claim (already Planned by the 065a plan), and recorded the 065a/066 slice-identity conflict. New evidence: `data-model.md` (12 entities / 61 validation rules), four contract files (92 clauses), `quickstart.md` (8 scenarios), `feature-ref.md`. No new violation; Complexity Tracking remains N/A.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/066-loop-state-awareness-a/
├── plan.md                       # This file (/speckit.plan output)
├── research.md                   # Phase 0 measured facts, decisions, rejected alternatives
├── data-model.md                 # Entities, stage map, derived/completion/action tables, validation rules
├── contracts/                    # CLI, snapshot schema, awareness rules, compatibility/tests
├── quickstart.md                 # Scenario walkthroughs + executed plan-time baseline
├── feature-ref.md                # Feature binding, FR/SC coverage, deliverables, boundaries
├── requirements.md               # Upstream (already committed)
├── checklists/requirements.md    # Upstream quality checklist (already committed)
├── notes/parent-fr-mapping.md    # Upstream dated mapping record (already committed)
├── test-evidence/                # Upstream gate evidence (already committed)
└── tasks.md                      # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/
├── SKILL.md                                  # Hard Requirement + References pointer to the new owner reference
├── references/
│   └── state-awareness.md                    # NEW owner reference: snapshot projection, attribution, state map, watchbeat read/write form
└── scripts/
    └── loop-state.py                         # NEW engine: snapshot action + stdlib --self-test (recover/check-spine reserved)

.specify/skills/sdd-loop-driver/              # Generated runtime mirror (sync-mirrors.py --write; never hand-edited)
docs/reference/skills/sdd-loop-driver.md      # Entry point, call shape, relationship to watcher/Registry, read-only boundary
tests/unit/test_loop_state_engine.py          # NEW unit suite (pure functions, self-test, no-write proof)
tests/contract/test_sdd_loop_driver_state_awareness.py  # NEW contract suite (clauses, watcher SHA, map/doc parity)
tests/integration/test_loop_state_snapshot_matrix.py   # NEW named-fixture matrix + real watcher/probe/git cases
tests/contract/test_sdd_loop_driver_skill.py  # Update pinned mirror file list with the two new files
```

**Structure Decision**: This slice extends the existing self-contained external skill. It adds exactly one engine file and one owner reference inside `skills/external/sdd-loop-driver/`, updates two existing documentation surfaces (`SKILL.md` and the docs entry), adds three test files, and updates the existing skill contract test's pinned mirror list. No new top-level directory, no `src/` or `templates/` change, and no new package dependency.

### Mirror Obligations

Baseline measured before this plan (2026-10-21): `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` reports the pair equal at 26 files (0 drift). The watcher SHA-256 baseline is `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4` (source and mirror equal); `watch-target.sh --self-test` reports 38 passed / 0 failed.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` | `sync-mirrors.py --check --only skills/external/sdd-loop-driver`; criterion "no NEW drift" against the measured 0-drift baseline; post-write `filecmp` on this pair |
| `skills/external/sdd-loop-driver/references/state-awareness.md` (new) | `.specify/skills/sdd-loop-driver/references/state-awareness.md` | Post-write file exists and is byte-identical; absent from the pre-write baseline; pair check remains 0 drift |
| `skills/external/sdd-loop-driver/scripts/loop-state.py` (new) | `.specify/skills/sdd-loop-driver/scripts/loop-state.py` | Post-write file exists and is byte-identical; the mirror file is executable-identical to the source; pair check remains 0 drift |
| `docs/reference/skills/sdd-loop-driver.md` | none (authored documentation entry, not mirrored) | Content assertions for the entry, call shape and read-only boundary are pinned by the new contract suite |
| `tests/unit/test_loop_state_engine.py`, `tests/contract/test_sdd_loop_driver_state_awareness.py`, `tests/integration/test_loop_state_snapshot_matrix.py`, `tests/contract/test_sdd_loop_driver_skill.py` | none | The suites run; the updated pinned mirror list includes the two new skill files |

`watch-target.sh` is **not edited**, so its SHA-256 baseline is a compatibility assertion, not a mirror obligation.

## Scope Boundary & Blocked-Review Findings Absorption

### In scope (slice A)

- `snapshot` action and its stdlib `--self-test`; JSON envelope and exit-code ladder 0/1/2 frozen.
- Input resolution, Registry read, state-spine read (machine segment and legacy downgrade), carrier attribution, watchbeat read, stage artifact map, git commit evidence, probe input.
- Derived `loop_state`, independent `completion`, eight interruption annotations, one advisory `recovery_action`, `isolation_required`, `recovery_reason`/`detail`, `effective`, `salvage`, `stale_signals`.
- Owner reference, SKILL pointer, docs entry, tests, mirror registration.

### Explicitly out of scope (later slices)

- `recover` and `check-spine` execution; state-spine writes; recovery records; `attempts/` isolation; recovery lock; handoff files; the `check-spine` lifecycle validator; retry/stop apply paths.
- Cross-slice test matrix aggregation (parent D-zone item 8) and record topology/recover lock (parent D-zone item 11).
- Any change to `watch-target.sh`, `watch-model.md` verdict semantics, `stage-prompts.md` state-spine write timing, Registry/lease/ownership, or `/speckit.*` command flows.
- Live-process stop decisions: A only recommends `watch` for a live `TIMEOUT`; `--confirm-live-stop` belongs to the recovery slice.

**Scope clarification**: the `lifecycle-spine-violation` interruption *form* is in slice A as an annotation (including the Registry-present/spine-missing path and the running-spine-with-no-live-evidence path). The `check-spine` action that deterministically validates the spine schema is out of slice. The watchbeat *writer* is a driver obligation carried by SKILL.md and the owner reference; the engine only reads the marker. The reserved `recover` action returns the shared envelope shape with `result="refused"` and exit 2; no execution is implemented.

### Blocked-review reconciliation (A-relevant findings)

Source: `.specify/specs/065-loop-interruption-recovery/notes/plan-blocked-review.md`. The rows below are the design home for each absorbed finding; findings 11, 13 and 15 are explicitly out of slice or not applicable.

| # | Finding | Slice-A design home |
|---|---------|---------------------|
| 1 | Attribution conflict (`own`/`legacy` defined twice) | `contracts/snapshot-schema.md` attribution rules + `contracts/awareness-rules.md`; envelope-only `own`; legacy only for a single active line |
| 2 | Salvage gate circularity | `contracts/snapshot-cli.md` `--salvage-evidence`; `contracts/awareness-rules.md` salvage as an input before the action; no salvage input ⇒ `retry` |
| 3 | ANOMALY predicate gated on own status | `contracts/awareness-rules.md` derived rule D2: `(exit record exists OR pid dead)` and last log line starts `ANOMALY:` |
| 4 | `dead-no-exit-record` vs sentinel | `contracts/awareness-rules.md` form I2 requires no sentinel; sentinel present routes to completion |
| 5 | Interruption forms override `loop_state` | `contracts/awareness-rules.md` annotation-only rule; every form has zero state-setting authority |
| 6 | Spine schema vs writers; `last_verdict` strictness | `contracts/snapshot-schema.md` spine fields and `contracts/awareness-rules.md` three-state consistency; `stalled`/`retrying` may omit `last_verdict` |
| 7 | Pseudo-completion double bind | `data-model.md` completion table + `contracts/awareness-rules.md`; `loop_state` stays verbatim, `completion=incomplete`, action `retry` |
| 8 | `stage_base_commit` writer missing | `data-model.md` commit evidence + `contracts/snapshot-schema.md`; missing base ⇒ `commit=unknown`; writer obligation is explicitly assigned to the later spine slice |
| 9 | Watcher non-regression cannot go red | `contracts/compatibility-and-tests.md` pins the measured SHA-256 and requires a byte-change mutation to turn red |
| 10 | Registry-missing path missing | `contracts/snapshot-cli.md` `registry.status` + `contracts/awareness-rules.md` Registry/spine precedence; `missing`/`unreadable`/`invalid` are distinct and continue evaluation when spine/carriers are readable |
| 11 | Lock vs no-write actions | Out of slice: A takes no lock, performs no mutation, and never returns a recovery result |
| 12 | Live TIMEOUT stop undefined | `contracts/awareness-rules.md` form I3 + action rule: live `TIMEOUT` recommends `watch` only; stop requires the later explicit-decision path |
| 14 | Test matrix lacks named fixtures | `contracts/compatibility-and-tests.md` + the contract/integration suites enumerate the named fixtures in the test files |
| 13 | Quickstart lifecycle | Reconciled: A produces a Phase 1 quickstart required by the plan command; every scenario is self-contained and tears down its own fixture, so the finding's shared-`$TMP` lifecycle defect does not apply |
| 15 | Baseline label | Not applicable to A: the plan states measured commands and dates, not an engine baseline number |

## Phase 0: Research Review

Standalone [research.md](research.md) (Phase 0 exceeded the inline threshold). Measured facts that shape the design:

- **Watcher**: SHA-256 `b6a275…f2b0b4`; `--self-test` 38 passed / 0 failed; `--help` exposes the defaults and the verdict/exit mapping; `--once` returns one `WATCH` line plus `EVIDENCE`; attribution is `own` only when both `line=` and `run=` match.
- **Registry**: entry file is `$SPECIFY_LINE_REGISTRY_DIR/<line>.json`, else `$XDG_STATE_HOME/spec-kit/lines`, else `$HOME/.local/state/spec-kit/lines`; the entry carries `run_id`, `state`, `stage`, `spine_path`, `status_path`, `log_path`, `heartbeat_path`, `worktree_path`, `repo_root`, and identity fields. `line-registry.py --action reattach-brief` is the existing read aggregation, but it does not expose every path the snapshot must report; the engine reads the entry JSON directly and pins a parity contract against the Registry resolver.
- **Carriers**: status line `exit=<rc> ... sentinel=<0|1>` with an optional `line= run= stage= event=` envelope; pid line `pid=<pid> start=<token> ...`; heartbeat mtime; log meta `log-<line>-<stage>.log.meta.jsonl`. The watcher's attribution precedence is status → meta → heartbeat → pid → unattributed, and it rejects non-own carriers.
- **Baselines**: targeted pytest set `tests/contract/test_sdd_loop_driver_skill.py`, `tests/contract/test_sdd_loop_driver_efficiency.py`, `tests/unit/test_line_registry_engine.py`, `tests/unit/test_decomposition_check.py` = 108 passed; mirror pair = 26 files, 0 drift.
- **Gate**: slice decomposition re-ran `proceed` (25 FR ≤ 30); the umbrella remains split/blocked and is not an input.

All decisions (D-01…D-20), rejected alternatives, determinism rules and the test strategy are in `research.md`.

## Implementation Sequencing

The sequence keeps the later `/speckit.tasks` breakdown inside the 40-task ceiling while preserving red-first coverage. Each phase starts by writing or extending its red test, then implements to green:

1. **A — Engine foundation**: red tests for the CLI parser, `schema_version=1` envelope, exit-code ladder and read-only guard; then the implementation and the self-test harness skeleton.
2. **B — Inputs and evidence**: red fixtures for line/run/stage resolution, Registry status mapping, spine machine/legacy parsing, probe loading, effective-value resolution (watcher `--help` parser, no hardcoded thresholds), carrier attribution, watchbeat read, stage artifact map and git commit/uncommitted evidence; then the readers.
3. **C — Semantics**: red unit tests for derived map D1–D11, `completion`, `spine.consistent`, interruption forms I1–I8 (annotation only), stale-signal classification, salvage input and the action table with the retry-limit and live-TIMEOUT guards; then the evaluator.
4. **D — Distribution**: contract assertions first for the owner reference, SKILL.md Hard Requirement + References pointer and docs entry; then the edits and mirror regeneration.
5. **E — Tests**: unit/contract/integration suites, named fixtures, determinism diff, no-write proof, watcher SHA anchor, map/doc parity and self-test coverage; red-first per suite.
6. **F — Evidence**: mutation drills (no-watcher detection, completion separation, interruption-only annotation), baseline/closure test-budget evidence, and quickstart execution verification once the engine exists.

## Risks

- **Stale-run precedence vs a live/complete attempt**: FR-003 rule (4) is ordered before `watch`/`verify`. A same-line `stale-run` carrier must not cause a retry of a provably running or provably complete current attempt. The design applies the rule only when the current attempt is not provably running and `completion≠complete`; the carrier is still reported and `isolation_required` stays false in the preserved cases. This interpretation is recorded as assumption A-P1 and pinned by a named fixture; if the next clarify wants the literal priority, only the action table changes.
- **Registry-dir resolution duplication**: the engine reads the entry directly to obtain every path, so the resolver is a small, pinned mirror of `line-registry.py`'s env/XDG/HOME order; a contract test compares both on env-set, XDG and default cases and turns red on drift.
- **Watcher help parsing**: defaults are parsed from `--help`, not copied. If the help format changes, the contract test fails loudly instead of silently falling back to a number.
- **Probe schema discipline**: a probe is a snapshot-shaped document; remote unreachability is carried as an additive `remote` object, not a private probe format. A probe never falls back to local files for missing fields.
- **Implement commit scope**: "code/test commits" is approximated as commits after `stage_base_commit` touching non-`.specify/` paths. This is a bounded proxy; the owner reference records it and the commit evidence exposes the observed commit list so U4 can judge.
- **Determinism**: no elapsed/age numbers in the output; time enters only through `evaluated_at` and through threshold comparisons whose inputs are stable fixtures. The determinism test strips `evaluated_at` and compares the rest byte-for-byte after canonical JSON serialization.
- **Task budget**: 25 FR / 8 SC should fit the 40-task ceiling, but the `tasks` U4 gate will re-measure; if it reports `split-required`, the driver must split or record an explicit upstream decision before analyze.
- **Plan-time non-execution**: the engine does not exist yet, so every quickstart engine example is marked not executable at plan time with its premises; the executable plan-time baseline uses only already-existing commands (watcher self-test, mirror check, targeted pytest). The contract suite pins the command grammar; implementation executes the examples and replaces the disclaimers with measured results.

## Phase 1: Design Artifacts Summary

Counts below were verified against the files on disk after the Phase 1 artifacts landed; they were not taken from memory.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 12 entities (`E-01`–`E-12`), 61 validation rules (`V-001`–`V-061`), stage map, D/I/A tables |
| Contracts | [`contracts/`](contracts/) | 4 files, 92 clauses: `snapshot-cli.md` (`CLI-01`–`CLI-20`), `snapshot-schema.md` (`SNP-01`–`SNP-30`), `awareness-rules.md` (`RUL-01`–`RUL-30`), `compatibility-and-tests.md` (`CMP-01`–`CMP-12`) |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 scenarios (S1–S8) plus one executed plan-time baseline section; every engine example carries a per-example plan-time disclaimer and premises |
| Feature reference | [`feature-ref.md`](feature-ref.md) | Feature binding, FR 25/25 and SC 8/8 coverage, deliverable list, cross-feature boundaries |
| Research | [`research.md`](research.md) | 20 decisions, measured baseline, rejected alternatives, test strategy |
| Plan-stage evidence | [`test-evidence/plan-stage-status.json`](test-evidence/plan-stage-status.json) | Pre-check, watcher self-test, mirror pair, targeted pytest and feature-registry results; engine examples marked not run at plan time |

**Drift from the Phase 0 expectation**: none. Phase 0 expected 12 entities, four contracts and eight quickstart scenarios; the final counts match. The plan-time baseline was executed with the existing watcher/mirror/pytest commands; engine examples remain non-executable until the implementation lands, as disclosed per example.

## Slice Identity Note

The repository already contains a tracked sibling slice `065a-state-awareness` with its own requirements, plan, contracts and tasks, and Feature 065 is already `Planned` from that plan. The upstream brief for this run designates `066-loop-state-awareness-a` as the active slice-A requirement; this plan therefore lands under 066 and does not modify, delete or re-plan 065a. The two specs overlap in scope; 066 supersedes 065a as the execution basis for the current line, while 065a remains a historical tracked artifact. Feature 065's status is already `Planned`; this plan records the 066 plan and performs no status transition or regression. Any later governance decision to retire 065a is a separate explicit action, not part of this slice.

## Assumptions Recorded by This Plan

- **A-P1 — Stale-run action guard**: FR-003 rule (4) is applied as a retry driver only when the current attempt is not provably running and `completion ≠ complete`. A running current attempt keeps `watch`; a complete current attempt keeps `verify` or `resume`. In both preserved cases the stale carrier remains visible in `stale_signals[]` and in the `stale-signal` interruption. Rationale: retrying a running or already complete stage would duplicate work and contradicts the "no re-dispatch of a completed stage" invariant. This is recorded for the next clarify and pinned by a named fixture.
- **A-P2 — Registry dispatch evidence**: the auto-generated `run_id` written at registration is not dispatch evidence. Registry contributes dispatch evidence only when a non-empty `stage` is bound together with stage runtime paths or a dispatch `last_event`; this keeps the "registration itself is not dispatch evidence" rule meaningful.
- **A-P3 — Legacy spine readability**: a readable legacy stage/checkpoint line is dispatch evidence even when `stage_started_at`/`stage_deadline_epoch` are absent; those fields then remain `unknown` and derived rules that depend on them are skipped rather than guessed.
- **A-P4 — Watchbeat freshness source**: marker age is taken from its own `at=<epoch>` when valid, otherwise from the marker file mtime; `window=` plus `effective.deadline_grace` is the freshness bound. An `unknown` freshness does not fire `unwatched`; a marker proving a normal window expiry does not produce `unwatched`.
- **A-P5 — Probe remote unreachability**: a probe may add a `remote: {unreachable: true, reason: ...}` object to the snapshot schema; this is an additive field, not a private probe format. It yields `remote-unreachable` and never `DEAD`.
- **A-P6 — `spine.consistent` representation**: the normative field contract writes the three states as `true`/`false`/`unknown`; this slice fixes their JSON representation as the strings `"true"`/`"false"`/`"unknown"` so the field has one JSON type. A reader must not coerce `"false"` to a boolean.
- **A-P7 — Quickstart reconciliation**: the plan command requires a Phase 1 `quickstart.md`; slice A produces one with self-contained scenarios. The blocked-review finding 13's shared-`$TMP` lifecycle defect does not apply because every scenario owns and tears down its own fixture.
- **A-P8 — Slice identity**: the tracked 065a plan is retained as a historical artifact; 066 is the active execution basis for this run per the upstream brief. Feature status remains `Planned`; no transition is claimed.
