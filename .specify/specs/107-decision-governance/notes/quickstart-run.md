# Quickstart execution record — 107-decision-governance (T055)

Executed: 2026-11-26 (UTC), worktree `decision-governance`, branch `107-decision-governance`.
Every scenario in `.specify/specs/107-decision-governance/quickstart.md` was run exactly as
written (the planned-surface commands after landing; the executed-today commands re-run).
Interpreter: the quickstart's literal `python3` (stdlib-only checker; the test entry keeps its
`SPECKIT_PYTHON` pin and is not used here). Teardown: the scenarios create no state — the
checker is read-only and the git/scan commands are read-only; the only scratch workspace lived
under the sanctioned `.specify/.tmp/` root and was removed after capture.

## Scenario 1 — author one ai-autonomous decision record (planned surface)

$ python3 scripts/python/validate-decisions.py --action records --spec .specify/specs/107-decision-governance
```text
PASS: 0 violation(s) (rules: M-01, M-02, M-03, M-04, M-08, M-09)
```
EXIT=0. The spec's own carriers judge clean; 16 legacy register rows are reported (not judged).

## Scenario 2 — the two production accidents are blocked (planned surface)

$ python3 scripts/python/validate-decisions.py --action records --spec .specify/specs/107-decision-governance --json
```text
{ "status": "pass", ..., "violations": [] }
```
EXIT=0. The red→green halves of both accidents run against the guard fixtures today:
`M-02 .../m02/red-empty-locator.md` = red, `.../green-complete.md` = green;
`M-08 .../m08/red-variant.md` (with the stubbed glossary) = red, `.../green-full-name.md` =
green — asserted by `tests/contract/test_decision_governance_guards.py`
(`test_m02_locator_red_then_green`, `test_m08_registered_variant_red`).

## Scenario 3 — closed option set (planned surface)

Same command as scenario 1 (the spec's carriers carry no option defect). The reverse samples
execute individually:
```text
M-03 tests/fixtures/decision-governance/m03/red-empty-set.md: the option set is empty        EXIT=1
M-03 .../red-duplicate-label.md / red-other-without-path.md / red-missing-reversibility.md   EXIT=1 each
M-03 .../green-complete.md                                                                   EXIT=0
```
Pinned by `tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples`.

## Scenario 4 — decision transmission round-trip (planned surface)

$ python3 scripts/python/validate-decisions.py --action payload --fixture tests/fixtures/decision-governance/m06/
```text
M-06 .../red-no-block.md:1: a decision-backed dispatch MUST carry a decision_block ... (the decision_block is absent)
FAIL: 6 violation(s)
```
EXIT=1 (the m06 directory is the reverse-sample set: five missing-field samples + the no-block
sample). The complete payload and the legal non-decision payload exit 0.

$ python3 scripts/python/validate-decisions.py --action chain --fixture tests/fixtures/decision-governance/m07/
```text
M-07 .../red-missing-record.md:1: the record segment is missing; ...
FAIL: 6 violation(s)
```
EXIT=1 (the m07 directory is the reverse-sample set; the green chain exits 0, asserted by
`test_m07_chain_three_segments`).

## Scenario 5 — audit reconstruction (planned surface)

$ git -C . diff --numstat 08b59695c..HEAD -- .specify/register.md .specify/specs/107-decision-governance/checkpoints .specify/specs/107-decision-governance/plan.md
```text
14	0	.specify/register.md
34	0	.specify/specs/107-decision-governance/checkpoints/05-goal-team-activation.md
26	0	.specify/specs/107-decision-governance/checkpoints/06-checklist.md
6	0	.specify/specs/107-decision-governance/checkpoints/07-analyze.md
217	0	.specify/specs/107-decision-governance/plan.md
```
EXIT=0; every line's deleted column is 0 (appended rows and files added after the base only).

$ python3 scripts/python/validate-decisions.py --action records --fixture tests/fixtures/decision-governance/reconstruct --register tests/fixtures/decision-governance/reconstruct/register.md
```text
PASS: 0 violation(s) (rules: M-01, M-02, M-03, M-04, M-08, M-09)
```
EXIT=0 — the four-carrier fixture set reconstructs all four records from register + carriers.

The planned red halves execute individually:
```text
M-01 tests/fixtures/decision-governance/m01/red-missing-actor.md:3: missing base-layer field(s): actor
     EXIT=1
M-09 tests/fixtures/decision-governance/m09/red-broken.md:20: evidence pointer
     'tests/fixtures/decision-governance/m09/does-not-exist.md' does not resolve
     EXIT=1
```

## Scenario 6 — legacy read and mirror closure (executed today)

$ grep -rn '^### D-' .specify/specs --include='*.md' | wc -l
```text
39
```
Unchanged from the measured pre-change count; all one/two-digit legacy headings, three-digit
record-form headings still 0.

$ python3 scripts/python/sync-mirrors.py --check        # EXIT=0, no drift member
$ python3 scripts/python/regen-command-copies.py --check   # EXIT=0 (all copies match)
$ python3 scripts/python/scan-confirmation-gates.py --summary
```text
blocking confirmation gates: 30
  destructive: 22
  governance_kept: 7
  reversible: 1
violations (reversible gates still blocking): 0
```
The acceptance reading is the delta against the recorded baselines, which is zero-new on all
three (`test-evidence/sync-mirrors-baseline.txt`, `regen-copies-baseline.txt`,
`scan-confirmation-gates-baseline.txt` + the adjudicated 31 -> 30 re-baseline in
`test-evidence/gate-neutrality.txt`).
