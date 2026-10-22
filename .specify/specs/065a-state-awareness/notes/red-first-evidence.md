# Red-First Evidence — 065a-state-awareness

Append-only record of red (failing) test runs taken BEFORE the corresponding
implementation. Format per task: command, real output, exit code, failure
attribution.

## T003 — contract CLI/envelope tests (2026-10-22)

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/contract/test_loop_state_contract.py
FAILED tests/contract/test_loop_state_contract.py::test_help_lists_actions_params_exit_ladder_and_watcher_data_note
FAILED tests/contract/test_loop_state_contract.py::test_not_implemented_action_refusal_envelope[recover-065c]
FAILED tests/contract/test_loop_state_contract.py::test_not_implemented_action_refusal_envelope[check-spine-065b]
FAILED tests/contract/test_loop_state_contract.py::test_snapshot_envelope_required_fields_and_decision_consistency
FAILED tests/contract/test_loop_state_contract.py::test_spine_consistency_nested_only
FAILED tests/contract/test_loop_state_contract.py::test_out_side_effects_and_boundary
FAILED tests/contract/test_loop_state_contract.py::test_snapshot_readonly_mtime_audit
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_owner_is_fr004_everywhere
8 failed in 0.70s
RED_EXIT=1
```

Attribution: subject-side (T004 engine + T018 reference not yet created); assertions
mirror `contracts/loop-state-cli.md` C-1..C-6 wording verbatim, no assertion defect.

## T005–T007 — unit test gaps filled (2026-10-22)

Command (all runs below use the same canonical runner and interpreter):

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/unit/test_loop_state_engine.py
51 failed, 4 passed in 24.23s
RUN_EXIT=1
```

Progression of the same file as the T005/T006 groups were appended (each line is a
real run taken right after the edit):

| after | tests | result |
|-------|-------|--------|
| pre-existing file (T005 + first T006 group) | 20 | 17 failed, 3 passed |
| added T005 resolution/legacy gaps + T006 artifact/checklist/commit/false-completion | 30 | 26 failed, 4 passed |
| added T007 derived ladder + detectors + watcher tri-state/attribution | 41 | 37 failed, 4 passed |
| added T007 IA-14/attempt/salvage/probe/SC-001 | 53 | 49 failed, 4 passed |
| added clarify no-change, unknown-baseline terminal states, watchbeat `event`, deadline inverse (final) | 55 | 51 failed, 4 passed |

Representative first failure lines (subject-side, engine still a skeleton):

```
E       AssertionError: pid
E       assert 'na' == 'missing'            # C-6 evidence-source projection (T010)
E       AssertionError: assert 'unknown' == 'known'   # legacy spine parse (T009)
E       AssertionError: assert 'na' == 'unknown'      # commits baseline (T011)
E       AssertionError: assert False is True          # false_completion (T011/T014)
E       AssertionError: assert 'UNKNOWN' == 'DONE'    # derived ladder (T013)
E       AssertionError: assert 'UNKNOWN' == 'STALLED' # watcher verbatim rule (T013)
E       AssertionError: provable attribution must pass --line-id/--run-id
                                                      # C-14 attribution form (T012)
E       AssertionError: error: --probe consumption is not implemented in this build
                                                      # probe shapes (T016)
```

Attribution: all 49 reds are subject-side (T009–T016 not implemented). No assertion
defect found; every literal asserted is owned by `contracts/*.md`, `data-model.md` or
`requirements.md` FR-004. The 4 already-passing tests are honest pre-existing greens
(not-dispatched short-circuit, na projection, single-line isolation, null path
projection) and are kept as regression guards.

## T003/T008 — contract test additions (2026-10-22)

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/contract/test_loop_state_contract.py
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_owner_is_fr004_everywhere
FAILED tests/contract/test_loop_state_contract.py::test_probe_shapes_a_and_b_are_accepted
FAILED tests/contract/test_loop_state_contract.py::test_probe_does_not_read_local_evidence
FAILED tests/contract/test_loop_state_contract.py::test_stage_artifacts_match_reference_five_dimensions
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_is_three_way_identical
5 failed, 20 passed in 2.47s
RUN_EXIT=1
```

Per-clause attribution of the 5 reds:

- `test_probe_shapes_a_and_b_are_accepted`, `test_probe_does_not_read_local_evidence`
  — C-11/C-13 shape consumption未实现（T016）；引擎当前对 `--probe` 直接 exit 2。
- `test_stage_artifacts_match_reference_five_dimensions` — C-50 两端同时缺失：
  脚本 `STAGE_ARTIFACTS`（T011）与 `references/state-awareness.md`
  §Stage Artifact Map（T018）。
- `test_derived_mapping_is_three_way_identical` — 脚本 `DERIVED_MAPPING`（T013）与
  reference §Derived Mapping（T018）缺失；FR-004 一侧解析成功（8 条子句）。
- `test_derived_mapping_owner_is_fr004_everywhere` — 唯一的 reference 缺失红（T018），
  与本段开始前一致，保留。

Honest greens added by T008 (pre-existing correct behavior, NOT claimed red):
`--line-id` 缺失 exit 2、`--probe` 四类拒绝 exit 2、`--probe` 与五个本地参数互斥 exit 2、
证据源不可读 → `status=missing` + exit 0、`--self-test` 输出契约、确定性（仅
`evaluated_at` 差异）。直接跑引擎自测：

```
$ python3 skills/external/sdd-loop-driver/scripts/loop-state.py --self-test
ok help-ladder
ok help-watcher-codes-are-data
ok refusal-check-spine
ok refusal-recover
SELF-TEST: 4 passed, 0 failed
EXIT=0
```

## T009–T014 — engine core lands, residual reds attributed (2026-10-22)

Part-scope: T009 (input parsing / read-only projection), T010 (evidence readers +
stale isolation), T011 (stage artifact map + commit evidence), T012 (watcher
delegation), T013 (`loop_state` derivation), T014 (six read-only detectors).
T015 (action closure), T016 (`--probe`), T017 (`--self-test` extension) and T018
(owner reference) stay out of scope by dispatch.

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q \
  tests/unit/test_loop_state_engine.py tests/contract/test_loop_state_contract.py
26 failed, 54 passed in 39.94s
RUN_EXIT=1
```

Baseline before this part: `56 failed, 24 passed` (80 tests). After: 30 tests turned
green — unit `34 passed / 21 failed`, contract `20 passed / 5 failed`. No test was
made green by weakening an assertion.

### Residual reds (26) and their owners

| count | location | failing assertion | owner |
|-------|----------|-------------------|-------|
| 18 | unit | `recovery_action` / `recovery_reason` (e.g. `assert 'stop' == 'verify'`, `assert 'unknown' == 'attempts-exhausted'`) | T015 C-46..C-49 ladder, attempt limit, salvage gate, live-TIMEOUT watch |
| 3 | unit | `--probe` exit 2 (`--probe consumption is not implemented in this build`) | T016 |
| 2 | contract | `test_probe_shapes_a_and_b_are_accepted`, `test_probe_does_not_read_local_evidence` | T016 |
| 3 | contract | `references/state-awareness.md missing (T018)` | T018 |

Every unit red stops on its first action assertion, so the assertions *after* it were
verified out of band with a throw-away harness (`/tmp/verify_t13_t14.py`, not
committed). Confirmed derived/al detector behavior that the red lines hide:

```
no-signal: NO_SIGNAL no-signal            running: RUNNING running ['unwatched']
timeout: TIMEOUT deadline-overrun ['unwatched','deadline-overrun-live']
ahead:   RUNNING ['unwatched']            (deadline not passed -> no finding)
unwatched-missing: ['unwatched']  fresh: []  expired: ['unwatched']  sentinel: []
stale run-mismatch -> forms ['stale-signal'] (1 signal, excluded from evaluation)
```

### Three defects the red run exposed and fixed in the engine

1. `collect_signals` unpacked `missing_signal(...)` (a dict) as a 2-tuple: every
   snapshot with a missing evidence file crashed with `ValueError: too many values
   to unpack`. Readers now return `(signal, meta)` uniformly.
2. Two dead helpers (`watcher_attribution_form`, `envelopes_agree_placeholder`) were
   written but never called — `delegate_watcher` implements the C-14 attribution
   inline. Removed (pyflakes clean, no unused defs/consts).
3. `resolve_thresholds` probed `watch-target.sh --help` even when all three
   thresholds were explicit. That extra invocation ran the recording watcher script
   in `test_watcher_attribution_forms`, which then saw an argv file and failed
   `stale evidence must prevent the watcher call`. The help probe now runs only when
   a value is missing (C-16 order preserved: explicit → `--help` → `unknown`).

### Test edits (no assertion weakened — rationale per item)

1. `test_v1_spine_fields_are_parsed_without_guessing` asserted
   `spine.consistent in (True, None)`. That fixture has no four-piece evidence and
   the start grace has elapsed, so FR-004 rule (6) derives `NO_SIGNAL` while the
   spine says `last_verdict=RUNNING`; C-39 then *mandates* `false`. Replaced with
   the stricter pair `loop_state == "NO_SIGNAL"` + `consistent is False`.
2. `test_analyze_artifacts_are_vacuously_complete`,
   `test_implement_document_only_commit_is_not_complete` and
   `test_clarify_legitimate_no_change_is_verify` wrote their four-piece files under
   the fixture default stage (`tasks`) while calling `--stage analyze|implement|
   clarify`, so the engine could never see that stage's sentinel/exit record. They
   now set `ws.stage` (the pattern `test_directory_artifact_*` and
   `test_checklist_stage_*` already use). Assertions untouched.

### Interpretive decisions taken contract-first (disclosure)

- **R-02 env fallback not implemented.** C-4 fixes resolution as explicit → Registry
  → failure ⇒ `null`. `SPECIFY_LINE_RUNTIME_DIR` is therefore *not* consulted for
  `state_dir`; doing so would invent a path the caller did not state. Deviation from
  `research.md` R-02 recorded here; `test_unresolved_paths_stay_null_and_are_not_invented`
  pins the contract reading.
- **Staleness with an unknown current attempt.** With no spine/Registry `run_id`, a
  lone `run=` claim is not enough to attribute evidence: fewer than two agreeing
  four-piece envelopes ⇒ `run-mismatch` (doubtful-strict, C-43). The watchbeat
  marker is exempt from that rule (C-40 owns its freshness via `window=`) and is
  only compared against a known attempt.
- **Liveness identity.** `compare_start_identity` returns `ok`/`mismatch` only for
  comparable tokens (equal, or both numeric); otherwise `unknown`. No invented
  "start ticks missing ⇒ pid reuse" verdict.
- **`missing_fields`** lists the six `REQUIRED_SPINE_FIELDS`, not all fourteen
  readable ones (a v1 spine may legitimately omit `salvage*`/`*_path`/`last_verdict`).
- **Baseline split (C1a residual risk).** `stage_base_commit` *absent* ⇒
  `artifacts.complete=null` + `commits.value_state=unknown` + empty
  `uncommitted_artifacts` (C-54/C-57/C-59). `stage_base_commit` *present but
  unresolvable* ⇒ file-level completeness is still computed, `commits.value_state=
  unknown`, `uncommitted_artifacts=[]`. C-54's “未知” is read as “no baseline
  recorded”; C-57's unreadable baseline is expressed through `commits`. If a later
  reviewer reads C-54 as also covering unresolvable bases, `artifacts.complete` /
  `false_completion` for that case must be revisited — this is the C1a item carried
  into T015.
- **`spine.consistent`** compares `last_verdict` with the final `loop_state`
  (including a verbatim watcher verdict) and is `null` when either side is unknown.
- **Reason literals emitted by T013/T014**: `spine-stalled`, `spine-reentry-required`,
  `anomaly-line`, `exit-nonzero`, `sentinel-and-artifacts`, `exit-zero-incomplete`,
  `sentinel-no-exit`, `dead-no-exit-record`, `deadline-overrun`, `no-signal`,
  `running`, `unknown`, `not-dispatched`, `evidence-gap`, `remote-unreachable`,
  `watcher-verdict`. T015 owns the `recovery_reason` literals.
- **T018 authoring warning**: `test_stage_artifacts_match_reference_five_dimensions`
  harvests backticked tokens from cells 0–2 and booleans from cells 3–4 of the
  §Stage Artifact Map table, and `test_derived_mapping_is_three_way_identical` does
  the same for §Derived Mapping. Path lists belong in backticks, prose must stay out
  of backticks, and booleans must read `true`/`false`.

