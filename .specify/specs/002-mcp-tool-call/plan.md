# Implementation Plan: MCP Tool Call Command

**Branch**: `002-mcp-tool-call` | **Date**: 2026-02-10 | **Spec**: [.specify/specs/002-mcp-tool-call/requirements.md](.specify/specs/002-mcp-tool-call/requirements.md)
**Input**: Specification from `.specify/specs/002-mcp-tool-call/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

为 `/speckit.mcpcall` 提供完整的实现规划：新增 MCP 工具记录模板与命令模板，定义工具发现与交互补全流程，并在本地 `.specify/memory/tools/` 形成可复用的工具记录，同时生成数据模型、合约与快速验证步骤。

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python >= 3.8  
**Primary Dependencies**: Typer, Rich, httpx[socks], mcp[cli], platformdirs, readchar  
**Storage**: 本地文件系统（`.specify/memory/tools/`）  
**Testing**: pytest（计划引入，用于命令行为与合约校验）  
**Target Platform**: 跨平台 CLI（Linux/macOS/Windows）
**Project Type**: single（CLI 工具）  
**Performance Goals**: 本地元数据读取与渲染 ≤ 2 秒；工具发现与清单渲染 ≤ 5 秒  
**Constraints**: 复用现有 CLI 与模板体系；不引入新持久化存储；交互步骤必须可跳过并可复用  
**Scale/Scope**: 多个 MCP Server，单次展示/管理数十个 MCP 工具

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: Feature Index is single source of truth; all phases re-evaluate Feature changes.
- **Specification-Driven Development**: Code serves specifications; specifications are executable and generate working systems
- **Intent-Driven Development**: Focus on "what" and "why" before "how"; use rich specifications with guardrails
- **Test-First & Contract-Driven**: TDD flow followed; pure functions have unit tests; critical flows have regression coverage
- **AI Agent Integration**: Only approved agents (GitHub Copilot, Qwen Code, opencode); configuration rejects unsupported providers
- **Continuous Quality & Observability**: Structured logging; semantic versioning; CI quality gates; simple designs (YAGNI)
- **SDD Workflow Compliance**: Follow spec → plan → tasks → implement workflow with proper validation at each phase

**Additional Constraints from Input**:

- 必须新增 `templates/mcptool-template.md` 作为 MCP 工具记录模板
- 必须新增 `templates/commands/mcpcall.md` 并参考 `templates/commands/clarify.md` 的结构

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/002-mcp-tool-call/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this spec. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── specify_cli/
  ├── __init__.py
  ├── commands/
  │   └── mcpcall.py
  └── templates/
    ├── mcptool-template.md
    └── commands/
      └── mcpcall.md

templates/
├── mcptool-template.md
└── commands/
  └── mcpcall.md

.specify/memory/
└── tools/
  └── <mcp tool name>.md

tests/
└── contract/
  └── test_mcpcall_contracts.py
```

**Structure Decision**: 单项目 CLI 结构，命令实现放在 `src/specify_cli/commands/`，模板放在 `templates/` 并复制到运行时上下文。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**
> If no violations, explicitly write "N/A" and remove the table.

N/A

## Phase 0: Research Review & Context

- 未发现 `research.md`，已使用现有文档与 Feature Memory 完成技术上下文决策。
- 无需额外研究即可进入设计阶段。

## Phase 1: Design & Contracts

### Data Model

- 生成 `.specify/specs/002-mcp-tool-call/data-model.md`，覆盖 MCP Tool 记录、Server、参数与调用会话等实体。

### Contracts

- 生成 `contracts/mcptool-record.schema.json` 描述工具记录结构。
- 生成 `contracts/mcpcall-input.schema.json` 描述命令输入结构。

### Quickstart

- 生成 `.specify/specs/002-mcp-tool-call/quickstart.md`，提供本地验证步骤。

### Feature Reference

- 生成 `.specify/specs/002-mcp-tool-call/feature-ref.md`，链接本次 spec/plan 与相关模板。

### Agent Context Update

- 运行 `.specify/scripts/bash/generate-instructions.sh` 更新 `.ai/instructions.md` 与工具文档。

## Phase 2: Implementation Planning

1. 新增 `templates/mcptool-template.md` 作为 MCP 工具记录模板。
2. 新增 `templates/commands/mcpcall.md`，沿用 `templates/commands/clarify.md` 的结构，补充 MCP 工具发现与交互补全流程。
3. 在 CLI 中注册 `/speckit.mcpcall` 命令入口，绑定模板与流程实现。
4. 实现 MCP 工具发现逻辑与本地记录读写（`.specify/memory/tools/`）。
5. 添加合约测试与关键流程测试，验证记录结构与调用行为。
