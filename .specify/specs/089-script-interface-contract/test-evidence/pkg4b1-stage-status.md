# PKG-4b1 stage status (partial completion, 2026-11-07)

## Done and verified

- `scripts/bash/script-interface.sh` — sourceable guard library (T055).
- `scripts/bash/generate-instructions.sh` — guard before `source common.sh` and before any write (T057).
- 12 command scripts under `scripts/bash/` — `main()` entry + guard; `bash -n` clean; 17 representative calls byte-identical against a pre-wrap copy (zero regression captured).
- `scripts/python/script_interface_cli.py` — `VersionAction` + pre-parse guard; 36 `scripts/python/*.py` carry `--version` (T056/T060 version limb).
- `scripts/bash/common.sh` and `scripts/bash/common-todo.sh` — adjudication A: applicable by FR-009, direct-invocation-only guard; sourcing with `--help` in the caller's args now survives and still publishes the helper functions; `--help`/`--version` exit 0, unknown options exit 2.
- `scripts/python/clause_extract.py` — `-h`/`--help` now exits 0 with the four labels; `--version` one line; unknown option exits 2.
- `sync-mirrors.py --check` exits 0; contract suite `tests/contract/test_script_interface_contract.py` = 61 passed.

## Open (blocks T060 completion)

1. **Python help epilogue missing the four labels** — sample `sync-mirrors.py --help` reports help=False. Argparse supplies `usage`/`options` but not `side-effects`/`exit-codes`. All 36 argparse scripts need the closed-set labels (owner page § 2) added to their help body/epilog.
2. **`generate-instructions.sh` help-wins probe fails** — probe observed `--help --write` exit 2 because the declared write-triggering option is not one the script accepts; the declaration (or the probe rule for a no-option action) needs aligning.
3. **`run-tests.sh` (declared passthrough)** — `recognized_does_not_rescue` is False by design (tokens are forwarded to pytest). Needs the checker/contract treatment per adjudication B, recorded as a contract-test leg.
4. **`clause_extract.py` precedence** — `--version --bogus` answers `--version` (exit 0) and rescues the unknown token; C-9 prefers rejecting the unknown token.


## Completion (2026-11-07)

All four open items are closed: every argparse script now emits the four closed-set labels; a script with no
write-triggering option reports `not applicable / no-write-option`; a declared-passthrough wrapper is compliant
with basis `passthrough`; `guard_argv()` validates all tokens before answering a flag. Sample probe over the four
previously-red classes: `violations=0`, exit 0. Contract suite + helper unit tests: 94 passed.
