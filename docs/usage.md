# Spec Kit Usage Guide

Spec Kit is a Specification-Driven Development (SDD) CLI tool that helps developers adopt structured development practices. The tool provides a comprehensive workflow from feature specification to implementation, with built-in quality checks and validation.

> **Important for Beginners**: Spec Kit involves two distinct types of interactions:
> 1. **Terminal CLI** (`specify ...`): Used for project initialization and configuration. Run these in your system terminal.
> 2. **AI Agent Commands** (`/speckit. ...`): Used for the development workflow. **Type these into your AI Assistant's chat interface (e.g., Copilot Chat), DO NOT run them in your terminal.**

## Command Overview

The following commands are **prompt instructions** for your AI Agent. Use them inside your AI chat interface, **not** in your terminal. Spec Kit provides the following core commands:

| Command | Purpose | Typical Workflow Stage |
|---------|---------|----------------------|
| `/speckit.requirements` | Create/update the requirements specification | Specification |
| `/speckit.clarify` | Clarify ambiguous requirements | Specification |
| `/speckit.plan` | Generate implementation plans | Planning |
| `/speckit.tasks` | Break down plans into actionable tasks | Planning |
| `/speckit.implement` | Implement tasks with validation | Implementation |
| `/speckit.analyze` | Analyze consistency across artifacts | Quality Assurance |
| `/speckit.checklist` | Generate quality checklists | Quality Assurance |
| `/speckit.review` | Review implementations against specs | Quality Assurance |
| `/speckit.research` | Conduct technical research | Research |
| `/speckit.constitution` | Manage project constitution | Governance |
| `/speckit.feature` | Manage feature registry | Governance |
| `/speckit.agents` | Create/refine custom agents | Extension |
| `/speckit.skills` | Manage specialized skills | Extension |
| `/speckit.instructions` | Generate usage instructions | Documentation |

## Command Relationships (Prerequisites & Next Steps)

Spec Kit 的命令不是独立使用的。下面这张表用“常见前置 / 常见后续”的方式，把核心主路径、可选分支与返工环路明确下来。

> 规则：如果 requirements/spec 中存在 `[NEEDS CLARIFICATION]`，优先走 `/speckit.clarify`；如果要进入实现阶段，建议先完成相关 checklist。

| Command | Common prerequisites | Common next commands | Notes |
|---------|----------------------|---------------------|-------|
| `/speckit.instructions` | Repo available | `/speckit.skills` | 生成/更新 AI 指引与兼容链接，通常用于初始化或文档更新后同步。 |
| `/speckit.skills` | (Optional) `/speckit.instructions` | (Depends) | 创建/刷新技能；不直接进入 core 生命周期，但会影响后续 agent 上下文。 |
| `/speckit.constitution` | Repo available | `/speckit.feature`, `/speckit.requirements` | 修改治理规则后，应重新审视 feature 与 requirements。 |
| `/speckit.feature` | (Optional) `/speckit.constitution` | `/speckit.requirements` | 建立/刷新长期 Feature 注册表，为规格与计划提供“主干”。 |
| `/speckit.requirements` | (Optional) `/speckit.feature` | `/speckit.clarify`, `/speckit.plan` | 产出 requirements.md；若存在歧义标记，先 clarify 再 plan。 |
| `/speckit.clarify` | `/speckit.requirements` | `/speckit.plan` | 解决关键歧义（并回写到 requirements.md），避免下游返工。 |
| `/speckit.research` | `/speckit.requirements` (or) `/speckit.plan` | `/speckit.plan` | 缺信息/需要决策依据时使用；研究结论应反馈到 plan。 |
| `/speckit.plan` | `/speckit.requirements` (clarify done if needed) | `/speckit.tasks`, `/speckit.checklist` | 产出 plan.md 及相关设计产物；下一步通常拆 tasks。 |
| `/speckit.tasks` | `/speckit.plan` | `/speckit.analyze`, `/speckit.checklist`, `/speckit.implement` | 产出 tasks.md；可先 analyze 做一致性检查，再实现。 |
| `/speckit.analyze` | `/speckit.tasks` | `/speckit.requirements`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement` | 严格只读；输出问题清单与修复建议，必要时先回到上游修订。 |
| `/speckit.checklist` | `/speckit.requirements` (or) `/speckit.plan` (or) `/speckit.tasks` | `/speckit.plan`, `/speckit.implement` | 作为质量门槛：不通过则建议回到 plan/tasks 修订。 |
| `/speckit.implement` | `/speckit.tasks` (and ideally checklists completed) | `/speckit.review` | 进入实现与验证；如缺 tasks，先回到 tasks。 |
| `/speckit.review` | `/speckit.implement` | `/speckit.analyze`, `/speckit.requirements`, `/speckit.plan` | 复盘流程质量与改进建议；必要时回到上游迭代。 |

## Detailed Command Reference

### `speckit.requirements`
**Purpose**: Create or update a **requirements specification** that defines WHAT needs to be built and WHY, without specifying HOW.

**Conceptual distinction**:
- **Feature** (`/speckit.feature`): a long-lived registry entry (ID/name/status) stored under `.specify/memory/`.
- **Requirements**: the statements of need/constraints/acceptance criteria (the content).
- **Specification**: the structured artifact that records those requirements. In Spec Kit, this is typically `.specify/specs/<REQUIREMENTS_KEY>/requirements.md` (the "requirements specification").

**Usage**: 
```bash
/speckit.requirements [feature description]
```

**Key Features**:
- Generates a structured requirements specification with user scenarios, functional requirements, and success criteria
- Automatically creates numbered branches and spec files
- Integrates with feature registry for tracking
- Validates requirements-specification quality before proceeding
- Limits clarifications to maximum 3 critical questions

**Output**: Creates or updates `.specify/specs/<REQUIREMENTS_KEY>/requirements.md` plus related spec artifacts under the same directory.

### `speckit.clarify`
**Purpose**: Resolve ambiguous or unclear requirements in an existing requirements specification (`requirements.md`).

**Usage**:
```bash
/speckit.clarify [clarification context]
```

**Key Features**:
- Identifies and resolves `[NEEDS CLARIFICATION]` markers in specs
- Presents clear options for user decision
- Updates the requirements specification with resolved requirements
- Maintains requirements-specification quality standards

### `speckit.plan`
**Purpose**: Generate detailed implementation plans based on the requirements specification (`requirements.md`).

**Usage**:
```bash
/speckit.plan [planning preferences or constraints]
```

**Key Features**:
- Translates the requirements specification into technical architecture decisions
- Defines data models, components, and integration points
- Respects constitutional constraints
- Creates phased implementation approach
- Outputs structured `plan.md` file

### `speckit.tasks`
**Purpose**: Break down implementation plans into granular, actionable tasks.

**Usage**:
```bash
/speckit.tasks [task prioritization or constraints]
```

**Key Features**:
- Decomposes plan phases into individual development tasks
- Assigns task priorities and dependencies
- Ensures tasks are implementable and testable
- Generates `tasks.md` file with complete task list

### `speckit.implement`
**Purpose**: Execute implementation tasks with built-in quality validation.

**Usage**:
```bash
/speckit.implement [implementation scope or priority]
```

**Key Features**:
- Implements tasks according to plan and spec
- Validates checklist completion before implementation
- Provides progress tracking and status reporting
- Ensures code quality and adherence to the requirements specification and plan

### `speckit.analyze`
**Purpose**: Identify inconsistencies, duplications, and ambiguities across specification artifacts.

**Usage**:
```bash
/speckit.analyze [analysis focus area]
```

**Key Features**:
- Performs cross-artifact consistency checks (spec, plan, tasks)
- Enforces constitutional compliance
- Generates structured analysis reports
- Identifies critical issues requiring resolution
- **Read-only operation** - does not modify files

### `speckit.checklist`
**Purpose**: Generate quality checklists that serve as "unit tests for English" requirements.

**Usage**:
```bash
/speckit.checklist [checklist type or focus area]
```

**Key Features**:
- Validates requirements quality, clarity, and completeness
- Creates domain-specific checklists (UX, security, testing, etc.)
- Ensures requirements are testable and unambiguous
- Tracks checklist completion status
- Prevents implementation of poorly-defined requirements

### `speckit.review`
**Purpose**: Review implemented features against the original requirements specification (`requirements.md`) and plan.

**Usage**:
```bash
/speckit.review [review criteria or focus areas]
```

**Key Features**:
- Validates implementation against the requirements specification and plan
- Checks for requirement coverage and compliance
- Identifies gaps or deviations from original plan
- Provides comprehensive review reports

### `speckit.research`
**Purpose**: Conduct technical research to inform requirements-specification and implementation decisions.

**Usage**:
```bash
/speckit.research [research topic or question]
```

**Key Features**:
- Investigates technical approaches and alternatives
- Evaluates technology choices and trade-offs
- Provides evidence-based recommendations
- Supports informed decision-making

### `speckit.constitution`
**Purpose**: Manage and enforce the project's core principles and governance rules (stored in `.specify/memory/constitution.md`).

**Usage**:
```bash
/speckit.constitution [constitutional update or query]
```

**Key Features**:
- Maintains core project principles and constraints in `.specify/memory/constitution.md`
- Enforces non-negotiable rules across all artifacts
- Provides constitutional guidance for decision-making
- Tracks constitutional changes and updates

### `speckit.feature`
**Purpose**: Manage the feature registry (stored in `.specify/memory/features.md`) and track feature evolution.

**Usage**:
```bash
/speckit.feature [feature management action]
```

**Key Features**:
- Maintains centralized feature index and per-feature memory documents
- Tracks long-lived feature identity (ID/name/status) across iterations
- Links to the current/most relevant spec artifacts produced by `/speckit.requirements`, `/speckit.plan`, and `/speckit.tasks`
- Ensures consistent feature naming and organization

### `speckit.skills`
**Purpose**: Manage specialized AI agent skills and capabilities.

**Usage**:
```bash
/speckit.skills [argument]
```

**Key Features**:
- **Create**: `/speckit.skills "name - description"` creates a new skill directory with standard templates
- **Refresh**: `/speckit.skills` (no args) scans and validates all installed skills
- Enforces standard structure (`SKILL.md`, `scripts/`, `references/`)
- Validates skill names and configurations

### `speckit.agents`
**Purpose**: Create or refine custom AI agents for focused workflows using `.agent.md` files.

**Usage**:
```bash
/speckit.agents [agent intent or constraints]
```

**Key Features**:
- Creates or updates workspace-scoped agents in `.github/agents/`
- Defines clear trigger descriptions for agent selection and subagent routing
- Enforces minimal, role-appropriate tool permissions
- Produces deterministic role/workflow/output guidance for each agent

### `speckit.instructions`
**Purpose**: Generate comprehensive usage instructions, maintenance guides, or system prompts. This command helps create documentation for humans or setup instructions for AI agents.

**Usage**:
```bash
/speckit.instructions [instruction scope or audience]
```

**Key Features**:
- Creates user-friendly documentation
- Generates context-specific instructions
- Supports multiple documentation formats
- Maintains documentation consistency

## Workflow Integration

The Spec Kit workflow consists of a **Core Lifecycle** for standardized development, supported by **Auxiliary Tools** that provide rigorous quality assurance and assistance when needed.

### Command Execution Flowchart

```mermaid
flowchart TD
    %% Setup Phase
    subgraph Setup ["Step 0: Preparation"]
        direction TB
        S1["/speckit.constitution"]
        S2["/speckit.instructions"]
        S3["/speckit.skills"]
    end

    %% Core Flow
    subgraph Core ["Core Development Lifecycle"]
        direction TB
        C1["1. /speckit.feature"]
        C2["2. /speckit.requirements"]
        C3["3. /speckit.plan"]
        C4["4. /speckit.tasks"]
        C5["5. /speckit.implement"]
    end

    %% Flow Connectivity
    Start([Start]) ====> Setup
    Setup ====> C1
    C1 ====> C2
    C2 ====> C3
    C3 ====> C4
    C4 ====> C5
    C5 ====> End([End])

    %% Auxiliary / Optional Tools - Context sensitive placement
    
    %% Research supports Specify
    T_Res[["/speckit.research\n(Optional)"]] -.- C2
    
    %% Clarify repairs Specify
    C2 -.- T_Clar[["/speckit.clarify\n(Ambiguity Resolver)"]] -.-> C2
    
    %% Checklist serves as a gate before Implement
    C4 -.- T_Chk[["/speckit.checklist\n(QA Gate)"]] -.-> C5
    
    %% Analyze watches over the artifacts
    C2 & C3 & C4 & C5 -.- T_Ana[["/speckit.analyze\n(Consistency Check)"]]
    
    %% Review validates the Implementation
    C5 -.- T_Rev[["/speckit.review\n(Post-Impl Review)"]] -.-> End

    %% Styling
    classDef setup fill:#2d3748,stroke:#a0aec0,color:#e2e8f0,stroke-width:1px,stroke-dasharray: 5 5;
    classDef core fill:#1e3a5f,stroke:#60a5fa,color:#e2e8f0,stroke-width:3px;
    classDef aux fill:#4a5568,stroke:#cbd5e0,color:#f7fafc,stroke-width:1px,stroke-dasharray: 5 5;
    classDef startEnd fill:#166534,stroke:#4ade80,color:#ffffff,stroke-width:2px;
    
    class Start,End startEnd
    class S1,S2,S3 setup
    class C1,C2,C3,C4,C5 core
    class T_Res,T_Clar,T_Chk,T_Ana,T_Rev aux
```

This flowchart distinguishes between the **Core Path** (solid arrows) and **Auxiliary Tools** (dashed lines):

1.  **Preparation**: `/speckit.constitution`, `/speckit.instructions`, `/speckit.skills` (Run once or as needed).
2.  **Core Lifecycle**:
    *   `1. /speckit.feature`: Create/select a feature registry entry (long-lived ID/name/status).
    *   `2. /speckit.requirements`: Create/update the requirements specification (WHAT/WHY) for that feature.
    *   `3. /speckit.plan`: Create the technical plan.
    *   `4. /speckit.tasks`: Breakdown into tasks.
    *   `5. /speckit.implement`: Execute code changes.
3.  **Auxiliary Tools (Optional)**:
    *   `/speckit.research`: Use during specification if external data is needed.
    *   `/speckit.clarify`: Use if specification has `[NEEDS CLARIFICATION]` tags.
    *   `/speckit.checklist`: Use to generate pre-implementation validation lists.
    *   `/speckit.analyze`: Use at any stage to check for artifact consistency.
    *   `/speckit.review`: Use after implementation to verify against spec/plan.

## Best Practices

- Always run `/speckit.requirements` to establish clear requirements before planning
- Use `speckit.checklist` before implementation to ensure quality
- Run `speckit.analyze` regularly to catch inconsistencies early
- Keep specifications focused on WHAT and WHY, not HOW
- Limit clarifications to critical decisions only
- Maintain constitutional compliance throughout the workflow
