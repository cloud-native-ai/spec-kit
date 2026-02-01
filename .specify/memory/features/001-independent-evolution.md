# Feature Detail: Independent Evolution & Legacy Cleanup

**Feature ID**: 001
**Name**: Independent Evolution & Legacy Cleanup
**Description**: Transition project to independent evolution mode by removing upstream legacy AI tools and dependencies.
**Status**: Implemented
**Created**: 2026-01-30
**Last Updated**: 2026-01-30

## Overview

The project is moving away from upstream tracking to evolve independently. We are removing support for all legacy upstream AI providers, retaining only GitHub Copilot, Qwen Code, and opencode. This ensures a cleaner codebase focused on our target tools.

## Latest Review

Tasks generated. Ready for execution.

## Key Changes

1. Remove all AI provider implementations except GitHub Copilot, Qwen Code, and opencode.
2. Update configuration parsing to reject unsupported providers.
3. Clean up legacy documentation and comments referencing upstream tools.

## Implementation Notes

- Ensure \`opencode\` support is preserved as it is a specific requirement.
- Verify \`GitHub Copilot\` and \`Qwen Code\` functionality remains intact.
- **Plan Note**: \`AGENT_CONFIG\` schema in \`__init__.py\` will be strictly limited to the 3 supported tools. All other templates in \`templates/commands/\` will be removed.
- **Task Note**: Implementation split into Configuration Cleanup (Phase 2), Logic Removal (Phase 3), and Documentation Update (Phase 4).

## Future Evolution Suggestions

- Re-evaluate the need for abstraction layers if we only support 3 specific tools.

## Related Files

- Specification: .specify/specs/001-cleanup-ai-support/spec.md
- Plan: .specify/specs/001-cleanup-ai-support/plan.md
- Tasks: .specify/specs/001-cleanup-ai-support/tasks.md
- Feature Index: memory/features.md
- Feature Detail: memory/features/001-independent-evolution.md

## Status Tracking

- **Draft**: Feature defined, spec in progress.
- **Planned**: Spec approved, implementation scheduled.
- **Implemented**: Code changes merged to feature branch.
- **Ready for Review**: PR open, tests passing.
- **Completed**: Merged to main, deployed.
