# Implementation Plan: 决策反题与反指标契约（Decision Tension Record）

**Branch**: `076-decision-tension-contract` | **Date**: 2026-10-29 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `076-decision-tension-contract` → Feature 076 决策反题与反指标契约（Decision Tension Record）
**Input**: Specification from `.specify/specs/076-decision-tension-contract/requirements.md`

## Summary

在计划阶段为承重决策建立可判定的反题契约：新建 owner `shared/guidelines/decision-tension.md`
（六字段 + `tension_id`，可采纳判据、拒绝形态、承重门槛、相邻边界各自只在此定义），在
`templates/plan-template.md` 的 `## Constitution Check` 直接后继处加 `## Decision Tensions`，
在 `/speckit.analyze` 的检测面加一条结构性通道（缺记录 / 六字段不全 / 代价不可映射 → HIGH，
无 advisory 档），并以两个只用标准库的确定性校验器判决 `scripts/python/validate-decision-tensions.py`
与 `scripts/python/validate-falsification-quartet.py`；同时把 SI-3C 的证伪尝试升级为封闭四元组
（`attempt` / `exit_code` / `observation` / `would_go_red_if`），由脚本判决、接收方不得反向覆盖。

交付面 = 1 份新 owner 文档 + 1 份既有 owner 改写（只增不改）+ 1 份工作流步骤的指针形核验（现状已无复述，本特性只加守卫断言并留证）+ 1 个模板章节 + 1 条分析通道
（`detection-and-severity.md` 的通道小节与其计数标题；`SKILL.md` 的枚举句同步更新）+ 1 个 ADR
引用位 + 2 个校验器 + 3 个契约测试文件。8 份契约共 34 条条款，FR 车道 26/26 全覆盖。零新命令、
零新存储、零常驻进程、零第三方依赖、零模型调用。

**本计划自身是 DTR 的首个实例**：下文 `## Decision Tensions` 的两条记录（`T-001`、`T-002`）是
手工试点，同时充当实现期的首个夹具；它们用未来校验器将要解析的同一文法书写。

## Technical Context

**Language/Version**: Markdown 规范面（owner / 模板 / 通道 / ADR 模板）+ Python ≥3.8 仅标准库（两个校验器）；测试为仓库既有 pytest 契约层
**Primary Dependencies**: 既有 `scripts/python/sync-mirrors.py`、`scripts/python/regen-command-copies.py`、`scripts/python/clause_extract.py`、既有 `pytest`；**不新增**任何第三方依赖、不引入网络或模型 API
**Storage**: N/A——张力记录搭在 `plan.md` 工件上；四元组搭在 SI-4 派发载荷与 SI-7 intervention 记录上；判定结果只进既有 analyze 报告与计划文本
**Testing**: Tests Mode **ON**。三个新契约测试文件按 red-first 写在实现之前：`test_decision_tension_contract.py`（owner / 模板锚点 / 通道 / ADR 槽位 / 镜像 / 术语 / 闭合面）、`test_decision_tension_validator.py`（六标签、退出码、正样本 + 六个反向输入，含逐字段删除与 `tension_id` 跳号）、`test_falsification_quartet_validator.py`（一个合规载荷 + 六类拒收 + 退出码 0/1/2）。plan 期定向测试基线：五个既有契约测试文件 70 passed
**Target Platform**: 仓库工具链（macOS 与 Linux），Python ≥3.8；校验器只读、无常驻、无平台分支
**Project Type**: 框架源（两顶帽子：改动落 `shared/`、`templates/`、`skills/internal/`、`scripts/`、`docs/`，`.specify/` 副本经 `sync-mirrors.py` 同步；`tests/` 与 `docs/decisions/` 无镜像）
**Performance Goals**: 单份计划的校验为一次线性扫描，无递归全仓遍历（检测范围只有 `REQUIREMENTS_DIR/plan.md`）；无轮询、无后台进程；不新增任何运行期等待
**Constraints**: 校验器只读、只用标准库、退出码 0/1/2；标签封闭六项、拒收原因封闭六值；`expected_sacrifice` 只有一个解析形态；通道取值只有 HIGH 与 0；不改动既有通道 A–H 的判据；`templates/commands/**` 不动
**Scale/Scope**: 1 份新 owner；1 份既有 owner 只增不改 + 1 份工作流步骤核验；1 个模板章节；1 条分析通道 + 2 处计数行；1 个 ADR 槽位；2 个校验器；8 份契约（34 条款）；3 个契约测试文件；镜像对以 `requirements.md` FR-025 的表为准（行数不在本行重复）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，共 18 项；同作者门见下方说明）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | Pass | `feature-ref.md` 逐条把 26 条 FR 映射到设计落点与契约；每个技术取舍在 `research.md` R-1…R-11 有理由与被否决读法；本 plan 的两条 DTR 即「决策可追溯到需求」自身的实例 |
| II | Feature-Centric Development | Pass | 绑定 Feature 076（已在册，Draft）；本 plan 只推进到 `Planned`，不新建/合并/废弃 Feature；详情文件与索引行在同一次提交内更新（`feature-ref.md` § 绑定关系） |
| III | Intent-Driven Development | Pass | 先定「什么算承重、什么算可采纳、什么时候必须重开」，再给承载形态；两条真实取舍以 DTR 形式留下反面与代价，而非事后追述 |
| IV | Test-First & Contract-Driven Implementation | Pass | Tests Mode ON；两个校验器与其正负样本先写测试后实现（`contracts/validator.md` C-4、`contracts/falsification-quartet.md` C-3）；文档/模板面由契约测试断言锚点、路径可解析、条款不复述（`contracts/plan-template-anchor.md` C-3） |
| V | AI Agent Integration Standards | Pass | 不改动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`、命令模板与任何 provider 配置；`templates/commands/**` 与 `regen-command-copies.py` 的副本面零变化 |
| VI | Continuous Quality & Observability | Pass | 判定全部走退出码与 `[label] pass/fail (count)`；本特性证据按执行时全量捕获写入 `test-evidence/`；不以「命令退出码 0」替代「相对基线无新增漂移」；不产生 `.bak` 类副本 |
| VII | Specification-Plan-Task-Implementation Workflow | Pass | reuse-first 已在 requirements § Related Feature 逐条核验六个候选；本阶段不落 `Implemented`；`[ ]` 任务与 SC 状态行的 Pre-Status-Flip Gate 留给 `/speckit.implement` |
| VIII | Code as the Single Source of Truth | Pass | Phase 0 以实测校准规格：「Constitution Check 之后、Complexity Tracking 之前」不可判定（标题序实测）、通道字母 H 已被 checklist 通道占用、基线提交 `ac63fe8c` 处五个目标文件零漂移（见 `research.md` R-1/R-2/R-7） |
| IX | Framework Scope Discipline (No Over-Engineering) | Pass | 两个校验器是单文件只读脚本，可删除且不留基础设施；四元组不重放 `attempt`（重放会引入执行运行时）；无新服务、无调度、无评分器（`contracts/mirrors-and-scope.md` C-1） |
| X | Documentation Naming & Location Conventions | Pass | 新文件走既有命名面：`shared/guidelines/decision-tension.md`（小写连字符）、`scripts/python/validate-decision-tensions.py`、`tests/contract/test_decision_tension_*.py`；不改动任何保留文件名 |
| XI | Dogfooding (Self-Application) | Pass | 改动落框架源侧，`.specify/` 副本经 `sync-mirrors.py` 产出；本特性自身走完整阶段链，并把 plan 本身作为首个 DTR 实例（机制先在自身生效，再谈分发） |
| XII | Tool Reuse Over Ad-Hoc Generation | Pass | 复用 `sync-mirrors.py`、`regen-command-copies.py`、`clause_extract.py`、`validate-requirements.py` 的输出与退出码先例；`.specify/memory/tools/` 无「张力记录校验」同能力记录，因此编写新脚本正是预期结果 |
| XIII | Better-Harness Orientation (Improvement North Star) | Pass | 强化 Task Understanding（计划期先写反面与代价）与 Change Validation（证伪产物可判红）；证据区分「程序判决」与「复核者判断」，不把 configured 当 used |
| XIV | One Source of Truth (Authority & Reference Discipline) | Pass | 新 owner 声明拥有面，四个消费者以路径引用；模板只放一条指针加字段清单；SI-3C 保留指针不复述；SKILL.md 与 owner 的通道枚举由契约测试钉住（唯一合法的「测试内冻结字面量」形态） |
| XV | User-Facing Comprehension (No Jargon, With Context) | Pass | 对外一律工程词；`requirements.md` A3 的五个内部别名在三棵分发面零命中（plan 期实测，实现后复测，`contracts/mirrors-and-scope.md` C-2）；模板与 owner 的措辞面向未参与本次运行的维护者 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | Pass | 缺章节一律 HIGH（fail-closed），不因「可能没有承重决策」而跳过；负样本必须留在测试里（绿不是证据）；校验器返回 2 与返回 1 语义分离，不把输入错误读成记录不成立 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | Pass | 不新建目录：新文件落在既有的 `shared/guidelines/`、`scripts/python/`、`tests/contract/`、`docs/decisions/`；`test-evidence/` 为既有 spec 目录约定 |
| XVIII | Grounded Naming | Pass | 命名取兄弟先例而非自创：owner 取 `shared/guidelines/<topic>.md`、脚本取 `validate-<artifact>.py`、条款 id 取 `contract-clause-definitions.md` 的规范形态 `C-N`、记录 id 取 `T-NNN` 与需求侧 `SC-NNN` 同族、测试取 `test_<subject>_*.py` |

**Gates Status**: 全部 18 项 Pass，无 Fail / Partial；`## Complexity Tracking` 记 N/A。

**Re-check after Phase 1**: 2026-10-29——Phase 1 产物（`data-model.md`、8 份契约、`quickstart.md`、`feature-ref.md`）落盘后复核：18 项维持 Pass；新增证据为条款形态 8 份 `md-bold-closed` / 34 条款、FR 车道 26/26、镜像六对 `ok`（与 Phase 0 基线一致）。复核未发现需要 Partial 的行，故 Complexity Tracking 仍为 N/A。

**Same-author gate**: 本 run 从 requirements 到 plan 无断点，被评分的工件由本 agent 在本会话内产出，
按 `.specify/shared/workflow/objective-analysis-gate.md` 应委派新鲜上下文只读子代理。本运行环境未向
执行 agent 暴露子代理派发工具（工具面只有文件读写、检索与命令执行），外部 CLI 派发会在一个无人值守
的计划阶段里嵌套一个不受监督的会话，因此按该文件 rule 7 走标记回退：本表 18 行与 Phase 1 复核均为
`(detected: direct read, subagent unavailable)`。该弱化证据路径在此可见，不作为委派路径的等价物。

## Decision Tensions

*本计划的承重决策记录。字段形态、可采纳判据、拒绝形态与承重门槛的 owner 是
`shared/guidelines/decision-tension.md`（实现期创建）；本节只按该形态记录两条真实取舍，不复述判据表。
`expected_sacrifice` 指向 `requirements.md` § Measurement Sources 中已声明的来源。*

### T-001 — 四元组的拒收判定者是确定性脚本，而不是接收方 agent

- **decision**: 证伪四元组的接收/拒收判决由 `scripts/python/validate-falsification-quartet.py` 作出，接收方 agent 只消费判决、不得反向覆盖。
- **antithesis**: 由接收方 agent 按一份「可复现判据清单」判定（清单列出转述、空真、字段缺失的判定要点，要求两位复核者按同一条目比对）；它在「判据需要读语义」时更优——当载荷的 `observation` 是一段真实的转述、而 `would_go_red_if` 用自然语言描述了足够具体的失败场景时，只有能读语义的判定者才能分清合格与不合格。
- **binding_constraints**:
  - pole_a: 同一载荷在任何模型、任何一次运行上必须得到同一 verdict（SC-004 的 6/6 拒收必须可重放），且判决不得被下游反向覆盖。
  - pole_b: 语义类判据（转述 vs 原样、空真 vs 具体）必须由能读语义的判定者执行，否则形状判据会被一个 `raw:` 前缀绕过。
- **discriminating_evidence**: 取 6 个语义类不合格载荷（内容为转述但加了 `raw:` 前缀、或反空真条件写得笼统但可读），分别交脚本与两位独立复核者判定；若出现 ≥1 例「脚本判接收 / 两位复核者一致判拒收」，则说明脚本一极在语义面失效；若两侧结论完全一致，则脚本一极成立。结果二值：是否存在脚本误接收。
- **expected_sacrifice**: SC-004 Source ↓ 语义类不合格（转述伪装为 `raw:`）的拒收率停在 0：形状判据可被前缀伪造，而声明的六类拒收样本不含这一类。
- **revision_trigger**: 复核者在两次连续的 SI-4 派发中发现「转述 + `raw:` 前缀」被接收（脚本误接收累计 ≥2 例），或任一被接收载荷在 SI-6 重放时 `attempt` 无法按原样执行 → 重开，改为「脚本 + 语义复核双判，复核可否决但须记录理由」。

### T-002 — `expected_sacrifice` 采用封闭语法，而不是自由文本

- **decision**: `expected_sacrifice` 只接受 `<SC-NNN> Source <↓|↑>` 形态，映射失败由程序判为 `expected-sacrifice-unmapped`，不回落为人工阅读。
- **antithesis**: 自由文本 + 两位复核者按同一判据映射（沿用本仓既有的「两位复核者得同一 verdict」标准，判据清单写明「必须能对上一条已声明测量来源」）；它在「代价真实但 requirements 尚未声明对应来源」时更优——此时封闭语法会把一个真实的取舍逼成「补一条不诚实的来源」或「撤销记录」。
- **binding_constraints**:
  - pole_a: 映射失败必须是退出码而非阅读结论；一条记录只能绑定一条来源，值单值可计数（SC-001 的一次合规 + 五次反向运行依赖这一点）。
  - pole_b: 任何真实代价都必须可被记录，即使 requirements 尚未声明对应来源；强制绑定会诱导作者写下看似成立、实则无来源的 `SC-NNN` 引用，而这正是本特性要防的「填表仪式」。
- **discriminating_evidence**: 在夹具集 F（3 条「代价真实但 requirements 无对应来源」的记录）上运行 `validate-decision-tensions.py`，逐条对照 § Measurement Sources 的 `**SC-NNN Source**` 条目：若某条被 `expected-sacrifice-unmapped` 命中，而复核者确实在 requirements 中找不到可绑来源，则该例为**正确拒绝**；若复核者找到了可绑来源，则该例为**误拒**。结果二值：误拒数是否大于 0。
- **expected_sacrifice**: SC-002 Source ↑ 意图合规但把代价写成散文的计划会多出 1 条 HIGH（假阳），使「合规计划三类各 0 条」的合规组计数从 0 变为 1。
- **revision_trigger**: 连续两份真实计划各出现 ≥1 例「两位复核者独立确认代价可绑、但文法判为不可映射」的误拒 → 重开，把文法扩展为二选一：`SC` 引用，或具名的「无来源声明」并显式把该决策降级为普通取舍。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/076-decision-tension-contract/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — 11 项实测与取舍
├── data-model.md        # Phase 1 output — 8 个实体、行文法、校验规则、状态迁移
├── quickstart.md        # Phase 1 output — 5 个场景，逐示例标前提与钉住者
├── contracts/           # Phase 1 output — 8 份契约 / 34 条款
├── feature-ref.md       # Phase 1 output — Feature 绑定、FR→设计映射、SC→观测
├── test-evidence/       # plan 期确定性检查的原始输出（本轮新增 6 份）
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/guidelines/                 # 新建 decision-tension.md；改写 critique-and-self-critique.md（只增不改）
shared/workflow/                   # self-improvement-workflow.md § SI-3C：核验仍为指针形并留证（现状无复述，不改写）
templates/                         # 改写 plan-template.md（新增 ## Decision Tensions，紧随 Constitution Check）
skills/internal/analyze-artifacts/ # 改写 references/detection-and-severity.md（新增 I 通道）与 SKILL.md（通道计数行）
scripts/python/                    # 新建两个确定性校验器（张力结构 / 证伪四元组）
docs/decisions/                    # 改写 template.md（Alternatives 增 tension_id 引用位）
tests/contract/                    # 新建三个 red-first 契约测试文件
.specify/specs/076-decision-tension-contract/   # 本特性 plan 与设计产物（不含实现代码）
```

**Structure Decision**: 本特性是**框架源的规范面扩展**，不是新组件：所有新增文件落在已有目录，
唯一的「新增顶层能力」是 `shared/guidelines/decision-tension.md` 这一份 owner 文档，其余都是对既有
owner / 模板 / 通道 / 脚本目录的增补。两顶帽子明确：编辑面是 `shared/`、`templates/`、
`skills/internal/analyze-artifacts/`、`scripts/python/`、`docs/decisions/` 与 `tests/`；`.specify/`
下的同名文件一律由 `sync-mirrors.py` 产出，MUST NOT 手改。

### Mirror Obligations

镜像对清单的 owner 是 `requirements.md` FR-025 的表（行数以该表为准，本节不重复计数）；本节按其行序逐对登记本次的同步与核验，
不重写表的语义。**基线**：改动前实测 `sync-mirrors.py --check` 退出码 0、六对全 `ok`
（templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 115 / shared 59 文件），
原始输出见 `test-evidence/sync-mirrors-check.txt`；`regen-command-copies.py --check` 同样退出码 0。

| # | Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|---|----------------------|---------------------------------------------------|--------|
| 1 | `shared/guidelines/decision-tension.md`（新建） | `.specify/shared/guidelines/decision-tension.md` | 改动后跑 `sync-mirrors.py --check`，判据为「shared 对相对上述基线无新增漂移」，不以退出码单独作判据 |
| 2 | `shared/guidelines/critique-and-self-critique.md` | `.specify/shared/guidelines/critique-and-self-critique.md` | 同上（shared 对） |
| 3 | `shared/workflow/self-improvement-workflow.md` | `.specify/shared/workflow/self-improvement-workflow.md` | 同上（shared 对） |
| 4 | `templates/plan-template.md` | `.specify/templates/plan-template.md` | 同上（templates 对）；本文件不在 `commands/` 排除子树内，故无工具命令副本 |
| 5 | `skills/internal/analyze-artifacts/references/detection-and-severity.md`、`skills/internal/analyze-artifacts/SKILL.md` | `.specify/skills/internal/analyze-artifacts/` 下同名两份 | 同上（skills/internal 对） |
| 6 | `scripts/python/validate-decision-tensions.py`（新建） | `.specify/scripts/python/validate-decision-tensions.py` | 同上（scripts 对） |
| 7 | `scripts/python/validate-falsification-quartet.py`（新建） | `.specify/scripts/python/validate-falsification-quartet.py` | 同上（scripts 对） |

**工具命令副本面**：本次 MUST NOT 触及 `templates/commands/**`，因此 `regen-command-copies.py` 的 per-tool
副本集合为空；`regen-command-copies.py --check` 在改动前后都应为 0，且不得出现新增副本。

**无镜像面**：`docs/decisions/template.md`（`docs/` 不在 `MIRROR_PAIRS`）与 `tests/**` 契约测试（不入镜像）
只做源文件改动，无第二份副本需要核验。

## Phase 0: Research Review

研究结论与被否决读法全部记在 [`research.md`](research.md)，本节只保留影响设计的裁决：

- **R-1 模板锚点**：实测 `templates/plan-template.md` 的 `##` 标题序为 Constitution Check → Project
  Structure → Complexity Tracking → Phase 1，故锚点定为三行相邻断言；计划实例侧由校验器的
  `dtr-anchor` 断言，模板侧由契约测试断言。
- **R-2 通道字母**：`SKILL.md` 的 checklist 通道已占用 `H`，新通道取 `I`；两处计数行随之一并更新，
  并列入 FR-014 声明的允许差异集。
- **R-3 校验器形态**：`--spec <dir>` + 退出码 0/1/2 + `status` 行 + `[label] pass|fail (count)`，
  与 `validate-requirements.py` / `account-clause-coverage.py` 同形；选目录是因为判定跨两份工件。
- **R-4 / R-5 两个解析面**：代价用 `<SC-NNN> Source <↓|↑>`（单值、方向必填），四元组用四个字面键
  各一次 + `raw:` 前缀 + 具名输入与红色信号；两处都只判形状，语义留给复核者，代价已写进 `T-001`/`T-002`。
- **R-6 / R-7 镜像与闭合面**：基线六对 `ok`、命令副本零变化；两个闭合面按「只增不改」处理，
  计数行是唯一被改写的行，且已在契约里点名。
- **R-8 术语**：三棵分发面零命中，并以「A3 别名清单仍存在」作正控，防止清单被改名后检查空转。
- **R-9 测试布局**：三个契约测试文件按被测对象拆分，负样本只存在测试里（FR-017）。
- **R-10 试点**：本 plan 的两条记录即首个夹具，避免「先发布文法、再由同一作者用它写第一个样例」。

**Plan 期偏离记录（disclosed, not silent）**

1. **脚手架**：`bash .specify/scripts/bash/create-new-plan.sh --json` 在本机以
   `Error: CWS_LIB_BASH_HOME environment variable is not set.` 退出 1，未产生任何分支动作也未创建
   `plan.md`。按调用方允许的偏差路径，plan.md 由 `.specify/templates/plan-template.md` 就地填写：
   编号与目录能力照用，分支保持 `076-decision-tension-contract` 不变。该脚本本身不含分支切换逻辑
   （只做 `check_feature_branch`），因此被抑制的动作是「模板复制」，不是分支操作。
2. **模板缺章节**：本 plan 携带 `## Decision Tensions`，而当前模板尚无该章节——这正是本特性要落地的
   改动，模板编辑属实现阶段。计划实例先行、模板后行，是本特性作为 dogfooding 首个实例的必然不对称，
   在此显式披露。

## Complexity Tracking

N/A — Constitution Check 18 项全部 Pass，无 Violation 需要辩护，本表按模板要求移除。

## Phase 1: Design Artifacts Summary

（各计数在产物落盘后回填，取自实际文件而非预写。）

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 8 个实体（E1–E8）+ 记录行文法 + 6 条校验规则 + 6 条状态迁移 |
| Contracts | [`contracts/`](contracts/) | 8 份文件 / 34 条条款，全部 `md-bold-closed`：`decision-tension-owner.md`(8)、`plan-template-anchor.md`(3)、`measurement-binding.md`(3)、`analyze-channel.md`(5)、`adr-reference.md`(2)、`validator.md`(4)、`falsification-quartet.md`(5)、`mirrors-and-scope.md`(4) |
| Quickstart | [`quickstart.md`](quickstart.md) | 5 个场景（S1 首条记录与校验、S2 六个反向输入、S3 analyze 三类缺陷、S4 四元组接收与六类拒收、S5 镜像与术语） |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 26 条 FR → 设计落点的逐行映射 + 8 条 SC → 观测方式 |
| Research | [`research.md`](research.md) | 11 项（R-1…R-11），含实测命令与被否决读法 |
| FR 车道核算 | [`test-evidence/account-clause-coverage.txt`](test-evidence/account-clause-coverage.txt) | 26 / 26 由条款引用组认领，uncovered 0；clause 车道 `baseline-missing`（tasks.md 尚未生成，属设计内红） |

## Plan Edits

*本轮（analyze #1 之后的修复轮）改动了 plan 属主面：以下逐条写明改了哪个文件、为什么、对应哪条 analyze 发现。
不含新增或删除 FR / SC / 契约条款 / 任务行——26 FR / 8 SC / 34 条款 / 27 任务行在改动前后相同。
对应 `tasks.md` DoD-9 的声明形态：表中每行即一句 `PLAN-EDIT: <path> — <reason>`，分类统一为
`minor`（只改措辞与夹具定义，把已声明的判据钉成可判定的机械形状；无需求、条款、任务增删，无范围扩张，
无 `substantive` 项，故无异常行需要回传）。*

| # | 文件 | 改动 | 为什么 | analyze 发现 |
|---|------|------|--------|--------------|
| 1 | `requirements.md`（SC-003、SC-003 Source、US4）、`tasks.md`（T017、US4 Checkpoint）、`feature-ref.md`（SC-003 行） | SC-003 与 US4 AS2 钉死「补入不可逆决策的同时移除合规 `N/A`」，并补一步「写入合规记录替换 `N/A` → HIGH 归 0」；T017 拆为 D-1/D-2/D-3 三个子场景 | 原措辞下「恰 1 条 HIGH」不可达：检测面按 FR-011 不判「计划里是否存在承重决策」，保留合规 `N/A` 与补记录并存时结果只能是 0 | A-01 |
| 2 | `requirements.md`（FR-016、Q3）、`data-model.md`（E1 R1/R2、§ 校验规则措辞）、`contracts/validator.md` C-2 | 增跨标签优先级（章节缺失 → 只报 `dtr-section-missing`，抑制 `dtr-anchor`）；「一一对应」改为「锚点 + 三类缺陷 + 两个记录级形态的 4 + 2 划分」 | 缺章节时三行相邻断言必然同红，同一根因被计两次会让「1 条 HIGH」与退出码计数翻倍；六标签与四件事本就不是一一对应 | A-02 |
| 3 | `requirements.md`（FR-021、US3 AS1）、`contracts/falsification-quartet.md`（C-2、C-3）、`data-model.md`（E5、E6）、`tasks.md` T015 | 给「具名红色信号」定义机械形状：`would_go_red_if` 的值 MUST 以字面 `red:` 分隔，前半是反引号跨度（被改坏输入）、后半至少一个反引号跨度（断言名 / 检查标签 / 非零退出码） | 原文只写「具名红色信号」，程序无从判定，`tautology` 实际不可确定性判 | A-03 |
| 4 | `requirements.md`（SC-004、SC-004 Source）、`tasks.md`（T012、US3 Independent Test / Checkpoint）、`quickstart.md` S4、`feature-ref.md`（SC-004 行） | 六个不合格载荷改为「封闭六拒收原因码各一例，6/6」；四字段各缺一降为 `missing-field` 的附加样本（11 次运行，退出码 0/1/2 全覆盖） | 原六个载荷（四字段各缺一 + 转述 + 空真）与六个原因码不是同一集合，6/6 无法同时成立 | A-04 |
| 5 | `requirements.md` FR-004、`contracts/decision-tension-owner.md` C-4、`tasks.md`（T002、T004）、`feature-ref.md`（FR-004 行） | 点名语义拒绝形态的判定者（两位复核者按同一判据，须同 verdict），并要求 owner 写出、owner 契约与契约测试各断言一次 | 原 FR-004 只列拒绝形态、未说谁判语义项，owner 与测试都无承接点 | A-05 |
| 6 | `requirements.md` FR-010 + Clarifications Q4、`contracts/measurement-binding.md` C-1、`data-model.md` E3 | 声明方向记号是**记录性断言**：程序只判取值落在两值内，不断言方向与来源指标语义一致，值里不写指标名 | 原文把方向记号写成机器判定的「变差方向」，但无任何绑定机制，读起来像已校验而实际没有 | A-06 |
| 7 | `requirements.md`（FR-015、SC-006、SC-006 Source）、`contracts/adr-reference.md` C-2、`feature-ref.md`（SC-006 行） | 明写断链检查的唯一调用面是契约测试（导入校验器的记录索引函数作库调用），并禁止新增命令或在 analyze 通道扫描 `docs/decisions/` | 原文要求「引用 MUST 可解析」，却没有任何程序在跑，断链实际无人判 | A-07 |
| 8 | `requirements.md` FR-020/FR-021 + Q5、`contracts/falsification-quartet.md` C-2/C-3、`data-model.md` E5/E6 | 声明 `attempt` 的「可重放」是复核者规则、不进程序判决，封闭原因集不设 `attempt-not-replayable` | 「可重放」原文列在字段语义里，看不出由谁判；扩原因集会破坏封闭六值 | A-08 |
| 9 | `requirements.md`（SC-001、SC-001 Source、FR-017、Edge Cases）、`tasks.md`（T003、T008、T026、US1 Checkpoint、MVP 步骤）、`quickstart.md` S2、`feature-ref.md`（SC-001 行）、本文件（§ Testing、§ Phase 1 Quickstart 行） | 反向输入由五类改为六类：补 `tension_id` 跳号，并把「删任一字段」明确为六字段逐一各跑一次（共 12 次运行） | 原五类反向输入缺 Edge Cases 已声明的跳号形态，SC-001 的「不依赖人工阅读」因此有一个已声明缺陷没有被夹具覆盖 | A-09 |
| 10 | `tasks.md` T013/T014 | 要求 owner 小节披露两处已披露限制（`raw:` 可伪造、红色结果不可证）及处置，并由契约测试断言其存在 | 两处限制此前只写在 Clarifications Q5，没有任何实现行承接 | A-10 |
| 11 | `requirements.md` § Shared Strings 的 Citation convention | 约定收窄为「仅 requirements.md 内」；契约与任务文件逐字书写字面量 | 原文要求契约与任务也写 `[[STR-NNN]]`，而它们实际逐字书写且必须逐字（实现期要匹配），约定与用法不一致 | A-11 |
| 12 | `requirements.md` A3 + FR-024 | 别名白名单三处对齐：A3、owner 术语注记、`.specify/memory/features/076.md` § 附（并说明该文件不在三棵分发面内）（**本轮已按 A-12 收缩为两处：A3 + Feature 详情 § 附，owner 侧术语注记项删除**） | A3 允许其映射存放在 Feature 详情附录，FR-024 的白名单却只列两处，两处自相矛盾 | A-12（第一轮口径已在第二轮收缩） |
| 13 | `feature-ref.md` § 绑定关系 | 删去不存在的 `plan.md § Feature Integration` 引用，改为指向本条绑定结论与 `tasks.md` T027 | 该章节不存在，引用不可解析 | A-13 |
| 14 | `.specify/memory/features/076.md`、`.specify/memory/features.md` 076 行 | 追加 checklist 阶段记录（`cde66c0b`），状态保持 `Planned` | 阶段记录缺失，索引与详情的「最后更新」停在 tasks 阶段 | A-14 |
| 15 | 本文件（Summary / Project Structure）、`tasks.md` T016 | 「改写并删复述」改为「核验 SI-3C 仍为指针形并留证」，交付面相应改为「1 份工作流步骤核验」 | 实测 SI-3C 已只保留步骤摘要与 owner 指针、无四元组字段清单可删；原文描述的是一次空操作，且会让交付面计数虚高 | A-15 |
| 16 | `tasks.md` § Requirement Coverage Map | 增一行：T001 / T026 / T027 是流程行，不映射任何 FR / SC（**第三轮已按 A-23 修正：T001 / T027 为流程行，T026 为执行/取证行，计入 SC-002 / SC-003**） | 原表只列有 FR / SC 映射的行，读者无法判断三行是漏映射还是流程行 | A-16 |
| 17 | 本文件 § Scale/Scope / § Mirror Obligations、`tasks.md` DoD-5 / § Mirror Obligations / T024 | 「七行 / 7 对」改为「以 `requirements.md` FR-025 的表为准（行数不在本处重复）」 | 同一个数字在四处各写一份，改表就会漂移（系统性建议，本轮采纳） | A-01…A-16 的系统性收口 |

**第一轮未改动**：`research.md`（Phase 0 实测记录，第一轮无新实测需要回填；第二轮按 A-18 / A-22 更新 R-5 / R-6 / R-9）；`checklists/readiness-2026-10-29.md`（dated record，不回改）；`coverage-baseline.txt`（claims 数未变，不重冻结）。

**连带面说明**：上表每行的文件列包含该发现的**分发面同步**（同一处措辞在 SC 源、契约条款、任务行、quickstart、feature-ref 上的一致性改写），不另立发现编号；没有第 17 条之外的独立改动。

### 第二轮（analyze #2 之后的 spec-only 修复）

本轮仍无 FR / SC / 契约条款 / 任务行增删——26 FR / 8 SC / 34 条款 / 27 任务行在改动前后相同。
逐文件声明（上表第 12 行的三处白名单口径已被本轮 A-12 收缩为两处）：

- PLAN-EDIT: research.md — align R-5/R-9 with the remediated shapes；分类=minor
- PLAN-EDIT: research.md — replace R-6's "seven rows" literal with a pointer to FR-025's table；分类=minor
- PLAN-EDIT: requirements.md — drop the owner terminology note from the A3 / FR-024 whitelist, add the third cross-label precedence (empty values → `dtr-rejected-form`), pin the first-`red:` split, and sync FR-004 / FR-017 / SC-007 / US2 AS2 / Q3 / FR-025 row 3；分类=minor
- PLAN-EDIT: data-model.md — mirror the third cross-label precedence in R3 / R5 and the dedup paragraph, and the first-`red:` split in E5 / E6；分类=minor
- PLAN-EDIT: contracts/validator.md — add the third cross-label precedence to C-2 and restate C-4's sample as the literal `none`；分类=minor
- PLAN-EDIT: contracts/decision-tension-owner.md — judge a blank `expected_sacrifice` under the first rejection entry（C-4）；分类=minor
- PLAN-EDIT: contracts/falsification-quartet.md — pin the first-occurrence `red:` split in C-2 / C-3；分类=minor
- PLAN-EDIT: contracts/mirrors-and-scope.md — replace the "seven-row" literal with a pointer to FR-025's table（C-3）；分类=minor
- PLAN-EDIT: tasks.md — T003 / T007 / T008 precedence, T012 double-`red:` fixture, T015 split rule, T017 / T026 report snapshots, T021 / T023 whitelist wording；分类=minor
- PLAN-EDIT: quickstart.md — S3 label / count sync, S4 first-`red:` split, dedup wording under 「失败时怎么读」；分类=minor
- PLAN-EDIT: plan.md — this record and row 12's superseding note；分类=minor

**A-19 选项（写明）**：SC-002 / SC-003 的观测保持「analyze 报告快照」（选项 ②）。快照产出落在
T017（SC-003 三连跑，D-1 / D-2 / D-3 各一份；D-1 的裸 `N/A` 那次是 SC-003 之外的附加断言，不产快照、
不计入 SC-003）与 T026（SC-002 四类夹具各一份，并按 T017 的 D-1 / D-2 / D-3 重跑 SC-003 三份），
因此 `tasks.md` § Requirement Coverage Map 把 T026 计入 SC-002 与 SC-003 两行，不把 SC 的观测
降级为「契约测试的标签→HIGH 映射输出 + 通过/失败计数」（选项 ① 未采用：它会把报告快照这一原始
观测意图换成测试断言，SC-002 / SC-003 的判据就只剩测试是否跑绿）。

### 第三轮（analyze #3 之后的 spec-only 修复）

本轮仍无 FR / SC / 契约条款 / 任务行增删——26 FR / 8 SC / 34 条款 / 27 任务行在改动前后相同。
逐文件声明：

- PLAN-EDIT: plan.md — sync the A-19 snapshot allocation with the coverage map (T026 credited for SC-002 / SC-003; D-1's bare `N/A` run declared an extra assertion outside SC-003) and record this round；分类=minor
- PLAN-EDIT: quickstart.md — scope the co-occurrence defect rule to an empty or literal `none` `expected_sacrifice`, leaving the undecidable-wording `dtr-rejected-form` free to co-exist with `expected-sacrifice-unmapped`（A-26）；分类=minor

非 plan 属主：`.specify/memory/features/076.md` 的正文别名改为工程词（§ 附 映射表保留，白名单不扩大）。
