> **STATUS: BLOCKED — NOT COMMITTED.** The decomposition gate remains `split-required` (52 FR > 30) and `state-spine.md` records plan as not dispatched. This file is a review draft only; it MUST NOT be treated as a completed plan or advanced to `/speckit.tasks`. See `notes/decomposition-gate.md` and `notes/plan-blocked-review.md`.

# Implementation Plan: 065-loop-interruption-recovery

**Branch**: `065-loop-interruption-recovery` | **Date**: 2026-10-21 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `065-loop-interruption-recovery` → Feature 065 SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）
**Input**: Specification from `.specify/specs/065-loop-interruption-recovery/requirements.md`

## Summary

在 Feature 058 的 U0–U6、每线状态脊、阶段哨兵与 watcher 判定之上增加一层**观测与恢复**能力，解决实测事故暴露的四个缺口：没有统一状态感知入口、没有确定性中断检测、没有自动化恢复程序、生命周期约束不可校验。

实现落点是一个新引擎加一个 owner 文档：

1. **状态感知**：`scripts/loop-state.py --action snapshot` 一次只读调用聚合状态脊、Registry、四件套、watchbeat、阶段产物、git 提交与 watcher 判定；watcher 可用时 `loop_state` 逐字等于其判定，否则按固定编号规则 D0–D8 派生并标注 `verdict_source=derived`。
2. **中断检测**：八类封闭形态 I1–I8（`unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable`），每类携带证据指针与落脊建议；多条并存时一次裁决。
3. **状态恢复**：`--action recover` 默认 dry-run，按 AD-1–AD-9 输出唯一动作 `none/watch/verify/resume/retry/stop`；`--apply` 下 resume 只补提交本阶段产物、retry 原子隔离旧信号、stop 落 `stalled` 并生成四要素上送件；同线独立锁与幂等保证可重入。
4. **生命周期约束**：SKILL.md Hard Requirements 固化「U2 派发与首个 U3 窗口同回合启动」「退出前落 stalled/reentry-required」，状态脊机读段（`<!-- loop-state:begin/end -->`、`spine_state:`）由 `--action check-spine` 确定性校验；watchbeat 作为第五个存在信号。

不改变 `watch-target.sh` 判定语义与退出码、不改 Registry/lease/ownership、不改各 `/speckit.*` 命令与三段骨架；不引入常驻服务、外部依赖或新运行时。源为 `skills/external/sdd-loop-driver/`，运行时镜像经 `sync-mirrors.py` 生成。

**Driver gate note**: `notes/decomposition-gate.md` records `split-required` (52 FR > 30). The upstream driver dispatched this plan for the full feature; per `efficiency-model.md` §5.3.3 that dispatch is the upstream-flow confirmation to advance. No FR is removed, merged or reordered. The `tasks` U4 gate remains in force (see Risks).

## Technical Context

**Language/Version**: Python 3.8+（标准库；本机 3.9.6）；Bash 仅复用既有 watcher，不新增 shell 实现
**Primary Dependencies**: 无新增第三方依赖；复用 `watch-target.sh`（判定与阈值 owner）、`line-registry.py`（只读 Registry 条目）、git（提交/工作树证据）、`sync-mirrors.py`（镜像）
**Storage**: 文件系统——状态目录中的四件套、watchbeat、`attempts/` 隔离目录、`recover-<line>.lock`、handoff 文件，以及状态脊内固定 fence 的机读段；无数据库、无 daemon
**Testing**: pytest（`tests/{unit,contract,integration}`）；Tests Mode = **ON**。可用解释器为 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest`（pytest 9.1.1）；仓库 `.venv` 无 pytest（环境事实，非产品要求）。基线：watcher `--self-test` 38/0；引擎单测 31 passed；skill 契约 23 passed / 2 pre-existing mirror failures
**Target Platform**: macOS/Linux 驱动与执行宿主；远端拓扑通过同一引擎在证据主机运行，或消费 `--probe` 快照；ssh 不可达记 `STALLED + remote-unreachable`
**Project Type**: SDD 框架 + 自包含 external skill（framework source + skill scripts + docs + tests）
**Performance Goals**: 单次调用一次 watcher `--once` 与 O(证据文件数) 的文件读取、O(提交数) 的 git 查询；无网络轮询、无常驻进程；snapshot 不写盘（`--out` 显式除外）
**Constraints**: 不改 watcher 判定/退出码/自测；不改 Registry/lease/ownership；不改阶段命令内部流程；不自动 push/merge/kill/delete；默认 dry-run；原子写；阈值只引用 watcher owner，不复述数值
**Scale/Scope**: 单次调用一条线一个阶段；多线由调用方逐线循环；八类中断形态、六个恢复动作、52 FR / 10 SC；新增 1 个引擎、1 个 owner reference、2 处 pointer 编辑、1 个 docs 入口、3 个新测试文件 + 1 个既有契约测试更新

## Design Completeness Gates

| Gate | What must be complete | Evidence | Status |
|------|-----------------------|----------|--------|
| G1 Technical Context | Every field answered from measured code/docs; no unresolved clarification marker | This section; `research.md` § 0–2 | ✅ |
| G2 Constitution Check | One row per constitution principle, dynamically derived; Fail/Partial justified | 16-row table below | ✅ |
| G3 Structure & Mirrors | Real directories, every mirror/generated copy listed, verify criterion measured against baseline | Project Structure + Mirror Obligations | ✅ |
| G4 Phase 1 Artifacts | data-model, contracts, quickstart and feature-ref landed; counts backfilled from disk | Phase 1 Design Artifacts Summary | ✅ |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every decision and contract clause maps to FR/SC (`feature-ref.md`); no untraced technical choice |
| II | Feature-Centric Development | ✅ Pass | Feature 065 registered and bound; plan advances Draft → Planned only; `feature-ref.md` records the binding and boundary |
| III | Intent-Driven Development | ✅ Pass | Requirements carry the what/why; `research.md` records decisions and rejected alternatives before the how |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; unit/contract/integration matrix + red-first naming; mutation drills (NR-19); watcher regression floor 38/0 |
| V | AI Agent Integration Standards | ✅ Pass | No agent provider, tier or `AGENT_CONFIG` change; the engine is CLI-agnostic |
| VI | Continuous Quality & Observability | ✅ Pass | JSON `schema_version`, evidence pointers, docs entry, no speculative subsystem; root-cause design for the measured accident |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan chain; plan never reaches Implemented; decomposition gate record disclosed and tracked |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 measured watcher exit codes, attribution, carrier formats, registry spine parsing; design cites code lines in `research.md` § 1 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | No daemon/scheduler/runtime; one one-shot CLI; orchestration remains prompt instructions; rejected a Registry extension and a watcher fork |
| X | Documentation Naming & Location Conventions | ✅ Pass | New reference uses lowercase path semantics `references/state-awareness.md`; existing docs page updated; no reserved name or nested README |
| XI | Dogfooding (Self-Application) | ✅ Pass | The feature is developed through SDD; two hats named; source edit + generated mirror + docs, not a `.specify`-only patch |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the `sync-mirrors.py` Tool record; `.specify/memory/tools/` has no state-awareness/watcher Tool, so writing the engine is the expected outcome; watcher and Registry are reused, not reimplemented |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Controlled Execution (recovery actions), Change Validation (check-spine/snapshot evidence), Reliable Delivery (handoff/no kill), Learning Capture (watchbeat + recovery record); no new scoring system |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | watch-model owns verdicts; stage-prompts owns stall defaults/spine write points; efficiency-model owns plan artifacts; state-awareness owns only new rules; code constants and doc rule ids are pinned by tests |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Handoff carries the four elements in plain language; docs entry explains the actions; JSON evidence provides paths without requiring log-body reading |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Unknown evidence → stop, never a guessed resume; missing probes/signals remain missing; the ANOMALY contract is preserved; mutation drills prove the checks can go red |

**Gates Status**: ✅ All gates pass (no ❌/⚠ row; Complexity Tracking is N/A).

**Re-check after Phase 1** (2026-10-21, after the artifacts landed): the same 16 rows remain ✅ Pass. New evidence: `data-model.md` (12 entities / 84 validation rules), five contracts (159 clauses, FR 52/52 and SC 10/10 covered), `quickstart.md` (7 scenarios), `feature-ref.md`. No new violation; Complexity Tracking remains N/A.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/065-loop-interruption-recovery/
├── plan.md                       # This file
├── research.md                   # Phase 0 decisions + measured baseline
├── data-model.md                 # 12 entities + 84 validation rules
├── contracts/                    # 5 files, 159 clauses
│   ├── loop-state-cli.md
│   ├── snapshot-and-interruptions.md
│   ├── recovery-actions.md
│   ├── spine-and-watchbeat.md
│   └── non-regression-and-tests.md
├── quickstart.md                 # 7 scenarios; § Baseline executed at plan time
├── feature-ref.md                # Binding + FR/SC coverage + deliverables
├── requirements.md               # Upstream (already committed)
├── checklists/requirements.md    # Upstream quality checklist
├── notes/
│   ├── source-requirement.md
│   └── decomposition-gate.md     # split-required record + upstream dispatch confirmation
└── tasks.md                      # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/
├── SKILL.md                                  # New State Awareness section + Hard Requirements + References
├── references/
│   ├── state-awareness.md                    # NEW owner reference (D0–D8, I1–I8, AD-1–AD-9, spine/watchbeat/lock/handoff)
│   ├── stage-prompts.md                      # Pointer edits: machine segment, check-spine call points, watchbeat
│   └── dispatch-recipes.md                   # Pointer edit: same-turn first window + watchbeat in Recipe 3
└── scripts/
    └── loop-state.py                         # NEW engine: snapshot / recover / check-spine / --self-test

.specify/skills/sdd-loop-driver/              # Generated runtime mirror (sync-mirrors.py --write)
docs/reference/skills/sdd-loop-driver.md      # Entry, actions, lifecycle, relationship to watcher/Registry
tests/unit/test_loop_state.py                 # NEW unit suite
tests/contract/test_sdd_loop_driver_state_awareness.py  # NEW contract suite
tests/contract/test_sdd_loop_driver_skill.py  # Update pinned H2 + mirror file lists only
tests/integration/test_loop_state_interruption_matrix.py # NEW interruption/reentry matrix
.specify/memory/features.md                   # Feature 065 row Draft → Planned
.specify/memory/features/065.md               # Detail status + plan note
```

**Structure Decision**: This spec extends the existing self-contained external skill. Two new files live inside `skills/external/sdd-loop-driver/` (one reference, one script); two existing references receive pointer-only edits; the docs entry is updated in place; the runtime mirror is regenerated. No new top-level directory, no engine (`src/`, `templates/`, root `scripts/`) change, and no new package dependency.

### Mirror Obligations

Baseline measured before this plan (research § 0.4): 11 files in this pair already differ; the source is canonical. The end state for this spec is zero drift for the whole pair after regeneration, not merely "no new drift" — the write resolves the disclosed baseline drift as part of the same pair.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` | `sync-mirrors.py --check --only skills/external/sdd-loop-driver`; baseline 11 DIFF recorded; post-write 0 DIFF, `filecmp` on this file |
| `skills/external/sdd-loop-driver/references/state-awareness.md` (new) | `.specify/skills/sdd-loop-driver/references/state-awareness.md` | Post-write file exists and is byte-identical; absent from the pre-write baseline |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` | `.specify/skills/sdd-loop-driver/references/stage-prompts.md` | Post-write byte-identical; baseline DIFF recorded |
| `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | `.specify/skills/sdd-loop-driver/references/dispatch-recipes.md` | Post-write byte-identical; baseline DIFF recorded |
| `skills/external/sdd-loop-driver/scripts/loop-state.py` (new) | `.specify/skills/sdd-loop-driver/scripts/loop-state.py` | Post-write file exists and is byte-identical; absent from the pre-write baseline |
| `docs/reference/skills/sdd-loop-driver.md` | none (documentation entry, not mirrored) | File updated; referenced commands/section names checked by the contract test |
| `tests/unit/test_loop_state.py`, `tests/contract/test_sdd_loop_driver_state_awareness.py`, `tests/integration/test_loop_state_interruption_matrix.py`, `tests/contract/test_sdd_loop_driver_skill.py` | none | The suite runs; the updated pinned lists include the new files |

## Complexity Tracking

N/A — no Constitution Check violation requires justification.

## Phase 0: Research Review

Standalone [research.md](research.md) (Phase 0 exceeded the inline threshold). Key measured facts:

- Watcher: exit codes 0/10–16, `--once` single-line output, `--help` default literals, and the `classify_pair` attribution rule (both `line=` and `run=` required). The new engine consumes, never redefines, these.
- Carriers: `stage-runner.sh` writes no `run=`; `run-stage.sh` does. Attribution therefore uses run envelope OR provable line/stage + mtime + registry identity.
- Registry: `reattach-brief` is the read path; its spine consistency check reads the first bare `state[:=]`, which the `spine_state:` prefix avoids.
- Baseline: watcher self-test 38/0; unit 31 passed; skill contract 23 passed / 2 pre-existing mirror failures; 11-file mirror drift.
- Gate: decomposition `split-required` (52 FR > 30); upstream dispatch recorded as the §5.3.3 confirmation.

All decisions (D-01–D-16), rejected alternatives, risks and the test strategy are in research.md.

## Implementation Sequencing

The sequence is designed to keep `/speckit.tasks` at or below 40 task rows while preserving red-first coverage:

1. **A — Foundation**: engine skeleton (arg parsing, JSON envelope, exit ladder, stdlib guard), artifact map constants, threshold resolver, self-test harness.
2. **B — Awareness (US1/US2)**: evidence readers/attribution, artifact/commit evidence, derived D0–D8, interruption I1–I8, probe input.
3. **C — Recovery (US3)**: action table AD-1–AD-9, dry-run, lock, resume/retry/stop/watch/verify, idempotency, handoff.
4. **D — Lifecycle & spine (US4)**: machine segment writer/validator, watchbeat, SKILL.md rules, stage-prompts/dispatch pointer edits.
5. **E — Distribution (US5)**: docs entry, mirror regeneration, existing skill contract update, non-regression run.
6. **F — Evidence**: integration matrix, mutation drills, quickstart execution, verification record.

## Risks

- **Task budget**: 52 FR is above the decomposition ceiling; the plan keeps one implementation chain and consolidates test rows per file. `tasks` U4 re-runs the gate; if it still returns `split-required`, the driver must split or record another explicit upstream decision before `analyze`.
- **Carrier format split**: 063-style files lack `run=`; the attribution rule (D-05/SN-06) and a dedicated integration fixture are the mitigation.
- **Threshold drift**: thresholds are parsed from the watcher help; a contract test compares resolver and script, so a format change fails loudly instead of silently guessing.
- **Mirror baseline**: 11 pre-existing DIFFs; the write resolves the whole pair and the criterion is zero drift after regeneration.
- **Live-process stop**: the engine never decides to stop a live TIMEOUT; it records `requires_explicit_decision=true` and waits for the user, preserving FR-015/FR-050.

## Phase 1: Design Artifacts Summary

Counts below were taken from the files on disk after they landed (not pre-written).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 12 entities (`E-01`–`E-12`), 84 validation rules (`V-001`–`V-084`) |
| Contracts | [`contracts/`](contracts/) | 5 files, 159 unique clauses: LS 23, SN 44, RC 38, SP 32, NR 22 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios (S1–S7) + one executed baseline section; every engine example carries a per-example not-yet-executable disclaimer and premises |
| Feature reference | [`feature-ref.md`](feature-ref.md) | Binding + FR 52/52 and SC 10/10 coverage + 13-row deliverable list |
| Research | [`research.md`](research.md) | 16 decisions, measured baseline, rejected alternatives, test strategy |

**Drift from the Phase 0 expectation**: none. Phase 0 expected 12 entities and five contracts; the final counts match. The quickstart grew from the planned six scenarios to seven when the probe/unreachable case (FR-024) was separated from the accident replay; the extra scenario is listed here rather than silently absorbed.
