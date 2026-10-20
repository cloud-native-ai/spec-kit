# Implementation Plan: 064-subagent-concurrency

**Branch**: `064-subagent-concurrency` | **Date**: 2026-10-20 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `064-subagent-concurrency` → Feature 064 Subagent 并发归属、CLI 能力档案与生命周期解耦
**Input**: Specification from `.specify/specs/064-subagent-concurrency/requirements.md`

## Summary

在 Feature 058 的 U0–U6、每线状态脊、通用阶段哨兵与 watcher 判定之上增加四层增量，解决「同环境多线串台、同仓多写线互毁、主/子会话生命周期绑定、CLI 行为知识无落点」四类问题：

1. **A 线路身份与归属**：环境级 Line Registry（每线 `<line_id>.json` + 同线锁 + 原子替换）、`(line_id, run_id)` JSON 旁路信封、无标识消息的确定性入口（>1 条活动线恰好一次澄清）、`foreign/stale-run/unattributed` 零状态影响。
2. **B 工作区隔离与集成**：worktree-per-write-line、Ownership Manifest + 归一化重叠检测、重叠 FIFO 串行化、运行时/镜像单次集成、确定性集成队列（FIFO + `line_id` tie-break + 拓扑依赖优先）。
3. **C CLI 能力档案**：`references/cli/<cli>.md` 五份档案、八维度 known/unknown + provenance、U2 查阅 / U4/U5 比对、`cli-profile:<cli>` 反馈、最小 Probe Object；063 的 provisional 范围收编为单一 owner。
4. **D 生命周期解耦**：detach 进程组 + 四件套 + `(line_id, stage)` 原子 reservation + driver lease；主会话 kill 后凭 Registry + 状态脊重接线，running/done/dead 三分支零重复派发。

不引入常驻服务、外部依赖或模型 API；不改既有哨兵字面量、watcher 判定状态机/退出码、确认门、阶段 deadline 与阶段命令内部流程。设计决策与基线见 [research.md](research.md)；实体与校验规则见 [data-model.md](data-model.md)；条款见 [contracts/](contracts/)；验收场景见 [quickstart.md](quickstart.md)。

## Technical Context

**Language/Version**: Python 3.8+（stdlib-only；本机 3.9.6）+ Bash（POSIX 兼容，macOS/Linux 双平台）
**Primary Dependencies**: 无新增第三方依赖；复用既有 `watch-target.sh`、`feedback-utils.py`、`probe-utils.py`、`sync-mirrors.py`、`regen-command-copies.py`
**Storage**: 文件系统——环境级 Registry 目录（`SPECIFY_LINE_REGISTRY_DIR` 覆盖）、每线 JSON、JSONL 旁路、lease/reservation 文件；无数据库、无 daemon
**Testing**: pytest（`tests/{unit,contract,integration}`）；Tests Mode = **ON**。本环境未安装 pytest，green 基线为 Unobserved，implement 阶段必须补测并留证（`research.md` § 0, `contracts/non-regression-and-tests.md` NG-10）
**Target Platform**: macOS/Linux 驱动与执行宿主；远端拓扑 = `ssh + su + nohup` + Linux 执行侧；macOS 无 `/proc` 时 cwd 校验记为 `unsupported`，start token 用定向 `ps -p <registered-pid> -o lstart=`
**Project Type**: SDD 框架 + 自包含外部技能（framework source + skill scripts）
**Performance Goals**: watcher 单窗口内归属过滤为 O(事件数) 的文件读取；Registry 单次读写毫秒级；集成队列排序 O(N log N + E)；无网络/无轮询常驻
**Constraints**: 零常驻服务、零外部服务、零模型 API、零新增运行时依赖；不改哨兵/退出码/确认门/deadline；不自动 push；不删除未提交工作；所有新脚本镜像义务明确
**Scale/Scope**: 单环境默认并发上限 4 条活动写线（可配置）；端口块缺省 20/线，起点 39000；N 条并发注册需保证 0 丢失/0 重复（SC-009）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计决策回指 FR；`contracts/` 每条款带 FR/SC 追溯表；无未溯源技术选择 |
| II | Feature-Centric Development | ✅ Pass | Feature 064 已登记；plan 执行 Draft→Planned；`feature-ref.md` 记录绑定与范围；未改动其他 Feature 状态 |
| III | Intent-Driven Development | ✅ Pass | requirements 的自然语言意图（what/why）先于本 plan 的 how；Decisions 逐条记录取舍 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON；每个新脚本 red-first；契约/单元/集成三层 + 三项变异演练（`contracts/non-regression-and-tests.md`） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增/变更 agent provider；CLI 档案引用 `CAPABILITY_MATRIX`，不触碰 `AGENT_CONFIG`/`_ASSISTANT_TIERS` |
| VI | Continuous Quality & Observability | ✅ Pass | 引擎 JSON 输出 + `schema_version`；心跳/status/log 既有观测面增强；docs 同步入口 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 按 requirements→clarify→plan 推进；Feature Index 同步；plan 不越过 Implemented；无 gate 例外 |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 以源码实测校准 watcher 解析、退出码 owner、`CAPABILITY_MATRIX`、probe 注册表；不以文档替代代码事实 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 无 daemon/外部服务；新引擎只做原子状态读写与查询，不做调度/派发——所有编排仍是驱动提示词（并发决策由会话按合同表决）；R1 否决 SQLite/全局锁/项目内 registry |
| X | Documentation Naming & Location Conventions | ✅ Pass | CLI schema owner 使用 `references/cli/index.md`（索引型文件按 X 的路径语义命名；X 的保留名阻断严格范围只覆盖项目根与 `docs/`，此处为命名一致性选择）；docs 路径语义化；未新增保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性经 SDD 流程开发；编辑框架源 `skills/external/**` 后经 `sync-mirrors.py` 投影；两顶帽子已声明（`research.md` R12） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `sync-mirrors.py` 的 Tool 记录（`.specify/memory/tools/sync-mirrors.py.md`）；`.specify/memory/tools/` 无 registry/watcher 能力记录，故按预期编写新引擎（Tool 复用门槛已查） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（归属/隔离）、Change Validation（独立校验/证据）、Reliable Delivery（预算/集成队列）、Learning Capture（CLI 档案/反馈）四个维度；无新评分系统 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 058 判定表/退出码引用 `watch-model.md` §3 与代码；061 矩阵只引用路径；063 吞吐保留其 owner；064 只拥有 Registry/信封/档案/生命周期；probe 行单点登记 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 入口澄清问题模板给出候选的 line/project/branch/stage/state；U5/收尾报告沿用四要素并含路径指针 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 派发注入 anomaly 行契约保留；Registry 不可写/租约冲突/队列环均显式失败上送；无静默修平路径 |

**Gates Status**: ✅ All gates pass（无 ❌/⚠ 行，Complexity Tracking 因此为 N/A）。

**Re-check after Phase 1**（2026-10-20，设计产物落盘后复核）：同一 16 行全部维持 ✅ Pass；新增证据为 `data-model.md`（11 实体 / 59 条 V 规则）与 6 份契约（98 条款，FR 68/68 覆盖）。无新增违规，无 Complexity Tracking 行。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/064-subagent-concurrency/
├── plan.md                       # This file
├── research.md                   # Phase 0 decisions + measured baseline
├── data-model.md                 # Phase 1 entities + validation rules
├── contracts/                    # Phase 1 (6 files: 98 clauses)
│   ├── line-registry.md
│   ├── line-envelope-and-ingress.md
│   ├── workspace-isolation.md
│   ├── lifecycle-detach-reattach.md
│   ├── cli-profiles.md
│   └── non-regression-and-tests.md
├── quickstart.md                 # Phase 1 (6 scenarios; § A baseline executed)
├── feature-ref.md                # Phase 1 binding + FR/SC mapping
├── notes/
│   ├── source-requirement.md     # dated snapshot of /tmp/sdd-064/brief.md
│   └── 063-overlap-adjudication.md
├── tasks.md                      # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md               # implement output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/
├── SKILL.md                                  # + H2 CLI Capability Profiles; concurrency/lifecycle pointers
├── references/
│   ├── cli/                                  # NEW: behaviour knowledge (index.md + 5 CLI profiles)
│   │   ├── index.md
│   │   ├── qodercli.md
│   │   ├── claude.md
│   │   ├── codex.md
│   │   ├── opencode.md
│   │   └── hermes.md
│   ├── dispatch-recipes.md                   # envelope runner, cli PID, reservation, detach, integration pointer
│   ├── stage-prompts.md                      # U0.5/U2/U4/U5/U6, ingress, reattach, spine additions
│   └── watch-model.md                        # attribution layer reference; verdict machine text unchanged
└── scripts/
    ├── line-registry.py                      # NEW: stdlib registry/lease/reservation/queue engine
    └── watch-target.sh                       # + --line-id/--run-id/--meta, attribution output, self-test cases

shared/definitions/probe-definitions.md       # + 1 Probe Object row
docs/reference/skills/sdd-loop-driver.md      # + concurrency/lifecycle + CLI profiles entry

tests/
├── unit/test_line_registry_engine.py                     # NEW
├── contract/test_line_registry_contract.py               # NEW
├── contract/test_line_envelope_contract.py               # NEW
├── contract/test_workspace_isolation_contract.py         # NEW
├── contract/test_lifecycle_detach_reattach.py            # NEW
├── contract/test_sdd_loop_driver_cli_profiles.py         # NEW
├── contract/test_sdd_loop_driver_skill.py                # UPDATED pinned H2 set + mirror coverage
└── integration/
    ├── test_two_line_isolation.py                        # NEW
    ├── test_worktree_integration_queue.py                # NEW
    └── test_session_kill_reattach.py                     # NEW
```

**Structure Decision**: 本特性落在既有「自包含外部技能 + 共享定义 + docs + pytest」结构内：引擎与 watcher 扩展位于 `skills/external/sdd-loop-driver/scripts/`，行为知识位于其 `references/cli/`，Probe Object 只向 `shared/definitions/probe-definitions.md` 追加一行；不新增顶层目录、不新增命令模板、不触碰 `src/specify_cli/`、`templates/`、`scripts/` 根级引擎。

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` | `sync-mirrors.py --check --only skills/external/sdd-loop-driver` — no NEW drift vs §0 baseline (baseline: 3 DIFF, all three files are edited by this feature and should converge to clean) |
| `skills/external/sdd-loop-driver/references/cli/index.md` + 5 profiles (new) | `.specify/skills/sdd-loop-driver/references/cli/*` | same command; new files must exist in both trees byte-identical |
| `references/dispatch-recipes.md`, `references/stage-prompts.md`, `references/watch-model.md` | `.specify/skills/sdd-loop-driver/references/*` | same command; the §0 baseline drift is exactly `SKILL.md`, `dispatch-recipes.md`, `watch-model.md` — all three are edited by this feature, so the pair must converge to no drift; `stage-prompts.md` has no baseline drift |
| `skills/external/sdd-loop-driver/scripts/line-registry.py` (new), `scripts/watch-target.sh` | `.specify/skills/sdd-loop-driver/scripts/*` | same command + `tests/contract/test_sdd_loop_driver_cli_profiles.py` pins the pair |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md` | `sync-mirrors.py --check --only shared/definitions/probe-definitions.md` — exit 0 for this file (it is not in the 9-file pre-existing drift baseline) |
| `docs/reference/skills/sdd-loop-driver.md` | none (docs tree is not mirrored) | n/a |

No per-tool command copies are touched (`regen-command-copies.py` not needed for this feature except the integration-pass rule in `contracts/workspace-isolation.md` WI-11).

## Complexity Tracking

N/A — Constitution Check has no ❌ or ⚠ rows. The new stdlib engine is justified inside Principle IX compliance (file-based state, no daemon/service, operated by the agent within the skill) and is the minimal mechanism that satisfies the atomicity/locking/identity requirements; shell-only alternatives cannot provide `fsync`+`os.replace`+exclusive locks portably across macOS/Linux.

## Phase 0: Research Review

Standalone [research.md](research.md) produced (>50 lines; includes external-source evaluation of the 063 in-flight branch and qodercli observed facts). Key outcomes carried into design:

- R1 Registry storage/atomicity/locking → contracts LR-03/LR-04, data-model E1.
- R2 envelope encoding → contracts EN-01/EN-02, data-model E2.
- R3 ingress decision table → contracts EN-08…EN-13, engine action `resolve-message`.
- R4 worktree/branch naming → contracts WI-01/WI-02, data-model E3.
- R5 ownership normalization/serialization → contracts WI-04…WI-08.
- R6 deterministic queue → contracts WI-13, data-model E7.
- R7 runtime/mirror single pass → contracts WI-09…WI-11, data-model E8.
- R8 detach/lease/reservation/reattach → contracts LC-01…LC-18, data-model E4/E5/E6.
- R9 orphan/stale/remote classification → contracts LC-13/LC-14.
- R10 CLI profiles + 063 adjudication → contracts CLP-01…CLP-17, notes/063-overlap-adjudication.md.
- R11 tests/baseline → Tests Mode section, contracts NG-10…NG-12.
- R12 docs/mirrors → Mirror Obligations.

All `NEEDS CLARIFICATION` items in Technical Context are resolved; residual unknowns are deliberately recorded as `unknown` in the qodercli profile (0/negative timeout semantics) and are not used to make stage decisions.

## Tests Mode

**Mode: ON.**

- **Why ON**: the feature delivers executable code (`line-registry.py`, `watch-target.sh` extension), not template/docs-only content; Constitution IV and FR-067 require automated coverage.
- **Red-first**: every new script/extension begins with failing contract/unit tests; red runs recorded in `verification.md` at implement time.
- **Placement**: `tests/unit/test_line_registry_engine.py`; contract files per family; integration files per scenario; existing `tests/contract/test_sdd_loop_driver_skill.py` updated only to add the new pinned H2 section and mirror coverage.
- **Gate**: implement cannot claim done while any of the 10 planned test files is absent or red; pytest is unavailable in this plan environment, so green is explicitly **Unobserved** until implement runs them.

## Validation & Verification Plan

| Concern | Verification |
|---------|--------------|
| Red-first | Each test file authored before its implementation; red evidence (command/time/failing assertion) in `verification.md` |
| Two lines, same sentinel | `tests/integration/test_two_line_isolation.py`: identical `PLAN-DONE`, identical CLI name; assert zero cross-attribution; both complete correctly |
| No-identifier message | Same integration file + PATH stubs for `ps`/`pgrep`: exactly one clarification; zero process scans; `ambiguous-stop` on unresolved answer |
| Foreign event | Inject foreign status/pid/meta into current watcher: `attribution=foreign`, verdict/state unchanged, not relayed as progress |
| Worktree conflict | `tests/integration/test_worktree_integration_queue.py`: overlap rejected/serialized; disjoint concurrent; `git fsck` clean; deterministic queue replay; runtime/mirror once |
| Main session kill / reattach | `tests/integration/test_session_kill_reattach.py`: detached process survives; reattach with `identity=ok` + `--once`; running/done/dead branches; zero redispatch; reservation exclusivity |
| Mutation drills | ① remove attribution filter → two-line test red; ② remove detach → reattach test red; ③ remove `O_CREAT|O_EXCL` reservation → duplicate-launch test red |
| Non-regression | `watch-target.sh --self-test` existing failures not increased; watcher exit codes pinned; probe validate exit 0; mirror no NEW drift; push-stub count 0 |

### Same-Author Review (objective-analysis-gate)

- **Condition**: requirements, clarify output and this plan were produced by the same agent in the same session; the gate fired for both the Constitution Check and the post-generation quality gate.
- **Staffing**: two fresh-context read-only subagents with disjoint scopes — A: constitution/plan/data-model/research coherence; B: contracts/feature-ref/quickstart/063 adjudication. Neither validated its own findings; the orchestrator performed the correction pass.
- **Result**: 25 findings (A 11, B 14; 7 HIGH, 13 MEDIUM, 5 LOW). All 25 were confirmed as corrections (one consistent reading, local, reversible) and repaired in place: mirror-baseline facts, `line_id` charset, lease/reservation interface and state-machine closure, queue dependency semantics, engine path consistency, FR-017/FR-067 clause ownership, per-line vs per-batch mirror execution, cwd/branch verification wording, orphan disposition, 063 CP-07/CP-08 branches, quickstart premises/unit-suite inclusion, and One-Source-Of-Truth wording for Constitution X.
- **Downgrade rate**: 0 of 25 downgraded on validation. Per the gate, a near-zero rate on a self-authored set is itself a signal; here it reflected a genuinely defect-dense first draft rather than over-strict detection (every accepted finding changed a clause body or a baseline fact).
- **No decision-class anomaly** remained: no finding required choosing between readings or inventing intent absent from the requirements.

## Decisions & Assumptions

**Design decisions**（均为实现既有已批准 FR 的方式，不改变需求范围）：

- **D-01**: 单一 stdlib 引擎 `line-registry.py` 承载 Registry/lease/reservation/identity/queue/ownership/resources/archive 动作；不拆多个脚本（共享底层原子读写）。
- **D-02**: FR-005 的 `qodercli_pid` 泛化为 `cli_pid`/`cli_start_token`（`cli=qodercli` 时即同一值），以支持多 CLI 档案；字段语义与 FR-005 一致。
- **D-03**: 信封载体与命名按 EN-02；watcher 未给 `--line-id/--run-id` 时保持 058 兼容（`attribution=legacy`，无过滤）。
- **D-04**: `ready_for_merge` 建模为 `merge_ready` 标记 + `ready_for_merge_at`，不加入 Registry `state` 封闭集。
- **D-05**: `line_id = <project-slug>-<YYYYMMDDTHHMMSSZ>-<4hex>`；`run_id = r<YYYYMMDDTHHMMSSZ>-<4hex>`；重接线复用 `run_id`。
- **D-06**: worktree 默认 `<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`，分支 `line/<line_id>`；Manifest 在 `$REGISTRY/manifests/`；lease/reservation 在 `$REGISTRY/` 与 `$REGISTRY/reservations/`。
- **D-07**: 集成队列 = 拓扑分层 + 同层 `(ready_for_merge_at, line_id)`；环显式拒绝。
- **D-08**: 资源缺省端口 39000 + 20/线、并发上限 4（`SPECIFY_LINE_CONCURRENCY_CAP` 覆盖），只登记不绑定，禁止全局服务。
- **D-09**: 远端身份校验 = 远端跑同一引擎产出 probe JSON，本地 `classify-remote` 分类；ssh 失败 = `stalled(remote-unreachable)`，不判 dead。
- **D-10**: CLI schema owner 为 `references/cli/index.md`（按宪法 X 的路径语义命名；063 的嵌套 `README.md` 不保留）；Probe Object id `skill-sdd-loop-driver-cli-profile`（优先 `skill-wrapup`，fallback `external-custom`）。
- **D-11**: 063 provisional 范围按 `notes/063-overlap-adjudication.md` 迁入/合并/保留；063 合并时删除其契约与档案测试，禁止双 owner。
- **D-12**: 状态脊只追加 `line_id/run_id`、`cli_observations`、派发三字段、lease/resume 快照字段；既有阶段状态词与写入顺序不变。
- **D-13**: 镜像策略 = 只对本特性触碰的文件负责，判据「no NEW drift」；基线 3（技能）/ 9（shared/definitions）文件漂移已记录。
- **D-14**: 既有 `test_sdd_loop_driver_skill.py` 的 H2 固定集合新增 `CLI Capability Profiles`，属结构契约同步，不改变行为断言。

**Assumptions**（无人值守运行下的自行裁决，可由后续 clarify 推翻）：

- 宿主具备 Python 3.8+ 与 bash；远端 Linux 具备 `python3`；本地 macOS 无 `setsid` 时使用 `nohup + disown`（Linux 优先 `setsid`）。
- Registry 目录由引擎以 `0700` 创建（含缺失的父目录），同一 OS 用户信任边界；不处理多用户 ACL。
- `git worktree` 可用（git ≥ 2.5）；`base-ref` 缺省 `main`，不存在时驱动显式选择而非猜测。
- 阶段子代理不切换分支、不写 worktree 拓扑，作为提示词纪律与 U4 抽查项执行；引擎不强制拦截 git 调用（不在本特性范围）。
- qodercli 的 0/负值超时语义、hermes 的矩阵条目缺失，均按 `unknown`/缺口记录，不在本阶段实验。
- 本环境无 pytest：不伪造测试通过；implement 阶段补测。

**PLAN-EDIT**: 本 plan 为首版，未修改既已批准的 064 需求/范围/架构；无 PLAN-EDIT 记录。跨特性的契约替换（063 provisional → 064）已在 D-11 与 `notes/063-overlap-adjudication.md` 逐条留痕。

## Cross-Feature Overlap Adjudication (063)

Summary（逐条见 [notes/063-overlap-adjudication.md](notes/063-overlap-adjudication.md)）：064 是 CLI 能力档案唯一 owner；063 的 `FR-044…FR-049`、`CP-01…CP-10`、`tests/unit/test_cli_profile_record.py` 与 Probe Object `skill-sdd-loop-driver-wrapup` 在合并时删除并改为指向 064；063 保留 stream-json 默认、nohup runner 与其 E6/E7/E8 字段，064 依赖引用。schema owner 由 `README.md` 更正为 `index.md`（按宪法 X 的路径语义）。无静默复制、无双 owner。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 14 sections (baseline + R1–R12 + unknowns) |
| Data model | [`data-model.md`](data-model.md) | 11 entities (E1–E11), 59 validation rules (V-*) |
| Contracts | [`contracts/`](contracts/) | 6 files / 98 clauses: line-registry (LR-01…LR-13), line-envelope-and-ingress (EN-01…EN-16), workspace-isolation (WI-01…WI-21), lifecycle-detach-reattach (LC-01…LC-18), cli-profiles (CLP-01…CLP-17), non-regression-and-tests (NG-01…NG-13) |
| Quickstart | [`quickstart.md`](quickstart.md) | 6 implement-stage scenarios (S1–S6) + 5 executed baseline commands (§ A) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | 68/68 FR mapped; 10/10 SC evidence planned; 19 delivered rows (24 files incl. 6 CLI reference files) |
| Overlap record | [`notes/063-overlap-adjudication.md`](notes/063-overlap-adjudication.md) | 14-row adjudication + 6-step merge verification |

Counts were taken from the landed files with `grep -c` in the same run and cross-checked by the plan integrity check (single heading, no placeholders, 16 constitution rows, 68/68 FR + 10/10 SC mapped, contiguous clause IDs: PASS). No drift from the Phase 0 expectation except the deliberate addition of the 063-overlap record under `notes/`.
