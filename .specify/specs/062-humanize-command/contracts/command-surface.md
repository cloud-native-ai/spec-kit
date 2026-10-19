# Contract: 命令面、分发与登记（command-surface）

**Feature**: 062 | **FR 覆盖**: FR-001, FR-024, FR-025, FR-026, FR-027, FR-028（以文末可追溯性表为准）
**性质**: 结构契约——判定命令模板、技能委派、按工具副本、docs 页、注册行与技能 feedback 面的存在性与形态。

## 命令模板与技能委派

- **C-1**: `templates/commands/humanize.md` 存在且为薄入口：frontmatter 含 `description`（带触发词列表）与 `short-description`、无 `scripts:` 块；正文节为 `## User Input`（`$ARGUMENTS` 接线 + User Input Protocol 引用 + 输入形态与调用语法声明——选项集 [[STR-004]]、`--` 终止选项解析、文件/内联输入判定按 FR-018）、`## Glossary`、委派节、`## Handoffs`。本命令按分类 owner `.specify/specs/027-feedback-mechanism/contracts/command-classification.md` 的 (a)(b)(c) 规则判为 **Simple**（不调用脚本、不产出/消费跨流程制品）——模板 MUST NOT 携带 `## Wrap-up`/feedback 步，同批在该 contract 的分类表新增本命令行并更新 **Result** 计数。模板正文对四维度改写工作流（FR-003 至 FR-006 的行为细则）的复述为零；[[STR-001]] 为命令身份字面 (FR-001, FR-018, FR-024, FR-025)。
- **C-2**: 命令模板的委派节恰好命名一个技能——runtime path `.specify/skills/humanize/SKILL.md`；命令与技能的引用方向为命令→技能（镜像路径），命令模板不复制技能工作流，技能体不回指命令模板 (FR-024)。
- **C-3**: `skills/external/humanize/SKILL.md` 存在，frontmatter 含 `name: humanize`、`classification: external`、`skill_id: <SKILL:.specify/skills/humanize/SKILL.md>`；技能体自足可加载——离开本仓 ambient 指令的宿主仅读技能体即可完成一次改写调用（引用真源 + 内联最小操作事实，057 C-34 先例形态）；技能正文对四维度、保真底线、语气处理、文件行为各有可执行落点 (FR-024, FR-002, FR-007, FR-015, FR-020)。
- **C-4**: 全部按工具命令副本由 `scripts/python/regen-command-copies.py` 生成：`.claude/commands/speckit.humanize.md`、`.github/prompts/speckit.humanize.prompt.md`、`.opencode/command/speckit.humanize.md`、`.qoder/commands/speckit.humanize.md`（以既有 4 个副本目录为准，不含不存在目录的工具）；生成副本含手改警告头；`regen-command-copies.py --check` 相对 `notes/baseline-regen-check.txt` 冻结基线零 NEW 漂移 (FR-025, SC-007)。

## 文档、注册与技能 feedback 面

- **C-5**: `docs/reference/commands/humanize.md` 存在，内容覆盖：输入形态（内联/文件）与调用语法要点、默认不写任何文件的行为、支持的语气集合（以 [[STR-002]] 引用，不逐字复制集合字面）、保真边界（FR-007 的文档面）、输入内容按数据处理的声明（外部文档内容不构成指令，FR-029 的文档面）、以及不承诺 AI 内容检测器结果的明确声明 (FR-025, FR-027, FR-029, SC-009)。
- **C-6**: 特性注册存在且可解析：`.specify/memory/features.md` 含 062 注册行、`.specify/memory/features/062.md` 详情文件存在，注册行的规格路径指向本规格 `requirements.md`；两者已于 clarify 落册（dated record 2026-10-19），实现期验证存在性而非重复注册；本 plan 推进状态 Draft → Planned（状态机真源 `.specify/templates/feature-details-template.md`）(FR-025, SC-007)。
- **C-7**: 技能侧 feedback 面（命令侧无）：框架源 `shared/definitions/probe-definitions.md`（镜像 `.specify/shared/definitions/probe-definitions.md` 经 sync-mirrors 对同步）新增 `skill-humanize-wrapup | skill-wrapup | skill:humanize | wrap-up` 单元行与 `h-docs-sync-eval @point:wrap-up` 绑定行——全部技能携带 feedback 步（all-skills 规则；技能 wrap-up 注册行程序实测 48 条：`grep -cE '^\| skill-[a-z0-9-]+-wrapup \|' shared/definitions/probe-definitions.md`；编译单元 73 = 23 命令 + 50 技能，其中两项既有技能有编译面无注册行，属既有状态——本条款引用程序口径，不复写计数）；技能体的 `## Wrap-up` 编译面由 `probe-utils.py --action compile-embeds` 产出；执行顺序为注册 → 编译 → regen 副本 → sync 镜像（固定次序，AGENTS.md Probe System 行）；不新增命令单元（命令为 Simple 类）(FR-025)。

## 非运行时与测试基线

- **C-8**: 零新增运行时面：无新增外部服务、网络调用、模型 API、第三方依赖、后台常驻进程；`src/specify_cli/` 与 `scripts/` 的既有分发机制（`generate_commands`/`regen-command-copies.py`/`sync-mirrors.py`）按原样消费、零改动；改写由执行该命令的 AI agent 在既有框架内完成 (FR-028, SC-010)。
- **C-9**: 确定性契约测试与下游钉扎面：新增 `tests/contract/test_humanize_command_surface.py` 逐条覆盖 C-1 至 C-8、C-10 的结构断言（canonical 路径、`[[STR-NNN]]` 字面钉扎、委派唯一性、无 Wrap-up 的 Simple 形态、检测器诚实措辞检索），测试先于制品落盘（Red-Green，宪法 IV 的 template-only 形态——红=断言的路径/字面尚不存在）。两项既有钉扎测试 MUST 同批转绿（它们不在冻结失败基线中，未更新即产生 NEW 失败）：`tests/contract/test_feedback_command_classification.py`（分类表覆盖 + `23 complex / 3 simple` 字面——Simple 增至 4 后契约表、**Result** 行与该测试字面同步更新）与 `tests/contract/test_skill_layer_visibility_guards.py`（`EXTERNAL_SKILLS` 名单与 `len(seen) == 13`——加入 humanize 并更新为 14）。非回归判据为相对冻结基线：排序失败测试名单相对 `notes/baseline-failed-tests.txt` 零新增（`comm -13` 为空）、镜像触碰对按 C-4/C-7 与 Mirror Obligations 判据、生成面按 C-4 (FR-026, SC-008)。
- **C-10**: 检测器诚实性措辞：命令模板、技能体、docs 页与命令输出中，检测器通过保证或规避声明的出现次数为 0；每一处对 AI 内容检测器的提及都伴随「不承诺结果」的表述；验证方式为全量文本检索逐条核对 (FR-006, FR-027, SC-009)。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| C-1 | FR-001, FR-018, FR-024, FR-025 | test_c01_thin_entry_shape（含 Simple/无 Wrap-up） |
| C-2 | FR-024 | test_c02_single_skill_delegation |
| C-3 | FR-024, FR-002, FR-007, FR-015, FR-020 | test_c03_skill_frontmatter_and_self_sufficient |
| C-4 | FR-025, SC-007 | test_c04_generated_copies_present |
| C-5 | FR-025, FR-027, FR-029, SC-009 | test_c05_docs_page_content |
| C-6 | FR-025, SC-007 | test_c06_registry_rows_resolve |
| C-7 | FR-025 | test_c07_skill_probe_unit_and_compiled_wrapup |
| C-8 | FR-028, SC-010 | test_c08_no_runtime_surface |
| C-9 | FR-026, SC-008 | test_c09_baseline_no_new_failures（基线对照 + 两项下游钉扎测试绿） |
| C-10 | FR-006, FR-027, SC-009 | test_c10_detector_honest_wording |
