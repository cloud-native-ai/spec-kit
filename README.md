# 🌱 Spec Kit

*Build high-quality software faster.*

**An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.**

This project is based on the open source project [github.com/github/spec-kit.git](https://github.com/github/spec-kit.git) and includes multiple custom extensions on top of the original Spec Kit. Thanks to the original project contributors for their work and dedication.

## Overview

Spec Kit is an open source toolkit built around **Spec-Driven Development**, designed to help teams focus on product scenarios, business constraints, and predictable outcomes rather than repeatedly writing large amounts of homogeneous code from scratch.

Unlike the traditional approach of "write code first, treat specs as reference only," Spec-Driven Development emphasizes that **the specification itself is the core input for the implementation process**. Requirements, plans, tasks, and implementation are connected through structured templates and commands, enabling AI to progress step by step around clear intent rather than generating code directly from one-off vague prompts.

> For a deep dive into the SDD methodology, see [Spec-Driven Development](docs/spec-driven.md).

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/installation.md) | Setup and install the `specify` CLI |
| [Quick Start & Usage Guide](docs/quickstart.md) | Three-phase walkthrough, workflow, examples, and best practices |
| [Command Reference](docs/quickstart.md#command-overview) | All `/speckit.*` commands with prerequisites and next steps |
| [Per-Command Details](docs/commands/) | Individual command docs with execution flow and output artifacts |
| [Spec-Driven Development](docs/spec-driven.md) | Methodology deep-dive |
| [Vibe Coding Guide](docs/vibe-coding.md) | Iterative AI-assisted style guide |
| [Upstream Project](docs/upstream.md) | Relationship to github/spec-kit |
| [Skills Specification](docs/skills/specification.md) | Skills system reference |
| [Skills Troubleshooting](docs/skills/problems.md) | Common skill issues |
| [VS Code Skills Guide](docs/skills/vscode.md) | VS Code integration |

## 🔧 Core Features

- **Specification-Driven Development**: A structured workflow from requirements → plan → tasks → implementation
- **AI Agent Integration**: Support for multiple AI coding assistants
- **Extensible Skills System**: Custom skills and tools, managed via `/speckit.skills`
- **Unified Skill Installation Layout**: Project-level skill master copies under `.specify/skills/`

## 🤖 Supported AI Agents

### Tier 1 (Priority Support)

- [Claude Code](https://www.anthropic.com/claude-code)
- [Codex CLI](https://github.com/openai/codex)
- [Qoder CLI](https://qoder.com/cli)
- [GitHub Copilot](https://code.visualstudio.com/)
- [opencode](https://opencode.ai/)

### Tier 2 (Standard Support)

- [Qwen Code](https://github.com/QwenLM/qwen-code)
- Hermes Agent
- iFlow

## Feature List

### Functional Features

- **Unify Command Handoffs**: Make command prerequisites and next steps explicit. (Status: Planned)
- **Analyze Command**: Analyze project context and code structure. (Status: Completed)
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
- **Skills Command**: Manage extensible skills/tools. (Status: Implemented)
- **Tasks Command**: Break down plans into atomic tasks. (Status: Completed)
- **Agents Command**: Create or refine custom AI agents (.agent.md) for workspace-specific workflows. (Status: Implemented)
- **Qoder Support**: Add Qoder as a supported CLI assistant across initialization, validation, documentation, and release distribution. (Status: Implemented)
- **Claude Code Support**: Add Claude Code as a first-class assistant with custom commands and Claude Code-specific configuration assets. (Status: Implemented)
- **AI Tools Support**: Ensure all officially supported AI tools receive complete initialization coverage and can coexist without overwriting shared Spec Kit core files. (Status: Implemented)

### Non-functional Features

- **CLI Interface**: Rich terminal interface using Typer. (Status: Completed)
- **Tools Command**: Definition-first tool management with explicit behavioral rules. (Status: Planned)
- **Template Engine**: Markdown-based template system. (Status: Completed)
- **Configuration Management**: Project configuration via pyproject.toml. (Status: Completed)
- **Prompt Template Quality**: Structural validation and consistency enforcement across all command and skill templates. (Status: Draft)
- **Specification Workspace Versioning**: Version management and migration support for .specify/ workspace across CLI releases. (Status: Draft)

## 📦 Installation

For detailed installation instructions, see [docs/installation.md](docs/installation.md).

## 🤝 Contributing & Support

- For contribution guidelines, see the [Spec Kit upstream contributing guide](https://github.com/github/spec-kit/blob/main/CONTRIBUTING.md)
- For support information, see the [Spec Kit upstream support guide](https://github.com/github/spec-kit/blob/main/SUPPORT.md)

## 📄 License

This project is licensed under the MIT open source license. See [LICENSE](LICENSE) for details.
