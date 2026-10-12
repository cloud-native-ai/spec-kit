<!-- AUTO-GENERATED from templates/commands/research.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

You **MUST** analyze the user input in `$ARGUMENTS`, infer the user's intent, and use that intent to supplement missing context and guide the research process.

The user input may include:

1. Special requests that require extra care or custom handling during the research workflow.
2. Supplemental information that provides additional context or reference material.
3. Specific research questions, technical uncertainties, or exploration areas that go beyond the default scope described in this document.

When processing the user input:

1. You **MUST** treat `$ARGUMENTS` as parameters for the current command.
2. Do **NOT** treat the input as a standalone instruction that overrides or replaces the command workflow.
3. If the input contains clear ambiguity, confusion, or likely misspellings that materially affect interpretation, stop and ask the user to rephrase the request with clearer wording. Provide brief guidance when possible.

## Delegation

Conduct the in-depth research and analysis that backs the implementation plan — resolve the documentation inventory, load spec + constitution + relevant project docs and feature memory, resolve every unknown, and land the findings as structured Decisions & Rationale. The entire executable flow (setup, context loading, analysis, `research.md` generation, and the research output structure) is delegated to one internal skill; this command keeps entry, the `scripts:` block, the User Input Protocol, and the wrap-up lifecycle only.

- **Skill**: `research-feature` — runtime path `.specify/skills/internal/research-feature/SKILL.md`.
- **Inputs**: setup variables (`FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`, `AVAILABLE_DOCS`) from the frontmatter `scripts:` run (`.specify/scripts/bash/research-project.sh --json`, executed by the skill from repo root); `$ARGUMENTS` research questions, supplemental reference material, and special-handling requests (wired by `## User Input` above).
- **Outputs**: `SPECS_DIR/research.md` — created or incrementally appended (merge-only: never overwrite existing valid research), structured as Project Context Analysis / References / Decisions & Rationale / Open Questions & Risks; the skill reports the generated path and the key findings.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.research" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before running this command**:

- Run when the plan/spec has open questions that require evidence or repo context confirmation.

**After running this command**:

- Proceed to `/speckit.plan` (or re-run it) to encode research decisions into the technical plan.