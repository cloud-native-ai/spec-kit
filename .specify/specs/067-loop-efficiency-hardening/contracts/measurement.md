# Contract: Measurement Protocol (MP-01…MP-10)

Owner of the mechanical measurement rules for FR-012 / SC-006. The clarify-ratified
protocol text is `test-evidence/measurement-protocol-2026-10-22.md` (dated record);
these clauses bind implementation behavior to it. Field schema: `data-model.md` E1.

- **MP-01**: The fixed measurement composite is defined ONCE here and reused verbatim
  for every pre/post complete-run measurement in this spec. Changing it requires a
  recorded scope decision; silently diverging commands produce invalid evidence.
- **MP-02**: The fixed command (reporting flags only — `-q` and `--durations=50`; the
  baseline-in-flight command keeps its exact argument set):
  ```sh
  rm -rf .pytest_cache
  find tests src -type d -name __pycache__ -prune -exec rm -rf {} +
  S=$(date +%s)
  bash scripts/bash/run-tests.sh -q --durations=50 2>&1 | tee <evidence-log>; ST=${PIPESTATUS[0]}
  E=$(date +%s)
  echo "wall=$((E-S))s exit=$ST"
  ```
- **MP-03**: Cold-cache basis: the clear step runs immediately before the measured run
  and no other run happens between clear and finish. At most ONE warm-up run is allowed,
  BEFORE the clear, and it is never counted as evidence.
- **MP-04**: Wall clock = wrapper start/end epoch delta around the runner only. The
  pytest self-reported time is recorded as a cross-check and is never the budget number.
- **MP-05**: A measured run is a valid complete run only if: single runner invocation;
  no path / `-k` / `-m` filter; contract, unit, and integration layers all executed;
  collection and fixture time included; per-layer `deselected` count is 0. Violating
  any of these invalidates the record regardless of the wall number.
- **MP-06**: Each measured run produces one dated record under this spec's
  test-evidence directory with exactly the E1 fields of `data-model.md`.
- **MP-07**: Host scope of the budget: the 2026-10-22 baseline dev host only
  (macOS arm64, runner-resolved Python 3.14.6 + pytest 9.1.1). Every record carries its
  host identity; other hosts are informational.
- **MP-08**: A budget claim (≤600 s) MUST cite a committed E1 record of the post-change
  tree measured by MP-02; estimates, extrapolations, and subset runs never support the
  claim (SC-006 wording).
- **MP-09**: Measurement runs are never wrapped in retry or loop shells.
- **MP-10**: New diagnostic markers (e.g. a slow marker) are composition-neutral: they
  MUST NOT change what MP-02 executes (FR-011).
