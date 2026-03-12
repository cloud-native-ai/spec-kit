# Implementation Plan: Deterministic Tool and Skill IDs

**Branch**: `005-tool-skill-ids` | **Date**: 2026-03-10 | **Spec**: [.specify/specs/005-tool-skill-ids/requirements.md](.specify/specs/005-tool-skill-ids/requirements.md)
**Input**: Specification from `.specify/specs/005-tool-skill-ids/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

为 `/speckit.tools` 与 `/speckit.skills` 增加确定性的资源标识体系，默认使用工作区相对路径作为 canonical ID。方案保留现有自然语言发现能力，但在命令产出与后续引用链路中优先使用精确 ID，以降低 tool/skill 触发歧义、误触发和错误选择问题。

## Technical Context

**Language/Version**: Python 3.11+（文档建议），兼容项目声明 Python >=3.8  
**Primary Dependencies**: Typer、Rich、现有 Bash 脚本体系、Markdown 模板体系  
**Storage**: 本地文件系统（`.specify/memory/tools/`、`.github/skills/` 及其衍生文档）  
**Testing**: pytest + 现有 contract/integration/unit 测试结构  
**Target Platform**: Linux 优先的 CLI/AI Agent 工作区，兼容项目现有跨平台脚本约束
**Project Type**: single（CLI + templates + scripts + tests）  
**Performance Goals**: 95% 有效 ID 引用在一次解析内完成定位；命令生成 ID 的额外开销对现有工作流用户可感知时间增加不超过 2 秒  
**Constraints**: 必须保留自然语言发现兼容性；默认 ID 需可读、可复制、可持久化；不能要求立即迁移所有历史 tool/skill 资产  
**Scale/Scope**: 单仓库内数十到百级 tool/skill 资产的创建、刷新、引用与渐进升级

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: 复用 Feature 013，不新增重复 feature；本次 plan 会补充其计划阶段证据。
- **Specification-Driven Development**: 所有设计决策均回溯至 FR-001~FR-012 与 SC-001~SC-005。
- **Intent-Driven Development**: 先解决“如何精确引用对象”，再讨论实现位置；不把脚本细节暴露为需求本身。
- **Test-First & Contract-Driven**: 先定义 ID 生成/解析契约与回归场景，再拆分实现任务。
- **AI Agent Integration**: 仅涉及已支持的 GitHub Copilot / Qwen Code / opencode 命令资产，不引入新 provider。
- **Continuous Quality & Observability**: 保持设计最小化，新增错误反馈仅围绕 ID 生成、失效和冲突解析。
- **SDD Workflow Compliance**: 满足 spec → plan 产物要求，下一步进入 `/speckit.tasks`。

**Additional Constraints from Input**:

- 用户已明确要求“唯一标识”优先解决 tool 与 skill 的触发不确定性问题。
- 用户建议使用相对文件路径作为唯一标识，本次计划采纳为 canonical 方案。
- 唯一标识必须能在后续文档或对话中复用，而不仅仅出现在创建当次输出中。

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/005-tool-skill-ids/
├── plan.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── deterministic-resource-ids.openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
templates/
├── commands/
│   ├── skills.md
│   └── tools.md
├── tool-mcp-call-template.md
├── tool-project-script-template.md
├── tool-shell-function-template.md
└── tool-system-binary-template.md

scripts/
├── bash/
│   ├── create-new-skill.sh
│   ├── create-new-tools.sh
│   └── refresh-tools.sh
└── python/
  ├── list_mcp_tools.py
  ├── list_project_tools.py
  ├── list_shell_tools.py
  └── list_system_tools.py

.github/
└── skills/
  └── <skill-name>/
    ├── SKILL.md
    └── tools/

.specify/
├── memory/
│   └── tools/
│       └── <tool-name>.md
└── specs/
  └── 005-tool-skill-ids/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: 采用现有单仓库 CLI/模板/脚本结构，不新增服务或子项目。实现主要落在 `templates/commands/`、`scripts/bash/`、必要的 Python/测试辅助，以及 `.specify/memory/tools/` 与 `.github/skills/` 的持久化文档资产。

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- `research.md` 不存在；已基于 `README.md`、[docs/usage.md](docs/usage.md)、[docs/quickstart.md](docs/quickstart.md)、[docs/speckit/spec-driven.md](docs/speckit/spec-driven.md)、[docs/skills/problems.md](docs/skills/problems.md)、Feature Index 与相关 feature 详情完成上下文补全。
- 已确认项目核心技术面为 Python CLI + Bash 脚本 + Markdown 模板体系，无需额外研究即可确定本次设计边界。
- 已确认本次不引入新 Feature，也不淘汰现有 Feature；继续绑定 Feature 013，并与 Feature 016（工具统一入口）保持兼容关系。
- 技术未知项已收敛：canonical ID 采用工作区相对路径；旧资产按渐进方式补齐；无阻塞性澄清项。

## Phase 1: Design & Contracts

### Design Decisions

1. **Canonical ID 方案**
  - Tool 使用工具记录文件的工作区相对路径作为 `tool_id`。
  - Skill 使用 skill 主目录或 `SKILL.md` 的工作区相对路径作为 `skill_id`，并在计划中统一为“skill 根对象路径”。
  - 输出中同时显示对象类型与 canonical 路径，避免只有路径没有语义。

2. **持久化策略**
  - `/speckit.tools` 在工具记录中增加持久化 ID 字段或等价显式段落。
  - `/speckit.skills` 在 `SKILL.md` frontmatter 或正文显式段中增加持久化 ID 字段。
  - 历史资产在被重新读取、刷新或保存时补齐，不做一次性全量迁移。

3. **解析优先级**
  - 有效 ID 存在时，优先使用 ID 精确定位。
  - 无 ID 或 ID 失效时，回退到现有自然语言发现/消歧流程。
  - 当自然语言与 ID 冲突时，返回冲突错误并暂停自动继续。

4. **错误与兼容性**
  - 对不存在、越界、类型错误、失效路径提供明确错误消息。
  - 保持 `/speckit.tools` 与 `/speckit.skills` 当前用户路径不变，只增强产出与后续定位能力。

### Data Model

- 生成 `.specify/specs/005-tool-skill-ids/data-model.md`，定义 `ResourceId`、`ToolArtifact`、`SkillArtifact`、`ResolutionRequest`、`ResolutionResult` 等实体。

### Contracts

- 生成 `.specify/specs/005-tool-skill-ids/contracts/deterministic-resource-ids.openapi.yaml`。
- 用契约描述“生成 ID”“通过 ID 解析对象”“冲突/失效错误”的行为，供后续 tasks 与测试分解使用。

### Quickstart

- 生成 `.specify/specs/005-tool-skill-ids/quickstart.md`，覆盖 tool 创建、skill 创建、旧资产补齐、ID 引用成功与冲突失败等验证场景。

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: 继续复用 Feature 013；无新增、拆分或淘汰 feature。
- **Specification-Driven Development**: 设计决策已与 requirements 中的 FR/SC 明确对齐。
- **Intent-Driven Development**: 设计围绕“降低触发歧义、提升精确引用”展开，没有扩展到无关能力。
- **Test-First & Contract-Driven**: 已先输出数据模型与 OpenAPI 契约，便于后续先写 contract/integration tests。
- **AI Agent Integration**: 不扩展 provider 范围，仍服务既有批准代理生态。
- **Continuous Quality & Observability**: 错误类型与解析结果可被明确观察和验证，且设计保持最小必要复杂度。
- **SDD Workflow Compliance**: plan 阶段产物完整，适合进入 `/speckit.tasks`。

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. 更新 `templates/commands/tools.md`，要求在创建/复用 ToolRecord 后计算并输出 canonical `tool_id`。
2. 更新 `templates/commands/skills.md`，要求在创建/刷新 skill 后计算并输出 canonical `skill_id`。
3. 必要时扩展 `create-new-tools.sh` 与 `create-new-skill.sh` 的 JSON 输出字段，或在命令层用返回路径派生 ID。
4. 为 tool 记录模板与 skill 文档模板增加可持久化的 ID 字段/段落。
5. 增加解析逻辑与错误处理约定：优先 ID、失效回退、冲突中止。
6. 为新旧资产补齐、成功解析、冲突解析和失效路径补充 contract/integration/unit 测试。
