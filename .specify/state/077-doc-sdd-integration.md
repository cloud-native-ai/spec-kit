# Line State — 077-doc-sdd-integration

<!-- loop-state:begin -->
spine_state: running
run_id: r20261030T010236Z-077a
slice: 077
stage: clarify
stage_started_at: 1793293871
stage_deadline_epoch: 1793299271
stage_base_commit: 481242b5
attempt: 0
retry_limit: 2
last_verdict: requirements DONE — 25 FR / 8 SC / 4 US；validate ok / pre-analyze pass / decomposition proceed；Feature 077 = Draft；gate 全过；wrap-up 记录待驱动者提交
<!-- loop-state:end -->

- line_id: `077-doc-sdd-integration`
- run_id: `r20261030T010236Z-077a`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，单工作区）`
- base_sha: `c1cd4600`（076 收尾后的 master）
- trunk: `master`（`docs/git-workflow.md`；`main` 为上游世系，不参与合并）
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`）
- **执行拓扑**：本地（宿主原生子代理）
- **终态权威文档**：用户本轮需求（把**项目文档**开发接入 SDD 阶段链，使 `sdd-loop-driver` 可无人值守驱动文档开发；项目文档须有与代码同等的结构与逻辑严密性）+ `shared/definitions/flow-class-definitions.md` + `shared/workflow/expression-gates.md` + `.specify/specs/069-execution-expression-sdd/requirements.md` + `.specify/memory/constitution.md` + `.specify/instructions.md` + `docs/concepts/spec-driven.md` + `skills/external/sdd-loop-driver/SKILL.md`
- **特性切片**：Feature 077 —— **项目文档的 SDD 接入**（特性级类别解析 + 六阶段命令按类切换门禁算子 + `sdd-loop-driver` 类别感知）。**不拆片**：FR 预算 ≤30、任务 ≤40；若门判 split-required 再议。
- **用户裁决（2026-10-30）**：项目文档 ≠ 办公文档；项目文档要像代码一样有严密结构与逻辑；接入 SDD 后要能用 `sdd-loop-driver` 无人值守开发。
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure（review 后全量）→ 工作树清扫 → 本地合并 master`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链
- **拆解开关**：`decomposition: auto`；`decomposition_stages: plan=auto, implement=auto, review=auto`；`decomposition_slot_cap: 2`
- **测试预算**：implement 起点一次全量、review 后一次 closure；中间用定向集
- **合并**：本地合并（缺省）；**不 push**（用户未授权时）

## U1 断点探测（2026-10-30 01:02）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `077-doc-sdd-integration`（自 `master@c1cd4600` 切出） |
| 工作树 | 干净 |
| Feature 注册 | 最大 076；**077 未登记** |
| spec 目录 | `.specify/specs/077*` 不存在 |
| 结论 | **断点 = requirements** |

## 现状锚点（2026-10-30 实测，供 requirements 阶段引用）

1. **分类轴已存在但按「流程单元」而非「特性」**：`flow-class-check.py --action check` 报 79 单元全覆盖；`lookup --unit-id "/speckit.implement"` 返回 `flow_class=execution`（basis=`mixed-oracle`）。特性索引 `.specify/memory/features.md` **没有** `flow_class` 列。
2. **六阶段命令未读类别**：`grep -rl "flow_class|flow-class|expression" templates/commands/` 仅命中 `docs.md`、`review.md`、`humanize.md`；`requirements/plan/tasks/checklist/analyze/implement` 六个模板零命中。
3. **表达式门禁已定义且部分接线**：`shared/workflow/expression-gates.md` 有六面封闭集 + 八阶段算子表（G-ID）；已接线入口 `/speckit.docs`、`skill:create-docs`（R6 两处）、`/speckit.humanize`/`skill:humanize`；`isomorphism` 检查 8 阶段 / 6 门禁 / 0 发现。
4. **文档型 SDD 的目标已写进 069**：US2「文档型特性仍走全阶段，但每阶段判定换成能证伪文档的算子」；Out of Scope 明确「不新建命令、属后续特性」。
5. **驱动侧无类别感知**：`skills/external/sdd-loop-driver/` 的阶段提示词、U4 校验与两槽位测试预算均按代码型特性设计；没有读取 `flow_class`、没有表达式门禁的 U4 检查项。
6. **宪法 VII 的 template-only 条款**：无运行时代码的特性 Test-First 可判 `Partial (justified)`，「tests」验证模板内容/规范路径/结构。

## 拟议范围（requirements 阶段须逐条裁决为 FR 或排除项）

- **特性级类别**：在特性注册/详情或 requirements 上声明 `flow_class`，由确定性引擎解析；未声明按 `execution` 并标注（沿用 069 FR-009）。
- **六阶段按类切换算子**：`requirements/clarify/plan/tasks/checklist/analyze/implement` 读取类别；`expression` 时执行 `expression-gates.md` 的阶段算子表（读者声明、证据/as-of、事实一致性、结构零新增违规），不再要求代码测试；`execution` 行为不变。
- **文档结构与逻辑的硬约束**：plan 必须产出文档结构（章节/读者/证据清单/事实 owner），implement 必须按结构落文并跑结构校验；「文档像代码一样」的要求落到可判定门禁。
- **驱动侧接入**：`sdd-loop-driver` 阶段提示词携带类别；U4 对 expression 特性校验表达式门禁证据；两槽位测试预算在 expression 下改为 docs 门禁槽位（不得静默跳过）。
- **保留不变量**：八阶段集合不变、analyze/review 100%、不新增 `/speckit.*` 命令、不引入运行时。

## 阶段记录

### requirements — DONE（2026-10-30）

- 提交：`63848d3b`（spec + 清单 + 证据 + 注册）、`481242b5`（STR id 引用与登记前行数）
- 产物：`requirements.md`（25 FR / 8 SC / 4 US / 2 STR / 9 排除 / 11 假设 / 9 边界）、`checklists/requirements.md`（16/16）、`test-evidence/` 3 份
- Feature：077 = `Draft`，`features/077.md` + `features.md` 行（Total 72→73）
- 门：`validate-requirements` ok（239 行 / 33 定义行）；`pre-analyze --stage requirements` pass（0/0）；`decomposition --mode plan` proceed（25 ≤ 30）
- 绑定：新建 Feature 077；069 作为前序 owner（分类轴），不触碰其正文与状态
- 偏差：A3 派发句「六个模板」与枚举七个命令名不一致 → 以枚举为准（含 clarify）；A7 脚手架在仓库外调用以抑制切分支

## 测试预算（E2/E3）

（implement 起点与 review 后写入。）

## 框架观察

（U4/U6 时补记：现象 / 框架位置 / 对驱动的影响。）
