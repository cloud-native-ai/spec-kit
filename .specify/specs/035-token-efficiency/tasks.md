# Tasks: 大模型 Token 使用效率纪律(程序优先 + 摘要优先 + 消耗观察反馈)

**Requirement ID**: 035
**Requirement Key**: 035-token-efficiency
**Related Feature**: 040 Token Efficiency Discipline (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/035-token-efficiency/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/(discipline-doc, feedback-marker, audit-and-gates), quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 强制;本需求交付物以模板/文档/共享约定为主 → 采用**结构性 contract 测试**(内容/标题/镜像一致性断言),引擎 `--contains` 改动附行为级 contract 测试;无运行时应用可跑 unit/integration 的部分不硬造)

**Organization**: Tasks are grouped by user story;doc-feature 分类法(author-section / mirror-parity / render-verify / refresh-verify),不套用 Models→Services→Endpoints。

**Environment Prerequisites**: 仅 python3 + pytest + git(本机已具备,计划期已探测);无 docker/网络/集群依赖,各阶段无需环境前置块。

## Definition of Done (DoD)

- DoD-1: FR-001…FR-009 全部落地,纪律定义唯 token-efficiency.md 一处(引用不复制)
- DoD-2: 全部新增 contract 测试通过;全套 pytest 相对 baseline.txt 零新增失败
- DoD-3: audit.md 冻结后未增删行;top-5 行全部 remediated 且附前后注入量实测对比
- DoD-4: 镜像零漂移(`sync-mirrors.py --check` exit 0;skills 双镜像 `diff -rq` 干净;per-tool 副本含整改措辞)
- DoD-5: quickstart.md 五步走查全部通过;verification.md 覆盖 SC-001…SC-005 各一行状态
- DoD-6: 一次真实 Token 观察条目可经 `list --contains token-efficiency` 完整检索(SC-005 实证)

**DoD Status**: pending

## Completion Gate

- GATE-1: 全套测试零新增失败 — check: `pytest -q` 输出与 `.specify/specs/035-token-efficiency/baseline.txt` 失败集比对
- GATE-2: plan.md Mirror Obligations 每行核验 — check: `python3 scripts/python/sync-mirrors.py --check`(exit 0)+ `diff -rq skills/ .specify/skills/` 触点子集
- GATE-3: 无 `[ ]`/`[>]` 任务行残留 — check: `grep -cE '^- \[[ >]\]' .specify/specs/035-token-efficiency/tasks.md` 返回 0
- GATE-4: verification.md 覆盖全部 SC — check: SC-001…SC-005 各有状态行(grep 比对 requirements.md)
- GATE-5: 审计清单冻结完整性 — check: audit.md 行数与冻结时点一致,top-5 行状态全为 `remediated`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖)
- **[Story]**: US1/US2/US3
- **[blockedBy: Txxx]**: 显式依赖,全部 `[X]` 前不得开工

---

## Phase 1: Setup

**Purpose**: 基线与预检(既有基线纪律:动手前记录,区分存量失败与新回归)

- [X] T001 记录全套 pytest 基线:`pytest -q` 输出摘要与失败清单写入 `.specify/specs/035-token-efficiency/baseline.txt`(含失败测试 ID 列表,供 GATE-1 comm 比对)
- [X] T002 [P] 预检镜像零漂移:`python3 scripts/python/sync-mirrors.py --check` exit 0;若有漂移先停下调查(不得顺手覆盖)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 纪律单一事实源 + ambient 引用 + 存量审计——三者是全部故事的判据与输入

**⚠️ CRITICAL**: 审计排序(top-5)决定 US1/US2 的整改对象;纪律文档是审计判据

- [X] T003 [P] 编写结构性 contract 测试(先 RED):`tests/contract/test_token_efficiency_discipline.py` 断言 C-D1(文件+镜像存在且字节一致)、C-D2(六节标题字面量)、C-D3(规则清单/例外 (a)(b)(c)/阈值 `≤ 100 行` 且 `≤ 10 KB`/标记约定/不编造数值)、C-D4(templates/instructions-template.md 含 token-efficiency 引用且模板双镜像一致);运行确认 RED
- [X] T004 [blockedBy: T003] 撰写 `shared/guidelines/token-efficiency.md`(canonical;六节结构按 data-model.md §1:程序优先/摘要优先/升级阶梯/小文件阈值/判定边界/消耗观察;互引 tool-reuse-gate.md 与 feedback-step.md,不复制其定义)
- [X] T005 [blockedBy: T003] 在 `templates/instructions-template.md` 增 ambient 引用节(置于 Task Complexity Rubric 相邻位置;引用路径,不内联规则全文)
- [X] T006 [blockedBy: T004,T005] 镜像扇出与核验:`python3 scripts/python/sync-mirrors.py --write` 后 `--check` exit 0(覆盖 shared/guidelines 新文件与 instructions-template 镜像)
- [X] T007 [blockedBy: T004] 执行两纪律存量审计并产出 `.specify/specs/035-token-efficiency/audit.md`:动态枚举 `templates/commands/*.md` + `skills/*/SKILL.md` + `shared/workflow/*.md` + `shared/guidelines/*.md` + `scripts/python/*-utils.py`(引擎按 data-model.md §4 矩阵复核);每违规行含 V-NNN/单元/纪律/证据 file:line/注入量 `wc -l`+`wc -c` 实测/频率/严重度名次/状态;排序定稿即冻结(C-A1/C-A2);Phase 0 采样五热点(plan/clarify/implement/tasks/requirements)必须逐一复核收录或说明排除理由
- [X] T008 [blockedBy: T006] 运行 `pytest tests/contract/test_token_efficiency_discipline.py -q` 确认 GREEN(纪律文档与 ambient 引用合同闭合)

**Checkpoint**: 纪律判据就绪、审计清单冻结——US1/US2/US3 可并行开工

---

## Phase 3: User Story 1 - 程序优先:确定性判断交还程序 (Priority: P1) 🎯 MVP

**Goal**: 固定规则判断交确定性程序;创作门槛带程序优先检查项;program-first 类 top-5 违规整改

**Independent Test**: 选一个 program-first 整改项重跑:判断结论与整改前一致,注入量显著下降;创作检查单含检查项且双镜像一致

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T009 [P] [US1] 编写创作门槛 contract 测试(先 RED):`tests/contract/test_token_efficiency_gates.py` 断言 C-A3 五文件(create-skills/improve-skills 两检查单 + create-agent/create-team/create-tools 三 SKILL.md)含字面量 `token-efficiency` 检查项、`.specify/skills/` 镜像一致、`templates/skills-template.md` 未新增检查单节
- [X] T010 [US1] [blockedBy: T007] 编写 program-first 整改钉扎测试(先 RED):`tests/contract/test_token_efficiency_remediation_program_first.py` 按 audit.md 冻结的 program-first 类 top-5 行写"违规原句消失 + 程序化替代指令存在"字符串对(预期候选:templates/commands/tasks.md 的宪法 MUST/TDD 关键词扫描改为 grep 步骤;实际以清单为准,若 top-5 无 program-first 行则测试标注 skip 理由)

### Implementation for User Story 1

- [X] T011 [P] [US1] [blockedBy: T009] 在 `skills/create-skills/references/skill-creation-quality-checklist.md` 增 Token 效率检查组(确定性步骤交程序?数据访问摘要化?引用 `shared/guidelines/token-efficiency.md`)
- [X] T012 [P] [US1] [blockedBy: T009] 在 `skills/improve-skills/references/skill-quality-checklist.md` 增对偶检查组(同 T011 形式)
- [X] T013 [P] [US1] [blockedBy: T009] 在 `skills/create-agent/SKILL.md`、`skills/create-team/SKILL.md`、`skills/create-tools/SKILL.md` 各自验证/校验步骤加一行 token-efficiency 检查项引用
- [X] T014 [US1] [blockedBy: T011,T012,T013] skills 镜像双写与核验:同步五文件至 `.specify/skills/` 对应路径,`diff -rq skills/create-skills .specify/skills/create-skills`(等五组)全部干净
- [X] T015 [US1] [blockedBy: T010] 整改 program-first 类 top-5 行(canonical 命令模板→`python3 scripts/python/sync-mirrors.py --write` 扇出 per-tool 副本);在 audit.md 对应行记录前后注入量实测对比并置 `remediated`
- [X] T016 [US1] [blockedBy: T014,T015] 运行 `pytest tests/contract/test_token_efficiency_gates.py tests/contract/test_token_efficiency_remediation_program_first.py -q` 确认 GREEN

**Checkpoint**: 程序优先纪律可独立验证交付

---

## Phase 4: User Story 2 - 摘要优先:数据文件原文不整体入上下文 (Priority: P1)

**Goal**: summary-first 类 top-5 违规整改(整读式上下文加载→摘要/投影级指令);引擎摘要模式缺口按名次处置

**Independent Test**: 选一个整改后的例行流程重跑:决策不受影响、注入量降 ≥ 50%、无机器管理数据文件原文整体注入

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T017 [P] [US2] [blockedBy: T007] 编写 summary-first 整改钉扎测试(先 RED):`tests/contract/test_token_efficiency_remediation_summary_first.py` 按 audit.md 冻结的 summary-first 类 top-5 行写字符串对(预期候选:plan.md "all files in `.specify/memory/features/`" 整读、clarify.md "Load common context" 整读、implement.md 一次性全工件加载、requirements.md 最新规格整读取家规;实际以清单为准)

### Implementation for User Story 2

- [X] T018 [US2] [blockedBy: T017] 整改 summary-first 类 top-5 行:改写 canonical `templates/commands/<cmd>.md` 为摘要级指令(行投影/定向节选/引擎查询 + 升级阶梯引用),`sync-mirrors.py --write` 扇出 `.specify/templates/` 与 5 套 per-tool 副本;audit.md 对应行记前后 `wc` 实测对比并置 `remediated`
- [X] T019 [US2] [blockedBy: T007] 引擎摘要模式缺口处置:history-utils.py(及审计新发现引擎)若入 top-5 → 增摘要级输出模式 + `.specify/scripts/python/` 镜像 + 行为测试;未入 → audit.md 记 `backlogged` 行(条件任务,二选一必落其一)
- [X] T020 [US2] [blockedBy: T018] 副本核验:`sync-mirrors.py --check` exit 0;抽查每个整改命令的 `.qoder/commands/`、`.claude/commands/` 等副本含整改措辞且保留 AUTO-GENERATED 头
- [X] T021 [US2] [blockedBy: T018] Manual QA(SC-003/SC-004 抽样):重跑 1 个整改后的流程(如 /speckit.plan 的上下文加载段),核对结论一致 + 注入量降 ≥ 50%,记录于 audit.md 备注列

**Checkpoint**: US1+US2 硬约束面完整,可独立验证

---

## Phase 5: User Story 3 - 消耗观察:Feedback 承载 Token 效率自评 (Priority: P2)

**Goal**: feedback-step Reflect 扩展三问自评 + [[STR-001]] 标记;`list --contains` 检索闭环

**Independent Test**: 跑一次命令至 wrap-up 产出带标记反馈点;`list --contains token-efficiency` 一次返回全部 Token 观察条目;干净运行零新增观察条目

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T022 [P] [US3] 编写反馈标记 contract 测试(先 RED):`tests/contract/test_token_efficiency_feedback.py` 断言 C-M1(feedback-step.md step 2 含三问自评、标记字面量 `token-efficiency`、干净运行句式、不编造数值规则)+ C-M2(`--contains` 大小写不敏感子串、与既有过滤器 AND、空结果 exit 0、输出仍为摘要级、省略时行为不变)+ C-M3(全量检索完备性,用临时反馈目录 fixture)

### Implementation for User Story 3

- [ ] T023 [US3] [blockedBy: T022] 扩展 `shared/workflow/feedback-step.md` Canonical block step 2(Reflect):三问自评 + 有发现内嵌 `token-efficiency` 标记 + 干净运行不加条目 + 定性/代理口径;嵌入单元零改动
- [ ] T024 [P] [US3] [blockedBy: T022] 在 `scripts/python/feedback-utils.py` 的 `list` action 实现 `--contains <text>`(引擎程序侧读文件匹配 frontmatter summary + 正文;输出保持摘要级)
- [ ] T025 [US3] [blockedBy: T023,T024] 镜像扇出核验:`sync-mirrors.py --write` + `--check` exit 0(shared/workflow 与 scripts/python 两触点)
- [ ] T026 [US3] [blockedBy: T025] 验证闭环(SC-005 实证):对本 spec 已存在的含标记反馈条目(035 运行已产生)执行 `python3 scripts/python/feedback-utils.py --action list --contains token-efficiency --limit 0`,确认全部返回、无误报;运行 `pytest tests/contract/test_token_efficiency_feedback.py -q` GREEN

**Checkpoint**: 三故事全部独立可验

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T027 [P] [blockedBy: T006] 将 ambient 引用同步应用到现行 `.specify/instructions.md`(生成文件,按模板同款措辞落节;注明下次 /speckit.instructions 再生时由模板保障)
- [ ] T028 [P] [blockedBy: T025] 文档增量:在 `docs/reference/skills/feedback.md` 补 Token 效率自评维度与 `--contains` 检索一段(引用纪律文档,不复制规则)
- [ ] T029 [blockedBy: T016,T020,T021,T026] GATE-1 终验:全套 `pytest -q` 与 baseline.txt 比对零新增失败;`sync-mirrors.py --check` exit 0
- [ ] T030 [blockedBy: T029] quickstart.md 五步走查逐条执行并产出 `verification.md`(SC-001…SC-005 各一行状态 + `deferred_tasks=` 登记;审计冻结完整性 GATE-5 复核)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: 无依赖,立即可跑(T001/T002 可并行)
- **Phase 2**: 依赖 Phase 1;T007(审计冻结)阻塞 US1 的 T010/T015、US2 的 T017/T019
- **Phase 3/4/5(US1/US2/US3)**: 均依赖 Phase 2;彼此文件面不相交(US1: skills 检查单 + program-first 模板;US2: summary-first 模板 + 引擎缺口;US3: feedback-step + feedback-utils),可并行
- **Phase 6**: 依赖全部故事完成(T029 汇聚)

### User Story Dependencies

- US1/US2 共享 audit.md(只写各自类别行的状态列,行集不相交);对 `templates/commands/` 的整改文件按审计分类互斥,若同一文件同时出现两类违规行则 T015 先于 T018 处理该文件(串行护栏)
- US3 与 US1/US2 零文件交集,完全独立

### Parallel Opportunities

- T003 与 T001/T002 后即可先行;T009/T017/T022 三个测试授权任务跨故事并行
- US1 内 T011/T012/T013 并行;US3 内 T023 与 T024 并行(不同文件)

## Parallel Example: Phase 2 完成后

```bash
# 三故事的 RED 测试并行开写:
Task: "T009 创作门槛 contract 测试 tests/contract/test_token_efficiency_gates.py"
Task: "T017 summary-first 钉扎测试 tests/contract/test_token_efficiency_remediation_summary_first.py"
Task: "T022 反馈标记 contract 测试 tests/contract/test_token_efficiency_feedback.py"
```

## Implementation Strategy

- **MVP**: Phase 1 → Phase 2 → Phase 3(US1)——纪律文档 + 审计 + 程序优先整改即最小可交付
- **Incremental**: US2(最大注入量收益)→ US3(观察闭环);每故事结束跑其 GREEN 验证任务后可停点交付
- **Pin Hygiene**: 钉扎字符串对在审计冻结时点写死(计数即合同);测试中的文件清单一律 glob 派生或写前 existence-check,禁止幻影路径;不做 `startswith` 版本钉

## Notes

- 全程 canonical → mirror 单向:任何 `.specify/`、`.qoder/` 等副本手改均为缺陷
- audit.md 冻结后只改状态列/备注列;发现新违规记后续迭代,不回填
- `--limit 0` 语义若引擎不支持,以足够大 limit 替代并在 C-M3 测试中固定口径
- 反馈灌水护栏:T026 验证用既有真实条目,不为凑数批量制造观察条目
