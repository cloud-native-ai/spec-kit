# Contract: In-Process Conversion and Boundary Classification

**Owner of these propositions**: this file. **Carrier of the classification data**:
`test-evidence/inprocess-conversion.md`. **Implementation surfaces**: the converting test files, the
in-process invocation helper, and the guard `tests/contract/test_inprocess_conversion_contract.py`.

## A. Classification

- **C-001**: Every `subprocess.run` call site under `tests/` (including `tests/fixtures/` and
  `tests/conftest.py`) is classified with exactly one verdict: `convert` (the call exists only to verify
  Python-side behaviour: return values, JSON, file effects) or `keep` (the call's subject IS the process
  boundary) (FR-018, FR-027).
- **C-002**: `keep` requires one boundary class from this closed set: `cli-contract` (console entry,
  `--help`/`--version`/unknown-option exit codes), `signal-timeout-interrupt`, `git-external`,
  `process-isolation-subject`, `other-interpreter`, `global-state-unrecoverable` (cwd/env the fixtures
  cannot restore), `copy-topology` (the subject is a projected or separately installed copy and its
  location/identity is what is asserted) (FR-027).
- **C-003**: `convert` requires an equivalence route in the row: the same assertions run against an
  in-process call, with stdout/stderr captured and the exit code taken from the engine's `main(argv)`
  return value; for the Typer CLI, `typer.testing.CliRunner` provides the equivalent result (FR-018,
  FR-027).
- **C-004**: Fixture-layer helpers that set `cwd=` or `env=` on the child (`tests/fixtures/client_project.py`
  `run_engine`/`run_script`, `tests/fixtures/line_fixtures.py` process drivers) are `keep` /
  `global-state-unrecoverable` by default. An in-process mode may be added only for a call whose engine
  invocation has no cwd/env dependence; the default stays subprocess (FR-027).

## B. Manifest and guard

- **C-005**: The manifest `test-evidence/inprocess-conversion.md` is a pipe table with the columns
  `file | call_site | verdict | boundary_class | reason` (data-model E-6). One row per discovered call
  site; `call_site` names the enclosing function plus a normalized target (engine file name or command
  kind), so line drift does not invalidate the row (FR-019).
- **C-006**: The manifest is generated from a deterministic AST scan of `tests/` and completed by hand for
  the verdicts; the scan output is the completeness denominator (B-9 census). A call site discovered by
  the scan but absent from the manifest MUST turn the guard red and be named (FR-019).
- **C-007**: Reverting a converted point to `subprocess.run` MUST turn the guard red and name the file and
  call site. The guard re-scans call sites rather than trusting the manifest alone (FR-019, SC-009).
- **C-008**: A `keep` row MUST have a class from C-002 and a one-line reason. A converted row MUST NOT
  weaken assertions: importing the module or asserting only `main() is not None` is forbidden; the same
  behaviour assertions (values, JSON fields, file effects) run before and after (FR-019).

## C. Equivalence evidence

- **C-009**: For each converted group, the before and after targeted runs are recorded with command, exit
  code and complete output under `test-evidence/`. The pair must show the same pass/fail names (FR-019).
- **C-010**: Boundary cases named by the requirements (086 C-006-style shim probes, `--help`/`--version`/unknown
  option, signal/timeout, git, process-isolation, different interpreter) stay subprocess and are each
  recorded with their class; they are the keep-side sample the guard checks for non-emptiness (FR-027).

## D. Mutation legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| IC-M1 | Change one converted call back to `subprocess.run` | C-007 |
| IC-M2 | Delete a manifest row for a discovered call site | C-006 |
| IC-M3 | Give a `keep` row a class outside the closed set | C-002 |
| IC-M4 | Weaken a converted assertion to an import-only check | C-008 |
| IC-M5 | Convert a `--help`/`--version` case that asserts the process contract | C-002/C-010 |
