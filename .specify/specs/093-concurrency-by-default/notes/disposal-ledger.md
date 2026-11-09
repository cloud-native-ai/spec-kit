# Disposal ledger — the pre-existing concurrency statements (T134, C-079…C-092, SC-010)

**Owner of the taxonomy**: `.specify/specs/093-concurrency-by-default/contracts/existing-semantics-disposal.contract.md`
(C-079: exactly one disposition per statement from `{owner-moved, pointer, removed, dated-record}`; there is
no fifth disposition). This ledger maps each **affected pre-existing statement** to its disposition and
evidence. It restates none of the owners' rules — every row reaches its subject and its evidence by path.

**Date of the review**: 2026-11-09 (the release wave). **Feature**: 093-concurrency-by-default.

**Notation**: `dated-record` = the statement is kept with this dated record of why it stays or why the
change is a record rather than a live rewrite (C-081); `pointer` = the statement now reaches its owner by
path and no longer restates the value (C-080); `owner-moved` = the asserted value now lives at the named
owner and the asserting surface reads it there; `removed` = the statement was explicitly removed by this
feature's ruling (FR-033/FR-035) and its replacement is named.

| # | Pre-existing statement (owner × entry, reached by path) | Disposition | Evidence | Date | Reason / record |
|---|---|---|---|---|---|
| 1 | 064 write-line / worktree / integration-queue statements (`skills/external/sdd-loop-driver/references/decomposition-model.md` §13.1, §16) | dated-record | `skills/external/sdd-loop-driver/references/decomposition-model.md` | 2026-11-09 | retained: 093 reuses the mechanism unchanged (C-091); this record marks the review, no rule text moved |
| 2 | 064/084 integration-order rule (SD-05 / VI-07, `decomposition-model.md` §13.2, §16) | dated-record | `skills/external/sdd-loop-driver/references/decomposition-model.md` | 2026-11-09 | retained; FR-017 adds the replay-equality sentence beside it, the order rule itself is unchanged |
| 3 | 070 slot-cap value (SD-04 in `.specify/specs/070-subagent-task-teams/contracts/scheduler-and-dispatch.md`; the preset's `slot_cap_default: 6`) | owner-moved | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` | 2026-11-09 | the numeric cap now lives only in the fact; the preset and the 070 test read the projection (T116/T124/T133) |
| 4 | 070 ceiling statements (`min(6, line remaining)`, `min(4, line remaining)`, `min(effective_concurrency, 24)` in `decomposition-model.md` §13.2/§22 and the preset) | pointer | `skills/external/sdd-loop-driver/scripts/wp-gate.py` | 2026-11-09 | the ceiling stays with the gate's declared default (`--slot-cap-ceiling`, WG-16); the prose sites now point at it |
| 5 | 070 WG-15 directory-level write-domain fixtures (`tests/contract/test_sdd_loop_driver_wp_coordination.py`, `tests/unit/test_wp_gate.py`) | dated-record | `tests/contract/test_sdd_loop_driver_wp_coordination.py` | 2026-11-09 | FR-012 makes the write domain file-level; the fixtures are re-pinned to file-level paths, recorded here rather than silently edited |
| 6 | 070 old local topology ("one native host subagent per package"; "MUST NOT launch `qodercli` locally"; `host-no-parallel-native`) | removed | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` § 本地原生拓扑 | 2026-11-09 | FR-035 disposes the rule by explicit revision; the fork / subprocess carriers and the in-process ban replace it, and the old literal survives only as the dated record in `decomposition-model.md` §13.2 |
| 7 | 086 test-execution entry ("prefer the canonical runner"; raw `pytest` forms) | pointer | `.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md` | 2026-11-09 | FR-036 hardens the entry to "only entry"; the runner's own behaviour stays with 086's owner |
| 8 | 092 "plan parallelism not delivered" deferral | dated-record | `tests/contract/test_concurrency_reproduction_092.py` | 2026-11-09 | resolved in this slice by the reproduction fixture (SC-005); this record names the closing artifact, the 092 deferral itself is not rewritten |
| 9 | 077 stage-class byte baselines (7 stage templates + `docs`/`humanize` entry points, `tests/contract/test_stage_class_wiring.py`) | dated-record | `tests/contract/test_stage_class_wiring.py` | 2026-11-09 | 093 T122 adds the authored concurrency-obligation pointer block outside the wiring card; the pins are re-measured under the test's documented legitimate-edit path |
| 10 | stage-team preset slot sentence (`slot_cap_default: 6`, `slot_cap_ceiling: "min(6, …)"`, `skills/external/sdd-loop-driver/templates/stage-team-preset.md`) | pointer | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` | 2026-11-09 | the preset now carries one obligation paragraph and two `projection-of` lines; the seat structure is unchanged (T116/T133) |
| 11 | decomposition-model §20.1 built-in per-stage defaults (the pre-093 list with `analyze: off`) | pointer | `shared/declarations/facts/decomposition-coverage.yaml` | 2026-11-09 | the fact owns per-stage coverage; the model resolves through it and the built-in list is removed (T118/T140) |
| 12 | 093's own four slot-cap prose restatements (`stage-team-preset.md`, `decomposition-model.md` §13.2/§22, driver `SKILL.md`, `dispatch-recipes.md`) | pointer | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` | 2026-11-09 | one disposition, not two values: the numeric cap lives in the fact and every other site points (T124) |

## Gate assertions and their owners (T125's retained half)

- The ceiling's assignable site remains `skills/external/sdd-loop-driver/scripts/wp-gate.py`'s
  `--slot-cap-ceiling` declared default (WG-16); `tests/contract/test_concurrency_disposal.py` asserts
  the owner and the absence of a second numeric site.
- 070's gate assertions (`WG-15`/`WG-16`) are retained; `WG-15` gained the file-level form and no other
  check in `wp-gate.py` changed (T061/T078).
- The suite reading after these dispositions is `test-evidence/wp5-suite-final.txt` (GATE-1) and the
  acceptance-module reading is `test-evidence/wp5-acceptance-final.txt`.
