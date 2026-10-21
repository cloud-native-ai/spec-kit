# Implementation Plan: 状态感知快照引擎（State Awareness Snapshot）— Feature 065 / Slice 065a

**Branch**: `065-loop-interruption-recovery` | **Date**: 2026-10-21 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `065a-state-awareness` → Feature 065 SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）
**Input**: Specification from `.specify/specs/065a-state-awareness/requirements.md`

## Summary

为 SDD 循环驱动技能增加一个确定性、只读的状态聚合入口 `loop-state.py`：一次 `snapshot` 调用聚合状态脊、Line Registry 条目、pid/status/log/heartbeat 四件套、watchbeat、阶段产物、git 提交与可用的 watcher 判定，输出统一 JSON 信封，识别六类中断形态，并给出唯一恢复动作建议（`none/watch/verify/resume/retry/stop`）。本切片只求值、不执行：不写脊、不提交、不隔离、不杀进程。退出码统一为 `0/1/2`，绝不复用 watcher 的 `10–16`。`recover` 与 `check-spine` 在本切片保留结构化拒绝分支：`recover` 由 `065c` 实现，`check-spine` 由 `065b` 实现（与 `notes/decomposition-gate.md` 一致）。

## Technical Context

**Language/Version**: Python 3，语法兼容 `>=3.8`（仓库 `pyproject.toml` 的下限），仅标准库。
**Primary Dependencies**: 无外部包。运行时消费既有 `watch-target.sh`（watcher 判定与阈值）、`line-registry.py`（Registry 条目）与 `git`（提交证据）；不修改它们的语义。
**Storage**: 文件系统——状态目录四件套 + watchbeat 标记、状态脊 markdown 机读段、Registry JSON；无数据库、无缓存服务。
**Testing**: `pytest`；新增 `tests/unit/test_loop_state_engine.py`（求值逻辑与夹具）与 `tests/contract/test_loop_state_contract.py`（信封、退出码、probe、自测、确定性、变异演练），并更新 `tests/contract/test_sdd_loop_driver_skill.py` 的镜像文件清单。
**Target Platform**: POSIX（macOS/Linux），与 runner 同一执行身份；无 GUI、无网络调用（watcher 为本地子进程）。
**Project Type**: 框架技能内的单文件引擎（既有 `sdd-loop-driver` 技能扩展），不新增顶层目录。
**Performance Goals**: 单次快照在一次进程内完成；最多一次有界的 `watch-target.sh --once` 子进程调用；无轮询、无 daemon。`--self-test` 不依赖真实进程或网络。
**Constraints**: 只读（`--out` 唯一例外且不得写入 state dir / 工作树）；零新依赖；Python 3.8 语法；输出除 `evaluated_at` 外逐字可复现；阈值不得在引擎内形成第二套默认值；退出码只用 `0/1/2`。
**Scale/Scope**: 每次调用一条线；8 个阶段、8 个信号块、8 类中断词表（本切片检测 6 类）；25 条切片功能需求、6 条成功标准。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（从 `.specify/memory/constitution.md` 的 `### <numeral>. <name>` 标题动态渲染，按出现顺序）：

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计决定回指 `requirements.md` 的 FR / clarify 裁决；FR-010 的驱动者写入侧按切片映射归 065b，本切片交付读取契约与消费（§Slice Landing Notes）。 |
| II | Feature-Centric Development | ✅ Pass | 复用 Feature 065、不新建 ID；Draft→Planned 由 `/speckit.plan` 与本阶段指令要求执行，与切片 requirements 的“不得改写注册状态”一句的差异已披露（§Disclosed Deviations）。 |
| III | Intent-Driven Development | ✅ Pass | `Summary` 先述价值与边界；`research.md` 每条裁决含被否方案与否决理由。 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` 的 60 条条款先于实现；Testing Strategy 为每个新检查配红先测试、逆样本、AM-01 映射一致性、拒绝信封与归属三态测试（SC-006）。 |
| V | AI Agent Integration Standards | ✅ Pass | 不触碰 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；无新增 agent CLI、配置键或 provider 面。 |
| VI | Continuous Quality & Observability | ✅ Pass | 统一 JSON 信封 + `schema_version` + 退出码阶梯 + `--self-test`；证据指针与 `value_state` 提供可观测性。 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本阶段只落地 `Planned`；`Implemented` 归 `/speckit.implement`；Feature 注册表按状态机推进。 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 信号格式、归属规则与阈值以 `watch-target.sh` / `stage-runner.sh` / `line-registry.py` 代码为准；已把“无 `run=` 信封在归属模式下被抑制”的代码事实写入 `LS-14`（`research.md` §1）。 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 单文件标准库引擎，无 daemon/外部服务/新运行时；`LS-02` 只冻结动作面与拒绝信封，不实现 `recover`/`check-spine`（§Slice Landing Notes）。 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新增文档均小写命名并落在既有位置（`references/state-awareness.md`、`docs/reference/skills/sdd-loop-driver.md`）；无保留名冲突。 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 改动落框架源 `skills/external/sdd-loop-driver/`；镜像由 `sync-mirrors.py` 生成，不手改 `.specify/` 副本（§Mirror Obligations）。 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 仓库无覆盖状态聚合的既有 Tool；实现复用 watcher 与 Registry，而非重写判定（`research.md` §1、R-06）。 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution 与 Change Validation 维度；不新增评分/记录引擎；基线证据见 `research.md` §1/§4。 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | derived `loop_state` 映射表与 watcher 优先不变量只在 `requirements.md` FR-004 定义一次，reference 与代码是镜像并由契约测试比对；阈值 owner 为 `watch-target.sh`；产物映射 owner 对为“脚本数据 + `references/state-awareness.md` 章节”，契约文件在实施后为 dated 记录（`AM-01`）。 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` 每条 planned 示例附前提；拒绝信封含用户可读 `message`（`LS-02`）；内部字段以路径指针引用。 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 不可解析 probe / 非法组合直接 exit 2；缺失与未知显式化；无静默默认值；独立评审发现的过载结论已在本轮修正并披露（§Disclosed Deviations）。 |

**Gates Status**: ✅ All 16 gates pass — 0 Fail，0 Partial；`Complexity Tracking` 为 N/A。

**Re-check after Phase 1**（2026-10-21，设计件落盘后）：16 行全部重新对照 `data-model.md`、`contracts/`、`quickstart.md` 与 `feature-ref.md` 复核，并叠加两次 fresh-context 只读评审（Constitution 评分与 Post-Generation Quality Gate 各一次）。评审发现的缺陷已在本轮修正：状态/值分层、watcher 归属三态、产物映射 owner 对、动作优先级引用、`false_completion` 与尝试上限的关系、示例前提。最终判定 16 Pass / 0 Partial / 0 Fail。

## Design Overview

```text
argv / probe ──> resolve paths ──> read evidence ──> exclude stale ──> derive state
                                                                        ├─ watcher verdict (verbatim)
                                                                        └─ derived ladder (FR-004)
                                                          ──> detect interruptions (6 forms)
                                                          ──> suggest action (closed set)
                                                          ──> emit JSON envelope / --out
```

1. **解析**：`LS-04` 的优先级解析 line/stage/state_dir/spine/spec_dir/repo；缺失项记 `missing`，不猜。
2. **读取**：按 `watch-target.sh` 的空格信封读取四件套与日志；读取 watchbeat、脊机读段、Registry 与 git 提交；`--probe` 时只消费 probe。watcher 调用按归属可证性分三态（`LS-14`）：归属形态（meta 或匹配 `run=`）→ 附 `--line-id/--run-id/--registry/--meta`；无归属但无 stale → 兼容形态；有 stale → 不调用，记 `unavailable` 并走 derived。
3. **隔离**：`run_id`/mtime/legacy 判据命中的信号进入 `stale_signals[]` 并从求值中排除（`IA-11`）。
4. **判定**：有 watcher 判定则逐字采用；否则走 `not-dispatched` / `remote-unreachable` 前置短路 + FR-004 映射（`IA-03`–`IA-06`）。
5. **形态与动作**：六类检测器产出 `interruptions[]`；按 `IA-14`–`IA-17` 得唯一动作建议；伪完成、salvage 门、尝试上限各自可审计。
6. **输出**：单一信封（`SN-02`）；`--out` 原子写且受路径边界约束（`LS-10`）。

## Project Structure

### Documentation (this slice)

```text
.specify/specs/065a-state-awareness/
├── requirements.md          # 切片需求（权威输入，已 clarify）
├── checklists/
│   └── requirements.md      # 需求质量清单（已通过）
├── plan.md                  # 本文件
├── research.md              # Phase 0：13 条技术裁决
├── data-model.md            # Phase 1：13 个实体与不变量
├── contracts/
│   ├── loop-state-cli.md    # C-1…C-18（别名 LS-01…LS-18）
│   ├── snapshot-envelope.md # C-19…C-32（别名 SN-01…SN-14）
│   ├── interruption-and-action.md # C-33…C-49（别名 IA-01…IA-17）
│   └── stage-artifact-map.md      # C-50…C-60（别名 AM-01…AM-11）
├── quickstart.md            # 3 项可执行基线 + 7 个 planned 场景
├── feature-ref.md           # Feature 065 绑定与切片边界
└── tasks.md                 # Phase 2 输出（/speckit.tasks 创建，本阶段不产出）
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/
├── scripts/
│   └── loop-state.py        # 新增：只读聚合引擎（标准库）
├── references/
│   └── state-awareness.md   # 新增：状态感知/形态/动作/产物映射的 owner reference
└── SKILL.md                 # 更新：References 行 + 只读入口 Hard Requirement

.specify/skills/sdd-loop-driver/
├── scripts/loop-state.py    # 生成镜像（sync-mirrors.py）
├── references/state-awareness.md
└── SKILL.md                 # 生成镜像

docs/reference/skills/
└── sdd-loop-driver.md       # 更新：入口、调用形态、与 watcher/Registry 的关系

tests/
├── unit/test_loop_state_engine.py        # 新增：求值逻辑 + 夹具 + 逆样本
└── contract/
    ├── test_loop_state_contract.py       # 新增：CLI/信封/退出码/probe/自测/确定性
    └── test_sdd_loop_driver_skill.py     # 更新：MIRROR_FILES 增补新文件
```

**Structure Decision**: 本切片扩展现有 `sdd-loop-driver` 技能，新增一个单文件引擎与一个 owner reference；不新增顶层目录、不引入独立包。运行时镜像 `.specify/skills/sdd-loop-driver/` 由 `scripts/python/sync-mirrors.py` 生成，**禁止手改**（两顶帽子）。

### Mirror Obligations

下表每一行都是实现阶段的正式产物；`Verify` 列是**测量程序**，plan 阶段未执行 `sync-mirrors.py`（隔离策略拒绝），实现阶段首次编辑前必须取得基线后再判“无新增漂移”，不得把既有漂移归因于本切片。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/scripts/loop-state.py` | `.specify/skills/sdd-loop-driver/scripts/loop-state.py` | 实现前先跑 `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` 记录基线；`--write` 后再跑同一命令，比较新增漂移项；对两文件做字节比较 |
| `skills/external/sdd-loop-driver/references/state-awareness.md` | `.specify/skills/sdd-loop-driver/references/state-awareness.md` | 同上：基线 → `--write` → `--check`，判“无新增漂移”；字节一致 |
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` | 同上；并运行 `tests/contract/test_sdd_loop_driver_skill.py` 的镜像断言 |
| `docs/reference/skills/sdd-loop-driver.md` | 无镜像 | 内容断言：入口路径、调用形态、与 watcher/Registry 的关系三处存在且与 `--help` 一致 |
| `tests/contract/test_sdd_loop_driver_skill.py` | 无镜像 | `MIRROR_FILES` 含新增脚本与 reference；镜像字节断言覆盖两者 |

## Testing Strategy (handed to `/speckit.tasks`)

- **红先**：每个检测器、每个动作分支先写失败断言，再实现；`tests/unit/test_loop_state_engine.py` 覆盖六类形态、派生映射、stale 排除、产物/提交、probe 两形状、legacy 脊、`not-dispatched`、尝试上限与 salvage 门。
- **逆样本**：正常窗口不报 `unwatched`；活进程不出 `stop`；哨兵在而产物缺不得 `resume`；缺失信号不得变 `ok`；本地证据在 probe 模式下不得混入；同输入两次运行除 `evaluated_at` 外 diff 为 0。
- **输入分档**：必需 CLI 参数/`--probe` 不可读 → exit 2；证据源不可读 → `status=missing` + exit 0；`--probe` 与本地路径参数并用 → exit 2 且不读本地证据。
- **特例动作**：analyze DONE（无文件产物 → vacuous `artifacts.complete=true`）→ `verify`；`commit_required=false` DONE → `verify`；未知提交基线 → `verify`（`reason=commit-baseline-unknown`）；clarify 合法无变更 → `verify`；implement 仅文档提交 → 不完整；checklist 仅预存文件 → 不完整。
- **哨兵边界**：末行哨兵 + 活进程 + 其后 `ANOMALY:` 行 → 不判 `DONE`、不判 `false_completion`；`false_completion` 与 `artifacts-without-completion` 互斥。
- **`--out` 边界**：目标与父目录先规范化再比较；symlink、相对路径与指向 state dir 的符号链接均 exit 2 且不留文件。
- **归属矩阵**：无 `run=` 的现行信封在无 stale 时走兼容形态并正常消费终止证据；有 stale 时不调用 watcher 且 `detail=stale-evidence`；有 meta 或匹配 `run=` 时走归属形态并附 `--line-id/--run-id/--registry/--meta`。三态各至少一条正样本与一条逆样本。
- **契约一致性**：`contracts/stage-artifact-map.md` 的五个维度与 `references/state-awareness.md` §Stage Artifact Map 及脚本 `STAGE_ARTIFACTS` 逐项一致（`AM-01`）；信封字段域、`recovery_action` 与 `recovery_decision.action` 相等、拒绝信封 exit 1 + 用户可读 `message` 均由契约测试钉住。
- **变异演练（SC-006）**：移除 `unwatched` 检测后至少一条测试转红；另对 salvage 门做一次 mutation drill（移除 `IA-16` 的完整记录门，至少一条测试转红）；演练命令、移除位置与转红用例写入实现阶段的验收记录（`verification.md` 或阶段日志），不得只保留通过路径的绿。
- **兼容**：`watch-target.sh --self-test`（plan 阶段实测 38/38）、Registry 引擎测试与镜像一致性检查保持绿色。

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial，无需要辩护的复杂度。

## Phase 0: Research Review

**Standalone research file**: [`research.md`](./research.md) — 13 条裁决（R-01–R-13），覆盖入口形态、路径解析、信号信封、状态/值边界、阈值发现、watcher 委托、derived 映射、产物与提交、probe、动作优先级、确定性、自测、分发面。

**Codebase exploration**: 通过 Explore 子代理完成一轮代码探查，证据见 `research.md` §1：watcher 的判定/退出码/默认值来自 `watch-target.sh --help`；四件套格式来自 `stage-runner.sh` 与 `watch-target.sh` 的读取函数；Registry 字段与 action 来自 `line-registry.py`；U4 产物与 plan-owned 集合分别来自 `stage-prompts.md` § Independent Verification 与 `efficiency-model.md` §3.1。

**Setup-script deviation (disclosed)**: `/speckit.plan` 的 `{SCRIPT}` 为 `.specify/scripts/bash/create-new-plan.sh`，它按分支前缀解析 feature 目录；当前分支 `065-loop-interruption-recovery` 会解析到 `.specify/specs/065-loop-interruption-recovery/`（并发隔离的 umbrella 草稿区，已有未提交 plan）。为遵守 SA-5 与隔离要求，本阶段**未运行该脚本**，而是把 `.specify/templates/plan-template.md` 的模板结构直接落到切片目录并就地填充。产物路径与技能要求一致（`IMPL_PLAN=.specify/specs/065a-state-awareness/plan.md`）。

**Baseline measurements**:
- `watch-target.sh --self-test` → `SELF-TEST: 38 passed, 0 failed`，exit 0（本次运行）。
- `sync-mirrors.py --check` 在 plan 阶段因并发隔离策略被工具拒绝执行；实现阶段 MUST 在首次编辑前测量基线，不得把既有漂移归因于本切片。

**Unknowns**: 无。`[NEEDS CLARIFICATION]` 计数为 0；5 项 clarify 裁决（六类形态、`present|missing|na` 与值级 `unknown`、probe 两形状、`not-dispatched` 判据、结构化 `watch_verdict`）分别落到 `IA-08`–`IA-12`、`SN-03`、`LS-11`–`LS-13`、`IA-03`/`IA-04`、`SN-07`。

### Slice Landing Notes（跨切片归属，不是缺口）

- **FR-010**：065a 定义并验证 watchbeat 标记的**读取契约**（路径、`run=`/`stage=`/`window=`/`at=`/`event=` 字段、新鲜度公式）与消费行为；驱动者 U3 的**写入指令与文档章节**按 Parent FR Mapping 的“标记写入属驱动者行为，快照只读消费”归 065b 完成。本切片无写入代码。
- **FR-044**：065a 落地入口文档、六类形态表、derived 映射与产物映射；恢复动作与 watchbeat 写侧章节由 065b/065c 在同一 FR 下补齐。
- **FR-012 / FR-046**：`--self-test` 覆盖快照、六类已实现形态与未实现动作拒绝；`heartbeat-stalled`、`lifecycle-spine-violation`、并发锁与 `recover/check-spine` 执行路径由 065b/065c 追加。移除“无 watcher 检测”的变异演练在本切片执行。
- **父编号 045 / 048**：按切片记录显式 out-of-slice，由 065c 汇总/承接（`feature-ref.md` §3）。

### Disclosed Deviations

1. **Feature 状态推进**：切片 `requirements.md` §Related Feature 已按 2026-10-21 analyze 修复改写为「不新建 Feature ID、不新增注册行；Draft→Planned 的状态推进由 plan 阶段按 Feature Integration 拥有」。本 plan 据此把 Feature 065 从 `Draft` 推进到 `Planned`，不新建 Feature ID 或注册行；requirements 与该推进现已一致，不再存在被违反的 MUST NOT。
2. **Setup 脚本**：`create-new-plan.sh` 按分支前缀会解析到并发隔离的 umbrella 目录，故未运行；模板结构直接落到切片目录（§Phase 0 上文）。
3. **镜像基线**：`sync-mirrors.py --check` 在 plan 阶段被隔离策略拒绝执行；基线改由 implement 首次编辑前测量，判据为“无新增漂移”。

## Phase 1: Design Artifacts Summary

*Backfilled after the artifacts landed on disk; counts measured with `grep -cE '^- \*\*C-[0-9]+\*\*'` against the canonical clause form, so alias tables and prose mentions do not inflate them.*

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 13 entities（快照、路径、Registry、脊、信号、watch 判定、watchbeat、产物映射、中断、动作、probe、stale、阈值） |
| Contracts | [`contracts/`](./contracts/) | 4 files / 60 clauses：`loop-state-cli.md`（18）、`snapshot-envelope.md`（14）、`interruption-and-action.md`（17）、`stage-artifact-map.md`（11） |
| Quickstart | [`quickstart.md`](./quickstart.md) | 3 项可执行基线检查 + 7 个 planned 调用场景（每条附前提） |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | 1 条绑定记录；切片边界、FR 覆盖、下游扩展点、注册表改动 |
| Research | [`research.md`](./research.md) | 13 条技术裁决 + 实测证据表 |

**Scope check**: 25 条切片 FR 均已映射到条款、实现文件或显式跨切片归属；6 条 SC 由 `quickstart.md` §9 与 `Testing Strategy` 承接。FR-010 的驱动者写入侧与 FR-044 的恢复/watchbeat 写侧按切片映射由 065b/065c 补齐（§Slice Landing Notes），不构成本切片的实现缺口；`recover` / `check-spine` 的执行路径、并发锁与 `heartbeat-stalled` / `lifecycle-spine-violation` 判定同样留在下游（`feature-ref.md` §2）。
