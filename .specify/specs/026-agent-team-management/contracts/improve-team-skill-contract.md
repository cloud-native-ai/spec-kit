# Contract: `improve-team` Skill

**Feature**: 027 Team Management | **Spec**: [requirements.md](../requirements.md)

`improve-team` is a new skill (FR-008) that adjusts and optimizes an **existing** team. It is the team-domain analogue of `improve-agent`, completing the create → improve lifecycle for teams (FR-014).

## Identity

- **Skill dir**: `skills/improve-team/` (mirrored to `.specify/skills/improve-team/`).
- **Frontmatter**: `name: improve-team`; `skill_id: "<SKILL:.specify/skills/improve-team/SKILL.md>"`; `description` with trigger phrases ("调整团队", "优化 team", "improve/adjust team", "refine team").
- **Non-declarable**: like other meta/authoring skills, `improve-team` is added to the non-declarable set (never appears in a role agent's `skills:` list).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| target team | yes | Slug/name resolving to `.specify/teams/<slug>/team.md`. |
| improvement direction | yes | What to change: add/remove member, change pattern, tune thresholds/parallelism/dimensions. |
| evidence | recommended | Concrete signals: run reports, non-convergence, oscillating scores, territory conflicts. |

## Behavior

1. **Resolve target** — load the `team.md`. If none exists → report "team not found" and offer to create one (FR-010).
2. **Gather evidence** — run history, convergence/oscillation, territory conflicts, stale/broken member references.
3. **Attribute root cause** — map each issue to the responsible part (roster, pattern, config/thresholds, member territories/DAG).
4. **Apply targeted edits** — minimal, evidence-based changes that preserve the parts of the team that work (SC-005). Re-persist the `team.md`; update `updated` date.
5. **Report** — list each change and the evidence that motivated it; recommend a `run` to validate.

## Refinement map (examples)

| Symptom | Likely cause | Team edit |
|---------|--------------|-----------|
| Team-loop never converges | Threshold too high or conflicting dimensions | Lower threshold / rebalance `quality_dimensions` weights |
| Score oscillates | Ambiguous evaluator criteria | Tighten evaluator rubric (via the moved stage templates) |
| Parallel file conflicts | Overlapping territories | Repartition `territories`; move shared files to forbidden-write |
| Serial stage stalls | Broken/missing handoff dependency | Fix `blockedBy` edges / handoff file path |
| Stale member | Agent renamed/deleted | Repoint or remove the member; surface the broken reference |

## MUST / MUST NOT

- MUST operate only on an existing persisted team; MUST NOT silently create one.
- MUST make targeted, evidence-based, structure-preserving edits (no broad rewrites).
- MUST NOT modify single agents (that is `improve-agent`'s domain) beyond team membership references.
