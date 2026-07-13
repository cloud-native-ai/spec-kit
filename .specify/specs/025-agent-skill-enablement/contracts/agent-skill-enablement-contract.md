# Contract: Agent Skill Enablement

**Feature**: 026 — Agent Skill Enablement
**Spec**: [../requirements.md](../requirements.md)
**Date**: 2026-07-13

This contract defines the normative interface for making the seven built-in role agents
skill-enabled. It governs three artifacts: the shipped agent definitions, their generator
templates, and the shared protocol snippet, plus the validation test that enforces them.

## C-1 — `skills` frontmatter field

Each built-in agent definition (`agents/<slug>.agent.md`) MUST declare a `skills` key in its
YAML frontmatter.

- The value MUST be a YAML list of strings.
- Each string MUST be the canonical slug of an installed skill — a directory name under
  `.specify/skills/` that contains a `SKILL.md`.
- The list MUST contain at least one slug.
- The list MUST NOT contain any non-declarable skill: `sdd-workflow`, `create-agent`,
  `improve-agent`, `create-skills`, `improve-skills`, `organize-agents`.
- Adding `skills` MUST NOT remove, reorder, or alter any existing frontmatter key
  (`name`, `description`, `user-invocable`, `disable-model-invocation`, `supervisor`,
  `role-scope`, `model`, `tools`, `maxTurns`, `color`).

The authoritative per-agent lists are defined in [../data-model.md](../data-model.md)
§ Agent–Skill Mapping.

## C-2 — `## Skill Enablement` body section

Each built-in agent definition MUST contain exactly one `## Skill Enablement` section.

The section MUST contain, in order:

1. A shared protocol paragraph, identical across all agents, stating:
   - Skills and agent definitions install together, so every declared skill is invocable.
   - The agent MUST prefer an applicable framework skill over performing the operation
     manually or ad-hoc.
   - When more than one skill applies, the agent MUST choose the most role-specific one.
   - When no relevant skill applies, or a relevant skill is unavailable or fails, the agent
     MUST complete the operation directly and surface the failure.
   - The agent MUST invoke the skill rather than reimplementing its logic inline.
2. A per-role table with columns `| Skill | When to use |`, one row per declared skill,
   whose skill set is identical to the `skills` frontmatter list.

The shared protocol text MUST have a single source of truth at
`skills/create-agent/templates/agent-skill-enablement.md` and MUST be composed into agents
rather than independently reworded.

## C-3 — Generator template parity

For each preset role, `skills/create-agent/templates/agent-role-<role>-template.md` MUST be
updated to include the same `skills` frontmatter field and `## Skill Enablement` section as
its shipped counterpart, so that a regenerated agent is byte-consistent in structure with the
shipped agent (no regression per FR-011).

## C-4 — Non-declarable skill exclusion

The union of all declared skills across all agents MUST be a subset of the installed skills
minus the non-declarable set defined in C-1. A reference-only or meta skill appearing in any
agent's `skills` list is a contract violation.

## C-5 — Validation test

A contract test at `tests/contract/test_agent_skill_enablement.py` (pytest marker `contract`)
MUST assert, for each of the seven preset agents:

- **T-1**: frontmatter contains a `skills:` key.
- **T-2**: the parsed `skills` list is non-empty.
- **T-3**: every slug resolves to an existing `.specify/skills/<slug>/SKILL.md` (equivalently,
  the shipped `skills/<slug>/SKILL.md`).
- **T-4**: no slug is a member of the non-declarable set.
- **T-5**: the agent body contains a `## Skill Enablement` heading.

The test MUST fail before the agent edits are applied and pass afterward.

## Non-Goals

- No new skills are authored (FR: "No new skills required").
- No changes to CLI runtime code in `src/specify_cli/`.
- No change to supervision/EEI loop behavior, tool lists, role scope, or the per-file symlink
  install model.
- Transient EEI stage sub-agents are not edited; they inherit the parent role's skills.

## Requirements Traceability

| Contract | Requirements | Success Criteria |
|----------|--------------|------------------|
| C-1 | FR-002, FR-004, FR-005, FR-006, FR-009 | SC-001, SC-002 |
| C-2 | FR-003, FR-007, FR-008, FR-010, FR-012 | SC-003, SC-005 |
| C-3 | FR-009, FR-011 | SC-004 |
| C-4 | FR-004, FR-005 | SC-002 |
| C-5 | FR-005 | SC-001, SC-002 |
