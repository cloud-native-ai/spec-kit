# Tasks-stage deterministic checks — Feature 074

Recorded 2026-10-28 during `/speckit.tasks` for
`.specify/specs/074-goal-team-sdd-unification`. Every line below is a command that was actually run
in this repository at `stage_base=6297c14f6`, followed by its real output. Nothing here is a
pre-written expectation.

Test budget for this stage: **targeted-set-v1** (stage_base `6297c14f6`); the tasks stage edits no
source and no test, so the targeted set has no new subject — it is run as the recorded baseline the
implementation stage compares against.

## 1. Structural validation of the generated tasks.md

```bash
python3 .specify/scripts/python/validate-tasks.py .specify/specs/074-goal-team-sdd-unification/tasks.md
```

```text
PASS: .specify/specs/074-goal-team-sdd-unification/tasks.md — 0 error(s), 0 warning(s)
rc=0
```

One warning was raised by the first draft and repaired before this record:
`green-cross-phase` on `contracts/report-and-attribution.md` — T028 claimed `#C-53` while T029 (the
next row) claimed `#C-50`, so the clause order ran backwards against row order. The partition was
re-cut (T028 → C-47/C-48/C-49; T029 → C-50…C-54) rather than the warning being silenced.

## 2. Clause partition and task population

```bash
grep -oE '\[green: [^]]+\]' tasks.md      # 68 matches
grep -oE '\[green: <contract>#[^]]+\]' …  # the Format section's own tag definition is the 68th
grep -cE '^- \[ \] T[0-9]{3}' tasks.md
```

```text
task rows: 57   (US1 9, US2 7, US3 5, US4 9, US5 6, non-story 21)
[P] rows: 11
[green:] claims: 67  — C-1…C-67, each exactly once, one claim per clause
```

Clause partition by contract file (claims in ascending clause order within each file, which is what
the validator's `green-cross-phase` check measures):

| Contract file | Clauses | Claiming rows |
|---|---|---|
| `route-decision.md` | C-1…C-14 | T017–T021 |
| `authorization-and-probe.md` | C-15…C-30 | T008–T011, T023–T026, T047 |
| `nested-invocation.md` | C-31…C-46 | T013, T014, T030–T035 |
| `report-and-attribution.md` | C-47…C-54 | T028, T029 |
| `diffusion-and-compat.md` | C-55…C-67 | T037–T041, T046–T051 |

## 3. Clause and FR coverage accounting (green)

```bash
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification --freeze > .specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074-goal-team-sdd-unification
```

```text
freeze rc=0 ; coverage-baseline.txt = 497 lines (2 header + 495 names), base-sha 6297c14f68fd
claimed clauses (this feature): 67
baseline: .specify/specs/074-goal-team-sdd-unification/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 28 / FR claimed: 28 / FR uncovered: 0
  [clause-uncovered] pass (495) — 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 28 of 28 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files declare no positive clause form (parse doubt, never read as covered)
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
status: ok ; rc=0
```

The clause lane was `status: baseline-missing` at the plan stage by design; it freezes here, once
the `[green:]` claims exist, which is the timing plan.md § Phase 1 named. Freezing before the
claims existed would have made this lane trivially green.

## 4. Targeted-set-v1 baseline at `stage_base=6297c14f6`

```bash
python3 -m pytest -q tests/contract/test_agent_dispatch_mechanism.py \
  tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py \
  tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py \
  tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py \
  tests/contract/test_instructions_section_propagation.py tests/contract/test_flow_class_ledger.py \
  tests/contract/test_flow_class_correctness.py tests/contract/test_shipped_agent_presets.py
```

```text
191 passed in 21.61s
rc=0
```

`stage-status` line (six fields):

```text
status=run ; command="python3 -m pytest -q <13 files>" ; selection_basis="suites that pin every surface this feature edits (anti-nesting, dispatch governance, neutral metadata schema + tool mapping, driver skill, team command routing, goal definition, instructions section propagation, flow-class ledger)" ; selected_paths=13 files as listed above ; sufficiency="each edited source surface has a pinning suite; the set is also the pre-change case set for FR-026/FR-027/SC-005" ; rc=0 ; passed-failed="191 passed / 0 failed" ; new_failures=[] ; baseline=191 passed at 6297c14f6 (test-evidence/targeted-set-v1-baseline.txt)
```

## 5. Plan-owned artifact touch (declared, minor)

```bash
grep -n 'new test files\|test files are new' .specify/specs/074-goal-team-sdd-unification/plan.md
```

Two prose counts said "7 new test files" / "seven test files are new" while every enumerated source
in the plan-owned set says six: `plan.md` § Source Code lists six `NEW` test files,
`feature-ref.md` § 2 rows 13–18 list six, `research.md` R14 says "six new contract/unit test files",
and each contract's "Pinned by" line resolves to that same six. Both phrases were corrected to
`6` / `six` — a line-level consistency repair, no change to scope, architecture, data-model,
contract semantics, FR/SC content, or task breakdown.
