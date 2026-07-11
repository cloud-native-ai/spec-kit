# Templates & Persisted Agents

This document is the reference for the framework's **artifacts**: the canonical template
catalog that `create-agent`/`improve-agent` operate on, the persisted agents under
`.specify/agents/`, the registry, and the directory/symlink model that makes agents
available to every supported tool. For the concept model see [design.md](./design.md); for
the command/skill surface see [command-and-skills.md](./command-and-skills.md).

## Canonical template catalog

All templates live at **`skills/create-agent/templates/`** (installed mirror:
`.specify/skills/create-agent/templates/`). There are 15 templates in four families:

### Role templates (`agent-role-*`)

Seven Worker roles plus the single Meta role. Each Worker role template carries
`supervisor: true` and `role-scope: <slug>` in frontmatter.

| Template | Role | Type |
|----------|------|------|
| `agent-role-requirements-analyst-template.md` | Requirements Analyst | Worker |
| `agent-role-ux-analyst-template.md` | UX Analyst | Worker |
| `agent-role-system-designer-template.md` | System Designer | Worker |
| `agent-role-module-designer-template.md` | Module Designer | Worker |
| `agent-role-test-engineer-template.md` | Test Engineer | Worker |
| `agent-role-qa-engineer-template.md` | QA Engineer | Worker |
| `agent-role-knowledge-manager-template.md` | Knowledge Manager | Worker |
| `agent-role-team-supervisor-template.md` | Team Supervisor | Meta (all stages) |

> Every role template enforces **six mandatory sections** (Identity & Responsibilities,
> Project Context, Workflow, Upstream, Downstream, Output Format), uses only approved
> `{{PLACEHOLDER}}` variables, and **omits** the `tools` field (inherits platform defaults).

### Stage templates (`agent-stage-*`) — the EEI triad

| Template | Stage | Type |
|----------|-------|------|
| `agent-stage-executor-template.md` | executor | Worker |
| `agent-stage-evaluator-template.md` | evaluator | Meta |
| `agent-stage-optimizer-template.md` | optimizer | Meta |

These are the canonical, current filenames. The former `agent-subrole-*` naming and the
`improver` stage name are **removed**; see [design.md §七](./design.md) for the migration record.

### Orchestration templates

| Template | Topology |
|----------|----------|
| `agent-parallel-orchestration-template.md` | parallel dispatch |
| `agent-serial-orchestration-template.md` | serial chain |
| `agent-triad-orchestration-template.md` | EEI triad loop |

### Shared assets

| Template | Purpose |
|----------|---------|
| `agent-supervision-delegation.md` | **Single-source** supervision snippet, inlined into every generated supervisor at generation time — edit only here |
| `agent-workflow-schema.md` | The `AgentWorkflow` JSON schema used by serial orchestration |

## Persisted agents (`.specify/agents/`)

Persistent agents are stored as `<slug>.agent.md` in `.specify/agents/`, the **single source
of truth**. The seven preset role agents ship active:

| Name | File | Status |
|------|------|--------|
| Requirements Analyst | `requirements-analyst.agent.md` | Active |
| UX Analyst | `ux-analyst.agent.md` | Active |
| System Designer | `system-designer.agent.md` | Active |
| Module Designer | `module-designer.agent.md` | Active |
| Test Engineer | `test-engineer.agent.md` | Active |
| QA Engineer | `qa-engineer.agent.md` | Active |
| Knowledge Manager | `knowledge-manager.agent.md` | Active |

The Team Supervisor (Meta role) is authored on demand from its template rather than shipping
as a preset row in the registry.

### Anatomy of a persisted role agent

Each generated role agent (example: `requirements-analyst.agent.md`) contains:

- **Frontmatter**: `name`, `description`, `user-invocable`, `disable-model-invocation`,
  `supervisor: true`, `role-scope: <slug>`, plus Qoder-compatible fields `model` (default
  `auto`), `tools`, `maxTurns`, and `color`. Optional Qoder fields (`disallowedTools`,
  `timeoutMins`, `skills`, `mcpServers`, `permissionMode`, `background`, `isolation`) are
  available but unset by default.
- **Role / Stage / Type** section — states the role's Type and its per-stage Type
  (`executor` Worker · `evaluator` Meta · `optimizer` Meta), and its place in the Team/Loop.
- The **six mandatory sections** (Identity, Project Context, Workflow, Upstream, Downstream,
  Output Format).
- **Supervision & EEI Delegation** section — composed from the single-source snippet; declares
  the role-scoped EEI triad, role-default scoring dimensions and weights, and delegation rules.

## Discovery & the role workflow chain

There is **no separate registry file**. Agents are discovered by globbing
`.specify/agents/*.agent.md` and reading each file's frontmatter `name`/`description`.
The seven preset roles form this workflow chain:

```
Requirements Analyst → System Designer → Module Designer → Test Engineer → QA Engineer
                                  ↑      ↑                                  ↑                     ↓
                     UX Analyst ──┘      └── (interaction contracts)        └── feedback loop ────┘
                                                                                                   ↓
                                                                         Knowledge Manager (all roles)
```

UX Analyst is a cross-cutting design-phase Worker covering **all** user surfaces (front-end/GUI, CLI, commands, skills); it feeds UX specifications and interaction contracts to the System Designer and Module Designer.

After adding or updating agents, run `/speckit.instructions` to refresh discovery metadata.

## Qoder expert crosswalk

Spec Kit's SDD roles and Qoder's built-in expert team are **different taxonomies**. The SDD
roles keep their own names and are made available to Qoder as per-file symlinks **alongside**
Qoder's built-ins (they do not force-override built-ins). The nearest mapping is:

| Qoder built-in | Responsibility | SDD role (nearest) | Coverage |
|---|---|---|---|
| Lead Agent (not customizable) | understand / decompose / coordinate | Team Supervisor | Conceptual match (Lead Agent itself cannot be replaced) |
| Researcher | investigate, code location | Requirements Analyst | Partial (RA adds a code-investigation facet) |
| Full-Stack Engineer | front/back-end implementation | Module Designer | Full |
| QA | run tests & builds | QA Engineer | Full |
| Code Reviewer | code review | — | Gap |
| UI Operator | browser/UI verification | — (UX Analyst is design, not runtime verification) | Gap |
| Debug Engineer | fault diagnosis | — | Gap |
| — | — | UX Analyst / System Designer / Test Engineer / Knowledge Manager | SDD-only (no Qoder equivalent) |

The three gaps (Code Reviewer, UI Operator, Debug Engineer) have no direct SDD equivalent;
author them on demand via `/speckit.agents` if needed. To actually **override** a Qoder
built-in, create a file in `.qoder/agents/` whose frontmatter `name` exactly matches the
built-in expert's name (per Qoder's priority mechanism).

## Directory & symlink model

`.specify/agents/` is the **only** place agents are authored. Every supported tool's agent
directory is a **real directory** populated with **per-file symlinks** back to it — one link
per `*.agent.md`. Never write framework agents into the tool directories directly.

```
.specify/agents/                 ← canonical source of truth (author here)
   ├── requirements-analyst.agent.md
   ├── system-designer.agent.md
   └── … (+ references/ shared assets)

.qoder/agents/    (real dir)  ── <slug>.agent.md ─▶ ../../.specify/agents/<slug>.agent.md
.github/agents/   (real dir)  ── (per-file symlinks, same scheme)
.qwen/agents/     (real dir)  ── (per-file symlinks, same scheme)
.opencode/agents/ (real dir)  ── (per-file symlinks, same scheme)
   (and .hermes/agents, .iflow/agents where supported)
```

The CLI (re)creates these per-file links on initialization, migrating any legacy
whole-directory symlink to the per-file model. Because each tool `agents/` is a real
directory, a tool can add its own agent files (e.g. Qoder overrides) beside the framework
links. Only `.specify/agents/references/` remains a shared-assets store in the canonical
scope; the former `AGENTS.md`/`MEMORY.md`/`SOUL.md`/`USER.md` shared files have been removed
(agent runtime context is per chat-session, so they served no purpose).

## Traceability

Normative source: `.specify/specs/023-agent-framework-redesign/`
(`data-model.md`, `contracts/template-migration-contract.md`). The deprecated-term guard
`tests/unit/test_agent_deprecated_terms.py` keeps the `Stage`/`optimizer` naming enforced
across all templates and persisted agents.
