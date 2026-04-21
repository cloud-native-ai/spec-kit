# 🌱 Spec Kit

*Build high-quality software faster.*

**An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.**

本项目基于 [github.com/github/spec-kit.git](https://github.com/github/spec-kit.git) 开源项目开发，并在原始 Spec Kit 的基础上进行了多项自定义扩展。感谢原项目贡献者的工作与投入。

## 项目简介

Spec Kit 是一个围绕 **Spec-Driven Development（规格驱动开发）** 构建的开源工具包，目标是让团队把注意力放在产品场景、业务约束与可预测结果上，而不是从零开始重复编写大量同质化代码。

与传统“先写代码、规格仅作参考”的流程不同，Spec-Driven Development 强调：**规格本身就是实现过程的核心输入**。需求、计划、任务与实现之间通过结构化模板和命令串联，使 AI 能够围绕明确意图逐步推进，而不是依赖一次性的模糊提示直接生成代码。

## 什么是 Spec-Driven Development？

Spec-Driven Development 改变了传统软件开发中“代码为主、规格为辅”的模式。它强调先定义 *what*，再约束 *how*，让规格从一次性文档演变为可以持续驱动实现、审查与迭代的核心资产。

这一方法特别适合以下场景：

- 从高层需求出发，逐步生成可执行的实现路径
- 在 AI 协作开发中保留明确边界、约束与上下文
- 面向企业或团队规范，沉淀一致的研发流程
- 在新建项目与存量系统演进中保持迭代可追踪

## 📚 文档索引

### 快速上手

- [安装指南](docs/installation.md)
- [快速开始](docs/quickstart.md)
- [使用说明](docs/usage.md)

### 方法与实践

- [Spec-Driven Development 方法论](docs/spec-driven.md)
- [Vibe Coding 说明](docs/vibe-coding.md)
- [上游项目说明](docs/upstream.md)

### 技能与扩展

- [技能规范](docs/skills/specification.md)
- [技能问题排查](docs/skills/problems.md)
- [VS Code 技能说明](docs/skills/vscode.md)

## 核心理念

Spec-Driven Development 强调以下原则：

- **意图优先**：先明确目标与约束，再进入实现细节
- **规格增强**：通过模板、守卫规则和组织原则丰富规格质量
- **多阶段细化**：由需求、计划、任务逐步收敛，而不是一次性生成全部代码
- **AI 深度协作**：充分利用先进模型对规格、上下文与流程的理解能力

## 适用开发阶段

| 阶段 | 关注点 | 典型活动 |
|-------|-------|----------|
| **0 到 1 开发**（Greenfield） | 从无到有构建 | 从高层需求开始，生成规格、规划实现步骤并构建可落地系统 |
| **创意探索** | 并行尝试不同方案 | 探索不同技术栈、架构选择与交互方式 |
| **迭代增强**（Brownfield） | 存量系统演进 | 持续增加功能、改造旧系统、适配新的组织流程 |

## 实验目标

本项目的研究与实践重点包括：

### 技术独立性

- 支持使用多样化技术栈构建应用
- 验证 Spec-Driven Development 作为流程方法，不依赖某一种特定语言、框架或平台

### 企业约束适配

- 支持面向关键业务场景的软件开发
- 将云平台、技术选型、工程规范与合规要求纳入规格过程
- 为组织级设计系统与流程约束提供支撑

### 用户导向开发

- 面向不同用户群体和偏好构建产品
- 同时支持从 vibe-coding 到 AI-native development 的不同工作方式

### 创造性与迭代式流程

- 支持并行探索多种实现方案
- 提供稳健的增量特性开发工作流
- 将流程扩展到升级、重构与现代化改造场景

## 🔧 核心功能

- **Specification-Driven Development**：以规格说明书驱动的开发流程
- **AI 智能代理集成**：支持多种 AI 编码助手
- **结构化工作流**：从需求到实现的完整开发流程
- **可扩展技能系统**：支持自定义技能与工具，并通过 `/speckit.skills` 进行管理
- **技能安装布局统一**：项目级 skill 主副本统一落在 `.specify/skills/`，`.github/skills/` 作为兼容入口

## 🤖 支持的 AI 代理

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

## 📦 安装

详细安装说明请参阅 [docs/installation.md](docs/installation.md)。

## 🤝 贡献与支持

- 贡献说明请参阅 [Spec Kit upstream contributing guide](https://github.com/github/spec-kit/blob/main/CONTRIBUTING.md)
- 支持说明请参阅 [Spec Kit upstream support guide](https://github.com/github/spec-kit/blob/main/SUPPORT.md)

## 📄 许可证

本项目采用 MIT 开源许可证。详情请参阅 [LICENSE](LICENSE)。