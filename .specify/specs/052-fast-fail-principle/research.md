# Phase 0 Research: 快速失败纪律(Fast Fail)

**Requirement**: `052-fast-fail-principle` → Feature 052  
**Date**: 2026-09-23  
**Method**: 本文件的每条决策都附**实测证据**(命令 + 输出 + 行号),不引用记忆。凡"改前即可实跑"的命令均已于本日实跑;凡依赖尚未创建制品的命令,标注为改前不可实跑并给出改前等价基线。

本特性与 Feature 040(Token Efficiency,规格目录 `035-token-efficiency`)、Feature 051(User-Facing Comprehension)同形:纪律真源文档 + 常驻章节 + 宪章双落点 + 契约守卫。**工件形态一律以 051 为准**(最新约定),不取 035 的旧约定(内联研究、`## C-1` 标题式条款、纯数字编号的 quickstart 场景)。

---

## D-1 常驻章节插入位置:UFC 之后、Dogfooding 之前

**裁定**:`## Fast Fail Discipline` 插在 `templates/instructions-template.md` 的 `## User-Facing Comprehension` 与 `## Dogfooding Practice` 之间。

**为何需要裁定**:该文件的位置被两处既有守卫约束,插错位置会直接转红。

**实测**:
- `test_user_facing_comprehension_section.py:51-52` 定义 `PREV_HEADING = "## Token Efficiency Discipline"`、`NEXT_HEADING = "## Dogfooding Practice"`。
- 其 `test_c8_section_sits_after_token_efficiency_and_before_dogfooding`(`:207-218`)断言的是 **`i_prev < i_new < i_next`(严格排序)**,**不是相邻**。故在 UFC 与 Dogfooding 之间插入一节,UFC 的 `i_prev=6 < i_new=7 < i_next=9` 仍成立。
- `test_c7_pinned_position_window_is_undisturbed`(`:195-205`)要求 `## Documentation Map` / `## Proactive Flow Trigger` / `## Fact, Correctness & Logic Checks (Input Sanity)` 三者**连续且有序**(模板 idx 1/2/3),并禁止 UFC 落在该窗口内。本插入点在 idx 8,不影响。
- 现状章节序(实测 `grep -n '^## '`,18 节):… `:66` Token Efficiency、`:74` User-Facing Comprehension、`:86` Dogfooding Practice …

**一处需订正的上游陈述**:研究子代理回传时把 `test_c8` 描述为"asserted adjacent";实读源码为严格不等式。已按源码为准——这正是本特性 FR-070"判据优先于二手描述"的实例。

**取舍**:放在四条"写法/行为纪律"章节(One Source Of Truth、Task Complexity Rubric、Token Efficiency、User-Facing Comprehension)之后,使同类相邻;若改放 `## Ask, Record, Repeat` 之后同样合法,但会把纪律章节群拆开。

---

## D-2 注入子句长度上限:≤ 10 行 且 ≤ 1,200 字节

**裁定方式**: **经用户裁定**(2026-09-23,`/speckit.plan` Phase 0 一轮批量提问,三选项:≤10 行/≤1,200 B(推荐)、≤5 行/≤500 B、不设数值上限)。用户取推荐项。理由与成本核算见下。

**裁定**:上限 = **10 行 / 1,200 字节**(双条件同时满足),由真源文档作为唯一定义点持有(FR-048)。

**实测**(草稿子句已写成并度量):

| 量 | 值 |
|---|---|
| 行数 | **8** |
| UTF-8 字节 | **933** |
| 字符数 | 457 |
| `BLOCKING_RE` 命中行 | **0**(门控中立,见 D-8) |

上限取实测值向上留余量(定界符注释 2 行已计入 8 行内;余量供中英文双渲染与措辞微调),不是凭空的整数。

**成本核算**:子句随**每一次派发**复制。6 成员团队一轮 ≈ 5.6 KB。参照系:活动指令文件 `.specify/instructions.md` 实测 **28,168 B**,预算 `INSTRUCTIONS_BUDGET_BYTES=32768`(`scripts/bash/generate-instructions.sh:38`),余量仅 **4,600 B**——故子句 MUST 保持小,但它又 MUST 自足于分类决定(FR-048 禁止以路径可达替代三项内容)。10 行 / 1,200 B 是这两个约束的交点。

**被拒方案**:① ≤5 行 / ≤500 B——须删去纪律路径行并把四条必要条件压成一句,压缩后可能不再自足,而"必须先打开文件才知道该不该停"正是 FR-048 禁止的形态;② 不设数值上限——正是房子在可理解性纪律上明确拒绝的"不可判定中间档"(`user-facing-comprehension.md:19`),且 SC-012 的变异演练将无阈值可校。

---

## D-3 通道三落点:Per-Agent Payload 新增第六字段行

**裁定方式**: **经用户裁定**(同上轮,两选项:新增第六字段行(推荐)、并入 `task_brief` 内容规则)。用户取推荐项。

**裁定**:在 `skills/create-team/references/patterns.md` 的 Per-Agent Payload 表(实测 `:96-102`,五字段行)后**新增第六行** `fast_fail_clause`,而不是改写 `task_brief` 单元格(`:98`)。

**实测**:
- 表结构:`:94` `Per-Agent Payload:` 标签、`:96` 表头、`:97` 分隔行、`:98-102` 五个字段行(`task_brief` / `territory` / `forbidden_files` / `output_convention` / `model_hint`),紧接 `:104-108` Context Isolation Rules、`:110` `### Summary Boundary`。
- **无任何测试钉死字段数**:`grep -rn 'task_brief\|Per-Agent Payload\|forbidden_files' tests/contract/` → **0 命中**。故新增一行不会转红任何既有守卫。

**取舍**:新增行使守卫可直接断言"该行存在且其内容规则指向拥有者字面量"(形态同 FR-035 第 6 项),且子句在载荷模式中对读者可见;代价是团队派发多填一个字段。并入 `task_brief` 单元格可省该字段,但守卫必须断言表格单元格内的散文(形态脆弱),且子句对读者不可见、易被漏掉。

---

## D-4 类 ⑪ 登记:登记进表 + 上调 Feature 051 的 C-14 钉子 8 → 9

**裁定方式**: **经用户裁定**(同上轮,三选项:登记 + 上调 051 的钉子(推荐)、不登记只携指针行、收窄主张为只拥有内容不拥有措辞)。用户取推荐项。这是本特性对 Feature 051 拥有制品的唯一改动。

**裁定**:把 `shared/guidelines/fast-fail.md` 加入 `shared/guidelines/user-facing-comprehension.md` 类 ⑪「失败如实报告」的**规则真源文件**单元格(该单元格已支持多文件——类 ⑤ 就列了两个),并同批把 `tests/contract/test_user_facing_comprehension_doc.py:400-402` 的 `len(deduped) == 8` 上调为 `9`。按 FR-024 要求,这是一次**显式列出的跨纪律改动**。

**实测**:
- 类映射表在 `user-facing-comprehension.md:96-108`(11 行,类 ① … ⑪);类 ⑪ 行现为 `| ⑪ | 失败如实报告 | shared/guidelines/confirmation-gates.md | — |`。
- 钉子:`test_c14_surface_class_table`(`:382`)在 `:396` 取 `规则真源` 列、`:397` 以 `` `([a-z0-9_./-]+\.md)` `` 提取路径、`:399-402` 断言**去重后恰为 8**。当前 8 个去重路径实测为:`confirmation-gates.md`(①②⑩⑪)、`feedback-step.md`(③)、`interview-pattern.md`(④)、`clarify.md` + `requirements-guidelines.md`(⑤)、`proactive-trigger.md`(⑥)、`requirements-guidelines.md`(⑦,与⑤重复)、`reporting-playbook.md`(⑧)、`glossary.md`(⑨)→ 去重 **8** ✓。加入 `fast-fail.md` 后为 **9**。
- 同文件另有 `test_c18a_override_registry_has_at_most_two_entries`(`:489`)只数 `reader_baseline_override` 列,与本改动无关(⑪ 的该列为 `—`,不改)。

**为何不选"不登记"**:那张表是"谁拥有某类措辞规则"的唯一索引。若不登记,读者顺表找到 `confirmation-gates.md`,只会看到三要素(失败点 / 原因 / 中间产物,`:68`),找不到第四要素「可选处置」与封闭处置集(FR-068),形成一处**真实的可发现性缺口**;而 `fast-fail.md` 携 canonical 指针行声明覆盖 ⑪ 却不在表内,正是 C-18 系列要防的"未登记的第二处基准"形态。

**代价(如实记)**:改动 Feature 051 拥有的守卫一行数值。该钉子的用途是探测**意外删除**,新增纪律使其增长属正常维护——本特性已因宪章双落点同批上调另外四个钉子(`TEMPLATE_COUNT`/`LIVE_COUNT`/`COMMAND_COUNT`/`MIN_VERSION`,见 D-7),故形态一致。

---

## D-5 观察标记字面量:`[fast-fail]`(带定界)

**裁定**:STR-001 由 `"fast-fail"` 改为 **`"[fast-fail]"`**。已回写规格(第三轮 Clarifications)。

**为何必须改**:FR-063 要求三个稳定字面量互不为子串。实测原值 `fast-fail` **是** `fast-fail-clause` 与 `shared/guidelines/fast-fail.md` 的子串,而引擎按大小写不敏感**子串**匹配(`scripts/python/feedback-utils.py:691-696`),故任何提到该纪律路径的反馈行都会被计为一次观察命中,FR-041"干净运行 MUST NOT 追加空洞条目"在机械上不可判别。

**实测修正后**(六对组合逐一验证):`[fast-fail]` / `fast-fail-clause` / `ANOMALY:` / `shared/guidelines/fast-fail.md` **两两互不为子串**,零违规。`[fast-fail]` 在框架目录(`templates shared skills scripts tests agents src docs`)**零命中**。

**与房子先例的形态偏离(记录理由)**:两处先例用**裸**记号——`token-efficiency`(`shared/guidelines/token-efficiency.md:54`)、`user-facing-comprehension`(`user-facing-comprehension.md:124`)。本特性取带定界形态,因为它同时满足两点:FR-063 的互斥要求(定界正是 FR-063 自己建议的 remedy),以及可读性(读者在反馈条目里能认出纪律名)。**附带观察**:那两处裸记号其实有同一潜在碰撞——其纪律路径都包含其标记字面量,故提到路径即被计为观察。该缺陷属上游、不属本特性修复范围,已记入 `features/052.md` › Future Evolution Suggestions。

**被拒方案**:改用与纪律名无关的裸记号(如 `ff-triage`,实测同样零命中)。它更贴近先例形态,但牺牲可读性,且并未比定界方案更安全。

---

## D-6 `ANOMALY:` 的检测判据:行首锚定

**裁定**:异常行 MUST 以**行首** `ANOMALY:` 起始;检测判据是行首锚定而非全文子串。

**理由**:该前缀无法不出现在注入子句正文里(子句必须告诉子代理用它),故 FR-063"MUST NOT 出现在承载它们的规则正文里"对它不可字面满足。改以**位置**作判据:子句对它的提及是行内反引号引用,真实异常行则以它起始一行。二者机械可分。已回写 STR-010 的消费者列与判据说明。

---

## D-7 宪章版本号形态:3 段 MINOR → 1.13.0(上游分歧如实记录)

**裁定**:活动宪章版本 `1.12.0` → **`1.13.0`**(MINOR,因新增原则),沿用 3 段形态。`test_constitution_double_landing.py:68` 的 `MIN_VERSION = (1, 12)` 同批上调为 `(1, 13)`(该钉子是**下限**语义,`:423` 用 `>=`,故 1.13.0 本就不会转红;上调是为把下限推到本特性之后)。

**上游分歧(检测子代理上送、经我复核成立)**:`templates/commands/constitution.md:64-70` 要求 4 段 `x.y.z.ddd` 形态(`:66` MINOR = `x.y+1.0.0`、`:69` 有 `ddd` 重置规则),但活动宪章 `:254` 是 3 段 `1.12.0`,051 的修订亦为 3 段(`1.11.0 → 1.12.0`,见其 Sync Impact Report `:3`),且守卫 `:420` 只解析 `(\d+)\.(\d+)` 两段。**取 3 段**:它是唯一与仓库实况及守卫解析口径一致的读法。分歧本身属上游缺陷(命令模板与实况不符),不在本特性修复范围,已记入 `features/052.md`。

**双落点四个钉子实测**(改前):`TEMPLATE_COUNT = 13`(`:65`,相等断言 `:202`)、`LIVE_COUNT = 15`(`:66`,相等断言 `:408`)、`COMMAND_COUNT = 7`(`:67`,相等断言 `:255`)、`MIN_VERSION = (1, 12)`(`:68`)。改后 MUST 为 **14 / 16 / 8 / (1, 13)**。原则数独立重算已核对:模板 `### I.`–`### XIII.` = 13、活动 `### I.`–`### XV.` = 15、命令 `MUST include` 在 `:77,87,91,100,111,126,137` = 7 ✓。

---

## D-8 门控预算处置:设计规避(零命中),实测草稿子句 0 命中

**裁定**:全部新增文本对 `BLOCKING_PATTERNS` **逐行零命中**;`scan-confirmation-gates.py` **零改动**(`POLICY_DOCS` / `SELF_REL` / `BLOCKING_PATTERNS` 均不动);实跑 `total` 与冻结基线**相等**。

**实测**(改前基线,2026-09-23):
```
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
```
冻结基线 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`:`"total": 23`、`"integerHeadroom": 0`、`"cap": 23.25`。

**计数单位是"命中的行"**:`scan()` 逐行 `if not BLOCKING_RE.search(line): continue` 后 `gates.append(…)`,故任何被扫描文件里任何一行命中即 +1。`classify()` 按 `GOVERNANCE_PATH_PATTERNS`(含 `constitution-template`)与 `DESTRUCTIVE_KEYWORDS` 分类,但**两类都计入 total**。

**扫描面覆盖本特性全部新增文本**:`SCAN_DIRS = ("templates/commands", "skills", "shared")`(`:35`)、`SCAN_ROOT_FILES = ("templates",)`(`:36`)⇒ 真源文档(`shared/guidelines/`)、常驻章节与宪章原则(根级 `templates/*.md`)、命令 `MUST include` 条目(`templates/commands/`)、通道三落点(`skills/create-team/references/`)、通道二的命令侧落点(`templates/commands/agents.md`)**全部在范围内**。`SKIP_DIR_PARTS` 含 `.specify`(`:37`),故镜像不重复计数。

**两处已实测的必踩陷阱**:
1. **相邻纪律的中文名**:阻塞模式含 `confirmation gate|确认门[禁控]`,而「确认门控治理」逐字命中。⇒ 真源文档 MUST 以**路径**指称(`shared/guidelines/confirmation-gates.md` 带连字符,不命中空格形态 `confirmation gate`)。已由 FR-036 承载。
2. **停止语义**:MUST 用「停在异常点并上送用户裁定」这类形态,MUST NOT 用「等待用户确认」「stop and confirm」「确认后执行」「确认门禁」「explicit user confirmation」。

**草稿子句已实测门控中立**:8 行逐行过 `BLOCKING_RE` → **0 命中**(以 `importlib` 载入扫描器取真正则,不重抄模式)。

**钉子集合(2026-09-23 实现期订正)**:本研究初版记为"双重钉子 / 两处",实现期实测证伪——`total` 的任何 +1 会同时打爆**三处**形态互不相同的断言(硬编码字面量 / 对冻结基线相等 / 由 Feature 044 基线派生的 `cap = total × 0.25 = 23.25` 上限)。该枚举的**唯一拥有者**是 `contracts/gate-neutrality.md` C-10,本行 MUST NOT 另抄一份数目;此处只保留订正记录本身(为何订正:第三处是上限形态,grep `== 23` 找不到它,初版因此漏计)。

**代价(FR-078 要求显式记录)**:本纪律的措辞从此永久受制于一个与它无关的扫描器的 17 条模式;日后每次修订真源文档都要先躲开它们。该代价已接受,并由 FR-064/FR-065 约束其唯一恶性形态(为躲模式而改语义)。

---

## D-9 注入子句副本的同步:守卫钉死 + 手工重灌 + 成对定界符

**裁定**:拥有者字面量以成对 HTML 注释定界(`<!-- fast-fail-clause:begin -->` … `<!-- fast-fail-clause:end -->`),宿主副本逐字节复制该区间;守卫按定界符机械提取后比对。**无引擎参与**。

**实测(为何不能声称"机器可再生")**:`scripts/python/regen-command-copies.py` 只处理 `templates/commands/*.md` → 四棵按工具树;Agent 渲染方向是 canonical → 按工具副本(`render_agents_for_tool`,`src/specify_cli/__init__.py:615`)。**无任何引擎会再生 `skills/create-team/references/patterns.md` 或 `agents/*.agent.md` 中的子句**。故 FR-052 称其为"守卫钉死的合法重复"(`one-source-of-truth.md:33` 三类合法重复的第二类),漂移修复路径为从拥有者手工重灌。

**定界符是必需的**:房式守卫惯用法是整文件字节相等(`test_user_facing_comprehension_doc.py:193` 的 `read_bytes()` 比对),而这里被比对的单位是**三个不同宿主文件里的内嵌子串**。没有定界符,"逐字节一致"无从机械提取(FR-052 已要求)。

**选 HTML 注释而非 Markdown 标题作定界符**:注释在渲染后的文档中不可见,不污染读者视角;且 `.md` 宿主里它不会与任何标题式断言冲突。

---

## D-10 真源文档的 H2 节集(封闭,守卫钉死)

**裁定**:`shared/guidelines/fast-fail.md` 的 H2 节集固定为 9 节,顺序如下(对齐房子骨架:实质规则 → 边界 → 程度 → 程序 → 与相邻原则的关系 → 范围限制):

1. `## 分流判据`(二值判据 + 四条必要条件 + 机械测试 STR-005 + 判据优先于清单命中 FR-070 + 存疑从严 FR-012 + 爆炸半径定义 FR-073)
2. `## Fast Fail List(快速失败清单)`(字面量以 [[STR-011]] 为**唯一拥有者**,本行是引用而非第二定义处;条目语法见 D-11;点名 7 项已实测失效)
3. `## In-Passing Repair List(顺手修复清单)`(字面量以 [[STR-012]] 为唯一拥有者;同上)
4. `## 上送件与披露`(四要素 + 封闭处置集 FR-068 + 界面类归属 FR-024 + 干净运行显式陈述 FR-067 + 粒度引用)
5. `## 子代理派发注入`(派发期义务 FR-047 + 注入子句拥有者字面量 + 三条通道 FR-050 + 派发前自检 FR-053 + 回传异常行 FR-054 + 异常停不得重派 FR-055 + 上送件所有权分层 FR-056 + 三模式同等 FR-057 + 调用方义务 FR-058 + 派发链逐跳 FR-059)
6. `## 生长闭环`(观察标记 FR-040 + 两条红线 FR-041 + 决定信号引用 FR-042 + 复用既有 probe FR-043 + 双向生长规则 FR-044 + 留痕 FR-045 + 自省入口引用 FR-046 + 过度触发三数 SC-015)
7. `## 与相邻纪律的边界`(五处:门控治理 / 输入健全性 / 同作者检测委托 / 自我提升 / 问一次记下来)
8. `## 冲突裁决顺序`(清单 vs 判据、子句 vs Agent 定义正文、既有实例点位 vs 新判据、并发异常、裁定 ping-pong 上限、跨会话既有裁定检索、真源文档自身异常 — FR-013/060/072/075)
9. `## 范围限制`(零新机制 + 已接受代价 FR-078 + 观察约定)

**头部所有权区**(前 8 行内,FR-002):H1 双语、单一真源声明、常驻章节指针、`MUST NOT 复制`、以及 UFC 要求的 canonical 指针行(FR-074,声明覆盖类 ⑪)。

**项目中立**(FR-008):MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai`。守卫形态同 `test_one_source_of_truth.py:37,158-163` 的 `FORBIDDEN`。

---

## D-11 两份清单的条目语法(使"每条携判据"可机械断言)

**裁定**:每条一行,形态固定为

```
- **FF-n <类名>** — 判据:<一句可复现的认定条件> | 实证:<路径或教训小节>
```

修复侧同形,前缀取 `RP-n`。守卫据 `^- \*\*(FF|RP)-\d+ ` 枚举条目,并断言每行含 `判据:` 分隔符(FR-076)。

**为何必须有语法**:没有它,"每条携判据"只能退化为"该节非空",而那是 STR-006 自己禁止的空转断言。`FF-` / `RP-` 前缀实测在仓库中零命中(`FF-[0-9]` 0 命中;`ff-pull`/`--ff-only` 属 git-fleet 的无关 token)。

**点名 7 项的落位**(FR-016 + SC-002):盲检四成因 = `FF-2`…`FF-5`;`git diff` 三形态 = `FF-6`…`FF-8`。清单总条数可多于 7 且**不设钉子**(FR-020),但这 7 项 MUST 逐项可定位。

---

## D-12 契约测试划分:两个文件

**裁定**:
- `tests/contract/test_fast_fail_discipline.py`(STR-007)——承载 FR-035 的 22 项断言(真源文档 + 镜像 + 常驻章节 + 清单语法 + 7 项覆盖 + 标记 + 边界 + 中立性)。
- **不新建** dispatch 专用测试文件:通道二/三的字节相等断言、四个宪章钉子的上调、以及 UFC C-14 的 8→9,都落在**既有**测试文件里(`test_constitution_double_landing.py`、`test_user_facing_comprehension_doc.py`)加新增断言,而不是另起文件——另起会把同一个命题的断言拆到两处,构成第二定义点。

**根定位与读取惯例**(照抄房子惯用法):`ROOT = Path(__file__).resolve().parents[2]`(`test_user_facing_comprehension_doc.py:34`);源 `ROOT/"shared"/"guidelines"/DOC_NAME`(`:36`)、镜像 `ROOT/".specify"/"shared"/"guidelines"/DOC_NAME`(`:37`);扫描器以 `importlib` 载入取真正则(该文件 `:20` 记有先例),**MUST NOT 重抄 17 条模式**(重抄即副本,会漂移)。

---

## D-13 基线冻结策略:三组基线,判据一律取"无新增漂移"

**实测(改前,2026-09-23)**:

| 基线 | 改前实测 | 判据 |
|---|---|---|
| 镜像漂移(**全树**)`sync-mirrors.py --check` | `DRIFT detected`,**EXIT=2** — 大量 `.specify/skills/*` DIFF,另有 `.specify/scripts/python/trigger-utils.py`、`.specify/shared/workflow/feedback-step.md`、`.specify/shared/workflow/runtime-mode.md`;`agents/ == .specify/agents/templates/ (2 files)` 为 ok | 仅记录,不作判据(既有漂移先于本特性) |
| 镜像漂移(**范围化**)`sync-mirrors.py --check --only shared` | `scope --only: shared`;**恰 2 条 DIFF**:`.specify/shared/workflow/feedback-step.md`、`.specify/shared/workflow/runtime-mode.md`;`DRIFT detected`,**EXIT=2** | **本特性的判据面**:改后 MUST 仍是**这同 2 条**、无新增。MUST NOT 用绝对判据(EXIT=0)——既有漂移使它不可通过 |
| 按工具副本 `regen-command-copies.py --check` | 列出大量 `.qoder/commands/*` 为待再生(既有漂移) | 同上:本特性触及的命令模板其再生副本含改动;既有漂移如实记为上游 |
| 门控扫描 `scan-confirmation-gates.py` | `total 23 / destructive 13 / governance_kept 10 / violations 0` | **相等**(余量 0;钉子集合见 `contracts/gate-neutrality.md` C-10) |
| 契约测试名级基线 | 待 Phase 1 末尾以 `run-tests.sh --names-out` 冻结 | `comm -13 baseline current` 输出为空(名字级,非条数级) |

**为何"无新增漂移"而非"全绿"**:plan 模板的 BASELINE DRIFT 段明写——绝对判据在既有漂移先于本特性存在时**不可通过**,写下去就是发运一条没人度量过的判据。实测确认既有漂移非空,故必须用相对判据。

**`--only shared` 的范围化(实测可用)**:`sync-mirrors.py --help` 载明 `--only PATH (repeatable) restrict the run to the given repo-relative path prefix`;实跑 `--check --only shared` 输出 `scope --only: shared` + 上述 2 条 DIFF + EXIT=2。该形态把判据收窄到本特性唯一触及的镜像对(051 的 Mirror Obligations 行用的就是这一形态)。**注意 EXIT=2 是既有状态,不是失败信号**:判据是"改前改后 DIFF 集合相同",而非退出码为 0。

---

## D-14 爆炸半径的可判定定义(FR-073)

**裁定**:**爆炸半径 = 本次修复会触及的工件集合**;判据为「该集合是否超出**当前动作在其所属工件中声明的范围**」。声明范围的来源按优先级:任务的 territory / Write Scope(团队派发时)、`plan.md` 的 Source Code tree 与 Mirror Obligations 行(实现时)、命令模板的产出声明(命令运行时)。三者皆无声明时,范围 = 当前正在编辑的那一个文件。

**为何这样定**:它把"半径"从形容词变成一个**集合包含判定**,两位复核者可独立复现(SC-001 要求 100% 一致)。房子已有同形先例:团队载荷的 `territory` 字段(`patterns.md:99`)与 `forbidden_files`(`:100`)本就是范围声明。

**被拒方案**:按"改动的文件数"或"改动的行数"定量——二者都与"是否越出声明范围"无关(改一个文件也可能越界,改十个文件也可能全在范围内)。

---

## D-15 封闭处置集的四项取值(FR-068)

**裁定**:上送件第四要素 MUST 从以下四项取值(封闭集,扩展只经修订真源文档):

1. **按建议处置** — 采纳上送件给出的建议动作。
2. **改为顺手修复并继续** — 用户判定该异常只需纠正,授权就地修完并继续(该授权只豁免本次)。
3. **照原样继续** — 用户知悉异常并接受现状,不改不修(记录为已接受代价)。
4. **终止本次运行** — 停止该动作链,保留已产生的中间产物。

**为何封闭**:临时发明处置就是发明工件未记录的意图,而那按本纪律自己的判据属快速失败。四项覆盖"改 / 修 / 受 / 停"四个互斥方向,无遗漏。

**与既有决定信号词汇的关系**:FR-042 引用的四值信号(approved-as-is / modified / asked-questions / denied)记录的是**用户如何回应**,本处置集是**提供给用户选什么**;二者一一对应但不互相替代(处置 1→approved-as-is、2→modified、3→approved-as-is 带代价记录、4→denied)。真源文档 MUST 载明该映射,MUST NOT 复述信号词汇的定义。

---

## D-16 过度触发三数的导出方式:零新增机制(SC-015)

**裁定**:三个数全部由**既有存据导出**,MUST NOT 新增计数器、台账或仪表盘:

| 数 | 导出方式 |
|---|---|
| 快速失败率 | 含 `[fast-fail]` 标记的反馈条目中,记为快速失败者 / 全部分流判定 |
| 用户推翻率 | 裁决记录的决定信号中 `modified` + `denied` / 快速失败次数 |
| 清单净生长方向 | 真源文档修订记录中升至 FF 侧的类数 − 降至 RP 侧的类数(FR-045 要求每次移动留痕,故可数) |

检索形态:`feedback-utils.py --action list --contains "[fast-fail]"`(实测 `--contains` 为大小写不敏感子串匹配,`:691-696`;方括号是字面量,不参与正则)。

**为何不设通过阈值**:三个数的作用是使"这条纪律正在被绕过"成为有数字的信号(用户推翻率持续偏高 + 净生长仍为正 = 单向棘轮正在生效),而不是一道会因正常波动而误报的门禁。

---

## D-17 尚未创建制品的验证策略(执行核验规则)

`quickstart.md` 的每条命令按 plan 命令的 execution-verify 规则处理:**改前可实跑的**一律本日实跑、期望值取自实跑输出;**依赖尚未创建制品的**逐条(而非文件级)标注,并给出改前可实跑的等价基线。051 的 `quickstart.md:6`  declaration + `:8-23` 改前基线表是形态先例。

**已实跑并取得期望值的命令**(本日):`scan-confirmation-gates.py`(total 23)、`sync-mirrors.py --check`(DRIFT,内容如上)、`regen-command-copies.py --check`(既有漂移)、`ls -1 shared/guidelines/*.md | wc -l` = **12**、`ls -1 agents/*.agent.md | wc -l` = **2**、`grep -c '^### ' templates/constitution-template.md` = **13**、活动宪章 `grep -c '^### [IVX]*\. '` = **15**、`grep -c 'MUST include' templates/commands/constitution.md` = **7**、`wc -c < .specify/instructions.md` = **28168**、`wc -c < templates/instructions-template.md` = **20817**、`grep -c '^## '` 模板 = **18** / 活动 = **19**、`INSTRUCTIONS_BUDGET_BYTES` = **32768**(`generate-instructions.sh:38`)、`sync-mirrors.py --check --only shared` = **EXIT=2 / 恰 2 条 DIFF**。以上十一项均于本日实跑,数值逐一核对相符。

**改前不可实跑**(依赖 `fast-fail.md` 等):`cmp` 源与镜像、守卫测试文件、真源文档节名扫描。这些在 quickstart 中逐条标注,并给出上表中的改前等价基线。
