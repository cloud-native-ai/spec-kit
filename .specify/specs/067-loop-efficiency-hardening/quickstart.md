# Quickstart — running and measuring the slimmed suite (067)

Audience: a maintainer who did not take part in this feature and needs to run the
framework's own tests, measure a complete run, or repeat the verification drills.
Numbers cited as baseline are the dated record
`test-evidence/baseline-full-2026-10-22.md`; procedures are pinned by the contracts in
this directory.

## S1 · Run the full suite (everyday entry)

```sh
bash scripts/bash/run-tests.sh -q
```

Prerequisite: an interpreter with pytest resolvable by the runner (it tries
SPECKIT_PYTHON, then .venv/bin/python, then python3, then python, and fails loudly if
none has pytest). Exit code = pytest's result. This is the same entry the two-slot test
budget of the loop-efficiency feature uses; no flags are added by this feature.

## S2 · Measure a complete run (SC-006)

Use the fixed composite exactly as pinned in `contracts/measurement.md` (MP-02):
clear pytest/bytecode caches, then run the runner wrapped in epoch timestamps, tee the
log. Warm-up at most once, before the clear, never counted. Record every E1 field of
`data-model.md` (command, host, date, commit, cache-clear proof, epochs, wall seconds,
exit code, per-layer counts, pytest summary, log pointer) into a dated file under
test-evidence/. The budget claim needs: wall ≤ 600 s, all three layers executed,
deselected = 0, on the baseline dev host. A run with any filter flag is invalid
evidence no matter how fast.

## S3 · Name-level failure comparison (SC-008)

```sh
bash scripts/bash/run-tests.sh -q --names-out post-failed.txt
comm -13 baseline-failed.txt post-failed.txt   # NEW failure names; empty = pass
```

Baseline side: `test-evidence/baseline-failures-2026-10-22.txt` (83 names). Pinned
tests that already fail in the baseline are pre-existing debt handled by the triage
contract (FB-05/FB-06), not by this diff.

## S4 · Coverage-set audit (SC-007)

At implement start (before the first consolidation task): generate the baseline id
list with the runner-resolved interpreter, `pytest --collect-only -q`, strip summary
lines, one id per line, header records command and date. At closure: regenerate the
post list the same way, then run the LED-05 join — every id in
`comm -23 baseline-ids post-ids` must match a row in the consolidation ledger (case
rows by full id, file rows by declared prefix). Zero unmatched ids is the bar; the
join output is the audit evidence.

## S5 · Repair mirror drift (triage class 1)

```sh
python3 scripts/python/sync-mirrors.py --check --only <pair-path>   # see the drift
python3 scripts/python/sync-mirrors.py --write --only <pair-path>   # repair
```

Never repair a mirror failure by editing or deleting its test. Pairs whose canonical
sources are being changed by other in-flight features are registered as pre-existing
debt instead of synced (FB-05).

## S6 · Injection and localization drills (SC-008/SC-009)

During implement verification: pick one consolidated (parametrized) test, temporarily
break one row's assertion so it fails, run the affected test, and check (a) the
failure output names a unique node id including the parametrized row, (b) re-running
that exact node id reproduces the failure, (c) the S3 diff surfaces the injected name.
Revert the injection. Commit the drill record (commands + outputs + date) under
test-evidence/.

## S7 · Dependency-boundary check (SC-010)

```sh
git diff <base>..HEAD -- pyproject.toml          # runtime deps diff must be empty
grep -rnE "urllib|requests|httpx|socket" tests/  # only pre-existing matches allowed
```

Test-side additions must sit in the dev dependency group; no network steps in tests.

## Where the evidence lives

All dated evidence of this feature lands in
`.specify/specs/067-loop-efficiency-hardening/test-evidence/` (one file per run or
drill; machine-local raw logs stay gitignored `.log` files outside commits).
