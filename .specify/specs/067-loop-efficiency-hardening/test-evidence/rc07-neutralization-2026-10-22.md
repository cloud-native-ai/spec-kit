# RC-07 Hook Neutralization — targeted timing evidence — 2026-10-22

**Task**: T003 (implement part A) · **Mechanism**: E6 autouse fixture in `tests/conftest.py`
(`_neutralize_host_git_config`) pointing `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` at empty
per-test temp files. Host git config untouched; reversible by deleting the fixture.

## Method

- Command (both sides): `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q --durations=0`
- Host: macOS arm64 (Darwin 25.6.0), Python 3.14.6 / pytest 9.1.1 (runner-resolved `python`)
- Tree: pre = `a8a097b6` + baseline evidence; post = same + conftest fixture (conftest-only delta)
- The targeted family is the whole file: 14 test functions / 23 collected ids
  (6 boundary + 5 manifest parametrized rows).
- Baseline dated anchor: `test-evidence/baseline-durations-2026-10-22.txt` — the 18 admission
  calls in the full-run top-50 sum to 87.45 s. That figure covers only the top-50 cutoff; the
  same-command pre-change run below is the apples-to-apples family total.

## Before / after (same command)

| metric | pre-change | post-RC-07 | delta |
|---|---|---|---|
| pytest family time | 121.33 s (23 passed) | 31.71 s (23 passed) | −89.62 s (−73.9%) |
| wrapper wall clock | 122 s | 33 s | −89 s |
| call-duration sum (all entries) | 121.06 s | 31.05 s | −90.0 s |
| slowest single call | 12.22 s (`test_exit_codes_0_1_2`) | 2.78 s (`test_sensitive_or_engine_path_rejected`) | — |

## Interpretation

- The dominant pre-change cost was the host global `core.hooksPath`
  (`/Users/liuqiming.lqm/.aliyunAKScanHook/hooks`) tax on every fixture `git commit`
  (plan-probes P-4: ≈0.9 s per commit) plus per-commit hook runtime scaling with repo
  scanning. Neutralizing global config for the test process tree removed it.
- RC-07 alone lands the family at 31.71 s — above the plan §W2 design band (15–25 s);
  the remaining share is the per-case interpreter cold start of the CLI subprocesses,
  addressed by T004/T005 (in-process direct call + shared template clone) and measured at T006.

## Risk handling

- 0 of the 23 admission cases depended on global git config (all pass unchanged; every
  fixture git call passes explicit `-c user.name/-c user.email`).
- Suite-wide exposure of the neutralization is validated by the driver at T007 (implement-start
  full run). If a non-admission case is found to depend on global git config, the per RC-07
  remedy is a minimal per-case env exemption, never wholesale de-neutralization.

## Raw outputs

- Pre-change run: 23 passed in 121.33 s; call sum 121.06 s over 24 duration entries ≥0.005 s.
- Post-RC-07 run: 23 passed in 31.71 s; full stdout captured in the run record
  (`/tmp/t003-post.txt` at run time; summary lines transcribed above).
- No test is claimed green beyond these two actually-run targeted invocations.

## T006 addendum (post-T004/T005 final state, same command)

- Final targeted run at `f14c4f49`: `25 passed in 27.69s` (call sum 23.03 s). Full
  before/after table, band comparison on both bases, and overhead attribution:
  `test-evidence/w2-admission-timing-2026-10-22.md`.
- RC-07 remains in effect for the whole suite (autouse); its share of the family
  reduction (121.33 → 31.71 s before T004/T005) is the single largest contributor
  to the final 121.33 → 27.69 s result.
