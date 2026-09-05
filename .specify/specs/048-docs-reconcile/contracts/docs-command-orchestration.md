# Contract: /speckit.docs 命令模板编排形态

**Requirement**: `048-docs-reconcile` → Feature 037 Docs Command
**Target artifact**: `templates/commands/docs.md`(权威源)+ 4 份生成副本
**Date**: 2026-09-01

本契约规定改造后命令模板的结构性约束。既有契约 `.specify/specs/033-docs-command/contracts/docs-command-template.md` 的 C-1…C-18 继续有效,其中 6 条按本契约 D-11 就地修订(5 条行为修订 + C-8 事实纠正)。

## D-1 三段编排落位

命令模板 MUST 在既有 `## Outline` 章节内部表达三个阶段(目标结构 → 差异与动作分解 → 双技能分发),MUST NOT 为此新增顶层 `##` 小节。顶层章节保持 6 章且顺序不变:`## User Input`、`## Glossary`、`## Outline`、`## Feedback`、`## Documentation`、`## Handoffs`。

理由:既有契约 C-3 规定六章节顺序固定;三段是同一引擎的编排阶段而非新模式(单引擎坍缩纪律)。

## D-2 必须存活的字面量

以下字符串 MUST 在改造后的模板中保留(既有测试与治理扫描依赖):

| 字面量 | 依赖方 |
|--------|--------|
| `stop-and-confirm` | `tests/contract/test_confirmation_gates_sweep.py` KEEP_LIST 行 |
| `reconcile-pattern.md` | `test_c7_thin_dispatch_references` |
| `docs-utils.py` | `test_c7_thin_dispatch_references` |
| `single source of truth` | `test_c4a_mandatory_delegation` |
| `skills/create-docs/SKILL.md` | `test_c4a_mandatory_delegation` |
| `观察快照`、`残差报告`、`审计日志`、`干跑计划` | `test_c5_*`(四件强制产物) |
| `全量`、`单目标`、`写作`、`扇出`、`Bootstrap` | `test_c4_scope_resolution_and_tiered_gates` |

## D-3 必须保持缺席的内容

- `R0 需求解析` —— 技能内部写作环标签 MUST NOT 内联进命令(`test_c7_thin_dispatch_references` 断言)。
- 引擎语义正文 —— 基线枚举、调谐环步骤展开、门禁判据正文 MUST NOT 复制进命令;一律以路径引用接入(宪法 XIV;`confirmation-gates.md` § 规定命令以单行引用接入)。
- `.specify/templates/commands/docs.md` 镜像 MUST NOT 被重建(2026-08-17 退役,`test_c1_source_and_mirror` 断言其缺席)。

## D-4 双技能委托声明

模板 MUST 同时点名两个 owning 技能及其路径:`skills/create-docs/SKILL.md`(结构与基线)、`skills/improve-docs/SKILL.md`(既有文档内容)。每个技能 MUST 被声明为其对应半边的单一事实源。MUST NOT 再表述为"仅委托单一技能"。

## D-5 目标结构声明接入

模板 MUST 声明:声明文件路径 `.specify/docs/target-structure.md`;骨架来源 `templates/docs-target-structure-template.md`;首次运行设计并经确认后持久化;已存在且未要求重设时**复用不重设**。模板 MUST NOT 内联声明的完整字段清单(属 `target-structure-declaration.md` 契约)。

## D-6 零新增确认门控

改造 MUST NOT 引入新的阻塞确认门控。以下确认全部并入**既有 R4 干跑计划**这一个门控:

| 确认需求 | 来源 FR | 承载方式 |
|----------|---------|----------|
| 声明经确认方可作为收敛依据 | FR-003 | 首次运行:声明与干跑计划**合并为一次确认**呈现 |
| 隐含结构变更回写声明 | FR-010 | 作为计划中的一项,随计划确认 |
| 目标重设计提议 | FR-015 | 作为计划中的提议项,随计划确认 |
| 扇出规模告知与中止 | FR-008 | 计划内告知计划文档数;不批准即为中止 |

验证:`scan-confirmation-gates.py --json` 的 `total` MUST 保持 23、`violations` MUST 为 0(实测基线;SC-002 上限为 baseline 93 × 25% = 23.25,新增一条即越界)。本契约亦 MUST NOT 通过改写 `baseline.json` 来换取门控增量。

## D-7 分级门禁原样保留

模板 MUST 保持既有三层表述:安全本地写自动执行;搬迁/归档/重组经干跑计划逐项确认;正式区只归档不删除。MUST NOT 新增层级,MUST NOT 把内容改写提升为需确认档(内容 section-level 编辑属安全本地写)。

## D-8 用户输入叠加与写作语义

模板 MUST 表述:用户附加输入在基线调协**之外**追加动作,MUST NOT 取代基线调协。作用域判定沿用既有五值表(无参=全量;目标路径=定向;委托/方向性=全量)。写作委托的行为从"只走写作流程"改为"调协 + 写作动作并行交付"。

每个写作动作 MUST 先回答两个问题:**写什么**与**放哪里**。内容计划必须显式综合目标读者、当前任务语境、本次用户输入、仓库事实证据和写作边界;落位计划必须先检索同主题 canonical owner,已覆盖则路由 improve-docs 而非创建近重复,否则解析到唯一 canonical home。

## D-9 分发、发现路径与报告

模板 MUST 表述:内容动作逐文档顺序分发(不合并批量改写);分发开始前告知计划文档数;不设上限且禁止隐式截断;中途中止时已完成项保留、未开始项以 pending 进入残差报告。残差报告 MUST 按 owning 技能分列;审计日志在零收敛时 MUST 照写。

创建/搬迁 canonical 文档的结构批次 MUST 同步维护所属目录索引和必要根入口;当 canonical 文档路径需要进入 Agent 项目知识入口时,命令 MUST 调度 `/speckit.instructions` 刷新 `.specify/instructions.md` Documentation Map,而不是直接编辑生成的 compatibility aliases。残差报告必须给出人类与 Agent 的固定检索路径。

## D-10 移交边界不变

站点/发布请求 MUST 仍移交 `create-pages`;技能本体改进 MUST 仍移交 `improve-skills`。

## D-11 既有 033 契约的修订清单

实现阶段 MUST 就地修订 `.specify/specs/033-docs-command/contracts/docs-command-template.md`(附日期修订 note,不改写历史条款语义之外的内容):

| 条款 | 修订内容 |
|------|----------|
| C-1 | 删除"并在 `.specify/templates/commands/docs.md` 存在字节一致镜像"——与 `test_c1_source_and_mirror` 的断言相反,措辞事实过时 |
| C-4a | 单技能 SoT → **技能对**:create-docs 为结构半边 SoT、improve-docs 为内容半边 SoT;命令为编排层而非"仅分发单一技能" |
| C-5 | 四件强制产物 → 追加**目标结构声明**为第五件(跨运行长存,区别于四件按次产物) |
| C-7 | thin-dispatch 语义保留;明确"编排叙述可在 Outline 内展开,引擎语义仍不得内联" |
| C-8 | 计数 `13→14` 更正为实测 **18 复杂 / 4 简单**(`docs` 已在复杂集,本特性不改分类) |
| C-18 | improve-docs 从"仅交接目标"扩为"命令分发链路成员";其禁止创建/搬迁/归档的红线不变 |

C-3 **不修订**(六章节枚举因 D-1 保持成立)。

## D-12 镜像与生成副本

`templates/commands/docs.md` 改动后 MUST 重生成 4 份工具副本(`.claude/commands/speckit.docs.md`、`.github/prompts/speckit.docs.prompt.md`、`.qoder/commands/speckit.docs.md`、`.opencode/command/speckit.docs.md`),验证 `regen-command-copies.py --check` exit 0。副本 MUST 保留 AUTO-GENERATED 头。

注意路径重写行为:仅 `memory/`、`scripts/`、`templates/`、`shared/` 前导段被改写为 `.specify/<seg>/`;`skills/` 与 `.specify/docs/` 原样保留。
