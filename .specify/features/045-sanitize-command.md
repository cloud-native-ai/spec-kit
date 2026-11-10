# Feature Detail: Framework Source Provenance

**Feature ID**: 045  
**Name**: Framework Source Provenance  
**Description**: Record the framework's source commit identity (commit id as the sole version identifier — no formal version numbers) into target projects at `specify init`, enabling reverse lookup of the exact framework code slice that produced a project's `.specify/` scaffolding.  
**Status**: Implemented  
**Created**: 2026-08-17  
**Last Updated**: 2026-08-17 (implemented)

## Overview

`specify init` scaffolds a `.specify/` workspace into a target project but leaves no record of which framework source produced it. This feature adds a **source stamp**: init writes the framework's git commit id into the target project (default `.specify/source.json`), so anyone holding the target project can answer "which framework commit built this?" with `git show <commit>` in the framework repo.

## Axis Distinction (why not Feature 024)

- **This Feature (045) — source/provenance axis**: *which framework source* produced the artifacts; identifier = git commit id; written by init.
- **Feature 024 (Specification Workspace Versioning, Draft) — schema axis**: *which workspace structure version* the project carries; identifier = a workspace schema version; feeds a migration registry / `upgrade` command. The two axes are orthogonal; 024 remains untouched.
- **Filename reservation**: 024's envisioned marker is `.specify/version` (schema). 045's stamp MUST NOT collide with that path — see the requirement's Shared Strings for the final name.

## Key Changes

1. init writes a machine-and-human readable source stamp (framework name, full 40-hex commit id or explicit `unavailable` sentinel + reason, UTC timestamp).
2. Cross-install-form availability: direct git probe when running from a checkout; build-time embedding for installed distributions (effect constrained by FR-004; mechanism decided at plan).
3. Re-init refreshes the stamp to the current commit — zero stale residue; legacy projects gain the stamp on their next init with zero migration.
4. Honest degradation: commit unavailable → sentinel + reason; stamping never blocks init.

## Implementation Notes

- Commit id is the SOLE version identifier — the pyproject version must not become the identity key (requirement FR-002).
- Stamp writing is independent of the per-tool agents manifest; neither reads nor overwrites the other.

## Related Files

- Feature Index: .specify/memory/features.md
- Requirement: .specify/specs/043-init-commit-stamp/requirements.md (Draft 2026-08-17: 3 US / 8 FR / 5 SC / 3 shared strings)
- Cross-referenced Feature: .specify/memory/features/024.md (schema-version axis, orthogonal; filename `.specify/version` reserved to 024)

## Status Tracking

- **Implemented**: 2026-08-17 via /speckit.implement (requirement 043) — 19/19 tasks, SC-001..005 pass; stdlib-only `_provenance` core shared verbatim with `hatch_build.py` (object identity pinned); real wheel build verified end-to-end (embedded commit == HEAD); zero new failures vs baseline. Evidence: `.specify/specs/043-init-commit-stamp/verification.md`.
- **Planned**: 2026-08-17 via /speckit.plan (requirement 043) — design landed as: single `_probe_head_commit` grammar shared by runtime and build hook (`hatch_build.py` custom hook embedding `src/specify_cli/_source_commit.json`); `resolve_source_commit` order checkout-git > embedded > `unavailable`; `write_source_stamp` full-overwrite at init's tail, non-blocking. 3 contracts + data-model + quickstart + feature-ref in the spec dir. Constitution: 12 Pass / 1 Partial (IX — build hook justified).
- **Draft**: Registered 2026-08-17 via /speckit.clarify when requirement 043-init-commit-stamp resolved its Related Feature binding — new Feature rather than extending 024, because provenance (source identity) and workspace schema versioning (migration) are orthogonal axes.
