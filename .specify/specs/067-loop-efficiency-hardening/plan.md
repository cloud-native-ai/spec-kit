# Implementation Plan: sdd-loop-driver 执行效率加固 —— 框架测试套件瘦身（Loop Efficiency Hardening）

**Branch**: `067-loop-efficiency-hardening` | **Date**: 2026-10-22 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `067-loop-efficiency-hardening` → Feature 058 无人值守 SDD 循环驱动机制（演化规格，状态保持 Implemented）
**Input**: Specification from `.specify/specs/067-loop-efficiency-hardening/requirements.md`（已 clarify，21 FR 定义 / 10 SC 定义）
**Plan stage scope (P3-plan-test-slimming)**: 本 plan 覆盖全部 21 条 FR 的设计归属；设计重心是 2026-10-22 范围扩展的 User Story 5（FR-011…FR-021、SC-006…SC-010，测试套件瘦身）。US1–US4 的派发机制面由 063 已落地的效率模型承载，本 plan 只做归属确认与引用性增量（见 Requirements Coverage）。

## Summary

框架自身完整测试在基线开发主机上实测 750 秒（pytest 748.56 秒），远超用户设定的 ≤600 秒目标；成本高度集中：最慢 50 条占 298.2 秒（其中 admission_check 18 条），根因是**宿主级 git 安全钩子对每个 fixture 提交征收约 0.9 秒**（本阶段实测，见 research B-2）、逐用例子进程冷启动与逐用例工作区复制；同时 83 条基线失败中 50 条为镜像漂移类，可由既有同步引擎确定性修复。本 plan 的瘦身设计 = 四个正交手段 + 一个有界债务处置：

1. **W1 基线失败集有界 triage**：镜像类（50 条）走 sync 引擎修复或显式登记既有负债；其余 33 条逐名 triage（陈旧钉住→按 owner 事实更新并记录理由 / 真回归→修机制 / 既有负债→dated 登记）；绝不以删除测试消灭失败（FB-05…FB-07）。
2. **W2 慢测试工作流**：fixture git 钩子中和（单点 autouse fixture，tests 侧 env，RC-07）+ 引擎进程内直调（保留 CLI 钉住用例）+ 模块级 fixture 复用与写时克隆 + 矩阵用例表驱动化；逐家族给出可验证假设、验证方法、预期节省与风险（§W2 表）。
3. **W3 镜像一致性合并**：以同步引擎的 pair 清单为表源建一个共享参数化套件（断言强度不降、node id 保留 pair 可定位性），逐文件折叠纯 byte-identity 用例并全部入留证台账（FR-014/015，LED-04/07）。
4. **W4 运行器与测量**：测量口径按 clarify 定案协议原样钉住（MP-02…MP-07）；**xdist 裁决 = 准入但本 spec 不采用**（R-7：串行恢复算术足以覆盖预算且并行安全性无法在本阶段验证；遗留 contingency 走 Edge Case 升级，不静默改命令）。
5. **W5 验收与演练**：SC-006…SC-010 逐项验证步骤、执行时点与证据落点（§W5）。

达标判据不变：瘦身后冷缓存完整运行墙钟 ≤600 秒（开发主机），三层全执行、覆盖不缩水（无台账不消失）、漂移防护不削弱（相对基线失败集不新增名称级失败 + 钉住 100% 保留）。禁止事项原样生效：不重定义完整运行、不默认过滤、不删整层、不伪绿、不为提速扩运行时依赖。

## Baseline Facts & Target（设计输入，均为 dated record）

| 事实 | 值 | 来源 |
|---|---|---|
| 完整运行基线 | 750 s 墙钟（pytest 748.56 s），exit 1 | test-evidence/baseline-full-2026-10-22.md |
| 计数 | 83 failed / 4467 passed / 1 skipped；collect 4553（contract 3428 / unit 734 / integration 391） | 同上 |
| 最慢 50 条 | 298.2 s（≈40% 墙钟）：admission_check 18、worktree queue 6、proactive trigger 4、trigger telemetry 3、workspace isolation 3、单条 self-test 28.21 s | test-evidence/baseline-durations-2026-10-22.txt |
| 失败集结构 | 83 条：50 条含 mirror/parity/sync/drift/distribution 标记；33 条为 gate-total 钉住、exec-quant、3 条 loop-state | test-evidence/baseline-failures-2026-10-22.txt |
| 宿主单位成本 | 空 spawn ≈10 ms；git CLI ≈29 ms；解释器 ≈55 ms；**fixture 提交 ≈0.9 s（全局 core.hooksPath 安全扫描钩子）**；admission_check 探针 call 相 2.93–9.62 s 而 CPU 仅 ≈2.6 s/全程 | test-evidence/plan-probes-2026-10-22.md（P-2…P-4） |
| 套件形态 | 298 个测试文件；110 文件含 subprocess/CliRunner、12 含 copytree（可复算口径） | notes/test-slimming-scope-2026-10-22.md |
| 镜像测试面 | ~40 个 contract 文件中 44 个纯 byte-identity/parity 用例；pair 唯一 owner = 同步引擎的 pair 清单 | plan-probes P-5；scripts/python/sync-mirrors.py |
| 目标 | 冷缓存完整运行 ≤600 s；覆盖不缩水（SC-007）；漂移防护不削弱（SC-008）；失败可定位（SC-009）；依赖零扩大（SC-010） | requirements SC-006…SC-010 |

串行恢复算术（设计依据，非达标主张）：750 − 慢家族钩子/冷启动恢复约 200–250 s − 收集与文件合并恢复约 30 s ≈ 470–520 s，落在预算内但留有不确定带；contingency 见 RC-04（Edge Case 升级路径，非静默）。

## Technical Context

**Language/Version**: 测试与夹具 = pytest（仓库既有 contract/unit/integration 三层；运行器解析 Python 3.14.6 + pytest 9.1.1）；测量包装 = POSIX sh；台账/审计 = Markdown + 确定性 inline 过程（comm/join），零新脚本交付
**Primary Dependencies**: 既有 `scripts/bash/run-tests.sh`（名称级失败清单、退出码语义不动）；既有 `scripts/python/sync-mirrors.py`（镜像对唯一 owner，修复机制复用——Tool Reuse）；既有 git/bash。**本 spec 不新增运行时依赖**；xdist 准入但不采用（R-7），故开发依赖组本 spec 预期零新增
**Storage**: 文件即存储——本 spec 目录 `test-evidence/` 的 dated 记录（FullRunMeasurement 一文一件、失败 triage 表、注入/定位演练记录、留证台账）；无数据库、无新服务
**Testing**: 本 spec 的交付物本身就是测试组织与测量证据。宪法 IV 的落法 = 每个瘦身动作配注入/重跑演练（SC-008/SC-009 drill）与名称级差集作为 red→green 证据；契约条款（MP/LED/RC/FB）由收口审计与既有契约测试承载
**Target Platform**: 达标口径 = 2026-10-22 基线开发主机（macOS arm64，Darwin 25.6.0，Python 3.14.6 + pytest 9.1.1）；其他主机仅参考（MP-07）
**Project Type**: 框架源（两顶帽子：改动落 tests/ 与本 spec 目录；运行器如需改动属框架源；不触碰 src/specify_cli 运行时行为）
**Performance Goals**: 冷缓存完整运行墙钟 ≤600 s（基线 750 s）；最慢 50 条家族合计从 298.2 s 降至 ≈60–100 s（设计预期，非承诺）；单测试可定位性 100% 保持
**Constraints**: FR-011 完整运行构成不变；FR-013 运行器契约不变；FR-015 无台账不消失；FR-018 钉住强度不降；FR-019/SC-010 依赖边界；FR-021 交付面 = tests/、运行器（如需）、pyproject 开发依赖组、本 spec 留证——MUST NOT 修改 src/specify_cli 运行时行为迁就速度，驱动面（FR-010 owner）只做引用性更新
**Scale/Scope**: 预计触碰 tests/ 下 8–15 个文件（5 个慢家族 + 镜像用例折叠 ~40 文件的函数级删除 + conftest 一处）+ 本 spec 目录设计/证据产物；不新增顶层目录、不新增技能/命令/模板

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md` v1.13.0，共 16 项）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个 W 工作流映射到 FR-011…FR-021/SC-006…SC-010；FR-001…FR-010 归属确认表见 Requirements Coverage；测量/台账判据全部追溯到 clarify 定案协议 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 058 演化规格；状态保持 Implemented、不新建 Feature、不改注册表计数（requirements Related Feature 已裁决） |
| III | Intent-Driven Development | ✅ Pass | 用户目标（一次完整运行 ≤10 分钟）先于手段；四个手段的取舍与被拒替代方案在 research R-1…R-10 留痕 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | 本 spec 交付物 = 测试重组与测量证据；每项重组以注入/重跑演练与名称级差集作 red→green 证据（FB-08/09、quickstart S6），契约条款由收口审计承载；详见 Complexity Tracking |
| V | AI Agent Integration Standards | ✅ Pass | 不新增/变更 agent provider；驱动面只做引用性更新（FR-021/RC-06） |
| VI | Continuous Quality & Observability | ✅ Pass | 全部测量/演练/triage 落 dated 证据；不可得指标如实记 not_evaluated；根因修复（钩子税、冷启动）而非只压数字 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 完整链推进中；不越权推进状态；tasks 阶段未开始，切分建议见 §Implementation Slicing |
| VIII | Code as the Single Source of Truth | ✅ Pass | 镜像对清单引用同步引擎（代码 owner）而非复述；慢因假设以本阶段探针实测校准（plan-probes），不凭文档印象 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新脚本/新系统：台账审计用 inline 确定性过程（LED-05）；xdist 不采用；watch-target 自测加速记为未来候选不实现（R-10） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 全部产物落在 spec 目录既有命名面（plan/research/data-model/quickstart/contracts/test-evidence/notes） |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本 spec 用自身 SDD 链优化自身测试面（两顶帽子：改 tests/ 属框架源帽）；镜像修复走机制侧 sync 引擎而非手补（Fix the mechanism） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 镜像修复复用 sync-mirrors.py；镜像套件表源取自引擎 pair 清单；进程内引擎调用沿用套件内既有 importlib 模式；无 Tool 记录覆盖测量包装/夹具场景，按预期编写 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Change Validation（两槽位成本下降、名称级防护保持）与 Controlled Execution（测量可重复、证据 dated）；configured ≠ used：达标只认 MP-08 证据 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 协议细节 owner = clarify 协议 dated record + contracts（本 spec）；pair 清单 owner = sync 引擎；基线数字 owner = baseline dated record；plan 不复述只引用 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | quickstart 面向未参与者：每个场景带前提、命令与证据落点；术语（冷缓存、两槽位、名称级差集）首次出现即给上下文 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 宿主钩子税异常在 plan 阶段即取证并上升为设计输入（未静默绕过）；预算不达标的处置 = 显式 Edge Case 升级（RC-04），禁止静默改口径 |

**Gates Status**: ⚠ 一项 Partial（IV，已在 Complexity Tracking 辩护）；无 Fail。

**Re-check after Phase 1**: 2026-10-22——Phase 1 产物（research/data-model/contracts×4/quickstart）落盘后复核：IV 维持 Partial（理由同 Complexity Tracking，属本 spec 交付物性质所致而非缺口），其余 15 项 Pass；未发现新增违规。同作者复核义务：本 plan 由驱动者派发的 fresh-context 执行者撰写，analyze 阶段的独立校验（mandatory gate）按流程另行派发，本表不自我豁免。

## Design by Workstream

### W1 · 基线失败集有界 triage（FR-018 / SC-008；契约 FB-01…FB-07）

- **输入**：83 条基线失败名（E3 权威清单）。
- **Class 1（50 条 mirror/parity/sync/drift/distribution 标记）**：先 `sync-mirrors.py --check` 盘点漂移对；可同步对用 `--write --only <pair>` 修复（机制侧修复，测试零改动）；canonical 源正被其他在途特性改动的对**不盲同步**，登记既有负债（FB-06 dated 记录，注明非本范围引入）。
- **Class 2（33 条：gate-total 钉住、exec-quant、3 条 loop-state）**：逐名 triage 并落 E5 表——陈旧钉住（owner 事实已合法移动）→ 按当前 owner 值更新钉住并记录理由（FR-018 允许）；真回归 → 修机制；无法在收口前归因/修复 → 显式既有负债登记。三选一，无第四种。
- **红线**：不删除失败测试（FB-07）；债务记录永不声称 green；本范围不得成为任何钉住测试失败的原因。
- **时点**：triage 表在 implement 起始部分建立（对照 owner 事实逐名裁决），执行分散在各 part，收口前全部闭环。

### W2 · 慢测试工作流（假设 → 验证 → 手段 → 预期节省/风险）

基线最慢家族逐条设计（时长来自 baseline-durations dated record；假设证据来自 plan-probes P-2…P-5）：

| 家族（基线实测） | 为什么慢：假设 + 证据 | 验证方法 | 手段 | 预期节省 | 风险 |
|---|---|---|---|---|---|
| test_admission_check.py 18 条 ≈82.5 s | 每用例建 fixture 仓（2–3 次 git commit）× 宿主钩子税 ≈0.9 s/提交（P-4）+ 引擎/解释器子进程 ≈0.3–0.5 s（P-3）；call 相 2.93–9.62 s 而 CPU 仅 ≈2.6 s/全程（P-2）＝等待非计算 | 实施期对 ≤3 个 node id 复测：套上 RC-07 env 后 call 相对比；再把脚本改进程内直调复测 | RC-07 钩子中和（全局受益）+ R-2 进程内直调（importlib 载入 admission-check 模块调入口，保留 1–2 条真 CLI 子进程钉住用例钉 exit code/argv 面）+ 同形 fixture 共享（R-3） | 82.5 → 15–25 s | env 覆盖影响依赖全局 git config 的用例 → 收窄作用域；进程内全局态 → 用例间显式重置 |
| test_worktree_integration_queue.py 6 条 ≈53.8 s（含单条 27.13 s 的 merge+replay） | integration executor 在 fixture 仓内多次 worktree add/commit/replay，每次提交付钩子税；replay 重复提交序列；fsck 重复跑 | 同上复测法（≤3 node id）+ 读 executor 提交次数静态核对 | RC-07（引擎子进程继承 env，fixture 仓全部免钩子）+ 模块级 base 仓 + 每用例廉价克隆 + fsck 收敛到终局一次（断言不变） | 53.8 → 12–18 s | replay-identical 断言必须逐字节保持；worktree 语义不得共享泄漏 |
| test_trigger_telemetry.py 3 条 ≈19.9 s（sixty-turns 用例循环 60+ 次引擎调用） | 每个引擎动作一次子进程冷启动（P-3 解释器 ≈55 ms × 60+）+ git init 每用例 | 对 sixty-turns 单 node 计时对照：进程内动作化前后 | R-2：importlib 载入 trigger 引擎直调 action（套件内既有模式），保留 1 条 CLI 冒烟；动作间显式状态重置 | 19.9 → 4–6 s | 引擎模块全局态泄漏 → 重置 helper；payload/退出码语义必须与子进程一致（保留冒烟钉住） |
| test_proactive_trigger_section.py 4 条 ≈17.6 s + test_instructions_size_budget.py idempotent 6.98 s | 每用例完整安装 template 树（copytree）+ 生成器 bash 跑 1–2 次（c9 幂等断言跑两次） | 对 c9 单 node 计时：快照+克隆 fixture 前后 | R-3：session 级模板只读快照 + 每用例 APFS clonefile 克隆（带普通 copy 回退）；生成器保持子进程（契约面不进程内化） | ≈24.6 → 10–12 s | 跨用例 fixture 污染（c9 断言裸起点）→ 每用例独立克隆保语义 |
| test_workspace_isolation_contract.py 3 条 ≈13.5 s | git fixture 提交钩子税（同第一行机制） | 同上复测法 | RC-07 即覆盖；必要时模块级仓 | 13.5 → 5–6 s | 低 |
| watch-target self-test 1 条 28.21 s | 脚本内实时 sleep/宽限窗口（自测用例 6 的 sleep 30 keeper 等，P-5）；脚本不在 FR-021 交付面 | 已静态取证（P-5） | 本 spec 不修（交付面外）；28 s 作为固定成本计入预算算术；脚本侧加速旋钮记为未来 spec 候选（R-10） | 0（固定成本） | 预算挤占已计入算术 |
| 全套件宽尾部（30+ 文件 52 处直接 commit 调用点 + 引擎脚本提交） | 每处提交付 ≈0.9 s 钩子税（P-4 全局 core.hooksPath 实测） | RC-07 落地后 implement 起点槽位全量运行对比基线 | RC-07 单点 autouse fixture（GIT_CONFIG_GLOBAL/SYSTEM 指向空临时文件，仅测试进程树） | 全局回收约 40–70 s | 个别用例依赖全局 git config → 收窄；baseline 槽位运行即验证点 |
| 收集/用例开销（298 文件导入 + 4553 用例） | 收集期导入所有测试模块；纯 byte-identity 折叠减少函数数但不减文件数，收益有限 | 收集期 `--collect-only` 计时（实施期一次性） | 仅作为 W3 的次要收益记录，不作独立杠杆 | ≈5–15 s | 低 |

**不做的事**（显式排除）：不改测试执行顺序/随机化；不引入常驻预览服务；不把整层移出完整运行；不为速度弱化断言（断言对象与隔离语义不变，FR-016）。

### W3 · 镜像一致性测试合并（FR-014/FR-015/FR-018；契约 LED-04/LED-07）

- **表源唯一 owner**：共享参数化套件的参数表从 `scripts/python/sync-mirrors.py` 的 pair 清单与文件枚举 helper 派生（importlib 载入，套件内既有模式），不复制 pair 清单（One Source of Truth / Tool Reuse）。断言语义 = 引擎 `--check` 的同一比对语义：对每对源/镜像文件断言字节一致，drift 即失败。
- **钉住强度（FR-018）**：套件覆盖引擎清单内的**全部**文件对——相对现状散落的 44 个纯 byte-identity 函数只可能更严（引擎新增对自动入列）；例外对（引擎标记非 strict 的语义）保持引擎语义，不额外放宽。
- **node id 可定位性（FR-020）**：parametrize id 携带源路径对（形如 源路径→镜像路径），失败输出可直接定位到对，按 node id 定向重跑可用；S6 演练（FB-09）验证。
- **折叠纪律**：仅折叠「纯字节比对」函数（P-5 盘点 44 个为候选，逐函数核对后定案）；带额外断言（节集合、计数、wiring、归一化等价）的测试保留其额外断言所在用例，仅其冗余字节比对部分由套件承载。每个被移除函数一行台账（case-merge，retained_equivalent_id = 套件对应参数 id，等价依据 = 字节断言由引擎驱动套件等价承载）。
- **与基线失败集的关系**：镜像漂移是真实存在的（50 条基线失败为证），套件对漂移对**继续失败**——这正是 SC-008 相对语义所需；W1 修复同步后转绿。顺序：W3 套件落地 → W1 同步修复 → post 运行核对该对转绿。

### W4 · 运行器与测量（FR-011/012/013/017/019/021；契约 MP/RC）

- **固定测量命令**：MP-02 逐字钉住（= clarify 协议 §1 原文），pre/post 同一组合；warm-up 至多一次且先于清缓存；墙钟 = 包装 epoch 差（MP-04）；证据 = E1 字段全集（MP-06）；达标主张只认 MP-08。
- **基线 node id 清单**：E4 定义；implement 起始（首个合并任务前、基线全量完成后）生成 baseline 清单；收口同法再生 post 清单；LED-05 join 审计。**本 plan 阶段不生成**（本阶段禁全量运行；实现期义务，非缺口——与 clarify 裁决一致）。
- **运行器**：入口/参数透传/解释器解析/`--names-out`/退出码语义零改动（RC-01/02）；本 spec 预期**不需要**改运行器；若实施中发现需要（例如诊断性标记注册），改动保持构成中立（RC-05）并同步镜像（见 Mirror Obligations）。
- **xdist 裁决：准入、本 spec 不采用**（research R-7 四条理由：串行恢复算术足够、并行安全性无法在本阶段验证、FR-017 默认分支即等价手段、采用需额外汇串行可用性证明）。串行默认路径保持唯一测量口径；预算不达标的 contingency = RC-04（Edge Case 显式升级，绝不静默改命令/改口径）。

### W5 · 验收与演练（SC-006…SC-010 的验证步骤、执行者、时点、证据落点）

| SC | 验证步骤 | 谁执行 / 何时 | 证据落点 |
|---|---|---|---|
| SC-006 墙钟 ≤600 s | MP-02 冷缓存完整运行；E1 全字段记录；与基线 750 s 对照 | implement 执行者在 closure 槽位（review 后、合并前）；驱动者 U4 独立复核记录字段完整性 | test-evidence/full-run-〈date〉-closure.md |
| SC-007 构成不缩水 | E4 双清单 + LED-05 join：基线清单每条 id 保留或台账指向等价覆盖；三层全执行（E1 layer_counts 交叉核对） | implement 执行者在 closure 槽位随 SC-006 同轮产出；审计输出落档 | test-evidence/coverage-audit-〈date〉.md |
| SC-008 漂移防护 | ①钉住类名册（implement 起始按 FR-018 类目生成）⊆ post 清单 100%；②FB-04 名称级差集为空；③基线内钉住失败全部闭环（修复或 FB-06 登记） | 名册与 triage 在 implement 起始；差集在 closure 槽位 | test-evidence/failure-triage-*.md、pinned-roster-*.txt、name-diff-〈date〉.txt |
| SC-008/SC-009 注入与定位演练 | FB-08：向一个合并后表驱动用例注入单行失败 → FB-04 差集 100% 命中；FB-09：失败输出唯一 node id + 按 id 定向重跑复现；随即还原 | implement 执行者在 W3 落地后、closure 前 | test-evidence/injection-drill-〈date〉.md |
| SC-010 依赖边界 | quickstart S7：pyproject 运行时依赖 diff 为空；测试侧新增依赖全在开发组；测试代码网络调用检索为 0（新增面） | implement 执行者在 closure 槽位 | test-evidence/dependency-boundary-〈date〉.md |

## Requirements Coverage（FR/SC → 设计归属；brief 验收项：每条有 owner 或显式理由）

- **FR-001…FR-010（US1–US4 派发机制面）**：机制 owner = `skills/external/sdd-loop-driver/` 的 SKILL.md / dispatch-recipes / `agents/sdd-executor.agent.md` + 063 效率模型已落地承载（run-turn-budget 120 固化提交 `696d5f4b`、part brief/预算纪律已在 065a 运行）。067 的设计归属 = **引用性更新**（FR-021：驱动面只做引用性更新）+ 本特性自身 implement 按该纪律执行（part brief、dispatch log、微缺口并流）。SC-001…SC-005 的证据 = 067 自身 dispatch log 与 verification（收口时如实记录，不可得记 not_evaluated）。
- **FR-011** 完整运行构成 → RC-05 / MP-05；**FR-012** 墙钟与测量 → MP-01…MP-08 + E1；**FR-013** 运行器契约 → RC-01/RC-02；**FR-014** 表驱动合并 → W2/W3 手段 + LED-04；**FR-015** 台账 → E2 + LED-01…LED-06；**FR-016** fixture 复用 → R-3（隔离语义不变、显式隔离修复）；**FR-017** 并行或等价加速 → R-7（等价加速分支：W2 手段合计）+ RC-03/04；**FR-018** 漂移防护 → FB-03 + LED-07 + W3 强度论证；**FR-019** 依赖边界 → RC-08；**FR-020** 失败定位 → W3 node id 设计 + FB-09 演练；**FR-021** 交付面 → RC-06。
- **SC-001…SC-005** → 067 自身执行的 dispatch log 证据（归属确认如上）；**SC-006…SC-010** → W5 表逐项。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/067-loop-efficiency-hardening/
├── requirements.md      # 已 clarify（21 FR / 10 SC）；本阶段不改（无直接矛盾发现）
├── plan.md              # 本文件
├── research.md          # Phase 0：B-1…B-5 证据 + R-1…R-10 取舍
├── data-model.md        # Phase 1：E1…E6 实体与校验规则
├── quickstart.md        # Phase 1：S1…S7 运行/测量/演练手册
├── contracts/           # Phase 1：4 文件 35 条款
│   ├── measurement.md            # MP-01…MP-10
│   ├── consolidation-ledger.md   # LED-01…LED-08
│   ├── runner-contract.md        # RC-01…RC-08
│   └── failure-baseline.md       # FB-01…FB-09
├── test-evidence/       # 基线 dated 记录 + 本阶段 plan-probes + 实施期证据（后置）
└── notes/               # dated 记录（state-spine 由驱动者维护，不随本 part 提交）
```

### Source Code (repository root)

```text
tests/                            # 瘦身主交付面（用例、夹具、conftest；不在镜像对内）
tests/fixtures/sdd_loop_efficiency/   # 既有夹具目录，按需扩展
scripts/bash/run-tests.sh         # 仅在确需时改动（本 plan 预期不动）；属镜像对，见下表
pyproject.toml                    # 仅开发侧依赖组（本 plan 预期零新增）
skills/external/sdd-loop-driver/  # FR-010 owner 面：仅引用性更新（FR-021）
```

**Structure Decision**: 全部落既有布局，零新顶层目录；改动重心是 tests/ 内的夹具与用例组织 + 本 spec 目录的设计/证据产物。

### Mirror Obligations *(mandatory)*

同步引擎：`scripts/python/sync-mirrors.py`（pair 清单 owner；`scripts` 对为 strict extras）。

| Source file (edited) | Mirror / generated copies | Verify |
|----------------------|---------------------------|--------|
| `scripts/bash/run-tests.sh`（若实施改动） | `.specify/scripts/bash/run-tests.sh`（strict 对） | `sync-mirrors.py --write --only scripts/bash/run-tests.sh` 后 `--check --only scripts` 本对零 drift |
| `skills/external/sdd-loop-driver/` 引用性更新（若有） | `.specify/skills/sdd-loop-driver/` 同名文件 | 同引擎 `--write --only` + `--check`，且相对实施前读数零 NEW drift |
| `tests/**`、`pyproject.toml`（开发组） | 无镜像（不在 MIRROR_PAIRS） | pytest 直跑 + SC-010 diff 判据 |
| 本 spec 目录产物 | 无镜像（规格工件） | pre-analyze-check / 评审 |

基线漂移披露：镜像基线当前即有大量漂移（50 条 mirror 标记基线失败为证）。本 spec 的镜像判据 = 相对基线零 NEW drift + 本 spec 触碰对本对零 drift；既有漂移的修复属 W1 triage 范围（可同步对修复、在途对登记负债），不采用绝对全绿判据（无法通过，且会误导范围）。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First 判 ⚠ Partial | 本 spec 的交付物是测试面重组与测量证据，不引入新产品行为——「先写测试再实现」的对象不存在；red→green 证据由等价演练承载：每个合并/夹具动作以注入失败（FB-08）与定位重跑（FB-09）验证防护有效，每个测量主张以 E1 dated 记录承载，基线失败处置以名称级差集承载。 | 把测试重组本身再测试化（为改测试先写测试）是无限回归；以演练与差集作证据满足 IV 的意图（防回归、可验证），063 先例同判。 |

## Phase 0: Research Review

独立 `research.md` 已产出（B-1…B-5 证据、R-1…R-10 取舍，均带来源）。关键结论：宿主 git 钩子税（≈0.9 s/fixture 提交）是跨家族首要根因且可用单点 tests 侧 env 覆盖中和（R-1）；引擎进程内直调是次级杠杆且套件内已有成熟模式（R-2）；镜像套件表源取引擎（R-5）使钉住强度只增不减；xdist 准入但不采用，串行算术 470–520 s 覆盖预算、contingency 走显式升级（R-7）。本阶段探针证据 = `test-evidence/plan-probes-2026-10-22.md`（2 node id 定时探针 + 微基准，无全量运行）。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 6 实体（E1 FullRunMeasurement / E2 ConsolidationLedger row / E3 BaselineFailureSet / E4 BaselineTestIdList / E5 FailureTriageRecord / E6 HookNeutralization 机制记录）+ 9 条 V 校验规则 |
| Contracts | [`contracts/`](contracts/) | 4 文件 35 条款：measurement.md（MP-01…MP-10）、consolidation-ledger.md（LED-01…LED-08）、runner-contract.md（RC-01…RC-08）、failure-baseline.md（FB-01…FB-09） |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 场景（S1 运行 / S2 测量 / S3 名称级对比 / S4 覆盖审计 / S5 镜像修复 / S6 注入与定位演练 / S7 依赖边界） |
| Research | [`research.md`](research.md) | B-1…B-5 + R-1…R-10 |
| Plan-stage probes | [`test-evidence/plan-probes-2026-10-22.md`](test-evidence/plan-probes-2026-10-22.md) | P-1…P-5（2 node id 定时探针 + 微基准 + 静态盘点） |

Phase 0 预期 vs 实际：实体 6（预估 5–6 ✓）；契约 4 文件 / 35 条款（预估 3–4 文件 ✓）；quickstart 7 场景（预估 6–7 ✓）；feature-ref.md 不在本 part 允许修改面，未产出（tasks 阶段如需按其模板补）。无预写计数漂移（本节在产物落盘后按实计数回填）。

## Implementation Slicing（Phase 2 建议；每 part ≤8 任务，按收益/风险优先）

| Part | 内容 | 预估任务数 | 优先理由 |
|---|---|---|---|
| A | RC-07 钩子中和 fixture + admission_check 直调/共享夹具（W2 行 1） | 6 | 收益最大（单家族 ≈60 s+ 全局尾部 40–70 s）、风险最低（env 覆盖 + 既有 importlib 模式） |
| B | worktree queue / workspace isolation / store-state·loop-state·audit-plan-changes 的夹具复用与 fsck 收敛（W2 行 2、5） | 5 | 次大收益；依赖 A 的 fixture 基建 |
| C | trigger telemetry 进程内动作化 + 冒烟钉住（W2 行 3） | 4 | 独立、模式已验证 |
| D | proactive trigger / instructions budget 的快照+克隆夹具（W2 行 4） | 4 | 平台相关回退需小心，放中段 |
| E | W1 Class 1 镜像同步修复 + W3 镜像套件与折叠 + 台账回填 | 7 | 套件先落、同步后转绿的顺序约束；台账随折叠同步写 |
| F | W1 Class 2 逐名 triage 执行（钉住更新/机制修复/负债登记）+ FB-08/09 演练 | 6 | 依赖 owner 事实核对，逐名工作量有界 |
| G | closure 槽位：E4 双清单 + MP-02 冷缓存全量测量 + SC-007 审计 + SC-008 差集 + SC-010 检查 + 证据收口 | 5 | 全部判据的最终验证轮 |

合计预估 ≈37 任务（<40，FR 21 < 30 → 不触发 split-required；tasks 阶段以 decomposition-check --mode tasks 机械复核）。依赖：A→B/C/D/E（基建与顺序约束），E 内部「套件→同步→转绿」为关键路径；F/G 收口。基线 id 清单（E4）在 A 开工前生成；implement 起点槽位全量运行兼作 RC-07 的验证点。

## Assumptions（plan 阶段记录，未越 clarify 裁决）

- 串行恢复算术（470–520 s）是设计依据而非达标主张；达标只认 MP-08 证据。若实施期证据推翻算术，走 RC-04 显式升级。
- 钩子中和只作用于测试进程树（fixture 仓），宿主 git 配置零改动；个别依赖全局 git config 的用例以收窄作用域修复而非放弃中和。
- 镜像套件以引擎 `--check` 语义为准绳；若引擎本身有 bug（漏报漂移），按 Fast Fail 上升，不在本 spec 内改引擎语义。
- 067 自身 implement 产生的 SC-001…SC-005 证据在 067 的 dispatch log 中如实记录；turn/token 不可得记 not_evaluated。
- watch-target 自测 28 s 在本 spec 保持原样（交付面外）；若瘦身后串行仍逼近 600 s，该条与 xdist 一并进入 RC-04 升级面。

