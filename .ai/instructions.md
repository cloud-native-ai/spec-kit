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

- **核心目标**：构建一套完整的 SDD 工作流指令集，实现从"规格 → 计划 → 任务 → 实现"的端到端自动化支持
- **设计原则**：
  - 确保指令集与 CLI 工具保持功能一致性
  - 提供清晰的输入/输出契约定义
  - 支持高质量、可验证的代码生成
  - 维护文档与实现的一致性
  - 遵循项目宪法约束进行技术决策

---

## 指令集架构设计

### 1. 核心指令组件

我们的 Copilot 指令集包含以下核心命令，每个命令对应特定的 SDD 阶段：

- `/speckit.constitution` - 项目宪法生成
- `/speckit.specify` - 规格文档生成  
- `/speckit.plan` - 技术实施计划生成
- `/speckit.tasks` - 可执行任务清单推导
- `/speckit.implement` - 代码实现执行
- `/speckit.clarify` - 需求澄清辅助
- `/speckit.analyze` - 跨文档一致性分析
- `/speckit.checklist` - 验收检查清单生成

### 2. 文件结构映射

作为开发者，我们需要维护以下文件映射关系：

| 源模板文件 | 目标部署路径 |
|------------|-------------|
| `templates/commands/analyze.md` | `.github/prompts/speckit.analyze.prompt.md` |
| `templates/commands/checklist.md` | `.github/prompts/speckit.checklist.prompt.md` |
| `templates/commands/clarify.md` | `.github/prompts/speckit.clarify.prompt.md` |
| `templates/commands/constitution.md` | `.github/prompts/speckit.constitution.prompt.md` |
| `templates/commands/features.md` | `.github/prompts/speckit.features.prompt.md` |
| `templates/commands/implement.md` | `.github/prompts/speckit.implement.prompt.md` |
| `templates/commands/plan.md` | `.github/prompts/speckit.plan.prompt.md` |
| `templates/commands/specify.md` | `.github/prompts/speckit.specify.prompt.md` |
| `templates/commands/tasks.md` | `.github/prompts/speckit.tasks.prompt.md` |

在 `specify init` 命令执行时，系统会自动将模板文件复制到对应的 IDE 提示目录。

---

## 各指令详细规范

### /speckit.constitution（项目宪法）
- **输入规范**：接收组织/团队的质量、测试、UX、性能、安全等原则诉求
- **输出规范**：生成或更新 `memory/constitution.md` 文件
- **成功标准**：条目必须清晰、可操作、可复用，能为后续计划提供可执行约束
- **开发注意事项**：确保与 CLI 版本的宪法生成功能保持一致

### /speckit.specify（规格生成）
- **输入规范**：处理自然语言的功能/场景描述，聚焦"做什么/为什么"
- **输出规范**：
  - `.specify/specs/<feature-branch>/spec.md`（基于 `templates/spec-template.md`）
  - `.specify/specs/<feature-branch>/checklist.md`（基于 `templates/checklist-template.md`）
- **成功标准**：需求完整、验收标准明确、边界条件可验证
- **开发注意事项**：确保目录命名规范化，支持语义化分支名

### /speckit.plan（技术实施计划）
- **前置条件**：必须已有有效的规格文档（spec.md）
- **输入规范**：规格文档内容与宪法约束
- **输出规范**：
  - `plan.md`（架构决策、组件边界、数据流）
  - `data-model.md`（领域模型、数据字典）
  - `contracts/`（API/事件契约）
  - `research.md`（技术调研记录，可选）
  - `quickstart.md`（核心验证场景）
- **成功标准**：业务到技术映射清晰，可直接推导出任务

### /speckit.tasks（任务推导）
- **输入规范**：必须包含 `plan.md`，可选包含其他计划文档
- **输出规范**：`tasks.md`（基于 `templates/tasks-template.md`）
- **内容要求**：
  - 明确的任务条目（含完成定义、依赖、产出）
  - 并行任务标注 `[P]` 与安全并行分组
- **成功标准**：任务粒度恰当，覆盖计划关键路径

### /speckit.implement（执行实现）
- **前置条件**：`tasks.md` 必须就绪
- **输入规范**：任务清单与相关设计文档
- **输出规范**：代码/配置/脚本/文档的增量变更
- **质量门要求**：
  - 构建：项目可编译/打包/通过健康检查
  - 静态分析：Lint/类型检查通过
  - 测试：核心单测/合约测试通过
  - 冒烟：关键用户旅程验证通过

---

## 开发与维护准则

### 目录结构管理
- 规格/计划/任务目录：`.specify/specs/<feature-branch>/`
- 模板源文件：`templates/` 目录下的各类模板
- Agent 集成目录：`.github/prompts/`（Copilot 专用）

### 质量保证要求
- **构建验证**：确保生成的项目无错误、可运行
- **代码质量**：Lint/类型检查必须通过，保持风格一致性
- **测试覆盖**：为关键业务路径提供充分测试
- **文档同步**：变更时必须同步更新相关文档
- **可追溯性**：技术决策必须能回溯到具体需求/约束

### 环境与分支策略
- 支持 `SPECIFY_FEATURE` 环境变量覆盖特性检测
- 推荐以规格特性为单位创建语义化分支
- 避免在主分支直接推进未成体系的变更

---

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