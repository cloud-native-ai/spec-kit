# Feature Detail: Prompt Template Quality

**Feature ID**: 023  
**Name**: Prompt Template Quality  
**Description**: Structural validation and consistency enforcement across all command and skill templates.  
**Status**: Draft  
**Created**: 2026-06-05  
**Last Updated**: 2026-11-22

## Overview

Spec Kit's primary artifacts are Markdown prompt templates that drive AI agent behavior. This feature tracks a unified structural schema and author guidance for command, skill, and agent templates. The current repository already has several narrower validators, but they do not yet form the unified contract originally envisioned here.

## Latest Review

2026-11-22 implementation audit: partial delivery exists through command `short-description` checks, role-template frontmatter and section checks, Agent metadata schema validation, and deterministic `skill-shape.py` validation. A unified all-template schema, complete handoff rules, and one authoring guide remain open. `Draft` is retained for that remaining unified scope; the earlier claim that no automated validation exists is false.

## Key Changes

1. Delivered: validate Qoder command descriptions, role-template frontmatter and required sections, Agent metadata, and skill shape through existing contract surfaces.
2. Remaining: define one structural schema for all command, skill, and agent templates, including placeholder and handoff conventions.
3. Remaining: make the unified schema and contributor authoring guide the single owner rather than distributing rules across unrelated features.
4. Remaining: run the complete unified validation set on every relevant change.

## Implementation Notes

- Templates are the product — their quality is equivalent to code quality in a traditional project.
- Validation should be schema-based (checking structure) rather than content-based (checking prose quality).
- The existing `tests/contract/` pattern is the right home for template validation tests.
- Must not block AI agent creativity in template content; only enforce structural consistency.

## Future Evolution Suggestions

- Add a template linting step to the skill creation workflow (`create-skills`).
- Consider versioning template schemas so older templates can be incrementally migrated.
- Expose validation as a sub-function of `/speckit.checklist` for self-service quality checks.

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/023-prompt-template-quality.md

## Status Tracking

- **Draft**: Gap identified; no formal template schema exists.
- **Planned**: Schema defined and template authoring guide drafted.
- **Implemented**: Contract tests validate all templates against schemas.
- **Ready for Review**: All existing templates pass validation; guide reviewed.
- **Completed**: Template quality is continuously enforced via automated checks.
