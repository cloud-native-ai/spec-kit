# Quickstart — 098 Suite Speed Optimizations

**Purpose**: the verification scenarios implement and review will run, each with the exact command, the
observable it proves, and its premises. Commands are written against the artifacts this feature creates;
every scenario that is not yet executable carries a per-example disclaimer naming the premises it rests on
(re-probe these at implement; do not inherit them).

## S-0 — Already measured at plan time (real output)

| id | command | output | exit |
|----|---------|--------|------|
| S-0.1 | `python3 -m pytest --collect-only -q` | `8543 tests collected` | 0 |
| S-0.2 | `python3 -m pytest --collect-only -q -m slow` | `no tests collected (8543 deselected)` | 5 |
| S-0.3 | `bash scripts/bash/run-tests.sh --workers 4 tests/contract/test_run_tests_runner_contract.py -q` | `40 passed in 13.90s` | 0 |
| S-0.4 | `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_client_metrics.py -q` | `16 passed in 6.62s` | 0 |
| S-0.5 | `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_coverage_receipt.py tests/contract/test_clause_coverage.py -q` | `2 failed, 62 passed in 31.92s`; failures `test_c5_gate_budget_is_unchanged_by_the_owner_document` and `test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census` are pre-existing baseline names | 1 |
| S-0.6 | session fixture probe: 3 tests on `-n 2` with a session-scoped build marker | 2 builds (`gw0`, `gw1`) | 0 |
| S-0.7 | the same corpus pair run while the harness `tee`d its own output into `.specify/specs` | `3 failed` including `test_c20` (md5 before/after differ); kept as the hazard record, not as baseline | 1 |

Full transcripts: `test-evidence/plan-baseline-probe.txt`, `runner-contract-pretest.txt`,
`targeted-pretest-baseline.txt`, `session-fixture-probe.txt`, and the hazard record
`corpus-write-hazard.txt` (S-0.7).

## S-1 — Default tier excludes exactly the marked set

```bash
bash scripts/bash/run-tests.sh --collect-only -q > /tmp/fast-ids.txt
bash scripts/bash/run-tests.sh --full --collect-only -q > /tmp/full-ids.txt
python3 -m pytest --collect-only -q -m slow > /tmp/slow-ids.txt
comm -13 /tmp/fast-ids.txt /tmp/full-ids.txt   # MUST equal the slow id set
```

Proves SC-006 / TS-02, TS-09, SL-06. **Run status at plan time**: not executable — `--full` and the
default exclusion do not exist yet. Premises: the runner gains `--full`; `--collect-only -q` is forwarded
to pytest unchanged; collection is the same in both runs (no test bodies execute).

## S-2 — Disclosure count and caller-selection priority

```bash
bash scripts/bash/run-tests.sh tests/contract -q 2>&1 | grep 'mode='
bash scripts/bash/run-tests.sh -m contract -q 2>&1 | grep 'mode='
bash scripts/bash/run-tests.sh --full -m contract -q 2>&1 | grep 'mode='
```

Proves TS-03/04/09/10: default run shows `tier=fast excluded_slow=<measured>`; a caller `-m` shows
`tier=caller excluded_slow=0` and no second `-m`. **Run status at plan time**: not executable. Premises:
mode-line fields are appended (086 C-002 prefix kept); the marker enumeration accepts a caller selection.

## S-3 — Empty-after-exclusion is a named error

```bash
# fixture tree where every test is marked slow
bash scripts/bash/run-tests.sh --workers 2 <fixture-tree> -q; echo "exit=$?"
```

Proves TS-11: stderr carries `error=empty-selection-after-tier-exclusion tier=fast excluded_slow=<n>` and
exit is 2. **Run status at plan time**: not executable. Premises: fixture tree registers both `serial` and
`slow` markers; the enumeration count is greater than zero.

## S-4 — Contract-subset parallel/serial name equality

```bash
bash scripts/bash/run-tests.sh --workers 4 tests/contract --names-out /tmp/c-par.txt -q
bash scripts/bash/run-tests.sh --serial tests/contract --names-out /tmp/c-ser.txt -q
comm -13 /tmp/c-par.txt /tmp/c-ser.txt   # MUST be empty
comm -23 /tmp/c-par.txt /tmp/c-ser.txt   # MUST be empty
```

Proves SC-002 / PC-02/03/06. **Run status at plan time**: runnable in form, but the comparison is
evidence for the implemented runner; take it after implement. Premises: both lists come from the same
tree; `--names-out` is written after the passes (a name list is not written mid-run).

## S-5 — Session cache build count and mutation drill

```bash
bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_coverage_receipt.py tests/contract/test_clause_coverage.py -q
bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_scan_cache_contract.py -q
```

Proves SC-007 / CA-07, CA-10, CA-11. The guard test records `build_count` and `traversals` and runs the
tmp-corpus cross-session drill. **Run status at plan time**: not executable (fixture and guard do not
exist). Premises: `account()` is importable in-process with `_corpus_files` monkeypatchable; xdist gives
each worker its own session scope (S-0.6).

## S-6 — Fixed-sleep scan

```bash
bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_event_wait_contract.py -q
```

Proves SC-008 / EW-02, EW-03, EW-09. **Run status at plan time**: not executable (guard does not exist;
scope files still carry the counted sleeps in S-0/`plan-baseline-probe.txt`). Premises: the scope file list
of EW-01 is final; the exemption registry names the two unit-test files; the guard parses the scope files
with Python's AST (no textual heuristic).

## S-7 — Ordering determinism without real time

```bash
bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_client_metrics.py -q
```

Proves FR-015 / EW-04, EW-05; the before/after wall pair is recorded in `test-evidence/`. **Run status at
plan time**: not executable as the converted form; the current baseline is S-0.4. Premises: `--now` is
accepted by `feedback-utils.py` and `--help` documents it; owner-file mtimes are set explicitly by the
tests.

## S-8 — In-process conversion manifest guard

```bash
bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_inprocess_conversion_contract.py -q
```

Proves SC-009 / IC-05…IC-09. **Run status at plan time**: not executable. Premises: the AST scan
enumerates `tests/**/*.py` and `tests/conftest.py`; the manifest is complete for that denominator.

## S-9 — Two-slot commands request the full tier

```bash
grep -n 'run-tests.sh' .specify/skills/sdd-loop-driver/references/efficiency-model.md | sed -n '1,4p'
grep -n 'run-tests.sh' .specify/skills/sdd-loop-driver/references/stage-prompts.md | sed -n '1,6p'
```

Proves FR-010: both slot rows and both stage-prompt restatements carry `--full`. **Run status at plan
time**: not executable as written (the update is an implement deliverable); the current rows are recorded
in `research.md` B-10. Premise: the skill mirror is regenerated after the edit
(`scripts/python/sync-mirrors.py --write --only skills/external`).

## S-10 — Forbidden-shortcut scan

```bash
git diff --name-only <stage-base>..HEAD -- tests/ | xargs -r grep -nE '@pytest\.mark\.(skip|xfail)|pytest\.skip\(|xfail\('
git diff <stage-base>..HEAD -- tests/ | grep -cE '^\+\s*@pytest\.mark\.parametrize'
```

Proves SC-010 / FR-021: zero new skip/xfail decorators; parametrize additions are inspected (removals MUST
be zero). **Run status at plan time**: not executable (no delta yet). Premise: `<stage-base>` is the
implement-stage base commit recorded in the spine.

## S-11 — Runner interface unchanged

```bash
bash scripts/bash/run-tests.sh --help | grep -- --full
bash scripts/bash/run-tests.sh --version
bash scripts/bash/run-tests.sh --definitely-undeclared; echo "exit=$?"
```

Proves SC-011 / TS-05, TS-12: help lists `--full`; version answers one line; the undeclared option exits
non-zero. **Run status at plan time**: not executable as written — the `--help`/`--version` legs work
today but do not yet list `--full`, and the undeclared-option leg exits non-zero today without a recorded
transcript. Premises: the script-interface guard wraps the runner; `--full` is added to the usage string
only; `--version` keeps one machine-readable line.

## S-12 — Full-selection non-regression

```bash
bash scripts/bash/run-tests.sh --full --collect-only -q > /tmp/full-after.txt
# baseline: the implement-start baseline slot's full-tier collection reading
python3 - <<'PY'
from pathlib import Path
after = set(Path('/tmp/full-after.txt').read_text().split())
before = set(Path('/tmp/full-baseline.txt').read_text().split())
print("removed:", sorted(before - after))
print("added:", sorted(after - before))
PY
```

Proves SC-001 / TS-15: `removed` equals the recorded disposed list (normally empty) and `added` equals the
tests this feature adds. **Run status at plan time**: not executable (`--full` does not exist; the baseline
reading is taken at implement start). Premises: both readings come from the same runner and the same tree;
the disposed list is written per test in `test-evidence/`.

## S-13 — Tier wall-clock ratio and anti-measurement

```bash
bash scripts/bash/run-tests.sh --names-out /tmp/base-full.txt -q           # baseline slot (full tier, by construction of the slot command)
bash scripts/bash/run-tests.sh --full --names-out /tmp/after-full.txt -q   # full tier after the change
bash scripts/bash/run-tests.sh -q                                          # default tier after the change
# record durations of all three; record the anti-measurement: default tier with the marked set re-merged
```

Proves SC-004 / SC-005 / TS-16: default-tier wall ≤ 50 % of baseline, full-tier wall ≤ 110 % of baseline,
same host/day/shape; the anti-measurement shows the default tier regresses when marked tests are re-merged.
**Run status at plan time**: not executable (default tier does not exist; the baseline slot is
implement-start). Premises: the baseline slot command includes `--full` (WP-3); measurement uses
`date`-based wall capture with command, exit code and complete output recorded; no third full run is added
for measurement.
