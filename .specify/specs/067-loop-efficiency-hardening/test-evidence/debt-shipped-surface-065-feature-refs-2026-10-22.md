# Debt — shipped sdd-loop-driver surface references framework feature IDs — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned test

- `tests/contract/test_shipped_surface_client_neutrality.py::test_shipped_surface_has_no_framework_runtime_references`

## Failure shape

Client-visible file `skills/external/sdd-loop-driver/scripts/loop-state.py` references the
framework project's own runtime artifacts in its docstrings:

- line 3: `"""loop-state.py — read-only loop state snapshot engine (Feature 065 / Slice 065a).`
- line 2871: `description="Read-only loop state snapshot engine (Feature 065 / slice "`

## Why not repaired here

1. The offending file is part of the `skills/external/sdd-loop-driver/` mirror pair — editing the
   mirror half directly is forbidden (mirrors are engine-written; hand edits create drift), and
   part F's write surface excludes `skills/` entirely.
2. The wording landed with feature 065a (the engine's own landing, 2026-10-22 commits
   `0ac387eb`/`0860092a` lineage) — i.e. **not introduced by this scope**; it is already in the
   pre-stage and T007 in-stage baselines.

## Repair path (owned elsewhere)

Rewrite the two docstring lines from the client-project perspective (no framework feature IDs)
in the mirror's source half, then ride `sync-mirrors.py --write --only skills/external` and the
engine's own regeneration flow.
