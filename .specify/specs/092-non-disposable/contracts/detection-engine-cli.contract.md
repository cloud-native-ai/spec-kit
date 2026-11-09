# Contract: Detection Engine CLI

**Feature**: 092-non-disposable | **Contract file**: `contracts/detection-engine-cli.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (C-602 / C-603 / C-605 / C-606 carry mutation legs)
**Owner**: the engine's constants (exit codes, the three actions, the projection rule) are owned by the engine module
header; the review-surface members and order are owned by
`shared/declarations/facts/non-disposable-review-surface.yaml`; the report fields are owned by
`contracts/report-schema.contract.md`. This file fixes the **calling surface** only.
**FR coverage**: each clause carries its own trailing citation group.

## C-601 — Shape: one stdlib file beside its siblings

The engine MUST be a single standard-library Python file at `scripts/python/non-disposable-check.py`, with no
third-party import, following the sibling engines' shape (`sanitize-utils.py`, `closure-acceptance-check.py`): shebang,
a module docstring stating usage and the exit codes, `from __future__ import annotations`, `main(argv=None) -> int`,
and an `if __name__ == "__main__": sys.exit(main())` tail. Its mirror is
`.specify/scripts/python/non-disposable-check.py`, produced by `sync-mirrors.py` (strict pair: the projection block is
inserted, so the pair is not byte-equal by construction). Reuse of `declaration_reader.py` and `renumber-utils.py` is
by import from the same directory, not by copy.

(FR-061, FR-059, SC-012)

## C-602 — Read-only in every mode, and self-consistent about its root

The engine MUST NOT write inside the repository in any mode — including `--json`, `--scope`, `--help` and every
error path. Its only permitted write location, if a future mode needs scratch, is `.specify/.tmp/` (git-ignored) with
removal on exit; today no mode needs it, and the guard asserts a `git status --porcelain` comparison around a full
run is byte-identical. When invoked through the `.specify/scripts/python/` mirror the engine MUST resolve the
repository root as the parent of `.specify`, never `.specify` itself. A mutation leg makes the engine touch a tracked
path and asserts red on the zero-write assertion.

(FR-031, FR-061, SC-004)

## C-603 — Exit codes are three-valued and mean three different things

| Exit | Meaning |
|------|---------|
| `0` | no findings over a stated, non-empty surface |
| `1` | findings exist (any entry, any class, including `unevaluated` entries) |
| `2` | argument or environment error — including a missing/invalid declaration, an unresolvable root, an unknown option |

`0` MUST NOT be reachable when the candidate set is empty (SC-014 / FR-011: "empty candidates" and "all green" are
different conclusions). `1` MUST NOT be reachable on an empty candidate set either — the empty surface is reported as
its own conclusion with a non-zero code pointing at the declaration, and the guard asserts which. Unknown options MUST
exit `2`, never `1`.

(FR-010, FR-011, FR-039)

## C-604 — Arguments

| Argument | Meaning | Required |
|----------|---------|----------|
| `--root PATH` | repository root (default: resolved from the engine's own location) | no |
| `--json` | machine-readable report on stdout (§ `contracts/report-schema.contract.md`) | no |
| `--scope SHARD` | judge only the declared root(s) in this shard (repeatable; the shard naming is deterministic, § C-607) | no |
| `--roots` | print the declared root set (path, presence, count) and exit `0` without judging candidates | no |
| `--emit-categories` | print the closed class set as JSON and exit `0`; no candidate is judged | no |
| `--declaration PATH` | override the fact file (for fixtures) — the **only** way to point the engine at another surface | no |
| `-h`, `--help` | usage | no |
| `--version` | version line | no |

No other option exists; an unrecognised option exits `2`. `--declaration` MUST NOT permit a directory list on the
command line: the surface is always a declaration file, never an inline list.

(FR-036, FR-037, FR-061)

## C-605 — The review surface comes from the declaration, only

The engine MUST read the ten roots, their order and their count from the fact file through the single read entry
`scripts/python/declaration_reader.py`. It MUST NOT inline a directory literal list, and neither the command template
nor the skill may carry a second copy. A missing declaration → exit `2` naming the missing path (never "zero candidates
therefore green"); a declaration whose `kind` or required keys are invalid → exit `2` naming the offending key; the
degraded-read label reuses `STR-014`, no new label. A declared-but-absent directory is reported per directory and
excluded from the candidate count **with a reason** (distinguishable from "present but empty"); an undeclared sibling
directory produces a hint and does not enlarge the candidate set.

(FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, SC-018)

## C-606 — `--scope` shards are disjoint, complete and order-free

Sharding MUST assign every candidate to exactly one shard; the union of shards MUST equal the candidate set and no
shard MAY be empty. Shard membership MUST be a pure function of the sorted path list (assignment by index modulo a
stable rule or by contiguous sorted ranges — either way, the assignment is reproducible from the path set alone). Two
runs at different concurrency degrees MUST produce the same entry set **by `entry_id`**. A mutation leg duplicates one
path across two scopes and asserts red.

(FR-047, FR-049, SC-009)

## C-607 — Determinism of output

Two runs on the same tree MUST produce byte-identical `--json` output after removing the run identifier: entries
sorted by `entry_id`, roots in declaration order, mappings sorted by key. A finding whose order depends on directory
iteration order is a violation. The guard runs the engine twice and diffs.

(FR-010, FR-049, FR-055)

## C-608 — Mirror projection

The `.specify/scripts/python/non-disposable-check.py` copy is generated by `sync-mirrors.py` and never hand-edited; the
projection marker appears exactly once and the `_bridge_*` block sits immediately before the `__main__` guard, matching
the other engines in that directory.

(FR-061, SC-012)
