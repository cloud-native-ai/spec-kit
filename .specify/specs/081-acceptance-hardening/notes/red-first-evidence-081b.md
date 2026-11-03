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

## 2. Polish readings (§ 2.1 written by T011; T012 did not run — § 2.2; T010 stopped — § 2.3)

**Part 3 outcome, stated first**: T011 **completed**; T010 **stopped** on a fast-fail (§ 2.3), and
T012 — whose row is `[blockedBy: T005,T009,T010]` — therefore did **not** run. The slice did not
close in part 3; the feature stays `Blocked` and no status was moved.

### 2.1 T011 — the feature's single smoke command, run twice (COMPLETED)

- 081a's record preserved **first**, before either run: `test-evidence/smoke-081a.txt` is a
  byte-identical copy of `test-evidence/smoke-081.txt` as committed at `da5e4480`
  (`diff smoke-081a.txt <(git show HEAD:.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt)`
  → no output). It is kept as a separate file, never merged: 081a's record describes a different tree.
- Run 1 — `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`
  → exit **0** · `1 passed in 1.33s`
- Run 2 — same command, immediately after → exit **0** · `1 passed in 1.21s`
- Identical exit status across the two runs: **yes** (0 / 0) — the property GATE-7 asks for.
- Refreshed `test-evidence/smoke-081.txt` content: **unchanged**. Both runs rewrote the same three
  sub-check blocks 081a recorded — `specify init` exit 0 with the generated `.specify/` tree; the
  closure checker on `positive` (accept, exit 0) and on `negative` (block, exit 1,
  `zero-final-path-pass`); `regen-command-copies.py --check` exit 0 — and `git diff HEAD` on the file
  is empty afterwards. That equality is a *reading* (the file was rewritten, its contents did not
  move), not a skipped refresh.
- **SC-008 stays `partial`**: its final claim is 081d's, over the 081d tree. T011 re-runs the smoke
  on *this* tree and proves nothing about later ones.

### 2.2 T012 — the slice's contract modules: NOT RUN (blocked by T010)

T012's row is `[blockedBy: T005,T009,T010]`. T010 could not complete (§ 2.3), so this row did not
start and `test-evidence/tasks-081b-slice-tests.txt` was **not** written — writing it would have
declared a slice-close record for a slice that did not close.

Measured anyway, as a **diagnostic only** (informational; NOT T012's close record):

```text
$ bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py \
      tests/contract/test_closure_acceptance_check.py tests/contract/test_expression_gates_doc.py \
      tests/contract/test_expression_gate_wiring.py tests/contract/test_premise_carrier_contract.py -q
89 passed in 4.85s          # exit 0
```

That green is confined to the fixtures and to the frozen guards. It says nothing about this
feature's own spec directory, which the checker refuses before it reaches any assertion (§ 2.3) —
which is precisely why it MUST NOT be read as a close record.

### 2.3 T010 — STOPPED: the checker cannot produce a payload for this feature's own spec dir

T010's second instruction is to re-run the closure checker with `--json-out` and **copy** the
acceptance summary from that payload. The payload does not exist: the checker exits `2` (input
error) on this feature's own artifacts. Measured on the unmodified tree at `793aff9e`:

```text
=== P1 — real spec dir, unchanged tree (HEAD 793aff9e) ===
closure-acceptance-check: input error: .specify/specs/081-acceptance-hardening/requirements.md
  § Runtime Stack row RS-001 names a `Contract` path that does not resolve in the checkout:
  pyproject.toml`（`[project] requires-python`）+ `scripts/bash/run-tests.sh`（`resolve_python`） (AS-06)
EXIT=2
```

Peeling that error back one layer at a time on a **temp copy** (`.specify/.tmp/probe-specA`,
`.specify/.tmp/probe-specB` — copies, never the tracked artifacts) shows there are **three**
independent defects, and that repairing the first only exposes the next:

```text
=== P2 — temp copy, only the 3 signed-contract `Contract` cells narrowed to bare resolvable paths ===
closure-acceptance-check: input error: plan.md § Inherited Blockers row IB-003 carries `Source row`
  '071:SC-001_status`（第 66 行）', which is not a `<feature>:<row>` locator — the join key has one
  grammar (C-17)
EXIT=2

=== P3 — temp copy, `Contract` cells + the 5 `Source row` annotations narrowed ===
verdict: block
final_path: pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2
reason: zero-final-path-pass
reason: inherited-blocker-undisposed: 081:SC-001_status
reason: inherited-blocker-undisposed: 081:SC-002_status
reason: inherited-blocker-undisposed: 081:SC-003_status
reason: inherited-blocker-undisposed: 081:SC-005_status
reason: inherited-blocker-undisposed: 081:SC-006_status
reason: inherited-blocker-undisposed: 081:SC-007_status
reason: inherited-blocker-undisposed: 081:SC-008_status
reason: inherited-blocker-undisposed: 081:SC-009_status
reason: inherited-blocker-undisposed: 081:deferred_tasks
EXIT=1
```

The three defects, each with its owner and the rule it contradicts:

| # | Where | Measured | Contradicts |
|---|-------|----------|-------------|
| 1 | `requirements.md` § Runtime Stack, the three `signed-contract` rows (`RS-001`, `RS-002`, `RS-003`) | the `Contract` cells are annotated prose, e.g. `` `pyproject.toml`（`[project] requires-python`）+ `scripts/bash/run-tests.sh`（`resolve_python`） `` — two paths plus two annotations in one cell, and `RS-001` names **two** candidate contract files | owner § Runtime Stack: `Contract` = "repo-relative path of the file the contract actually lives in … it MUST resolve in the checkout"; AS-06 / C-13 make an unresolvable path an input error |
| 2 | `plan.md` § Inherited Blockers, all five disposition rows (`IB-003`, `IB-004`, `IB-006`, `IB-007`, `IB-008`) | every `Source row` cell carries a `（第 N 行）` annotation, e.g. `` `071:SC-001_status`（第 66 行） `` | the same section's own grammar line ("`Source row` = `<feature-id>:<row-locator>`, **no whitespace**", FR-011 `^\S+:\S+$`) and C-17's join key |
| 3 | `scripts/python/closure-acceptance-check.py` — `declared_dependency_files()` + `extracted_dependency_rows()` | any backticked `.md` token in § Inherited Blockers that resolves **under this spec dir** is treated as a dependency artifact, so the section's prose mention of `` `verification.md` `` resolves to *this* spec's own log; the feature id is then read from that log's first line (`# Verification Log — 081-…`) → nine `inherited-blocker-undisposed: 081:*` reasons. Measured: the tokens `requirements.md`, `research.md`, `tasks.md`, `verification.md` all resolve under the spec dir | FR-011 / C-17: the dependency set is "declared, never implied", and a feature cannot be its own dependency — the recorded reading (T010's row, `plan.md` § Readings) is **7/8 records settled + 1 `inherited-later`**, never 9 undisposed rows |

Defect 3 is load-bearing for T010 beyond the two input errors: even with both artifacts repaired,
the checker cannot emit the reading T010 is instructed to record, and any attempt to state
"7/8 settled + 1 `inherited-later`" from a payload would be a hand-computed number the checker
never produced (C-08 forbids exactly that).

**Why the 89-green suite never saw defect 3**: the fixtures declare their dependencies by
fixture-local *filenames* — `tests/fixtures/acceptance-hardening/inherited-clean/plan.md` names
`dependency-feature-901.md` and `dependency-verification-901.md`, which resolve only inside that
fixture directory. A real plan instead writes bare generic filenames in prose (`requirements.md`,
`research.md`, `tasks.md`, `verification.md`), and every one of those also resolves under its own
spec directory. The guard is green against the shape it was written for; the collision only exists
in the shape a real plan has. That is the "the subject must be able to break" question asked of the
wrong subject, and it is recorded here rather than fixed here.

**Consequence for T010**: neither half was performed.

- the SC-005 row was **not** rewritten — its evidence is the checker's own reading of the four
  findings, the three `in-scope` duties and the 8 inherited records, and that reading is the payload
  that does not exist; writing the numbers by hand is the recomputation C-08 forbids;
- the acceptance summary was **not** copied — there is no payload to copy it from;
- `verification.md`'s existing acceptance-summary block therefore still describes the 081a tree and
  MUST NOT be read as this slice's close state.

**Why this stopped here rather than being repaired in passing**: each of the three needs a ruling,
not a correction — `RS-001` names two legitimate contract files and the schema admits one cell
(choosing is inventing intent); `plan.md` and `requirements.md` are outside T010's declared write
scope (its rows write `verification.md` and the evidence paths); and defect 3 is a rule choice about
which tokens constitute a declared dependency artifact, with a fixture suite that currently asserts
the present behaviour. Two of the three are in artifacts the dispatch brief explicitly puts out of
bounds. Recorded, not touched.

The raw transcript of P1/P2/P3 is reproducible from the commands above; the temp copies live under
`.specify/.tmp/` (git-ignored) and were removed after the readings were taken.

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
