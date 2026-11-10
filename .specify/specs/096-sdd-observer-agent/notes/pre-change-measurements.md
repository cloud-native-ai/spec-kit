# Pre-change measurements — 096-sdd-observer-agent

One entry per measurement: value · re-derivation command · capture date. Written by the
sequential Setup rows T002 (guard baselines) and T005 (coverage baseline re-freeze); no
other row writes this file.

## Guard baselines (T002)

Capture date: 2026-11-10 (implement entry, worktree `096-sdd-observer-agent`, base `c9b86e7fa4d2`).

### Mirror baseline — `python3 scripts/python/sync-mirrors.py --check` — expect exit 0

Value: **exit 0** (`ok shared/ == .specify/shared/ (111 files, byte-identical)`).

```text
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (111 files, byte-identical)
exit=0
```

Re-derivation: `python3 scripts/python/sync-mirrors.py --check` · capture 2026-11-10.

### Driver-skill guard baseline — `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` — expect 25 passed

Value: **25 passed** (parallel pass; the runner's second pass runs the 1 declared serial test: `1 passed, 25 deselected`).

```text
# test runner exceptions: 1 declared serial test(s)
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_sdd_loop_driver_skill.py -q
# test runner: mode=parallel workers=auto dist=load passes=2
bringing up nodes...
bringing up nodes...

.........................                                                [100%]
25 passed in 6.14s
.                                                                        [100%]
1 passed, 25 deselected in 16.23s
exit=0
```

Re-derivation: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` · capture 2026-11-10.

### Fast-fail guard baseline — `bash scripts/bash/run-tests.sh tests/contract/test_fast_fail_discipline.py -q -k "i10 or i11"` — expect 2 passed

Value: **2 passed**.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_fast_fail_discipline.py -q -k i10 or i11
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

..                                                                       [100%]
2 passed in 6.22s
exit=0
```

Re-derivation: `bash scripts/bash/run-tests.sh tests/contract/test_fast_fail_discipline.py -q -k "i10 or i11"` · capture 2026-11-10.

## Coverage baseline re-freeze (T005)

Capture date: 2026-11-10 (implement entry). Command:

```text
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs --freeze > .specify/specs/096-sdd-observer-agent/coverage-baseline.txt
exit=0
```

- **base-sha (new header)**: `c9b86e7fa4d2` (was `c691d658a426` at the tasks-stage freeze).
- **frozen names**: 640 → 640, body byte-identical — delta **0 added / 0 removed** (`LC_ALL=C comm -13` and `comm -23` on the name-only bodies both empty; `cmp` equal).
- **header delta**: only `base-sha` advanced; `files: 286 (parsed 179 + named 107)` unchanged.
- **live re-check against the re-frozen baseline** (read-only, no `--freeze`):
  `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` → `exit=0`, `status: ok`,
  `[clause-uncovered] pass (640) — 640 uncovered, 0 beyond the frozen baseline`,
  `[fr-uncovered] pass (0) — 23 of 23 FRs cited from citation groups`,
  `[coverage-baseline-delta] pass (0)`; the single `[clause-unparsable] fail (107)` warning is the pre-existing corpus-level parse-doubt reading already disclosed by the analyze stage (E-01 carrier; 1 warning).

Re-derivation: `bash` re-run of the two commands above · capture 2026-11-10.
