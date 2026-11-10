# Contract: Slow Marker Membership and Guard

**Owner of these propositions**: this file. **Carrier of membership data**: `test-evidence/slow-members.md`.
**Implementation surfaces**: `pyproject.toml` (marker registration), the marked test files, and
`tests/contract/test_suite_tier_contract.py` (guard cases).

## A. Membership

- **C-001**: The marker name is [[STR-001]] and it is registered in `pyproject.toml` with a description
  that states its semantics and that the runner's default tier excludes it (FR-005).
- **C-002**: Membership is limited to two categories, closed (FR-006):
  - `process-boundary`: an integration test that spawns, waits for, or terminates an external process or
    queue (e.g. a detached stage runner, a heartbeat writer it must outlive).
  - `corpus-scan`: a contract test that traverses the whole corpus or multiple spec directories on the
    real framework tree.
- **C-003**: Every member row in `test-evidence/slow-members.md` carries exactly the columns
  `test_id | category | reason | date`; `category` is one of the two values above; `reason` names the
  spawned process family or the traversed corpus; `date` is the measurement date. A member without a row,
  a row without a member, a duplicate row, or a category outside the set MUST turn the guard red (FR-006,
  FR-024).
- **C-004**: Membership MUST NOT be derived from a single duration sample, subject feeling, or a blanket
  application to ordinary unit tests. The registry records the measured duration that motivated the
  classification in `reason` or in the accompanying evidence record (FR-006).

## B. Guard obligations

- **C-005**: The guard derives the marked set with `pytest --collect-only -q -m slow` and the registry set
  by parsing the table; it asserts exact one-to-one correspondence. It MUST NOT read or embed a member
  count (FR-024).
- **C-006**: On the real tree, the guard asserts collection equality: the default-tier collection set
  equals the full-tier collection set minus the marked set. Both collections are obtained through the
  canonical runner with `--collect-only -q` (collection only; no test bodies execute) (FR-024).
- **C-007**: On a throwaway fixture tree, the guard asserts the disclosure arithmetic: adding one slow test
  to the tree increases the reported `excluded_slow` by one, and `--full` reports zero and restores the
  full collection (FR-024).
- **C-008**: The guard itself MUST NOT be a member; if it were, the default-tier run could never evaluate
  the equality it owns.

## C. Evidence

- **C-009**: The membership measurement is recorded once in `test-evidence/slow-members.md` (the table) and
  its measurement run (per-test durations for the candidate pool) in
  `test-evidence/slow-members-measurement.txt`. The two files are the membership evidence; no other file
  restates the list (FR-024, A6).

## D. Mutation legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| SL-M1 | Delete a registry row for a marked test | C-005 |
| SL-M2 | Add a registry row for an unmarked test | C-005 |
| SL-M3 | Change a category to a value outside the two-member set | C-003 |
| SL-M4 | Mark a new test without adding a row | C-005 / C-007 |
| SL-M5 | Replace the derived count with a constant in the guard | C-006/C-007 cannot go red on membership drift |
