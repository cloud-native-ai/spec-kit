# Implementation Plan: `/speckit.humanize` 人性化改写命令（Humanize Command）

**Branch**: `062-humanize-command` | **Date**: 2026-10-19 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `062-humanize-command` → Feature 062 Humanize Command（人性化改写命令）
**Input**: Specification from `.specify/specs/062-humanize-command/requirements.md`

## Summary

新增框架命令 `/speckit.humanize`：把调用者给定的内容、结论或外部文档（Markdown/纯文本）做四维度人性化改写——语气与风格自然化、上下文与逻辑补全（限于输入已蕴含的范围）、格式与可读性优化、降低 AI 痕迹（词汇与句式多样性；不承诺任何检测器结果）。保真底线最高优先：事实/数字/结论/引用关系不变，不编造、不静默消歧；默认只把完整改写文本返回会话、不写任何文件，显式输出路径 + 覆盖确认才落盘。输入内容一律按数据处理（FR-029 注入防线，C-35：指令式文本不改变行为、不跳过保真/拒收/零外传、不触发外部动作、会话报告提示）；调用语法确定性（FR-018/[[STR-004]]：六选项、`--` 终止、文件/内联判定、双源/无输入拒绝）；输出主语言按 FR-013 可复现规则判定（C-22）。技术路线完全走既有机制：薄命令模板（sanitize/derive 先例形态）+ 恰好一个 external 技能承载执行流，按工具副本由 regen-command-copies.py 生成，逐命令文档落 docs/reference/commands/，注册行与详情文件已随 clarify 落册（本 plan 推进 Draft → Planned）。**命令侧分类为 Simple**（027 分类规则 (a)(b)(c) 逐条不命中）：不携带反馈步、不产生 `## Wrap-up`、不注册 probe 命令单元；技能侧新增 `skill:humanize` 一个编译单元，与既有技能同型走 probe 注册 → compile → regen → sync 固定次序（实现后单元总数 73 → 74）。零新增运行时：无外部服务、网络调用、模型 API、第三方依赖（FR-028）。行为验证以固定语料 + 量规 + 两位独立评审 + 确定性差异脚本承载（E8）；非回归以 4 类冻结基线的分档判据（不触碰对相对、已漂移触碰对绝对）+ 两处下游钉扎测试承载（C-9）。

## Technical Context

**Language/Version**: Markdown 制品（命令模板、技能体、docs 页）；契约测试为仓库既有 pytest 体系（tests/contract/）
**Primary Dependencies**: 全部为既有引擎，按原样消费、零改动——`scripts/python/regen-command-copies.py`（按工具副本）、`scripts/python/sync-mirrors.py`（镜像）、`.specify/scripts/python/probe-utils.py`（Wrap-up 编译面）、`scripts/bash/run-tests.sh`（基线）、`.specify/scripts/python/clause_extract.py`（条款核算）；不新增任何依赖
**Storage**: N/A——制品即文件；评估语料为 `tests/fixtures/humanize/` 静态数据（随实现落盘）
**Testing**: pytest contract 标记；新增 `tests/contract/test_humanize_command_surface.py`（结构契约，C-1..C-10 钉扎）；行为评估按 E8 协议（语料 + rubric + 两位独立评审 + 差异脚本），记录落 verification.md
**Target Platform**: 技能/提示词框架层——宿主 agent 按技能体执行改写，无运行时进程（宪法 IX）
**Project Type**: 框架源（两顶帽子：全部编辑落框架源侧 `templates/`、`skills/`、`shared/`、`tests/`、`docs/`，镜像经 sync-mirrors 特性限定同步）
**Performance Goals**: N/A（Markdown 制品；改写质量由量规与保真约束承载，不由性能指标承载）
**Constraints**: 零新增运行时面（FR-028，C-8）；保真优先于语气与任何其他条款（FR-016 → C-16）；输入内容一律按数据处理（FR-029 → C-35 注入防线）；模板措辞项目中立；基线判据分档——生成面绝对（当前零漂移）；镜像面不触碰对相对、已漂移触碰对（probe-definitions）同步后绝对字节一致；编译面相对（既有 73 单元漂移先于本规格，新单元须带当前指纹）；测试面相对冻结名单（零新增失败节点）
**Scale/Scope**: 17 项交付面（feature-ref.md 清单）；契约 35 条款（C-1..C-35，`clause_extract` 实跑派生；C-35 落 rewrite-behavior.md 末节）；FR 映射 29/29；SC 映射 11/11；命令分类 Simple、技能编译单元 1 个（实现后 74 单元）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，16 项；初步自评，同作者门委派复核结果见下文 Re-check 记录）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 全部设计决策溯源 requirements.md FR-001..029（feature-ref.md 映射表逐行，29/29 由 clause_blocks 实跑验证） |
| II | Feature-Centric Development | ✅ Pass | Feature 062 已随 clarify 落册（注册行 + features/062.md）；本 plan 推进 Draft → Planned，不越权 Implemented（C-6） |
| III | Intent-Driven Development | ✅ Pass | 契约表达「什么行为、什么边界」（四维度/保真/语气），执行「怎么做」留给技能工作流与实现期 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | 交付面为 Markdown 制品 + 测试资产（template-only 形态），依 VII 门判 Partial（正当化）；结构契约测试仍先于制品落盘（红=断言的路径/字面尚不存在） |
| V | AI Agent Integration Standards | ✅ Pass | 分发经既有按工具副本机制覆盖全部受支持工具的既有副本目录（C-4）；AGENT_CONFIG/_ASSISTANT_TIERS 零改动（C-8） |
| VI | Continuous Quality & Observability | ✅ Pass | docs 页与命令输出义务含上下文与诚实措辞（C-5/C-10）；首版排除项显式（requirements Out of Scope）；无投机特性 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass (NON-NEGOTIABLE gates) | 复用优先已履行——既有 Feature 覆盖盘点见 requirements.md § Clarifications（2026-10-19 记录），plan 不复述其计数；绑定先例=新命令各占一 Feature；template-only 门用于 IV；状态推进不越权 |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 事实全部实测自源码/引擎（副本目录、镜像对、probe 行形态、--unit 行为），dated record 落 notes/ 与 quickstart |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新增运行时/服务/依赖/常驻进程（C-8）；改写由执行命令的 agent 完成；最简制品形态（薄模板 + 单技能） |
| X | Documentation Naming & Location Conventions | ✅ Pass | `docs/reference/commands/humanize.md` 小写落惯例路径；`SKILL.md` 工具强制名保留；无保留名占用 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已命名：框架制品编辑全落源侧（`templates/`、`skills/`、`shared/`、`tests/`、`docs/`），镜像随 sync 落位；`.specify/memory/features*.md` 属项目运行态记录（非框架镜像，直接编辑是注册义务而非镜像手改）；本特性即用 SDD 流程开发自身能力（Dogfooding 本体） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 regen/sync/probe-utils/run-tests/clause_extract 既有引擎；无新工具、无新脚本引擎（E8 差异脚本是测试资产非运行时） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Reliable Delivery 维度（agent 产出对人类读者可读可交付）；引用 better-harness 锚定，不另立目标模型 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 字面量单一落点：[[STR-001..004]] 在契约/数据模型中以引用出现（2026-10-19 复核删除了 C-25/C-29 与 data-model E4 的枚举复制）；命令引用技能零工作流复述（C-2）；计数取程序输出不复写（quickstart S5；C-7/S7 的 48/73 口径取程序派生） |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 拒收消息义务「指出问题 + 支持格式/集合」（C-27/C-29/C-31）；检测器措辞诚实声明（C-10）；docs 页自带输入形态与缺省行为（C-5） |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 4 项基线改动前冻结（notes/）；既有漂移披露采用相对判据不静默修平；同作者评分委派 fresh-context 只读子代理，12 项发现逐项按纠正/裁定判据分流（记录见 § Same-Author Scoring Record） |

**Gates Status**: ✅ 全部通过——唯一 ⚠（IV）为 VII 门明文允许的 template-only 正当化形态，见 Complexity Tracking。

**Re-check after Phase 1**: 2026-10-19——Phase 1 产物（data-model.md、contracts/ ×3、quickstart.md、feature-ref.md）落盘后复核：IV 维持 Partial（交付面性质不变）。同作者门按 `.specify/shared/workflow/objective-analysis-gate.md` 委派 fresh-context 只读评分者对 16 行独立评分，评分记录见本文件末尾 § Same-Author Scoring Record。repair round 1（2026-10-19）：analyze 门 HIGH=2 修复传播后再次委派 fresh-context 只读评分者复核 16 行——16/16 confirm（IV 维持 Partial），0 项翻盘；发现与处置记录已并入 § Same-Author Scoring Record。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/062-humanize-command/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # 无独立文件——Phase 0 发现内联于本文件 § Phase 0（<50 行且全内部证据）
├── requirements.md      # /speckit.requirements 产物（已澄清）
├── checklists/requirements.md  # 质量清单（requirements 阶段 16/16 pass）
├── checklists/requirements-quality.md  # 调查清单（checklist 阶段新增，f2fe4027）
├── data-model.md        # Phase 1 output — 8 实体（E1–E8）+ 30 条校验规则
├── quickstart.md        # Phase 1 output — 8 场景（S1–S6 实跑留痕 + S7–S8 逐例免责）
├── contracts/           # Phase 1 output — 3 文件 35 条款
│   ├── command-surface.md          # C-1..C-10：命令面、分发与登记
│   ├── rewrite-behavior.md         # C-11..C-23 + C-35：四维度改写行为、保真与注入防线
│   └── tone-input-file.md          # C-24..C-34：语气、输入解析与文件行为
├── feature-ref.md       # Phase 1 output — FR 29/29 映射 + SC 11/11 映射 + 交付清单 + 基线记录
├── notes/               # 冻结基线（本 plan 产出，6 文件）+ 后续阶段新增记录（source-requirement.md[requirements 修复轮]；pre-change-measurements.md、red-first-evidence.md、e8-run/[implement 期]）
│   ├── baseline-regen-check.txt       # 生成面基线（零漂移）
│   ├── baseline-mirror-check.txt      # 镜像基线（209 条既有 DIFF；第 181 行为触碰对 probe-definitions.md）
│   ├── baseline-test-run.txt          # 测试基线全量日志（`*.log` 被 git 忽略，取 .txt 可提交形态）
│   ├── baseline-failed-tests.txt      # 71 条排序失败节点名单（SC-008 对照基线）
│   ├── baseline-compile-check.txt     # 编译面基线（73/73 旧指纹漂移，逐单元名单）
│   ├── baseline-compile-unit-no-scope.txt  # `--unit` 不限定 compile-embeds 范围的实测留痕
│   └── source-requirement.md          # 语义权威与源需求原文 dated record（requirements 修复轮归档）
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
templates/commands/                   # 新增 humanize.md（薄命令模板源，Simple 分类）
skills/external/humanize/             # 新增 SKILL.md（external 执行技能，唯一执行流承载者）
shared/definitions/                   # 增强 probe-definitions.md（skill 侧一单元行 + 一绑定行；命令侧零单元）
docs/reference/commands/              # 新增 humanize.md（逐命令参考文档）
.specify/specs/027-feedback-mechanism/contracts/  # 增强 command-classification.md（humanize=Simple 行 + Result 计数）
tests/contract/                       # 新增 test_humanize_command_surface.py；更新两个下游钉扎测试（分类、技能可见性）
tests/fixtures/humanize/              # 新增：评估语料 + rubric.md + 确定性差异脚本（E8，随实现落盘）
.claude/commands/ 等 4 个副本目录      # 生成面：regen-command-copies.py 产出（禁手改）
.specify/skills/humanize/             # 镜像：skills/external 平铺对
.specify/shared/definitions/          # 镜像：shared 对（probe-definitions）
```

**Structure Decision**: 本特性落在既有框架源布局内，无新顶层目录——命令模板入既有 `templates/commands/`（sanitize/derive 的兄弟位）、技能入既有 `skills/external/` 平铺镜像体系、probe 注册入既有 `shared/definitions/probe-definitions.md` 单元表、docs 入既有逐命令目录、测试入既有 `tests/contract/` + `tests/fixtures/` 体系。模板不落 `.specify/templates/commands/`（该镜像已退役，per-tool copies 是唯一分发面）。

### Mirror Obligations *(mandatory)*

同步引擎：`scripts/python/sync-mirrors.py`（MIRROR_PAIRS 实测：skills/external 平铺、skills/internal 嵌套、agents、scripts、shared、templates-排除 commands 六对形态）。**基线漂移（2026-10-19 实测）**：`sync-mirrors --check` 报 209 条既有 DIFF；其中 `shared/definitions/probe-definitions.md`（第 181 行）是本特性**触碰对**——对已漂移的触碰对，「零 NEW drift」没有判别力，判据取特性限定同步后**绝对字节一致**；其余不触碰对取零 NEW drift（相对）。全量留痕 `notes/baseline-mirror-check.txt`。`docs/`、`tests/`、`.specify/memory/`、`.specify/specs/` 不在 MIRROR_PAIRS，无镜像义务（直接落位）。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/humanize.md`（新增） | `.claude/commands/speckit.humanize.md`；`.github/prompts/speckit.humanize.prompt.md`；`.opencode/command/speckit.humanize.md`；`.qoder/commands/speckit.humanize.md` — per-tool copies via regen-command-copies.py；NO `.specify/templates/commands/` mirror（retired） | 相对 `notes/baseline-regen-check.txt`：新副本落位且与模板一致，其余副本零变化（「no NEW drift」判据；复跑 `--check` 实测，不预写退出码） |
| `skills/external/humanize/SKILL.md`（新增） | `.specify/skills/humanize/SKILL.md`（平铺对，新增） | 特性限定同步后**绝对字节一致**（新对无既有漂移可作相对基线） |
| `shared/definitions/probe-definitions.md`（增强） | `.specify/shared/definitions/probe-definitions.md`（shared 对；基线**已漂移**，见第 181 行） | 特性限定同步（`--only shared/definitions/probe-definitions.md`）后**绝对字节一致**；同步不拖入其他对 |
| `tests/contract/test_humanize_command_surface.py`（新增）及两个下游钉扎测试（更新） | 无镜像（tests/ 不在 MIRROR_PAIRS） | pytest 直跑；分类测试与可见性测试必须绿（C-9） |
| 技能体的编译 `## Wrap-up` 面 | 由 probe-utils compile-embeds 维护（`skill:humanize` 一个单元注册后编译）；命令侧 Simple，无编译面 | C-7 固定次序；相对 quickstart S3 判据（73/73 既有旧指纹漂移先于本规格；新单元落位带当前指纹；`--unit` 不限定范围已实测） |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First 判 ⚠ Partial | 本特性交付面为 Markdown 制品（命令模板/技能体/docs/注册行）+ 测试资产（契约测试与语料），无纯函数与运行时行为可单测；按宪法 VII 门「template-only features judge Test-First as Partial (justified)」处理，「tests」验证模板内容、canonical 路径与结构 | 把改写逻辑实现为可执行运行时以换取「完整单测覆盖」——违反 FR-028 与宪法 IX（框架非运行时平台，改写由执行命令的 agent 完成）；行为面改由 E8 评估协议（量规 + 差异脚本）承载，结构面由契约测试承载（060/057 先例形态） |
| 行为面无可自动化的回归守卫（IV 的延伸） | 「人性化」的通过判据是语义与语用判断，确定性程序只能守结构（路径/字面/计数）与保真差异（受保护内容逐项比对、编造检测），不能判语气自然度；行为质量由 E8 的固定语料 + `rubric.md` 两位独立评审协议承载 | 以 LLM 自动评分替代人工评审——引入非确定性判据与新的模型依赖（违反 FR-028/IX），且与「同一评审判据可复现」冲突；以检测器分数作判据——FR-006/FR-027 明文禁止承诺检测器结果 |

## Phase 0: Research Review

无独立 research.md——发现内联（全内部证据，2026-10-19 勘探实测；代码面勘察由 Explore 子代理执行、回报无异常，引擎行为由本 plan 直接实跑复测）：

- **命令模板先例形态**：sanitize.md（frontmatter 仅 `description`+`short-description`，`## Delegation` 节承载技能/输入/产出三行）与 derive.md（frontmatter 另含 `handoffs:`）两型并存；humanize 取 sanitize 型（无脚手架前置脚本需求，无 `scripts:` 块）。裁决记录 D-1。
- **技能面与镜像**：`skills/external/` 13 目录平铺镜像到 `.specify/skills/<name>/`（host 发现面）；internal 37 目录嵌套（路径引用面）。humanize 为通用内容能力 → external（clarify 裁决，词汇表判据复核维持）。frontmatter `skill_id: <SKILL:.specify/skills/humanize/SKILL.md>`。裁决记录 D-2。
- **命令分类（纠正级发现）**：`.specify/specs/027-feedback-mechanism/contracts/command-classification.md` 的规则是机械判据——Complex 当且仅当 (a) 调用脚本/CLI、(b) 产出被下游流程消费的制品、(c) 消费上游流程制品；humanize 三条都不命中 → **Simple**。Simple 命令 MUST NOT 携带反馈步/`## Wrap-up`（实测：agents/constitution/feature 三个 Simple 模板无 Wrap-up、无 probe 命令单元）。因此本特性只在技能侧注册一个单元；两处下游钉扎测试须随之更新并转绿（见下条）。
- **副本生成引擎**：`regen-command-copies.py` 委派 `generate_commands`（`src/specify_cli/__init__.py`），仅对既有副本目录生成（实测 4 个：`.claude/commands`、`.github/prompts`、`.opencode/command`、`.qoder/commands`）；命名 `speckit.<name>.md`（copilot `.prompt.md`）；`--check` 模式存在且当前零漂移。裁决记录 D-3（副本目录集以实测为准，不预设不存在的工具目录）。
- **probe 注册面**：技能单元行 `skill-<name>-wrapup | skill-wrapup | skill:<name> | wrap-up` + `h-docs-sync-eval @point:wrap-up` 绑定行（技能 wrap-up 注册行程序实测 48 条——两项既有技能有编译面无注册行，属既有状态；humanize 按同型注册 `skill-humanize-wrapup`）。命令侧因 Simple 分类不注册单元（编译单元 73 = 23 命令 + 50 技能，实测）。编译次序 注册 → compile → regen → sync。`compile-embeds --check` 当前 73/73 旧指纹可再生漂移（先于本规格），`--unit` 实测不限定范围——Verify 取相对判据（纠正级处置，quickstart S3 披露）。
- **下游钉扎测试（实现期必须随分类更新并转绿）**：`tests/contract/test_feedback_command_classification.py` 从 027 契约表派生分类，钉扎 23 complex / 3 simple 与模板计数——humanize 加入后 simple 变 4，契约表与 Result 行须同批更新；`tests/contract/test_skill_layer_visibility_guards.py` 钉扎 external 普查（13）与平铺发现面——humanize 加入后为 14，internal 37 不变。两者均**不在**冻结的 71 条失败名单中，故 SC-008 的「零新增失败」要求它们复跑必须绿，正是分类修正的机械守卫。
- **文档落点**：`docs/reference/commands/` 为逐命令文档惯例路径；实测无命令总花名册页（README.md、docs/concepts/overview.md、docs/reference/agents/command-and-skills.md 对近期命令名零命中）——本特性只新增 `docs/reference/commands/humanize.md`，无花名册同步义务。裁决记录 D-4。
- **测试先例**：`tests/contract/` 有命令面契约测试先例（test_docs_command_template.py、test_sanitize_template.py、test_qoder_command_frontmatter.py 等）；`tests/fixtures/` 为分特性子目录形态；`run-tests.sh --names-out` 接口实测可用。行为评估语料按 E8 布局落 `tests/fixtures/humanize/`。裁决记录 D-5。
- **基线冻结（本 plan 产出，4 类 / 6 文件）**：生成面零漂移（`baseline-regen-check.txt`）/ 镜像 209 条既有 DIFF（`baseline-mirror-check.txt`；其中第 181 行 `probe-definitions.md` 为触碰对，判据为同步后绝对字节一致）/ 编译面 73/73 旧指纹（`baseline-compile-check.txt`；`--unit` 不限定范围留痕 `baseline-compile-unit-no-scope.txt`）/ 测试 71 failed、3929 passed（`baseline-test-run.txt` + 冻结名单）。裁决记录 D-6：基线在 plan 期冻结（060 先例 notes/ 形态），实现期 `comm -13` 对照。
- **术语复核**：glossary 技能分类判据唯一指向 external（与 spec-kit 无依赖、任何项目皆可直接使用）——humanize 判 external 维持，无冲突。语气字面取 [[STR-002]] 英文集合，中文释义在技能/docs 中并列展示。裁决记录 D-7。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 8 实体（E1 命令模板 / E2 执行技能 / E3 请求 / E4 源内容 / E5 结果 / E6 语气画像 / E7 保真约束 / E8 评估语料）+ 30 条校验规则（V-E1×4 + V-E2×4 + V-E3×5 + V-E4×4 + V-E5×4 + V-E6×2 + V-E7×3 + V-E8×4） |
| Contracts | [`contracts/`](contracts/) | 3 文件 35 条款：command-surface.md（C-1..C-10）+ rewrite-behavior.md（C-11..C-23, C-35）+ tone-input-file.md（C-24..C-34）。计数与 FR 覆盖由程序派生（quickstart S5 实跑 repair round 1：`clause_extract` 合计 35、`clause_blocks` FR 覆盖 29/29 missing NONE） |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 场景（S1–S6 已实跑留痕，S5/S6 于 repair round 1 复跑；S7–S8 实现期场景逐例免责 + 前提清单） |
| Feature ref | [`feature-ref.md`](feature-ref.md) | FR 29/29 映射 + SC 11/11 映射 + 17 项交付清单 + 5 类基线记录 |
| 冻结基线 | [`notes/`](notes/) | 4 类 / 6 文件：regen（零漂移）/ mirror（209 既有 DIFF，含触碰对第 181 行）/ compile（73/73 旧指纹 + `--unit` 不限定范围留痕）/ tests（71 条失败名单） |

Phase 0 预期 vs 实际（round 1 记录，dated record——repair round 1 传播后的现行计数以本文件 Scale/Scope、§ Phase 1 汇总表与 quickstart S5 复跑输出为准）：契约文件 3（预估 2–3 ✓）；实体数 8（requirements Key Entities 5 项 + 交付制品 3 项 ✓）；quickstart 场景 8（预估 6–8 ✓）；FR 覆盖 28/28、零缺失（程序派生 ✓，round 1 时点）；同作者评分 12 项发现全部关闭（见下节），分类与基线表述的纠正已并入本文件与全部兄弟产物。

## Same-Author Scoring Record

**条件声明**：本 plan 与全部 Phase 1 产物由同一执行者撰写；检测委托按 `.specify/shared/workflow/objective-analysis-gate.md` 执行——一名 fresh-context 只读评分者，输入为 requirements.md、本 plan、Phase 1 四类产物与 notes/ 基线，按宪法 16 行与工件内部一致性独立核查，返回 12 项发现；评分者无写权限、不参与修复。

**处置结果**：
- 12 项发现经逐项独立复核：**11 项纠正级 + 1 项非阻断清理（已完成）**；0 项裁定级、0 项驳回、0 项需上抛。降级率 12/12（全部关闭于本层，0 项保留为阻断）。
- 复核基准：每项均回到记录性 owner 判定，而非由本代理自证——027 分类契约（机械规则）、`sync-mirrors --check` 基线留痕（逐行）、`probe-utils` 实测、两处下游测试文件的断言正文、宪法与工程约定文档。凡 owner 只有一种读法者为纠正；无一项需要发明未记录意图，故无裁定上抛。
- **分类纠正（本 plan 阶段新增发现，已在全部兄弟产物传播）**：按 027 规则 humanize 为 **Simple**——命令侧不得携带 `## Wrap-up`、不得注册 probe 单元；只有技能侧注册 `skill-humanize-wrapup`。该事实改正了初稿的命令侧编译面设计，并同步到 C-1/C-7/C-9、data-model E1、quickstart S2/S3/S7、feature-ref、本 plan 与注册表记录。属纠正级（owner 机械判据唯一读法），在此显式披露。
- **宪法复评**：评分者的逐行结论未推翻自评——无 Pass→Fail 翻盘；IV Partial 维持并依 VII 门正当化；纠正项均为证据/一致性缺陷，无原则违反。
- **遗留**：无阻断项。行为面的语义判据不在确定性程序能力内（见 Complexity Tracking 第二行），由 E8 评估协议承载，属已记录的范围边界而非未决问题。

**Repair round 1 addendum（2026-10-19）**：本轮按 analyze 门（HIGH=2）修复简报向 plan 与 Phase 1 产物传播裁定（新增 C-35；H-01/H-02/B-01/U-01..07/F-01..04/L-01..03 落位）。同作者条件声明（mixed set）：本轮新增/修改内容为本执行者所写，既有产物主体先于本会话（五个前序派发作者）——按 gate 的 mixed-set 规则，委派一名 fresh-context 只读评分者对 16 行宪法检查与本轮传播一致性独立复核；briefed premises 全部先经程序派生（`clause_extract` 合计 35 = 10+14+11、`clause_blocks` FR 覆盖 29/29 missing NONE、`validate-requirements.py` exit 0、技能 wrap-up 注册行 48、编译单元 73 = 23 命令 + 50 技能）。

- **复核结果**：16/16 行 confirm（IV 维持 Partial 依 VII 门正当化），0 项翻盘；FR-029/FR-018/FR-013/FR-021/FR-008 五条传播链（C-35/E4/E7/E8/S8/feature-ref、C-1+C-28、C-22、C-30/C-31、C-17+C-33）一致性确认；计数与基线前提复验全部成立。
- **4 项发现的处置**：① plan「Phase 0 预期 vs 实际」行的 round-1 计数（28/28）未标轮次——按 One-Source-Of-Truth 的 dated-record 类补「round 1 记录」标记并指向现行计数（纠正级，就地完成）；② C-22 复述 FR-023 的分段语言规则但引用组缺 FR-023——引用组与溯源行补 FR-023，feature-ref FR-023 行同步列 C-22（纠正级，就地完成）；③ `.specify/memory/features.md` 062 行仍记 round-1 计数（34 条款/FR 28/SC 10/27 规则）——注册表编辑按修复简报 G-01 属 tasks 修复轮范围，本轮不越范围，作为上送披露由下一轮处理；④ `account-clause-coverage.py` 仅匹配 ASCII 括号引用组（本契约集用全角括号，13/29 不命中）——既有工具/书写惯例分歧，未产生虚假声明（门的覆盖核径为 `clause_blocks` 正文扫描），非本轮修复面，留作观察披露。降级率：4 项中 2 项纠正级就地关闭、2 项披露上送，0 项裁定级阻断、0 项驳回。
