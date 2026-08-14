# Feature Specification: Agent Framework Refactor

**Feature Branch**: `014-agent-framework-refactor`  
**Created**: 2026-06-15  
**Status**: Draft  
**Input**: User description: "重构项目中的agent相关的流程. 当前的agent机制实现不太合理,需要重建进行设计和实现. 我希望实现的效果:1) 在/speckit.agents 命令执行之后会在.specify/agents目录中创建一个通用的agent定义结构,包括AGENTS.md MEMORY.md SOUL.md USER.md等一般AI cli工具的标准结构;2) 在执行/speckit.agents之后需要根据当前使用的工具,通过软连接的方式进行适配,如claude code中subagent格式兼容 VS Code Copilot custom agent 规范,因此对于claude code和vscode copilot可以创建.github/agents/<name>.agent.md -> .specify/agents/<name>.agent.md 的软连接来进行桥接. qoder中的agents保存在 .qoder/agents/*.md, 也可以通过软链接来进行桥接, 以此类推; 3) speckit框架中会预置一些通用的agent放在agents目录中,在执行specify init命令的时候需要将agents也拷贝到工具对应的.specify目录中,这点可以参考已有的skills目录的逻辑. 4)每个agent应该是一个md文件作为入口,然后不同的引用分散到references子目录中,注意在最终安装的agents目录中,多个agent的md文件可以共享一个references目录."

## Related Feature *(mandatory)*

**Feature ID**: 019  
**Feature Name**: Agents Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Agent via `/speckit.agents` Command (Priority: P1)

A developer using Spec Kit runs `/speckit.agents` to create a new custom AI agent. The command generates a standard agent definition structure under `.specify/agents/`, including the agent's entry `.agent.md` file and any supporting reference files in a shared `references/` subdirectory. The developer can immediately use this agent in their preferred AI tool without manual setup.

**Why this priority**: This is the foundational capability — without agent creation in the canonical `.specify/agents/` directory, none of the downstream features (symlink bridging, init bundling) have anything to operate on.

**Independent Test**: Can be fully tested by running `/speckit.agents` with a name/description and verifying the resulting directory structure under `.specify/agents/` contains the expected `.agent.md` entry point and any referenced files.

**Acceptance Scenarios**:

1. **Given** a Spec Kit project with no existing agents, **When** the user runs `/speckit.agents` with an agent description, **Then** a new `.specify/agents/<name>.agent.md` file is created with valid frontmatter and body sections.
2. **Given** the agent requires supporting context (domain knowledge, reference prompts), **When** the agent is created, **Then** reference files are placed in `.specify/agents/references/` and the agent's `.agent.md` file includes relative paths to those references.
3. **Given** a `.specify/agents/` directory already exists with other agents, **When** a new agent is created, **Then** the new agent's reference files coexist in the shared `references/` directory without overwriting existing reference files.
4. **Given** the user also wants standard workspace agent support files, **When** `/speckit.agents` runs for the first time, **Then** it creates `AGENTS.md` (index), `MEMORY.md`, `SOUL.md`, and `USER.md` in `.specify/agents/` if they do not already exist.

---

### User Story 2 - Tool-Specific Symlink Bridging (Priority: P1)

After creating agents in the canonical `.specify/agents/` location, the developer's preferred AI tool (Claude Code, VS Code Copilot, Qoder, Qwen, opencode) can discover and use those agents via directory-level symlinks from tool-specific paths to `.specify/agents/`. This matches the existing skills symlink pattern and ensures all agent files (`.agent.md` entries, workspace files, and references) are automatically accessible without managing individual symlinks.

**Why this priority**: Equally critical as P1/US1 because agent discoverability by the AI tool is what delivers the value. An agent that exists but is invisible to the tool is useless.

**Independent Test**: Can be tested by creating an agent via `/speckit.agents`, then verifying that a directory-level symlink exists at the tool-specific path (e.g., `.github/agents/ → .specify/agents/`) and that agents are discoverable through the symlink.

**Acceptance Scenarios**:

1. **Given** agents exist in `.specify/agents/`, **When** the current tool is Claude Code or VS Code Copilot, **Then** a directory-level symlink `.github/agents/` → `.specify/agents/` is created, making all agents discoverable.
2. **Given** agents exist in `.specify/agents/`, **When** the current tool is Qoder, **Then** a directory-level symlink `.qoder/agents/` → `.specify/agents/` is created.
3. **Given** multiple AI tools are configured for the project, **When** symlink bridging runs, **Then** all relevant tool directories receive directory-level symlinks pointing to the same canonical `.specify/agents/`.
4. **Given** an agent is updated or added in `.specify/agents/`, **When** the user accesses agents via any tool-specific symlink, **Then** the changes are immediately visible (directory symlink semantics).
5. **Given** the tool-specific parent directory (e.g., `.github/`) does not contain an `agents/` entry, **When** symlink bridging runs, **Then** the `agents/` symlink is created automatically.

---

### User Story 3 - Pre-built Agents Bundled with `specify init` (Priority: P2)

When a developer initializes a new Spec Kit project via `specify init`, pre-built agents bundled in the Spec Kit package are automatically copied into the project's `.specify/agents/` directory, and appropriate tool-specific symlinks are established — mirroring the existing skills installation flow.

**Why this priority**: Provides immediate out-of-the-box value but depends on the canonical agent structure (US1) and symlink mechanism (US2) being in place first.

**Independent Test**: Can be tested by running `specify init` on a new project and verifying that bundled agents appear in `.specify/agents/` with correct structure, and tool-specific symlinks are created.

**Acceptance Scenarios**:

1. **Given** the Spec Kit package contains pre-built agents in its `agents/` directory, **When** the user runs `specify init`, **Then** all bundled agents are copied to `.specify/agents/` preserving the `.agent.md` entry + shared `references/` structure.
2. **Given** the project already has a `.specify/agents/` directory with user-created agents, **When** `specify init` runs, **Then** bundled agents are merged without overwriting existing user agents.
3. **Given** `specify init` completes agent installation, **When** the tool is Claude Code, **Then** symlinks are created under `.github/agents/` for all installed agents.
4. **Given** `specify init` completes agent installation, **When** the tool is Qoder, **Then** symlinks are created under `.qoder/agents/` for all installed agents.

---

### User Story 4 - Shared References Directory Across Agents (Priority: P2)

Multiple agents in the same project can share common reference materials (prompts, knowledge files, guidelines) through a single `references/` subdirectory within `.specify/agents/`. When creating a new agent, the author can reference existing shared materials or add new ones without file duplication.

**Why this priority**: Reduces maintenance burden and file duplication, but agents function correctly without shared references (each could embed its own context). This is an ergonomic improvement.

**Independent Test**: Can be tested by creating two agents that both reference a common guideline file in `references/`, verifying both `.agent.md` files can resolve the shared reference, and confirming no duplicate copies exist.

**Acceptance Scenarios**:

1. **Given** two agents (`code-reviewer.agent.md` and `security-auditor.agent.md`) need the same coding standards reference, **When** both are created, **Then** both reference files in `.specify/agents/references/` by relative path, and only one copy of the shared reference exists.
2. **Given** a new agent is created that introduces new reference material, **When** the reference is placed in `.specify/agents/references/`, **Then** existing agents' references remain unaffected.

---

### Edge Cases

- What happens when a tool-specific agents directory already exists as a regular directory (not a symlink)? The system should migrate existing content into `.specify/agents/`, then replace the directory with a symlink, mirroring the existing skills symlink behavior.
- What happens when multiple AI tools are configured for the same project? All configured tools should receive their own directory-level symlinks pointing to the same canonical `.specify/agents/`.
- What happens when an agent is deleted from `.specify/agents/`? Since tool-specific paths are directory symlinks, deletions are automatically reflected — no dangling symlink cleanup needed for individual agents.
- What happens when `.specify/agents/references/` contains a file name collision from two different agents? Reference files should use agent-prefixed or namespaced naming when ambiguity is possible (e.g., `code-reviewer-guidelines.md` vs `security-auditor-guidelines.md`), or use subdirectories within `references/` if needed.
- What happens when running `/speckit.agents` outside a Spec Kit project (no `.specify/` directory)? The command should fail with a clear error message directing the user to run `specify init` first.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `/speckit.agents` MUST create agent definition files in the canonical directory `.specify/agents/<name>.agent.md`.
- **FR-002**: `/speckit.agents` MUST generate standard workspace support files (`AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md`) in `.specify/agents/` on first run if they do not already exist.
- **FR-003**: Each agent MUST consist of a single `.agent.md` entry-point file that contains frontmatter metadata and body instructions.
- **FR-004**: Agent reference materials MUST be stored in a shared `.specify/agents/references/` directory, accessible to all agents via relative paths.
- **FR-005**: After agent creation or update, the system MUST create directory-level symlinks from tool-specific agent directories to the canonical `.specify/agents/` directory, based on the detected or configured AI tool(s). This mirrors the existing skills directory symlink pattern.
- **FR-006**: Directory-level symlink bridging MUST support at minimum: `.github/agents/` (Claude Code, VS Code Copilot), `.qoder/agents/` (Qoder), `.qwen/agents/` (Qwen), `.opencode/agents/` (opencode) — all pointing to `.specify/agents/`.
- **FR-007**: `specify init` MUST copy pre-built agents from the package's `agents/` directory into `.specify/agents/`, following the same pattern as the existing skills installation flow.
- **FR-008**: `specify init` MUST create tool-specific directory-level agent symlinks for all supported tools after copying bundled agents.
- **FR-009**: Agent installation during `specify init` MUST NOT overwrite existing user-created agents with the same name.
- **FR-010**: The system MUST auto-create tool-specific directories (e.g., `.github/agents/`) if they do not exist before placing symlinks.
- **FR-011**: When a tool-specific path contains a regular file (not a symlink) that conflicts with a new symlink target, the system MUST handle the conflict by migrating the existing content into `.specify/agents/` and replacing the file with a symlink, consistent with existing skills symlink behavior.
- **FR-012**: The `.agent.md` file format MUST remain compatible with VS Code Copilot custom agent specification (YAML frontmatter + markdown body).

### Key Entities

- **Agent Definition**: A single `.agent.md` file serving as the entry point for an agent. Contains YAML frontmatter (name, description, tools, model, etc.) and markdown body (purpose, constraints, workflow, output format). Stored canonically at `.specify/agents/<name>.agent.md`.
- **Agent Reference**: Supporting material (knowledge files, prompt fragments, domain guidelines) stored in `.specify/agents/references/`. Referenced by relative path from agent `.agent.md` files. Shared across multiple agents.
- **Agent Workspace Files**: Standard infrastructure files (`AGENTS.md` index, `MEMORY.md`, `SOUL.md`, `USER.md`) that provide project-wide agent context. Created once in `.specify/agents/` and updated as agents are added.
- **Symlink Bridge**: A directory-level symbolic link (e.g., `.github/agents/` → `.specify/agents/`) that makes the entire canonical agents directory accessible from tool-specific paths. Mirrors the existing skills symlink pattern. Ensures tool discoverability without content duplication.
- **Bundled Agent**: A pre-built agent shipped in the Spec Kit package's `agents/` directory. Installed into user projects during `specify init`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After running `/speckit.agents`, the resulting `.specify/agents/` directory contains the expected `.agent.md` file and workspace support files within 30 seconds.
- **SC-002**: All created agents are discoverable by their target AI tool via symlinks — users can invoke them without additional manual configuration steps.
- **SC-003**: Running `specify init` on a fresh project installs all bundled agents and creates symlinks for all detected tools, matching the completeness of the existing skills installation flow.
- **SC-004**: Two or more agents in the same project can share reference files in `references/` without file duplication, and both agents function correctly when invoked.
- **SC-005**: Updating an agent's content in `.specify/agents/` is immediately reflected when accessed via any tool-specific symlink, with zero manual sync steps required.

## Assumptions

- The existing skills symlink pattern (`ensure_agent_skills_symlink` function in `__init__.py`) is a proven approach that can be adapted for agents with minimal modification.
- The VS Code Copilot custom agent `.agent.md` format is the canonical format, and other tools either natively support it or can consume it with minimal naming adjustments (e.g., Qoder drops the `.agent` suffix).
- The standard workspace files (`AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md`) follow industry conventions for AI CLI tool workspaces and do not need per-tool format variations.
- Pre-built agents bundled with the package are general-purpose enough to be useful across different project types without customization.

## Clarifications

### Session 2026-06-15

- Q: Which existing Feature should this spec bind to? → A: Feature 019 (Agents Command) — this spec refactors and extends the existing agents feature under the many-specs-to-one-feature model.
- Q: Should workspace support files also be symlinked, or only `.agent.md` files? → A: Use directory-level symlinks (e.g., `.github/agents/ → .specify/agents/`), matching the existing skills pattern. This automatically exposes both `.agent.md` files and workspace files without managing individual symlinks.
