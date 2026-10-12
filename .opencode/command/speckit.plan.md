<!-- AUTO-GENERATED from templates/commands/plan.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

You **MUST** analyze the user input in `$ARGUMENTS`, infer the user's intent, and use that intent to supplement missing context and guide the planning process.

The user input may include:

1. Special requests that require extra care or custom handling during the planning workflow.
2. Supplemental information that provides additional context or reference material.
3. Specific planning constraints, architectural preferences, or technical requirements that go beyond the default scope described in this document.

When processing the user input:

1. You **MUST** treat `$ARGUMENTS` as parameters for the current command.
2. Do **NOT** treat the input as a standalone instruction that overrides or replaces the command workflow.
3. If the input contains clear ambiguity, confusion, or likely misspellings that materially affect interpretation, stop and ask the user to rephrase the request with clearer wording. Provide brief guidance when possible.

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`, ambient via the Documentation Map) and apply the protocol in `.specify/shared/workflow/glossary.md`:

- **Before acting on the user input**, map any recorded homophone/confusable variant to its canonical term (correcting voice/dictated input); surface each correction so the user can override it, and defer to the user on ambiguous variants.
- **At wrap-up**, propose any new project-specific terms (`origin=auto`, `status=proposed`), excluding common words; run conflict detection; non-conflicting new terms MUST be written directly and merged into the wrap-up report (non-blocking); only writes that conflict with or overwrite an existing user entry MUST still pause for user confirmation. User-authored entries are authoritative.

## Skill Delegation

The executable core of this command is the **`create-plan`** skill (`.specify/skills/internal/create-plan/SKILL.md`): it turns a validated requirements spec into the implementation planning artifact set and advances the feature tracking system. This template keeps entry, user input, glossary, and the wrap-up lifecycle only.

- **Inputs**: `$ARGUMENTS` as processed above (background / planning outline / specific constraints); setup variables FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH from the `.specify/scripts/bash/create-new-plan.sh --json` prerequisite run (frontmatter `scripts:`), all paths absolute; a `requirements.md` free of unresolved `[NEEDS CLARIFICATION]` markers.
- **How to call**: read the skill and follow its Outline steps 1–5 — setup; user-input classification (mid-run addenda land upstream in `requirements.md` first, with its checklist re-validated once); context load (spec + constitution + `research.md` + existing docs + feature memory); in-place template fill with the dynamically derived Constitution Check table (same-author scoring delegated to fresh-context read-only subagents) and Phase 0 research review; Phase 1 design artifacts (`data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`); the Post-Generation Quality Gate (deliberation-marker cleanup; execution-verify every emitted command example); the plan integrity gate; and Feature Integration (`Draft → Planned`; never `Implemented` — that transition is owned by `/speckit.implement`).
- **Outputs**: the filled `plan.md` (no residual placeholders, exactly one `# Implementation Plan:` heading, the Requirement → Feature stamp), the Phase 1 artifact set, and the updated feature index + feature detail entry.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.plan" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Artifact Commit

At wrap-up, **before** the Feedback and Documentation steps, commit the artifact this command produced — and only that artifact, staged by explicit path. Follow the canonical convention in `.specify/shared/workflow/artifact-commit-step.md`: run the deletion-surface audit first, use a single-line message per `.specify/templates/commit-template.md`, never `git add -A`, and never fold another command's uncommitted artifacts into this commit (report that as an upstream deviation instead). A read-only run that produced no artifact skips this step and says so in one line rather than creating an empty commit. Committing here does not advance the feature's lifecycle status and does not push.

## Handoffs

**Before running this command**:

- Ensure `/speckit.requirements` has produced a requirements specification.
- If `requirements.md` contains any `[NEEDS CLARIFICATION]`, run `/speckit.clarify` first.

**After running this command**:

- Typically run `/speckit.tasks` to decompose the plan into an executable task list.
- Optionally run `/speckit.checklist` to introduce domain-specific quality gates before implementation.