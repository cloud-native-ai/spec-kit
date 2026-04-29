# 🌱 Spec Kit

*Build high-quality software faster.*

**An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.**

This project is based on the open source project [github.com/github/spec-kit.git](https://github.com/github/spec-kit.git) and includes multiple custom extensions on top of the original Spec Kit. Thanks to the original project contributors for their work and dedication.

## Overview

Spec Kit is an open source toolkit built around **Spec-Driven Development**, designed to help teams focus on product scenarios, business constraints, and predictable outcomes rather than repeatedly writing large amounts of homogeneous code from scratch.

Unlike the traditional approach of "write code first, treat specs as reference only," Spec-Driven Development emphasizes that **the specification itself is the core input for the implementation process**. Requirements, plans, tasks, and implementation are connected through structured templates and commands, enabling AI to progress step by step around clear intent rather than generating code directly from one-off vague prompts.

## What is Spec-Driven Development?

Spec-Driven Development transforms the traditional "code-first, spec-secondary" model in software development. It emphasizes defining *what* first, then constraining *how*, evolving specifications from one-time documents into core assets that continuously drive implementation, review, and iteration.

This approach is particularly well-suited for the following scenarios:

- Progressively generating executable implementation paths from high-level requirements
- Maintaining clear boundaries, constraints, and context in AI-assisted development
- Establishing consistent development processes aligned with enterprise or team standards
- Keeping iterations traceable in both greenfield projects and brownfield system evolution

## 📚 Documentation Index

### Getting Started

- [Installation Guide](docs/installation.md)
- [Quick Start](docs/quickstart.md)
- [Usage Guide](docs/usage.md)

### Methodology & Practice

- [Spec-Driven Development Methodology](docs/spec-driven.md)
- [Vibe Coding Guide](docs/vibe-coding.md)
- [Upstream Project](docs/upstream.md)

### Skills & Extensions

- [Skills Specification](docs/skills/specification.md)
- [Skills Troubleshooting](docs/skills/problems.md)
- [VS Code Skills Guide](docs/skills/vscode.md)

## Core Philosophy

Spec-Driven Development is built on the following principles:

- **Intent-First**: Clarify goals and constraints before diving into implementation details
- **Specification Enhancement**: Enrich specification quality through templates, guardrails, and organizational principles
- **Multi-Stage Refinement**: Converge progressively through requirements, plans, and tasks rather than generating all code at once
- **Deep AI Collaboration**: Leverage advanced models' ability to understand specifications, context, and processes

## Applicable Development Stages

| Stage | Focus | Typical Activities |
|-------|-------|----------|
| **0-to-1 Development** (Greenfield) | Building from scratch | Start from high-level requirements, generate specifications, plan implementation steps, and build a functional system |
| **Creative Exploration** | Trying different approaches in parallel | Explore different tech stacks, architectural choices, and interaction patterns |
| **Iterative Enhancement** (Brownfield) | Evolving existing systems | Continuously add features, modernize legacy systems, adapt to new organizational processes |

## Research Goals

The research and practice focus areas of this project include:

### Technology Independence

- Support building applications with diverse technology stacks
- Validate Spec-Driven Development as a process methodology that does not depend on any specific language, framework, or platform

### Enterprise Constraint Adaptation

- Support software development for critical business scenarios
- Incorporate cloud platforms, technology choices, engineering standards, and compliance requirements into the specification process
- Provide support for organizational design systems and process constraints

### User-Oriented Development

- Build products for different user groups and preferences
- Support diverse working styles from vibe-coding to AI-native development

### Creative & Iterative Processes

- Support parallel exploration of multiple implementation approaches
- Provide robust workflows for incremental feature development
- Extend the process to upgrades, refactoring, and modernization scenarios

## 🔧 Core Features

- **Specification-Driven Development**: A specification-driven development process
- **AI Agent Integration**: Support for multiple AI coding assistants
- **Structured Workflow**: Complete development process from requirements to implementation
- **Extensible Skills System**: Support for custom skills and tools, managed via `/speckit.skills`
- **Unified Skill Installation Layout**: Project-level skill master copies are consistently placed under `.specify/skills/`, with `.github/skills/` serving as a compatibility entry point

## 🤖 Supported AI Agents

- [GitHub Copilot](https://code.visualstudio.com/)
- [Qwen Code](https://github.com/QwenLM/qwen-code)
- [opencode](https://opencode.ai/)
- [Qoder](https://qoder.com/cli)

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

## 📦 Installation

For detailed installation instructions, see [docs/installation.md](docs/installation.md).

## 🤝 Contributing & Support

- For contribution guidelines, see the [Spec Kit upstream contributing guide](https://github.com/github/spec-kit/blob/main/CONTRIBUTING.md)
- For support information, see the [Spec Kit upstream support guide](https://github.com/github/spec-kit/blob/main/SUPPORT.md)

## 📄 License

This project is licensed under the MIT open source license. See [LICENSE](LICENSE) for details.