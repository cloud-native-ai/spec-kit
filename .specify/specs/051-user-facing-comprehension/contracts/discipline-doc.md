# Contract: discipline-doc — 真源文档结构契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: `shared/guidelines/user-facing-comprehension.md`(E1)  
**Test file**: `tests/contract/test_user_facing_comprehension_doc.py`  
**Date**: 2026-09-17

本契约钉死真源文档的**存在性、所有权声明、七节齐备、内容下限、中立性、零阻塞模式命中与观察接入**。条款编号 C-1…C-17 由测试函数名 `test_cN_*` 一一对应。全部条款为**结构断言**,不涉及运行时行为(本特性零可执行运行时代码)。

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
