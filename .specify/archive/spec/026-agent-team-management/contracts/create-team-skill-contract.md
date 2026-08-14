# Contract: `create-team` Skill

**Feature**: 027 Team Management | **Spec**: [requirements.md](../requirements.md)

`create-team` is the renamed successor of `organize-agents` (FR-005). It owns two responsibilities in the team domain: **defining** a team and **executing** it (the orchestration engine inherited from `organize-agents`). It is the single source of truth for the multi-agent Conceptual Model (FR-012).

## Identity

- **Skill dir**: `skills/create-team/` (mirrored to `.specify/skills/create-team/`).
- **Frontmatter**: `name: create-team`; `skill_id: "<SKILL:.specify/skills/create-team/SKILL.md>"`; `description` describing team creation + execution (parallel / serial / team-loop). No lingering `organize-agents` string.
- **Owns**: `skills/create-team/references/conceptual-model.md` (extracted single source of truth) and `skills/create-team/templates/` (moved orchestration/triad/team-supervisor/stage templates — see data-model § Template Classification).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| goal / team intent | one of | Natural-language description of what the team must accomplish. |
| member agent list | one of | Explicit roster; if absent, `create-team` proposes members from the goal (FR-007). |
| pattern hint | optional | parallel / serial / team-loop; inferred via the decision tree when omitted. |
| persist? | optional | Whether to write `.specify/teams/<slug>/team.md` (default: persist). |
| target team (run) | run only | Existing `team.md` to execute. |

## Behavior

### Define (create mode)

1. Select the pattern via the decision tree (independent→parallel; sequenced→serial; iterative-quality→team-loop).
2. Build the roster (static structure) and pattern config (dynamic structure); for team-loop include exactly one Team Supervisor.
3. If members are missing, propose them (existing agents from `.specify/agents/`, or temporary stage/worker templates) for confirmation.
4. Persist a `Team` to `.specify/teams/<slug>/team.md` per the data-model schema (unless one-shot).

### Execute (run mode)

1. Load the team, then honor the **preview → confirm → execute** gate defined in the command contract (render Static + Dynamic structure, require confirmation).
2. On confirmation, orchestrate per pattern, preserving the inherited hard constraints:
   - territory validation before parallel dispatch;
   - DAG (no-cycle) validation before serial chain;
   - mandatory max-iteration cap for team loops;
   - file-path-only handoff; context isolation per subagent; idempotent execution.

## MUST / MUST NOT

- MUST preserve the three collaboration patterns and their hard constraints from `organize-agents` (FR-005).
- MUST NOT contain single-agent authoring modes (`role`, `supervisor`, `custom`, `project-custom` remain in `create-agent`).
- MUST define the Conceptual Model exactly once (in `references/conceptual-model.md`); other skills reference, never duplicate (FR-012).
- MUST leave no `organize-agents` reference in its own body, frontmatter, or `skill_id`.

## Outputs

- A persisted or one-shot `Team`; on run, an orchestration result report (parallel/serial/team-loop report per pattern).
