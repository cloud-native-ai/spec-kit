# Tasks: State Awareness Snapshot（状态感知快照）— Feature 065 / Slice 065a

**Requirement ID**: 065a（Feature 065 的第一个切片）
**Requirement Key**: `065a-state-awareness`
**Branch**: `065-loop-interruption-recovery`
**Related Feature**: Feature 065 — SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery），状态 Planned
**Input**: `.specify/specs/065a-state-awareness/` 的 plan.md、requirements.md、research.md、data-model.md、contracts/ ×4、quickstart.md、feature-ref.md
**Prerequisites**: plan.md（required）、requirements.md（required）、research.md、data-model.md、contracts/、quickstart.md、feature-ref.md；父特性 `.specify/specs/065-loop-interruption-recovery/requirements.md` 与 `notes/decomposition-gate.md` 只读引用

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating — unit tests for pure functions/utilities and contract/regression coverage for critical flows; this slice ships executable Python, so the template-only gate does not apply)

**Tests**: 每条新增检查先写红测试再实现；逆样本与变异演练属于交付面（FR-046、SC-006）。失败测试名基线按其 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 捕获与比较，本文件不复述其路径、参数或比较形式。

**Organization**: 按用户故事组织：US1（P1，快照引擎与六类只读检测）是 MVP；US2（P2，既有语义与分发面不回归，承接分解门要求的 US5 兼容性验收）。Setup 冻结改前基线；Foundational 交付两个故事共同依赖的 CLI/信封骨架；Polish 收口变异演练、SC 证据矩阵与 Completion Gate 复验。

## Definition of Done (DoD)

- DoD-1: 所有任务行为 `[X]`；如有 `[~]`，理由记录在 `.specify/specs/065a-state-awareness/verification.md` 的 `deferred_tasks=`。
- DoD-2: `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `snapshot`、`--probe`、`--self-test`，对 `recover`/`check-spine` 返回结构化拒绝；全部执行路径只读（显式 `--out` 除外）。
- DoD-3: 4 份契约的 60 条规范条款（`C-1`…`C-60`；`LS`/`SN`/`IA`/`AM` 为别名）逐条由任务行 `[green:]` 认领并有测试或文档落点；另有一条契约测试断言 `loop-state.py` 的 `STAGE_ARTIFACTS`、`references/state-awareness.md` §Stage Artifact Map 与 `requirements.md` FR-004 的 derived 映射表三方逐项一致（代码表 == reference 表 == FR-004 表）。
- DoD-4: `tests/unit/test_loop_state_engine.py`、`tests/contract/test_loop_state_contract.py`、`tests/contract/test_sdd_loop_driver_skill.py` 全绿，且全量回归相对 T001 基线零 NEW 失败。
- DoD-5: 源与运行时镜像字节一致（`scripts/loop-state.py`、`references/state-awareness.md`、`SKILL.md` 三对）；`sync-mirrors.py --check` 相对 T001 基线无新增漂移。
- DoD-6: `.specify/specs/065a-state-awareness/verification.md` 以 `- **SC-001**:` 至 `- **SC-006**:` 列出六条成功标准的状态、命令、输出与证据，并以 `- **US5-A1**:` 至 `- **US5-A4**:` 列出四条兼容性验收。
- DoD-7: 文档取值与代码一致：`references/state-awareness.md`、`SKILL.md`、`docs/reference/skills/sdd-loop-driver.md` 均含入口、调用形态与 watcher/Registry 关系，且与 `--help` 一致。
- DoD-8: 范围审计通过：未改动 066/067/068 目录、`.specify/specs/065-loop-interruption-recovery/`、watcher/Registry 语义、命令模板与依赖清单；无 daemon、无 push/merge/kill/删除。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/065a-state-awareness/tasks.md` exit 0。
- GATE-2: 跨产物无漂移 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/065a-state-awareness --stage tasks --repo .` 输出含 `decision=pass`。
- GATE-3: 新增与扩展测试全绿 — check: `SPECKIT_PYTHON=<§ Environment Prerequisites（2026-10-21）的 pytest 解释器> bash scripts/bash/run-tests.sh tests/unit/test_loop_state_engine.py tests/contract/test_loop_state_contract.py tests/contract/test_sdd_loop_driver_skill.py -q` exit 0（`No module named pytest` 判 probe failure，不得记空基线）。
- GATE-4: watcher 判定零回归 — check: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` exit 0 且汇总含 `0 failed`。
- GATE-5: 镜像字节一致 — check: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` exit 0，且 `plan.md` § Mirror Obligations 三对文件逐一 `cmp` exit 0。
- GATE-6: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/065a-state-awareness/tasks.md` 返回 0。
- GATE-7: SC 与 US5 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-6]\*\*' .specify/specs/065a-state-awareness/verification.md` 返回 6，且 `grep -cE '^- \*\*US5-A[1-4]\*\*' .specify/specs/065a-state-awareness/verification.md` 返回 4。

## Environment Prerequisites

- Python 3 语法目标: **available** — probe: `python3 --version` → `Python 3.9.6` @ 2026-10-21; affected: `loop-state.py` 必须保持 Python 3.8 语法兼容，当前解释器满足 `>=3.8`。
- pytest 运行器: **partial** — probe: `python3 -m pytest --version` → `No module named pytest`；`.venv/bin/python -m pytest --version` → 同样缺失；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` → `pytest 9.1.1`，且 `tests/unit/test_pre_analyze_check.py` → `15 passed` @ 2026-10-21; affected: T003、T005–T008、T019–T027、GATE-3; 处置: 通过 `SPECKIT_PYTHON` 指向该解释器或向 `.venv` 安装 pytest；`No module named pytest` 按 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 判 probe failure，不得记空基线。
- watcher 自测: **available** — probe: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` → `SELF-TEST: 38 passed, 0 failed`，exit 0 @ 2026-10-21; affected: T024、GATE-4。
- 镜像基线: **clean** — probe: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` → `ok skills/external/ == .specify/skills/ (26 files)`，exit 0 @ 2026-10-21; affected: T001、T023、GATE-5；判据是“相对该基线无新增漂移”，不是绝对零漂移。
- 外部环境（容器/集群/网络）: **none** — 本切片全部检查为本地文件、`git` 与本地 watcher 子进程，无 docker、镜像仓库、实集群或远程网络依赖 @ 2026-10-21; affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同一阶段内其它 `[P]` 行并行（写目标不同、无未完成依赖）。
- **[Story]**: 用户故事标签（`[US1]` / `[US2]`），仅用户故事阶段的任务携带。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列出的任务全部 `[X]` 前不得开始本行。存在具体依赖时用它替代散文式“depends on”。
- **契约绿点**: 本切片契约使用项目规范条款形态 `C-1`…`C-60`（语法 owner：`.specify/shared/definitions/contract-clause-definitions.md` §3），`LS`/`SN`/`IA`/`AM` 仅作为别名保留在各契约开头的映射表。`clause_extract.py` 只识别 `C-<n>` 形式，故绿点用 `[green: contracts/<file>#C-<n>]` 声明；60 条条款必须被任务行完整认领（T003 C-1…C-6、T004 C-7…C-32、T007 C-33…C-49、T011 C-50…C-60），并由 `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed；`- [X]` — Closed；`- [~]` — Deferred（理由须记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **Framework source（编辑面）**: `skills/external/sdd-loop-driver/`、`tests/`、`docs/reference/skills/sdd-loop-driver.md`。
- **Generated mirrors（生成面，禁止手改）**: `.specify/skills/sdd-loop-driver/`，仅由 `scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 再生成。
- **Feature evidence**: `.specify/specs/065a-state-awareness/` 下的 `notes/`、`verification.md`、`coverage-baseline.txt`；`test-evidence/` 是驱动侧证据通道，本切片任务不写、不提交。
- **Read-only isolation**: `.specify/specs/066-*/`、`067-*`、`068-*`、`.specify/specs/065-loop-interruption-recovery/`、`.specify/memory/feedback/`、`.specify/memory/session/`、`.specify/memory/exec-quant/`、`.specify/memory/evidence/`、`.specify/memory/features*` 一律只读。
- **既有未提交改动**: `skills/external/sdd-loop-driver/` 与 `tests/contract/test_sdd_loop_driver_skill.py`、`docs/reference/skills/sdd-loop-driver.md` 已含外部同步产生的未提交改动；实现只做增量编辑，不得回退、重排或整文件重写这些改动。

## Measured Premises (re-measured at generation time 2026-10-21)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 契约条款数 | `grep -cE '^- \*\*C-[0-9]+\*\*' .specify/specs/065a-state-awareness/contracts/*.md` | `loop-state-cli.md` 18、`snapshot-envelope.md` 14、`interruption-and-action.md` 17、`stage-artifact-map.md` 11；合计 60（`LS`/`SN`/`IA`/`AM` 为别名，不计入） |
| 契约条款数（历史形态，勿用） | `grep -cE '^- \*\*[A-Z]{2,4}-[0-9]{2}\b' .specify/specs/065a-state-awareness/contracts/*.md` | 0 —— 条款已改为规范 `C-N` 形态；该命令只作迁移前对照 |
| 契约条款数（naive 变体，勿用） | `grep -ohE '[A-Z]{2,4}-[0-9]{2}' .specify/specs/065a-state-awareness/contracts/*.md \| wc -l` | 80 —— 把散文引用计入，与条款定义数不一致 |
| 任务行数 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/065a-state-awareness/tasks.md` | 30（红线 ≤40） |
| 任务行数（naive 变体，勿用） | `grep -ohE 'T[0-9]{3}' .specify/specs/065a-state-awareness/tasks.md \| wc -l` | 182 —— 把 `blockedBy` 引用与正文提及计入，与任务行定义数不一致 |
| watcher 基线 | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | `SELF-TEST: 38 passed, 0 failed`，exit 0 |
| 兼容测试基线 | `.venv` 外的 pytest 解释器运行 `tests/unit/test_line_registry_engine.py tests/contract/test_sdd_loop_driver_skill.py` | `48 passed in 22.70s` |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (26 files)`，exit 0；naive 变体 `find skills/external/sdd-loop-driver -type f \| wc -l` = 27，差 1 为 `__pycache__` |
| 引擎与 reference 尚不存在 | `ls skills/external/sdd-loop-driver/scripts/loop-state.py skills/external/sdd-loop-driver/references/state-awareness.md` | 两个路径均返回 `No such file or directory` |

`missing-path` 类 advisory 在实现前属于预期（新文件尚未创建），不构成 blocking；`error` 必须为 0。

## Requirement Coverage Map

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T004、T009–T017、T029 |
| FR-002 | T005、T009、T016、T003 |
| FR-003 | T003、T004、T015 |
| FR-004 | T007、T013 |
| FR-005 | T007、T012 |
| FR-006 | T008、T011、T018 |
| FR-007 | T006、T011 |
| FR-008 | T006、T011 |
| FR-009 | T007、T014 |
| FR-010 | T006、T010、T018 |
| FR-011 | T007、T014 |
| FR-012 | T003、T004、T008、T017 |
| FR-038 | T024、T029 |
| FR-039 | T010、T024 |
| FR-040 | T029 |
| FR-041 | T029 |
| FR-042 | T020、T023 |
| FR-043 | T018、T022 |
| FR-044 | T021、T022 |
| FR-046 | T005–T008、T026 |
| FR-047 | T005、T009 |
| FR-049 | T029 |
| FR-050 | T003、T029 |
| FR-051 | T007、T015 |
| FR-052 | T024、T029 |
| SC-001 | T007、T019 |
| SC-002 | T005、T006、T008、T019 |
| SC-003 | T007、T019、T026 |
| SC-004 | T024 |
| SC-005 | T020、T023、T029 |
| SC-006 | T005–T008、T026 |

父编号 045 / 048 为显式 out-of-slice（分别由 065c 汇总/承接），不在本表冒充切片需求。T001（改前基线）、T002（覆盖基线冻结）、T030（Completion Gate 复验）是流程任务，按设计不映射 FR/SC。

**Task Distribution**: Setup 2 · Foundational 2 · US1 15 · US2 6 · Polish 5 · 任务行合计 30。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结改前基线与契约覆盖基线，让后续每条“与改前对比”的前提都有日期化依据。

- [X] T001 捕获改前基线并把命令与真实输出写入 `.specify/specs/065a-state-awareness/notes/pre-change-measurements.md`：`python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 的漂移集（判据是“相对基线无新增漂移”，不得把既有漂移归因本切片）、`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` 的汇总行、`tests/unit/test_line_registry_engine.py` 与 `tests/contract/test_sdd_loop_driver_skill.py` 的跑前结果、以及 `git status --short -- skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver docs/reference/skills/sdd-loop-driver.md tests/contract/test_sdd_loop_driver_skill.py` 的快照；失败测试名基线按 `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 的 owner 形态捕获（本行只指向 owner，不复述其路径/参数/比较形式）；pytest 解释器见 § Environment Prerequisites（2026-10-21）。
- [X] T002 [P] 冻结契约覆盖基线：在仓库根运行 `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/065a-state-awareness --freeze > .specify/specs/065a-state-awareness/coverage-baseline.txt`，核对首行以 `# coverage-baseline:` 起首、`frozen-from:` 明示 `excluding 065a-state-awareness` 且记录 `base-sha`，并把该文件保留为后续 `LC_ALL=C comm -13` 的冻结侧（脚本只打印、不写文件）。

**Checkpoint**: 改前基线与覆盖基线已落盘；每个“diff against pre-change”前提都有日期化基线。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 交付两个用户故事共同依赖的 CLI 面、退出码阶梯、共享 JSON 信封与 `--out` 边界。

**⚠️ CRITICAL**: 本阶段完成前，用户故事阶段不得开始。

- [X] T003 红先编写 CLI/信封契约测试到 `tests/contract/test_loop_state_contract.py`：`--help` 的 `0/1/2` 阶梯与“watcher 判定码只作数据”、`recover`/`check-spine` 结构化拒绝（`schema_version=1`、`applied=false`、`result=failed`、`reason=not-implemented-in-065a`、逐动作 `owner`：`check-spine`→`065b`、`recover`→`065c`、exit 1）、快照顶层必填字段与 `recovery_decision.action/reason` 一致性、嵌套 `spine.consistent` 且无顶层别名、`--out` 原子写与目标/父目录先 `realpath` 后比较（含 symlink、相对路径、指向 `state_dir` 的符号链接）落在 `state_dir`/`repo` 内时 exit 2 且不留文件、快照只读 mtime 审计、derived 映射 owner 归属解析断言（切片 `requirements.md` FR-004/FR-043、父 `065-loop-interruption-recovery/requirements.md` FR-004、`research.md` R-13、`plan.md` 结构树、`references/state-awareness.md` §Derived Mapping 与 `loop-state.py` 中任一产物若声称 derived 表 owner 不是 FR-004，或声称 reference/代码拥有该表，测试 MUST 失败）；运行并把失败输出（命令、真实输出、退出码）写入 `.specify/specs/065a-state-awareness/notes/red-first-evidence.md`。 [green: contracts/loop-state-cli.md#C-1] [green: contracts/loop-state-cli.md#C-2] [green: contracts/loop-state-cli.md#C-3] [green: contracts/loop-state-cli.md#C-4] [green: contracts/loop-state-cli.md#C-5] [green: contracts/loop-state-cli.md#C-6]；红证据详见 notes/red-first-evidence.md §T003/T008（contract 25 项 / 5 failed）
- [X] T004 实现 `skills/external/sdd-loop-driver/scripts/loop-state.py` 的 CLI 骨架与共享进程契约：`--action snapshot|recover|check-spine`、`--self-test` 与 `--line-id/--stage/--state-dir/--spec-dir/--repo/--spine/--probe/--watch-script/--out/--start-grace/--deadline-grace/--heartbeat-max-age/--retry-limit` 参数面；`--help` 列出三动作、全部参数、退出码阶梯与“watcher 判定码是数据”；`0/1/2` 退出阶梯；两个未实现动作的结构化拒绝（`owner` 按动作：`check-spine`→`065b`、`recover`→`065c`）；顶层信封组装（含嵌套 `spine.consistent`）；`--out` 目标与父目录先 `realpath` 再比较、同目录临时文件加原子替换，目标落入 `state_dir` 或 `repo` 时 exit 2 且不留文件；仅标准库、Python 3.8 语法。 [blockedBy: T003] [green: contracts/loop-state-cli.md#C-7] [green: contracts/loop-state-cli.md#C-8] [green: contracts/loop-state-cli.md#C-9] [green: contracts/loop-state-cli.md#C-10] [green: contracts/loop-state-cli.md#C-11] [green: contracts/loop-state-cli.md#C-12] [green: contracts/loop-state-cli.md#C-13] [green: contracts/loop-state-cli.md#C-14] [green: contracts/loop-state-cli.md#C-15] [green: contracts/loop-state-cli.md#C-16] [green: contracts/loop-state-cli.md#C-17] [green: contracts/loop-state-cli.md#C-18] [green: contracts/snapshot-envelope.md#C-19] [green: contracts/snapshot-envelope.md#C-20] [green: contracts/snapshot-envelope.md#C-21] [green: contracts/snapshot-envelope.md#C-22] [green: contracts/snapshot-envelope.md#C-23] [green: contracts/snapshot-envelope.md#C-24] [green: contracts/snapshot-envelope.md#C-25] [green: contracts/snapshot-envelope.md#C-26] [green: contracts/snapshot-envelope.md#C-27] [green: contracts/snapshot-envelope.md#C-28] [green: contracts/snapshot-envelope.md#C-29] [green: contracts/snapshot-envelope.md#C-30] [green: contracts/snapshot-envelope.md#C-31] [green: contracts/snapshot-envelope.md#C-32]；红证据详见 notes/red-first-evidence.md §T003/T008（同一 contract 文件）

**Checkpoint**: `--help`、退出码阶梯、拒绝信封与 `--out` 边界可由契约测试验证；US1 可以开始。

---

## Phase 3: User Story 1 - 一次调用看清一条线的真实状态 (Priority: P1) 🎯 MVP

**Goal**: 一次只读 `snapshot` 调用聚合状态脊、Registry、四件套、watchbeat、阶段产物、git 提交与可用 watcher 判定，识别六类中断形态并给出唯一恢复动作建议。

**Independent Test**: 用夹具构造“产物齐备、未提交、`exit=1`、无哨兵、无 watcher”的线、正常运行中的线与未派发的线，分别调用快照并核对 `loop_state`、`verdict_source`、`interruptions[]`、`recovery_action`、证据指针与缺失信号语义；再运行两个新增测试文件。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [X] T005 [US1] 红先编写单元测试到 `tests/unit/test_loop_state_engine.py`：路径解析优先级（显式 `--spine/--state-dir/--spec-dir/--repo` → Registry → `missing`）、Registry 缺失继续求值、v1 机读段与 legacy 脊降级（`missing_fields`、`value_state=unknown`）、“有派发证据但脊缺失 → `UNKNOWN`+`stop`”与 `not-dispatched` 的判据互斥、`--stage` 仅为意图、脊存在且 `spine_state` 非空时排除 `not-dispatched`、never-dispatched 时四件套/watchbeat/artifacts/commits 记 `status=na`/`value_state=na`、单线求值不跨线推断、两次同输入除 `evaluated_at` 外逐字相等；把红跑输出写入 `.specify/specs/065a-state-awareness/notes/red-first-evidence.md`。 [blockedBy: T004]；红证据详见 notes/red-first-evidence.md §T005–T007（unit 55 项 / 51 failed）
- [X] T006 [US1] 红先扩展 `tests/unit/test_loop_state_engine.py`：四件套空格信封读取（含无 `run=` 的现行 status/pid）、watchbeat 的 `run/stage/window/at/event` 与新鲜度、日志末行哨兵与 `ANOMALY:`（哨兵 MUST 为最后非空行；末行 `ANOMALY:` 时更早的哨兵字样不置真）、stale 三类判据（run 不符、mtime 早于 `stage_started_at`、无归属 `legacy-stale`）与求值排除、产物“存在且非空”（目录至少一个非空文件）、`checklist` 阶段要求自 `stage_base_commit` 起新增/修改的 checklist 文件（仅有预存文件的负例 → 不完整）、`stage_base_commit` 基线的提交证据、analyze 无必需文件 → `artifacts.complete=true`（vacuous truth）、implement 仅文档提交的负例 → 不完整、`false_completion` 与 `artifacts-without-completion` 互斥；记录红跑。 [blockedBy: T005]；红证据详见 notes/red-first-evidence.md §T005–T007（artifact/commit/checklist 组全红）
- [X] T007 [US1] 红先扩展 `tests/unit/test_loop_state_engine.py`：FR-004 的 derived 八条优先级与两个前置短路、六类检测器的正/逆样本（正常窗口不报 `unwatched`、活进程不出 `stop`、哨兵在而产物缺不 `resume`）、watcher 判定三态（取得 `present=true`/`status=present`/`known`/字面量；不可用 `present=false`/`status=missing`/`value_state=na`/`reason=unavailable`；无 target `present=false`/`status=na`/`value_state=na`）、watcher 归属三态（own / legacy / 有 stale 不调用）、`IA-14` 动作优先级与特例（analyze DONE → `verify`；`commit_required=false` 的 DONE → `verify`；DONE + `commits.value_state=unknown` → `verify` + `reason=commit-baseline-unknown`；clarify 合法无变更 → `verify`；`STALLED`/`ANOMALY`/`DEAD` + `artifacts.complete=true` + `commits.value_state=unknown`（无哨兵、无 salvage）分别落到 `stop`/`retry`/`retry`，MUST NOT 落到 `verify`；`STALLED`/`REENTRY_REQUIRED` + 产物齐备不得被行 8–10 改判、`false_completion=true` + `STALLED`/`REENTRY_REQUIRED` → `stop` 不得按 C-31/C-42 的 retry 默认）、末行哨兵 + 活进程 + 其后 `ANOMALY:` 行 → 不判 `DONE`（RUNNING + `watch`，`false_completion=false`）、stale 存在时仅列入并排除求值、不因单纯 stale 改变动作（`stale-unisolated` 归 065c）、salvage 门与尝试上限、probe 两形状与本地证据隔离、事故回放夹具（SC-001）；记录红跑。 [blockedBy: T006] [green: contracts/interruption-and-action.md#C-33] [green: contracts/interruption-and-action.md#C-34] [green: contracts/interruption-and-action.md#C-35] [green: contracts/interruption-and-action.md#C-36] [green: contracts/interruption-and-action.md#C-37] [green: contracts/interruption-and-action.md#C-38] [green: contracts/interruption-and-action.md#C-39] [green: contracts/interruption-and-action.md#C-40] [green: contracts/interruption-and-action.md#C-41] [green: contracts/interruption-and-action.md#C-42] [green: contracts/interruption-and-action.md#C-43] [green: contracts/interruption-and-action.md#C-44] [green: contracts/interruption-and-action.md#C-45] [green: contracts/interruption-and-action.md#C-46] [green: contracts/interruption-and-action.md#C-47] [green: contracts/interruption-and-action.md#C-48] [green: contracts/interruption-and-action.md#C-49]；红证据详见 notes/red-first-evidence.md §T005–T007（derived/action/probe 组全红）
- [X] T008 [US1] 红先扩展 `tests/contract/test_loop_state_contract.py`：`--probe` 两形状与拒绝路径（不可解析、`schema_version≠1`、`reachable=true`、与 `--spine/--state-dir/--spec-dir/--repo/--watch-script` 互斥且 exit 2、不读本地证据）、必需输入与证据源矩阵（`--line-id` 缺失 → exit 2；`--probe` 不可读/不可解析 → exit 2；`--spine`/`--state-dir`/`--spec-dir`/`--repo` 不可读 → `status=missing` + exit 0）、`--self-test` 输出契约（`ok <case>` / `FAIL <case> — <detail>` / `SELF-TEST: N passed, M failed` / exit 0|1）、确定性（除 `evaluated_at` 外 diff 为 0）、`C-50`（`AM-01`）的脚本 `STAGE_ARTIFACTS` 与 `references/state-awareness.md` §Stage Artifact Map 五维逐项一致、以及脚本 derived 映射表 == reference §Derived Mapping 表 == `requirements.md` FR-004 表的三方逐项一致；记录红跑。 [blockedBy: T003,T004]；红证据详见 notes/red-first-evidence.md §T003/T008（contract 25 项 / 5 failed）

### Implementation for User Story 1

- [X] T009 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现输入解析与只读投影：按 `LS-04` 解析 `line_id/stage/state_dir/spine/spec_dir/repo`、读取 Registry 条目（缺失记 `status=missing` 且不致命）、解析脊 v1 fence 与 legacy `state[:=]`、输出 `paths`/`spine`/`registry`；缺失值用 `null`，不猜路径、不填默认值。 [blockedBy: T005]；绿证据：unit `test_explicit_paths_win_over_registry`/`test_registry_fallback_resolves_paths_and_stage`/`test_unresolved_paths_stay_null_and_are_not_invented`/`test_v1_spine_fields_are_parsed_without_guessing`/`test_legacy_spine_marks_degraded_fields_unknown` 转绿（notes/red-first-evidence.md §T009–T014）
- [X] T010 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现证据读取器：pid/status/log/heartbeat 空格信封、watchbeat 标记、可选 hook、产物与提交证据的输入面；按信封 `run=`、mtime 与 legacy 判据产出 `stale_signals[]` 并从 `loop_state`/产物/动作求值中排除；只输出原始 `at`/`mtime_ns`，不输出年龄。 [blockedBy: T006]；绿证据：unit 四件套/ watchbeat / 末行哨兵 / 三类 stale 组转绿，`stale_signals[]` 原始 `at`/`mtime_ns` 与求值排除由 `test_stale_*` 组钉住（notes/red-first-evidence.md §T009–T014）
- [X] T011 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `STAGE_ARTIFACTS` 数据表（requirements/clarify/plan/tasks/checklist/analyze/implement/review 八阶段，含 `artifacts[]`/`owned_paths[]`/`commit_required`/`no_change_allowed`）、产物完整性（存在且非空；目录至少一个非空文件；`checklist` 要求自 `stage_base_commit` 起新增/修改的 checklist 文件）、`missing_artifacts[]`、以 `stage_base_commit` 为基线的 `git log <base>..HEAD -- <pathspec>` 提交证据（implement 的 pathspec 枚举为 `src/`、`skills/`、`scripts/`、`tests/`、`templates/`、`agents/`，仅文档提交不计）、`uncommitted_artifacts[]`、`false_completion` 与 analyze 的 vacuous `artifacts.complete=true`；基线缺失记 `commits.value_state=unknown` 且不回退 HEAD；提交齐备谓词按 `C-46`（`IA-14`）投影。 [blockedBy: T006] [green: contracts/stage-artifact-map.md#C-50] [green: contracts/stage-artifact-map.md#C-51] [green: contracts/stage-artifact-map.md#C-52] [green: contracts/stage-artifact-map.md#C-53] [green: contracts/stage-artifact-map.md#C-54] [green: contracts/stage-artifact-map.md#C-55] [green: contracts/stage-artifact-map.md#C-56] [green: contracts/stage-artifact-map.md#C-57] [green: contracts/stage-artifact-map.md#C-58] [green: contracts/stage-artifact-map.md#C-59] [green: contracts/stage-artifact-map.md#C-60]；绿证据：unit `test_directory_artifact_requires_one_nonempty_file`/`test_checklist_stage_needs_a_checklist_added_since_base`/`test_commit_evidence_uses_stage_base_commit`/`test_unknown_base_commit_marks_value_unknown_not_head_guess` 的 artifacts/commits 断言转绿；`STAGE_ARTIFACTS` 八阶段五维一致性的 reference 侧比对留待 T018（notes/red-first-evidence.md §T009–T014）
- [X] T012 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 watcher 委托：仅在有活动 target、非 `not-dispatched`、非 `--probe` 时调用 `watch-target.sh --once`；按 `C-14`（`LS-14`）三态选择归属参数（可证归属 / 兼容形态 / 有 stale 不调用），解析 `WATCH key=value` 的 `verdict/rc/reason/attribution`；判定三态 MUST 与 T007 的断言一致——取得 `present=true`/`status=present`/`value_state=known`/字面量；不可用 `present=false`/`status=missing`/`value_state=na`/`verdict=null`/`reason=unavailable` + `detail` 值域；无 target `present=false`/`status=na`/`value_state=na`/`reason=null`；绝不伪造 verdict 或判 `DEAD`。 [blockedBy: T007]；绿证据：unit `test_watcher_verdict_tristate`/`test_watcher_attribution_forms` 除动作断言外全绿（含“有 stale 不调用 watcher”）
- [X] T013 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `loop_state` 求值：watcher 判定存在时逐字采用；否则按 FR-004 固定优先级导出，并先执行 `not-dispatched`、远端不可达、有派发证据但缺脊三个前置分支；标注 `verdict_source` 与 `loop_state_reason`；与 `spine.last_verdict` 冲突只报 `spine.consistent=false`，不静默择一。 [blockedBy: T007]；绿证据：unit `test_derived_*` 组的 `loop_state`/`loop_state_reason`/`verdict_source`/`spine.consistent` 断言转绿，仅余动作断言红（归 T015）
- [X] T014 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现六类只读检测器：`unwatched`（缺失/过期两分支，哨兵存在时不触发）、`dead-no-exit-record`、`deadline-overrun-live`、`artifacts-without-completion`、`stale-signal`、`remote-unreachable`；每条含 `form/detail/evidence[]/detector`，不同根因各自成条；`heartbeat-stalled` 与 `lifecycle-spine-violation` 只保留词表与 `missing`/`unknown` 语义、不检测。 [blockedBy: T007]；绿证据：unit `unwatched` 两分支正逆样本、`dead-no-exit-record`、`deadline-overrun-live`、`artifacts-without-completion`、`stale-signal` 检测器断言转绿；`remote-unreachable` 形态随 probe 由 T016 验收
- [ ] T015 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现动作建议与信封收口：动作建议按 C-46 行 6 仅对 `loop_state=DONE` 的 `commit-baseline-unknown` 进入 `verify`，行 8–10 MUST NOT 消费 `STALLED`/`REENTRY_REQUIRED`（落到行 11 `stop`；C-31/C-42 的 false_completion retry 默认同样不得覆盖行 11）；按 `IA-14` 顺序取唯一 `recovery_action`，应用 `IA-15` 尝试上限与 `attempt` 未知时不得 `resume`、`IA-16` salvage 完整记录门、`IA-17` 活进程 `TIMEOUT` 优先 `watch`；组装 `recovery_decision` 的 `action/reason/preconditions/blocked_by` 并保证与顶层字段相等。 [blockedBy: T007]
- [ ] T016 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `--probe`：形状 (a) 逐字消费探针的 `spine`/`registry`/`watch_verdict`/`evidence` 并本地重算派生字段、`evidence_source=probe`；形状 (b) 输出 `STALLED`+`remote-unreachable`+`stop`；不可解析、`schema_version≠1`、`reachable=true`、`line_id` 冲突或与本地路径参数并用一律 exit 2；probe 模式不读本地证据、不调用本地 watcher。 [blockedBy: T008]
- [ ] T017 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `--self-test`：自建临时夹具，逐例输出 `ok <case>` / `FAIL <case> — <detail>`，末行 `SELF-TEST: N passed, M failed`，退出 0/1；覆盖 `LS-18` 列出的六类形态（含 `unwatched` 两分支）、旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 脊、不可达证据、`not-dispatched`、Registry 缺失继续求值、probe 两形状与拒绝、未实现动作拒绝、确定性与 `--help` 阶梯钉住。 [blockedBy: T009,T010,T011,T012,T013,T014,T015,T016]
- [ ] T018 [P] [US1] 编写 owner reference `skills/external/sdd-loop-driver/references/state-awareness.md`：快照入口与调用形态、八类形态表（标注 065a 六类检测 / 065b 两类）、§Derived Mapping（必须包含一张逐项镜像 `requirements.md` FR-004 的映射表，首行声明 FR-004 为唯一 owner；不得声称拥有该表）、§Stage Artifact Map（与脚本 `STAGE_ARTIFACTS` 五维逐项一致）、probe 契约、动作建议表、watchbeat 读取契约；SKILL.md 与其它 references 只引用本章节、不复述整表。 [blockedBy: T011]

### Verification for User Story 1

- [ ] T019 [US1] 跑绿并实证 US1：`SPECKIT_PYTHON=<§ Environment Prerequisites（2026-10-21）的 pytest 解释器> bash scripts/bash/run-tests.sh tests/unit/test_loop_state_engine.py tests/contract/test_loop_state_contract.py -q` 全绿；按 `quickstart.md` §2–§8 用真实夹具执行事故回放、正常窗口、未派发、两种 probe、`--self-test` 与 `--out` 场景，把命令、输出与退出码写入 `.specify/specs/065a-state-awareness/notes/quickstart-run.md`；发现漂移在本行内修正并重跑。 [blockedBy: T017,T018]

**Checkpoint**: US1 可独立验收：单次快照给出完整聚合、六类形态、唯一动作建议，且 `--self-test` 与 probe 行为符合契约。

---

## Phase 4: User Story 2 - 既有语义与分发面不回归 (Priority: P2)

**Goal**: 升级后既有 watcher 判定、四件套格式、Registry、阶段命令、确认门与 fast-fail 纪律保持原样；框架源、运行时镜像、文档与测试一致，无新增常驻服务或外部依赖。

**Independent Test**: 运行既有 watcher `--self-test`、驱动技能契约测试、Registry 引擎测试与镜像一致性检查；逐条核对 US5 A1–A4 的四类不回归结论。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T020 [US2] 红先更新 `tests/contract/test_sdd_loop_driver_skill.py` 的 `MIRROR_FILES`，加入 `scripts/loop-state.py` 与 `references/state-awareness.md`（保留工作树中已有的外部同步未提交改动，只做增量、不回退/重排），运行镜像断言并把失败输出写入 `.specify/specs/065a-state-awareness/notes/red-first-evidence.md`。 [blockedBy: T019]
- [ ] T021 [US2] 红先扩展 `tests/contract/test_loop_state_contract.py` 的分发/文档断言：`skills/external/sdd-loop-driver/SKILL.md` 含 `references/state-awareness.md` 的 References 行与只读 Hard Requirement；`docs/reference/skills/sdd-loop-driver.md` 含入口路径、调用形态、与 watcher/Registry 的关系；断言取值与脚本 `--help`/数据一致；记录红跑。 [blockedBy: T019]

### Implementation for User Story 2

- [ ] T022 [US2] 更新分发文档：在 `skills/external/sdd-loop-driver/SKILL.md` 增加 `references/state-awareness.md` 的 References 行与“快照只读、不得写脊/杀进程”的 Hard Requirement；在 `docs/reference/skills/sdd-loop-driver.md` 增加 `loop-state.py` 入口、`snapshot`/`--probe`/`--self-test` 调用形态及与 watcher/Registry 的关系；只增量编辑并保留既有未提交改动。 [blockedBy: T021]
- [ ] T023 [US2] 再生成运行时镜像并验证：运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`，随后 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 相对 T001 基线无新增漂移，并对 `scripts/loop-state.py`、`references/state-awareness.md`、`SKILL.md` 三对源/镜像做 `cmp`/`diff -q` 字节比较；禁止手改 `.specify/skills/sdd-loop-driver/`。 [blockedBy: T017,T018,T022]

### Verification for User Story 2 (US5 Compatibility)

- [ ] T024 [US2] 运行兼容性回归（US5 A1–A3）：`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`（`0 failed`、判定与退出码零差异）、`SPECKIT_PYTHON=<§ Environment Prerequisites（2026-10-21）的 pytest 解释器> bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py tests/contract/test_sdd_loop_driver_skill.py -q`、以及 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver`；与 T001 基线做名字级比较（比较形态 owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs），把命令、输出与差异写入 `.specify/specs/065a-state-awareness/verification.md`。 [blockedBy: T023]
- [ ] T025 [US2] 完成 US5 四条兼容性验收：在 `.specify/specs/065a-state-awareness/verification.md` 以 `- **US5-A1**:` 至 `- **US5-A4**:` 逐条记录 A1 watcher 自测与退出码零差异、A2 四件套与 Registry 旧条目可读（含无 `run=` 信封）、A3 源/镜像字节一致与漂移为零、A4 既有 `/speckit.*` 命令三段骨架/哨兵字面量/确认门/no-push 策略无改动（以 `git diff` 为证）；每条给命令、输出与证据指针。 [blockedBy: T024]

**Checkpoint**: US2 可独立验收：既有测试全绿、镜像字节一致、文档与代码取值一致、US5 四场景均有证据。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 变异演练、全量回归、SC 证据矩阵、范围审计与 Completion Gate 复验。

- [ ] T026 执行 SC-006 变异演练：先把 `skills/external/sdd-loop-driver/scripts/loop-state.py` 按字节备份到临时路径，再就地移除 `unwatched` 检测分支，运行 `tests/unit/test_loop_state_engine.py` 的对应用例并确认至少一条转红；然后恢复备份，再移除 `IA-16`（`C-48`）的 salvage 完整记录门（把未完整记录当作完整），确认至少一条 salvage 用例转红；每次从备份按字节恢复并校验 sha256 一致；把两处移除位置、命令与转红用例写入 `.specify/specs/065a-state-awareness/verification.md`。 [blockedBy: T019]
- [ ] T027 全量名字级回归：用 `SPECKIT_PYTHON=<§ Environment Prerequisites（2026-10-21）的 pytest 解释器> bash scripts/bash/run-tests.sh --names-out /tmp/065a-current-failed.txt -q` 运行全量套件，并与 T001 按其 owner 形态捕获的失败名基线做 `comm -13`（比较形态 owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs）；要求零 NEW 失败；命令、计数与差集写入 `.specify/specs/065a-state-awareness/verification.md`。 [blockedBy: T025]
- [ ] T028 写 SC 证据矩阵：在 `.specify/specs/065a-state-awareness/verification.md` 以 `- **SC-001**:` 至 `- **SC-006**:` 逐条给出状态、度量命令、真实输出摘要与证据路径（事故回放、确定性 diff、误报计数、watcher/Registry 回归、镜像/文档/依赖、逆样本与变异）；无法测量的量显式记 `not-evaluated`，不得手填。 [blockedBy: T026,T027]
- [ ] T029 只读与范围审计：用 `git status --short` 与 `git diff --stat` 证明 `.specify/skills/sdd-loop-driver/` 的改动仅来自 `sync-mirrors.py` 再生成且与源字节一致，未改动 066/067/068 目录、`.specify/specs/065-loop-interruption-recovery/`、`watch-target.sh`、`line-registry.py`、命令模板与 `pyproject.toml`；确认无 daemon/外部依赖、无 push/merge/kill/删除，且 `--out` 之外无写入（mtime 审计）；结论写入 `.specify/specs/065a-state-awareness/verification.md`。 [blockedBy: T025]
- [ ] T030 收口复验全部 Completion Gate：逐条运行 GATE-1 至 GATE-7 的 check 命令，把命令、退出码与关键输出追加到 `.specify/specs/065a-state-awareness/verification.md`；任一失败不得声称完成，按失败项修复后重跑。 [blockedBy: T028,T029]

**Checkpoint**: 变异演练可复现、全量回归零 NEW 失败、六条 SC 与四条 US5 均有测量证据、全部 GATE 通过。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **Foundational (Phase 2)**: 依赖 Setup；阻塞全部用户故事。
- **User Story 1 (Phase 3)**: 依赖 Foundational；是 MVP。
- **User Story 2 (Phase 4)**: 依赖 US1 的引擎、reference 与文档改动；其测试与文档可在 US1 收口后开始。
- **Polish (Phase 5)**: 依赖 US1 与 US2 完成。

### User Story Dependencies

- **US1 (P1)**: 无其它故事依赖；独立测试为两个新增测试文件加 `quickstart.md` §2–§6/§8。
- **US2 (P2)**: 依赖 US1 的产物存在（镜像再生成需要最终引擎与 reference），但兼容性结论独立于 US1 的功能断言。

### Within Each User Story

- 测试必须先写并失败，再实现；三个 US1 单元测试行写同一文件，按 T005 → T006 → T007 顺序执行，不得并行。
- 引擎实现行都写同一文件 `skills/external/sdd-loop-driver/scripts/loop-state.py`，按 T009 → T017 顺序执行。
- `T018` 只写 `references/state-awareness.md`，可与 T012–T017 并行（`[P]`），但必须在 T011 之后。
- US2 的 T020 与 T021 都向 `notes/red-first-evidence.md` 追加红跑记录，按 T020 → T021 顺序执行。

### Parallel Opportunities

- T001 与 T002 可并行（写不同文件）。
- T018 可与 T012–T017 并行（写不同文件，且 T011 已完成）。
- 其余实现行因共享 `loop-state.py` 或共享证据文件，不标 `[P]`。

---

## Parallel Example

```bash
# Setup: 两条基线互不覆盖
Task: "T001 捕获改前基线到 notes/pre-change-measurements.md"
Task: "T002 冻结 coverage-baseline.txt"

# US1: reference 与引擎实现并行（T011 完成后）
Task: "T012 实现 watcher 委托"
Task: "T018 编写 references/state-awareness.md"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: 仅 User Story 1（P1）。它单独交付“一次调用看清一条线的真实状态”的完整价值，并由 T019 独立验收。

1. 完成 Phase 1（Setup）与 Phase 2（Foundational）。
2. 完成 US1 的测试先写 → 实现 → T019 实证。
3. **STOP and VALIDATE**: 按 US1 checkpoint 独立验收，再进入 US2。

### Incremental Delivery

1. Setup + Foundational → CLI/信封骨架可测。
2. US1 → 快照引擎与六类检测可用（MVP）。
3. US2 → 镜像、文档与兼容性验收收口。
4. Polish → 变异演练、全量回归、SC 证据与 Gate 复验。

---

## Notes

- `[P]` 仅表示可并行，不表示可跳过依赖；带 `blockedBy` 的行必须在被列任务全部 `[X]` 后开始。
- 本切片只实现 `snapshot`、`--probe`、`--self-test`；`recover` 与 `check-spine` 只返回结构化拒绝，执行路径、并发锁、`heartbeat-stalled`、`lifecycle-spine-violation` 不进入本切片。
- 契约条款使用规范 `C-1`…`C-60`；`LS`/`SN`/`IA`/`AM` 为别名。60 条条款由 `[green:]` 在 T003/T004/T007/T011 完整认领（原因见 § Format），并由 `account-clause-coverage.py` 核对 claimed=60、FR 25/25。
- 工作树中的驱动技能文件已含外部同步产生的未提交改动；实现只做增量编辑，不得回退、重排或整文件重写。
- `test-evidence/` 是驱动侧证据通道，本切片任务不写、不提交；`notes/`、`verification.md`、`coverage-baseline.txt` 是本切片的证据落点。
- 快照只读：不得写状态脊、四件套、Registry 或工作树；`--out` 是唯一写路径且不得落在 `state_dir` 或 `repo` 内。
- 任何流程不 push、不合并、不删除分支、不 kill 进程、不删除证据；清理只能是显式动作，隔离只能是移动。
- `pre-analyze-check` 的 `missing-path` advisory 在实现前是预期（新文件尚未创建）；`error` 必须为 0。
