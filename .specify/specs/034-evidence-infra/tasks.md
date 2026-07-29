# Tasks: 公共证据采集基础设施(Better Harness 能力移植)+ improve-* 证据驱动改造

**Requirement ID**: 034
**Requirement Key**: 034-evidence-infra
**Related Feature**: 038 Evidence Infrastructure (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/034-evidence-infra/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/ ×3, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 为 MUST 级;本 spec 为"代码 + 技能文档"混合形态——Python/Node 侧出 pytest contract 与 node --test 回归,技能/共享约定侧出结构性合同测试,不强造 runtime 测试)

**Organization**: Tasks are grouped by user story (US1–US7, priorities P1–P4 from requirements.md).

## Definition of Done (DoD)

- DoD-1: 全部 FR-001~014 对应实现落地,交付边界 = US1–US6 + US7 doctor 探测报告(Clarify Q3)
- DoD-2: pytest contract 新增测试全绿;`tests/js/run.sh` 引擎子集测试通过;全套 pytest 相对基线零新增失败
- DoD-3: 全部镜像义务(plan.md Mirror Obligations 8 行)`diff -rq`/`diff -q` 零差异
- DoD-4: quickstart.md 全部 CLI 示例实测通过(或由合同测试钉住)
- DoD-5: findings.json 抽查:七态封闭、裁决字段零出现、脱敏双闸生效(SC-002/004)
- DoD-6: 对 improve-skills 完成一次"采集 → 分拣 → 优化 → 台账"闭环(SC-006);verification.md 记录 SC-001…008 逐项结论

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1–US7
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` Open / `- [X]` Closed / `- [~]` Deferred(理由记入 verification.md `deferred_tasks=`)

## Path Conventions

单仓布局(plan.md § Source Code):引擎 `scripts/js/better-harness/`(镜像 `.specify/scripts/js/`)、编排器 `.specify/scripts/python/evidence-utils.py`(镜像 `scripts/python/`)、技能 `skills/`(镜像 `.specify/skills/`)、共享约定 `shared/workflow/`(镜像 `.specify/shared/workflow/`)、测试 `tests/js/` + `tests/contract/`。

## 环境前提(生成时已探测)

- Python 3.11 ✅;Node **v25.9.0** ✅ 可执行,但超出上游 engines 声明(`>=22.20.0 <25.0.0`)——处理策略:doctor 的 `satisfies` 如实报 false 并附提示,collect 对"available 但 not satisfies"的 Node 仍尝试运行(engines 是声明非强制);若引擎在 Node 25 下实测报错,按泳道降级处理并在 verification.md 记录,不阻塞纯 Python 泳道交付。
- 上游仓库 `/cws_work/better-harness` 本地可读(commit b2e621d)✅;零网络依赖。
- `scripts/js/` 当前为 root 属主空目录 ⚠ — T001 处理。

---

## Phase 1: Setup

**Purpose**: 目录权限、存储骨架、测试基线

- [X] T001 重建 `scripts/js/` 为当前用户属主(`sudo rm -rf scripts/js && mkdir -p scripts/js` 或等效;若无 sudo 则记录并改用 `.specify/scripts/js/` 为主写入侧再反向镜像),并创建 `.specify/scripts/js/` 目录
- [X] T002 [P] 创建证据存储骨架 `.specify/memory/evidence/.gitkeep`,并确认 `.specify/memory/feedback/` 的 package 逻辑不扫描 evidence 目录(阅读 feedback-utils.py L519-594 确认收集范围仅 feedback 目录,记录结论备 C-F13 测试引用)
- [X] T003 [P] 运行 `pytest -q 2>&1 | tail -5` 记录全套测试基线(通过/失败计数)到 `.specify/specs/034-evidence-infra/baseline.txt`(基线纪律:区分存量失败与本 spec 回归)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 引擎子集复制是 US2(Node 泳道)的物理前提;与 US1 验收解耦——本阶段只做"复制落位",US1 阶段做溯源/测试/验收

**⚠️ CRITICAL**: T004 完成前,US1/US2 不可开始;US3 不受阻(纯 Python)

- [X] T004 按 contracts/engine-subset-boundary.md C-B1 从 `/cws_work/better-harness`(commit b2e621d)复制子集到 `scripts/js/better-harness/`:`session-analysis.mjs` + `session-analysis/`(整目录含 platforms/)+ `core-change-watch/` + `agent-customize/` + `coding-agent-practices/{asset-baseline,asset-integrity,inventory}.mjs` + `agent-lint/` + `dependency-governance/cli.mjs`;新建最小 `package.json`(`{"type":"module","engines":{"node":">=22.20.0 <25.0.0"}}`);逐项核对 C-B2 排除清单零混入(特别是 checkup/、harness-analysis/、better-harness-cli/)
- [X] T005 静态验证子集自洽:grep 断言子集内所有 `import`/`from` 仅指向 `node:` 内置或子集内相对路径(无越界引用、无 npm 包);若发现越界引用按 C-B3 处理(删除引用或记录修改)

**Checkpoint**: 引擎子集在位、依赖闭合 — US1/US2 可开始

---

## Phase 3: User Story 1 - 采集引擎源码落库与托管(D1)(Priority: P1)🎯 MVP-part-A

**Goal**: 子集获得溯源台账、许可、回归测试与镜像,成为 spec-kit 托管资产

**Independent Test**: `bash tests/js/run.sh` 通过;两次手动 CLI 演练产出合法 JSON;UPSTREAM.md 清单与实际目录一致(SC-001)

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T006 [P] [US1] 从上游 `test/` 摘取 C-B5 清单的 12 个 `.test.mjs`(+ 所需 fixtures)到 `tests/js/`,按新布局改写 import 路径;创建 `tests/js/run.sh`(`node --test tests/js/`,Node 缺失时 exit 0 + skip 提示);先运行确认当前可执行(引擎已在位,此测试为"移植回归"性质,预期直接通过——不适用先红后绿)

### Implementation for User Story 1

- [X] T007 [P] [US1] 撰写 `scripts/js/better-harness/UPSTREAM.md`(C-B4 五节:Provenance/Subset Manifest 含 agent-lint 纳入理由/Exclusions/Local Modifications 含 T005-T006 的 import 改写总述行/Resync Policy)并复制上游 `LICENSE` 到同目录
- [X] T008 [US1] 手动 CLI 演练并存档输出:`node scripts/js/better-harness/session-analysis.mjs facts --platform qoder --workspace . --format json` 与 `node scripts/js/better-harness/core-change-watch/project-profile.mjs --json`(会话不存在时验证如实报告不崩溃;输出片段记入后续 verification.md 素材;Node 25 兼容问题在此暴露并记录)
- [X] T009 [US1] 全量镜像 dual-write:`cp -rf` 同步 `scripts/js/better-harness/` → `.specify/scripts/js/better-harness/`
- [X] T010 [US1] 镜像 parity 验证:`diff -rq scripts/js/better-harness .specify/scripts/js/better-harness` 零差异(C-B6)

**Checkpoint**: 引擎子集可独立回归、有溯源、双镜像一致

---

## Phase 4: User Story 2 - 统一证据合同与泳道编排引擎(Priority: P1)🎯 MVP-part-B

**Goal**: evidence-utils.py 的 doctor/collect(session+project+assets)/list/latest 与 findings.json 合同落地

**Independent Test**: collect 三 Node 泳道产出通过合同测试的 findings.json;泳道失败显式降级(SC-002;SC-003 的 Node 缺失面在 US3 后全量演练)

### Tests for User Story 2 (MANDATORY) ⚠️

> 先写先红:T011/T012 在 evidence-utils.py 存在前编写并确认收集失败/断言失败

- [X] T011 [P] [US2] 合同测试 `tests/contract/test_evidence_utils_cli.py`(仿 test_feedback_utils_cli.py):C-E1 action 枚举封闭与 JSON 输出、C-E2 静态断言(源码无 shell=True/网络调用/仅 stdlib import)、C-E3 doctor 键结构与零副作用、C-E5/C-E6 list/latest 行为(含 found:false 与 stale 警告)、C-E11 退出码;pin 纪律:枚举/键名断言精确,版本类断言用下限语义
- [X] T012 [P] [US2] 合同测试 `tests/contract/test_evidence_findings_schema.py`:C-F1 顶层白名单、C-F2 target 正则、C-F3 runId 格式、C-F4 七态枚举封闭、C-F5 泳道五键与状态枚举、C-F6 裁决字段递归黑名单、C-F7 隐私模式断言、C-F8 digest 格式与交叉一致、C-F9 条目字段、C-F10 manifest 必填、C-F12 index 结构(以运行真实 collect 产物 + 构造夹具双路径校验)

### Implementation for User Story 2

- [X] T013 [US2] 实现 `.specify/scripts/python/evidence-utils.py` 骨架与公共层:argparse(--action 五枚举)、resolve_workspace_root(仿 feedback-utils.py L112-134)、JSON 输出约定、存储路径常量(`.specify/memory/evidence/`)、runId 生成、index 读写与损坏重扫(C-F12)、脱敏过滤器(密钥模式 + 绝对路径掩码 + 字段白名单,C-F7)、findingsDigest 计算(C-F8)
- [X] T014 [US2] 实现 doctor(C-E3):Node 探测(版本 + satisfies 按 engines 判定但不阻断)、引擎子集在位性(含读 UPSTREAM.md 的 upstreamCommit)、八工具会话落盘探测(qoder `~/.qoder/projects/`、codex/claude/cursor 按上游 paths 约定,其余四工具按各自默认目录探测、探不到即 not-detected)、五泳道可用性汇总
- [X] T015 [US2] 实现 collect 的三条 Node 泳道(C-E4/C-E8):argv-array subprocess(120s 超时)、envelope → 证据条目映射(session-core-facts/asset-baseline/core-change-watch JSON → E3 结构,evidenceState 赋值规则记入实现注释引用 discipline 文档)、单泳道失败标注后继续、lanes/*.json 落盘、manifest/findings 合成
- [X] T016 [US2] 实现 list + latest(C-E5/C-E6,含 --max-age-days 默认 7 与 stale 警告)
- [X] T017 [US2] 运行 T011/T012 至全绿;并在本仓库实测 `--action doctor` 与 `--action collect --target project --lanes session,project,assets`,确认 quickstart §1-2 命令逐字可执行(执行验证门)
- [X] T018 [US2] 镜像 dual-write + parity:`cp -f` `.specify/scripts/python/evidence-utils.py` → `scripts/python/evidence-utils.py`;`diff -q` 零差异

**Checkpoint**: MVP 达成 — 引擎 + 合同 + 三 Node 泳道可独立演示

---

## Phase 5: User Story 3 - Spec Kit 自有泳道:runs 与 feedback(D3)(Priority: P2)

**Goal**: runs/feedback 纯 Python 泳道 + compare 基础;无 Node 环境保底可用

**Independent Test**: 存量 feedback(动态计数)与 teams 工件进入 findings 且脱敏;无 Node 演练零崩溃(SC-003/004)

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T019 [P] [US3] 集成测试 `tests/integration/test_evidence_python_lanes.py`(先写先红):runs 泳道对 fixture 团队目录(完整版含 STATE.md/run-log.jsonl + 残缺版仅 runs/)的 partial 降级(C-E9)、feedback 泳道 recurrence 聚合与 index 缺失回退(C-E10)、无 Node PATH 下 collect --lanes all 的降级行为(C-E4.3,SC-003)、C-F13 package 排除断言(构造 evidence 目录后跑 feedback package,断言 zip 无 evidence 路径)

### Implementation for User Story 3

- [X] T020 [US3] 实现 runs 泳道(C-E9):扫描 `.specify/teams/*/`,解析 runs/*-report.md 计数、STATE.md `## Post-Run Critique` 追加行、run-log.jsonl 七字段;缺文件按 partial,无 teams 目录 unavailable;Python 侧脱敏后成条目(signals:cycles/escalations/falsePositives 等)
- [X] T021 [US3] 实现 feedback 泳道(C-E10):读 index.json + 条目 `## Optimization Points`,跨条目重复主题聚合为 `signals.recurrence`,evidenceRefs 用条目相对路径;index 缺失回退全量扫描(partial)
- [X] T022 [US3] 实现 compare 基础(C-E7 前半):baseline/current 解析(默认次新/最新)、signalDeltas 计算、newEvidence/resolvedEvidence 对账;intervention verdict 部分留 US6(输出结构预留 intervention 键)
- [X] T023 [US3] 运行 T019 全绿 + 真实数据演练:`--action collect --target project --lanes all` 断言 feedback 泳道 entries 与 `.specify/memory/feedback/index.json` 动态一致、runs 泳道 teamsScanned=2(bh-port-monitor 完整 + draw-plantuml-optimizer partial);quickstart §6 无 Node 命令实测;更新镜像 `scripts/python/evidence-utils.py` 并 `diff -q`

**Checkpoint**: 五泳道齐备,纯 Python 环境保底可用

---

## Phase 6: User Story 4 - collect-evidence 公共技能与标准证据步骤(Priority: P2)

**Goal**: 公共采集入口技能 + evidence-step.md 单一事实源

**Independent Test**: 技能独立编排一次且零优化建议表述;双镜像通过;注册表登记(SC-005)

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T024 [P] [US4] 结构合同测试 `tests/contract/test_evidence_step_conformance.py`(先写先红,本任务先落 US4 断言,US5 断言同文件预写并以 xfail/skip 标注待 US5 实现):collect-evidence SKILL.md 存在性、frontmatter 完整、≤500 行、含范围解析/doctor/collect/边界申明四步与标准 `## Feedback` 节、全文零裁决词(建议/严重度/severity/recommendation 模式)、references 两文件存在且 evidence-discipline.md 含七态定义与四纪律及 C-B7 只进事实句、`shared/workflow/evidence-step.md` 与 `.specify/shared/workflow/evidence-step.md` 一致且含分拣规则与候选冻结与 Unobserved 红线

### Implementation for User Story 4

- [ ] T025 [P] [US4] 撰写 `.specify/shared/workflow/evidence-step.md`(FR-009,与 feedback-step.md 对偶结构:定位与红线 → canonical 步骤块 Step A 采集/复用 → Step B 按 evidenceState 分拣(四路规则)+ 候选冻结 → Step E 干预台账 → embedder 注意事项);源侧镜像 `shared/workflow/evidence-step.md`(确认仓库存在顶层 shared/ 后双写;不存在则以 .specify/ 侧为单源并在 verification.md 记录)
- [ ] T026 [P] [US4] 撰写 `skills/collect-evidence/SKILL.md`(编排四步 + Feedback 节,红线:不解读证据)与 `references/evidence-contract.md`(findings 合同人读版,引用 contracts/findings-contract.md 内容)、`references/evidence-discipline.md`(四纪律 + 七态定义,移植上游 agent-work-loop.md:97-103 语义 + C-B7 边界句)
- [ ] T027 [US4] 双镜像 + 注册:`cp -rf skills/collect-evidence .specify/skills/collect-evidence` 且 `diff -rq` 零差异;`.specify/instructions.md` Skills 注册表追加 collect-evidence 行 + Key Directories 技能计数更新为真实值(现 23 + 1 = 24,列表补 code-review/collect-evidence 等实际在位技能名)
- [ ] T028 [US4] 运行 T024 的 US4 断言全绿;对话式演练技能一次(doctor → collect → 边界申明),输出存档为 SC-005 素材

**Checkpoint**: 证据层公共入口就绪,消费改造可开始

---

## Phase 7: User Story 5 - improve-* 三技能接入证据驱动范式(Priority: P2)

**Goal**: 三技能"先证据后优化";improve-team 原始工件解析下沉

**Independent Test**: 三 SKILL.md 引用 evidence-step + Unobserved 红线 + ≤500 行 + 镜像一致;improve-skills 闭环演练(SC-006)

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T029 [US5] 启用 T024 中预写的 US5 断言(去除 xfail/skip):三个 improve SKILL.md 均含对 `evidence-step.md` 的引用(单一事实源,零复制定义)、含 Unobserved 红线句、行数 ≤500、improve-team 不再含直接解析 STATE.md/run-log.jsonl 的指令文本(grep 断言其 evidence 输入改为 runs 泳道/findings 表述)——先运行确认全红

### Implementation for User Story 5

- [ ] T030 [P] [US5] 改造 `skills/improve-skills/SKILL.md`:Workflow Step 2("Measure execution effectiveness from history",L32-41)升级为 Step A/B(调 evidence-utils latest/collect,session+feedback 泳道分拣,候选冻结);保留失败模式分类法与既有纪律;改动 30~60 行级
- [ ] T031 [P] [US5] 改造 `skills/improve-agent/SKILL.md`:同构接入 Step A/B(assets 泳道模板 lint 证据入分析);"不从通用最佳实践优化"红线与 Unobserved 红线合并表述;保留六节结构分析法(§3 Analyze root causes)
- [ ] T032 [P] [US5] 改造 `skills/improve-team/SKILL.md`:Inputs 表 evidence 行(L21)与 Behavior Gather evidence 步骤改为消费 runs 泳道 findings(evidence-utils latest/collect),移除对 STATE.md/run-log.jsonl 的直接解析表述;保留 Refinement Map 与结构保持编辑
- [ ] T033 [US5] 三技能镜像 dual-write + parity:分别 `cp -f` 到 `.specify/skills/{improve-skills,improve-agent,improve-team}/SKILL.md`;逐个 `diff -q` 零差异;运行 T029 断言全绿;改造前后 SKILL.md diff 存档(保留项完好性复核,SC-006 素材)
- [ ] T034 [US5] Dogfood 闭环演练(SC-006):对 `skill:improve-skills` 走完整流程——collect(全泳道)→ 按 evidenceState 分拣并冻结候选 → 选一条 Exercised 负向证据做最小定向修改 → 写 `intervention.json`(E8 四要素,verdict 留空)→ 演练记录存档

**Checkpoint**: 消费层改造完成,第一轮干预台账在库

---

## Phase 8: User Story 6 - 纵向验证闭环(Priority: P3)

**Goal**: compare 的 intervention verdict 判定;禁止无证据"已修复"

**Independent Test**: 第二轮采集后 compare 引用第一轮台账并给出判定(SC-007)

### Tests for User Story 6 (MANDATORY) ⚠️

- [ ] T035 [US6] 单元/集成测试(追加到 `tests/integration/test_evidence_python_lanes.py` 或新建 `tests/integration/test_evidence_compare_verdict.py`,先写先红):C-F14 intervention 字段校验、C-E7 verdict 三分支(信号改善 → Outcome-supported;无可比信号 → Unobserved;targetFinding 不存在 → 错误)、verdict 写回幂等

### Implementation for User Story 6

- [ ] T036 [US6] 实现 compare 的 verdict 判定与写回(C-E7 后半):读 baseline 目录 intervention.json → expectedSignal 方向比对 → verdict 写回(compare 为唯一写回方);运行 T035 全绿;镜像同步 `scripts/python/evidence-utils.py` + `diff -q`
- [ ] T037 [US6] 第二轮闭环演练(SC-007):对 T034 同目标再次 collect → compare → 断言输出含第一轮 intervention 引用与 verdict 判定(改善证据不足时如实 Unobserved,禁止"已修复"表述);演练记录存档 <!-- 若两轮间隔内无新执行数据导致信号不可比,verdict=Unobserved 本身即合法验收结果 -->

**Checkpoint**: 纵向验证闭环走通

---

## Phase 9: User Story 7 - 平台适配器探测报告(D2 边界内)(Priority: P4)

**Goal**: 交付边界内仅 doctor 探测报告 + 定序建议(Clarify Q3)

**Independent Test**: doctor 对八工具产出探测报告,定序建议成文(SC-008 边界内段)

### Implementation for User Story 7

- [ ] T038 [US7] 运行 `--action doctor` 产出八工具本地落盘探测快照,结合探测结果撰写 `.specify/specs/034-evidence-infra/platform-adapter-survey.md`:各工具 sessionStore 探测结论、现有适配器现状(qoder/codex/claude/cursor 按源码)、后续适配器实施定序建议(初始候选 opencode → Qwen → iFlow → Hermes → Copilot 按探测修正)、每适配器工作量级注记(Claude = 核实补齐)

**Checkpoint**: US7 边界内交付完成

---

## Phase 10: Polish & Cross-Cutting Concerns

- [ ] T039 [P] 全镜像汇总校验(plan.md Mirror Obligations 全 8 行逐行执行 diff 命令)+ `find . -maxdepth 1 -type l` 符号链接完好检查
- [ ] T040 [P] quickstart.md 全 7 场景逐条实测(§4 技能演练引用 T028 存档;§5 引用 T034;其余命令逐字执行),修正文档与实现的任何漂移(执行验证门)
- [ ] T041 运行全套 `pytest -q` 与 `bash tests/js/run.sh`,对比 T003 基线:零新增失败;新增测试计数入账;结果与 SC-001…008 逐项结论写入 `.specify/specs/034-evidence-infra/verification.md`(含 deferred_tasks= 清单、Node 25 兼容性实测结论、glossary 新词提案记录:泳道/证据合同/干预台账)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1(Setup)**: 无依赖
- **Phase 2(Foundational)**: 依赖 T001;T004-T005 BLOCKS US1/US2(US3 的实现不受阻,但其测试 T019 依赖 T013 骨架)
- **US1(Phase 3)**: 依赖 Phase 2
- **US2(Phase 4)**: 依赖 Phase 2;T011/T012 可与 US1 并行编写
- **US3(Phase 5)**: 依赖 T013(骨架);与 US1 后半可并行
- **US4(Phase 6)**: 依赖 US2(技能要调用 doctor/collect);T025/T026 文档可提前起草
- **US5(Phase 7)**: 依赖 US3(runs 泳道)+ US4(evidence-step.md)
- **US6(Phase 8)**: 依赖 US5 的 T034(第一轮台账)+ US3 的 T022(compare 基础)
- **US7(Phase 9)**: 仅依赖 US2 的 T014(doctor)
- **Polish(Phase 10)**: 依赖全部期望故事完成

### User Story Dependencies

US1 ⊥ US3(可并行);US2 ← US1(引擎在位);US4 ← US2;US5 ← US3+US4;US6 ← US5;US7 ← US2(仅 doctor)。

### Parallel Opportunities

- T002/T003 并行;T006/T007 并行;T011/T012 并行(不同测试文件)
- T025/T026 并行(不同文档);T030/T031/T032 并行(三个不同 SKILL.md)
- US7(T038)可在 US2 完成后任意时点插入

## Parallel Example: User Story 5

```bash
# 三技能改造并行(不同文件):
Task: "改造 skills/improve-skills/SKILL.md Step 2 → Step A/B"
Task: "改造 skills/improve-agent/SKILL.md 接入 Step A/B"
Task: "改造 skills/improve-team/SKILL.md 切换 runs 泳道消费"
```

## Implementation Strategy

**MVP = Phase 1-4(US1+US2)**:引擎托管 + 合同 + 三 Node 泳道,即可独立演示证据采集。随后增量:US3(保底泳道)→ US4(公共入口)→ US5(消费改造)→ US6(纵向闭环)→ US7(探测报告)。每个 Checkpoint 可停下独立验证。

## Notes

- 先测后码:T011/T012/T019/T024/T029/T035 均须在对应实现前编写并确认失败(T006 为移植回归,豁免先红)
- 镜像纪律:每个触碰镜像面的任务内嵌 dual-write + diff 验证,Phase 10 再全量复核
- `cp` 可能别名为 `cp -i`:统一用 `cp -f`/`\cp`(既有环境 gotcha)
- 候选冻结红线(T034):分拣完成后不得增删候选;Unobserved 只记录
- Node 25 兼容:engines 越界不阻塞尝试,实测异常按泳道降级并记录——不修改上游 engines 声明
