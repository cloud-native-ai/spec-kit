# 在 VS Code Copilot 中使用 Agent Skills

Agent Skills 是一组指令、脚本和资源，GitHub Copilot 可以在相关时加载这些内容以执行专门的任务。Agent Skills 是一个开放标准，适用于多种 AI 代理，包括 VS Code 中的 GitHub Copilot、GitHub Copilot CLI 和 GitHub Copilot 编码代理。

与主要定义编码准则的自定义指令（Custom Instructions）不同，Skills 启用了包含脚本、示例和其他资源的专门功能和工作流。您创建的 Skills 是可移植的，并且可以在任何兼容 Skills 的代理中工作。

## 核心优势

*   **Copilot 专项化**：为特定领域的任务定制能力，无需重复上下文。
*   **减少重复**：一次创建，在所有对话中自动使用。
*   **能力组合**：组合多个 Skill 以构建复杂的工作流。
*   **高效加载**：仅在需要时将相关内容加载到上下文中。

> **注意**：VS Code 中的 Agent Skills 支持目前处于预览阶段。可能需要启用 `chat.useAgentSkills` 设置才能使用。

## Agent Skills 与自定义指令 (Custom Instructions)

虽然两者都能定制 Copilot 的行为，但用途不同：

| 特性 | Agent Skills | Custom Instructions |
| :--- | :--- | :--- |
| **目的** | 教授专门的能力和工作流 | 定义编码标准和准则 |
| **可移植性** | 跨 VS Code, Copilot CLI, Copilot Agent 通用 | 仅限 VS Code 和 GitHub.com |
| **内容** | 指令、脚本、示例和资源 | 仅指令 |
| **范围** | 任务特定，按需加载 | 始终应用（或通过 glob 模式应用） |
| **标准** | 开放标准 (agentskills.io) | VS Code 专用 |

**使用场景对比：**

*   **Agent Skills**：创建可重用的能力（如测试、部署流程），包含辅助脚本或示例。
*   **Custom Instructions**：定义项目特定的代码风格、框架约定或提交信息格式。

## 创建 Skill

Skills 存储在带有 `SKILL.md` 文件的目录中。

### 存储位置

*   **项目级 Skills**（推荐）：存储在工作区的 `.github/skills/` 目录下。
*   **用户级 Skills**（推荐）：存储在用户配置文件的 `~/.copilot/skills/` 目录下。

### 目录结构

每个 Skill 应有自己的子目录。例如，创建一个名为 `webapp-testing` 的 Skill：

1.  创建目录 `.github/skills/webapp-testing/`
2.  在其中创建 `SKILL.md` 文件。
3.  （可选）添加脚本、模板或示例文件。

结构示例：
```text
.github/skills/webapp-testing/
├── SKILL.md           # 定义 Skill 行为和元数据
├── test-template.js   # 模板文件
└── examples/          # 示例场景
```

### SKILL.md 文件格式

`SKILL.md` 是包含 YAML frontmatter 的 Markdown 文件。

**头部 (Frontmatter)**

```yaml
---
name: skill-name
description: 关于该 Skill 做什么以及何时使用的描述
---
```

*   `name` (必填): 唯一标识符，小写，使用连字符（如 `webapp-testing`）。
*   `description` (必填): 描述 Skill 的功能和使用场景。Copilot 依据此描述决定何时加载该 Skill。

**正文 (Body)**

包含 Copilot 使用该 Skill 时应遵循的详细指令、准则和示例。

```markdown
# Skill Instructions

在此处编写详细的指令...

您可以引用目录内的文件，例如：[测试脚本](./test-template.js)。
```

## Copilot 如何使用 Skills

Skills 使用渐进式披露（Progressive Disclosure）机制，仅在需要时加载内容：

1.  **Skill 发现**：Copilot 读取所有可用 Skills 的名称和描述。
2.  **指令加载**：当用户请求与 Skill 描述匹配时，Copilot 加载 `SKILL.md` 的正文。
3.  **资源访问**：仅当 Copilot 需要引用辅助文件（脚本、示例）时，才会读取这些文件。

## 最佳实践

*   **保持专注**：为不同的工作流创建独立的 Skill，而不是一个巨大的万能 Skill。
*   **清晰的描述**：描述对于 Copilot 判断何时调用 Skill 至关重要。
*   **使用示例**：在 `SKILL.md` 中包含输入输出示例。
*   **安全性**：在添加脚本时要谨慎，避免硬编码敏感信息。

---
更多信息请参考 Agent Skills 开放标准：[agentskills.io](https://agentskills.io)。
