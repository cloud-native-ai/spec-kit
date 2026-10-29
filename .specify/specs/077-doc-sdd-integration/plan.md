# Implementation Plan: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Branch**: `077-doc-sdd-integration` | **Date**: 2026-10-30 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `077-doc-sdd-integration` → Feature 077 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）
**Input**: Specification from `.specify/specs/077-doc-sdd-integration/requirements.md`

## Summary

把「类别可查」变成「类别被读取并改变门禁算子集」。三件事互为支撑：

1. **特性级类别**：`requirements.md` 头部一行 `**Flow Class**: <值>`，经既有唯一引擎
   `flow-class-check.py --action lookup` 的**新键族** `spec:<spec 目录名>` 解析（同形记录、退出码三段
   0/1/2、作者错误与机制缺席分离、不写逐流程台账）。
2. **七个阶段命令按类切换**：`requirements` / `clarify` / `plan` / `tasks` / `checklist` / `analyze` /
   `implement` 七个模板各新增**一个子节**——一次 lookup、两条 owner 指针、一个两分支句、一条降级可见句；
   执行类剥离该子节后与基线提交 `c1cd4600` **逐字相同**（可复算的零行为变化）。
3. **文档结构与逻辑硬约束 + 驱动接入**：表达类 `plan.md` 的 `## Document Structure` 四子节由
   `doc-consistency-check.py` 的**新动作** `--action structure` 校验（不新增第七面）；`sdd-loop-driver`
   的派发载荷携带类别四元组、U4 增补四项 blocking 校验、两槽位换成两个文档门禁槽位
   （`selection_basis=docs-gate-full`，时点与审计口径不变）。

交付面 = 7 个命令模板子节 + 1 个模板字段行 + 1 个 plan 模板的结构骨架（`## Document Structure` 四子节，判定侧的「可达一侧」）+ 2 份 owner 的类条件追加 + 2 个既有引擎的扩展（1 个键族、
1 个动作）+ 3 份驱动 references 的类别分支 + 5 个新测试文件 + 1 个既有闭合集测试的名册修订。
零新命令、零新门禁面、零新存储、零常驻进程、零第三方依赖。25 条 FR / 8 条 SC / 4 个用户故事。

## Technical Context

**Language/Version**: Markdown 规范面（模板 / owner / 驱动 references）+ Python ≥3.8 仅标准库（两个引擎的扩展）；测试为仓库既有 pytest 契约层
**Primary Dependencies**: 既有 `scripts/python/flow-class-check.py`、`scripts/python/doc-consistency-check.py`、`sync-mirrors.py`、`regen-command-copies.py`、`skills/external/sdd-loop-driver/scripts/audit-test-budget.py`（**不改**）；**不新增**任何第三方依赖、不引入网络或模型 API
**Storage**: N/A——声明行落既有 `requirements.md` 头部；结构基线落既有 spec 目录的命名面（`<spec-dir>/structure-baseline.txt`，由 `--freeze` 打印、脚本不写文件）；槽位落既有状态脊围栏；门禁输出落既有 `test-evidence/`
**Testing**: Tests Mode **ON**。五个新测试文件 red-first 写在实现之前（对象见 `research.md` R-10）；plan 期定向基线 = 14 个既有测试文件 **1015 passed**（`test-evidence/plan-targeted-tests-baseline.txt`）
**Target Platform**: 仓库工具链（macOS 与 Linux），Python ≥3.8；两个引擎扩展均为只读、无常驻、无平台分支
**Project Type**: 框架源（两顶帽子：改动落 `templates/`、`shared/`、`skills/`、`scripts/`；`.specify/` 副本与 per-tool 命令副本经既有再生成机制产出——副本套数以 `regen-command-copies.py` 实际产出的目标目录为准，注册表最多六个、本仓当前四个；`tests/` 无镜像）
**Performance Goals**: 单次解析为「读一份 `requirements.md` 头部 + 正则匹配」，单次结构校验为一次线性扫描；无递归全仓遍历、无轮询、无后台进程
**Constraints**: 解析退出码封闭三段（0/1/2，另加一个退出码 0 的 advisory 码 `declaration-absent`）；结构 finding 码集封闭四族；模板子节 MUST NOT 出现 `G-` 算子 id、face id 表、`flow_class=` 赋值形与任何白名单；`--faces` 四面取值集与六面 owner 不变；`templates/commands/**` 不入 templates 镜像对；确认门预算零整数余量（实测 blocking gates 27），子节措辞 MUST NOT 新增阻断式确认句，且该预算按 requirements FR-022 在改动前后各测一次计数相等
**Scale/Scope**: 7 个模板子节；1 个模板字段 + 1 个 plan 模板结构骨架；2 份 owner 类条件追加；2 个引擎扩展；3 份驱动 references；6 份契约（77 条款）；5 个测试文件 + 1 个测试名册修订；镜像对以 `requirements.md` 的接线面与本节 Mirror Obligations 为准（行数不在本行重复）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，共 18 项；同作者降级说明见本节末）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | Pass | `feature-ref.md` 把 25 条 FR 逐条映射到设计落点与契约；每个形制取舍在 `research.md` R-1…R-13 有理由；执行类零变化的判据是「与基线提交逐字相同」，不是印象 |
| II | Feature-Centric Development | Pass | 绑定 Feature 077（requirements 阶段已登记）；本 plan 只推进到 `Planned`，不新建/合并/废弃 Feature；索引行与详情文件在同一次提交内更新（`feature-ref.md` § 绑定关系） |
| III | Intent-Driven Development | Pass | 先定「类别在哪声明、由谁读、读一次还是两次、作者写错和引擎缺席怎么分开」，再定形态；三条真实取舍以 DTR 形式留下反面与代价（`## Decision Tensions`） |
| IV | Test-First & Contract-Driven Implementation | Pass | Tests Mode ON；五个测试文件按红先行写，起点都是本次实测的红（`spec:` 键退出码 2、`--action structure` 退出码 2、七模板零命中）；负样本只留在测试里 |
| V | AI Agent Integration Standards | Pass | 不改 `AGENT_CONFIG` / `_ASSISTANT_TIERS`、不改 provider 配置；六个 per-tool 命令副本由 `regen-command-copies.py` 产出，不新增任何工具面 |
| VI | Continuous Quality & Observability | Pass | 判定全走退出码与既有 `[label] pass/fail (count)` 形态；本阶段证据按执行时全量捕获写入 `test-evidence/`（13 份）；不以「命令退出码 0」替代「相对基线无新增漂移」；不产生 `.bak` 类副本 |
| VII | Specification-Plan-Task-Implementation Workflow | Pass | reuse-first 已在 requirements § Related Feature 逐条核验八个候选；本阶段不落 `Implemented`；`[ ]` 任务与 SC 状态行的 Pre-Status-Flip Gate 留给 `/speckit.implement`；表达类 implement 的 Test-First 按 template-only 条款判 `Partial (justified)`（`contracts/document-structure.md` C-019） |
| VIII | Code as the Single Source of Truth | Pass | 现状以实测校准规格：`--action structure` 不存在、`spec:` 键退出码 2、七模板零命中、审计对 `selection_basis` 不做枚举校验；四处都在 `research.md` 有原始输出，未凭记忆断言 |
| IX | Framework Scope Discipline (No Over-Engineering) | Pass | 全部能力落在既有文件的扩展点（一个键族、一个动作、三份 references 的分支），无新服务、无调度器、无评分器、无第二份台账（`contracts/invariants-and-distribution.md` C-001…C-003） |
| X | Documentation Naming & Location Conventions | Pass | 新文件走既有命名面：`tests/unit/test_flow_class_spec_key.py`、`tests/contract/test_*_*.py`；spec 目录内 `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md` 为既有约定；不改动任何保留文件名 |
| XI | Dogfooding (Self-Application) | Pass | 改动落框架源侧，`.specify/` 副本与命令副本经既有机制产出；本线自身走完整阶段链，并在 requirements 头部先行自用该字段（`requirements.md` 第 6 行） |
| XII | Tool Reuse Over Ad-Hoc Generation | Pass | 复用两个既有引擎、`sync-mirrors.py`、`regen-command-copies.py`、`audit-test-budget.py`（明确不改）与 `clause_extract.py` 的判定；`.specify/memory/tools/` 无「特性线类别解析」同能力记录，扩展既有引擎正是预期结果 |
| XIII | Better-Harness Orientation (Improvement North Star) | Pass | 强化 Task Understanding（类别在链上第一个阶段可读）与 Change Validation（门禁证据成为 U4 放行前置，`contracts/driver-integration.md` C-004）；证据区分「程序判决」与「复核者判断」，不把 configured 当 used |
| XIV | One Source of Truth (Authority & Reference Discipline) | Pass | 判据归分类 owner、算子与降级归门禁 owner、槽位归 efficiency-model §2、证据四键归 `verification-log-template.md`；七模板子节只出现 lookup 调用与两条指针，零表副本（`contracts/stage-wiring.md` C-003） |
| XV | User-Facing Comprehension (No-Jargon, With Context) | Pass | 七模板子节面向未参与本轮的维护者：分支句用语义措辞（表达类 / 执行类）、降级句写「显示标签并保持既有门禁集」而非内部键名；`data-model.md` 每个实体给出承载位置与判定器 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | Pass | 作者输入错误（四个声明码）与机制缺席（退出码 2）分离且都可见，不得静默回落（`contracts/class-resolution.md` C-006/C-007）；七模板接线会让闭合集守卫转红，已用 mutation 实证并列入同一改动（`research.md` R-8） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | Pass | 不新建目录：新文件落在既有 `tests/unit/`、`tests/contract/`、`scripts/python/`、`skills/external/sdd-loop-driver/references/`；plan 期临时夹具落 `.specify/.tmp/`（`.specify/.gitignore` 已忽略，实测 `git check-ignore` 命中） |
| XVIII | Grounded Naming | Pass | 命名取兄弟先例：键族 `spec:<dir>` 与既有 `/speckit.<stem>` / `skill:<dir>` 同族；动作名 `--action structure` 与既有 `--action verify|check|lookup` 同形；基线文件名 `structure-baseline.txt` 与 `coverage-baseline.txt` 同面；测试名 `test_<subject>.py` |

**Gates Status**: 全部 18 项 Pass，无 Fail / Partial；`## Complexity Tracking` 记 N/A。

**Re-check after Phase 1**: 2026-10-30——Phase 1 产物（`data-model.md`、6 份契约、`quickstart.md`、
`feature-ref.md`）落盘后复核：18 项维持 Pass；新增证据为 6 份契约全部 `md-bold-closed` / 77 条款、
FR 车道 `FR uncovered: 0`、镜像与命令副本相对基线零新增漂移。复核未发现需要 Partial 的行，
故 Complexity Tracking 仍为 N/A。

**Same-author gate**（`.specify/shared/workflow/objective-analysis-gate.md`）：本 run 从 requirements 到 plan
无断点，被评分的工件由本 agent 在本会话内产出，按该 owner 应委派新鲜上下文只读子代理。本执行环境未向
执行 agent 暴露子代理派发工具（工具面只有文件读写、检索与命令执行），按该 owner §7 的
subagent-unavailable 降级形态，本表与「Post-Generation Quality Gate」均走直接受限读，标记为
**(detected: direct read, subagent unavailable)**——逐行自我评分，可信度低于委派路径，读者应据此折算权重。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository
root. This section lists the field names and points at that file; it does not restate the criteria
table, the rejection list or the threshold table.*

### T-001 — 类别声明落在规格头部，而不是特性索引加一列

- **decision**: 类别只声明在 `requirements.md` 头部的一行字段上，`.specify/memory/features.md` 不新增类别列。
- **antithesis**: 在特性索引宽表上加一列 `flow_class`（或写进 `features/<ID>.md` 的 frontmatter），注册表即成类别的唯一视图；当一个 Feature 恰对应一条规格线、且维护者已习惯「先开索引再开规格」时它更优——一次查表就能看到全仓类别分布，不必逐目录打开文件。
- **binding_constraints**:
  - pole_a: 类别必须在该线第一个阶段的第一次门禁判定之前可读，否则第一个阶段就在错误的算子集下跑完再翻转。
  - pole_b: 类别必须能一表纵览全部特性线，否则跨线审计要逐目录解析、无法回答「全仓有哪几条表达类线」。
- **discriminating_evidence**: 在基线提交上构造同一 Feature 下的两条切片夹具（`069a-` 声明执行、`069b-` 声明表达），只按索引列回答「切片 B 该跑哪套门禁」；结果二值——索引列给出的取值与切片 B 自己声明行一致（是／否）。索引列版本必然答「否」，因为它只有一格。
- **expected_sacrifice**: SC-001 Source ↓ 类别分布无法一张表看完，跨线审计必须逐线调用解析入口，单次全仓盘点从「读一列」变成「逐目录跑一次命令」。
- **revision_trigger**: 两个迭代内出现 ≥2 次「需要一次列出全仓所有表达类线」的重复诉求 → 重开，改为「注册表只留指针 + 由解析引擎派生的视图」，且派生视图 MUST NOT 手写。

### T-002 — 扩既有引擎的键族，而不是新建一个特性线解析器

- **decision**: 特性级类别复用 `scripts/python/flow-class-check.py --action lookup`，以新增键族 `spec:<spec 目录名>` 表达。
- **antithesis**: 新建 `scripts/python/flow-class-spec-check.py` 专管特性线声明，与台账引擎互不引用；当「台账守卫的失败面与阶段命令的读取面需要各自独立的发布节奏、且一处 owner 解析失败不该牵动另一条链」时它更优——两个引擎可各自测试、各自降级，台账守卫的红不会让七个阶段同时拿不到类别。
- **binding_constraints**:
  - pole_a: 类别只能有一条读取路径；两条路径就是两份判据，迟早在默认标记或退出码语义上分叉。
  - pole_b: 台账守卫（79 行对账）与阶段解析必须能各自失败——台账里的一处格式错误不该让七个阶段的读取一起降级。
- **discriminating_evidence**: 在仓库的临时副本里移走 `scripts/python/flow-class-check.py`，然后只凭仓库内剩下的文件尝试解析一条特性线的类别；结果二值——还能解析出来（是／否）。若答案是「是」，说明仓库里存在第二条读取路径。
- **expected_sacrifice**: SC-002 Source ↓ 台账守卫与阶段解析共用一个进程：owner 不可解析时七个阶段的读取一起降级（标签可见、门禁集不变，但无法只让阶段命令降级）。
- **revision_trigger**: 两个迭代内出现 ≥2 次「台账守卫红导致七个阶段都拿不到类别」且降级标签被误读为通过 → 重开，拆出只读子模块，但必须共用同一解析函数与同一 owner 解析顺序。

### T-003 — 结构校验落既有检查器的新动作，而不是新建结构检查器

- **decision**: `## Document Structure` 的校验落 `scripts/python/doc-consistency-check.py` 的新增动作 `--action structure`，不新建检查器、不新增门禁面。
- **antithesis**: 新建 `scripts/python/docs-structure-check.py` 专管四子节与章节两向比对；当「结构面的判定对象（一份 plan 的章节树）与四面判定对象（落文文档）会由不同特性长期演进、且两个 CLI 的取值集不应互相牵制」时它更优——结构面可以独立扩码、独立改退出码，`--faces` 的封闭语义也不会因为多了一个动作而变得含混。
- **binding_constraints**:
  - pole_a: 读者标记、证据三件套与副本下限这套语法只能有一份实现，两份实现必然在正则与窗口上漂移。
  - pole_b: 每个判定面的命令行契约必须能独立演进：一个面的参数或退出码变更不得牵动另一个面。
- **discriminating_evidence**: 把证据三件套里 `as-of` 的识别正则收紧一个字符，然后分别跑四面动作与结构动作，数「需要改动的实现文件数」；结果二值——同一处改动即可让两者同时生效（是／否）。共用实现答「是」，双实现答「否」。
- **expected_sacrifice**: SC-004 Source ↓ 结构动作的 `--action` 取值集与四面共用同一个 CLI，`--faces` 的封闭性从此多了一个需要复核的邻面，每新增一个动作都要多走一道「有没有动到四面域」的检查。
- **revision_trigger**: 两个迭代内出现 ≥2 次「结构动作的改动被迫修改四面解析路径」，或 `--faces` 的封闭性被误扩 → 重开，把结构判定拆成共用语法层的子模块，但命令行入口仍保持单一。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/077-doc-sdd-integration/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — 13 条形制裁决 + 实测基线 + 3 条披露
├── data-model.md        # Phase 1 output — 9 个实体（E1…E9）与校验规则汇总
├── quickstart.md        # Phase 1 output — 7 个场景（S1…S7，含清理）
├── contracts/           # Phase 1 output — 6 份契约 / 77 条款
│   ├── class-declaration.md
│   ├── class-resolution.md
│   ├── stage-wiring.md
│   ├── document-structure.md
│   ├── driver-integration.md
│   └── invariants-and-distribution.md
├── feature-ref.md       # Phase 1 output — 25 条 FR → 设计落点 + 8 条 SC → 证据来源
├── checklists/          # requirements 阶段的 16 项质量清单
├── test-evidence/       # 本阶段 13 份全量捕获（见 Phase 1 表的 Evidence 行）
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement)
```

### Source Code (repository root)

```text
templates/commands/                          # 七个阶段模板各新增一个接线子节（docs / humanize 不动）
templates/requirements-template.md           # 头部新增 **Flow Class** 字段行（Status 之后、Input 之前）
templates/plan-template.md                   # 新增 `## Document Structure` 四子节骨架（表达类必要产出、执行类非必填）
shared/definitions/flow-class-definitions.md # 类条件追加：特性线声明面与 `spec:` 键的消费方指针
shared/workflow/expression-gates.md          # 类条件追加：特性线调用点行（六面与算子表不动）
scripts/python/flow-class-check.py           # 扩展 `spec:` 键族 + 四个作者错误码 + 三段退出码
scripts/python/doc-consistency-check.py      # 扩展 `--action structure`（--faces 四面不变）
skills/external/sdd-loop-driver/SKILL.md     # 类别感知落点（指针 + Hard Requirement 的类别分支）
skills/external/sdd-loop-driver/references/stage-prompts.md    # 第①段类别四元组 + U4 四项
skills/external/sdd-loop-driver/references/efficiency-model.md # §2 槽位内容的类别分支（时点与审计不变）
tests/unit/test_flow_class_spec_key.py                        # 新建（red-first）
tests/contract/test_flow_class_spec_declaration.py            # 新建（red-first）
tests/contract/test_stage_class_wiring.py                     # 新建（red-first）
tests/contract/test_document_structure_gate.py                # 新建（red-first）
tests/contract/test_docs_gate_driver.py                       # 新建（red-first）
tests/contract/test_expression_gate_wiring.py                 # 改写：闭合集名册并入七模板，分母不变
.specify/specs/077-doc-sdd-integration/      # 本特性 plan 与设计产物（不含实现代码）
```

**Structure Decision**: 本特性是**框架源的接线扩展**，不是新组件：七个命令模板加子节、plan 模板加结构骨架、两份 owner 加类条件段落、
两个既有引擎各加一个扩展点、三份驱动 references 加类别分支。唯一的「新增能力」是特性线声明这一对象族，
它没有自己的存储——声明就是规格文件里的一行。两顶帽子明确：编辑面是 `templates/`、`shared/`、`skills/`、
`scripts/`、`tests/`；`.specify/` 下的同名文件与 per-tool 命令副本一律由 `sync-mirrors.py` /
`regen-command-copies.py` 产出，MUST NOT 手改。

### Mirror Obligations

镜像对清单的 owner 是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对）；本节按其行序登记本次受影响的四对
与命令副本面（第 1 行现有两个文件：requirements 模板的字段行与 plan 模板的结构骨架）。**基线**：改动前实测 `sync-mirrors.py --check` 退出码 0、六对全 `ok`
（skills/external 406 / skills/internal 136 / agents 3 / scripts 117 / shared 60 文件，templates 对同 `ok`），
`regen-command-copies.py --check` 同样退出码 0；原始输出见 `test-evidence/plan-sync-mirrors-baseline.txt` 与
`test-evidence/plan-regen-command-copies-baseline.txt`。

| # | Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|---|----------------------|---------------------------------------------------|--------|
| 1 | `templates/requirements-template.md`、`templates/plan-template.md` | `.specify/templates/requirements-template.md`、`.specify/templates/plan-template.md` | 改动后跑 `sync-mirrors.py --check`，判据为「templates 对相对上述基线无新增漂移」，不以单一退出码作判据 |
| 2 | `templates/commands/{requirements,clarify,plan,tasks,checklist,analyze,implement}.md` | **无 templates 镜像**（`commands` 在 MIRROR_PAIRS 的排除集内）；per-tool 副本由 `regen-command-copies.py` 产出——注册表 `_ASSISTANT_COMMAND_DIRS` 最多六个目标，但只为**本仓已存在**的目录产出，本仓当前四个：`.claude/commands/speckit.<stem>.md`、`.github/prompts/speckit.<stem>.prompt.md`、`.opencode/command/speckit.<stem>.md`、`.qoder/commands/speckit.<stem>.md`（`.codex` / `.hermes` 目录不存在，故不产出） | 改动后跑 `regen-command-copies.py --check`，判据为「副本集合相对基线无新增漂移」且**每个实际产出的副本**含接线子节（契约测试断言；套数由脚本实测，不写死） |
| 3 | `shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md` | `.specify/shared/definitions/…`、`.specify/shared/workflow/…` | 同 #1（shared 对） |
| 4 | `scripts/python/flow-class-check.py`、`scripts/python/doc-consistency-check.py` | `.specify/scripts/python/…` 同名两份 | 同 #1（scripts 对） |
| 5 | `skills/external/sdd-loop-driver/{SKILL.md,references/stage-prompts.md,references/efficiency-model.md}` | `.specify/skills/sdd-loop-driver/…`（skills/external 对的 `external` 层展开） | 同 #1（skills/external 对） |

**无镜像面**：`tests/**` 不入任何镜像对；`.specify/specs/077-doc-sdd-integration/**` 是规格产物、不是分发载荷
（`.specify/specs/` 不在 `MIRROR_PAIRS` 内），只做源文件改动。

## Complexity Tracking

N/A——Constitution Check 18 项全部 Pass，无 Fail / Partial 行需要理由。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 9 entities（E1 声明行 / E2 解析记录 / E3 声明发现 / E4 接线卡 / E5 结构产物 / E6 结构违规 / E7 算子结果 / E8 槽位行 / E9 派发载荷）+ 校验规则汇总（行数以该文件 § 校验规则汇总 的实测为准，本表不复述计数） |
| Contracts | [`contracts/`](contracts/) | 6 files：`class-declaration.md`(13) / `class-resolution.md`(12) / `stage-wiring.md`(13) / `document-structure.md`(19) / `driver-integration.md`(11) / `invariants-and-distribution.md`(9) = **77 条款**，全部 `md-bold-closed`（`clause_extract.py` 实测，`test-evidence/plan-clause-extract.txt`） |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios（S1 解析 / S2 三例判定 / S3 结构门禁 / S4 接线存在性 / S5 分发漂移 / S6 槽位审计 / S7 清理）；S1–S6 六个场景的「今天实测」输出均为本次会话跑出，实施后的期望值一律由各场景的 Pinned by 指名的测试负责 |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 25 条 FR → 设计落点 + 8 条 SC → 证据来源 |
| Evidence | `test-evidence/` | 本阶段新增 13 份：探针 7 份（`plan-resolution-baseline.txt`、`plan-stage-template-zero-hit.txt`、`plan-sync-mirrors-baseline.txt`、`plan-regen-command-copies-baseline.txt`、`plan-targeted-tests-baseline.txt`、`plan-audit-test-budget-docs-gate-probe.txt`、`plan-a6-mutation-probe.txt`）+ 门证据 3 份（`plan-clause-extract.txt`、`plan-account-clause-coverage.txt`、`plan-scan-confirmation-gates.txt`）+ 阶段门 3 份（`plan-pre-analyze-check.txt`、`plan-decision-tensions.txt`、`plan-distribution-postcheck.txt`） |

**与 Phase 0 预期的偏差**：预期 6 份契约、实际 6 份；预期「每个 FR 至少被引用一次」的 FR 车道实测
`FR uncovered: 0`（25/25）。条款数（77）在写契约前未预设，是落盘后由 `clause_extract.py` 读出的。

## Plan Edits

*`/speckit.analyze` 修复轮（2026-10-30）对 plan 属主制品的逐行声明。`minor` = 措辞/计数/引用的收紧与更正，不改变已批准的范围与语义读数；`substantive` = 在「两种自洽读法」之间择一、或改变某条已声明义务的边界。所有 substantive 行都对应 analyze 报告点名的冲突簇，修复轮已按调用方派发逐条裁决（裁决记录见 `requirements.md` § Clarifications 的「analyze 修复轮裁决」小节），故未就地停机，而是把选择连同理由登记在此。*

- **PLAN-EDIT**: `requirements.md` — 择一登记三处冲突（FR-001 的作用域收窄为「新增声明线」并新增 advisory 码 `declaration-absent`；FR-017 的「四面」定义为「门禁输出的面」而 U4(a) 取算子表分母；FR-019(b) 降为「存在且非空」、不做哈希），补 FR-005 的 exit-1 停止句、FR-009 的调用方可观察触发、FR-018 的 `error` 位、FR-020 的 `rc` 聚合与 `not-applicable` 单列、FR-022 的确认门计数判据、FR-023 的 `templates/plan-template.md`，并把派生计数改为指针；分类=**substantive**。
- **PLAN-EDIT**: `data-model.md` — E2 字段集统一为九项（原「八项」与其自身 9 行表冲突）、E3 增 `declaration-absent` 与解析顺序变更登记、E4 增停止句与标题字面量指针、E5 增产出侧、E6 码族统一四族并增两个缺节码与落文输入、E7 计数规则与「不新增哈希字段」、E8 `rc` 聚合与 `not-applicable` 单列、E9 四元组；分类=**substantive**。
- **PLAN-EDIT**: `contracts/class-declaration.md` — C-001 作用域 + C-008 缺省两形态 + C-009 阶段侧停止句；分类=**substantive**。
- **PLAN-EDIT**: `contracts/class-resolution.md` — C-004 九项字段、C-006 补 `declaration-absent`、C-009 登记顺序变更、C-012 调用方可观察触发与降级可表示；分类=**substantive**。
- **PLAN-EDIT**: `contracts/stage-wiring.md` — C-002 标题字面量的登记处指向 R-9、C-003 增停止句、C-007 钉死剥离算法与块末单空行、C-012 接线面加 `templates/plan-template.md`、C-013 守卫同时断言子节在场；分类=**substantive**。
- **PLAN-EDIT**: `contracts/document-structure.md` — C-001 缺节码与产出侧、C-008 落文输入复用 `--path`、C-013 四族与术语消歧、C-017 四面读法与结构子步、C-019 结构绿内容红实例；分类=**substantive**。
- **PLAN-EDIT**: `contracts/driver-integration.md` — C-001 四元组、C-004(a)(b)(c) 三项重写、C-006 `rc` 聚合、C-007 `not-applicable` 单列与计数等式；分类=**substantive**。
- **PLAN-EDIT**: `contracts/invariants-and-distribution.md` — C-005 副本套数改为「以脚本实测为准、不写死」；分类=minor。
- **PLAN-EDIT**: `research.md` — R-9 增子节标题的唯一登记处与剥离算法、可复算样例（原「到下一个 `##` 或 `###` 为止」不足以让两个实现者算出同一字节）；分类=**substantive**。
- **PLAN-EDIT**: `research.md` — 更正偏差 #2 的 freeze 判断：`coverage-baseline.txt` **已**由 tasks 阶段按 77 条款认领冻结，clause 车道实测 `status: ok` / `beyond baseline=0`，原「不冻结 / 设计内红」不再成立（保留原判断并标注更正时点）；分类=minor。
- **PLAN-EDIT**: `research.md` — R-3 字段数 8→9、R-5 `rc`/`not-applicable`、R-6 四元组与 (b)、R-7/R-11 副本套数去数字、R-12 确认门判据可判定化、R-4 四面→四族；分类=minor。
- **PLAN-EDIT**: `quickstart.md` — S2/S3 的期望值补 `declaration-absent` 与 `two-way: not-run`、S5 的副本套数改为按实测、S6 的槽位计数补 `not-applicable` 单列；分类=minor。
- **PLAN-EDIT**: `feature-ref.md` — 25 条 FR 的设计落点列按上述改动回填（不增删 FR 行）；分类=minor。
- **PLAN-EDIT**: `checklists/readiness-2026-10-30.md` — 追加「修复轮处置」表，并更正 CHK039 的「没有任何门会响」这一表述（该缺口已由 FR-022 + T021 承接）；分类=minor。
- **PLAN-EDIT**: `checklists/requirements.md` — 派生计数（shared strings 等）改为按 `validate-requirements.py` 输出取值，不再写死；分类=minor。

**非 plan 属主制品**：`tasks.md` 的改动（T001…T028，任务行 27→28）属 tasks 阶段产物，不在此登记；`coverage-baseline.txt` 未改动（条款认领仍为 77，无需重冻结）。

### 修复轮 2（analyze #2，2026-10-30）

*第二轮 analyze（HEAD `6217a86f`）判 BLOCKED：1 HIGH + 6 MEDIUM + 5 LOW。本轮为 spec-only 修复，计数不变（25 FR / 8 SC / 77 条款 / 6 STR / 28 任务），`coverage-baseline.txt` 不重冻结，`shared/workflow/expression-gates.md` 与 `shared/definitions/flow-class-definitions.md` 不动。*

- **PLAN-EDIT**: `requirements.md` — R-01 取「构建并入单条结果」支（FR-019(a) 把站点构建登记为 `G-implement-structure` 的 `face=build` 子行；FR-020 删除「算子总数 − (passed+failed) = NA 条数」跨级等式；SC-003 的 NA 断言改为面级）；R-02 收窄载荷 `error` 值域为 `{owner-unavailable, -}`（FR-018 / FR-019(c)）；LOW 组：FR-001 补「引擎不可判存量/新增，`declaration-absent` 仅 advisory，新线漏声明归 plan/tasks 阶段检查」、FR-013 补缺节优先级；R-05 更正确认门脚本路径；R-03 更正 Clarifications 第 6 条并加带日期注记；分类=**substantive**（NA 计量单位与 `error` 值域各改变一条已声明义务的边界）。
- **PLAN-EDIT**: `data-model.md` — E1 行数统一为「至多一行（缺省合法）」；E6 增 `document-structure-missing` 优先于 `subsection-missing`；E7 增算子级行/子行二分（`face_scope` 三值、NA 只在子行）、重写计数规则；E8 计数口径去跨级等式；E9 `error` 值域收窄；校验规则汇总同步；分类=**substantive**。
- **PLAN-EDIT**: `contracts/driver-integration.md` — C-001 `error` 值域；C-004(a) 补子行、C-004(c) 补值域；C-007 重写为「算子级行数 = `passed`+`failed`，NA 面级单列、不设跨级等式」；分类=**substantive**。
- **PLAN-EDIT**: `contracts/class-resolution.md` — C-012 的载荷示例由 `error=<label>` 收窄为 `error=owner-unavailable` 并注明值域；分类=minor。
- **PLAN-EDIT**: `contracts/stage-wiring.md` — C-007 补「块内任何同级或更高级标题（含 `###`）一律视为块结束」；分类=minor。
- **PLAN-EDIT**: `contracts/document-structure.md` — C-001 补「父子同因只报一次」（整章缺失抑制四条 `subsection-missing`）、C-017 ③ 把站点构建改写为 `G-implement-structure` 的 `face=build` 面级子行；分类=minor。
- **PLAN-EDIT**: `research.md` — R-5 计数口径去跨级等式、R-6 `error` 值域、R-7 子节字面量改为指向 R-9 的指针（不重抄、不引带后缀标题）、R-9 补块内标题纪律；分类=minor。
- **PLAN-EDIT**: `quickstart.md` — S6 的计数读法改为「算子级 `passed`/`failed` + `build` 子行面级单列，不用跨级等式反推」；分类=minor。
- **PLAN-EDIT**: `checklists/readiness-2026-10-30.md` — 追加「修复轮处置」第 20–29 行（R-01…R-07 与 5 条 LOW），使表共 29 行、29/29 可复核；分类=minor。

**本轮非 plan 属主制品**：`tasks.md` 的 T016/T017/T019/T021/T028 修订属 tasks 阶段产物；`.specify/memory/features.md` 077 行与 `.specify/memory/features/077.md` 的阶段记录属 Feature 登记面——均不在本表登记。
