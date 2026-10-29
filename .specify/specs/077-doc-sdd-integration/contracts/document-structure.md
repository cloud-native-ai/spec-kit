# Contract: 文档结构与逻辑门禁（Document Structure Gate）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：四子节的字面量归 requirements § Shared Strings（[[STR-003]]…[[STR-006]]）；证据三件套语法、
`reader-purpose` 面与「结构只是必要条件」归 `shared/workflow/expression-gates.md`；副本机械下限归
`shared/guidelines/one-source-of-truth.md`。本契约只登记**子节语法、检查动作与码集**。

## plan 侧四项

- **C-001** 表达类特性线的 `plan.md` MUST 产出 `## Document Structure` 章节（[[STR-002]]），且 MUST 含四个固定子节，
  标题逐字取 [[STR-003]]（章节树）/ [[STR-004]]（基准读者）/ [[STR-005]]（证据清单）/ [[STR-006]]（事实 owner 清单）。
  **缺节 MUST 有码**：整章缺失 → `document-structure-missing`；子节缺任一 → `subsection-missing`
  （finding 以 `name=` 携带缺失子节的登记字面量，取值域恰为这四个）。**父子同因只报一次**：整章缺失时 MUST 只报
  `document-structure-missing`，MUST NOT 再对四个子节逐个报 `subsection-missing`；子节缺席判定只在章节存在时执行。
  **产出侧 MUST 同时落地**：
  `templates/plan-template.md` MUST 携带该章节与四个子节骨架（标题与登记值逐字相同、表头列名同 C-002 / C-004 / C-005），
  并写明该章节对表达类是必要产出、对执行类 MUST NOT 构成必填项。模板是这四个字面量的**产出方**；骨架之外的一切工件
  （契约正文、FR、任务、测试、脚本常量）MUST 只写 `[[STR-NNN]]`，MUST NOT 重抄字面量。(FR-013)

- **C-002** 章节树子节的表头 MUST 为 4 列且列语义固定：节名 / 父节 / 目的 / 边界。`父节` MUST 取顶层标记 `—`
  或本表另一行的节名；`目的` MUST 写成「读者读完要做的决定」；`边界` MUST 写出本节不覆盖什么。(FR-013)

- **C-003** 基准读者子节 MUST 为两行，标记逐字 `**Readers**:` 与 `**Reading scenario**:`。读者定义 MUST 沿用
  `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议，MUST NOT 新建第二套定义。
  该两行 MUST NOT 套用落文文档的「前 40 个非空行」窗口。(FR-013)

- **C-004** 证据清单子节的表头 MUST 为 4 列：断言 / 证据等级 / as-of / source；每条拟写入文档的事实性断言 SHOULD 有对应行。
  三件套成组规则与码集归门禁 owner，本契约不复述。(FR-013, FR-015)

- **C-005** 事实 owner 清单子节的表头 MUST 为 3 列：事实 / owner 路径 / 章节锚；每条事实 MUST 恰有一个 owner。(FR-013)

- **C-006** 三张表的列名 MUST 由检查器以常量声明（code-first owner），解析 MUST 按列名匹配，MUST NOT 猜列位；
  测试 MUST 从该常量读取列名，MUST NOT 手抄。(FR-013)

## 检查动作

- **C-007** 校验器 MUST 是既有 `scripts/python/doc-consistency-check.py` 的新增动作 `--action structure`
  （`--action` 取值从 `("verify",)` 扩为 `("verify", "structure")`）。本特性 MUST NOT 新增第七个门禁面：
  该检查器 `--faces` 仍为四面，六面 owner 不变。(FR-013, FR-023)

- **C-008** 判定对象 MUST 是指定 spec 目录的 `plan.md`（plan 侧）；类别 MUST 经 `class-resolution.md` 的同一条路径解析。
  解析为表达类 → 执行四子节与四族码检查；解析为执行类或未声明 → `status: not-applicable` 并打印 `class=` /
  `source=` 与非空伴生量（被检查文件数），MUST NOT 呈现为「0 违规通过」。**落文输入 MUST 复用既有 `--path`**
  （verify 动作在用的同一 flag、同一解析器，MUST NOT 新增参数）：缺省只做 plan 侧并显式标注 `two-way: not-run`
  （MUST NOT 被读作两向通过、不得计入 `passed`）；给 `--path` 才执行两向比对。(FR-013, FR-014)

- **C-009** 基线 MUST 是「该线首次声明那一次实测出的违规集」，判据 MUST 是「当前违规集 ⊆ 基线集」，按
  `文件 + 违规码 + 节名` 三元组比对（差集为空），MUST NOT 用总数不增代替。基线文件不存在 MUST 读作空集
  （绝对判定），MUST NOT 读作豁免。基线 MUST 由 `--freeze` 打印、脚本自身 MUST NOT 写文件。(FR-013)

- **C-010** 四项的校验 MUST 可重跑：同一份 `plan.md` 上重跑同一命令 MUST 得同一违规集，finding 顺序 MUST 稳定。(FR-013)

## 章节两向比对

- **C-011** implement 落文 MUST 以章节树为唯一结构来源。计划中的每一节 MUST 出现在落文中；落文出现的计划外**顶层**
  章节 MUST 判违规。判定 MUST 只读章节标题与计划表即可完成，MUST NOT 依赖通读正文。(FR-014)

- **C-012** 两向比对 MUST 只产出两个具名码：落文缺失计划中的节 → `chapter-missing`；落文出现计划外顶层章节 →
  `chapter-unexpected`。MUST NOT 引入第三个阻断码；非顶层的计划外章节 MUST NOT 因本条转红。(FR-014)

- **C-013** 章节树自身的语法违规 MUST 由同一动作报出，MUST NOT 另判一处：父节指向不存在的节 → `parent-unknown`；
  节名重复 → `chapter-duplicate`；目的为空 → `chapter-purpose-missing`；边界为空 → `chapter-boundary-missing`。
  缺节归 C-001 的两个码（`document-structure-missing` / `subsection-missing`），MUST NOT 另造同义码。
  本动作的 finding 码集 MUST 恰为四族（结构语法 / 两向比对 / 证据面 / owner 面，逐族见 `data-model.md` E6），
  MUST NOT 出现第五族；这些 finding 属「文档结构产物与落文结构」的判定，**不等于**门禁 owner 的
  `structure-links-build` 面（后者判据归 `docs-utils.py`）。(FR-014)

## 证据面与事实面

- **C-014** 证据清单 MUST 覆盖 implement 写入的每条事实性断言；清单外的断言 MUST 判 `evidence-unlisted`。
  等级、as-of、source MUST 成组出现，缺任一 MUST 判违规；码 MUST 复用 `grade-invalid` / `as-of-malformed` /
  `source-missing` / `grade-asof-unpaired`，MUST NOT 另造同义码。(FR-015)

- **C-015** 同一事实 MUST 恰有一个 owner。判定 MUST 用三个具名码：同一事实两行 owner → `owner-duplicate`；
  owner 路径在仓库内不存在 → `owner-path-missing`；章节锚为空 → `owner-anchor-missing`。(FR-016)

- **C-016** 正文重复手写 MUST 沿用既有 `duplicate` 面的机械下限（归一化后全等且长度 ≥ 24 字符，或相似度 ≥ 0.90
  且长度 ≥ 40 字符）；MUST NOT 自建第二套阈值，MUST NOT 把该下限读作判据放宽。(FR-016)

## implement 侧

- **C-017** 表达类特性线的 implement MUST 按章节树落文，并 MUST 通过以下判定，全部按 blocking 处理：
  ① **门禁输出的四面** `reader` / `evidence` / `duplicate` / `count`（取值集归 `scripts/python/doc-consistency-check.py`
  的 `FACES` 常量，本契约只引用、MUST NOT 重定义或增删）；② **结构子步** `structure`（章节树语法 + 两向比对，
  MUST NOT 被登记为第五个 CLI 面）；③ 站点层存在时的构建检查——它是 `G-implement-structure` 的 `face=build`
  **面级子行**（`face_scope=sub`），MUST NOT 被登记为独立算子或独立 `operator_id`；站点层不存在时该子行取
  `not-applicable`（显式）。任一面、子步或子行为 `not-evaluated` MUST NOT 计为通过。
  **「四面」的唯一读法**：指 ① 的四个 CLI 输出面，MUST NOT 被读作阶段算子表的四行——该表在 implement 只登记
  一行 blocking（`G-implement-structure`）与一行 advisory（`G-implement-reader`），U4(a) 的计数分母取该表
  （`driver-integration.md` C-004），四个 CLI 面由其绑定的同一份门禁输出文件承载。(FR-017)

- **C-018** 四面结果 MUST 落在同一份门禁输出文件，并作为该阶段 SC 证据的唯一来源：`verification.md` 的
  `SC-NNN_value=` 记逐面 `面=verdict` 摘要，证据记录沿用既有四键（`sample_id` / `evidence_path` /
  `evidence_sha256` / `verdict`）；某面 `not-evaluated` → 该 SC 记 `unknown` 并点名面与原因，MUST NOT 记 `pass`。(FR-017)

- **C-019** 结构面通过 MUST NOT 被援引为内容正确性的证据——它只是必要条件，且该命题 MUST 有可执行的反例：
  同一份落文上结构/链接/构建零新增违规、而证据面因一条断言缺 `source` 判 `fail` 时，该次门禁 MUST 判 fail
  （「结构绿而内容红」的验收实例，见 SC-004 的第二个落文夹具）。implement 阶段的 Test-First MAY 按
  宪法 VII 的 template-only 条款判 `Partial (justified)`，justification MUST 写明替代验证是四项文档门禁输出。(FR-017)
