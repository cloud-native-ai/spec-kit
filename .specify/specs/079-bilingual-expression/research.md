# Research: 双语表述（Bilingual Expression）— Phase 0 findings

**Spec**: `.specify/specs/079-bilingual-expression/` | **Date**: 2026-10-30 | **Flow Class**: expression（`flow-class-check.py --action lookup --unit-id "spec:079-bilingual-expression"` 本次运行 exit 0，source=declaration，一次读取复用全阶段）

Phase 0 结论以仓库内实测为准（Program-First）；每条记录给出可复算来源。现状锚点 M-1…M-7 已在 `requirements.md` § 现状锚点 登记（dated record），本节不复述其数值，只登记 plan 阶段新做的测量与裁决。

## R-1 既有先例：077 表达类 plan 的形制

`.specify/specs/077-doc-sdd-integration/plan.md` 是最近的表达类 plan 先例：`## Document Structure` 四子节、`contracts/` 条款文件（`md-bold-closed` 形态，经 `clause_extract.py` 实测）、Mirror Obligations 基线「改动前先测一次」、`feature-ref.md` FR 车道。本 plan 沿用该形制；077 plan 自身缺 `## Document Structure` 章节（其 plan 早于 plan 模板结构骨架落地），不构成降级先例——本线模板已带该骨架，按模板填充。

来源：`ls .specify/specs/077-doc-sdd-integration/` + plan.md 目录扫描（2026-10-30 实测）。

## R-2 镜像与生成面基线（改动前冻结）

- `python3 scripts/python/sync-mirrors.py --check` → 退出码 0，六对全 `ok`（templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 117 / shared 60 文件），per-tool 命令副本 `OK`。
- 原始输出：`.specify/specs/079-bilingual-expression/test-evidence/plan-sync-mirrors-baseline.txt`（2026-10-30 实测）。
- 判据采用「本特性触碰的镜像对相对此基线无新增漂移」，不用绝对「全绿」——既有漂移不继承为失败也不顺手修复。

## R-3 结构面基线（docs-utils validate）

- `python3 .specify/skills/create-docs/scripts/docs-utils.py --action validate` → `violations = 4`（broken-link 3 + note-frontmatter 1；docs/concepts/overview.md 2 处、docs/reference/commands/improve.md 1 处、docs/notes/type-follows-stage-misclassification.md 1 处）。
- 原始输出：`test-evidence/plan-docs-utils-validate-baseline.txt`（2026-10-30 实测）。
- `expression-gates.md` 登记的 2026-10-24 基线是 3；今日实测为 4——既有漂移，不属本特性，判据为「相对 2026-10-30 实测基线零新增」。

## R-4 确认门预算（新增 ambient 小节的措辞约束）

- `python3 scripts/python/scan-confirmation-gates.py --summary` → blocking 27（destructive 20 / governance_kept 7），violations 0。
- 原始输出：`test-evidence/plan-scan-confirmation-gates.txt`（2026-10-30 实测）。
- 约束：`templates/instructions-template.md` 新增 ambient 小节 MUST NOT 含阻断式确认句（077 实测预算零整数余量）；ambient 只写摘要 + 指针，天然不触发确认门。

## R-5 instructions 体积余量

- `wc -c` 实测：`templates/instructions-template.md` = 27,940 B；`.specify/instructions.md` = 32,259 B。
- 预算 owner：`scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES`（`tests/contract/test_instructions_size_budget.py` 以引擎常量为准，不复述数值）；超预算报 warning 而非硬失败。
- 约束：ambient 小节保持紧凑（目标 ≤ 900 B），implement 刷新后须留档生成器的 size report 输出。

## R-6 词汇表消费方式（检查器的读取模式）

- `scripts/python/glossary-utils.py`（框架源；镜像 `.specify/scripts/python/`）以 `TABLE_HEADER_RE` / `SEPARATOR_RE` 解析 `.specify/memory/glossary.md` 的 Markdown 表，stdlib only、JSON 输出、退出码 0/2。
- 检查器复用其读取模式（表行解析、变体切分），不新造解析引擎；词汇表条目计数（161 总 / 132 双语 Canonical）以 requirements 现状锚点 M-7 为 dated record，plan 不复测。

## R-7 检查器落点裁决输入（T-014 的判别证据）

- `scripts/python/doc-consistency-check.py` 是六面门禁的守卫引擎，已有契约测试群（`test_expression_gate_wiring.py`、`test_document_structure_gate.py` 等）钉其 `--faces` 封闭语义与 `--action structure`；其判定对象是**落文文档**（spec 产物 / 交付文档）。
- 本特性检查器的判定对象是**框架源定义行**（shared/、templates/、词汇表），运行时机是维护者提交前/评审时（FR-010），与阶段门禁不同生命周期。
- 判别证据（T-014）：在临时副本中使双语扫描出错，观察六面门禁是否连带转红——解耦设计下不连带，耦合设计（同一文件加 `--action bilingual`）连带。
- 裁决：新建独立脚本 `scripts/python/bilingual-expression-check.py`（复用 `glossary-utils.py` 读取模式与既有 `*-check.py` 形态），MUST NOT 向 `doc-consistency-check.py` 增加动作（其守卫面不被本特性牵动）。

## R-8 三项基线冻结（表达类开工基线，expression-gates § 三项基线）

冻结点 = `requirements.md` 首次新增提交 `2fc9f22f`（2026-10-30，`git log --diff-filter=A --format='%h %as' -- <requirements.md>` 实测）：

| 量 | 基线值 | 来源通道（实测） |
|---|---|---|
| 门禁调用次数 | 2（本线 run `r20261030T081645Z-079a` 已记录 unit：`/speckit.requirements` + `/speckit.clarify`） | `exec-quant.py --action list-records --since 2026-10-30T00:00:00Z --format json` 按本线 run_id 过滤（3 条记录中 1 条属无关 instructions 运行，不计） |
| 人工确认次数 | 0（无 `gate-*` 生命周期 feedback 记录；clarify 为无人值守运行，提问轮次 0，8 条 Q/A 全部自行裁决） | `feedback-utils.py --action list` + `requirements.md` § Clarifications Session 2026-10-30 |
| requirements→analyze 墙钟 | `null` + reason：`/speckit.analyze` 尚未运行，无法在 plan 期测量；收尾时按同一通道（首提交 author date → analyze 运行判定记录时间戳）补测 | `git log --diff-filter=A` + analyze 运行判定记录 |

收口（review/closure）时逐项对照同一通道重测；基线缺失项 MUST NOT 记 0 或记达成。

## R-9 plan 阶段门禁算子（expression-gates § 阶段算子表登记行）

本阶段执行两行（类别读取已在本阶段入口完成一次）：

- `G-plan-fact`（blocking）：`pre-analyze-check.py --stage plan --spec-dir .specify/specs/079-bilingual-expression`（事实唯一性与悬空引用比对）。
- `G-plan-structure`（blocking）：`docs-utils.py --action validate`，判据「相对 R-3 基线零新增违规」；站点构建不存在，构建子项记 `not-applicable`（不显式记通过）。
- 结构面补充判定：`doc-consistency-check.py --action structure --spec-dir .specify/specs/079-bilingual-expression` 读本 plan 的 `## Document Structure`（模板 JUDGEMENT 行登记）。

## R-10 检查器退出码与入口（FR-010 plan 期决定，落 contracts/checker.md）

- 入口：`python3 scripts/python/bilingual-expression-check.py --action scan --path <file|dir> [--json]`；覆盖面核验 `--action coverage`；census（SC-005）`--action census`。
- 退出码封闭三段：`0` = 无 findings；`1` = 有 findings（stdout 逐行 `file:line [code] message`）；`2` = 用法错误。
- 挂接面：本特性**不绑定**任何阶段门禁算子（FR-010）；运行时机 = 维护者提交前自跑 + review 阶段按 contracts/measurement.md 采证。SC-002 的测量模式 = `--scope changed`（只扫改动路径上的定义行，存量不进入合规率分母，FR-006/FR-016）。

## R-11 SC-005 抽样比例（plan 期决定）

不做抽样：总体 = 词汇表全部双语 Canonical 词条（现状 132，dated record M-7），量级小且可程序枚举 → 取 **100% census**（全查），由检查器 `--action census` 执行，误差 0。若未来词汇表双语条目增长到全查成本不可忽略（单次 census 墙钟 > 60s，检查器自报），重开抽样决策（revision_trigger 落 contracts/measurement.md）。

## R-12 披露

1. `077` 的 plan 无 `## Document Structure`（R-1 已述）——本线按当前模板补齐，不回改 077。
2. docs-utils 既有基线从 3 漂到 4（R-3）——非本特性引入，登记不修。
3. 本仓 `.specify/memory/glossary.md` 是**本仓客户端**的词汇表；owner 文档中的指针写作 `.specify/memory/glossary.md`（运行时路径），与 `shared/workflow/glossary.md`（协议 owner）分工：协议归后者，词条归前者（FR-005 的消费关系不变）。
