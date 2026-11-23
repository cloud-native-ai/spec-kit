# Feature Detail: Configuration Management

**Feature ID**: 018  
**Name**: Configuration Management  
**Description**: Manage package, dependency, build, pytest, and Ruff configuration through pyproject.toml.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`pyproject.toml` is the packaging and development-configuration owner for `specify-cli`: project metadata, runtime and development dependencies, the console entry point, Hatch build resources, pytest markers, and the local Ruff security gate.

## Latest Review

2026-11-22 implementation audit: the current dependency set no longer includes `platformdirs`; Hatch includes framework assets and a custom source-provenance hook, while Ruff is development-only and limited to shell-security rules. This is not a runtime configuration reader for client projects.

## Key Changes

1. Declare package metadata, Python compatibility, dependencies, and the `specify` entry point.
2. Configure Hatch build hooks and wheel inclusion for CLI, memory, scripts, templates, agents, and shared assets.
3. Declare pytest markers and the canonical runner's parallel, serial, and slow-test selection inputs.
4. Configure the development-only Ruff S602/S604/S605 security gate and distribution exclusions.

## Implementation Notes

- Primary source: `pyproject.toml`; build behavior also uses `src/hatch_build.py`.
- Distribution, build-hook, and lint-guard behavior is covered by current contract tests.

## Future Evolution Suggestions

- Keep runtime dependencies minimal and development-only tooling outside the shipping boundary.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/018-configuration-management.md`
- Implementation: `pyproject.toml`, `src/hatch_build.py`
- Specification: none registered for this legacy row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Packaging and development configuration delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
