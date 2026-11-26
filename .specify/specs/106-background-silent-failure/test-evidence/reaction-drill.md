# Reaction Drill — US3 (T021, spec 106)

Scenario: an old attempt ends silently (`silent-end`) and the parent retries under a **new
label**; the retry completes. The drill proves the five reaction readings required by
FR-023 / FR-024 and is the SC-004 source reading. Fixture builders:
`tests/fixtures/settlement/builders.py`; engine: `scripts/python/role-edge-check.py
--action settle` (read-only). No fixed `sleep` anywhere; the drill is deterministic.

## Fixture

- `drill-old` — C2 attempt, recorded pid gone, no `.end` / `.status` → `silent-end`; a stale
  return file `drill-old.return.txt` is present after the silent end.
- `drill-retry` — a **new label** with its own attempt / end / status / live log, its own
  return file and a version-bearing `completed` claim (`return-record`).

## Assertion run (test entry)

- `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py -q -k "retry or late_completion"`
  → rc **0**, `2 passed in 6.25s`
  (`test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value`,
  `test_late_completion_after_the_deadline_lands_on_its_own_label`)
- `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_carriers.py -q -k "run_agent_reports or run_agent_retry"`
  → rc **0**, `2 passed in 6.26s`
  (`test_run_agent_reports_every_attempt_before_the_outward_report`,
  `test_run_agent_retry_and_stop_rules_forbid_silent_repair`)

## Measured readings (drill run, `/usr/local/bin/python3`)

Command: `/usr/local/bin/python3 .specify/.tmp/p3-drill/reaction-drill.py` (tmp roots under
`.specify/.tmp/p3-drill/reaction-*`, removed after the run). Real output:

```
settle_rc=0
uplink_entries={"drill-old": {"value": "silent-end", "evidence_items": 3}, "drill-retry": {"value": "completed", "evidence_items": 4}}
retry_label_differs=yes
old_verdict=silent-end old_claim=None
retry_verdict=completed retry_claim=drill-retry.settlement
old_evidence_hashes_equal=yes
tree_unchanged=yes
engine_created_attempts=0
engine_kill_signals=[0] non_zero_kills=0
stale_return_unchanged=yes
```

| Reading | Value | Meaning |
|---------|-------|---------|
| 上送条目存在 (uplink entries) | old `silent-end` with 3 evidence pointers; retry `completed` with 4 | each attempt carries its own settlement value + evidence in the findings |
| 重试 label 不同 (retry label differs) | yes (`drill-old` ≠ `drill-retry`) | a retry is a new attempt, never a reused label |
| 旧证据哈希前后相等 | yes | settle is read-only; the old attempt's evidence is kept byte-identically |
| 自动 kill 次数 | 0 (`engine_kill_signals=[0]`, non-zero kills 0) | the engine has no kill authority; its only `os.kill` is the signal-0 liveness probe |
| 旧返回消费次数 | 0 (old claim `None`; stale return file hash unchanged; tree unchanged; engine-created attempts 0) | a stale return is never consumed as the current result and no retry is fabricated |

Result: **pass** — the reaction is visible, nameable, and not silently repairable.
