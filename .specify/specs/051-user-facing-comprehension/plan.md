# Implementation Plan: 面向用户可理解性纪律(User-Facing Comprehension)

**Branch**: `051-user-facing-comprehension` | **Date**: 2026-09-17 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `051-user-facing-comprehension` → Feature 051 面向用户可理解性纪律(User-Facing Comprehension)
**Input**: Specification from `.specify/specs/051-user-facing-comprehension/requirements.md`

## Summary

框架今天已在多处执行"面向用户的输出不用行话、带足上下文"这条规矩,却从未定义它:实测 **38 处独立措辞**分散在至少 4 个互不引用的领域,**真源文档 0 份、统一名字 0 个**。本计划把这条无名规矩落地为一条有名字、有程度、有守卫的纪律。

技术路线是**纯文档制品 + 契约测试**,零运行时代码(FR-033 明令禁止任何新检查器/评分器/台账):

1. **一份真源文档** `shared/guidelines/user-facing-comprehension.md`,承载行话侧白/黑名单、上下文侧下限/上限与裁决顺序、第三方可复现机械判据、11 类面向用户界面的封闭枚举、唯一基准读者 + 按类覆盖协议、范围限制子句。
2. **一个常驻章节** `## User-Facing Comprehension` 注入 `templates/instructions-template.md`,经既有增量调谐与 symlink 模型抵达全部 8 个受支持 agent 的必读文件。
3. **8 行指针**接入 11 类界面的规则真源(11 类去重后为 8 个文件,`confirmation-gates.md` 一个文件共管 4 类),把 38 处内容形态复述收敛为引用。
4. **两处内容搬家**:访谈模式文档的可理解性四规则收敛为指针(其模式特有两规则原文保留),项目总结技能的内部标识黑名单与改写映射提升为全框架可达的实例来源。
5. **宪章双落点导出**:模板新增两条原则(本纪律 + 回流的 Principle XIV)且命令 `MUST include` 清单新增对应条目,下游经 `plan` 门控的动态枚举自动生效。
6. **五份结构契约 + 四个新测试文件**,以三层表面模式(真源文档 → 常驻章节 → 契约测试)钉死一致性。

计划期的实测推翻了需求阶段的 **6 处陈述**(阻塞模式条数、传播足迹计数、两处行号、一处引文粗体、以及 FR-035 的全称守卫**不可实现**),全部按 Principle VIII 就地订正并记入规格第三轮 Clarifications。最硬的机械约束是**确认门控预算整数余量为 0**:三处新增文本中任何一行命中 17 条阻塞模式,即同时打爆两个契约测试——处置取**设计规避**(零命中 + 测试钉死),而非扩大扫描器豁免集(`research.md` D-2)。

## Technical Context

**Language/Version**: 制品语言为 Markdown;**唯一可执行代码是契约测试**,Python(repo floor `>=3.8` per `pyproject.toml`;本机实测 3.11.12)。**无运行时逻辑改动**——`src/specify_cli/` 与 `scripts/` 零修改。
**Primary Dependencies**: 仅 `pytest`(`contract` marker,见 `pyproject.toml` → `[tool.pytest.ini_options]`)。**零新增依赖**。复用既有引擎且**不修改**:`sync-mirrors.py`、`regen-command-copies.py`、`generate-instructions.sh`、`scan-confirmation-gates.py`、`feedback-utils.py`。
**Storage**: N/A。制品为版本控制下的 Markdown。观察条目(FR-036)落进既有 `.specify/memory/feedback/` 存储,经未修改的 `feedback-utils.py` 写入。
**Testing**: `pytest -m contract`。新增 4 个测试文件 + 扩展 1 个既有文件;5 份结构契约文档提供 C-N 条款编号(命名与组织依 `research.md` D-10/D-11 的既有分裂先例)。
**Target Platform**: 平台无关。纪律文本经既有 symlink 模型抵达 8 个受支持 agent 的必读文件;`.specify/shared/guidelines/` 镜像经 `specify init` 的附加式 copytree 抵达每个下游项目。
**Project Type**: 代码生成器 / 框架 —— `templates/`、`shared/`、`scripts/`、`src/specify_cli/`,并**同时**是它自己的一个客户项目(`.specify/`)。两顶帽子:本计划的全部规范性改动落在**框架源**侧,`.specify/` 侧一律为再生镜像。
**Performance Goals**: N/A —— 无运行时性能特征。读者可理解性目标由 SC-001(门控提示抽样通过率 100%)与 SC-006(双评审者一致率 ≥90%)承载。Token 成本由上下文上限(FR-010)与 SC-007(建议行零长度膨胀)约束。
**Constraints**:
- **确认门控预算整数余量 = 0**(实测 `total = 23`,`cap = 93 × 0.25 = 23.25`,且 `test_proactive_trigger_section.py:288-306` 钉死 `total == 23` 为**相等**)⇒ 三处新增文本 MUST 零 `BLOCKING_RE` 命中(`research.md` D-2 列出 17 条必避字面形态与两个高危陷阱)。
- **全树镜像字节相等**:`test_scripts_distribution_parity.py:71-87` 对整棵树跑 `sync-mirrors.py --check` 并断言 EXIT=0 ⇒ 每处源改动 MUST 同批再生镜像。改前基线实测**已全绿**(EXIT=0),故本特性可用绝对判据。
- **常驻章节位置窗口**:`## Documentation Map` → `## Proactive Flow Trigger` → `## Fact, Correctness & Logic Checks` 三者的相对位置被两个测试双向钉死 ⇒ 新章节 MUST 插在窗口之外(取 `## Token Efficiency Discipline` 之后)。
- **`confirmation-gates.md` 判据各节逐字冻结**(FR-017):两级判据 `:7-12`、破坏性清单 `:14-21`、治理保留清单 `:23-41`、存疑从严 `:43-45`、回流约束 `:47-52` MUST NOT 改写;指针只能落在头部所有权区 `:3-5`。
- **零新机制**(FR-033 / Principle IX):MUST NOT 引入行话 lint、措辞评分器、成熟度报告、跟踪台账;`scan-confirmation-gates.py` 的 `POLICY_DOCS` **不修改**(D-2 取设计规避)。
- **既有测试基线**:24 failed / 1924 passed,其中 23 条在 049 冻结基线内、1 条(`test_review_prerequisite_flags_are_supported`)因本分支尚无 `tasks.md` 而失败、`/speckit.tasks` 后自愈(`research.md` D-15)。实现期门禁 = 失败集 ⊆ 该集合,任何新增失败 ID 即回归。
**Scale/Scope**: 1 份新真源文档(`shared/guidelines/` 11 → 12);1 个新常驻章节(指令模板 `## ` 章节 17 → 18);宪章模板 2 条新原则(11 → 13)+ 活动宪章 1 条(14 → 15,版本 1.11.0 → 1.12.0);**8 行指针**覆盖 11 类界面;3 处内容搬家;5 份契约文档;4 个新测试文件 + 1 个扩展;38 处内容形态复述 → 0。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `requirements.md`(38 FR / 18 SC / 5 stories / 26 acceptance scenarios)驱动本计划;`research.md` D-1…D-15 每条决策均回溯到具体 FR 或实测事实,无凭空设计 |
| II | Feature-Centric Development | ✅ Pass | Feature 051 已注册(Draft)并绑定本 spec;`feature-ref.md` 记录 FR → 契约映射;本计划在 § Feature List Review 重新评估 Feature 增删合并 |
| III | Intent-Driven Development | ✅ Pass | 规格记录 WHY(38 处措辞 / 0 真源 / 门控零措辞规则)而非仅 WHAT;6 项用户裁定连同其依据与**被否决方案的代价**一并成文(clarify 三轮 session 块) |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | 依 Principle VII `:95` 的 **template-only 门**:本特性**零可执行运行时代码**(FR-033 明令禁止新机制),故"测试"验证的是文档内容、canonical 路径与结构,而非运行时行为。仍按测试先行:5 份契约文档先于被钉死的文档内容撰写,4 个新测试文件 + 扩展 `test_confirmation_gates_execution_report.py`(FR-034) |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent、不改 provider 配置、不动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`;纪律文本经**既有** symlink 模型抵达全部受支持 agent,是 agent 无关的散文 |
| VI | Continuous Quality & Observability | ✅ Pass | 可观察性经 FR-036 的稳定标记 `user-facing-comprehension`(沿用 `token-efficiency` 形态);活动宪章版本 MINOR 递增 1.11.0 → 1.12.0 + 前置 Sync Impact Report;**根因优先**体现在 FR-035 订正——发现全称守卫不可实现后改为可实现的具名名单,而非勉强保留一个必然失败的断言 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 逐门核验:`:91` **feature reuse-first** 已履行(8 个候选逐个核验同胞吸收证据,新建理由记入规格 `Related Feature`);`:92` **无状态回退**(Draft → Planned 是合法转移);`:93` Pre-Status-Flip Gate 本阶段不触发;`:94` 延后任务一等公民(暂无);`:95` **template-only 门**已适用于 Principle IV |
| VIII | Code as the Single Source of Truth | ✅ Pass | 计划期实测**推翻 6 处**需求阶段陈述并就地订正(阻塞模式 18→17、传播足迹 194→195、`merge-skills/SKILL.md:180`→`:179-180`、`docs/reference/skills/feedback.md:139-141`→`:140-142`、`feedback-step.md` 引文粗体、**FR-035 全称形式不可实现**),全部记入规格第三轮 Clarifications;`research.md` 每条决策附实测命令或行号 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | **零新机制**:无 lint 引擎、无评分器、无注册表、无台账(FR-033)。两处主动选择**更小的制品**:D-2 取设计规避而非改扫描器豁免集;D-6 取具名观察名单而非全称守卫。制品面 = Markdown 文档 + 契约测试,无新顶层目录、无新依赖、无 `src/` 改动 |
| X | Documentation Naming & Location Conventions | ✅ Pass | `user-facing-comprehension.md` 为小写、路径语义化(`shared/guidelines/<topic>.md` 读作"guidelines 的 <topic>"),**非**保留的 ALL-CAPS 名;不新造全局唯一文件名;无新增顶层目录;工具强制名(4 棵按工具命令副本树)保持其规定形态不改名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性**即**自我应用:框架把自己已在遵守的规矩形式化。**两顶帽子**——全部规范性改动落框架源(`shared/`、`templates/`、`skills/`、`tests/`),`.specify/` 侧一律再生镜像、不手改。**修复落机制侧**——38 处复述的收敛方向是"把副本变成引用"而非"把措辞改得一致"(FR-015/FR-031),正是 Principle XIV `:160` 要求的机制修复形态 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | **零新脚本代码**。复用既有引擎且不修改:`sync-mirrors.py`(镜像)、`regen-command-copies.py`(按工具副本)、`generate-instructions.sh`(指令再生)、`scan-confirmation-gates.py`(预算核验)、`feedback-utils.py`(观察记录)。无值得提升为 Tool 的新重复能力 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化两个 Agent Work Loop 维度:**Task Understanding**(用户能理解被问的是什么)与 **Reliable Delivery**(需要解码的门控提示换来"自信地批准错东西",直接削弱不可逆动作的唯一防线)。**证据纪律**:18 条 SC 全部带实测基线,传播足迹计数附实测日期并声明 MUST NOT 被守卫钉死(避免 configured ≠ used 式的伪精确) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 本特性是该原则的**直接应用**:38 个定义点 → 1 个 owner + 指针。规格自身也遵守它——传播足迹计数收敛为 Overview 单一定义点,6 处复述改为引用。D-5 用**完整标题**匹配避免把 `Code as the Single Source of Truth`(命令 `:91` 既有条目)与 STR-006 混为一谈。FR-028 更进一步:**把 XIV 自身回流到模板双落点**,闭合它今天"无下游项目收到"的可达性缺口 |

**Gates Status**: ⚠ 1 项 Partial(Principle IV),依 Principle VII `:95` 的 template-only 门正当化,已填 Complexity Tracking;其余 13 项 Pass。无 Fail。

**Re-check after Phase 1**: 2026-09-17 —— Phase 1 制品(`data-model.md`、`contracts/` ×5、`quickstart.md`、`feature-ref.md`)落盘后重评。**结论不变:13 Pass / 1 Partial(IV)**。Phase 1 未引入任何可执行运行时代码(契约文档是 Markdown、测试文件是 test-side),故 template-only 判定继续成立;Principle IX 经复核仍 Pass——5 份契约文档对应 5 个**互不重叠**的受守护表面,无投机制品;Principle XIV 经复核仍 Pass——`data-model.md` 的实体定义引用规格 Key Entities 而不复述,`feature-ref.md` 的 FR → 契约映射是**派生索引**(machine-checkable、不作为第二真源)。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/051-user-facing-comprehension/
├── plan.md              # 本文件(/speckit.plan 输出)
├── research.md          # Phase 0 输出 —— 独立成文(15 条决策 D-1…D-15,全部仓库内部实测,超 50 行故不内联)
├── data-model.md        # Phase 1 输出
├── quickstart.md        # Phase 1 输出
├── contracts/           # Phase 1 输出(5 份结构契约文档)
├── feature-ref.md       # Phase 1 输出(Feature 051 绑定 + FR → 契约映射)
├── requirements.md      # 上游(/speckit.requirements + 三轮 /speckit.clarify 订正)
├── checklists/          # 上游质量清单(/speckit.requirements 输出,16/16 通过)
├── baseline-failed.txt  # 实现期开工前冻结的既有失败集(承 049/050 惯例)
├── tasks.md             # Phase 2 输出(/speckit.tasks —— 非本命令产出)
└── verification.md      # 实现输出(/speckit.implement)
```

### Source Code (repository root)

```text
shared/guidelines/       # 新真源文档 user-facing-comprehension.md(第 12 份);confirmation-gates.md / proactive-trigger.md / requirements-guidelines.md 各加 1 行指针
shared/patterns/         # interview-pattern.md:可理解性四规则(:121-124)与两条反模式(:280-281)收敛为指针,:125-126 原文保留,:255 不可丢弃清单追加指针
shared/workflow/         # feedback-step.md / glossary.md 各加 1 行指针(既有措辞规则保留为界面类实例)
templates/               # instructions-template.md 新增 ## 章节(17→18);constitution-template.md 新增 2 条原则(11→13)
templates/commands/      # clarify.md(补齐行话半侧)、interview.md(收敛内容形态复述)、constitution.md(MUST include 清单 +2 条)
skills/summarize-project/references/   # reporting-playbook.md §1.7 黑名单提升出去并收敛为指针;project-overview.md / consistency-rules.md 收敛
tests/contract/          # 4 个新测试文件 + 扩展 test_confirmation_gates_execution_report.py
docs/reference/          # 3 处手写内容形态复述收敛(commands/interview.md、skills/feedback.md、commands/requirements.md)
scripts/python/          # 不改动 —— scan-confirmation-gates.py 的 POLICY_DOCS 刻意不动(D-2 取设计规避)
src/specify_cli/         # 不改动 —— 零运行时逻辑变更(FR-033 / Principle IX)
.specify/                # 仅再生镜像(shared/ templates/ skills/)+ 再生 instructions.md;一律不手改
.claude/ .github/ .qoder/ .opencode/   # 仅再生按工具命令副本(regen-command-copies.py);一律不手改
```

**Structure Decision**: 本特性落在既有的**代码生成器 / 框架**形态内,不新增任何顶层目录。制品分三圈:**规范圈**(`shared/` 的 12 份 guideline + 3 份 pattern/workflow 文档)、**投递圈**(`templates/` 与其 4 棵按工具副本树)、**守卫圈**(`tests/contract/`)。唯一的"新面"是 `shared/guidelines/` 里的第 12 份文档;其余全部是对既有文件的**加一行指针**或**把复述改成引用**。`.specify/` 与 4 棵按工具树是**再生目标而非编辑目标**——这是两顶帽子纪律(Principle XI)在本计划里的具体落点:任何直接编辑 `.specify/` 副本的动作都是错的。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

改前基线已实测(2026-09-17):`python3 scripts/python/sync-mirrors.py --check` → **EXIT=0**(`ok templates/ == .specify/templates/ (22 files)`、`ok skills/ == .specify/skills/ (489 files)`、`ok agents/ == .specify/agents/templates/ (2 files)`、`ok scripts/ == .specify/scripts/ (104 files)`、`ok shared/ == .specify/shared/ (40 files)`,外加 18 条非致命 `note extra file only in mirror:`);`python3 scripts/python/regen-command-copies.py --check` → **EXIT=0**。故本表可用**绝对判据**(全树 `--check` EXIT=0),无需 050 那样的 `--only` workaround。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/guidelines/user-facing-comprehension.md`(**新**) | `.specify/shared/guidelines/user-facing-comprehension.md` | `sync-mirrors.py --check --only shared` EXIT=0;新测试断言 `read_bytes()` 相等 |
| `shared/guidelines/confirmation-gates.md` | `.specify/shared/guidelines/confirmation-gates.md` | 同上;另断言 `:7-52` 判据各节逐字未变(FR-017) |
| `shared/guidelines/proactive-trigger.md` | `.specify/shared/guidelines/proactive-trigger.md` | 同上 |
| `shared/guidelines/requirements-guidelines.md` | `.specify/shared/guidelines/requirements-guidelines.md` | 同上 |
| `shared/patterns/interview-pattern.md` | `.specify/shared/patterns/interview-pattern.md` | 同上;另断言 `:125-126` 两规则原文保留、`:255` 清单含新指针 |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md` | 同上;另断言 `:89-90`/`:113-115`/`:141` 三处既有规则保留未删(FR-019) |
| `shared/workflow/glossary.md` | `.specify/shared/workflow/glossary.md` | 同上 |
| `templates/instructions-template.md` | ① `.specify/templates/instructions-template.md`(字节相等,被 `test_proactive_trigger_section.py:135` 与 `test_ask_record_repeat.py:185` 钉死);② **再生** `.specify/instructions.md`(新标题须逐字出现,`test_instructions_section_propagation.py:34-42` C-1);③ 8 条 symlink 别名(根 `AGENTS.md`/`CLAUDE.md`/`QODER.md`/`HERMES.md`、`.github/copilot-instructions.md`、`.qoder/project_rules.md`、`.claude/project_rules.md`、`.opencode/instructions.md`,创建于 `generate-instructions.sh:235-267`) | `bash scripts/bash/generate-instructions.sh` 后 `sync-mirrors.py --check` EXIT=0;C-1 测试绿;`ls -l` 确认 8 条仍为 symlink(未被替换成普通文件) |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` | `sync-mirrors.py --check` EXIT=0;新测试断言两条新原则结构合规 |
| `templates/commands/clarify.md` | `.claude/commands/speckit.clarify.md`、`.github/prompts/speckit.clarify.prompt.md`、`.qoder/commands/speckit.clarify.md`、`.opencode/command/speckit.clarify.md` —— **无** `.specify/templates/commands/` 镜像(该对已退役,`sync-mirrors.py:73` 的 templates 对排除 `commands`) | `regen-command-copies.py --check` EXIT=0 |
| `templates/commands/interview.md` | 同上 4 棵 | 同上 |
| `templates/commands/constitution.md` | 同上 4 棵 | 同上 |
| `skills/summarize-project/references/reporting-playbook.md`、`project-overview.md`、`consistency-rules.md` | `.specify/skills/summarize-project/references/` 下同名 3 份 | `sync-mirrors.py --check --only skills` EXIT=0 |
| `docs/reference/commands/interview.md`、`docs/reference/skills/feedback.md`、`docs/reference/commands/requirements.md` | `docs/public/**` = **Hugo 构建产物**,`git ls-files docs/public` 为 0、经 `docs/.gitignore` 忽略(证据:`skills/create-pages/references/hugo-site.md:22`)⇒ **MUST NOT 手改** | 非 CI 门禁;修好手写源后由既有 create-pages 流程重建。`quickstart.md` 场景 6 记一条提醒 |

## Complexity Tracking

> Principle IV 的 Partial 判定依 Principle VII `:95` 的 template-only 门正当化。无其他违规。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV(Test-First & Contract-Driven)判为 **Partial** 而非 Pass | 本特性**零可执行运行时代码**:`src/specify_cli/` 与 `scripts/` 均不改动,FR-033 明令禁止任何新检查器/评分器/台账。制品面全是 Markdown(1 份真源文档、1 个常驻章节、8 行指针、2 条宪章原则、3 处搬家)加 test-side 契约测试。Principle VII `:95` 正是为此形态设的门:"features with no executable runtime code judge Test-First as Partial (justified) — 'tests' verify template content, canonical paths, and structure instead"。**测试先行仍被履行**:5 份契约文档(带 C-N 条款)先于被钉死的文档内容撰写,4 个新测试文件 + 扩展 1 个既有文件,验收场景经 `quickstart.md` 的 6 个场景端到端核验 | **"给它加一个可执行检查器以让 Principle IV 判 Pass"被拒**:那正是 FR-033 与 Principle IX 禁止的投机基础设施——一个行话 lint 引擎需要词表、阈值、误报治理与调优回路,而它要判定的对象是散文措辞,本质上不适合确定性规则(规格 FR-013 因此把可判定性落在**第三方可复现的机械判据** + SC-006 的双评审一致率 ≥90%,而不是落在一个自动打分器上)。用新增机制去换一个更好看的门控判定,是拿真实复杂度换账面合规 |

## Feature List Review

依 Principle II `:36`(每阶段 MUST 重新评估 Feature 增删合并):

- **未暴露新 Feature**:本计划的 6 项交付面全部落在 Feature 051 已声明的范围内(规格 FR-001…FR-038),无溢出能力。
- **未使既有 Feature 失效**:8 个交叉引用 Feature 的能力范围均不变;`confirmation-gates.md` 的判据各节逐字冻结(FR-017),Feature 046 的所有权不受影响;`interview-pattern.md` 的模式特有规则原文保留(FR-021),Feature 042 的所有权不受影响;`feedback-step.md` 的三处既有规则保留为实例(FR-019),Feature 028 的所有权不受影响。
- **发现两项跨 Feature 效应,归属均在对方、051 为交付方**(依 Feature 050 tasks 阶段的同类先例记入对方详情文件):
  1. **SC-017 的悬空指针守卫覆盖全部 11 份既有 guideline**,不只新文档 ⇒ 它把一个既有结构性缺口变成**受测**的。真正修投递机制(`generate-instructions.sh` 同步 `shared/`)属**另一条尚未登记的 Feature**,已在规格 Out of Scope 与 `features/051.md` 的 Future Evolution Suggestions 记录。
  2. **FR-028 回流 Principle XIV** 使下游项目首次收到该原则 ⇒ 交付效应落在 Feature 040 的 backlog 上(`features/040.md` 的 Future Evolution Suggestions 第 1 条"把 token 效率纪律提升为宪章原则"今天仍待办,而 051 建立的正是它需要的双落点通道)。已在本轮把反向交叉引用写入 `features/040.md`。
- **功能/非功能分类一致性**:Feature 051 是**非功能(纪律/质量属性)**类,与 040 Token Efficiency Discipline、032 Task Complexity Rubric 同类;索引行的描述与详情文件的 Overview 均未把它表述为功能能力。一致。
- **状态推进**:`Draft → Planned`(本命令拥有该转移,依 `.specify/templates/feature-details-template.md` § Canonical Status State Machine)。**MUST NOT** 落 `Implemented`——那由 `/speckit.implement` 拥有。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Phase 0 研究 | [`research.md`](./research.md) | 15 条决策 D-1…D-15(全部仓库内部实测,无外部源);推翻需求阶段 6 处陈述 |
| 数据模型 | [`data-model.md`](./data-model.md) | 9 个实体(对应规格 Key Entities)+ 4 组校验规则 V1…V4 + 2 个状态机(指针接入态、观察名单双落点态) |
| 结构契约 | [`contracts/`](./contracts/) | 5 份:`discipline-doc.md`(17 条款)、`ambient-section.md`(11 条款)、`surface-pointers.md`(14 条款)、`constitution-export.md`(13 条款)、`gate-neutrality.md`(7 条款)—— 合计 **62 条款** |
| 快速上手 | [`quickstart.md`](./quickstart.md) | 6 个验证场景(全部命令实测执行,期望结果取自实跑输出) |
| Feature 绑定 | [`feature-ref.md`](./feature-ref.md) | Feature 051 绑定 + 38 条 FR → 62 条款契约映射 + 18 条 SC → 产出任务映射 |

**与 Phase 0 预期的漂移**:无。D-10 预期 5 份契约文档,实际 5 份;D-11 预期 4 个新测试文件 + 1 个扩展,`feature-ref.md` 的映射按此编排。一处**范围收窄已在 Phase 0 内消化**(非 Phase 1 漂移):FR-035 的全称双落点守卫经实测不可实现,改为具名观察名单(D-6),故 `constitution-export.md` 的双落点条款以名单常量而非"遍历全部原则"表述。

**计数已于制品落盘后机械核验**(2026-09-17 首次落盘;2026-09-18 因 `/speckit.analyze` 的修复批次新增 2 条契约条款后**重新核验**,依模板"summarize after, not before"要求):`grep -cE '^\*\*C-[0-9]+\*\*'` 逐份实跑得 `discipline-doc` **17**(原 16,+C-17 观察约定,修 T-3)/ `ambient-section` 11 / `surface-pointers` 14 / `constitution-export` **13**(原 12,+C-13 两块新原则零阻塞命中,修 G-5)/ `gate-neutrality` 7 = **62**;`grep -cE '^## E[0-9]'` data-model = **9**、`'^### V[0-9]'` = **4**、`'^### S[0-9]'` = **2**;`grep -cE '^## 场景'` quickstart = 7,其中 6 个为验证场景、1 个为「场景 → SC 覆盖对照」表 ⇒ **6 场景**;`research.md` 决策 **D-1…D-15 = 15 条**。上表全部数值与实测一致,无一处为预写。
