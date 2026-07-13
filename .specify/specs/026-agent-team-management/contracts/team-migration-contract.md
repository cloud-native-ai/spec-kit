# Contract: Team Migration (rename + extraction + relocation)

**Feature**: 027 Team Management | **Spec**: [requirements.md](../requirements.md)

This contract enumerates the concrete edits that realize the single-agent ↔ team split and guarantees zero dangling references (FR-006, FR-011, FR-013, FR-015; SC-003, SC-004, SC-006).

## M1 — Rename `organize-agents` → `create-team`

- Rename directory `skills/organize-agents/` → `skills/create-team/`.
- Update `SKILL.md` frontmatter `name`, `description`, and `skill_id` (`<SKILL:.specify/skills/create-team/SKILL.md>`).
- Update installed mirror `.specify/skills/organize-agents/` → `.specify/skills/create-team/` (regenerated on install) and the `.github/skills` symlink target.

## M2 — Extract the Conceptual Model

- Remove the `## Conceptual Model (Role × Stage × Type + Team/Loop)` section from `skills/create-agent/SKILL.md`.
- Create `skills/create-team/references/conceptual-model.md` as the single source of truth.
- Replace the removed section in `create-agent` with a one-line pointer to the team-domain reference (no re-definition).

## M3 — Relocate multi-agent templates

Move these from `skills/create-agent/templates/` to `skills/create-team/templates/` (per data-model § Template Classification):
`agent-role-team-supervisor-template.md`, `agent-stage-executor-template.md`, `agent-stage-evaluator-template.md`, `agent-stage-optimizer-template.md`, `agent-triad-orchestration-template.md`, `agent-parallel-orchestration-template.md`, `agent-serial-orchestration-template.md`, `agent-workflow-schema.md`.

## M4 — Re-scope the single-agent skills

- `create-agent`: drop `triad` and `team-supervisor` from the capability matrix; retain `role`, `supervisor`, `custom`, `project-custom`. Repoint any template paths to their new team-domain locations where still referenced (none should remain for moved templates).
- `improve-agent`: remove the **Triad Refinement** section and stage/orchestration targets; those move to `improve-team`.

## M5 — Add the new command + skill

- Create `templates/commands/team.md` (source of `/speckit.team`, 3 modes) per the command contract.
- Create `skills/improve-team/SKILL.md` per the improve-team contract.
- Create `docs/commands/team.md` (user doc).

## M6 — Update references, registries, and docs (no dangling `organize-agents`)

Known reference sites to update (active paths only; historical `.specify/specs/*` archives excluded):

| File | Change |
|------|--------|
| `templates/commands/agents.md` | Remove organize/execute rows + `organize-agents` routing; scope `/speckit.agents` to create/refine single agents; point team intents to `/speckit.team`. |
| `templates/commands/skills.md` | Update any `organize-agents` reference to the team skills. |
| `skills/create-skills/SKILL.md` (line ~149) | Replace `organize-agents` in the non-declarable list with `create-team`, `improve-team`. |
| `tests/contract/test_agent_skill_enablement.py` | Update `NON_DECLARABLE` set: replace `organize-agents` with `create-team`, `improve-team`. |
| `tests/scenarios/agents-command/single-entry-routing-scenario.md` | Remove team routing from the `/speckit.agents` scenario. |
| `docs/agents/{design,command-and-skills,multi-agent-orchestration,README}.md` | Repoint Conceptual Model + orchestration ownership to the team domain and `/speckit.team`. |
| `docs/commands/agents.md`, `docs/commands/skills.md` | Update routing tables; add `/speckit.team`. |
| `.specify/instructions.md` | Regenerate via `/speckit.instructions` (skills registry, resource registry, skill inventory). |
| Per-tool command copies (`.qoder/commands/`, `.claude/commands/`, `.github/prompts/`, `.opencode/command/`, `.qwen/…`) | Regenerate so `speckit.agents.*` drops team routing and `speckit.team.*` is added. |

## M7 — Guard tests (Test-First, Constitution IV)

Author before implementation:

1. **Zero dangling reference** — repository-wide search asserts `organize-agents` appears in **no** active path (SC-004).
2. **Single Conceptual Model** — asserts the Conceptual Model is defined exactly once (team domain) and not embedded in `create-agent/SKILL.md` (SC-006).
3. **Single-agent purity** — asserts `create-agent`/`improve-agent` contain no team/orchestration content and no `triad`/`team-supervisor` modes (SC-003).
4. **Command routing** — asserts `/speckit.team` exposes create/modify/run and that team ops are not served by `/speckit.agents` (SC-002).
5. **Skill presence** — asserts `create-team` and `improve-team` skills install and resolve; `organize-agents` no longer resolves.

## Acceptance

All of M1–M7 complete, all guard tests green, `/speckit.instructions` regenerated, and Feature 027 advanced per the state machine.
