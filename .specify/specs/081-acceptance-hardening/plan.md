# Implementation Plan: Stricter Acceptance & Artifact Review（更严格的验收与产物审查）

**Branch**: `081-acceptance-hardening` | **Date**: 2026-11-03 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `081-acceptance-hardening` → Feature 081 更严格的验收与产物审查（Stricter Acceptance & Artifact Review）
**Input**: Specification from `.specify/specs/081-acceptance-hardening/requirements.md` (clarified 2026-11-03; 25 FR / 9 SC / 17 STR）

## Summary

把「Implemented」从「任务勾完 + 每条 SC 有一行状态」收紧为「每条 `final` 路径 SC 为 `pass` + 一条确定性最小 smoke 记录在案」，把「本能力由某仓提供」收紧为一张可验收的运行时栈所有权表加一张执行前提／继承 blocker 表，并把 `/speckit.review` 从「恰好两段」扩为「四段 + 一次确定性判定」。

技术路线是**一条判定源、两个新载体、零第二套门禁**：

- **一条判定源**：新脚本 `scripts/python/closure-acceptance-check.py`（stdlib-only、只读、退出码 0/1/2）产出 `accept|block` + 封闭原因集里的命名原因 + `final` 路径的 `final_path` 计数记录（`{pass, blocked, deferred, partial, fail, unknown, total}`）；`/speckit.implement`、`/speckit.review`、`sdd-loop-driver` 的 closure/merge 三处共用它，MUST NOT 各自重判。
- **两个新载体**：单一 schema owner 文档 `shared/workflow/acceptance-hardening.md`（`Path` 标注、`Blocked` 状态与四条转移、verification 词表与五项测量阶梯、两张新表的列与取值域、封闭原因集、review 组合与 ARC 边界），以及一个运行时可达的内部技能 `skills/internal/review-feature-quality/`（承载产物审查段与实现审查段；命令模板只引用路径与章节锚，MUST NOT 内联方法论）。
- **零第二套门禁**：四类确定性发现落进既有 `pre-analyze-check.py` 与既有 `expression-gates.md` 的 requirements/plan 门行；不存在「只能由模型判断」的新门禁。

本特性自己的 smoke 是一条命令（`bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`），覆盖 `specify init`（临时夹具）、正／负夹具过 checker、`regen-command-copies.py --check` 三件事，连跑两次退出码一致。

## Technical Context

**Language/Version**: Markdown（模板 / 技能 / 命令面）+ Python 3（新引擎 stdlib-only；实测解释器 CPython 3.14.6，`requires-python >= "3.8"` 不变）；不新增第三方依赖
**Primary Dependencies**: 既有引擎 `scripts/python/{validate-requirements,regen-command-copies,sync-mirrors}.py`、`skills/external/sdd-loop-driver/scripts/{pre-analyze-check,line-registry,integrate-lines}.py`、`skills/internal/code-review/scripts/git-delta-review.sh`（`base..head` 解析，实现审查段复用它而不重写）；新增 `scripts/python/closure-acceptance-check.py` 与内部技能 `review-feature-quality`
**Storage**: 无数据库、无服务。判定输入是 spec 目录内的 Markdown/JSON（`requirements.md`、`plan.md`、`tasks.md`、`verification.md`、特性详情与索引、依赖特性详情）；夹具是声明式最小文件集（`tests/fixtures/acceptance-hardening/`）；证据落 `<spec-dir>/test-evidence/` 与 `<spec-dir>/baseline-failed.txt`
**Testing**: `bash scripts/bash/run-tests.sh`（解析 `.venv/bin/python` 优先）→ `pytest 9.2.0` on `CPython 3.14.6`；基线失败 id 集 `<spec-dir>/baseline-failed.txt`（`--names-out` 采集），关闭判据是 `head 失败集 − 基线失败集` 为空；pins 与采集过程见 `research.md` § R1 与 `test-evidence/plan-runner-pins.txt`
**Target Platform**: 任何支持 Spec Kit 的 agent 宿主；判定面只要求 POSIX shell + `python3` + `git`；`specify init` 依赖 `specify` 控制台入口（前提 EP-003）
**Project Type**: single（框架源码 + 自举运行时双帽：改 `templates/`、`shared/`、`skills/`、`scripts/`、`src/`、`tests/`，`.specify/` 同名文件由再生成入口产出）
**Performance Goals**: 无吞吐目标。checker 对 081 自身规格的判定 < 1 s（4 个 Markdown 输入 + 1 个注册表）；smoke 单次 ≤ 2 min（`specify init` 一次 + 3 次引擎调用）；两次 smoke 退出码一致（2/2）
**Constraints**: checker MUST 只读（零写入，`--audit-existing` 只读审计）且 stdlib-only；退出码三态 0/1/2；封闭原因集 7 项不得扩张；MUST NOT 新建第二套并行门禁；MUST NOT 替换 `code-review`；MUST NOT 回写历史特性状态与历史 verification 记录；不 push
**Scale/Scope**: 4 条用户故事；25 FR / 9 SC（`final` 仅 SC-001、SC-002）；预计改/建 **43 个源面**（模板 10、shared 3、技能 11、脚本 2、`src/` 1、测试 16）+ 6 对镜像关系 + 4 份按工具命令副本；实现任务自然计数 ≈58（分组读数之和 55，加本阶段补入的三行：集合级基线比较、覆盖率账目、`manage-features` 词表）> 40 → 按 US1–US4 切 081a–081d（见 § Design Decisions D10）。六个分项逐项加总 = 43：模板 `feature-details`/`verification-log`/`tasks`/`feature-index`/`plan`/`review` 6 个 + `commands/` 下 `review`/`implement`/`tasks`/`checklist` 4 个；shared 3 个；技能 5 个内部技能 + `sdd-loop-driver` 的 `SKILL.md`、两份 `references/`、三个 `scripts/` = 11；脚本 2 个；`src/` 1 个；测试 = 6 个新契约模块 + 1 个 schema 唯一性守卫 + 1 个 smoke + 8 个按 `research.md` § R3 逐条改的钉扎模块 = 16（夹具目录是数据而非源面，不计入）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 18 principles in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计决定都追到 FR：`contracts/gate-wiring.contract.md` § 可追溯性是 FR→条款→测试的唯一映射；两句 `MUST NOT` 阈值（`final` 路径全 `pass`、smoke 在案）直接来自 FR-002/FR-005 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 081（`feature-ref.md`）；本阶段只落 `Draft → Planned` 与 `Key Changes`，不新建行、不回退他人状态（`features.md` 行与 `features/081.md` 同趟更新） |
| III | Intent-Driven Development | ✅ Pass | Summary 先给「用户看到的差别」，实现细节留给 `contracts/`；D1–D10 逐条记录被否决的替代方案（`## Design Decisions`）而非只留结论 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 每个新判定都有先写或同批写的契约/单元测试：`tests/contract/test_closure_acceptance_check.py`（正／负夹具红先行）、`test_line_state_blocked.py`（A6 八项处置）、`test_acceptance_state_machine.py`、`test_acceptance_review_composition.py`、`test_acceptance_premises.py`、`test_gate_wiring_081.py`（三处调用点，081a 断言 implement 一处）、`test_acceptance_schema_ownership.py`（SC-009 ④ 唯一性守卫与声明点豁免断言，081d）；第四条件把既有 `test_status_gate_owner.py` 钉的「三个合取条件」改为四个（`all required` 措辞保留，条件计数 3→4），该模块因此进入 `research.md` § R3 的钉扎清单并随 081c 同批改；验收场景 SC-001…SC-009 的采集方法已由 requirements § Measurement Sources 声明 |
| V | AI Agent Integration Standards | ✅ Pass | 不动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；四份按工具副本只经 `regen-command-copies.py` 生成（`## Mirror Obligations`） |
| VI | Continuous Quality & Observability | ✅ Pass | 关闭判据用基线差集而不是「看起来绿」：`head 失败集 − 基线失败集` 为空且 `基线失败集 − head 失败集` 逐条列为已修复项（SC-009）；历史状态不回写，审计只读（FR-020） |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本阶段只推进到 `Planned`；Pre-Status-Flip Gate 的判据 owner 保持 `templates/feature-details-template.md` § Canonical Status State Machine，本文件与命令面只加「第四条合取条件」的指针（FR-002/FR-016） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 设计前实测而非引用记忆：`get_resource_path()` 的真实行为（`research.md` § R2）、`line-registry.py` 七个状态值与守卫行号（§ R6）、两处 `--check` 的零漂移基线（§ R5）、测试收集数与缺失依赖（§ R1） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 一个 stdlib 脚本 + 一个内部技能 + 一份 owner 文档；无运行时、无守护进程、无新依赖、无第二套门禁；被否决的「重编号 review 报告小节」「wheel 安装进 smoke」记录在 § Design Decisions 与 `research.md` |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件均为小写 kebab-case 且路径即语义：`shared/workflow/acceptance-hardening.md`、`skills/internal/review-feature-quality/SKILL.md`、`tests/fixtures/acceptance-hardening/`；不触保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 改动全部落框架源；`.specify/` 下的 templates / shared / skills / scripts 四层由 `sync-mirrors.py` 产出，四份按工具命令副本由 `regen-command-copies.py` 产出（`## Mirror Obligations` 逐行给出再生成命令）；081 自身按本特性的新规则走（`## Execution Premises` / `## Inherited Blockers` 已在本文件成立） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `pre-analyze-check.py`（而不是第四类检查器）、`line-registry.py`（而不是第二个线状态存储）、`integrate-lines.py --gate-cmd`（而不是新的合并器）、`git-delta-review.sh`（而不是重写 base 解析）、`validate-requirements.py`（而不是第二个需求校验器） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Change Validation（`final` 路径阈值 + smoke 硬条件）与 Reliable Delivery（closure/merge 判定共享一条源），并把「声称 vs 实测」的差额交给 ARC，对应 `shared/guidelines/better-harness.md` 的五维 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 新 schema 单一 owner = `shared/workflow/acceptance-hardening.md`（[[STR-017]]），其余位置只带路径 + 章节锚；三处词表 owner 各写自己的值（A5）；SC-009 ④ 用守卫测试机械断言「除 owner 外 0 处出现」 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 面向人的产出（review 报告、wrap-up 结论、拒绝原因）按 `shared/guidelines/user-facing-comprehension.md` 写作；机器面字面量一律英文原样（A10），翻译只发生在人的一侧 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 判定是二值（`accept` / `block`），无中间严重度层（FR-006 + `## Constraints`）；本计划已按 fast-fail 处置一处实测矛盾：`specify init` 前提不成立 → 记为 `EP-002` `falsified` + `Decision: resolve-in-scope`，不静默绕过 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | 新目录 `tests/fixtures/acceptance-hardening/` 登记进 `.specify/instructions.md` § Key Directories 的 `tests/` 行（`tests/fixtures/` 当前未登记），该登记是 **081a T018** 的一部分而不留作 081d 的欠账；临时产物落 `.specify/.tmp/`（`git check-ignore` 已覆盖） |
| XVIII | Grounded Naming | ✅ Pass | 名字取自需求与兄弟形态：`closure-acceptance-check.py`（同目录既有 `validate-requirements.py` / `flow-class-check.py` 形态）、`review-feature-quality`（兄弟 `review-sdd-process` / `code-review`）、`acceptance-hardening`（branch 与 spec key）。用户裁定的中文名「更严格的验收与产物审查」贯穿 Feature 名与描述 |

**Gates Status**: ✅ All gates pass — no Fail, no Partial, no Complexity Tracking row.

**Re-check after Phase 1**: 2026-11-03, re-run against the landed Phase 1 artifacts — all 18 rows stay ✅ Pass. The only row whose evidence moved is IV: the red-first contract test paths now exist as planned deliverables in § Source Code, each annotated with the slice that owns it (081a's three new modules plus the extended `test_requirements_checker.py`; 081b's `test_acceptance_premises.py`; 081c's `test_acceptance_review_composition.py` with the deliberate updates of `test_review_code_composition.py` and `test_status_gate_owner.py`; 081d's `test_line_state_blocked.py` and `test_acceptance_schema_ownership.py`), and the fixture set (`tests/fixtures/acceptance-hardening/{positive,negative,…,mixed-path,expr-supporting-only,execution-without-final}/`) is enumerated in `data-model.md` § Fixture set instead of being named only in this table.

## Decision Tensions

Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`. The five records below are the load-bearing trade-offs this plan makes; every one of them touches either a contract other features depend on, the gate every future feature passes, or a constitution `MUST`.

### T-001 — `final` 路径阈值是二值阻断，且 `Blocked` 是一等状态而不是「带备注的 Implemented」

- **decision**: 一条 `final` 路径 SC 非 `pass` 时特性 MUST 落 `Blocked`（一等状态、写入状态机 owner、线状态同名字面按 A5 分属各自 owner），不再允许以 `partial` / `deferred` / `unknown` 混过 `Planned → Implemented`。
- **antithesis**: 保留「每条 SC 有状态行即可 Implemented」，只把 `final` 路径未通过记为 `Implemented (with gaps)` 的备注列并在 review 中警告；当该特性的下游消费者都是人、且状态字段只用于排序而不是用于放行时，它更优——改动面只有一处词表，零新状态、零新转移、零迁移风险。
- **binding_constraints**:
  - pole_a: 状态字段必须能阻断下游——被引用为「已验证前提」的状态不许与实测脱钩（026 形态的失效面就是这里）。
  - pole_b: 状态机必须可恢复——把「暂时测不到」写成终态会让线永久停在不可动作状态（`Blocked → Ready for Review` 因此 MUST 非法）。
- **discriminating_evidence**: 用负夹具（任务全关、每 SC 有状态行、`final` 路径 SC 全 `blocked`）跑三处调用点，看是否三处都输出 `block` 且原因逐字命中封闭集；结果二值：3/3 拒绝 / 存在一处放行。
- **expected_sacrifice**: SC-001 Source ↑ 三处调用点各自接线、共享一条判定源；任一调用点的接线遗漏都会让该 SC 的 3/3 退回 2/3，关门成本从「加一行词表」上升到「三处接线 + 一处夹具」。
- **revision_trigger**: 出现一个 `execution` 特性因环境限制无法产出任何 `final` 路径测量而被迫长期停在 `Blocked` ≥2 个迭代 → 重开，评估把 `final` 下限改为「至少一条 `final` 或显式用户豁免」的形态。

### T-002 — review 的终态是「四段 + 一次确定性判定」，ARC 不委派给任何技能

- **decision**: `/speckit.review` 固定顺序执行 过程段 → 产物段 → 实现段 → 代码段 → Acceptance Reality Check；前四段各自成文各自定级，ARC 是确定性判定（读取 `verification.md` 与特性状态），不是第五段。
- **antithesis**: 合并为三段（把实现段并入代码段），ARC 作为代码段内的一个必检项；当切片很小、`code-review` 与实现审查的 diff 视图高度重叠时它更优——一次 diff 阅读同时回答「代码对不对」与「实现满足需求没有」，省掉一段的重复读盘成本。
- **binding_constraints**:
  - pole_a: 两个判定对象不许互相代答——「本次实现是否满足 requirements/tasks」与「已提交代码 delta 是否有可验证缺陷」是不同问题，一个过了不代表另一个过（FR-014 明文）。
  - pole_b: review 一次运行的成本必须有界——每多一段就多一次全量读盘或一次 smoke 实跑。
- **discriminating_evidence**: 取一个「实现满足需求但代码含 `blocking` 缺陷」的切片和一个「代码干净但漏实现一条 FR」的切片，分别跑 review，看两段是否各自给出对方给不出的 finding；结果二值：两个切片都能被对应段单独抓到 / 有一段无法独立成立。
- **expected_sacrifice**: SC-006 Source ↑ 一次 review 从两段变四段，单次运行时长与读盘量上升；本特性的 census 也从三个单元变四个单元（产物/实现段的载体技能各有自己的收尾记录），`test_review_feedback_boundary.py` 的 C-58 因此必须同趟改。
- **revision_trigger**: 连续两次真实 review 出现「产物段与实现段的 finding 完全重叠」→ 重开，评估合并为三段并把 ARC 固定为段内判定。

### T-003 — 线状态 `blocked` 可恢复（不进终态守卫集），但与 `merge_ready` 结构性互斥

- **decision**: `blocked` 加入线状态集，`ACTIVE_STATES` 与 `HOLDING_STATES` 不变、`merge_ready=false` 不变量、`integration-*` 不可达、终态守卫集 `{closed, stale, orphaned}` **不**纳入 `blocked`；恢复路径是 `update --state active` + 记录 unblock 原因。
- **antithesis**: 把 `blocked` 归入终态守卫集（与 `closed`/`stale`/`orphaned` 同款不可动作），恢复只能靠 `deregister` + 重新 `register`；当「阻塞几乎总是以重建线收场」时它更优——一条线一个生命周期，状态转换数量最少，不需要为 `blocked → active` 单独解一条守卫。
- **binding_constraints**:
  - pole_a: 阻塞必须可解且不泄漏资源——转入 `blocked` 时释放 lease 并清空 `holder_line_id` / `waiting_reason`，否则阻塞线像泄漏的 lease 一样把等待者钉死。
  - pole_b: 终态语义不许被稀释——`closed`/`stale`/`orphaned` 的「不可再动作」是 `release-ownership`、`archive-runtime` 等动作的守卫前提。
- **discriminating_evidence**: 造一条 `blocked` 线，跑 `promote-waiting`、`integration-enqueue`、`merge-ready`、`update --state active` 四个动作，看「前三个拒绝、第四个放行且 lease 已释放」；结果二值：四个动作判定与 A6 八项逐项一致 / 存在一项相反。
- **expected_sacrifice**: SC-001 Source ↑ 增量落在状态机而不是判定逻辑——八项处置每一项都是一条可拨动断言，任一拨错都会让「blocked 线可入队」这类旧约束与新值矛盾而不报错。
- **revision_trigger**: 出现一条进入 `blocked` 后又因 `update --state active` 绕过 ownership 重新取权的事故（或该路径被守卫发现）≥1 次 → 重开，改为「`blocked` 恢复必须经 `ownership-check` 显式动作」。

### T-004 — 产物段与实现段的方法论载体是**新增内部技能**，不是既有技能下的命名文档

- **decision**: 新建 `skills/internal/review-feature-quality/SKILL.md`，其正文以两个具名段承载（`Segment A — Artifact Review`、`Segment B — Implementation Review`），运行时路径 `.specify/skills/internal/review-feature-quality/SKILL.md`；`templates/commands/review.md` 只引用路径与章节锚。
- **antithesis**: 把方法论写成 `skills/internal/review-sdd-process/references/artifact-and-implementation-review.md` 一类的命名文档，由过程段技能顺带承载；当希望「段数不变、只加文档」而避开技能普查改动时它更优——零新增技能、零普查计数变化、零第四套收尾记录。
- **binding_constraints**:
  - pole_a: 每段必须有独立且可运行时抵达的 owner——否则「两段各自成文、互不代答」没有承载物（A12 要求载体是能以运行时路径抵达的具名 owner）。
  - pole_b: 过程技能的判定对象不许被污染——`review-sdd-process` 的判定对象是「产出该切片的 SDD 流程」，把产物/实现审查塞进它的 references 会让「过程段 MUST NOT 被当作产物段或实现段的替代」变成一句无对象的话。
- **discriminating_evidence**: 检查 `review-sdd-process` 的正文在加入载体后是否仍只声明一个判定对象；结果二值：其判定对象仍唯一（新技能承载两段）/ 出现第二个判定对象（文档方案）。
- **expected_sacrifice**: SC-006 Source ↑ 三份冻结普查（`test_skill_layer_visibility_guards.py` 37→38、`test_expression_compatibility.py` 52→53、`test_migration_distribution.py` 52→53）与四单元 census 必须同趟改；这些是「段→技能」形态的既有代价，不是本决策的意外。
- **revision_trigger**: 该技能在实践中被复用为零次（两个迭代内没有除 review 之外的调用点，且其正文与过程段正文出现 >30% 重复段）→ 重开，评估降级为过程技能的命名文档。

### T-005 — `specify init` 的开发树前提由「修 resolver」而不是「smoke 里装 wheel」解决

- **decision**: 给 `src/specify_cli/__init__.py` § `get_resource_path()` 补上其 docstring 已声明的 repo-root 回退分支（安装布局优先不变），使 `specify init` 在开发检出上使用工作树模板。
- **antithesis**: smoke 里先 `pip install .` 再跑 `specify init`（或让 smoke 指向 `.venv` 里已安装的旧副本）；当「smoke 必须验证发布形态」时它更优——它证明的是用户真正拿到的那份 wheel，而不是开发树。
- **binding_constraints**:
  - pole_a: smoke 必须验证**工作树**——否则模板改动（本特性的主交付面之一）不被任何 smoke 覆盖，绿了也不代表改对了。
  - pole_b: smoke 必须确定性且最小——一次命令、无网络、无构建工具依赖。
- **discriminating_evidence**: 在开发检出上跑 `.venv/bin/specify init <tmp> --ai claude --script sh --no-git --ignore-agent-tools`，看它使用工作树模板并退出 0，且安装到 site-packages 的 CLI 行为不变；结果二值：两者同时成立 / 任一不成立。
- **expected_sacrifice**: SC-008 Source ↑ smoke 依赖 `specify` 控制台入口存在（前提 EP-003），比纯 python 调用多一条环境前提；该前提已进 `## Execution Premises` 并以命名原因在缺失时失败，不静默跳过。
- **revision_trigger**: 该回退分支被下游项目报告为「装好后仍读取本地 templates」≥1 次 → 重开，改回仅安装布局并把 smoke 换成 wheel 安装路线。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/081-acceptance-hardening/
├── requirements.md      # /speckit.requirements output — this spec's What
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 output — R1…R9 实测与否决方案
├── data-model.md        # Phase 1 output — 实体 / 字段 / 取值域 / 状态转移
├── quickstart.md        # Phase 1 output — 可执行场景（逐例标注执行状态与前提）
├── contracts/           # Phase 1 output — 5 份契约（含条款 → FR → 测试 可追溯性）
├── feature-ref.md       # Phase 1 output — Feature 081 绑定与交付面
├── baseline-failed.txt  # FR-023 基线失败 id 集（本阶段采集，实现期比较用）
├── test-evidence/       # 本阶段与实现期的证据（plan 门禁输出、runner pins、smoke 证据）
├── tasks.md             # Phase 2 output (/speckit.tasks — 不在本阶段产出)
└── verification.md      # 实现输出 (/speckit.implement)
```

### Source Code (repository root)

```text
# 框架源（本特性实际改/建的面；.specify/ 侧是生成镜像）
templates/
├── feature-details-template.md        # 状态机：四条件 Planned→Implemented、Blocked 四条转移、第四条件（081a）
├── verification-log-template.md       # 词表 +blocked、五项测量阶梯、smoke 三件记录（081a）
├── tasks-template.md                  # GATE-4 升级（final 路径 pass/豁免 + smoke 记录）（081a）
├── feature-index-template.md          # 状态词表 +Blocked（081d）
├── plan-template.md                   # 新增两张强制表骨架（Execution Premises / Inherited Blockers），无取值域（AS-15；081b）
├── review-template.md                 # 新增 ### 2.2 / 2.3 / 2.4 三个稳定槽位（081c）
└── commands/
    ├── review.md                      # Composition 改写：四段 + ARC、逐段五项、四单元 census（081c）
    ├── implement.md                   # Pre-Status-Flip 接线 checker + Blocked 翻转（081a）
    ├── tasks.md                       # GATE-4 接线 + smoke 任务义务（081a）
    └── checklist.md                   # 只引用 owner，不复制第四条件（081c 改写指针，081d 复核镜像）
shared/
├── workflow/acceptance-hardening.md   # NEW 唯一 schema owner（STR-017）；081a 落 4 节，081b 加 § Runtime Stack & Dependency Ownership / § Execution Premises / § Inherited Blockers（含 Source row 与 Carrier 语法），081c 加 § Review Composition
├── workflow/feature-integration.md    # § Pre-Status-Flip Gate 增加 checker 调用与 Blocked（081a）
└── workflow/expression-gates.md       # requirements/plan 门行接入四类确定性发现（081b）
skills/
├── internal/review-feature-quality/SKILL.md   # NEW 产物段 + 实现段载体（081c）
├── internal/review-sdd-process/SKILL.md       # 严重度家族 owner + 组合顺序指针（081c）
├── internal/manage-features/SKILL.md          # 状态词表 +Blocked（081d）
├── internal/implement-feature/SKILL.md        # 步骤 8/9 接线 checker（081a）
├── internal/code-review/SKILL.md              # 段位声明（仍是第 4 段，未被替换）（081c）
└── external/sdd-loop-driver/
    ├── SKILL.md                               # U6 收束步骤引用 closure 判定（081d）
    ├── references/stage-prompts.md            # § U6 收尾：线闭合前跑 checker（081d）
    ├── references/dispatch-recipes.md         # § 集成序列：quality gate = checker，block → 线 blocked（081d）
    └── scripts/{pre-analyze-check,line-registry,integrate-lines}.py   # 四类发现（081b）、线状态八项（081d）、closure 门（081d）
scripts/python/
├── closure-acceptance-check.py        # NEW 唯一判定源（stdlib-only、只读、0/1/2）（081a CLI + US1 判定；081b 补齐三处外部来源抽取）
└── validate-requirements.py           # 新增 path-marker 检查（第六个标签）（081a）
src/specify_cli/__init__.py            # get_resource_path() 的 repo-root 回退（smoke 前提）（081a）
tests/
├── contract/{test_closure_acceptance_check,test_acceptance_state_machine,
│             test_gate_wiring_081}.py  # NEW 红先行契约测试（081a）
├── contract/test_acceptance_premises.py  # NEW 四类发现 + in-scope 三项义务 + inherited 载体 + pin 有效性（081b）
├── contract/test_acceptance_review_composition.py  # NEW 四段 + ARC（081c；与既有 test_review_code_composition.py 同批改）
├── contract/test_line_state_blocked.py   # NEW 线状态八项处置的断言载体（081d）
├── contract/test_acceptance_schema_ownership.py  # NEW SC-009 ④ 唯一性守卫（owner 字面量 0 处外溢 + 三个声明点豁免断言；081d）
├── integration/test_acceptance_smoke.py         # NEW 唯一 smoke（081a）
├── fixtures/acceptance-hardening/               # NEW 声明式最小夹具集（081a 造 7 组：positive/negative/ladder-mutation/smoke-mutation/mixed-path/expr-supporting-only/execution-without-final；081b 补 premise-mutation / runtime-gap-mutation / runtime-zero-row / inherited-mutation / inherited-clean；081c 补 review-implemented-clean / review-implemented-blocked / expected-artifact-missing；081d 补 audit-history）
└── （既有 8 个钉扎模块按 research.md § R3 逐条改，理由随行；含 test_status_gate_owner.py、test_review_code_composition.py）
docs/reference/commands/review.md      # 文档面：两段 → 四段 + ARC（081c）
CHANGELOG.md                           # 本特性条目（081d）
.specify/instructions.md               # § Key Directories 的 tests/ 行补 fixtures/（081a T018）
```

**Structure Decision**: 落在既有的「框架源 + 自举运行时」形状上，不新建任何顶层目录：新引擎进 `scripts/python/`（同目录既有 30+ 个 checker 的兄弟形态，镜像到 `.specify/scripts/python/`），新技能进 `skills/internal/`（嵌套层，不出现在平铺发现面上），新 schema 文档进 `shared/workflow/`（同目录既有 `feature-integration.md` / `expression-gates.md` 的兄弟形态），夹具进 `tests/fixtures/acceptance-hardening/`（既有 `tests/fixtures/` 下的一级概念目录）。

### Mirror Obligations

Baseline measured **before** any edit on this branch (2026-11-03): `regen-command-copies.py --check` exit 0; `sync-mirrors.py --check` exit 0 with templates 22 / skills-external 408 / skills-internal 136 / agents 3 / scripts 118 / shared 61. Baseline drift is zero, so the criterion below is an absolute `exit 0` **and** the reason it is legitimate to state it absolutely is that measurement — not a pre-written expectation.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/{review,implement,tasks}.md` | `.claude/commands/speckit.<name>.md`; `.github/prompts/speckit.<name>.prompt.md`; `.qoder/commands/speckit.<name>.md`; `.opencode/command/speckit.<name>.md` — per-tool copies via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `python3 scripts/python/regen-command-copies.py --check` → exit 0 (baseline exit 0, measured) |
| `templates/{feature-details,verification-log,tasks,feature-index,plan,review}-template.md` | `.specify/templates/` same names | `python3 scripts/python/sync-mirrors.py --check` → exit 0 |
| `shared/workflow/{acceptance-hardening(NEW),feature-integration,expression-gates}.md` | `.specify/shared/workflow/` same names | same `--check` |
| `skills/internal/{review-feature-quality(NEW),review-sdd-process,manage-features,implement-feature,code-review}/**` | `.specify/skills/internal/<name>/**` | same `--check` |
| `skills/external/sdd-loop-driver/**` | `.specify/skills/sdd-loop-driver/**` | same `--check` |
| `scripts/python/{closure-acceptance-check(NEW),validate-requirements}.py` | `.specify/scripts/python/` same names (this pair is `STRICT`: an extra mirror-only file fails) | same `--check` |
| `src/specify_cli/__init__.py`, `tests/**`, `docs/**`, `CHANGELOG.md`, `.specify/instructions.md` | none — `src/` and `tests/` are not in `MIRROR_PAIRS`; `.specify/instructions.md` is this project's canonical instructions (its `§ Key Directories` is project-specific, not template-generated) | n/a (no mirror duty; `git ls-files` shows the single copy) |

## Execution Premises

Owner of this table's shape, its `Status` domain and its `Decision` domain: `shared/workflow/acceptance-hardening.md` § Execution Premises. `falsified` MUST carry a `Decision` from `resolve-in-scope | fallback | user-waiver`.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 一条可用的 pytest 运行器存在（Python ≥ 3.10 + pytest），且是仓内既有入口 `scripts/bash/run-tests.sh` 能解析到的那一条 | 修复后 `.venv/bin/python -m pytest --collect-only -q` → `7016 tests collected in 0.99s`，0 collection error；`pytest 9.2.0` / `CPython 3.14.6`（`research.md` § R1、`test-evidence/plan-runner-pins.txt`） | verified | — |
| EP-002 | `specify init` 能在开发检出上跑通（081 smoke 的第三件事） | `.venv/bin/specify init demo --ai claude --script sh --no-git --ignore-agent-tools` → `Error: Local templates not found.`（`research.md` § R2 逐字） | falsified | resolve-in-scope |
| EP-003 | `specify` 控制台入口在解释器同级可执行文件处存在（smoke 的调用形态前提） | `.venv/bin/specify --help` 打印 Typer 帮助并以 exit 0 结束 | verified | — |
| EP-004 | 两处 `--check` 在动手前零漂移，因此「本特性关闭时 exit 0」是可达判据 | `research.md` § R5 的实测输出（六对镜像 + 四份按工具副本） | verified | — |
| EP-005 | `line-registry.py` 的实际状态集与守卫位置与 A6 的描述一致（含「文件中不存在 `revival` 符号」） | `research.md` § R6 的行号与 grep 零命中；`STATE_VALUES` 七值在第 46 行 | verified | — |
| EP-006 | 内部技能的嵌套层不出现在平铺发现面上，因此新增内部技能无需注册发现面 | `tests/contract/test_skill_layer_visibility_guards.py` guard 1 的实测行为 + `research.md` § R3 | verified | — |
| EP-007 | 仓内 bash 脚本入口可执行（`scripts/bash/create-new-plan.sh` 等），使 plan/tasks 阶段的门禁与产物生成不被环境阻塞 | 直接跑 `bash scripts/bash/create-new-plan.sh --json` 失败（`CWS_LIB_BASH_HOME` 未设）；带 `CWS_LIB_BASH_HOME=/Users/liuqiming.lqm/project/cloud-native-tools/cws-lib-bash` 时输出 `{"FEATURE_SPEC":…,"IMPL_PLAN":…,"SPECS_DIR":…,"BRANCH":"081-acceptance-hardening"}` | verified | — |
| EP-008 | 依赖特性 071 / 077 的 `verification.md` 与 `tasks.md` 是可解析的继承 blocker 来源（FR-011 的抽取对象存在） | `research.md` § R8 的逐条 grep 结果（五条 `_status=partial`、`deferred_tasks=` 为空、两处零 `[~]`） | verified | — |
| EP-009 | 实现起始提交上可采集到失败用例 id 集合，且此后「零新增失败」是可判的 | 本阶段实测 `bash scripts/bash/run-tests.sh --names-out .specify/specs/081-acceptance-hardening/baseline-failed.txt -q` → `39 failed, 6970 passed, 7 skipped in 596.80s`；失败 id 集落 `baseline-failed.txt`（39 行），控制台全文落 `test-evidence/plan-baseline-run.txt`；实现后按 id 级差集比较。**可比性前提**：每次比较前按 FR-023 重读 `pytest --version` / `git --version`，与 `test-evidence/plan-runner-pins.txt` 不一致即判该次比较无效（exit 2），MUST NOT 读作新增失败 | verified | — |
| EP-010 | `git` 可执行并在同一层可读版本（`base..head` 解析、两个 `--check` 的树差异判定、审计的 `git status --porcelain` 都压在这条前提上） | `git --version` → `git version 2.54.0 (Apple Git-157)`，与 `test-evidence/plan-runner-pins.txt` 的 pin 原文一致（同一次采集）；运行时栈 `RS-003` 的 `Premises` 单元格指向本行 | verified | — |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain (`resolved | inherited | not-applicable`), the `Carrier` requirement for `inherited` rows and its pointer duty: `shared/workflow/acceptance-hardening.md` § Inherited Blockers; the obligations themselves are stated once in `requirements.md` FR-011 (081b lands the owner section; 081a's owner-doc skeleton carries only the extension point). Boundary (Assumptions A13): this table owns **dependency-inherited** records only; the plan-time load-bearing premises live in § Execution Premises above; environment probe verdicts live in `tasks.md` § Environment Prerequisites. No fact is written twice; a cross-reference is a pointer, never a restatement.

**Dependency set (derived, not assumed)** — in: Feature 071 (owns the review composition sentence and the status-gate carriers 081 rewrites), Feature 077 (owns the stage-gate rows and the feature-class read 081 rides). Out with reason: Feature 062 ← spec 080 (humanize) has no shared owner document with 081; 072/073/074/076 likewise. Derivation evidence: `research.md` § R8.

**Row grammar (one syntax, owned by `requirements.md` FR-011)**: `Source row` = `<feature-id>:<row-locator>`, no whitespace, `<row-locator>` ∈ `SC-\d{3}_status` / `deferred_tasks` / `deferred:<slug>`; it is the **join key** between the rows extracted from the dependencies and the dispositions below. `Carrier` = `task:<T-ID>+test:<repo-relative test path>` (conjunctive) or `gate:<GATE-ID>`; `Carrier slice` = `this-slice` or a later slice id, and a later slice reads as **`inherited-later`** (legal while Feature 081 is `Blocked` and the slice is in § D10's table — disclosed, neither blocking nor resolved). The extraction set is the closed three-source set: `## Deferred` rows, `blocked`/`deferred`/**`partial`** status rows, non-empty `deferred_tasks=` — `partial` is in it because the five rows actually found below are `partial` and nothing else; excluding it would make this table's extraction empty and the fourth finding unreachable.

**Extraction readings (the closed three sources, measured — two of them yield zero rows, and a zero-row source is a reading, not a disposition)**: `071` detail `## Deferred` → 0 rows, because the section does not exist anywhere in the registry (`grep -rln '^## Deferred' .specify/memory/features/` zero hits) — recorded as **IB-001**; `071` `deferred_tasks=` → empty (line 96) — recorded as **IB-002**; `077` `deferred_tasks=` → empty (line 107), `tasks.md` zero `[~]` rows — recorded as **IB-005**; `071` / `077` `verification.md` status rows in `blocked`/`deferred`/**`partial`** → **five** rows, all `partial` (071 lines 66, 86; 077 lines 77, 89, 101) — these five are the only disposition rows and they are IB-003 · IB-004 · IB-006 · IB-007 · IB-008 below. A source that yields zero rows MUST be recorded as such here and MUST NOT be given an invented locator: a disposition row for a row that does not exist would poison the join key the fourth finding rides on.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| IB-003 | `071:SC-001_status` | not-applicable | — | — | 071 verification.md line 66；该 SC 度量 071 自己切片的一次端到端 review 运行；081 的 SC-001 用自建负夹具在三处调用点独立度量，不消费 071 的该测量 |
| IB-004 | `071:SC-006_status` | inherited | `task:T004+test:tests/contract/test_acceptance_review_composition.py` | `this-slice` | 071 verification.md line 86；081 的 review 组合改写了 071 建立的两段结构，其结构证据必须由 081 重新采集（产物段/实现段/`final_path` 计数记录），不得继承 071 的旧结构结论。载体落在 081c 的必做任务行 T004 + 其测试模块；081b 曾按 **`inherited-later`** 读作已披露，081c 在 tasks 阶段完成载体并改为 `this-slice`，现在两条部分都可解析。**载体不取 SC-006**：SC-006 是 `supporting` 路径、可被 `deferred`，按 FR-011 不构成载体 |
| IB-006 | `077:SC-002_status` | inherited | `task:T012+test:tests/contract/test_acceptance_premises.py` | `this-slice` | 077 verification.md line 77；081 在 `expression-gates.md` 的同一批门行上加四类发现，门行接线改动后必须重测。载体 = 081c 的 T012（逐行复跑 077 门禁并测量 081b 模块的行）+ 其测试模块；081b 以 T005 为载体的行随 `tasks-081b.md` 归档，tasks 阶段将其重指向活行 T012。**载体不取 SC-005**：SC-005 是 `supporting` 路径、可被 `deferred` |
| IB-007 | `077:SC-005_status` | inherited | `task:T012+test:tests/contract/test_acceptance_premises.py` | `this-slice` | 077 verification.md line 89；同上：门行接线改动后必须重测；T012 是逐行复跑对应门禁的必做行，其模块即本切片的唯一测试载体 |
| IB-008 | `077:SC-008_status` | not-applicable | — | — | 077 verification.md line 101；该 SC 度量表达类试点线在真实项目上的文档门禁表现；081 是 `execution` 类，不消费该测量 |

**Dependency artifacts (declared, never implied)**: the checker reads only the paths in this block, never arbitrary backticked `.md` tokens elsewhere in the section.
- `071`: `.specify/memory/features/071.md`, `.specify/specs/071-review-code-integration/verification.md`
- `077`: `.specify/memory/features/077.md`, `.specify/specs/077-doc-sdd-integration/verification.md`

**Readings**: 8 records, 5 dispositions. All five extracted rows carry a disposition (5/5, none undisposed). Of the three `inherited` rows **2 resolve in this slice** (IB-006, IB-007) and **1 reads `inherited-later`** (IB-004, carrier in 081c). The three zero-row sources (IB-001, IB-002, IB-005) carry no disposition because there is no row to dispose — treating them as `resolved` rows would be exactly the invented-locator defect the join key exists to prevent. So the settled count in this slice is **7 of 8 records** with **1 disclosed as `inherited-later`** — not an unresolved blocker, and not a resolved carrier.

**081c update (tasks stage, 2026-11-03)**: the two live carriers were reconciled against the 081c `tasks.md` — IB-004 completes to `task:T004+test:tests/contract/test_acceptance_review_composition.py` with `Carrier slice = this-slice`, and IB-006 re-points from 081b's archived `T005` to the live `T012`. The 081b reading above remains the dated record of that slice's closure, not the current cell values. The underlying mechanism has no archive notion: a `this-slice` carrier is resolved against the live `tasks.md`, so closing a slice invalidates its own `this-slice` carriers until the next slice re-points them. This is recorded as a known item for the driver/schema owner (081d) — either carriers name an explicit slice id resolved against `tasks-<slice>.md`, or a completed-slice reading is introduced; until then, each slice's tasks stage re-points the live rows and measures them.

## Design Decisions (D1–D10)

### D1 — Single owner doc

`shared/workflow/acceptance-hardening.md` (NEW, [[STR-017]]) is the only definition point for: the `Path` marker (form + last-token rule), the feature-status `Blocked` + its four transitions + the narrow `Implemented → Blocked` audit-correction rule, the verification vocabulary and the five measurement-ladder fields, the Runtime Stack & Dependency Ownership table, the Execution Premises table, the Inherited Blockers table, the closed reason set and the three exit codes, and the review composition's **content definitions** (the four segments, the fixed order, the per-segment boundary sentences, the expected-artifact derivation rule, the ARC clause and the census: process / artifact / implementation / code + ARC). Every other artifact carries a path + section-anchor pointer. Machine-checkable consequence: SC-009 ④ asserts that the column names and domain literals exported from the owner's tables appear **zero** times outside the owner across `templates/` and `shared/` (guard test enumerates real hits and asserts equality with an explicit exemption list). That list has **four** members, each with its own assertion: `data-model.md` + `contracts/` (projection surfaces), FR-003 of `requirements.md` (the declaration site), and `templates/plan-template.md` (the skeleton carrier — its empty tables carry **column names only**, zero domain literals, and it is the owner doc's fourth declared carrier). The exemption is per-surface, not a blanket path skip: a fourth member that starts carrying a domain literal fails its own assertion.

### D2 — `closure-acceptance-check.py`

Contract (full text in `contracts/closure-acceptance-check.contract.md`):

- **CLI**: `--spec-dir <dir>` (required), `--repo <root>` (path resolution), `--feature-detail <path>` | `--feature-registry <path>` (claim source; default: resolve from the registry row), `--audit-existing`, `--json` / `--json-out <path>`, `--waive CODE:TARGET` (repeatable, same waiver shape as `pre-analyze-check.py`).
- **Parses**: `requirements.md` (SC definition lines + `**Path**` marker + `§ Runtime Stack & Dependency Ownership` rows), `plan.md` (`§ Execution Premises`, `§ Inherited Blockers`), `tasks.md` (`[ ]` / `[>]` / `[~]` counts), `verification.md` (`SC-NNN_status=`, ladder fields, `smoke_command|smoke_exit_code|smoke_evidence_path`), feature detail/registry (claimed status), dependency feature details (`## Deferred`, `verification.md` status rows, `deferred_tasks=`).
- **Output**: `verdict: accept|block`, `reasons: [{code, target}]` drawn from the closed 7-item set, and `final_path: {pass, blocked, deferred, partial, fail, unknown, total}` computed **once** here (FR-006; ARC reads this, never re-counts). Six status buckets plus `total`, the owner doc's closed shape — `unknown` counts a criterion with no status row, `partial` counts a measured one.
- **Exit codes**: `0` accept, `1` block, `2` input missing/unparsable. `--audit-existing` is zero-write and exits `0` whenever inputs are valid, regardless of findings (FR-020).
- **Shape**: stdlib-only, read-only, no model judgement, self-contained parser (it must run in a checkout without `src/` on `sys.path`; the two existing parsers are reused only where their regexes are stable, per `research.md` § R4).
- **Fixtures**: `tests/fixtures/acceptance-hardening/{positive,negative,premise-mutation,runtime-gap-mutation,runtime-zero-row,inherited-mutation,inherited-clean,review-implemented-clean,review-implemented-blocked,expected-artifact-missing,ladder-mutation,smoke-mutation,mixed-path,expr-supporting-only,execution-without-final,audit-history}/` — each a declarative minimal file set (requirements/plan/tasks/verification/registry), never a real feature directory. The four 081b cases each answer a question the earlier corpus could not: `runtime-zero-row` proves zero data rows is a finding rather than silence; `inherited-mutation` and `inherited-clean` carry a **dependency-side detail and its `verification.md`** (a `## Deferred` section, `blocked`/`deferred`/`partial` status rows and a non-empty `deferred_tasks=`), so the extraction branch is shown to discover rows and not merely to judge fixtures; the mutation half leaves one row undisposed and one carrier pointing at a `supporting`-path SC, the clean half disposes everything and includes one `inherited-later` row. The `negative` set reproduces the 026 shape; `positive` carries a `final`-path pass + a complete smoke record; `mixed-path` carries one failing `final` next to a passing one plus one non-`pass` `supporting` SC (Edge Case "final 与 supporting 混合"); `expr-supporting-only` and `execution-without-final` are the two halves of the class rule — an `expression` feature is not forced to invent a `final` SC, an `execution` feature with zero `final`-path SC fails (V-1 / V-11); `smoke-mutation` is `positive` with the smoke record deleted **and the claimed status set to `Implemented`**, so it is the fixture that proves the claimed-`Implemented`-but-not-accepted reason (`status-claims-implemented-but-blocked`) — without it that reason would carry no counter-example. The three 081c cases answer the two review-site questions no earlier case can: `review-implemented-clean` is `positive` with the claim moved to `Implemented` (the review site's fourth condition is then **judged and passed** instead of skipped as inapplicable — the only honest input for SC-002's `Implemented → Ready for Review` leg), `review-implemented-blocked` is `negative` with the claim moved to `Implemented` (claimed `Implemented` **and** a zero `pass` bucket, which is RC-15's conjunction and the only input that reaches `F-ACCEPTANCE`), and `expected-artifact-missing` lists a required artifact its directory does not hold (the only case where "expected set" and "the set that exists" read differently, so FR-013's missing-artifact clause has something that can go red). Which slice authors which set is fixed in § Source Code.

### D3 — State machine and all call sites

| Surface | Exact edit | Owner reference |
|---|---|---|
| `templates/feature-details-template.md` | `Planned → Implemented` becomes four conjunctive conditions; add `Blocked` rows `Planned → Blocked`, `Blocked → Implemented`, `Blocked → Ready for Review` (**illegal**), `Implemented → Blocked` (audit correction only, must cite evidence); `Implemented → Ready for Review` gains the fourth condition; `[FEATURE_STATUS]` glossary token gains `Blocked` | owner doc § Feature Status |
| `templates/verification-log-template.md` | status set becomes `pass` / `fail` / `partial` / `blocked` / `deferred` / `unknown`; the five ladder fields by their `SC-NNN_`-prefixed names for `blocked` / `deferred` / `partial`; the three-field smoke record; the illegal-row rule (`SC-NNN_reduced_measurement` non-empty AND `SC-NNN_reduced_measurement_run=no`) | owner doc § Verification Vocabulary |
| `templates/tasks-template.md` | GATE-4 upgrade: every `final`-path SC `pass` **and** the smoke record present (or an explicit user waiver); Environment Prerequisites gains its A13 boundary note | owner doc § Gates |
| `templates/feature-index-template.md`, `skills/internal/manage-features/SKILL.md` | status vocabulary gains `Blocked`; the never-regress rule gains its narrow audit-correction exception. Measured: `templates/feature-index-template.md` is 21 lines and carries only the `Status` **column header** — it has no value-domain list today, so its edit is to **add** a closed status vocabulary containing `Blocked`, not to insert one value into an existing list (SV-06) | owner doc § Feature Status |
| `skills/internal/implement-feature/SKILL.md` (**Step 8 — Completion validation** and **Step 9 — Pre-Status-Flip Gate and Verification Log**), `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate | run the checker before the flip and land `Blocked` at the status-landing point (Step 9; Step 8 is the completion-gate re-validation); `block` → land `Blocked` (never a zero-final-pass `Implemented`); one pointer to the owner, no restated criteria | owner doc § Gates |
| `templates/commands/implement.md`, `templates/commands/tasks.md`, `templates/commands/checklist.md` | wire the gate / GATE-4 / fourth-condition reference | owner doc § Gates |

### D4 — Runtime stack, premises, inherited blockers

- `requirements.md` gains the mandatory § Runtime Stack & Dependency Ownership (columns `ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises`; `Form ∈ {in-scope, signed-contract, user-waived}` and `not-required` for expression-class features with a stated reason). `Contract` and `Premises` are **their own cells, read by column name**: the contract path used to live inside `Owner` prose, which is why the contract-path check had nothing to read, and the premise ids need a cell for FR-010's "every runtime-dependent FR cites a premise" to be checkable at all. Prose-only dependency declaration is a violation (`runtime-dependency-not-owned: RS-NNN`), and "prose" is decidable rather than a reading: inside the section, fenced code blocks and headings are removed, then a `- **Runtime dependency**: <capability> — <owner>` line is a declaration (id ⇒ the reason, no id ⇒ input error naming the line) while a narrative line without the marker is not. **Zero data rows is a finding, not silence**: section absent ⇒ input error; present with zero rows ⇒ `runtime-dependency-not-owned: runtime-stack` (the reserved argument); a row with a required-but-empty cell ⇒ `runtime-dependency-not-owned: RS-NNN`. Zero rows was measured today to produce *no* reason at all, which is the false green this feature exists to remove.
- **`in-scope` is three judged obligations, not one prose claim** (owner: `requirements.md` FR-009 / FR-012): (1) the `FR` cell resolves to an FR defined in this spec; (2) at least one `tasks.md` row quotes that FR — a **line-level** match (`^- \[.\] T\d{3}.*\bFR-0NN\b`), because an FR mentioned in a table cell or in prose is not a task row; (3) `verification.md` carries a joint-acceptance row naming that `RS-NNN`. Judgment stays inside the existing closed set: (1) failing is an **input error (exit 2)**, never a `block`; (2) or (3) failing is `runtime-dependency-not-owned: RS-NNN` — the same reason as the prose-only case, so no eighth reason is coined. **Each duty is judged where its carrier is readable** — (1) at requirements, (2) at tasks, (3) at closure — because a stage that cannot see `tasks.md` or `verification.md` cannot report the duty as satisfied; the 081a parser may stay minimal and the three checks are 081b's.
- `plan.md` gains § Execution Premises (`verified | unverified | falsified`; `falsified` requires `Decision`) and § Inherited Blockers (every dependency `## Deferred`/blocked row dispositioned, with a `Carrier` for every `inherited` row — FR-011).
- **Table skeletons land in `templates/plan-template.md`** (two empty tables with the fixed column sets, **no value domains and no invalid-row rules** — AS-15 keeps the semantics in the owner doc). 081b owns that edit; without it every future plan would have to invent the columns. The skeleton is therefore the owner doc's **fourth declared carrier** and the fourth member of SC-009 ④'s exemption list: it may repeat the column set and nothing else, and the guard asserts that it carries zero domain literals.
- The four deterministic findings land in `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` and are surfaced through the existing `expression-gates.md` rows `G-req-clarity` / `G-plan-fact` — no new gate registry row, no second checker (FR-012). The obligations added by FR-009 (items 2–3) and FR-011 (carrier existence) are absorbed by the **existing** runtime-row and inherited-blocker classes, so the finding count stays four.
- A13 boundary is stated once in the owner and pointed at from `templates/tasks-template.md`: plan § Execution Premises = planning-time load-bearing premises; plan § Inherited Blockers = dependency-inherited records; tasks § Environment Prerequisites = task-generation probe verdicts (with probe command + date). Same fact in two places is the defect.

### D5 — Review composition (A12 carrier decision)

**Carrier = new internal skill `skills/internal/review-feature-quality/SKILL.md`** (runtime `.specify/skills/internal/review-feature-quality/SKILL.md`), with two explicitly named segments: `## Segment A — Artifact Review` and `## Segment B — Implementation Review`. Rationale and the rejected alternative (a named reference doc under `review-sdd-process`) are recorded as **T-004**.

- Severity: both new segments emit `P0`/`P1`/`P2` — family owner `skills/internal/review-sdd-process/SKILL.md`; finding form = severity + artifact/implementation path + line (**required whenever the artifact is line-addressable**; a finding that omits it MUST name why in its own text — a MUST with one decidable escape, never an optional field). The implementation segment **quotes** the `final_path` record and never re-judges it; the hard condition stays the implement gate's (V-9). `code-review` keeps its six levels; ARC's item is fixed `P0` [[STR-016]]. No mapping table, no conversion, no unified score.
- `templates/commands/review.md` § Composition becomes "four segments plus one deterministic check, one fixed order" (process → artifact → implementation → code → ARC) and rewrites `## Delegation` to per-segment `Skill / Judgment object / Severity / Inputs / Outputs`; it references the new skill by runtime path and inlines no methodology.
- ARC is not a segment and is not delegated: it runs the checker, copies the `final_path` record (`pass` / `blocked` / `deferred` / `partial` / `fail` / `unknown` / `total`) into `review.md` (carrier slot `### 2.4`), and on "claimed Implemented/Ready for Review with zero `pass`" emits P0 `F-ACCEPTANCE` and refuses the transition.
- Consequence recorded (not a surprise): the feedback **unit census grows from three to four** (`/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review`) because the command MUST NOT suppress a delegated skill's wrap-up. `tests/contract/test_review_feedback_boundary.py` (C-58) is updated deliberately, with the reason stated in the plan and in the commit.

### D6 — Line state `blocked`

**Obligation authority = `requirements.md` § Assumptions A6 items 1–8** (which invariants change, which must not, and where recovery goes). This section is a **landing map**, not a second definition: it names, per A6 item, the symbol or guard in `skills/external/sdd-loop-driver/scripts/line-registry.py` that the obligation touches, with the measured line numbers from `research.md` § R6. The single test carrier is `tests/contract/test_line_state_blocked.py` (081d), which pins each item with at least one assertion; § E-9 of `data-model.md` keeps only the entity boundary. Nothing here restates A6.

| A6 item | Landing point in `line-registry.py` (measured, `research.md` § R6) |
|---|---|
| 1 — `STATE_VALUES` 7 → 8 | the closed set literal at line 46 |
| 2 — `ACTIVE_STATES` unchanged | the `--active` list, `_active_entries`, and `promote-waiting`'s `state == "active"` counter |
| 3 — `HOLDING_STATES` unchanged, `blocked` holds nothing | the transfer cleanup that mirrors `closed` (`holder_line_id` / `waiting_reason` / `queued_at`) |
| 4 — `blocked ⇒ merge_ready` false | the same validation point that enforces `merge_ready ⇒ completed` (line 707) |
| 5 — `integration-*` unreachable | the three actions' `state == "completed"` requirements |
| 6 — terminal guard set stays three-valued | lines 1447/1949/2139/2249/2266 |
| 7 — `promote-waiting` keeps `state == "waiting"`; recovery is `update --state active` | `promote-waiting`'s precondition **and** the "entering `active`" guard at line 764, which must admit `blocked` alongside `{waiting, stalled}` — the one measured interaction where A6 talks to the same line from both sides (§ R6) |
| 8 — `stale_from_state` may carry `blocked` | `deregister --reason stale-cleanup`'s write point (comment + test only, no enum expansion) |

`integrate-lines.py` runs the closure checker as its gate **by default** (the existing `--gate-cmd` hook, not a second path); on `block` it records `integration-record --result failed --reason closure-blocked` **and** marks the line `blocked` with the named reason, so the line never reaches `completed`. **Timing** (FR-017 / GW-03): the judgement runs at the **feature line's closure** — one line spans 081a–081d — and MUST NOT be read as "every slice merge passes the closure judgement"; slice merges are judged by the review gate (D5). `references/stage-prompts.md` § U6 and `references/dispatch-recipes.md` § 集成序列 point at that step; they do not restate the reason set.

### D7 — Smoke test for 081

- **Exactly one command** (recorded verbatim in `tasks.md` / `verification.md`):
  `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`
- **Helper location**: `tests/integration/test_acceptance_smoke.py` (it must import the repo's own engines and use `tmp_path`, which the suite's `conftest.py` already provides, including the neutralized host git config).
- **What it covers** (FR-005): (a) `specify init` on a `tmp_path` fixture — `<interpreter dir>/specify init <tmp>/demo --ai claude --script sh --no-git --ignore-agent-tools`, asserting exit 0 and a generated `.specify/` tree; (b) the closure checker on the positive fixture (expect `accept` / exit 0) and on the negative fixture (expect `block` / exit 1 with `zero-final-path-pass` in the reason set, ⊆ closed set); (c) `regen-command-copies.py --check` → exit 0.
- **Determinism**: no network, no wall-clock in the assertions, sorted output; the evidence file is byte-identical across runs so "twice the same exit code" is a stronger, machine-visible fact.
- **Evidence**: the test writes `<spec-dir>/test-evidence/smoke-081.txt` (repo-relative path recorded as `smoke_evidence_path=`), containing the three sub-commands and their exit codes; `verification.md` records command / exit code / evidence path.

### D8 — Test-runner preflight (result: **runner established**)

`research.md` § R1 is the measurement. Summary decision: repair `.venv` in place (six missing distributions from the internal mirror), keep `scripts/bash/run-tests.sh` as the single entry (it resolves `.venv/bin/python` first), and pin RS-002 / RS-003 from the first real run — `pytest 9.2.0` on `CPython 3.14.6`, `git version 2.54.0 (Apple Git-157)`. No version is invented; nothing was written into `pyproject.toml` (the repo has never pinned these). Baseline collection: `bash scripts/bash/run-tests.sh --names-out <spec-dir>/baseline-failed.txt -q`, run at plan time so the baseline predates 081's own new tests (a baseline taken after they exist would contaminate the comparison).

**Pin validity** (owner: `requirements.md` FR-023; `contracts/artifact-schemas.contract.md` AS-07): a pin that is a transcript of one run is only valid while re-reading it reproduces it. Every baseline-difference comparison therefore re-reads `pytest --version` and `git --version` first; a mismatch against `test-evidence/plan-runner-pins.txt` makes **that comparison invalid** (input error, exit 2) and MUST NOT be read as new failures. A rebuilt `.venv` or a different machine means re-collecting the baseline, not reusing the old one — the 39-id baseline belongs to `pytest 9.2.0` on `CPython 3.14.6`.

### D9 — Two Hats and mirrors

Source edits land in `templates/`, `shared/`, `skills/`, `scripts/`, `src/`, `tests/`. Then exactly two regeneration entries: `python3 scripts/python/regen-command-copies.py` (+ `--check`) for the four per-tool command copies, and `python3 scripts/python/sync-mirrors.py` (+ `--check`) for the six mirror pairs. `.specify/` copies are never hand-edited as the primary change; `src/` and `tests/` have no mirror. Exact pairs and the measured baseline: `## Mirror Obligations`.

### D10 — Tasks / decomposition (estimate: ≈52 > 40 → slices declared)

Natural task count by surface group: Setup 3; Foundational (owner doc + checker + fixtures + `validate-requirements` marker) 8; US1 (state machine, verification vocabulary, GATE-4, implement/feature-integration wiring, three call sites) 11; US2 (runtime-stack table, premises, inherited blockers, four `pre-analyze` findings, A13 boundary) 9; US3 (new skill, review template slots, command rewrite, ARC, census 3→4 + its guard) 11; US4 (three vocabulary owners, `--audit-existing`, mirror/regen, docs + CHANGELOG + directory registration) 8; Polish (baseline compare, smoke evidence, full-suite zero-new-failure) 5 → **≈52 tasks**, above the ceiling of 40.

Slices (boundaries at plan entry; **no requirement is dropped** — every FR/SC is assigned to exactly one slice, and the mapping table lives in `tasks.md`):

| Slice | Scope | Est. tasks | Depends on |
|---|---|---|---|
| `081a` | US1 + the shared core: owner doc § Feature Status / Verification Vocabulary / Gates / Closure Verdict (with extension points for the 081b/081c sections, including § Inherited Blockers), `closure-acceptance-check.py`, seven fixture sets, state machine, verification template, implement wiring, checker at the implement call site, `validate-requirements.py` `path-marker`, the 081a contract modules (`test_closure_acceptance_check.py`, `test_acceptance_state_machine.py`, `test_gate_wiring_081.py`, the extended `test_requirements_checker.py`), the smoke module, `tests/fixtures/` registration in the instructions § Key Directories, and the slice-close set-level baseline comparison | ~14 | — |
| `081b` | US2: runtime-stack table (§ requirements, including the three `in-scope` obligations), Execution Premises + Inherited Blockers (§ plan + the two table skeletons in `templates/plan-template.md`, no domains), the four `pre-analyze-check.py` findings **plus** the absorbed `in-scope` task/joint-acceptance checks and the `inherited` carrier check, `expression-gates.md` rows, A13 boundary. Its row set MUST name **`tests/contract/test_acceptance_premises.py`** — the single test carrier for the four findings and for the carrier/obligation checks (SC-005) — and MUST contain a row that lands the carrier check | ~10 | 081a (owner doc sections) |
| `081c` | US3: `review-feature-quality` skill, review-template slots, `review.md` composition rewrite, ARC, census 3→4 + guards, checker at the review call site, the expected-artifact denominator (FR-013). Its row set MUST name **`tests/contract/test_acceptance_review_composition.py`**, the deliberate update of **`tests/contract/test_review_code_composition.py`** and **`tests/contract/test_status_gate_owner.py`**, and **`templates/commands/checklist.md`** (owner pointer only, no criteria copy) | ~12 | 081a (counts come from the checker) |
| `081d` | US4 + all remaining wiring: three vocabulary owners, `--audit-existing`, driver line state `blocked` (A6 items 1–8) + closure/merge call site, mirrors/regen, docs/CHANGELOG. Its row set MUST name **`tests/contract/test_line_state_blocked.py`** (the single carrier pinning A6's eight dispositions), **`tests/contract/test_acceptance_schema_ownership.py`**, the final sweep of **`tests/contract/test_status_gate_owner.py`** and **`templates/commands/checklist.md`**, and the feature-level id-level baseline re-run | ~16 | 081a (checker), 081c (composition text) |

`/speckit.tasks` MAY keep a single 52-row list if its own decomposition check accepts it; the four boundaries above are the pre-declared fallback and they preserve the 25 FR / 9 SC set intact (requirements § Decomposition & Ceiling).

## Complexity Tracking

N/A — the Constitution Check has no Fail and no Partial row; no violation needs justification.

## Phase 0: Research Review

Research is recorded as a standalone file because it exceeds the inline threshold and carries external/environmental measurement: [`research.md`](./research.md) § R1–R9. The four decisions that came out of it: the runner repair route (R1), the `specify init` enabler (R2, T-005), the closed verdict surface of the `Path` marker (R4 → validator check + checker input error), and the driver landing points with the one measured interaction between A6 item 6 and the "entering `active`" guard (R6).

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed; every count below was produced by running the command shown, not from memory.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | see the file's entity census (E-entities + validation rules + state transitions) |
| Contracts | [`contracts/`](./contracts/) | five files: `closure-acceptance-check.contract.md`, `state-vocabulary.contract.md`, `artifact-schemas.contract.md`, `review-composition.contract.md`, `gate-wiring.contract.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | executable scenarios, each row carrying its execution status and premises |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 081 binding + delivery surface |
