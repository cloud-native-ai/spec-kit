# Overlap Adjudication — Feature 070 (plan stage)

**Date**: 2026-10-24
**Command**: `python3 /home/agent/sdd-070/tools/overlap-check.py --spec-dir .specify/specs/070-subagent-task-teams --repo .`
**Result**: exit 1 (`decision=overlap`), 21 relations, 61 specs checked, 6 current delivery paths.
**Raw records**: `test-evidence/overlap-plan.json` (machine), `test-evidence/overlap-plan.txt` (stdout + stderr).

## Why this note exists

The deterministic check compares path strings, not time. Feature 070 adds two sections to files that ten predecessor features already edited, and four new files under a directory that one predecessor declared as a whole. All predecessors are merged into the base history (`master` at `76ce86a0`); 070 is the only active line in this worktree. The check therefore reports the historical surface, not a live collision. This note adjudicates every relation and states the ownership disposition.

A literal `clear` is not achievable for an honest full-surface declaration. Narrowing the declaration to new files only would hide the two modified files and produce a green check that would not turn red if a real collision appeared — the Fast Fail anti-pattern. The plan keeps the full declaration and records the adjudication.

## Current delivery paths (declared in `feature-ref.md`)

1. `docs/reference/skills/sdd-loop-driver.md` (modified)
2. `skills/external/sdd-loop-driver/SKILL.md` (modified)
3. `skills/external/sdd-loop-driver/references/decomposition-model.md` (new)
4. `skills/external/sdd-loop-driver/scripts/wp-gate.py` (new)
5. `skills/external/sdd-loop-driver/scripts/wp-report.py` (new)
6. `skills/external/sdd-loop-driver/templates/stage-team-preset.md` (new)

## Relations

| # | Other spec | Relation | Current path | Other path |
|---|------------|----------|--------------|------------|
| 1 | `056-probe-handler-system` | `nested-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference` |
| 2 | `058-sdd-loop-driver` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 3 | `058-sdd-loop-driver` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 4 | `059-exec-quant-recording` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 5 | `060-decompose-subagent-dispatch` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 6 | `060-decompose-subagent-dispatch` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 7 | `062-humanize-command` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 8 | `063-review-p1-governance` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 9 | `074-sdd-loop-efficiency` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 10 | `074-sdd-loop-efficiency` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 11 | `064-subagent-concurrency` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 12 | `064-subagent-concurrency` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 13 | `065-loop-interruption-recovery` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 14 | `065-loop-interruption-recovery` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 15 | `066-loop-state-awareness-a` | `same-path` | `docs/reference/skills/sdd-loop-driver.md` | `docs/reference/skills/sdd-loop-driver.md` |
| 16 | `066-loop-state-awareness-a` | `same-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver/SKILL.md` |
| 17 | `067-loop-efficiency-hardening` | `nested-path` | `skills/external/sdd-loop-driver/SKILL.md` | `skills/external/sdd-loop-driver` |
| 18 | `067-loop-efficiency-hardening` | `nested-path` | `skills/external/sdd-loop-driver/references/decomposition-model.md` | `skills/external/sdd-loop-driver` |
| 19 | `067-loop-efficiency-hardening` | `nested-path` | `skills/external/sdd-loop-driver/scripts/wp-gate.py` | `skills/external/sdd-loop-driver` |
| 20 | `067-loop-efficiency-hardening` | `nested-path` | `skills/external/sdd-loop-driver/scripts/wp-report.py` | `skills/external/sdd-loop-driver` |
| 21 | `067-loop-efficiency-hardening` | `nested-path` | `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | `skills/external/sdd-loop-driver` |

## Adjudication

### Group A — driver SKILL.md (relations 3, 4, 6, 7, 8, 10, 12, 14, 16, 17)

- **Owner of the change**: Feature 070 owns the new `## Work Package Decomposition` section and its reference pointers. Every predecessor section stays byte-for-byte semantically unchanged.
- **No rule transfer**: 058 owns the loop/sentinels/u4; 059/068 own exec-quant; 060 owns the dispatch delegation; 062/063 own their command/efficiency surfaces; 064 owns concurrency; 065/066 own state awareness. 070 redefines none of them.
- **No live writer**: all listed predecessors are merged in the base history; 070 is the only active line.
- **Guard**: `tests/contract/test_non_regression_070.py` pins their sentinel, gate, budget, and boundary literals; the existing 058/063/064 pinned suites remain green.

### Group B — driver documentation page (relations 1, 2, 5, 9, 11, 13, 15)

- **Owner of the change**: Feature 070 owns the new documentation section; predecessor sections stay as they are.
- **Nested relation 1**: 056's historical declaration names `docs/reference` as a whole area; the current path is a file under that area. There is no file-level collision and no live writer.
- **Guard**: the docs page is documentation only; no runtime behavior is asserted from it beyond the entry pointer.

### Group C — new driver files (relations 18, 19, 20, 21)

- **Owner**: Feature 070 creates these files.
- **Nested relation**: 067's historical declaration names the driver skill directory as a whole. 067 delivered no file at these exact paths; its admission-check script and test work remain untouched.
- **Guard**: non-regression pins the 067 part brief/dispatch-log fields, which 070 extends rather than replaces.

## Disposition

- **Ownership transfer required**: none.
- **Second registry / ownership model / integration queue / ledger**: none created (D9.3).
- **Live collision**: none; every overlapping predecessor is merged before the 070 branch base.
- **Implementation re-check**: after the first driver-source edit, re-run the same command and compare against this relation set. A relation outside Groups A–C (a new path or a new spec) is unadjudicated and blocks further edits until resolved.
- **Gate outcome for this stage**: `overlap-adjudicated`. The deterministic `clear` criterion is unattainable for an additive change to an already-delivered skill surface; this recorded adjudication is the resolution, not an ignored finding.
