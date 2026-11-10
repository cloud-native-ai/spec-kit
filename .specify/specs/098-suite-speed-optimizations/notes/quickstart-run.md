# Quickstart run — S-1…S-13 (098 Suite Speed Optimizations)

- Owner: `tasks.md` T060; scenario source `quickstart.md` (S-1…S-13).
- Date: 2026-11-11; host: the slot-1 baseline host (192 vCPU).
- Tree: `098-suite-speed-optimizations` worktree, head `ec1620289` + WP-9 evidence
  (no test-tree change after WP-8).
- Run-time output landed under `.specify/.tmp/wp9/qs/` (gitignored scratch) and was copied
  here afterwards; nothing was written under `.specify/specs` while a run was in flight
  (corpus-write hazard). Every run goes through `scripts/bash/run-tests.sh`.
- Each scenario records: command, exit code, observable output, duration, and every FAILED
  name that is not already in the slot-1 baseline (`baseline-failed.txt`) — attributed in
  place.

## S-1 — Default tier excludes exactly the marked set

```text
$ bash scripts/bash/run-tests.sh --collect-only -q
exit 0, wall 11.37 s, 8582 ids
mode: mode=parallel workers=auto dist=load passes=2 tier=fast excluded_slow=7

$ bash scripts/bash/run-tests.sh --full --collect-only -q
exit 0, wall 8.42 s, 8589 ids
mode: mode=parallel workers=auto dist=load passes=2 tier=full excluded_slow=0

$ bash scripts/bash/run-tests.sh -m slow --collect-only -q
exit 0, wall 3.16 s, 7 ids
mode: mode=parallel workers=auto dist=load passes=1 tier=caller excluded_slow=0
```

- Set comparison: `full − fast` = 7 ids = the `-m slow` set exactly; `fast − full` = 0.
  The default tier excludes exactly the marked set (SC-006 / C-002 / C-009).
- Teardown: the three id files remain under gitignored `.specify/.tmp/wp9/qs/` (scratch only).

## S-2 — Disclosure count and caller-selection priority

```text
$ bash scripts/bash/run-tests.sh tests/contract -q
exit 1, wall 69.11 s, summary 162 failed, 6756 passed, 2 skipped in 44.80 s
mode: mode=parallel workers=auto dist=load passes=2 tier=fast excluded_slow=5

$ bash scripts/bash/run-tests.sh -m contract -q
exit 1, wall 47.19 s, summary 90 failed, 5122 passed, 2 skipped in 45.77 s
mode: mode=parallel workers=auto dist=load passes=1 tier=caller excluded_slow=0

$ bash scripts/bash/run-tests.sh --full -m contract -q
exit 1, wall 45.89 s, summary 90 failed, 5122 passed, 2 skipped in 44.47 s
mode: mode=parallel workers=auto dist=load passes=1 tier=caller excluded_slow=0
```

- The default run discloses `tier=fast excluded_slow=5`; both caller `-m` runs show
  `tier=caller excluded_slow=0` and carry no second `-m` (C-003/C-009/C-010).
- Attribution: the two caller-tier runs have 0 FAILED names outside the slot-1 baseline.
  The default-tier run has two outliers, both in `tests/contract/test_trigger_engine.py`
  (whose only feature change is the c2 in-process conversion, not on these paths):
  `test_c4_format_choices_and_default` (isolated 3/3 green: 6.63 s / 6.66 s / 6.62 s) and
  `test_c11_out_of_range_vocabulary_exits_invalid` (isolated 3/3 green: 6.55 s / 6.55 s /
  6.56 s; the failure is `do_init` returning 2 with empty stderr under the auto-worker pool).
  Both passed in the slot-1 full run and are load-induced parallel-isolation flakes, not new
  regressions — 160 of the 162 names are slot-1 baseline names.
- Teardown: none (no files created outside scratch).

## S-3 — Empty-after-exclusion is a named error

- Fixture tree: `.specify/.tmp/wp9/s3-tree` — `pytest.ini` registers `serial`/`slow`/`contract`;
  one test carries `@pytest.mark.slow`.
- Command: `bash scripts/bash/run-tests.sh --workers 2 .specify/.tmp/wp9/s3-tree -q`

```text
exit=2
mode: mode=parallel workers=2 dist=load passes=1 tier=fast excluded_slow=1
error=empty-selection-after-tier-exclusion tier=fast excluded_slow=1
```

- Teardown: `rm -rf .specify/.tmp/wp9/s3-tree` after recording (executed after this file was
  written; scratch only).

## S-4 — Contract-subset parallel/serial name equality

```text
$ bash scripts/bash/run-tests.sh --workers 4 tests/contract --names-out .specify/.tmp/wp9/qs/s4-par2-names.txt -q
exit 1, wall 177 s, summary 157 failed, 6761 passed, 2 skipped in 151.74 s
mode: mode=parallel workers=4 dist=load passes=2 tier=fast excluded_slow=5

$ bash scripts/bash/run-tests.sh --serial tests/contract --names-out .specify/.tmp/wp9/qs/s4-ser-names.txt -q
exit 1, wall ≈569 s (capture files born 01:35:43.5 → finished 01:45:12.8; pytest summary 565.34 s)
summary: 159 failed, 6760 passed, 2 skipped, 5 deselected in 565.34 s (0:09:25)
mode: mode=serial reason=explicit tier=fast excluded_slow=5
```

- Both arms disclose the same selection: `tier=fast excluded_slow=5`.
- `comm -23` (parallel-only names): **0**. `comm -13` (serial-only names): **2** —
  `test_trigger_engine.py::test_c20_new_session_is_not_suppressed` and
  `::test_c21_auto_execute_is_only_a_flag`. Both are pre-existing slot-1 baseline names
  (`baseline-failed.txt` lines 154–156) and fail 3/3 in isolation (6.60–6.80 s), so they are
  stable pre-existing reds whose parallel-arm pass is the flaky direction.
- New-name judgement (the criterion's discriminating property): every name in each arm is in
  the slot-1 baseline — parallel 157/157, serial 159/159 — so **0 new failure names in either
  direction**. The raw symmetric difference flips among pre-existing baseline names between
  observations (an earlier parallel observation at 01:25 showed c15 as the only serial-only
  name; c15 is also a baseline name with isolated fail/fail/pass). No retry was used to chase
  a green pair (FR-021 forbids retry-until-green).
- The SC-002 primary record remains `test-evidence/parallel-consistency-contract.txt`
  (T015/T017: both comm directions empty on 160/160 identical names, plus the
  non-parallel-safe fixture drill). This quickstart re-run adds the final-tree check with the
  flake attribution above.
- Persisted lists: `test-evidence/quickstart-s4-parallel-names.txt`,
  `test-evidence/quickstart-s4-serial-names.txt`.
- Teardown: name lists copied; scratch remains gitignored.

### S-4 repair r1 — final-tree re-run after the fixture-isolation repair (2026-11-11)

The pre-repair readings above recorded a raw `comm -13` of 2 serial-only names in
`test_trigger_engine.py`. Review-repair r1 fixed the root cause (the engine's C-7
self-location defeated the pytest fixture in this nested worktree, so the file wrote the
parent repo's trigger store and raced/flipped across arms; see
`test-evidence/review-repair-r1-trigger-fix.txt`). Re-run on the repaired final tree:

```text
$ bash scripts/bash/run-tests.sh --workers 4 tests/contract --names-out <scratch>/s4r-par-names.txt -q
exit 1, wall 175.76 s, summary 137 failed, 6781 passed, 2 skipped in 150.68 s
mode: mode=parallel workers=4 dist=load passes=2 tier=fast excluded_slow=5

$ bash scripts/bash/run-tests.sh --serial tests/contract --names-out <scratch>/s4r-ser-names.txt -q
exit 1, wall 557.04 s, summary 137 failed, 6782 passed, 2 skipped, 5 deselected in 553.16 s
mode: mode=serial reason=explicit tier=fast excluded_slow=5
```

- `comm -13` (serial-only): **0**; `comm -23` (parallel-only): **0** — the criterion's
  reading now holds on the final tree, one run per arm, no retry.
- Both lists carry 137 names and are set-equal; the two former serial-only names
  (`test_c20_new_session_is_not_suppressed`, `test_c21_auto_execute_is_only_a_flag`) pass
  in both arms after the repair.
- Record: `test-evidence/review-repair-r1-sc002-comm.txt`; lists
  `test-evidence/review-repair-s4-parallel-names.txt` /
  `test-evidence/review-repair-s4-serial-names.txt`; logs
  `test-evidence/run-logs/review-repair-s4-parallel.log.gz` /
  `test-evidence/run-logs/review-repair-s4-serial.log.gz`.

## S-5 — Session cache build count and mutation drill

Adaptation (recorded): the default tier now excludes the five slow-marked corpus cases, so
the corpus pair is run with `--full`; the scenario's subject is the cache over the corpus
files, which requires the marked members to execute.

```text
$ bash scripts/bash/run-tests.sh --full --workers 2 tests/contract/test_coverage_receipt.py tests/contract/test_clause_coverage.py -q
exit 1, wall 16.43 s, summary 2 failed, 62 passed in 14.92 s
FAILED: test_c5_gate_budget_is_unchanged_by_the_owner_document,
        test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census
        — both slot-1 baseline names (0 new)

$ bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_scan_cache_contract.py -q
exit 0, wall 2.42 s, summary 7 passed in 0.68 s
```

- The counted probe (`build_count` / `traversals`) and the before/after equivalence pair are
  in `test-evidence/cache-counts.txt` (T028); the cross-session tamper drill is inside the
  guard. Teardown: none.

## S-6 — Fixed-sleep scan

```text
$ bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_event_wait_contract.py -q
exit 0, wall 2.24 s, 8 passed in 0.50 s
mode: mode=parallel workers=2 dist=load passes=1 tier=fast excluded_slow=0
```

The guard's AST zero-synchronization-sleep scan over the six scope files is green (SC-008).

## S-7 — Ordering determinism without real time

```text
$ bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_client_metrics.py -q
exit 0, wall 3.63 s, 16 passed in 1.86 s
```

Pre-change reading on the same host/day/worker count: exit 0, wall 8.11 s, `16 passed in
6.76 s` (base tree, `notes/pre-change-measurements.md` §3). Same 16 cases; the eight 1.1 s
ordering sleeps are gone.

## S-8 — In-process conversion manifest guard

```text
$ bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_inprocess_conversion_contract.py -q
exit 0, wall 6.22 s, 9 passed in 4.47 s
```

The guard covers the complete manifest, the closed keep-class set and the revert-red leg
(SC-009); conversion evidence is `test-evidence/inprocess-equivalence.txt` /
`inprocess-mutations.txt`.

## S-9 — Two-slot commands request the full tier

```text
$ grep -n 'run-tests.sh' .specify/skills/sdd-loop-driver/references/efficiency-model.md | sed -n '1,4p'
91:| `baseline` | ... | `run-tests.sh --full --names-out <spec-dir>/baseline-failed.txt`，按名称捕获失败名单 |
92:| `closure` | ... | `run-tests.sh --full --names-out <spec-dir>/final-failed.txt`，`comm -13` 名称级比较 |

$ grep -n 'run-tests.sh' .specify/skills/sdd-loop-driver/references/stage-prompts.md | sed -n '1,6p'
165:  bash scripts/bash/run-tests.sh --full --names-out <spec-dir>/baseline-failed.txt
206:  bash scripts/bash/run-tests.sh --full --names-out <spec-dir>/final-failed.txt
```

Both slot rows and both dispatched restatements carry `--full` (FR-010); the runtime mirror
is the copy the driver reads.

## S-10 — Forbidden-shortcut scan

```text
$ git diff --name-only b3da3a26d..HEAD -- tests/ | xargs -r grep -nE '@pytest\.mark\.(skip|xfail)|pytest\.skip\(|xfail\('
15 hits — all pre-existing forms in changed files (plus one function-name false positive,
test_c006_a_timeout_is_never_converted_to_skip_or_xfail); none is an added line.
$ git diff b3da3a26d..HEAD -- tests/ | grep -cE '^\+\s*@pytest\.mark\.parametrize'
1   (one added parametrize decorator in the new tier contract; removals: 0)
```

The authoritative added-line + base-vs-HEAD AST scan is `test-evidence/forbidden-shortcuts.txt`:
zero new skip/skipif/xfail/retry decorators, zero new in-function skip/xfail calls, zero new
conditional skips, zero retry-until-green loops, zero parametrize removals, no
worker-resolution drift (SC-010). A re-run reproduced the recorded scan verbatim.

## S-11 — Runner interface unchanged

```text
$ bash scripts/bash/run-tests.sh --help | grep -- --full
usage: run-tests.sh [--names-out <file>] [--full] [pytest arguments...]
  --full                                  (exit 0)
$ bash scripts/bash/run-tests.sh --version
run-tests.sh 0.0.22                       (exactly one line, exit 0)
$ bash scripts/bash/run-tests.sh --definitely-undeclared
exit=4; pytest rejects the undeclared argument (non-zero)
```

Complete transcript: `test-evidence/interface-evidence.txt` (T058). The 086 runner contract
suite (40 cases) is green in `test-evidence/tier-contract-green.txt`.

## S-12 — Full-selection non-regression

```text
$ bash scripts/bash/run-tests.sh --serial --full --collect-only -q
exit 0, wall 2.95 s, 8589 tests collected
```

Comparison against the implement-start id set (`notes/pre-change-measurements.md`,
`implement-start-full-ids` block, 8543 ids, tree root normalized):

- removed: **0**; added: **46** — exactly the five new contract files:
  event-wait 8, inprocess-conversion 9, parallel-consistency 4, scan-cache 7, suite-tier 18.
- Disposed list: `test-evidence/full-collection-disposed.txt` (no per-test dispositions).
  Full record: `test-evidence/full-collection-diff.txt` (T022).

## S-13 — Tier wall-clock ratio and anti-measurement

All readings are same tree, same host, same day. No additional full run was started
(FR-020 / A9 / A14); the full-tier leg is the slot-1 baseline run itself.

| leg | command | exit | wall | summary |
|-----|---------|------|------|---------|
| full tier (slot 1) | `bash scripts/bash/run-tests.sh --full --names-out .specify/.tmp/wp9/baseline-failed.txt` | 1 | 70.99 s | `287 failed, 8299 passed, 2 skipped in 47.55 s` |
| default parallel | `bash scripts/bash/run-tests.sh -q` | 1 | 73.42 s | `282 failed, 8297 passed, 2 skipped in 47.03 s` |
| default serial | `bash scripts/bash/run-tests.sh --serial -q` | 1 | 692.15 s | `268 failed, 8312 passed, 2 skipped, 7 deselected in 687.34 s` |

- Selection equality (the two `--collect-only` readings): parallel 8582 ids and
  `--serial` 8582 ids, both `tier=fast excluded_slow=7`; set difference 0 in both directions.
- Ratio: `73.42 / 692.15 = 0.1061` → **10.6 %**, inside the required **≤ 50 %** (SC-004).
- Scope disclosure (T055): the default-vs-full raw walls are `73.42 s` (fast, 8582 selected)
  vs `70.99 s` (full, 8589 selected) — a selection difference plus run noise, never an
  efficiency claim. The anti-measurement re-merges the marked set into the default tier,
  i.e. reproduces the full selection whose wall is the slot-1 reading; the observed change
  `+2.43 s` is a selection-difference observation, not a regression.
- Outlier attribution (default parallel): its 282 names are 281 slot-1 baseline names plus
  `tests/integration/test_trigger_promotion.py::test_invalid_environment_threshold_is_ignored`
  — the file is untouched by this feature, the case passed in the slot-1 full run and in the
  serial arm, and passes 3/3 isolated re-runs (6.55 s / 6.28 s / 6.26 s). The serial arm's
  268 names are all slot-1 baseline names (0 new).
- Complete outputs: `test-evidence/run-logs/slot1-full.log.gz`,
  `test-evidence/run-logs/default-parallel.log.gz`,
  `test-evidence/run-logs/default-serial.log.gz`.

## Teardown

- Removed: `.specify/.tmp/wp9/s3-tree` (S-3 fixture), after its output was recorded above.
- Retained only as gitignored scratch: `.specify/.tmp/wp9/` (id lists, raw logs, scan script);
  every durable reading has been copied into `notes/` or `test-evidence/` before this record
  was finalized.
- No tracked file was modified by any scenario; no pytest cache or corpus write landed under
  `.specify/specs/` during a run (corpus-write hazard respected).
- Post-run verification (GATE-5's exact targeted command, not a quickstart scenario):
  `bash scripts/bash/run-tests.sh tests/contract/test_suite_tier_contract.py tests/contract/test_parallel_consistency_contract.py tests/contract/test_scan_cache_contract.py tests/contract/test_event_wait_contract.py tests/contract/test_inprocess_conversion_contract.py -q`
  → exit 0, `46 passed in 18.41 s`, `tier=fast excluded_slow=0`.

## Anomaly line

- S-4's raw bidirectional diff is non-empty by two pre-existing baseline names (attributed
  above; no retry was used, no new failure name exists in either arm). S-2's default-tier run
  has two load-induced flakes outside the baseline (attributed above). No other anomaly and no
  in-passing repair was applied.
