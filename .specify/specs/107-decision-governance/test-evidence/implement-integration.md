# Implement integration — 107-decision-governance

Stage `implement` of line `decision-governance` (run id `r20261125T134500Z-107a`), single
closing execution by the stage integrator. Branch `107-decision-governance`, worktree
`.specify/.tmp/sdd-loop/worktrees/decision-governance`, merged base `0d7519521`
(includes the 106 merge).

## Integration order

P1 → P2 → P3 → P4 → P5, serial in one shared worktree (the decomposition's declared
write-alone order). Part commits are not rewritten; this integration adds one closing
commit on top of `7c1d882b0`.

## Coverage — 56/56

Program-checked over the five package verdicts (not eyeballed): every row T001–T056 is
covered by exactly one check row, every check result is `pass`, zero missing, zero
duplicate, zero non-pass, and each package's range is contiguous:

| Package | Task range | Check rows | Verdict |
|---------|-----------|------------|---------|
| P1 | T001–T008 | 8 | pass |
| P2 | T009–T017 | 9 | pass |
| P3 | T018–T031 | 14 | pass |
| P4 | T032–T045 | 14 | pass |
| P5 | T046–T056 | 11 | pass |

The verdict JSONs are runtime state under `.specify/state/wp/` (git-ignored per
`.specify/.gitignore`), so they are cited, not committed:

- `decision-governance-implement-p1-a1.verdict.json` (verified 04:43:55Z)
- `decision-governance-implement-p2-a1.verdict.json` (verified 04:59:48Z)
- `decision-governance-implement-p3-a1.verdict.json` (verified 05:20:40Z)
- `decision-governance-implement-p4-a1.verdict.json` (verified 05:44:33Z)
- `decision-governance-implement-p5-a1.verdict.json` (verified 06:07:18Z)

Package commit ranges as dispatched (endpoints inclusive; each verdict's
`evidence_refs` carries its complete commit list):

- P1 `98bf3328a..4e4d79fa6`, P2 `98bee6d2c..b3c702a2c`, P3 `57fc19258..5be7f0694`,
  P4 `9398f50e6..36bf03649`, P5 `68b9e1866..7c1d882b0`.

The substance behind each verdict lives in this spec's committed evidence:
`notes/` (red-first slots, per-package green records, quickstart run) and
`test-evidence/` (phase logs, mirror checks, gate neutrality, mutation drill,
migration closure, preservation sweep, verification input).

## Task-table closure

All 56 rows flipped `- [ ]` → `- [X]` by this integration with task text untouched
(diff verified: 56 single-token checkbox changes, zero text changes).
`validate-tasks.py .specify/specs/107-decision-governance/tasks.md` → PASS, 0 errors,
0 warnings.

## Test readings

**Stage-start baseline (the line's single baseline slot, TB-02/TB-03).** Full suite at
`0d7519521` through the single runner: **221 failed / 10,152 passed**, failed names in
`baseline-failed.txt` (221 names); evidence `test-evidence/implement-baseline.txt` and
`implement-baseline-rerun.log`; trunk baseline 217. TB-03 forbids a second full suite
inside `implement` — the closure slot belongs to the post-review close-out.

**Five enumerated worktree-environment deltas** (`test-evidence/implement-baseline-environment-deltas.md`,
each reproduced individually, expected green on the trunk):

1. `tests/contract/test_ask_record_repeat.py::test_canonical_engine_does_not_self_resolve_to_the_framework_repo` — path-resolution guard tuned for a normal checkout (worktree `.git` is a file).
2. `tests/contract/test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool` — runtime-copy presence resolution in the worktree.
3. `tests/contract/test_execution_config_engine.py::TestErrorsAndWarnings::test_warning_surface_is_json_and_stderr` — execution-config default resolution in the worktree.
4. `tests/contract/test_settlement_preservation.py::test_test_budget_keeps_one_baseline_and_at_most_one_closure_slot` — reads the state spine from the main repo path.
5. `tests/integration/test_trigger_telemetry.py::test_cli_subprocess_smoke_pins_payload_and_exit_semantics` — CLI subprocess root resolution in the worktree.

**Targeted batteries at HEAD (per-package verifier re-runs).**

- P1: contracts module 5 passed; unit CLI surface 1 passed.
- P2: recorded phase run 10 passed; verifier re-run 11 passed.
- P3: 23 passed (5 unit + 12 contract + 6 guard nodes).
- P4: 37 passed battery; US4 phase 14 passed; US5 phase 32 passed.
- P5: US6 phase 21 passed; five-module smoke 43 passed.
- Preservation sweep (T054): 5 failed / 241 passed, all five names inside
  `baseline-failed.txt`, `comm -13` empty — zero new failure names.

**Closure-time names-level reading (this integration).** The five failed node ids were
extracted programmatically from the recorded T054 sweep into
`test-evidence/closure-failed-names-preservation-sweep.txt` (5 names) and compared to
`baseline-failed.txt`: added = none. Scope: the six protected modules of the T054 sweep,
not a second full suite (TB-03); the full-suite names-level closure comparison remains
the post-review closure slot's obligation.

**Mirror / copy / budget closure.** `sync-mirrors.py --check` rc 0 — six trees
byte-identical (templates 23, skills/external 394, skills/internal 139, agents 20,
scripts 133, shared 117), zero drift against `sync-mirrors-baseline.txt`;
`regen-command-copies.py --check` rc 0; all 19 byte-identical plan pairs cmp-verified and
the projected `generate-instructions.sh` pair reported ok; Decision Items section 1,276 B
in template and live alike; live total 40,170 B < `INSTRUCTIONS_BUDGET_BYTES` 40,960.

**Gate neutrality.** `scan-confirmation-gates.py --summary`: 30 blocking / 22 destructive
/ 7 governance_kept / 1 reversible / 0 violations against the re-baselined 31 (the one
removed member — the 106 merge's `superagent-definitions.md` Termination line — is
adjudicated in `test-evidence/gate-neutrality.txt`; added set empty). FR-025:
`git diff --quiet fbab7a45c..HEAD` on the three protected paths rc 0, `--numstat` zero
rows.

## Residuals (disclosed P5 anomalies)

1. **C-503 surface wording.** The criterion's sentence names "the `.specify/instructions.md`
   convergence item"; the measured migrate surface converges
   `templates/instructions-template.md` under the existing `templates-generated`
   dimension and never compares the generated file directly. Corrected reading disclosed
   in `test-evidence/migration-closure.md` § Disclosure and pinned by the passing
   `test_instructions_generated_dimension`.
2. **Glossary premise.** T053's literal expectation — `git diff d05c3a350..HEAD --
   .specify/glossary.md` empty — does not hold on the merged tree: 106's own `silent-end`
   proposed row arrived with the merge. The judged FR-005 property holds: this feature
   wrote no glossary entry (`grep -c Decision` = 0; feature-scope diff
   `36bf03649..HEAD` empty; both proposal files present). Disclosed in
   `test-evidence/glossary-discipline.txt`.
3. **Stale section-count pin (repaired at its root).** The added
   `## Decision Items（决策项）` section required the section-count pin in
   `tests/contract/test_fast_fail_discipline.py` to move 38/39 → 39/40; repaired in
   `75af9f5eb` with the dated stale-pin note, measured 39/40, post-repair sweep shows
   zero new failure names.
4. **Illustrative text only.** The T054 sweep prose's G-9 example cites "frozen 31"
   while the 050 frozen baseline is 23; illustrative wording, the failed-set reading is
   unaffected (verifier-disclosed in the P5 verdict).

No contradiction was found between package outputs. Closing commit carries the closed
task table, this record and the closure names file; the five part commits and all
implementation content are otherwise untouched.
