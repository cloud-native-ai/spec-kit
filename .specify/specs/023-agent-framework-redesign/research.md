---
description: "FR-021 cross-project agent-framework research for Agent Framework Redesign"
---

# Research: Agent Framework Redesign (FR-021)

**Requirement ID**: 023
**Requirement Key**: 023-agent-framework-redesign
**Deliverable for**: FR-021, SC-008, DoD-7
**Method**: One research agent dispatched per in-scope `/cws_work/*` sibling (excluding `spec-kit`) via the `organize-agents` parallel pattern, mining agent-framework best practices. Findings consolidated below and cited by ≥1 concrete redesign decision (see § Redesign Decisions).

## Scope

Seven sibling projects were studied for how they model, dispatch, and persist agents:
`OpenSpec`, `superpowers`, `claw-code-agent`, `intellegix-code-agent-toolkit`, `claude-code-ts`, `claude-code-py`, `learn-claude-code`.

---

## Per-Project Findings

### 1. OpenSpec (`/cws_work/OpenSpec`)

- Single CLI entry (`commander`) with a root-command resolution priority order; every capability is reached through one dispatcher, not per-feature commands.
- `--json` agent contract: each invocation emits exactly one JSON document, making agent I/O machine-parseable and composable.
- Artifact-driven workflow: a schema defines the dependency graph between spec artifacts; work is gated on artifact presence rather than free-form prompting.
- Persistence split: a store registry holds durable context; `cwd`-scoped runs are ephemeral.
- Not a traditional multi-agent framework — a spec-driven tool. Reinforces "single entry + explicit artifacts" over ad-hoc agent proliferation.
- Key files: `docs/agent-contract.md`, `docs/concepts.md`, `docs/customization.md`, `src/cli/index.ts`.

### 2. superpowers (`/cws_work/superpowers`)

- `SKILL.md` + YAML frontmatter enables zero-config auto-discovery of capabilities.
- Multi-harness plugin mirrors (`.claude-plugin`, `.opencode`, `.codex-plugin`, `.cursor-plugin`, `.kimi-plugin`, `.pi`) — one source, many installed mirrors.
- Subagents run in a brand-new isolated context; parallel dispatch = a single response issuing multiple tool calls.
- Single bootstrap entry (`using-superpowers`) injected via a `SessionStart` hook.
- All agents are ephemeral (no persisted agent store).
- Key files: `hooks/session-start`, `skills/subagent-driven-development/SKILL.md`, `skills/dispatching-parallel-agents/SKILL.md`, `.opencode/plugins/superpowers.js`.

### 3. claw-code-agent (`/cws_work/claw-code-agent`)

- Single command entry via `argparse` subparsers (`agent` / `agent-chat` / `agent-bg` / `agent-resume` / `daemon`).
- Explicit temporary vs persistent split: temporary = in-memory `LocalCodingAgent`; persistent = `StoredAgentSession` written to `.port_sessions/agent`.
- Agents defined as an `AgentDefinition` dataclass; filesystem custom-agent discovery (`~/.claude/agents`) with precedence built-in < userSettings < projectSettings.
- `AgentManager` tracks nested-delegation lineage (`ManagedAgentGroup`, strategy=serial).
- Flat agent `type` — no Role/Stage matrix.
- Key files: `src/main.py`, `src/builtin_agents.py`, `src/agent_registry.py`, `src/session_store.py`, `src/agent_manager.py`.

### 4. intellegix-code-agent-toolkit (`/cws_work/intellegix-code-agent-toolkit`)

- Orchestration commands: `/orchestrator` (single loop), `/orchestrator-multi` (parallel git worktrees), `/orchestrator-new`.
- Orchestrator is an instruction-writer, not an implementer — a clean Meta/Worker boundary.
- Temporary = `session_context.py` (~500–2000 tokens); persistent = `.workflow/state.json`.
- Territory-based conflict prevention + sequential merge for parallel work.
- `agents/*.md` role definitions; `orchestrator-guard.py` PreToolUse hook enforces path boundaries; exit codes 0/1/2/3.
- Key files: `agents/orchestrator.md`, `commands/orchestrator-multi.md`, `automated-loop/loop_driver.py`, `automated-loop/state_tracker.py`, `hooks/orchestrator-guard.py`.

### 5. claude-code-ts (`/cws_work/claude-code-ts`)

- `Task` typed by execution target (`local_agent` / `remote_agent` / `in_process_teammate` / `local_workflow`).
- Temporary = `LocalAgentTask` sidechain; persistent = workflow `state.json` / teammate.
- Two-level skill loading (catalog + on-demand) with conditional activation.
- Coordinator mode (star topology) vs Swarm (team + mailbox).
- Worker agents exclude internal orchestration tools (capability follows role).
- Single entry `AgentTool` routing (`named` / `fork` / `general-purpose`).
- Key files: `src/Task.ts`, `src/skills/loadSkillsDir.ts`, `src/coordinator/coordinatorMode.ts`, `src/coordinator/workerAgent.ts`, `src/workflow/persistence.ts`, `docs/agent/coordinator-and-swarm.mdx`.

### 6. claude-code-py (`/cws_work/claude-code-py`)

- Plugin framework layout: `plugin-name/{.claude-plugin/, commands/, agents/, skills/, hooks/}`.
- Agent = markdown + frontmatter (`name` / `description` / `model` / `color`).
- Command is the single orchestration entry.
- Temporary = context; persistent = `.claude/agents/`.
- `memory` field with user / project / local scope.
- Key files: `.claude-plugin/marketplace.json`, `plugins/README.md`, `plugins/pr-review-toolkit/agents/*.md`, `commands/review-pr.md`.

### 7. learn-claude-code (`/cws_work/learn-claude-code`)

- Minimal agent loop that progressively gains capabilities across stages `s01`–`s13`.
- Subagents isolate context with fresh `messages[]` (s04 / s06).
- Two-level skill loading via `SKILL_REGISTRY` (s07).
- Task persistence: JSON + `blockedBy` DAG (s12); background tasks via daemon thread + notification injection (s13).
- Memory files `.memory/*.md` + `MEMORY.md` index (s09); teammate JSONL inbox (`s09_agent_teams.py`).
- Directories: `s01_agent_loop` … `s13_background_tasks`, `agents/`.

---

## Cross-Project Synthesis

1. **Single command entry is universal.** All 7 projects funnel every agent action through one dispatcher (CLI subparser, `AgentTool`, orchestrator command, or command file) rather than per-operation commands.
2. **Temporary vs persistent is a first-class split.** Temporary lives in memory / context / fresh `messages[]`; persistent is written to disk (`.port_sessions`, `.workflow`, `.tasks`, `.memory`, `.claude/agents`, workflow runs).
3. **Three recurring multi-agent topologies:** parallel (single response, many tool calls), serial chain, and team-loop (coordinator/worker or team-lead/teammate + mailbox).
4. **Subagents get an isolated context** (superpowers, learn-claude-code, claude-code-ts) — the standard for delegation.
5. **Agents are defined as markdown + frontmatter** (claw-code-agent, claude-code-py, intellegix, claude-code-ts).
6. **Capability follows role:** worker agents are denied orchestration tools (claude-code-ts `workerAgent`, intellegix orchestrator boundary).
7. **One source, many installed mirrors** (superpowers multi-harness plugin mirrors) validates a canonical-source + generated-mirror layout.

---

## Redesign Decisions (citing this research — SC-008 / DoD-7)

- **RD-1 (Single `/speckit.agents` entry, FR-001/FR-019).** Adopt one intent-routing command for create/organize/execute. **Cites** the universal single-entry pattern in OpenSpec, claw-code-agent (`argparse` subparsers), claude-code-ts (`AgentTool` routing), and claude-code-py (single command orchestration). Rejects per-operation commands.
- **RD-2 (Temporary vs persistent lifecycle, FR-010/011/012).** Temporary agents live only in context; persistent agents are stored under `.specify/agents/`. **Cites** the explicit temporary/persistent split in claw-code-agent (`LocalCodingAgent` vs `StoredAgentSession`), intellegix (`session_context` vs `.workflow/state.json`), and claude-code-ts (sidechain vs workflow `state.json`).
- **RD-3 (Canonical source + generated mirror, M7).** Keep `skills/create-agent/templates/` as source of truth and generate the `.specify/skills/create-agent/templates/` mirror. **Cites** superpowers' one-source/many-mirror multi-harness plugin model.
- **RD-4 (Type-follows-Stage / capability follows role, FR-005/C6).** Worker types are constrained by stage; the Team Supervisor (Meta role) is denied worker-only framing. **Cites** claude-code-ts `workerAgent` tool exclusion and intellegix's orchestrator-is-not-implementer boundary.
- **RD-5 (Two-layer Team Loop, FR-007/M3).** Collapse to Team Supervisor + Workers, merging Meta-Coordinator into the Team Supervisor. **Cites** intellegix's single orchestrator/worker boundary and claude-code-ts coordinator↔worker (2-role) topology, which show a distinct third coordinator layer is unnecessary.
