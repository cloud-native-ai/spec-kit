# Implementation Plan: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Branch**: `053-machine-decidable-artifacts` | **Date**: 2026-10-02 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `053-machine-decidable-artifacts` → Feature 053 机器可判定的制品命题(Machine-Decidable Artifact Propositions)
**Input**: Specification from `.specify/specs/053-machine-decidable-artifacts/requirements.md`

**Date span(两个日期戳的含义)**:本特性的生命周期跨了两天的机器时钟——`/speckit.requirements` 与 `/speckit.clarify` 的产物与其提交为 **2026-09-24**(提交 `7c01b928` 等的时间戳可证),`/speckit.plan` 本轮及其全部产物为 **2026-10-02**。故文中出现的 `2026-09-24` **只**用于指称 clarify 轮的裁定、以及「本特性自己的契约落盘**之前**」的那组改前基线;凡本轮实测一律标 `2026-10-02`。初版把本轮产物也戳成 09-24(取自会话上下文而非机器时钟),已全部订正——一个错的日期戳会让下游把「今天的实测」当成「八天前的实测」来判断其是否仍然成立,这与本特性要消灭的假命题同类。

## Summary

把制品对**自己**或对**兄弟制品**做出的结构性断言,从「代理阅读后声明」改为「程序判定后输出」。动机是本仓最贵的一类缺陷形态:检查跑完给出了绿,但那个绿不是关于它被写来判定的那个命题的——一份声称「107/107 条款已覆盖」的 `tasks.md` 会把一个结构性不可满足的验收条件送进 implement,而没有任何东西会发现(判据归属 `.specify/shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿)。

技术路径是**沿用房子既有的确定性检查器形态**,不新造机制:新增两个单一入口只读脚本(`validate-requirements.py`、`account-clause-coverage.py`)、给既有 `validate-tasks.py` 增四项检查、给既有 `goal-utils.py` 增一个 `run-checks` action、给 `shared/definitions/goal-definitions.md` 增一个判据主体指代形,并为契约的**条款语法**新建唯一 owner 文档。每个新检查项都 MUST 有逆样本;断言「某集合为空」的检查都 MUST 配反空真哨兵;守卫负面命题的检查都 MUST 有一次变异演练。

范围边界(承自规格):不做语义正确性判断(仍归 `/speckit.analyze` 与 `/speckit.clarify`);不新增门控停等点、不改阶段划分或状态机、不引入守护进程或文件监听;检查器只由命令在其既有步骤内调用或由测试直接调用。

**Phase 0 产出**:18 条决策(D-1…D-18)+ 7 条上送异常(A-1…A-7;A-7 由 2026-10-03 第二轮 `/speckit.analyze` 增)落在 [research.md](./research.md),每条附实测命令与行号。其中 **3 条经用户裁定**(D-1 条款语法 owner 的形态、D-2 `.yaml` 的处置、D-3 FR-018 的辖域);D-3 扩大了 FR-018 的范围,故按上游优先规则**先改 `requirements.md`**(FR-018 改写、US2 增验收场景 6、`## Clarifications` 追加第 5 条)并复验清单一次(16/16),再填本模板。

## Technical Context

**Language/Version**: Python `>= 3.8`(承自 `pyproject.toml`);全部新增/修改脚本为**标准库 only**(`re`、`json`、`argparse`、`pathlib`、`glob`、`hashlib`、`filecmp`)。

**Primary Dependencies**: **不新增任何依赖**。`pyproject.toml` 的六项运行依赖(`typer`、`rich`、`httpx[socks]`、`platformdirs`、`readchar`、`truststore`)保持不变。**PyYAML 明确不引入**——实测它不是声明依赖(当前环境可导入纯属偶然),全部 `scripts/python/*.py` 零 `import yaml`,房子先例是 `gate-check.py:48` 的手写行解析器;为 45 个条款 id 而加一个框架级依赖很可能构成 Principle IX 违例(D-2,经用户裁定)。

**Storage**: 仅文件。全部实体都是对既有 Markdown / YAML 文本的一次只读解析结果,生命周期止于一次调用的 stdout 与退出码。**不引入任何新存据**。唯一的新增落盘物是 FR-027 裁定产生的冻结基线文件 `<spec-dir>/coverage-baseline.txt`(有序名字集,与 `run-tests.sh --names-out` 同构),它是文本而不是数据库。

**Testing**: `pytest`,markers `contract` 与 `integration`(见 `pyproject.toml` → `[tool.pytest.ini_options]`)。规范跑法为 `.specify/scripts/bash/run-tests.sh`(解析一次解释器、管道安全),基线与回归均用 `--names-out <file>` 采集**名字级**失败集,以 `comm -13 baseline current` 为空作判据——MUST NOT 以计数比对作判据。改前参考基线(本轮实跑):**65 failed / 2927 passed / 2 skipped**,名字集与 052 冻结基线 md5 相同。

**Target Platform**: 本地 CLI(Linux / macOS),经 `specify-cli` wheel 分发;`pyproject.toml:32-37` 的 `[tool.hatch.build.targets.wheel.force-include]` 把整个 `scripts` 树映射到 `specify_cli/scripts`,故新脚本自动随包安装(FR-047)。

**Project Type**: 代码生成器 / 框架——`templates/`(出厂模板)、`scripts/`(可重复工作流脚本)、`shared/`(共享约定)、`src/specify_cli/`(CLI 实现)、`tests/`(contract / integration / unit / scenarios),加同仓的客户运行时 `.specify/`(两顶帽子)。

**Performance Goals**: 无吞吐目标(检查器都是交互式单次调用)。唯一的尺度约束:对全仓 `.specify/specs/*/contracts/` 的一次只读扫描 MUST 在数秒内完成,MUST NOT 需要网络、缓存或索引。扫描面的规模由 `notes/clause-form-census.md` 唯一拥有(它是**会变动的量**:本特性自己的 7 份契约落盘后,同一命令的总数与条款 id 数都会增长),本行不复写。

**Constraints**:
1. **门控预算整数余量为 0**——`scan-confirmation-gates.py` 的 total 为 **23**,cap = 93 × 0.25 = **23.25**,由**三种形态**的断言钉住(合计 9 个断言站点 + 4 个正则匹配这些站点**源码文本**的元钉子,故改动任一钉子的措辞即打红一个元钉子)。唯一合法路径是措辞设计回避命中;MUST NOT 放宽被扫描文档集、调高上限或修改任何基线数据(FR-045、D-16)。
2. **模板项目中立**——`templates/` 下新增内容 MUST NOT 含本仓专名(FR-044)。
3. **检查器只读**——判定只经 stdout 与退出码表达(FR-005,普遍适用于全部检查器含既有的)。
4. **两条触发通道的封闭集**——命令在其既有步骤内调用,或测试直接调用;MUST NOT 接入 CI(实测本仓无任何 CI 配置)或任何守护/监听(FR-048、A-2)。
5. **退出码不得一码两义**——`run-checks` 落在既有二进制内,故 MUST 复用 `goal-utils.py:44-47` 的 `EXIT_*` 原义,`blocked` 取实测空闲的 **5**(FR-033、D-13,经用户裁定)。
6. **不新增依赖、不新增存据、不改状态机**(见上)。

**Scale/Scope**: 48 FR / 12 SC / 10 STR / 5 user stories(P1×2、P2×2、P3×1)/ 8 Key Entities / 10 Edge Cases。交付面的**行数与逐行内容以 `feature-ref.md` § 交付面清单为唯一拥有者**,本节不复写行数也不复写分类计数(初版曾在此印一份分类计数,其与拥有者的行集互不吻合,已删除而不是订正——两处各留一份就是第二处漂移点)。该清单覆盖的类别为:新建脚本、改既有脚本、新建 owner 文档、改既有文档与 Tool 记录、改命令模板(各带 4 个逐工具副本)、改既有测试、新建测试与钉子、新建基线文件、镜像副本。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**(rendered from `.specify/memory/constitution.md`,**版本 1.13.0**,动态枚举 `### <numeral>. <name>` 得 **16** 项,按出现序;实测无 `(NON-NEGOTIABLE)` / `(MANDATORY)` 标注出现在**标题**上,Principle VII 的 `**Workflow Gates (NON-NEGOTIABLE)**` 是其**正文内**的子标题,故按模板要求逐字保留在证据列而非行标签):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `feature-ref.md` 的 FR→条款映射 **48 / 48**(未覆盖 0)、SC→条款 **12 / 12**(未覆盖 0),两张表由脚本反向索引生成而非手写;`plan.md` 的每条决策可回溯到一条 FR 或一次用户裁定 |
| II | Feature-Centric Development | ✅ Pass | `plan.md:4` 的 `Requirement → Feature` 戳记;`.specify/memory/features.md` 第 053 行与 `.specify/memory/features/053.md` 均在场;状态为 `Draft`,由本命令推进为 `Planned`(§ Feature Integration) |
| III | Intent-Driven Development | ✅ Pass | `plan.md` § Summary 先讲动机与范围边界再讲技术路径;`research.md` 的 D-1/D-2/D-3 各带一个显式「被拒方案」段,说明为何不取另一条路 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | **本特性不适用 Principle VII 的 template-only 豁免**(它交付真实可执行 Python,已由委托评分独立确认):7 份契约 / **182** 条条款,其中 `checker-form.md` C-15…C-21 规定每个新检查项都有逆样本、C-19 反空真哨兵、C-20 变异演练、C-22…C-28 规定标签集与退出码表分别被钉且无零守卫检查器;`feature-ref.md` § 交付面清单含 4 组新建测试 |
| V | AI Agent Integration Standards | ✅ Pass | `plan.md` § Mirror Obligations 逐对点名 `templates/commands/` 的 **4** 个逐工具副本目录并给出 `regen-command-copies.py --check` 判据;不新增/删除任何受支持 agent |
| VI | Continuous Quality & Observability | ✅ Pass | 第一轮评分判 ⚠ Partial(`run-checks.md` C-27 要求 `docs/reference/commands/team.md` 与两份 `skills/create-team/references/*` 保持一致,却无落点行);已订正——`feature-ref.md` § 交付面清单新增两行覆盖它们,故该义务有了排期落点 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 四阶段齐备;`plan.md` § Documentation 明写 `tasks.md` 是 Phase 2 输出、本命令 MUST NOT 创建(实测该文件不存在);Feature 复用优先已履行(053 已在 clarify 轮完成绑定,本命令只推进状态,无回退) |
| VIII | Code as the Single Source of Truth | ✅ Pass | 第二轮评分判 ⚠ Partial(`notes/clause-form-census.md` 印的当前值已被自己追加的条款推翻,且该文件要求「数字 MUST 由命令重导」却没给命令);已订正——该文件现有可跑的普查命令、一张「稳定性」列区分**可安全引用的字面量**(改前基线)与**MUST 现场重导的量**,并注明该命令 MUST 从仓根运行(实测从 spec 目录运行会静默返回 `(0, 0)` 而不报错) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | `plan.md` § Technical Context:零新依赖(明确拒绝 PyYAML,D-2)、零新存据、零新顶层目录、无 CI/守护进程;唯一新增落盘物是一个文本基线文件。委托评分复核 D-3 的 FR-018 扩围**不是**范围蔓延,因为 `templates/commands/tasks.md:197` 已逐字要求那个自检 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新 owner 文档取 `shared/definitions/contract-clause-definitions.md`,与该目录既有 **8** 份 `*-definitions.md` 同体例(该目录共 9 个文件,`framework-map.md` 不匹配该模式——初版误写 9,已订正);无大写专名新登记;基线文件落在 spec 目录内 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制侧自举:FR-014 移除 `clarify-taxonomy.md` 的过渡 awk 副本而不是手改;两顶帽子:`plan.md` § Mirror Obligations 明写镜像由 `sync-mirrors.py` 生成、MUST NOT 手改。**最强的一处自举**:本特性自己的 7 份契约就在覆盖核算的扫描面内,故其 182 条条款 MUST 被本特性自己的 `tasks.md` 逐条 green-claim,MUST NOT 被 FR-027 的基线豁免 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 第一轮评分判 ❌ Fail(`.specify/memory/tools/goal-utils.py.md:39` 只列 6 个 subcommand 而二进制实有 9 个,053 再加第 10 个 `run-checks` 与 `EXIT_BLOCKED = 5`,而该 Tool 记录不在任何交付面里);已订正——`feature-ref.md` § 交付面清单新增一行,要求同一提交内把该记录订正到 10 个 action 并补退出码表 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 第一轮评分判 ⚠ Partial(全套制品对 better-harness 零引用);已订正——`.specify/memory/features/053.md` § Implementation Notes 新增归因行(强化 Agent Work Loop 的**验证/证据**维度,属 Operationalize 轨),只给指针不复写其维度表 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass(见 Gates Status 的限定) | 第一轮判 ❌ **Fail(CRITICAL)**、第二轮仍判 ❌ Fail;两轮共查出 5 处活跃重复,已全部订正为引用:(a) 镜像义务表曾在 4 处重复且**已分叉**(D-17 的 11 行漏了 `templates/commands/team.md`,plan.md 是 12 行)→ D-17 改为引用、`plan.md` § Mirror Obligations 为唯一拥有者;(b) 条款普查计数在 ~10 处被当作当前现实复写 → `notes/clause-form-census.md` 为唯一拥有者,其余全部改为引用,且**只有改前基线可作字面量**;(c) SC-006 的反空真哨兵原为字面 `110`,而本特性自己的契约就在扫描面内 → 改为关系式(见下 § 订正记录 1);(d) `plan.md` 复写交付面行数 → 改为只在带导出命令的度量表里出现;(e) `feature-ref.md` 的 SC 表曾抄录规格的度量来源原文 → 改为引用该节 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 第一轮判 ⚠ Partial(全套制品对该纪律零引用;新 owner 文档无指针义务;新检查器的 verdict **词汇**无任何约束,只钉了数字尾行形态);已订正——`clause-coverage.md` C-1 要求新 owner 文档携 canonical 指针且禁止复写其界面类表,`checker-form.md` C-33 约束 verdict 消息词汇(点名文件与行号、违反的规则、下一步),并明确 MUST NOT 向该封闭集新增类别(⑪ 失败如实报告已覆盖) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | `plan.md` § Constitution Check 记录同作者委托与必须的异常回传行;`research.md` § 上送与披露 逐条给出 A-1…A-6 的处置(A-1/A-2 作为**裁定**上送未就地修、A-3 记为 MUST NOT 而未改上游、A-4/A-5/A-6 订正);编排者自己的两处缺陷(探针设计错误、假测量)已披露并推广成规则(`checker-form.md` C-21) |

**Gates Status**: ✅ **16 / 16 Pass,0 Fail,0 Partial**。

**但这个 16/16 需要一句限定,否则它会读起来比实际更干净**:第三轮(Post-Generation Quality Gate)又查出 **9** 项缺陷,其中 **6** 项(第 2、3、6、7、8、9 项)属**同一个 XIV 类**——一个数在多处出现、或一个数被自己的后续编辑推翻。也就是说 XIV 在**连续三轮**里都被查出实例:第一轮 5 处、第二轮 5 处(部分与第一轮重叠)、第三轮 6 处。三轮都已订正,故当前状态是 Pass;但**「同一类缺陷在三轮里反复出现」本身就是证据**,说明靠人工评审收敛这一类是不可靠的——而这恰好是本特性 US1/US3 要用程序接管的命题。故本行的 Pass MUST 读作「本轮制品在被机械检查器接管**之前**、经三轮人工+委托评审后达到的一致性状态」,MUST NOT 读作「这一类缺陷已被本计划的设计排除」。

**两轮委托评分的历史与本表的订正来源**(本表不是自评分;每一行的 Pass 都建立在一次独立评分加上对其订正的机械复核之上):

| 轮次 | 评分者 | 结果 | 处置 |
|---|---|---|---|
| 第一轮 | 新鲜上下文只读子代理 A | **13 Pass / 3 Partial(VI、XIII、XV)/ 2 Fail(XII、XIV-CRITICAL)** | 6 项全部订正:补 5 个交付面落点行、补 Better-Harness 归因、补 UFC 指针与 verdict 词汇约束、把普查计数收敛到唯一拥有者、把 SC-006 的字面哨兵改为关系式 |
| 第二轮 | 新鲜上下文只读子代理 B(与 A 不相交) | **14 Pass / 1 Partial(VIII)/ 1 Fail(XIV-CRITICAL)**;并确认第一轮 6 项订正中 5 项 FIXED、1 项 PARTIALLY-FIXED | 余下 5 处重复全部订正;另外它查出**两处我新引入的假测量**(见下) |
| 第三轮 | 新鲜上下文只读子代理 C(Post-Generation Quality Gate,与前两者不相交) | 16 项判据中 **3 项全清**(契约散文无审议痕迹:7 份 / 182 条全量读过而非抽样;逐例前提清单齐备;结构完整性 4 项),另查出 **9 项缺陷** | 9 项全部订正,见下 |

**第三轮查出的 9 项(全部已订正,逐项经编排者复跑源码确认)**:

1. `contracts/run-checks.md` C-10 的判据「五项 `name` 集合与 verdict 词表集合的**交集为空**」在源码下**不可满足**——实测五项 `name` 里有 **4** 个同时也是 `goal-utils.py` 发出的 verdict 字面量(`dangling` `:665`、`target-terminal` `:669`、`cross-goal` `:643`、`goal-terminal` `:660`),只有 `goal-binding` 是纯 name。照原判据写的测试会一落地即红。已改为两条可满足的判据(至少一项 name 不在 verdict 词表内 + 逐项钉住 name→可能 verdict 集的映射)。
2. `BLOCKING_PATTERNS` 被印为 **18** 条,实测(AST `literal_eval`)为 **17**,错处 **7** 个文件位置。更糟的是这是一个**已被本仓订正过两次**的数:`051` 的规格记录了 18→17 的订正、`052` 全程用 17、且有测试断言 `== 17`;本轮的错误源自一个探查子代理称「18 entries verbatim」却在同一段里只列出 17 项,而编排者**未重导即继承**——正是本轮早些时候自己记为反馈要点的那条纪律,当场又犯一次。
3. `quickstart.md` 场景 6 的第二组三元组印「可解析 **21** / 点名 **96** / 总数 **117**」,混用了两个基底(21 属 110-基底、117 属当前树);实跑该文件自己的分类器得 **28 / 89 / 117**(本特性自己的 7 份契约也用闭合粗体形,故落在可解析侧)。
4. `quickstart.md` 场景 12 的判据「三者 MUST 全为 0」在当前树上**不可满足**,即一条**永久红**的检查:`git status --porcelain .specify/specs/` 实测 **15**(本特性自己的未跟踪制品),`find .specify/specs -name '*probe*'` 实测 **4**(全是 041/044 的既有**已跟踪**合法文件)。已重设计为「只看未跟踪 + 只在本特性目录内 + 只匹配本特性演练命名」,并**配反空真哨兵**(植入 `b9.md` → 计数变 1 → `\rm -f` → 归零,本轮实跑取证),因为没有哨兵时 `0` 无法与「模式写错了什么都匹配不到」区分。
5. `plan.md` 的 Contracts 行把两条 **spec 目录相对**的命令标注为「MUST 从仓根跑」——**方向反了**(从仓根跑得 0 并伴 `ls` 报错);且它与 `notes/clause-form-census.md` 那条**仓根相对**的命令前提相反,故两处 cwd 前提现各自写在各自行内。
6. 逐例免责块声明 **7** 处,而所给 grep 实跑得 **8**(场景 3 新增的「构造命令可实跑、验证不可」混合块未被计入)——数字对而**导出路径不可复现**,与该行自己警告的 `'^## 场景'` 过宽匹配同类。
7. `feature-ref.md` 散文段印「**15** 条不引用 FR 的条款」,而其**同文件的表**印 **16**;独立重算得 16,散文为陈旧值。
8. `requirements.md` FR-027 与 `contracts/clause-coverage.md` C-21 印「44 个 spec 目录(其中 **42** 个含 `contracts/`)」——两个数**不同基**(44 含本特性、42 不含);实测同基为 **44 / 43**。
9. `notes/clause-form-census.md` 自己印出 `(7, 180)` 与 `(117, 688)`,而实跑其自身命令得 `(7, 182)` 与 `(117, 690)`——**被自己追加的两条条款推翻第二次**(第一次是 687→688)。已按该文件自己的规则删去这两组易变字面量,只保留可安全引用的改前基线 `(110, 508)`。

**另查出 1 项编排者自身的制品缺陷(第三轮之外,由该轮回传的附带观察发现)**:`requirements.md` 的 FR-003 里「量化词辖域」整段**逐字重复两次**——clarify 轮把 `FR-003a` 折叠进 FR-003 时,先做了一次替换、又做了一次追加,两步都写了同一段。它逃过了当时全部结构核验(FR 计数、编号连续性、STR 双向、活动标记、H2 序都与之无关),因为**没有任何一项检查看 bullet 内部的重复**。已删除一份,复核该段出现次数为 **1**。这一类(单个 bullet 内部的逐字重复)是本特性 US1 检查器值得覆盖而当前 FR-006…FR-011 未覆盖的命题,已记入 `features/053.md` § Future Evolution。

**第二轮查出的两处「互相抵消」的缺陷(已订正,并升为契约条款)**:`feature-ref.md` 的两张映射表由脚本反向索引生成,而生成器有两个缺陷——① 把反引号包裹的**示例** `` `FR-7` `` 与 `` `FR-007` `` 当成对 FR-007 的两次引用(于是 FR-007 行印出 `C-6,C-6`,同一条款重复);② 用「单个反引号的奇偶位置」近似代码跨度,在正文含**行内围栏标记**处反相,把行尾真实的 `(FR-020)` 吞掉,于是 FR-020 一度显示为**零覆盖**。**两个错误在总数上恰好抵消**,故只看总数(当时印 190)完全看不出来,只有按 `(文档, C-N)` 对去重后**逐行**核对才暴露。修法与规则已写进 `contracts/requirements-checker.md` C-28(代码跨度 MUST 按 CommonMark 的 N-反引号串解析)与 C-29(先判提及/引用、再判代码跨度,顺序不可交换;计数 MUST 按对去重)。

**订正记录 1 — SC-006 的反空真哨兵曾是自我证伪的**:初版把哨兵写成「两者之和等于 **110**」,而本特性自己的 7 份契约就在被扫描面内,落盘后同一命令的总数变为 117。一份声称「110/110」的核算在分母已经变成 117 时**依然报绿**——这正是本特性要消灭的缺陷形态,出现在它自己的规格里。已改为关系式:「可解析数 + 点名数 == **本次实扫总数**」,总数由脚本运行时导出。取证与两个 as-of 值见 `notes/clause-form-census.md` § 自指修正。

**订正记录 2 — 两处与制品无关的假测量**:① `shared/definitions/` 的 `*-definitions.md` 是 **8** 份而不是 9 份(该目录共 9 个文件,`framework-map.md` 不匹配该模式),该错误曾在 3 个文件里出现;② 为报告 A-2 而抄录的旧路径字面量本身就是 `test_goal_migration.py:19` 的 `OLD_PATH_NEEDLE` 所禁止的,导致 `test_no_live_face_file_retains_the_old_path` 转红并点名 `research.md`——已改为只给坐标,并把该类失效推广成规则记在 A-2 末尾。

**Gates Status**: 见上表与 § Complexity Tracking。

**Re-check after Phase 1**: 见上表末行与 § Complexity Tracking;两次评分(初评与 Phase 1 后复评)均由新鲜上下文只读子代理执行,理由见下。

**同作者检测已委托**:本计划与其全部设计制品(`research.md`、`data-model.md`、`contracts/`×7、`quickstart.md`、`feature-ref.md`)由同一 agent 在同一会话写成,且规格本身也是同一 agent 在 clarify 轮之前写的——同作者条件成立,故 Constitution Check 的评分与 Post-Generation Quality Gate 均按 `.specify/shared/workflow/objective-analysis-gate.md` 委托给新鲜上下文只读子代理。本命令的本地参数:一个 `Fail` 或 **Partial** 行 MUST 点名它打破的**下游制品**——无制品继承的合规判定是 Complexity Tracking 噪音,不是门禁失败。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/053-machine-decidable-artifacts/
├── plan.md              # 本文件(/speckit.plan 输出)
├── research.md          # Phase 0 输出:18 条决策 D-1…D-18 + 7 条上送异常 A-1…A-7
├── data-model.md        # Phase 1 输出:8 个实体标题 + 3 个派生实体 / 40 条校验规则 V-1…V-40
├── quickstart.md        # Phase 1 输出:12 个场景(10 个含改前已实跑的真实输出)/ 7 处逐例前提清单
├── contracts/           # Phase 1 输出:7 份文档 / 182 条条款(139 制品类 + 43 行为类)
│   ├── checker-form.md            # 33 条 —— FR-001…005、FR-039…043、FR-046、FR-047
│   ├── requirements-checker.md    # 29 条 —— FR-006…014(US1)
│   ├── green-point-claim.md       # 27 条 —— FR-015…021(US2)
│   ├── clause-coverage.md         # 27 条 —— FR-022…028(US3)
│   ├── run-checks.md              # 28 条 —— FR-029…034(US4)
│   ├── criterion-subject.md       # 19 条 —— FR-035…038(US5)
│   └── neutrality-budget.md       # 19 条 —— FR-044、FR-045、FR-048
├── feature-ref.md       # Phase 1 输出:FR→条款映射 48 行 / SC→度量映射 12 行 / 交付面清单(行数由该文件拥有)
├── checklists/
│   └── requirements.md  # 质量清单,已复验 3 轮(16/16)
├── notes/
│   ├── clause-form-census.md          # 条款形态普查的可复现取证(FR-022 / SC-006 的基线)
│   └── clarify-current-failed.txt     # clarify 轮的名字级回归证据(65 条)
├── tasks.md             # Phase 2 输出(/speckit.tasks —— 本命令 MUST NOT 创建)
└── verification.md      # 实现输出(/speckit.implement)
```

### Source Code (repository root)

只列**本特性实际触及**的目录,一行一用途:

```text
scripts/python/                     # 新增 2 个检查器 + 改 2 个既有脚本(validate-tasks.py、goal-utils.py)
shared/definitions/                 # 新增条款语法 owner 文档 + 改 goal-definitions.md(判据主体指代形)
shared/guidelines/                  # 改 requirements-guidelines.md § Validation Process(FR-013)
shared/constants/                   # 改 clarify-taxonomy.md(移除过渡 awk 副本,FR-014)
templates/                          # 改 tasks-template.md(归属声明面,FR-015)
templates/commands/                 # 改 requirements.md(step 7 内增调用)与 tasks.md(step 5 内扩校验面;:197 散文自检改为指向新检查)
tests/contract/                     # 改 3 个既有测试 + 新增 4 组钉子与逆样本
.specify/scripts/python/            # 上述脚本的运行时镜像(sync-mirrors.py 生成,MUST NOT 手改)
.specify/shared/                    # 上述 shared/ 文档的运行时镜像(同上)
.specify/templates/                 # tasks-template.md 的运行时镜像(同上)
.claude/commands/                   # templates/commands/ 的逐工具副本(regen-command-copies.py 生成)
.github/prompts/                    # 同上
.qoder/commands/                    # 同上
.opencode/command/                  # 同上
```

**Structure Decision**: 本特性落在房子既有的**「代码生成器 / 框架」**形态内,**不新增任何顶层目录**。它的形状是:在 `scripts/python/` 增两个与既有 `validate-tasks.py` 同形的单一入口只读脚本、在既有两个脚本上增检查项与一个 action、在 `shared/definitions/` 增一份 `*-definitions.md` owner 文档(与该目录既有 **8** 份 `*-definitions.md` 同体例;该目录共 9 个文件,第 9 个 `framework-map.md` 不匹配该模式)、在 `templates/` 与 `templates/commands/` 的**既有步骤内**接线,并为全部新增判定面建标签集与退出码表钉子。唯一的新增落盘物是一个文本基线文件,落在本 spec 目录内。

### Mirror Obligations

改前逐对实测(2026-10-02,`sync-mirrors.py --check --only <path>`,退出码经赋值后取而非经管道取):

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/validate-requirements.py`(新建) | `.specify/scripts/python/validate-requirements.py` | `sync-mirrors.py --check --only scripts/python`;改前该对为 **EXIT=2**(既有 `.specify/scripts/python/trigger-utils.py` DIFF,先于本特性)⇒ 判据取**相对形**:无**新增** DIFF |
| `scripts/python/account-clause-coverage.py`(新建) | `.specify/scripts/python/account-clause-coverage.py` | 同上(同一对) |
| `scripts/python/validate-tasks.py`(改) | `.specify/scripts/python/validate-tasks.py` | 同上;改前实测 `--only scripts/python/validate-tasks.py` 为 `ok (1 files)` EXIT=0,故该**单文件**可用绝对判据 |
| `scripts/python/goal-utils.py`(改) | `.specify/scripts/python/goal-utils.py` | 同上;改前实测该单文件为 `ok` |
| `shared/definitions/contract-clause-definitions.md`(新建) | `.specify/shared/definitions/contract-clause-definitions.md` | `--only shared/definitions`;改前 **EXIT=0 `ok (9 files)`** ⇒ 绝对判据可用 |
| `shared/definitions/goal-definitions.md`(改) | `.specify/shared/definitions/goal-definitions.md` | 同上(同一对) |
| `shared/guidelines/requirements-guidelines.md`(改) | `.specify/shared/guidelines/requirements-guidelines.md` | `--only shared/guidelines`;改前 **EXIT=0 `ok (13 files)`** |
| `shared/constants/clarify-taxonomy.md`(改) | `.specify/shared/constants/clarify-taxonomy.md` | `--only shared/constants`;改前 **EXIT=0 `ok (3 files)`** |
| `templates/tasks-template.md`(改) | `.specify/templates/tasks-template.md`(**无** `.specify/templates/commands/` 镜像——已退役) | `--only templates/tasks-template.md`;改前 **EXIT=0 `ok (1 files)`** |
| `templates/commands/requirements.md`(改) | `.claude/commands/speckit.requirements.md`、`.github/prompts/speckit.requirements.prompt.md`、`.qoder/commands/speckit.requirements.md`、`.opencode/command/speckit.requirements.md` | `regen-command-copies.py --check`;改前 **EXIT=0**「OK: all per-tool command copies match the source templates.」⇒ 绝对判据可用 |
| `templates/commands/tasks.md`(改) | 同上 4 个逐工具副本(`speckit.tasks`) | 同上(同一命令) |
| `templates/commands/team.md`(改,增 `run-checks` 调用形式) | 同上 4 个逐工具副本(`speckit.team`) | 同上 |
| `skills/create-team/references/execution-guide.md`、`skills/create-team/references/goal.md`(改,US4 的义务落点)、`skills/create-team/scripts/build-summary-input.py`(改,退出码表对齐) | `.specify/skills/create-team/references/execution-guide.md`、`.specify/skills/create-team/references/goal.md`、`.specify/skills/create-team/scripts/build-summary-input.py` —— `skills` 是 `sync-mirrors.py` `MIRROR_PAIRS`(`:72-78`,顺序为 templates, skills, agents, scripts, shared)的**第二**对,初版把这行整条漏了(见订正记录 3) | 逐文件判据:`--check --only <该文件>`。改前 2026-10-03 实测三个**单文件**均为 **EXIT=0**(与镜像逐字节相同),故这三处**绝对判据可用**;但整对 `--only skills` 改前为 **EXIT=2 / 30 DIFF**(先于本特性,含同目录的 `operating-loops.md`、`summary-mapping.md` 两个兄弟文件),故**对级判据 MUST 取关系形**,改前名字清单由 T002 落进 `notes/pre-change-measurements.md`,此后只对新增 DIFF 阻断 |
| `templates/` 对里的两个既有欠账文件(本特性不写它们,但 T023 的 `sync-mirrors.py --write --only templates` 按**对**复制,会把它们一并同步) | `.specify/templates/proactive-trigger-seed.json`、`.specify/templates/skills-template.md` | `--check --only templates`;改前实测 **EXIT=2 / 2 DIFF**(2026-10-03;先于本特性,`templates/` 与其镜像最后提交 2026-09-20)⇒ **对级判据 MUST 取关系形**,改前名单由 T002 采集。本行是 2026-10-03 第二轮 `/speckit.analyze` 补的漏项(订正记录 4):此前 DoD-4 的「every other pair absolute」在读到本对时会默认它们干净,而写侧范围大于所有被认领的读侧范围 |

**全树判据 MUST NOT 用绝对形**:不带 `--only` 的 `sync-mirrors.py --check` 改前为 **EXIT=2 DRIFT**,实测 **33** 处 DIFF(2026-10-03 重跑,退出码经赋值后取)。初版记为「三处既有 DIFF」并只点名 `.specify/skills/summarize-project/SKILL.md`、`.specify/skills/think-skills/SKILL.md`、`.specify/scripts/python/trigger-utils.py` 三个文件——这三处确在列,但**逐对分解是 `skills` 30 + `templates` 2 + `scripts/python` 1 = 33**:初版把余下 30 处全归给 `skills`,而其中 **2 处在 `templates` 对内**(`.specify/templates/proactive-trigger-seed.json`、`.specify/templates/skills-template.md`),该对当时在表里根本没有行(2026-10-03 由第二轮 `/speckit.analyze` 查出并补,见下表与订正记录 4)。33 处皆先于本特性存在——依据是 `skills/` 与其镜像的最后提交 **2026-09-23**、`templates/` 与其镜像的最后提交 **2026-09-20**,两者都早于本特性的任何编辑;此处原先写的「工作树干净」是**假前提**(本轮整改自己就有 6 个未提交文件),结论靠提交日期成立,不靠工作树状态。

**订正一处旧结论**:052 的 plan 记录称 `regen-command-copies.py --check`「有大量既有待再生项」;本轮实测为 **EXIT=0** 全清(该批待再生项已在此间的反馈轮里再生完毕)。本特性 MUST NOT 继承那句旧结论。

**测量陷阱(本轮踩到并已订正)**:经 `| tail` 取 `$?` 得到的是 `tail` 的退出码而非脚本的,第一次测量因此把 `scripts/python` 的 EXIT=2 误报为 0。MUST 用 `PIPESTATUS` 或先赋值再取码。

**订正记录 3 — `/speckit.analyze`(2026-10-03)在本表查出两个缺陷,二者同根**:(E-04)表里**没有 `skills` 行**,而 T034/T041 要写 `skills/create-team/` 下的三个文件,该目录确有运行时镜像(`sync-mirrors.py:74`)且三个文件的镜像**当前逐字节相同**——于是本特性会在一对无人观察的镜像上制造新漂移,GATE-2 与 DoD-4 都会照常报绿。(F-03)本表所属的全树计数写作 3、实为 33。**同根**在两处缺陷都出自同一条纪律的反面:该表被 research.md 声明为镜像义务的**唯一拥有者**,于是表里的漏项与错数会被下游无条件采信;而漏项之所以发生,是因为「哪些目录有镜像」被当作**记忆**写而不是当**实测**写(`MIRROR_PAIRS` 有 5 对:templates / skills / agents / scripts / shared;初版表只覆盖其中 **3** 对的方向——scripts、shared、templates——漏掉 skills,agents 本特性不写故漏之无害)。据此本表增 `skills` 行,并 MUST 由 T037/T043 携带 `--only skills` 的同步与 GATE-2 的逐文件复核。

**订正记录 4 — 第一轮整改自己复现了它要修的缺陷(2026-10-03 第二轮 `/speckit.analyze`)**:上面那条「增 `skills` 行」的整改是 PARTIAL——它把 `--only skills` 加进了 GATE-2/T002/T037/T043 与 quickstart 场景 11,却把全树 33 处的**分解**写成「余下 30 处全在 `skills` 对内」。实测分解是 30(`skills`)+ 2(`templates`)+ 1(`scripts/python`):那 2 处是 `.specify/templates/proactive-trigger-seed.json` 与 `.specify/templates/skills-template.md`,而 `templates` 对**在表里同样没有行**——与订正记录 3 完全同形的漏项,只是换了一对。后果不是新漂移而是**范围越界**:T023 跑 `--write --only templates` 时按对复制,会把这两个无人认领的文件一并同步,DoD-4 又会把「every other pair」读成绝对判据而默认它们干净。据此本表再增 `templates` 对一行(对级关系判据 + 基线名单由 T002 采集),并订正 `requirements.md` 的 FR-027 Source 行、`tasks.md` 的 DoD-6(它把基线采集路径委托给一个**已退役**目录 `.specify/templates/commands/`,而 `MIRROR_PAIRS` 的 templates 对明确排除 `commands/`)、DoD-4 的措辞与 GATE-9 的判据形。根因写在这里供后来者复用:**改一条规则 = 改所有承载它的界面**,而「我改完了」这句话必须由逐界面复测的命令输出证明,不能由改写者的记忆证明。

## Complexity Tracking

**N/A** —— 无违例需论证,**因为两轮委托评分报出的全部违例都已被订正而不是被论证**。

这一点值得写清楚,因为「N/A」有两种截然不同的来路:一种是设计从未触犯任何原则,另一种是触犯了、然后被修掉。本计划属**后者**——第一轮报出 2 个 Fail(XII、XIV-CRITICAL)与 3 个 Partial(VI、XIII、XV),第二轮仍报出 1 个 Fail(XIV)与 1 个 Partial(VIII),逐项处置见 § Constitution Check 的两轮历史表。既然没有一项违例被**保留**,本节就没有需要论证的行;若第三轮确认评分报出任何未被订正的 Fail/Partial,本节 MUST 被填入对应行(每行点名它打破的下游制品),`N/A` 随之删除。

## Phase 1: Design Artifacts Summary

以下每个数字都由命令实跑得出(命令见每行末列),**不是**预先写下的期望值。

| Artifact | Path | Count / Scope | 导出命令 |
|----------|------|---------------|----------|
| Phase 0 研究 | [`research.md`](./research.md) | **18** 条决策(D-1…D-18)+ **7** 条上送异常(A-1…A-7,A-7 由 2026-10-03 第二轮 analyze 增记:FR 侧基线未裁定);其中 **3** 条经用户裁定 | `grep -c '^## D-' research.md` → 18;`grep -c '^- \*\*A-[0-9]' research.md` → 7(2026-10-03 重跑,先前印 6) |
| Data model | [`data-model.md`](./data-model.md) | **8** 个实体标题(E-1…E-8)+ **3** 个派生实体(E-3a/b/c)= **11** 个实体;**40** 条校验规则 V-1…V-40(连续无缺号) | `grep -cE '^## E-[0-9]' data-model.md` → 8;`grep -oE '\*\*V-[0-9]+\*\*' \| sort -u \| wc -l` → 40 |
| Contracts | [`contracts/`](./contracts/) | **7** 份文档 / **182** 条条款(**139** 制品类 + **43** 行为类,**0** 条未标注);逐文件条款 id 均连续无缺号 | `cd .specify/specs/053-machine-decidable-artifacts && ls contracts/*.md \| wc -l` → 7;`cat contracts/*.md \| grep -cE '^\*\*C-[0-9]+\*\*'` → 182(**这两条 MUST 从本 spec 目录跑**:其 glob 是 spec 目录相对路径,从仓根跑得 0 并伴一条 `ls` 报错。注意这与 `notes/clause-form-census.md` 的普查命令**相反**——后者的 glob 是仓根相对,从 spec 目录跑会静默返回 `(0, 0)` 而不报错。两者的 cwd 前提各自写在各自行内,MUST NOT 互相推断) |
| Quickstart | [`quickstart.md`](./quickstart.md) | **12** 个场景;**10** 个含改前已实跑的真实输出(✅5 + ◐5)、**2** 个纯不可实跑(❌);**8** 处逐例前提清单(7 纯 + 1 混合),**0** 处文件级免责 | `grep -c '^## 场景 [0-9]' quickstart.md` → 12(**MUST 用该精确式**:裸 `'^## 场景'` 会同时匹配 `## 场景覆盖表` 而给出 13);`grep -cE '^> \*\*.*改前不可实跑' quickstart.md` → **8**(8 处逐例块:7 处纯「不可实跑」免责 + 1 处「构造命令可实跑但验证不可」的混合式,后者在场景 3;初版印 7 是因为写作时还没有那处混合块) |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | FR→条款映射 **48** 行(**未覆盖 0**)/ SC→度量映射 **12** 行(**未覆盖 0**)/ 交付面 **26** 行(初版印 22,而拥有者实为 21;本轮补齐 5 个「义务已写进契约却无落点行」的缺口后为 26);条款引用去重 **165** 个唯一 `(文档, C-N)` 对、含重复 **188**、不引用 FR 的条款 **17**(2026-10-03 由第二轮 analyze 按 C-2 新记录的引用组规则整表重导;重导前印的是 166 / 192 / 16,那三个数出自一条从未写下来的抽取规则)| `grep -c '^\| FR-' feature-ref.md` → 48;`grep -c '^\| SC-' feature-ref.md` → 12;`awk '/^## 交付面清单/,/^## 交叉引用/' feature-ref.md \| grep '^\| ' \| grep -vc '^\| 类别'` → 26 |

**与 Phase 0 期望的漂移**:两处,均已订正而非掩盖——

1. **规格印出的条款形态分布为假**。clarify 轮印「可解析面 31 / 110、其余 79 份 `.md` 无任何机器可抽取形态」;Phase 0 重新分类后实测为**可解析 57 / 110、残余 53 份**,因为 `## C-N` 标题形(**25** 份、141 个 id)与 `**C-N (标签)**` 括注形(**1** 份、10 个 id)同样机器可抽取,而原测量只认闭合粗体(79 = 100 − 21,即「`.md` 中不含闭合粗体者」)。已按**追加**方式订正规格 4 处 + 清单 + `features/053.md` + `features.md` 的 053 行,取证落盘 `notes/clause-form-census.md`。**该假数曾出现在提交给用户的一个裁定问题的框定语里**;裁定本身不受影响(残余量级 79 → 53 不改变取舍理由),已如实披露。
2. **镜像判据不能一律取相对形**。052 的 plan 结论是「一律写成无新增漂移」;本轮逐对实测发现 6 个触及对里有 **5** 个改前即为 EXIT=0 `ok`,只有 `scripts/python` 因既有 `trigger-utils.py` DIFF 需要相对形;而 `regen-command-copies.py --check` 已从 052 期的「大量待再生」变为 **EXIT=0** 全清。故上表逐对给出判据形态,而不是一律取相对。

**覆盖核算的唯一拥有者是 `feature-ref.md`**:本节的计数只是它的摘要;两处若不一致,以 `feature-ref.md` 的实跑命令为准。
