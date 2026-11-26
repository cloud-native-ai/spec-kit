# Implementation Plan: Team View Degradation Hardening（真实团队定义下的诚实呈现与降级语义）

**Branch**: `108-team-view-degradation` | **Date**: 2026-11-26 | **Spec**: `.specify/specs/108-team-view-degradation/requirements.md`
**Requirement → Feature**: `108-team-view-degradation` → Feature 027 Team Management
**Input**: Specification from `.specify/specs/108-team-view-degradation/requirements.md`

## Summary

Make `/speckit.team view` honest on real-world team definitions by amending its single reader `scripts/python/team-view.py` (no second reader, no second store, no team-schema change): run reports are recognized by a closed, parseable leading UTC timestamp grammar (five forms plus an optional `-<4hex>` conflict segment and a `report` / `stage` role word), every `runs/` file is classified as run report / auxiliary artifact / residue in a fixed order, latest is selected by parsed timestamp (never falling back to an older conforming report), and any residue (count + bounded examples) makes the latest determination unprovable → `report-recognition-uncertain` (exit 5). The other obligations land as presentation, not inference: missing `items.jsonl` carries its consequences, continuous-spine absence is judged by the declared pattern, binding/goal states carry the engine's precise reason plus sanctioned repair pointers, and a roster matrix without the `agent` column becomes `形态异常` with `roster_delta = 不可比对（not comparable）`. Degradation reasons stay the closed set `{engine-degraded, report-recognition-uncertain}` mapped to the unchanged exit-code set `0/2/3/4/5`; healthy outputs stay byte-identical to the baseline program of commit `54c6efa8c`. The rendering label vocabulary moves into this feature's contract face as its single live owner, and `103-team-view`'s data-model keeps only dated-record status.

## Technical Context

**Language/Version**: Python `>= 3.8`, standard library only (`pyproject.toml` `requires-python`; no new third-party import)
**Primary Dependencies**: none new — CPython stdlib, `pytest` and POSIX `bash` through the existing single test entry (RS-001…RS-003)
**Storage**: files only — the team archive under `.specify/teams/` read live per view; no cache, snapshot, index, registry or second store (FR-021)
**Testing**: `pytest` through `scripts/bash/run-tests.sh` (targeted set; parallel default). Measured on this host: the profile `python3` carries no pytest, the runner resolves with `SPECKIT_PYTHON=/usr/local/bin/python3` (pytest 8.4.2) — the implement stage MUST pass that override. This plan stage is docs-only and records `not-run-docs-only` in the stage-status row.
**Target Platform**: framework repository (sources under `scripts/`, `skills/`, `docs/`, `tests/`); `.specify/` copies are regenerated mirrors; downstream client projects receive the program and skill through `specify init` / refresh
**Project Type**: CLI / prompt-asset framework — one read-only program plus one skill and its docs
**Performance Goals**: one linear pass over each `runs/` directory; bounded examples in output; no resident process, no network
**Constraints**: healthy byte-fidelity on the FR-022 predicate (baseline `54c6efa8c` program vs amended program, same fixture, machine diff — SC-004); exit-code set unchanged `0/2/3/4/5` (FR-018); no new top-level envelope key (the existing 103 contract test pins the exact ten-key set — EP-007); single engine and single recognition entry (FR-006, FR-021); `goal-utils.py` zero modification (RS-004); report-naming owner and `team.md` schema untouched, any proposed shape change must ship migration or deterministic refusal (FR-023); no NEW mirror drift against the plan-stage baseline (rc 0, zero DIFF); docs page / skill / program three-surface consistency (FR-020); no push, no state-spine or feature-registry edit in this stage (stage brief)
**Scale/Scope**: 25 FR (FR-001…FR-025) / 8 SC (SC-001…SC-008); one engine amendment; four contracts; three new test files plus the four existing team-view test files as the regression surface; two doc surfaces and their mirrors; measured corpus 46 run files over 14 teams

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0 — one row per principle in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every delivered surface traces to an FR: contracts clause map in `feature-ref.md`; tests per SC (§ Project Structure); no untraced file |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 027 as slice row 108; this plan re-evaluates the feature list (no add / merge / split) and advances the slice row `Draft → Planned` with the parent detail's plan note (Feature Integration); `.specify/register.md` and the state spine are untouched (the stage brief's "registry" boundary, as adjudicated at clarify) |
| III | Intent-Driven Development | ✅ Pass | What/why precede how: `research.md` carries measured premises M1–M8 and resolved design points R-1…R-15; contracts are declarative; § Decision Tensions states why no load-bearing choice exists |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Three new test files are written before the engine edit (tasks order); every SC names its pinning test; closed sets get reverse samples (reason set, exit map, label closure) |
| V | AI Agent Integration Standards | ✅ Pass | No supported-agent roster, tier or config key changes; the view reads the team archive only |
| VI | Continuous Quality & Observability | ✅ Pass | Root cause fixed at the reader (A-3 keeps the naming owner unchanged); no `.bak` copies; guards can go red (source scans + behavioral fixtures) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Plan set produced from the validated spec; status ceiling `Planned` respected — this plan does not land `Implemented` |
| VIII | Code as the Single Source of Truth | ✅ Pass | Every behavior claim measured at plan time from code/probes (`research.md` M1–M8); owner facts cited from `skills/internal/create-team/SKILL.md` § Report contract, `references/operating-loops.md` § 8, `shared/definitions/anchor-definitions.md` § The Binding Record |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine amendment + one skill + one docs page + tests; no runtime, scheduler, store, cache, index or second format |
| X | Documentation Naming & Location Conventions | ✅ Pass | New contracts are lowercase kebab-case under the spec's `contracts/`; no reserved ALL-CAPS name; `docs/reference/commands/team.md` keeps its registered path |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: edits land in framework sources (`scripts/`, `skills/`) and ride `sync-mirrors.py`; the brief's no-registry-edit constraint is disclosed as a recorded deviation from create-plan's Feature Integration step (§ Re-check / stage record) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `run-tests.sh`, `sync-mirrors.py`, `regen-command-copies.py --check`, `validate-decision-tensions.py`, `pre-analyze-check.py` and the `goal-utils.py` read actions; no ad-hoc second tool |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Change Validation and Reliable Delivery via honest latest/uncertainty and repair pointers; claims rest on measured before/after (`research.md` M1–M7) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Label vocabulary single owner = `contracts/view-labels.contract.md`; reason set and exit map single owner = `contracts/team-view-program.contract.md`; 103 artifacts demoted by pointer and left untouched as dated records |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Degradation text adds reason, count, bounded examples and the next command in plain Chinese; owner paths are given for every pointer; established project vocabulary (slug / pattern / exit code) is used as-is |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The dispatch clause is carried; the stage records its anomaly line explicitly; in-passing corrections are disclosed at wrap-up |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | The only new directory is the spec's standard `contracts/`; fixtures stay in the existing `tests/fixtures/team_view_fixtures.py`; scratch lives under `.specify/.tmp/sdd-loop/tmp/team-view-degradation/` |
| XVIII | Grounded Naming | ✅ Pass | Names come from the spec's adjudicated vocabulary (`report-recognition-uncertain`, `不可比对`, `未识别`) and sibling files (`contracts/` naming follows 103/106/107) |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | Outputs carry counts, bounded examples, reasons and repair pointers; contract file names read as their subject (`report-recognition`, `degradation-semantics`, `view-labels`, `team-view-program`) |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Targeted set through the parallel-default runner; no full suite; baseline comparison by failure names; plan stage records `not-run-docs-only` |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `team-view.py` keeps `-h` / `--help` / `--version` and undeclared-option rejection with zero writes (existing pinning test + targeted re-check); no new script is added |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | Stage anchor and rules reloaded at each core step; verdicts recorded in the stage record (`test-evidence/plan-stage-2026-11-26.md`) |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | The change is AI-written → the AI review flow applies at the review stage (direct merge to trunk + AI review of merged history); this plan adds no review ledger |

**Gates Status**: ✅ All 23 gates pass — no Fail or Partial row; Complexity Tracking is N/A.

**Re-check after Phase 1**: 2026-11-26 — refreshed against the landed design artefacts (`data-model.md`, four contracts, `quickstart.md`, `feature-ref.md`, § Phase 1 summary). No row changed status. Feature Integration performed: slice row 108 `Draft → Planned`, parent 027 detail gains a dated plan note, parent status unchanged (`Ready for Review`, no status regression).

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`.*

N/A

本计划无承重决策：下列四类触发均不成立，逐类说明如下。

- 不可逆：不适用——本特性不迁移任何数据、不重写任何团队定义、不换契约载体；回滚就是 revert 本次提交，读取程序无写面（C-101），团队档案逐字节不动，命名 owner 与 `team.md` schema 不变（FR-023），没有需要重建或迁移的东西。
- 跨团队：不适用——退出码闭集 `0/2/3/4/5` 与 CLI 面逐字不变（C-103/C-104）；残留团队从 exit 0 变为 exit 5 是需求阶段已裁决的修正（FR-005 / FR-017，A-11 的具名增量），不是本计划的取舍；`--json` 信封是内部测试面（103 E9）且本计划不新增顶层键（C-105）；`goal-utils.py` 零修改（RS-004）。计划唯一落点选择（降级原因复用既有 `errors[]` 以 `code` 区分）同时满足「既有消费方不被迫改动」与「原因可结构化区分」，两极同向，不构成二选一。
- 高爆炸半径：不适用——一次 view 失败只影响本次查看输出；程序不写盘、不派发席位、不登记 run line，故障面不出本特性边界。
- 与宪法原则相关：不适用——设计遵守而非取舍相关 MUST：单一事实源、测试义务、零新机制均按既有原则落地，没有一处以放宽某条 MUST 换取方案成立。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/108-team-view-degradation/
├── plan.md                        # This file (/speckit.plan command output)
├── research.md                    # Phase 0 output (standalone: measurements M1–M8 + design points R-1…R-15)
├── data-model.md                  # Phase 1 output (classification / presentation model)
├── contracts/                     # Phase 1 output (4 contracts — this feature's live contract face)
│   ├── team-view-program.contract.md
│   ├── report-recognition.contract.md
│   ├── presentation.contract.md
│   └── view-labels.contract.md
├── quickstart.md                  # Phase 1 output (scenario set, per-example premises)
├── feature-ref.md                 # Phase 1 output (Feature 027 binding + delivery surface)
├── checklists/                    # requirements-quality checklist
├── test-evidence/                 # gate captures, plan-stage record, workspace signatures
├── tasks.md                       # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md                # Implementation output (/speckit.implement — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
scripts/python/team-view.py                        # single engine: closed timestamp grammar, file classifier, latest selection, degradation reasons, presentation obligations
skills/internal/view-team/SKILL.md                 # error-navigation row 5 (reasons) + additive-presentation wording
docs/reference/commands/team.md                    # View Mode: recognition + degradation reasons/exit codes + repair pointers
tests/unit/test_team_view_report_recognition.py    # NEW: grammar, classifier, latest, residue bound, uncertainty predicate
tests/contract/test_team_view_degradation_contract.py # NEW: closed reasons/exit map, single entry, envelope keys, label closure, three-surface consistency
tests/integration/test_team_view_degradation.py    # NEW: production replica, corpus replica, residue-only, degraded definition, healthy fidelity, overview, snapshot
.specify/scripts/python/team-view.py               # mirror of the engine (regenerated, never hand-edited)
.specify/skills/internal/view-team/SKILL.md        # mirror of the skill (regenerated, never hand-edited)
```

**Structure Decision**: extends the existing 103 surface rather than adding a new layer — the report classifier, latest selection and degradation reasons all live inside the one reader `scripts/python/team-view.py`; the skill and the docs page gain pointer-shaped text; the four contracts become the single live contract face for the amended program, the report-recognition rules, the presentation obligations and the rendering labels. No new top-level directory, no new fixture directory (the existing `tests/fixtures/team_view_fixtures.py` builder already writes arbitrary `runs/` names), no `templates/commands/` change (so per-tool command copies are unaffected).

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/team-view.py` | `.specify/scripts/python/team-view.py` | `python3 scripts/python/sync-mirrors.py --check` — no NEW drift against the plan-stage baseline (measured rc 0, zero DIFF); the pair lands byte-identically |
| `skills/internal/view-team/SKILL.md` | `.specify/skills/internal/view-team/SKILL.md` | same mirror check — no NEW drift on this pair |
| no `templates/commands/` change | per-tool command copies | `python3 scripts/python/regen-command-copies.py --check` rc 0 (plan-stage baseline: `OK: all per-tool command copies match the source templates.`) |
| `docs/reference/commands/team.md` | none — `docs/` is this project's development documentation, never shipped | no mirror duty |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The existing CPython `>=3.8` stdlib + pytest + POSIX bash stack carries the grammar, classifier and all new tests with zero new third-party imports | `pyproject.toml` (`requires-python = ">=3.8"`, `pytest`); `scripts/bash/run-tests.sh`; measured host: `/usr/local/bin/python3` = pytest 8.4.2, profile `python3` has none | verified | — |
| EP-002 | The `goal-utils.py` read actions (`binding` / `list` / `targets --list`) are the only source of binding/anchor facts, and the engine already names why a binding is unreadable | plan probe 2026-11-26: `binding team no-binding-team` → exit 2, `binding-missing: … carries no binding block; … (owner / owner_id / origin)`; the partial-keys message names `owner_id, origin`; `--help` action set unchanged (RS-004) | verified | — |
| EP-003 | A healthy fixture satisfying the completed FR-022 predicate (three-key binding, compact report names, zero auxiliary artifacts, zero residue, `agent` column, `goal` absent or slug-form, `items.jsonl` present with at least one line, all three continuous-spine files present) is buildable with the existing fixture helper (`reports=` / `items_lines=` / `spine=` parameters), and the baseline program materialized from `54c6efa8c` runs beside the current siblings and is byte-identical to the current program on that fixture | plan probe under `.specify/.tmp/sdd-loop/tmp/team-view-degradation/`: both runs exit 0, stdout diff lines = 0, fixture snapshot unchanged (3 files; builder-default fixture without ledger/spine — this plan-time reading covers the baseline-vs-current equality only; the amended-vs-baseline reading is re-taken on the completed-predicate fixture by S-1); `git cat-file -e 54c6efa8c` ok; sha256 of `git show 54c6efa8c:scripts/python/team-view.py` equals the current file (`81fad3f9…`) | verified | — |
| EP-004 | The in-repo corpus still carries the 46-file composition: 41 reports (28 compact-conforming + 13 parseable-non-conforming report-style), 3 auxiliary artifacts, 2 residue, over 14 teams | plan measurement 2026-11-26 over `.specify/teams/*/runs/` (research.md M1); the three all-non-conforming teams hold 5 / 7 / 1 reports | verified | — |
| EP-005 | The `-<4hex>-report.md` / `-<4hex>-stage.md` forms exist only in the user-supplied production evidence, not in this repository; their fixtures are synthesized from A-12, not from the live corpus | corpus name scan: zero four-hex report-or-stage name matches (M1); requirements `生产证据` records `…-93cc-stage.md` | verified | — |
| EP-006 | The current program misreports real non-conforming histories: three teams render `运行报告: 为空` with reports present and `最近报告: 未记录`, all at exit 0; a residue-only fixture does the same | plan probe: `team-view.py viz-skill-arena` and `draw-two-layer-structure` → `运行报告: 为空`, latest `未记录`, exit 0; residue-only fixture → same | verified | — |
| EP-007 | The existing 103 contract test pins the `--json` top-level key set exactly, so the amendment must not add a top-level envelope key | `tests/contract/test_team_view_program_contract.py` (`ENVELOPE_KEYS`, `assert set(payload) == ENVELOPE_KEYS` at two sites) | verified | — |
| EP-008 | The mirror and per-tool-copy toolchain is at a green baseline, so the mirror criterion is "no NEW drift" rather than an absolute pass | plan measurement: `sync-mirrors.py --check` rc 0 zero DIFF; `regen-command-copies.py --check` prints `OK: all per-tool command copies match the source templates.` | verified | — |
| EP-009 | The declared dependency Feature 027 carries no `blocked` / `deferred` / `partial` verification row and no deferred list, so the inherited-blocker extraction set is empty | `.specify/features/027-team-management.md` carries no `## Deferred` section; `.specify/specs/103-team-view/verification.md` has `deferred_tasks=` empty and every status row `pass` (measured 2026-11-26) | verified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `027`: `.specify/features/027-team-management.md`, `.specify/specs/103-team-view/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | The declared dependency's extraction set is empty: Feature 027's detail has no `## Deferred` section, and `103-team-view/verification.md` carries no `blocked` / `deferred` / `partial` status row and an empty `deferred_tasks=` (EP-009). The 103 view surface is consumed as the live predecessor contract, superseded only where the 108 contracts say so. |

## Complexity Tracking

N/A — no Constitution Check row is Fail or Partial.

## Phase 1: Design Artifacts Summary

Filled after the artifacts landed (counts read from the written files):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 10 entities (C1–C10), 10 invariants |
| Contracts | [`contracts/`](./contracts/) | 4 files, 35 clauses: `team-view-program.contract.md` (C-101…C-109), `report-recognition.contract.md` (C-201…C-208), `presentation.contract.md` (C-301…C-309), `view-labels.contract.md` (C-401…C-409) |
| Quickstart | [`quickstart.md`](./quickstart.md) | 8 scenarios (S-0 executed, S-1…S-7 test-pinned with per-example premises) |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 027 binding, delivery surface, FR→surface map, supersession map, handoff |
| Research | [`research.md`](./research.md) | 8 measurements (M1–M8) + 15 resolved design points (R-1…R-15) + re-measure list |
