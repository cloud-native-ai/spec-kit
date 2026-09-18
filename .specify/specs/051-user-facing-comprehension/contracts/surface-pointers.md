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

**C-10** `:89-90`、`:113-114`、`:141` 三处既有措辞规则 MUST **保留未删**,其地位由"该规则的权威"降级为"本纪律在界面类 ③ 上的实例"。**`:115` 不在逐字保留集内**(订正发现项 B-09:实测 `:113-114` 才是完整的一句措辞规则——"Present the choices in user-facing terms: the notification references the / `/speckit.feedback package` command, never the raw `feedback-utils.py` engine path.";`:115` 是其后的**独立括注**"(Embedded copies that still say only "invite the user to submit" defer to this section):")。`:115` MUST 被**改写**:其并存措辞收敛权威 MUST 已从"以本节为准"上移为"以本纪律真源为准"。故本条同时含一个**保留**义务与一个**改写**义务,二者作用于**不相交**的行;MUST NOT 把 `:115` 写进保留集——原表述 `:113-115` 即犯此错,使它与其自身的改写义务构成不可满足对,并与 FR-019(需求侧真源,写的是 `:113-114`)相矛盾。

## 搬家 C:`summarize-project`(FR-022)

**C-11** `skills/summarize-project/references/reporting-playbook.md` §1.7(`:109-113`)MUST 已收敛为指针;其内部标识黑名单与读者向改写映射 MUST 已提升进真源文档(`discipline-doc.md` C-10 的另一侧)。

**C-12** `shared/` + `skills/` 下**独立黑名单副本数 MUST 为 0**——即除真源文档外,不存在第二份枚举内部标识类别的清单。`reporting-playbook.md:309` 的落盘门禁与 `references/project-overview.md:51` 的 `- [ ] 无内部黑话;外部读者不读代码也能看懂` MUST **保留**(它们是该界面类的落盘检查,不是黑名单定义)。

**C-12(a) 区分规则(机械可判;订正发现项 B-10)**:上段两句话在 `:309` 上**直接冲突**——该行字面枚举了七类内部标识(`T1`–`T5` / `E1`–`E5` / `RC-*` / `CG-*` / `§编号` / `M-*` / 脚本名),故"保留该行"与"不存在第二份枚举"不可同时满足;而 C-13 的判定针又含"黑名单条件",于是同一行被两条条款以相反方向指认,撰写 T014 时无规则可依。裁定:**判据是"是否枚举",不是"用途为何"**。一处文本 MAY 为落盘检查而**指称**黑名单(按名引用真源文档的黑名单节),但 MUST NOT **复述其类别枚举**。故 `:309` 的处置是:保留该清单项本身(勾选框、`§1.7` 引用、"无内部标识渗入"这一断言与"只出现在 `## 元信息` 或技能内部文档"这一限定),把括号内的七类枚举替换为对真源文档黑名单节的**指称**;`:51` 不含枚举,原样保留即合规。

**C-12(b) 该指称 MUST NOT 含仓库路径**(与 C-1 的交互,发现项 B-11):C-1 规定 8 个规则真源文件**各含且仅含一行**指向 STR-002 的路径。若 `:309` 的替换文本再写一次路径,`reporting-playbook.md` 就会出现第二行含路径的引用,C-1 在 T052(全部 US5 并行任务的汇聚点)转红,而 C-12 同时禁止删掉 `:309` ⇒ 形成不可满足对。故该指称 MUST 以**不含路径**的形式书写(如"见本纪律真源的黑名单节"),由该文件唯一的那一行指针承担定位。T046 与 T041 的编辑 MUST 遵守同一约束。

**C-12(c) 机械判定形态**:独立副本数 = 在 `shared/` + `skills/`(豁免:真源文档自身、机械副本 `.specify/**`、测试内钉死的字面量)中匹配真源文档黑名单**类别枚举字面量**的文本处数,MUST 为 **0**。判定针 MUST 取自真源文档黑名单节的类别字面量本身(而非用途、标题或节名),使 `:309` 在改写前为 **1**、改写后为 **0**——即该针**可证伪**,不是恒零。T014 撰写该断言时 MUST 同时在 red-first 取证里记录改写前的命中数,以证明针有效。

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
