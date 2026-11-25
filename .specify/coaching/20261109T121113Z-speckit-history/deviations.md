## Outcome Correctness
- **D-1 (result-deviation — environment, coach-caused).** OC-1's expected terminal state was "gate reached with
  review+design presented"; the actual terminal state is **seam-stop before Step B**: snapshot #1 ≠ #2 because
  external writers (the trigger engine and **this coach's own close-out commits for the sibling run**,
  `1e4d462ea`/`3d52ea09a`) changed the tracked tree inside the review window. The Trainee's Skill Step A.3
  forbids continuing under an unstable seam, so the stop is contract-faithful; the *cause* is a coach-side
  process violation — the coaching harness wrote and committed during a live run's seam window, and two
  history-seam runs of the same subject were allowed to overlap. Evidence: observation § Anomaly + State changes.
- OC-2 pass: the no-argument semantics were honoured — the run covered the full incremental set, invented no
  topic, and reported the exact scope (2,075 candidates / 861 entries).
- The inherited `none-of` decision was applied correctly and not re-asked (dated decision `3d52ea09a`).

## Process Efficiency
- **D-2 (process-deviation — serialization).** The subject write-lock (owner: `references/nested-runs.md`
  § claim/write lock) says runs at one subject serialize. Both history runs share the same subject (the
  workspace seam). Dispatching the second while the first was live, then committing the first's records inside
  the second's window, is exactly what the lock exists to prevent. No gate was weakened; the Trainee's seam
  check caught it.
- Elapsed ~6 min, within the PE calibration for a full incremental review.

## Where the readings diverged
- The coach assumed the second run was read-only until its gate and therefore harmless alongside the first;
  the Trainee reads the seam as binding the whole tracked tree, so any write — including the coach's own
  records — invalidates the window. The harness must treat a live seam window as exclusive.
