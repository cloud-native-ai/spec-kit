# Data Model: 面向用户可理解性纪律(Feature 051)

**Date**: 2026-09-17  
**Nature**: 本特性无数据库、无运行时状态存储(FR-033 禁止任何新台账)。下列"实体"是**文档结构实体**——它们的实例是 Markdown 文档中的具名节、表行或字面量,其"字段"是这些结构必须携带的成分,其"校验"由契约测试执行。9 个实体与规格 `## Requirements` > `### Key Entities` 一一对应,本文档**引用**该节的语义定义而不复述。

---

## E1 可理解性纪律真源(Comprehension Discipline Owner)

**物化位置**: `shared/guidelines/user-facing-comprehension.md`(STR-002)+ 镜像 `.specify/shared/guidelines/user-facing-comprehension.md`(STR-001)  
**基数**: 恰好 **1**(FR-001;SC-003 断言真源文档数量为 1)

| 字段 | 形态 | 约束 | 来源 FR |
|---|---|---|---|
| `ownership_declaration` | 文首 3–8 行的散文或 `>` 块引 | MUST 声明本文档为该纪律唯一定义处;MUST 含 MUST-cite / MUST-NOT-copy 语义 | FR-001 |
| `failure_statement` | 紧随所有权声明的一段 | MUST 说明防的是什么失效(读者解码术语→自信答错;读者翻页找上下文→答另一个问题) | FR-004 |
| `section_headings` | 七个 H2 节 | MUST 齐备:白名单 / 黑名单 / 上下文下限 / 上下文上限与裁决顺序 / 机械判据 / 界面类枚举 / 基准读者与覆盖协议 | FR-005…FR-014, FR-037 |
| `rfc2119_keywords` | 全文 | MUST 使用大写 MUST / MUST NOT / SHOULD / MAY | FR-004 |
| `scope_limit_clause` | 一条子句 | MUST 声明本纪律不新增机制(对齐 `one-source-of-truth.md:70` 先例) | FR-033 |
| `surface_class_map` | 一张 11 行表 | MUST 为封闭集;每行 = 界面类 → 规则真源文件路径 | FR-014 |
| `project_neutrality` | 全文 | MUST NOT 含本仓专有名称 | FR-030 |
| `blocking_pattern_hits` | 可派生量 | MUST 为 **0** | FR-032(条件前提不成立)、SC-012 |
| `observation_convention` | 一段或一节 | MUST 载明 STR-005 字面量与三条红线(干净运行不追加空洞条目 / 不编造数值 / 不阻塞宿主流程);载体形态不限(独立节或范围限制节的子条),由 `discipline-doc` **C-17** 断言 | FR-036 |

**关系**: 被 E2 的每行以指针引用;被 E7 的宪章原则锚定;被 E8 全部条目钉死;其违规观察落为 E9。

---

## E2 面向用户界面类(User-Facing Surface Class)

**物化位置**: E1 的 `surface_class_map` 表(枚举真源)+ 8 个规则真源文件各 1 行指针  
**基数**: **11 类**,去重后落在 **8 个文件**(裁定见 `research.md` D-3)

| 字段 | 形态 | 约束 |
|---|---|---|
| `class_id` | ①…⑪ | 封闭集;扩展 MUST 只经修订 E1 |
| `class_name` | 短名 | 11 个名字逐字取自 FR-014 |
| `rule_source_path` | 仓库相对路径 | MUST 存在;`confirmation-gates.md` 一行覆盖 ①②⑩⑪ |
| `reader_baseline_override` | 可选散文 | 缺省即适用 E6 的全局基准;声明处生效、MUST NOT 回写 E1(FR-037) |
| `pointer_line` | 规则真源文件内 1 行 | 每文件**含且仅含一行**指向 STR-002(SC-004) |

**11 → 8 映射**(实测裁定):

| 文件 | 覆盖类 |
|---|---|
| `shared/guidelines/confirmation-gates.md` | ①②⑩⑪ |
| `shared/workflow/feedback-step.md` | ③ |
| `shared/patterns/interview-pattern.md` | ④ |
| `templates/commands/clarify.md` | ⑤ |
| `shared/guidelines/requirements-guidelines.md` | ⑤⑦ |
| `shared/guidelines/proactive-trigger.md` | ⑥ |
| `skills/summarize-project/references/reporting-playbook.md` | ⑧ |
| `shared/workflow/glossary.md` | ⑨ |

**已记录的真源缺口**(不在本特性内补):类 ⑦ 的 plan/tasks 侧实测零措辞规则;类 ⑩ 无专属真源,裁定归 `confirmation-gates.md:62-66`。

---

## E3 许可行话条目(Permitted-Jargon Entry)

**物化位置**: E1 的白名单节  
**基数**: **≥5** 条(FR-005 列举的下限),封闭条件集

| 字段 | 形态 | 约束 |
|---|---|---|
| `condition` | 一句可判定条件 | MUST 可判定,MUST NOT 为"尽量少用"一类形容(FR-007) |
| `basis` | 依据短语 | 例:读者可能数天后单独读到本条 |
| `example` | 可选 | 正例 |

FR-005 列举的 5 条:① 用户已先用的术语 ② 词汇表 canonical 术语(该消费单元内首次出现就地注解)③ 用户 MUST 逐字键入/复制的标识符 ④ 用户自身项目/领域业务术语 ⑤ 输出格式自身定义且同时具名的短形式。  
**白名单之外一律违规**(FR-007)——这是"不能完全杜绝 jargon"的可判定落地形态。

---

## E4 禁用行话条目(Forbidden-Jargon Entry)

**物化位置**: E1 的黑名单节  
**基数**: **≥4** 条(FR-006 列举的下限),封闭条件集

| 字段 | 形态 | 约束 |
|---|---|---|
| `condition` | 一句可判定条件 | MUST 可判定 |
| `internal_identifier_class` | 内部标识类别 | 例:引擎/脚本/函数调用形态、分级码、字段名、库表列名 |
| `reader_facing_rewrite` | 可选改写映射 | 由 E4 的**实例来源**提供(见下) |

FR-006 列举的 4 条:① 存在用户视角途径时的引擎/脚本/函数内部调用形态 ② 内部代号/分级码/字段名/库表列名渗入面向读者正文 ③ 该消费单元内首次出现却无就地注解的缩写 ④ 以代码符号名充当行为概念名的提问。

**实例来源(FR-022 的提升结果)**: `skills/summarize-project/references/reporting-playbook.md` §1.7(`:109-113`)的内部标识黑名单(`T1–T5`、`E1–E5`、`RC-*`、`CG-*`、`§编号`、`M-*`、引擎字段名、库/表/列/SQL、脚本名)与读者向改写映射(`unknown-schedule` → 「无计划日期,无法判定延期」)提升进 E1 作为条目 ② 的实例来源;提升后 §1.7 收敛为指针,MUST NOT 保留第二份独立黑名单(SC-014)。

**E3/E4 的临界裁定**(规格 Edge Cases 已载,此处为结构化落地):无用户视角途径时 → E3 ③ 优先,原始标识符保留但标注为引擎细节;用户先用行话 → E3 ① 优先,MUST NOT 降级改写;白话改写损失精度 → 精度优先,保留术语并就地注解;机器消费的消息 → 不属任何 E2 类,本纪律不适用。

---

## E5 上下文界项(Context Bound Item)

**物化位置**: E1 的上下文下限节 + 上限与裁决顺序节  
**基数**: 下限 **≥3** 项(FR-009)、上限 **≥3** 约束(FR-010)、裁决顺序 **≥2** 条(FR-012)

| 字段 | 形态 | 约束 |
|---|---|---|
| `direction` | `floor` \| `ceiling` \| `adjudication` | 三态封闭 |
| `content` | 一句规范陈述 | — |
| `applies_to` | E2 类 id 集合或"全部" | — |
| `reconciliation` | 与既有纪律的和解方式 | `direction=floor` 且与摘要优先或单行约束冲突时 **MUST** 非空(FR-012) |

**下限三项**(FR-009):为何此刻出现 / 该决定将改变什么 / 用户可以做什么(确切用户视角途径或编辑入口);门控类另加不可撤销后果与可逆性。执行报告三要素的定义**仍归** `confirmation-gates.md:58-60`,E1 只引用(FR-009)。

**上限三约束**(FR-010/FR-011):承载方式 = 陈述决定所依赖的事实 + 以路径引用其余一切;非阻塞建议保持单行(形态真源 `proactive-trigger.md:47`,只引用);MUST NOT 把机器管理数据文件原文当上下文注入(Token 效率纪律 摘要优先,只引用)。

**裁决顺序两条**(FR-012,均为已点名的冲突):① 下限 vs 非阻塞单行 → 属**不同界面类**,不折叠;② 下限 vs 摘要优先 → 陈述**派生事实** + **路径引用**,不注入原文。

**程度形态裁定**(clarify R2-Q3=A):取**定性上限 + 沿用各界面既有数值约束**,MUST NOT 新增逐类或全局裸数值。**已知代价经知情接受**:门控确认提示与流程收尾报告两类无长度界;接受条件 = 长度不设界但**形态**设界(复述工件即违规,不论长短)。升级路径 = 在该类真源处声明覆盖值(E6 同型协议),不回写 E1。

---

## E6 基准读者与机械判据(Baseline Reader & Mechanical Verdict Test)

**物化位置**: E1 的基准读者与覆盖协议节 + 机械判据节  
**基数**: 全局基准 **恰好 1**;类级覆盖 **≤2**(SC-018 断言声明总数 ≤3)

| 字段 | 形态 | 约束 |
|---|---|---|
| `global_baseline` | 一句定义 | = 未在本会话打开过本仓库、但具备该项目领域知识的人(FR-037) |
| `override_sites` | ≤2 处 | 只在对应界面类的规则真源文件内声明;声明处生效、MUST NOT 回写 E1 |
| `verdict_tests` | ≥2 条判句 | 行话侧 1 条 + 上下文侧 1 条;MUST 使两个独立评审者得出同一结论(FR-013) |
| `consumption_unit` | 一句定义 | 就地注解义务的计账粒度;按消费单元计而非按会话计(FR-008) |

**已知的两处覆盖**(实测其今天的表述):类 ⑦ = "非技术干系人 / 业务干系人"(`requirements-guidelines.md:24,101`);类 ⑧ = "不读代码也能看懂的外部读者"(`summarize-project` 各层参考文档)。三种既有基准表述 MUST 收敛为 1 全局 + ≤2 覆盖(FR-037、SC-018)。

**判据形态**: 对齐房子的"粗体机械测试"先例(`one-source-of-truth.md:29`、`ask-record-repeat.md:97`),即一句可执行的判问,而非打分表。两条判问:`这个术语能不能归入白名单某一条?`(行话侧)、`读者要不要翻页才能行动?`(上下文侧)。

---

## E7 宪章原则导出(Constitution Principle Export)

**物化位置**: `templates/constitution-template.md`(2 条新原则)+ `templates/commands/constitution.md` 的 `MUST include` 清单(2 条新条目)+ `.specify/memory/constitution.md`(1 条新原则)  
**基数**: 模板 11 → **13**;活动宪章 14 → **15**

| 字段 | 形态 | 约束 |
|---|---|---|
| `title` | `### <罗马数字>. <Title Case 名称>` | STR-003 / STR-006 **逐字**;守卫按完整标题匹配 |
| `lead_sentence` | 一句以冒号结尾的主张 | — |
| `bullets` | 3–6 条 MUST/MUST NOT 要点 | 硬折行 <100 字符(`constitution.md:166`) |
| `anchor_bullet` | 其中 1 条 | MUST 锚定 STR-001 并写明 "reference it, do not restate it"(先例 `:103-106`) |
| `scope_limit_bullet` | 其中 1 条 | MUST 声明不新增机制(先例 `:110-111`) |
| `blank_line` | 恰好 1 个 | `constitution.md:167` |
| `rationale` | `Rationale:` 段 1–4 句 | — |
| `double_landing` | 布尔对 | 模板侧 ∧ 命令侧 MUST 同时为真(FR-025/FR-035) |

**编号裁定**(`research.md` D-9):模板 **XII = STR-006(回流)、XIII = STR-003(新增)**,使模板与活动宪章的相对顺序一致(活动宪章 XIV = OneSource 已存在、新增 XV = Comprehension)。守卫 MUST NOT 钉死罗马字面量。

**命名冲突防线**(`research.md` D-5):命令 `:91` 既有 **"Code as the Single Source of Truth"** 与 STR-006 **"One Source of Truth (Authority & Reference Discipline)"** 是**不同原则**(活动宪章 XIV 的 Rationale `:163` 已显式区分),二者共享子串 ⇒ 匹配 MUST 用完整标题的**集合成员判定**,MUST NOT 用子串包含。

**版本**: 活动宪章 `1.11.0`(`:215`)→ **`1.12.0`**(MINOR,依 `templates/commands/constitution.md:66`),并前置 Sync Impact Report(`:142-148`)。

**下游自动传导**: `templates/plan-template.md:31-42` 的 Constitution Check 按 `:37` "Do NOT hard-code principle names" + `:38-39` 动态枚举 ⇒ **零改动**自动纳入;FR-026 要求实测验证(`quickstart.md` 场景 5)。

---

## E8 漂移守卫(Drift Guard)

**物化位置**: `tests/contract/` 的 4 个新文件 + 1 个扩展文件;条款编号由 `contracts/` 的 5 份文档提供  
**基数**: 5 份契约(条款编号区间见各文件头部声明;跨文件总数派生方式见 `plan.md` § Phase 1 摘要,MUST NOT 在此手写)/ 5 个测试文件

| 字段 | 形态 | 约束 |
|---|---|---|
| `guarded_surface` | 受测表面 | 5 个:真源文档 / 镜像一致性 / 常驻章节 / 宪章双落点 / 界面类指针(FR-029) |
| `assertion_kind` | 断言类型 | 存在性 / 镜像字节相等 / 所有权声明 / 节齐备 / 唯一性 / 项目中立性 / 单源扫描 / 双落点 / **零阻塞模式命中** |
| `legitimate_duplicate_exemptions` | 豁免集 | 机械副本(镜像、4 棵按工具树、生成索引)与测试钉死字面量(`one-source-of-truth.md:33-41` 承认的两类) |
| `mutation_probe` | 变异式抽查 | 人为删除任一受测表面后测试 MUST 失败(SC-009/SC-015)——证明守卫**有效**而非仅存在 |

**形态**(实测 `test_one_source_of_truth.py` 与 `test_token_efficiency_discipline.py`):独立 `pathlib` + `pytest`,`pytestmark = pytest.mark.contract`,`ROOT = Path(__file__).resolve().parents[2]`,组标识用 `# --- C-N: … ---` 横幅或 `test_cN_*` 函数名,**不导入** `tests/conftest.py` 或 `tests/script_api.py` 的 fixture;需在测试内调用扫描器时用 `test_ask_record_repeat.py:41,106-108` 的内联 `importlib` 先例。

**分裂约定**(`research.md` D-11,取 `test_proactive_trigger_discipline_doc.py` / `_section.py` 先例):文档侧与章节侧**显式不重叠**。

---

## E9 可理解性观察条目(Comprehension Observation Entry)

**物化位置**: 既有 `.specify/memory/feedback/` 存储,经**未修改**的 `feedback-utils.py` 写入  
**基数**: 0…n(干净运行为 0)

| 字段 | 形态 | 约束 |
|---|---|---|
| `marker` | 稳定字面量 STR-005 = `user-facing-comprehension` | MUST 内嵌于正文,供 `--action list --contains` 检索聚合(FR-036) |
| `unit_id` / `unit_type` | 既有引擎字段 | 沿用既有归属解析 |
| `observation` | 观察事实散文 | MUST NOT 编造计数或数值 |

**红线**(FR-036):干净运行 MUST NOT 追加空洞观察条目;MUST NOT 阻塞宿主流程;MUST NOT 追加对用户的提问。形态对齐 `token-efficiency.md:54` 的 `token-efficiency` 标记先例。

---

## 校验规则(Validation Rules)

四组,全部由 E8 的契约测试机械执行。

### V1 真源文档结构(E1)

- **V1.1** `shared/guidelines/user-facing-comprehension.md` 存在,且与 `.specify/shared/guidelines/` 下同名文件 `read_bytes()` 相等。
- **V1.2** 前 8 行含所有权声明,且同时含 `single source of truth` 或"唯一定义处/唯一真源"语义 **与** `MUST NOT copy` 或"MUST NOT 复制"语义。
- **V1.3** 七个 H2 节全部存在(白名单 / 黑名单 / 下限 / 上限与裁决顺序 / 机械判据 / 界面类枚举 / 基准读者与覆盖协议)。
- **V1.4** 全文含 MUST 与 MUST NOT 关键词各 ≥1 次;含范围限制子句(不新增机制语义)。
- **V1.5** 白名单 ≥5 条、黑名单 ≥4 条、下限 ≥3 项、上限 ≥3 约束、裁决顺序 ≥2 条、判问 ≥2 条;**消费单元定义恰好 1 条**(E6 的第 4 个字段,FR-008),且白名单 ② 与黑名单 ③ 的转述 MUST 保留"该消费单元内"限定词。
- **V1.6** `surface_class_map` 恰为 11 行,类名逐字匹配 FR-014,且 8 个 `rule_source_path` 全部存在。

### V2 常驻章节(E1 的投递面)

- **V2.1** `templates/instructions-template.md` 与 `.specify/templates/instructions-template.md` **各含且仅含一次** STR-004 标题,且节体含 STR-001 指针。
- **V2.2** 两份模板 `read_bytes()` 相等。
- **V2.3** 新标题逐字出现在 `.specify/instructions.md`(增量调谐已重跑)。
- **V2.4** 节体 ≤25 行、无 `###` 子标题、零 `/speckit.` 命令形式与参数形式。
- **V2.5** 节体**不内联** E1 的七个 H2 节名(非内联断言,对齐 `test_one_source_of_truth.py:125-131`)。
- **V2.6** 新章节**不在**被钉死的位置窗口内(`## Documentation Map` → `## Proactive Flow Trigger` → `## Fact, Correctness & Logic Checks (Input Sanity)` 三者的相对顺序不变)。

### V3 收敛与指针(E2/E3/E4)

- **V3.1** 8 个规则真源文件各含**且仅含一行**指向 STR-002 的指针。
- **V3.2** 单源扫描:`shared/` + `templates/` + `skills/` 下以**内容形态**复述 E1 规则(白名单条件 / 黑名单条件 / 下限项 / 上限约束 / 判问)的位置数为 **0**;豁免 = 机械副本 + 测试钉死字面量。
- **V3.3** `interview-pattern.md:125-126` 两条模式特有规则**原文保留**;`:255` 不可丢弃清单含新指针;`:121-124` 已收敛为指针。
- **V3.4** `feedback-step.md:89-90`/`:113-115`/`:141` 三处既有规则**保留未删**。
- **V3.5** `confirmation-gates.md` 的 `:7-12`、`:14-21`、`:23-41`、`:43-45`、`:47-52` **逐字未改写**(FR-017);`:68` 已收敛为指针**且仍含** `非阻塞` 与 `自动传输` 两个字面量(既有测试 `test_confirmation_gates_execution_report.py:44-46` 仍须通过)。
- **V3.6** `reporting-playbook.md` §1.7 已收敛为指针,且 `shared/` + `skills/` 下独立黑名单副本数为 **0**;`:309` 落盘门禁仍在。
- **V3.7** 项目中立性:随包分发的 E1 与两个模板文件中,本仓专有名称(`spec-kit`、`specify-cli`、`specify_cli`、`cloud-native-ai`)命中数为 **0**。

### V4 导出与预算(E7/E8)

- **V4.1** 宪章模板含 STR-003 与 STR-006 两条原则,各结构合规(标题形态 / 冒号结尾主张 / 3–6 要点 / 恰好一个空行 / `Rationale:` 段 / 折行 <100 字符 / 含锚定要点 / 含范围限制要点)。
- **V4.2** **具名双落点观察名单**中每个完整标题**同时**属于模板标题集与命令 `MUST include` 名称集(集合成员判定,非子串);名单初始 = {STR-003, STR-006}。
- **V4.3** `Code as the Single Source of Truth` 与 STR-006 **不被判为同一原则**(D-5 冲突防线)。
- **V4.4** 活动宪章含 STR-003 对应原则,版本前两段 ≥ `(1, 12)`,且文件头部含 Sync Impact Report。
- **V4.5** `scan-confirmation-gates.py` 实跑:`total == 23` 且 `violations == []`;`POLICY_DOCS` 与 `SELF_REL` 字面**未被修改**。
- **V4.6** E1、新常驻章节、两条新宪章原则三处文本的 `BLOCKING_RE` 命中数均为 **0**。
- **V4.7** 无新增可执行检查器/评分器/台账:本特性新增文件中可执行脚本数为 **0**(新增 `.py` 仅限 `tests/contract/`)。

---

## 状态机(State Machines)

### S1 指针接入态(每个规则真源文件)

```
unlinked ──(加 1 行指针)──▶ linked
linked   ──(内容形态复述被检出 V3.2)──▶ drifted ──(改回引用)──▶ linked
```

- `unlinked`:文件不含指向 STR-002 的指针。**初始态 = 全部 8 个文件**(实测今天 0/8)。
- `linked`:含且仅含一行指针,且不以内容形态复述 E1 规则。**终态**,由 V3.1 + V3.2 钉死。
- `drifted`:含指针但另有内容形态复述(即"既指又抄")。V3.2 检出后 MUST 回到 `linked`——修复方向是**删除复述**而非删指针(FR-031 / Principle XIV `:160` 的"把副本变成引用")。
- **不可达转移**:`linked → unlinked`(删指针)由 V3.1 直接拦下。

### S2 观察名单双落点态(每条名单内原则)

```
absent-both ──(FR-028 回流)──▶ landed-both
landed-both ──(任一侧被删)──▶ landed-one ──(V4.2 失败,阻断)──▶ landed-both
```

- `absent-both`:两侧均无。**STR-006 的初始态**(实测 `grep -c "One Source"` 在两个模板文件双双为 0)。
- `landed-both`:模板侧 ∧ 命令侧同时存在。**终态**,由 V4.2 钉死。STR-003 与 STR-006 均须达此态。
- `landed-one`:只落一侧 —— 这正是 Principle XIV 今天所处的态,也是本状态机存在的理由。V4.2 使其**不可停留**(测试失败)。
- 守卫按**完整标题**判定,故 `landed-one` 不会因罗马数字不同而误判为 `landed-both`(FR-035 / D-9)。
