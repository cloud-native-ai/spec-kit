# Contract: Feedback-Step Convention (Skills & Complex Commands)

**Feature**: 028 Feedback Mechanism | **Type**: Authoring convention contract

Defines the normative `## Feedback` step that qualifying units MUST carry, and how it executes at wrap-up. This is the "embedded by convention" surface (FR-002, FR-010).

## Where the step lives

- **Skills**: Every `SKILL.md` MUST contain a `## Feedback` section (the last workflow section). `templates/skills-template.md` carries it so new skills inherit it by default. A skill without it is **non-conformant** (FR-002); `create-skills` validation MUST fail such a skill, and `improve-skills` MUST offer to repair it.
- **Complex commands**: Each of the 13 complex command templates (see `command-classification.md`) MUST carry the feedback step **at the existing wrap-up / Git-commit-prompt stage** (e.g. next to `## Optional: Git Commit`), NOT mid-flow (FR-004).
- **Simple commands**: MUST NOT carry the step (FR-006, FR-007).

## Canonical step text (normative content)

The step instructs the executing agent to, at wrap-up:

1. **Gate on qualification & completion.** Only run for a qualifying unit that reached wrap-up. If the run was trivial/aborted, follow the abort rule below.
2. **Reflect (agent self-reflection — no user input).** Review the just-completed run against the unit's declared purpose/description and produce: a short review + ≥1 concrete, unit-specific optimization point (or the explicit no-op sentence). MUST NOT solicit feedback content from the user (FR-012).
3. **Scope guard.** Keep strictly to the current operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job) (FR-005).
4. **Dedup guard.** Use a stable `run_id` for this run. If a parent flow already recorded feedback for this same unit+run, skip (FR-008).
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "<skill:NAME | /speckit.COMMAND>" --unit-type "<skill|command>" \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file or heredoc>"
   ```
6. **Consolidated submission prompt.** Read the `should_prompt` field returned by `record` (or call `--action status`). When `true`, surface a single consolidated notification inviting the user to submit collected feedback to the Spec Kit developers; on user confirmation, run `--action mark-submitted`. Below threshold, DO NOT prompt (FR-011, SC-007).

## Abort / partial-run rule

If the run failed or was interrupted before wrap-up, the step MUST either skip recording OR record with `--partial` and a review labeled as covering a partial run — never present a partial run as a complete review (FR-009).

## Nesting rule

When a command invokes a skill (or a skill invokes a skill), each qualifying unit records feedback for **its own** scope only, keyed by its own `(unit_id, run_id)`. The same unit+run MUST NOT be recorded twice (FR-008, SC-005).

## Conformance checks (for tests)

- Every `skills/*/SKILL.md` contains a `## Feedback` section → contract test.
- `templates/skills-template.md` contains the `## Feedback` section.
- Each complex command template contains the feedback step; each simple command template does NOT → contract test driven by `command-classification.md`.
- The engine `record` path produces an entry matching `feedback-entry-schema.md`.
