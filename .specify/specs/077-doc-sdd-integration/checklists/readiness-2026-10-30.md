# Readiness Checklist: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Purpose**: 阶段就绪审计——检查 077 规格集里**每一条被声明的行为是否已可判定**（可从 requirements / plan / contracts / tasks 推出唯一读法），不验证实现行为。判 `fail` 的条目是规格侧的缺口，本轮不就地修复，只点名「将继承缺口的实现面」。
**Created**: 2026-10-30
**Feature (Requirement Scope)**: [`077-doc-sdd-integration`](../requirements.md) → Feature 077
**Requirements (What)**: [`requirements.md`](../requirements.md)（25 FR / 8 SC / 4 US / 6 STR）
**Specifications (How, context only)**: [`plan.md`](../plan.md) · [`tasks.md`](../tasks.md) · [`data-model.md`](../data-model.md) · [`contracts/`](../contracts/) · [`quickstart.md`](../quickstart.md) · [`feature-ref.md`](../feature-ref.md)

**Note**: 本清单的每条都是对「规格是否说清」的提问，不是对实现的测试。`[x]` = 判 **pass**；`[ ]` = 判 **fail**（缺陷在规格侧，不在本轮修复）。每条附可追溯锚点（`Req §…` / `Plan §…` / `Contract C-…` / `Gap` / `Ambiguity` / `Assumption`）与从树上读到的真实证据引文；证据 as-of 2026-10-30，HEAD `af15468e`，分支 `077-doc-sdd-integration`。`fail` 条目末尾的「将继承缺口」只点名实现面，不提出修复方案——修复属 `/speckit.analyze` 或回改上游阶段。
**Same-author gate**: 本 run 从 requirements 到 tasks 无断点，被评工件由同一 agent 产出；执行环境未向执行 agent 暴露子代理派发工具，按 `.specify/shared/workflow/objective-analysis-gate.md` §7 走受限直读，本清单整体标记为 **(detected: direct read, subagent unavailable)**；确定性程序门的读数不受此限（该 owner § 不适用清单已排除 program validators）。
**Depth / Audience / Focus**: Standard / Reviewer / 派发点名的七个簇（声明行语法 · 解析退出码 · 七模板接线 · 文档结构 · 驱动 U4 与槽位 · 回退四条 · 不变量）。`$ARGUMENTS` 已把这七簇钉死，故不再生成澄清提问。

## Verdict summary

| 分节 | 条目 | pass | fail |
|------|------|------|------|
| A. 类别声明行（US1） | CHK001–CHK006 | 4 | 2 |
| B. 解析引擎与退出码（US1） | CHK007–CHK011 | 2 | 3 |
| C. 七模板接线与 execution 零变化（US2） | CHK012–CHK016 | 3 | 2 |
| D. 文档结构（US3） | CHK017–CHK023 | 3 | 4 |
| E. 驱动 U4 与两槽位（US4） | CHK024–CHK031 | 3 | 5 |
| F. 回退四条（US2/US4） | CHK032–CHK035 | 3 | 1 |
| G. 不变量与登记（跨切） | CHK036–CHK040 | 3 | 2 |
| **合计** | **40** | **21** | **19** |

---

## A. 类别声明行（US1）

- [x] **CHK001** — **pass** — 声明行的逐字形态（字段名、半角冒号 + 一个空格、行尾无空白、大小写敏感）是否钉到「要么匹配、要么 malformed」的程度？ `[Clarity · Req §FR-001 · Contract C-001 (class-declaration)]`
  - 证据: FR-001「行形态逐字为 `**Flow Class**: <value>`——[[STR-001]] 后接半角冒号、一个空格、取值，行尾 MUST NOT 有尾随空白，字段名与取值均大小写敏感」；`§ Shared Strings` 行「| `STR-001` | "**Flow Class**" | FR-001 |」；`requirements.md` 第 6 行「**Flow Class**: execution」。

- [x] **CHK002** — **pass** — 三个形态码（`declaration-duplicate` / `declaration-misplaced` / `declaration-malformed`）是否各自有触发判据与优先级，且都不会坍缩成「无该字段」？ `[Completeness · Req §FR-001 · Contract C-004/C-005/C-006]`
  - 证据: Plan §data-model E3「同一文件既重复又错位时只报 `declaration-duplicate`（同一根因只报一次）」；Contract C-006「字段在场而形态不合 C-001 时 MUST 报 `declaration-malformed`，MUST NOT 落成「无该字段」」。

- [x] **CHK003** — **pass** — 取值越界是否被规定为**阻断的作者错误**（点名文件、行号与取值），且明确不并入退出码 2？ `[Measurability · Req §FR-005 · Contract C-009/C-010 (class-declaration)]`
  - 证据: FR-005「门禁侧 MUST 以非零退出阻断并点名文件、行号与越界取值」；C-010「作者输入错误（C-004 / C-005 / C-006 / C-009 四个码）MUST 全部归退出码 1，MUST NOT 归退出码 2」。

- [ ] **CHK004** — **fail** — 是否有**任何执行面**告诉阶段：解析返回退出码 1 时必须停下，并用驱动自己的终止语汇表达？ `[Gap · Req §FR-005 · Contract C-003 (stage-wiring)]`
  - 证据: C-002/C-003 只要求子节携带「两条 owner 指针…、一条分支句与一条降级可见句」，没有 exit-1 分支；T010 同样只列「一次 lookup + 两条 owner 指针 + 两分支句…+ 降级可见句」；而阶段协议只在 `skills/external/sdd-loop-driver/references/stage-prompts.md:40` 提供「最后一行输出显式异常行：`ANOMALY: <一句话事实>`」。
  - 风险形态: FR-005 用 CLI 语汇「非零退出」描述一个 agent 阶段的失败，二者没有映射；子节的「其余既有门禁集逐字不变」可被读成「exit 1 也按执行类继续」——正是 FR-005 要禁的静默回落。
  - 将继承缺口的实现面: **T010**（七模板子节文本）、**T009**（接线契约测试）、`contracts/stage-wiring.md` C-003。

- [ ] **CHK005** — **fail** — 「每条特性线 MUST 声明」与「缺省按 execution 且 exit 0」是否被裁决成**一个**判定（缺声明到底算不算缺陷、有没有对应 finding 码）？ `[Consistency · Req §FR-001 vs §FR-004]`
  - 证据: FR-001「每条特性线 MUST 在其 `requirements.md` 的头部区…声明恰好一行类别字段」；FR-004「未声明类别的特性线 MUST 按 `execution` 运行，`source` MUST 标为 `default`」；E3 码表没有任何「absence」码，且缺省路径的退出码是 0。
  - 风险形态: 按 FR-001 字面，树上 73 条 spec 中 72 条未声明即为违规；按 FR-004 与 E3，它们都是合法缺省。两种读法都自洽，评审者无法只读退出码判定，迁移义务也随之悬空。
  - 将继承缺口的实现面: **T002/T007**（无 absence 码）、FR-001。

- [x] **CHK006** — **pass** — 默认标记、它与 `source: declaration` 的互斥、以及「每个消费点显示」是否都写成了可判定的字段约束？ `[Clarity · Req §FR-004 · Contract C-008 (class-declaration)]`
  - 证据: FR-004「同一解析记录 MUST NOT 同时携带该默认标记与 `source: declaration`——两者互斥，同时出现即第三态缺陷」；Plan §data-model E2「`source: declaration` 与 `marker: <默认标记>` MUST NOT 同时出现」；引擎常量 `DEFAULT_MARKER = "未声明·按默认"`。

---

## B. 解析引擎与退出码（US1）

- [x] **CHK007** — **pass** — 特性线键的文法、basename 语义与「拒绝裸目录名 / `feature:<ID>`」是否都钉死？ `[Clarity · Req §FR-003/FR-007 · Contract C-002 (class-resolution)]`
  - 证据: C-002「键文法为 `^spec:[a-z0-9][a-z0-9-]*$`。MUST NOT 接受裸目录名，MUST NOT 接受含 `/` 的路径形，MUST NOT 以 `feature:<ID>` 为键」；Plan §research R-2「取值是 spec 目录的 **basename**…绝对路径会让同一个特性线在不同环境下拿到两个键」。

- [x] **CHK008** — **pass** — 0/1/2 三段退出码是否把「已声明越界」与「机制缺席」分成两个不同失败，且逐类列出输入？ `[Measurability · Req §FR-003 · Contract C-006 (class-resolution)]`
  - 证据: C-006「**0** = 已解析（含未声明按默认…）；**1** = 已声明但取值不在封闭集内，或声明行形态错误…；**2** = 键或输入非法、spec 目录不存在、owner 不可解析…。1 与 2 MUST NOT 合并」。

- [ ] **CHK009** — **fail** — 「引擎缺席或不可执行」是否有可观察的触发条件，使测试能真正演练它而不与「`--repo` 指错路径」混为一谈？ `[Gap · Req §FR-009 · SC-002 Source]`
  - 证据: FR-009 把「引擎缺席或不可执行」并入「解析退出码 2」这一条；但引擎不在时没有任何进程能返回 2。SC-002 Source 的构造是「把引擎路径指向不存在的位置」——实测两种候选构造：脚本路径缺失 → `can't open file '/nonexistent/flow-class-check.py': [Errno 2] No such file or directory`；`--repo` 指不存在 → `repository root is not a directory: /nonexistent`。两者都不产生 `owner-unavailable`。
  - 风险形态: 两条失败在证据上不可区分，SC-002 的「引擎移走后执行类仍完成」就没有被真正验证；模板也无法判断该降级还是该报错。
  - 将继承缺口的实现面: **T002/T009**（测试与接线契约）、`contracts/class-resolution.md` C-012、SC-002。

- [ ] **CHK010** — **fail** — 解析记录的字段集是否被**一致地**计数与枚举（到底是 8 项还是 9 项）？ `[Measurability · Plan §data-model E2 · Contract C-004 (class-resolution)]`
  - 证据: E2 写「**与单元键逐字段同形**（八项键集，不新增第九项）」，其表却列出 9 个字段（含 `error`）；C-004 枚举 9 个字段后写「MUST NOT 新增第九个字段」；T002 写「记录与单元键逐字段同形（八字段…）」。
  - 风险形态: 一个断言 `len(record) == 8` 的测试与实现（现有 `default_lookup_record` 恰为 9 键）必然冲突；测试作者只能二选一，规格本身不裁决。
  - 将继承缺口的实现面: **T002/T004**、E2 / C-004。

- [ ] **CHK011** — **fail** — 规格声称的解析顺序（owner 先于键文法）是否与它自称沿用的既有引擎一致，且该改动对既有键族的可观察差异已被计入？ `[Ambiguity · Plan §data-model E3 · Req §FR-011]`
  - 证据: E3 写「`owner-unavailable` 先于键文法判断（owner 先解析，**与既有 `action_lookup` 顺序一致**）」；但 `scripts/python/flow-class-check.py` 的 `action_lookup` 先做 `if not UNIT_ID_RE.fullmatch(...)` → `invalid-unit-id`，之后才 `ledger = parse_owner(repo)`。对「键非法 + owner 不可解析」同一输入，既有顺序报 `invalid-unit-id`，规格要求的新顺序报 `owner-unavailable`。
  - 风险形态: 测试若照 E3 的括注写「沿用既有顺序」会与实现相反；若按新顺序实现，又可能被读成 FR-011「执行类可观察行为 MUST 不变」的破口（仅标签变化，但未在规格里登记）。
  - 将继承缺口的实现面: **T004/T007**、C-009 (class-resolution)、FR-011。

---

## C. 七模板接线与 execution 零变化（US2）

- [x] **CHK012** — **pass** — 接线面是否恰为七个阶段模板（`clarify` 在内），每模板恰一次 lookup，且委派技能不再读第二次？ `[Coverage · Req §FR-008 · Contract C-001/C-002/C-006 (stage-wiring)]`
  - 证据: FR-008「七个模板 MUST…读取一次类别…同一次阶段运行 MUST 只读取一次，结果复用于本阶段全部算子调用；…技能 MUST NOT 再读一次」；实测七模板今日对 `flow-class-check.py` 命中数全为 `0`，正控 `docs.md` 为 `1`。

- [x] **CHK013** — **pass** — 分支句是否被限制为「执行本阶段登记的算子行」，没有第三分支，也没有算子表 / 六面表副本？ `[Consistency · Req §FR-008/FR-012 · Contract C-003/C-004 (stage-wiring)]`
  - 证据: C-003「子节 MUST NOT 出现：任何 `G-` 算子 id、任何六面 face id 表、任何 `flow_class=` 或 `flow_class:` 赋值形、任何按特性号 / 路径 / 关键词 / 文件类型的允许列表」；C-004「MUST NOT 存在第三个分支，MUST NOT 由模板自行判断「该阶段要不要走文档门禁」」。

- [ ] **CHK014** — **fail** — 子节标题——既是「恰一个子节」的计数锚，又是剥离守卫的边界——是否被登记为**唯一字面量**？ `[Clarity · Plan §research R-9 · Contract C-007 (stage-wiring)]`
  - 证据: T010 点名 `### 类别读取与文档型门禁`；C-007 与 T009 只写「固定三级标题」，`§ Shared Strings` 的 6 行里没有它（STR-001…006 是字段、章节与四个子节）。既有先例 `templates/commands/docs.md:32` 的标题还带后缀「(判定前一次,本命令不复制判据)」。
  - 风险形态: 测试（T009）与剥离器（R-9）都要逐字复制这个标题，却各无 owner；这正是 Shared Strings 机制要防的漂移。
  - 将继承缺口的实现面: **T009/T010**、C-007、`§ Shared Strings`。

- [ ] **CHK015** — **fail** — 剥离算法的边界（标题到下一个 `##`/`###`，以及插入点留下的空行如何处理）是否钉到两个实现者能算出同一 SHA-256？ `[Ambiguity · Plan §research R-9 · Contract C-007 (stage-wiring)]`
  - 证据: R-9「以子节标题为界、到下一个 `##` 或 `###` 为止」；C-007「把 C-002 的子节整块剥离后，七个模板 MUST 与基线提交的同名文件逐字相同（SHA-256 相等）」；T010 要求子节插在 `## User Input` 之后，而该块与下一个 `##` 之间基线已有一个空行。规格未规定剥离器是否吞掉子节尾部空行、是否保留插入点前空行。
  - 风险形态: 两个都「按 R-9 实现」的剥离器可差一个换行，SHA-256 判据随即失效；这是 execution 零变化的主证据。
  - 将继承缺口的实现面: **T009/T010**、C-007、R-9。

- [x] **CHK016** — **pass** — execution 零变化是否以**具名基线 + 可复算测量**表达，而不是印象？ `[Measurability · Req §FR-011 · SC-002 · Contract C-007]`
  - 证据: FR-011「门禁判定集合与基线提交 `c1cd4600` 逐项相同」；T009「剥离后七个模板 MUST 与基线提交 `c1cd4600` 的同名文件逐字相同（SHA-256 常量在编写时以 `git show c1cd4600:<path> | shasum -a 256` 实测钉入…）」；`tasks.md § Measured Premises` 已列出七条实测哈希。

---

## D. 文档结构（US3）

- [x] **CHK017** — **pass** — 四个子节标题是否逐字登记且只以引用形态消费？ `[Traceability · Req §FR-013 · Req §Shared Strings]`
  - 证据: `§ Shared Strings` 行「| `STR-003` | "### Chapter Tree" | FR-013, FR-014 |」等四行；FR-013「四项 MUST 各落一个固定子节，子节标题逐字取 [[STR-003]]（章节树）/ [[STR-004]]（基准读者）/ [[STR-005]]（证据清单）/ [[STR-006]]（事实 owner 清单）」。

- [x] **CHK018** — **pass** — 三张表的列名与解析规则（按列名匹配、常量由检查器持有、测试从常量读取）是否钉死？ `[Clarity · Req §FR-013 · Contract C-002/C-004/C-005/C-006]`
  - 证据: FR-013「列名由检查器以常量声明（code-first owner），解析 MUST 按列名，MUST NOT 猜列位——与逐流程台账同一纪律，测试 MUST 从该常量读取列名，MUST NOT 手抄」。

- [ ] **CHK019** — **fail** — 封闭码集是否覆盖 FR-013 的「四个子节缺任一即判违规」？ `[Coverage · Req §FR-013 · Plan §data-model E6]`
  - 证据: FR-013「子节标题缺任一即判违规」；E6 的章节树语法族里，与「子节缺失」对应的只有 `chapter-tree-missing`（「表达类 `plan.md` 无 `## Document Structure` 或缺章节树子节」），没有「缺 Reader Baseline / Evidence List / Fact Owners 子节」的码；`reader-declaration-missing` 只覆盖两行标记，不覆盖子节标题本身。
  - 风险形态: 实现只能自造码（违反「码集封闭」）或对三种缺失静默放过（违反 FR-013）。
  - 将继承缺口的实现面: **T014/T015**、E6 / C-001 (document-structure)。

- [x] **CHK020** — **pass** — 章节树的四个语法码与两向比对的两个码是否被分开，且明确不引入第三个阻断码？ `[Consistency · Req §FR-014 · Contract C-012/C-013]`
  - 证据: FR-014「MUST NOT 引入第三个阻断码，非顶层的计划外章节不因本条转红」；同条列出 `parent-unknown` / `chapter-duplicate` / `chapter-purpose-missing` / `chapter-boundary-missing` 与 `chapter-missing` / `chapter-unexpected`。

- [ ] **CHK021** — **fail** — 结构动作是否有一个指向**落文文档**的输入，供章节两向比对读取？ `[Gap · Req §FR-014/FR-017 · Contract C-008/C-011]`
  - 证据: C-008「判定对象 MUST 是指定 spec 目录的 `plan.md`」；T014「主体是 `--spec-dir` 下的 `plan.md`」；而 FR-014 要求「计划中的每一节 MUST 出现在**落文**中…落文出现的计划外顶层章节 MUST 判为结构违规」。CLI 的既有输入是 `--spec-dir` / `--path`，规格没有为新动作定义「落文」参数（哪个文件、哪棵树、由谁传入）。
  - 风险形态: 两向比对在实现上无对象可读；若借用 `--path`，该参数在 verify 动作里是「显式受检路径」，其与新动作的关系未在任何契约登记。
  - 将继承缺口的实现面: **T014/T015**、C-008/C-011/C-012。

- [ ] **CHK022** — **fail** — 是否有任何面告诉表达类线的 plan **去产出** `## Document Structure`？ `[Gap · Req §FR-013 · Plan §Summary]`
  - 证据: `templates/plan-template.md` 与 `templates/commands/plan.md` 对 `Document Structure` / `Chapter Tree` / `Reader Baseline` / `Evidence List` / `Fact Owners` 的命中数均为 `0`；T010 的子节只说「表达类按阶段算子表执行本阶段登记的行」；而门禁 owner 的 plan 两行是 `G-plan-fact`（pre-analyze）与 `G-plan-structure`（docs-utils），都不要求写这四节。
  - 风险形态: 结构检查器会把每一条表达类 plan 判成 `chapter-tree-missing`，而作者从未被要求写它；规格的「可判定」只完成了判红一侧，没有完成可达一侧。
  - 将继承缺口的实现面: **T010** + `templates/plan-template.md`（**没有任何任务编辑它**）、FR-013。

- [ ] **CHK023** — **fail** — 「结构通过只是必要条件」是否有**结构绿而内容红**的验收实例？ `[Consistency · Req §FR-017 · Contract C-019 · Req §Clarifications Q5]`
  - 证据: Clarifications 第 5 条答「SC-004 的第四个负向夹具（同一事实两个 owner）本身就是「结构绿而内容红」的验收实例，不新增 SC」；但 E6 把 `owner-duplicate` 归入同一个 `--action structure` 的 findings，该夹具会让**动作**转红，而不是结构绿。
  - 风险形态: 「结构只是必要条件」目前只有一个红动作实例，没有「动作绿、内容错」的实例；若把「结构面」窄化为章节子面，则 E6 的码族又与之不对应，同一术语两个外延。
  - 将继承缺口的实现面: **T013/T015**、C-019、E6。

---

## E. 驱动 U4 与两槽位（US4）

- [x] **CHK024** — **pass** — 派发载荷的三元组是否键名固定、位置固定（第①段），本地与远端同规，且缺键即派发构造缺陷？ `[Completeness · Req §FR-018 · Contract C-001/C-002 (driver-integration)]`
  - 证据: C-001「在第①段携带类别三元组：`flow_class=<值>`、`source=<declaration|default>`、`marker=<默认标记或空>`。本地原生子代理与远端 CLI 两种拓扑 MUST 同规——提示词是类别的唯一载体」；C-002「载荷缺任一元组键 MUST 判为派发构造缺陷，U4 MUST NOT 放行」。

- [x] **CHK025** — **pass** — U4 的四个增补项是否都写明 blocking 与证据来源？ `[Clarity · Req §FR-019 · Contract C-004 (driver-integration)]`
  - 证据: FR-019「增补项 MUST 是以下四条且全部 blocking：(a) 本阶段登记的 blocking 算子各有一条结果记录，且无 `not-evaluated`；(b) 该记录指向的证据文件存在、非空，且其 SHA-256 与记账值一致…；(c) 派发载荷的类别与 U4 当场解析值一致…；(d) 本阶段的 `stage-status` 行在场」。

- [ ] **CHK026** — **fail** — U4(a) 的「本阶段登记的 blocking 算子」与 FR-017 的「implement 四面 blocking」能否在不改阶段算子表的前提下同时成立？ `[Conflict · Req §FR-017/FR-019 · Contract C-004 (driver-integration)]`
  - 证据: FR-017「表达类特性线的 implement MUST…通过四面 blocking 门禁：读者声明…、证据三件套、事实唯一性、结构/链接/构建零新增违规」；`shared/workflow/expression-gates.md` 的 implement 两行只有 `G-implement-structure`（blocking）与 `G-implement-reader`（**advisory**），没有证据面与事实面算子；T011 明令「阶段算子表一行不动」。
  - 风险形态: 若按算子表计，implement 只有 1 个 blocking 算子，四面中有三面不在 U4(a) 的计数内；若按 FR-017 计，则新算子无处登记，且 T011 禁止登记。
  - 将继承缺口的实现面: **T011/T017/T018**、FR-017/FR-019、`expression-gates.md` implement 行。

- [ ] **CHK027** — **fail** — U4(b) 的「SHA-256 与记账值一致」是否有可比的记账值？ `[Gap · Req §FR-019(b) · Plan §data-model E7]`
  - 证据: FR-019(b)「其 SHA-256 与记账值一致（复用既有 `gate-implement-evidence-binding` 口径）」；E7 的字段集是 `operator_id / face / verdict / entry / rc / evidence_path`，**没有哈希字段**；既有绑定门的四键（`sample_id` / `evidence_path` / `evidence_sha256` / `verdict`）绑定的是 `verification.md` 的 SC 样本行，且 `templates/verification-log-template.md:66` 写明「Verdicts other than `pass` carry no binding duty」。
  - 风险形态: 对算子结果要么无值可比（U4(b) 退化成「文件存在」），要么必须给 E7 加第九个字段并重新定义非 pass 的绑定义务，两者都超出已登记契约。
  - 将继承缺口的实现面: **T017/T019**、E7 / C-004 (driver-integration)。

- [ ] **CHK028** — **fail** — 「四面」在 implement 门禁与槽位 `command` 中是否是同一个成员集？ `[Consistency · Req §FR-017 vs §FR-020]`
  - 证据: FR-017 的四面 = 读者声明 / 证据三件套 / 事实唯一性 / 结构·链接·构建；FR-020 的四面 =「读者 / 证据 / 副本 / 计数四面 + 结构两向比对」（含 `count`，结构另算；FR-017 则用结构面取代 `count`）；CLI 的四面是 `FACES = ("reader", "evidence", "duplicate", "count")`。
  - 风险形态: 槽位 `command` 是否跑 `count`、`passed`/`failed` 的分母含哪些面，取决于选哪个「四面」；同一份记录可被两种读法算出两个和。
  - 将继承缺口的实现面: **T019**、C-006/C-017。

- [ ] **CHK029** — **fail** — `not-applicable` 是否有封闭的合法成因集，且与槽位计数规则一致？ `[Conflict · Req §FR-020 · SC-003]`
  - 证据: FR-020「`passed` 记 verdict ∈ {pass, not-applicable} 的 blocking 算子数」；E7「`pass` 与 `not-applicable` 计 `passed`」；但 `shared/workflow/expression-gates.md` § 结构/链接/构建写「站点层不存在时，构建算子记为 `not-applicable`（显式），**不得记为通过**」，SC-003 也写「构建算子记 `not-applicable` **而非通过**」。
  - 风险形态: 同一个 verdict 在一处计入 `passed`、在另一处不得记为通过；站点层缺失的表达类线可凭 `not-applicable` 拿到满分。
  - 将继承缺口的实现面: **T019**、FR-020 / E7、SC-003。

- [x] **CHK030** — **pass** — `not-evaluated` 是否被定义成永远不能转成通过或 0？ `[Measurability · Req §FR-020 · Contract C-007 (driver-integration)]`
  - 证据: FR-020「逐面的 `not-evaluated` 原因 MUST 写在 `evidence_ptr` 指向的门禁输出里，MUST NOT 并入 `passed`、MUST NOT 以 0 表示未运行」；C-007「MUST NOT 并入 `passed`，MUST NOT 以 0 表示未运行」；`doc-consistency-check.py` 对降级的 blocking 面默认 exit 1。

- [ ] **CHK031** — **fail** — 槽位行的 `rc`（「门禁进程退出码」）是否有一个在封闭接线面内存在的**单一进程**？ `[Ambiguity · Plan §data-model E8 · Contract C-006 (driver-integration)]`
  - 证据: E8「| `rc` | 门禁进程退出码 | 同 |」；FR-020「`command` 记该次文档门禁命令串（读者 / 证据 / 副本 / 计数四面 + 结构两向比对，站点层存在时加构建算子）」——这是 5–6 条命令，规格没有提供聚合器；FR-023 的封闭接线面不含新 runner，新增一个聚合脚本即超出接线面。
  - 风险形态: `rc` 只能取「最后一条命令」或「自造 `&&` 串」两种未登记读法；前者会让后面的面掩盖前面的失败，后者是新增命令形态。
  - 将继承缺口的实现面: **T019**、E8 / C-006。

---

## F. 回退四条（US2/US4）

- [x] **CHK032** — **pass** — `owner-unavailable` 与键/输入非法两条是否都保持既有门禁集、不中断、不把降级读作通过？ `[Clarity · Req §FR-009 · Contract C-012 (class-resolution)]`
  - 证据: FR-009「MUST 打印 `owner-unavailable` 并保持既有 `execution` 门禁集不变；MUST NOT 中断流程、MUST NOT 静默切换门禁集、MUST NOT 把降级结果读作通过」；`expression-gates.md` § 调用时机与降级「owner 不可解析或引擎缺席（文件不存在 / 退出码 2）→ 显示 `owner-unavailable`，并保持既有门禁不变」。

- [ ] **CHK033** — **fail** — 降级态是否在派发载荷与 U4 中可表示，使一条表达类线不会**静默按执行类跑完**？ `[Gap · Req §FR-009 vs §FR-019 · Plan §data-model E9]`
  - 证据: E3 把 `owner-unavailable` 的记录写成「`flow_class: execution` / `source: default`」（`owner-unavailable` 行注「同上」）；E9 的载荷三元组只有 `flow_class` / `source` / `marker`，没有 error/label 字段；FR-019 的增补校验只适用于「表达类特性线的 U4」。
  - 风险形态: 降级后解析值为 `execution`，U4 不走表达类分支，四项 blocking 全部不触发；`source: default` + 默认标记又与「真正未声明」不可区分。这正是 FR-009 禁止的静默切换，却在记录与载荷层被结构性地允许。
  - 将继承缺口的实现面: **T017/T020**、E9 / FR-009。

- [x] **CHK034** — **pass** — 「已声明但取值越界」是否被明确排除在回退家族之外？ `[Consistency · Req §FR-009/FR-005 · Contract C-010 (class-declaration)]`
  - 证据: FR-009「MUST NOT 把「已声明但取值越界」（FR-005）并入本路径——把作者输入错误降级成默认类，正是本条与 FR-005 要分开的那件事」；C-010「MUST 全部归退出码 1，MUST NOT 归退出码 2」。

- [x] **CHK035** — **pass** — 未刷新副本这条回退是否有两态证据，且差异被限定在「是否含类别读取」一点？ `[Coverage · Req §FR-024 · SC-007 · Contract C-006 (invariants-and-distribution)]`
  - 证据: FR-024「未刷新的项目 MUST 保持改动前行为（旧副本不含类别读取）」；T023「逐模板断言差异只出现在「是否含接线子节」这一点上——未刷新副本的七个模板不出现 `flow-class-check.py` 与两条 owner 指针，已刷新副本各出现一次」。

---

## G. 不变量与登记（跨切）

- [x] **CHK036** — **pass** — 「零新增 `/speckit.*` 命令」是否钉到具名基线与可测差异？ `[Measurability · Req §FR-022 · Contract C-001 (invariants-and-distribution)]`
  - 证据: C-001「`templates/commands/*.md` 的文件清单 MUST 与基线提交 `c1cd4600` 逐字相同（差异集为空）」；实测当前 `ls templates/commands/*.md | wc -l` = `27`；T021 负责前后两次采集。

- [x] **CHK037** — **pass** — 「零运行时 / 零新依赖 / 只用标准库」是否写成可验证约束？ `[Measurability · Req §FR-022 · Contract C-002 (invariants-and-distribution)]`
  - 证据: FR-022「MUST NOT 引入运行时调度器、评分器或常驻服务，MUST NOT 新增第三方依赖；新增的确定性检查 MUST 只用标准库并落在既有 `scripts/python/` 下」；T021 对比依赖清单与进程清单，差异必须为空集。

- [x] **CHK038** — **pass** — 069 的契约与状态是否可证明未被回写？ `[Consistency · Req §FR-025 · Contract C-009 (invariants-and-distribution)]`
  - 证据: `git diff --stat c1cd4600..HEAD -- .specify/specs/069-execution-expression-sdd .specify/memory/features/069.md .specify/memory/features/069a.md .specify/memory/features/069b.md` 输出为空；`features.md` 的 069 行状态为 `Implemented`；FR-025「MUST NOT 回退 069 的 `Implemented` 状态、MUST NOT 改写其正文或其切片规格」。

- [ ] **CHK039** — **fail** — 确认门预算 27 在改动后由哪条 FR / 契约 / 任务**重新测量**？ `[Coverage · Plan §Constraints · Plan §research R-12]`
  - 证据: R-12「实测 `scan-confirmation-gates.py --summary` = blocking gates **27**…该预算是整数、零余量」（今日复跑仍为 `blocking confirmation gates: 27`）；但 077 的 25 条 FR / 8 条 SC / 6 份契约都没有提到它，27 个任务里也没有一行跑扫描器。既有守卫只对四个具名面断言零命中（`GOAL_SURFACES` / `RUN_DETERMINATION_SURFACES`），总量断言是 `cap = baseline["total"] * 0.25`，+1 不会转红。
  - 风险形态: 七模板子节的措辞一旦命中阻断式确认语，预算从 27 变 28，没有任何门会响；「零整数余量」只停留在 plan 的散文里。
  - **更正（2026-10-30 analyze 修复轮）**: 上面这句「没有任何门会响」描述的是**既有守卫的现状**（总量断言是 `baseline.total * 0.25`，+1 不转红），不是本缺口可被接受的结论——它正说明缺口必须靠**直接读计数**关闭。修复已落：requirements FR-022 把「两次 `scan-confirmation-gates.py --summary` 的 `blocking confirmation gates` 计数相等」写成可判定条款，SC-006 同列该项，T021 增加一次扫描器运行与两次读数对照。故本缺口不再是「预算只活在散文里」。
  - 将继承缺口的实现面: **T010**（子节措辞）、**T021/T027**（无门禁计数任务）。

- [ ] **CHK040** — **fail** — Feature 登记里的派生计数是否由某个任务重新校准？ `[Consistency · Gap · Plan §Feature Integration · T024]`
  - 证据: `features.md` 的 077 行写「25 FR / 8 SC / 4 user stories / **2 shared strings**」，`features/077.md` 写「25 FR / 8 SC / 4 用户故事 / **2 Shared Strings**」；今日 `validate-requirements.py` 报「scanned: 256 lines, 33 definition rows, **6 shared strings**」。T024 只要求「复核 `.specify/memory/features.md` 的 077 行状态由实现阶段推进、tasks 阶段不改」，没有计数校准步。
  - 风险形态: 派生计数在登记面与规格面分叉（2 vs 6），任何以登记面为输入的阶段都会读到旧计数；这是 One Source Of Truth 意义上的 stale copy。
  - 将继承缺口的实现面: **T024** + `.specify/memory/features.md` 077 行 / `.specify/memory/features/077.md`。

---

## Report

- **Path**: `.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md`
- **Items**: 40（CHK001–CHK040）；**pass 21 / fail 19**
- **Focus areas**: ① 声明行语法与位置 ② `flow-class-check.py` 三段退出码 ③ 七模板「一次读取 / 算子行 / 零副本 / execution 反向守卫」 ④ `## Document Structure` 四子节与结构只是必要条件 ⑤ 驱动 U4 四项 + 两槽位 `docs-gate-full` ⑥ 回退四条与 `owner-unavailable` ⑦ 不变量（零新命令 / 零运行时 / 069 未回写 / 确认门预算）
- **Depth**: Standard（派发已指定 40 项上限与七簇重点，未另做深度澄清）
- **User-specified items incorporated**: 七条重点全部落为分节骨架；其中 4 条（③ 的剥离边界、④ 的两向输入与 plan 指令面、⑤ 的 U4 证据绑定与 `not-applicable` 计数、⑦ 的确认门预算）各拆出多于一条检查项
- **Same-author condition**: held；检测走受限直读（subagent unavailable），见文件头标记
- **No repair in this stage**: 19 条 fail 均只点名继承面，未修改任何 plan-owned 工件

---

## 修复轮处置（/speckit.analyze 之后，2026-10-30）

> 本节是**追加的处置记录**，不改写上文的判定与证据（上文是 checklist 阶段的 dated record）。19 条 `fail`
> 全部由 `/speckit.analyze` 修复轮关闭；`/speckit.analyze` 的 29 条发现（14 HIGH / 9 MEDIUM / 6 LOW）逐条对应下表。
>
> **第二轮 analyze（HEAD `6217a86f`，判 BLOCKED）**：1 HIGH（R-01）+ 6 MEDIUM（R-02…R-07）+ 5 LOW（首轮 14 HIGH 已全关闭）。
> 处置分工——R-01 与 R-02 分别**复关**已有的第 12/14/15 行（CHK026/CHK028/CHK029）与第 17 行（CHK033）；
> R-03…R-07 与 5 条 LOW 落**第 20–29 行**。表共 **29 行**（19 条首轮 + 10 条第 20–29 行），可 29/29 逐行复核。

| CHK | 处置落点 | 修法一句话 |
|-----|----------|------------|
| CHK004（exit-1 无停止句） | FR-005、`contracts/class-declaration.md` C-009、`contracts/stage-wiring.md` C-003、data-model E4、T009/T010 | 接线子节增「退出码 1 的停止句」，并明确它 MUST NOT 落入「既有门禁集逐字不变」那一支 |
| CHK005（MUST vs 缺省合法） | FR-001/FR-004、C-001/C-008（decl）、E3 | 择一：MUST 只约束**新增声明线**，存量线按缺省 + advisory 码 `declaration-absent`（退出码 0） |
| CHK009（引擎缺席不可观测） | FR-009、C-012（res）、E3 | 改为**调用方可观察**触发（引擎文件不存在 / 拒绝执行 / 无记录 → 由调用方记 `owner-unavailable`） |
| CHK010（8 vs 9 字段） | FR-003、C-004（res）、E2、T002/T004 | 统一为**九项**（含 `error`），"MUST NOT 新增第十项" |
| CHK011（查找顺序声明错） | FR-003、C-009（res）、E3、FR-011 豁免①、T007 | 承认这是**顺序变更**（owner 先于键文法），登记可观察差异（`invalid-unit-id` → `owner-unavailable`，同为退出码 2） |
| CHK014（子节标题无字面量 owner） | R-9、C-002（wire）、E4、T009/T010 | 标题登记为**唯一字面量**（登记处 = R-9，STR 表行数不变） |
| CHK015（剥离边界未定） | C-007（wire）、R-9、T009/T010 | 钉死算法（起点=标题行，终点=下一个 `^#{1,3} ` 行前一行）+ 块末恰一个空行 + **可复算样例** |
| CHK019（缺三缺节码） | FR-013、C-001/C-013（doc）、E6、T013/T014 | 统一 `subsection-missing`（`name=` 取四个登记字面量）+ `document-structure-missing` |
| CHK021（无落文输入） | FR-014、C-008（doc）、E6、T013/T014/T015 | 把既有 `--path` 登记为落文输入；缺省只做 plan 侧并标 `two-way: not-run` |
| CHK022（plan 侧不产四子节） | FR-013/FR-023、C-001（doc）、E5、**T028**、plan § Plan Edits | `templates/plan-template.md` 进接线面与编辑面，任务 27→28 |
| CHK023（结构绿内容红无实例） | FR-017、C-019（doc）、SC-004 与 Source | 增「结构/链接/构建零新增违规 + 证据面缺 `source`」的落文夹具，并消歧「结构动作 finding ≠ 门禁结构面」 |
| CHK026（U4 四项 vs 算子表） | FR-017/FR-019、C-017（doc）、C-004（drv）、T017/T018 | 「四面」= 门禁输出的面（`FACES`）；U4(a) 分母只取算子表（implement 1 行） |
| CHK027（E7 无哈希） | FR-019(b)、C-004(b)（drv）、E7、T016/T017 | 择一：(b) 降为「存在且非空」，删哈希比对，并写明为何不给 E7 加字段 |
| CHK028（四面两义） | FR-017/FR-020、C-017（doc）、C-006/C-007（drv）、SC-003 | 统一为 CLI `FACES = (reader, evidence, duplicate, count)`；结构两向登记为 `structure` 子步 |
| CHK029（not-applicable 计 pass） | FR-020、C-007（drv）、E7/E8、SC-003 | `not-applicable` **单列**，不计 `passed`/`failed`，并由条数等式约束 |
| CHK031（rc 无单一进程） | FR-020、C-006（drv）、E8、T019 | `rc` = 逐命令**非零优先**的聚合退出码；逐命令原始 rc 落证据文件；不新增聚合脚本 |
| CHK033（降级不可表示） | FR-009/FR-018/FR-019(c)、C-001/C-004（drv）、E9、T017/T020 | 载荷增 `error=<label|->` 第四位；U4 在 `error` 非 `-` 时走 `owner-unavailable` 分支 |
| CHK039（确认门预算） | FR-022、SC-006 与 Source、T021 + 本条更正行 | 写成可判定条款（两次扫描读数相等），T021 实跑扫描器 |
| CHK040（派生计数 stale） | `.specify/memory/features.md` 077 行、`.specify/memory/features/077.md`、`checklists/requirements.md` | 计数一律**指针化**到 `validate-requirements.py` 输出，不再复述数字 |
| **20** R-01（HIGH · NA 计量单位） | requirements FR-019(a)/FR-020/SC-003 与 SC-003 Source、data-model E7/E8、C-007（drv）、T016/T019、quickstart S6、research R-5 | 站点构建并入 `G-implement-structure` 的 `face=build` **子行**（`face_scope=sub`，不另立 `operator_id`）；**删除**槽位「算子总数 − (passed+failed) = NA 条数」跨级等式；SC-003 的 NA 断言改为**面级**（`structure` 面 = pass、`build` 子行 = NA，不参与算子级计数）。**复关**第 12/14/15 行（CHK026/CHK028/CHK029） |
| **21** R-02（MEDIUM · `error` 值域双义） | FR-018/FR-019(c)、C-001/C-004（drv）、C-012（res）、E9、research R-6、T017 | 取「收窄值域」支：载荷 `error ∈ {owner-unavailable, -}`；`declaration-absent` 只出现在 advisory 发现里、**不进载荷**。**复关**第 17 行（CHK033） |
| **22** R-03（MEDIUM · Clarifications 陈旧副本） | requirements § Clarifications Session 2026-10-30 第 6 条 | 把「`passed` 记 `pass` 与 `not-applicable`」改为「算子级 `pass` + `build` 子行 NA 单列」，并在同条加**带日期更正注记**（保留原答其余判定） |
| **23** R-04（MEDIUM · 登记面第三种「四面」） | `.specify/memory/features.md` 077 行 | 「读者/证据/事实/结构四面」→「reader / evidence / duplicate / count 四面 + `structure` 子步」 |
| **24** R-05（MEDIUM · 路径错） | FR-022、T021 | `skills/external/…/scan-confirmation-gates.py` → `scripts/python/scan-confirmation-gates.py`（实跑 `blocking confirmation gates: 27`） |
| **25** R-06（MEDIUM · T028 绿而不证） | tasks.md T028 | 增**自有断言**：读取 `templates/plan-template.md`，断 `## Document Structure` 四子节字面量与「表达类 MUST 产出」句在场——不再只引用 T009/T013（二者都不读该模板） |
| **26** R-07.1（MEDIUM · 阶段记录缺失） | `features/077.md`、`features.md` 077 行 | 追加 tasks 阶段记录（`ab288aab` 落 tasks + 77 条款分区并冻结基线、`45b6b732` 收尾记账）、更新 `Last Updated`；状态保持 `Planned` |
| **27** R-07.2（MEDIUM · 派生计数写死） | `features.md` 077 行、`features/077.md` | 两处「239 行」改为指针——行数/定义行/字符串数以 `validate-requirements.py` 输出为准（现值 264 行），登记面不复述 |
| **28** R-07.3（MEDIUM · 29/29 可复核） | 本清单文件 | 追加本表第 20–29 行，使两轮 analyze 的全部发现各有一行处置记录、29 行可逐行复核 |
| **29** LOW 组（5 条） | ① research R-7 → R-9；② data-model E1；③ FR-013 / E6 / C-001（doc）；④ research R-9 / C-007（wire）；⑤ FR-001 | ① 子节字面量改为**指向 R-9 的指针**（不再重抄、不引带后缀标题）；② E1「头部区内恰 1 行」统一为「**至多一行**，缺省合法」；③ 整章缺失时只报 `document-structure-missing`、**抑制**四条 `subsection-missing`（父子同因只报一次）；④ 明确「块内任何同级或更高级标题（含 `###`）一律视为块结束」、需分层用 `####`；⑤ `declaration-absent` 只作 **advisory**、不承担合规判定；新线漏声明由 plan / tasks 阶段对 `**Flow Class**` 存在性的检查承担 |

**未在任何行关闭的项**：无。**清单判定的保留**：上文的 21/19 判定仍是那个时点的实测结论，不回填为 pass——
本节只说明它们在修复轮之后由谁承接。
