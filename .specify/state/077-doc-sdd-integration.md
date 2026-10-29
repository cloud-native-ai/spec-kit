# Line State — 077-doc-sdd-integration

<!-- loop-state:begin -->
spine_state: running
run_id: r20261030T010236Z-077a
slice: 077
stage: review
stage_started_at: 1793303420
stage_deadline_epoch: 1793308820
stage_base_commit: 0abf94c3
attempt: 0
retry_limit: 2
last_verdict: implement DONE — 28/28 任务（4 段）；Feature 077 = Implemented；8 SC 状态行（4 pass / 4 partial，partial 均需真实表达类试点线）；174 定向测试；零新增机制；镜像与副本 clean；下一步 review
<!-- plan-fence: decomposition=single-package reason=not-beneficial (28 tasks <= 40, tightly coupled shared engine and seven templates) test-budget=baseline@implement-start + closure@post-review -->
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

### clarify — DONE（2026-10-30）

- 提交：`5f88e3b5`
- 八条裁定：① `**Flow Class**: <value>` 单行、仅 requirements 头部、非法值阻断/缺省 execution+标注；② 接线面 **七个**命令；③ `flow-class-check.py lookup` 第三键族 `spec:<dir>`，退出码 0/1/2 三分；④ `## Document Structure` 四子节 + `doc-consistency-check.py --action structure`（不新增第七面），基线=主体集合首次运行违规集；⑤ implement 证据面 = template-only Partial + SC 记门禁 verdict；⑥ 驱动从规格读类别、U4 四项 blocking、两槽位换 docs-gate 内容；⑦ 077 新 Feature 承接边，069 保持 Implemented；⑧ 回退四条且「取值越界」不在回退列
- 门：validate ok（256 行 / 33 定义行 / 6 STR）；overlap clear；pre-analyze pass（0/0）

### plan — DONE（2026-10-30）

- 提交：`159aa940`
- 产物：`plan.md`（18 行宪法检查 + 3 条 DTR）/ `research.md`（R-1…R-13）/ `data-model.md`（E1–E9 + 9 规则）/ `contracts/` 6 文件 77 条款 / `quickstart.md` 7 场景 / `feature-ref.md` / 13 份证据
- 门：`pre-analyze --stage plan` pass（errors=0 / advisories=13–14，全为待建测试文件）；FR 25/25；clause 车道 baseline-missing（设计内）；镜像六对 ok；`validate-decision-tensions` 0 error / 0 HIGH
- 关键发现：① 七模板接线必然打破 069a 的 `test_a6_wiring_set_is_closed`，修订方式是把七模板并入已接线名册、分母不变；② `flow-class-check.py` 对 `spec:` 键今天返回 exit 2 + default，声明行不可区分；③ `audit-test-budget.py` 不校验 `selection_basis` 枚举，`docs-gate-full` 可被接纳；④ 确认门预算 27 项零余量
- 结构：`## Constitution Check` → `## Decision Tensions` → `## Project Structure` 相邻（076 模板契约生效）

### tasks — DONE（2026-10-30）

- 提交：`ab288aab`（tasks + baseline + 证据）、`45b6b732`（wrap-up）
- 27 任务（Setup 1 / US1 7 / US2 4 / US3 3 / US4 5 / Polish 7）；77 条款由 19 行认领，各一次、同文件内单调
- 门：`validate-tasks` PASS（0/0，green_claims=77）；`decomposition --mode tasks` proceed（25 FR / 27 tasks）；`pre-analyze --stage tasks` pass（32 advisory，全为待建测试文件）；coverage ok（77/25/25）；baseline 冻结 `1a00c4b5…` @`06c31b1d`
- 偏差：五个红先行项落四个测试文件（execution 反向守卫是同文件具名腿）；`green-path-divergence` WARN 以 `see` 指针消解；MVP = US1+US2+US3

### checklist — DONE（2026-10-30）

- 提交：`d05d3bef`；产物 `checklists/readiness-2026-10-30.md`（40 项：21 pass / 19 fail）+ `test-evidence/checklist-stage-checks.md`
- 失败簇：声明与接线（exit-1 停止指令、子节字面量、剥离边界）、解析引擎（字段 8 vs 9、查找顺序、引擎缺席不可观测、声明/缺省未裁决）、文档结构（缺三子节码、章节两向比对无输入、plan 不产四子节）、驱动槽位（U4 与 implement 算子表不相容、无哈希字段、`not-applicable` 记 pass 冲突、槽位 rc 无单一进程）、不变量（确认门 27 无复测、features 仍写 2 STR）
- 零修改面成立；`validate-requirements` ok（256 行 / 33 定义行 / 6 STR）

### analyze — BLOCKED ×2，两轮修复均已落地（2026-10-30）

- 提交：`6217a86f`（analyze #1：14 HIGH / 9 MEDIUM / 6 LOW → 29/29 修复）；本轮 spec-only 提交（analyze #2：1 HIGH + 6 MEDIUM + 5 LOW）
- analyze #2 发现：R-01（HIGH，U4(a) 分母与槽位 NA 跨级等式在「structure=pass + build=NA」的合规样例上给出 `1−1=0≠1` 的伪违规）；R-02（`error` 值域双义）；R-03（Clarifications 陈旧副本）；R-04（登记面第三种「四面」）；R-05（确认门脚本路径错）；R-06（T028 绿而不证）；R-07（阶段记录与台账缺失）；5 条 LOW（R-7 字面量重抄、E1 行数、缺节码同真、剥离遇块内 `###`、FR-001 存量/新增不可判）
- 处置：R-01 取「构建并入单条结果」——站点构建是 `G-implement-structure` 的 `face=build` 子行；删除「算子总数 − (passed+failed) = NA 条数」跨级等式；SC-003 改面级断言。R-02 收窄 `error ∈ {owner-unavailable, -}`。R-03 更正并留日期注记。R-04 改为 reader / evidence / duplicate / count 四面 + `structure` 子步。R-05 改为 `scripts/python/scan-confirmation-gates.py`。R-06 T028 增自有断言。R-07 补 tasks 记录（`ab288aab` / `45b6b732`）、`239 行` 改指针、处置表补第 20–29 行
- 门：validate-requirements / validate-tasks / account-clause-coverage / pre-analyze --stage tasks / validate-decision-tensions / sync-mirrors --check / regen-command-copies --check 全 exit 0（证据 `test-evidence/*-fix2.txt`）；R-01 算术自检 PASS（`test-evidence/r01-na-arithmetic-fix2.txt`）
- 计数：25 FR / 8 SC / 77 条款 / 6 STR / 28 任务；`coverage-baseline.txt` 未重冻结；`expression-gates.md` 与 `flow-class-definitions.md` 未改动

### analyze #1–#3 — PASS（2026-10-30）

- analyze #1（`d05d3bef`）：14 HIGH / 9 MEDIUM / 6 LOW → 修复 `6217a86f`（29/29）
- analyze #2（`6217a86f`）：1 HIGH（R-01 NA 计数单位）/ 6 MEDIUM / 5 LOW → 修复 `0c8f95d3`（12/12，R-01 取「构建并入 `G-implement-structure` 单条结果、删槽位等式、NA 面级」）
- analyze #3（`0c8f95d3`）：**0 CRITICAL / 0 HIGH** / 5 MEDIUM / 10 LOW → 放行 implement；实现前提醒 F-01/F-02/F-03 由 `f7ec22c5` 微修（13/13，记录形态，计数不变）
- 七道门全程 exit 0；069 契约与状态零回写

## Implement 分段计划

- **拆解决策**：`single-package`（reason=not-beneficial）——28 任务 ≤ 40、共享同一引擎与七模板、拆包无收益
- **测试预算**：implement 起点一次全量（`baseline-failed.txt`，后台 b7yhd4v28，PATH 修正）；中间定向；review 后一次 closure
- **分段**（每段 ≤8 任务）：
  1. **P1**：T001–T008（证据槽 / `spec:` 键 / 声明文法与发现 / requirements 模板 / 台账边界）
  2. **P2**：T009–T015（七模板接线 / 两 owner 追加 / 闭合集守卫 / 文档结构 CLI 与两向比对）
  3. **P3**：T016–T022（驱动载荷四元组 / stage-prompts / efficiency-model 槽位 / SKILL / 零新增机制 / 镜像）
  4. **P4**：T023–T028（两态等价 / 069 不变量 / owner 取证 / quickstart S1–S7 / 收尾门禁 / plan 模板骨架）

### implement P1 — DONE（2026-10-30）

- 提交：`29b515b4`；T001–T008 闭合（8/28）
- 产物：`scripts/python/flow-class-check.py` 的 `spec:` 键族 + 声明解析 + 四错码；`templates/requirements-template.md` 的 `**Flow Class**:` 行；两个新测试文件；`features/077.md` 指针
- 定向：43 passed；邻近引擎 292 passed；既有 39 条基线失败未触碰
- 探针：`lookup spec:077-doc-sdd-integration` → `flow_class=execution, source=declaration, error=null`
- 门：validate-tasks PASS；镜像六对 ok；命令副本 OK
- 偏差：Measured Premises 条款提及数 85→99（定义数仍 77）；测试断言改为点名第二行取值；缺 spec 目录取 `invalid-unit-id`；模板字段行不带行尾两空格

### implement P2 — DONE（2026-10-30）

- 提交：`a401db98`；T009–T015 闭合（15/28）
- 产物：七模板接线子节 + 四工具副本；两 owner 类条件追加（只增不改）；`doc-consistency-check.py --action structure`（17 码 / 四族 / 两向仅 `--path`）；两个新测试文件 + 两个既有守卫修订
- 定向：四关键文件 129 passed；邻近 432 passed；`test_expression_gate_wiring` 七模板并入名册、分母不变
- 门：validate-tasks PASS；镜像六对 ok；命令副本 OK
- D-1 披露：`test_expression_compatibility.py` 以文件自带的 `ALLOWED_POST_BASELINE_CHANGES` 机制为七模板登记 reason + marker，未删断言、未改冻结计数；驱动者接受
- 同趟纠正：`--faces` 对照腿补空绿；读者声明行从 duplicate 面剔除

### implement P3 — DONE（2026-10-30）

- 提交：`0fb8a2bf` + `f5835e0e`；T016–T022 闭合（22/28）
- 产物：`test_docs_gate_driver.py`（33 条）；`stage-prompts.md` 四元组 + U4 四项 + implement 证据面；`efficiency-model.md` §2.8 `docs-gate-full`；`SKILL.md` Hard Requirement 13；零新增机制与镜像收尾证据
- 零新增机制：命令 27/27 差分 `[]`、依赖 6/6、进程 19/19、服务空集、确认门 27=27、FACES 仍四面
- 门：validate-tasks PASS；镜像六对 ok；命令副本 OK
- 偏差：证据文件双轨命名（四份并存）；五次同趟断言对齐；T018 以新增 H3 落位，未改既有清单

### implement P4 — DONE（2026-10-30）

- 提交：`0abf94c3`；T023–T028 闭合（28/28，0 `[ ]` / 0 `[~]`）
- 两态等价：35 文件剥离后逐字回基线；owner 追加 +28/−0，11 个禁动章节逐字节相同；069 六份规格 diff 空
- SC：SC-001/004/006/007 = pass；SC-002/003/005/008 = **partial**（均需一条真实表达类试点线；每条 note 写明测了什么/没测什么）
- quickstart S1–S7 实跑；S2 前提补 owner 后三例吻合；S4 正控口径更正（humanize 基线 0→0）
- plan-template 骨架 +61 行；`test_x16` 未转红；镜像第二次同步后六对 ok
- 偏差：T027 在 T028 之后跑两次（取最终树）；翻转与最后两个 `[X]` 同提交；S2 夹具补 owner 文档

## 测试预算（E2/E3）

| seq | slot | stage | selection_basis | command | rc | passed/failed | failed_names_path | evidence_ptr |
|-----|------|-------|-----------------|---------|----|---------------|-------------------|--------------|
| 1 | baseline | implement | full-suite | `PATH=<pybin>:$PATH SPECKIT_PYTHON=<profiles-venv> bash .specify/scripts/bash/run-tests.sh --names-out .specify/specs/077-doc-sdd-integration/baseline-failed.txt` | 1（39 既有失败） | 6593 passed / 39 failed / 7 skipped（553.62s） | `.specify/specs/077-doc-sdd-integration/baseline-failed.txt`（39 名，与 076 closure 逐名相同） | 本行 + 基线文件 |

中间阶段一律用定向集，禁止第二次全量；closure 全量在 review 之后。

（implement 起点与 review 后写入。）

## 框架观察

（U4/U6 时补记：现象 / 框架位置 / 对驱动的影响。）
