# Red-first evidence — 087 arch-diagram-docs (implement stage)

## Evidence landing points (T001)

- notes: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/notes`
- test-evidence: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/test-evidence`

Both are repository paths under `.specify/specs/087-arch-diagram-docs/`; the absolute forms above are the
resolved reading of the same two directories in this worktree. Every row below quotes the command it ran and
the real output it got — nothing here is copied from a planning-phase projection.

Interpreter used for every reading in this file (the one that can `import typer`):

```text
$ /usr/bin/python3 -c "import sys, typer, pytest; print(sys.version); print('typer', typer.__version__); print('pytest', pytest.__version__)"
3.11.13 (main, May 13 2026, 09:30:18) [GCC 10.2.1 20200825 (Alibaba 10.2.1-3.9 2.32)]
typer 0.27.3
pytest 9.2.0
```

(A bare `python3` that cannot `import typer` reports a false red on the mirror checks; see
`notes/pre-change-measurements.md` § T003 for that trap's measured output. It is an environment gap, never
drift.)

## T008–T012 — the red-first reading (before `--action obligation` existed)

Command, run in the worktree with the typer-capable interpreter:

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py \
    tests/unit/test_docs_utils_carriers.py tests/integration/test_docs_obligation_scenarios.py \
    -q --no-header -p no:cacheprovider
=========================== short test summary info ============================
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_action_registered
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_option_set_closed
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_before_implementation_exit2
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_precedence_order
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_no_backtracking
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_no_second_precedence_owner
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_payload_schema
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_field_order_stable
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_field_set_and_order
FAILED tests/unit/test_docs_utils_carriers.py::test_carriers_typed_dirs_recursive
FAILED tests/unit/test_docs_utils_carriers.py::test_c003_non_carrier_not_judged
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c002_two_runs_identical_json
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c002_no_writes_on_dirty_fixture
13 failed, 1 warning in 0.18s
exit status = 1
```

The cause is the one every one of these assertions is supposed to catch — the action does not exist:

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py::test_c001_action_registered \
    tests/unit/test_docs_utils_carriers.py::test_carriers_typed_dirs_recursive -q
E       AssertionError: `--action obligation` is not a registered choice: usage: docs-utils.py [-h] --action
E                              {scan,expire,clean,archive-check,stats,validate,fix-links,audit}
E                              …
E         docs-utils.py: error: argument --action: invalid choice: 'obligation' (choose from 'scan', 'expire', 'clean', 'archive-check', 'stats', 'validate', 'fix-links', 'audit')
E       assert 2 == 0
```

Thirteen assertions, thirteen reds — no test was written against a behaviour that already worked. The one test
count that does not move is `test_c016_precedence_order`'s per-fixture loop: it fails on its first fixture
(`deleted-rendered`), which is the fixture the contract names as the ordering's sharpest case, so the red names
the intended subject.

### Per-task attribution

| Task | Assertions authored (all red at this point) |
|------|---------------------------------------------|
| T008 | `test_c001_action_registered`, `test_c001_option_set_closed`, `test_c001_before_implementation_exit2` |
| T009 | `test_carriers_typed_dirs_recursive`, `test_c003_non_carrier_not_judged` |
| T010 | `test_c002_two_runs_identical_json`, `test_c002_no_writes_on_dirty_fixture` |
| T011 | `test_c016_precedence_order`, `test_c016_no_backtracking`, `test_c016_no_second_precedence_owner` |
| T012 | `test_c006_payload_schema`, `test_c006_field_order_stable`, `test_c006_field_set_and_order` |

### Fixture build readings (T005–T007)

```text
$ /usr/bin/python3 tests/fixtures/docs-obligation/build_fixtures.py
built 11 fixture spaces: clean, no-diagram, deleted-rendered, orphan-rendered, orphan-source, stale-source, no-trace, trace-incomplete, exempt-ok, exempt-bad, exempt-superseded
OK: 11 docs-obligation fixture spaces match their registered composition
rc=0
```

`copy_fixture` + the `os.utime` step, applied to every space (the mtime fact lands only where a space registers
one):

```text
copy_fixture over all 11 spaces: ok
clean             source=1793954841.1 rendered=1793954841.1 newer=False
stale-source      source=1793954901.1 rendered=1793954841.1 newer=True   (rendered + 60s)
others            (no both-faces pair, or intentionally equal — never stale by accident)
```

The +60s gap on the copy and the post-`utime` assertion are the T007 build step; a filesystem that silently
refused `os.utime` would fail that assertion instead of turning `stale-source/` green on one machine and red on
the next.


## T017–T032 (Part 2) — the red-first reading, and what turned each assertion green

Part 2's order was the one the brief fixes: the assertion first, its red reading recorded, then the engine work
that turns it green. Three readings were taken at three moments, and each red is quoted with the command that
produced it.

### 1. Red, first moment — T025 / T026 / T028 / T029 / T030 asserted before their implementation

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py \
    tests/integration/test_docs_obligation_scenarios.py -q --no-header -p no:cacheprovider
tests/unit/test_docs_utils_obligation.py: FFFFFFFFF..
tests/integration/test_docs_obligation_scenarios.py: FFFF
=========================== short test summary info ============================
FAILED tests/unit/test_docs_utils_obligation.py::test_c005_reason_pairs_closed
FAILED tests/unit/test_docs_utils_obligation.py::test_c005_faces_not_swapped
FAILED tests/unit/test_docs_utils_obligation.py::test_c005_every_entry_named
FAILED tests/unit/test_docs_utils_obligation.py::test_c004_verdict_domain_closed
FAILED tests/unit/test_docs_utils_obligation.py::test_c004_not_evaluated_breaks_clean
FAILED tests/unit/test_docs_utils_obligation.py::test_c013_clean_is_strict
FAILED tests/unit/test_docs_utils_obligation.py::test_c013_converged_ignores_exemptions
FAILED tests/unit/test_docs_utils_obligation.py::test_c013_only_empty_scope
FAILED tests/unit/test_docs_utils_obligation.py::test_c013_documents_field_set
FAILED tests/unit/test_docs_utils_obligation.py::test_c012_four_conditions_closed
FAILED tests/unit/test_docs_utils_obligation.py::test_c015_exit_codes
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c011_exempt_ok
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c011_exempt_bad
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c011_superseded
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c012_trace_incomplete_end_to_end
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c016_deleted_rendered_first
16 failed, N passed
```

Three of those reds were real defects in the Part 1 engine, not assertion bugs — each is quoted with its
symptom because the fix, not the test, was the change:

| Assertion | Red symptom (quoted) | Cause | Fix (engine) |
|---|---|---|---|
| `test_c015_exit_codes` | `--record unreadable ... got 1` | `_load_trace_record` raised `SystemExit(message)`, which is exit **1**, while `C-001`/`C-015` fix input errors at **2** | print to `stderr`, then `raise SystemExit(2)` |
| `test_c012_four_conditions_closed` | `render-unreadable` unreachable: a chmod-000 rendered face read `satisfied` | tier 8 tested the digest rule before the readability rule, so an unreadable face short-circuited to the digest comparison | tier 8 restructured: digest **and** readability are gathered first, readability wins |
| `test_c005_reason_pairs_closed` | the parse found a verdict named `verdict` | the helper read the contract table's header row as data | `if verdict not in VERDICTS: continue` |

The remaining thirteen were red for the intended reason (`exempted` not counted at all; `_superseded` not
reported; `trace-incomplete` masked by `no-trace-record`; the space-level `converged` predicate absent), which
is what T017–T024 then implemented.

### 2. Red, second moment — T031 / T032 (US4) asserted before their subject existed

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_obligation_reuse.py -q --no-header -p no:cacheprovider
=========================== short test summary info ============================
FAILED tests/unit/test_docs_obligation_reuse.py::test_sc005_surfaces_reach_by_reference
FAILED tests/unit/test_docs_obligation_reuse.py::test_sc005_engine_domain_is_single_owner
FAILED tests/unit/test_docs_obligation_reuse.py::test_record_carries_the_four_faces[engine]
FAILED tests/unit/test_docs_obligation_reuse.py::test_record_carries_the_four_faces[engine_reason]
FAILED tests/unit/test_docs_obligation_reuse.py::test_record_carries_the_four_faces[ldm_summary]
FAILED tests/unit/test_docs_obligation_reuse.py::test_record_carries_the_four_faces[delivery]
FAILED tests/unit/test_docs_obligation_reuse.py::test_engine_sticky_on_update
7 failed, 12 passed
```

The four-face and stickiness reds are `C-010` reading the record one face at a time; they turned green without
an engine change — the Part 1 record reader already refuses a record missing any of the four faces — which is
itself the reading: the assertion was measuring the engine, and the engine was already right. The two SC-005
reds are treated separately in § 3.

### 3. Green, final moment — the whole obligation set

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py \
    tests/unit/test_docs_utils_carriers.py tests/integration/test_docs_obligation_scenarios.py \
    tests/unit/test_docs_obligation_reuse.py -q --no-header -p no:cacheprovider
FAILED tests/unit/test_docs_obligation_reuse.py::test_sc005_surfaces_reach_by_reference
1 failed, 66 passed, 1 warning in 3.41s
```

The single remaining red is **declared, not patched**: `test_sc005_surfaces_reach_by_reference` asserts that the
three diagram-producing surfaces (`skills/external/create-docs/SKILL.md`,
`skills/external/improve-docs/SKILL.md`, `templates/commands/docs.md`) name `skills/external/draw-diagram` by
path. That pointer text is T037–T044's and T048/T049's delivery, and T031 lists no `[blockedBy]` on any of
them, so at this point in the task order the assertion must be red. Its red is the evidence that the pointer is
not yet delivered; the alternative (writing the pointer into the skill files from T031) would be executing
T037–T044 ahead of order, outside this Part's territory. Its second half — no surface restates a routing row or
the `ldm_summary` schema — already holds on all three files and is re-checked on every run.

`test_sc005_engine_domain_is_single_owner`'s first draft failed on a **vacuous premise**
(`assert changed` over an empty set, because the only non-excluded file this feature changed under the scanned
roots is `docs-utils.py`, which carries the `.mmd`/`.puml` suffixes and is therefore excluded by name). A
premise that can only be satisfied vacuously is not a premise; it was rewritten so the population
(`tracked_files()`, non-empty) and the claim (no authored file enumerates two or more engine layers) are two
separate readings. That rewrite is a correction, recorded here rather than silently made.

### Per-task red → green attribution (Part 2)

| Task | Assertions | Red reason | Green by |
|---|---|---|---|
| T017–T018 | `test_c005_*` (3), `test_c006_payload_schema` | reason pairs not closed / header row parsed as data | the verdict↔reason table + payload keys |
| T019 | `test_c007_satisfied_requires_all_five`, `test_c007_no_record_not_satisfied` | the five-way conjunction was an "or" over present files | the conjunction |
| T020–T021 | `test_c008_*` (3), `test_c009_*` (3) | both `stale` halves absent; the semantic half had no non-verdict exit | tier 8 time/digest rules; `D-001`'s semantic half produces no verdict |
| T022 | `test_c010_*` (3) | record read was whole-file, not field-by-field | `_load_trace_record` + `_record_path` |
| T023 | `test_c011_exempt_ok/bad/superseded` | exemptions not read at all | `_superseded` flag + `exempted` count |
| T024 | `test_c012_four_conditions_closed` | `render-unreadable` unreachable | tier 8 restructure |
| T025 | `test_c013_*` (5) | no space-level predicate | `converged` / `clean` computed in `cmd_obligation` |
| T026 | `test_c015_exit_codes`, `test_c015_validate_action_intact`, `test_c015_validate_zero_new_violations` | input errors exited 1 | `raise SystemExit(2)` |
| T027 | `test_c016_precedence_order` | tier order was not single-pass | the nine-tier ordered pass |
| T028–T029 | `test_c005_*`, `test_c004_*` | a verdict outside the closed set was reachable | the closed set enforced at the one assignment site |
| T030 | `test_c011_*`, `test_c012_*`, `test_c016_deleted_rendered_first` | end-to-end scenarios had no engine | all of the above |
| T031 | `test_sc005_no_second_engine` (green), `test_sc005_surfaces_reach_by_reference` (declared red) | the pointer text is T037–T044's delivery | — (see § 3) |
| T032 | `test_record_carries_the_four_faces` (×4), `test_engine_sticky_on_update` | red on the record reader, green without engine change | Part 1's reader |

---

## T033–T048 — Part 3 (US4 boundary → US2 baseline/reconcile → US1 authoring)

Interpreter for every reading below: `/usr/bin/python3` — CPython 3.11.13 / pytest 9.2.0 / typer 0.27.3.

### 1. The delivery under test is text plus two scenario families

Part 3's subject is the *flow text* (`skills/external/create-docs/SKILL.md`,
`skills/external/improve-docs/SKILL.md`, `templates/commands/docs.md`) and the checker that text calls
(`docs-utils.py --action obligation`, landed in Part 2). Red-first therefore has two distinguishable reds, and
both were taken before their implementation landed:

- the **assertions** asserting a pointer/section/row that does not exist yet
  (`F::*` in `tests/integration/test_docs_command_scenarios.py`), and
- the **premise** assertions that guard the measurement itself (an anchored heading, a five-row classification
  table, a parameterised assertion actually being parametrised).

### 2. Red, first moment — the flow assertions before T037–T048 (T035/T036/T045/T046/T047)

```text
$ /usr/bin/python3 -m pytest tests/integration/test_docs_command_scenarios.py \
    tests/integration/test_docs_obligation_scenarios.py -q --no-header -p no:cacheprovider --tb=no -rf
FAILED tests/integration/test_docs_command_scenarios.py::test_c002_assets_subsection_present
FAILED tests/integration/test_docs_command_scenarios.py::test_c007_baseline_single_owner
FAILED tests/integration/test_docs_command_scenarios.py::test_c008_authoring_r2_plans_and_r6_checks
FAILED tests/integration/test_docs_command_scenarios.py::test_c010_authoring_flow_produces
FAILED tests/integration/test_docs_command_scenarios.py::test_c013_improve_verify_includes_obligation
FAILED tests/integration/test_docs_command_scenarios.py::test_c014_improve_report
FAILED tests/integration/test_docs_command_scenarios.py::test_c018_improve_docs_literal_kept
FAILED tests/integration/test_docs_command_scenarios.py::test_c020_reader_projection_bounded
FAILED tests/integration/test_docs_command_scenarios.py::test_c021_path_unchanged
FAILED tests/integration/test_docs_command_scenarios.py::test_c022_no_destructive_reclassification
FAILED tests/integration/test_docs_command_scenarios.py::test_sc005_surfaces_reach_by_reference
11 failed, 61 passed
exit status = 1
```

The eleven reds are the delivery named task by task: `test_c002_assets_subsection_present` (T038's `#### Assets`),
`test_c007_baseline_single_owner` (T037's fifth baseline item), `test_c008_authoring_r2_plans_and_r6_checks`
(T039/T040/T041/T042/T043 + T045's authoring wiring), `test_c010_authoring_flow_produces` and
`test_c015_authoring_r2` / `test_c016_authoring_r5_render` / `test_c017_authoring_r6` (T045/T048),
`test_c013_improve_verify_includes_obligation` / `test_c014_improve_report` (T052/T053), and the three
repository-level readings whose subject is a **later** Part (`test_c018_improve_docs_literal_kept` needs the
Diagram-sync row of T050, `test_c020_reader_projection_bounded` is T064's reader section, `test_c021_path_unchanged`
reads that same file's diff line).

### 3. Red, second moment — the premise assertions before their fixtures text existed

Three assertions in this Part are **premises**, not claims: they must be able to say "the thing I am about to
check is present" out loud instead of failing on an empty read (the same defect Part 2 corrected in
`test_sc005_engine_domain_is_single_owner`).

| Premise | Was red because | Fixed by |
|---------|-----------------|----------|
| `F::test_c004_refusal_carried_through` | the three refusal points are `draw-diagram`'s; the assertion has to read them from the owner by path, so it must first assert the owner carries three Step markers | reads `skills/external/draw-diagram/SKILL.md`; red if the owner stops naming Step 2 / 2.5 / 4 |
| `F::test_c012_improve_minimal_edit` | the assertion compares the classification table's row count before/after, so the "before" reading has to be the table's own rows (a five-row table, not an empty parse) | pins the pre-existing five rows by name, then the sixth (`Diagram-sync`) |
| `F::test_c020_reader_projection_bounded` | an absent section and a section of zero lines are different states; the assertion must distinguish them | requires the heading to exist, then bounds it to ≤ 12 lines |

### 4. What actually turned green, measured at the end of Part 3

The four rows above are the expected readings; these are the measured ones (`tests/integration/test_docs_command_scenarios.py`
plus `tests/integration/test_docs_obligation_scenarios.py`):

```text
$ /usr/bin/python3 -m pytest tests/integration/test_docs_obligation_scenarios.py     tests/integration/test_docs_command_scenarios.py -q --no-header -p no:cacheprovider --tb=no -rf
9 failed, 39 passed
```

The nine reds are all owned by later rows, one line each:

| Red | Owner |
|-----|-------|
| `test_c002_by_reference_only` (its `improve-docs` leg) | T058 / T049 |
| `test_c011_improve_pointer` … `test_c015_named_staleness_keeps_source` (5) | T049–T053 |
| `test_c016_dispatch_names_both_paths`, `test_c017_residual_five_counts` | T063 |
| `test_c020_reader_projection_bounded` | T064 |

`test_c021_path_unchanged` is **green**: it measures that the reader document was not renamed, deleted or
dropped from the area map — which is exactly true in Part 3, where `docs/` is deliberately untouched.

### 5. The one cross-Part red that stays red until its own Part

`tests/unit/test_docs_obligation_reuse.py::test_sc005_surfaces_reach_by_reference` (authored by T031 in Part 2)
asserts that all three diagram-producing surfaces name `skills/external/draw-diagram`. After T037–T048 two of the
three do (`create-docs/SKILL.md`, `templates/commands/docs.md`); the third, `improve-docs/SKILL.md`, is delivered
by **T058** (Part 4, on T049's evidence step). The assertion therefore stays red at the end of Part 3 **by
construction**, and is declared as remaining work rather than patched: writing the `improve-docs` pointer here
would execute T049/T058 out of order.

### 6. Two authoring-test repairs the measured readings forced

Both are in the test helper layer, never in the owner text, and both were found by a *false green* rather than by
a red — which is why they are recorded here:

- `section()` cuts a heading's body at the next heading of any level, so a `####` child of a `###` section was
  invisible to `subsection()`. The child-must-sit-inside-parent claim could therefore never fail. Fixed by
  measuring the child's scope inside a parent scope that runs to the next heading at the parent's own level.
- `bullet_after()` matched the step marker anywhere in a line, so R4's sentence cross-referencing "R6" resolved
  to R6's bullet, and R4's own cross-reference to "R3"/"R5" made the label ambiguous. Fixed by anchoring on the
  bullet's label token (`R5`, `R5 写作收敛`), which also keeps an indented `R6` sub-bullet from matching `R4`.
