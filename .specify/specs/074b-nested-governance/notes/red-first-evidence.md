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

<!-- E-5 block pasted below after the T016 green run -->



