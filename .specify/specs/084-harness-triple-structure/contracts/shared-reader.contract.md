# Contract — Shared Read Entry（`scripts/python/declaration_reader.py`）

**Feature**: 084 Harness 三重结构 | **Date**: 2026-11-05
**Why this file exists as a contract**: the failure this feature removes is "the same rule implemented twice". A shared
read entry is the mechanism that makes a second implementation visible as a defect instead of a stylistic remark.

## Clauses

- **C-052** The read entry is one module, `scripts/python/declaration_reader.py`, standard library only, Python
  `>= 3.8`. `pyproject.toml`'s `dependencies` MUST NOT gain any YAML library (the list is compared byte-for-byte against
  the baseline at closure).
- **C-053** It is both importable and callable. Every sibling engine is invoked as `python3 scripts/python/<name>.py`
  (and, in a client project, as `python3 .specify/scripts/python/<name>.py`), so the script's own directory is
  `sys.path[0]` and a bare `import declaration_reader` resolves without path games. The CLI form exists for humans and
  for the contract test only.
- **C-054** It owns the entire YAML-subset grammar of `contracts/declaration-schema.contract.md` C-008, the parsing of
  `contract.yaml`, the loading of one fact, and the loading of the exclusion rows. No other file in the repository
  parses declaration YAML.
- **C-055** Public functions (names fixed so a consumer's read point is greppable):
  `load_contract(repo)`, `load_fact(repo, slug)`, `load_facts(repo)`, `load_exclusions(repo)`,
  `normalize_path(value)`.
  Each raises a single typed error carrying the finding template id when the input is invalid; the caller maps it to the
  exit code. No function prints.
- **C-056** Degradation: when `<repo>/shared/declarations/` does not exist, the module signals the degraded state through
  that same typed error (never through an exception type of its own invention), and the caller turns it into the exit-2
  label. A consumer MUST NOT crash on a legacy client project.
- **C-057** `normalize_path()` strips exactly one optional leading `.specify/` and returns a repo-relative value. This is
  the single place where the three-copy problem (`research.md` § R3) is solved; a consumer that normalizes paths itself
  is a second implementation.
- **C-058** A boundary guard test asserts, mechanically, that the module is the only file under `scripts/` and
  `skills/` that implements a subset parser (the assertion is a search for a parser-shaped function or a duplicated
  subset marker, not a semantic review). The pre-existing inline parsers `scripts/python/execution-config.py`
  (`parse_yaml_subset`) and `scripts/python/gate-check.py` (`parse_gate`) are grandfathered by an explicit allowlist in
  that guard, with the reason "registered under § Non-Goals N4, not touched by this feature".
- **C-059** The module and the checker are mirrored together (`scripts/ → .specify/scripts/`, the strict pair): a source
  file without its mirror is drift, and this pair fails on a mirror-only extra file.

## Sibling-precedent note (Grounded Naming)

The repository has two naming shapes for Python scripts: kebab-case for scripts invoked as commands
(`evidence-utils.py`, `flow-class-check.py`) and underscore for modules meant to be imported
(`clause_extract.py`). This feature takes the second shape because the entry point IS imported; the name
`declaration_reader` reads as "the reader of declarations" (what it is), not as a place it happens to be used.

## Verification (route (b), per example)

| Example | Pinned by | Premises |
|---------|-----------|----------|
| `python3 scripts/python/declaration_reader.py --action get --fact <fact-slug>` | `tests/contract/test_harness_triple_structure.py` (CLI parity case: CLI output equals the function output for the same fixture) | the CLI action names `get` / `list` as declared here; the module exists and is mirrored; the fixture's fact file passes the subset |
| `python3 -c "import declaration_reader"` run from `scripts/python/` | same module (importability case) | the interpreter used is the one `scripts/bash/run-tests.sh` resolves; `sys.path[0]` is the script directory under that interpreter |
