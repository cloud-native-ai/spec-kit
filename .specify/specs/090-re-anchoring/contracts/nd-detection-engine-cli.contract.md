# Contract: Detection Engine CLI

**Feature**: 090-re-anchoring · Non-Disposable slice (absorbed from 092) | **Contract file**: `contracts/nd-detection-engine-cli.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (ND-C-602 / ND-C-603 / ND-C-605 / ND-C-606 carry mutation legs)
**Owner**: the engine's constants (the three exit codes, the projection rule) are owned by the engine module
header; the review-surface members and order are owned by
`shared/declarations/facts/non-disposable-review-surface.yaml`; the report fields are owned by
`contracts/nd-report-schema.contract.md`. This file fixes the **calling surface** only.
**FR coverage**: each clause carries its own trailing citation group.

## ND-C-601 — Shape: one stdlib file beside its siblings

The engine MUST be a single standard-library Python file at `scripts/python/non-disposable-check.py`, with no
third-party import, following the sibling engines' shape (`sanitize-utils.py`, `closure-acceptance-check.py`): shebang,
a module docstring stating usage and the exit codes, `from __future__ import annotations`, `main(argv=None) -> int`,
and an `if __name__ == "__main__": sys.exit(main())` tail. Its mirror is
`.specify/scripts/python/non-disposable-check.py`, produced by `sync-mirrors.py` (strict pair: the projection block is
inserted, so the pair is not byte-equal by construction). Reuse of `declaration_reader.py` and `renumber-utils.py` is
by import from the same directory, not by copy.

(FR-061, FR-059, SC-012)

## ND-C-602 — Read-only in every mode, and self-consistent about its root

The engine MUST NOT write inside the repository in any mode — including `--json`, `--scope`, `--help` and every
error path. Its only permitted write location, if a future mode needs scratch, is `.specify/.tmp/` (git-ignored) with
removal on exit; today no mode needs it, and the guard asserts a `git status --porcelain` comparison around a full
run is byte-identical. When invoked through the `.specify/scripts/python/` mirror the engine MUST resolve the
repository root as the parent of `.specify`, never `.specify` itself. A mutation leg makes the engine touch a tracked
path and asserts red on the zero-write assertion.

(FR-031, FR-061, SC-004)

## ND-C-603 — Exit codes are three-valued and mean three different things

| Exit | Meaning |
|------|---------|
| `0` | no findings over a stated, non-empty surface |
| `1` | findings exist (any entry, any class, including `unevaluated` entries) |
| `2` | argument or environment error — including a missing/invalid declaration, an unresolvable root, an unknown option |

**The empty candidate set has exactly one exit code, and this clause is its only statement: `2`.** The reading is
"the surface I was given declared no candidates", which is an environment/declaration defect, not a verdict — the
engine exits `2`, names the declaration path, and prints the coverage declaration with `candidates: 0`. `0` MUST NOT
be reachable on an empty surface (SC-014 / FR-011: "empty candidates" and "all green" are different conclusions), and
`1` MUST NOT be reachable on it either (a finding count over zero candidates is arithmetic, not evidence). The guard
asserts the code is `2` **and** that the reason names the declaration — three readings of this one case ("non-zero,
pointing at the declaration" / "its own conclusion code" / "0 with a warning") is how the case would be re-decided per
implementation, and the point of fixing it here is that it is not. Unknown options MUST exit `2`, never `1`.

(FR-010, FR-011, FR-039)

## ND-C-604 — Arguments

| Argument | Meaning | Required |
|----------|---------|----------|
| `--root PATH` | repository root (default: resolved from the engine's own location) | no |
| `--json` | machine-readable report on stdout (§ `contracts/nd-report-schema.contract.md`) | no |
| `--scope SHARD` | judge only the candidates whose path falls in this shard (repeatable; the shard id is the formula `s{index:03d}-of-{n:03d}` in clause ND-C-606, and it partitions the **file set**, never the classes) | no |
| `--roots` | print the declared root set (path, presence, count) and exit `0` without judging candidates | no |
| `--emit-categories` | print the closed class set as JSON and exit `0`; no candidate is judged | no |
| `--declaration PATH` | override the fact file (for fixtures) — the **only** way to point the engine at another surface | no |
| `-h`, `--help` | usage | no |
| `--version` | version line | no |

No other option exists; an unrecognised option exits `2`. `--declaration` MUST NOT permit a directory list on the
command line: the surface is always a declaration file, never an inline list.

**Actions and arguments are two different counts, and neither is "three".** An *action* is an option that makes the
engine print something and stop without judging candidates: `--roots` and `--emit-categories` — **two** of them. An
*argument* is any accepted option: the **eight** rows in the table above, counting `-h` / `--help` as one row and
`--version` as another. A third action does not exist (`--version` is a script-interface answer, not a review action,
and it is listed as its own argument row). The engine's exit code under either action is `0`; the verdict domain of
ND-C-603 applies only to a judging run.

(FR-036, FR-037, FR-061)

## ND-C-605 — The review surface comes from the declaration, only

The engine MUST read the ten roots, their order and their count from the fact file through the single read entry
`scripts/python/declaration_reader.py`. It MUST NOT inline a directory literal list, and neither the command template
nor the skill may carry a second copy. A missing declaration → exit `2` naming the missing path (never "zero candidates
therefore green"); a declaration whose `kind` or required keys are invalid → exit `2` naming the offending key; the
degraded-read label reuses `STR-014`, no new label. A declared-but-absent directory is reported per directory and
excluded from the candidate count **with a reason** (distinguishable from "present but empty"); an undeclared sibling
directory produces a hint and does not enlarge the candidate set.

**The undeclared-directory predicate is three comparisons against the declared set `S`, and no shape inference.** Let
`S` be the declared root set and `d` a first-level directory under `.specify/`:

| Reading | Predicate | What the report says |
|---|---|---|
| declared-but-absent | `p ∈ S` and the directory does not exist | the root `p`, absent, excluded from `candidates` with its reason |
| present-but-undeclared | the directory exists and `d ∉ S` | `d`, once, as an undeclared sibling — **no** claim about what it "looks like" |
| newly appeared | `d ∉ S` and `d` absent from the previous run's root reading | the same reading as the row above; it is not a fourth category |

"Does its name look like one of the roots" is **not** a predicate this clause permits: it would define the test by the
thing under test. The consequence of "does not enlarge" is concrete — an undeclared directory's subtree is **not
scanned**, its candidate count is `0`, and that zero is carried in the coverage declaration with "undeclared" as its
reason, never folded in silently.

(FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, SC-018)

## ND-C-606 — `--scope` shards act on the file set, and the naming formula is this clause's

**The subject of a shard is the file set, never the class set.** A candidate is a `(path, line)` reading produced by
some class; a shard is a subset of **candidates**, assigned by **path**. The class that discovered a candidate does not
participate in the assignment: a path in shard `k` has *all* of its candidates in shard `k`, whatever classes found
them. This is the sentence that removes the conflict with `contracts/nd-detection-categories.contract.md` ND-C-102 — ND-C-102
says one *entry* carries one class (no stacking), and this clause says one *path* has one *shard* (no splitting by
class). The two claims are about different axes and both hold; a reading that shards by category would violate ND-C-102's
"a defect reported twice stays two entries" by making the same path appear in two shards.

**The naming formula**, so that `--scope` values are not invented per run:

```text
shard_id = "s{index:03d}-of-{n:03d}"          # e.g. s000-of-004, s001-of-004
index    = ordinal of the shard in sorted(range(n))
n        = shard count requested for the run
assignment: sorted_paths[i] -> shard_id of index (i mod n)   # stable, reproducible from the path set alone
```

Three consequences, each decidable without running the engine:

- The shard **count** `n` is a property of the run, not of the tree; the same tree at two values of `n` yields two
  different partitions, both legal. What MUST NOT change is the entry set **by `entry_id`** — only its distribution.
- The shard id **names the partition**, never the content: two runs with different `n` produce different ids for the
  same path, and a consumer MUST NOT cache anything keyed on a shard id alone.
- An empty shard is a run error (exit `2` naming the requested `n`), never an empty report: `n` greater than the
  candidate count cannot partition the set into non-empty pieces.

Sharding MUST assign every candidate to exactly one shard; the union of shards MUST equal the candidate set. A mutation
leg duplicates one path across two scopes and asserts red, and a second leg requests `n` larger than the candidate
count and asserts exit `2`.

(FR-047, FR-049, SC-009)

## ND-C-607 — Determinism of output

Two runs on the same tree MUST produce byte-identical `--json` output after removing the run identifier: entries
sorted by `entry_id`, roots in declaration order, mappings sorted by key. A finding whose order depends on directory
iteration order is a violation. The guard runs the engine twice and diffs.

(FR-010, FR-049, FR-055)

## ND-C-608 — Mirror projection

The `.specify/scripts/python/non-disposable-check.py` copy is generated by `sync-mirrors.py` and never hand-edited; the
projection marker appears exactly once and the `_bridge_*` block sits immediately before the `__main__` guard, matching
the other engines in that directory.

(FR-061, SC-012)
