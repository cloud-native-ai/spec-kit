---
name: improve-team
description: Adjust and optimize an existing agent team — add/remove members, change the collaboration pattern, tune thresholds/parallelism/quality dimensions — with targeted, evidence-based, structure-preserving edits. Use when the user mentions ["调整团队", "优化团队", "优化 team", "修改团队", "improve team", "adjust team", "refine team", "tune team", "给团队增加", "给团队减少"]
skill_id: "<SKILL:.specify/skills/improve-team/SKILL.md>"
---

# improve-team

## Goal

Adjust and optimize an **existing** agent team. `improve-team` is the team-domain analogue of `improve-agent`, completing the create → improve lifecycle for teams. It loads a persisted team, makes **targeted, evidence-based, structure-preserving** edits (never a broad rewrite), re-persists the team, and reports what changed and why. The multi-agent Conceptual Model it operates against is defined once in `../create-team/references/conceptual-model.md`.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| target team | yes | Slug/name resolving to `.specify/teams/<slug>.team.md`. |
| improvement direction | yes | What to change: add/remove member, change pattern, tune thresholds/parallelism/dimensions. |
| evidence | recommended | Concrete signals: run reports, non-convergence, oscillating scores, territory conflicts, stale member references. |

## Behavior

1. **Resolve target** — load the `.team.md` from `.specify/teams/<slug>.team.md`. If none exists → report **"team not found"** and offer to **create** one (hand off to `create-team` via `/speckit.team create`). Never silently create a team.
2. **Gather evidence** — inspect run history, convergence/oscillation, territory conflicts, and stale/broken member references before proposing changes.
3. **Attribute root cause** — map each issue to the responsible part (roster, pattern, config/thresholds, member territories/DAG).
4. **Apply targeted edits** — make the **minimal, evidence-based** change that fixes the issue while **preserving the parts of the team that already work** (SC-005). Do not touch unaffected fields — they must remain byte-identical.
5. **Re-persist** — write the updated `.team.md` and **bump the `updated` date**; leave `created` and all unaffected frontmatter/members untouched.
6. **Report** — list each change and the evidence that motivated it, and recommend a `run` to validate.

## Refinement Map (examples)

| Symptom | Likely cause | Team edit |
|---------|--------------|-----------|
| Team-loop never converges | Threshold too high or conflicting dimensions | Lower threshold / rebalance `quality_dimensions` weights |
| Score oscillates | Ambiguous evaluator criteria | Tighten the evaluator rubric (via the moved stage templates in `create-team/templates/`) |
| Parallel file conflicts | Overlapping territories | Repartition `territories`; move shared files to forbidden-write |
| Serial stage stalls | Broken/missing handoff dependency | Fix `blockedBy` edges / handoff file path |
| Stale member | Agent renamed/deleted | Repoint or remove the member; surface the broken reference |
| Missing a role (e.g. no QA gate) | Roster gap | Add a member (e.g. a `qa-engineer`) without altering existing members |

## MUST / MUST NOT

- MUST operate only on an **existing** persisted team; MUST NOT silently create one (on miss, report "team not found" and offer to create).
- MUST make **targeted, evidence-based, structure-preserving** edits — no broad rewrites; unaffected fields stay byte-identical.
- MUST bump the `updated` date on every successful edit.
- MUST NOT modify single agents (that is `improve-agent`'s domain) beyond team-membership references.

## Outputs

- An updated `.specify/teams/<slug>.team.md` (with a bumped `updated` date) and a change report listing each edit and its motivating evidence.

## Feedback

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/skills/sdd-workflow/references/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:improve-team" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
