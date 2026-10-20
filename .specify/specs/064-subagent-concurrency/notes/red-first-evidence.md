# Red-First Evidence — Feature 064

Each entry records the real red run captured before the implementation it exercises.

## R1 — Foundational engine unit tests (T004 → T005)

- Time: 2026-10-20 (implement run)
- Command: `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py -q`
- Exit status: 1
- Output (tail): `9 failed in 0.05s`; every failure is `AssertionError: engine missing: …/skills/external/sdd-loop-driver/scripts/line-registry.py` (the engine does not exist yet).
- Meaning: the foundational tests fail for the right reason (missing implementation), not for fixture errors.

## R2 — US1 contract/integration/unit tests (T007–T011)

- Time: 2026-10-20 (implement run)
- Command: `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py tests/contract/test_line_registry_contract.py tests/contract/test_line_envelope_contract.py tests/integration/test_two_line_isolation.py -q`
- Exit status: 1
- Output (tail): `24 failed, 24 passed in 8.71s`
- Failing: envelope classification/ingress unit functions missing; `resolve-message`/`verify-identity` not dispatched (exit 2); watcher emits no `attribution=` field; carrier documentation absent; two-line integration cases red for the same reasons.
- Passing baseline: foundational primitives, register/update/deregister/list, LR-01..LR-06/08/09/11..13.

## R3 — US2 workspace isolation tests (T021–T024)

- Time: 2026-10-20 (implement run)
- Command: `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py tests/contract/test_workspace_isolation_contract.py tests/integration/test_worktree_integration_queue.py -q`
- Exit status: 1
- Output (tail): `26 failed, 16 passed in 17.04s`
- Failing: ownership-check/release/promote, integration-enqueue/plan/record, allocate-resources, archive-runtime, path/queue pure helpers, worktree-path uniqueness, and the documentation clauses for the integration protocol (not yet written).
- Passing baseline: registry core and US1 attribution coverage.
