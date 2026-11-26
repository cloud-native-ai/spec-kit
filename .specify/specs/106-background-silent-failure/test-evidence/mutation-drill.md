# Mutation Drill — US4 (T025 / T026, spec 106)

Rule owner: `shared/definitions/superagent-definitions.md` § Termination. Pinning
clauses: `contracts/enforcement-and-migration.contract.md` C-30 (mutation drill) and
C-24 (zero second mechanism). Each drill mutates the real source
`scripts/python/role-edge-check.py` in place, runs a targeted selection through
`scripts/bash/run-tests.sh`, records at least one failing test with its real output, then
restores the file from a byte-identical backup. Restore is proven by `sha256sum` plus
`git diff --quiet`.

- Engine baseline sha256: `4a1b898b597896ef69b234bf6e6ed55f409f7e65696a592ef6554f6c6c2dd125`
- Backup: `.specify/.tmp/p3-drill/mutation-backup.py` (transient; removed with the temp root)
- Every drill below ends `engine-restored (git diff empty)`

## Drill 1 — remove/weaken silent-end detection

Mutation: all four `silent-end` derivations in `_derive_settlement` return `running`
instead (`pid-reused`, `pid-gone`, `start-grace-expired`, `deadline-passed`; 4/4
replacements).

Command:
`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py -q -k "silent or pid_reuse"`

Real output (tail):

```
FAILED tests/contract/test_settlement_engine.py::test_silent_end_is_a_judged_attempt_not_a_violation
FAILED tests/contract/test_settlement_engine.py::test_pid_reuse_is_not_liveness
FAILED tests/contract/test_settlement_engine.py::test_terminal_classes_settle_with_evidence[c2_silent_end-silent-end]
3 failed in 6.24s
```

Verdict: red (3 failing tests). Restored, sha256 back to baseline, `git diff` empty.

## Drill 2 — remove/weaken the live-evidence requirement

Mutation: the pid-liveness branch `if _pid_liveness(attempt["pid"]) == "alive":` becomes
`if False:` — a live subject falls through to the silent-end derivation.

Command:
`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q -k "live"`

Real output (tail):

```
FAILED tests/contract/test_settlement_carriers.py::test_c2_long_silence_with_a_live_pid_stays_running
FAILED tests/contract/test_settlement_engine.py::test_running_requires_a_live_check_and_is_reverse_safe
FAILED tests/contract/test_settlement_carriers.py::test_c1_live_stage_is_running_not_silent_end
FAILED tests/contract/test_settlement_carriers.py::test_c2_live_attempt_is_running_not_silent_end
4 failed, 3 passed in 6.34s
```

Verdict: red (4 failing tests; the C3/C4 pid-less legs pass because their liveness leg is
the return channel, not the pid branch). Restored, sha256 back to baseline, `git diff` empty.

## Drill 3 — make `unknown` return 0

Mutation: the `settle_exit_code` refusal `if payload["summary"]["unknown"]: return 2` is
deleted, so a detection defect becomes exit 0.

Command:
`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py -q -k "unknown"`

Real output (tail):

```
FAILED tests/contract/test_settlement_engine.py::test_unreadable_evidence_is_unknown_exit_two
FAILED tests/contract/test_settlement_engine.py::test_missing_start_record_is_unknown_exit_two
FAILED tests/contract/test_settlement_engine.py::test_unknown_is_never_exit_zero
3 failed in 6.24s
```

Verdict: red (3 failing tests; the mutated run returned `"values": {"unknown": 2}` with
rc 0). Restored, sha256 back to baseline, `git diff` empty.

## Drill 4 — remove the evidence-pointer requirement

Mutation: in `_claim_backed`, the `completed` branch returns `True` instead of
`_evidence_resolves(claim, attempt["bases"])`, so a claim with empty evidence counts as
backed.

Command:
`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q -k "without_evidence"`

Real output (tail):

```
FAILED tests/contract/test_settlement_engine.py::test_completed_claim_without_evidence_is_unbacked
E       assert 0 == 1
1 failed in 6.27s
```

Verdict: red (the empty-evidence claim settled `completed` with exit 0 instead of
`settlement-unbacked` / exit 1). Restored, sha256 back to baseline, `git diff` empty.

## Post-drill state

`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q`
→ rc **0**, `54 passed in 6.44s`; `git status --porcelain -- scripts/python/role-edge-check.py`
empty. No drill failed to turn a test red; no guard defect recorded.

## T026 meta-mutation — the scope guard can go red

Proof that `tests/contract/test_settlement_scope.py`'s second-value-table leg is a real
guarantee, not a vacuous scan: a second settlement value table was injected into a scanned
declaration surface (`shared/workflow/external-dispatch-recipes.md`, sha256 base
`1406c61cae4dceed5fa8767ec96095e5ac2e1d42edefbf26270350e6747a5c36`), the guard was run,
then the file was restored byte-identically.

Command:
`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_scope.py -q -k "second_settlement_value_table"`

Real output (tail):

```
E       AssertionError: a second settlement value table exists outside the owner page: [('shared/workflow/external-dispatch-recipes.md', [['anomaly', 'cancelled', 'completed', 'failed']])]
FAILED tests/contract/test_settlement_scope.py::test_no_second_settlement_value_table_on_declaration_surfaces
1 failed in 6.29s
```

Verdict: red (1 failing test naming the injected file and the four value names). Restored,
sha256 back to `1406c61c…`, `git diff` empty; the full scope module is green afterwards
(`10 passed`).
