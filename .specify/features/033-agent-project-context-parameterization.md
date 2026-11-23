# Feature Detail: Agent Project Context Parameterization

**Feature ID**: 033  
**Name**: Agent Project Context Parameterization  
**Description**: Render Worker capability Project Context from target-project facts instead of leaving placeholders unresolved.
**Status**: Draft  
**Created**: 2026-07-21  
**Last Updated**: 2026-11-22

## Overview

The seven Worker capability templates now contain `{{PROJECT_NAME}}`, `{{TECH_STACK}}`, `{{SPECS_DIR}}`, and related placeholders, and the generic agent renderer exists. The remaining gap is that init/render only rewrites paths and copies body text: it does not detect the target project, substitute those placeholders, or refresh only `## Project Context` while preserving edits elsewhere.

## Latest Review

2026-11-22 implementation audit: the earlier claim that templates still hard-code Spec Kit facts is outdated. Parameterized template text is delivered; target-project detection, placeholder resolution, and segment-level non-destructive refresh are not. `Draft` remains appropriate for the unfinished core behavior, but the record now distinguishes the delivered template work from the missing installer behavior.

## Key Changes (planned)

1. Add explicit section-boundary markers (or a stable heading convention) around `## Project Context` in the 7 role agent templates so the installer can rewrite exactly that section.
2. Extend the init/refresh flow (`copy_local_templates()` / instructions generation) to render Project Context from detected target-project facts: project name, tech stack (reuse `detect_tech_stack`), existing specs (scan `.specify/specs/`), doc map pointers.
3. Non-destructive refresh: re-running init updates only the Project Context section and never touches user edits in other sections.
4. Acceptance evidence: init on a non-spec-kit project yields agents whose Project Context names that project; re-init preserves hand-edited sections; detection-failure fallback produces a clearly marked placeholder rather than spec-kit facts.

## Implementation Notes

- Current templates live at `skills/internal/create-agent/templates/agent-capacity-*-template.md` and already carry project placeholders.
- `src/specify_cli/__init__.py` provides the shared renderer but currently leaves those placeholders unresolved; do not mistake template parameterization for target-project rendering.
- A future implementation must update only `## Project Context` and preserve user edits outside that section.
- Detection failure must never silently substitute Spec Kit's own project facts.

## Future Evolution Suggestions

- Extend parameterization to other project-coupled agent content discovered during future rollouts (e.g., default verification commands per tech stack).
- Let `/speckit.agents` regenerate or hand-edit Project Context for project-custom agents created after init.
- Feed drift between detected facts and the rendered section into the feedback mechanism (028) to tune detection precedence.

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/033-agent-project-context-parameterization.md
- Installer copy logic: src/specify_cli/__init__.py (`copy_local_templates()`)
- Detection helper: src/specify_cli/__init__.py (`detect_tech_stack`)
- Motivating rollout: shared/workflow/interview-walkthrough.md; reference case (project-internal): draft/case-study/01-interview-driven-ui-refactor.md

## Status Tracking

- **Draft**: Feature row first added to `.specify/memory/features.md`. *(current state)*
- **Planned**: `plan.md` (and any design artifacts) exist for the bound spec; Constitution Check has no unjustified Fail rows.
- **Implemented**: `tasks.md` has zero `[ ]` rows AND `verification.md` records a pass/deferred status for every Success Criterion.
- **Ready for Review**: All deferred tasks resolved/waived and review evidence produced.
- **Completed**: Final acceptance / merged.

## Related Specifications/Requirements

- None yet — create via `/speckit.requirements` when this feature is picked up.

## Cross-References

- **Feature 044 Agent Metadata Portability** (registered 2026-08-13 via requirement 040): complementary layer, not a dependency. 044 owns the neutral-metadata + per-tool render/distribution pipeline at init/refresh time; 033's body-side `## Project Context` parameterization is designed to ride on that same render path once it exists. When both land, the two render passes (metadata translation / body Project Context rewrite) must compose on the same refresh semantics (non-destructive, user-edits-preserving).
