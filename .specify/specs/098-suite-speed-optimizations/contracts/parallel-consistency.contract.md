# Contract: Parallel Consistency Verification (xdist already default)

**Owner of these propositions**: this file. **Relation to 086**: this contract verifies and fixes the
parallel default 086 landed; it introduces no second parallelism mechanism and reopens no 086 clause.
**Evidence carrier**: `test-evidence/parallel-consistency*.txt`.

## A. Judgement

- **C-001**: Parallel safety is judged by failure NAME comparison, never by reading tests and never by
  wall-clock thresholds (FR-002, A7).
- **C-002**: The comparison is bidirectional: two runs of the same tree with the same selection and
  `--names-out`, one default-parallel and one `--serial`; `comm -13` and `comm -23` between the two lists
  MUST both be empty. A single-direction comparison is not evidence (FR-002).
- **C-003**: Both runs of a comparison MUST happen on the same tree. A comparison across trees, branches
  or spec directories MUST NOT be recorded as isolation evidence (edge case in requirements).
- **C-004**: Existing failures are compared by name: their presence in both lists is fine, their
  appearance/disappearance is not. New failure names MUST be zero; a non-empty difference is repaired as
  an isolation defect or registered as a `serial` exception with evidence — never ignored, retried or
  weakened (FR-002, SC-003).
- **C-005**: No case may assert a wall-clock threshold; evidence runs record durations only as disclosure
  (086 contract § F carries the same construction constraint).

## B. Staged order (FR-003)

- **C-006**: Verification starts on `tests/contract`: default-parallel vs `--serial` with `--names-out`,
  bidirectional `comm` empty; the command lines (with an explicit `--workers` bound such as 4, never
  `auto` for evidence stability), exit codes and complete name lists are recorded before the full-tree
  judgement is attempted (FR-003).
- **C-007**: The full-tree judgement happens at the closure stage as two same-tree runs: the closure slot's
  default-parallel full run and a `--full --serial` validation run. The validation run consumes no budget
  slot and its duration is not an SC-004/SC-005 wall-clock reading (FR-003, FR-010, A14; C-010).
- **C-008**: A subset that has been verified MUST NOT be reported as "the full suite is parallel-safe"
  until the full-tree comparison lands (FR-003).

## C. Discriminating evidence (the check must be able to go red)

- **C-009**: A constructed non-parallel-safe fixture suite (two tests writing one shared path with a
  barrier) MUST turn the parallel-vs-serial name comparison non-empty. The drill is run on a throwaway
  tree and recorded; it proves the comparison is a discriminator, not a green label (FR-002, SC-002).

## D. Missing-engine integrity (FR-004)

- **C-010**: The 086 C-006 construction (PYTHONPATH shim hiding `xdist`) is re-used: a complete serial run
  over `tests/contract` exits with the suite's own code, emits `reason=no-xdist`, and writes a valid
  `--names-out` list. No Python 3.8 interpreter exists on this host; the shim is the declared reduced
  measurement for the missing-engine branch and this reduction is disclosed (FR-004).
- **C-011**: A no-xdist run MUST NOT error out or run nothing; its mode line carries `reason=no-xdist`
  (086 C-006 unchanged).

## E. Evidence fields

- **C-012**: Every verification record carries: command, exit code, duration, complete `--names-out` lists
  (or their recorded paths plus line counts), and the two `comm` outputs. A record missing a field does not
  support the claim (FR-003, FR-020).

## F. Mutation legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| PC-M1 | Compare only one `comm` direction | C-002 |
| PC-M2 | Compare lists from two different trees | C-003 (recorded-tree identity check) |
| PC-M3 | Drop `--serial` from the comparison run | C-002 |
| PC-M4 | Treat `serial`-marked tests as absent from the serial list | C-004 (names differ) |
| PC-M5 | Record the subset result as full-suite safety | C-008 |
