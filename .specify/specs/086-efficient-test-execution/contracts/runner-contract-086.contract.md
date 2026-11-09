# Contract: Canonical Runner Execution Model (C-001…C-016)

Owner of the propositions below: this contract. The implementation owner is
`scripts/bash/run-tests.sh` (runtime copy `.specify/scripts/bash/run-tests.sh`, byte-identical).

> **Superseded**: the "byte-identical" carriage above and in C-016 is superseded by
> `.specify/specs/089-script-interface-contract/contracts/mirror-projection.contract.md` (source + declared
> projection). The original wording is retained verbatim as the pre-089 record.

**Inherited, not restated**: RC-01…RC-08 of
`.specify/specs/067-loop-efficiency-hardening/contracts/runner-contract.md` stay in force verbatim. This
contract adds the **execution model** (default mode, worker resolution, exclusions, output combination); it
does not restate, weaken or reopen 067's conclusions. Where the two touch the same surface, 067 owns
`--names-out` semantics, argument passthrough, interpreter-resolution order and the serial-runnability
guarantee; this contract owns only what 067 left to "a future recorded scope decision" (RC-03).

## A. Default mode

- **C-001**: With a parallel engine importable by the resolved interpreter, no `--serial`, no caller
  `-n`/`--numprocesses`, and `PYTEST_XDIST_WORKER` unset, the runner MUST execute the caller's selection in
  **parallel** (`-n <effective>`, `--dist load`) without the caller passing any parallel argument
  (FR-001, FR-010).
- **C-002**: The runner MUST state the executed mode on stderr as a line matching
  `# test runner: mode=parallel` or `# test runner: mode=serial reason=<explicit|nested|no-xdist>`. A run
  whose stderr carries neither line is non-conforming (FR-006, FR-021).
- **C-003**: The pre-existing header line `# test runner: <interpreter> -m pytest <args>` MUST remain, and
  it MUST describe the arguments the runner actually passes — no argument that was resolved but not applied
  may appear in it (FR-007).

## B. Serial escape hatch

- **C-004**: `--serial` (`STR-007`, FR-002) MUST run one complete pass over the caller's full selection with
  `-n0`, write the failure-name list if `--names-out` was given, and exit with pytest's own code. The runner
  MUST NOT label such a run degraded, partial or unsupported (FR-002, FR-007).
- **C-005**: When `PYTEST_XDIST_WORKER` is set, the runner MUST run serial with `reason=nested` and MUST NOT
  create a second worker pool; the nested run's failure-name list MUST be valid (FR-005).
- **C-006**: When the resolved interpreter cannot `import xdist`, the runner MUST run serial with
  `reason=no-xdist`, MUST complete the run (no error exit, no empty run) and MUST keep pytest's exit code
  (FR-006, FR-015, FR-016).

## C. Worker resolution

- **C-007**: `--workers <N|auto>` MUST take precedence over `SPECKIT_TEST_WORKERS` (`STR-006`), which MUST
  take precedence over the literal `auto` (FR-003).
- **C-008**: A `--workers` or `SPECKIT_TEST_WORKERS` value that is not a positive integer and not `auto`
  MUST exit non-zero with a named error on stderr. Silent fallback to one worker is forbidden (FR-003).
- **C-009**: If the caller's own arguments already contain `-n`, `-n<value>`, `--numprocesses` or
  `--numprocesses=<value>`, the runner MUST NOT append `-n` or `--dist`. The result MUST contain exactly one
  worker-count switch (FR-004). The same guard covers a caller-supplied scheduler (`--dist <value>` /
  `--dist=<value>`): the runner MUST NOT append its own `--dist load` on top of it, MUST forward the
  caller's scheduler verbatim, and MUST name the executed scheduler in the mode line (C-002/C-003), so the
  A13 `load` vs `loadfile` experiment (`quickstart.md` S-5 / T016) measures the arm it claims.

## D. Declared serial exceptions

- **C-010**: The runner MUST support a registered `serial` marker: in parallel mode it excludes marked
  tests from the parallel pass and re-runs them in a serial pass (`-n0`) (FR-010, FR-011, FR-012).
- **C-011**: The exception set MUST be enumerable by name with `pytest -m serial --collect-only -q`, and the
  number of members MUST be recordable in evidence. A global "parallel off" switch is not an admissible
  implementation (FR-011).
- **C-012**: Exit code 5 (nothing collected) from the **serial** pass MUST be normalized to 0; the same exit
  code from the parallel pass MUST NOT be normalized (FR-007, FR-008).

## E. Outputs

- **C-013**: `--names-out <file>` MUST produce exactly one sorted, de-duplicated list of `FAILED` node ids,
  one per line, combining all passes of that run (FR-007, FR-008).
- **C-014**: The stderr line is `# failed-name list written: <path> (<n> entries) passes=<k>`
  (`STR-002`), and it MUST be emitted on every run that writes a list. `<n>` is the entry count of the
  combined list and `<k>` is the number of passes that contributed, so an empty list is distinguishable
  both from a missing list and from a list that was not combined (FR-008).
- **C-015**: The run's exit code MUST be non-zero if and only if at least one pass failed after
  normalization; a two-pass run whose serial pass is empty and whose parallel pass is green exits 0
  (FR-007, FR-008).
- **C-016**: `scripts/bash/run-tests.sh` and `.specify/scripts/bash/run-tests.sh` MUST be byte-identical at
  every commit that touches either; the mirror is written by `scripts/python/sync-mirrors.py`, never by hand
  (FR-009).
  **Superseded by
  `.specify/specs/089-script-interface-contract/contracts/mirror-projection.contract.md` (source + declared
  projection)**: `bash-version-guard` is declared for this pair, so the mirror MUST equal `project(source)`
  and byte equality no longer holds; the "written by `sync-mirrors.py`, never by hand" half stays in force
  (089 C-33/C-35). The clause above is kept verbatim as the pre-089 record.

## F. Contract test obligations

The behaviors above are carried by `tests/contract/test_run_tests_runner_contract.py` (created in WP-A4).
Minimum case set, one case per clause: C-001, C-002+C-003 (same case), C-004, C-005, C-006, C-007, C-008,
C-009, C-010+C-011, C-012, C-013, C-014, C-015, C-016.

Test-construction constraints (load-bearing, not style):

- Cases that must not depend on this host's CPU count MUST pass `--workers 2` explicitly.
- The "no xdist" case MUST stub the engine rather than uninstall it: run the runner with
  `SPECKIT_PYTHON` pointing at a wrapper that answers `-m pytest --version` and `-c 'import xdist'` by
  failing only the latter, or with a temporary `PYTHONPATH` shim that shadows `xdist`. The chosen mechanism
  MUST be recorded in the test's docstring so the premise is re-probeable.
- No case may assert a wall-clock threshold.

## Mutation Legs

A guard that cannot go red proves nothing. Each leg below must fail its named case when applied.

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| M-1 | Delete the `--serial` branch from mode resolution | C-004 |
| M-2 | Change worker precedence to env-over-flag | C-007 |
| M-3 | Always append `-n <effective>`, even when the caller passed `-n` | C-009 |
| M-4 | Drop the `PYTEST_XDIST_WORKER` check | C-005 |
| M-5 | Normalize exit code 5 on the parallel pass too | C-012, C-015 |
| M-6 | Write the failure-name list from the parallel pass only | C-013 |
| M-7 | Edit the runner source without regenerating the mirror | C-016 |
