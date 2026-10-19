# Data Model: Humanize Command（人性化改写命令）

**Feature**: 062 Humanize Command（人性化改写命令）
**Spec**: [requirements.md](requirements.md)
**说明**: 本特性交付面为 Markdown 制品（命令模板、技能体、docs 页、注册行）+ 结构契约测试 + 行为评估语料，无运行时数据库、无 Python 运行时代码变更。本数据模型描述制品承载的**信息实体**及其约束——它们是实现契约测试与结构校验时的判定对象。E1/E2/E8 是本特性新增的**制品实体**；E3–E7 是 requirements § Key Entities 定义的**运行时概念实体**，此处登记其字段面与校验规则，供契约与测试引用，不重定义其语义（语义 owner 是 requirements.md）。

## 实体一览

| # | 实体 | 层 | 承载制品 | 本特性变更 |
|---|------|-----|----------|------------|
| E1 | Humanize 命令模板 | Template | `templates/commands/humanize.md`（源）→ 4 个按工具副本目录（生成面） | 新增 |
| E2 | Humanize 执行技能 | Skill | `skills/external/humanize/SKILL.md`（源）→ `.specify/skills/humanize/`（镜像） | 新增 |
| E3 | Humanize Request（改写请求） | 运行时概念 | 技能执行期的输入契约（不落盘） | 语义新增（FR-014..FR-021 字段面） |
| E4 | Source Content（源内容） | 运行时概念 | 同上 | 语义新增（FR-019、FR-008 字段面） |
| E5 | Humanized Result（改写结果） | 运行时概念 | 会话返回或显式输出路径 | 语义新增（FR-012、FR-021、FR-022 字段面） |
| E6 | Tone & Audience Profile | 运行时概念 | 同 E3 | 语义新增（FR-014..FR-017） |
| E7 | Fidelity Constraint（保真约束） | 运行时概念 | 同上 + 评估差异脚本 | 语义新增（FR-007、FR-010） |
| E8 | 评估语料与量规 | 测试资产 | `tests/fixtures/humanize/`（随实现落盘） | 新增（SC-001..SC-006 证据载体） |

## E1 — Humanize 命令模板

**定位**: 薄命令入口（sanitize.md/derive.md 先例形态）——只保留入口、输入接线与收尾生命周期；改写工作流零复述。

| 字段/节 | 取值/形态 | 来源约束 |
|---------|-----------|----------|
| frontmatter | `description`（含触发词列表）+ `short-description`；无 `scripts:` 块（无脚手架前置脚本需求，sanitize 先例） | 命令模板惯例；Qoder 副本对 `description` 的必需性由生成器保证 |
| 命令身份 | `[[STR-001]]`（`/speckit.humanize`） | FR-001 |
| `## User Input` | `$ARGUMENTS` 接线 + User Input Protocol 引用；声明输入形态（内联内容 / 文件路径 / 可选语气·受众·输出路径） | FR-001、FR-018 |
| `## Glossary` | 术语锚定引用（既有命令同型） | 命令模板惯例 |
| Delegation 节 | 委派恰好一个技能（runtime path `.specify/skills/humanize/SKILL.md`）；真源引用不复述 | FR-024 |
| `## Handoffs` | Before/After 说明（humanize 无强制前置；After 建议按内容去向自定） | 命令模板惯例 |
| 分类面 | **Simple**（027 分类规则 (a)(b)(c) 逐条不命中）→ 无 `## Wrap-up`、无 probe 单元；分类表须有本命令行 | FR-025、C-1/C-9 |

**校验规则**:
- V-E1-1: frontmatter 含 `description` 与 `short-description`；`description` 含触发词列表（host 检索面）。模板全文零运行时配置（无 scripts 块、无引擎路径）。
- V-E1-2: 薄入口判定——模板对四维度改写行为的正文复述为零（四维度、保真细则、语气处理只出现在技能体）；Delegation 恰好命名一个技能（FR-024；SC-007 的结构面）。
- V-E1-3: 分类一致性——模板**不含** `## Wrap-up` 节（Simple 命令不得携带反馈步）；`.specify/specs/027-feedback-mechanism/contracts/command-classification.md` 的分类表含 `humanize` 行且分类为 **Simple**，结果计数行与行数一致（C-1、C-9；`test_feedback_command_classification.py` 必须绿）。
- V-E1-4: 4 个按工具副本（`.claude/commands/speckit.humanize.md`、`.github/prompts/speckit.humanize.prompt.md`、`.opencode/command/speckit.humanize.md`、`.qoder/commands/speckit.humanize.md`）由 `regen-command-copies.py` 生成，`--check` 对该命令零漂移（FR-025；SC-007）。

## E2 — Humanize 执行技能

**定位**: 执行流唯一承载者（external 分类）——四维度改写、保真底线、语气处理、文件行为的工作流全落此技能；对 spec-kit 内部制品零依赖（词汇表技能分类判据：任何项目皆可直接使用）。

| 字段/节 | 取值/形态 | 来源约束 |
|---------|-----------|----------|
| frontmatter `name` | `humanize` | 技能命名惯例（目录名一致） |
| frontmatter `classification` | `external` | clarify 2026-10-19 裁决（词汇表判据复核通过，维持） |
| frontmatter `skill_id` | `<SKILL:.specify/skills/humanize/SKILL.md>`（external 平铺镜像形态） | 镜像模型：`skills/external` ↔ `.specify/skills` 平铺对 |
| `description` | 能力描述 + 触发词（host 侧可检索） | 技能惯例 |
| 正文 | 四维度改写工作流、输入解析与拒收规则、文件安全默认、语气集合与缺省、保真底线与冲突出口、检测器诚实措辞、Wrap-up 编译面（unit-id `skill:humanize`） | FR-002..FR-023、FR-027 |

**校验规则**:
- V-E2-1: frontmatter `classification: external` 且 `skill_id` 指向平铺镜像路径；技能正文对 spec-kit 内部制品（specs/templates/引擎脚本）的**功能依赖**为零（引用 spec-kit 通用工作流文档不属于功能依赖——057 C-34 先例：自足可加载，离开本仓 ambient 指令的宿主仅读技能体即可执行改写）。
- V-E2-2: 镜像对 `skills/external/humanize/` ↔ `.specify/skills/humanize/` 字节一致（sync-mirrors 对，零 NEW drift）。
- V-E2-3: 技能体含全部四维度的可执行指令与保真底线（FR-002..FR-007 在技能侧各有落点）；检测器相关措辞满足 SC-009（零通过保证/规避声明；每处提及带不承诺表述）。
- V-E2-4: 拒收与报告面（FR-017、FR-018、FR-019、FR-021）在技能体有明确处置指令，不留「由 agent 自行判断」的空白。

## E3 — Humanize Request（改写请求）

**定位**: 一次调用的输入契约（requirements § Key Entities 的字段面登记）。

| 字段 | 取值域 | 缺省 | 来源 |
|------|--------|------|------|
| input source | 内联内容 XOR 文件路径（恰一个） | — | FR-018 |
| tone | `[[STR-002]]` 封闭集合之一 | `professional` | FR-014、FR-015 |
| audience | 自由文本 | 无 | FR-015 |
| output path | 文件路径 | 无（只返回会话） | FR-020 |
| overwrite confirmed | 显式给出 / 未给出 | 未给出 | FR-021 |

**校验规则**:
- V-E3-1: 双输入源同给 → 拒绝并说明「一次一个输入源」；多文件/目录 → 同一拒收面（FR-018 边界场景实例）。
- V-E3-2: 内联内容为空或仅空白 → 拒绝，不产生输出文件（FR-018）。
- V-E3-3: tone 不在封闭集合 → 报告该值与支持集合；不静默替换、不声称已应用（FR-017）。
- V-E3-4: output path 已存在且 overwrite confirmed 未显式给出 → 拒绝覆盖，目标逐字节不变（FR-021）。
- V-E3-5: output path == input path → 拒绝原地覆盖（首版显式排除，边界场景）。

## E4 — Source Content（源内容）

| 字段 | 取值域 | 来源 |
|------|--------|------|
| format | Markdown 或纯文本（扩展名集合见 [[STR-003]]） | FR-019、FR-022 |
| language | 主语言（中/英/混合按主语言） | FR-013 |
| frontmatter | 有/无；有则标记逐字保留 | 边界场景、FR-008 |
| substantive claims | 事实/数字/单位/日期/名称/结论/因果关系清单 | FR-007 |
| protected elements | 引文、代码块/行内代码、命令、路径、URL、标识符、公式、表格数据 | FR-008 |

**校验规则**:
- V-E4-1: 文件路径解析为可读普通文件；不存在/目录/不支持扩展名/二进制或不可解码/空文件 → 拒绝并指出问题与支持格式（FR-019）。
- V-E4-2: 改写前 protected elements 已盘点（评估差异脚本的比对清单来源，SC-002）。
- V-E4-3: YAML frontmatter 逐字保留，仅正文进入改写（边界场景；SC-005 的文件面）。

## E5 — Humanized Result（改写结果）

| 字段 | 取值域 | 来源 |
|------|--------|------|
| text | 完整改写文本（主要输出） | FR-012 |
| language/format | 跟随输入 | FR-013、FR-022 |
| completeness | complete XOR partial+未处理部分报告 | FR-011 |
| fidelity statement | 保真说明（含冲突报告，若有） | FR-007、FR-010 |
| applied tone | 实际采用语气 | FR-014..FR-017 |

**校验规则**:
- V-E5-1: 输出语言 == 输入主语言；技术术语/专有名词/代码标识符原样（SC-003）。
- V-E5-2: partial 结果 MUST 附未处理部分报告；禁止把部分结果呈现为完整结果（FR-011；SC-006）。
- V-E5-3: applied tone == 请求语气或缺省；MUST NOT 声称已应用被拒收的语气（FR-017）。
- V-E5-4: 显式输出路径写入成功时报告写入位置；写入失败不得声称成功（FR-021）。

## E6 — Tone & Audience Profile（语气与受众画像）

| 字段 | 取值域 | 来源 |
|------|--------|------|
| tone | `[[STR-002]]` 封闭集合 | FR-015 |
| audience | 自由文本描述 | FR-015 |
| 作用层 | 仅表达层（词汇、句式节奏、解释深度、例子选择） | FR-015、FR-016 |

**校验规则**:
- V-E6-1: 语气/受众与保真冲突时保真优先，并报告限制（FR-016）。
- V-E6-2: 缺省 `professional`——专业、自然、面向一般读者（FR-014）。

## E7 — Fidelity Constraint（保真约束）

| 字段 | 取值域 | 来源 |
|------|--------|------|
| invariant set | 事实、数字、单位、日期、名称、结论、因果关系、引用关系 | FR-007 |
| protected set | E4 的 protected elements + frontmatter + 表格数据 | FR-008 |
| conflict exit | 冲突/未决 → 保留原状 + 报告；歧义不靠编造消除 | FR-007、FR-010 |

**校验规则**:
- V-E7-1: 评估语料上 invariant set 改变数为 0；编造事实/例子/统计/来源数为 0（SC-002，确定性差异脚本逐项比对）。
- V-E7-2: 矛盾陈述全部保留且冲突被报告；不自行择一、不编造统一结论（FR-010）。

## E8 — 评估语料与量规（tests/fixtures/humanize/）

**定位**: SC-001..SC-006 的证据载体，随实现落盘（本 plan 只定义布局契约，不落语料本体——语料内容属实现期交付）。

| 成员 | 覆盖 | 服务于 |
|------|------|--------|
| 双语样本 ≥8（中/英/混合；内联与文件形态） | SC-001 语料下限、SC-003 语言矩阵 | 评估协议 |
| 受保护内容样本（代码/URL/版本号/路径/引文/表格/模板占位符） | SC-002 差异脚本比对 | 评估协议 |
| 语气样本（同一夹具 ×4 语气 + 缺省） | SC-004 | 评估协议 |
| 文件行为样本（frontmatter 文档、纯文本、超长多章节文档） | SC-005、SC-006 | 文件安全测试 + 长文档完整性 |
| 非法输入样本（空、不支持扩展名、二进制替身、目录路径） | SC-005 拒收分支 | 文件安全测试 |
| `rubric.md` | 四维度评分量规 + 两位独立评审协议 | SC-001、SC-004 |
| 受保护内容确定性差异脚本 | 逐项比对 + 退出码语义 | SC-002、V-E7-1 |

**校验规则**:
- V-E8-1: 语料覆盖 requirements 全部 User Story 的 Independent Test 声明面（US1 双语夹具、US2 文件行为、US3 语气矩阵）；样本数下限按 SC-001（≥8）。
- V-E8-2: `rubric.md` 含四维度各自的通过判据与「适用维度失败即样本失败」规则；两位评审独立记录形态明确。
- V-E8-3: 差异脚本为确定性程序（Program-First）：输入样本对 → 逐项受保护内容比对结论 + 退出码；无 LLM 参与。

## 状态与生命周期

无状态机实体——命令无持久状态；唯一生命周期面是 Feature 062 的注册状态（Draft → Planned 由本 plan 推进；Planned → Implemented 由 /speckit.implement 推进，状态机真源 `.specify/templates/feature-details-template.md`）。
