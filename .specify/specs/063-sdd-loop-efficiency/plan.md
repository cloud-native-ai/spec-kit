# Implementation Plan: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Branch**: `063-sdd-loop-efficiency` | **Date**: 2026-10-20 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `063-sdd-loop-efficiency` → Feature 058 无人值守 SDD 循环驱动机制
**Input**: Specification from `.specify/specs/063-sdd-loop-efficiency/requirements.md`

## Summary

在编排层为 `sdd-loop-driver` 增加四项吞吐优化，不修改任何框架阶段命令内部：① 中型特性快车道（入口 [[STR-006]] 显式启用，`tasks` 后以制品实测七判据裁决，跳过 `checklist` 但保留 `analyze`/`review`，fail-closed 回退；被跳过的 checklist 记 [[STR-008]]、不计入完整性分母）；② 每线两个全量测试槽位（implement 起点 baseline、review 后收口 closure），中间阶段与 review 只用固定程序 `targeted-set-v1` 选择的定向集并留证据；③ plan 完成后「只小修、不重审」约束（编排层执行，U4 按最终 diff 分类，实质改动走两分支；已批准需求基线锚定 `plan_commit` 中的 `requirements.md`，分类记录写 `approved_baseline_commit`，框架内部硬执行显式排除）；④ 阶段 runner 默认 `--output-format stream-json`，原始事件流落盘，自包含派生紧凑实时日志（事件→派生行延迟 ≤120s），哨兵只认终止 `result` 文本；本地与远端都用 `nohup` 完全脱离驱动会话。

SC-010 以冻结提交上录制的三类卡死处置元组（[[STR-007]]）为行为基线，收口用同一驱动侧可执行夹具归一化重放比较；名称级测试失败基线只服务 SC-012。实现前复核（N-08）：冻结读数 `ba2a18db` 不适用，首个行为面提交为 `9e69f3de`，实际行为基线取父提交 `a1aac7e5`（见 § Plan Repair Record 第 5 轮）。镜像验收 = 本对零 drift + 全部镜像对相对 B-2 冻结清单零 NEW drift。

**CLI 能力档案归属（2026-10-20 裁决）**：CLI 能力档案（集合、八维、`known`/`unknown`、U2/U4/U5 观测、probe/feedback、契约与测试）唯一归属于 Feature 064（`contracts/cli-profiles.md` CLP-01…CLP-17、`.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`）。063 只保留 stream-json 输出默认（FR-026）与 nohup 脱离（FR-031），并只读引用 064 的 `references/cli/index.md`；不新增/修改 `references/cli/`、不注册 Probe Object、不定义 CP 契约或档案测试。

交付面 = 1 个技能（3 份既有 references 更新 + 1 份效率 owner 文档 + 5 个新脚本 + 1 个扩展脚本）+ docs 参考页 + 契约/单元/集成测试与夹具（含驱动侧卡死夹具）+ Feature 058 扩展记录。零新技能、零新命令、零常驻服务、零外部依赖、零模型 API。完成哨兵、watcher 判定状态机、退出码、确认门、独立校验与卡死处置保持不变。063 自身走完整阶段链，快车道只作用于未来运行。CLI 能力档案不属于本交付面（064 owner）。

## Technical Context

**Language/Version**: Markdown 技能面；Bash（runner/watcher，兼容 bash 3.2+ 的常见用法）；Python ≥3.8 仅标准库（准入/派生/台账审计/plan 改动判定）；测试为 pytest（仓库既有 contract/unit/integration 分层）
**Primary Dependencies**: 既有 `git`、`bash`、`python3`；既有 `scripts/bash/run-tests.sh`（名称级基线）；既有 `scripts/python/sync-mirrors.py`（镜像）；既有 `skills/external/sdd-loop-driver/scripts/watch-target.sh`。**不新增任何依赖**，不引入 `jq`/网络/模型 API
**Dispatch Eligibility**: supported CLI = Feature 061 的 `CAPABILITY_MATRIX` eligible 集合（owner: `scripts/python/execution-config.py`；Feature 详情 `.specify/memory/features/061.md`；064 `contracts/cli-profiles.md` CLP-15 同口径）。CLI 能力档案存在不等于可派发；063 只决定 stream-json 输出模式默认与 nohup 形态，不定义派发资格。
**Storage**: 文件即存储——状态脊 Markdown（准入记录、JSONL 台账围栏、plan 约束）、`<spec-dir>/test-evidence/<stage>.jsonl`、`baseline-failed.txt`/`final-failed.txt`、`notes/stall-behavior-baseline.json`（SC-010 行为基线）、阶段产物 raw/live/pid/status/heartbeat/runner-log。无数据库、无新服务。CLI 观测段与派发记录中的 CLI 查档字段由 064 的 `data-model.md` E10 扩展，本特性不定义。
**Testing**: Tests Mode **ON**。契约测试钉文档面与条款（5 份契约 / 50 条款）；单元测试钉四个 Python 脚本与驱动侧卡死夹具；集成测试钉 runner 脱离/降级与名称级回归；`watch-target.sh --self-test` 扩流式用例。既有契约测试 23/23 绿（plan 期为 21/23，镜像漂移已由合并 064 关闭），本特性保持绿色
**Target Platform**: Linux 与 macOS 驱动/执行宿主；远端拓扑 = `ssh + su + nohup` + Linux 执行侧；macOS 无 `/proc` 的 watcher 分支按平台跳过或退化
**Project Type**: 框架源（两顶帽子：改动落 `skills/external/`、`docs/`、`tests/`，镜像经 sync-mirrors 同步；`.specify/memory` 仅记录 Feature 扩展）
**Performance Goals**: 每线全量套件恰 2 槽位（需求方报告的一次运行 6 次为 dated baseline，本 plan 未复测、不据此宣称提速百分比）；事件→派生行延迟 ≤120s（无事件区间不适用；伪造进度行数为 0）；驱动零独立 `sleep` 回合；checklist 在中型夹具中派发 0 次
**Constraints**: 哨兵/判定状态机/退出码/确认门/独立校验/卡死处置不变；快车道默认关且仅显式启用；预算不得静默超支；plan 约束不改框架内部；CLI 能力档案不属本特性（064 owner），本特性不复制其档案、契约或测试；无新服务/依赖/API；063 自身完整链
**Scale/Scope**: 1 个技能；references = 3 份既有更新 + `efficiency-model.md`；6 个 scripts（5 新 + 1 扩）；1 个 docs 页；5 个契约文件 / 50 条款；2 个契约测试文件（1 新 + 1 有意更新）；4 个单元测试；2 个集成测试；1 个夹具目录（含驱动侧卡死夹具）；Feature 058 两个登记面。CLI 档案/契约/测试/Probe Object = 064 拥有，不计入本特性交付。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，共 16 项；初步自评，同作者门委派复核见 Re-check）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `feature-ref.md` FR-001…043 逐行映射到设计落点；每个设计决定在 `research.md` R-1…R-12 有理由与替代方案 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 058（演化特性）；扩展切片规则：状态保持 `Implemented`，只更新 Feature detail 与索引 Last Updated；未新建 Feature |
| III | Intent-Driven Development | ✅ Pass | 先定义「快车道何时可信、预算如何不丢回归、plan 约束边界、脱离后如何接管」，再给命令形态；四项优化的取舍和显式排除在 research/contracts。CLI 行为知识由 064 拥有，本特性只引用 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Tests Mode ON；5 个新脚本按 red-first 编写并配单元测试；50 个契约条款、决策表策略测试、FR-042(a)–(e) 夹具、名称级回归集成测试。SC-010 卡死处置以 `a1aac7e5` 行为基线（[[STR-007]]）录制与归一化重放证明（冻结读数 `ba2a18db` 因 064 行为面提交 `9e69f3de` 而不适用，见第 5 轮记录）；名称级基线只服务 SC-012。LLM 驱动的端到端阶段序列无法在 CI 自动化，由实现期录制 trace 证明（见 Complexity Tracking） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增/变更 agent provider；沿用 qodercli/claude 的 stream-json 事件形状；`AGENT_CONFIG` 与 `_ASSISTANT_TIERS` 零改动 |
| VI | Continuous Quality & Observability | ✅ Pass | raw/live 双证据、四件套、状态脊、准入记录、预算台账、plan 分类、收尾汇总；失败与降级均显式留痕 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature 058 已在册；本 plan 产出四件套 + research；不越权推进 `Implemented`；Pre-Status-Flip Gate 留给 implement |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 以源码/测试实测校准：watcher 判定表、runner 四件套、`--names-out`、镜像引擎、stream-json 先例；文档不覆盖代码事实 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | runner 是单阶段 shell 进程，不是调度器/平台；无常驻服务、无新依赖；四个脚本各自单一职责，可被删除而不留基础设施 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件走既有命名面：`references/efficiency-model.md`、`scripts/*.sh|*.py`（小写）、`docs/reference/skills/sdd-loop-driver.md`；`SKILL.md` 保留工具强制名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制修复落框架源侧 `skills/external/`，镜像经 sync-mirrors 同步；063 自身完整链；基线缺陷（watcher 自测、镜像漂移）披露并按机制侧修复 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `sync-mirrors.py`（有 Tool 记录）、`run-tests.sh`、`watch-target.sh`；查 `.specify/memory/tools/` 无 stream 派生/准入/台账同能力记录，按预期编写新脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（脱离/可见）、Change Validation（两槽位/定向证据）、Learning Capture（台账/收尾）；证据区分自动测试与录制 trace，不把 configured 当 used |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 四项机制由 `references/efficiency-model.md` 单一 owner；CLI 行为知识由 064 的 `references/cli/` 单一 owner（本特性只读引用，不复制）；SKILL/docs 只摘要+指针；字段面由 `data-model.md` 拥有；阈值/退出码由脚本与契约测试钉住，不在多处复述 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | docs 页与 quickstart 面向未参与运行的维护者/操作者；每个术语首次出现给上下文；quickstart 每条示例带前提与钉住者；CLI 档案的 known/unknown 与证据指针由 064 文档承载 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 准入 fail-closed、plan 实质改动显式异常行、派生降级不伪完成、基线异常披露；无静默超预算/静默跳过/静默重审；CLI 观测异常按 064 的既有 U5/重试程序处置 |

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
- **计数口径**：准入只使用 FR-003(a) 的窄模式（FR 定义行 `^- **FR-[0-9]{3}**:`；任务行 `^- \[[ xX]\] T[0-9]{3}`）；宽模式 `^- \[[ xX>~]\] T[0-9]{3}` 仅用于仓库任务记账（tasks.md 当前 53 行，tasks-repair-3 后），MUST NOT 用于准入，两者不得混用；当前 requirements 为 43 条 FR 定义行（tasks-repair-2 收口 CLI-profile 条款后复算），准入夹具始终以窄模式为准。
- **录取**：状态脊写入 E1 记录 + [[STR-003]]；派发 `analyze`，跳过 `checklist`；`implement`/`review` 提示词携带跳过标记与准入证据指针。
- **回退**：`analyze` 等阶段发现新引擎/安全面/任务越界 → 回退完整链，补派 `checklist`；若 `analyze` 已过则补派后重过 analyze 一次。
- **不变量**：`analyze`/`review` 门判据、回环上限、独立校验完全不变。

### ② 两槽位测试预算

- **槽位**：`baseline`（implement 首任务前，`run-tests.sh --names-out baseline-failed.txt`）与 `closure`（review 后合并前，`--names-out final-failed.txt` + `comm -13`）。
- **中间阶段/review**：`targeted-set-v1` 固定程序选定向集——输入 `stage_base`、工作树改动与 `test_roots`，按三条并集（改动路径覆盖、交付物契约测试、夹具改动测试）做固定字符串映射，`LC_ALL=C sort -u` 输出每行一个测试路径；算法 owner = `contracts/test-budget.md` TB-05，`efficiency-model.md` §2.3 为实现载体。阶段记录完整命令、`stage_base`、输出与充分性；空集且改可执行面 → 扩大或显式例外。快车道授权跳过的 `checklist` 记 [[STR-008]]，不产生测试运行、不计入完整性分母。
- **台账**：状态脊 JSONL 围栏（E2）+ 阶段证据文件（E3）；`audit-test-budget.py` 审计槽位、例外、环境失败与 unknown。E2 是唯一台账；本地 `spine_write_mode=direct`，远端 `transport` 由执行侧写 `<spec-dir>/test-evidence/implement.jsonl` 传输行，驱动合并进状态脊并记 `merge_source`/`merged_at`，合并前不得作为审计来源。
- **完整性**：每个适用阶段恰有一条 E3 `row_type=stage-status` 行；`not-run-docs-only` 按缩减字段集（stage/status/selection_basis/changed_paths/evidence_ptr + row_type）判完整，运行字段不适用且不报 unknown；授权跳过记 [[STR-008]] 不入分母；整阶段缺行计入分母；审计输出 `stages=N complete=N`。
- **修复循环**：收口新失败 → 修复或归因；修复重跑同一套件记 `in-slot-rerun`；实现阶段 closure-repair 重入不再消耗 baseline。

### ③ Plan 只小修约束

- **生效**：plan U4 通过时状态脊 `plan_constraint=active`，记录 `plan_commit` 与 `approved_baseline_commit`（初始 = `plan_commit`）；下游四阶段提示词携带只小修块。
- **声明**：任何 plan 制品改动须在哨兵前回传 `PLAN-EDIT:` 声明行；完整格式由 `references/efficiency-model.md` §3.2 单一 owner 定义（本 plan 不复写）。
- **校验**：`audit-plan-changes.py` 机械输出 touched/declared；驱动按最终 diff 分类 minor/substantive/undeclared；未声明或实质 → 阶段门失败。
- **分流**：修复既有缺陷且不变更批准面 → 一次完整 plan 重审 + U4 复验；改变批准面/新能力/无法判定 → 四要素上送。判定比较对象 = E4 最新 `approved_baseline_commit` 中 `requirements.md` 的 FR/SC 定义集合与语义；分类记录写该值，不得用工作树文本或其它提交替代。每次实质改动都按其分支处置并留痕；重复回环由既有 stall/retry 纪律兜底，不设人工次数上限。
- **Re-anchoring**：plan 约束激活后，`requirements.md` 的任何门内变更（analyze 路由修复、clarify 写回、显式范围修订）必须在下一个依赖该基线的 U4 分类前触发 re-baseline：E4 记录事件（触发/时间/前基线/新基线/差异摘要）并更新 `approved_baseline_commit`；未提交或无法定位提交时不得 re-anchor，受影响 plan 改动按 (b) 上送。re-anchoring 不构成 plan 重审，不移动约束生效点；新基线所含需求对应的 plan 改动按两分支正常分类，不得因旧基线缺该需求而误判越界。本特性自身即实例：plan U4 在 `5ab8a5e7`，requirements-repair 第 1 轮在 `0c719b80`、第 2 轮在 `864940de`；plan-repair-2 的 requirements delta 在 `bcf27c77`，tasks-repair-2 的 CLI-profile 收口 requirements 变更提交是下一个锚点候选。CLI 能力档案本身由 064 拥有，其 profile 内容不进入本特性的已批准需求基线。
- **显式排除**：框架命令内部硬执行不做；手工调用不受约束；若编排层不安全，另立特性。

### ④ 进度可见与脱离

- **runner**：`scripts/stage-runner.sh` 参数化；auto 模式探测 `--output-format` 能力；stream 模式 `CLI | tee raw.jsonl | derive-live-log.py > live.log`。
- **派生**：非终止事件只输出带前缀进度行；EOF 时追加终止 `result` 文本，保证 live log 最后非空行 = 哨兵；派生失败由 runner 一次性 `--finish` 恢复或判 `degraded`。
- **watcher**：判定表与退出码不变；可选 `--raw-stream` 只输出成长/字节证据；自测覆盖非终止哨兵、终止哨兵、派生失败、脱离存活。
- **脱离**：远端保留 `ssh+su+nohup`；本地 `nohup ... </dev/null >runner-log 2>&1 &`（可用时 `setsid`）；派发记录 `detached`；重入 `--once` 只核验不重派。

### ⑤ CLI 行为知识边界（064 owner；本特性只读引用）

- **归属**：CLI 能力档案的集合、八维、`known`/`unknown`、provenance、U2/U4/U5 观测、probe/feedback、契约与测试由 Feature 064 唯一拥有（`contracts/cli-profiles.md` CLP-01…CLP-17；`.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`）。063 MUST NOT 新增/修改 `references/cli/`、复制档案内容、注册 Probe Object 或建立第二套 CP 契约/测试。
- **本特性保留**：stream-json 输出默认（FR-026）与 nohup 脱离（FR-031）是 064 档案（CLP-02/04/08、CLP-13）记录的既有事实；064 只读引用，不改写本特性的输出模式默认。
- **派发边界**：063 的 E6/E8 只保留基础派发与状态脊字段；CLI 查档字段与 `cli_observations` 由 064 `data-model.md` E10 定义。063 实现 stream-json/nohup 时可按 064 `references/cli/index.md` 只读查档，但不得把档案更新当作行为修复或改变当前阶段判定。

### Verification & Mutation Plan (red-first)

- **Red-first**：5 个新脚本（`admission-check.py`、`derive-live-log.py`、`audit-test-budget.py`、`audit-plan-changes.py`、`stage-runner.sh`）、watch-target 扩展与驱动侧卡死夹具均先写失败测试，再实现；每个 red 运行的时间、命令与失败断言记入 `verification.md`，不事后补记。CLI 档案 schema/观测测试属于 064，不在本特性 red-first 范围。
- **卡死行为基线（SC-010）**：实现首个行为面提交之前，在实际行为基线提交 `a1aac7e5` 的只读 worktree 上（冻结读数 `ba2a18db` 不适用：首个行为面提交为 `9e69f3de`，见第 5 轮记录），用**驱动侧可执行夹具** `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` 录制三类处置元组到 [[STR-007]]：stub runner 产生受控 pid/status/heartbeat/runner-log 与 rc，真实 `watch-target.sh` 提供 U3 判定，夹具执行文档化的 U4/U5 驱动侧程序（状态脊先写后动、重试消耗、四要素上送件、下一阶段派发决策）并观测七个字段；watcher 自动夹具只提供 U3，录制 trace 只作补充证据。夹具 MUST NOT 从判定表转录或硬编码期望值，`initial_retries=0`，`exit_code` 分为 `{watcher, runner}`。录制不是全量测试运行，不消耗 FR-011 槽位。收口用同一夹具与同一初始重试数在当前树重放，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较，零差异为通过；名称级基线只服务 SC-012。
- **变异演练**（实现期逐项执行、立即还原、记录证据；任一项未变红即视为该测试不设防）：

| 目标 | 变异 | 必须变红的测试 |
|------|------|----------------|
| admission-check | 放宽 FR/任务区间端点；把 SC 行计入 FR；删去 (c)/(d) 扫描；接受多行 lines manifest；把宽任务模式用于准入 | `test_admission_check.py` 边界/计数/路径/单线/窄宽模式用例 |
| derive-live-log | 对非终止事件输出裸哨兵；在 result 之前追加结果文本；删除 result 提取 | `test_derive_live_log.py` 三类哨兵用例 |
| audit-test-budget | 允许第三个槽位；缺 `exception_reason` 仍通过；用计数比较替代名称级差集；忽略日志扫描命中；遗漏 docs-only 缩减字段或 `stages=N complete=N` | `test_audit_test_budget.py` 槽位/例外/差集/扫描/完整性用例 |
| audit-plan-changes | 忽略未提交改动；忽略空声明仍判 declared；忽略 re-baseline 后的新锚点 | `test_audit_plan_changes.py` 未声明/未提交/re-anchor 用例 |
| stage-runner | stream 能力可用时强选 buffered；跳过 status 写入；去掉 detached 记录 | runner 集成测试（stream/degraded/detached） |
| watch-target | 让进度增长产生 DONE；从 raw 直接读哨兵 | `watch-target.sh --self-test` 与 stream 用例 |
| driver-stall-fixture | 把 `initial_retries` 改为非 0；从场景→期望值表转录字段；翻转下一阶段派发/先写后动顺序 | 基线 vs 收口逐字段比较必须失败（SB-5 反转录） |

- **既有断言的有意更新**：C-3 的 H2 集合新增 `Efficiency Optimizations` 一节（`CLI Capability Profiles` 节由 064 拥有且已在该集合中，本特性 MUST NOT 删除或改写）；C-4 的 `sed` 派生断言改为 `stage-runner.sh`。两项在 tasks 中以独立任务记录理由，禁止静默删除。
- **镜像与基线**：每个脚本落盘后跑 `sync-mirrors.py --write --only skills/external/sdd-loop-driver`，以 `--check --only skills/external/sdd-loop-driver` 本对零 drift 为验收；另跑 `--check --only skills/external` 并与 `research.md` B-2 冻结清单（预合并 68 DIFF / 12 目录）比较，本特性面以外的既有 DIFF 不得新增（零 NEW drift）。2026-10-20 合并 064 后实测为 62 DIFF / 12 目录、本对 0 DIFF，作为实现起点的当前读数。全量测试的 name-level 基线在 implement 起点冻结，变异演练后复跑并确认零新增失败（只服务 SC-012）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/063-sdd-loop-efficiency/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — R-1…R-12 + B-1…B-8 基线实测
├── data-model.md        # Phase 1 output — E1…E8 + 41 条 E 校验规则 + 卡死行为基线（SB-1…SB-5）
├── quickstart.md        # Phase 1 output — S1…S7（逐例前提与钉住者）
├── contracts/           # Phase 1 output — 5 文件 50 条款
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
skills/external/sdd-loop-driver/references/cli/  # 064 拥有（index + 五份档案）；本特性只读引用，不修改
skills/external/sdd-loop-driver/scripts/         # 5 个新脚本 + watch-target.sh 扩展
docs/reference/skills/                           # sdd-loop-driver 用户文档页更新
tests/contract/                                  # 新增效率条款契约 + 有意更新既有 loop-driver 契约
tests/unit/                                      # 4 个脚本单测 + 驱动侧卡死夹具 `--self-test`
tests/integration/                               # runner 脱离/降级 + 名称级回归集成
tests/fixtures/sdd_loop_efficiency/              # 中型/大型 spec、stream 事件、stub CLI、临时 repo、driver-stall-fixture
.specify/memory/features/                        # 058 扩展规划记录
.specify/memory/features.md                      # 索引 Last Updated 注记
```

**Structure Decision**: 本特性落在既有框架源布局内，无新顶层目录：四项优化进入 `skills/external/sdd-loop-driver/` 的 references 与 scripts 面；docs 页在同目录惯例路径更新；测试进入既有 `tests/{contract,unit,integration,fixtures}` 分层。`references/cli/` 与 Probe Object `skill-sdd-loop-driver-cli-profile` 由 064 拥有，本特性不新增、不修改、不注册。不新增技能目录、不新增 command/template、不触碰 `.specify/templates/commands/`。

### Mirror Obligations *(mandatory)*

同步引擎：`scripts/python/sync-mirrors.py`（`skills/external` ↔ `.specify/skills` 对）。**基线漂移**：plan 期（合并 064 前）实测 `--check --only skills/external` 退出码 2，68 个 DIFF 跨 12 个技能目录，其中 sdd-loop-driver 3 文件；2026-10-20 合并 064 后复测为 62 DIFF / 12 目录、sdd-loop-driver 对 0 DIFF（完整清单与先后读数见 `research.md` B-2）。本特性 MUST 在实现期用 `sync-mirrors.py --write --only skills/external/sdd-loop-driver` 维持本对源→镜像一致，并以「本对零 drift」为验收；另以 `--check --only skills/external` 对照冻结清单，其余目录的既有漂移不属本特性面，采用「零 NEW drift」相对判据并完整披露。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md`、`references/*.md`（不含 `references/cli/`，该目录由 064 拥有）、`scripts/*` | `.specify/skills/sdd-loop-driver/` 同名文件 | `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 后 `--check --only skills/external/sdd-loop-driver` exit 0（本对零 drift；`references/cli/` 只验证字节一致，不得修改内容）；`--check --only skills/external` 相对冻结清单零 NEW drift；新增脚本保持可执行位 |
| `skills/external/sdd-loop-driver/SKILL.md` 的编译 `## Wrap-up` 面 | 同文件镜像 | 不编辑该面；`probe-utils.py --action compile-embeds --check` 零漂移 |
| `docs/reference/skills/sdd-loop-driver.md` | 无镜像 | docs 漂移检查/文档结构测试；不复制 064 的 CLI 档案内容 |
| `tests/contract/*`、`tests/unit/*`、`tests/integration/*`、`tests/fixtures/*` | 无镜像（tests 不在 MIRROR_PAIRS） | pytest 直跑 |
| `.specify/memory/features/058.md`、`.specify/memory/features.md` | 无镜像（运行时记忆） | 索引一致性检查；状态不回退 |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First 判 ⚠ Partial | 确定性组件（准入/派生/台账/plan 分类/脱离/名称级回归/驱动侧卡死夹具）全部有单元或集成测试；SC-010 卡死处置以 `a1aac7e5` 上的行为基线（[[STR-007]]）与 `driver-stall-fixture.py` 的观测/归一化重放作为确定性证据（禁止判定表转录/硬编码期望值）；但端到端阶段序列由 LLM 按提示词执行，CI 无法真实重放 driver。实现期以录制编排 trace 作为该层证据，并在 verification.md 如实标注。 | 把 driver 改写成可自动调度的运行时以换取端到端 CI——违反宪法 IX（框架是提示词而非运行时平台），且会替换本特性要优化的对象；058 先例同样以录制演练 + 结构契约承载不可自动化的部分。 |

## Phase 0: Research Review

独立 `research.md` 已产出（超过 50 行，含基线实测与替代方案）。关键结论：

- **R-1**：runner 打包为参数化 `stage-runner.sh`，取代逐阶段 sed 派生；既有契约 C-4 的 `sed` 断言有意更新（理由：单点可测试、消除每阶段副本漂移）。
- **R-2**：派生自包含实现（不复用 internal create-team 脚本），事件形状取既有 Visibility Contract；result 文本置尾。
- **R-3**：准入用 `admission-check.py`，七判据全部机械判定（无自证），fail-closed；阈值由契约测试钉住。
- **R-4**：预算台账 = 状态脊 JSONL 围栏 + 阶段证据文件 + 审计脚本；名称级 `comm -13`。
- **R-5**：plan 约束只在编排层；`audit-plan-changes.py` 机械判定 touched/undeclared，驱动做语义分类与两分支路由；每次实质改动按其分支处置并留痕，重复回环由既有 stall/retry 纪律兜底。
- **R-6/R-7**：本地补 nohup；watcher 只加 `--raw-stream` 证据面，判定表/退出码零改动；既有 4 个平台/时序自测缺陷一并修正。
- **R-8**：SKILL.md 新增一个 H2（`Efficiency Optimizations`）+ 有意更新既有 C-3/C-4 断言，理由记录。`CLI Capability Profiles` 节由 064 拥有且已在该 H2 集合中，本特性不修改。
- **R-9/R-10**：全部证据落文件；确定性组件自动化，LLM 序列用录制 trace，证据形态如实区分。
- **R-11**：CLI 能力档案的唯一 owner 是 Feature 064（`references/cli/index.md`、`contracts/cli-profiles.md`、Probe Object `skill-sdd-loop-driver-cli-profile`）；063 只保留 stream-json 默认与 nohup 事实并由 064 引用，不复制档案、不注册 Object、不新增 CP 契约/测试。
- **R-12**：U-01R 的驱动侧字段由 `driver-stall-fixture.py` 观测产生（stub runner + 真实 watcher + 文档化 U4/U5 程序），禁止判定表转录/硬编码期望值；N-01 的 `state_spine_path` 进入 E6/E8 与阶段提示词骨架，远端走 transport→driver merge；N-02 的 re-anchoring 落 E4/E5 与 PC-11；N-03 的 docs-only 缩减字段集与 `stages=N complete=N` 落 E3/TB-06/07。

基线异常（已取证、非本特性引入、按机制侧修复）：watcher 自测 12/4（macOS 平台 + 时序）、镜像漂移导致既有契约 2 红。2026-10-20 合并 064 后，sdd-loop-driver 的 probe `embed without probe object` 缺口已由 064 的 `skill-sdd-loop-driver-cli-profile` 关闭；`skill:sdd-project-setup` 的同类缺口保留为既有例外并完整披露。以上均写入 `feature-ref.md` 基线记录与实现任务，不静默修平。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 8 实体（E1 准入记录 / E2 预算台账 / E3 定向证据 / E4 plan 约束 / E5 plan 改动分类 / E6 派发记录 / E7 raw-live 对 / E8 状态脊）+ 41 条 E 校验规则（原 32 + V-E2-7、V-E3-5/6、V-E4-4/5、V-E5-6、V-E6-4/6、V-E8-4）+ 一个非实体证据制品（卡死行为基线 SB-1…SB-5）；CLI 档案/观测字段指向 064 E9/E10 |
| Contracts | [`contracts/`](contracts/) | 5 文件 50 条款：fast-lane.md（FL-01…FL-10）、test-budget.md（TB-01…TB-10）、plan-constraint.md（PC-01…PC-11）、progress-decoupling.md（PD-01…PD-10）、delivery-and-invariants.md（DI-01…DI-09）；每文件带 FR/测试追溯表 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 场景（S1 录取 / S2 拒绝 / S3 台账审计 / S4 派生哨兵 / S5 本地脱离 / S6 plan 分类与 re-anchor / S7 端到端录制演练）；每条带前提与钉住者 |
| Feature ref | [`feature-ref.md`](feature-ref.md) | FR 43/43 + SC 13/13 映射；24 项交付清单；基线记录；显式排除；自应用声明 |
| Research | [`research.md`](research.md) | R-1…R-12 + B-1…B-8 基线实测（R-11/B-8 为 064 归属指针） |

Phase 0 预期 vs 实际：实体 8（预估 7–8 ✓）；契约文件 5（原预估 4–5 ✓；CLI 档案增量已裁决给 064，不计入本特性）；条款 50（原预估 40–50，含 PC-11）；quickstart 场景 7（原预估 6–7 ✓；S8 已裁决给 064）；初次产出无漂移需修正项（2026-10-20 analyze 门回环的 plan-owned 修复见 Plan Repair Record 第 1 轮；plan-repair-2 的本轮传播见第 2 轮；tasks-repair-2 的 CLI-profile 收口见第 3 轮）。

## Plan Repair Record（2026-10-20，analyze 门回环第 1 轮）

**触发**：`/speckit.analyze` 报告（0 CRITICAL / 2 HIGH / 10 MEDIUM / 1 LOW）中的 plan-owned 项：U-01/CHK036、A-01/CHK021、I-03/CHK033、I-02/CHK016、I-04/CHK037、U-03/CHK005、U-02/CHK012、I-06，以及 I-01 的 plan 侧正则。上游口径由 requirements-repair 提交 `0c719b80` 冻结（Clarifications Session 2026-10-20 第二轮）。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — 传播 SC-010 行为基线（[[STR-007]]）、事件→派生行延迟、approved_baseline_commit、[[STR-008]] 跳过语义、镜像选择器收窄与零 NEW drift；分类=substantive（新增证据制品/计时对象/字段引用），理由=实施 FR-038/FR-012/FR-022/FR-040 的已批准口径，不改变需求范围或任务分解。`
- `PLAN-EDIT: data-model.md — 新增 E1 lines.manifest 行语法 owner、E3 not-applicable-skipped-stage（V-E3-4）、E5 approved_baseline_commit（V-E5-5）、Stall Behavior Baseline 证据制品（SB-1…SB-4）；分类=substantive（字段面与证据制品扩展），理由=同上。`
- `PLAN-EDIT: contracts/fast-lane.md — FL-03(a) 计数正则改为引用 requirements FR-003(a) owner，FL-03(e) 引用 data-model E1 行语法 owner；分类=minor（引用与一致性修复，消除 I-01 plan 侧漂移）。`
- `PLAN-EDIT: contracts/test-budget.md — TB-05 固定选择程序 targeted-set-v1（输入/算法/排序/输出），TB-06/07 增加授权跳过语义与审计联结；分类=substantive（新增确定性算法与审计规则），理由=FR-013/FR-012/SC-005 已批准口径。`
- `PLAN-EDIT: contracts/plan-constraint.md — PC-01/PC-06 绑定 approved_baseline_commit = plan_commit 并要求以该提交的 requirements.md 比较；分类=substantive（分类输入字段），理由=FR-022 已批准口径。`
- `PLAN-EDIT: contracts/progress-decoupling.md — PD-02 增加事件→派生行延迟与派生行可追溯性；分类=substantive（计时对象与可追溯约束），理由=SC-007/FR-027 已批准口径。`
- `PLAN-EDIT: contracts/delivery-and-invariants.md — DI-03 行为基线、DI-05 镜像判据、DI-06 基线证据形态；分类=substantive（判据细化），理由=FR-038/SC-010/SC-012 已批准口径。`
- `PLAN-EDIT: feature-ref.md — FR-012/013/022/038/040 与 SC-005/007/010/012 映射更新，基线记录增加 [[STR-007]]；分类=minor（映射与引用一致性）。`
- `PLAN-EDIT: research.md — B-5 规格校验行补充 requirements-repair 后实测值（313 lines / 8 shared strings）；分类=minor（dated record 的当前值注记，不改设计决定）。`
- `PLAN-EDIT: quickstart.md — S1/S2 引用计数 owner、S3/S6 新口径、S7 补充卡死行为基线录制/重放；分类=minor（示例前提与引用更新，不新增场景编号）。`

**FR-022 分类与不重审理由**：本轮改动是 analyze 门回环中 plan 阶段自身的修复，不是 plan 约束激活后的下游阶段编辑。改动只把 requirements-repair 已冻结的口径落到 plan 设计面；不改变已批准的需求范围/FR/SC 语义、架构方向或任务分解范围。数据模型与契约的字段面扩展（`approved_baseline_commit`、`not-applicable-skipped-stage`、`targeted-set-v1`、[[STR-007]]）是该口径的唯一可实现形态，属于 FR-022(a) 所称「修复既有缺陷所必需」。因此不触发嵌套的完整 plan 重审；本阶段完整性由随后重跑 `/speckit.analyze` 复核（FR-023）。若驱动判断存在其它读法，按 FR-022(b) 四要素上送。

**假设**：

- `ba2a18db` 之后至实现首个行为面提交之间只含规格/计划/清单文档（requirements-repair 的自述），故 SC-010 行为基线冻结提交初取 `ba2a18db`；**实现前复核（第 5 轮）**发现 `ba2a18db` 之后的首个行为面提交为 `9e69f3de`，按 FR-038 改取首个行为面改动前的父提交 `a1aac7e5` 并在状态脊记录差异。
- `lines.manifest` 行语法 owner 选择 `data-model.md` E1（而非契约），因为 E1 已拥有 `lines_manifest_ptr` 字段且准入脚本输入以 E1 为准；FL-03(e) 只引用。
- `targeted-set-v1` 以现有 shell 工具实现，不新增脚本交付面；算法 owner 放 `contracts/test-budget.md` TB-05，`efficiency-model.md` §2.3 为实现载体并由契约测试钉住。
- SC-010 行为重放不是全量测试运行，不消耗 FR-011 的两个槽位；重试上限驾驶使用录制 trace，并在 `verification.md` 如实标注。

## Plan Repair Record（2026-10-20，plan-repair-2）

**触发**：① analyze-rerun 报告（0 CRITICAL / 1 HIGH / 4 MEDIUM / 2 LOW）的 plan-owned 项：U-01R（驱动侧字段同义反复）、N-01（`state_spine_path` / 远端证据合并 / T002 与 D-T3 兜底措辞）、N-02（requirements 变更后的 re-anchoring）、N-03（`not-run-docs-only` 缩减字段集与 `stages=N complete=N`）、N-05（窄/宽任务计数边界）；② plan-repair-2 曾在用户授权下临时加入 CLI Capability Profiles 增量。该增量已在 tasks-repair-2 按 064 的 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` 裁决迁入 064，并从本规格删除（见 Plan Repair Record 第 3 轮）。本轮保留的 plan 传播只覆盖 U-01R/N-01/N-02/N-03/N-05。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — 驱动侧卡死夹具、re-anchoring、state_spine_path/远端合并、docs-only 完整性、窄/宽计数边界与第 2 轮记录；分类=substantive（新增证据程序与字段引用），理由=实施 FR-022/FR-038/FR-012 口径，不改变四项核心优化的范围或既有任务分解。CLI-profile 增量已由第 3 轮删除。`
- `PLAN-EDIT: data-model.md — E2 增加 merge_source/merged_at（V-E2-7）、E3 增加 row_type/changed_paths 与 V-E3-5/6、E4 增加 approved_baseline_commit/rebaseline_events（V-E4-4/5）、E5 更新基线引用与 V-E5-6、E6 增加 state_spine_path/spine_write_mode（V-E6-4/6）、E8 增加 state_spine_path（V-E8-4）、SB 元组拆分 exit_code 并新增 SB-5 反转录；分类=substantive（字段面与证据制品扩展），理由=FR-022/FR-017/FR-038 已批准口径。CLI 字段/观测由 064 E10 拥有，已由第 3 轮移出。`
- `PLAN-EDIT: contracts/plan-constraint.md — PC-01/PC-06 绑定最新 approved_baseline_commit，新增 PC-11 re-anchoring；分类=substantive（分类输入与路由规则），理由=FR-022 已批准口径（N-02）。`
- `PLAN-EDIT: contracts/test-budget.md — TB-03 增加 state_spine_path/远端 transport→merge；TB-06 增加 docs-only 缩减字段集；TB-07 增加 stage-status 唯一性、stages=N complete=N、merge 校验；分类=substantive（证据字段与审计规则），理由=FR-012/FR-017 已批准口径（N-01/N-03）。`
- `PLAN-EDIT: contracts/fast-lane.md — FL-03(a) 增加窄/宽任务计数边界；分类=minor（引用澄清，不改判据语义；N-05）。`
- `PLAN-EDIT: contracts/progress-decoupling.md — PD-04 明确 BASH_* 超时上限不是阶段 deadline；分类=minor（边界澄清）。CLI 档案引用已由第 3 轮删除。`
- `PLAN-EDIT: contracts/delivery-and-invariants.md — DI-03 改为驱动侧可执行夹具、exit_code 双字段、initial_retries=0、反转录；DI-06 更新证据形态；分类=substantive（证据形态），理由=FR-038 已批准口径（U-01R）。references/cli/CP 交付项已由第 3 轮移出。`
- `PLAN-EDIT: quickstart.md — S3 增加 stages=N complete=N 与远端 merge 前提；S6 增加 re-anchor；S7 改为驱动侧可执行夹具；分类=substantive（证据形态），理由=同上。S8 CLI 档案场景已由第 3 轮删除。`
- `PLAN-EDIT: feature-ref.md — SC-005/010 证据更新、基线记录更新、交付清单重算；分类=substantive（映射与证据）。CLI 映射与交付项已由第 3 轮删除。`
- `PLAN-EDIT: research.md — 新增 R-12（U-01R/N 传播）；更新 B-5 的当前计数；B-8/R-11 改为指向 064 的归属记录；分类=minor（dated 证据与设计理由，不改既有决定）。`

**U-01R 传播（HIGH）**：

- **SB-2/SB-5**：三类场景统一由 `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` 驱动；stub runner 产生受控 pid/status/heartbeat/runner-log 与 rc，真实 watcher 只提供 U3 判定，夹具执行文档化 U4/U5 程序并观测七个字段；watcher 自动夹具不得作为驱动侧字段来源；录制 trace 只作补充。夹具禁止判定表转录/硬编码期望值/基线回填，只允许内部一致性断言；`initial_retries=0`，`retries_consumed` 按实际重试累加；`spine_write_before_action` 由可复核顺序产生。
- **exit_code 语义**：元组字段改为 `exit_code: {watcher, runner}`，分别记录 watcher 判定退出码与 runner/CLI rc；SC-010 的"七字段"计数不变（`exit_code` 内含两个子字段）。
- **DI-06**：契约测试钉住夹具输出与字段语义；`verification.md` 如实标注自动夹具 vs 录制 trace；禁止把名称级基线用于 SC-010。
- **quickstart S7 / feature-ref SC-010**：证据改为"驱动侧可执行夹具 + 真实 watcher"，trace 只作补充。
- **tasks-repair-2 义务**：T001 的录制步骤必须调用该夹具并把 `initial_retries=0`、`base_commit`、`recorded_at` 写入状态脊；T051 的收口重放必须调用同一夹具并做归一化逐字段比较；两处都不得再写"按 U3/U4/U5 判定表记录"。

**N-01 传播（MEDIUM）**：

- **E6/E8**：`state_spine_path` 加入 U0 entry 与 E6；阶段提示词骨架加入 `STATE_SPINE_PATH`、`EVIDENCE_DIR`、`SPINE_WRITE_MODE=direct|transport`；本地直写、远端 transport→driver merge；驱动是状态脊唯一权威写入者（本地可由阶段直接追加，但状态脊仍是唯一台账）。
- **E2**：`merge_source`/`merged_at` 记录远端或传输合并来源；V-E2-7 要求 merge 后槽位语义一致，合并前不得审计。
- **T002 与 D-T3 统一措辞**：`test-evidence/implement.jsonl` 只是传输载体，不是台账、不是审计来源、不是"兜底"；remote 模式允许它承载 E2 形态行，但驱动必须在 closure 前合并并记 `merge_source`；closure 审计在状态脊看不到 baseline 时必须失败。T002 的"不得用 test-evidence 兜底"改为"不得把它当台账/审计来源；remote transport 例外按 TB-03 合并"。

**N-02 传播（MEDIUM）**：

- **E4/E5/PC-11**：见上；`approved_baseline_commit` 初始 = `plan_commit`，re-baseline 后更新；未提交/不可定位 → 不 re-anchor，受影响 plan 改动走 (b)；re-anchoring 不构成 plan 重审、不移动生效点。
- **quickstart S6**：补充 re-anchor 前提与本特性实例（`5ab8a5e7` → `0c719b80` → `864940de` → 本轮 requirements delta 提交）。
- **feature-ref FR-022**：映射到 PC-11 与 E4 `rebaseline_events[]`。

**N-03 传播（MEDIUM）**：

- **E3/TB-06/TB-07**：每个适用阶段恰一条 `row_type=stage-status`；`not-run-docs-only` 六项缩减字段集；运行字段不适用、不报 unknown；授权跳过不入分母；整阶段缺行计入分母；审计输出 `stages=N complete=N`。
- **quickstart S3 / feature-ref SC-005**：期望输出和证据说明同步。

**N-05 传播（LOW）**：

- **FL-03(a)/plan §①**：准入只用窄模式；宽模式只作仓库记账；两者不混用；重入文件出现 `[>]`/`[~]` 时宽模式会多计，准入仍按窄模式。
- **tasks-repair-2 义务**：T001/T010/T013/T052 的计数说明必须区分窄/宽；两者当时恰好同数是巧合，不得写成"两者一致"。

**CLI Capability Profiles（已迁出）**：plan-repair-2 的临时 CLI-profile 增量已由 tasks-repair-2 按 064 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` 迁入 064（`contracts/cli-profiles.md` CLP-01…CLP-17）。本规格不再保留档案、契约、观测、Probe Object 或测试条款；064 是唯一 owner。

**tasks-repair-2 承接的未同步项**（本轮只修改 `tasks.md`）：

1. 不新增 US6 任务：CLI 档案/契约/测试/Probe Object 由 064 拥有；`tasks.md` 只记录指向 064 的边界说明，不出现 CLI-profile 实施任务。
2. 更新 T001/T051：驱动侧可执行夹具、`initial_retries=0`、`exit_code` 双字段、禁止判定表转录；更新 T002/D-T3：`state_spine_path` 与 transport→merge 统一措辞。
3. 更新 T025/T026/T027/T028/T052：PC-11 re-anchoring 与 E4 `rebaseline_events[]`；更新 T016/T019/T022/T052：`stages=N complete=N` 与 docs-only 缩减字段集；更新 T010/T013/T052：窄/宽计数边界。
4. 更新 T044/T045/T046：C-3 只新增 `Efficiency Optimizations` 一节；`CLI Capability Profiles` 节由 064 拥有且已在该集合中，不得删除、复制或改写；DoD-3 保持 50 条款（含 PC-11，不含 CP）；任务行数保持 52，不新增 CLI 任务（第 4 轮新增 T000 夹具作者行，非 CLI 任务）。
5. 更新 tasks 的 `Measured premises`：requirements 为 43 FR / 13 SC / 8 STR；契约 5 文件 / 50 条（含 PC-11；本轮的 49 计数已在第 4 轮纠正）；交付清单 24 项；数据模型 41 条 E 规则；quickstart 7 场景。

**本轮假设**：

- CLI 档案/观测/probe 由 064 拥有；063 需要 qodercli 行为事实时只读引用 064 `references/cli/qodercli.md` 与 `index.md`，不复制其内容。
- `BASH_DEFAULT_TIMEOUT_MS` / `BASH_MAX_TIMEOUT_MS` 的具体值由 064 档案记录；063 的 PD-04 只声明它们不是阶段 deadline，阶段 TIMEOUT 仍只由阶段 deadline 产生。
- `skill:sdd-project-setup` 的 probe reconcile 缺口保留为既有例外并披露；063 不注册任何 Probe Object，不修改 `shared/definitions/probe-definitions.md`。
- 本轮 requirements 收口提交后，若后续再有 requirements 变更，按 PC-11 在执行 U4 前 re-anchor；本轮的 requirements 提交本身是一次锚点候选。

## Plan Repair Record（2026-10-20，tasks-repair-2：CLI-profile 重叠收口）

**触发**：Feature 064 的 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` 与已实现资产（`references/cli/`、`contracts/cli-profiles.md`、Probe Object `skill-sdd-loop-driver-cli-profile`、`test_sdd_loop_driver_cli_profiles.py`）确认 064 是 CLI 能力档案的唯一 owner；063 的临时 CLI-profile 增量必须删除或改为指针，避免双 owner 与静默复制。本轮只做规格/规划收口，不实现代码。

**裁决结果**：

- 删除：063 的 provisional CLI-profile 契约（条款组与 Probe Object 注册设计，编号见 064）、US6、CLI-profile FR 条款组、SC 条款组、CLI 实体、CLI 边界用例、CLI 共享字符串、档案测试引用、CLI 档案与 README 交付项、最小 Probe Object 注册设计。
- 保留：快车道（checklist 跳过准入/回退）、两槽位测试预算、plan 只小修约束、stream-json 输出默认与 nohup 脱离；064 对后两项只读引用（CLP-08/CLP-13）。
- 指针：064 `requirements.md`（CLI 档案条款）、`contracts/cli-profiles.md` CLP-01…CLP-17、`.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`、`data-model.md` E9/E10、`references/cli/index.md`。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — 删除 §⑤ CLI Capability Profiles 设计、CLI 交付/镜像/Probe/测试条目与相关计数，新增“CLI 行为知识边界（064 owner）”指针与第 3 轮记录；分类=substantive（删除已迁出的能力面），理由=执行 064 的收编条款（CLP-17）与 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` 的逐条裁决，不改变四项吞吐优化的范围。`
- `PLAN-EDIT: data-model.md — 删除 CLI Capability Profile 证据制品、CLI schema 规则组、E6 CLI 查档字段与其校验规则、E8 CLI observations 与其校验规则，改为指向 064 E9/E10；分类=substantive（字段面收窄），理由=同一裁决；E1–E8 基础实体与其余 41 条校验规则不变。`
- `PLAN-EDIT: contracts/cli-profiles.md — 删除该 provisional 契约文件；分类=substantive（删除重复 owner），理由=064 是唯一 owner，仓库级守卫 `test_clp_17_no_063_duplicate_owner` 要求 063 不得保留第二份契约。`
- `PLAN-EDIT: contracts/progress-decoupling.md — PD-01/PD-04 的 CLI 行为事实与工具超时改为指向 064 的 `references/cli/` 与 CLP-02/CLP-08；分类=minor（指针与引用修复），理由=CLI-profile 契约已迁出 064，063 只保留 stream-json/nohup 行为规则。`
- `PLAN-EDIT: contracts/delivery-and-invariants.md — DI-01/DI-04/DI-05/DI-06/DI-09 删除 CLI 档案、CP 条款与 Probe Object 交付项及 FR-049/SC-014/SC-016 引用，DI-05 更新镜像基线表述，追溯表与覆盖核对重新映射；分类=substantive（交付面与引用面收窄），理由=同一裁决，消除悬空引用。`
- `PLAN-EDIT: quickstart.md — 删除 S8 CLI 档案查档/观测场景与相关清理/术语/钉住项，S6 锚点链更新；分类=minor（删除已迁出场景），理由=同一裁决，场景编号收口为 S1…S7。`
- `PLAN-EDIT: feature-ref.md — 删除 CLI 档案 FR/SC 映射、交付项与基线记录，更新为 43 FR / 13 SC / 24 项交付；分类=substantive（映射与交付面收窄），理由=同一裁决。`
- `PLAN-EDIT: research.md — 将 B-8/R-11 改为指向 064 的归属记录，更新 B-5 计数与未决项；分类=minor（dated 证据与指针），理由=同一裁决。`
- `PLAN-EDIT: tasks.md — 仅由 tasks 阶段更新：不新增 US6；T044 只新增 `Efficiency Optimizations` H2；T048 增加 064 归属守卫；计数与实测前提按 43 FR / 13 SC / 50 条款 / 24 交付 / 7 场景重算；分类=minor（任务侧收口），理由=同一裁决。`

**编号与计数**：FR 收口到 FR-043（43 条），SC 收口到 SC-013（13 条），Shared Strings 收口到 STR-008（8 条），契约 5 文件 / 50 条款（含 PC-11），数据模型 8 实体 / 41 条 E 规则，quickstart 7 场景，交付 24 项。所有引用由 `validate-requirements.py` 与 `validate-tasks.py` 复算，MUST exit 0。

**纠正类发现（就地修复并披露）**：PC-11 已在 plan-repair-2 引入，但 tasks.md 的 DoD-3、T026、T046、T049、Clause partition 与 plan 的若干计数仍写 49 条款且遗漏 PC-11。本轮统一为 50 条款，并把 `test_pc_11_reanchoring` 纳入 T026 与 T046 的覆盖要求；同时把合并 064 后的实测值（镜像 62 DIFF / 本对 0；既有契约 23 passed；watcher 自测 28 passed / 0 failed）写回 tasks/feature-ref/research 的实测前提。以上均为可复算事实的纠正，不改变需求范围或设计。

**不重审理由**：本轮是 plan 约束激活后的下游规格修复，但 CLI-profile 增量的迁出是 064 已记录的跨特性裁决，不是对已批准需求范围的改写；四项吞吐优化的 FR/SC 语义、架构、数据模型与任务分解均未改变。该情形属于 FR-022(a) 所称“修复既有缺陷所必需”，且 064 的 owner 地位是唯一一致读法；若驱动认为存在其它读法，按 FR-022(b) 四要素上送。

## Plan Repair Record（2026-10-20，tasks-repair-3：analyze-rerun-2 聚焦修正）

**触发**：`/speckit.analyze` 复核报告（0 CRITICAL / 1 HIGH U-01R / 6 MEDIUM / 3 LOW）中的 plan-owned 项：N-07（061 `CAPABILITY_MATRIX` 派发资格指针）、L-01（49→50）、L-02（064 裁决路径前缀）；tasks-owned 项（U-01R、N-06、N-01R/N-02R/N-03R、N-04、F-01 路由）由 tasks-repair-3 在 `tasks.md` 内承接，见 tasks.md § D-T10。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — Technical Context 增加 Dispatch Eligibility 行，点名 Feature 061 的 CAPABILITY_MATRIX 为派发资格唯一 owner（supported CLI = matrix eligible；档案存在 ≠ 可派发）；Constitution IV 证据 49→50；064 裁决路径补全为 .specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md；新增第 4 轮记录；分类=minor（指针/计数/路径纠正，不改设计或范围），理由=analyze-rerun-2 的 N-07/L-01/L-02 纠正项。`
- `PLAN-EDIT: contracts/progress-decoupling.md — PD-01 增加 Feature 061 CAPABILITY_MATRIX 派发资格 owner 指针（064 CLP-15 同口径）；分类=minor（指针澄清），理由=N-07；不改变 PD-01 的 stream-json 行为规则。`
- `PLAN-EDIT: tasks.md — 由 tasks 阶段承接 U-01R（T000 夹具作者、T001/T051 同一可执行夹具、initial_retries=0、exit_code={watcher,runner}、删除判定表转录/trace-only）、N-06（7 组/24 应用）、N-01R/N-02R/N-03R/N-04/N-05；分类=substantive（证据程序与覆盖修正），理由=实施 FR-038/FR-012/FR-022 已批准口径，不改变四项优化的范围。`

**纠正与范围说明**：

- N-07：061 的 `CAPABILITY_MATRIX`（`scripts/python/execution-config.py`）是派发资格唯一 owner；064 CLP-15 同口径。063 只决定 stream-json 输出默认与 nohup 形态。
- L-01：plan 自身后文与当前契约计数均为 50（含 PC-11），Constitution IV 证据同步为 50。
- L-02：plan 与 `contracts/progress-decoupling.md` 的点名统一使用 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`。`requirements.md` 的同类指针不在本轮允许的修改面（tasks.md + plan-owned 小修），保留给 requirements-owned 阶段；这是范围披露，不是判据降低。

**不重审理由**：本轮只纠正指针、计数与路径，并把 tasks 层证据程序对齐已冻结的 requirements/plan/data-model/contracts 口径；不改变已批准需求范围、FR/SC 语义、架构、数据模型、契约语义或任务分解，属于 FR-022(a) 所称“修复既有缺陷所必需”。

## Plan Repair Record（2026-10-20，implement 起点：analyze-rerun-3 记录项落地）

**触发**：analyze-rerun-3 门 READY（0 CRITICAL / 0 HIGH）的记录项在 implement 前落实：N-08（SC-010 冻结提交不适用）、L-02（064 裁决完整路径）、L-03（夹具「单测」措辞）、L-04（收窄「或 trace」为夹具唯一、trace 补充）。N-03R 与 F-01 由 tasks-owned 行（T022/T050）承接。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — Summary / Constitution Check / Verification & Mutation Plan / Complexity Tracking 的 SC-010 基线提交表述由 ba2a18db 修正为「冻结读数不适用，实际基线 a1aac7e5（首个行为面提交 9e69f3de 的父提交）」；Phase 1 结构的夹具单测注释改写为 --self-test；新增第 5 轮记录；分类=minor（日期化基线纠正与措辞收窄，不改设计、范围或判定语义），理由=N-08/L-03/L-04。`
- `PLAN-EDIT: data-model.md — § Stall Behavior Baseline 的录制对象改为实际基线 a1aac7e5 并保留冻结读数差异说明；分类=minor（证据基线纠正），理由=N-08。`
- `PLAN-EDIT: contracts/delivery-and-invariants.md — DI-03 的 base_commit 改为实际基线 a1aac7e5，保留冻结读数与父提交规则；分类=minor（证据基线纠正），理由=N-08。`
- `PLAN-EDIT: quickstart.md — SC-010 准备步骤的 worktree 提交改为 a1aac7e5 并说明 N-08 复核结论；分类=minor（操作步骤纠正），理由=N-08。`
- `PLAN-EDIT: feature-ref.md — FR-038/SC-010 映射与基线记录的冻结提交改为实际基线 a1aac7e5；分类=minor（证据基线纠正），理由=N-08。`
- `requirements.md` 的 FR-038 / SC-010 / 术语 / SC-010 Source / 两条澄清记录由 requirements-owned 修正在 implement 起点落地（完整路径 L-02、trace 收窄 L-04、基线提交 N-08），并按 PC-11 在状态脊记录 re-baseline 事件；不属于本 PLAN-EDIT 面。
- `tasks.md` 的 T001 兜底检测显式化为「先跑 git log 复核、确认 9e69f3de、取 a1aac7e5」，T022 增补「每适用阶段恰一条 stage-status」；tasks.md 不是 plan-owned 制品。

**不重审理由**：本轮只纠正已披露基线的提交取值与措辞收窄，按 FR-038/SC-010 的既有兜底条款执行，不改变四项优化的范围、FR/SC 语义、架构、数据模型语义或任务分解，属于 FR-022(a) 所称「修复既有缺陷所必需」。

## Plan Repair Record（2026-10-20，第 6 轮：post-review repair，P0/P1 + 效率案例）

**触发**：review.md 的 P0/F1（test-budget 完整性分母静默缩小）、P1/F2（driver closure 前误报 pass）、P1/F3+F7（`next_stage_dispatched` 同义反复、`evidence_ptr` 指向已删除临时目录）、P1/F6（watcher grace 自检抖动）与 `notes/efficiency-case-study-2026-10-20.md` 的案例输入要求。修复保持判据只增不减：缺失/空证据计入分母并报 `unknown`（exit 1）；基线增加成功派发正控；watcher 增加零窗口回归钉。

**PLAN-EDIT 声明**：

- `PLAN-EDIT: plan.md — 新增第 6 轮记录与 scope 决策；分类=minor（记录修复范围与判据变化），理由=review F1/F2/F3/F6/F7 与效率案例输入。`
- `PLAN-EDIT: data-model.md — § Stall Behavior Baseline 录制对象增加成功完成正控，SB-2 明确双向观测，SB-3 明确按场景相对路径比较，新增 SB-6 证据持久化；分类=minor（证据程序澄清，不改变 E1–E8 实体、字段或 SC 判据），理由=review F3/F7。`
- `PLAN-EDIT: contracts/delivery-and-invariants.md — DI-03 明确成功正控与 durability 要求；分类=minor（证据程序澄清，不降低任何 MUST），理由=review F3/F7。`
- `audit-test-budget.py` 与 `tests/unit/test_audit_test_budget.py`：P0 修复，属实现面而非 plan-owned 制品；分母改为全部适用阶段，缺失/空证据计 `unknown` 并判失败。
- `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`、`tests/contract/test_sdd_loop_driver_efficiency.py`、`skills/external/sdd-loop-driver/scripts/watch-target.sh` 与 `references/efficiency-model.md`：实现/技能面修复，不是 plan-owned 制品。

**Scope 决策（templates/commands/implement.md）**：本轮**不**修改 `templates/commands/implement.md`。driver-closure `pending` 规则作为 dated closing rule 落在本特性的 `review.md` 与 `verification.md`，并明确「closure E2 行 + `comm -13` 证据落地前不得报 pass」。理由：修改框架命令提示词会改变所有下游项目的 implement 行为，属于跨项目能力变更，应在独立特性中按完整 SDD 链设计并测试；本次 post-review repair 只关闭 063 的 P0/P1，不扩大范围。

**不重审理由**：本轮只修复已批准判据的正确实现（分母、双向观测、持久证据、确定性自检）并记录案例输入；不改变 FR/SC 语义、四项优化范围、架构或任务分解。判据只增强不削弱：P0 使审计可失败，SC-010 基线由三场景扩为三场景+正控，watcher 自检新增回归钉。
