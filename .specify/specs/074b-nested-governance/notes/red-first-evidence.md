# Red-first evidence — slice 074b-nested-governance

Append-only evidence sink for this slice's red→green cycles. Each entry records the command, the real
output and the exit code. Nothing here is a paraphrase of a run: the blocks are pasted.

## E-1 · `tests/contract/test_nested_run_report.py` — RED (T004)

**Captured**: 2026-10-29T05:58Z, HEAD `241a6082b`, after the suite was written and before any edit of the
report contract.
**Red shape**: the mandatory section does not exist, so the cases fail as a *missing section*, not as a
contradictory assertion.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
FFFFFFFFFFFFF.FF                                                         [100%]
=================================== FAILURES ===================================
____________ test_heading_literal_is_stated_verbatim_and_line_exact ____________

    def test_heading_literal_is_stated_verbatim_and_line_exact():
        text = _read(CREATE_TEAM)
        exact = [line for line in text.splitlines() if line.strip() == HEADING_LITERAL]
>       assert len(exact) == 1, (
            f"the report contract MUST state {HEADING_LITERAL!r} verbatim on its own line "
            f"exactly once (C-21); found {len(exact)} line-exact occurrences"
        )
E       AssertionError: the report contract MUST state '## Nested SDD Runs' verbatim on its own line exactly once (C-21); found 0 line-exact occurrences
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_nested_run_report.py:249: AssertionError
________ test_the_literal_lands_in_exactly_one_shipped_source_document _________

    def test_the_literal_lands_in_exactly_one_shipped_source_document():
        holders = _documents_carrying(HEADING_LITERAL)
>       assert holders == ["skills/internal/create-team/SKILL.md"], (
            "the heading literal MUST have exactly one definition point, the report contract "
            f"(C-21 / C-30); documents carrying it: {holders}"
        )
E       AssertionError: the heading literal MUST have exactly one definition point, the report contract (C-21 / C-30); documents carrying it: []
E       assert [] == ['skills/inte...eam/SKILL.md']
E         Right contains one more item: 'skills/internal/create-team/SKILL.md'

tests/contract/test_nested_run_report.py:267: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_nested_run_report.py::test_heading_literal_is_stated_verbatim_and_line_exact
FAILED tests/contract/test_nested_run_report.py::test_the_literal_lands_in_exactly_one_shipped_source_document
FAILED tests/contract/test_nested_run_report.py::test_the_section_is_appended_after_an_unchanged_section_list
FAILED tests/contract/test_nested_run_report.py::test_section_is_mandatory_for_every_run_in_both_pattern_families
FAILED tests/contract/test_nested_run_report.py::test_no_invocation_is_stated_explicitly_and_omission_is_a_violation
FAILED tests/contract/test_nested_run_report.py::test_per_invocation_row_carries_five_fields_and_the_closed_outcome_set
FAILED tests/contract/test_nested_run_report.py::test_blocked_and_failed_are_carried_through_never_dressed_as_success
FAILED tests/contract/test_nested_run_report.py::test_paths_are_carried_as_paths_and_bodies_are_never_inlined
FAILED tests/contract/test_nested_run_report.py::test_nested_section_is_a_peer_of_verification_not_a_replacement
FAILED tests/contract/test_nested_run_report.py::test_routing_verdict_is_a_reference_and_a_missing_record_is_never_rederived
FAILED tests/contract/test_nested_run_report.py::test_handoff_fields_are_read_by_reference_and_an_incomplete_handoff_is_not_success
FAILED tests/contract/test_nested_run_report.py::test_supervisor_is_the_sole_writer_and_a_nested_run_writes_no_tracked_artifact
FAILED tests/contract/test_nested_run_report.py::test_attribution_reuses_the_existing_ledger_field_and_adds_no_goal_field
FAILED tests/contract/test_nested_run_report.py::test_attribution_cardinality_is_exactly_one_with_a_target_and_none_without
FAILED tests/contract/test_nested_run_report.py::test_single_owner_audit_across_the_three_skill_documents
======================== 15 failed, 1 passed in 0.18s ========================
rc=1
```

**Reading of the one green case in the red run**: `test_attribution_is_observational_so_the_goal_field_set_is_unchanged`
executes the SC-002 instrument (`goal-utils.parse_goal` over the `074a` fixture Goal, before and after the
supervisor's ledger row). It is green at the pre-change commit because no change has been made to the Goal
yet — that is exactly the invariance it pins, and it stays green after the edit. It is executed rather than
asserted on purpose: a prose-only test of "the Goal field set is unchanged" would prove nothing.

## E-2 · `tests/contract/test_nested_run_report.py` — GREEN (T005–T007 landed)

**Captured**: 2026-10-29T06:05Z, after the report contract gained the mandatory section.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
................                                                         [100%]
16 passed in 0.08s
rc=0
```

The same 16 cases that were red in E-1 are the ones now green; no case was removed, renamed or relaxed
between the two runs.

## Single-owner audit (T008)

```text
$ grep -n 'Nested SDD Runs' skills/internal/create-team/SKILL.md skills/internal/run-team/SKILL.md skills/internal/run-agent/SKILL.md
skills/internal/create-team/SKILL.md:63:## Nested SDD Runs
skills/internal/create-team/SKILL.md:76:### Nested SDD Runs section（必填段,本节为该段的唯一真源）
skills/internal/create-team/SKILL.md:78:每个 run 报告 MUST 在既有必填段之后**末尾追加**一个嵌套段,标题字面量逐字为 `## Nested SDD Runs`(不得改写、不得改变标题层级、不得并入其它段)。该段对**每次运行**强制 —— 有界 pattern(parallel / serial / iteration)与 continuous 一律适用,与该次运行是否真的发生过嵌套 SDD 调用无关。既有必填段的名称、次序与内容义务逐字不变;MUST NOT 省略该段,省略即判违约。
rc=0

$ for f in <the three skill documents>; do echo "$(grep -c 'Nested SDD Runs' $f) $f"; done
3 skills/internal/create-team/SKILL.md
0 skills/internal/run-team/SKILL.md
0 skills/internal/run-agent/SKILL.md

$ grep -n '报告契约' skills/internal/run-team/SKILL.md
66:执行结束后把带日期的运行报告写入 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`(**每次运行强制**,报告契约真源:create-team SKILL.md → Report;含 `## Verification` 节)。…
```

**Reading**: all three occurrences live in the one owner (`create-team/SKILL.md` § Report contract) — the
skeleton literal, the subsection heading that states the obligation, and the sentence naming the literal.
`run-team` keeps delegating at `:66` and gains no second statement; `run-agent` is untouched by this face.
Measured per **document**, which is the unit "one owner" is decidable in.

## E-3 · `tests/contract/test_nested_run_report.py` — GREEN (T009, US1 closed)

**Captured**: 2026-10-29T06:0Z, HEAD `f26eb59ac`, at the start of implement part 2, before any Phase 3 edit.
No case was added, renamed, relaxed or removed relative to E-1/E-2.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
................                                                         [100%]
16 passed in 0.08s
rc=0
```

**Reading**: US1's acceptance surface is green at the part-2 base commit, so US2's edits can be judged
against a known-green neighbour rather than against a moving one.

## E-4 · `tests/contract/test_sdd_diffusion.py` — RED (T010)

**Captured**: 2026-10-29T06:2Z, HEAD `f26eb59ac`, after the suite was written and before any Phase 3 edit.
**Red shape**: the four diffusion surfaces are not landed yet, so the surface cases fail as *absent
statements/sections*, not as contradictory assertions.

```text
$ python3 -m pytest -q tests/contract/test_sdd_diffusion.py
FF.F.FFFFFF..F.                                                          [100%]
=================================== FAILURES ===================================
____ test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation _____

    def test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation():
        bullet = _stage_bullet()
        stated = re.findall(r"`([^`]+)`", bullet.split("(canonical names")[0])
>       assert tuple(stated) == TEAM_STAGE_VALUES, (...)
>       assert "SDD" in bullet and re.search(r"阶段名册|roster", bullet), (
            "the added text MUST state that this dimension is not the SDD stage roster (C-13)"
        )
E       AssertionError: the added text MUST state that this dimension is not the SDD stage roster (C-13)

______________________ test_no_added_surface_enumerates_the_sdd_stage_roster ______________________
E       in _added_texts -> hosting = _hosting_paragraph()
E       AssertionError: the authoring baseline must carry exactly one hosting-responsibility
        paragraph (C-17), found 0

=================== short test summary info ====================
FAILED tests/contract/test_sdd_diffusion.py::test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation
FAILED tests/contract/test_sdd_diffusion.py::test_no_added_surface_enumerates_the_sdd_stage_roster
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_states_the_three_responsibilities_and_the_together_reading
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_sits_immediately_after_the_existing_key_paragraph
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_points_at_the_key_set_owner_and_restates_no_domain
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_carry_exactly_one_routing_pointer_section
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_pointer_restates_no_owner_fact
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_section_declares_and_respects_its_own_byte_ceiling
FAILED tests/contract/test_sdd_diffusion.py::test_trigger_gains_the_conjunction_sentence_inside_an_existing_section
FAILED tests/contract/test_sdd_diffusion.py::test_generated_instructions_carry_the_section_verbatim_and_follow_the_symlinks
10 failed, 5 passed in 0.38s
rc=1
```

**Reading of the five green cases in the red run** — each is an *invariance* pin, green before the edit
because nothing has moved yet, and red if this slice breaks its subject:

- `test_shipped_stage_executor_preset_declares_no_hosting_capability` — the shipped leaf already carries
  no `sdd-invocation` key; asserted against the artifact, not against a convention (C-15).
- `test_the_hosting_criterion_fails_in_both_directions` — the C-16 criterion is *executed* over
  synthetic definitions (declaration-only fails, statements-only fails); it does not depend on the
  authoring baseline carrying the rule yet.
- `test_trigger_section_set_stays_the_delivered_closed_set` — the trigger document already has exactly
  its delivered 10 sections; the pin exists to go red when a section is added.
- `test_trigger_edit_moves_no_gate` — the scanner already reports the pre-change total (27); the pin
  exists to go red when the sentence adds a gate-scannable declaration.
- `test_every_shared_string_citation_resolves_to_a_registry_row` — all `[[STR-NNN]]` citations in the
  slice already resolve; the pin exists to catch a new dangling citation.

One in-passing test-defect repair, disclosed: the first red run of this suite reported 11 failures
because `_shared_string_ids()` looked the registry section up by *exact* title, while
`requirements.md`'s heading carries a parenthetical suffix (`## Shared Strings *(optional, …)*`). The
lookup was replaced by `_section_starting()` (prefix match, one hit) — a structural read instead of a
spelling test. `notes/red-first-evidence.md` keeps both numbers: 11 failed / 4 passed before the
repair, 10 failed / 5 passed after it. No implementation face was touched to produce the difference.

## E-5 · `tests/contract/test_sdd_diffusion.py` — GREEN (T011–T015 landed, T016)

**Captured**: 2026-10-29T06:3Z, after the five edits and the regeneration. The same 15 cases that ran in
E-4 are the ones that run here; no case was added, renamed or relaxed, and the 10 that were red are
now green.

```text
$ python3 -m pytest -q tests/contract/test_sdd_diffusion.py
...............                                                          [100%]
15 passed in 0.31s
rc=0
```

**E3 · targeted-set-v1 (part 2)** — the 19 baseline files plus the two suites this slice owns, run
**once** (no second full suite in this part; the full-suite slot belongs to implement start / review
closure). Full capture: `test-evidence/implement-targeted-part2-run.txt`.

```text
$ bash scripts/bash/run-tests.sh --names-out test-evidence/implement-targeted-part2-failed.txt \
    <the 19 files of test-evidence/targeted-set-v1-baseline.txt> \
    tests/contract/test_nested_run_report.py tests/contract/test_sdd_diffusion.py
collected 321 items
======================== 1 failed, 320 passed in 32.54s ========================
# failed-name list written: …/implement-targeted-part2-failed.txt (1 entries)
rc=1

$ cat test-evidence/implement-targeted-part2-failed.txt
tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged

$ comm -13 <(sort test-evidence/implement-targeted-part1-failed.txt) \
           <(sort test-evidence/implement-targeted-part2-failed.txt)
                       # empty → zero NEW failing node ids
```

**Reading**: the single failure is the same pre-existing red node id recorded in
`test-evidence/targeted-set-v1-baseline.txt` (gate total 27 vs the frozen 23, four earlier features'
declarations, not this slice's to repair), and the name-level comparison is empty in the
new-failures direction. Collected count moved 290 → 321 exactly by the two suites this slice owns
(16 + 15 cases); no existing case disappeared.

**Two disclosures, both corrections repaired in passing** — neither changed a contract:

1. **Test-side lookup defect (E-4)**: `_shared_string_ids()` matched the registry heading exactly while
   it carries a parenthetical suffix; replaced by a prefix match. Affected only my own new suite and
   only its first red run (11 failed / 4 passed → 10 failed / 5 passed).
2. **Section position (T013)**: the routing section was first placed between `## Proactive Flow
   Trigger` and `## Fact, Correctness & Logic Checks (Input Sanity)`. Two delivered guards pin that
   exact adjacency (`tests/contract/test_proactive_trigger_section.py` C-3 / C-9 and
   `test_ask_record_repeat.py`), so the first placement turned them red. The section moved to the next
   free slot (after Input Sanity, before `## One Source Of Truth`); commit `e1ee11c35`. Both guards are
   green in the E3 run above.





### E-5b · supplementary targeted check — the template-reading suites (part 2)

**Why this run exists**: `templates/instructions-template.md` is read by ~28 contract suites, most of
them outside the 19-file targeted set. Part 1 already ran a supplementary set for the same reason
(`implement.jsonl` seq 3); part 2 does the same rather than trust that no neighbour reads the surface
it edits *on principle*, without verification.

**First supplementary run (before the two repairs below)**: `1189 collected / 1182 passed / 7 failed`.
Set-diff against `baseline-failed.txt` (`comm -13`) named **four** new failures:

```text
tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/SKILL.md->.specify/skills/internal/create-team/SKILL.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/references/conceptual-model.md->.specify/skills/internal/create-team/references/conceptual-model.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/run-agent/SKILL.md->.specify/skills/internal/run-agent/SKILL.md]
```

**Repair 1 — the section-count pin (disclosed, cross-feature)**. `test_a7_section_counts_…` pins the
template at exactly 29 top-level `## ` sections and the live file at 30; C-18 requires exactly one
additive `## ` section, so both counts move by one. The pin's own docstring documents the protocol
("Stale-pin update (2026-10-27): the Closed-Set Claims amendment adds one ambient section"), i.e. the
integer is a *counter of ambient sections*, and adding one is its recorded update path. Bumped
29 → 30 and 30 → 31 with a dated docstring line naming slice 074b. This is the only file this part
touches outside the delivery surface `feature-ref.md` § 2 declares, and it changes two integers plus
one comment line — no clause, no proposition, no scope.

**Repair 2 — the three drifted skill mirrors**. `skills/internal/{create-team/SKILL.md,
create-team/references/conceptual-model.md, run-agent/SKILL.md}` had stale `.specify/` projections
(the first is part 1's T005–T007 edit, which left the mirror for T021; the other two are part-2 edits).
Synced with `python3 scripts/python/sync-mirrors.py --write --only skills/internal` — the projection is
mechanical, one reading only (mirror := source). `sync-mirrors.py --check` is now clean on all six
pairs and `regen-command-copies.py --check` still reports `OK`.

**Second supplementary run (after both repairs)**: `1189 collected / 1186 passed / 3 failed`, and the
three remaining failures are all **pre-existing** members of the 21-name `baseline-failed.txt`
(`test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline`,
`test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc`,
`test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`). `comm -13` against the
baseline is **empty**. Capture: `test-evidence/implement-targeted-part2-supp-run.txt`, failing names
in `implement-targeted-part2-supp-failed.txt`, row: `implement.jsonl` seq 5.

## E-6 · `tests/contract/test_sdd_invocation_governance.py` — superset edit (T017, no red step by instruction)

**Why no red step**: `tasks.md` T017 places this row under the migration/regression exception — the
file guards behaviour `074a` already delivered (`sdd-route.py --action authorize`, whose absent-key
default is owned by `NEUTRAL_AGENT_METADATA_KEYS`), so there can be no red-first run: the behaviour
exists before the case does. The guard against a sham superset is the *pre-edit* run below plus the
rule that no existing case's proposition changes.

**Pre-edit run** (before any line of this edit, 2026-10-29):

```text
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
.................                                                        [100%]
17 passed in 0.24s
rc=0
```

**Post-edit run** (same command, after the six new cases landed):

```text
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
.......................                                                  [100%]
23 passed in 0.59s
rc=0
```

**Reading**: 23 = the 17 preserved cases + 6 new ones; `17 ⊂ 23` and all 17 keep their verdict, so the
edit is a superset in the direction C-1/C-2 require. The six added node ids:

```text
tests/contract/test_sdd_invocation_governance.py::test_c1_an_agent_definition_without_the_key_resolves_forbidden
tests/contract/test_sdd_invocation_governance.py::test_c1_a_seat_without_the_policy_entry_resolves_forbidden[block-seat_absent-absent-entry]
tests/contract/test_sdd_invocation_governance.py::test_c1_a_seat_without_the_policy_entry_resolves_forbidden[no-seats-seat_allowed-absent-map]
tests/contract/test_sdd_invocation_governance.py::test_c1_the_absent_recipient_cannot_receive_a_driver_naming_dispatch
tests/contract/test_sdd_invocation_governance.py::test_c2_an_absent_agent_key_changes_no_other_field_of_the_dispatch
tests/contract/test_sdd_invocation_governance.py::test_c2_an_absent_seat_key_changes_no_other_field_of_the_dispatch
```

**Non-vacuity of the C-2 cases** (measured, not assumed): the declared/absent pair differs by one
line of the same document at the same path, and the two records differ in exactly the declaring
source — `supplying.agent: declared → absent-key`, with `effective`, `failed_half` and `reason`
identical:

```text
diff fields: ['supplying']
supplying: {'agent': 'declared', 'seat': 'declared'} -> {'agent': 'absent-key', 'seat': 'declared'}
reason equal: True | failed_half: agent agent
effective: forbidden forbidden
```

Had any other field moved, the C-2 cases fail — which is the property they are written to hold.

## E-7 · `tests/contract/test_sdd_compat_containment.py` — RED (T019)

**Captured**: 2026-10-29, before the file existed. The red form for a not-yet-written suite is its
absence, so the capture is the failing lookup rather than a failing assertion:

```text
$ test -e tests/contract/test_sdd_compat_containment.py; echo "exists rc=$?"
exists rc=1

$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py
ERROR: file or directory not found: tests/contract/test_sdd_compat_containment.py
no tests ran in 0.01s
rc=4
```

**Reading**: rc=4 is pytest's "no such path", so no case of this suite could have run before it was
written — the red is the missing file, and the green below is therefore the first execution of every
case in it.

## E-8 · `tests/contract/test_sdd_compat_containment.py` — GREEN (T019 file landed, T020 run)

```text
$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py
...........                                                              [100%]
11 passed in 0.32s
rc=0
```

**T020's run** — the compatibility suite together with the file T017 extended, because the two files
together are what carry C-1…C-12:

```text
$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py tests/contract/test_sdd_invocation_governance.py
..................................                                       [100%]
34 passed in 0.85s
rc=0
```

**Non-vacuity of the six negative clauses** (measured, not assumed). Each clause is an *absence*, and
an absence assertion is worthless if its token set could never appear. Two checks, both executed:

1. The section reader is live — `_report_section()` returns `1612` characters of the actual
   `### Nested SDD Runs section` body (and the helper asserts a single heading and a non-empty body
   before any case uses it), so the absence checks are run against text, not against `""`.
2. Injecting the forbidden token into the extracted text flips the corresponding criterion:

```text
clean offenders: []
mutated 集成  : ['集成']
mutated 确认门: ['确认门']
C-8 on clean: []
C-8 mutated : ['Work Package']
C-9 U-token on clean: None
C-9 U-token mutated : <re.Match object; span=(1617, 1619), match='U3'>
C-12 target_ref on clean: True True
```

The tokens are also ordinary vocabulary elsewhere in the framework sources (`集成` in 18 files,
`确认门` in 17, `daemon` in 13, `scheduler` in 4, `自动上送` in 2), so their absence from this one
section is a property of the section rather than of an unreachable string list.

3. The C-10 gate case carries its own positive control: the scanner reports gates in
   `skills/internal/create-team/references/summary-mapping.md` and
   `shared/guidelines/task-complexity-rubric.md`, i.e. it does see these document families, while
   none of the slice's nine delivered paths is a gate source.
