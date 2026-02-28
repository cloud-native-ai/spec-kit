# 🌱 Spec Kit

**An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.**

本项目基于 [github.com/github/spec-kit.git](https://github.com/github/spec-kit.git) 开源项目开发，在 Spec Kit 的基础上做了很多自定义扩展。感谢对原 Spec Kit 项目做出贡献的所有开发者！

## 📚 文档索引

- [快速开始](docs/quickstart.md)
- [安装指南](docs/installation.md)
- [升级指南](docs/upgrade.md)
- [Spec-Driven Development 方法论](docs/speckit/spec-driven.md)
- [技能系统](docs/skills/requirements.md)

## 🔧 核心功能

- **Specification-Driven Development**: 以规格说明书驱动的开发流程
- **AI 智能代理集成**: 支持多种 AI 编码助手
- **结构化工作流**: 从需求到实现的完整开发流程
- **可扩展技能系统**: 支持自定义开发技能和工具，可通过 `/speckit.skills` 命令轻松管理

## 🤖 支持的 AI 代理

- [GitHub Copilot](https://code.visualstudio.com/)
- [Qwen Code](https://github.com/QwenLM/qwen-code)
- [opencode](https://opencode.ai/)

## Feature List

### Functional Features

- **Unify Command Handoffs**: Make command prerequisites and next steps explicit. (Status: Planned)
- **Analyze Command**: Analyze project context and code structure. (Status: Completed)
- **Agents Command**: Create and refine custom AI agents (.agent.md). (Status: Completed)
- **Checklist Command**: Verify project alignment with constitution. (Status: Completed)
- **Clarify Command**: Resolve ambiguities in specifications. (Status: Completed)
- **Constitution Command**: Manage project governance and principles. (Status: Completed)
- **Feature Command**: Manage feature lifecycle and metadata. (Status: Completed)
- **Implement Command**: Generate code from tasks and plans. (Status: Completed)
- **Instructions Command**: Generate prompts for AI agents. (Status: Completed)
- **Plan Command**: Create implementation plans from specs. (Status: Completed)
- **Requirements Command**: Define requirements and specifications. (Status: Completed)
- **Research Command**: Gather context and dependencies. (Status: Completed)
- **Review Command**: Review implementation against rules. (Status: Completed)
- **Skills Command**: Manage extensible skills/tools. (Status: Completed)
- **Tasks Command**: Break down plans into atomic tasks. (Status: Completed)

### Non-functional Features

- **CLI Interface**: Rich terminal interface using Typer.
- **MCP Support**: Integration with Model Context Protocol.
- **Template Engine**: Markdown-based template system.
- **Configuration Management**: Project configuration via pyproject.toml.

## 📦 安装

详细安装说明请参阅 [安装指南](docs/installation.md)。

## 📄 许可证

本项目采用 MIT 开源许可证。详情请参阅 [LICENSE](./LICENSE) 文件。