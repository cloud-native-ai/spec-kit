# Dogfooding Dry-Run Plan — Spec Kit docs/ 激进重组（spec 033 US4 / FR-008）

- scope: full sweep, aggressive re-taxonomy (user-directed baseline, Clarifications 2026-07-28)
- generated: 2026-07-28 (R4 artifact; no writes performed while planning)
- 每行可勾选退出：`[x]` = 执行；改为 `[ ]` = 本次跳过

## A. 归位搬迁（move — 需确认）

- [x] M01 docs/installation.md → docs/tutorials/installation.md
- [x] M02 docs/quickstart.md → docs/tutorials/quickstart.md
- [x] M03 docs/spec-driven.md → docs/concepts/spec-driven.md
- [x] M04 docs/overview.md → docs/concepts/overview.md
- [x] M05 docs/vibe-coding.md → docs/concepts/vibe-coding.md
- [x] M06 docs/upstream.md → docs/concepts/upstream.md
- [x] M07 docs/security.md → docs/concepts/security.md
- [x] M08 docs/glossary.md → docs/reference/glossary.md
- [x] M09 docs/commands/ → docs/reference/commands/（19 个命令参考）
- [x] M10 docs/cli/ → docs/reference/cli/（8 个工具参考）
- [x] M11 docs/skills/ → docs/reference/skills/
- [x] M12 docs/agents/ → docs/reference/agents/
- [x] M13 docs/teams/ → docs/reference/teams/
- [x] M14 docs/history/ → docs/reference/history/（既有蒸馏知识库，只读迁移）
- [x] M15 docs/summary/03-sdd-workflow-refactor-proposal.md → docs/archive/（派生报告，归档）

## B. 新建（safe write — 自动层，列出备审）

- [x] N01 根 ARCHITECTURE.md（≤一屏，摘要 concepts + decisions）
- [x] N02 根 CONTRIBUTING.md（≤一屏，摘要 docs/contribute/）
- [x] N03 根 CHANGELOG.md（自包含时间线stub，Unreleased 节）
- [x] N04 docs/decisions/README.md + template.md + 0001-adopt-docs-taxonomy.md（ADR-0001：采纳六类 taxonomy 的决策记录）
- [x] N05 docs/concepts/documentation-model.md（文档模型 What & Why——两份设计笔记的正式归宿）
- [x] N06 docs/contribute/dev-setup.md（开发环境最小指引，承接 CONTRIBUTING.md）
- [x] N07 docs/tasks/README.md（占位索引：任务式文档的落点说明）
- [x] N08 docs/notes/README.md（notes 规则 + frontmatter 模板）

## C. Notes 退场（生命周期）

- [x] X01 docs/notes/docs-design.md：补 frontmatter → status: archived, target: docs/concepts/documentation-model.md，正文顶部标注归宿
- [x] X02 docs/notes/notes-design.md：同上（同一归宿文档的 lifecycle 章节）

## D. 一贯性同步（重组随动，必须与 A 同批执行）

- [x] S01 README.md 收敛 ≤60 行 + 文档导航表更新至新路径（含修复断链 docs/skills/vscode.md）
- [x] S02 全 docs/ 内部相对链接与 docs/reference/commands/todo.md 断链修复
- [x] S03 测试钉点同步：test_ai_tools_support_surfaces.py（installation/quickstart 路径）、test_shared_reference_rewrite.py（5 个 docs 路径）、test_docs_command_template.py（quickstart/参考文档路径）
- [x] S04 .specify/instructions.md Documentation Map 更新（AGENTS.md 等符号链接自动随动）+ docs/notes/ 行状态
- [x] S05 templates/commands/docs.md 等源内 `docs/commands/docs.md` 引用改 `docs/reference/commands/docs.md` + regen --check

## E. 容忍（不动）

- docs/assets/（图片资源辅助目录，非文档类型，容忍）
- 根部 AGENTS.md/CLAUDE.md/QODER.md/QWEN.md/LICENSE（工具/生态强制名，锚点区）
- .github/skills、.github/agents 符号链接（C 区锚点）
