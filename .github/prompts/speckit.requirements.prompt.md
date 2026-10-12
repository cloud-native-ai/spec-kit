<!-- AUTO-GENERATED from templates/commands/requirements.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). The text after `/speckit.requirements` IS the feature description.

## Glossary

Apply the glossary protocol in `.specify/shared/workflow/glossary.md`, reading the project glossary at `.specify/memory/glossary.md` (ambient via the Documentation Map). That file owns every rule of this step and this section restates none of them: input correction and anchoring, **including the constraint-side reading of a registered term** (§1); progressive enrichment at wrap-up (§2); conflict detection and which writes proceed directly (§3); manual edits and user precedence (§4).

## Delegation

Create or update the feature's Requirements from the feature description — branch-numbered, house-convention-aligned, deterministic-checker-validated. The entire executable flow is delegated to one internal skill; this command keeps entry, input wiring, 
```bash
cat << 'EOF' | .specify/scripts/bash/create-new-requirements.sh --json --short-name "<SHORT_NAME>"
$ARGUMENTS
EOF
```
, and the wrap-up lifecycle only.

- **Skill**: `create-requirements` — runtime path `.specify/skills/internal/create-requirements/SKILL.md`.
- **Inputs**: the feature description (this command's `$ARGUMENTS`, wired by `## User Input` above); the scaffold script from the frontmatter `scripts:` slot, run by the skill from repo root (`BRANCH_NAME`, `SPEC_FILE` parsed from its JSON); glossary anchoring runs first inside the skill.
- **Outputs**: `requirements.md` at the skill-resolved SPEC_FILE (`Related Feature` initialized to "Need clarification"), the quality checklist at `FEATURE_DIR/checklists/requirements.md`, and the report (branch name, spec file path, checklist results, next phase readiness).

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.requirements" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Artifact Commit

At wrap-up, **before** the Feedback and Documentation steps, commit the artifact this command produced — and only that artifact, staged by explicit path. Follow the canonical convention in `.specify/shared/workflow/artifact-commit-step.md`: run the deletion-surface audit first, use a single-line message per `.specify/templates/commit-template.md`, never `git add -A`, and never fold another command's uncommitted artifacts into this commit (report that as an upstream deviation instead). A read-only run that produced no artifact skips this step and says so in one line rather than creating an empty commit. Committing here does not advance the feature's lifecycle status and does not push.

## Handoffs

**Before**: Optional `/speckit.feature` to ensure feature registry is up to date — **recommended whenever `.specify/memory/features.md` is absent or still a placeholder**, otherwise `/speckit.clarify` has to bootstrap the registry mid-run while binding the Feature.

**After**: If spec has `[NEEDS CLARIFICATION]` or `Related Feature: Need clarification` → `/speckit.clarify`. Otherwise → `/speckit.plan`.