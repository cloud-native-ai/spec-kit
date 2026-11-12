# Implementation Plan: Anchor / Goal Realignment

**Branch**: `101-anchor-goal-realignment` | **Date**: 2026-11-12 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `101-anchor-goal-realignment` → Feature 101 Anchor / Goal Realignment
**Input**: Specification from `.specify/specs/101-anchor-goal-realignment/requirements.md` (71 FR / 10 SC)

## Summary

Invert the project's two top-level concepts and split the command surface that currently conflates them.
**Anchor** becomes the project-level, long-horizon objective (`.specify/anchoring/<slug>/anchor.md`) and
`/speckit.anchor` takes over the old `/speckit.goal`'s seven modes as the sole authoring entry; **Goal**
drops to action-level, short-horizon practical guidance (`.specify/goals/<slug>/goal.md`) with four modes
and a named refusal for the Anchor-only ones. The single engine `goal-utils.py` is **extended, not
duplicated**: filenames resolve from a layer (`anchor` / `goals` / `teams`), `--scope` becomes a closed
four-member set, and two new action groups appear (action-level Goal, and an independent
`cleanup --check|--apply`). Finally the 14 existing `.specify/anchoring/` entries are classified (9 anchor /
3 action-goal / 2 obsolete), migrated or archived archive-not-delete with per-entry receipts, and all
16 team bindings are renamed `goal_slug` → `anchor_slug` with two dangling bindings disposed.

The technical approach is deliberately conservative: zero new dependencies, zero new binaries, zero
deletions, and every dated record byte-identical to `d7c9da7a3`. Convergence is made decidable by a
measured residue baseline (C1–C4 = 26 line-hits; C5 = 16 lines, 11 of them in the 9 retained anchors;
C6 = 40 line-hits; C7 = 3 index rows — `research.md` §5) and by contract tests that turn red on the old
semantics.

## Technical Context

**Language/Version**: Python `>=3.8` (declared in `pyproject.toml`; measured interpreter 3.11.11)
**Primary Dependencies**: none added — `typer` / `rich` / `httpx` / `platformdirs` / `readchar` /
`truststore` are unchanged and untouched by this feature; `pytest` 8.4.2 for tests
**Storage**: files — markdown definitions (`.specify/anchoring/**`, `.specify/goals/**`,
`.specify/teams/**`), JSON receipts co-located with each acted entry, `.specify/archive/anchoring/**` as
the archival destination
**Testing**: `pytest` through `scripts/bash/run-tests.sh` only (parallel default, `-n <effective>
--dist load`); markers `contract` / `integration` / `serial`; Tests Mode **ON**
**Target Platform**: CPython on the platforms the CLI already supports; POSIX shell for scripts
**Project Type**: code generator / prompt framework (`templates/`, `skills/`, `shared/`, `scripts/`, `src/`)
**Performance Goals**: not a throughput feature — the cleanup acts on 14 entries and ~20 team files; a
single `cleanup --apply` is expected to finish in seconds
**Constraints**: no new dependency; no second engine or writer; archive-not-delete; dated records never
rewritten; every mirror pair delivered in the same change
**Scale/Scope**: 14 anchor entries (9 / 3 / 2), 20 team definitions (16 bound, 4 unbound), 71 FR, 6 work
packages, 4 contract files (49 clauses)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0, in declaration order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design decision cites an FR; this plan set is the stage output of the declared workflow |
| II | Feature-Centric Development | ✅ Pass | Feature 101 registered as a new feature (not a 041 extension); 041 keeps its status and gains only a successor note |
| III | Intent-Driven Development | ✅ Pass | Intent captured as two named concepts with one owner each — `anchor-definitions.md` (new) / `goal-definitions.md` (rewritten), FR-002 / FR-004 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Four contract files / 49 clauses (`contracts/` C-1…C-49); Tests Mode ON; every FR-062…FR-070 guard named in § Testing Strategy |
| V | AI Agent Integration Standards | ✅ Pass | `/speckit.anchor` ships through the existing mirror model to the four per-tool copy directories plus a skill; no tool-specific special-casing |
| VI | Continuous Quality & Observability | ✅ Pass | Probe object/binding for `/speckit.anchor` (FR-014 / FR-055); measured readings go to `test-evidence/` (FR-071) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This file is the plan stage; decomposition, fence and ceiling below, `tasks.md` deliberately not produced here |
| VIII | Code as the Single Source of Truth | ✅ Pass | Design facts were read from code, not memory: `goal-utils.py` 0.0.22 flags, `DEFINITION_FILENAME`, `--scope` members, `MIGRATE_STATIC_POINTERS` (`src/specify_cli/__init__.py:3367`) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine extended; no new binary, no new runtime, no new dependency; cleanup is an engine action group, not a tool |
| X | Documentation Naming & Location Conventions | ✅ Pass | `docs/reference/commands/anchor.md` (new) and `goal.md` (rewritten) follow the per-command reference convention |
| XI | Dogfooding (Self-Application) | ✅ Pass | The framework's own anchor archive is the cleanup subject; no new machinery is introduced for it |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | The existing `goal-utils.py` engine is reused and extended; no throwaway script is authored for migration |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Convergence guards (residue scan, store purity, binding resolution) make the harness decidable after the rename |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Anchor owner holds the shared binding/lifecycle/scope owner; every other surface cites it (C-24 pointer rule, FR-030) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Refusals name the next command; glossary owner rewritten (FR-051); reader baseline recorded for SC-010 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Conflict → exit 4 naming both candidates; I5 half-state never silently repaired; three requirements corrections declared as `PLAN-EDIT:` |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `.specify/goals/` is a new tracked definition store: registered in `framework-map.md` (FR-050) with its owner, not a runtime-ignored directory |
| XVIII | Grounded Naming | ✅ Pass | Names follow existing siblings (`anchoring/`, `anchor.md`, `anchor_slug`); FR-009 disambiguates Anchor / anchoring archive / Re-Anchoring |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The Goal store mirrors the anchor store's shape (one directory per definition, one file per slug); no new navigation dimension |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Runs go through the parallel runner default; targeted suites per package; serial-marked tests excluded; GATE-1 compares by failing-id name |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `-h` / `--help` / `--version` and undeclared-option rejection retained (FR-034); new actions declare exit codes (C-30) |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | `re-anchoring-definitions.md` keeps the runtime discipline and only re-points the entity reference (FR-053) |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | Implement/review stage reviews per authorship; this plan adds no authoring surface of its own |

**Gates Status**: ✅ All gates pass — no violation, no Complexity Tracking row.

**Re-check after Phase 1**: 2026-11-12 — table re-read against the landed design artifacts
(`data-model.md` E-1…E-11, `contracts/` C-1…C-49): unchanged. The only row that gained a concrete
carrier is IV (the six contract surfaces and the named guard tests exist on disk).

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md`.*

### T-001 — extend the one engine with a layer parameter, instead of adding a second engine for the Goal store

- **decision**: `goal-utils.py` keeps the sole-writer role and resolves the definition filename and
  summary directory **from the layer** (`anchor` / `goals` / `teams`); the Goal store's actions are a new
  action group inside the same executable (C-23, C-26, C-28).
- **antithesis**: add `goal-store-utils.py` that owns `.specify/goals/**` while `goal-utils.py` keeps the
  anchor archive; each file stays small and neither has to grow a layer abstraction — but then two
  writers, two `--help` surfaces, two exit-code tables and two audit targets must be kept in step forever.
- **binding_constraints**:
  - pole_a: 定义文件只有一个写者，违反必须由契约测试转红（FR-028 / FR-065 / SC-006）。
  - pole_b: 引擎已经承担 20 个动作与三个消费者（`sdd-route.py`、`concurrency-check.py`、`logical-framework.py`）；再加一套引擎会把「谁写档案」重新变成文档解释问题。
- **discriminating_evidence**: 在夹具树上创建 `anchor` 与 `goal` 同 slug 的两个定义，断言写入路径分属
  `.specify/anchoring/` 与 `.specify/goals/` 且来自同一进程的同一动作组；结果二值：一个写者 / 两个写者。
- **expected_sacrifice**: SC-006 Source ↓ 引擎签名面变大（动作组 + 层参数），单文件复杂度上升；`_sig_guard` 与动作分派表
  的维护成本由一次承担换取长期单写者（C-34）。
- **revision_trigger**: 层参数使任一既有动作对既有层产生行为变化 ≥2 次（094 既有契约转红）→ 重开，改为
  两个引擎并显式声明「锚点档案写者」与「Goal 存档写者」各自的守卫。
- **tension_id**: T-001

### T-002 — split the command surface, instead of one command with a layer flag

- **decision**: `/speckit.anchor` (seven modes) and `/speckit.goal` (four modes) are two commands with two
  canonical templates; the Goal command refuses Anchor-only modes by name (C-14, C-20).
- **antithesis**: keep one `/speckit.goal` and add a `--layer anchor|goal` switch; when a user only ever
  authors one kind of object per session and the skill already knows the layer, one entry point is simpler
  — no duplicate glossary preamble, no second probe, no cross-command pointer obligation.
- **binding_constraints**:
  - pole_a: 用户必须能从命令名判断自己在写项目级远期目标还是本周行动，且拒绝必须指路而不是静默降级。
  - pole_b: 两个命令共享同一引擎与同一绑定/生命周期 owner，不能因拆分产生第二套 schema 或第二套模式语义。
- **discriminating_evidence**: 对 `/speckit.goal targets` 做子进程调用，读退出码、stderr 与写入集合；结果
  二值：具名拒绝且零写入 / 任意形式的接受或静默回退。
- **expected_sacrifice**: SC-002 Source ↓ 命令面从一处变两处，参考页、flow-class 台账行、探针登记与四处 per-tool 副本都要
  成对维护（FR-054 / FR-055 / FR-070）。
- **revision_trigger**: 出现「用户按旧习惯调用 `/speckit.goal` 写锚点」的实测事故 ≥2 次且拒绝文本未能纠正
  → 重开，评估单命令 + 强制 `--layer` 并保留具名拒绝文案。
- **tension_id**: T-002

### T-003 — archive obsolete entries, instead of deleting them

- **decision**: obsolete entries move to `.specify/archive/anchoring/<slug>/` with a receipt carrying
  `delete_policy: archive-not-delete`; removal of the source is the last phase of a move (C-37, C-42).
- **antithesis**: `git rm` the two obsolete entries and rely on history; when a definition is superseded
  and git already keeps every byte, keeping a second copy looks like duplication — and history is an
  unambiguous backup.
- **binding_constraints**:
  - pole_a: 任何动作不得删除定义数据；可复核的「零丢失」必须以回执与摘要相等判定（SC-004 / FR-042 / FR-043）。
  - pole_b: 归档目的地必须与活档案物理分离，否则「档案纯度」不可判定（SC-003 / FR-064）。
- **discriminating_evidence**: 在夹具上对同一归档动作跑两次并比对 `git status --porcelain` 与回执计数；
  结果二值：零新增 diff 与零重复回执 / 任一增量。
- **expected_sacrifice**: SC-004 Source ↓ 仓库里多出一棵归档树与逐条回执，检索时需要用 `research.md` §5 的排除集把它们
  与活面分开。
- **revision_trigger**: 归档树在两次以上评审中被读成活定义（读者或检索混淆）→ 重开，改为
  `archive/anchoring/<slug>/` 下加 `ARCHIVED` 标记文件并在 framework-map 中显式标注不可编辑。
- **tension_id**: T-003

### T-004 — let the retired scope member and the retired modes fail, instead of aliasing them

- **decision**: `--scope goal` and the singular `--scope team` are invalid choices (exit 2); the four
  Anchor-only modes on `/speckit.goal` fail by name; neither is silently mapped to its successor (C-24, C-14).
- **antithesis**: accept `goal` as an alias of `anchor` for one release so old scripts keep working; when
  downstream projects call the engine directly, a silent alias avoids a breaking change — at the cost of
  keeping the inverted semantics reachable by an old word.
- **binding_constraints**:
  - pole_a: 旧词不得继续指向新概念，否则「Goal 是项目级」的读法在参数面上存活（FR-005 / FR-030）。
  - pole_b: 破坏性改名必须有可诊断的失败：错误信息要指出新取值，而不是一个裸的 argparse 报错。
- **discriminating_evidence**: 用 `--scope goal` 与 `/speckit.goal targets` 各调用一次，读退出码与 stderr；
  结果二值：exit 2 且点名 `anchor` / 任意形式的成功。
- **expected_sacrifice**: SC-002 Source ↓ 直接调用引擎的下游脚本会一次性失效，必须自行改名（本仓的调用点在本特性内一并
  修好，见 C-32 消费者表）。
- **revision_trigger**: 出现仓外下游因别名缺失而无法迁移的实际阻塞 ≥2 次 → 重开，增加一个带弃用警告的
  过渡取值并在其后的特性中移除。
- **tension_id**: T-004

## Project Structure

### Documentation (this spec)

```text
.specify/specs/101-anchor-goal-realignment/
├── plan.md                          # This file
├── research.md                      # Phase 0 output — baseline, 14-row classification, rulings R-01…R-15
├── classification.json              # Plan artifact: the 14 entry verdicts + 7 team dispositions (C-36 input)
├── data-model.md                    # Phase 1 output — E-1…E-11
├── quickstart.md                    # Phase 1 output — S-0…S-8
├── contracts/
│   ├── anchor-command.contract.md   # C-1…C-12
│   ├── goal-command.contract.md     # C-13…C-22
│   ├── goal-engine.contract.md      # C-23…C-35
│   └── migration-cleanup.contract.md # C-36…C-49
├── feature-ref.md                   # Phase 1 output — binding, delivery surface, FR→contract / SC→measurement maps
├── test-evidence/
│   ├── plan-baseline-2026-11-12.txt
│   ├── live-semantic-scan-baseline-2026-11-12.txt
│   ├── requirements-anchor-inventory-2026-11-12.md
│   └── clarify-2026-11-12.md
├── tasks.md                         # Phase 2 (/speckit.tasks — not produced here)
└── verification.md                  # Implement close — one SC status row per criterion + smoke record
```

### Source Code (repository root)

```text
shared/definitions/                  # Concept owners
├── anchor-definitions.md            # NEW — Anchor owner + shared binding/lifecycle + archive-layer/scope owner
├── goal-definitions.md              # REWRITTEN — action-level Goal owner
├── framework-map.md                 # four store rows
├── sdd-routing-definitions.md       # hierarchy: Anchor on top, Goal out of it
├── re-anchoring-definitions.md      # entity reference → Anchor owner
├── flow-class-definitions.md        # `/speckit.anchor` row, `/speckit.goal` row
├── probe-definitions.md             # `/speckit.anchor` wrap-up probe
└── non-disposable-definitions.md    # member set update
shared/patterns/interview-pattern.md # anchor authoring pointer
skills/internal/
├── manage-anchor/                   # NEW — seven-mode skill
├── manage-goal/                     # REWRITTEN — four-mode skill
└── create-team/ improve-team/ run-team/ summarize-project/   # Anchor terminology + team-domain paths
skills/external/
├── sdd-project-setup/               # archive check instead of the retired path
└── sdd-house-keeping/               # archive check instead of the retired path
templates/commands/
├── anchor.md                        # NEW — canonical seven-mode template
└── goal.md                          # REWRITTEN — canonical four-mode template
scripts/python/
├── goal-utils.py                    # layer parameter, two new action groups, four-member --scope
├── sdd-route.py concurrency-check.py                          # consumers (scope projection, layout probe)
skills/external/sdd-project-setup/scripts/logical-framework.py # consumer (Anchor paths/labels)
skills/external/sdd-house-keeping/scripts/logical-framework.py # consumer (Anchor paths/labels)
skills/internal/create-team/scripts/build-summary-input.py     # consumer (summary input paths)
src/specify_cli/__init__.py          # MIGRATE_STATIC_POINTERS ownerCommand + command list
docs/reference/commands/
├── anchor.md                        # NEW reference page
└── goal.md                          # REWRITTEN reference page
tests/
├── contract/                        # one guard per FR-062…FR-067 / FR-070 + migration suite
├── integration/                     # convergence test on a fixture tree
└── fixtures/anchor-goal-realignment/# classification × 14, teams × 20, protected-path fixture
.claude/commands/ .github/prompts/ .qoder/commands/ .opencode/command/   # per-tool copies (generated)
.specify/                            # runtime mirrors of every file above + the three definition stores
.specify/anchoring/ .specify/goals/ .specify/teams/ .specify/archive/anchoring/   # the stores acted on
```

**Structure Decision**: this feature keeps the repository's existing generator/framework shape and adds no
top-level directory. `.specify/goals/` is a **new second definition store beside the existing
`.specify/anchoring/`**, registered in `framework-map.md` as a documented directory (Constitution XVII) and
written only by the engine. The command templates fan out through the existing per-tool copy model;
`.specify/templates/commands/` stays retired.

### Mirror Obligations

Baseline measured **before** the edit (2026-11-12): `python3 scripts/python/sync-mirrors.py --check` → exit
0, `shared/ == .specify/shared/ (113 files, byte-identical)`; `python3 scripts/python/regen-command-copies.py
--check` → exit 0, `OK: all per-tool command copies match the source templates`. Criterion below is
therefore **"no NEW drift on the pairs this feature touches"**, never a bare exit code.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/*.md` (8 files) | `.specify/shared/definitions/` (same 8 files) | `sync-mirrors.py --check` reports no NEW DIFF for `shared/` |
| `shared/patterns/interview-pattern.md` | `.specify/shared/patterns/` | same check, same pair |
| `skills/internal/manage-anchor/**`, `skills/internal/manage-goal/**` | `.specify/skills/internal/manage-anchor/**`, `…/manage-goal/**` | `sync-mirrors.py --check`, `skills/` pair, no NEW DIFF |
| `skills/external/sdd-project-setup/**`, `sdd-house-keeping/**`, `create-team/**`, `improve-team/**`, `run-team/**`, `summarize-project/**` | `.specify/skills/external/…` (same trees) | same check, `skills/` pair |
| `scripts/python/goal-utils.py` (+ 4 consumer scripts) | `.specify/scripts/python/…` | same check, `scripts/` pair |
| `templates/commands/anchor.md` (new) | `.claude/commands/speckit.anchor.md`; `.github/prompts/speckit.anchor.prompt.md`; `.qoder/commands/speckit.anchor.md`; `.opencode/command/speckit.anchor.md` — via `regen-command-copies.py`; **no** `.specify/templates/commands/` mirror (retired) | `regen-command-copies.py --check` exits 0 and the four copies carry the seven-mode hint |
| `templates/commands/goal.md` (rewritten) | the same four copies for `/speckit.goal` | same check; copies carry the four-mode hint |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` plus the standard library is sufficient for every engine action, migration and guard this feature adds | `pyproject.toml` `requires-python`; measured interpreter 3.11.11; `test-evidence/plan-baseline-2026-11-12.txt` records zero new imports | verified | — |
| EP-002 | `scripts/bash/run-tests.sh` can execute the contract/integration markers on this tree, and the suite already carries pre-existing failures that MUST be compared by failing-id name | pytest 8.4.2 measured; markers registered in `pyproject.toml`; 094's recorded baseline of pre-existing ids; the 101 baseline is captured at implement entry (Single-Run Evidence) | verified | — |
| EP-003 | The existing engine `goal-utils.py` (0.0.22) exposes the flags and action surface this contract cites, so extension is additive | `goal-utils.py --help` and per-action `--help` readings in `test-evidence/plan-baseline-2026-11-12.txt`; `C-26`/`C-27`/`C-28` name measured flags | verified | — |
| EP-004 | The mirror, copy-regeneration and flow-class engines are green **before** the edit, so "no NEW drift" is a decidable criterion | `sync-mirrors.py --check` exit 0 (113 files byte-identical); `regen-command-copies.py --check` exit 0; flow-class reading 89 units / 0 findings | verified | — |
| EP-005 | `git` can compare protected paths against the pre-feature commit, so the dated-record guard is measurable | `git --version` 2.43.5; `git cat-file -e d7c9da7a3^{commit}` succeeds; per-file `hash-object` counts recorded in `test-evidence/plan-baseline-2026-11-12.txt` | verified | — |
| EP-006 | The documentation site builds on this tree, so SC-008's docs-build limb can be read as a pass/fail | `hugo` v0.141.0 exits **1** with `.Site.Language.Locale: can't evaluate field Locale in type *langs.Language` — a pre-existing condition unrelated to this feature | falsified | fallback — SC-008's docs-build limb reports `not-evaluated` with that measurement attached; the other three limbs (page existence, flow-class row, probe face) carry the criterion. Re-measuring is a later feature's job, not silently waived |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:

- `037`: `.specify/features/037-docs-command.md`, `.specify/specs/037-goal-registry/verification.md`
- `038`: `.specify/features/038-evidence-infrastructure.md`, `.specify/specs/038-goal-target/verification.md`
- `042`: `.specify/features/042-interview-mode.md`, `.specify/specs/042-goal-team-creation/verification.md`
- `074`: `.specify/features/074-goal-team-sdd-unification.md`, `.specify/specs/074-goal-team-sdd-unification/verification.md`
- `085`: `.specify/features/085-sdd-temporary-goal-team.md`, `.specify/specs/085-sdd-temporary-goal-team/verification.md`
- `094`: `.specify/features/094-goal-team-parallel.md`, `.specify/specs/094-goal-team-parallel/verification.md`

Extraction over those artifacts (2026-11-12) yields exactly four records: two `deferred_tasks` rows whose
value is literally `none`, and two `094` `partial` status rows. `037` / `074` / `085` contribute no record
(no `blocked`/`deferred`/`partial` status line and no non-empty `deferred_tasks=`).

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `038:deferred_tasks` | resolved | — | — | `038-goal-target/verification.md` records `deferred_tasks=none`; 038's Targets surface is re-asserted under the new layers by this feature's convergence suite, so nothing was deferred into it |
| 2 | `042:deferred_tasks` | resolved | — | — | `042-goal-team-creation/verification.md` records `deferred_tasks=none  # 33/33 closed, no [~]`; the team-creation path this feature rewrites carries no inherited deferred work |
| 3 | `094:SC-001_status` | not-applicable | — | — | 094's own ruling R2 (2026-11-09) re-scoped the criterion and forbids authoring its missing fixture guard; this feature rewrites the command surface but does not reopen 094's criterion, and a delegated pass would be delegated evidence, not its own |
| 4 | `094:SC-010_status` | not-applicable | — | — | 094's recorded unblock condition requires a user ruling narrowing "whole contract suite green"; this feature's GATE-1 compares the failing-id **set by name** against its own entry baseline and never claims whole-suite green |

## Complexity Tracking

N/A — the Constitution Check has no violation, so there is no row to justify.

## Phase 0: Research Review

`research.md` is a standalone file (≈200 lines, exceeds the inline threshold) and carries the measured
baseline. Its load-bearing outputs:

1. **Baseline** (`test-evidence/plan-baseline-2026-11-12.txt`): interpreter 3.11.11, pytest 8.4.2, git
   2.43.5, engine 0.0.22, mirror checks exit 0, flow-class 89 units / 0 findings / floor 39, protected
   roots enumerated, protected baseline `d7c9da7a3`, HEAD `d3f85f059`.
2. **Classification** — 14 rows decided at plan with rule id and evidence; the deviation from the A-5
   provisional baseline is **none** (9 anchor / 3 action-goal / 2 obsolete; Targets ledger recorded).
   `classification.json` is the machine-readable carrier and the engine's only classification input.
3. **Team dispositions** — R3 for `088-reporting-dogfood`, `091-auto-git-closeout`,
   `085-sdd-temporary-goal-team`, `post-refactor-mechanism-integrity`, `draw-diagram-interactive`,
   `demo-seat-dispatch`; **R2** for `viz-skill-arena` (create `visualization-skill-selection` through
   the engine `migrate` action). No team qualifies for R1. `091-auto-git-closeout` was first recorded
   `already-satisfied`; the checklist repair corrected it to `apply` — it already carries
   `lifecycle_state: archived` but still carries its binding line and has no receipt, and R3's terminal
   state (archived + binding removed + `disposition-receipt.json`) is what the criterion reads.
4. **Live-surface roots** — the SC-001 declaration (directories, files, closed exclusion list) and the
   class definitions C1–C7 with the narrowed baseline patterns; baseline readings
   `C1 4 · C2 0 · C3 7 · C4 15 · total 26`, plus `C5 16 / C6 40 / C7 3` from the checklist repair
   (`test-evidence/checklist-repair-residue-baseline-2026-11-12.txt`).
5. **Rulings R-01…R-15** — each gap the research found and the reading it closed it with (mirrored in
   `feature-ref.md` §5).
6. **Not evaluated** — SC-010 reader restatement, SC-007 idempotency, SC-004 receipts: the mechanisms do
   not exist before implement.

Four requirements corrections were made at this stage and are declared in `requirements.md` as
`PLAN-EDIT:` items: FR-011 / FR-028 / SC-006 scope the single-writer invariant to **definition files**
(`summary/**` is a derived tree already written by `build-summary-input.py`); FR-061 / SC-009 scope the
`.specify/archive/**` equality assertion to **baseline-existing entries**, because FR-041 mandates creating
the new `.specify/archive/anchoring/**` subtree in the same change. Validator re-run: 0 error / 0 warning.

The checklist gate's round-1 repair then closed eleven findings (F-1…F-11) across requirements, contracts,
data model, research, tasks and `classification.json`; each resolution, its owner and its evidence are
recorded in `notes/checklist-repair.md`, and the affected requirement edits appear in `requirements.md`
§ Checklist-round-1 corrections.

## Decomposition & Ceiling

Six work packages, ordered by dependency. Each names its scope, inputs, outputs, write territory and the
fence it obeys. Territories are **file-level** where two packages share a directory.

| WP | Scope | Inputs | Outputs | Write territory | Depends on |
|----|-------|--------|---------|-----------------|-----------|
| **WP-01** | Concept owners + engine | FR-001…FR-009, FR-028…FR-034; `contracts/goal-engine.contract.md`; T-001/T-004 | `anchor-definitions.md` (new), `goal-definitions.md` (rewritten), engine layer parameter + two action groups + four-member `--scope`, engine user-facing hints repointed to `/speckit.anchor` and `run-checks` JSON key `anchor_slug`, consumer updates | `shared/definitions/anchor-definitions.md`, `shared/definitions/goal-definitions.md`, `scripts/python/goal-utils.py`, `scripts/python/sdd-route.py`, `scripts/python/concurrency-check.py`, `skills/external/sdd-project-setup/scripts/logical-framework.py`, `skills/external/sdd-house-keeping/scripts/logical-framework.py`, `skills/internal/create-team/scripts/build-summary-input.py`, `src/specify_cli/__init__.py`, + their `.specify/` mirrors | — |
| **WP-02** | Command surface | FR-010…FR-027; `contracts/anchor-command.contract.md`; `contracts/goal-command.contract.md` | `templates/commands/anchor.md` (new), `goal.md` (rewritten), `manage-anchor` skill (new), `manage-goal` skill (rewritten), four per-tool copies, two reference pages | `templates/commands/anchor.md`, `templates/commands/goal.md`, `skills/internal/manage-anchor/**`, `skills/internal/manage-goal/**`, the four per-tool copy directories, `docs/reference/commands/anchor.md`, `docs/reference/commands/goal.md`, + mirrors | WP-01 (mode semantics) |
| **WP-03** | Live-surface convergence | FR-050…FR-060; `research.md` §5; T-002 | framework-map, glossary, routing hierarchy, re-anchoring, flow-class, probe, non-disposable, interview pattern, setup / house-keeping, four team-domain skills, tutorials, and the three live feature-index rows (C7: 027 / 041 / 094) plus the 094 detail-page successor note | the remaining `shared/definitions/*.md` (6 files), `shared/patterns/interview-pattern.md`, `skills/external/{sdd-project-setup,sdd-house-keeping}/**`, `skills/internal/{create-team,improve-team,run-team,summarize-project}/**`, `docs/tutorials/**`, `.specify/features.md` (three rows), `.specify/features/094-goal-team-parallel.md` (successor note only), + mirrors | WP-01, WP-02 |
| **WP-04** | Cleanup, migration, dispositions | FR-035…FR-049; `classification.json`; `contracts/migration-cleanup.contract.md`; T-003 | 9 renames + anchor body normalization (A-N-1…A-N-4), 3 migrations, 2 archival moves with receipts, 16 structural renames, team body normalization, 6 R3 dispositions + 1 R2 anchor | `.specify/anchoring/**`, `.specify/goals/**` (new), `.specify/archive/anchoring/**`, `.specify/teams/*/team.md` + receipt files, no other file | WP-01 (engine actions) |
| **WP-05** | Guards and evidence | FR-061…FR-071; `contracts/` C-31/C-41/C-49 | contract guards per class, migration/idempotency/resume suite, protected-path guard, convergence integration test, fixtures, all readings | `tests/contract/**`, `tests/integration/**`, `tests/fixtures/anchor-goal-realignment/**`, `test-evidence/**` of this spec | WP-01…WP-04 |
| **WP-06** | Registry and close | FR-071; `feature-ref.md` | registry row + feature detail status, cross-references, final readings | `.specify/features.md`, `.specify/features/101-anchor-goal-realignment.md` | WP-05 |

**Fence** (binding on every package):

1. No second engine, writer, schema or `--scope` owner — the only store writer is `goal-utils.py`.
2. No new dependency, no new top-level directory, no new command beyond `/speckit.anchor`.
3. No byte change under the protected set of FR-061 (037/038/042/074/085/094, dated spec dirs,
   `.specify/teams/**/runs/**`, `.specify/history/**`, `docs/notes/**`, and the `.specify/archive/**`
   entries that exist at baseline). The **new** `.specify/archive/anchoring/**` subtree this feature
   creates is an addition, not a rewrite — it is outside the equality set and is evidenced by receipts
   (PLAN-EDIT 4).
4. No deletion of definition data — archival only, one receipt per acted entry.
5. Every mirrored source lands with its mirror in the same package; a missed mirror is a defect, not a
   follow-up.
6. No push; commits are feature-local.

**Ceiling readings**: FR count **71** against the ceiling of **120**; estimated task count **≈48** against
the ceiling of **160** (estimate; the measured value is `tasks.md`'s own count at the next stage). The six
work packages are **ordered phases of one line**, not parallel decomposition slots — the stage's slot cap
of **2** is a cap on concurrent dispatch, and this plan stays well inside it: at most two packages may run
at once (WP-05's guard authoring may overlap WP-03 only after WP-01 has landed the names it asserts).

## Testing Strategy

**Tests Mode: ON.** Every guard below is a real test that turns red on the defect it names; "green on a
tree where the subject is fine" is not evidence.

| Guard | Subject | Test | Fails red when |
|-------|---------|------|----------------|
| G-1 | Anchor command surface | `tests/contract/test_anchor_command_surface.py` | `anchor.md` missing; modes ≠ 7; template restates the `--scope` value set instead of citing the owner |
| G-2 | Goal command surface + refusal | `tests/contract/test_goal_command_surface.py` | modes ≠ 4; an Anchor-only mode is accepted, or refused without the literal `anchor-only-mode` naming `/speckit.anchor`; a refusal writes anything |
| G-3 | Store purity | `tests/contract/test_anchor_definitions.py` | any `.specify/anchoring/*/` lacks `anchor.md`; an entry classified `action-goal` is still there |
| G-4 | Single writer + two-writer simulation | `tests/contract/test_goal_store_write_boundary.py` | any non-engine code path writes either definition store; two simulated writers on different slugs land on one path |
| G-5 | Binding completeness | `tests/contract/test_binding_rename.py` | any live `team.md` contains `goal_slug`; any `anchor_slug` fails to resolve; an affected team has no disposition record; the two dangling bindings are unresolved; an R3 team still carries a binding line or lacks `disposition-receipt.json` |
| G-6 | Live-semantic residue | `tests/contract/test_live_semantic_residue.py` | any declared class C1–C7 counts ≠ 0 over the declared roots (`C5` scoped to the anchor store, `C6` mode pointers, `C7` the feature index); the injection case does not turn the scan red |
| G-7 | Migration semantics | `tests/contract/test_cleanup_idempotency.py`, `tests/contract/test_cleanup_resume.py` | a second apply adds a diff or a receipt; digest mismatch passes; a dropped Target passes; I5 is silently repaired; a receipt-less deletion exists |
| G-8 | Protected history | `tests/integration/test_101_protected_paths.py` | any **baseline-existing** protected path's `hash-object` differs from `d7c9da7a3`, or one is deleted (run at implement entry **and** at close); additions under `.specify/archive/anchoring/**` are listed separately and are not failures |
| G-9 | Convergence | `tests/integration/test_101_convergence.py` | on a fixture tree: an action-level entry left in the anchor store, a `goal_slug` survivor, or a dangling `anchor_slug` |
| G-10 | Command-family drift | `tests/contract/test_command_family_101.py` | the flow-class ledger lacks a `/speckit.anchor` row, the reference page is missing, or `command-family` answers a single boolean instead of per-layer |

**Execution**: every run goes through `bash scripts/bash/run-tests.sh` (parallel default; `-m contract` /
`-m integration` to select). `serial`-marked tests run outside the parallel pass. GATE-1 is the failing-id
**set comparison by name** against the baseline captured at implement entry — never a count comparison and
never a parallel-mode reading. Targeted suites run per package; the full suite runs once at close.

**Existing suites are part of the surface**: a package that renames a surface updates every existing test
that asserts the old one, in the same package (tests are mirrors of the surface, not a later cleanup). The
candidates measured at plan entry are `test_goal_command_template.py`, `test_goal_definition.py`,
`test_goal_targets_check.py`, `test_goal_targets_engine.py`, `test_goal_migration.py`,
`test_goal_writeset.py`, `test_temp_goal_contract.py`, `test_binding_model.py`,
`test_migration_interruption.py`, `test_archive_migration.py`, `test_anchor_layout_migrate.py` and
`skill_reference_matrix.py`; which of them actually assert a renamed fact is measured at implement entry
(a red-then-green diff), never guessed from the filename.

## Migration & Cleanup Plan

The executable contract is `contracts/migration-cleanup.contract.md`; this section is the plan-level view.

- **Input**: `classification.json` (14 entries, 7 team dispositions, `mapping_version: 101-mapping-v1`),
  read verbatim; the engine validates schema, class/rule pairs, `mapping_version` and completeness against
  the live directory listing before any write (C-36).
- **Phases (P1→P8)**: anchor renames **+ declared anchor body normalization (A-N-1…A-N-4,
  `anchor-body-receipt.json`)** → Goal migrations + obsolete archival (with receipts) → R2 Anchor
  creation → summary moves → team structural rename (one line per file) → team body normalization
  (declared table N-1…N-6, per-line receipts) → R3 dispositions → self-checks. Each phase is
  per-entry resumable. The anchor rename carries the byte-identity assertion; the normalization that
  follows it is a separate declared rewrite with its own per-line receipt, which is what keeps both
  "rename only" and "the archive speaks Anchor" true at once.
- **Zero-loss evidence**: one JSON receipt per acted entry co-located with the target, carrying source and
  target paths, the concept digest computed through the declared mapping (equal before/after), engine
  identity, result identity, `delete_policy: archive-not-delete` (C-38…C-40).
- **Idempotency**: success is "target exists **and** receipt exists **and** digests match"; a second apply
  must produce no diff and no receipt. Interruption states are named (I1–I5); I5 — source absent, target
  present, receipt absent — is exit 4 `half-state`, never silently blessed.
- **Conflict**: an existing target with a non-equivalent digest stops with exit 4 and names both paths; no
  overwrite, no suffix, no winner (C-43).
- **Exit criteria**: SC-003 (purity), SC-004 (receipts + digest + zero deletions), SC-005 (binding), SC-007
  (idempotency + resume) all measured and written to `test-evidence/`.
- **Rollback**: `git revert` of the package's commits; archive-not-delete means no data can be lost, and the
  receipts make the re-run path the primary recovery, not the rollback.

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed on disk (2026-11-12).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | `research.md` | 7 sections; 14-row classification; 7 team dispositions; R-01…R-14 + R-15 (contract) |
| Classification | `classification.json` | 14 entries + 7 teams, `schema: 101-classification/v1` |
| Data model | `data-model.md` | 11 entities (E-1…E-11), one state-transition table, seven engine-enforced rules |
| Contracts | `contracts/` | 4 files, 49 clauses: `anchor-command` C-1…C-12, `goal-command` C-13…C-22, `goal-engine` C-23…C-35, `migration-cleanup` C-36…C-49 |
| Quickstart | `quickstart.md` | 9 scenarios (S-0…S-8), each marked `[today]` / `[premise]` / `[pin]` |
| Feature reference | `feature-ref.md` | binding + delivery surface + FR→contract map + SC→measurement map + 16 rulings |

**Drift from the Phase 0 expectation**: one addition — `classification.json` was promoted from "a table
inside `research.md`" to a standalone machine-readable plan artifact, because the engine needs an input it
can validate rather than a table it must parse (R-01). No artifact was dropped; no count was pre-written.
