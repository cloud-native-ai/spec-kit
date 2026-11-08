# Contract: Mirror Projection

**Feature**: 089-script-interface-contract | **Contract file**: `contracts/mirror-projection.contract.md`
**Guard carriers**: `tests/contract/test_script_interface_contract.py` (projection clauses) and the existing
`tests/contract/test_mirror_parity_suite.py` (which derives its parameters from `MIRROR_PAIRS` and therefore
picks the new rule up automatically)
**FR coverage**: each clause carries its own trailing citation group; that group, not this header, is the owner of the mapping

`.specify/scripts/` and `.specify/skills/` are generated copies. Today every generated copy is byte-identical to
its source and `sync-mirrors.py --check` asserts that. This feature needs a mirror-side flag surface that a
byte-identical copy cannot carry (measured: a bridge appended after `if __name__ == "__main__":` never runs, and a
bridge inserted before it is erased by the next projection). This contract replaces byte equality for the named
files with an **executable** projection rule, and forbids every byte written by hand.

## C-33 — Projection, never hand edit

No file under `.specify/scripts/` or `.specify/skills/` is edited by a human or an agent. The mirror is produced
by `scripts/python/sync-mirrors.py` and by nothing else. A hand-edited mirror is a defect judged by C-35 and by
the existing parity suite.

(FR-022)

## C-34 — The projection rule is declared, named, and deterministic

`sync-mirrors.py` MUST carry one declaration of the projected files — a table whose rows name the repo-relative
mirror path and the projection kind — and MUST apply it while writing (write mode) and while checking (check
mode). Two kinds exist and no third may be added without revising this contract:

| Kind | Effect on the mirror |
|------|----------------------|
| `python-version-bridge` | the mirror equals the source with one bridge block inserted immediately **before** the source's `if __name__ == "__main__":` line |
| `bash-version-guard` | the mirror equals the source with one guard block inserted immediately after the shebang line, ahead of everything else |

The projection MUST be idempotent: applying it to a file that already carries it changes nothing, and applying it
twice equals applying it once. The projection MUST fail loudly (exit 1, named pair) when its anchor line is
absent; it MUST NOT silently append at end of file.

(FR-022)

## C-35 — The check mode asserts the projection, not raw equality

For a projected file, `--check` MUST assert `mirror == project(source)`; for every other file it MUST keep the
existing byte-equality assertion. The check output MUST name the projection kind for each projected pair so a
reader can tell why the two files differ. The existing parity suite derives its parameters from `MIRROR_PAIRS`; it
MUST therefore be extended to consult the same declaration rather than maintaining a second list.

(FR-030)

## C-36 — The mirror surface is self-sufficient

The projected block MUST depend on nothing that only exists in the source tree. It re-derives its own version
line from the `pyproject.toml` located by the same bounded upward search as the source rule (to the enclosing
repository root) and prints `unknown` when there is none. A downstream project, whose `.specify/` copy has no source sibling, MUST therefore
get a working `--version` and a working `--help` from its own copy.

(FR-022)

## C-37 — The strictness rule stays strict

The measured flags differ per pair (`scripts` → `strict_extras=True`; `skills/external` → `False`), because a projected scripts tree may not gain stray files while a project may legitimately carry local skills of its own.
The projection MUST NOT change that flag: it narrows nothing outside the declared rows, and a `MIRROR_PAIRS` row
whose third element changes is a different change governed by its own evidence.

(FR-022)

## C-38 — Frame: what a reader of a mirror sees

A projected mirror MUST NOT carry a comment claiming it is byte-identical to its source, and the source MUST NOT
claim to be the whole truth of the mirror's surface. The authoritative statement lives here (C-34) and in the
owner page; each projected file carries one short marker line so its projection is visible in place.

(FR-022, FR-030)
