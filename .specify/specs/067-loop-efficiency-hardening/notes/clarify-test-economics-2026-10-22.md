# Clarify Rulings — test economics (P2-clarify-test-economics, 2026-10-22)

Dated record backing `requirements.md` § Clarifications
`Session 2026-10-22（clarify：测试经济学裁决）`. No pytest run in this stage; no
pass/fail claimed anywhere below.

## Evidence read this stage

- `.pytest_cache/v/cache/lastfailed` (2026-10-22 read): **109** name-level failures.
  Mechanical check: `json.load` key count = 109. Sample pinned-class entries present in
  the set (provisional record; authoritative set = driver's full-run FAILED list):
  `tests/contract/test_fast_fail_discipline.py::test_x13_double_landing_three_count_pins`,
  `tests/contract/test_constitution_double_landing.py::test_c1_template_carries_both_new_principles`,
  `tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean`,
  plus multiple mirror byte-identity tests (`test_derivation_definitions`,
  `test_derive_command_surface`, `test_docs_command_template`, `test_ask_record_repeat`).
  Consequence: an absolute "pinned tests are green" criterion is already falsified by
  the pre-slimming baseline regardless of slimming work — SC-008/FR-018 green wording
  is re-based to baseline-failure-set semantics (no NEW failures + explicit pre-existing
  debt), preserving the anti-regression intent.
- Host identity (probe this stage): macOS arm64, OS 26.6.2; interpreter versions
  (Python 3.14.6 / pytest 9.1.1) cited from the P1 dated record
  `notes/test-slimming-scope-2026-10-22.md`, not re-measured.
- Baseline full-run log: still in flight at ~82% progress, no `elapsed=` footer —
  NOT read as evidence, not cited, not committed by this part.

## Ruling rationale (7 open items)

1. **Parallel dev-only deps**: admitted (pytest-xdist or equivalent) under FR-017
   (a)(b)(c); serial path stays the default runnable mode; network-free; zero runtime
   dependency expansion. Rationale: suite cost is dominated by per-test subprocess cold
   starts and workspace copies, which parallelism distributes across workers; it is the
   standard acceleration that does not touch coverage or the runtime package.
2. **Measurement basis**: cold-cache complete run as the primary口径 (cache clear
   contiguous with the measured run; ≤1 warm-up allowed, before the clear, never
   counted); wrapper epoch-difference wall clock; fixed command pinned at plan stage and
   reused verbatim post-slimming. Rationale: cold is the conservative, non-gameable
   basis (warm cache could otherwise absorb the very cold starts this spec removes);
   the protocol file owns exact mechanics.
3. **Host scope**: this dev host only (macOS arm64, Python 3.14.6, pytest 9.1.1);
   other hosts/CI informational. Rationale: no CI exists (dated fact in the spec's
   现状锚点), and a second达标口径 would double the measurement cost for no user goal.
4. **Baseline id list**: `--collect-only -q` node-id full set →
   `test-evidence/baseline-test-ids.txt`; generated at implement start (before the
   first consolidation task, after the baseline run completes). Not generated in this
   stage — pytest runs are forbidden while the baseline holds the machine; recorded as
   an implement obligation, not a clarify gap.
5. **Baseline failure-set semantics**: SC-008 green re-based (see evidence above);
   debt rule: fix or register; injection drill unchanged and absolute.
6. **Consolidation granularity & ledger**: file-level and case-level merges both
   allowed; ledger stays the FR-015 single append-only file (sequential implement
   dispatch chain — no two concurrent writers expected; rows carry date + commit so
   attribution survives); audit join is deterministic (`comm -23` + ledger join,
   file-level rows expanded by prefix).
7. **Complete-run boundary**: confirmed verbatim as FR-011 states it (single runner
   invocation, no path/`-k`/`-m` filters, all three layers, collection + fixture time
   included, diagnostic markers composition-neutral); measurement runs must not be
   wrapped in retry/loop shells.

## Same-author note

This stage ran as a fresh-context read-only-context subagent dispatched by the driver;
the seven candidate questions were enumerated by the driver's part brief from the P1
artifact, so the coverage scan did not inherit the requirements author's own reading
(`objective-analysis-gate.md` condition not met — no further delegation needed).

## Files touched by this part

`requirements.md` (Assumptions resolved, FR-012/FR-018/SC-007 Source/SC-008 minimal
revisions, 现状锚点 lastfailed line, Clarifications session appended) + this file +
`test-evidence/measurement-protocol-2026-10-22.md`. Nothing under `tests/`, `scripts/`,
`pyproject.toml`, source, mirrors, or registries was modified.
