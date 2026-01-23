# GitHub Copilot 指令集开发指南（Spec Kit 项目）

**🚨 🚨 🚨 CRITICAL CONTEXT - PAY EXTREME ATTENTION 🚨 🚨 🚨**

**>> 当前项目是 spec-kit 的源代码项目。 <<**  
**>> 这个项目本身也使用 spec-kit 辅助开发。 <<**  
**>> 当前项目中存在两套 spec-kit 的相关文件：一套是作为 spec-kit 用户（主要在 `.specify` 目录和 `.github/prompts` 目录中），一套是作为 spec-kit 开发者（主要在 `src`、`templates`、`scripts` 等目录中）。 <<**  
**>> 在执行代码修改的时候要注意区分这两者。 <<**  
**>> 本地的修改应该只局限于作为 spec-kit 开发者的代码，MUST NOT 修改作为 spec-kit 用户的相关代码。 <<**

作为 Spec Kit 项目的开发者，本文档指导我们如何为 GitHub Copilot 设计和维护 AI 指令集，以支持 Spec-Driven Development（SDD，规格驱动开发）工作流。

---

## 开发目标与原则

- **核心目标**： 基于spec-kit开源项目实现一个自定义版本的Specification-Driven Development开发工作流，实现从"需求(spec) → 计划(plan) → 任务(task) → 实现(implement)"的端到端自动化支持，同时维护一个以特性(feature)为中心的项目文档结构。
---

## 架构设计

### 文件结构映射

作为开发者，我们需要维护以下文件映射关系：

| 源代码文件 | 安装后路径（用户项目） |
|------------|-------------|
| `templates/commands/analyze.md` | `.github/prompts/speckit.analyze.prompt.md` |
| `templates/commands/checklist.md` | `.github/prompts/speckit.checklist.prompt.md` |
| `templates/commands/clarify.md` | `.github/prompts/speckit.clarify.prompt.md` |
| `templates/commands/constitution.md` | `.github/prompts/speckit.constitution.prompt.md` |
| `templates/commands/feature.md` | `.github/prompts/speckit.feature.prompt.md` |
| `templates/commands/implement.md` | `.github/prompts/speckit.implement.prompt.md` |
| `templates/commands/plan.md` | `.github/prompts/speckit.plan.prompt.md` |
| `templates/commands/research.md` | `.github/prompts/speckit.research.prompt.md` |
| `templates/commands/review.md` | `.github/prompts/speckit.review.prompt.md` |
| `templates/commands/specify.md` | `.github/prompts/speckit.specify.prompt.md` |
| `templates/commands/tasks.md` | `.github/prompts/speckit.tasks.prompt.md` |

在 `specify init` 命令执行时，系统会自动将模板文件复制到对应的 IDE 提示目录。

## 开发最佳实践

- **一致性优先**：确保 Copilot 指令与 CLI 工具行为一致
- **渐进式开发**：按任务逐步提交，每步都通过质量门
- **可运行验证**：所有生成的示例/脚手架必须能实际运行
- **边界考虑**：充分考虑空值、并发、超时、权限等边界条件
- **安全合规**：遵守项目宪法，避免引入未评估的依赖
- **文档即产品**：将文档视为产品的一部分，保持规格-计划-实现一致性

---

## 与其他 Agent 的集成差异

作为 Copilot 专属指令集开发者，需要注意：
- Copilot 是 IDE 内置的 agent，不需要 CLI 工具安装
- 不依赖 `$ARGUMENTS`、`{SCRIPT}` 等 CLI 占位符
- 使用自然语言描述即可触发相应功能
- 目录结构遵循 `.github/prompts/` 规范

---

## 参考文档

开发过程中请参考以下项目文档：
- `spec-driven.md`：SDD 方法论与端到端工作流
- `README.md`：快速开始、受支持的 Agent、核心命令与示例  
- `AGENTS.md`：Agent 与目录/格式约定、占位符、扩展指引
- `CONTRIBUTING.md`：贡献/验证/测试与质量要求

> **重要提示**：修改 `src/specify_cli/__init__.py` 涉及 Agent 配置与行为时，必须同步提升 `pyproject.toml` 版本并更新 `CHANGELOG.md`（详见 AGENTS.md "General practices"）。