# Feature Detail: Implement Command

**Feature ID**: 007  
**Name**: Implement Command  
**Description**: Execute implementation tasks with evidence-backed closure.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.implement` executes `tasks.md` in dependency order, applies the declared test mode, verifies each task with fresh evidence, revalidates the Completion Gate, and computes a deterministic closure verdict before claiming implementation.

## Latest Review

2026-11-22 implementation audit: the current command is an evidence-driven execution flow, not a simple code generator. Only an `accept` closure verdict can support an `Implemented` claim; final-path failures produce an honest blocked outcome.

## Key Changes

1. Parse and execute tasks by dependency and phase with test-driven development where required.
2. Close tasks only through identify, run, read, verify, and claim evidence.
3. Revalidate the Completion Gate and use `closure-acceptance-check.py` for the final verdict.

## Implementation Notes

- Primary surfaces: `templates/commands/implement.md`, `skills/internal/implement-feature/SKILL.md`, and `scripts/python/closure-acceptance-check.py`.
- Current acceptance tests pin final-path, smoke, and closure behavior.

## Future Evolution Suggestions

- Preserve deterministic evidence and closure semantics as execution carriers evolve.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/007-implement-command.md`
- Implementation: `templates/commands/implement.md`, `skills/internal/implement-feature/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Implementation workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
