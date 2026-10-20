# sdd_loop_efficiency fixtures

Every fixture here is consumed by a named test or by the driver-stall baseline
procedure. Paths are repository-relative.

| Fixture | Consumed by | Contract clauses |
|---------|-------------|------------------|
| `medium/.specify/specs/012-medium/` | `tests/unit/test_admission_check.py` (T008), `tests/contract/test_sdd_loop_driver_efficiency.py` FL tests (T009) | FL-02, FL-03, FL-09 |
| `large/.specify/specs/013-large/` | `tests/unit/test_admission_check.py` (T008) | FL-03 |
| `plan-repo/.specify/specs/012-medium/` | `tests/unit/test_audit_plan_changes.py` (T025), `test_pc_11_reanchoring` (T026) | PC-05, PC-06, PC-10, PC-11 |
| `state-spine-valid.md` | `tests/unit/test_audit_test_budget.py` (T016), `test_tb_07_ledger_audit_unknown` (T018) | TB-02, TB-03, TB-06, TB-07 |
| `test-evidence/analyze.jsonl` | `tests/unit/test_audit_test_budget.py` (T016) | TB-06 |
| `test-evidence/checklist.jsonl` | `tests/unit/test_audit_test_budget.py` (T016) — `not-applicable-skipped-stage` linkage | TB-06, TB-07 |
| `test-evidence/plan.jsonl` | `tests/unit/test_audit_test_budget.py` (T016) — docs-only reduced field set | TB-06 |
| `stream/non_terminal_sentinel.jsonl` | `tests/unit/test_derive_live_log.py` (T033) | PD-02, PD-03 |
| `stream/result_sentinel.jsonl` | `tests/unit/test_derive_live_log.py` (T033) | PD-02, PD-03 |
| `stream/malformed.jsonl` | `tests/unit/test_derive_live_log.py` (T033) | PD-05 |
| `stub-cli.sh` | `tests/unit/test_derive_live_log.py`, `tests/integration/test_sdd_loop_efficiency_runner.py` | PD-01, PD-05, PD-10 |
| `driver-stall-fixture.py` | T001 baseline recording and T051 replay + mutation drill | SB-1…SB-5, DI-03 |

## driver-stall-fixture.py

Single execution body for the SC-010 behavior baseline. It creates a stub
runner (controlled pid/status/heartbeat/runner-log and rc), calls the real
`watch-target.sh` of the supplied worktree for the U3 verdict, runs the
documented U4/U5 driver program, and reads the seven observed fields back from
the state spine, status file, runner log and dispatch log. The four scenarios
are timeout, retry-limit, fake-done (INCOMPLETE, no next-stage dispatch) and
success (DONE, writes `next_stage=<stage>` to `dispatch.log`), so
`next_stage_dispatched` is observed in both directions. It never contains an
expected tuple and never backfills from a baseline file (SB-5). `--record`,
`--replay` and `--self-test` are the only modes; `--initial-retries` accepts
only `0`.

Per-scenario artifacts are copied to `--evidence-dir` (default: a
`stall-evidence` / `stall-evidence-replay` sibling of `--out`) before the
temporary run root is deleted, and `evidence_ptr` is rewritten to that durable
relative path.

## Self-check (2026-10-20)

```text
$ bash tests/fixtures/sdd_loop_efficiency/stub-cli.sh --output-format stream-json --delay 0
{"type":"system","subtype":"init","session_id":"fixture"}
{"type":"assistant","message":{"content":[{"type":"text","text":"working; this text mentions PLAN-DONE but is not terminal"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"more progress"}]}}
{"type":"result","subtype":"success","is_error":false,"result":"stage finished\nthe final line is exact\nPLAN-DONE"}
rc=0

$ bash tests/fixtures/sdd_loop_efficiency/stub-cli.sh --mode no-stream
buffered stage output
PLAN-DONE
rc=0

$ bash tests/fixtures/sdd_loop_efficiency/stub-cli.sh --help | grep -c -- --output-format
0
```

`python3 tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py --self-test`
→ `PASS: driver-stall-fixture self-test`.
