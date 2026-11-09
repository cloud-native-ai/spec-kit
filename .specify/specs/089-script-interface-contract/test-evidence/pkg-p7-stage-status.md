# P7 stage status (T078, T079, T082, T084 — polish test surface, 2026-11-08)

All rows live in `tests/contract/test_script_interface_contract.py`, in the section appended after the
T073/T074/T076/T077 section. Nine tests; the file now holds 93.

## Per-row status

- **T078 [US4] wiring discipline (C-32)** — DONE. The C-32 clause's "only new executable artifacts"
  inventory corrected to the four artifacts (each *plus its mirror*): the checker, the shared CLI
  library, the bash library, and the contract test itself. `workspace-guard.py` is deliberately left
  out of the clause (an adjudication, not a correction) and is instead pinned as a measured-but-
  undeclared path. Five tests: source-level `pytestmark = pytest.mark.contract`; behavioural
  `pytest --collect-only -m contract -q` non-zero; declared==measured over ADD rows between the
  computed merge base and HEAD (the declared list is parsed out of the clause, never hand-typed);
  no new command / driver stage gate / confirmation gate / second checker; every consumer's
  `bash-version-guard` mirror projection carries the library's statements with the 086 flag block
  as its first executable line. Reading: `T078-wiring.txt`.
- **T079 [US5] mutation M-1 (SC-008)** — DONE. Sandbox pair in `tmp_path`: a strict compliant bash
  script (control, exit 0, zero violations, zero findings) and the same script with the
  `-h|--help` arm deleted (mutant, exit 1). The mutant's `violation_rows` names exactly
  `scripts/keepme.sh` with `help` missing, and the human face prints a line naming script+limb.
  Reading: `SC-008-mutation.txt`.
- **T082 [US4] owner page ↔ `--emit-rule` (C-21)** — DONE. Both-directions agreement on the label
  closed set (`usage`, `options`, `side-effects`, `exit-codes`): the page's label line is read at
  test time, the emitted `rule.labels` is read live, and each is asserted equal to the other and to
  the module's `LABELS` and the checker's own label keys. Class vocabulary compared in the page's
  own prose (`即判(适用|豁免)` → `{applicable, exempt}`) against the report counters; the page's
  codified bases are asserted to be a subset of the rule's `exempt_basis` union the reserved bases.
- **T084 [US5] positional-flag regression guard** — DONE. Two fixture shapes modelled on
  `goal-utils.py` (a subcommand plus top-level options), each exercised with the option at both
  positions. An undeclared token is refused at *both* positions (exit 2, stderr message, empty
  stdout) — never silently ignored and executed; the documented `(0, "human")` library behaviour is
  pinned as well. The live `goal-utils.py` is additionally read and judged at both positions.
  Position-dependence of `goal-utils.py`'s own options is accepted under FR-018 (no change to
  existing option semantics), which the test states explicitly. Reading: `T084-positional-flag.txt`.

## Readings

| check | command | result |
|---|---|---|
| contract test file | `/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py` | 93 passed in 25.78s |
| marker selection | `pytest --collect-only -m contract -q tests/contract/test_script_interface_contract.py` | 93 collected, exit 0 |
| mirror projection | `python3 scripts/python/sync-mirrors.py --check` | exit 0, `shared/ == .specify/shared/` (95 files, byte-identical) |
| workspace guard | `python3 scripts/python/workspace-guard.py --check /var/tmp/086-p7.json --repo .` | `clean`, exit 0 |

Safety pre-condition: the snapshot `/var/tmp/086-p7.json` was taken before any probe; the check
after all edits is `clean` — no drift outside the declared territory.

## Territory

Changed: `contracts/governance-landing.contract.md` (C-32 inventory only),
`tests/contract/test_script_interface_contract.py`, `test-evidence/` (three files),
`tasks.md` (four ticks). Mirrors refreshed via `sync-mirrors.py --write`; no hand edit under
`.specify/scripts` or `.specify/shared`. No change to `requirements.md`, `plan.md`, other contracts,
`data-model.md`, implementation code, the state spine, or agents.
