# Contract: 种子规则集与漂移检出 (seed-derivation)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Surfaces under contract**: `templates/proactive-trigger-seed.json` · `.specify/templates/proactive-trigger-seed.json`(镜像)· 25 个 `templates/commands/*.md` 的 `## Handoffs` 段(**只读参照,本契约不改动它们**)
**Test file**: `tests/contract/test_trigger_seed_derivation.py`
**Clauses**: C-1 … C-10
**合法性地位(analyze 2026-09-08 订正)**: 种子文件**不属** `.specify/shared/guidelines/one-source-of-truth.md` 的三类合法副本中任何一类 —— guard copy 须"pinned **inside** a test"且"serves the build, never the reader",而本文件是随包分发、被引擎每回合消费的运行时制品,守卫它的是**另一个**文件;它既非 generator 再生(本契约禁止散文解析),也非 dated record(第一天即被当作当前现实消费)。故 Principle XIV 在 `plan.md` §Constitution Check 记为 **⚠ Partial**,其需要理由、被否决的四条更简替代、五项缓解与残留代价**全部归 `plan.md` §Complexity Tracking**(该节是本归类的唯一权威,本契约不复述)。本契约只负责把漂移**变得响亮**:provenance 可回溯 + C-6/C-7 机械检出 + C-16 维护义务

---

## 制品形态

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-1** | 双表面 + 字节相同 | `templates/proactive-trigger-seed.json` 存在且为合法 JSON;`.specify/templates/proactive-trigger-seed.json` 与其**字节相同**(sync-mirrors templates 对) |
| **C-2** | 顶层 schema 封闭 | 顶层键恰为 `schemaVersion`(int)、`generatedFrom`(string)、`situations`(array)、`rules`(array);无多余键 |
| **C-3** | 规则条目 schema | 每条 `rules[]` 元素的键集为 `data-model.md` E2 中 `origin=seed` 应携带的字段:`ruleId`、`situationId`、`flow`、`invocation`、`rationale`、`confirmationClass`、`origin`(恒 `"seed"`)、`priority`、`provenance`,外加**可选** `notes`(仅用于记分类判据出处,见 C-9);除 `notes` 外无其他可选键,且 MUST NOT 携带 `tuning`、`stats`、`promotion`、`state`(那是运行期状态,不随包分发) |
| **C-4** | 与学习规则**同构** | 种子条目与运行期 `learned` 条目的字段集差异**恰为**:种子侧多 `provenance` 与可选 `notes`,运行期侧多 `tuning`/`stats`/`promotion`/`state`;两者的 `ruleId`/`situationId`/`flow`/`invocation`/`rationale`/`confirmationClass`/`priority` 语义与类型完全一致(FR-022「同构」的机械判据) |

## Provenance 与漂移检出(本契约的核心)

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-5** | 每条种子规则携带可回溯 provenance | `provenance` 键集恰为 `file`(相对仓库根路径)、`anchorKind`(`"handoffs"` \| `"owning-section"`)、`anchor`(段落定位串:前者恒为 `## Handoffs`,后者为拥有该流程触发条件的段落标题)、`quote`(逐字引文片段);`origin=seed` 而 `provenance` 缺失或四键不全 → 测试失败并指名 `ruleId` |
| **C-6** | provenance 指向的文件与段落真实存在 | 对每条种子规则:`provenance.file` 存在;`anchorKind=handoffs` 时该文件 MUST 含 `## Handoffs` 章节且 `quote` 作为**子串**出现在该章节正文内;`anchorKind=owning-section` 时该文件 MUST 含 `anchor` 指名的段落且 `quote` 出现在该段落正文内(均为逐字匹配、空白归一) |
| **C-7** | **漂移检出**:目标流程名仍在其来源段中 | 对每条种子规则,其顶层 `flow` 字段所指的可调用名(如 `/speckit.clarify`)MUST 仍出现在 `provenance.file` 的**对应段落**内(`handoffs` 类 = `## Handoffs` 段;`owning-section` 类 = `anchor` 指名段落)。某来源段被改写而种子未跟进 → 本条款失败,错误信息 MUST 同时给出 `ruleId`、`provenance.file`、`anchorKind` 与缺失的 `flow` 值,使修复指向明确 |
| **C-8** | 覆盖完整性与身份可解析性 | 种子规则集覆盖 `data-model.md` §命名情境表的全部 **13** 个 `situationId`(s01…s13),每个至少一条规则;`situations[]` 每项 MUST 携带 E1 的**完整形状**(`id`/`name`/`stage`/`signals`/`match{stage,signalsAll,signalsAny}`),不只 `id`/`stage`/`signalsAll` —— 因 `trigger-engine.md` C-12 的"唯一身份"依赖 `signalsAny` 与 V1.6 的最具体优先规则。另断言两项词表自洽:① **V1.3** 任意两个 `id` 的 `(stage, signalsAll)` 组合 MUST 不相同;② `stage` 与 `signals` 的每个取值 MUST 属 `data-model.md` §受控词表的封闭枚举(9 阶段 / 12 信号) |
| **C-9** | 分类不越权 | 每条 `confirmationClass` ∈ `{reversible, destructive}`;取值与 `data-model.md` §命名情境表的分类列**逐项一致**;`destructive` 的条目在 `notes` 字段说明其判据出处(引用 `shared/guidelines/confirmation-gates.md` 的破坏性清单或"存疑从严")。种子文件 MUST NOT 复述该判据文档的分类表(Principle XIV:引用不复述) |

## 分发与合并

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-10** | init 整体拷贝可达 + 合并不回退用户调优 | `templates/` 的顶层非 `commands` 文件由 `src/specify_cli/__init__.py:copy_local_templates`(L1940–1951 的 `iterdir()` 整体拷贝)自动分发,故新种子文件无需改拷贝清单(以在临时根上运行 init 后断言 `.specify/templates/proactive-trigger-seed.json` 存在来验证)。合并语义:`trigger-utils.py --action init` 对已存在 `ruleId` 只刷新 `rationale`/`invocation`,凡 `tuning` 非空者其 `state`/`priority`/`confirmationClass` 以本地为准(V2.3 / FR-022「用户已确认的调优 MUST NOT 被后续种子更新覆盖回退」) |

---

## 明确不属于本契约的事

- **不改动任何命令模板或共享工作流文档**:`templates/commands/*.md` 的 `## Handoffs` 段、以及 `owning-section` 类来源段落(`shared/workflow/feedback-step.md` §Threshold prompt protocol、`templates/commands/feedback.md` 的 Mode 表)都是**只读参照**。本契约不引入结构化 frontmatter 键(P-Q2 已否决方案 B),因此 `regen-command-copies.py` 与 4 棵 per-tool 副本树零变动,`src/specify_cli/__init__.py:1466–1473` 的块终止符元组零变动。
- **不与既有 `handoffs:` frontmatter 交互**:该键(20/25 模板)编码 agent dispatch(`label`/`agent`/`prompt`/`send`),与 `## Handoffs` 散文段**同名不同义**,且 `src/specify_cli/__init__.py:1471` 仅将其作为 `scripts:` 块的终止符 token、从不消费其条目(plan.md D-5)。种子派生的来源一律是**既有散文文面**(两类 `anchorKind` 皆然),不是任何结构化元数据。
- **不做散文解析**:引擎与测试都 MUST NOT 尝试从 Handoffs 散文自动抽取规则。漂移由 C-7 的**逐字子串存在性**检出,而非由解析重建 —— 这是"确定性可断言"与"散文不可确定性解析"之间取得的形态(plan.md D-5 裁定)。

## 实现期义务

1. 撰写种子文件时,每条规则的 `provenance.quote` MUST 从其 `anchorKind` 对应的来源段落**逐字复制**(空白归一后),不得改写或概括 —— C-6 的子串断言据此成立。`handoffs` 类取该模板的 `## Handoffs` 段;`owning-section` 类取 `anchor` 指名的段落。
2. `generatedFrom` 字段记录派生批次(如 `"templates/commands/*.md ## Handoffs + shared/workflow/*.md owning-sections @ <commit>"`),使副本的时点可追溯。**注意**:该字段只是时点戳,**不**使种子文件成为 `one-source-of-truth.md` 意义上的 "dated record" —— 种子在新项目第一天就被当作当前现实消费,故该合法副本类别不适用(本制品的 Principle XIV 归类问题见 plan.md §Complexity Tracking)。
3. 新增或改写任一来源段落(命令模板的 `## Handoffs`,或 `owning-section` 类段落)时,C-7 会失败 —— 这是**预期的**联动义务,修复方式是把变更同步进种子文件(而非放宽测试)。该义务须写入纪律文档的维护章节(`discipline-doc.md` C-16 ①)。
4. **撰写前 MUST 机械核验每条 anchor**:对 13 条规则逐条执行"打开 `provenance.file` → 定位对应段落 → 断言 `flow` 值与 `quote` 都在段内",把结果记入 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的 `seedAnchorsPrecheck`(即 tasks.md T003)。**本条是 analyze 2026-09-08 的直接教训**:初版 14 条 anchor 中有 9 条不成立(被引段落根本不含所声称的流程名),根因是从 8 条已核实样例外推到 14 行而未逐条核验;若不前置机械核验,该缺陷会一直到实现期 C-7 失败才暴露。
