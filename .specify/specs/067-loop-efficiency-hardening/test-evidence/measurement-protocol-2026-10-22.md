# Test-Economics Measurement Protocol — 2026-10-22 clarify rulings (dated record)

Owner of the exact mechanics ratified in `requirements.md` § Clarifications
`Session 2026-10-22（clarify：测试经济学裁决）` and FR-012 / SC-007 / SC-008 wording.
Dated record created by the clarify stage; **no pytest run happened in this stage**
(the driver's full-suite baseline was still running in the background), so nothing
here claims a measurement result. Exact numbers land here only as later dated records.

## 1. Fixed measurement command (定案于 plan 阶段一次，瘦身后原样复用)

Pre/post measurements MUST use the identical composite:

```sh
# pre-step: cold-cache clear (documented in evidence; runs before the timer starts)
rm -rf .pytest_cache
find tests src -type d -name __pycache__ -prune -exec rm -rf {} +

# fixed runner command with wall-clock wrapper
S=$(date +%s)
bash scripts/bash/run-tests.sh -q --durations=50 2>&1 | tee <evidence-log>; ST=${PIPESTATUS[0]}
E=$(date +%s)
echo "wall=$((E-S))s exit=$ST"
```

- The baseline-in-flight command is `bash scripts/bash/run-tests.sh -q --durations=50`;
  the post-slimming measurement MUST keep this exact runner argument set (reporting
  flags only — `-q` and `--durations` change no run composition; `-k`/`-m`/path args
  are forbidden and their presence in a recorded command invalidates the evidence).
- Cache clear → measured run must be contiguous: no other run in between. An optional
  warm-up run (at most ONE, not counted as evidence) must happen BEFORE the cache clear.
- Wall clock = wrapper start/end epoch difference around the runner only. pytest's own
  `in N.NNs` summary line is recorded as a cross-check, never as the达标 number.

## 2. Evidence record fields (FullRunMeasurement, one dated record per complete run)

Each measured run appends one record to `test-evidence/` with: command string (verbatim),
host identity (`uname -m`, macOS version, resolved interpreter + `pytest --version`),
date, git commit, cache-clear confirmation (commands + timestamp), start/end epoch,
wall seconds, exit code, per-layer counts (contract / unit / integration ×
passed/failed/error/skipped; any `deselected` count > 0 = filter present = invalid),
pytest summary line, evidence log path, and (for the达标 run) the cross-checked
baseline record pointer.

## 3. Baseline test-id list (generation deferred to implement; obligation, not a gap)

Definition: the full node-id set of the pre-slimming suite. Generation: run
`pytest --collect-only -q` via the runner-resolved interpreter, strip summary lines,
one node id per line → `test-evidence/baseline-test-ids.txt`, header records command +
date. Timing: after the full baseline run completes, BEFORE the first
consolidation-affecting implement task. This stage could not generate it (pytest
forbidden while the baseline holds the machine) — recorded as an implement-stage duty.

## 4. Baseline failure set authority (SC-008 / FR-018 green semantics)

- Authoritative baseline failure set = the FAILED name list of the driver's
  2026-10-22 full run (`notes/baseline-full-2026-10-22.log`, once finished).
- Provisional dated record until then: `.pytest_cache/v/cache/lastfailed`, read
  2026-10-22 by the clarify stage → **109 name-level failures**, including pinned-class
  tests (mirror byte-identity, constitution double-landing, fast-fail contract entries).
- Green verdict = (a) no NEW name-level failures vs the baseline set; (b) pinned tests
  100% retained, pin literals and strength untouched; (c) pinned tests already failing
  in the baseline are pre-existing debt: fix before收口 OR register explicitly under
  `test-evidence/` as a dated pre-existing-debt record (marked as not introduced by
  this scope). The slimming scope must not be the cause of any pinned-test failure.

## 5. Ledger reconciliation (FR-015 audit mechanics)

At close: regenerate the post-slimming id list (same `--collect-only -q` method), then
a deterministic script computes `comm -23 baseline-ids post-ids` and joins each missing
id against `test-evidence/test-consolidation-ledger.md` rows (case-level rows join by
full node id; file-level merge rows join by the declared node-id prefix, mechanically
expanded). Any unmatched id = silent deletion = audit fail. Ledger rows: original id
(or file + prefix), disposition (deleted / case-merge / file-merge / retained),
retained equivalent coverage id, equivalence rationale, date, commit.

## 6. Host scope

达标 host = the 2026-10-22 baseline dev host only: macOS arm64 (OS 26.6.2),
runner-resolved interpreter Python 3.14.6 + pytest 9.1.1. Other hosts / CI numbers are
informational only; every evidence record MUST carry the host identity fields of § 2.

## 7. Serial fallback (FR-017(c))

If the fixed command adopts parallel execution (e.g. `-n auto`), the same command minus
the parallel arguments MUST remain a runnable complete run with unchanged semantics;
its availability proof (one serial full run charged to a 063 slot, or a plan-defined
equivalent verification) is fixed at plan stage and recorded. A degradation serial run
is never达标 evidence (Edge Cases).
