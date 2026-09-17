# Contract: surface-pointers — 界面类指针接入与收敛契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: 8 个界面类规则真源文件的指针接入、3 处内容搬家的收敛与保留项、`confirmation-gates.md` 判据各节的冻结  
**Test file**: `tests/contract/test_user_facing_comprehension_pointers.py`  
**Date**: 2026-09-17

条款编号 C-1…C-14 由测试函数名 `test_cN_*` 一一对应。11 类界面 → 8 个文件的映射裁定见 `research.md` D-3,枚举真源在真源文档的界面类节(由 `discipline-doc.md` C-14 钉死),本契约只钉**接入与收敛**。

---

## 指针接入(8 个文件)

**C-1** 下列 **8 个**规则真源文件各 MUST 含**且仅含一行**指向 `shared/guidelines/user-facing-comprehension.md` 的指针(计数按"含该路径的行数"判定,MUST == 1):

| # | 文件 | 覆盖界面类 |
|---|---|---|
| 1 | `shared/guidelines/confirmation-gates.md` | ①②⑩⑪ |
| 2 | `shared/workflow/feedback-step.md` | ③ |
| 3 | `shared/patterns/interview-pattern.md` | ④ |
| 4 | `templates/commands/clarify.md` | ⑤ |
| 5 | `shared/guidelines/requirements-guidelines.md` | ⑤⑦ |
| 6 | `shared/guidelines/proactive-trigger.md` | ⑥ |
| 7 | `skills/summarize-project/references/reporting-playbook.md` | ⑧ |
| 8 | `shared/workflow/glossary.md` | ⑨ |

**C-2** `confirmation-gates.md` 的指针 MUST 落在**头部所有权区**(`:3-5`,紧邻既有的"命令模板与技能 MUST 以单行引用接入本文档"规则),MUST NOT 落在 `:7-52` 的任何判据节内。一行头部指针覆盖 ①②⑩⑪ 四类,MUST NOT 拆成四条分节指针(SC-004 的"仅含一行")。

**C-3** 上表 8 个文件的 `.specify/` 侧镜像 MUST 与源文件 `read_bytes()` 逐字节相等(`sync-mirrors.py` 的 `shared` 与 `skills` 两个镜像对)。

## 判据冻结(FR-017)

**C-4** `confirmation-gates.md` 的下列各节 MUST **逐字未改写**:`## 两级判据`(`:7-12`)、`## 破坏性动作清单`(`:14-21`)、`## 治理保留清单`(`:23-41`,含其 **13 行**数据行)、`## 存疑从严`(`:43-45`)、`## 回流约束`(`:47-52`)。断言方式:逐节提取文本并与本契约冻结的哈希/字面量比对,MUST NOT 用"包含关键词"的弱断言。

**C-5** `confirmation-gates.md:58-60` 的执行报告三要素(执行内容 / 产出·变更工件 / 修改途径)MUST **仍由该文件拥有**,真源文档 MUST 以路径引用而非复述的方式指向它(`discipline-doc.md` C-11 的另一侧)。

## 搬家 A:`interview-pattern.md`(FR-021)

**C-6** `:121-124` 的四条可理解性规则(白话优先 / 无未解释缩写或行话 / 就地注解特殊术语 / 绝不假定共享上下文)MUST 已收敛为指向真源文档的指针;`:119` 的 `**Comprehension rules (可理解性规则)**` 标题行 MAY 保留作为指针的挂载点。

**C-7** `:125-126` 的两条模式特有规则(**每问一决策** / **问 what 不问 whether**)MUST **原文保留**——二者不属可理解性纪律,真源文档 MUST NOT 吞并它们。

**C-8** `:255` 的嵌入契约不可丢弃清单 MUST 含"接入本纪律的指针"一项。实测该清单今天列了 write-through、决策记录持久化、撤回传播、自足开放式提问格式、事实/决策拆分、用户确认退出门,而**未列** Comprehension rules——不补此项则宿主收窄时指针可被合法丢弃。

**C-9** `:280-281` 的两条反模式(`Context-free questions`、`Jargon and bare abbreviations`)MUST 已收敛为一条指向真源文档黑名单/下限的短引用,MUST NOT 保留其原始的条件复述。

## 搬家 B:`feedback-step.md`(FR-019)

**C-10** `:89-90`、`:113-115`、`:141` 三处既有措辞规则 MUST **保留未删**,其地位由"该规则的权威"降级为"本纪律在界面类 ③ 上的实例";`:115` 的并存措辞收敛权威 MUST 已从"以本节为准"上移为"以本纪律真源为准"。

## 搬家 C:`summarize-project`(FR-022)

**C-11** `skills/summarize-project/references/reporting-playbook.md` §1.7(`:109-113`)MUST 已收敛为指针;其内部标识黑名单与读者向改写映射 MUST 已提升进真源文档(`discipline-doc.md` C-10 的另一侧)。

**C-12** `shared/` + `skills/` 下**独立黑名单副本数 MUST 为 0**——即除真源文档外,不存在第二份枚举内部标识类别的清单。`reporting-playbook.md:309` 的落盘门禁与 `references/project-overview.md:51` 的 `- [ ] 无内部黑话;外部读者不读代码也能看懂` MUST **保留**(它们是该界面类的落盘检查,不是黑名单定义)。

## 单源扫描(FR-031)

**C-13** `shared/` + `templates/` + `skills/` 下以**内容形态**复述真源文档规则的位置数 MUST 为 **0**。复述的判定针:白名单条件、黑名单条件、上下文下限项、上限约束、机械判问、七个 H2 节名(对齐 `test_one_source_of_truth.py:142-153` 与 `test_token_efficiency_discipline.py:94-104` 的既有扫描形态)。**豁免**:真源文档自身;机械副本(`.specify/**` 镜像、4 棵按工具命令树、`docs/public/**`);测试内钉死的字面量常量。

**C-14** `templates/commands/interview.md` 与 `templates/commands/clarify.md` 改动后,4 棵按工具副本树(`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`)MUST 经 `regen-command-copies.py` 再生且 `--check` 返回 0;MUST NOT 存在手工批改痕迹。注意 `.specify/templates/commands/` 镜像**已退役**(`sync-mirrors.py:73` 的 templates 对排除 `commands`),MUST NOT 被创建。

---

## 已知真源缺口(如实记录,本契约不断言其被补齐)

- **类 ⑦ 的 plan/tasks 侧**:实测 `templates/plan-template.md` 与 `templates/tasks-template.md` 的 stakeholder / plain-language / business 检索**零命中**——plan/tasks 侧今天无任何措辞规则。裁定:`requirements-guidelines.md` 为类 ⑦ 的**唯一真源**(表中第 5 行),缺口如实记录,**不在本特性内**给这两个模板新增措辞规则(计划面向实现者,不面向干系人;新增即扩范围)。
- **类 ⑩**:无专属真源,裁定归 `confirmation-gates.md:62-66` 的粒度与形态规则(琐碎并入 / 合并呈现 / 失败如实报告),由表中第 1 行的头部指针覆盖。FR-011 已记录本类**无长度界**。

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-3 | FR-015 | SC-004 |
| C-4, C-5 | FR-017 | SC-016 |
| C-6, C-7, C-8, C-9 | FR-021 | SC-016 |
| C-10 | FR-019, FR-018 | SC-013 |
| C-11, C-12 | FR-022 | SC-014 |
| C-13 | FR-031 | SC-003 |
| C-14 | FR-023 | SC-016 |
