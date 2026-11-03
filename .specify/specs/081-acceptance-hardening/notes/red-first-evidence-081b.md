# Red-First Evidence — Feature 081, slice 081b (implement stage)

**Opened**: 2026-11-03 at implement part 1 (T002), HEAD `ce4c0f11`, branch `081-acceptance-hardening`.
**Owner of the obligation**: `tasks.md` § Definition of Done **DoD-2** — red-first may be claimed **only** if a
red run was actually recorded here with **command line, real output, exit status and failing count**; if the
module is authored against a subject that landed in the same part, this note says that instead of claiming a red.
**This file is a dated record of slice 081b.** 081a's `notes/red-first-evidence.md` records a different slice and
MUST NOT be rewritten, merged into, or superseded by anything written here.

**Status of this file**: § 1 is the landing point T002 opens and **T005 fills**; § 2 is filled by T011 and T012 at
Polish; § 3 is the measured state at the moment the landing point was opened. Nothing here is a claim until it
carries a real command, a real exit status and a real failing count — a section that still reads `pending` is
`pending`, not covered.

## 1. The slice's single test carrier

`tests/contract/test_acceptance_premises.py` is the **one** test module this slice names (`plan.md` § D10: the
081b row set MUST name it). It is authored by **T005** and must be red before **T006** (the four findings in
`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`) and **T008** (the closure checker's external-source
extraction) close.

| Leg | What it asserts | Contract clauses | Fixtures it reads |
|---|---|---|---|
| (a) | the four findings fire through `pre-analyze-check.py`, every emitted instance passing the two-part membership test of `requirements.md` § Shared Strings — **including the reserved argument** `runtime-stack` | AS-05, AS-08, AS-09, AS-10; GW-05…GW-07 | `premise-mutation`, `runtime-gap-mutation`, `runtime-zero-row`, `inherited-mutation` |
| (b) | the three `in-scope` duties judged separately and at their own stage: an empty/unresolvable `FR` cell is an input error (exit 2) and never a block; a missing joint-acceptance row naming that `RS-NNN` yields `runtime-dependency-not-owned: RS-NNN` at closure; the tasks-side duty is a **line-level** match with a table-row counterexample that MUST NOT satisfy it | AS-07; C-13 | `positive`, a purpose-built row set |
| (c) | the `inherited` carrier rule: missing carrier, unparseable carrier, unresolvable carrier and a `supporting`-path-SC carrier are all judged as one undisposed row under one reason, while `task:<T-ID>+test:<path>` (both parts) and `gate:<GATE-ID>` pass | AS-10; C-17 | `inherited-mutation`, `inherited-clean` |
| (c2) | the join key: a locator disposed twice is an input error; a dependency row not reproduced verbatim is an undisposed row; extraction is shown to **discover** rows (`inherited-clean` is the counterexample, and its one `inherited-later` row neither blocks nor counts as resolved) | AS-10; C-17 | `inherited-mutation`, `inherited-clean` |
| (d) | cross-producer agreement: for every mutation fixture the closure checker and the pre-analyze gate name the **same** reason instance | FR-006, FR-012; C-17, C-18 | all four mutation fixtures |
| (e) | pin validity: a `pytest --version` / `git --version` reading that differs from `test-evidence/plan-runner-pins.txt` makes that comparison an input error (exit 2), never new failures | AS-07; FR-023 | `test-evidence/plan-runner-pins.txt` |
| (f) | the A13 one-fact rule: the owner states the three carriers once and the plan skeletons carry pointers only | AS-12; FR-019 | `shared/workflow/acceptance-hardening.md`, `templates/plan-template.md` |
| (g) | the runtime-row class's three shapes are three verdicts, with the **zero-data-row** case asserting a block and **not** a silent pass | AS-05; C-13; V-27 | `runtime-zero-row` |
| (h) | the prose rule's arms: a marked declaration with an `RS-NNN` fires; a marked declaration without an id is an input error; an unmarked narrative line carrying an id does not fire; a marker-shaped line inside a fenced code block does not fire | AS-08; C-18 | `runtime-gap-mutation` |

### 1.1 `tests/contract/test_acceptance_premises.py` — red run recorded by T005

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py -q`
- Real output (tail, verbatim — full transcript in the run's console):

```text
# test runner: .venv/bin/python -m pytest tests/contract/test_acceptance_premises.py -q
...
FAILED tests/contract/test_acceptance_premises.py::test_h2_a_marked_declaration_without_an_id_is_an_input_error_naming_the_line
FAILED tests/contract/test_acceptance_premises.py::test_h3_the_fenced_exclusion_is_mechanical_not_a_reading
17 failed, 6 passed in 1.49s
```

- Exit status: **1** · Failing count: **17 failed, 6 passed**
- The 17 red legs are exactly the ones whose subject is T006's four findings or T008's extraction:
  `test_a_every_mutation_fixture_blocks_with_member_instances`, `test_b1…`,
  `test_b1b…`, `test_b3…`, `test_c1…`, `test_c2…`, `test_c3…`, `test_c4…`, `test_c5…`, `test_d…`,
  `test_g1…`, `test_g2…`, `test_g3…`, `test_g4…`, `test_h1…`, `test_h2…`, `test_h3…`.
- The 6 legs that were **already green when authored** are stated rather than dressed up as a red,
  because their subject landed earlier — part 1 for the schema, 081a for the closure verdict:
  `test_a2…` and `test_f…` (T003/T004's owner doc and plan skeleton), `test_a3…` (the membership
  helper reads `requirements.md` § Shared Strings), `test_b2…` (081a's joint-acceptance check),
  `test_c2b…` (the fixtures' own `Path` markers) and `test_e…` (the runner pins recorded by 081a).
- Why a red is claimable here at all: this module is authored **before** T006 and T008 in the same
  part, and it was run against the unmodified checkers — so the red is a measurement of the
  missing implementation, not a re-statement of it.

## 2. Polish readings (written by T011 and T012)

- **T011 — the feature's single smoke command, run twice**: both exit codes, plus the refreshed
  `test-evidence/smoke-081.txt` content, land here; 081a's smoke evidence is preserved first as
  `test-evidence/smoke-081a.txt`. Status: **pending** (part 3).
- **T012 — the slice's contract modules**: `test_acceptance_premises.py`, `test_closure_acceptance_check.py`,
  `test_expression_gates_doc.py`, `test_expression_gate_wiring.py` and `test_premise_carrier_contract.py`, with the
  console transcript written to `test-evidence/tasks-081b-slice-tests.txt`. Status: **pending** (part 3).
- **Not this file's job**: the feature-level id-level baseline comparison is **081d's** (FR-023). This slice's
  narrower observation MUST NOT stand in for it, and no full-suite run is taken in 081b.

## 3. Absence record measured when this landing point was opened (T002)

The state a red run requires, measured — not assumed:

```text
$ for f in tests/contract/test_acceptance_premises.py \
           tests/fixtures/acceptance-hardening/{premise-mutation,runtime-gap-mutation,runtime-zero-row,inherited-mutation,inherited-clean}; do
    if [ -e "$f" ]; then echo "PRESENT $f"; else echo "ABSENT  $f"; fi
  done
ABSENT  tests/contract/test_acceptance_premises.py
PRESENT tests/fixtures/acceptance-hardening/premise-mutation
PRESENT tests/fixtures/acceptance-hardening/runtime-gap-mutation
PRESENT tests/fixtures/acceptance-hardening/runtime-zero-row
PRESENT tests/fixtures/acceptance-hardening/inherited-mutation
PRESENT tests/fixtures/acceptance-hardening/inherited-clean
```

```text
$ bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py -q
# test runner: .venv/bin/python -m pytest tests/contract/test_acceptance_premises.py -q
ERROR: file or directory not found: tests/contract/test_acceptance_premises.py

no tests ran in 0.00s
exit status: 4
```

Exit `4` is pytest's usage error, so the honest reading is **"the module does not exist"**, never "zero failures".
A missing module is not a green and it is not a red; it is the absence that T005's first run resolves one way or
the other. The five fixture directories above are this part's deliverable and are the inputs those runs will read.

## 4. What MUST NOT be written here

- A red that was not run, an output that was not captured, or a failing count that was inferred from a diff.
- A merged or rewritten 081a record: `notes/red-first-evidence.md` stays exactly as 081a left it.
- A pass claimed on a check that could not have gone red — for example a fixture assertion whose subject is a
  fixture the same test just wrote.
