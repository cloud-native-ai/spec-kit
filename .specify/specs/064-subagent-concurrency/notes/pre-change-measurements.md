# Pre-Change Measurements — Feature 064 (implement, 2026-10-20)

Recorded before any source edit, in this worktree (`064-subagent-concurrency`).

| Premise | Command actually run | Measured result |
|---|---|---|
| Skill mirror baseline | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | exit 2; 3 DIFF: `SKILL.md`, `references/dispatch-recipes.md`, `references/watch-model.md` |
| Shared definitions baseline | `python3 scripts/python/sync-mirrors.py --check --only shared/definitions` | exit 2; 9 DIFF: `agent-definitions.md`, `contract-clause-definitions.md`, `derivation-definitions.md`, `dogfooding-definitions.md`, `framework-map.md`, `goal-definitions.md`, `self-improvement-definitions.md`, `subagent-definitions.md`, `tool-definitions.md` |
| Watcher self-test baseline | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | exit 1; `SELF-TEST: 12 passed, 4 failed`; failures: `pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced` (macOS platform degradation, same as 063 baseline) |
| Probe registry baseline | `python3 .specify/scripts/python/probe-utils.py --action probes --validate` | exit 0; `Probe registry valid: 10 classes, 113 internal + 0 external objects`; no `skill:sdd-loop-driver` object |
| Compiled embeds baseline | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` | exit 0; `compile-embeds --check: 74 units, zero drift` |
| SKILL H2 baseline | `grep -c '^## ' skills/external/sdd-loop-driver/SKILL.md` | `11` |
| Planned test files | explicit `[ -e ]` loop over the 10 planned paths | 9 absent; only `tests/contract/test_sdd_loop_driver_skill.py` present (1/10) |
| Toolchain | `python3 --version`; `git --version`; `command -v setsid`; `command -v nohup`; `python3 -c 'import fcntl'` | Python `3.9.6`; git `2.54.0 (Apple Git-157)`; `setsid` absent; `nohup` at `/usr/bin/nohup`; `fcntl ok` |
| pytest availability | `python3 -m pytest --version` | `No module named pytest` for the system interpreter |
| pytest via runner | `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` | runner resolves the interpreter; `21 passed, 2 failed` (the two mirror-drift pins match the 3-file baseline; red is not a feature regression) |

**Correction (recorded at the measurement point, not a decision):** the tasks/plan premise "pytest unavailable everywhere" is falsified — a pytest-capable interpreter exists at `/Users/liuqiming.lqm/project/profiles/.venv/bin/python3` (pytest 9.1.1). All test executions in this run use `scripts/bash/run-tests.sh` with `SPECKIT_PYTHON` set to it, so green is observed rather than `Unobserved`. The system `python3` remains pytest-free; the runner's loud-fail contract is unchanged.

**Trap forms honoured:** mirror `--check` legitimately exits 2 at baseline; the count of `DIFF` lines (3 and 9) is the comparison basis, never the exit code.

T002 name-level baseline: see `baseline-failed.txt` (produced by `run-tests.sh tests -q --names-out …`).
