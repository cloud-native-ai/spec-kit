# Contract: discipline-doc — 真源文档结构契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: `shared/guidelines/user-facing-comprehension.md`(E1)  
**Test file**: `tests/contract/test_user_facing_comprehension_doc.py`  
**Date**: 2026-09-17

本契约钉死真源文档的**存在性、所有权声明、七节齐备、内容下限、中立性、零阻塞模式命中、观察接入与读者基准计数**。条款编号 C-1…C-18 由测试函数名 `test_cN_*` 一一对应。全部条款为**结构断言**,不涉及运行时行为(本特性零可执行运行时代码)。

---

## 存在性与镜像

**C-1** `shared/guidelines/user-facing-comprehension.md` MUST 存在。

**C-2** `.specify/shared/guidelines/user-facing-comprehension.md` MUST 存在,且与源文件 `read_bytes()` **逐字节相等**。

**C-3** 文件名 MUST 逐字为 `user-facing-comprehension.md`(STR-002 的 basename),MUST NOT 被重命名;该名称是 STR-005 观察标记的取值来源。

## 所有权声明

**C-4** 文档**前 8 行**内 MUST 含所有权声明,且该声明 MUST 同时满足:
- (a) 含 `single source of truth` 或 `唯一定义处` 或 `唯一真源` 之一(大小写不敏感);
- (b) 含 `MUST NOT copy` 或 `MUST NOT 复制` 之一;
- (c) 指名其 ambient 指针所在处(`templates/instructions-template.md` 的 STR-004 章节)。

**C-5** 所有权声明之后 MUST 紧随一段失效陈述,说明本纪律防的是什么失效。该段 MUST 同时覆盖两个失效面:读者需要**解码术语**(导致自信地答错)与读者需要**翻页找上下文**(导致答另一个问题)。

## 七节齐备

**C-6** 文档 MUST 含以下 **7 个** H2 节,节名逐字固定(测试以常量元组钉死):

1. 许可行话(白名单)
2. 禁用行话(黑名单)
3. 上下文下限
4. 上下文上限与裁决顺序
5. 机械判据
6. 面向用户界面类
7. 基准读者与覆盖协议

**C-7** 全文 MUST 含大写 `MUST` 与 `MUST NOT` 各至少 1 次(RFC-2119 关键词)。

**C-8** 文档 MUST 含一条**范围限制子句**,声明本纪律不新增机制(不引入行话 lint、措辞评分器、成熟度报告或跟踪台账),形态对齐 `one-source-of-truth.md:70`。

## 内容下限

**C-9** 白名单节 MUST 含 **≥5** 条可判定许可条件,且 MUST 覆盖 FR-005 列举的五类(用户已先用术语 / 词汇表 canonical 术语在**该消费单元内**首次出现时就地注解 / 用户须逐字键入的标识符 / 用户领域业务术语 / 格式自身定义且具名的短形式)。白名单节 MUST 含一句声明"白名单之外的行话一律按违规处理"。**"该消费单元内"这一限定词 MUST NOT 被简化为"首次出现"**——其定义归 C-13 的消费单元条,丢掉限定词会把按消费单元计账悄悄改回按会话计账(FR-008)。

**C-10** 黑名单节 MUST 含 **≥4** 条可判定禁止条件,且 MUST 覆盖 FR-006 列举的四类(存在用户视角途径时的引擎调用形态 / 内部标识渗入面向读者正文 / 在**该消费单元内**首次出现却无就地注解的缩写 / 以代码符号名充当行为概念名)。黑名单节 MUST 指明其条目 ② 的**实例来源**为 `skills/summarize-project/references/reporting-playbook.md` §1.7 提升而来的内部标识类别与读者向改写映射。限定词约束同 C-9。

**C-11** 上下文下限节 MUST 含 **≥3** 项(为何此刻出现 / 该决定将改变什么 / 用户可以做什么),并 MUST 对门控类界面追加"不可撤销后果与可逆性"一项。该节 MUST 以**路径引用**而非复述的方式指向 `confirmation-gates.md` 的执行报告三要素。

**C-12** 上下文上限与裁决顺序节 MUST 含 **≥3** 条上限约束(承载方式 = 事实 + 路径引用 / 非阻塞建议单行 / 不注入机器管理数据原文),并 MUST 含 **≥2** 条裁决顺序,逐条对应 FR-012 点名的两处冲突(下限 vs 单行、下限 vs 摘要优先)。该节 MUST 显式记录 clarify R2-Q3=A 裁定的**已接受代价**:门控确认提示与流程收尾报告无长度界,接受条件为"长度不设界但形态设界"。

**C-13** 机械判据节 MUST 含 **≥2** 条判问(行话侧 1 条、上下文侧 1 条),且 MUST 含一句声明该判据的目标是使两个独立评审者得出同一结论(该句是**目标形态**的声明,批量验收阈值归 SC-006 的 ≥90% 一致率所有,二者是两层而非同一量)。基准读者与覆盖协议节 MUST 含**恰好 1** 条全局基准读者定义,并 MUST 声明覆盖值"声明处生效、MUST NOT 回写本文档"。同一节 MUST 另含**恰好 1** 条 `消费单元`(consumption unit)定义,并 MUST 声明就地注解义务**按消费单元计而非按会话计**(FR-008);该定义是白名单 ②(C-9)与黑名单 ③(C-10)中"该消费单元内首次出现"这一限定词的唯一出处,故 C-9 / C-10 的转述 MUST 保留该限定词而 MUST NOT 简化为"首次出现"。

**C-14** 面向用户界面类节 MUST 含一张 **11 行**表,类名逐字匹配 FR-014 的 ①…⑪,每行携带其规则真源文件的仓库相对路径;表中出现的**去重后路径数 MUST 为 8**,且 8 个路径全部 MUST 存在于仓库。该节 MUST 声明集合为封闭集且扩展只经修订本文档。

## 中立性与预算

**C-15** 文档 MUST NOT 含本仓专有名称:`spec-kit`、`specify-cli`、`specify_cli`、`cloud-native-ai`(大小写不敏感)。

**C-16** 文档全文对 `scan-confirmation-gates.py` 的 `BLOCKING_RE` 命中数 MUST 为 **0**。测试 MUST 以 `importlib` 内联加载真实扫描器模块并复用其 `BLOCKING_RE`(先例:`test_ask_record_repeat.py:41,106-108`),MUST NOT 在测试内重写一份模式副本。

## 观察接入

**C-17** 文档 MUST 载明 FR-036 的观察约定,且 MUST 含字面量 `user-facing-comprehension`(STR-005)与以下三条红线中的全部:干净运行 MUST NOT 追加空洞观察条目、MUST NOT 编造计数或数值、MUST NOT 阻塞宿主流程或追加对用户的提问。形态 MUST 与 `shared/guidelines/token-efficiency.md:54` 的 `token-efficiency` 标记先例一致。

> **载体形态不限**:该约定 MAY 作为 C-6 七节之外的独立节,也 MAY 作为范围限制节(C-8)的子条——C-17 断言的是**内容存在**,不断言节标题,故不与 C-6 的七节封闭元组冲突。本条的存在理由是 `feature-ref.md` 曾声称 FR-036 由 C-6 钉住,而 C-6 的七节元组内并无观察节 ⇒ 该声称此前无对应断言。

---

## 读者基准计数

**C-18** SC-018("全框架声明的读者基准总数 **≤3**")的**可度量**形态。SC-018 断言的是一个全框架计数,而"声明处"此前**没有判定针**,故本条 MUST 同时钉死**计数口径**与**完备性**——否则该 SC 无任何条款度量,却仍会被 T059 记为 `pass`(此即发现项 B-08)。

**C-18(a) 计数口径 = 登记项,不是模式命中数**:断言 C-14 所钉的 11 行界面类表中 `reader_baseline_override` 列的**非空条目数 ≤ 2**(按**类**计:同一类的多处命中算一个登记项);与 C-13 的"全局基准恰好 1 条"合并即 1 + (≤2) = **≤3**,正是 SC-018。**MUST NOT 改用全框架裸模式计数**:实测 `外部读者` 一词仅在 `skills/summarize-project/` 的 9 个文件里就作为普通散文出现 **17** 次,裸计数无法区分"声明基准"与"提到读者",所得数与 SC-018 无关。

**C-18(b) 完备性 = 声明形态针扫描**:以 `Written for [^.]*stakeholders` 与 `外部读者不读代码也能看懂` 两个**声明形态**正则扫 `shared/` + `templates/` + `skills/`(豁免:真源文档自身;机械副本 `.specify/**` 与 4 棵按工具命令树;测试内钉死的字面量),断言**两个**条件:① 命中集 **⊆ 已登记的覆盖站点集**;② 每一处命中都落在**其所属类的已登记覆盖站点文件内**。**条件 ② 的判据是"覆盖站点",不是 C-14 的"规则真源路径"**(撰写 T014 时发现的原表述缺陷:二者对类 ⑧ 不是同一个文件——C-14 的去重 8 路径里类 ⑧ 的规则真源是 `skills/summarize-project/references/reporting-playbook.md`,而其读者基准声明按 T047 与 DoD-3 落在同目录的 `project-overview.md`;若按规则真源判定,该命中会被误判为未登记复述)。故 11 行表的 `reader_baseline_override` 列 MUST **具名该覆盖站点文件**,使条件 ② 可机械判定。落在登记站点之外的命中即未登记的复述,MUST 收敛为指针。2026-09-18 实测该针命中 **4 处 / 3 个文件、零散文误报**:`shared/guidelines/requirements-guidelines.md:24`(`Written for non-technical stakeholders`)与 `:101`(`Written for business stakeholders, not developers`)⇒ 类 ⑦ 的**一个**登记项(站点 = `requirements-guidelines.md`);`skills/summarize-project/references/project-overview.md:51`(`无内部黑话;外部读者不读代码也能看懂`)⇒ 类 ⑧ 的一个登记项(站点 = `project-overview.md`);以及 `templates/commands/requirements.md:82`(`Written for business stakeholders`)⇒ **类 ⑦ 的命令侧孪生,`research.md` D-14 从未登记的第 4 处**,且**违反条件 ②**(不在类 ⑦ 的登记站点 `requirements-guidelines.md` 内)。

**C-18(c) 第 4 处的处置**:D-3 已裁定 `requirements-guidelines.md` 是类 ⑦ 的**唯一**真源,故 `templates/commands/requirements.md:82` 是**复述**而非第二个覆盖站点。它 MUST 在同一批内收敛为指针(由 T043 承担;该文件是命令模板,故同批 MUST 再生其 4 棵按工具副本树),MUST NOT 被登记为类 ⑦ 的第二个覆盖处——否则 1 条全局 + 3 处覆盖 = 4,**SC-018 直接不成立**。收敛后命中集为 {`requirements-guidelines.md` ×2,`project-overview.md` ×1},对应登记项 2 个(类 ⑦、类 ⑧),计数 1 + 2 = 3 ≤ 3 ✅。

> **"处"的口径已显式裁定(避免 SC-018 的歧义被静默解决)**:SC-018 写"至多 **2 处**类级覆盖",而"处"可读作**类**或**行**。C-18(a) 取**按类计**,理由是 SC-018 约束的对象是"类级覆盖"这一机制的数量,而非某个真源文件内部把同一基准说了几遍。**已知代价并如实记录**:类 ⑦ 的真源 `requirements-guidelines.md` 今天在 `:24`(检查清单项)与 `:101`(散文规则)各表述一次,按类计为 **1** 处、按行计为 **2** 处;若采按行口径,则 1 全局 + 3 行 = 4 > 3,SC-018 需改为"≤4"或要求把 `:24`/`:101` 合并为一处。本契约**不**替规格作该选择,只把口径与其代价写明;口径的最终裁定归 `requirements.md` 的 SC-018,已在第五轮 Clarifications 记录为待用户确认项。

> **为何 C-13 / C-14 都不足以承载**:C-13 只断言真源文档内"全局基准恰好 1 条"与"覆盖值声明处生效、不回写",**不做任何跨框架计数**;C-14 只断言该表的行数、类名与去重路径数,**完全不涉及** `reader_baseline_override` 列。`feature-ref.md` 此前把 SC-018 映射到"C-13, C-14",于是 SC-018 的两半——"总数 ≤3"与"覆盖值只在类真源处"——**均无断言**;`data-model.md` 的 V1.1…V1.6 亦无一条断言 E6 的 `override_sites` 字段。本条补齐**覆盖侧**,全局侧仍归 C-13,二者合起来才构成 SC-018。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-3 | FR-001, FR-002 | SC-003 |
| C-4, C-5 | FR-001, FR-004 | — |
| C-6, C-7, C-8 | FR-004, FR-033 | SC-011 |
| C-9, C-10 | FR-005, FR-006, FR-007, FR-022 | SC-014 |
| C-11, C-12 | FR-009, FR-010, FR-011, FR-012 | SC-008 |
| C-13 | FR-008, FR-013, FR-037 | SC-006, SC-018 |
| C-14 | FR-014 | SC-004 |
| C-15 | FR-030 | SC-010 |
| C-16 | FR-032 | SC-012 |
| C-17 | FR-036 | —(运行时行为,由收尾自省履行,结果落 `verification.md`) |
| C-18 | FR-014, FR-037 | SC-018(覆盖侧;全局侧仍归 C-13,二者合计才构成 SC-018) |
