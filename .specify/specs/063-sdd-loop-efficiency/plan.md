# Implementation Plan: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Branch**: `063-sdd-loop-efficiency` | **Date**: 2026-10-20 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `063-sdd-loop-efficiency` → Feature 058 无人值守 SDD 循环驱动机制
**Input**: Specification from `.specify/specs/063-sdd-loop-efficiency/requirements.md`

## Summary

在编排层为 `sdd-loop-driver` 增加四项吞吐优化，不修改任何框架阶段命令内部：① 中型特性快车道（入口 [[STR-006]] 显式启用，`tasks` 后以制品实测七判据裁决，跳过 `checklist` 但保留 `analyze`/`review`，fail-closed 回退）；② 每线两个全量测试槽位（implement 起点 baseline、review 后收口 closure），中间阶段与 review 只用确定性选择的定向集并留证据；③ plan 完成后「只小修、不重审」约束（编排层执行，U4 按最终 diff 分类，实质改动走两分支，框架内部硬执行显式排除）；④ 阶段 runner 默认 `--output-format stream-json`，原始事件流落盘，自包含派生紧凑实时日志，哨兵只认终止 `result` 文本；本地与远端都用 `nohup` 完全脱离驱动会话。

交付面 = 1 个技能（3 份 references 更新 + 1 份新 owner 文档 + 5 个新脚本 + 1 个扩展脚本）+ docs 参考页 + 契约/单元/集成测试与夹具 + Feature 058 扩展记录。零新技能、零新命令、零常驻服务、零外部依赖、零模型 API。完成哨兵、watcher 判定状态机、退出码、确认门、独立校验与卡死处置保持不变。063 自身走完整阶段链，快车道只作用于未来运行。

## Technical Context

**Language/Version**: Markdown 技能面；Bash（runner/watcher，兼容 bash 3.2+ 的常见用法）；Python ≥3.8 仅标准库（准入/派生/台账审计/plan 改动判定）；测试为 pytest（仓库既有 contract/unit/integration 分层）
**Primary Dependencies**: 既有 `git`、`bash`、`python3`；既有 `scripts/bash/run-tests.sh`（名称级基线）；既有 `scripts/python/sync-mirrors.py`（镜像）；既有 `skills/external/sdd-loop-driver/scripts/watch-target.sh`。**不新增任何依赖**，不引入 `jq`/网络/模型 API
**Storage**: 文件即存储——状态脊 Markdown（准入记录、JSONL 台账围栏、plan 约束）、`<spec-dir>/test-evidence/<stage>.jsonl`、`baseline-failed.txt`/`final-failed.txt`、阶段产物 raw/live/pid/status/heartbeat/runner-log。无数据库、无新服务
**Testing**: Tests Mode **ON**。契约测试钉文档面与条款；单元测试钉四个 Python 脚本；集成测试钉 runner 脱离/降级与名称级回归；`watch-target.sh --self-test` 扩流式用例。既有契约测试 21/23 绿，2 红为既有镜像漂移（Phase 0 B-2），本特性修复为绿
**Target Platform**: Linux 与 macOS 驱动/执行宿主；远端拓扑 = `ssh + su + nohup` + Linux 执行侧；macOS 无 `/proc` 的 watcher 分支按平台跳过或退化
**Project Type**: 框架源（两顶帽子：改动落 `skills/external/`、`docs/`、`tests/`，镜像经 sync-mirrors 同步；`.specify/memory` 仅记录 Feature 扩展）
**Performance Goals**: 每线全量套件恰 2 槽位（需求方报告的一次运行 6 次为 dated baseline，本 plan 未复测、不据此宣称提速百分比）；有事件到达时实时日志静默间隔 ≤120s；驱动零独立 `sleep` 回合；checklist 在中型夹具中派发 0 次
**Constraints**: 哨兵/判定状态机/退出码/确认门/独立校验/卡死处置不变；快车道默认关且仅显式启用；预算不得静默超支；plan 约束不改框架内部；无新服务/依赖/API；063 自身完整链
**Scale/Scope**: 1 个技能；4 份 references（1 新）；6 个 scripts（5 新 + 1 扩）；1 个 docs 页；2 个契约测试文件（1 新 + 1 有意更新）；4 个单元测试；2 个集成测试；1 个夹具目录；Feature 058 两个登记面

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，共 16 项；初步自评，同作者门委派复核见 Re-check）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `feature-ref.md` FR-001…043 逐行映射到设计落点；每个设计决定在 `research.md` R-1…R-10 有理由与替代方案 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 058（演化特性）；扩展切片规则：状态保持 `Implemented`，只更新 Feature detail 与索引 Last Updated；未新建 Feature |
| III | Intent-Driven Development | ✅ Pass | 先定义「快车道何时可信、预算如何不丢回归、plan 约束边界、脱离后如何接管」，再给命令形态；四项优化的取舍与显式排除在 research/contracts |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Tests Mode ON；5 个新脚本按 red-first 编写并配单元测试；49 个契约条款、决策表策略测试、FR-042(a)–(e) 夹具、名称级回归集成测试。LLM 驱动的端到端阶段序列无法在 CI 自动化，由实现期录制 trace 证明（见 Complexity Tracking） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增/变更 agent provider；沿用 qodercli/claude 的 stream-json 事件形状；`AGENT_CONFIG` 与 `_ASSISTANT_TIERS` 零改动 |
| VI | Continuous Quality & Observability | ✅ Pass | raw/live 双证据、四件套、状态脊、准入记录、预算台账、plan 分类、收尾汇总；失败与降级均显式留痕 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature 058 已在册；本 plan 产出四件套 + research；不越权推进 `Implemented`；Pre-Status-Flip Gate 留给 implement |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 以源码/测试实测校准：watcher 判定表、runner 四件套、`--names-out`、镜像引擎、stream-json 先例；文档不覆盖代码事实 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | runner 是单阶段 shell 进程，不是调度器/平台；无常驻服务、无新依赖；四个脚本各自单一职责，可被删除而不留基础设施 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件走既有命名面：`references/efficiency-model.md`、`scripts/*.sh|*.py`（小写）、`docs/reference/skills/sdd-loop-driver.md`；`SKILL.md` 保留工具强制名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制修复落框架源侧 `skills/external/`，镜像经 sync-mirrors 同步；063 自身完整链；基线缺陷（watcher 自测、镜像漂移）披露并按机制侧修复 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `sync-mirrors.py`（有 Tool 记录）、`run-tests.sh`、`watch-target.sh`；查 `.specify/memory/tools/` 无 stream 派生/准入/台账同能力记录，按预期编写新脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（脱离/可见）、Change Validation（两槽位/定向证据）、Learning Capture（台账/收尾）；证据区分自动测试与录制 trace，不把 configured 当 used |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 四项机制由 `references/efficiency-model.md` 单一 owner；SKILL/docs 只摘要+指针；字段面由 `data-model.md` 拥有；阈值/退出码由脚本与契约测试钉住，不在多处复述 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | docs 页与 quickstart 面向未参与运行的维护者/操作者；每个术语首次出现给上下文；quickstart 每条示例带前提与钉住者 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 准入 fail-closed、plan 实质改动显式异常行、派生降级不伪完成、基线异常披露；无静默超预算/静默跳过/静默重审 |

**Gates Status**: ⚠ 一项 Partial（IV，已在 Complexity Tracking 辩护）；无 Fail。

**Re-check after Phase 1**: 2026-10-20——Phase 1 产物落盘后复核：IV 维持 Partial（LLM 编排序列用录制 trace，确定性组件全自动测试），其余 15 项 Pass。同作者门委派 fresh-context 只读子代理按 `objective-analysis-gate.md` 分两个不相交 scope 复核（宪法评分/设计一致性；Post-Generation Quality Gate/计数与执行验证）；结果与处置见下方「Delegated review」记录。

**Delegated review（2026-10-20）**：
- **Scope A（宪法评分 + 设计一致性）**：独立评分 16 项，识别 11 项发现（HIGH 7 / MEDIUM 2 / LOW 2），核心为：`attested` 自证判据不满足 FR-003 的可复算要求；FR 计数误把 SC 计入；一处「第二次实质改动不再重审」与 FR-022(a) 冲突；DI-08 与 stream-json 默认矛盾；派生降级可选导致伪 INCOMPLETE；台账看不见阶段自行发起的全量运行；U4 漏掉未提交 plan 改动；SC 比例声明超出证据；quickstart S4 用 `python3` 跑 bash 脚本；镜像基线不完整；宪法全 Pass 自评与上述部分冲突。
- **Scope B（Quality Gate）**：11 项发现（HIGH 2 / MEDIUM 7 / LOW 2），核心为：S4 调用错误；S5 未真正退出驱动 shell；镜像基线漏报 6 个目录；交付计数 22≠23；S6 少传 plan 路径；退出码约定与 watcher 冲突；quickstart 变量未定义；清理未验证；`[[STR-006]]`/U4 术语未展开；S4 4b 的 DONE 来自手写 status 而非派生日志。
- **处置**：全部为纠正类（与已记录意图只有一种一致读法）或按 FR-022/FR-003 收紧设计——已逐项修正：七判据全部机械化（去除自证，新增 `--lines-manifest`）；FR-only 计数；移除重审次数上限；DI-08 收窄并披露日志形态变化；`--finish` 恢复改为强制；台账新增 `--logs-dir` 扫描；U4 加未提交改动；SC 证据按自动/录制如实分层；quickstart 修正调用、变量、夹具、清理与 4b 判据；镜像基线补全 68 文件/12 目录；交付计数改为 23。无遗留决策项。

## Design by Optimization

### ① 中型特性快车道

- **启用**：U0 入口声明出现 [[STR-006]] 并原文入状态脊；无人值守唯一入口；交互式允许一次非阻塞提议。
- **裁决点**：`tasks` U4 通过后、`checklist` 派发前；`scripts/admission-check.py` 输出七判据 JSON（全部机械判定，无自证项），任何解析失败 fail-closed。
- **录取**：状态脊写入 E1 记录 + [[STR-003]]；派发 `analyze`，跳过 `checklist`；`implement`/`review` 提示词携带跳过标记与准入证据指针。
- **回退**：`analyze` 等阶段发现新引擎/安全面/任务越界 → 回退完整链，补派 `checklist`；若 `analyze` 已过则补派后重过 analyze 一次。
- **不变量**：`analyze`/`review` 门判据、回环上限、独立校验完全不变。

### ② 两槽位测试预算

- **槽位**：`baseline`（implement 首任务前，`run-tests.sh --names-out baseline-failed.txt`）与 `closure`（review 后合并前，`--names-out final-failed.txt` + `comm -13`）。
- **中间阶段/review**：三条并集选定向集（改动路径覆盖、交付物契约测试、夹具改动测试），记录选择命令与充分性；空集且改可执行面 → 扩大或显式例外。
- **台账**：状态脊 JSONL 围栏（E2）+ 阶段证据文件（E3）；`audit-test-budget.py` 审计槽位、例外、环境失败与 unknown。
- **修复循环**：收口新失败 → 修复或归因；修复重跑同一套件记 `in-slot-rerun`；实现阶段 closure-repair 重入不再消耗 baseline。

### ③ Plan 只小修约束

- **生效**：plan U4 通过时状态脊 `plan_constraint=active`；下游四阶段提示词携带只小修块。
- **声明**：任何 plan 制品改动须在哨兵前回传 `PLAN-EDIT:` 声明行；完整格式由 `references/efficiency-model.md` §3.2 单一 owner 定义（本 plan 不复写）。
- **校验**：`audit-plan-changes.py` 机械输出 touched/declared；驱动按最终 diff 分类 minor/substantive/undeclared；未声明或实质 → 阶段门失败。
- **分流**：修复既有缺陷且不变更批准面 → 一次完整 plan 重审 + U4 复验；改变批准面/新能力/无法判定 → 四要素上送。每次实质改动都按其分支处置并留痕；重复回环由既有 stall/retry 纪律兜底，不设人工次数上限。
- **显式排除**：框架命令内部硬执行不做；手工调用不受约束；若编排层不安全，另立特性。

### ④ 进度可见与脱离

- **runner**：`scripts/stage-runner.sh` 参数化；auto 模式探测 `--output-format` 能力；stream 模式 `CLI | tee raw.jsonl | derive-live-log.py > live.log`。
- **派生**：非终止事件只输出带前缀进度行；EOF 时追加终止 `result` 文本，保证 live log 最后非空行 = 哨兵；派生失败由 runner 一次性 `--finish` 恢复或判 `degraded`。
- **watcher**：判定表与退出码不变；可选 `--raw-stream` 只输出成长/字节证据；自测覆盖非终止哨兵、终止哨兵、派生失败、脱离存活。
- **脱离**：远端保留 `ssh+su+nohup`；本地 `nohup ... </dev/null >runner-log 2>&1 &`（可用时 `setsid`）；派发记录 `detached`；重入 `--once` 只核验不重派。

### Verification & Mutation Plan (red-first)

- **Red-first**：5 个新脚本（`admission-check.py`、`derive-live-log.py`、`audit-test-budget.py`、`audit-plan-changes.py`、`stage-runner.sh`）与 watch-target 扩展均先写失败测试，再实现；每个 red 运行的时间、命令与失败断言记入 `verification.md`，不事后补记。
- **变异演练**（实现期逐项执行、立即还原、记录证据；任一项未变红即视为该测试不设防）：

| 目标 | 变异 | 必须变红的测试 |
|------|------|----------------|
| admission-check | 放宽 FR/任务区间端点；把 SC 行计入 FR；删去 (c)/(d) 扫描；接受多行 lines manifest | `test_admission_check.py` 边界/计数/路径/单线用例 |
| derive-live-log | 对非终止事件输出裸哨兵；在 result 之前追加结果文本；删除 result 提取 | `test_derive_live_log.py` 三类哨兵用例 |
| audit-test-budget | 允许第三个槽位；缺 `exception_reason` 仍通过；用计数比较替代名称级差集；忽略日志扫描命中 | `test_audit_test_budget.py` 槽位/例外/差集/扫描用例 |
| audit-plan-changes | 忽略未提交改动；忽略空声明仍判 declared | `test_audit_plan_changes.py` 未声明/未提交用例 |
| stage-runner | stream 能力可用时强选 buffered；跳过 status 写入；去掉 detached 记录 | runner 集成测试（stream/degraded/detached） |
| watch-target | 让进度增长产生 DONE；从 raw 直接读哨兵 | `watch-target.sh --self-test` 与 stream 用例 |

- **既有断言的有意更新**：C-3 的 H2 集合新增 `Efficiency Optimizations` 一节；C-4 的 `sed` 派生断言改为 `stage-runner.sh`。两项在 tasks 中以独立任务记录理由，禁止静默删除。
- **镜像与基线**：每个脚本落盘后跑 `sync-mirrors.py --write --only skills/external`，以 `--check` 本对零 drift 为验收；全量测试的 name-level 基线在 implement 起点冻结，变异演练后复跑并确认零新增失败。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/063-sdd-loop-efficiency/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — R-1…R-10 + 基线实测
├── data-model.md        # Phase 1 output — E1…E8 + 30 条校验规则
├── quickstart.md        # Phase 1 output — S1…S7（逐例前提与钉住者）
├── contracts/           # Phase 1 output — 5 文件 49 条款
│   ├── fast-lane.md
│   ├── test-budget.md
│   ├── plan-constraint.md
│   ├── progress-decoupling.md
│   └── delivery-and-invariants.md
├── feature-ref.md       # Phase 1 output — FR/SC 映射 + 交付清单 + 基线
├── requirements.md      # /speckit.requirements 产物（已澄清）
├── checklists/requirements.md  # 需求质量清单（16/16）
├── notes/source-requirement.md # dated brief 快照
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/                 # 技能唯一承载面（源）
skills/external/sdd-loop-driver/references/      # efficiency-model（新 owner）+ 三份既有手册更新
skills/external/sdd-loop-driver/scripts/         # 5 个新脚本 + watch-target.sh 扩展
docs/reference/skills/                           # sdd-loop-driver 用户文档页更新
tests/contract/                                  # 新增效率条款契约 + 有意更新既有 loop-driver 契约
tests/unit/                                      # 4 个脚本单测
tests/integration/                               # runner 脱离/降级 + 名称级回归集成
tests/fixtures/sdd_loop_efficiency/              # 中型/大型 spec、stream 事件、stub CLI、临时 repo 夹具
.specify/memory/features/                        # 058 扩展规划记录
.specify/memory/features.md                      # 索引 Last Updated 注记
```

**Structure Decision**: 本特性落在既有框架源布局内，无新顶层目录：四项优化全部进入 `skills/external/sdd-loop-driver/` 的 references 与 scripts 面；docs 页在同目录惯例路径更新；测试进入既有 `tests/{contract,unit,integration,fixtures}` 分层。不新增技能目录、不新增 command/template、不触碰 `.specify/templates/commands/`。

### Mirror Obligations *(mandatory)*

同步引擎：`scripts/python/sync-mirrors.py`（`skills/external` ↔ `.specify/skills` 对）。**基线漂移（2026-10-20 实测）**：`--check --only skills/external` 退出码 2，68 个 DIFF 跨 12 个技能目录；其中本特性拥有的 sdd-loop-driver 3 文件（SKILL.md、references/dispatch-recipes.md、references/watch-model.md）已 DIFF（镜像含 `.specify/` 前缀路径与不同 fingerprint），既有契约 C-12/C-18 因此红。完整清单见 `research.md` B-2。本特性 MUST 在实现期用 `sync-mirrors.py --write --only skills/external` 把 sdd-loop-driver 修复为源→镜像一致（契约测试为权威），并以「本对零 drift」为验收；其余 11 个目录的既有漂移不属本特性面，采用「零 NEW drift」相对判据并完整披露。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md`、`references/*.md`、`scripts/*` | `.specify/skills/sdd-loop-driver/` 同名文件 | `python3 scripts/python/sync-mirrors.py --write --only skills/external` 后 `--check --only skills/external` 输出 ok（本对零 drift）；新增脚本保持可执行位 |
| `skills/external/sdd-loop-driver/SKILL.md` 的编译 `## Wrap-up` 面 | 同文件镜像 | 不编辑该面；`probe-utils.py --action compile-embeds --check` 零漂移（若 scan 认领不变） |
| `docs/reference/skills/sdd-loop-driver.md` | 无镜像 | docs 漂移检查/文档结构测试 |
| `tests/contract/*`、`tests/unit/*`、`tests/integration/*`、`tests/fixtures/*` | 无镜像（tests 不在 MIRROR_PAIRS） | pytest 直跑 |
| `.specify/memory/features/058.md`、`.specify/memory/features.md` | 无镜像（运行时记忆） | 索引一致性检查；状态不回退 |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First 判 ⚠ Partial | 确定性组件（准入/派生/台账/plan 分类/脱离/名称级回归）全部有单元或集成测试；但端到端阶段序列由 LLM 按提示词执行，CI 无法真实重放 driver。实现期以录制编排 trace 作为该层证据，并在 verification.md 如实标注。 | 把 driver 改写成可自动调度的运行时以换取端到端 CI——违反宪法 IX（框架是提示词而非运行时平台），且会替换本特性要优化的对象；058 先例同样以录制演练 + 结构契约承载不可自动化的部分。 |

## Phase 0: Research Review

独立 `research.md` 已产出（超过 50 行，含基线实测与替代方案）。关键结论：

- **R-1**：runner 打包为参数化 `stage-runner.sh`，取代逐阶段 sed 派生；既有契约 C-4 的 `sed` 断言有意更新（理由：单点可测试、消除每阶段副本漂移）。
- **R-2**：派生自包含实现（不复用 internal create-team 脚本），事件形状取既有 Visibility Contract；result 文本置尾。
- **R-3**：准入用 `admission-check.py`，七判据全部机械判定（无自证），fail-closed；阈值由契约测试钉住。
- **R-4**：预算台账 = 状态脊 JSONL 围栏 + 阶段证据文件 + 审计脚本；名称级 `comm -13`。
- **R-5**：plan 约束只在编排层；`audit-plan-changes.py` 机械判定 touched/undeclared，驱动做语义分类与两分支路由；每次实质改动按其分支处置并留痕，重复回环由既有 stall/retry 纪律兜底。
- **R-6/R-7**：本地补 nohup；watcher 只加 `--raw-stream` 证据面，判定表/退出码零改动；既有 4 个平台/时序自测缺陷一并修正。
- **R-8**：SKILL.md 新增一个 H2 + 有意更新两条既有断言，理由记录。
- **R-9/R-10**：全部证据落文件；确定性组件自动化，LLM 序列用录制 trace，证据形态如实区分。

基线异常（已取证、非本特性引入、按机制侧修复）：watcher 自测 12/4（macOS 平台 + 时序）、镜像三文件漂移导致既有契约 2 红。两项均写入 `feature-ref.md` 基线记录与实现任务，不静默修平。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 8 实体（E1 准入记录 / E2 预算台账 / E3 定向证据 / E4 plan 约束 / E5 plan 改动分类 / E6 派发记录 / E7 raw-live 对 / E8 状态脊）+ 30 条校验规则（E1×5 + E2×6 + E3×3 + E4×3 + E5×4 + E6×3 + E7×3 + E8×3） |
| Contracts | [`contracts/`](contracts/) | 5 文件 49 条款：fast-lane.md（FL-01…FL-10）、test-budget.md（TB-01…TB-10）、plan-constraint.md（PC-01…PC-10）、progress-decoupling.md（PD-01…PD-10）、delivery-and-invariants.md（DI-01…DI-09）；每文件带 FR/测试追溯表 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 场景（S1 录取 / S2 拒绝 / S3 台账审计 / S4 派生哨兵 / S5 本地脱离 / S6 plan 分类 / S7 端到端录制演练）；每条带前提与钉住者 |
| Feature ref | [`feature-ref.md`](feature-ref.md) | FR 43/43 + SC 13/13 映射；23 项交付清单；基线记录；显式排除；自应用声明 |
| Research | [`research.md`](research.md) | R-1…R-10 + B-1…B-7 基线实测 |

Phase 0 预期 vs 实际：实体 8（预估 7–8 ✓）；契约文件 5（预估 4–5 ✓）；条款 49（预估 40–50 ✓）；quickstart 场景 7（预估 6–7 ✓）；无漂移需修正项。
