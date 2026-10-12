<!-- AUTO-GENERATED from templates/commands/skills.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
> `/speckit.skills` is the orchestration entrypoint for Skill management. It delegates to `create-skills` (new) or `improve-skills` (existing, with a mandatory spec-compliance modernization pass first); it never authors or edits a Skill inline.

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Extract target Skill name (concise command-like identifier: letters, digits, hyphens, underscores).

## Delegation

### Routing

1. **Parse the target Skill** — use the name the user gave; if empty, infer from the conversation or ask one targeted question.
2. **Check existence** — canonical source `.specify/skills/<name>/SKILL.md`.
3. **Route** on the result:

| Condition | Skill | Runtime path |
|-----------|-------|--------------|
| NOT exists | `create-skills` | `.specify/skills/create-skills/SKILL.md` |
| EXISTS | `improve-skills` | `.specify/skills/improve-skills/SKILL.md` |

### `create-skills` — new Skill

- **Input**: the parsed Skill name + capability description (or empty — the skill then distills from conversation history).
- **What it owns**: the full creation workflow — runtime-mode detection, scaffolding (start from `.specify/templates/skills-template.md`), frontmatter and `${SKILL_HOME}`/`${SKILL_WORKDIR}` path conventions, identity finalization (`skill_id`), validation, pressure test, and the built-in agent propagation (Skill Enablement) with its guard/analyze/match/apply invariants.
- **Output**: a new `.specify/skills/<name>/SKILL.md` (+ optional `.specify/scripts/`, `references/`, `assets/`) and the skill's completion report (paths, `skill_id`, propagated agents, validation results).

### `improve-skills` — existing Skill (two-phase pass)

- **Phase A — spec-compliance modernization (mandatory before any optimization)**: run the compliance pass against the rules `improve-skills` owns — canonical path, directory structure, frontmatter, path conventions, legacy idiom migration (`./X` → `${SKILL_HOME}/X`, `${SKILL_ROOT}/X` → `${SKILL_HOME}/X`), discoverability, hygiene. The rules are the skill's truth source; apply them there, do not restate them here.
- **Phase B — user-requested refinement**: standard `improve-skills` workflow.
- **Input**: target Skill identity (name / `skill_id` / canonical path) + optimization direction.
- **Output**: the updated Skill package with `improve-skills`' final-check verdicts (shape gate, red-line gate, contract suite).

For detailed path conventions (`${SKILL_HOME}` / `${SKILL_WORKDIR}` semantics, computation idioms, nested invocations), see `.specify/skills/create-skills/SKILL.md`. For agent-specific operational guidance, see `.specify/shared/workflow/agent-configuration.md`.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.skills" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**After**: Run `/speckit.instructions` to update discovery metadata.