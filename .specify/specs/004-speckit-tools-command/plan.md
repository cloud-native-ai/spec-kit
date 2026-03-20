# Implementation Plan: Speckit Tools Command

**Branch**: `004-speckit-tools-command` | **Date**: 2026-03-02 | **Spec**: [.specify/specs/004-speckit-tools-command/requirements.md](.specify/specs/004-speckit-tools-command/requirements.md)
**Input**: Specification from `.specify/specs/004-speckit-tools-command/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

将历史 MCP-only 命令能力统一为 `/speckit.tools`，并将“显式工具说明+记录+确认调用”能力从 MCP-only 泛化为 MCP/System/Shell/Project 四类工具。方案基于现有模板命令体系与 `scripts/bash/refresh-tools.sh` 的多来源发现能力，统一输出工具记录到 `.specify/memory/tools/`，并保持与现有 feature memory 及 SDD 流程一致。

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+（项目文档建议），兼容项目声明 Python >=3.8  
**Primary Dependencies**: Typer、Rich、httpx（含 socks）、项目现有 Bash 脚本体系  
**Storage**: 本地文件系统（`.specify/memory/tools/*.md`）  
**Testing**: pytest（命令模板/脚本行为测试与契约一致性校验）  
**Target Platform**: Linux/macOS/Windows 的 CLI 使用场景  
**Project Type**: single（CLI + templates + scripts）  
**Performance Goals**: 95% 已记录工具调用在 20 秒内完成“读取记录→参数确认→执行/取消”；工具来源列举在 5 秒内完成  
**Constraints**: 不破坏现有 `/speckit.*` 命令工作流；保持 `.specify/memory/tools/` 兼容；仅支持批准的 AI agent 生态（Copilot/Qwen/opencode）  
**Scale/Scope**: 单仓库内数十到百级工具条目（MCP/System/Shell/Project）管理与调用说明

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

- 本次未提供额外 `$ARGUMENTS` 约束，按 `requirements.md` 与项目既有文档执行。
- 命令统一必须体现为 `/speckit.tools`，并保留历史 MCP-only 场景的可迁移语义。
- 泛化必须覆盖 MCP 之外的 system/shell/project tools。

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/004-speckit-tools-command/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command, optional)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command, optional)
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
  ├── commands/
  │   └── (tooling command handlers)
  ├── models/
  └── utils/

templates/
├── commands/
│   └── tools.md
└── mcptool-template.md

scripts/
├── bash/
│   └── refresh-tools.sh
└── python/
  └── list_mcp_tools.py

.specify/memory/
├── tools/
│   └── <tool-name>.md
└── features/
  └── 016.md

# Existing generic layout kept unchanged
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

```

**Structure Decision**: 采用单项目 CLI 结构，不新增独立服务。核心变更落在命令模板、工具发现脚本协同与 memory 文档资产结构，保证与现有 `src/`、`templates/`、`scripts/` 目录风格一致。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**
> If no violations, explicitly write "N/A" and remove the table.

N/A

## Phase 0: Research Review & Context

- `SPECS_DIR/research.md` 不存在；已基于 `README.md`、`docs/`、`.specify/memory/features.md` 与 `features/*.md` 完成上下文补全。
- 关键技术决策已明确：复用现有 `refresh-tools.sh` 作为多来源工具发现基座，并保持工具记录路径与格式兼容。
- 不存在阻塞性的 NEEDS CLARIFICATION；可直接进入设计阶段。

## Phase 1: Design & Contracts

### Data Model

- 生成 `.specify/specs/004-speckit-tools-command/data-model.md`，定义 `ToolRecord`、`ToolSourceDescriptor`、`ToolInvocationSession`、`ToolAlias` 等实体。

### Contracts

- 生成 `.specify/specs/004-speckit-tools-command/contracts/tools-command.openapi.yaml`。
- 以 API-style 合约描述 `/speckit.tools` 的发现、补全、预览确认、执行与重命名行为。

### Quickstart

- 生成 `.specify/specs/004-speckit-tools-command/quickstart.md`，覆盖 MCP 与非 MCP 来源、冲突消歧、记录复用与重命名。

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: 继续沿用 Feature 016，不新增重复 Feature。
- **Specification-Driven Development**: 所有设计均可追溯到 FR-001~FR-010 与 SC-001~SC-005。
- **Intent-Driven Development**: 计划围绕“显式说明工具调用”用户价值，未提前落入实现细节。
- **Test-First & Contract-Driven**: 已先定义契约与数据模型，后续 tasks 将按 contract/integration 优先拆解。
- **AI Agent Integration**: 与批准 agent 生态一致，不引入未批准 provider。
- **Continuous Quality & Observability**: 结果输出与错误说明可核验，保留简化设计（YAGNI）。
- **SDD Workflow Compliance**: 满足 spec → plan 产物要求，下一步进入 `/speckit.tasks`。

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. 将命令文档入口统一到 `templates/commands/tools.md`，并保留兼容迁移说明。
2. 统一工具发现流程：聚合 MCP/System/Shell/Project 四类来源，并标准化为统一候选模型。
3. 建立工具记录读写策略：优先复用 `.specify/memory/tools/<tool-name>.md`，缺失时交互补全再写入。
4. 增加冲突消歧与执行前确认步骤：处理同名来源冲突、命名冲突与未确认执行。
5. 对记录封装与重命名能力定义稳定规则，确保可检索、可复用、可追踪。
6. 按契约生成后续任务（contract → integration → unit），并补充回归验证路径。
