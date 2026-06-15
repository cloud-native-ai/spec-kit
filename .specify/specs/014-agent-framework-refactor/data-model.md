# Data Model: Agent Framework Refactor

**Spec**: 014-agent-framework-refactor | **Date**: 2026-06-15

## Entities

### Agent Definition

A single `.agent.md` file — the entry point for an agent.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | Display name (defaults to filename stem) |
| description | string | Yes | Trigger description for agent selection |
| tools | string[] | No | Allowed tool set (least-privilege); omit = platform defaults |
| model | string \| string[] | No | Preferred model or fallback array |
| argument-hint | string | No | Prompt guidance for user input |
| agents | string[] | No | Allowed subagent names; `[]` = no delegation |
| user-invocable | boolean | No | Whether user can invoke directly (default: true) |
| disable-model-invocation | boolean | No | Prevent other agents from invoking (default: false) |
| handoffs | object[] | No | Transitions to other agents |
| body | markdown | Yes | Role, constraints, workflow, output format sections |

**Canonical path**: `.specify/agents/<name>.agent.md`
**Naming**: kebab-case derived from display name or role
**Format**: YAML frontmatter + Markdown body (VS Code Copilot `.agent.md` compatible)

### Agent Reference

Supporting material shared across agents.

| Field | Type | Description |
|-------|------|-------------|
| filename | string | File name within `references/` directory |
| content | markdown | Knowledge file, prompt fragment, or domain guideline |

**Canonical path**: `.specify/agents/references/<filename>`
**Naming convention**: Agent-prefixed when ambiguity possible (e.g., `code-reviewer-guidelines.md`), or generic when shared (e.g., `coding-standards.md`)

### Agent Workspace Files

Standard infrastructure files for project-wide agent context.

| File | Purpose | Created By |
|------|---------|------------|
| `AGENTS.md` | Index of all agents — names, descriptions, invocation hints | `/speckit.agents` (first run) |
| `MEMORY.md` | Persistent context shared across agent invocations | `/speckit.agents` (first run) |
| `SOUL.md` | Project identity and principles for agent internalization | `/speckit.agents` (first run) |
| `USER.md` | Current user context, preferences, working style | `/speckit.agents` (first run) |

**Canonical path**: `.specify/agents/<FILE>.md`
**Lifecycle**: Created once on first `/speckit.agents` invocation if absent; never overwritten by `specify init`.

### Symlink Bridge

Directory-level symbolic link for tool discoverability.

| Field | Type | Description |
|-------|------|-------------|
| source | path | Tool-specific path (e.g., `.github/agents/`) |
| target | path | Canonical `.specify/agents/` (relative path) |
| is_directory | boolean | Always `true` — directory-level symlink |

**Mapping**:

| Tool | Source Directory | Target |
|------|-----------------|--------|
| Claude Code / VS Code Copilot | `.github/agents/` | `.specify/agents/` |
| Qoder | `.qoder/agents/` | `.specify/agents/` |
| Qwen | `.qwen/agents/` | `.specify/agents/` |
| opencode | `.opencode/agents/` | `.specify/agents/` |

### Bundled Agent

Pre-built agent shipped in the Spec Kit package.

| Field | Type | Description |
|-------|------|-------------|
| source_path | path | `agents/<name>.agent.md` in package |
| install_path | path | `.specify/agents/<name>.agent.md` in target project |
| references | path[] | Associated files in `agents/references/` |

**Installation behavior**: Copied during `specify init`; existing user agents with same name are preserved (no overwrite).

## Relationships

```
Agent Definition ──references──▶ Agent Reference (0..N, via relative path)
Agent Definition ◀──indexes──── AGENTS.md (workspace file)
Agent Definition ◀──symlinked── Symlink Bridge (1..N, one per tool)
Bundled Agent ──installs-as──▶ Agent Definition (during specify init)
```

## Directory Layout

```
.specify/agents/                    # Canonical directory
├── AGENTS.md                       # Agent index (workspace file)
├── MEMORY.md                       # Shared persistent context
├── SOUL.md                         # Project identity/principles
├── USER.md                         # User preferences
├── code-reviewer.agent.md          # Agent entry point
├── security-auditor.agent.md       # Agent entry point
└── references/                     # Shared reference materials
    ├── coding-standards.md         # Shared across agents
    └── security-checklist.md       # Used by security-auditor
```

## State Transitions

Agent lifecycle is simple — agents are static files, not runtime entities:

```
[Not Exists] → create via /speckit.agents → [Created]
[Created] → update via /speckit.agents → [Updated] (overwrite)
[Created] → delete manually → [Removed] (symlinks auto-reflect)
```

Symlink lifecycle:

```
[Not Exists] → specify init or /speckit.agents → [Linked]
[Regular Dir] → migrate + replace → [Linked]
[Linked, stale target] → specify init → [Re-linked]
```
