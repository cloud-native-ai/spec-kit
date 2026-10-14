# Pre-Change Measurements — 057-decompose-command-skills

变更前基线(冻结测量;implement 起点实测 2026-10-14,与 tasks.md Phase 2 preamble 及 plan.md § Technical Context 一致)。回归网判据:名字级——`comm -13 baseline-failed.txt current-failed.txt` 为空。**在 T020 之前,回归网排除 `tests/contract/test_run_skills_wiring.py`**(红先行预期红,不构成回归)。

| # | 命令 | 实测输出(2026-10-14) |
|---|------|----------------------|
| 1 | `python3 scripts/python/sync-mirrors.py --check` | EXIT=2;恰 1 条既有 DIFF:`.specify/skills/git-workspace/scripts/git_fleet.py`(不在本特性触及对上) |
| 2 | `python3 .specify/scripts/python/scan-confirmation-gates.py` | blocking confirmation gates: 23(16 destructive + 7 governance_kept);violations 0 |
| 3 | `python3 scripts/python/probe-utils.py --action compile-embeds --check` | 69 units, zero drift |
| 4 | `python3 scripts/python/regen-command-copies.py --check` | OK: all per-tool command copies match the source templates. |
| 5 | `scripts/bash/run-tests.sh --names-out <spec-dir>/baseline-failed.txt` | 4 failed, 3718 passed, 109.85s;baseline-failed.txt 4 条(含 test_trigger_engine.py::test_c2_sync_mirrors_check_clean——既有镜像漂移的既有红,与本特性无关) |

相对判据:改后 (1) DIFF 仍恰该 1 条;(2) total 仍 23;(3) 71 units 零漂移;(4) 仍 OK;(5) 名字级差集为空。
