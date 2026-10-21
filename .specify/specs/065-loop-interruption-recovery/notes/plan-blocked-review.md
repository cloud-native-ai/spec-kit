# Plan Blocked — Review Findings & Gate Conflict (2026-10-21)

**Status**: draft plan not landed. No commit, no feature status advance, no tasks dispatch.

## Blocking condition

- `notes/decomposition-gate.md`: `split-required` (52 FR > 30; `fr_ceiling=30`; exit 1), re-measured at 2026-10-21T10:06:47Z.
- `state-spine.md`: `state: stalled`, `current_stage: plan (not dispatched)`, "Do not dispatch plan for the umbrella", next action `confirm-split`.
- The `/speckit.plan` dispatch arrived against that spine. Treating the dispatch as the §5.3.3 upstream confirmation is self-confirmation; the stage halted instead.
- The `tasks` U4 gate will also fire for the umbrella: `FR=52 > 30` is independent of task count, so `analyze` cannot be reached without a split or an explicit recorded override.

## Independent review findings (fresh-context, read-only)

Two reviewers split the artifact set (plan/research/data-model vs contracts/quickstart/feature-ref). Findings that must be fixed before any plan is landed:

1. **Attribution conflict (CRITICAL)**: LS-21/SN-05/SN-06 define `own`/`legacy` twice and inconsistently; 063-style carriers have no `run=` and would be marked stale, breaking the accident-replay path. Define one selection rule (status carrier envelope decides) and one carrier-attribution rule for legacy mode.
2. **Salvage gate circularity (HIGH)**: `--salvage` is rejected unless the resolved action is `resume`, but a missing sentinel resolves to `retry` before salvage is considered. Make `--salvage --evidence` an input to adjudication (AD-7), not a post-decision flag.
3. **D2 ANOMALY scope (HIGH)**: D2 is gated on an own status record, so a dead process whose log ends in `ANOMALY:` derives `DEAD` instead of `ANOMALY`. Apply the anomaly predicate when `(status exists OR pid dead)`.
4. **I2 vs sentinel (HIGH)**: `dead-no-exit-record` fires even when a sentinel and complete artifacts exist, contradicting D3. I2 must require absence of a sentinel.
5. **Interruption forms override `loop_state` (HIGH)**: SN-30/SN-31 assign TIMEOUT/RUNNING unconditionally, contradicting watcher-verbatim SN-08. Forms must annotate; only derived rules set `loop_state`.
6. **Spine schema vs writers (HIGH)**: E-04 omits `spine_stall_reason`, `spine_retry_reason` and `spine_stage_base_commit`; V-028/SP-16 require a present `last_verdict` that stop/retry never write. Add the keys, require the base commit at U2, and relax consistency so stalled/retrying may omit `last_verdict`.
7. **Pseudo-completion double bind (HIGH)**: V-003 requires `loop_state` = watcher `DONE`, V-078 forbids `DONE` for the same sentinel-with-missing-artifacts case. Resolve with a separate `completion` field: `loop_state` stays watcher-verbatim, `completion=incomplete`, action `retry`.
8. **Commit-base writer missing (HIGH)**: FR-008's `stage_base_commit` is not in the current spine fields and no deliverable writes it. Add it to the machine segment, U2 write obligation and tests.
9. **Watcher non-regression cannot go red (HIGH)**: `watch-target.sh --self-test` lives inside the file it protects. Pin a SHA-256 of the watcher (baseline `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4`) in the contract suite so any byte change turns red.
10. **Registry-missing path missing (HIGH)**: FR-002's "Registry missing but spine+carriers readable → continue with `registry=missing`" has no clause or envelope field. Add a `registry` object and the continue path.
11. **Lock vs no-write actions (HIGH)**: LS-16 requires a lock for every `recover --apply`, while V-070 says `verify/none` never lock. Limit the lock to mutating actions.
12. **Live TIMEOUT stop undefined (MEDIUM)**: define `--confirm-live-stop`; without it `stop --apply` refuses (no mutation); with it and a final `--once`, it applies.
13. **Quickstart lifecycle (MEDIUM)**: S1 deletes `$TMP` before S2–S7; make scenarios self-contained or move teardown to the end; replace "fixture setup omitted".
14. **Test matrix naming (MEDIUM)**: NR-17 omits named fixtures for sentinel-with-missing-artifact and legacy-spine snapshot; FR-012's "self-test case list" has no owner.
15. **Baseline label (LOW)**: "engine unit tests 31 passed" actually covers `test_line_registry_engine.py` + `test_decomposition_check.py`.

## What exists

- Draft plan/research/data-model/contracts/quickstart/feature-ref under this spec dir, uncommitted.
- `pre-analyze-check --stage plan` reports 0 errors and 24 expected `missing-path` advisories for not-yet-implemented files; this is not a landing criterion.
- No source or mirror edits; no tests changed; no commit.

## Options

1. Confirm the three-slice split (`065a`/`065b`/`065c`), update the state spine, and run each slice through the full chain (the gate's intended path).
2. Record an explicit upstream override of the decomposition gate in the state spine, then fix findings 1–15 and re-run this plan.
3. Stop the line with a handoff if neither decision is available.
