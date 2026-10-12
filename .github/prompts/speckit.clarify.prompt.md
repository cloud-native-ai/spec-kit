<!-- AUTO-GENERATED from templates/commands/clarify.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Delegation

`/speckit.clarify` detects and reduces ambiguity or missing decision points in the current phase's primary artifact and records clarifications directly in that file. The operating mode (A post-requirements / B post-plan / C post-tasks) is auto-detected from file existence in `REQUIREMENTS_DIR`; `$ARGUMENTS` may explicitly override the target artifact.

**Load and follow** `.specify/skills/internal/clarify-artifact/SKILL.md`:

- **Inputs**: the JSON fields parsed from this command's declared prerequisite script, `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` (`REPO_ROOT`, `BRANCH`, `REQUIREMENT_ID`, `REQUIREMENTS_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, `TASKS`); `$ARGUMENTS` as explicit decisions to integrate first and/or a mode override; the active mode's taxonomy and integration rules (`.specify/shared/constants/clarify-taxonomy.md`).
- **Outputs**: the clarified target file (`requirements.md` / `plan.md` / `tasks.md`) — user-provided decisions integrated, a bounded closed-question loop run (max 5 questions, options table with consequence previews and a Recommended pick), answers validated under `## Clarifications` after each write; a report (operating mode + target path, questions asked & answered, sections touched, coverage summary). When the answer space is unbounded → escalate to `/speckit.interview`; when the user re-scopes after downstream artifacts exist → the skill's Scope Revision Protocol instead of a clarification run.

The skill owns the entire workflow: phase detection, the fail-fast writability probe, summary-first context loading, the taxonomy coverage scan (including same-author delegation), question generation and the interactive loop, integration and validation rules, and the behavior rules (never exceed 5 questions; respect early termination; do not modify upstream artifacts in later modes).

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.clarify" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Artifact Commit

At wrap-up, **before** the Feedback and Documentation steps, commit the artifact this command produced — and only that artifact, staged by explicit path. Follow the canonical convention in `.specify/shared/workflow/artifact-commit-step.md`: run the deletion-surface audit first, use a single-line message per `.specify/templates/commit-template.md`, never `git add -A`, and never fold another command's uncommitted artifacts into this commit (report that as an upstream deviation instead). A read-only run that produced no artifact skips this step and says so in one line rather than creating an empty commit. Committing here does not advance the feature's lifecycle status and does not push.

## Handoffs

**Before**: At minimum `/speckit.requirements` first. Phase auto-detected from file existence.

**After**: Mode A → `/speckit.plan`. Mode B → `/speckit.tasks`. Mode C → `/speckit.implement`.