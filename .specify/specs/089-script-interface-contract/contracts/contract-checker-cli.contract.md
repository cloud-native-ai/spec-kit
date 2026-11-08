# Contract: Contract Checker CLI

**Feature**: 089-script-interface-contract | **Contract file**: `contracts/contract-checker-cli.contract.md`
**Guard carrier**: `tests/contract/test_script_interface_contract.py`
**FR coverage**: each clause carries its own trailing citation group; that group, not this header, is the owner of the mapping

The calling surface of `scripts/python/script-interface-check.py` and of its mirror. This contract fixes what a
caller may rely on; it does not restate the criteria (those are
`contracts/script-interface-criteria.contract.md`).

## C-14 — Shape

The engine MUST be a single standard-library Python file at `scripts/python/script-interface-check.py`, with no
third-party import, and MUST follow the sibling engines' shape (`scan-confirmation-gates.py`,
`gate-check.py`): shebang, a module docstring naming the usage and the exit codes, `from __future__ import
annotations`, a `main(argv=None) -> int`, and a `if __name__ == "__main__": sys.exit(main())` tail. Its mirror is
`.specify/scripts/python/script-interface-check.py`, produced by `sync-mirrors.py`.

(FR-031)

## C-15 — Read-only, and self-consistent about its own root

The engine MUST NOT write inside the repository. Its only writes are to the sandbox copy it creates under the
system temp root or under `.specify/.tmp/`, and both MUST be removed on exit (success and failure). When invoked
through its `.specify/scripts/python/` mirror, the engine MUST resolve the repository root to the parent of
`.specify`, never to `.specify` itself — the same guard `scan-confirmation-gates.py` and `sync-mirrors.py`
already implement.

(FR-024, FR-031)

## C-16 — Arguments

| Argument | Meaning | Required |
|----------|---------|----------|
| `--root PATH` | repository root (default: resolved from the engine's own location) | no |
| `--json` | machine-readable report on stdout | no |
| `--files PATH[,PATH…]` | restrict judgement to these candidates (repeatable); the screen's coverage assertion is narrowed to them and the report says `mode=subset` | no |
| `--emit-rule` | print the classification rule as JSON and exit 0; no candidate is probed | no |
| `--skip-probe` | classify nothing; list candidates and exit 0 with `applicable=0`, `mode=screen-only` | no |
| `--sandbox DIR` | place the sandbox copy here instead of the default location | no |
| `--budget-seconds N` | soft wall-clock budget for the probe phase (default 900) | no |
| `--check-projection` | verify the mirror projection rule against the mirror tree instead of probing candidates | no |

`--json` with `--emit-rule` is allowed and produces the same payload; `--emit-rule` with `--files` is an argument
error (exit 2). Unknown flags are rejected by `argparse` with exit 2 — this engine obeys the contract it checks.

(FR-008, FR-018, FR-031)

## C-17 — Exit codes

| Code | Meaning |
|------|---------|
| `0` | the screen ran, every applicable candidate is compliant and every exempt candidate carries a basis; `violations == 0` |
| `1` | at least one violation, or a structural finding (`candidate-not-collected`, `exception-unverifiable`, `probe-unavailable`, `probe-budget-exhausted`, `probe-inconclusive`, `projection-mismatch`) |
| `2` | argument or environment error (bad flag combination, `--root` not a repository); a sandbox that cannot be created is a C-13 finding at exit 1, never exit 2 |

The code MUST be derived from the report's own findings; the engine MUST NOT compute a code the report cannot
explain.

(FR-010)

## C-18 — Report payload

The `--json` payload MUST carry, at minimum: `schema` (`script-interface-check/1`), `mode`
(`full` · `subset` · `screen-only` · `emit-rule` · `check-projection`), `source` (`tracked` · `walk-only`),
`root`, `candidates`, `applicable`, `exempt`, `violations`, `elapsed_ms`, and the arrays `candidates[]`,
`exemptions[]`, `exceptions[]`, `findings[]`, `projection[]`. Each `candidates[]` row MUST carry `path`,
`language`, `applicable`, `basis`, `help`, `help_content`, `version`, `unknown_rejected`, `zero_side_effect`, and
`evidence`. Each `exemptions[]` row MUST carry `path`, `basis`, `evidence`. Each `exceptions[]` row MUST carry
`path`, `skill`, `recomputed`, `unsatisfied_clause`.

`candidates[].version` MUST be the literal string `unknown` when the candidate's `--version` line reported
`unknown` (C-8's unreachable-`pyproject.toml` case). This is an **observation**, not a violation: a candidate whose
version resolves to `unknown` still passes C-8 (which explicitly permits it at exit 0), so the field exists to let
a reader select such candidates (`select(.version=="unknown")`) and never changes the exit code. A candidate that
prints `unknown` while a reachable `pyproject.toml` exists at its resolved repository root is a C-8 violation and appears in
`findings[]` under the checker's own basis, not in this field.

(FR-010)

## C-19 — Human output

Without `--json`, the engine MUST print one line per violation (`<path>: <missing limbs>`) and a summary line
`candidates=N applicable=N exempt=N violations=N`. A run with zero violations MUST still print the summary (so
"nothing printed" is never the passing signal).

(FR-010)

## C-20 — Determinism

Two runs over the same tree state MUST produce the same `candidates[]` ordering (sorted by path) and the same
verdict set. `elapsed_ms` is the only field allowed to differ; the engine's own guard MUST assert this by running
twice and comparing the payload with `elapsed_ms` removed.

(FR-010, FR-029)

## C-21 — `--emit-rule`

`--emit-rule` MUST print a JSON object whose keys are `labels`, `flag_forms`, `separator`, `version_line`,
`version_source`, `exempt_basis`, `findings`, `exceptions`. The engine's own classification code MUST read its
constants from one module-level table so the emitted rule and the executed rule cannot drift; the guard asserts
the identity by comparing `--emit-rule` against `exempt_basis` values actually produced in a full run. The same
guard MUST also read the label set and the class vocabulary out of the owner page and assert set equality with the
emitted rule in both directions; the page, never a hand-written list, is the compared surface.

(FR-015, FR-031)

## C-22 — `--check-projection`

`--check-projection` MUST verify, for each declared projected mirror: the mirror equals `source + declared
projection`, and re-applying the projection is idempotent. A mismatch MUST name the pair and exit 1.

(FR-022, FR-030)
