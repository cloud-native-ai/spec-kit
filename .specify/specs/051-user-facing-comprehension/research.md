# Phase 0 Research: 面向用户可理解性纪律(Feature 051)

**Date**: 2026-09-17  
**Method**: 全部结论为**仓库内部实测**(源码阅读 + 命令实跑),无外部源评估。每个决策附实测证据;凡推翻需求阶段陈述的,已在 `requirements.md` 的 `## Clarifications` > `### Session 2026-09-17(第三轮)` 就地订正。

---

## D-1 真源文档身份与落点

**决策**: `shared/guidelines/user-facing-comprehension.md`(STR-002),镜像 `.specify/shared/guidelines/user-facing-comprehension.md`(STR-001)。

**实测依据**:
- `scripts/python/sync-mirrors.py:72-78` 的 `MIRROR_PAIRS` 含 `("shared", ".specify/shared", False, set())`(`:77`),`:83-94` 以 `rglob("*")`(`:86`)发现全部文件 ⇒ **无 manifest、无逐文件注册**,新文件自动被拾取。
- `pyproject.toml:37` `"shared" = "specify_cli/shared"` 与 `src/specify_cli/__init__.py` 的 `_CORE_SPECIFY_ASSETS`(列表字面量在 `:1075-1083`,含 `".specify/shared"` 于 `:1081`)均为**目录级** ⇒ 打包与 init 拷贝无需改动。
- `tests/contract/test_shared_reference_directory.py:19-22` 的 `TYPED_DOCS["guidelines"]` 是 `issubset` 断言(`:43`)⇒ 新文件静默通过;可选择性加入以钉死存在性。
- 现状:`shared/guidelines/` **11 个文件**(实测),落地后 12 个。

**需求阶段行号订正**:`_CORE_SPECIFY_ASSETS` 实际在 `:1075-1083`(规格未引用该符号,无需改正文);`_INSTRUCTIONS_FILE_MAP` 实际在 **`:1187-1194`**、`_check_instructions` 实际在 **`:1212-1218`**——需求阶段记录的 `:1090-1097` / `:1115-1121` **错误**(那两处分别是 `is_core_asset_initialized` 与 `get_canonical_command_stems`)。本规格未引用这两个符号,故只在此记录以免后续阶段沿用错行号。

---

## D-2 门控预算处置:**设计规避**,不改扫描器

**这是本特性最硬的机械约束,也是唯一可能一次打爆两个契约测试的地方。**

**实测基线**(2026-09-17 实跑):

```
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
EXIT=0
```

- 冻结基线 `.specify/specs/044-reduce-confirmation-flows/baseline.json:2` → `"total": 93`。
- 上限:`tests/contract/test_confirmation_gates_sweep.py:63-71` 计算 `cap = 93 × 0.25 = 23.25`,`assert total <= cap` ⇒ **最大可通过整数为 23**。
- **整数余量 = 0**。Feature 050 的冻结文件 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json:14-24` 独立记录了同一结论(`"total": 23, "integerHeadroom": 0, "cap": 23.25`)。
- **第二道更严的钉子**:`tests/contract/test_proactive_trigger_section.py:288-306`(`test_c11_gate_scan_total_unchanged`)断言 `total == 23`,是**相等**而非 ≤。⇒ 任何一处新增命中同时打爆两个测试。

**扫描范围**(实测 `scan-confirmation-gates.py`):
- `SCAN_DIRS = ("templates/commands", "skills", "shared")`(`:35`),递归 `rglob("*.md")`(`:85`)⇒ **`shared/guidelines/` 在范围内**(证据:`shared/guidelines/task-complexity-rubric.md` 出现在今天的 23 条中)。
- `SCAN_ROOT_FILES = ("templates",)`(`:36`),非递归 `glob("*.md")`(`:94`)⇒ **根级 `templates/instructions-template.md` 与 `templates/constitution-template.md` 都在范围内**。
- `SKIP_DIR_PARTS`(`:37`)含 `.specify/.claude/.qoder/.github/.opencode` ⇒ 镜像与按工具副本**不重复计数**。
- 豁免仅两处:`SELF_REL = shared/guidelines/confirmation-gates.md`(`:38`)与 `POLICY_DOCS = {reconcile-pattern.md, interview-pattern.md}`(`:41-44`),在 `:115` 整体跳过。
- **关键**:`constitution-template.md` 的路径命中 `GOVERNANCE_PATH_PATTERNS`(`:71-76` 含 `constitution-template`)⇒ 其命中被归类 `governance_kept`,但 **`governance_kept` 仍计入 `total`**,不豁免。

**候选方案与取舍**:

| 方案 | 可行性 | 取舍 |
|---|---|---|
| (a) 把新真源文档登记进 `POLICY_DOCS` | 可行(需改扫描器代码一行) | **只救真源文档,救不了两个模板文件**——把整个 `instructions-template.md` 或 `constitution-template.md` 加进豁免集会掩盖那 17 个章节 / 11 条原则里的真实回流,豁免面过宽 |
| (b) **设计规避:三处新增文本零 `BLOCKING_RE` 命中** | 可行,零代码改动 | **采用**。与房子先例一致:`test_proactive_trigger_discipline_doc.py::test_c3_zero_blocking_pattern_hits` 对 050 的纪律文档钉死零命中;`test_ask_record_repeat.py:233-249` 对其文档 + 两个模板章节同样钉死零命中 |

**决策**: 取 **(b)**。三处新增文本(真源文档、指令模板新章节、宪章模板两条新原则)MUST 零 `BLOCKING_RE` 命中,各由契约测试钉死。**FR-032 的条件前提("若真源文档为说明违规形态而引用任何命中阻塞模式的措辞")因此不成立 ⇒ 不改 `POLICY_DOCS`,本特性对扫描器零代码改动。** SC-012(计数完全不变)由构造满足。

**必须规避的字面形态**(17 条,实测 `:46-64`;逐条列出以便撰写时自检):

`等待用户确认` · `等待确认` · `用户确认后才` · `确认后才(执行|写入|落盘|启动|持久化)` · `显式用户确认|explicit user confirmation` · `wait for user confirmation` · `MUST NOT execute before confirmation` · `stop and confirm` · `after user confirmation|after confirmation` · `[Cc]onfirm before` · `[Pp]roceed[^\n]{0,40}yes/no` · `preview\s*(?:→|->)\s*confirm\s*(?:→|->)\s*execute` · `confirmation gate|确认门[禁控]` · `Confirm and persist|确认并落盘|合并确认` · `Execute on Confirmation` · `interactive confirmation` · `inviting the user to submit collected feedback`

**两个高危陷阱**:
1. **`确认门[禁控]`**——本纪律必须频繁谈论门控提示。写成 `确认门控` / `确认门禁` 即命中。⇒ 统一用 **`门控`** / **`门控提示`** / **`前置确认`**;`门控确认提示` 的字序是「门-控-确-认」,**不含** `确认门`,安全。
2. **`classify()` 第 3 条**(`:98-109`):命中 `BLOCKING_RE` 且行内**不含** `执行/写入/落盘/启动/继续` 五个中文字面之一、且无破坏性关键词、路径不命中 governance ⇒ 判为 **`reversible`**,这不仅使 `total` +1,还会**额外**打爆 `test_confirmation_gates_sweep.py:54-60`(`test_no_reversible_gates_remain_blocking`)并使扫描器在 `--baseline` 下 **exit 2**。本纪律文档必然频繁出现「执行」「写入」,故该路径比单纯计数更易触发 ⇒ 规避是**强制**的,不是优化。

**注**:`classify()` 的 reversible-context 判定**只认那五个中文字面**,英文 `execute` / `execute before` **不算**(`:106`)。撰写英文反例时不可依赖英文词提供豁免。

---

## D-3 11 类界面 → 8 个规则真源文件(归属裁定)

FR-014 枚举 11 类。实测其规则真源**不是 11 个文件**——存在共管与缺口:

| # | 界面类 | 规则真源文件 | 指针插入点(实测行号) | 备注 |
|---|---|---|---|---|
| ① | 门控确认提示 | `shared/guidelines/confirmation-gates.md` | 头部所有权区 `:3-5`(紧邻 `:5` 既有的"命令模板与技能 MUST 以单行引用接入本文档"规则) | FR-017 冻结 `:7-12` 两级判据、`:14-21` 破坏性清单、`:23-41` 治理保留清单、`:43-45` 存疑从严、`:47-52` 回流约束 ⇒ 指针**不能**进这些节内 |
| ② | 门控执行报告 | **同上**(共管) | `## 执行报告` `:54-68`;三要素 `:58-60` 仍归此处拥有(FR-009 只引用) | `:68` 按 FR-018 提升后收敛为指针 |
| ③ | 反馈阈值/提交通知 | `shared/workflow/feedback-step.md` | 头部所有权段 `:1-9`(所有权声明在 `:3`),或 `## Threshold prompt protocol` 起始 `:106`(紧邻 `:113-115`) | 既有三处规则 `:89-90`/`:113-114`/`:141` **保留**为实例(FR-019;`:115` 属改写项、不在保留集——订正发现项 B-09,本行原写 `:113-115` 与其所引的 FR-019 矛盾) |
| ④ | 访谈提问 | `shared/patterns/interview-pattern.md` | `Comprehension rules` 块 `:119-126`;**另需**改嵌入契约不可丢弃清单 `:255` | `:121-124` 四条收敛为指针;`:125-126`(每问一决策、问 what 不问 whether)**原文保留**(FR-021);反模式 `:280-281` 一并收敛 |
| ⑤ | 澄清提问与选项表 | **两个共管**:`templates/commands/clarify.md` + `shared/guidelines/requirements-guidelines.md` | clarify.md 借用段 `:70`(把借用扩到行话半侧);requirements-guidelines.md 的 `[NEEDS CLARIFICATION]` 呈现步骤 `:70-72` 或模板块 `:72-88` | FR-020 显式点名两个表面;clarify 既有裁定(封闭式、选项表 + Recommended、不采纳开放式提问)不变 |
| ⑥ | 主动流程建议行 | `shared/guidelines/proactive-trigger.md` | `## Suggestion Shape` `:45-55`(在 `:47`),**或**头部"归属不在本文档"要点列表 `:11-15`(已有三条"只以路径引用",含 `:15` 指向 confirmation-gates.md)——后者是加第四条的自然位 | 指令模板 `:31` 的镜像 MUST 保持摘要形态,不内联 |
| ⑦ | 面向干系人的需求/规划/任务工件 | `shared/guidelines/requirements-guidelines.md`(**仅需求侧**) | `## General Guidelines > Quick Rules` `:97-102`(在 `:101`) | **实测缺口**:`templates/plan-template.md` 与 `templates/tasks-template.md` 的 stakeholder / plain-language / business 检索**零命中**——plan/tasks 侧今天**无任何措辞规则**。裁定见下 |
| ⑧ | 面向外部读者的项目总结报告 | `skills/summarize-project/references/reporting-playbook.md` §1.7 `:109-113` | §1.7 正文 `:111`;落盘门禁 `:309` 保留但改指提升后的来源 | 次级实例面:`references/project-overview.md:22,38,51`、`references/consistency-rules.md:31` |
| ⑨ | 词汇表校正的对外呈现 | `shared/workflow/glossary.md` §1 `:17-28` | surface-it 要点 `:23-24`(或节首 `:17`) | 出向 canonical 术语规则在 `templates/commands/interview.md:30`,属类 ④ 的载体而非本类真源 |
| ⑩ | 流程收尾报告 | **无专属真源(缺口)** → 裁定归 `shared/guidelines/confirmation-gates.md` § 执行报告 的粒度与形态规则 `:62-66` | 由 ① 的头部指针覆盖 | 实测规则分裂在 `confirmation-gates.md:62-66`(琐碎并入 / 合并呈现)与 `feedback-step.md:86-93`(收尾提交提示)。FR-011 已记录本类**无长度界** |
| ⑪ | 失败如实报告 | `shared/guidelines/confirmation-gates.md:66`(在 § 执行报告 内) | 由 ① 的头部指针覆盖 | 已有守卫:`test_confirmation_gates_execution_report.py:38-41` 断言 `失败` + `中间产物` |

**去重后 = 8 个文件**:`confirmation-gates.md`(①②⑩⑪)、`feedback-step.md`(③)、`interview-pattern.md`(④)、`clarify.md`(⑤)、`requirements-guidelines.md`(⑤⑦)、`proactive-trigger.md`(⑥)、`reporting-playbook.md`(⑧)、`glossary.md`(⑨)。

**两处缺口的裁定**(不扩大范围):
- **类 ⑦ 的 plan/tasks 侧**:实测零措辞规则。裁定 `requirements-guidelines.md` 为类 ⑦ 的**唯一真源**(它是今天唯一存在的规则源),缺口**如实记录**而**不在本特性内**给 `plan-template.md` / `tasks-template.md` 新增措辞规则——那属新增范围,且这两个模板的读者纪律与需求工件不同(计划面向实现者,不面向干系人)。
- **类 ⑩**:裁定 `confirmation-gates.md` § 执行报告 为真源(它已拥有定义收尾报告形态的粒度规则),**不新造文档**。

**指针数量裁定**:`confirmation-gates.md` 一类文件覆盖 4 个界面类。SC-004 要求"各含且仅含一行指针"⇒ 采用**一行头部指针覆盖 ①②⑩⑪**,而非四条分节指针。理由:FR-017 冻结了该文档的判据各节,头部所有权区是唯一可安全落笔处;且一行指针正是 FR-015 的字面要求。**8 个文件 × 各 1 行指针 = 8 行**,映射关系以真源文档内的"界面类 → 真源"表承载(该表是 11 类枚举的一部分,不是第二份指针)。

---

## D-4 `confirmation-gates.md:68` 的提升机制(FR-018 + FR-034)

**实测现状**:`:68` 是 `## 执行报告`(`:54`)的尾段,verbatim:「收尾阶段达阈值触发的反馈提交提示 MUST 为非阻塞一次性提示(附 `/speckit.feedback package` 用户视角途径,不展示 `feedback-utils.py` 引擎原始调用),MUST NOT 阻塞收尾,MUST NOT 自动传输任何内容。」

**既有守卫**:`tests/contract/test_confirmation_gates_execution_report.py:44-46`(`test_nonblocking_submission_notice_rule`)**只**断言 `非阻塞`(`:45`)与 `自动传输`(`:46`)两个字面量——**未**断言 `用户视角途径` / 不暴露引擎调用子句。FR-034 的前提成立。

**提升方案**:
1. 一般化规则(**存在用户视角途径时 MUST NOT 暴露引擎/脚本内部调用形态;无途径时保留标识符但标注为引擎细节**)落进真源文档的**黑名单第 ① 条**(FR-006 ①)与**白名单第 ③ 条**(FR-005 ③)。
2. `:68` 收敛为:保留 `非阻塞` / `自动传输` 两个字面量(既有测试仍须通过),把"用户视角途径 / 不展示引擎原始调用"改为指向真源文档的单行引用。
3. **FR-034 的断言落点**:扩展 `test_confirmation_gates_execution_report.py`,断言 `confirmation-gates.md` 携带该指针;一般化规则本身的字面量断言落进新的纪律文档测试。
4. **门控预算安全**:`confirmation-gates.md` 是 `SELF_REL`(`:38`)⇒ **整体豁免计数**,编辑它不影响 `total`。✓

---

## D-5 宪章原则命名冲突(实测发现的高危陷阱)

`templates/commands/constitution.md` 的 `MUST include` 清单实测有 **5 条**(`:77-86` Documentation-First、`:87-90` Feature-centric development、**`:91-99` Code as the Single Source of Truth**、`:100-110` Documentation Naming & Location Conventions、`:111-125` Better-Harness Orientation),新块插在 **`:125` 与 `:126` 之间**(`:126` 是 step 3 的收尾要点,step 4 从 `:128` 开始)。

**冲突**:清单第 3 条名为 **"Code as the Single Source of Truth"**,与 STR-006 **"One Source of Truth (Authority & Reference Discipline)"** 是**两条不同原则**——活动宪章 XIV 的 Rationale(`:163`)已显式区分二者。二者共享子串 `Single Source of Truth` / `Source of Truth`。

**决策**:FR-035 的按名匹配 MUST 用**完整标题字符串**(含括注),MUST NOT 用子串包含。具体:
- 模板侧标题集 = regex `^### [IVXLC0-9]+\. (.+)$` 捕获组;
- 命令侧名称集 = regex `\*\*MUST include\*\* a principle for "([^"]+)"` 捕获组;
- 断言 = 观察名单中每个名字**同时**属于两个集合(集合成员判定,非子串判定)。

`Code as the Single Source of Truth` ∉ {`One Source of Truth (Authority & Reference Discipline)`},反之亦然 ⇒ 不混淆。

---

## D-6 FR-035 全称形式**不可实现**(实测推翻,已订正规格)

**实测**:
- `templates/constitution-template.md` 有 **11 条原则**(I–XI,`:14`–`:132`)。
- `templates/commands/constitution.md` 的 `MUST include` 清单有 **5 条**。
- **交集仅 3 条**:III Documentation-First、VIII Feature-Centric Development、IX Better-Harness Orientation。
- 清单另含 **2 条不在模板中**的原则:Code as the Single Source of Truth、Documentation Naming & Location Conventions。

⇒ 模板 ⊆ 清单 **假**(8 条反例);清单 ⊆ 模板 **假**(2 条反例)。**两个方向都不成立**,全称守卫会在既有原则上立即失败。

**语义辨析**:`MUST include` 清单的语义是"命令 bootstrap 时**至少**必须生成的原则"(`:77` 起,配合 `:40-41` 授权拒绝不相关模板原则),**不是**模板的镜像。二者本就允许不对称。

**决策**:FR-035 改为**具名双落点观察名单**(watchlist),初始 {STR-003, STR-006},扩展只经追加名单条目。已就地订正 FR-035 / SC-015 / SC-015 Source,并记入第三轮 Clarifications。**用户意图未被削弱**:XIV 在名单内,从任一侧删除它仍使 CI 失败——这正是 clarify R1-Q2 选 C 所要的证明力。

**旁证**:`tests/contract/test_one_source_of_truth.py:168-173`(`test_c8_constitution_principle_present`)今天用 regex `^### XIV\. One Source of Truth` 断言**活动宪章**,并**钉死了罗马数字 XIV**——FR-035 明确要求新守卫 MUST NOT 钉死罗马字面量,故新守卫与这条既有测试形态**不同**,不可复制。

---

## D-7 指令模板章节落位与同批义务

**实测**:`templates/instructions-template.md` 现有 **17 个顶级 `## ` 章节**(`:3, 8, 24, 34, 49, 59, 65, 73, 82, 94, 106, 122, 135, 139, 145, 151, 154`),另有 H1 `# Tool And Skills Usage Guide` 在 `:119`(增量调谐只按 `^## ` 切分,故该 H1 随前一节体一起传播)。活动 `.specify/instructions.md` 有 **18 个**(17 + 项目自有 `## Recurring Operational Lessons`)。

**被钉死的位置窗口**(不可插入其中):`## Documentation Map`(`:8`) → `## Proactive Flow Trigger`(`:24`) → `## Fact, Correctness & Logic Checks (Input Sanity)`(`:34`),由 `test_proactive_trigger_section.py:141-152` 与 `test_ask_record_repeat.py:220-227` 双向钉死。

**决策**:新章节 `## User-Facing Comprehension`(STR-004)插在 **`## Token Efficiency Discipline`(`:65-71`)之后、`## Dogfooding Practice`(`:73`)之前**——与同类纪律相邻(One Source Of Truth `:49`、Task Complexity Rubric `:59`、Token Efficiency `:65`),且在钉死窗口之外。模板章节数 17 → **18**。

**同批义务**(缺一即 CI 红):
1. `scripts/bash/generate-instructions.sh` 重跑 ⇒ `.specify/instructions.md` 含新标题。`test_instructions_section_propagation.py:34-42`(C-1)要求模板每个 `^## .+$` 标题**逐字**存在于活动文件(方向:模板 ⊆ 活动;只比标题不比节体)。该测试**不钉死章节总数**(实测无硬编码计数),活动文件多出项目自有章节被容忍。
2. `python3 scripts/python/sync-mirrors.py --write` ⇒ `.specify/templates/instructions-template.md` 与 `.specify/shared/guidelines/user-facing-comprehension.md` 逐字节镜像。`test_proactive_trigger_section.py:135` 与 `test_ask_record_repeat.py:185` 各自钉死 instructions-template 的镜像字节相等;`tests/contract/test_scripts_distribution_parity.py:71-87` 对**全树**跑 `sync-mirrors.py --check` 并断言 `returncode == 0` ⇒ 任何一处镜像缺失/漂移都使 CI 红。
3. 新章节体内**零 `BLOCKING_RE` 命中**(D-2)。

**实测当前镜像状态(改前基线)**:`python3 scripts/python/sync-mirrors.py --check` → **EXIT=0**,`ok templates/ == .specify/templates/ (22 files)`、`ok skills/ == .specify/skills/ (489 files)`、`ok agents/ == .specify/agents/templates/ (2 files)`、`ok scripts/ == .specify/scripts/ (104 files)`、`ok shared/ == .specify/shared/ (40 files)`,外加 18 条非致命 `note extra file only in mirror:`(17 × `.specify/skills/.migration-backups/layout-int-*/SKILL.md`,1 × `browser-utils/scripts/js/.temp-execution-*.js`)。`regen-command-copies.py --check` → **EXIT=0**。⇒ **改前基线全绿**,故本特性的镜像判据可以写成绝对形式("全树 `--check` EXIT=0"),无需 050 那样的 `--only` workaround。

---

## D-8 常驻章节的自约束(取自兄弟章节的既有钉子)

`test_proactive_trigger_section.py` 对 `## Proactive Flow Trigger` 章节钉死的约束,是本特性新章节应**自愿对齐**的房子形态(除 C-11 属全局预算、C-10 属该特性专有外):

| 既有钉子 | 位置 | 051 新章节是否沿用 |
|---|---|---|
| C-1 标题 + 指针在**两份副本**各出现且仅一次 | `:~100-130` | **沿用** |
| C-2 模板与镜像**逐字节相等** | `:135` | **沿用**(D-7 义务 2) |
| C-3 位置在钉死窗口内 | `:141-152` | **不适用**——051 章节**必须避开**该窗口 |
| C-4 节体 **≤25 行**、**无 `###` 子标题** | `:~155-170` | **沿用**(与规格 FR-003 的"2–5 条要点"一致) |
| C-5 节体内**零 `/speckit.` 命令形式与参数形式** | `:~175-185` | **沿用**——本纪律谈的是"不暴露引擎调用",章节自身更不该出现命令形式 |
| C-6 节体内**零 `BLOCKING_RE` 命中** | `:187-193` | **沿用**(D-2) |
| C-7 项目中立性 | `:~195-210` | **沿用**(FR-030) |

---

## D-9 宪章落点、编号与版本

**决策**:
- `templates/constitution-template.md`:在 Principle XI(`:132-141`)之后、`## [SECTION_2_NAME]`(`:143`)之前插入两条:
  - **XII = `One Source of Truth (Authority & Reference Discipline)`**(STR-006,回流)
  - **XIII = `User-Facing Comprehension (No Jargon, With Context)`**(STR-003,新增)
  - 模板原则数 11 → **13**。
- **顺序依据**:使模板与活动宪章的**相对顺序一致**——活动宪章已有 XIV = One Source of Truth,新增的是 XV = User-Facing Comprehension,即「OneSource 在前、Comprehension 在后」。模板取同序可避免两份名册读起来相反。
- 活动宪章 `.specify/memory/constitution.md`:新增 **XV = User-Facing Comprehension**(它已含 XIV,故只加一条),原则数 14 → **15**;版本 `1.11.0`(`:215`)→ **`1.12.0`**(MINOR,依 `templates/commands/constitution.md:66`「adding/removing/renaming principles = MINOR」),并前置 Sync Impact Report(`:142-148`)。
- **单条结构**(实测既有原则形态,以最短完整实例 XI `:132-141` 为范):`### <罗马数字>. <Title Case 名称>` → 一句以冒号结尾的主张 → 3–6 条 MUST/MUST NOT 要点(硬折行 <100 字符,`:166`)→ **恰好一个空行**(`:167`)→ `Rationale:` 段(1–4 句)。
- **唯一的 guideline 锚定先例**:`:103-106`(Better-Harness 锚定 `.specify/shared/guidelines/better-harness.md` 并写明 "reference it, do not restate it"),配套范围限制要点在 `:110-111`("adds orientation, not machinery: it MUST NOT justify new scoring systems, maturity reports, or tracking/recording engines")。两条新原则各按此形态写一条锚定要点 + 一条范围限制要点。
- **下游自动传导**:`templates/plan-template.md:31-42` 的 `## Constitution Check` 明写 `:37` "Do NOT hard-code principle names here"、`:38-39` 按 `### <roman-or-arabic-numeral>. <name>` 动态枚举、`:40-41` 每原则一行 ⇒ `plan-template.md` **零改动**。FR-026 要求实测验证,方式见 `quickstart.md` 场景 5。

---

## D-10 契约制品形态:结构契约文档,非 OpenAPI

本特性无 API、无运行时端点。按 050 的房子先例(`contracts/` 存放带 C-N 条款的**结构契约文档**),产出 **5 份**:

| 文件 | 守护对象 | 条款主题 |
|---|---|---|
| `contracts/discipline-doc.md` | 真源文档 | 存在性与镜像字节相等、所有权声明(前 8 行 + MUST NOT copy)、七节齐备(白名单/黑名单/下限/上限/机械判据/界面类枚举/基准读者)、RFC-2119 关键词、消费单元定义、覆盖协议、范围限制子句、项目中立性、零 `BLOCKING_RE` 命中 |
| `contracts/ambient-section.md` | 指令模板新章节 | 标题与指针在两份副本各一次、镜像字节相等、节体 ≤25 行且无 `###`、零 `/speckit.` 形式、零 `BLOCKING_RE`、不内联真源文档节名、位置在钉死窗口之外、项目中立性 |
| `contracts/surface-pointers.md` | 8 个规则真源文件 | 每文件含且仅含一行指针、11 类 → 8 文件映射表存在、两处搬家的收敛与保留项、`confirmation-gates.md` 的判据各节逐字未改写、`interview-pattern.md:255` 不可丢弃清单已含新指针 |
| `contracts/constitution-export.md` | 宪章双落点 | 两条新原则的结构合规(标题/主张/要点数/空行/Rationale/折行)、guideline 锚定要点、范围限制要点、**具名观察名单双落点**(D-5 的完整标题匹配)、活动宪章版本 ≥1.12、Sync Impact Report 存在 |
| `contracts/gate-neutrality.md` | 门控预算与零新机制 | 三处新增文本零 `BLOCKING_RE` 命中、`scan-confirmation-gates.py` 的 `total == 23` 且 `violations == []`、`POLICY_DOCS` 未被修改、无新增可执行检查器/评分器/台账 |

---

## D-11 测试文件组织(取既有分裂先例)

**实测先例**:`test_proactive_trigger_discipline_doc.py` 与 `test_proactive_trigger_section.py` 是**显式不重叠的分裂**(文档侧 vs 常驻章节侧),docstring 写明 "Maps to contracts/discipline-doc.md clauses C-1 … C-16"。

**决策**:沿用该分裂,新增 **4 个**测试文件 + 扩展 **1 个**既有文件:

| 测试文件 | 对应契约 |
|---|---|
| `tests/contract/test_user_facing_comprehension_doc.py` | `discipline-doc.md` + `gate-neutrality.md`(文档侧条款) |
| `tests/contract/test_user_facing_comprehension_section.py` | `ambient-section.md` + `gate-neutrality.md`(章节侧条款) |
| `tests/contract/test_user_facing_comprehension_pointers.py` | `surface-pointers.md` |
| `tests/contract/test_constitution_double_landing.py` | `constitution-export.md`(名称取通用形,因为它守护的是观察名单机制而非单一原则) |
| `tests/contract/test_confirmation_gates_execution_report.py`(**扩展**) | FR-034 的指针断言(D-4) |

**共同形态**(实测 `test_one_source_of_truth.py` 与 `test_token_efficiency_discipline.py`):独立 `pathlib` + `pytest`,`pytestmark = pytest.mark.contract`,`ROOT = Path(__file__).resolve().parents[2]`,组标识 `# --- C-N: … ---` 横幅或 `test_cN_*` 函数名,**不导入** `tests/conftest.py` 或 `tests/script_api.py` 的任何 fixture。门控扫描器如需在测试内调用,先例是 `test_ask_record_repeat.py:41,106-108` 的内联 `importlib` 加载(不是 `tests/script_api.py`)。

---

## D-12 两处搬家的确切编辑面

**搬家 A —— `shared/patterns/interview-pattern.md`(FR-021)**
- `:119` 保留 `**Comprehension rules (可理解性规则)**` 标题行,但把 `:121-124` 四条规则替换为**一行指针** + 一句"细则归真源文档"。
- `:125-126`(每问一决策、问 what 不问 whether)**原文保留**——二者不属可理解性纪律(FR-021 明令不吞并)。
- `:255` 嵌入契约不可丢弃清单**追加**"接入本纪律的指针"——实测该清单今天列了 write-through、决策记录持久化、撤回传播、自足开放式提问格式、事实/决策拆分、用户确认退出门,**未列 Comprehension rules**,故宿主收窄时它可以被合法丢弃(规格 Edge Case 已记录)。
- `:280-281` 两条反模式(`Context-free questions`、`Jargon and bare abbreviations`)收敛为一条指向真源文档黑名单/下限的短引用。
- **门控预算安全**:该文件在 `POLICY_DOCS`(`:41-44`)⇒ 整体豁免计数。✓
- **连带面**:`.specify/shared/patterns/interview-pattern.md`(镜像,`sync-mirrors.py`)。

**搬家 B —— `skills/summarize-project/references/reporting-playbook.md`(FR-022)**
- §1.7(`:109-113`)的内部标识黑名单与读者向改写映射(`unknown-schedule` → 「无计划日期,无法判定延期」)**提升进真源文档**,作为黑名单第 ② 条的**实例来源**;§1.7 正文收敛为指针。
- `:309` 的落盘门禁 `- [ ] **读者用语纪律已过**(§1.7)` 保留,但改指提升后的来源。
- 次级实例面收敛为指针:`references/project-overview.md:22`、`:38`、`:51`(其中 `:51` 的 `- [ ] 无内部黑话;外部读者不读代码也能看懂` 是**可机械核查的门禁形态**,提升后应保留在技能侧作为该类的落盘检查)、`references/consistency-rules.md:31`。
- **连带面**:`.specify/skills/summarize-project/`(镜像,489 文件对之一)。

**搬家 C(规格已含,一并列出)—— `confirmation-gates.md:68`**:见 D-4。

**机械副本(不手工改)**:`templates/commands/interview.md:30,153-154` 是手写源 ⇒ 手工收敛;其 4 棵按工具副本树(`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`)⇒ `python3 scripts/python/regen-command-copies.py` 再生(`:11-13`;仅处理目录已存在的工具,4 棵都存在)。

---

## D-13 FR-038 悬空指针义务的实现形态

**实测确认缺口**:`scripts/bash/generate-instructions.sh`(270 行)**全文无 `shared/` 同步逻辑**——它只做 tools JSON(`:34-45`)、instructions(`:88-192`)、glossary init(`:194-207`)、skills/tools 文档(`:209-219`)、废弃清理、symlinks(**`:235-267`**,需求阶段记录的 ~`:193-212` 错误)。真源文档只经 `src/specify_cli/__init__.py:2202` 的附加式 `shutil.copytree(..., dirs_exist_ok=True)`(`:2210-2214`)或 `sync-mirrors.py` 抵达。

**决策**:FR-038 的义务落在**文本层**而非脚本层——
1. 常驻章节的指针行附一句**获取途径说明**(重跑 init 或镜像同步),使章节自身在文档缺失时仍告诉读者怎么办;
2. 真源文档的守卫断言"章节与文档同批存在"——即 `test_user_facing_comprehension_section.py` 断言:若模板含 STR-004 章节,则 `shared/guidelines/user-facing-comprehension.md` **必须存在**;
3. SC-017 的"守卫覆盖全部 11 份既有 guideline"落成一条**遍历断言**:对指令模板中每个指向 `.specify/shared/guidelines/<x>.md` 的指针,断言 `shared/guidelines/<x>.md` 存在。这条今天就能通过(11 份都在),但它把窗口变成**受测**的,而不是靠运气。
4. **不改** `generate-instructions.sh`(Out of Scope 已裁定)。

---

## D-14 文档空间漂移点(手写 vs 生成)

**手写、需收敛或会静默漂移**:
1. `docs/reference/commands/interview.md` —— 规格只引了 `:65`,实测**三处**:`:65`(self-contained: ID + plain-language title + Context quote block)、**`:71-73`**(`## Question Format` 节,近乎逐字复述 `interview-pattern.md:81`)、**`:126-127`**(保证表两行:"Plain language, your vocabulary" / "Special terms glossed inline, every question")。该文件 `:5` 已声明模式文档为唯一真源,却仍以内容形态复述——正是本特性要修的形态。
2. `docs/reference/skills/feedback.md` —— 实测 **`:140-142`**(规格记 `:139-141`,已订正)。
3. `docs/reference/commands/requirements.md:63` —— "Write for business stakeholders, not developers"(类 ⑦ 的复述),**规格未引用**,是额外漂移点。
4. `docs/reference/agents/quality-loop.md:100` —— "jargon-heavy" 只出现在一句示例评审里,**非规则复述,无需动作**。
5. 其余 `docs/concepts`、`docs/tutorials`、`docs/contribute`、`docs/decisions`、`docs/tasks`、`docs/notes`、`docs/archive` 对相关模式**零命中**。

**生成、MUST NOT 手工编辑**:
- `docs/public/**` —— **Hugo 构建产物**。证据:`docs/hugo.toml`、`docs/layouts/`、`docs/static/` 存在;`skills/create-pages/references/hugo-site.md:22` 明写 "`docs/public/` | Hugo | Build output. Never committed, never documentation.";`git ls-files docs/public` = **0 个跟踪文件**,`git check-ignore docs/public` → 被忽略(经 `docs/.gitignore`)。⇒ 上面 1–3 项修好后需 Hugo 重建,`docs/public` 内的副本才会跟上;绝不手改。
- 4 棵按工具命令树 —— `regen-command-copies.py` 再生。
- `.specify/**` 镜像 —— `sync-mirrors.py`。

**裁定**:`docs/reference/**` 的 3 处收敛**在本特性范围内**(FR-016 裁定为全量接入,且它们是手写内容形态复述);`docs/public/` 重建**不在范围内**(生成物,由既有构建流程处理),但 `quickstart.md` 记一条验证步骤提醒重建。

---

## D-15 测试基线与一处分支状态相关的失败

**实测**:`python3 -m pytest tests/contract/ -q` → **24 failed, 1924 passed**(38.28s)。

- **23 条在 `.specify/specs/049-docs-reconcile/baseline-failed.txt`(47 条,其中 28 条属 `tests/contract/`)之内**:4× `test_agent_specific_config_commands`、1× `test_create_new_skill_contract`、1× `test_dogfooding_practice`、1× `test_no_nested_skills[.specify/skills]`、1× `test_shared_reference_rewrite`、10× `test_skill_home_workdir_template`、1× `test_token_efficiency_remediation_program_first::test_v004_mirror_identical`、4× `test_token_efficiency_remediation_summary_first::test_mirror_identical[V-001/002/003/005]`。
- **1 条不在任何冻结基线内**(049 的 47 条与 050 的 44 条均无):`test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`。
- **成因已确诊**:`tests/contract/test_specify_script_paths.py:68-90` 调用 `check-prerequisites.sh --json --require-spec --include-spec --include-plan --include-tasks`,并在 `:89` 断言 `"plan.md" in stdout`、`:90` 断言 `"tasks.md" in stdout`。该脚本按**当前分支**解析 spec 目录;`tasks.md` 只在 `$INCLUDE_TASKS && [[ -f "$TASKS" ]]` 时才进 `AVAILABLE_DOCS`(`check-prerequisites.sh:248-250`)。⇒ 本分支处于 Mode A/B 时该测试**必然失败**,`/speckit.tasks` 生成 `tasks.md` 后自愈,**无需改任何源码**。
- **反向证据**:049 基线中有 5 条今天**已通过**(`test_summarize_project_prompt_assets::test_mirror_is_byte_equivalent`、`test_spec_feature_binding_integrity::test_c2_active_spec_feature_bindings_resolve`、`test_no_organize_agents_refs::test_skills_mirror_parity`、`test_scripts_distribution_parity::test_repo_has_no_orphan_or_drifted_scripts`、`test_browser_site_exclusions::test_mirror_check_ignores_site_probe`)⇒ 基线是**上界**而非精确集合。

**决策**:实现期门禁 = "失败集 ⊆ 049 基线 ∪ {`test_review_prerequisite_flags_are_supported`}",且该分支状态项在 `/speckit.tasks` 后消失。任何**新增**失败 ID 即本特性引入的回归。开工前重新冻结一份 `baseline-failed.txt` 到本 spec 目录(承 049/050 惯例)。

**附带发现(不在本特性范围,如实报告)**:该测试把**当前分支的 spec 目录状态**当作断言对象,使它在任何 Mode A/B 分支上都失败——这是测试设计缺陷(契约测试不应依赖所在分支),应另立处置。
