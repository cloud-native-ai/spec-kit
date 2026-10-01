# Feature Reference: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement**: `053-machine-decidable-artifacts`  
**Date**: 2026-10-02  
**本文件的职责**:承担 FR→契约条款与 SC→产出/度量两张映射表,是「哪些 FR 未被条款覆盖」的**唯一拥有者**。其余制品(plan.md 的摘要、契约文档的 Covers 行)只引用本文件,不复制其计数。

## 绑定摘要

| 项 | 值 |
|---|---|
| Feature ID | **053** |
| Feature Name | 机器可判定的制品命题(Machine-Decidable Artifact Propositions) |
| 绑定判定 | **新建**而非绑定(2026-09-24 `/speckit.clarify` 经用户裁定);决定性先例 `.specify/memory/features/040.md` 记录的 051 判新建,沿用 052 的「投递载体 ≠ 归属事实」 |
| 索引行 | `.specify/memory/features.md` 第 053 行,Status `Draft`(`/speckit.plan` 推进为 `Planned`) |
| 详情文件 | `.specify/memory/features/053.md` |
| 规格 | `requirements.md` —— 48 FR / 12 SC / 10 STR / 5 user stories(P1×2、P2×2、P3×1)/ 8 Key Entities / 10 Edge Cases / 0 活动标记 |
| 契约条款引用形态 | `<contract-file> C-N`(与 `.specify/specs/052-fast-fail-principle/feature-ref.md:21` 同一约定) |

## 覆盖统计(全部由命令实跑得出,MUST NOT 手抄)

| 量 | 值 | 导出命令(去重形态) |
|---|---|---|
| 契约文档数 | **7** | `ls contracts/*.md \| wc -l` |
| 条款总数 | **182** | 对 `contracts/*.md` 数 `^\*\*C-[0-9]+\*\*` |
| ↳ 制品类 / 行为类 | **139 / 43**(未标注 **0**) | 同上,分别加 ` \[制品类\]` / ` \[行为类\]` 后缀 |
| 条款 id 逐文件连续 | **7 / 7** 文件均为 `C-1…C-n` 无缺号 | 逐文件抽取 id 序列比对 `range(1, n+1)` |
| FR 总数 | **48** | 对 `requirements.md` 数 `^- \*\*FR-[0-9]+\*\*` |
| 有 ≥1 条款的 FR | **48**(**未覆盖 0**) | 反向索引:条款正文里**代码跨度之外**的 `FR-\d+` 引用 → 按 FR 聚合 |
| FR→条款引用总数(**去重**) | **166** 个唯一 `(文档, C-N)` 对 | 上述聚合后取集合大小 |
| FR→条款引用总数(**含重复**) | **192** | 下表第 3 列求和 |
| 不引用任何 FR 的条款 | **16** | 逐条检查正文(代码跨度之外)是否含 `FR-\d+` |
| SC 总数 / 有 ≥1 条款的 SC | **12 / 12**(未覆盖 **0**) | 同法按 `SC-\d+` 聚合 |
| 含重复引用的行(同一条款被列两次) | **0** | 逐行按 `(文档, C-N)` 对去重后比对长度 |

**生成这两张表时踩到并修掉的两个提取缺陷**(二者都是 US1 检查器 MUST 实现的规则,故在此留证):

1. **提及 ≠ 引用**(规格 FR-009 已明文):初版生成器把 `contracts/requirements-checker.md` C-6 正文里的**反引号包裹示例** `` `FR-7` `` 与 `` `FR-007` `` 当成了对 FR-007 的两次引用——于是 FR-007 行印出 `C-6,C-6`(同一条款重复),而 `FR-7` 与 `FR-007` 又都归一到 FR-007,一个错误产出两行假象。修法:只在**代码跨度之外**扫描引用形态。
2. **代码跨度 MUST 按反引号「串」解析,不能按单个反引号奇偶**:C-8 正文含一个行内围栏标记(连续多个反引号),按单反引号奇偶切分会在其后**反相**,把行尾真实的 `(FR-020)` 引用吞进"代码内",于是 FR-020 一度变成**零覆盖**。修法:按 CommonMark 规则——一段代码跨度以 N 个反引号开启、在下一处**恰为 N 个**反引号处闭合;未闭合的串按字面处理。已配自检样本(`写在 ```` ``` ```` 围栏内的 (FR-020) 与 `FR-9` 提及` → 只抽出 `FR-020`)。

这两条一起构成一个**互相抵消**的错误对:缺陷 1 多算一次引用、缺陷 2 少算一次,含重复总数因此一度看起来正确(190),而两行都是错的。**只有按 `(文档, C-N)` 对去重后逐行核对才暴露得出来**——单看总数看不出来。

**两个计数为什么不同(去重 166 vs 含重复 192)**:一条条款可以服务多条 FR(例:`checker-form` C-13 同时被 FR-005 与 FR-043 引用),故按 FR 求和会重复计入。**166 是唯一 `(文档, C-N)` 对数,192 是下表第 3 列的和**;报覆盖时必须说明用的是哪一个——052 plan 期曾因混用二者而印出 85 而非实际的 78。

**16 条不引用 FR 的条款并非孤儿**:它们逐条可追溯到一条 SC、一个边界情形、或 `research.md` 的一个决策/上送项(例:`checker-form` C-18 → SC-001;`run-checks` C-16 → 边界情形「五项里有一项自身抛异常」;`clause-coverage` C-25 → `research.md` A-3 上送项)。

## FR → 契约条款映射

条款引用形态为 `<contract-file> C-N`。第 3 列是该 FR 引用的条款数(含跨文档)。

| FR | 主题(规格原文前 44 字) | 条款数 | 契约条款 |
|---|---|---|---|
| FR-001 | 每个新增的确定性检查器 MUST 是单一入口的可执行脚本,以被校验制品的路径为参数,以退… | 2 | `checker-form` C-1,C-2 |
| FR-002 | 每个**新增**检查器的模块 docstring MUST 按 STR 的形态声明其 P… | 4 | `checker-form` C-4,C-5,C-6; `run-checks` C-25 |
| FR-003 | 每个**新增**检查器 MUST 同时提供人读输出与 `--json` 机读输出,且二者… | 5 | `checker-form` C-3,C-7,C-8,C-9,C-33 |
| FR-004 | 检查器 MUST 对「被校验文件不存在」「被校验文件不可解析」「被校验文件为空或仅含模板… | 3 | `checker-form` C-10,C-11,C-12 |
| FR-005 | 所有检查器 MUST 是只读的:判定只经 stdout 与退出码表达,MUST NOT … | 2 | `checker-form` C-13,C-14 |
| FR-006 | 系统 MUST 提供一个校验 `requirements.md` 的确定性检查器,其检查… | 3 | `requirements-checker` C-1,C-2,C-3 |
| FR-007 | 编号连续性检查 MUST 按前缀分序列独立进行(`FR-` 与 `SC-` 各自成序),… | 4 | `requirements-checker` C-2,C-4,C-5,C-29 |
| FR-008 | 文档序检查 MUST 锚定在**定义行**上,而不是在 ID 的每次出现上;其违例输出形… | 5 | `requirements-checker` C-5,C-7,C-8,C-9,C-10 |
| FR-009 | 引用可解析检查 MUST 覆盖 `FR-\d+`、`SC-\d+` 与 `[[STR-\… | 6 | `requirements-checker` C-11,C-12,C-14,C-15,C-28,C-29 |
| FR-010 | 活动标记计数 MUST 只统计**带冒号且未被反引号包裹**的实例。依据:一份讨论澄清机… | 2 | `requirements-checker` C-16,C-17 |
| FR-011 | 检查器 MUST 对同一 ID 被定义两次报 ERROR,且与「引用不可解析」分列(二者… | 3 | `requirements-checker` C-2,C-13,C-29 |
| FR-012 | `/speckit.requirements` MUST 在写完规格后调用该检查器,并在… | 4 | `neutrality-budget` C-2,C-15; `requirements-checker` C-18,C-19 |
| FR-013 | `shared/guidelines/requirements-guidelines.m… | 3 | `neutrality-budget` C-15; `requirements-checker` C-20,C-21 |
| FR-014 | US1 落地后,`shared/constants/clarify-taxonomy.m… | 6 | `requirements-checker` C-21,C-22,C-23,C-24,C-26,C-27 |
| FR-015 | tasks 模板 MUST 定义一个行内归属声明面,其字面形态为 STR;一行任务 MA… | 5 | `green-point-claim` C-1,C-2,C-3,C-5; `neutrality-budget` C-2 |
| FR-016 | `validate-tasks.py` MUST 把 STR 形态的声明解析为 `(契约… | 5 | `green-point-claim` C-6,C-7,C-9,C-10,C-11 |
| FR-017 | `validate-tasks.py` MUST 增一项 **WARN** 级检查:某条… | 3 | `green-point-claim` C-12,C-13,C-14 |
| FR-018 | 归属声明的冲突检查 MUST 覆盖**两个**命题;二者相关但不是同一个检查,故 MUS… | 5 | `green-point-claim` C-15,C-16,C-17,C-18,C-19 |
| FR-019 | 归属声明 MUST 与既有的行形态检查正交:一行只声明归属而不声明文件路径时,既有检查 … | 5 | `green-point-claim` C-20,C-21,C-22,C-23,C-24 |
| FR-020 | 出现在**围栏代码块内**的 STR 形态 MUST NOT 被当作真实归属声明解析。… | 3 | `green-point-claim` C-8; `requirements-checker` C-28,C-29 |
| FR-021 | 归属声明面 MUST 项目中立:MUST NOT 含本仓专有名词,其形态说明 MUST … | 2 | `green-point-claim` C-4; `neutrality-budget` C-3 |
| FR-022 | 系统 MUST 为契约的**条款语法**指定唯一 owner:要么指定一份既有文档为 o… | 6 | `clause-coverage` C-1,C-2,C-3,C-4,C-5; `green-point-claim` C-11 |
| FR-023 | 核算脚本 MUST 按 owner 定义的形态抽出条款全集;对无法按该形态解析的文件 M… | 5 | `clause-coverage` C-7,C-8,C-9,C-13,C-14 |
| FR-024 | 核算 MUST 以**集合差**表达结果:全集减去被认领子集,印出未覆盖集,前缀形态为 … | 1 | `clause-coverage` C-16 |
| FR-025 | 未覆盖集为空时,脚本 MUST 同时印出至少一个**必须非空**的伴生量(已认领条款数、… | 1 | `clause-coverage` C-17 |
| FR-026 | 条款未覆盖与 FR 未覆盖 MUST 分列,二者的全集来源不同,MUST NOT 合并为… | 1 | `clause-coverage` C-18 |
| FR-027 | 覆盖核算 MUST NOT 要求改造既有 spec 的契约文件。对既有 **44** 个… | 6 | `clause-coverage` C-20,C-21,C-22,C-23,C-24; `neutrality-budget` C-17 |
| FR-028 | `.yaml` 形态的契约(实测 **10** 份)MUST 被覆盖核算显式处置:MUS… | 5 | `clause-coverage` C-10,C-11,C-12,C-13,C-26 |
| FR-029 | `goal-utils.py` MUST 增一个名为 STR 的 action,一次调用… | 4 | `run-checks` C-1,C-2,C-26,C-27 |
| FR-030 | 该 action MUST 复用既有的内部解析函数而**不重写第二套文法**;无 `--… | 4 | `run-checks` C-5,C-6,C-7,C-8 |
| FR-031 | 机读输出的每条 check MUST 含 `id`(1..5)、`name`(上述五个名… | 5 | `run-checks` C-2,C-6,C-9,C-10,C-11 |
| FR-032 | 单项检查的 verdict MUST 沿用既有词表 STR;因前置条件不成立而被短路的检… | 5 | `run-checks` C-7,C-10,C-12,C-13,C-14 |
| FR-033 | 退出码 MUST 按 STR 分档,且「检查判为阻塞」与「输入不合法」与「定义不可解析」… | 4 | `run-checks` C-17,C-18,C-19,C-20 |
| FR-034 | 该 action MUST 零写入:任何一次调用都 MUST NOT 修改 `.spec… | 3 | `checker-form` C-28; `run-checks` C-3,C-4 |
| FR-035 | `shared/definitions/goal-definitions.md` MUS… | 6 | `criterion-subject` C-1,C-2,C-3,C-4,C-14,C-18 |
| FR-036 | 指代形指向不存在的路径时 MUST 报可区分的错误,MUST NOT 退化为空集合;导出… | 3 | `criterion-subject` C-5,C-6,C-7 |
| FR-037 | 一条判据同时使用指代形与成员枚举时 MUST 报冲突,MUST NOT 静默择一。… | 3 | `criterion-subject` C-8,C-9,C-10 |
| FR-038 | 既有的纯枚举判据 MUST 保持完全一致的解析行为;本特性 MUST NOT 使任何既有… | 2 | `criterion-subject` C-11,C-12 |
| FR-039 | 本特性新增的**每一项**检查 MUST 有逆样本取证:证明被守物真的坏掉时该检查会变红… | 5 | `checker-form` C-15,C-16,C-21; `green-point-claim` C-24,C-27 |
| FR-040 | 凡断言「某集合为空」的检查(未覆盖集、不可解析集、冲突集),MUST 在同处配一条**反… | 5 | `checker-form` C-19; `clause-coverage` C-17; `criterion-subject` C-7,C-12; `requirements-checker` C-25 |
| FR-041 | 凡守卫**负面命题**的检查(某物不存在 / 未变化 / 未泄漏),其取证 MUST 含… | 2 | `checker-form` C-17,C-20 |
| FR-042 | 检查项集合的钉子 MUST 以**标签集**表达,而不是以计数表达;退出码表 MUST … | 3 | `checker-form` C-5,C-22,C-23 |
| FR-043 | 每个检查器 MUST 至少对一份**真实存在**的仓内制品只读地跑通一次并留下真实输出,… | 1 | `checker-form` C-29 |
| FR-044 | `templates/` 下新增的一切内容 MUST 项目中立:MUST NOT 含 `… | 4 | `green-point-claim` C-4; `neutrality-budget` C-1,C-2,C-3 |
| FR-045 | 本特性落地后,`scripts/python/scan-confirmation-gat… | 10 | `clause-coverage` C-5,C-6; `criterion-subject` C-19; `neutrality-budget` C-4,C-5,C-6,C-7,C-8,C-9,C-10 |
| FR-046 | 本特性触及的每个检查器 MUST 在落地时**同时**具备钉住其检查项标签集与退出码表的… | 10 | `checker-form` C-24,C-25,C-26,C-27; `criterion-subject` C-17; `green-point-claim` C-25,C-26; `run-checks` C-22,C-23,C-24 |
| FR-047 | 检查器 MUST 随包安装到运行时镜像,并被镜像同步的一致性检查覆盖(与 `valida… | 3 | `checker-form` C-30,C-31,C-32 |
| FR-048 | 本特性 MUST NOT 新增任何门控停等点、MUST NOT 改变 `/speckit… | 5 | `neutrality-budget` C-11,C-12,C-13,C-14,C-15 |

### 未由契约条款覆盖的 FR(0 条)

无。48 条 FR 全部有 ≥1 条款;该结论由上表的反向索引命令实跑得出,不是目测。

## SC → 产出与度量映射

| SC | 主题(规格原文前 40 字) | 条款数 | 契约条款 |
|---|---|---|---|
| SC-001 | `requirements.md` 的四类结构命题(编号连续、文档序、引用可解析… | 2 | `checker-form` C-17,C-18 |
| SC-002 | `shared/constants/clarify-taxonomy.md` 里… | 4 | `requirements-checker` C-22,C-23,C-24,C-25 |
| SC-003 | 「条款由哪一行任务转绿」成为可解析面:对一份归属序与阶段序一致的最小 tasks… | 1 | `green-point-claim` C-12 |
| SC-004 | 悬空归属(指向不存在的契约文件或条款 id)被判为 ERROR 而非 WARN,… | 3 | `green-point-claim` C-9,C-10,C-14 |
| SC-005 | 覆盖核算以集合差表达:对一份 3 条款契约、2 条被认领的最小 spec,印出的… | 3 | `clause-coverage` C-16,C-19; `neutrality-budget` C-18 |
| SC-006 | 条款语法有唯一 owner:owner 文档存在、声明其覆盖的形态、并被核算脚本… | 2 | `clause-coverage` C-7,C-27 |
| SC-007 | [[STR-005]] 一次调用输出五条 check 且字段齐备;对一个 goa… | 2 | `run-checks` C-3,C-28 |
| SC-008 | 短路项不报绿:构造一个使某项检查前置条件不成立的团队,该条 verdict 为 … | 1 | `run-checks` C-13 |
| SC-009 | 指代形的价值可被直接看见:对同一主体集合分别用指代形与成员枚举写两条判据,在目录… | 1 | `criterion-subject` C-13 |
| SC-010 | 向后兼容:本特性落地前后,对仓内**全部**既有 goal 定义跑一次解析,失败… | 4 | `clause-coverage` C-24; `criterion-subject` C-11,C-12; `neutrality-budget` C-18 |
| SC-011 | 「机器给出的绿」的证据纪律被执行:本特性新增的检查项**逐项**都有逆样本,逆样… | 3 | `checker-form` C-16,C-17; `green-point-claim` C-27 |
| SC-012 | 预算与中立性保持:落地后 `scan-confirmation-gates.py… | 7 | `clause-coverage` C-24; `neutrality-budget` C-1,C-4,C-16,C-17,C-18,C-19 |

## 交付面清单

| 类别 | 落点 | 归属决策 |
|---|---|---|
| 新建脚本 | `scripts/python/validate-requirements.py` | D-4 |
| 新建脚本 | `scripts/python/account-clause-coverage.py` | D-10 |
| 新建 owner 文档 | `shared/definitions/contract-clause-definitions.md` | D-1(经用户裁定) |
| 改既有脚本 | `scripts/python/validate-tasks.py`(+4 检查项、归属声明解析、路径分类修复) | D-5、D-7 |
| 改既有脚本 | `scripts/python/goal-utils.py`(+`run-checks` action、+`EXIT_BLOCKED = 5`、docstring roster 与退出码表扩充) | D-11…D-13 |
| 改模板 | `templates/tasks-template.md`(归属声明面) | FR-015、C-1…C-5 |
| 改命令模板 | `templates/commands/requirements.md`(step 7 内增调用) | FR-012、C-15 |
| 改命令模板 | `templates/commands/tasks.md`(step 5 内扩校验面;`:197` 散文自检改为指向新检查) | US2、D-3 |
| 改既有文档 | `shared/guidelines/requirements-guidelines.md` § Validation Process | FR-013 |
| 改既有文档 | `shared/constants/clarify-taxonomy.md`(移除过渡 awk 副本与「Until that validator ships」) | FR-014、D-9 |
| 改既有文档 | `shared/definitions/goal-definitions.md`(新增判据主体指代形一节) | FR-035、D-14 |
| 改既有文档 | `templates/commands/team.md:114-119`(增 `run-checks` 调用形式) | FR-029、C-26 |
| 改既有测试 | `tests/contract/test_validate_tasks_parallel_safety.py`(扩 `EXPECTED_CHECKS` 与退出码表) | FR-046、C-25/C-26 |
| 改既有测试 | `tests/contract/test_clarify_semantic_completeness.py`(两个 test_c4 改写方向) | FR-014、D-9、C-26/C-27 |
| 改既有测试 | `tests/contract/test_goal_definition.py`(roster 9 元组 → 10 元) | FR-046、D-12 |
| 新建测试 | `validate-requirements.py` 的标签集钉子 + 退出码表钉子 + 5 个逆样本 | FR-039、FR-042、FR-046 |
| 新建测试 | `account-clause-coverage.py` 的形态抽取钉子 + 反空真哨兵 | FR-025、FR-040 |
| 新建测试 | `goal-utils.py` 的退出码表钉子(抄 `test_trigger_engine.py:48` 形态)+ 封闭 roster 断言 | FR-046、D-13 |
| 新建测试 | 判据主体指代形的正则钉子 + 两档失败逆样本 | FR-036、FR-046 |
| 新建基线文件 | `coverage-baseline.txt`(未覆盖项名字集,含 owner 形态集声明) | FR-027、D-10、C-21/C-23 |
| 镜像副本 | 全部 `scripts/python/` 与 `shared/` 落点的 `.specify/` 对偶 + `templates/commands/` 的 4 个逐工具副本 | D-17 |
| 改既有 Tool 记录 | `.specify/memory/tools/goal-utils.py.md` —— 其 `:39` 的 subcommand 枚举行当前只列 **6** 个(`create`/`validate`/`list`/`status`/`criteria`/`migrate`)而二进制实有 **9** 个(缺 `check-statement`/`objective`/`targets`);US4 再加第 10 个 `run-checks` 与 `EXIT_BLOCKED = 5`,故 MUST 在同一提交内把该记录订正到 10 个并补退出码表 | Principle XII(Tool 记录的权威高于模型知识,故一份陈旧记录会被下游当作事实继承);本轮委托评分查出的 ❌ Fail |
| 改既有文档 | `docs/reference/commands/requirements.md`、`docs/reference/commands/tasks.md`、`docs/reference/commands/team.md`(后者 `:68,70` 已被 `contracts/run-checks.md` C-27 点名要求与新调用形式一致) | Principle VI(可观测面文档);本轮委托评分查出的 ⚠ Partial —— 义务已写进契约却无落点行 |
| 改既有文档 | `skills/create-team/references/execution-guide.md:27,30`、`skills/create-team/references/goal.md:45`(描述同五项检查的散文面) | `contracts/run-checks.md` C-27; Principle VI |
| 新建 owner 文档的可理解性接线 | `shared/definitions/contract-clause-definitions.md` 的新增节 MUST 携一行指向 `.specify/shared/guidelines/user-facing-comprehension.md` 的 canonical 指针,且新检查器 verdict 消息的**词汇**MUST 受该纪律约束(不只受 `checker-form.md` C-8 的数字尾行形态约束) | Principle XV;本轮委托评分查出的 ⚠ Partial |
| Better-Harness 归因 | 本特性强化的是 Agent Work Loop 的**验证/证据**维度(把「代理声明已核验」换成「程序给出会红的判定」),归因行落在 `.specify/memory/features/053.md` § Implementation Notes | Principle XIII(`docs/concepts/better-harness.md`);本轮委托评分查出的 ⚠ Partial |

## 交叉引用(消费关系,不构成归属)

见 `.specify/memory/features/053.md` § 交叉引用——本 Feature 消费 032 / 040 / 041 / 046 / 051 / 052 / 028 的既有权威,均只引用不改写;其中对 052 的 `clarify-taxonomy.md` 过渡副本是**偿还债务**(FR-014),不是改写其真源。
