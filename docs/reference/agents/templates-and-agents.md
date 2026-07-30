# Templates & Persisted Agents

This document is the reference for the framework's **artifacts**: the canonical template
catalog that `create-agent`/`improve-agent` operate on, the persisted agents under
`.specify/agents/`, the registry, and the directory/symlink model that makes agents
available to every supported tool. For the concept model see [design.md](./design.md); for
the command/skill surface see [command-and-skills.md](./command-and-skills.md).

## Canonical template catalog

Agent templates are split by domain. This document covers the **single-agent** families, which
live at **`skills/create-agent/templates/`** (installed mirror:
`.specify/skills/create-agent/templates/`). The **multi-agent** templates — the Team Supervisor,
the three EEI stages, the parallel/serial/triad orchestration templates, and the workflow schema —
live at **`skills/create-team/templates/agents/`** and are catalogued in the team docs
([`docs/teams/orchestration.md`](../teams/orchestration.md); normative source
[`conceptual-model.md`](../../../skills/create-team/references/conceptual-model.md)).

### Capacity templates (`agent-capacity-*`)

The seven Worker roles. Each Worker role template carries `supervisor: true` and
`capacity-scope: <slug>` in frontmatter.

| Template | Role | Type |
|----------|------|------|
| `agent-capacity-requirements-analyst-template.md` | Requirements Analyst | Worker |
| `agent-capacity-ux-analyst-template.md` | UX Analyst | Worker |
| `agent-capacity-system-designer-template.md` | System Designer | Worker |
| `agent-capacity-module-designer-template.md` | Module Designer | Worker |
| `agent-capacity-test-engineer-template.md` | Test Engineer | Worker |
| `agent-capacity-qa-engineer-template.md` | QA Engineer | Worker |
| `agent-capacity-knowledge-manager-template.md` | Knowledge Manager | Worker |

> The eighth role, **Team Supervisor** (the single Meta role, Meta at all stages), is a
> multi-agent template: `agent-team-supervisor-template.md` lives in
> `skills/create-team/templates/agents/`. See [`docs/teams/`](../teams/overview.md).

> Every role template enforces **six mandatory sections** (Identity & Responsibilities,
> Project Context, Workflow, Upstream, Downstream, Output Format), uses only approved
> `{{PLACEHOLDER}}` variables, and **omits** the `tools` field (inherits platform defaults).

### Project-custom & shared single-agent assets

| Template | Purpose |
|----------|---------|
| `agent-project-custom-template.md` | A project-bound custom agent (marks its project + carries a scope guard) |
| `agent-supervision-delegation.md` | **Single-source** supervision snippet, inlined into every generated supervisor at generation time — edit only here |
| `agent-skill-enablement.md` | **Single-source** Skill Enablement protocol, composed into each role agent's `## Skill Enablement` section |

### Multi-agent templates (owned by the team domain)

The Stage templates (`agent-stage-{executor,evaluator,optimizer}`), the orchestration templates
(`agent-{parallel,serial,triad}-orchestration-template.md`), the Team Supervisor template, and the
`agent-workflow-schema.md` (the `AgentWorkflow` JSON schema used by serial orchestration) are all
**multi-agent** artifacts under `skills/create-team/templates/agents/`. They are documented in
[`docs/teams/orchestration.md`](../teams/orchestration.md), not here.

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
  `supervisor: true`, `capacity-scope: <slug>`, plus Qoder-compatible fields `model` (default
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

Normative source: the template catalog under `skills/create-agent/templates/` and
`skills/create-team/templates/agents/`, and the persisted agents under `.specify/agents/`. The
deprecated-term guard `tests/unit/test_agent_deprecated_terms.py` keeps the `Stage`/`optimizer`
naming enforced across all templates and persisted agents.
