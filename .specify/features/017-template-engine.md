# Feature Detail: Template Engine

**Feature ID**: 017  
**Name**: Template Engine  
**Description**: Render Markdown templates and install packaged framework assets.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

The template engine parses command frontmatter and bodies, selects script blocks, substitutes script and agent placeholders, rewrites paths, and renders per-assistant command formats. Initialization also installs templates, scripts, skills, agents, and shared reference assets.

## Latest Review

2026-11-22 implementation audit: the current system includes safe frontmatter-body parsing, Qoder description metadata, TOML escaping, and generated AUTO-GENERATED markers. It is both a renderer and a packaged-asset installation pipeline.

## Key Changes

1. Parse frontmatter separately from Markdown bodies and render per-assistant command files.
2. Substitute script and agent placeholders and select the appropriate script blocks.
3. Install packaged framework assets and preserve assistant-specific directory layouts.
4. Guard generated output with frontmatter, TOML, Qoder metadata, and mirror contract tests.

## Implementation Notes

- Primary sources: `src/specify_cli/__init__.py`, `templates/`, and `scripts/python/regen-command-copies.py`.
- `.specify/` command and asset copies are generated projections, not independent source documents.

## Future Evolution Suggestions

- Keep rendering behavior deterministic as new assistant formats and asset classes are added.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/017-template-engine.md`
- Implementation: `src/specify_cli/__init__.py`, `templates/`
- Specification: none registered for this legacy row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Template rendering and asset installation delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
