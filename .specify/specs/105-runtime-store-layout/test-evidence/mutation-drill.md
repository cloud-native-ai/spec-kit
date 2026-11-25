# Mutation drills — 105 runtime-store-layout

One entry per drill: the mutation, the guard function it must turn red, the real output, and the
restore reading. Restore proof is an exact reverse substitution plus a `sha256sum` equality against
the pre-drill checksum (the touched files already carry this feature's edits, so an empty `git diff`
is not the right oracle here — the checksum is), plus a re-run of the same guard function.

The four L-5 drills were declared by T025 and executed in T032; T036's two US6 drills merge below
them.

Drill declarations (L-5 item 4 / `contracts/live-reference-migration.contract.md`):

- **D1 — unlisted file (mutation)** — copy the retired-root literal into an unlisted live file of a
  measured product class; `test_product_class_occurrence_sets_equal_the_allowlist` MUST turn red
  naming that file.
- **D2 — unlisted file (restore)** — exact reverse substitution; the same function MUST turn green
  and the checksum MUST equal the pre-drill value.
- **D3 — unlisted line (mutation)** — place the literal on an unlisted line of an allowlisted file
  (a free comment line in `scripts/python/anchor-layout-migrate.py`); the function
  `test_allowlisted_files_keep_only_allowed_lines` MUST turn red naming that line.
- **D4 — unlisted line (restore)** — exact reverse substitution; the same function MUST turn green
  and the checksum MUST equal the pre-drill value.

## D1 — unlisted file (red) — 2026-11-25

- Mutation: appended `<!-- drill probe: .specify/memory/drill-probe -->` to
  `shared/guidelines/todo-in-context.md` (a measured current-guideline file, not allowlisted).
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_store_layout_live_refs.py::test_product_class_occurrence_sets_equal_the_allowlist -q`
- Exit code: **1**
- Output: `AssertionError: framework-source: unexpected=['shared/guidelines/todo-in-context.md'] missing=[]` — `1 failed in 6.23s`

## D2 — unlisted file restore (green) — 2026-11-25

- Restore: exact reverse substitution (the marker line removed; `grep -c 'drill probe'` = 0).
- Checksum: pre-drill `sha256sum` equals post-restore (`sha_equal=yes`).
- Same command as D1 → `1 passed in 6.22s`, exit **0**.

## D3 — unlisted line (red) — 2026-11-25

- Mutation: inserted `PROBE_DRILL = ".specify/memory/drill-probe"` after `import argparse` in the
  allowlisted `scripts/python/anchor-layout-migrate.py` (the line carries no legacy context).
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_store_layout_live_refs.py::test_allowlisted_files_keep_only_allowed_lines -q`
- Exit code: **1**
- Output: `AssertionError: scripts/python/anchor-layout-migrate.py: the literal escaped its allowed lines (L-5): [(22, 'PROBE_DRILL = ".specify/memory/drill-probe"')]` — `1 failed in 6.23s`

## D4 — unlisted line restore (green) — 2026-11-25

- Restore: exact reverse substitution (`grep -c 'PROBE_DRILL'` = 0); checksum equals the pre-drill
  value (`sha_equal=yes`); `py_compile` exit 0 on the restored file.
- Same command as D3 → `1 passed in 6.23s`, exit **0**.
