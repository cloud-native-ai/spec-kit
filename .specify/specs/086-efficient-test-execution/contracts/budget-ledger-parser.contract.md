# Contract: Budget Ledger Parallel-Flag Recognition (C-017…C-020)

Owner of the propositions below: this contract. Implementation owner:
`skills/external/sdd-loop-driver/scripts/audit-test-budget.py` (+ `.specify/skills/external/sdd-loop-driver/
scripts/audit-test-budget.py`, byte-identical mirror).

**Inherited, not restated**: the two-slot test budget, the ledger fence, the slot value domain and the
selection-budget procedure are owned by `skills/external/sdd-loop-driver/references/efficiency-model.md` and
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md`. This contract changes exactly one thing —
which command-line tokens the parser treats as carrying a value — and nothing about slot semantics,
classification targets or the audit's other checks.

## Scope

`VALUE_FLAGS` in `audit-test-budget.py` currently reads
`("--names-out", "-m", "-k", "--maxfail", "-p", "--rootdir", "-c")`. This contract adds four tokens:

`-n`, `--numprocesses`, `--dist`, `--maxprocesses`.

## Clauses

- **C-017**: `-n` and `--numprocesses` MUST be treated as value-carrying flags, in both the separated form
  (`-n 4`) and the attached forms pytest accepts (`-n4`, `--numprocesses=4`).
- **C-018**: `--dist` and `--maxprocesses` MUST be treated as value-carrying flags in both the separated
  (`--dist load`) and attached (`--dist=load`) forms.
- **C-019**: A full-suite run whose command carries an explicit parallel switch MUST classify as a full run
  (`selection_basis` unchanged from the equivalent serial command). It MUST NOT be dropped, downgraded to
  targeted, or reported as unaccounted.
- **C-020**: Replaying every pre-existing ledger row through the upgraded parser MUST produce the same
  classification and the same positional-argument list as before the upgrade. Regression equivalence is
  asserted over a fixture set of existing-shaped rows, not argued from the diff.

## Consequence for the report surface

A value token MUST NOT appear in the parser's positional-argument list (i.e. the values `4`,
`load`, `auto` MUST NOT be read as paths). This is the failure mode C-019 protects against: a parallel
full run whose `-n auto` turned `auto` into a positional path would be classified as a targeted run against
a nonexistent path.

## Contract test obligations

Carried by `tests/unit/test_audit_test_budget.py` (existing file, new rows):

| Case | Asserts |
|------|---------|
| separated `-n 4` full run | C-017, C-019 |
| attached `-n4` full run | C-017, C-019 |
| `--numprocesses=auto` full run | C-017, C-019 |
| `--dist load` and `--dist=loadfile` | C-018 |
| `--maxprocesses 8` | C-018 |
| replay fixture of existing rows | C-020 |

## Mutation Legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| M-8 | Revert `VALUE_FLAGS` to the pre-change tuple | C-017, C-018, C-019 |
| M-9 | Add `-n` to `VALUE_FLAGS` but strip only the separated form | C-017 (attached-form case) |
