# Feature Detail: CLI Interface

**Feature ID**: 015  
**Name**: CLI Interface  
**Description**: Typer/Rich CLI for initialization, checks, versions, agent rendering, and migration.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

The `specify` console entry point provides project initialization, environment checks, text or JSON version output, host-agent rendering, and workspace migration. Typer and Rich provide the terminal interface, with machine-readable output where automation requires it.

## Latest Review

2026-11-22 implementation audit: recent hardening includes Rich markup escaping, safe TOML command rendering, explicit frontmatter-body separation, Windows UTF-8 stream handling, and a closed JSON version record. The former text described only a generic Rich interface.

## Key Changes

1. Expose init, check, version, render-agents, and migrate through the `specify` entry point.
2. Support deterministic JSON output and safe command rendering for automation.
3. Escape Rich markup and handle Windows UTF-8 output without corrupting user text.
4. Preserve packaged resource and build configuration through `pyproject.toml` and Hatch.

## Implementation Notes

- Primary sources: `src/specify_cli/__init__.py` and `pyproject.toml`.
- Current unit tests cover version JSON, frontmatter, TOML rendering, markup escaping, and UTF-8 streams.

## Future Evolution Suggestions

- Keep machine-output schemas and terminal escaping covered whenever a CLI surface changes.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/015-cli-interface.md`
- Implementation: `src/specify_cli/__init__.py`, `pyproject.toml`
- Specification: none registered for this legacy row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: CLI surfaces delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
