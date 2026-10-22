# Plan-Stage Timing Probes — 2026-10-22 (P3-plan-test-slimming)

Dated record of every probe executed during the plan stage to verify the
"why slow" hypotheses designed in `../plan.md`. No full-suite run happened;
exactly one targeted pytest probe with 2 node ids was executed (within the
≤3-node-id budget). The two probed tests happened to pass; that fact is
recorded here as a probe observation ONLY — it is not green evidence for any
scope claim, and no unexecuted test is claimed as run anywhere.

## P-1 · Runner interpreter resolution (no test run)

- `bash scripts/bash/run-tests.sh --help` → header line
  `# test runner: python -m pytest --help`; resolved `python` =
  `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` (Python 3.14.6,
  pytest 9.1.1). The repo-local `.venv/bin/python` exists but has no pytest
  (`No module named pytest`, 0.066 s), so the runner's resolve order falls
  through to PATH `python`.

## P-2 · Targeted timing probe (2 node ids, allowed budget)

Command (verbatim):

```
time (/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest \
  "tests/unit/test_admission_check.py::test_medium_fixture_admitted" \
  "tests/unit/test_admission_check.py::test_sensitive_or_engine_path_rejected" \
  -q --durations=0 -p no:cacheprovider --no-header)
```

- Result: `2 passed in 12.76s` (probe observation only).
- Durations: `test_sensitive_or_engine_path_rejected` call 9.62 s;
  `test_medium_fixture_admitted` call 2.93 s; setup 0.01 s.
- Process CPU for the whole probe: user 1.13 s + sys 1.43 s ≈ 2.6 s against
  13.2 s wall → the cost is WAITING, not computation. Consistent with
  per-subprocess spawn overhead, not with algorithmic cost inside
  `admission-check.py`.

## P-3 · Per-process spawn microbenchmarks (no test run)

| Probe | Command loop | Wall |
|---|---|---|
| Empty process | 5 × `/usr/bin/true` | 0.049 s (~10 ms each) |
| Git CLI | 5 × `git --version` | 0.146 s (~29 ms each) |
| Interpreter start | 3 × `python -c pass` | 0.165 s (~55 ms each) |

Plain spawn costs are small — they alone cannot explain 3–9 s per
admission-check test. The remaining cost is identified in P-4.

## P-4 · Git commit hook tax on this host (no test run)

The host has a GLOBAL `core.hooksPath = /Users/liuqiming.lqm/.aliyunAKScanHook/hooks`
(a security scanner; four hook scripts run per commit: pre-commit,
prepare-commit-msg, commit-msg, post-commit, each logging `Running git hook`).

Measured on a throwaway fixture repo in /tmp:

| Operation | Wall |
|---|---|
| `git commit --allow-empty -m probe-with-hooks` | **0.96 s** |
| same + `-c core.hooksPath=/dev/null` | **0.077 s** |

≈ 0.9 s of pure hook overhead per fixture commit. Static scan of the suite:
52 `"commit"` call sites across 30+ test files spawn git commits in fixture
repos (plus engine scripts invoked by tests that commit inside those repos),
which places the hook tax across the whole slow-test families listed in the
baseline (admission_check builds 2–3 commits per test; worktree queue and
store-state merge build several; audit_plan_changes is multi-commit).

## P-5 · Static structure scans (no test run)

- Mirror byte-identity/parity style: 44 test functions matching
  `byte_identical|byte-identical|mirror.*identical|mirror parity|byte_equivalent`
  across ~40 files under `tests/contract/`.
- Pair authority: `scripts/python/sync-mirrors.py` owns the pair table
  (`MIRROR_PAIRS` + `compare_pair()`; `--check` exit 2 on drift) — a shared
  parametrized suite can derive its table from the engine instead of
  restating pairs (Tool Reuse / one source of truth).
- In-process engine import pattern already exists in the suite
  (`importlib.util.spec_from_file_location` in 5+ test files), so
  direct-call fixtures are an established pattern, not a new invention.
- `skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`
  spawns a `sleep 30` keeper process (self-test case 6) and several
  real-time grace windows; the script is outside this spec's delivery
  surface, so that 28.21 s case is treated as fixed cost (see plan.md W2).

## Boundary statement

This record contains no full-suite measurement, no pass/fail claim about the
suite, and no claim that any unexecuted test passes. The authoritative
pre-change numbers remain the baseline dated record
(`test-evidence/baseline-full-2026-10-22.md`).
