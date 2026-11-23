# Feature Detail: Code Quality Tooling

**Feature ID**: 035  
**Name**: Code Quality Tooling  
**Description**: Python linting, formatting, and type checking configuration for consistent codebase maintenance.  
**Status**: Draft  
**Created**: 2026-07-22  
**Last Updated**: 2026-11-22

## Overview

The project now has a development-only Ruff gate over `src`, `scripts`, and `skills`, targeted at Python 3.8 and limited to the S602/S604/S605 shell-security rules. Contract tests prove both that the current tree passes and that seeded violations are rejected. Formatting, mypy/pyright type checking, canonical-runner integration, and CI enforcement remain undelivered.

## Latest Review

2026-11-22 implementation audit: the earlier “no linter configuration” premise is false. The delivered scope is a local security lint gate, not the full linting/formatting/type-checking feature. `Draft` is retained for the remaining scope and no CI claim is made because Feature 034 still has no workflow implementation.

## Key Changes

1. Delivered: add dev-only Ruff configuration and the three-rule shell-security gate to `pyproject.toml`.
2. Delivered: add positive and seeded-negative contract coverage in `tests/contract/test_lint_gate.py`.
3. Remaining: decide and implement formatting and type-checking scope.
4. Remaining: integrate the quality gate with the canonical runner and a real CI pipeline.

## Implementation Notes

- The project targets Python 3.8+, so tooling must support that baseline.
- `ruff` is the preferred tool (fast, replaces flake8/black/isort in a single tool).
- Initial configuration should be lenient (avoid mass reformatting of existing code).

## Future Evolution Suggestions

- Add pre-commit hooks for local enforcement.
- Consider adding `pyupgrade` for Python version modernization.
- Add type stubs for public API surfaces.

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/035-code-quality-tooling.md

## Status Tracking

- **Draft**: Gap identified and feature registered. (current)
- **Planned**: Tool selection and configuration scope approved.
- **Implemented**: Linter/formatter configured and passing on existing codebase.
- **Ready for Review**: CI gate enforced; no new violations introduced.
- **Completed**: Codebase fully compliant with configured rules.
