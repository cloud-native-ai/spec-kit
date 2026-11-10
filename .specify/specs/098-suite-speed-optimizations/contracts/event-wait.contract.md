# Contract: Event Wait and Fixed-Sleep Elimination

**Owner of these propositions**: this file. **Implementation surfaces**: the scope files below,
`tests/fixtures/line_fixtures.py` (the shared wait helper), and the new guard
`tests/contract/test_event_wait_contract.py`.

## A. Scope

- **C-001**: The zero-synchronization-sleep requirement applies to exactly these files:
  `tests/contract/test_client_metrics.py` (FR-015),
  `tests/integration/test_sdd_loop_efficiency_runner.py`,
  `tests/integration/test_session_kill_reattach.py`,
  `tests/contract/test_line_envelope_contract.py` (FR-016), plus the two declared same-class additions
  `tests/contract/test_feedback_probe_cli.py` and `tests/contract/test_store_state_protocol.py` (ordering
  determinism, same defect class as FR-015).
- **C-002**: In every scope file, `time.sleep` used for synchronization or ordering MUST be zero after this
  feature. The guard scans the scope files mechanically (AST call-site scan) and names file and line for
  every hit (FR-017).
- **C-003**: Exemptions are a closed, per-line registry with reasons; this slice declares two:
  `tests/unit/test_line_registry_engine.py` (the generated flock holder must outlive the 0.2 s lock
  timeout under test) and `tests/unit/test_concurrency_check_engine.py` (synthetic task duration that a
  wall-clock comparison measures). Polling intervals inside fixture writer processes are not test
  synchronization and are out of scope. A new exemption requires revising this clause (FR-017).

## B. Deterministic ordering (FR-015)

- **C-004**: Entry ordering in `test_client_metrics.py`, `test_feedback_probe_cli.py` and
  `test_store_state_protocol.py` is produced by the injected clock (`feedback-utils.py --now`,
  data-model E-4) and by explicit file mtimes (`os.utime`) where closure evidence compares mtime against
  `created`. No assertion may depend on real elapsed time (FR-015).
- **C-005**: The assertion set of `test_client_metrics.py` is unchanged: the same numeric, boundary and
  disclosure assertions run against the same four metrics (FR-015).

## C. Event waits (FR-016, FR-026)

- **C-006**: Completion waits observe an event or status file through the shared helper
  `wait_until(predicate, timeout, interval)`. The helper returns `True` as soon as the predicate holds and
  `False` on deadline; callers assert the return value with a named failure message. Timeout MUST NOT be
  converted into `skip`, `xfail`, or a retry (FR-021, FR-026).
- **C-007**: Every wait site records an explicit deadline; the default is 30 seconds and a longer deadline
  must carry a one-line reason at the site. The polling interval MUST be ≤ 0.2 seconds. Polling occurs
  only while the predicate is false; once the event appears the test continues immediately (FR-026).
- **C-008**: The former fixed graces (`test_session_kill_reattach.py` SIGHUP grace, post-exit residue;
  `test_line_envelope_contract.py` heartbeat first-write and advance) are replaced by predicates over the
  observable file state, never by a shorter sleep (FR-016).

## D. Proof

- **C-009**: The guard asserts the zero count (C-002), the helper defaults (`timeout <= 30` in the adopted
  call sites, `interval <= 0.2`), and the exemption registry's per-line justification. A reintroduced
  scope sleep turns the guard red with file and line (FR-017).
- **C-010**: The directional wall-clock measurement for `test_client_metrics.py` is taken before and after
  at the same worker count on the same host and day, with command, exit code, complete output and duration
  recorded under `test-evidence/` (SC-008).

## E. Mutation legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| EW-M1 | Reintroduce one `time.sleep` in a scope file | C-002 |
| EW-M2 | Raise the wait interval above 0.2 s | C-009 |
| EW-M3 | Convert a timeout into `pytest.skip` | C-006 (static assertion + case) |
| EW-M4 | Put a fixed sleep back as a "shorter" grace | C-008 / C-002 |
| EW-M5 | Depend on real elapsed time in a metrics ordering assertion | C-004 drill (injected clock removed) |
