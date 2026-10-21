# Tasks: 状态感知（State Awareness）— Feature 065 / Slice 066

**Requirement ID**: 066（Feature 065 的切片 A）
**Requirement Key**: `066-loop-state-awareness-a`
**Branch**: `065-loop-interruption-recovery`（父特性线；切片规格目录 `066-loop-state-awareness-a`）
**Related Feature**: Feature 065 — SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery），状态 `Planned`
**Input**: `.specify/specs/066-loop-state-awareness-a/` 的 plan.md、requirements.md、research.md、data-model.md、contracts/ ×4、quickstart.md、feature-ref.md、notes/parent-fr-mapping.md
**Prerequisites**: plan.md（required）、requirements.md（required）、research.md、data-model.md、contracts/、quickstart.md、feature-ref.md；父特性 `.specify/specs/065-loop-interruption-recovery/requirements.md` 与 `notes/plan-blocked-review.md` 只读引用

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating — pure functions/utilities MUST have unit tests, critical flows MUST have automated regression coverage, integration/contract tests MUST cover external APIs; this slice ships executable Python, so the template-only Partial gate does not apply)

**Tests**: 每条新增行为先写红测试再实现；逆样本、具名夹具与三项变异演练属于交付面（FR-020、SC-007）。失败测试名基线按 `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 的 owner 形态捕获与比较，本文件不复述其路径、参数或比较形式。

**Organization**: 按用户故事组织：US1（P1，只读快照引擎、八类中断注释与动作建议）是 MVP；US2（P2，既有语义与分发面不回归，承接拆分记录要求每切片执行的兼容性验收）。Setup 冻结改前基线；Foundational 交付两个故事共同依赖的 CLI/信封/退出码骨架；Polish 收口 quickstart、变异演练、SC 证据矩阵与 Completion Gate 复验。

## Definition of Done (DoD)

- DoD-1: 所有任务行为 `[X]`；如有 `[~]`，理由记录在 `.specify/specs/066-loop-state-awareness-a/verification.md` 的 `deferred_tasks=`。
- DoD-2: `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `snapshot`、`--probe`、`--self-test`，对 `recover`/`check-spine` 返回结构化拒绝（exit 2）；全部执行路径只读（显式 `--out` 除外）。
- DoD-3: 4 份契约的 92 条条款（CLI 20 / SNP 30 / RUL 30 / CMP 12）逐条有测试或 owner reference 落点；§ Requirement Coverage Map 与 § Contract Coverage Map 保持当前。
- DoD-4: 新增 `tests/unit/test_loop_state_engine.py`、`tests/contract/test_sdd_loop_driver_state_awareness.py`、`tests/integration/test_loop_state_snapshot_matrix.py` 与更新后的 `tests/contract/test_sdd_loop_driver_skill.py` 全绿，且相对 T001 基线零 NEW 失败。
- DoD-5: 源与运行时镜像字节一致（`SKILL.md`、`references/state-awareness.md`、`scripts/loop-state.py` 三对）；`sync-mirrors.py --check` 相对 T001 基线无新增漂移。
- DoD-6: `.specify/specs/066-loop-state-awareness-a/verification.md` 以 `- **SC-001**:` 至 `- **SC-008**:` 列出八条成功标准的状态、命令、输出与证据；`notes/quickstart-run.md` 与 `notes/mutation-drills.md` 提供 quickstart 与变异演练的真实记录。
- DoD-7: 文档取值与代码一致：`references/state-awareness.md`、`SKILL.md`、`docs/reference/skills/sdd-loop-driver.md` 均含入口、调用形态与 watcher/Registry 关系，且与 `--help` 一致；owner reference 不含 watcher 阈值数值，不声称 `recover`/`check-spine` 已实现。
- DoD-8: 范围审计通过：未改动 `watch-target.sh`、`line-registry.py`、`references/watch-model.md`、`references/stage-prompts.md`、`references/efficiency-model.md`、命令模板与依赖清单；无 daemon、无 push/merge/kill/删除。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/066-loop-state-awareness-a/tasks.md` exit 0。
- GATE-2: 跨产物无漂移 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/066-loop-state-awareness-a --stage tasks --repo .` 输出含 `decision=pass`。
- GATE-3: 新增与扩展测试全绿 — check: 用 § Environment Prerequisites（2026-10-21）记录的 pytest 解释器运行 `tests/unit/test_loop_state_engine.py`、`tests/contract/test_sdd_loop_driver_state_awareness.py`、`tests/integration/test_loop_state_snapshot_matrix.py`、`tests/contract/test_sdd_loop_driver_skill.py`、`tests/unit/test_line_registry_engine.py`、`tests/unit/test_decomposition_check.py`，exit 0 且零 NEW 失败。
- GATE-4: watcher 判定零回归 — check: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` exit 0 且汇总含 `0 failed`，且 `shasum -a 256` 等于 CMP-01 钉住值。
- GATE-5: 镜像字节一致 — check: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` exit 0，且三对源/镜像逐一 `cmp` exit 0。
- GATE-6: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/066-loop-state-awareness-a/tasks.md` 返回 0。
- GATE-7: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-8]\*\*' .specify/specs/066-loop-state-awareness-a/verification.md` 返回 8。
- GATE-8: 受保护面未改动 — check: `git diff --name-only` 不包含 `watch-target.sh`、`line-registry.py`、`watch-model.md`、`stage-prompts.md`、`efficiency-model.md`、命令模板或依赖清单。

## Environment Prerequisites

- Python 语法目标（>=3.8）: **available** — probe: `python3 --version` → `Python 3.9.6` @ 2026-10-21; affected: 全部引擎任务（T004–T021）；`loop-state.py` 必须保持 Python 3.8 语法兼容。
- pytest 运行器: **partial** — probe: `python3 -m pytest --version` → `No module named pytest`；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` → `pytest 9.1.1` @ 2026-10-21; affected: T006–T010、T022–T023、T028、T031–T032、GATE-3；处置: 测试命令一律使用该解释器；`No module named pytest` 判 probe failure，不得记空基线。
- git: **available** — probe: `git --version` → `git version 2.54.0 (Apple Git-157)` @ 2026-10-21; affected: T001、T014、T033。
- watcher 自测: **available** — probe: `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` → `SELF-TEST: 38 passed, 0 failed`，exit 0 @ 2026-10-21; affected: T019、T028、GATE-4。
- 镜像基线: **clean** — probe: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` → `ok skills/external/ == .specify/skills/ (26 files)`，exit 0 @ 2026-10-21; affected: T001、T027、GATE-5；判据是“相对该基线无新增漂移”，不是绝对零漂移。
- 外部环境（容器/集群/网络）: **none** — 本切片全部检查为本地文件、`git` 与本地 watcher 子进程，无 docker、镜像仓库、实集群或远程网络依赖 @ 2026-10-21; affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同一阶段内其它 `[P]` 行并行（写目标不同、无未完成依赖）。
- **[Story]**: 用户故事标签（`[US1]` / `[US2]`），仅用户故事阶段的任务携带。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列出的任务全部 `[X]` 前不得开始本行。存在具体依赖时用它替代散文式“depends on”。
- **契约绿点**: 本切片契约使用 `CLI`/`SNP`/`RUL`/`CMP` 条款编号，`.specify/scripts/python/clause_extract.py` 只识别 `C-<n>` 形式，声明 `[green: contracts/<file>#CLI-01]` 会被 `validate-tasks.py` 判 `green-dangling`；因此绿点归属由 § Requirement Coverage Map、§ Contract Coverage Map 与对应测试行承担，不使用 `[green:]` 标签。
- 每行必须单行完成（含文件路径），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed；`- [X]` — Closed；`- [~]` — Deferred（理由须记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **Framework source（编辑面）**: `skills/external/sdd-loop-driver/`、`tests/`、`docs/reference/skills/sdd-loop-driver.md`。
- **Generated mirrors（生成面，禁止手改）**: `.specify/skills/sdd-loop-driver/`，仅由 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 再生成。
- **Feature evidence**: `.specify/specs/066-loop-state-awareness-a/` 下的 `notes/`、`verification.md`、`coverage-baseline.txt`；`test-evidence/` 是驱动侧证据通道，本切片任务不写、不提交。
- **Read-only isolation**: `.specify/specs/065-loop-interruption-recovery/`、`.specify/specs/065a-state-awareness/`、`.specify/memory/feedback/`、`.specify/memory/session/`、`.specify/memory/exec-quant/`、`.specify/memory/evidence/`、`.specify/memory/features*` 一律只读。
- **既有未提交改动**: `skills/external/sdd-loop-driver/` 与 `tests/contract/test_sdd_loop_driver_skill.py`、`docs/reference/skills/sdd-loop-driver.md` 已含外部同步产生的未提交改动；实现只做增量编辑，不得回退、重排或整文件重写这些改动。

## Measured Premises (re-measured at generation time 2026-10-21)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 切片 FR 定义数 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*' .specify/specs/066-loop-state-awareness-a/requirements.md` | 25（拆分门上限 30） |
| 切片 SC 定义数 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*' .specify/specs/066-loop-state-awareness-a/requirements.md` | 8 |
| 契约条款定义数 | `grep -cE '^- \*\*(CLI\|SNP\|RUL\|CMP)-[0-9]{2}\*\*' .specify/specs/066-loop-state-awareness-a/contracts/*.md` | `snapshot-cli.md` 20、`snapshot-schema.md` 30、`awareness-rules.md` 30、`compatibility-and-tests.md` 12；合计 92 |
| 契约条款数（naive 变体，勿用） | `grep -ohE '(CLI\|SNP\|RUL\|CMP)-[0-9]{2}' .specify/specs/066-loop-state-awareness-a/contracts/*.md \| wc -l` | 96 —— 把散文引用计入，与条款定义数不一致 |
| 任务行数 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/066-loop-state-awareness-a/tasks.md` | 33（红线 ≤40） |
| 任务行数（naive 变体，勿用） | `grep -ohE 'T[0-9]{3}' .specify/specs/066-loop-state-awareness-a/tasks.md \| wc -l` | 278 —— 把 `blockedBy` 引用与正文提及计入，与任务行定义数不一致 |
| 具名夹具数 | `python3 -c "import re;l=[x for x in open('.specify/specs/066-loop-state-awareness-a/contracts/compatibility-and-tests.md').read().splitlines() if x.startswith('- **CMP-07**')][0];print(len(re.findall(r'\x60([^\x60]+)\x60',l)))"` | 18 |
| 具名夹具数（naive 变体，勿用） | `grep -oE '`[a-z0-9-]+`' .specify/specs/066-loop-state-awareness-a/contracts/compatibility-and-tests.md \| sort -u \| wc -l` | 28 —— 把文件内其它反引号 token 计入，与 CMP-07 的夹具清单不一致 |
| watcher 基线 | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | `SELF-TEST: 38 passed, 0 failed`，exit 0 |
| watcher SHA-256 | `shasum -a 256 skills/external/sdd-loop-driver/scripts/watch-target.sh` | `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4` |
| 兼容测试基线 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py tests/unit/test_line_registry_engine.py tests/unit/test_decomposition_check.py` | `108 passed in 37.38s` |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (26 files)`，exit 0；naive 变体 `find skills/external/sdd-loop-driver -type f \| wc -l` = 27，差 1 为 `__pycache__` |
| 引擎与 reference 尚不存在 | `ls skills/external/sdd-loop-driver/scripts/loop-state.py skills/external/sdd-loop-driver/references/state-awareness.md` | 两个路径均返回 `No such file or directory` |

`missing-path` 类 advisory 在实现前属于预期（新文件尚未创建），不构成 blocking；`error` 必须为 0。

## Requirement Coverage Map

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T003、T004、T022、T033 |
| FR-002 | T006、T011、T012 |
| FR-003 | T003、T006、T008、T018、T020 |
| FR-004 | T007、T012、T015 |
| FR-005 | T008、T010、T011、T019 |
| FR-006 | T007、T014、T024 |
| FR-007 | T007、T014、T016 |
| FR-008 | T007、T014 |
| FR-009 | T008、T017、T024 |
| FR-010 | T007、T013、T024、T025 |
| FR-011 | T007、T013、T017 |
| FR-012 | T003、T021 |
| FR-013 | T023、T028 |
| FR-014 | T028 |
| FR-015 | T028、T033 |
| FR-016 | T028、T033 |
| FR-017 | T027 |
| FR-018 | T023、T024 |
| FR-019 | T025、T026 |
| FR-020 | T008、T030 |
| FR-021 | T008、T020 |
| FR-022 | T003、T008、T033 |
| FR-023 | T003、T008、T033 |
| FR-024 | T008、T016、T018 |
| FR-025 | T026、T028、T033 |
| SC-001 | T009、T010、T022、T029 |
| SC-002 | T008、T009、T031 |
| SC-003 | T007、T008、T009、T010 |
| SC-004 | T008、T009、T016、T022 |
| SC-005 | T023、T028 |
| SC-006 | T026、T027、T028 |
| SC-007 | T009、T010、T030 |
| SC-008 | T008、T009、T018、T022 |

## Contract Coverage Map

| Contract | Clauses | Owning tasks |
|----------|---------|--------------|
| `contracts/snapshot-cli.md` | CLI-01…CLI-20 | T003、T004、T005、T006、T011、T019、T020、T022 |
| `contracts/snapshot-schema.md` | SNP-01…SNP-30 | T003、T007、T008、T013、T020 |
| `contracts/awareness-rules.md` | RUL-01…RUL-30 | T006、T007、T008、T012、T013、T015、T016、T017、T018、T019、T024 |
| `contracts/compatibility-and-tests.md` | CMP-01…CMP-12 | T009、T010、T021、T023、T027、T028、T030、T033 |

## Named Fixtures

CMP-07 的 18 个具名夹具由测试文件自身枚举；两个套件共同覆盖全集，单个套件只枚举其可执行的子集：

| Fixture | Primary suite |
|---------|---------------|
| `sentinel-with-missing-artifact` | contract + integration |
| `legacy-spine-snapshot` | contract |
| `artifacts-without-completion` | contract |
| `dead-no-exit-record` | contract |
| `unwatched-vs-window` | contract + integration |
| `registry-missing` | contract |
| `registry-present-spine-missing` | contract |
| `registry-present-spine-missing-with-watcher-verdict` | contract + integration |
| `not-dispatched` | contract |
| `probe-snapshot` | contract + integration |
| `stale-run` | contract |
| `foreign-carrier` | contract |
| `deadline-overrun-live` | contract |
| `heartbeat-stalled` | contract |
| `accident-replay` | contract + integration |
| `salvage-two-state` | contract |
| `implement-commit-missing` | contract + integration |
| `resume-commit-missing` | contract + integration |

## Feature Review (tasks phase)

- 任务拆解未暴露新的 Feature，也未使既有 Feature 失效；切片 A 仍归属 Feature 065，状态保持 `Planned`。
- 本命令不修改 `.specify/memory/features.md` 或 `.specify/memory/features/065.md`；Feature 状态转移与索引更新留给实现/评审阶段的既有程序。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结改前基线、契约覆盖基线与红先证据落点，让后续每条“与改前对比”的前提都有日期化依据。

- [ ] T001 创建 `.specify/specs/066-loop-state-awareness-a/notes/` 并把改前基线写入 `notes/pre-change-measurements.md`：`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` 的汇总行、`shasum -a 256 skills/external/sdd-loop-driver/scripts/watch-target.sh`、`python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 的漂移集、带 § Environment Prerequisites（2026-10-21）解释器的四文件 pytest 基线、以及 `git status --short -- skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver docs/reference/skills/sdd-loop-driver.md tests/contract/test_sdd_loop_driver_skill.py` 的快照；失败测试名基线按 `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 的 owner 形态捕获（本行只指向 owner，不复述其路径/参数/比较形式）。
- [ ] T002 [P] 冻结契约覆盖基线：在仓库根运行 `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/066-loop-state-awareness-a --freeze > .specify/specs/066-loop-state-awareness-a/coverage-baseline.txt`，核对首行以 `# coverage-baseline:` 起首且 `frozen-from:` 排除 `066-loop-state-awareness-a`；在 `notes/pre-change-measurements.md` 记录“本切片契约使用 `CLI/SNP/RUL/CMP` 编号，被脚本归入 md-none（named-unparseable），条款覆盖改由 § Contract Coverage Map 与测试行承担”，不得伪造空的逐条款覆盖。

**Checkpoint**: 改前基线与覆盖基线已落盘；每个“与改前对比”前提都有日期化基线。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 交付两个用户故事共同依赖的 CLI 面、退出码阶梯、共享 JSON 信封、只读边界与 `--out` 唯一写路径。

**⚠️ CRITICAL**: 本阶段完成前，用户故事阶段不得开始。

- [ ] T003 红先编写 CLI/信封契约测试到 `tests/contract/test_sdd_loop_driver_state_awareness.py`：`--help` 的 `0/1/2` 阶梯与“watcher 判定码只作数据”、`--action snapshot` 唯一实现动作、`recover`/`check-spine` 的结构化拒绝（`schema_version=1`、`applied=false`、`result="refused"`、`reason="action-not-available-in-slice"`、exit 2）、`--out` 原子写与落在 `state_dir`/`repo worktree` 内时 exit 2、快照只读（无 `--out` 时夹具树哈希不变）；运行并把失败输出（命令、真实输出、退出码）写入 `.specify/specs/066-loop-state-awareness-a/notes/red-first-evidence.md`。
- [ ] T004 实现 `skills/external/sdd-loop-driver/scripts/loop-state.py` 的 CLI 骨架与共享进程契约：`--action snapshot|recover|check-spine`、`--self-test` 与 `--line-id/--stage/--spine/--state-dir/--spec-dir/--repo/--probe/--watch-script/--salvage-evidence/--sentinel/--no-sentinel/--start-grace/--deadline-grace/--heartbeat-max-age/--retry-limit/--attempt/--out` 参数面；`--help` 列出三动作、全部参数与 `0/1/2` 退出阶梯；两个保留动作返回共享信封拒绝；顶层信封组装；仅标准库、Python 3.8 语法。 [blockedBy: T003]
- [ ] T005 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现只读边界与 `--out`：所有读取路径不写状态脊/载体/watchbeat/Registry/工作树；`--out` 解析为绝对路径后若落在已解析的 `state_dir` 或 `repo` 内则 exit 2，否则同目录临时文件加原子替换，并仍向 stdout 打印同一 JSON；不得启动 daemon、后台进程或网络监听。 [blockedBy: T004]

**Checkpoint**: `--help`、退出码阶梯、拒绝信封、只读边界与 `--out` 可由契约测试验证；US1 可以开始。

---

## Phase 3: User Story 1 - 一次调用看清一条线的真实状态 (Priority: P1) 🎯 MVP

**Goal**: 一次只读 `snapshot` 调用聚合状态脊、Registry、四件套、watchbeat、阶段产物、git 提交与可用 watcher 判定，识别八类中断形态（只注释）并给出唯一恢复动作建议；`completion` 独立于 `loop_state`。

**Independent Test**: 用夹具构造“产物齐备、未提交、`exit=1`、无哨兵、无 watcher”的线、正常运行中的线、未派发的线、以及“哨兵在而产物缺”的线，分别调用快照并核对 `loop_state`、`verdict_source`、`completion`、`interruptions[]`、`recovery_action`、证据指针与缺失信号语义；再运行三个新增测试文件。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T006 [P] [US1] 红先编写单元测试到 `tests/unit/test_loop_state_engine.py`：输入解析优先级（显式 `--spine/--state-dir/--spec-dir/--repo` → Registry → `missing`/`unknown`，无 CWD 回退）、Registry 目录解析与 `line-registry.py` 的三案例对齐、`registry.status=found/missing/unreadable/invalid` 四值不合并、Registry 缺失继续求值、v1 机读段与 legacy 脊降级、`registry-present-spine-missing`（有/无 watcher 判定两态）、`not-dispatched` 谓词与派发证据互斥；把红跑输出追加到 `.specify/specs/066-loop-state-awareness-a/notes/red-first-evidence.md`。 [blockedBy: T005]
- [ ] T007 [US1] 红先扩展 `tests/unit/test_loop_state_engine.py`：信封优先归属（`own/stale-run/foreign/unattributed` 与 `stale_signals[]` 的 `run-id-mismatch/before-stage-start/stage-mismatch/unprovable-envelope/legacy-stale`）、watchbeat 路径与新鲜度（`fresh/stale/missing/unknown`，正常窗口不误报）、八阶段产物映射（含 plan 六件套与 clarify/analyze 例外）、产物“存在且非空”（目录至少一个非空 `.md`）、`stage_base_commit` 基线的提交/未提交证据、`effective` 五项来源与 unknown 语义、derived D1–D11、`spine.consistent` 三态；记录红跑。 [blockedBy: T006]
- [ ] T008 [US1] 红先扩展 `tests/unit/test_loop_state_engine.py`：completion 表与伪完成、中断形态 I1–I8 的正/逆样本且均不覆盖 `loop_state`、动作表 A1–A10（重试上限守卫、同线 `stale-run` 守卫、活进程 TIMEOUT 只 `watch`）、salvage 两态（无输入 `retry`/有输入 `resume` 候选）、watcher 不可用与 probe 判定采用、`foreign` 载体不驱动 `retry`、两次同输入除 `evaluated_at` 外逐字相等、无 `--out` 时无写入；记录红跑。 [blockedBy: T007]
- [ ] T009 [US1] 红先编写契约套件 `tests/contract/test_sdd_loop_driver_state_awareness.py`：按 CLI/SNP/RUL/CMP 条款分区逐条断言，钉住 watcher SHA-256 `b6a275…f2b0b4` 与 `--help`/`--self-test` 的 `0/1/2` 阶梯，枚举 § Named Fixtures 的纯夹具子集（事故回放、伪完成、legacy 脊、未派发、probe、Registry 三态、stale/foreign、dead-no-exit-record、deadline-overrun-live、heartbeat-stalled、salvage 两态、两种 resume/commit-missing），并包含确定性 diff；记录红跑。 [blockedBy: T003,T005]
- [ ] T010 [US1] 红先编写集成套件 `tests/integration/test_loop_state_snapshot_matrix.py`：真实 `watch-target.sh --once` 的 `loop_state` 逐字采用、真实 `git commit`/未提交证据、probe 缺字段不回退本地同名文件、无 `--out` 快照前后夹具树哈希相等、`--out` 仅新增输出文件；枚举其可执行的 § Named Fixtures 子集并在源文件内写明夹具名；记录红跑。 [blockedBy: T005]

### Implementation for User Story 1

- [ ] T011 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现输入解析与只读投影：按 CLI-06…CLI-13 解析 `line_id/run_id/stage/spine/state_dir/spec_dir/repo`，读取 `<registry-dir>/<line>.json`（`SPECIFY_LINE_REGISTRY_DIR → XDG → HOME`），输出 `registry.status/entry/pointer/error`，校验 `--probe` 的 `schema_version=1` 并装载 probe 证据；缺失值记 `missing`/`unknown`，不猜路径、不填默认值。 [blockedBy: T006,T009]
- [ ] T012 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现状态脊解析与前置裁决：解析 `<!-- loop-state:begin -->`…`<!-- loop-state:end -->` 的 `spine_schema: v1` 与 `spine_` 前缀键，legacy 兜底识别 `**current_stage**`/`**tries**`/`**state**` 与显式 `stage_started_at`/`stage_deadline_epoch`/`stage_base_commit`/`last_verdict` 行；实现 Registry/spine 优先级与 `not-dispatched` 谓词（注册 `run_id` 单独不算派发证据）；缺字段记 `"unknown"`。 [blockedBy: T006,T009]
- [ ] T013 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现载体归属与 watchbeat：status/pid/log/heartbeat 的信封解析与 `own` 唯一裁决（`line=`/`run=`/`stage=` 全匹配），非 own 只进入 `stale_signals[]`；legacy 模式仅限可读 Registry 证明恰有一条活动线；watchbeat 路径 `<state-dir>/watchbeat-<line>-<stage>`，新鲜度用标记自身 `at`（无效回退 mtime）+ `window` + `effective.deadline_grace`，不输出年龄数字。 [blockedBy: T007,T009]
- [ ] T014 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现八阶段产物映射与提交证据：`requirements/clarify/plan/tasks/checklist/analyze/implement/review` 的 `required`/`commit_required`/`no_change_allowed`/`sentinel`/`commit_scope` 数据表（plan 六件套、clarify 条件提交、analyze 不要求提交、implement 非 `.specify/` 提交）；产物完整性只按“文件存在且非空”判定；提交证据以 `spine_stage_base_commit` 为唯一基线，缺失记 `commit=unknown`，`commit_required=false` 记 `not-applicable`，未提交清单用 `git status --porcelain --untracked-files=all`。 [blockedBy: T007,T009]
- [ ] T015 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 `effective` 解析与 derived 映射：每个值按 CLI → probe → spine → 阶段映射（仅哨兵）→ watcher `--help`（仅阈值）解析并标注来源，不可得记 `"unknown"`；实现 D1–D11 固定优先级、`spine.consistent` 三态字符串、`start_anchor` 取 `stage_started_at` 或最早可归属载体 mtime；不得嵌入 watcher 阈值字面量。 [blockedBy: T011,T012,T013,T014]
- [ ] T016 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现独立 completion 表：未派发 `not-applicable`；`exit≠0` `incomplete`；哨兵在且产物齐备且（无退出记录或 `exit=0`）`complete`；哨兵在产物缺 `incomplete`；产物齐备哨兵缺 `incomplete`；`--no-sentinel` 时 `exit=0` + 产物齐备 `complete`；哨兵配置未知或产物不可评估 `unknown`；伪完成只改 `completion`，绝不改写 `loop_state`。 [blockedBy: T015]
- [ ] T017 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现八类中断形态 I1–I8（`unwatched`、`dead-no-exit-record`、`deadline-overrun-live`、`heartbeat-stalled`、`artifacts-without-completion`、`stale-signal`、`lifecycle-spine-violation`、`remote-unreachable`）：每条含 `form/evidence[]/detail/attribution`，按 I1–I8 与归属顺序稳定排序；所有形态只注释，MUST NOT 设置或覆盖 `loop_state`；`dead-no-exit-record` 要求无哨兵，`unwatched` 的 `unknown` 新鲜度不触发。 [blockedBy: T013,T016]
- [ ] T018 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 salvage 输入与动作表 A1–A10：`--salvage-evidence`（可重复、只读）或状态脊 `spine_salvage: accepted` + evidence + at 作为裁决前输入；按固定顺序输出唯一 `recovery_action` 与 `recovery_reason`，实现重试上限守卫（`attempt`/`retry_limit` 任一 unknown 时跳过并记 `retry-limit-unknown`）、同线 `stale-run` 守卫（运行中保留 `watch`、已完成保留 `verify`/`resume`）、活进程 TIMEOUT 只 `watch`、`isolation_required` 仅同线 stale-run retry 为 true。 [blockedBy: T016,T017]
- [ ] T019 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现 watcher 委托与 probe 判定：仅在有活动 target 且非 probe 判定时以有界子进程运行 `watch-target.sh --once`，传入解析后的 pid/status/log/heartbeat/sentinel/envelope/registry/deadline/effective；解析 `WATCH`/`EVIDENCE` 行；watcher 缺失、超时、非判定退出码或无 `WATCH` 行时输出 `watch_status="unavailable"`、`watch_verdict=null`，绝不复用 10–16 或伪造判定；probe 携带 `watch_status=available` + 非空 `watch_verdict` 时逐字采用。 [blockedBy: T011,T012]
- [ ] T020 [US1] 在 `skills/external/sdd-loop-driver/scripts/loop-state.py` 实现快照收口：按 SNP-01…SNP-30 组装顶层字段（含 `watch` 对象、`spine.fields` 四键、`evidence` 七键、`effective` 六键、`salvage`、`interruptions[]`、`missing_artifacts`/`uncommitted_artifacts`、`stale_signals[]`），固定列表顺序，只输出 `evaluated_at` 一个时间字段，stdout 恰好一个 JSON、诊断走 stderr；同一输入除 `evaluated_at` 外 canonical JSON 逐字相等。 [blockedBy: T015,T016,T017,T018,T019]
- [ ] T021 [US1] 扩展 `--self-test`（`skills/external/sdd-loop-driver/scripts/loop-state.py`）覆盖 CMP-10：全部适用中断形态、stale/foreign/unattributed 污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、活 TIMEOUT、legacy 脊、remote-unreachable、`registry.status=missing/unreadable/invalid`、`registry-present-spine-missing` 有/无 watcher 判定、`not-dispatched`、`retry_limit`/`attempt` unknown、probe 快照、“形态不覆盖 `loop_state`”、foreign 不驱动 `retry`、退出阶梯 `0/1/2`；逐例打印 `ok <case>` 或 `FAIL <case> — <detail>`，末行 `SELF-TEST: <n> passed, <m> failed`，仅当 `m=0` exit 0；不得声称 recover 锁/拒绝路径。 [blockedBy: T020]

### Verification for User Story 1

- [ ] T022 [US1] 跑绿并实证 US1：用 § Environment Prerequisites（2026-10-21）的 pytest 解释器运行 `tests/unit/test_loop_state_engine.py tests/contract/test_sdd_loop_driver_state_awareness.py tests/integration/test_loop_state_snapshot_matrix.py -q`，并运行 `python3 skills/external/sdd-loop-driver/scripts/loop-state.py --self-test`；把红→绿的命令、输出与退出码追加到 `.specify/specs/066-loop-state-awareness-a/notes/red-first-evidence.md`；发现漂移在本行内修正并重跑。 [blockedBy: T021]

**Checkpoint**: US1 可独立验收：单次快照给出完整聚合、八类形态注释、唯一动作建议、独立 completion，且 `--self-test`、probe 与只读边界符合契约。

---

## Phase 4: User Story 2 - 既有语义与分发面不回归 (Priority: P2)

**Goal**: 升级后既有 watcher 判定、四件套格式、Line Registry、阶段命令、确认门与 fast-fail 纪律保持原样；框架源、运行时镜像、owner reference 与文档一致，无新增常驻服务或外部依赖。

**Independent Test**: 运行既有 watcher `--self-test`、驱动技能契约测试、Registry 引擎测试与镜像一致性检查；逐条核对 US2 A1–A5 的五类不回归结论；核对 `state-awareness.md`/`SKILL.md`/docs 与 `--help` 取值一致。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T023 [P] [US2] 红先更新 `tests/contract/test_sdd_loop_driver_skill.py`：把 `references/state-awareness.md` 与 `scripts/loop-state.py` 加入 `MIRROR_FILES`；新增 docs 入口断言（read-only `skills/external/sdd-loop-driver/scripts/loop-state.py` 的入口、`snapshot`/`--probe`/`--self-test` 调用形态、与 watcher/Registry 的关系、只读边界、`recover`/`check-spine` 不可用）与 owner reference 断言（章节、`recovery_reason` 闭集、无 watcher 阈值数值、阶段映射表与代码数据一致）；运行镜像/文档断言并把失败输出追加到 `.specify/specs/066-loop-state-awareness-a/notes/red-first-evidence.md`。 [blockedBy: T022]
- [ ] T024 [P] [US2] 编写 owner reference `skills/external/sdd-loop-driver/references/state-awareness.md`：快照投影与字段闭域、derived D1–D11、归属裁决、completion 与 `loop_state` 分离、I1–I8 注释语义、`effective` 来源、`recovery_reason` 闭集、八阶段产物映射散文表、watchbeat 原子写形态与驱动者写入义务；用指针引用 `watch-model.md`/`stage-prompts.md`/`efficiency-model.md`，不复制 watcher 阈值数值，不声称 `recover`/`check-spine` 已实现。 [blockedBy: T022]
- [ ] T025 [US2] 更新 `skills/external/sdd-loop-driver/SKILL.md`：在 Hard Requirements 增加一条“快照只读、不得写脊/载体/工作树、不得停活进程”的硬要求，在 References 增加 `references/state-awareness.md` 指针；不新增 H2 章节，保持既有 H2 契约稳定；只做增量编辑并保留工作树中的未提交改动。 [blockedBy: T024]
- [ ] T026 [P] [US2] 更新文档入口 `docs/reference/skills/sdd-loop-driver.md`：新增状态感知小节，写清 read-only `skills/external/sdd-loop-driver/scripts/loop-state.py` 的入口、`snapshot`/`--probe`/`--self-test` 调用形态、与 watcher 和 Registry 的关系、只读边界，以及 `recover`/`check-spine` 在本切片不可用；取值以该脚本只读 `--help` 和 owner reference 为准。 [blockedBy: T022]

### Implementation for User Story 2

- [ ] T027 [US2] 再生成运行时镜像并验证：运行 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`，随后 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 相对 T001 基线无新增漂移，并对 `SKILL.md`、`references/state-awareness.md`、`scripts/loop-state.py` 三对源/镜像做 `cmp` 字节比较；禁止手改 `.specify/skills/sdd-loop-driver/`。 [blockedBy: T023,T024,T025,T026]
- [ ] T028 [US2] 运行兼容性回归并写入 `.specify/specs/066-loop-state-awareness-a/verification.md`：`bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`（`0 failed`）、watcher SHA-256 等于 CMP-01 钉住值、既有 `tests/contract/test_sdd_loop_driver_skill.py` 与 `tests/unit/test_line_registry_engine.py`/`tests/unit/test_decomposition_check.py` 全绿、Registry 旧条目可读且无写回、依赖清单无新增、无 daemon/外部服务、命令模板与 `stage-prompts.md` 写入时点未变；以 `- **US2-A1**:` 至 `- **US2-A5**:` 记录命令、输出与证据指针。 [blockedBy: T027]

**Checkpoint**: US2 可独立验收：既有测试全绿、镜像字节一致、文档与代码取值一致、五条兼容性验收均有证据。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实测、变异演练、确定性与只读证据、SC 矩阵、范围审计与 Completion Gate 复验。

- [ ] T029 [P] 执行 quickstart 并回填实测：按 `quickstart.md` 的 S1–S8 用真实夹具逐一运行 `snapshot`（没有 watcher 的用 `--probe` 或不可用路径），把命令、真实输出、退出码与拆卸步骤写入 `.specify/specs/066-loop-state-awareness-a/notes/quickstart-run.md`，并把 `quickstart.md` 中每个“not executable at plan time”替换为实测结果或记录不可执行原因；夹具不得泄漏进仓库。 [blockedBy: T022]
- [ ] T030 [P] 执行三项变异演练并记录到 `.specify/specs/066-loop-state-awareness-a/notes/mutation-drills.md`：把 `skills/external/sdd-loop-driver/scripts/loop-state.py` 复制到临时树，分别移除（a）无 watcher 检测、（b）completion 与 `loop_state` 分离、（c）中断只注释不覆盖；每项运行具名测试并确认至少一条转红，再从备份恢复并确认转绿；记录变异位置、命令、转红用例名与恢复结果；保持绿即记为 finding，不得记通过。 [blockedBy: T022]
- [ ] T031 [P] 收集确定性与只读证据并写入 `.specify/specs/066-loop-state-awareness-a/verification.md`：同一夹具两次快照、剔除 `evaluated_at` 后 canonical JSON diff 为 0；无 `--out` 时快照前后夹具树哈希相等；有 `--out` 时仅新增输出文件；缺失信号以 `missing`/`unknown` 出现且无零值/`ok` 猜测；记录命令、输出与证据路径。 [blockedBy: T022]
- [ ] T032 全量收口回归与 SC 证据矩阵：用 § Environment Prerequisites（2026-10-21）的 pytest 解释器运行新增三个套件加 `tests/contract/test_sdd_loop_driver_skill.py`、`tests/unit/test_line_registry_engine.py`、`tests/unit/test_decomposition_check.py`，与 T001 基线做名字级比较并要求零 NEW 失败；在 `.specify/specs/066-loop-state-awareness-a/verification.md` 以 `- **SC-001**:` 至 `- **SC-008**:` 逐条给出状态、度量命令、真实输出摘要与证据指针；无法测量的量显式记 `not-evaluated`，不得手填。 [blockedBy: T027,T031]
- [ ] T033 范围审计与 Completion Gate 复验：运行 GATE-1…GATE-8 的 check 命令；用 `git status --short` 与 `git diff --name-only` 证明未改动 `watch-target.sh`、`line-registry.py`、`watch-model.md`、`stage-prompts.md`、`efficiency-model.md`、命令模板与 `pyproject.toml`，镜像改动仅来自 `sync-mirrors.py`；确认无 push/merge/kill/删除/daemon，`--out` 之外无写入；把命令、退出码与关键输出追加到 `.specify/specs/066-loop-state-awareness-a/verification.md`。 [blockedBy: T032]

**Checkpoint**: quickstart 与变异演练可复现、确定性与只读证据齐备、八条 SC 均有测量证据、全部 GATE 通过。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **Foundational (Phase 2)**: 依赖 Setup；阻塞全部用户故事。
- **User Story 1 (Phase 3)**: 依赖 Foundational；是 MVP。
- **User Story 2 (Phase 4)**: 依赖 US1 的引擎、owner reference 与文档改动；兼容性结论独立于 US1 的功能断言。
- **Polish (Phase 5)**: 依赖 US1 与 US2 完成。

### User Story Dependencies

- **US1 (P1)**: 无其它故事依赖；独立测试为三个新增测试文件加 `quickstart.md` 的 S1–S8。
- **US2 (P2)**: 依赖 US1 的最终引擎与文档产物（镜像再生成需要最终文件），但五条兼容性验收可独立核对。
- **Polish**: 依赖 US1/US2；T032 依赖 T027（镜像已再生成）与 T031（确定性证据已落盘）。

### Within Each User Story

- 测试必须先写并失败，再实现；T006 → T007 → T008 写同一单元文件，按序执行，不得并行。
- T009 与 T010 分别写两个新测试文件，但都与 T006–T008 共享 `notes/red-first-evidence.md`，因此不标 `[P]`，按列表顺序执行。
- 引擎实现行都写同一文件 `skills/external/sdd-loop-driver/scripts/loop-state.py`，按 T011 → T021 顺序执行；其中 T011/T012 可先于 T013/T014，但 T015 必须等四者完成。
- US2 的 T023、T024、T026 写不同文件，可并行；T025 依赖 T024；T027 依赖前三者与 T025。
- Polish 的 T029、T030、T031 写不同证据文件，可并行；T032 依赖 T027 与 T031；T033 依赖 T032。

### Parallel Opportunities

- T001 与 T002 可并行（写不同文件）。
- T006 与 Foundational 完成后的 T009/T010 中的测试文件准备可并行，但因共享红先证据日志而不标 `[P]`。
- US2 的 T023/T024/T026 可并行（分别写既有契约测试、owner reference、docs 入口）。
- Polish 的 T029/T030/T031 可并行（quickstart 记录、变异记录、verification 证据）。

---

## Parallel Example: User Story 2

```bash
# 三条 US2 工作流写不同文件，可在 US1 收口后并行：
Task: "T023 更新 tests/contract/test_sdd_loop_driver_skill.py 的镜像与文档断言"
Task: "T024 编写 skills/external/sdd-loop-driver/references/state-awareness.md"
Task: "T026 更新 docs/reference/skills/sdd-loop-driver.md 的状态感知小节"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: 仅 User Story 1（P1）。它单独交付“一次调用看清一条线的真实状态”的完整价值，并由 T022 独立验收。

1. 完成 Phase 1（Setup）与 Phase 2（Foundational）。
2. 完成 US1 的测试先写 → 实现 → T022 实证。
3. **STOP and VALIDATE**: 按 US1 checkpoint 独立验收，再进入 US2。

### Incremental Delivery

1. Setup + Foundational → CLI/信封/退出码骨架可测。
2. US1 → 快照引擎、八类中断注释与动作建议可用（MVP）。
3. US2 → owner reference、SKILL/docs、镜像与兼容性验收收口。
4. Polish → quickstart 实测、变异演练、SC 证据、范围审计与 Gate 复验。

---

## Notes

- `[P]` 仅表示可并行，不表示可跳过依赖；带 `blockedBy` 的行必须在被列任务全部 `[X]` 后开始。
- 本切片只实现 `snapshot`、`--probe`、`--self-test`；`recover` 与 `check-spine` 只返回结构化拒绝（exit 2），执行路径、状态脊写入、恢复记录、隔离、恢复锁、handoff 与活进程停线决策不进入本切片。
- 契约条款编号为 `CLI`/`SNP`/`RUL`/`CMP`，不使用 `[green:]` 绿点标签（原因见 § Format）；条款覆盖由 § Contract Coverage Map 与测试行承担。
- 工作树中的驱动技能文件已含外部同步产生的未提交改动；实现只做增量编辑，不得回退、重排或整文件重写。
- `test-evidence/` 是驱动侧证据通道，本切片任务不写、不提交；`notes/`、`verification.md`、`coverage-baseline.txt` 是本切片的证据落点。
- 快照只读：不得写状态脊、四件套、watchbeat、Registry 或工作树；`--out` 是唯一写路径且不得落在 `state_dir` 或 `repo` 内。
- 任何流程不 push、不合并、不删除分支、不 kill 进程、不删除证据；清理只能是显式动作，隔离只能是移动。
- `pre-analyze-check` 的 `missing-path` advisory 在实现前是预期（新文件尚未创建）；`error` 必须为 0。
