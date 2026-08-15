# 主题：SDD 全周期特性开发（requirements → plan → tasks → implement）

覆盖会话：207f8d40 (2026-06-22, Feature 018 Codex/Tier)、5878b07d (2026-06-25, Feature 021→022 agent-specific-config)、5ee06f07 (2026-07-03, Feature 022 EEI Supervisor + git-submodule-edit)、b252f216 (2026-07-17, Feature 031 词汇表)。相关：[[00-cross-cutting-lessons]]、[[03-framework-mechanics]]。

## 1. 关键决策与理由

- **规格绑定策略（两次同构决策）**：新特性优先绑既有 Feature 而非新建——021-agent-specific-config 绑 Feature 022（AI Tools Support 的运行时延伸）；EEI 三角绑 Feature 019（组合式增强而非独立特性）。
- **in-place amend ≠ 重跑脚手架**（5ee06f07）：`create-new-plan.sh` 无条件覆盖 plan.md，Amend 既有 feature 时原地追加 § Plan Amendment + 追加任务 T032–T057，保留历史。
- **承载方式差异化**（5878b07d）：4 个技能用 `references/<agent-slug>-guide.md` 子文档，3 个命令模板内联 guidance——避免重构被大量引用的单文件模板；放弃"命令模板转目录"与"共享 templates/commands/references/"两方案。反馈集中存 `.specify/memory/feedback/`（弃 `${SKILL_HOME}/feedback/` 就近存放）。
- **Codex 接入走配置驱动**（207f8d40）：`generate_commands()` 从模板配置生成，只需加 `_OFFICIAL_ASSISTANT_KEYS` + config dict + init 三处 case；引入 `_ASSISTANT_TIERS`（Tier 1 CLI 形态 / Tier 2 非 CLI）。契约 enum 缺 `codex` 时选择补契约而非放宽测试。
- **模板中立性约束**（207f8d40）：constitution-template 保持项目无关，项目特定修正只落 `.specify/memory/constitution.md`；T042 deferred。
- **词汇表定位为文档/提示词框架工件而非运行时设施**（b252f216，Constitution Principle IX / No-DFX）；单一项目级 `.specify/memory/glossary.md`（弃 per-feature 副本）；引擎 stdlib-only `glossary-utils.py` 复刻 feedback-utils 风格；冲突/覆盖必须 `--confirmed-resolution` 单一卡点。
- **EEI supervision 是 prompt 指令而非 runtime scheduler**（5ee06f07，守框架范围约束）；6 个角色模板只加 `supervisor: true` + `role-scope:` 元数据，由 create-agent 内联单一 canonical snippet（弃 include/复制到每角色——模板系统无 transclusion、复制有漂移风险）。
- **git-submodule-edit 技能**：submodule 内建 `project-<项目名>/<topic>` 分支（owner 可识别来源项目），gitlink bump 与 `submodule-edits.md` 台账同行提交保持同步。

## 2. 可复用经验 / 踩坑

- 完整 SDD 链（多会话一致）：`/speckit.requirements`（建分支）→ `/speckit.clarify` Mode A 顺序提问（每次一题）→ `/speckit.plan`（动态 Constitution Check + contracts + quickstart）→ `/speckit.tasks`（Tests Mode ON，`- [ ] [TaskID] [P?] [Story?]`）→ `/speckit.implement`（TDD 逐阶段、Pre-Status-Flip Gate、verification.log 播种回填、features.md Planned→Implemented、commit-template 渲染后用户 yes 确认）。
- **Pre-Status-Flip Gate 实操**：`grep -cE '^\- \[ \]'` 必须为 0；verification.log 每 SC-NNN 补 status 行；SC 行在 requirements 出现两次会双算，需核对唯一 SC 数；deferred 任务登记 `<!-- deferred: reason -->` + deferred_tasks 注册表。
- 模板/提示词类特性的 Test-First 记为 **justified Partial**：无运行时代码，验证走结构化检查 + quickstart 清单，pytest 标 `[~]` deferred（T008/T013 模式）。
- 含 `${...}` 字面量、模板锚点不统一（tools.md 无 `## Handoffs`）、additivity grep 假阳性（"Step" 命中技能自身流程）——契约测试需兜底分支 + 人工确认。
- 批量内容生成（8 份 reference 文档）可交并行 agent，完成后用确定性测试验收。
- pytest 基线：`.venv` 无 pytest 但系统有（`/usr/local/bin/pytest`）→ 先探测；先记基线（97 failed/660 passed），收尾 diff 失败集定位唯一回归。
- 正则坑：`TABLE_HEADER_RE` 误匹配 Column Definitions 表行 → 收紧要求第二列 `Variants`；`ugrep` 下正则转义误报 → 改 `grep -F` fixed-string。
- git 合并验证后清理：`git branch --merged` + 0 未合入提交 → `-d` 安全删除，只删本地不动远程。

## 3. 未完成 / 待办

- SC-006 类"采用后使用率指标"在两个特性中均 deferred（需真实使用数据 / live run）。
- Reference 文档仅 Claude Code + Copilot 两 Agent；Qoder、Codex、opencode、Hermes 指南待扩展。
- `create-new-requirements.sh` 以 root 建 spec 目录的根因未查——下个 feature 会复发。
- 遗留同步：`contracts/agent-authoring-contract.md` R2 与 `plan.md` Open Questions 仍描述被取代的 dormant-by-default；review P1 未修（verification-log 命名被 `*.log` 吞、Test-First 无 "Tests N/A" 安放路径）。
- 多个会话以 `/exit` 结束，`/speckit.review` 建议未执行、分支未 push。

## 4. 关键交互流程

- Amend 流程（5ee06f07）：`/speckit.review`（产物 review.md 0 P0/2 P1/5 P2）→ `/speckit.plan` 原地追加 → `/speckit.tasks` 追加 → `/speckit.clarify` Mode C 解决 OQ 写回 → `/speckit.implement` 收 Gate 后翻状态。
- `/speckit.skills` 编排流：解析目标 → 查 `.specify/skills/<name>/SKILL.md` 存在性 → 路由 create-skills / improve-skills → 脚手架/两阶段（Phase A 合规清单 → Phase B 用户优化）→ 注册 instructions Skills 表（去重排序）→ 校验（frontmatter、<500 行、`${SKILL_HOME}` 约定、真实冒烟）。

## 5. 用户 ↔ 模型的冲突/分歧点

- OQ-1 激活模型：用户主张 default-on（6 角色默认开启 EEI supervision）；模型推荐 opt-in + dormant section；最终 default-on（`false` 为 opt-out），DoD-8/T034 起全部重写。
- submodule 分支规范：用户主张 `project-<项目名>/*` 且 PR 列明受影响消费者与迁移步骤；模型原本 `parent/<PARENT_SLUG>/<topic>`；最终按用户规范重新端到端冒烟。
- references/ 归属：用户主张仅用于 skills、命令模板内联；模型推荐共享 references/ 目录；最终按用户方案改写 FR-005/FR-011。
- 反馈存储：用户主张集中 `.specify/memory/feedback/`；模型推荐就近 `${SKILL_HOME}/feedback/`；最终集中式（FR-009）。
- 前提核查：用户称"owner 已修复直接继续"；模型发现澄清版 requirements 并未落盘；最终自行回填 staged 成品再继续。用户称"两分支已合并可清理"；模型先独立验证再删。
